"""Local-only MCP tools for deterministic clinical calculations.

This module performs calculations only. It does not provide diagnosis,
dosing, or treatment recommendations and makes no network requests.
"""

from __future__ import annotations

import math
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field, FiniteFloat

mcp = FastMCP(
    "clinical-calc-mcp",
    mask_error_details=True,
    strict_input_validation=True,
    instructions=(
        "Perform only the documented mathematical calculations. These tools are not "
        "a diagnostic or treatment-decision system. Always present calculated results "
        "with their units and clinical limitations; never infer that a result is suitable "
        "for a particular patient."
    ),
)


def _positive_finite(value: Any, name: str, unit: str) -> float:
    """Validate a positive, finite numeric value without accepting booleans."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ToolError(f"{name} must be a finite number greater than 0 {unit}.")
    try:
        number = float(value)
    except OverflowError as error:
        raise ToolError(f"{name} is too large for supported finite numeric precision.") from error
    if not math.isfinite(number):
        raise ToolError(f"{name} must be finite; NaN and infinity are not allowed.")
    if number <= 0:
        raise ToolError(f"{name} must be greater than 0 {unit}.")
    return number


def _rounded(value: float, name: str, places: int = 2) -> float:
    """Return a clean rounded finite result, or fail clearly on overflow."""
    if not math.isfinite(value):
        raise ToolError(
            f"The calculated {name} is outside the supported finite numeric range. "
            "Check the input values and units."
        )
    return round(value, places)


def _validate_drop_factor(value: Any) -> int:
    """Require a positive integer drop factor (not a bool or fractional value)."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ToolError(
            "drop_factor must be a positive whole number in gtt/mL (for example, 15)."
        )
    try:
        finite_value = math.isfinite(float(value))
    except OverflowError as error:
        raise ToolError(
            "drop_factor must be within the supported finite numeric range in gtt/mL."
        ) from error
    if not finite_value:
        raise ToolError(
            "drop_factor must be within the supported finite numeric range in gtt/mL."
        )
    return value


@mcp.tool
def parkland_formula(
    weight_kg: Annotated[
        FiniteFloat,
        Field(gt=0, description="Body weight in kilograms; must be greater than zero."),
    ],
    tbsa_percentage: Annotated[
        FiniteFloat,
        Field(
            gt=0,
            le=100,
            description="Total body surface area affected, as a percentage from >0 to 100.",
        ),
    ],
) -> dict[str, float | str]:
    """Calculate the classic Parkland-formula 24-hour crystalloid estimate.

    Parameters
    ----------
    weight_kg:
        Body weight in kilograms (kg), finite and greater than zero.
    tbsa_percentage:
        Burn size expressed as percent TBSA (%), greater than zero and at most 100.

    Returns
    -------
    dict[str, float | str]
        Formula, supplied inputs, estimated total volume (mL), the formula's
        first-eight-hour and remaining-sixteen-hour volumes (mL), and their
        corresponding constant average rates (mL/hr), rounded to two decimals.

    Notes
    -----
    This is a mathematical calculation using the classic formula
    ``4 mL × weight in kg × TBSA percentage``; it does not determine a patient's
    actual fluid requirement. The conventional first eight hours are measured from
    the time of burn, not hospital arrival. Fluid already administered after the
    burn must be accounted for clinically. Current burn-management protocols may
    differ. Do not use this result as a substitute for clinical assessment or as
    an independent treatment recommendation.
    """
    weight = _positive_finite(weight_kg, "weight_kg", "kg")
    tbsa = _positive_finite(tbsa_percentage, "tbsa_percentage", "%")
    if tbsa > 100:
        raise ToolError("tbsa_percentage must be greater than 0 and no more than 100%.")

    total = _rounded(4.0 * weight * tbsa, "24-hour volume")
    first_volume = _rounded(total / 2.0, "first 8-hour volume")
    first_rate = _rounded(first_volume / 8.0, "first 8-hour rate")
    remaining_volume = _rounded(total / 2.0, "remaining 16-hour volume")
    remaining_rate = _rounded(remaining_volume / 16.0, "remaining 16-hour rate")
    return {
        "formula": "4 mL × kg × %TBSA",
        "weight_kg": weight,
        "tbsa_percentage": tbsa,
        "total_24h_volume_ml": total,
        "first_8h_volume_ml": first_volume,
        "first_8h_rate_ml_hr": first_rate,
        "remaining_16h_volume_ml": remaining_volume,
        "remaining_16h_rate_ml_hr": remaining_rate,
        "clinical_notice": (
            "Classic-formula estimate only; not the patient's actual fluid requirement. "
            "The first 8 hours are conventionally measured from burn time. Account for "
            "fluid already given; current protocols may differ. Clinical assessment is required."
        ),
    }


@mcp.tool
def bsa_mosteller(
    weight_kg: Annotated[
        FiniteFloat,
        Field(gt=0, description="Body weight in kilograms; must be greater than zero."),
    ],
    height_cm: Annotated[
        FiniteFloat,
        Field(gt=0, description="Height in centimeters; must be greater than zero."),
    ],
) -> dict[str, float | str]:
    """Calculate body surface area by Mosteller and body mass index.

    Parameters
    ----------
    weight_kg:
        Body weight in kilograms (kg), finite and greater than zero.
    height_cm:
        Height in centimeters (cm), finite and greater than zero.

    Returns
    -------
    dict[str, float | str]
        Supplied inputs, converted height (m), BSA (m²), and BMI (kg/m²),
        rounded to two decimal places.

    Notes
    -----
    BSA = sqrt((height_cm × weight_kg) / 3600). BMI = weight_kg / height_m²,
    where height_m = height_cm / 100. This tool calculates values only; it does
    not provide BMI categories, diagnosis, dosing, or treatment recommendations.
    """
    weight = _positive_finite(weight_kg, "weight_kg", "kg")
    height = _positive_finite(height_cm, "height_cm", "cm")
    height_m = height / 100.0
    bsa_argument = (height * weight) / 3600.0
    height_squared = height_m * height_m
    if height_m <= 0 or height_squared <= 0:
        raise ToolError(
            "height_cm is too small to calculate reliably in finite floating-point precision."
        )
    if not math.isfinite(bsa_argument) or not math.isfinite(height_squared):
        raise ToolError(
            "The calculated BSA or BMI is outside the supported finite numeric range. "
            "Check the input values and units."
        )

    bsa = _rounded(math.sqrt(bsa_argument), "BSA")
    bmi = _rounded(weight / height_squared, "BMI")
    return {
        "weight_kg": weight,
        "height_cm": height,
        "height_m": _rounded(height_m, "height in meters"),
        "bsa_m2": bsa,
        "bmi": bmi,
        "clinical_notice": (
            "Mathematical values only; no BMI category, diagnosis, dose, or treatment "
            "recommendation."
        ),
    }


@mcp.tool
def drip_rate_calculator(
    volume_ml: Annotated[
        FiniteFloat,
        Field(gt=0, description="Fluid volume in milliliters; must be greater than zero."),
    ],
    time_hours: Annotated[
        FiniteFloat,
        Field(gt=0, description="Infusion duration in hours; must be greater than zero."),
    ],
    drop_factor: Annotated[
        int,
        Field(
            gt=0,
            description=(
                "Giving-set calibration in drops per milliliter (gtt/mL), positive whole number."
            ),
        ),
    ] = 15,
) -> dict[str, float | int | str]:
    """Calculate a volume/time rate and gravity drip rate.

    Parameters
    ----------
    volume_ml:
        Volume in milliliters (mL), finite and greater than zero.
    time_hours:
        Infusion duration in hours (hr), finite and greater than zero.
    drop_factor:
        Giving-set calibration in drops per milliliter (gtt/mL), positive whole
        number. Defaults to 15 gtt/mL. Use the calibration printed on the set.

    Returns
    -------
    dict[str, float | int | str]
        Pump-equivalent rate (mL/hr), exact gravity rate (gtt/min) rounded to
        two decimal places, and nearest-whole practical rate (gtt/min), rounded
        half up. The unrounded mathematical value is retained as a separate field.

    Notes
    -----
    The formulas are mL/hr = volume_ml / time_hours and
    gtt/min = (volume_ml × drop_factor) / (time_hours × 60). Rounding to a
    whole drop uses nearest-integer, ties-half-up rounding. A rounded rate is
    not necessarily clinically appropriate; verify equipment, orders, and
    applicable institutional protocol. This tool makes no treatment recommendation.
    """
    volume = _positive_finite(volume_ml, "volume_ml", "mL")
    duration = _positive_finite(time_hours, "time_hours", "hours")
    factor = _validate_drop_factor(drop_factor)

    rate_ml_hr = _rounded(volume / duration, "rate in mL/hr")
    exact_gtt = (volume * factor) / (duration * 60.0)
    rounded_gtt = _rounded(exact_gtt, "exact rate in gtt/min")
    if not math.isfinite(exact_gtt):
        raise ToolError(
            "The calculated gravity drip rate is outside the supported finite numeric range. "
            "Check the input values and units."
        )
    practical_gtt = math.floor(exact_gtt + 0.5)
    return {
        "volume_ml": volume,
        "time_hours": duration,
        "drop_factor_gtt_per_ml": factor,
        "rate_ml_hr": rate_ml_hr,
        "rate_gtt_min_exact": rounded_gtt,
        "rate_gtt_min_rounded": practical_gtt,
        "rounding_method": "nearest whole drop, ties rounded up (half up)",
        "clinical_notice": (
            "Mathematical rate only. The rounded value is not necessarily clinically "
            "appropriate; verify the prescribed order, equipment, and local protocol."
        ),
    }


def main() -> None:
    """Start the MCP server using FastMCP's default stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()

"""Tests for calculator results, input validation, and MCP exposure."""

import asyncio
import math

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from clinical_calc_mcp.server import (
    bsa_mosteller,
    drip_rate_calculator,
    mcp,
    parkland_formula,
    temperature_converter,
    vital_signs_summary,
    weight_converter,
)


@pytest.mark.parametrize(
    ("weight", "tbsa", "expected"),
    [
        (70, 20, (5600, 2800, 350, 2800, 175)),
        (1, 100, (400, 200, 25, 200, 12.5)),
        (0.1, 0.01, (0, 0, 0, 0, 0)),
    ],
)
def test_parkland_known_values(weight, tbsa, expected):
    result = parkland_formula(weight, tbsa)
    fields = (
        "total_24h_volume_ml",
        "first_8h_volume_ml",
        "first_8h_rate_ml_hr",
        "remaining_16h_volume_ml",
        "remaining_16h_rate_ml_hr",
    )
    assert tuple(result[field] for field in fields) == expected
    assert result["formula"] == "4 mL × kg × %TBSA"
    assert "from burn time" in result["clinical_notice"]


@pytest.mark.parametrize(
    ("weight", "height", "expected_bsa", "expected_bmi"),
    [(70, 175, 1.844, 22.857), (80, 180, 2.0, 24.691)],
)
def test_mosteller_bsa_and_bmi(weight, height, expected_bsa, expected_bmi):
    result = bsa_mosteller(weight, height)
    assert math.isclose(result["bsa_m2"], round(expected_bsa, 2), abs_tol=0.01)
    assert math.isclose(result["bmi"], round(expected_bmi, 2), abs_tol=0.01)
    assert result["height_m"] == height / 100
    assert "category" not in result


def test_vital_signs_summary_known_values_and_no_interpretation():
    result = vital_signs_summary(80, 120, 80)
    assert result["pulse_pressure_mmhg"] == 40
    assert result["estimated_map_mmhg"] == 93.33
    assert result["shock_index"] == 0.67
    assert "no thresholds or interpretation" in result["clinical_notice"]


@pytest.mark.parametrize("bad", [0, -1, float("nan"), float("inf")])
def test_vital_signs_summary_rejects_invalid_numeric_inputs(bad):
    with pytest.raises(ToolError):
        vital_signs_summary(bad, 120, 80)
    with pytest.raises(ToolError):
        vital_signs_summary(80, bad, 80)
    with pytest.raises(ToolError):
        vital_signs_summary(80, 120, bad)


def test_vital_signs_summary_rejects_reversed_pressures_and_extreme_overflow():
    with pytest.raises(ToolError, match="systolic_bp_mmhg must be greater"):
        vital_signs_summary(80, 70, 80)
    with pytest.raises(ToolError, match="finite numeric range"):
        vital_signs_summary(1.0e308, 1.0e-308, 1.0e-309)


@pytest.mark.parametrize(
    ("value", "unit", "expected_unit", "expected"),
    [(37, "C", "F", 98.6), (98.6, "F", "C", 37.0), (0, "C", "F", 32.0)],
)
def test_temperature_conversions(value, unit, expected_unit, expected):
    result = temperature_converter(value, unit)
    assert result["converted_temperature"] == pytest.approx(expected)
    assert result["to_unit"] == expected_unit


@pytest.mark.parametrize("value,unit", [(-273.16, "C"), (-459.68, "F")])
def test_temperature_converter_rejects_below_absolute_zero(value, unit):
    with pytest.raises(ToolError, match="absolute zero"):
        temperature_converter(value, unit)


def test_temperature_converter_rejects_invalid_values_and_overflow():
    with pytest.raises(ToolError, match="finite number"):
        temperature_converter(True, "C")
    with pytest.raises(ToolError, match="finite numeric range"):
        temperature_converter(1.0e308, "C")
    with pytest.raises(ToolError, match="either 'C' or 'F'"):
        temperature_converter(37, "K")
    assert temperature_converter(-273.15, "C")["converted_temperature"] == -459.67


@pytest.mark.parametrize(
    ("weight", "unit", "expected_unit", "expected"),
    [(70, "kg", "lb", 154.32), (154.3236, "lb", "kg", 70.0)],
)
def test_weight_conversions(weight, unit, expected_unit, expected):
    result = weight_converter(weight, unit)
    assert result["converted_weight"] == pytest.approx(expected, abs=0.01)
    assert result["to_unit"] == expected_unit


@pytest.mark.parametrize("bad", [0, -1, float("nan"), float("inf"), True])
def test_weight_converter_rejects_nonpositive_or_nonfinite_values(bad):
    with pytest.raises(ToolError):
        weight_converter(bad, "kg")


def test_weight_converter_rejects_unknown_units_and_overflow():
    with pytest.raises(ToolError, match="either 'kg' or 'lb'"):
        weight_converter(70, "stone")
    with pytest.raises(ToolError, match="finite numeric range"):
        weight_converter(1.0e308, "kg")


def test_drip_rate_known_values_and_rounding():
    result = drip_rate_calculator(1000, 8, 15)
    assert result["rate_ml_hr"] == 125.0
    assert result["rate_gtt_min_exact"] == 31.25
    assert result["rate_gtt_min_rounded"] == 31
    assert "half up" in result["rounding_method"]


def test_drip_rate_half_up_tie():
    result = drip_rate_calculator(1, 1, 30)
    assert result["rate_gtt_min_exact"] == 0.5
    assert result["rate_gtt_min_rounded"] == 1


@pytest.mark.parametrize("bad", [0, -1, float("nan"), float("inf"), float("-inf")])
def test_parkland_rejects_invalid_weight(bad):
    with pytest.raises(ToolError, match="weight_kg"):
        parkland_formula(bad, 20)


@pytest.mark.parametrize("bad", [0, -1, 100.01, float("nan"), float("inf")])
def test_parkland_rejects_invalid_tbsa(bad):
    with pytest.raises(ToolError, match="tbsa_percentage"):
        parkland_formula(70, bad)


@pytest.mark.parametrize("bad", [0, -1, float("nan"), float("inf")])
def test_bsa_rejects_invalid_weight_and_height(bad):
    with pytest.raises(ToolError, match="weight_kg"):
        bsa_mosteller(bad, 175)
    with pytest.raises(ToolError, match="height_cm"):
        bsa_mosteller(70, bad)


@pytest.mark.parametrize("bad", [0, -1, float("nan"), float("inf")])
def test_drip_rejects_invalid_volume_and_time(bad):
    with pytest.raises(ToolError, match="volume_ml"):
        drip_rate_calculator(bad, 8)
    with pytest.raises(ToolError, match="time_hours"):
        drip_rate_calculator(1000, bad)


@pytest.mark.parametrize("bad", [0, -1, 15.5, True, "15", 10**400])
def test_drip_rejects_invalid_drop_factor(bad):
    with pytest.raises(ToolError, match="drop_factor"):
        drip_rate_calculator(1000, 8, bad)


def test_booleans_are_not_accepted_as_numbers():
    with pytest.raises(ToolError, match="weight_kg"):
        parkland_formula(True, 20)
    with pytest.raises(ToolError, match="volume_ml"):
        drip_rate_calculator(True, 8)


def test_extreme_values_fail_cleanly_when_result_overflows():
    with pytest.raises(ToolError, match="finite numeric range"):
        parkland_formula(1.0e308, 100)
    with pytest.raises(ToolError, match="supported finite numeric precision"):
        parkland_formula(10**400, 20)


def test_mcp_tools_are_registered_and_callable_over_protocol():
    async def exercise_client():
        async with Client(mcp) as client:
            tools = await client.list_tools()
            assert {tool.name for tool in tools} == {
                "parkland_formula",
                "bsa_mosteller",
                "drip_rate_calculator",
                "vital_signs_summary",
                "temperature_converter",
                "weight_converter",
            }
            response = await client.call_tool(
                "drip_rate_calculator",
                {"volume_ml": 1000, "time_hours": 8, "drop_factor": 15},
            )
            assert response.structured_content["rate_gtt_min_rounded"] == 31
            with pytest.raises(ToolError, match="less than or equal to 100"):
                await client.call_tool(
                    "parkland_formula",
                    {"weight_kg": 70, "tbsa_percentage": 101},
                )
            with pytest.raises(ToolError):
                await client.call_tool(
                    "parkland_formula",
                    {"weight_kg": True, "tbsa_percentage": 20},
                )

    asyncio.run(exercise_client())

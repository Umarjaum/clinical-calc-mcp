"""Tests for calculator results, input validation, and MCP exposure."""

import asyncio
import math

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from clinical_calc_mcp.server import bsa_mosteller, drip_rate_calculator, mcp, parkland_formula


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

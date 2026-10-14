from dataclasses import replace

import pytest

from test_automation_prioritization.models import (
    TestCaseAssessment as Assessment,
)


@pytest.fixture
def valid_assessment():
    return Assessment(
        test_type="API",
        oracle="YES",
        repeatability="YES",
        access="YES",
        impact="HIGH",
        likelihood="ORDINARY",
        cadence="FREQUENT",
        distinct_coverage="YES",
        implementation_effort="LOW",
        maintenance="LOW",
    )


def test_valid_assessment_is_created(valid_assessment):
    assert valid_assessment.test_type == "API"
    assert valid_assessment.impact == "HIGH"


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("test_type", "PERFORMANCE"),
        ("oracle", "MAYBE"),
        ("repeatability", "SOMETIMES"),
        ("access", "TRUE"),
        ("impact", "CRITICAL"),
        ("likelihood", "CERTAIN"),
        ("cadence", "DAILY"),
        ("distinct_coverage", "PARTIALLY"),
        ("implementation_effort", "VERY_HIGH"),
        ("maintenance", "NONE"),
    ],
)
def test_invalid_values_are_rejected(
    valid_assessment,
    field,
    invalid_value,
):
    with pytest.raises(ValueError, match="Invalid value"):
        replace(
            valid_assessment,
            **{field: invalid_value},
        )


def test_unknown_is_allowed(valid_assessment):
    assessment = replace(
        valid_assessment,
        likelihood="UNKNOWN",
    )

    assert assessment.likelihood == "UNKNOWN"


def test_partial_feasibility_is_allowed(valid_assessment):
    assessment = replace(
        valid_assessment,
        oracle="PARTIALLY",
    )

    assert assessment.oracle == "PARTIALLY"


def test_assessment_is_immutable(valid_assessment):
    from dataclasses import FrozenInstanceError

    with pytest.raises(FrozenInstanceError):
        valid_assessment.impact = "LOW"
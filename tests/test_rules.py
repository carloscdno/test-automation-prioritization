from dataclasses import replace

import pytest

from test_automation_prioritization.models import (
    TestCaseAssessment as Assessment,
)
from test_automation_prioritization.rules import evaluate


@pytest.fixture
def base_assessment():
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


@pytest.mark.parametrize(
    "changes, expected_verdict, expected_rule",
    [
        ({}, "HIGH_PRIORITY", "R6"),
        (
            {"distinct_coverage": "NO"},
            "ALREADY_COVERED",
            "R1",
        ),
        (
            {"oracle": "NO"},
            "KEEP_MANUAL",
            "R2",
        ),
        (
            {"repeatability": "NO"},
            "KEEP_MANUAL",
            "R2",
        ),
        (
            {"access": "NO"},
            "NEEDS_INVESTIGATION",
            "R3",
        ),
        (
            {"distinct_coverage": "UNKNOWN"},
            "NEEDS_INVESTIGATION",
            "R4",
        ),
        (
            {
                "impact": "LOW",
                "likelihood": "ORDINARY",
                "cadence": "ANNUAL",
            },
            "KEEP_MANUAL",
            "R5",
        ),
        (
            {"implementation_effort": "HIGH"},
            "CONSIDER",
            "R7",
        ),
    ],
)
def test_decision_rules(
    base_assessment,
    changes,
    expected_verdict,
    expected_rule,
):
    assessment = replace(base_assessment, **changes)

    result = evaluate(assessment)

    assert result.verdict == expected_verdict
    assert result.triggered_rule == expected_rule


def test_unknown_likelihood_changes_annual_decision(base_assessment):
    assessment = replace(
        base_assessment,
        impact="LOW",
        likelihood="UNKNOWN",
        cadence="ANNUAL",
    )

    result = evaluate(assessment)

    assert result.verdict == "NEEDS_INVESTIGATION"
    assert result.triggered_rule == "R8"
    assert "likelihood: UNKNOWN" in result.limitations


def test_unknown_likelihood_does_not_change_occasional_decision(
    base_assessment,
):
    assessment = replace(
        base_assessment,
        impact="LOW",
        likelihood="UNKNOWN",
        cadence="OCCASIONAL",
    )

    result = evaluate(assessment)

    assert result.verdict == "CONSIDER"
    assert result.triggered_rule == "R7"
    assert "likelihood: UNKNOWN" in result.limitations


def test_all_known_technical_blockers_are_reported(base_assessment):
    assessment = replace(
        base_assessment,
        oracle="NO",
        repeatability="NO",
        access="NO",
    )

    result = evaluate(assessment)

    assert result.verdict == "KEEP_MANUAL"
    assert "oracle: NO" in result.limitations
    assert "repeatability: NO" in result.limitations
    assert "access: NO" in result.limitations


def test_result_contains_explanation(base_assessment):
    result = evaluate(base_assessment)

    assert result.reason.strip()
    assert result.next_step.strip()
    assert result.supporting_factors


def test_multiple_blockers_and_unknowns(base_assessment):
    assessment = replace(
        base_assessment,
        oracle="NO",
        repeatability="NO",
        access="NO",
        likelihood="UNKNOWN",
        maintenance="UNKNOWN",
    )

    result = evaluate(assessment)

    assert result.verdict == "KEEP_MANUAL"
    assert result.triggered_rule == "R2"

    assert "oracle: NO" in result.limitations
    assert "repeatability: NO" in result.limitations
    assert "access: NO" in result.limitations
    assert "likelihood: UNKNOWN" in result.limitations
    assert "maintenance: UNKNOWN" in result.limitations
    

def test_multiple_unknowns_can_change_verdict(base_assessment):
    assessment = replace(
        base_assessment,
        impact="UNKNOWN",
        likelihood="UNKNOWN",
        cadence="FREQUENT",
    )

    result = evaluate(assessment)

    assert result.verdict == "NEEDS_INVESTIGATION"
    assert result.triggered_rule == "R8"

    assert "impact: UNKNOWN" in result.limitations
    assert "likelihood: UNKNOWN" in result.limitations

    assert any(
        "Decision-critical fields:" in factor
        and "impact" in factor
        and "likelihood" in factor
        for factor in result.supporting_factors
    )


def test_multiple_unknowns_do_not_change_verdict(base_assessment):
    assessment = replace(
        base_assessment,
        impact="UNKNOWN",
        likelihood="UNKNOWN",
        cadence="OCCASIONAL",
    )

    result = evaluate(assessment)

    assert result.verdict == "CONSIDER"
    assert result.triggered_rule == "R7"

    assert "impact: UNKNOWN" in result.limitations
    assert "likelihood: UNKNOWN" in result.limitations


def test_existing_coverage_takes_precedence(base_assessment):
    assessment = replace(
        base_assessment,
        distinct_coverage="NO",
        oracle="NO",
        repeatability="NO",
        access="NO",
        impact="UNKNOWN",
    )

    result = evaluate(assessment)

    assert result.verdict == "ALREADY_COVERED"
    assert result.triggered_rule == "R1"

    assert "oracle: NO" in result.limitations
    assert "repeatability: NO" in result.limitations
    assert "access: NO" in result.limitations
    assert "impact: UNKNOWN" in result.limitations


def test_known_technical_blocker_overrides_unknowns(base_assessment):
    assessment = replace(
        base_assessment,
        oracle="NO",
        impact="UNKNOWN",
        likelihood="UNKNOWN",
        maintenance="UNKNOWN",
    )

    result = evaluate(assessment)

    assert result.verdict == "KEEP_MANUAL"
    assert result.triggered_rule == "R2"
    assert "oracle: NO" in result.limitations
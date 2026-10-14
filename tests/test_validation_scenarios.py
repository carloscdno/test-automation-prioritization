import pytest

from test_automation_prioritization.models import (
    TestCaseAssessment as Assessment,
)
from test_automation_prioritization.rules import evaluate


@pytest.mark.parametrize(
    "case_id, data, expected_verdict, expected_rule",
    [
        (
            "C01",
            ("API", "YES", "YES", "YES", "HIGH", "ORDINARY",
             "FREQUENT", "YES", "LOW", "LOW"),
            "HIGH_PRIORITY", "R6",
        ),
        (
            "C02",
            ("UI", "YES", "YES", "YES", "HIGH", "ELEVATED",
             "FREQUENT", "YES", "MEDIUM", "MEDIUM"),
            "HIGH_PRIORITY", "R6",
        ),
        (
            "C03",
            ("UI", "YES", "YES", "YES", "LOW", "ORDINARY",
             "ANNUAL", "YES", "LOW", "LOW"),
            "KEEP_MANUAL", "R5",
        ),
        (
            "C04",
            ("UI", "NO", "YES", "YES", "MEDIUM", "ORDINARY",
             "PER_RELEASE", "YES", "MEDIUM", "HIGH"),
            "KEEP_MANUAL", "R2",
        ),
        (
            "C05",
            ("INTEGRATION", "YES", "NO", "YES", "HIGH",
             "ELEVATED", "FREQUENT", "YES", "HIGH", "HIGH"),
            "KEEP_MANUAL", "R2",
        ),
        (
            "C06",
            ("API", "YES", "YES", "YES", "MEDIUM", "ORDINARY",
             "FREQUENT", "NO", "LOW", "LOW"),
            "ALREADY_COVERED", "R1",
        ),
        (
            "C07",
            ("API", "YES", "YES", "NO", "HIGH", "ORDINARY",
             "FREQUENT", "YES", "MEDIUM", "MEDIUM"),
            "NEEDS_INVESTIGATION", "R3",
        ),
        (
            "C08",
            ("INTEGRATION", "YES", "YES", "YES", "HIGH",
             "ELEVATED", "FREQUENT", "YES", "HIGH", "HIGH"),
            "CONSIDER", "R7",
        ),
        (
            "C09",
            ("UI", "PARTIALLY", "YES", "YES", "MEDIUM",
             "ORDINARY", "PER_RELEASE", "YES", "MEDIUM", "MEDIUM"),
            "NEEDS_INVESTIGATION", "R3",
        ),
        (
            "C10",
            ("API", "YES", "YES", "YES", "LOW", "ELEVATED",
             "FREQUENT", "YES", "LOW", "LOW"),
            "CONSIDER", "R7",
        ),
        (
            "C11",
            ("INTEGRATION", "YES", "PARTIALLY", "YES", "HIGH",
             "ORDINARY", "FREQUENT", "UNKNOWN", "MEDIUM", "MEDIUM"),
            "NEEDS_INVESTIGATION", "R3",
        ),
        (
            "C12",
            ("API", "YES", "YES", "YES", "LOW", "UNKNOWN",
             "OCCASIONAL", "YES", "LOW", "LOW"),
            "CONSIDER", "R7",
        ),
        (
            "C13",
            ("INTEGRATION", "NO", "YES", "NO", "MEDIUM",
             "ORDINARY", "PER_RELEASE", "YES", "HIGH", "HIGH"),
            "KEEP_MANUAL", "R2",
        ),
        (
            "C14",
            ("UI", "YES", "YES", "YES", "MEDIUM", "ORDINARY",
             "PER_RELEASE", "YES", "LOW", "LOW"),
            "CONSIDER", "R7",
        ),
        (
            "C15",
            ("INTEGRATION", "YES", "YES", "YES", "HIGH",
             "ORDINARY", "FREQUENT", "YES", "HIGH", "MEDIUM"),
            "CONSIDER", "R7",
        ),
    ],
)
def test_validation_scenarios(
    case_id,
    data,
    expected_verdict,
    expected_rule,
):
    assessment = Assessment(*data)

    result = evaluate(assessment)

    assert result.verdict == expected_verdict, (
        f"{case_id}: expected {expected_verdict}, "
        f"got {result.verdict}"
    )

    assert result.triggered_rule == expected_rule, (
        f"{case_id}: expected {expected_rule}, "
        f"got {result.triggered_rule}"
    )

    assert result.reason.strip(), f"{case_id}: missing reason"
    assert result.next_step.strip(), f"{case_id}: missing next step"
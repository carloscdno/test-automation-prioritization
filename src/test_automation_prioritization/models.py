from dataclasses import dataclass, fields
from typing import Literal

TestType = Literal["UI", "API", "INTEGRATION"]

FeasibilityAnswer = Literal[
    "YES", "PARTIALLY", "NO", "UNKNOWN"
]

Impact = Literal["HIGH", "MEDIUM", "LOW", "UNKNOWN"]

Likelihood = Literal["ELEVATED", "ORDINARY", "UNKNOWN"]

Cadence = Literal[
    "FREQUENT",
    "PER_RELEASE",
    "OCCASIONAL",
    "ANNUAL",
    "UNKNOWN",
]

CoverageAnswer = Literal["YES", "NO", "UNKNOWN"]

EffortLevel = Literal["LOW", "MEDIUM", "HIGH", "UNKNOWN"]

Verdict = Literal[
    "HIGH_PRIORITY",
    "CONSIDER",
    "KEEP_MANUAL",
    "NEEDS_INVESTIGATION",
    "ALREADY_COVERED",
]


ALLOWED_VALUES = {
    "test_type": {"UI", "API", "INTEGRATION"},
    "oracle": {"YES", "PARTIALLY", "NO", "UNKNOWN"},
    "repeatability": {"YES", "PARTIALLY", "NO", "UNKNOWN"},
    "access": {"YES", "PARTIALLY", "NO", "UNKNOWN"},
    "impact": {"HIGH", "MEDIUM", "LOW", "UNKNOWN"},
    "likelihood": {"ELEVATED", "ORDINARY", "UNKNOWN"},
    "cadence": {
        "FREQUENT",
        "PER_RELEASE",
        "OCCASIONAL",
        "ANNUAL",
        "UNKNOWN",
    },
    "distinct_coverage": {"YES", "NO", "UNKNOWN"},
    "implementation_effort": {"LOW", "MEDIUM", "HIGH", "UNKNOWN"},
    "maintenance": {"LOW", "MEDIUM", "HIGH", "UNKNOWN"},
}


@dataclass(frozen=True)
class TestCaseAssessment:
    test_type: TestType
    oracle: FeasibilityAnswer
    repeatability: FeasibilityAnswer
    access: FeasibilityAnswer
    impact: Impact
    likelihood: Likelihood
    cadence: Cadence
    distinct_coverage: CoverageAnswer
    implementation_effort: EffortLevel
    maintenance: EffortLevel

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            allowed = ALLOWED_VALUES[field.name]

            if value not in allowed:
                raise ValueError(
                    f"Invalid value '{value}' for '{field.name}'. "
                    f"Allowed values: {', '.join(sorted(allowed))}"
                )


@dataclass(frozen=True)
class EvaluationResult:
    test_type: TestType
    verdict: Verdict
    triggered_rule: str
    reason: str
    supporting_factors: tuple[str, ...]
    next_step: str
    limitations: tuple[str, ...]
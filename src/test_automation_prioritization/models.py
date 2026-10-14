from dataclasses import dataclass
from typing import Literal

TestType = Literal["UI", "API", "INTEGRATION"]

FeasibilityAnswer = Literal["YES", "PARTIALLY", "NO", "UNKNOWN"]

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


@dataclass(frozen=True)
class EvaluationResult:
    test_type: TestType
    verdict: Verdict
    triggered_rule: str
    reason: str
    supporting_factors: tuple[str, ...]
    next_step: str
    limitations: tuple[str, ...]
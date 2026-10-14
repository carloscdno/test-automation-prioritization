from dataclasses import fields, replace
from itertools import product

from test_automation_prioritization.models import (
    EvaluationResult,
    TestCaseAssessment,
)

# Allowed values for decision-related unknown inputs.
POSSIBLE_VALUES = {
    "impact": ("LOW", "MEDIUM", "HIGH"),
    "likelihood": ("ORDINARY", "ELEVATED"),
    "cadence": ("ANNUAL", "OCCASIONAL", "PER_RELEASE", "FREQUENT"),
    "implementation_effort": ("LOW", "MEDIUM", "HIGH"),
    "maintenance": ("LOW", "MEDIUM", "HIGH"),
}

FEASIBILITY_FIELDS = ("oracle", "repeatability", "access")


def make_result(
    assessment: TestCaseAssessment,
    verdict: str,
    rule: str,
    reason: str,
    next_step: str,
    supporting_factors: tuple[str, ...] = (),
    limitations: tuple[str, ...] = (),
) -> EvaluationResult:
    """Build a consistent evaluation result."""
    return EvaluationResult(
        test_type=assessment.test_type,
        verdict=verdict,
        triggered_rule=rule,
        reason=reason,
        supporting_factors=supporting_factors,
        next_step=next_step,
        limitations=limitations,
    )


def collect_limitations(
    assessment: TestCaseAssessment,
) -> tuple[str, ...]:
    """Collect all known blockers and incomplete inputs."""
    limitations = []

    for field in fields(assessment):
        name = field.name
        value = getattr(assessment, name)

        if value in ("UNKNOWN", "PARTIALLY"):
            limitations.append(f"{name}: {value}")

        elif name in FEASIBILITY_FIELDS and value == "NO":
            limitations.append(f"{name}: NO")

    return tuple(limitations)


def evaluate_known_assessment(
    assessment: TestCaseAssessment,
) -> EvaluationResult:
    """
    Apply the ordered rules to an assessment whose
    decision-relevant qualitative inputs are known.

    The public evaluate() function should be used when
    UNKNOWN values may be present.
    """
    limitations = collect_limitations(assessment)

    # R1 — Existing automated coverage
    if assessment.distinct_coverage == "NO":
        return make_result(
            assessment,
            "ALREADY_COVERED",
            "R1",
            "Equivalent automated coverage already exists.",
            "Verify that the existing automated test covers "
            "the same behavior and failure conditions.",
            ("Existing automated coverage",),
            limitations,
        )

    # R2 — Unreliable automated verification
    blockers = []

    if assessment.oracle == "NO":
        blockers.append("No reliable automated test oracle")

    if assessment.repeatability == "NO":
        blockers.append("Test conditions are not repeatable")

    if blockers:
        return make_result(
            assessment,
            "KEEP_MANUAL",
            "R2",
            "The test cannot currently be automated reliably.",
            "Maintain appropriate manual validation and "
            "reevaluate after addressing the technical limitations.",
            tuple(blockers),
            limitations,
        )

    # R3 — Technical prerequisites
    unresolved = [
        name
        for name in FEASIBILITY_FIELDS
        if getattr(assessment, name) in ("PARTIALLY", "UNKNOWN")
        or (name == "access" and assessment.access == "NO")
    ]

    if unresolved:
        return make_result(
            assessment,
            "NEEDS_INVESTIGATION",
            "R3",
            "Technical feasibility has not been established.",
            "Investigate the unresolved technical prerequisites "
            "before prioritizing automation.",
            tuple(unresolved),
            limitations,
        )

    # R4 — Unknown automated coverage
    if assessment.distinct_coverage == "UNKNOWN":
        return make_result(
            assessment,
            "NEEDS_INVESTIGATION",
            "R4",
            "Existing automated coverage has not been verified.",
            "Review the current automation suite to identify "
            "potentially equivalent tests.",
            limitations=limitations,
        )

    # R5 — Low-value annual check
    if (
        assessment.impact == "LOW"
        and assessment.likelihood == "ORDINARY"
        and assessment.cadence == "ANNUAL"
    ):
        return make_result(
            assessment,
            "KEEP_MANUAL",
            "R5",
            "The test has low business impact, no evidence of "
            "elevated failure likelihood, and annual execution.",
            "Keep manual validation when appropriate and "
            "reevaluate if the test's value or cadence changes.",
            ("Low impact", "Annual execution"),
            limitations,
        )

    # R6 — Strong automation candidate
    sufficient_value = (
        assessment.impact == "HIGH"
        or (
            assessment.impact == "MEDIUM"
            and assessment.likelihood == "ELEVATED"
        )
    )

    manageable_effort = assessment.implementation_effort in (
        "LOW",
        "MEDIUM",
    )

    manageable_maintenance = assessment.maintenance in (
        "LOW",
        "MEDIUM",
    )

    if (
        assessment.cadence == "FREQUENT"
        and sufficient_value
        and manageable_effort
        and manageable_maintenance
    ):
        return make_result(
            assessment,
            "HIGH_PRIORITY",
            "R6",
            "The test provides significant recurring value "
            "and has manageable automation costs.",
            "Prioritize this candidate for automation planning.",
            (
                "Frequent execution",
                "Significant testing value",
                "Manageable implementation and maintenance",
            ),
            limitations,
        )

    # R7 — Remaining feasible candidates
    return make_result(
        assessment,
        "CONSIDER",
        "R7",
        "The test appears technically feasible, but its value "
        "or implementation trade-offs do not establish high priority.",
        "Review its expected benefits, implementation effort, "
        "and maintenance requirements before scheduling automation.",
        (
            f"Cadence: {assessment.cadence}",
            f"Impact: {assessment.impact}",
            f"Implementation effort: {assessment.implementation_effort}",
            f"Maintenance: {assessment.maintenance}",
        ),
        limitations,
    )


def get_unknown_fields(
    assessment: TestCaseAssessment,
) -> tuple[str, ...]:
    """Find unknown fields relevant to qualitative prioritization."""
    return tuple(
        name
        for name in POSSIBLE_VALUES
        if getattr(assessment, name) == "UNKNOWN"
    )


def generate_completions(
    assessment: TestCaseAssessment,
):
    """Generate every allowed completion of decision-related unknowns."""
    unknown_fields = get_unknown_fields(assessment)

    if not unknown_fields:
        yield assessment
        return

    choices = [POSSIBLE_VALUES[name] for name in unknown_fields]

    for values in product(*choices):
        replacements = dict(zip(unknown_fields, values))

        yield replace(assessment, **replacements)


def evaluate(
    assessment: TestCaseAssessment,
) -> EvaluationResult:
    """
    Evaluate one test case using the documented decision policy.

    Unknown qualitative values only block the recommendation
    when their possible resolutions would change the verdict.
    """
    initial_result = evaluate_known_assessment(assessment)

    # Explicit rules R1-R4 take precedence over uncertainty analysis.
    if initial_result.triggered_rule in ("R1", "R2", "R3", "R4"):
        return initial_result

    unknown_fields = get_unknown_fields(assessment)

    if not unknown_fields:
        return initial_result

    completed_results = [
        evaluate_known_assessment(completion)
        for completion in generate_completions(assessment)
    ]

    possible_verdicts = {result.verdict for result in completed_results}

    # All possible completions produce the same recommendation.
    if len(possible_verdicts) == 1:
        verdict = completed_results[0].verdict
        rule = completed_results[0].triggered_rule

        return make_result(
            assessment,
            verdict,
            rule,
            "The recommendation remains unchanged across all "
            "permitted resolutions of the unknown inputs.",
            "Review the listed unknowns when practical, but "
            "they do not currently change this recommendation.",
            (
                f"Stable recommendation: {verdict}",
                f"Unknown fields: {', '.join(unknown_fields)}",
            ),
            collect_limitations(assessment),
        )

    # Identify unknowns that can actually alter the verdict.
    critical_fields = []

    for name in unknown_fields:
        other_fields = [
            field for field in unknown_fields if field != name
        ]

        other_choices = [
            POSSIBLE_VALUES[field] for field in other_fields
        ]

        changes_outcome = False

        for other_values in product(*other_choices):
            fixed_values = dict(zip(other_fields, other_values))
            verdicts = set()

            for value in POSSIBLE_VALUES[name]:
                completed = replace(
                    assessment,
                    **fixed_values,
                    **{name: value},
                )

                verdicts.add(
                    evaluate_known_assessment(completed).verdict
                )

            if len(verdicts) > 1:
                changes_outcome = True
                break

        if changes_outcome:
            critical_fields.append(name)

    return make_result(
        assessment,
        "NEEDS_INVESTIGATION",
        "R8",
        "One or more unknown inputs could change the final "
        "automation recommendation.",
        "Clarify the decision-critical inputs before "
        "prioritizing this test for automation.",
        (
            f"Possible outcomes: {', '.join(sorted(possible_verdicts))}",
            f"Decision-critical fields: {', '.join(critical_fields)}",
        ),
        collect_limitations(assessment),
    )
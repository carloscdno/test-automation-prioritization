from textwrap import fill

import questionary

from test_automation_prioritization.models import TestCaseAssessment
from test_automation_prioritization.rules import evaluate

LINE_WIDTH = 100

FIELD_LABELS = {
    "oracle": "Automatic verification of expected results",
    "repeatability": "Ability to repeat the test reliably",
    "access": "Required tools, environments, and system access",
    "impact": "Business impact",
    "likelihood": "Likelihood of failure",
    "cadence": "Execution frequency",
    "distinct_coverage": "Existing automated test coverage",
    "implementation_effort": "Implementation effort",
    "maintenance": "Expected maintenance effort",
}

VALUE_LABELS = {
    "NO": "Not currently possible",
    "PARTIALLY": "Partially available or reliable",
    "UNKNOWN": "Not enough information",
    "LOW": "Low",
    "MEDIUM": "Medium",
    "HIGH": "High",
    "ORDINARY": "Ordinary",
    "ELEVATED": "Elevated",
    "FREQUENT": "Frequent",
    "PER_RELEASE": "Per release",
    "OCCASIONAL": "Occasional",
    "ANNUAL": "Annual",
}

FACTOR_LABELS = {
    "No reliable automated test oracle": (
        "The expected result cannot be verified reliably through automation"
    ),
    "Test conditions are not repeatable": (
        "The test cannot currently be repeated under controlled conditions"
    ),
    "Existing automated coverage": "An equivalent automated test already exists",
    "Frequent execution": "The test needs to run frequently",
    "Significant testing value": "The test provides significant testing value",
    "Manageable implementation and maintenance": (
        "The effort to build and maintain this test appears manageable"
    ),
    "Low impact": "A failure would have limited business impact",
    "Annual execution": "The test only needs to run about once a year",
}

# Used to avoid printing the same technical obstacle twice.
FACTOR_FIELDS = {
    "No reliable automated test oracle": "oracle",
    "Test conditions are not repeatable": "repeatability",
}


def show_header(title: str) -> None:
    questionary.print("=" * LINE_WIDTH, style="bold fg:darkblue")
    questionary.print(title, style="bold fg:yellow")
    questionary.print("=" * LINE_WIDTH, style="bold fg:darkblue")


def ask(question):
    """Stop the entire evaluation if the user cancels any question."""
    answer = question.ask()
    if answer is None:
        questionary.print("\nEvaluation cancelled by user.", style="fg:yellow")
        raise SystemExit(0)
    return answer


def show_intro() -> None:
    show_header("TEST AUTOMATION PRIORITIZATION")
    print(
        "Evaluate whether a functional UI, API, or integration test "
        "is a good candidate for automation."
    )
    print(
        "This tool considers technical feasibility, testing value, "
        "and automation effort."
    )
    print("\nPossible recommendations:")
    print("  HIGH_PRIORITY       A strong candidate to prioritize for automation.")
    print("  CONSIDER            A viable candidate with trade-offs to review.")
    print("  KEEP_MANUAL         Manual testing is more appropriate for now.")
    print("  NEEDS_INVESTIGATION More information or technical checks are needed.")
    print("  ALREADY_COVERED     Equivalent automated coverage already exists.")
    print("\nThese are recommendations, not mandatory decisions.\n")
    print("\nLet's get to it!\n")
    ask(questionary.press_any_key_to_continue())


def select_answer(message: str, options):
    choices = [
        questionary.Choice(title=label, value=value)
        for label, value in options
    ]
    return ask(questionary.select(message, choices=choices))


def ask_feasibility(message: str):
    return select_answer(
        message,
        [
            ("Yes - It can be done reliably", "YES"),
            ("Partially - Some limitations exist", "PARTIALLY"),
            ("No - Not currently possible", "NO"),
            ("I'm not sure", "UNKNOWN"),
        ],
    )


def ask_test_type():
    return select_answer(
        "What type of functional test are you evaluating?",
        [
            ("UI - User interface", "UI"),
            ("API - Application programming interface", "API"),
            ("Integration - Communication between systems", "INTEGRATION"),
        ],
    )


def ask_impact():
    return select_answer(
        "How serious would a failure in this functionality be?",
        [
            ("High - Critical operations or business impact", "HIGH"),
            ("Medium - Important functionality is affected", "MEDIUM"),
            ("Low - Minor inconvenience or limited impact", "LOW"),
            ("I'm not sure", "UNKNOWN"),
        ],
    )


def ask_likelihood():
    return select_answer(
        "What is the current likelihood of failure?",
        [
            (
                "Elevated - Recent defects, changes, or known instability",
                "ELEVATED",
            ),
            (
                "Ordinary - No evidence of increased failure risk",
                "ORDINARY",
            ),
            (
                "Unknown - Not enough information to assess",
                "UNKNOWN",
            ),
        ],
    )


def ask_cadence():
    return select_answer(
        "How often would this test need to be executed?",
        [
            ("Frequently - Daily, per commit, or similar", "FREQUENT"),
            ("Before each release", "PER_RELEASE"),
            ("Occasionally - Several times a year", "OCCASIONAL"),
            ("Annually - About once a year", "ANNUAL"),
            ("I'm not sure", "UNKNOWN"),
        ],
    )


def ask_existing_coverage():
    return select_answer(
        "Would this test check behavior not already covered by "
        "an equivalent automated test?",
        [
            ("Yes - It would add new automated coverage", "YES"),
            ("No - Equivalent automated coverage already exists", "NO"),
            ("I'm not sure", "UNKNOWN"),
        ],
    )


def ask_effort(message: str):
    return select_answer(
        message,
        [
            ("Low - Relatively straightforward", "LOW"),
            ("Medium - Moderate work or complexity", "MEDIUM"),
            ("High - Significant work or complexity", "HIGH"),
            ("I'm not sure", "UNKNOWN"),
        ],
    )


def collect_assessment() -> TestCaseAssessment:
    show_header("1. ABOUT YOUR TEST")
    test_type = ask_test_type()

    show_header("2. CAN THIS TEST BE AUTOMATED?")
    oracle = ask_feasibility(
        "Can the expected result be checked reliably through automation?"
    )
    repeatability = ask_feasibility(
        "Can this test run repeatedly under controlled conditions?"
    )
    access = ask_feasibility(
        "Are the necessary tools, environments, and system access available?"
    )

    show_header("3. HOW VALUABLE IS THIS TEST?")
    impact = ask_impact()
    likelihood = ask_likelihood()
    cadence = ask_cadence()
    distinct_coverage = ask_existing_coverage()

    show_header("4. AUTOMATION EFFORT")
    implementation_effort = ask_effort(
        "How difficult would it be to build this automated test?"
    )
    maintenance = ask_effort(
        "How much ongoing maintenance would this automated test require?"
    )

    return TestCaseAssessment(
        test_type=test_type,
        oracle=oracle,
        repeatability=repeatability,
        access=access,
        impact=impact,
        likelihood=likelihood,
        cadence=cadence,
        distinct_coverage=distinct_coverage,
        implementation_effort=implementation_effort,
        maintenance=maintenance,
    )


def format_limitation(limitation: str) -> str:
    field, separator, value = limitation.partition(": ")
    if not separator:
        return FIELD_LABELS.get(limitation, limitation)
    label = FIELD_LABELS.get(field, field.replace("_", " ").capitalize())
    friendly_value = VALUE_LABELS.get(value, value)
    return f"{label}: {friendly_value}"


def format_factor(factor: str) -> str:
    if factor in FACTOR_LABELS:
        return FACTOR_LABELS[factor]
    if factor in FIELD_LABELS:
        return FIELD_LABELS[factor]

    prefix, separator, value = factor.partition(": ")
    if separator and prefix in ("Cadence", "Impact", "Implementation effort", "Maintenance"):
        return f"{prefix}: {VALUE_LABELS.get(value, value)}"
    if separator and prefix in ("Unknown fields", "Decision-critical fields"):
        names = [name.strip() for name in value.split(",")]
        translated = ", ".join(FIELD_LABELS.get(name, name) for name in names)
        label = "Missing information" if prefix == "Unknown fields" else "Information that could change the decision"
        return f"{label}: {translated}"
    if separator and prefix == "Possible outcomes":
        return f"Possible recommendations: {value.replace('_', ' ').title()}"
    if separator and prefix == "Stable recommendation":
        return f"Recommendation is unchanged: {value.replace('_', ' ').title()}"
    return factor


def covered_fields_from_factors(factors: tuple[str, ...]) -> set[str]:
    covered = set()
    for factor in factors:
        if factor in FACTOR_FIELDS:
            covered.add(FACTOR_FIELDS[factor])
        elif factor in FIELD_LABELS:
            covered.add(factor)
        else:
            prefix, separator, value = factor.partition(": ")
            if separator and prefix in ("Unknown fields", "Decision-critical fields"):
                covered.update(part.strip() for part in value.split(","))
    return covered


def show_bullets(items) -> None:
    for item in items:
        print(fill(item, width=LINE_WIDTH, initial_indent="  - ", subsequent_indent="    "))


def show_result(result) -> None:
    print()
    show_header("AUTOMATION RECOMMENDATION")
    questionary.print(f"Verdict: {result.verdict}", style="bold fg:yellow")
    print(f"Test Type: {result.test_type}\n")

    print("Why this recommendation?")
    print(fill(result.reason, width=LINE_WIDTH))
    print()

    if result.supporting_factors:
        print("Key Factors:")
        show_bullets(format_factor(item) for item in result.supporting_factors)
        print()

    print("Recommended Next Step:")
    print(fill(result.next_step, width=LINE_WIDTH))
    print()

    covered = covered_fields_from_factors(result.supporting_factors)
    extra_limitations = [
        item
        for item in result.limitations
        if item.partition(": ")[0] not in covered
    ]
    if extra_limitations:
        print("Additional Limitations / Missing Information:")
        show_bullets(format_limitation(item) for item in extra_limitations)
        print()

    print(
        "This recommendation supports QA decision-making "
        "and does not replace engineering judgment."
    )


def main() -> None:
    show_intro()
    assessment = collect_assessment()
    result = evaluate(assessment)
    show_result(result)


if __name__ == "__main__":
    main()
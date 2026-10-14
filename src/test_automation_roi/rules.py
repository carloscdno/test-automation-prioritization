def evaluate_regression(regression_value, previous_bugs):
    """
    Evaluates whether the test provides regression-detection value.

    Returns:
        None if the evaluation should continue.
        A decision tuple (verdict, reason, recommendation) if it should stop.
    """
    if regression_value:
        return None

    if previous_bugs:
        return (
            "MANUAL",
            (
                "The test does not currently provide clear recurring "
                "regression-detection value, but previous bugs or incidents "
                "in this area justify continued manual validation."
            ),
            (
                "Execute the test manually and reevaluate it in the future "
                "if repeated manual execution shows that automation could "
                "reliably detect recurring regressions."
            ),
        )

    return (
        "DEFERRED",
        (
            "The test does not currently provide recurring regression-detection "
            "value and there is no previous defect history indicating a strong "
            "need for continued automation investment."
        ),
        (
            "Do not prioritize automation unless the test's frequency, risk, "
            "defect history, business relevance, or regression value changes."
        ),
    )


def evaluate_coverage(coverage):
    """
    Evaluates whether the test belongs to a feature-specific scope
    or an application-wide responsibility.

    Returns:
        None for FEATURE coverage.
        A decision tuple for APP coverage.
    """
    if coverage == "APP":
        return (
            "DEFERRED-APP",
            (
                "The test represents an application-wide or "
                "cross-cutting responsibility."
            ),
            (
                "Evaluate this test as part of a global test suite rather "
                "than as automation tied to a specific feature."
            ),
        )

    return None


def evaluate_automation_suitability(requires_human_judgment):
    """
    Evaluates whether the test requires human judgment that cannot
    be reliably replaced by automation.

    Returns:
        None if automation remains suitable.
        A MANUAL decision otherwise.
    """
    if requires_human_judgment:
        return (
            "MANUAL",
            (
                "Automation cannot reliably replace the human judgment "
                "required by this validation."
            ),
            (
                "Keep this test in the appropriate manual test suite "
                "and reevaluate it if its validation criteria become automatable."
            ),
        )

    return None


def calculate_base_roi(
    frequency,
    impact,
    stability,
    effort,
    dependencies,
):
    """
    Calculates the base automation ROI.

    Formula:
        (F * I * S) / (E * D)
    """
    if effort <= 0 or dependencies <= 0:
        raise ValueError(
            "Effort and dependencies must be greater than 0."
        )

    return (
        frequency
        * impact
        * stability
        / (effort * dependencies)
    )


def calculate_adjusted_roi(base_roi, reuse_count):
    """
    Adjusts the base ROI according to additional reuse opportunities.

    Formula:
        Base ROI * (1 + 0.2 * N)
    """
    if reuse_count < 0:
        raise ValueError(
            "Reuse count must be greater than or equal to 0."
        )

    return base_roi * (1 + 0.2 * reuse_count)


def evaluate_final_verdict(
    adjusted_roi,
    previous_bugs,
    critical_happy_path,
):
    """
    Determines the final verdict after ROI calculation.

    Thresholds:
        ROI > 3.0:
            CANDIDATE

        1.5 <= ROI <= 3.0:
            CANDIDATE if previous bugs exist
            MANUAL otherwise

        0.5 <= ROI < 1.5:
            MANUAL

        ROI < 0.5:
            DEFERRED

    A critical Happy Path promotes the test to CANDIDATE.
    """

    if critical_happy_path:
        return (
            "CANDIDATE",
            (
                "The test represents a critical business Happy Path. "
                "Critical business flows receive automation priority even "
                "when their calculated ROI would not normally reach the "
                "automation threshold."
            ),
            (
                "Add this test to the automation backlog and prioritize it "
                "according to business risk and available automation capacity."
            ),
        )

    if adjusted_roi > 3.0:
        return (
            "CANDIDATE",
            (
                "The adjusted ROI is above the automation threshold of 3.0, "
                "indicating strong recurring value for automation."
            ),
            (
                "Add this test to the automation backlog and prioritize it "
                "against other automation candidates."
            ),
        )

    if 1.5 <= adjusted_roi <= 3.0:
        if previous_bugs:
            return (
                "CANDIDATE",
                (
                    "The adjusted ROI is within the conditional automation "
                    "range and previous defects in this area increase the "
                    "value of automated regression coverage."
                ),
                (
                    "Consider this test an automation candidate and prioritize "
                    "it according to defect risk and available automation capacity."
                ),
            )

        return (
            "MANUAL",
            (
                "The adjusted ROI is within the conditional automation range, "
                "but there is no previous defect history providing additional "
                "justification for automation."
            ),
            (
                "Continue executing this test manually and reevaluate it if "
                "its frequency, defect history, reuse potential, or business "
                "risk increases."
            ),
        )

    if 0.5 <= adjusted_roi < 1.5:
        return (
            "MANUAL",
            (
                "The adjusted ROI indicates that automation currently provides "
                "limited value compared with its expected implementation and "
                "maintenance cost."
            ),
            (
                "Keep this test in the appropriate manual test suite and "
                "reevaluate it if its automation value increases."
            ),
        )

    return (
        "DEFERRED",
        (
            "The adjusted ROI is below the minimum automation threshold, "
            "indicating insufficient current value to justify automation."
        ),
        (
            "Do not prioritize automation at this time. Reevaluate the test "
            "if its execution frequency, business impact, stability, reuse "
            "potential, or risk changes."
        ),
    )
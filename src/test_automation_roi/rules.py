def evaluate_pre_filter_regression(regression, previous_bugs):
    if regression:
        return None
    
    if previous_bugs:
          return (
            "MANUAL",
            "The test does not currently provide clear recurring regression-detection value, but previous bugs or incidents in this area justify continued manual validation.",
            "Execute the test manually and reevaluate it in the future if repeated manual execution shows that automation could reliably detect recurring regressions."
        )
    return (
        "DEFERRED",
        "The test does not currently provide recurring regression-detection value and there is no previous defect history indicating a strong need for continued automation investment.",
        "Do not prioritize automation unless the test's frequency, risk, defect history, business relevance, or regression value changes."
    )


def evaluate_pre_filter_coverage(coverage):
    if coverage == "APP":
        return (
            "DEFERRED-APP",
            "The test represents an application-wide or cross-cutting responsibility.",
            "This should be evaluated as part of a global test suite rather than as automation tied to a specific feature.",
        )

    return None

def evaluate_pre_filter_suitability(requires_human_judgment):
    if requires_human_judgment:
        return (
            "MANUAL",
            "Automation cannot reliably replace the human judgment required by this validation.",
            "Include this test in a manual regression suite."
        )

    return None
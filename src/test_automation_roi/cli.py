from textwrap import fill

import questionary

from test_automation_roi.evaluator import (
    calculate_adjusted_roi,
    calculate_base_roi,
)
from test_automation_roi.rules import (
    evaluate_automation_suitability,
    evaluate_coverage,
    evaluate_final_verdict,
    evaluate_regression,
)
from test_automation_roi.validators import validate_non_negative_integer


def show_header(title):
    questionary.print(
        "=" * 136,
        style="bold fg:darkblue",
    )
    questionary.print(
        title,
        style="bold fg:yellow",
    )
    questionary.print(
        "=" * 136,
        style="bold fg:darkblue",
    )

def show_intro():
    show_header("TEST AUTOMATION EVALUATION")

    print(
        "This tool will help you determine if a test case "
        "is a good candidate to be automated."
    )
    print(
        "It uses predefined heuristic ROI thresholds "
        "to support automation prioritization."
    )
    print()

    print(
        """The final verdict could be one of the following options:
    - CANDIDATE: meaning 'Candidate for automation' and not necessarily 'must be automated'
    - MANUAL: in this case, manual execution is more appropriate
    - DEFERRED-APP: if you are evaluating a non-functional or application-wide responsibility
    - DEFERRED: automation would not provide value"""
    )

    print()
    questionary.press_any_key_to_continue().ask()
    print()


def show_prefilter_results(decision):
    show_header("AUTOMATION VERDICT")

    print(f"Verdict: {decision[0]}")
    print()

    print("Reason:")
    print(fill(decision[1], width=80))
    print()

    print("Recommendation:")
    print(fill(decision[2], width=80))


def show_final_results(
    coverage,
    frequency,
    impact,
    stability,
    effort,
    dependencies,
    base_roi,
    reuse,
    adjusted_roi,
    previous_bugs,
    critical_happy_path,
    decision,
):
    show_header("AUTOMATION VERDICT")

    print(f"Coverage Level: {coverage}")
    print()

    print("Factor Scores")
    print("-------------")
    print(f"Execution Frequency (F):   {frequency}")
    print(f"Business Impact (I):       {impact}")
    print(f"Flow Stability (S):        {stability}")
    print(f"Automation Effort (E):     {effort}")
    print(f"External Dependencies (D): {dependencies}")
    print()

    print(f"Base ROI:                   {base_roi:.2f}")
    print(f"Additional Reuse (N):       {reuse}")
    print(f"Adjusted ROI:               {adjusted_roi:.2f}")
    print()

    print(
        f"Previous Bug History:       "
        f"{'Yes' if previous_bugs else 'No'}"
    )
    print(
        f"Critical Happy Path:        "
        f"{'Yes' if critical_happy_path else 'No'}"
    )
    print()

    print(f"Final Verdict: {decision[0]}")
    print()

    print("Reason:")
    print(fill(decision[1], width=80))
    print()

    print("Recommendation:")
    print(fill(decision[2], width=80))


def ask_regression():
    return questionary.confirm(
        "Would this test provide value by detecting a future regression?"
    ).ask()


def ask_previous_bugs():
    return questionary.confirm(
        "Have there been previous bugs or incidents "
        "in this feature or functional area?"
    ).ask()


def ask_coverage():
    return questionary.select(
        "What is the coverage level of this test case?",
        choices=[
            questionary.Choice(
                title="Feature - Specific functional behavior",
                value="FEATURE",
            ),
            questionary.Choice(
                title="Application-wide - Cross-cutting or global responsibility",
                value="APP",
            ),
        ],
    ).ask()


def ask_automation_suitability():
    return questionary.confirm(
"""Does this test require visual inspection, subjective interpretation, 
or human judgment that cannot be evaluated reliably through automation?"""
    ).ask()


def ask_frequency():
    return questionary.select(
        "Select Frequency",
        choices=[
            questionary.Choice("1 - Yearly", value=1),
            questionary.Choice("2 - Per Release", value=2),
            questionary.Choice("3 - Per Sprint", value=3),
            questionary.Choice("4 - Daily", value=4),
            questionary.Choice("5 - PR/Commit", value=5),
        ],
    ).ask()


def ask_impact():
    return questionary.select(
        "Select Impact",
        choices=[
            questionary.Choice("1 - Cosmetic", value=1),
            questionary.Choice("2 - Minor", value=2),
            questionary.Choice("3 - UX Degradation", value=3),
            questionary.Choice("4 - Feature Blocking", value=4),
            questionary.Choice("5 - Core Business/Revenue", value=5),
        ],
    ).ask()


def ask_stability():
    return questionary.select(
        "Select Stability",
        choices=[
            questionary.Choice("1 - Highly Volatile", value=1),
            questionary.Choice("2 - Unstable", value=2),
            questionary.Choice("3 - Moderate", value=3),
            questionary.Choice("4 - Stable", value=4),
            questionary.Choice(
                "5 - Very Stable/No Expected Changes",
                value=5,
            ),
        ],
    ).ask()


def ask_effort():
    return questionary.select(
        "Select Effort",
        choices=[
            questionary.Choice("1 - Trivial", value=1),
            questionary.Choice("2 - Hours", value=2),
            questionary.Choice("3 - One or two days", value=3),
            questionary.Choice("4 - Several days", value=4),
            questionary.Choice("5 - One week or more", value=5),
        ],
    ).ask()


def ask_dependencies():
    return questionary.select(
        "Select Dependencies",
        choices=[
            questionary.Choice("1 - None", value=1),
            questionary.Choice(
                "2 - One or two dependencies",
                value=2,
            ),
            questionary.Choice(
                "3 - Three or four dependencies",
                value=3,
            ),
            questionary.Choice(
                "4 - Over five dependencies",
                value=4,
            ),
            questionary.Choice(
                "5 - Complex integrations",
                value=5,
            ),
        ],
    ).ask()


def ask_reuse_factor():
    reuse = questionary.text(
        "How many additional flows, scenarios, or components "
        "could reuse this automation?\n"
        "Enter 0 if there are no additional reuse opportunities.",
        validate=validate_non_negative_integer,
    ).ask()

    return int(reuse)


def ask_critical_happy_path():
    return questionary.confirm(
        "Does this test represent a critical business Happy Path?"
    ).ask()

def main():
    show_intro()
    
    show_header("1. PRE-FILTERS")
    regression_value = ask_regression()
    
    if not regression_value:
        previous_bugs = ask_previous_bugs()
        
        decision = evaluate_regression(
            regression_value, 
            previous_bugs
            )
        
        show_prefilter_results(decision)
        return
    
    coverage = ask_coverage()
    decision = evaluate_coverage(coverage)
    
    if decision:
        show_prefilter_results(decision)
        return
    
    automation_suitability = ask_automation_suitability()
    decision = evaluate_automation_suitability(automation_suitability)
    
    if decision:
        show_prefilter_results(decision)
        return
    
    previous_bugs = ask_previous_bugs()
        
    show_header("2. FACTOR SCORING")
    frequency = ask_frequency()
    impact = ask_impact()
    stability = ask_stability()
    effort = ask_effort()
    dependencies = ask_dependencies()
    
    show_header("3. REUSE FACTOR")
    reuse = ask_reuse_factor()
    
    show_header("4. CALCULATION & FINAL VERDICT")

    critical_happy_path = ask_critical_happy_path()

    base_roi = calculate_base_roi(
        frequency,
        impact,
        stability,
        effort,
        dependencies,
    )

    adjusted_roi = calculate_adjusted_roi(
        base_roi,
        reuse,
    )

    decision = evaluate_final_verdict(
        adjusted_roi,
        previous_bugs,
        critical_happy_path,
    )

    show_final_results(
        coverage=coverage,
        frequency=frequency,
        impact=impact,
        stability=stability,
        effort=effort,
        dependencies=dependencies,
        base_roi=base_roi,
        reuse=reuse,
        adjusted_roi=adjusted_roi,
        previous_bugs=previous_bugs,
        critical_happy_path=critical_happy_path,
        decision=decision,
    )
    
      
if __name__ == "__main__":
    main()
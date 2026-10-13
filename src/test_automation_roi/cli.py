import questionary

from test_automation_roi.validators import validate_non_negative_integer


def show_header(title):
    questionary.print("========================================================================================================================================", style="bold fg:darkblue")
    questionary.print(title, style="bold fg:yellow")
    questionary.print("========================================================================================================================================", style="bold fg:darkblue")

def show_intro():
    show_header("TEST AUTOMATION EVALUATION")
    print("This tool will help you determine if a test case is a good candidate to be automated.")
    print()
    print("""The final verdict could be one of the following options:
    - CANDIDATE: meaning 'Candidate for automation' and not necessarily 'must be automated'
    - MANUAL: in this case, manual execution is more appropriate
    - DEFERRED-APP: if you are evaluating a non-functional or application-wide responsibility
    - DEFERRED: automation would not provide value""")
    print()
    questionary.press_any_key_to_continue().ask()
    print()

def ask_coverage():
    coverage = questionary.select(
            "What is the coverage level of this test case?",
            choices=[
                questionary.Choice(
                title="Feature (Specific/Functional)",
            value="FEATURE"
            ),
            questionary.Choice(
            title="App (Large Scale/Non-functional)",
            value="APP"
            ),
            questionary.Choice(
            title="Unknown",
            value="UNKNOWN"
            ),
        ]   
    ).ask()
    return coverage

def ask_regression():
    protects_regression = questionary.confirm(
            "Does this test protect against a potential future regression?"
        ).ask()
    return protects_regression

def ask_previous_bugs():
    previous_bugs = questionary.confirm(
            "Have there been previous bugs or incidents in this feature or functional area?"
        ).ask()
    return previous_bugs

def ask_frequency():
    frequency = questionary.select(
                "Select Frequency",
                choices=[
                    questionary.Choice("1 - Yearly", value=1),
                    questionary.Choice("2 - Per Release", value=2),
                    questionary.Choice("3 - Per Sprint", value=3),
                    questionary.Choice("4 - Daily", value=4),
                    questionary.Choice("5 - PR/Commit", value=5),
                ]
            ).ask()
    return frequency

def ask_impact():
    impact = questionary.select(
                "Select Impact",
                choices=[
                    questionary.Choice("1 - Cosmetic", value=1),
                    questionary.Choice("2 - Minor", value=2),
                    questionary.Choice("3 - UX Degradation", value=3),
                    questionary.Choice("4 - Feature Blocking", value=4),
                    questionary.Choice("5 - Core Business/Revenue", value=5),
                ]
            ).ask()
    return impact

def ask_stability():
    stability = questionary.select(
                "Select Stability",
                choices=[
                    questionary.Choice("1 - Highly Volatile", value=1),
                    questionary.Choice("2 - Unstable", value=2),
                    questionary.Choice("3 - Moderate", value=3),
                    questionary.Choice("4 - Stable", value=4),
                    questionary.Choice("5 - Very Stable/No Expected Changes", value=5),
                ]
            ).ask()
    return stability

def ask_effort():
    effort = questionary.select(
                "Select Effort",
                choices=[
                    questionary.Choice("1 - Trivial", value=1),
                    questionary.Choice("2 - Hours", value=2),
                    questionary.Choice("3 - One or two days", value=3),
                    questionary.Choice("4 - Several days", value=4),
                    questionary.Choice("5 - One week or more", value=5),
                ]
            ).ask()
    return effort

def ask_dependencies():
    dependencies = questionary.select(
                "Select Dependencies",
                choices=[
                    questionary.Choice("1 - None", value=1),
                    questionary.Choice("2 - One or two dependencies", value=2),
                    questionary.Choice("3 - Three or four dependencies", value=3),
                    questionary.Choice("4 - Over five dependencies", value=4),
                    questionary.Choice("5 - Complex integrations", value=5),
                ]
            ).ask()
    return dependencies
    
def ask_reuse_factor():
    reuse = questionary.text(
"""How many additional flows, scenarios, or components could reuse this automation?
Enter 0 if there are no additional reuse opportunities.""",
        validate=validate_non_negative_integer).ask()
    return int(reuse)

def ask_human_judgment_and_critical_path():
    human = questionary.confirm(
"""Does this test require visual inspection, subjective interpretation, 
or human judgment that cannot be evaluated reliably through automation?"""
            ).ask()
        
    critical = questionary.confirm(
                    "Does this test represent a critical business Happy Path?"
                ).ask()
    return human, critical
     
def main():
    show_intro()
    
    show_header("1. PRE-FILTERS")
    coverage = ask_coverage()
    protects_regression = ask_regression()
    previous_bugs = ask_previous_bugs()
    
    show_header("2. FACTOR SCORING")
    frequency = ask_frequency()
    impact = ask_impact()
    stability = ask_stability()
    effort = ask_effort()
    dependencies = ask_dependencies()
    
    show_header("3. REUSE FACTOR")
    reuse = ask_reuse_factor()
    
    show_header("4. HUMAN JUDGMENT & CRITICAL HAPPY PATH")
    human_judgment, critical_happy_path = ask_human_judgment_and_critical_path()
            
if __name__ == "__main__":
    main()
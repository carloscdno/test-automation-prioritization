# Test Automation Prioritization CLI

A small, interactive Python tool that helps QA engineers decide whether **a single functional test case** is worth automating now.

Instead of estimating an arbitrary financial ROI or generating a numerical score, it provides a **qualitative recommendation** based on technical feasibility, testing value, existing coverage, and implementation/maintenance effort.

> This is a decision-support tool, not an official ISTQB decision algorithm or a substitute for engineering judgment.

## What it does

The CLI guides you through ten questions, organized into four sections:

1. **About your test:** UI, API, or integration.
2. **Can this test be automated?** Whether outcomes can be verified automatically, the test can run repeatedly, and the necessary tools and access exist.
3. **How valuable is this test?** Failure impact, evidence of elevated failure risk, execution frequency, and whether the proposed test adds coverage.
4. **Automation effort:** Expected implementation and ongoing maintenance effort.

The result includes a recommendation, an explanation, relevant factors and limitations, and a suggested next step.

## Possible recommendations

| Recommendation | Meaning |
| --- | --- |
| `HIGH_PRIORITY` | Strong candidate to prioritize for automation. |
| `CONSIDER` | Viable candidate, but its trade-offs should be reviewed. |
| `KEEP_MANUAL` | Manual validation is more appropriate for the test in its current form. |
| `NEEDS_INVESTIGATION` | Resolve missing information or technical prerequisites before deciding. |
| `ALREADY_COVERED` | Equivalent automated coverage already exists; avoid duplicating it. |

These labels describe **one proposed test**, not a ranking of an entire test suite.

## Requirements

- Python **3.12 or newer**.
- A terminal capable of interactive prompts.

## Installation

Clone the repository and open its root directory. Creating a virtual environment is recommended:

```bash
python -m venv .venv
```

Activate it:

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

Install the project in editable mode:

```bash
python -m pip install -e .
```

## Usage

Start the interactive evaluation:

```bash
test-automation-prioritization
```

Select an answer for each question. The CLI shows a recommendation and explains the reasoning. You can cancel an evaluation using `Ctrl+C`.

### Example: API authentication check

For a proposed authentication API test, suppose the outcome can be checked reliably, the test is repeatable, access is available, and the following conditions apply:

| Input | Answer |
| --- | --- |
| Test type | `API` |
| Automatic verification | `YES` |
| Repeatability | `YES` |
| Tools and access | `YES` |
| Failure impact | `HIGH` |
| Evidence of elevated failure risk | `ORDINARY` |
| Execution frequency | `FREQUENT` |
| Adds distinct automated coverage | `YES` |
| Implementation effort | `LOW` |
| Maintenance effort | `LOW` |

**Expected recommendation:** `HIGH_PRIORITY`.

Here, `ORDINARY` means there is *no specific evidence of elevated failure risk*; it does not mean failures are impossible.

## Testing

Run the test suite from the repository root:

```bash
python -m pytest -q
```

If pytest is not installed, install the project's development/test dependencies as configured in `pyproject.toml`, or install pytest in your virtual environment:

```bash
python -m pip install pytest
```

The suite covers input validation, the recommendation rules, reference scenarios, and the interactive CLI behavior using simulated user responses.

## How decisions are made

The rules engine applies explicit, ordered checks. Existing equivalent coverage is assessed before considering new automation. Technical feasibility, testing risk and value, execution frequency, and automation effort influence the remaining verdicts. Where an unknown answer might change the outcome, the tool recommends further investigation instead of pretending to have enough evidence.

The rules are **project-defined qualitative heuristics**, informed by software testing principles, not experimentally validated thresholds or a standardized scoring formula.

See [`docs/methodology.md`](docs/methodology.md) for the full input definitions, rule precedence, limitations, and references.

## Project structure

```text
src/test_automation_prioritization/
    cli.py          # User-facing prompts and output formatting
    models.py       # Input/output data models and validation
    rules.py        # Decision logic
    validators.py   # Validation helpers (if used)
tests/
    test_models.py
    test_rules.py
    test_validation_scenarios.py
    test_cli.py
docs/
    methodology.md
```

The CLI handles presentation, the models represent the data, and the rules engine makes the recommendation.

## Scope and limitations

- Evaluates **one functional UI, API, or integration test case at a time**.
- Does **not** generate or run automated tests.
- Does **not** calculate financial return on investment, assign numerical scores, or rank a portfolio of tests.
- Relies on the accuracy of the user's answers; incorrect assumptions can produce inappropriate recommendations.
- A `KEEP_MANUAL` verdict reflects present circumstances and can change if technical constraints are addressed.
- Human review remains necessary before making team or release decisions.
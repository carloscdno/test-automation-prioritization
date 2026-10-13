# Test Automation ROI Evaluation

The purpose of this evaluation is to determine whether a test case should be classified as:

- `CANDIDATE`
- `MANUAL`
- `DEFERRED-APP`
- `DEFERRED`

The evaluation consists of four phases:

1. Pre-Filters
2. Factor Scoring
3. ROI Calculation
4. Final Verdict and Exceptions

---

# 1. Pre-Filters

## 1.1 Coverage Level

Ask:

**What is the coverage level of this test case?**

Options:

- `FEATURE`
- `APP`
- `UNKNOWN`

### If the answer is `FEATURE`

Continue to **1.2 Regression Protection**.

### If the answer is `APP`

Stop the evaluation.

**Verdict: `DEFERRED-APP`**

Reason:

The test covers an application-wide or cross-cutting responsibility and should be handled by a global test suite rather than being automated as part of a specific feature.

### If the answer is `UNKNOWN`

Use the following scope classification rules.

---

## 1.1.1 Scope Classification — Feature vs. App

Ask:

**Does this test validate an explicit and specific Acceptance Criterion defined for this User Story or Feature?**

Options:

- Yes
- No

### If Yes

Classify the test as:

`FEATURE`

Continue to **1.2 Regression Protection**.

### If No

Ask:

**Does this test validate an application-wide quality standard, large-scale test, global scanner, or cross-cutting behavior?**

Examples may include:

- Application-wide accessibility checks
- Global security scans
- Large-scale performance/load testing
- Global compatibility checks
- Application-wide quality policies

Options:

- Yes
- No

### If Yes

Classify the test as:

`APP`

Stop the evaluation.

**Verdict: `DEFERRED-APP`**

### If No

Treat the test as:

`FEATURE`

for the purpose of this evaluation.

Continue to **1.2 Regression Protection**.

---

## 1.2 Regression Protection

Ask:

**Does this test protect against a potential future regression?**

Options:

- Yes
- No

### If Yes

Continue to:

**Phase 2 — Factor Scoring**

### If No

Evaluate previous defect history.

---

## 1.3 Previous Bug History

Ask:

**Have there been previous bugs or incidents in this feature or functional area?**

Options:

- Yes
- No

### If Regression Protection = No and Previous Bugs = Yes

Stop the evaluation.

**Verdict: `MANUAL`**

Reason:

The test does not currently demonstrate enough recurring regression-protection value to justify automation, but previous defects in this area justify continued manual validation.

Recommendation:

Execute the test manually.

If future manual executions demonstrate that the test could reliably prevent recurring regressions, perform a new automation evaluation.

### If Regression Protection = No and Previous Bugs = No

Stop the evaluation.

**Verdict: `DEFERRED`**

Reason:

There is currently insufficient evidence of recurring value to justify automating this test.

The test may be reevaluated if its frequency, risk, defect history, or business relevance changes.

---

# 2. Factor Scoring

If the test passes the pre-filters, score the following factors from `1` to `5`.

| Factor | Variable | Reference Scale |
|---|---:|---|
| Execution Frequency | `F` | 1 = Yearly, 2 = Per Release, 3 = Per Sprint, 4 = Daily, 5 = PR/Commit |
| Business Impact | `I` | 1 = Cosmetic, 2 = Minor, 3 = UX Degradation, 4 = Feature Blocking, 5 = Core Business/Revenue |
| Flow Stability | `S` | 1 = Highly Volatile, 2 = Unstable, 3 = Moderate, 4 = Stable, 5 = Very Stable/No Expected Changes |
| Automation Effort | `E` | 1 = Trivial, 2 = Hours, 3 = 1–2 Days, 4 = Several Days, 5 = One Week or More |
| External Dependencies | `D` | 1 = None, 2 = 1–2 Simple Dependencies, 3 = 3–4 Dependencies, 4 = 5+ Dependencies, 5 = Complex Integrations |

Each value must be an integer between `1` and `5`.

Values outside this range must be rejected.

---

# 3. ROI Calculation

## 3.1 Base ROI

Calculate:

```text
Base ROI = (F × I × S) / (E × D)
```

Where:

- `F` = Execution Frequency
- `I` = Business Impact
- `S` = Flow Stability
- `E` = Automation Effort
- `D` = External Dependencies

---

## 3.2 Reuse Factor

Ask the user:

**How many additional test flows, scenarios, or components could reuse code or infrastructure created by this automation?**

Enter:

`0` if there are no additional reuse opportunities.

Otherwise, enter the number of additional flows, scenarios, or components that could benefit from this automation.

Example:

```text
Additional reuse opportunities: 0
```

means that the automation is only useful for the current test.

```text
Additional reuse opportunities: 3
```

means that three additional test flows, scenarios, or components could reuse part of the automation.

---

## 3.2.1 Definition of `N`

`N` represents:

**The number of additional test flows, scenarios, or components that could reuse code or infrastructure created by the automation being evaluated.**

The current test itself is not included in `N`.

Therefore:

- `N = 0` → No additional reuse
- `N = 1` → One additional reuse opportunity
- `N = 2` → Two additional reuse opportunities
- `N = 5` → Five additional reuse opportunities

---

## 3.2.2 Validation Rules for `N`

`N` must:

- Be an integer
- Be equal to or greater than `0`

Negative values are not allowed.

Examples:

Valid:

```text
0
1
3
10
```

Invalid:

```text
-1
-5
2.5
abc
```

If the user enters an invalid value, the CLI should reject the input and ask again.

Suggested CLI prompt:

```text
How many additional flows, scenarios, or components could reuse this automation?

Enter 0 if there are no additional reuse opportunities.

> 
```

---

## 3.3 Reuse-Adjusted ROI

Calculate:

```text
Adjusted ROI = Base ROI × (1 + 0.2 × N)
```

Where:

`N` is the number of additional reuse opportunities.

### Example 1

Given:

```text
Base ROI = 2.50
N = 0
```

Then:

```text
Adjusted ROI = 2.50 × (1 + 0.2 × 0)
Adjusted ROI = 2.50
```

There is no reuse bonus.

### Example 2

Given:

```text
Base ROI = 2.50
N = 2
```

Then:

```text
Adjusted ROI = 2.50 × (1 + 0.2 × 2)
Adjusted ROI = 2.50 × 1.4
Adjusted ROI = 3.50
```

The reuse potential increases the automation value.

---

# 4. Final Verdict and Exceptions

Before applying the final ROI thresholds, evaluate two special conditions.

---

## 4.1 Human Judgment Requirement

Ask:

**Does this test require visual inspection, subjective interpretation, or human judgment that cannot be evaluated reliably through automation?**

Options:

- Yes
- No

Examples may include:

- Subjective visual quality
- Natural-looking animation
- Whether text "looks good"
- Human interpretation of usability
- Exploratory behavior
- Subjective audio or visual assessment

### If Yes

The test should not automatically become an automation candidate, even if its calculated ROI is high.

Default verdict:

**`MANUAL`**

Reason:

Automation cannot reliably replace the human judgment required by this validation.

This rule takes precedence over ROI-based classification.

---

## 4.2 Critical Happy Path

Ask:

**Does this test represent a critical business Happy Path?**

Options:

- Yes
- No

A critical Happy Path represents a core user journey whose failure could have significant business impact.

Examples may include:

- User login for a core application
- Checkout or payment
- Purchase completion
- Account creation
- Critical transaction processing
- Core product workflow

If the test is a critical Happy Path, it may be promoted to:

**`CANDIDATE`**

even when its ROI would normally result in `MANUAL` or `DEFERRED`.

However, this exception does not override the Human Judgment rule.

---

# 5. ROI Classification Rules

After calculating the Adjusted ROI, apply the following rules.

## Rule 1 — ROI Above 3.0

If:

```text
Adjusted ROI > 3.0
```

Verdict:

**`CANDIDATE`**

---

## Rule 2 — ROI Between 1.5 and 3.0

If:

```text
1.5 <= Adjusted ROI <= 3.0
```

and previous bugs exist:

**`CANDIDATE`**

If:

```text
1.5 <= Adjusted ROI <= 3.0
```

and no previous bugs exist:

**`MANUAL`**

---

## Rule 3 — ROI Between 0.5 and 1.5

If:

```text
0.5 <= Adjusted ROI < 1.5
```

Verdict:

**`MANUAL`**

---

## Rule 4 — ROI Below 0.5

If:

```text
Adjusted ROI < 0.5
```

Verdict:

**`DEFERRED`**

---

# 6. Critical Happy Path Exception

After determining the initial ROI-based verdict:

If:

```text
Critical Happy Path = Yes
```

and:

```text
Human Judgment Required = No
```

Promote the verdict to:

**`CANDIDATE`**

if it is currently:

- `MANUAL`
- `DEFERRED`

The final explanation should explicitly mention that the test was promoted because it protects a critical business Happy Path.

---

# 7. Rule Priority

To avoid conflicting decisions, rules should be evaluated in the following order:

1. Application-Level Scope
2. Regression Protection
3. Previous Bug History during Pre-Filtering
4. Human Judgment Requirement
5. Factor Scoring
6. ROI Calculation
7. ROI Classification
8. Critical Happy Path Exception
9. Final Verdict

---

# 8. Decision Summary

The overall decision flow can be summarized as follows:

```text
START
  |
  v
Determine Coverage Level
  |
  +--> APP
  |      |
  |      +--> DEFERRED-APP
  |
  +--> FEATURE
  |
  +--> UNKNOWN
         |
         v
      Resolve APP vs FEATURE
         |
         +--> APP --> DEFERRED-APP
         |
         +--> FEATURE
                  |
                  v
       Protects Against Regression?
                  |
          +-------+-------+
          |               |
         NO              YES
          |               |
          v               v
   Previous Bugs?     Factor Scoring
          |               |
      +---+---+           v
      |       |       Calculate Base ROI
     YES     NO            |
      |       |            v
   MANUAL  DEFERRED    Ask for N
                          |
                          v
                  Calculate Adjusted ROI
                          |
                          v
                 Human Judgment Required?
                          |
                    +-----+-----+
                    |           |
                   YES          NO
                    |           |
                 MANUAL         v
                         Apply ROI Rules
                                |
                                v
                     Critical Happy Path?
                                |
                        +-------+-------+
                        |               |
                       YES              NO
                        |               |
                 Promote Candidate   Keep Verdict
                        |               |
                        +-------+-------+
                                |
                                v
                           FINAL RESULT
```

---

# 9. Final Verdicts

## `CANDIDATE`

The test provides sufficient value to be considered for automation.

This does not necessarily mean it should be automated immediately.

It means the test should be considered for inclusion in the automation backlog and prioritized against other candidates.

## `MANUAL`

The test still provides testing value, but manual execution is currently more appropriate.

The test may be reevaluated in the future.

## `DEFERRED-APP`

The test represents an application-wide or cross-cutting responsibility.

It should be evaluated as part of a global testing strategy or global automation suite rather than as automation tied to a specific feature.

## `DEFERRED`

The current value of automating the test is insufficient.

The test should not be prioritized unless its frequency, risk, defect history, business relevance, or reuse potential changes.

---

# 10. Evaluation Output

The CLI should not return only the verdict.

Whenever the evaluation reaches the ROI calculation phase, the final result should ideally include:

- Coverage Level
- Execution Frequency (`F`)
- Business Impact (`I`)
- Flow Stability (`S`)
- Automation Effort (`E`)
- External Dependencies (`D`)
- Base ROI
- Additional Reuse Opportunities (`N`)
- Adjusted ROI
- Previous Bug History
- Critical Happy Path
- Human Judgment Requirement
- Final Verdict
- Verdict Reason
- Recommendation

Example:

```text
Test Automation ROI Evaluation
==============================

Coverage Level: FEATURE

Scores
------
Execution Frequency:    4
Business Impact:        5
Flow Stability:         4
Automation Effort:      3
External Dependencies:  2

Base ROI:                6.67

Additional Reuse Opportunities: 2
Adjusted ROI:            9.33

Previous Bugs:           Yes
Critical Happy Path:     No
Human Judgment Required: No

Verdict: CANDIDATE

Reason:
The adjusted ROI is above the automation threshold.

Recommendation:
Add this test to the automation backlog and prioritize it
against other automation candidates.
```

For evaluations terminated during the Pre-Filter phase, ROI values do not need to be calculated or displayed.

Example:

```text
Test Automation ROI Evaluation
==============================

Coverage Level: APP

Verdict: DEFERRED-APP

Reason:
This test represents an application-wide responsibility
and should be handled by a global test suite.

ROI calculation was not required.
```

---

# 11. Important Interpretation

`CANDIDATE` should be interpreted as:

**Candidate for automation**

rather than:

**Must be automated**

The tool provides decision support.

It does not replace engineering judgment, team priorities, available automation capacity, technical feasibility, or broader test strategy decisions.
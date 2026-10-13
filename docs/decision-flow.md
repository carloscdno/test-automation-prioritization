# Test Automation ROI Evaluation Flow

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

The purpose of the pre-filter phase is to stop the evaluation early when there is not enough value or feasibility to justify ROI scoring.

## 1.1 Regression Value

Ask:

**Would this test provide value by detecting a future regression?**

Options:

- Yes
- No

### If Yes

Continue to **1.2 Coverage Level**.

### If No

Ask:

**Have there been previous bugs or incidents in this feature or functional area?**

#### If Yes

Stop the evaluation.

**Verdict: `MANUAL`**

Reason:

The test does not currently provide clear recurring regression-detection value, but previous bugs or incidents in this area justify continued manual validation.

Recommendation:

Execute the test manually and reevaluate it in the future if repeated manual execution shows that automation could reliably detect recurring regressions.

#### If No

Stop the evaluation.

**Verdict: `DEFERRED`**

Reason:

The test does not currently provide recurring regression-detection value and there is no previous defect history indicating a strong need for continued automation investment.

Recommendation:

Do not prioritize automation unless the test's frequency, risk, defect history, business relevance, or regression value changes.

---

## 1.2 Coverage Level

Ask:

**What is the coverage level of this test case?**

Options:

- `FEATURE` — Specific functional behavior
- `APP` — Application-wide, cross-cutting, global, or large-scale responsibility

### If `FEATURE`

Continue to **1.3 Automation Suitability**.

### If `APP`

Stop the evaluation.

**Verdict: `DEFERRED-APP`**

Reason:

The test represents an application-wide or cross-cutting responsibility and should be evaluated as part of a global test suite rather than as automation tied to a specific feature.

Examples may include:

- Application-wide accessibility checks
- Global security scans
- Large-scale performance or load testing
- Global compatibility checks
- Cross-cutting application quality policies

---

## 1.3 Automation Suitability

Ask:

**Does this test require visual inspection, subjective interpretation, or human judgment that cannot be evaluated reliably through automation?**

Options:

- Yes
- No

### If Yes

Stop the evaluation.

**Verdict: `MANUAL`**

Reason:

Automation cannot reliably replace the human judgment required by this validation.

Examples may include:

- Subjective visual quality
- Whether an animation feels natural
- Whether content looks visually balanced
- Exploratory testing
- Human interpretation of usability
- Subjective audio or visual assessment

### If No

Continue to **1.4 Previous Bug History**.

---

## 1.4 Previous Bug History

Ask:

**Have there been previous bugs or incidents in this feature or functional area?**

Options:

- Yes
- No

Store the answer for later use during the final verdict calculation.

This answer does not stop the evaluation at this point.

Continue to:

**Phase 2 — Factor Scoring**

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

`Base ROI = (F × I × S) / (E × D)`

Where:

- `F` = Execution Frequency
- `I` = Business Impact
- `S` = Flow Stability
- `E` = Automation Effort
- `D` = External Dependencies

---

## 3.2 Reuse Factor

Ask:

**How many additional test flows, scenarios, or components could reuse code or infrastructure created by this automation?**

Enter:

`0` if there are no additional reuse opportunities.

Otherwise, enter the number of additional flows, scenarios, or components that could benefit from this automation.

### Definition of `N`

`N` represents:

**The number of additional test flows, scenarios, or components that could reuse code or infrastructure created by the automation being evaluated.**

The current test itself is not included in `N`.

Examples:

- `N = 0` → No additional reuse
- `N = 1` → One additional reuse opportunity
- `N = 3` → Three additional reuse opportunities

### Validation Rules for `N`

`N` must:

- Be an integer
- Be equal to or greater than `0`

Negative values are not allowed.

Valid examples:

```text
0
1
3
10
```

Invalid examples:

```text
-1
-5
2.5
abc
```

---

## 3.3 Reuse-Adjusted ROI

Calculate:

`Adjusted ROI = Base ROI × (1 + 0.2 × N)`

Where:

- `Base ROI` is the result of the base ROI formula
- `N` is the number of additional reuse opportunities

Example:

```text
Base ROI = 2.50
N = 2

Adjusted ROI = 2.50 × (1 + 0.2 × 2)
Adjusted ROI = 2.50 × 1.4
Adjusted ROI = 3.50
```

---

# 4. Final Verdict and Exceptions

## 4.1 Critical Happy Path

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

The Human Judgment restriction has already been handled during the pre-filter phase, so only tests that are technically suitable for automation reach this step.

---


## 4.2 Automation Thresholds

The ROI thresholds used by this tool are predefined heuristic decision thresholds used to classify automation value consistently.

The current thresholds are:

- `Adjusted ROI > 3.0` → Strong automation candidate
- `1.5 <= Adjusted ROI <= 3.0` → Conditional automation candidate
- `0.5 <= Adjusted ROI < 1.5` → Manual execution preferred
- `Adjusted ROI < 0.5` → Automation should be deferred

The main automation threshold is:

`Adjusted ROI > 3.0`

A result above this value is considered sufficient, by default, to classify the test as `CANDIDATE`.

Results between `1.5` and `3.0` require additional context, such as previous defect history, before being promoted to `CANDIDATE`.

> **Important:** These thresholds are heuristic rules defined for this tool. They are not universal industry standards. They are intended to provide consistency in automation prioritization and may be recalibrated in the future using historical defect data, automation effort, maintenance cost, execution frequency, or business priorities.


# 5. ROI Classification Rules

After calculating the Adjusted ROI, apply the following rules.

## Rule 1 — Adjusted ROI Above 3.0

If:

`Adjusted ROI > 3.0`

Verdict:

**`CANDIDATE`**

---

## Rule 2 — Adjusted ROI Between 1.5 and 3.0

If:

`1.5 <= Adjusted ROI <= 3.0`

and:

Previous bugs exist

Then:

**`CANDIDATE`**

If:

`1.5 <= Adjusted ROI <= 3.0`

and:

No previous bugs exist

Then:

**`MANUAL`**

---

## Rule 3 — Adjusted ROI Between 0.5 and 1.5

If:

`0.5 <= Adjusted ROI < 1.5`

Verdict:

**`MANUAL`**

---

## Rule 4 — Adjusted ROI Below 0.5

If:

`Adjusted ROI < 0.5`

Verdict:

**`DEFERRED`**

---

# 6. Critical Happy Path Exception

After determining the initial ROI-based verdict:

If:

`Critical Happy Path = Yes`

promote the verdict to:

**`CANDIDATE`**

if it is currently:

- `MANUAL`
- `DEFERRED`

The final explanation should explicitly mention that the test was promoted because it protects a critical business Happy Path.

---

# 7. Rule Priority

To avoid conflicting decisions, rules should be evaluated in the following order:

1. Regression Value
2. Previous Bug History when Regression Value is `No`
3. Coverage Level
4. Automation Suitability / Human Judgment
5. Previous Bug History when Regression Value is `Yes`
6. Factor Scoring
7. Base ROI Calculation
8. Reuse Adjustment
9. ROI Classification
10. Critical Happy Path Exception
11. Final Verdict

---

# 8. Pre-Filter Decision Summary

```text
START
  |
  v
Would this test provide value
by detecting a future regression?
  |
  +---------------- NO ----------------+
  |                                    |
 YES                                   v
  |                             Previous bugs?
  |                                /       \
  |                              YES       NO
  |                               |         |
  |                            MANUAL    DEFERRED
  |                               |         |
  |                              STOP      STOP
  |
  v
Coverage Level?
  |
  +--------- APP ----------> DEFERRED-APP
  |                              |
FEATURE                          STOP
  |
  v
Requires human judgment
that cannot be reliably automated?
  |
  +--------- YES ----------> MANUAL
  |                           |
  NO                         STOP
  |
  v
Previous bugs?
  |
 YES / NO
  |
  v
Store answer
  |
  v
PHASE 2
Factor Scoring
```

---

# 9. Final Verdicts

## `CANDIDATE`

The test provides sufficient value to be considered for automation.

This does not necessarily mean it should be automated immediately.

It means the test should be considered for inclusion in the automation backlog and prioritized against other candidates.

---

## `MANUAL`

The test still provides testing value, but manual execution is currently more appropriate.

The test may be reevaluated in the future.

---

## `DEFERRED-APP`

The test represents an application-wide or cross-cutting responsibility.

It should be evaluated as part of a global testing strategy or global automation suite rather than as automation tied to a specific feature.

---

## `DEFERRED`

The current value of automating the test is insufficient.

The test should not be prioritized unless its frequency, risk, defect history, business relevance, or reuse potential changes.

---

# 10. Evaluation Output

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
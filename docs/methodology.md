# Test Automation Prioritization CLI — Methodology

## 1. Purpose and scope

Evaluate **one individual functional test case** per CLI session and issue an explainable recommendation about whether to prioritize its automation. Supported targets: **UI, API, and integration tests**. The tool does **not** calculate financial ROI, rank a portfolio of tests, automate tests, or evaluate specialized non-functional testing.

Its output is **decision support**, not a mandatory engineering decision.

## 2. Source-backed foundations

| Principle | Primary reference | What we take from it |
| --- | --- | --- |
| Automation suitability and viability | ISTQB CT-TAS v1.0, §3.3 | Technical feasibility, value of frequent execution, implementation challenges, and automation context should influence selection. |
| Automation costs and sustainability | ISTQB CT-TAS v1.0, chapters on costs, dependencies and maintenance | Initial implementation is not the only cost; environment and ongoing maintenance matter. |
| Product-risk considerations | ISTQB CTFL v4.0.1, product-risk and risk-based testing sections | Consider the likelihood and impact of failure, based on available evidence. |
| Avoid redundant and non-actionable tests | Angie Jones, *Which Tests Should We Automate?* | Distinctness, useful failure signals, history and cost help decide what deserves automation. |

**Important:** The questions, labels, precedence rules, and outputs below are **project design choices informed by these sources**, not an official ISTQB algorithm or certified prioritization scale.

## 3. Inputs (one case)

### A. Identification and technical feasibility

1. **Test type** — `UI` / `API` / `INTEGRATION` (context only; no category is automatically rejected).
2. **Reliable automated oracle** — *Can an automated check determine pass/fail reliably?* `YES` / `PARTIALLY` / `NO` / `UNKNOWN`.
3. **Repeatability** — *Can the scenario be reproduced with controllable test data and environment?* `YES` / `PARTIALLY` / `NO` / `UNKNOWN`.
4. **Access/tools** — *Are the necessary interfaces, tools and access available?* `YES` / `PARTIALLY` / `NO` / `UNKNOWN`.

### B. Risk and testing value

5. **Failure impact** — `HIGH` (core business transaction, major loss or outage) / `MEDIUM` (important behavior impaired; workaround possible) / `LOW` (minor user-facing consequence) / `UNKNOWN`.
6. **Failure likelihood evidence** — `ELEVATED` (recent changes, repeated failures or known fragility) / `ORDINARY` (no specific elevated signal) / `UNKNOWN`. **Ordinary does not mean proven low risk.**
7. **Useful execution cadence** — `FREQUENT` (per change, CI or daily) / `PER_RELEASE` / `OCCASIONAL` / `UNKNOWN`. This means the useful frequency of running the check, not the frequency of user activity.
8. **Distinct actionable coverage** — *Would failure provide useful, actionable information not already adequately covered by another automated test?* `YES` / `NO` / `UNKNOWN`.

### C. Cost and sustainability

9. **Implementation effort** — `LOW` / `MEDIUM` / `HIGH` / `UNKNOWN` (relative estimates given the team's existing automation capabilities; no time-to-score conversion).
10. **Expected maintenance burden** — `LOW` / `MEDIUM` / `HIGH` / `UNKNOWN` (flow changes, data setup, dependencies, environment stability).

Do **not** ask for additional reuse count `N` in v1. Reuse may influence a human decision but is deliberately omitted to keep the first model small and auditable.

## 4. Recommendation labels

- `HIGH_PRIORITY`: Strong, feasible candidate with a clear reason to automate soon.
- `CONSIDER`: Feasible candidate with mixed value/cost signals; compare against team priorities.
- `KEEP_MANUAL`: An automated check is presently unsuitable, non-actionable or redundant; retain manual coverage as appropriate.
- `NEEDS_INVESTIGATION`: A critical unknown or partial technical prerequisite should be researched before recommending automation.

No label means that a test may never be automated. `KEEP_MANUAL` is **not** an instruction to execute every test manually forever.

## 5. Proposed decision policy (project-defined; subject to validation)

Apply in the following order. Each recommendation includes the triggered rule and supplied evidence.

1. **Technical blockers**: If the oracle is `NO` or repeatability is `NO`, return `KEEP_MANUAL` with a specific reason. If tools/access are `NO`, return `NEEDS_INVESTIGATION` (blocked until access/tools change), not a false assertion that automation is intrinsically impossible.
2. **Uncertain feasibility**: If any feasibility answer is `PARTIALLY` or `UNKNOWN`, return `NEEDS_INVESTIGATION` and name the missing prerequisite. Do not convert uncertainty into a low score.
3. **Redundancy/actionability**: If distinct actionable coverage is `NO`, return `KEEP_MANUAL` *for this proposed new automation*, recommending review of existing coverage rather than duplication. If it is `UNKNOWN`, return `NEEDS_INVESTIGATION`.
4. **Uncertain decision-critical context**: If impact, likelihood, cadence, implementation effort, or maintenance burden is `UNKNOWN`, return `NEEDS_INVESTIGATION`, identifying the unknowns. (May be relaxed after validation if excessive.)
5. **Strong candidate**: When technically feasible and actionable, return `HIGH_PRIORITY` **only if** useful execution cadence is `FREQUENT`, failure impact is `HIGH` or likelihood is `ELEVATED`, **and** neither implementation effort nor maintenance burden is `HIGH`.
6. **Trade-off**: Otherwise return `CONSIDER` if feasible and actionable. Describe both positive and negative signals; do not imply that this is an ordinal score.

This is a **small, transparent baseline policy**. It is not claimed to be optimal. In particular, the cadence and high-priority rule are **design choices** that must be challenged through realistic scenarios before coding.

## 6. Output contract

Every completed run displays:

- Test type
- `Verdict` (`HIGH_PRIORITY`, `CONSIDER`, `KEEP_MANUAL`, or `NEEDS_INVESTIGATION`)
- `Reason` (specific rule and decisive input)
- `Supporting factors` (key positive and negative signals)
- `Recommendation / next step`
- `Limitations / unknowns` where relevant

No numeric score, ROI percentage, or financial savings figure is displayed.

## 7. Limitations

- The tool depends on the user's estimates and knowledge of current coverage.
- Qualitative categories are context-sensitive; they are not measured probabilities or financial amounts.
- The baseline rules may classify too many uncertain cases as `NEEDS_INVESTIGATION` and require refinement through validation.
- This model does not replace team planning or a formal test automation strategy.

## 8. References

1. ISTQB, *Certified Tester Test Automation Strategy (CT-TAS) Syllabus*, v1.0 (2024). https://istqb.org/wp-content/uploads/2024/11/ISTQB_CT-TAS_Syllabus_v1.0.pdf
2. ISTQB, *Certified Tester Foundation Level (CTFL)*, v4.0.1. https://www.istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/
3. Angie Jones, *Which Tests Should We Automate?* presentation. https://slides.com/angiejones/which-tests-should-we-automate
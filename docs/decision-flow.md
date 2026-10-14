# Test Automation Prioritization — Decision Flow v1.0

**Status:** Implementation baseline · **Scope:** One functional UI/API/integration test per run.

Read [methodology.md](methodology.md) for definitions, evidence and limitations. These recommendations are **project-defined heuristics** informed by literature, **not ISTQB-certified rules**.

## 1. Ask all inputs

- `test_type`: `UI / API / INTEGRATION` (context only)
- `oracle`, `repeatability`, `access`: `YES / PARTIALLY / NO / UNKNOWN`
- `impact`: `HIGH / MEDIUM / LOW / UNKNOWN`
- `likelihood`: `ELEVATED / ORDINARY / UNKNOWN`
- `cadence`: `FREQUENT / PER_RELEASE / OCCASIONAL / ANNUAL / UNKNOWN`
- `distinct_coverage`: `YES / NO / UNKNOWN`
- `implementation_effort`, `maintenance`: `LOW / MEDIUM / HIGH / UNKNOWN`

Prompt descriptions must clarify that `ORDINARY` does not mean a proven low defect probability; access `NO` means currently unavailable; `FREQUENT` is useful test execution, not traffic. Tests must have objective oracles to be reliably automated; missing technical prerequisites are tracked rather than ignored.

## 2. Decision order

1. `distinct_coverage == NO` → **ALREADY_COVERED**; verify existing automated coverage and do not duplicate it.
2. `oracle == NO or repeatability == NO` → **KEEP_MANUAL** for the current design; explain all known feasibility blockers and re-evaluation condition.
3. `oracle/repeatability/access in {PARTIALLY, UNKNOWN}` **or** `access == NO` → **NEEDS_INVESTIGATION**; identify the concrete dependency. (Previous rules take precedence.)
4. `distinct_coverage == UNKNOWN` → **NEEDS_INVESTIGATION**; establish whether automation already exists.
5. For context fields with `UNKNOWN`, enumerate possible allowed values and apply steps 6–8 below to each completion. If outcomes disagree → **NEEDS_INVESTIGATION**; if all outcomes agree → keep that result and report the unknowns.
6. If `impact == LOW and likelihood == ORDINARY and cadence == ANNUAL` → **KEEP_MANUAL** (low-value, occasional check).
7. If `cadence == FREQUENT and (impact == HIGH or (impact == MEDIUM and likelihood == ELEVATED)) and implementation_effort in {LOW, MEDIUM} and maintenance in {LOW, MEDIUM}` → **HIGH_PRIORITY**.
8. Otherwise → **CONSIDER**.

**Note:** In step 5, the possible-outcome evaluator only applies steps 6–8 for the risk/cost fields. Feasibility and coverage are evaluated by steps 1–4, not expanded into synthetic answers. If multiple unknowns are present, list all unknowns and flag those capable of changing the result.

## 3. Output for every verdict

Always show:

```text
Test Type: UI / API / INTEGRATION
Verdict: ...
Rule: ...
Reason: ...
Supporting Factors: ...
Limitations / Unknowns: ...
Recommended Next Step: ...
```

For simultaneous blockers, choose the first verdict by priority but **include all identified blockers**, not just the first one. Never imply `ALREADY_COVERED` means the user should execute the same test manually. No ROI calculations or numerical scoring.

## 4. Outcome patterns to test

| Pattern | Verdict |
| --- | --- |
| Reliable, nonredundant, frequent, high impact, reasonable build and maintenance | `HIGH_PRIORITY` |
| Annual + low impact + ordinary likelihood | `KEEP_MANUAL` |
| Subjective oracle that cannot be made reliable (`NO`) | `KEEP_MANUAL` |
| Missing integration credentials (`access=NO`) | `NEEDS_INVESTIGATION` |
| Existing adequate automated coverage (`distinct_coverage=NO`) | `ALREADY_COVERED` |
| High risk, but expensive or high maintenance | `CONSIDER` |
| Unknown likelihood that cannot change classification | Keep determined verdict; disclose limitation |
| Unknown input that can change result | `NEEDS_INVESTIGATION` |

## 5. Implementation notes

- `cli.py`: ask questions, handle cancel/empty responses, print result. No business decisions.
- `rules.py`: one pure `evaluate_case(inputs)` rule engine, plus pure helpers if useful. No `questionary`, `print`, or `input`.
- `models.py`: represent the nine answers + test type and structured `Decision` (verdict, rule, reason, factors, next step, limitations). Prefer named fields over tuple indexes.
- `validators.py`: validate declared categorical choices and cancellation as appropriate.
- No need for an `evaluator.py` calculation module, a database, or scoring thresholds in this version.
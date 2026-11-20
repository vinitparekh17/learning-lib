# F03 — Hints and worked answers

| Field | Value |
| --- | --- |
| ID and revision | F03 answers · 1.0 · 2026-11-03 |
| Prerequisite | [F03 learning pack](SDE_F03.md) |
| Capability | Audit a measurement claim and design a comparison that can answer it |
| Evidence | R03 and R13 locators are in the core pack. All data below are constructed. |
| Check status | Exact arithmetic executed on the included examples. The live experiment is a design exercise. |

## Hints

1. Ask which pipeline saw more exceptions. Compare both at one agreed mix.
2. Start with the cases on which the pipelines disagree.
3. Follow what the reviewer learns and which queues they share.
4. Include the cost of failed work in the numerator.
5. Decide what happens to an eligible record when its final label is missing.
6. Follow a debugging task from issue intake to an independently verified fix.

## 1. The dashboard and the common workload

A's observed total is 84% and B's is 71%, giving B −13 percentage points. At an 80% routine mix, A scores 0.8 × 0.9 + 0.2 × 0.6 = 0.84. B scores 0.8 × 0.95 + 0.2 × 0.65 = 0.89. Both within-type comparisons give +5 points. The direction reverses because B was disproportionately assigned difficult cases.

Even within exceptions, B might have seen suppliers whose supporting documents were more complete. Establish whether those documents were available at receipt, then replay both versions against the same point-in-time evidence. The observed change in case mix is visible in the table. Supplier completeness is a proposed rival explanation, not an observed fact about these cases.

## 2. Pair the outcomes

Both succeed on 76 cases, only A on 8, only B on 13, neither on 3. A's 84 and B's 89 are compatible with 21 disagreements. Net change is 13 − 8 = 5 additional successes per 100 cases. Inspect the eight regressions for severe unsupported actions, then inspect the thirteen gains to understand the mechanism. Comparing error severity can change a decision even at the same success rate.

For the fixed suite the difference is exactly five points. If estimating variability across future suppliers drawn by a similar sampling process, resample whole suppliers, preserve paired outputs, and recompute the difference on each draw. Log how many suppliers there are and whether one supplies most cases. If there is only one supplier, the observed suite gives no between-supplier variation to estimate. Repeated runs of the same stochastic pipeline address a separate source of variation.

## 3. Assignment and interference

Assign teams within matched pairs. Measure each eligible invoice case once, linking all revisions and retries. Aggregate to team-level success rates, then average within-pair treatment differences. The target weights each participating team equally. If the target changes to a typical invoice, define volume weighting in advance and still account for team-level assignment.

A central reviewer shared across both teams may learn treatment practices or experience treatment-induced delay. Reassigning individual cases leaves both paths open. If stable, sufficiently numerous non-overlapping reviewer pools exist, consider pool assignment and plan power at that level. If there is only one shared pool and carryover cannot be controlled, continue with paired replay for the offline question and record the live effect as unresolved.

## 4. Cost and decision

| Measure | A | B |
| --- | ---: | ---: |
| Cost per eligible case | 420 / 100 = 4.20 | 480 / 100 = 4.80 |
| Cost per verified success | 420 / 84 = 5.00 | 480 / 89 ≈ 5.39 |
| Extra cost per net extra verified success on this suite | — | (480 − 420) / (89 − 84) = 12.00 |

At a hard ceiling of 5.2 per verified success, B exceeds the budget despite better quality. Keep A for the stated decision, or redesign B and evaluate a fresh version. If the business owner explicitly revises the budget because a correct outcome is worth more, the decision can change. These costs include all 100 cases by construction. Using only successful cases' processing costs would hide wasted work.

## 5. An adjudication and stopping plan

Include all supported invoices arriving during the frozen enrollment window. Exclude only predeclared ineligible records identifiable at intake, such as synthetic test traffic. Keep timed-out cases and crossovers in their assigned arm. Count successful outcomes only when verified by the deadline. Separately report the fraction with unavailable labels. For a sensitivity check, bound each arm's rate between verified successes divided by eligible cases and (verified successes + unknown cases) divided by eligible cases. A pessimistic bound for the treatment difference gives A the favorable missing-case assumption and B the unfavorable one.

Report routine and exception cases and supplier familiarity as prespecified subgroups, with their denominators. Keep subgroup findings exploratory unless the study was designed to test them. Freeze team count, enrollment horizon, deadline, meaningful effect, budget, and severity limits before the trial. Use a single final efficacy analysis after outcomes mature. Stop exposure for prespecified safety or data-integrity failures and document the interruption.

The example interval [−1, +11] points fails a gate requiring its lower bound to exceed +2 points. A +5 point estimate alone cannot pass the gate. Keep the decision inconclusive and inspect uncertainty and guardrails. A replay win supports improved performance on the tested workload. A successful randomized trial supports an effect of assignment in the participating teams under its operating conditions. Expansion to new teams needs evidence about their workload and constraints.

## 6. Debugging assistant transfer

Define an issue as one task, including its reopened attempts. Require a reproducer or failing test before eligibility. Success might mean a fix that passes an independent regression test, preserves the specified behavior, and survives a defined reopen window. Compare on historical issues using repositories as split groups when the claim concerns unfamiliar repositories.

A retrieval index containing the eventual merged fix leaks the answer. A developer who learns a diagnosis from the assistant on one ticket can reuse it on a control ticket. For a live evaluation, consider assignment by collaborating team, subject to enough independent teams and contained collaboration across arms. Measure time to verified resolution and regressions along with completion. The number of generated patches alone gives little evidence about successful debugging.

## Assessment criteria

A complete plan names the decision, population, case, assignment unit, denominator, outcome window, data split, independent units, exclusions, guardrails, cost, stopping rule, and inference boundary. It identifies a concrete mechanism for leakage, selection, or interference and changes the design to address it. The rubric describes an answer a learner could produce. No learner assessment was performed.

## Reproducible arithmetic

```python
from fractions import Fraction as F

a, b = (F(72, 80), F(12, 20)), (F(19, 20), F(52, 80))
assert F(71, 100) - F(84, 100) == F(-13, 100)
for routine_weight in (F(4, 5), F(1, 2)):
    def total(rates):
        return routine_weight * rates[0] + (1 - routine_weight) * rates[1]
    assert total(b) - total(a) == F(5, 100)
assert sum((76, 8, 13, 3)) == 100
assert (76 + 13) - (76 + 8) == 5
assert F(420, 84) < F(52, 10) < F(480, 89)
assert F(480 - 420, 89 - 84) == 12
waits = [1] * 9 + [21]
assert sum(waits) == sum([3] * 10)
assert sum(t > 10 for t in waits) == 1
print("PASS: workload mix, paired counts, budget, marginal cost, and deadline example")
```

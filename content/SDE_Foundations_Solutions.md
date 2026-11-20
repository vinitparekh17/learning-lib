# SDE Foundations — Solutions Export

This export combines all 24 worked-answer companions. Attempt the matching exercise before reading its solution. These are authored solutions, not learner answers or evidence of mastery.

---

---

# F01 — Hints, worked answers, and checks

| Field | Value |
| --- | --- |
| ID / revision | F01 answers / 1.0 |
| Date | 2026-11-02 |
| Prerequisites | [F01 core pack](SDE_F01.md) |
| Capability developed | Check a proof, trace, and cost claim against a concrete contract |
| Source-check status | Same R01 passages as core §9; solutions below are original derivations |
| Experiment status | Reproduction block executed under Python 3; bounded exhaustive checks passed |

## Hints before solutions

1. At outer position j, test earlier positions in ascending order. Stop counting when the function returns.
2. State exactly what `seen` contains before the membership test. Keep “no previous duplicates” as a separate clause.
3. The triangular sum counts comparisons, not elapsed time. A container call may perform multiple comparisons.
4. Which information did a plain set discard? Store just enough to restore the required output.
5. Locate the forgotten key. Decide whether the allowed duplicate horizon can change.
6. A local proof assumes sequential execution. Find the gap between checking and performing a consequential action.

## 1. Trace

| j | Current value | Pairwise comparisons at this step | Set membership result |
| ---: | ---: | --- | --- |
| 0 | 4 | 0 | Absent |
| 1 | 9 | 4 vs 9: 1 comparison | Absent |
| 2 | 1 | 4, 9 vs 1: 2 comparisons | Absent |
| 3 | 7 | 4, 9, 1 vs 7: 3 comparisons | Absent |
| 4 | 9 | 4 vs 9, then 9 vs 9: 2 comparisons | Present |

Both return `True`. The baseline performs 8 equality comparisons. The remembered-state procedure performs 5 membership calls and 4 insertion calls. These are abstract calls; the trace does not imply only 5 equality comparisons inside a real set.

## 2. Proof and bug

Before processing position k, the set contains exactly the keys at positions below k. If execution has reached this point without returning, those earlier keys are distinct. Empty initialization satisfies this. A successful membership test implies an earlier matching position; an unsuccessful test permits adding the new value while preserving distinctness and exact membership. After the last unsuccessful test, the entire input is distinct. The loop consumes one item per iteration from a finite input, so it terminates.

If insertion precedes membership, `[8]` inserts 8 and immediately finds it, even though the required different position does not exist. The invariant no longer describes an exclusively earlier prefix at the test. A returned positive must have a witness consisting of two distinct positions.

## 3. Cost and assumptions

For 100 distinct values: 100×99/2 = 4,950 comparisons. For 1,000: 1,000×999/2 = 499,500. The ratio is 100.909…, rather than exactly 100, because the lower-order term still contributes at finite n.

For expected linear total work, assume constant-cost keys/equality/hashing, an appropriate hashing model, controlled load, and a resizing policy whose costs amortize across insertions. Also assume the keys maintain their identity while stored. The abstract membership count is at most n. It does not bound the number of actual equality comparisons by n: collisions can require examining multiple candidates. A constant-hash chained representation is a counterexample to unconditional linear time.

## 4. Return indices

Store a map `first_index[key] = earliest processed position`. Before position j, the map associates each earlier key with its first index. Check membership before inserting. When present, return `(first_index[x], j)`; otherwise insert j. The example returns `(1, 4)` using zero-based positions.

Because this procedure terminates on its first repeated key, all earlier keys are still distinct. Its first-index convention is unambiguous. If requirements change to all repeated pairs, a single index per key will not preserve enough information; output size may itself be quadratic. Returning one witness retains expected O(n) total time and O(n) extra entries under the same map assumptions as the set. No-match inputs return `None`.

## 5. Bounded memory

Before the last key in `[1, 2, 3, 1]`, a previous-two-items cache contains 2 and 3. It misses the duplicate 1. Legitimate alternatives include:

- Define a last-two-items question explicitly, accepting that older repeats are outside scope.
- Permit external exact storage that retains earlier keys and defines its lookup/durability guarantees.
- Restrict IDs to a small known universe and allocate membership flags for that universe.
- Permit replaying an immutable stored input and compare each new position against earlier positions, trading time and input access for auxiliary memory.

These alternatives change different assumptions. “Use a hash” alone does not create unlimited exact history in fixed memory. A probabilistic summary would require a specified error model; no such summary is implemented or analyzed here.

## 6. Duplicate business effects

Possible timeline: worker A checks absent; worker B checks absent; A pays; B pays; both record the ID. The membership set may end up containing a single key despite two payments. The final set contents cannot prove that only one effect occurred.

A stronger intended invariant is “For each business operation key, at most one committed payment effect occurs.” Its scope must include the durable state and payment boundary, retries, and failures. A coordination mechanism, atomic constraint, or idempotency contract must be chosen and checked in S03/S04 and C01. This answer intentionally does not claim that putting a lock around one process solves cross-process or external effects.

## Assessment criteria

| Capability | Evidence of a useful answer |
| --- | --- |
| Formulation | Defines equality, distinct positions, empty input, and output shape |
| Derivation | Identifies repeated prefix membership and the state needed to answer it |
| Correctness | Names the program boundary and handles initialization, preservation, both returns, and termination |
| Analysis | Counts an explicit operation and qualifies expected/amortized and key-size assumptions |
| Transfer | Explains a changed contract and an invalid extension of the local proof |

No learner score is recorded. If a step is unclear, revisit that step using a three-element input and manually inspect the state before each test.

## Reproduction appendix — executed checks

The following standard-library-only block is the executed validation code. It checks all sequences of lengths 0 through 7 over `{0,1,2}`: 3,280 inputs. The oracle uses frequency counting, distinct from the two detection procedures. Assertions verify the remembered-state invariant on every processed prefix. Additional tests check a one-bucket collision model, the insert-before-check bug, the forgetting counterexample, and arithmetic. This is a bounded correctness check, not a performance benchmark or evidence for all possible keys.

```python
from itertools import product
from collections import Counter

def pairs(a):
    comparisons = 0
    for j in range(len(a)):
        for i in range(j):
            comparisons += 1
            if a[i] == a[j]:
                return True, comparisons
    return False, comparisons

def seen_check(a):
    seen = set()
    for k, x in enumerate(a):
        assert seen == set(a[:k]) and len(seen) == k
        if x in seen:
            return True
        seen.add(x)
    return False

def witness(a):
    first = {}
    for j, x in enumerate(a):
        if x in first:
            return first[x], j
        first[x] = j
    return None

cases = 0
for n in range(8):
    for a in product(range(3), repeat=n):
        oracle = any(count > 1 for count in Counter(a).values())
        assert pairs(a)[0] == seen_check(a) == oracle
        w = witness(a)
        assert (w is not None) == oracle
        if w is not None:
            i, j = w
            assert 0 <= i < j < n and a[i] == a[j]
        cases += 1
assert cases == 3280
assert pairs([4, 9, 1, 7, 9]) == (True, 8)
assert pairs([8, 3, 6, 3]) == (True, 5)
assert witness([4, 9, 1, 7, 9]) == (1, 4)
for n in (0, 1, 2, 10, 100, 1000, 2000):
    assert pairs(list(range(n))) == (False, n * (n - 1) // 2)

# Explicit one-bucket chained model; each contains scan checks keys.
# Append follows a confirmed miss, so no second search is needed.
bucket = []
checks = 0
for x in range(100):
    for y in bucket:
        checks += 1
        assert x != y
    bucket.append(x)
assert checks == 4950
assert 1 % 10 == 11 % 10 and 1 != 11

def insert_first_bug(a):
    seen = set()
    for x in a:
        seen.add(x)
        if x in seen:
            return True
    return False
assert insert_first_bug([8]) is True
assert pairs([8])[0] is False

def previous_two(a):
    recent = []
    for x in a:
        if x in recent:
            return True
        recent.append(x)
        recent = recent[-2:]
    return False
assert previous_two([1, 2, 3, 1]) is False
assert seen_check([1, 2, 3, 1]) is True
print(f"PASS: {cases} exhaustive inputs; traces, counts, witnesses, and counterexamples")
```

Source and review limits: R01 passages support the abstract foundations; all exercise inputs and calculations are original. No current Python hash implementation details were inspected, and no claim about its precise collision or resizing policy is needed for these checks. Audit A remains queued.
---

# F02 — Hints, worked answers, and checks

| Field | Value |
| --- | --- |
| ID / revision | F02 answers / 1.0 |
| Date | 2026-11-02 |
| Prerequisites | [F02 core](SDE_F02.md) |
| Capability developed | Reconstruct conditional probabilities and audit an action rule |
| Source-check status | Same R02 and R23 passages as core §9; solutions are original derivations |
| Experiment status | Exact rational arithmetic and boundary checks executed; no empirical experiment |

## Hints

1. Split the population into error and clean groups first, then split each by alert status.
2. Divide true alerts by all alerts, including clean-record alerts.
3. Write both expected losses before rearranging an inequality.
4. Review must beat both alternatives. For imperfect review, include the fee and residual errors.
5. Average the equally sized groups, then inspect them separately.
6. A deliberately balanced test set has an assigned prevalence, not necessarily the deployment prevalence.

## 1. Two populations

For L, true alerts=100×0.9=90; missed errors=10; false alerts=9,900×0.05=495; correct non-alerts=9,405. Precision is 90/585=2/13≈15.3846%. Non-alert error probability is 10/9,415=2/1,883≈0.1062%.

For H, true alerts=2,000×0.9=1,800; missed errors=200; false alerts=8,000×0.05=400; correct non-alerts=7,600. Precision is 1,800/2,200=9/11≈81.8182%. Non-alert error probability is 200/7,800=1/39≈2.5641%.

Each table sums to 10,000. Sensitivity divides true alerts by all erroneous records; precision divides them by all alerted records. Their equal numerator does not make the ratios interchangeable. Recover the base rate by weighting each row's error probability by its share of the population.

## 2. Third population

| Outcome | Error | Clean | Total |
| --- | ---: | ---: | ---: |
| Alert | 800 | 180 | 980 |
| No alert | 200 | 8,820 | 9,020 |
| Total | 1,000 | 9,000 | 10,000 |

P(E|A)=800/980=40/49≈81.6327%. The no-alert error probability, if needed, is 200/9,020=10/451≈2.2173%. The table is a designed scenario. Observing exactly these counts in a future sample is not guaranteed merely by specifying rates.

## 3. Different costs, same probability

At p=0.2, with missed-error cost 100 and unnecessary-pause cost 20: pass loss=20; pause loss=16. Pause wins. Threshold=20/(100+20)=1/6.

Raise only the unnecessary-pause cost to 40: pass loss remains 20; pause loss becomes 32. Pass wins. Threshold=40/140=2/7≈28.5714%. The probability estimate and detector evidence stayed fixed. The loss of interrupting a clean case changed the decision. At either threshold, the alternatives tie; state a tie policy rather than claim a strict preference.

More generally, if correct actions also have nonzero costs, compute each action's full expected loss. Do not insert the old threshold formula without checking its premises.

## 4. Review boundaries

Perfect review at cost 4 beats passing when 4<100p, so p>1/25=0.04. It beats pausing when 4<20(1−p), so p<4/5=0.8. Review is strictly best inside that interval. Outside it, the relevant automatic action is cheaper; endpoints are ties.

Imperfect review has loss 6+3p. Against passing:

6+3p<100p ⇒ p>6/97≈0.061856.

Against pausing:

6+3p<20−20p ⇒ p<14/23≈0.608696.

The review region narrows to (6/97,14/23). Below its lower endpoint, pass is best; above its upper endpoint, pause is best. The two automatic losses cross at 1/6, which lies inside this review region, so there is no overlooked interval where one of them defeats review. At p=0.2, review loss is 6.6, less than both 20 and 16.

This calculation assumes reviewer error rates conditional on true status remain the stated values among routed records. Selection can change those rates: difficult cases sent to review may not resemble cases in a general reviewer assessment.

## 5. Calibration and subgroups

With equal-sized groups, (0.1+0.9)/2=0.5. All predictions have score 0.5, so aggregate event frequency agrees with that score. Within the first group it overstates risk by 0.4; within the second it understates risk by 0.4. This is an exact hypothetical construction, not a sampled finding.

Check event frequencies by relevant subgroup and score range on suitable labeled cases. Record sample sizes, label definitions, uncertainty, and whether the data represent deployment. A common action threshold may still be appropriate when losses match, but the input probabilities need to represent the information used. Apparent aggregate calibration cannot certify that property for subgroups.

## 6. Balanced evaluation versus deployment

Precision computed on a 50%-error evaluation set uses that set's prevalence. It cannot simply be reported as deployment precision at 1%. If sensitivity and false-positive rate transfer unchanged, substitute the deployment base rate in Bayes' expression. That transfer assumption itself needs checking across document types, sources, and time.

Before automatic decisions, measure or otherwise justify at least: deployment prevalence with an appropriate sampling design; conditional detector rates on relevant labeled inputs; and the losses and operational consequences of permitted actions. Review accuracy, queue capacity, and subgroup calibration are further relevant measurements. Do not label only alerted cases if you also need to estimate missed errors: that selection leaves an important denominator unobserved. F03 develops the sampling and experimental design needed to investigate these questions.

## Assessment criteria

| Capability | Evidence in an answer |
| --- | --- |
| Conditional reasoning | Names the population after “among” and uses the correct denominator |
| Mechanism | Builds joint counts and derives the Bayesian update |
| Decision analysis | Includes every modeled action/state loss and treats ties explicitly |
| Transfer | Explains how changed prevalence, losses, or reviewer errors affect policy |
| Evidence discipline | Distinguishes hypothetical rates, measured estimates, calibration, and decisions |

No learner score or readiness judgment is recorded.

## Reproducible checks — executed

```python
from fractions import Fraction as F

def table(b, s, f):
    errors, clean = 10000*b, 10000*(1-b)
    return errors*s, clean*f, errors*(1-s), clean*(1-f)

cases = [
    (F(1,100),F(9,10),F(1,20),(90,495,10,9405),F(2,13)),
    (F(1,5),F(9,10),F(1,20),(1800,400,200,7600),F(9,11)),
    (F(1,10),F(4,5),F(1,50),(800,180,200,8820),F(40,49)),
]
for b,s,f,expected,precision in cases:
    tp,fp,fn,tn = table(b,s,f)
    assert (tp,fp,fn,tn) == expected
    assert tp+fp+fn+tn == 10000
    assert tp/(tp+fn) == s and fp/(fp+tn) == f
    assert tp/(tp+fp) == precision == s*b/(s*b+f*(1-b))
    assert (tp+fp)/10000*precision + (fn+tn)/10000*fn/(fn+tn) == b
assert F(10,9415) == F(2,1883)
assert F(200,7800) == F(1,39)
assert F(200,9020) == F(10,451)
p=F(1,5)
assert (100*p,20*(1-p),40*(1-p)) == (20,16,32)
assert F(20,120)==F(1,6) and F(20,220)==F(1,11)
assert F(40,140)==F(2,7)
assert 4+F(1,20)*p*100+F(1,10)*(1-p)*20 == F(33,5)
for k in range(1001):
    p=F(k,1000)
    automatic = (20*(1-p) < 100*p)
    assert automatic == (p > F(1,6))
    for review,lower,upper in [(F(4),F(1,25),F(4,5)),
                                (6+3*p,F(6,97),F(14,23))]:
        assert (review < min(100*p,20*(1-p))) == (lower < p < upper)
for p in [F(1,25),F(4,5)]:
    assert min(100*p,20*(1-p)) == 4
for p in [F(6,97),F(14,23)]:
    assert min(100*p,20*(1-p)) == 6+3*p
assert (F(1,10)+F(9,10))/2 == F(1,2)
print('PASS: three tables; Bayes reconstruction; losses; 1001 grid points; exact boundary ties')
```

These assertions check arithmetic and the derived rule on the stated examples and a finite grid. Algebra establishes the continuous boundary under the model. No experiment establishes that the invented rates or costs hold in a real system. Audit A is pending.
---

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
---

# F04 — Hints, worked answers, and reproducible checks

| Field | Value |
| --- | --- |
| ID, revision, date | F04 answers · 1.0 · 2026-11-05 |
| Prerequisite | [F04 learning pack](SDE_F04.md) |
| Capability | Check the feature contract, ranking, update direction, step size, and evaluation boundary |
| Source check | R02 passage locators in the core pack. Numerical cases and derivations are original. |
| Experiment status | Executed the Python 3 checks below on the constructed inputs. |

## Hints

1. The query assigns one unit of weight to the second coordinate.
2. A positive scaling factor appears in both the numerator and the denominator of cosine.
3. A deterministic function returns the same output when given the same input.
4. Evaluate the derivative at the *current* weight before taking the second step.
5. Compare distances to the optimum on both sides of the step.
6. Separate the task of finding supporting evidence from the task of estimating minutes.

## 1. Shape and coordinate order

Multiplying each document row by (0, 1)ᵀ returns its payment-reference count. The output is (0, 4, 2)ᵀ, a 3 × 1 column indexed by passage. If a caller says it requested payment evidence but receives (2, 3, 0)ᵀ, it may have emitted (1, 0)ᵀ. Check the encoded query, the stored column order, and the expected output for a passage with only payment references. Shape validation alone accepts both query vectors.

## 2. Ranking and missing direction

For delivery q = (1, 0)ᵀ, the raw scores in document order are 2, 3, 0. Their descending order is B, A, C. Divide each by its document length and by the unit query length to obtain 1, 3/5, 0. Cosine orders them A, B, C. After tripling B its vector is (9, 12)ᵀ, its length is 15, and its raw score is 9. Its normalized score is 9/15 = 3/5. Both rankings retain their respective orders, although B's raw lead grows.

A zero query provides no direction. One defensible policy is to return an explicit “insufficient query features” status and ask for a usable reference type. Include that outcome when computing the fraction of all queries served successfully. Assigning a numerical score to every passage would require a separate fallback rule and a way to evaluate its relevance.

## 3. A transformation that loses information

T times A gives 1 × 2 + 1 × 0 = 2. T times C gives 1 × 0 + 1 × 2 = 2. For any function g using only the transformed count, g(2) must serve both passages. Delivery evidence occurs in A and is absent from C. Consequently at least one answer must be wrong if g always chooses present or absent. Keep the delivery coordinate or the original reference data if this distinction is part of the contract. The total still answers a question about overall volume.

## 4. A second update

After the first step w = 3/2. The current derivative is 5(3/2 − 2) = −5/2. With η = 1/10 the next weight is 3/2 + 1/4 = 7/4. Predictions of 7/4 and 7/2 minutes have residuals −1/4 and −1/2. The mean of their squared residuals is (1/16 + 1/4)/2 = 5/32 minutes². Substituting in (5/2)(7/4 − 2)² gives the same result. A fresh gradient matters because the remaining error shrinks at each step.

## 5. An overshoot

From w = 1 the slope is −5. A step size of 1/2 sends the weight to 7/2, which lies 3/2 from the optimum. The new loss is (5/2)(3/2)² = 45/8 minutes², larger than the initial 5/2. Increasing w from 1 initially moves downhill. The step travels past the minimum far enough to lose the whole gain. Under repeated updates the error multiplier is 1−5η = −3/2, so the weight alternates sides and its distance grows. In the worked convention, dividing the entire loss by two would also halve each gradient and double the corresponding stable step-size interval.

## 6. Two separate acceptance checks

In the constructed holdout, a two-page invoice took two minutes. Training reduced squared loss from 5/2 to 5/8, yet held-out squared error went from 0 to 1. For a workload claim, freeze a representative test population before selecting weights. Compare predictions with independently recorded active minutes, report mean absolute error by supplier type, and check the fraction of critical cases underestimated beyond an agreed tolerance. Decide beforehand what improvement and tolerance the workflow requires.

A higher top score can also reward repeated words without finding an applicable source. Use the same frozen queries, candidate passages, and eligibility rules for both rankers. Have blinded reviewers check the selected passage against the original invoice and required fact. Count cases with missing evidence and cases the ranker declines. A decision can then use the fraction of all eligible queries with verified supporting evidence and the observed cost of review.

**Self-assessment.** A complete solution preserves the document and feature axes, explains the scale invariance and zero case, derives the next weight using the current slope, and names a held-out outcome for each task. The numerical checks below can be run after attempting the exercises.

## Reproduction

```python
from fractions import Fraction as F
from math import isqrt

docs = [(2, 0), (3, 4), (0, 2)]
def dot(x, y):
    assert len(x) == len(y)
    return sum(a*b for a, b in zip(x, y))

def cosine(x, y):
    squared = dot(x, x) * dot(y, y)
    if squared == 0:
        return None
    root = isqrt(squared)
    assert root*root == squared  # exact roots in these examples
    return F(dot(x, y), root)

q = (1, 0)
assert [dot(d, q) for d in docs] == [2, 3, 0]
assert [dot(d, (0, 1)) for d in docs] == [0, 4, 2]
assert [cosine(d, q) for d in docs] == [1, F(3, 5), 0]
assert cosine((9, 12), q) == F(3, 5) and dot((9, 12), q) == 9
assert cosine((0, 0), q) is None
assert dot(docs[0], (1, 1)) == dot(docs[2], (1, 1)) == 2

def loss(w):
    return sum((w*x-y)**2 for x, y in [(1, 2), (2, 4)]) / F(2)
def step(w, eta):
    return w - eta * 5*(w-2)

w1 = step(F(1), F(1, 10))
w2 = step(w1, F(1, 10))
assert (w1, w2) == (F(3, 2), F(7, 4))
assert [loss(w) for w in (1, w1, w2, 2)] == [F(5, 2), F(5, 8), F(5, 32), 0]
assert loss(step(F(1), F(1, 2))) == F(45, 8)
assert (1*2-2)**2 == 0 and (w1*2-2)**2 == 1
for k in range(51):
    eta = F(k, 100)
    for w in [F(-1), F(1), F(3)]:
        assert loss(w) == F(5, 2)*(w-2)**2
        assert (loss(step(w, eta)) < loss(w)) == (0 < eta < F(2, 5))
        h = F(1, 100)
        assert (loss(w+h)-loss(w-h))/(2*h) == 5*(w-2)
print('All F04 checks passed.')
```

The symmetric difference equals the derivative exactly here because the loss is quadratic. The algebra in the learning pack establishes the step-size interval for every starting weight away from the optimum. The finite sweep checks the implementation on both sides of each boundary.
---

# S01 — Hints, worked answers, and reproducible checks

| Field | Value |
| --- | --- |
| ID / revision / date | S01 answers · 1.0 · 2026-11-04 |
| Companion | [Resource models, locality, and abstraction costs](SDE_S01.md) |
| Prerequisites / capability | F01 and S01's declared toy machine. Explain resource counts, latency, and a falsifiable comparison. |
| Source-check status | Uses R04 passages and evidence boundaries recorded in the core pack. |
| Experiment status | Python 3 model checks below executed successfully. No measured hardware performance. |
| Assessment status | Suggested criteria only. No learner answers received or mastery inferred. |

## Hints

1. Divide an address by the block size and discard the remainder. Track data lines and translated pages separately. A node has two loads.
2. Keep the cache contents after pass one. Ask how many distinct blocks are touched before a block is revisited.
3. Preserve the offset when changing a virtual page number to a physical frame number.
4. Separate assembly waiting, whole-batch service, and service cost divided by record count.
5. Design a comparison where the suspected mechanism changes while useful work stays the same.
6. Include how positions are found, how storage is allocated, and whether a compact snapshot must be built.

## 1. First-pass traffic

For the array, the line IDs are four 0s followed by four 1s. All eight page IDs are 0. There are two line misses and one translation miss.

For packed nodes, the sixteen field loads have four accesses per line, covering lines 0–3. Pages 0 and 1 each hold four nodes. There are four line misses and two translation misses.

For scattered nodes, value addresses give line IDs 0, 8, 2, 10, 4, 12, 6, 14 and page IDs 0, 4, 1, 5, 2, 6, 3, 7. Each next-pointer load repeats its value's line and page. There are eight misses of each kind, eight data hits, and eight TLB hits. A 50% TLB hit rate here reflects one hit on every node's pointer. It does not establish good absolute performance.

Multiplying data misses by the hypothetical 32-byte fill unit gives 64, 128, and 256 bytes. The pointer values contain the next addresses, including a terminating sentinel stored at the final node. Reading that sentinel counts as a load. Following it does not occur.

**Criterion.** Explain every miss and hit using the access sequence. Keep field storage, virtual span, requested bytes, and transferred bytes distinct.

## 2. Capacity changes and the second pass

With four cache lines, the array's two lines and the packed list's four lines remain resident after pass one. Neither has another data miss. Their one and two translations also fit, so their second-pass TLB misses are zero. The scattered layout exceeds both capacities and reuses blocks only after eviction. It incurs eight of each kind again.

With only two data-cache lines, the array still fits and has zero second-pass data misses. The packed list finishes its first pass with lines 2 and 3. Reading lines 0 and 1 evicts those, then reading 2 and 3 misses again. Its second pass has four data misses. The scattered list still has eight. Translation capacity is unchanged, so second-pass TLB misses remain 0, 0, and 8.

This is a concrete counterexample to “a second run is warm, therefore every access hits.” Warmth requires the relevant state to survive. It is also a counterexample to “every linked list has poor locality.” The packed list fits the original cache and translation capacities, though it still loads pointers and occupies more bytes than the array.

**Criterion.** Show which state survives and which is evicted. Do not infer time from miss counts alone.

## 3. Translation

136 = 2 × 64 + 8, so the virtual page number is 2 and the offset is 8. Mapping page 2 to frame 7 yields physical address 7 × 64 + 8 = **456**.

The TLB remembers a mapping. The data cache remembers data. A TLB miss can be resolved from page tables for an already-resident page. It says nothing by itself about whether the resulting physical data line is cached. Storage I/O requires a separate condition such as fetching a nonresident backed page. Our simulation excludes that condition. It also excludes the page-table memory traffic needed to repair a translation miss.

**Criterion.** Preserve the offset and distinguish translation work, data-cache lookup, and nonresident-page handling. The R04 chapter 19 and 21 passages in the core ledger support this boundary.

## 4. Batching

The one-record service cost is 24 + 3 = 27 microseconds. For eight records it is 24 + 8 × 3 = 48, or 6 per record. With an indefinitely backlogged worker, throughputs are 1,000,000/27 ≈ 37,037 records/s and 8,000,000/48 ≈ 166,667 records/s. Their ratio is 4.5. These are conditional model outputs, not benchmark results.

At 100-microsecond arrival spacing, eight arrivals occur at 0, 100, …, 700. The full batch completes at 748. Latencies are 748, 648, 548, 448, 348, 248, 148, and 48 microseconds. Their mean is (748 + 48)/2 = **398**. Each immediately processed record takes 27 because service completes before the next arrival.

For general positive integer k in this scenario, first-record latency is

\[
100(k-1)+24+3k = 103k-76.
\]

The requirement 103k−76 ≤ 750 gives k ≤ 826/103 ≈ 8.019. Thus the largest permitted full batch is eight. Nine would take 851. A wait timeout can cap assembly time when arrivals vary, but must leave time for actual service and any queueing. It does not guarantee a deadline on its own.

**Criterion.** Name the arrival and load conditions. Never call the amortized 6-microsecond service cost a 6-microsecond batch-member latency.

## 5. A test that can overturn the explanation

A useful hypothesis is that dependent scattered accesses cause longer traversal time for the target record sizes. Start with one compiled implementation and the same immutable records and checksum. Measure packed and scattered node traversal at several sizes. Use the same field representation so pointer overhead is not confused with array-versus-node layout. Separately include the packed array as the practical alternative.

Allocation inside only one timed region is a confound. So is placing one candidate's data in a different memory region or running it under different competing load. Report construction-inclusive and traversal-only times with matching boundaries. Check warmup, compiler elimination, generated dependencies, and output correctness.

Where the platform exposes suitable counters, compare cache misses, translation events, and memory traffic using their documented meanings. Test a small working set that fits, then enlarge it. A small-set speed gap that persists without the predicted miss difference weakens a cache-miss-only explanation. Add identical expensive per-record arithmetic as a separate sensitivity test. If arithmetic then dominates, layout may matter less to whole-task time. A null result with noisy measurements is inconclusive, so include repeated-run variation.

**Criterion.** State a predicted change, a controlled comparison, a mechanism observation, and a result that would change the explanation. This is a proposed experiment, not an executed one.

## 6. Changed constraints

For frequent insertion after already-known nodes, a linked representation can avoid shifting a packed array's suffix. That conclusion assumes node references are already available and storage can be allocated. Searching for the insertion point, allocation, ownership, and concurrent mutation can dominate or invalidate a simple constant-work splice story. A segmented or slack-filled representation is another candidate if scans and updates both matter.

For a repeatedly scanned immutable snapshot, a compact array is a reasonable starting choice. Measure the cost of constructing the snapshot and how many scans reuse it. If compacting costs C and each subsequent scan saves Δ, the simple serial break-even condition is mΔ > C for m scans, assuming Δ > 0 and no other changes. Include extra peak memory while both forms coexist. If only one scan occurs, conversion can lose overall despite a faster scan.

An integer sum invariant remains that after k logical visits the accumulator equals the sum of exactly those k values. A cycle, missed node, duplicate visit, overflow, or reordering that violates the actual task contract invalidates the comparison before speed matters.

**Criterion.** Defend a conditional choice and include construction, memory, and correctness. A representation name alone is not an explanation.

## Reproduction appendix

The following standard-library Python 3 block was executed on 2026-11-04. It models references to explicitly assigned addresses. The Python runtime's own memory layout and execution time have no role in these results. It verifies list termination and sums, cache and TLB counts over two passes, changed capacity, translation arithmetic, batch deadlines, and units-based throughput ratios. LRU state is retained between passes and reset between layouts.

```python
from collections import OrderedDict
from fractions import Fraction

class LRU:
    def __init__(self, capacity):
        assert capacity > 0
        self.capacity = capacity
        self.items = OrderedDict()

    def touch(self, block):
        miss = block not in self.items
        if not miss:
            self.items.move_to_end(block)
        else:
            self.items[block] = None
            if len(self.items) > self.capacity:
                self.items.popitem(last=False)
        return int(miss)

def linked_trace(addresses):
    nodes = {
        a: (i + 1, addresses[i + 1] if i + 1 < len(addresses) else None)
        for i, a in enumerate(addresses)
    }
    trace, seen, total = [], set(), 0
    p = addresses[0]
    while p is not None:
        assert p in nodes and p not in seen
        seen.add(p)
        value, nxt = nodes[p]
        trace.extend([p, p + 8])
        total += value
        p = nxt
    assert len(seen) == len(addresses) and total == 36
    return trace

traces = {
    'array': list(range(0, 64, 8)),
    'packed': linked_trace(list(range(0, 128, 16))),
    'scattered': linked_trace([0, 256, 64, 320, 128, 384, 192, 448]),
}
assert sum(range(1, 9)) == 36

def two_passes(trace, cache_capacity=4):
    cache, tlb = LRU(cache_capacity), LRU(2)
    results = []
    for _ in range(2):
        data_misses = translation_misses = 0
        for address in trace:
            assert address % 8 == 0
            assert address // 32 == (address + 7) // 32
            data_misses += cache.touch(address // 32)
            translation_misses += tlb.touch(address // 64)
        results.append((data_misses, translation_misses))
    return results

expected = {
    'array': [(2, 1), (0, 0)],
    'packed': [(4, 2), (0, 0)],
    'scattered': [(8, 8), (8, 8)],
}
for name, trace in traces.items():
    result = two_passes(trace)
    assert result == expected[name]
    # Independent first-pass counts work because no block is revisited
    # after moving on from its contiguous run in these particular traces.
    assert result[0][0] == len({a // 32 for a in trace})
    assert result[0][1] == len({a // 64 for a in trace})
    print(name, result, 'fill bytes', result[0][0] * 32)

assert two_passes(traces['array'], 2) == [(2, 1), (0, 0)]
assert two_passes(traces['packed'], 2) == [(4, 2), (4, 0)]
assert two_passes(traces['scattered'], 2) == [(8, 8), (8, 8)]
assert divmod(136, 64) == (2, 8)
assert 7 * 64 + 8 == 456

h, c, k, spacing = 24, 3, 8, 100
service = h + c * k
arrival = [i * spacing for i in range(k)]
finish = arrival[-1] + service
latencies = [finish - t for t in arrival]
assert service == 48 and Fraction(service, k) == 6
assert Fraction(k, service) / Fraction(1, h + c) == Fraction(9, 2)
assert (latencies[0], latencies[-1]) == (748, 48)
assert Fraction(sum(latencies), k) == 398
def first_latency(size):
    return (size - 1) * spacing + h + c * size
assert first_latency(8) == 748 and first_latency(9) == 851
assert max(s for s in range(1, 101) if first_latency(s) <= 750) == 8
# A monotone expression establishes the bound beyond the tested range.
assert spacing + c > 0
assert h + c < spacing
print('All S01 model checks passed.')
```

Expected printed rows are `array [(2, 1), (0, 0)] fill bytes 64`, `packed [(4, 2), (0, 0)] fill bytes 128`, and `scattered [(8, 8), (8, 8)] fill bytes 256`, followed by the success line. These checks establish the declared model's bookkeeping, not production speed, physical memory consumption, or a real scheduler's behavior.

## Revision history

- 1.0 — 2026-11-04. Six worked answers, assessment criteria, and executed model checks. Curriculum Audit A remains pending.
---

# S02 — Hints, worked answers, and checks

| Field | Value |
| --- | --- |
| ID / revision / date | S02 answers · 1.0 · 2026-11-05 |
| Prerequisite | [Data organization, indexes, and recovery](SDE_S02.md) |
| Capability | Audit a query path and a commit promise against explicit invariants |
| Sources | R05 and R04 passages are recorded in the core pack. |
| Experiment | Executed SQLite queries against synthetic facts and enumerated a separate redo-only recovery model in Python. |

## Hints

1. Follow the approval after the head moves. Which row and which source bytes does it identify?
2. Translate each row ID into a page before adding index reads.
3. Distinguish a revision that exists from one selected by Head.
4. Count row-ID associations before estimating bytes or writes.
5. List the durable prefix and the two home values separately.
6. Consider a crash immediately before the reply and immediately after dispatch.

## 1. Keep the evidence behind an approval

Suppose D17/1 records a total of 90 and D17/2 records 95 in the same currency. Joining an old approval to the current head returns 95 even if the reviewer approved 90. Joining only by doc and name across history can return *both* totals. Store the approved evidence's (doc, rev, slot) and join by that key. Resolve its page locator against the immutable source reference attached to that same revision. Keep the source version readable throughout the evidence-retention period. A checksum alone cannot reconstruct a deleted page.

## 2. Count what each path actually reads

Q1 finds row 5 on P2 and row 10 on P3. Its indexed path inspects two candidate records and reads four distinct cold pages including root and leaf. Q2 finds 2, 5, 12 on P1, P2, P3. It inspects three candidate records and reads five distinct cold pages. Scanning either query inspects twelve records over three pages. A resident root reduces the respective cold reads to three and four under the same other assumptions. The root lookup still occurs. If the leaf contains every requested field and sufficient visibility information, the heap fetches could also disappear.

The count includes only facts that pass the exact index predicate as candidate heap records. An index keyed just on doc would return four D17 candidates and require a revision check. The narrower key may be useful for other queries. It answers a different performance question.

## 3. Historical versus current

Historical X hits are 2, 5, 12. D17/1 has been superseded by D17/2, so only 5 and 12 survive the current-revision filter under the assigned heads. After publishing D17/3 with Y, only 12 survives. Join each candidate's (doc, rev) to (doc, published_rev) in Head. A cached Head entry for D17 can serve two candidate checks. Additional cold reads depend on Head's index and data layout. The given fact-page model has insufficient information to assign an exact cold total to the join. A current-only secondary index could accelerate this query, at the cost of removing obsolete entries and installing new ones atomically when Head changes.

## 4. Ingestion and the decision

Two base inserts are required. Keeping only the revision index adds two revision associations, for four logical additions. Keeping only the delivery index adds one delivery association, for three. Keeping both gives five. Revision metadata and Head updates are outside those figures. Old revision entries stay available for historical queries. If X becomes ubiquitous and each investigation needs full locators from nearly every page, compare a scan against the secondary lookup. If selective historical investigations become frequent, measure how much the secondary index saves under that mix and whether ingestion can absorb the cost.

## 5. Recover partial installation

The durable prefix contains SET F3, SET H=3, and COMMIT. Home contains F3 and H=2. Reapply the complete bundle assignment, then assign H=3. Rebuilding derived indexes from the recovered facts restores their query results. The immutability of old revisions preserves approvals pointing to D17/1 or D17/2.

Now allow H=3 to reach home before COMMIT. A crash with the update-only log leaves H=3 but F3 missing. The toy recovery skips incomplete transactions and therefore preserves the dangling reference. Valid fixes include preventing this flush or retaining undo information and using a recovery protocol that restores the prior state. Replaying every update unconditionally would expose an uncommitted revision.

## 6. State the promise and its boundary

A success reply promises that after a process or power failure with the modeled stable storage intact, recovery will expose the complete published revision and preserve earlier evidence. A timeout is compatible both with a transaction that never committed and with one whose reply was lost. Look up a stable operation key before deciding to retry. The write protocol must enforce the operation-key constraint at the same transaction boundary if a retry is to reuse the existing result.

Surviving loss of the device requires an independently durable copy with a tested recovery procedure. If every acknowledged revision must survive that loss, success must wait for sufficient data to be durable outside that failure domain. A nightly backup alone leaves a window of acknowledged changes at risk. S04 will specify the replication and failure assumptions in detail.

**Assessment criteria.** A defensible answer names the revision key, states the query semantics, counts pages and matching rows separately, identifies the durable commit boundary, and gives a crash or workload that defeats an overbroad claim.

## Reproduce the checks

Run this block under Python 3. SQLite checks the logical query results. The assigned heap layout and cold-page counts are calculated separately. The recovery function models ordered durable records and atomic home writes. These are three different checks.

```python
import sqlite3
from itertools import product

data = [
    (17,1,'total','90'), (17,1,'delivery','X'),
    (8,1,'total','55'), (8,1,'delivery','Y'),
    (17,2,'delivery','X'), (9,1,'total','48'),
    (9,1,'delivery','Z'), (10,1,'total','70'),
    (10,1,'delivery','Y'), (17,2,'total','95'),
    (11,1,'total','75'), (11,1,'delivery','X'),
]
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE fact(id INTEGER PRIMARY KEY, doc INT, rev INT, name TEXT, val TEXT)')
db.executemany('INSERT INTO fact(doc,rev,name,val) VALUES(?,?,?,?)', data)
q1 = 'SELECT id FROM fact WHERE doc=17 AND rev=2 ORDER BY id'
q2 = "SELECT id FROM fact WHERE name='delivery' AND val='X' ORDER BY id"
def ids(query):
    return [row[0] for row in db.execute(query)]

assert ids(q1) == [5,10] and ids(q2) == [2,5,12]
db.execute('CREATE INDEX by_rev ON fact(doc,rev)')
db.execute("CREATE INDEX by_delivery ON fact(val) WHERE name='delivery'")
assert ids(q1) == [5,10] and ids(q2) == [2,5,12]
db.execute('CREATE TABLE head(doc INTEGER PRIMARY KEY, rev INT)')
db.execute('INSERT INTO head SELECT doc, MAX(rev) FROM fact GROUP BY doc')
current = "SELECT id FROM fact JOIN head USING(doc,rev) WHERE name='delivery' AND val='X' ORDER BY id"
assert ids(current) == [5,12]
def heap_pages(row_ids):
    return {(row_id-1)//4 + 1 for row_id in row_ids}
assert len(heap_pages(range(1,13))) == 3
assert 2 + len(heap_pages(ids(q1))) == 4
assert 2 + len(heap_pages(ids(q2))) == 5
db.executemany('INSERT INTO fact(doc,rev,name,val) VALUES(?,?,?,?)',
               [(17,3,'total','98'), (17,3,'delivery','Y')])
db.execute('UPDATE head SET rev=3 WHERE doc=17')
assert ids(current) == [12] and ids(q2) == [2,5,12]
assert db.execute('SELECT val FROM fact WHERE id=1').fetchone() == ('90',)

# One transaction and one complete, ordered log prefix.
bundle = ('total=98','delivery=Y')
log = [('bundle',bundle), ('head',3), ('commit',True)]
old = {'head':2,'bundle':None}
new = {'head':3,'bundle':bundle}
def recover(home, prefix):
    state = home.copy()
    if prefix and prefix[-1] == ('commit',True):
        state.update(prefix[:-1])
    return state

for length in range(3):  # no durable commit, NO-STEAL
    assert recover(old, log[:length]) == old
for wrote_bundle, wrote_head in product((False,True), repeat=2):
    home = {'head':3 if wrote_head else 2,
            'bundle':bundle if wrote_bundle else None}
    assert recover(home, log) == new
    assert recover(recover(home, log), log) == new
# Illegal flush breaks the invariant when there is no durable COMMIT.
assert recover({'head':3,'bundle':None}, log[:2]) == {'head':3,'bundle':None}
print('S02 query, page-count, publication and recovery checks passed.')
```

The toy log uses full after-values. An operation such as “increment a balance” would require a replay guard or a different log encoding to tolerate repeated application. Real device flush behavior and database crash handling require a deployment-specific test.
---

# S03 — Hints, worked answers, and checks

| Field | Value |
| --- | --- |
| ID / revision / date | S03 answers · 1.0 · 2026-11-06 |
| Prerequisites | [Concurrency, transactions, and logical time](SDE_S03.md), F01, S02 |
| Capability developed | Test a history against an invariant and identify where a guarantee ends |
| Source-check status | R05 and R06 primary passages and locators recorded in the core pack |
| Experiment status | Finite Python models executed. These checks do not test an actual database, lock manager, network, or external payment service. |

## Hints

1. Include the row each transaction reads but does not write.
2. Ask whether another transaction can change the state before the first decision commits.
3. Two occurrences of “empty” can belong to different approval rounds.
4. Follow process and message arrows before comparing numbers.
5. A timeout describes client knowledge. It does not identify the commit outcome.
6. Draw who waits for whom. Then separate safety, eventual progress, and observed latency.

## 1. Read dependencies can defeat disjoint writes

One expanded history is `R_A(a)=0, R_A(b)=0, R_B(a)=0, R_B(b)=0, W_A(a)=1, C_A, W_B(b)=1, C_B`. The writes become visible at their respective commits. Both transactions base their decisions on (0,0).

`R_A(b)` precedes `W_B(b)`, giving A→B. `R_B(a)` precedes `W_A(a)`, giving B→A. Preserving both read dependencies requires a cycle, so this history is not conflict serializable. The direct serial comparison is even more specific to the application. A then B produces (1,0), and B then A produces (0,1). The actual (1,1) is neither.

Both rows are valid bits and both candidate IDs are unique. The violated condition spans the pair. A unique key on `(doc,epoch)` in the authoritative Acceptance relation can encode the one-slot invariant. The rule must apply to every acceptance path, and the rejected transaction must not report success or execute a payment.

## 2. Hold the guard across the decision

B obtains the guard, reads (0,0), stages its acceptance and evidence, commits, then releases the guard. A waits, acquires it, reads current committed (0,1), and declines. If either transaction aborts, all of its database changes are discarded before the guard becomes available.

Early release gives this counterexample. A acquires, reads (0,0), releases. B acquires, reads (0,0), releases. A commits a=1. B commits b=1. Each read held a lock, but the decision was not protected through the update. The missing property is exclusion across the whole read/validate/write/commit interval, or an atomic revalidation at the write boundary.

Holding the guard while using an old snapshot is also insufficient. B must read state that includes A's committed acceptance after waiting, or restart. All acceptance, reopening, and publication writers must participate in the same protocol. A lock on an unrelated row creates no such exclusion.

## 3. Reopening with unchanged evidence

State changes from (7,2,empty) to (8,2,empty). A delayed request expecting (7,2) passes a revision-only comparison because both revisions are 2. It fails the epoch comparison because 7 differs from 8. Checking both fields at the same atomic decision boundary rejects it without altering the current round.

Let `Accepted(d,e)` be the set of accepted operation keys for document d and epoch e. The invariant is `|Accepted(d,e)| <= 1` for every historical epoch. Never clear an owner and reuse the epoch. Reopening creates a new epoch, and old receipts remain historical facts. An immutable evidence key still points to D17/2 even after D17/3 is published.

If an old request had already succeeded, replaying its operation key returns that previous receipt. It must not create another acceptance in epoch 8. Return enough information to distinguish “accepted in epoch 7” from “currently selected approval.” If the same key carries a different payload, reject the key reuse. The examples assume keys remain available for the entire possible retry period. Deciding that period is a deployment requirement.

## 4. Clock values and missing information

P increments from 0 to 1 for p1, then to 2 for p2. Q independently increments to 1 for q1. D receives q1 at `max(0,1)+1=2`, performs d2 at 3, receives p1 at `max(3,1)+1=4`, and rejects at 5.

The events p2 and d2 have timestamps 2 and 3 but no happened-before path in either direction. A clock comparison therefore does not prove causal dependence. In contrast, p1→d3 follows the actual message, and d3→d4 follows D's process order. The clock inequality holds along both edges and their transitive consequence.

The table's row placement is one possible display order, not an extra communication edge. A physical observer could record a chronology that is absent from the modeled processes' information. Neither a wall-clock timestamp nor a Lamport timestamp grants permission to accept an old epoch.

If D has only received one request, sorting its received set cannot distinguish a world with no other request from a world with an earlier request still delayed. A policy promising causal request order needs additional information or waiting assumptions. The pack's authority instead decides using validated current state. It promises the capacity and epoch invariants, without promising that the earliest sender wins.

## 5. The response and the effect are separate boundaries

Store the acceptance, exact evidence references, operation key, payload binding, and result in one database transaction. After an uncertain reply, query or retry that key. An identical accepted retry returns its receipt with no new consumption. An aborted transaction leaves no accepted receipt in this model. Durability of a successful commit still depends on S02's storage/failure assumptions.

A stable key stored in a worker's volatile memory is insufficient. Writing a receipt in a later transaction leaves a gap after acceptance in which a retry cannot find it. Writing a receipt first in a separate transaction can claim success even if the later acceptance fails.

Now send a payment before committing, then abort the database transaction. The payee may already have received the money while the local transaction disappears. Retrying can send again. Database rollback cannot reverse that external service's state. An atomic record of intent plus a dispatcher can make delivery recoverable, but duplicate delivery still requires a suitable receiver-side effect contract. C01 develops that boundary. This pack does not claim exactly-once payment from a local receipt or logical timestamp.

## 6. Multi-document scope and a decision

A holds D17 and wants D18. B holds D18 and wants D17. A waits for B and B waits for A. Neither can reach its release step unaided. Require every transaction to acquire guards in ascending document order, D17 then D18, and retain them through the combined commit. B then waits for D17 before it can hold D18, excluding the constructed cycle. Atomic acceptance of both reservations still requires one transaction encompassing both.

For one very hot document with short validations, begin by testing the guarded design because its waiting behavior and proof are simple. Keep slow extraction or remote requests outside the lock. A conditional transition is attractive when collisions are rare and validation is cheap to repeat. At high contention, aborted attempts may consume significant work. The recommendation is practitioner judgment to test, not a universal ranking.

Measure useful committed decisions, retries per success, wait-time distribution, transaction duration, and fairness under the same arrival pattern. A guard might cause unacceptable waits behind a slow holder, or optimistic retries might waste more time than waiting. Neither protocol proves a latency bound. The real database's conflict handling, recovery, and all write paths need validation before deployment.

**Assessment criteria.** A useful response supplies a concrete violating history, checks the aggregate invariant, identifies a protocol that excludes the history, and states the boundary of that protocol. It distinguishes serializability, causal order, wall-clock time, stale request validity, and external effects. Artifact checks do not establish learner mastery.

## Reproduce the finite checks

Run the following block under Python 3. Each two-candidate history contains three ordered operations per transaction. `R` takes a snapshot and decides, `W` stages that candidate's bit, and `C` commits the staged value. There are 20 interleavings preserving each transaction's order. In 18, both snapshots precede the other candidate's commit, so the model permits both acceptances. The two serial histories accept only one. These counts describe enumerated histories, not their probability in a real scheduler.

The guarded model uses a single indivisible current-state transition, representing the contract the implementation must supply. Its finite tests cannot prove a database implements that contract. The separate invariant argument is in the core pack.

```python
from itertools import combinations, permutations
from collections import Counter

# All interleavings of R,W,C for each of two candidates.
histories = []
for positions_a in combinations(range(6), 3):
    aset = set(positions_a)
    actors = ['A' if i in aset else 'B' for i in range(6)]
    pc = dict(A=0, B=0)
    history = []
    for actor in actors:
        history.append((actor, ('R','W','C')[pc[actor]]))
        pc[actor] += 1
    histories.append(history)

def snapshot_run(history):
    state = dict(A=0, B=0)
    decisions, staged = {}, {}
    for actor, operation in history:
        if operation == 'R':
            decisions[actor] = sum(state.values()) == 0
        elif operation == 'W':
            staged[actor] = int(decisions[actor])
        else:
            state[actor] = staged[actor]
    return state

assert len(histories) == 20
bad = sum(sum(snapshot_run(h).values()) > 1 for h in histories)
assert bad == 18
serial_a = [(a,s) for a in ('A','B') for s in ('R','W','C')]
serial_b = [(a,s) for a in ('B','A') for s in ('R','W','C')]
assert snapshot_run(serial_a) == dict(A=1, B=0)
assert snapshot_run(serial_b) == dict(A=0, B=1)

# Fixed-object precedence graph for the expanded violating history.
rw = [('A','R','a'), ('A','R','b'), ('B','R','a'),
      ('B','R','b'), ('A','W','a'), ('B','W','b')]
edges = set()
for i, (t1,op1,x1) in enumerate(rw):
    for t2,op2,x2 in rw[i+1:]:
        if t1 != t2 and x1 == x2 and 'W' in (op1,op2):
            edges.add((t1,t2))
assert edges == {('A','B'), ('B','A')}

# Single document. Each method is an assumed atomic guarded transaction.
# The receipt payload's rev stands for already-validated immutable evidence.
class Authority:
    def __init__(self):
        self.epoch, self.rev, self.owner = 7, 2, None
        self.receipts = {}  # key -> (actor, expected_epoch, expected_rev)

    def approve(self, key, actor, epoch, rev):
        payload = (actor, epoch, rev)
        if key in self.receipts:
            if self.receipts[key] != payload:
                raise ValueError('operation key reused for different inputs')
            return 'replay'
        if (epoch,rev) != (self.epoch,self.rev):
            return 'stale'
        if self.owner is not None:
            return 'occupied'
        self.owner = key
        self.receipts[key] = payload
        return 'accepted'

    def reopen(self, rev):
        self.epoch += 1
        self.rev, self.owner = rev, None

    def check(self):
        per_epoch = Counter(p[1] for p in self.receipts.values())
        assert all(n <= 1 for n in per_epoch.values())
        if self.owner is not None:
            assert self.receipts[self.owner][1:] == (self.epoch,self.rev)

for order in permutations(('A','B')):
    d = Authority()
    results = [d.approve(a,a,7,2) for a in order]
    assert results == ['accepted','occupied']
    d.check()

# A and B target epoch 7; C targets epoch 8. N reopens with the same revision.
for order in permutations(('A','B','C','N')):
    d = Authority()
    for op in order:
        if op == 'N':
            d.reopen(2)
        else:
            expected = 8 if op == 'C' else 7
            before = len(d.receipts)
            result = d.approve(op,op,expected,2)
            if result == 'accepted':
                assert d.epoch == expected and d.rev == 2
                assert len(d.receipts) == before + 1
            else:
                assert len(d.receipts) == before
        d.check()

d = Authority()
d.reopen(2)
assert d.rev == 2  # revision-only check would pass an old request
assert d.approve('old','A',7,2) == 'stale' and d.owner is None
assert d.approve('new','B',8,2) == 'accepted'

d = Authority()
assert d.approve('k','A',7,2) == 'accepted'
# Lost reply, retry, then reopen, and retry again.
assert d.approve('k','A',7,2) == 'replay'
d.reopen(3)
assert d.approve('k','A',7,2) == 'replay' and d.owner is None
assert len(d.receipts) == 1
try:
    d.approve('k','A',8,3)
except ValueError:
    pass
else:
    raise AssertionError('key reuse was accepted')
assert d.approve('wrongrev','B',8,2) == 'stale'
d.check()

# Clock trace and transitive happened-before closure.
clock = dict(P=0,Q=0,D=0)
timestamps = {}
events = [('p1','P',None), ('p2','P',None), ('q1','Q',None),
          ('d1','D','q1'), ('d2','D',None),
          ('d3','D','p1'), ('d4','D',None)]
hb, previous = set(), {}
for event,process,sent in events:
    if process in previous:
        hb.add((previous[process],event))
    if sent is not None:
        hb.add((sent,event))
        clock[process] = max(clock[process], timestamps[sent]) + 1
    else:
        clock[process] += 1
    timestamps[event] = clock[process]
    previous[process] = event
while True:
    closure = hb | {(a,d) for a,b in hb for c,d in hb if b == c}
    if closure == hb:
        break
    hb = closure
assert [timestamps[e] for e,_,_ in events] == [1,2,1,2,3,4,5]
assert all(timestamps[a] < timestamps[b] for a,b in hb)
assert ('p2','d2') not in hb and ('d2','p2') not in hb
assert timestamps['p2'] < timestamps['d2']
assert ('p1','d4') in hb

print('20 snapshot histories checked; 18 violate capacity.')
print('2 guarded orders and 24 reopen/request orders preserve capacity.')
print('Stale epoch/revision, replay, payload binding, and clocks passed.')
```

The 24 orders enumerate all placements of four modeled atomic calls, including a future-epoch request arriving before reopening. Such a request fails rather than forcing the authority to advance. The tests also cover accepted-key replay after a round ends. They do not prove fairness, bound network delay, or establish crash durability of a production implementation. No learner answers have been inferred.

## Revision history

- 1.0 — 2026-11-06. Six worked answers and executable finite-history, epoch, replay, and logical-clock checks.
---

# S04 — Hints, worked answers, and checks

| Field | Value |
| --- | --- |
| ID / revision / date | S04 answers · 1.1 · 2026-11-08 |
| Prerequisites | [Replication, consensus, and partial failure](SDE_S04.md), S03 and S02 |
| Capability developed | Separate replicated commitment, client knowledge and repeated business effects |
| Source-check status | R07 and R10 locators in the core pack |
| Experiment status | Python finite checks executed; no distributed deployment or complete protocol simulator |

## Hints

1. Write AB, AC and BC before making a general claim.
2. Separate where the entry exists from who knows it is committed.
3. Compare the surviving logs before holding an election.
4. Term is the first comparison key. An inherited entry retains its original term.
5. The operation key belongs to the business request, not the network connection.
6. A process can be alive while unreachable. A majority must be able to communicate.

## 1. An intersection needs a rule

The majorities are {A,B}, {A,C}, {B,C}. Distinct pairs intersect in A, B or C. For N members and q-member sets, their union has size at most N, so the intersection has size at least 2q−N. With N=3 and q=2 the bound is one. With N=5 and q=3 it is also one.

If A votes for both B and C in the same term, B+A and C+A can each claim a majority. Intersection has not helped because the shared member contradicted itself. Persisting the vote before responding is essential across restarts. The majority calculation also does not prove the elected log contains every committed entry; the log freshness restriction and log-matching properties supply further structure.

## 2. Three distinct observations

Entry 5 becomes committed once A, its term-2 leader, has durably replicated it on A+B. A learns that threshold was reached from B's successful response. B can still be unaware of commitment because no commit notification reached it. The client times out and cannot distinguish this history from one in which A never committed.

B wins term 3 with its own vote and C's. C has an older last log term. A candidate C cannot win using B because B's log is more up-to-date. In this particular trace A is down, so C's own vote is insufficient.

B's term-3 no-op at index 6 reaches B+C. B can advance its commit boundary through 6 under the current-term rule and apply entry 5 before 6. B reconstructs the acceptance and receipt even if it had never applied them before the election. An identical retry of k returns that receipt. The term-3 no-op does not change D17's epoch 7 or selected revision 2.

## 3. The local-only suffix

If only A stored entry 5 before crashing, B and C retain the common prefix through 4. B can win term 3 and append command j at index 5, then commit it on B+C. When A rejoins as a follower, an AppendEntries extension whose predecessor is (4,1) can replace A's conflicting term-2 entry with term-3 j.

No committed entry has been removed in this branch. A's success reply after only its local append would have been invalid because the promised result can disappear during valid failover. The correct client outcome before replicated commitment is still pending or failed/unknown, depending on the exact API contract; a timeout alone remains unknown.

## 4. Log freshness and an inherited entry

(term 3,index 6) is more up-to-date than (term 2,index 9), because term is compared first. Within the same last term, the higher last index wins. This is a log comparison, distinct from the candidate's current election term and distinct from a wall-clock timestamp.

R07 Figure 8 constructs a history in which a previous-term entry reaches a majority through later replication yet can still be overwritten. Therefore the general replica-count rule requires an entry from the current leader's term. Once that newer entry commits, the preceding prefix is committed with it. In the main case entry 5 had already committed under A; the extra step lets B establish a safe boundary without assuming knowledge it did not receive. It does not change the historical fact of commitment.

## 5. Replaying an identity

Retain k with its canonical input payload and result in replicated application state. Apply acceptance and receipt together. A repeat with matching inputs returns the stored result. A repeat with different inputs is an error. Retain enough receipt history to cover the supported retry period, including snapshots and restores. The lesson's model retains every receipt indefinitely; a bounded production policy must define what happens to expired keys.

After reopening, return “accepted in epoch 7” for k without consuming the new round. A fresh key targeting epoch 7 fails epoch validation. The key-reuse check must not silently reinterpret an old request against today's evidence.

A payment dispatcher can send once, crash before recording the response, then send again after recovery. The local receipt cannot prove how many effects the destination performed. Replicated intent helps recover pending work; safe retry at the payment boundary needs the destination's identity/effect contract or explicit reconciliation. Transport acknowledgements and application completion acknowledgements answer different questions.

## 6. Partition behavior and the choice

With A isolated from B+C, B+C can elect and commit once communication and scheduling stabilize. A cannot obtain a majority for a new entry. It may still believe it is leader, so authority-sensitive reads need the read protocol described in the core pack. With all three isolated, no group can form a majority. Stopping new commitments preserves safety while availability is lost.

A malicious server inventing successful replication acknowledgements, loss of required stable state, or divergent application logic violates the stated model. Correlated host or region failure can also remove more members than the tolerated number. Three members need two available; five need three. Measure failure domains, quorum write latency, election disruption and restoration behavior before paying for five. A larger member count is not evidence of a lower business outage rate without those assumptions.

**Assessment criteria.** A useful answer distinguishes stored, committed, applied and acknowledged; traces a valid election; preserves request identity; and states both a safety property and a limit on progress. It does not equate consensus with authorization or exactly-once external payment. These criteria do not record learner mastery.

## Executable checks

Run the block under Python 3. Log entries are (term, command) pairs in a one-based conceptual log. Prefix entries 1–4 are synthetic setup. The append helper models only the predecessor check and conflicting-suffix replacement. The commit helper models only the leader's current-term majority rule. Using its result as a commitment decision requires caller-provided match indexes to be truthful and durably acknowledged; the helper does not establish that premise. The synthetic input sweep below also includes unreachable protocol states to exercise the predicate. Elections, crashes, message delivery, persistent votes, snapshots and actual storage are not simulated.

```python
from itertools import combinations, product
from copy import deepcopy

# Exhaust all majority-pair intersections for three and five members.
pair_counts = []
for n in (3,5):
    q = n//2 + 1
    groups = [set(g) for g in combinations(range(n),q)]
    pairs = list(product(groups, repeat=2))
    assert all(len(a & b) >= 2*q-n for a,b in pairs)
    pair_counts.append(len(pairs))
assert pair_counts == [9,100]

# Lexicographic (last term,last index) vote freshness predicate.
def fresh(candidate, voter):
    return candidate >= voter
assert fresh((2,5),(1,4))
assert not fresh((1,4),(2,5))
assert fresh((3,6),(2,9))
assert not fresh((2,9),(3,6))
assert fresh((2,6),(2,5)) and fresh((2,5),(2,5))
assert not fresh((2,4),(2,5))

prefix = [(1,'setup'+str(i)) for i in range(1,5)]
x = (2,'approve-k')
def append(log, prev_index, prev_term, entries):
    out = list(log)
    if prev_index > len(out):
        return False, out
    if prev_index and out[prev_index-1][0] != prev_term:
        return False, out
    for index,entry in enumerate(entries, start=prev_index):
        if index < len(out) and out[index][0] != entry[0]:
            out = out[:index]
        if index == len(out):
            out.append(entry)
        else:
            # Raft's same-index/same-term command identity is assumed.
            assert out[index] == entry
    return True,out

def commit(log, term, matches, old=4):
    q = len(matches)//2 + 1
    candidates = [i for i in range(old+1,len(log)+1)
                  if log[i-1][0] == term
                  and sum(m >= i for m in matches) >= q]
    return max([old]+candidates)

A = prefix + [x]
B = list(prefix)
C = list(prefix)
ok,B = append(B,4,1,[x])
assert ok and commit(A,2,[5,5,4]) == 5
# B inherits entry 5, but its term-3 rule cannot count it directly.
assert commit(B,3,[5,5,4]) == 4
B.append((3,'noop'))
ok,C = append(C,4,1,B[4:])
assert ok and C == B
assert commit(B,3,[5,6,6]) == 6
# Duplicate RPC adds no entries. Incorrect predecessor is rejected.
assert append(C,4,1,B[4:]) == (True,C)
assert append(prefix,4,2,[x]) == (False,prefix)
assert append(prefix,5,2,[x]) == (False,prefix)
# Alternative branch: local-only x is replaced after valid successor election.
y = (3,'approve-j')
ok,repaired = append(A,4,1,[y])
assert ok and repaired == prefix+[y]
assert commit(A,2,[5,4,4]) == 4  # early reply cannot claim replicated commit

# Enumerate synthetic term/match-index inputs for the commitment predicate.
# Some combinations are unreachable in a valid leader state; this is not
# an enumeration of legal Raft executions or protocol-state coverage.
for term in (2,3):
    for matches in product(range(4,7),repeat=3):
        boundary = commit(B,term,matches)
        if boundary > 4:
            assert B[boundary-1][0] == term
            assert sum(m >= boundary for m in matches) >= 2

# Deterministic application state; all calls here represent committed commands.
def initial():
    return {'epoch':7,'rev':2,'owner':None,'receipts':{}}
def apply(s,key,epoch,rev,actor):
    payload = (epoch,rev,actor)
    if key in s['receipts']:
        old_payload,result = s['receipts'][key]
        if payload != old_payload:
            return 'key-conflict'
        return result
    if (epoch,rev) != (s['epoch'],s['rev']):
        result = 'stale'
    elif s['owner'] is not None:
        result = 'occupied'
    else:
        s['owner'] = key
        result = 'accepted-epoch-'+str(epoch)
    s['receipts'][key] = (payload,result)
    return result

a,b = initial(),initial()
for state in (a,b):
    assert apply(state,'k',7,2,'R') == 'accepted-epoch-7'
assert a == b
before = deepcopy(b)
assert apply(b,'k',7,2,'R') == 'accepted-epoch-7' and b == before
b.update(epoch=8,rev=3,owner=None)
assert apply(b,'k',7,2,'R') == 'accepted-epoch-7' and b['owner'] is None
assert apply(b,'k',8,3,'R') == 'key-conflict'
assert apply(b,'late',7,2,'R') == 'stale'
assert apply(b,'new',8,3,'R') == 'accepted-epoch-8'
restored = deepcopy(b)  # modeled snapshot includes receipts
assert apply(restored,'new',8,3,'R') == 'accepted-epoch-8'
assert restored == b
print('109 quorum pairs; freshness, append/repair, commit and retry checks passed.')
```

The commitment loop checks 54 synthetic term/match-index combinations, including unreachable states. For example, it passes current term 2 with a log containing a term-3 entry, which is not a valid leader state under Raft's monotonic term rules. It checks the predicate's output conditions; it neither establishes state reachability nor validates Raft's full safety proof. See R07 Figure 2, p. 4, and §§5.1, 5.4 in the core source ledger. The two crash branches are constructed histories with declared durable state, not injected machine failures. A production evaluation needs actual crash, partition, delayed-message and restoration tests, including observably correct client results.

## Revision history

- 1.0 — 2026-11-06. Six worked answers, finite protocol-component checks, and receipt replay checks.

- 1.1 — 2026-11-08. Audit B corrected the scope of the 54-input commitment check: synthetic predicate cases include unreachable states. Executable assertions and exercise answers unchanged; corrected block rerun successfully.
---

# S05 — Hints, worked answers, and reproducible checks

| Field | Value |
| --- | --- |
| ID / title | S05 answers · Queues, tail latency, and cloud elasticity |
| Revision / date | 1.0 · 2026-11-07 |
| Prerequisites | F02, F03, S01; [S05 core pack](SDE_S05.md) |
| Capability developed | Defend a capacity policy with an explicit workload, deadline, denominator and cost boundary |
| Source-check status | R08, R09 and R12 passages inspected; exact URLs and locators in the core evidence table and source register |
| Experiment status | Python checks below executed successfully on constructed inputs; no deployment benchmark |

These are model solutions, not a record of your answers or mastery. Try the six core exercises before opening the corresponding solutions. Alternative policies are valid when their assumptions, objective and accounting are explicit.

## Hints

1. A FIFO request waits until both its arrival and the preceding completion. Service duration is only part of response time. Apply the stated nearest-rank convention, not interpolation.
2. A rejected job consumes no reserved processing time in this model. Keep rejected requests in the offered population.
3. A pair releases two outputs together. With multiple workers, assign the next queued job to the earliest available worker, breaking availability ties by worker index.
4. Track work units, not request counts. Spare capacity is what drains backlog; full utilization alone does not drain it.
5. Compute the probability that none of the lookups is slow, then take its complement. State where independence enters.
6. Sum paid worker-hours, including startup. A useful replay must preserve the original arrivals when the service slows down.

## 1. FIFO, distributions and the missing waiting time

For costs `[1,1,4,1,1,1]`, all arriving at zero, starts and waiting times are `[0,1,2,6,7,8]`. Finishes and response times are `[1,2,6,7,8,9]`. The total service demand is nine worker-seconds, so mean service time is 9/6 = 1.5 seconds. Mean response time is 33/6 = 5.5 seconds; mean waiting time is 24/6 = 4 seconds. The identity mean response = mean waiting + mean service holds for this population.

Nearest-rank p50 takes observation `ceil(0.5*6)=3`, giving six seconds. p95 takes observation `ceil(0.95*6)=6`, giving nine. These are response percentiles across six offered, completed jobs from this constructed burst. A six-job p95 is its maximum and says little about the tail of a different workload.

Moving the four-second job to the end yields finishes `[1,2,3,4,5,9]`. Mean response falls to four seconds and timely completions increase from two to four without changing mean service demand. The test code checks all six positions of the long job: mean response ranges from 6.5 to 4 seconds, and timely counts range from one to four. An average service cost leaves ordering and arrival clustering unspecified.

**Assessment criterion:** Correct recurrence and population; distinction between service and response; an ordering or burst counterexample. An unexplained claim that “p95 is always the maximum” fails: it is true here because the population has six observations.

## 2. Admission and the denominator

| Job | Predicted finish if accepted | Decision | Reserved finish after decision |
| --- | ---: | --- | ---: |
| J1 | 1 | Accept | 1 |
| J2 | 2 | Accept | 2 |
| J3 | 6 | Reject | 2 |
| J4 | 3 | Accept | 3 |
| J5 | 4 | Accept | 4 |
| J6 | 5 | Reject | 4 |

Accepted IDs are J1, J2, J4 and J5. They finish at seconds 1, 2, 3 and 4. The offered-request timely fraction is 4/6; the completed-request timely fraction is 4/4. Neither fraction alone describes every outcome. Report two rejections, zero late completions and four worker-seconds of busy work.

For a concrete estimation failure, predict every job costs one second. The rule admits J1 through J4 and rejects J5 and J6. Actual processing still takes costs `[1,1,4,1]`, finishing at `[1,2,6,7]`. Only two of six offered jobs finish on time. Admission is a policy using information; an optimistic estimate is not a guarantee. Rejection checks, retries and request-value differences are additional costs deliberately excluded from the baseline model. R09 chapter 21 explains why real rejection can itself consume meaningful resources.

**Assessment criterion:** Track reservations after a rejection; retain the offered denominator; show a concrete failure of a stated assumption. Do not claim that all overload should be rejected or that the long job lacks value.

## 3. Batching, capacity and startup

Adjacent pair durations are 1.5, 4.5 and 1.5 seconds. Their cumulative finishes are 1.5, 6 and 7.5. Since both outputs are released at each pair completion, per-job finishes are `[1.5,1.5,6,6,7.5,7.5]`. Pair mode does 7.5 worker-seconds of busy work, saving 1.5 relative to FIFO, yet still has only two timely completions. The short J4 inherits the long J3's batch completion. No assembly delay occurs because every request was already waiting; a staggered arrival workload would need a batch timeout rule.

With two workers ready at zero, worker 0 handles J1 from 0–1 and J3 from 1–5. Worker 1 handles J2 from 0–1, J4 from 1–2, J5 from 2–3 and J6 from 3–4. In job order, finishes are `[1,1,5,2,3,4]`. Five are timely; busy work remains nine worker-seconds.

With worker 1 ready only at second two, worker 0 executes J1 from 0–1, J2 from 1–2 and J3 from 2–6. The worker-index tie rule assigns J3 to worker 0. Worker 1 executes J4 from 2–3, J5 from 3–4 and J6 from 4–5. Finishes are `[1,2,6,3,4,5]`; four are timely. The final completion is at six, even though J6 finishes at five: always take the maximum completion, not the final array element.

**Assessment criterion:** Correct pair release semantics and worker assignment; count outcomes against the same deadline; distinguish busy worker-seconds from provisioned and billed capacity. A faster drain is useful but does not establish a better user outcome for every request.

## 4. Backlog and spare capacity

During the four-second burst, net input is `3−2=1` work unit per second. Thus Q(4)=4. Afterward spare capacity is `2−1=1` unit per second, and the backlog drains in four additional seconds, at t=8.

| Time t (seconds) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Outstanding work Q(t) | 0 | 1 | 2 | 3 | 4 | 3 | 2 | 1 | 0 |

If arrivals fall only to two units/s, input equals capacity and the accumulated four units remain. If arrivals stay above two, backlog grows. If the system is empty and arrivals are below capacity, unused capacity disappears rather than making Q negative. This is a deterministic fluid model; it is not a stochastic queue or a per-request latency simulator.

**Assessment criterion:** Correct units and time origin; explain that recovery needs spare capacity. A long-window mean arrival rate below capacity can coexist with short-window deadline misses.

## 5. Fan-out and correlation

Under the independent model, each lookup is fast enough with probability 0.98. All 20 are fast enough with probability `0.98^20`. The complete request exceeds d with probability `1−0.98^20 = 0.332392…`, or about 33.24%.

For the perfectly correlated construction, all lookups exceed d in the same two percent of requests. The whole request therefore exceeds d with probability 0.02. Every component retains the same marginal exceedance as before, but the joint distribution changes. Correlation cannot be ignored; these two constructions alone do not specify every possible dependence pattern.

Measure latency for complete original user operations over a specified window and workload, starting at original arrival and ending at the promised complete result. Separately record rejected, failed, timed-out and retried operations. If calculating a percentile only for completed operations, label that conditional population and also report the offered-operation success rate. Do not silently treat timeout duration as a successful completion, omit incomplete operations, or average component percentiles. Component-level distributions remain useful diagnostics, not substitutes for the user clock.

**Assessment criterion:** Show the complement and independence assumption, supply the correlated counterexample, and define the measured population. The 33.24% is a calculated teaching case, not R08's reported benchmark.

## 6. Capacity charges and evidence that changes the policy

Fixed provisioning buys `6*10=60` worker-hours. Ideal elasticity buys `2*9+6*1=24`. If elastic unit price is p times the fixed unit price, break-even is `24p=60`, so p=2.5. Elasticity is cheaper below that threshold, equal at it, and more expensive above it under these assumptions.

Four extra workers each incur 0.25 paid startup hours. That adds one worker-hour, giving 25 and break-even `60/25=2.4`. This assumes baseline capacity is ready initially and the peak is anticipated; the extra startup is inside the accounting boundary. It excludes minimum billing units, commitments, network costs, operational labor and the value lost when deadlines are missed. It is not a current cloud quote or a profit calculation.

A bounded replay could compare a warm baseline plus scaling against a larger always-ready pool. Predeclare the useful-outcome deadline, correctness requirement and offered-operation denominator. Replay identical timestamped arrivals and payload costs, including several bursts shorter than measured startup time, a sustained peak and a post-peak drain. Record ready capacity over time, startup work, queue depth in both requests and estimated work units, paid capacity, original-operation latency, rejections, late completions, failed attempts and retries. Keep retry budgets and cancellation behavior explicit; do not let a response-driven load generator reduce offered load when latency rises.

If short frequent bursts cause unacceptable misses before additional workers become ready, and the value of avoiding those misses exceeds the headroom charge, increase warm capacity. If long deadlines and sparse peaks permit buffering without loss of useful outcomes, favor a smaller baseline. If rejection and retries amplify overload, change admission and retry behavior before interpreting a scaling comparison. Different value by request class may call for reservations or a revised objective. These are decision rules, not measured findings. Real observations must supply the costs and acceptance limits.

**Assessment criterion:** Correct capacity arithmetic and a test capable of falsifying the recommendation. The replay must account for failures, startup and work spent on retries; aggregate successful-request latency alone is insufficient.

## Executed checks and limits

Run the following with Python 3; it needs only the standard library. It checks the worked traces using exact rational arithmetic, compares FIFO with independently accumulated service costs, varies all six placements of the long job, checks admission under cost underestimation, validates the two capacity traces and busy-work conservation across five startup values, and verifies fluid conservation, probability and cost thresholds.

These finite deterministic checks establish consistency of the examples. They do not establish queue stability under a random process, estimate a production tail, validate an implementation's scheduler, measure rejection overhead or prove a policy optimal. No simulated result is treated as learner evidence.

```python
from fractions import Fraction as F
from itertools import accumulate
from math import ceil
import heapq

costs = [1, 1, 4, 1, 1, 1]
deadline = 4

def schedule(work, ready):
    workers = [(F(t), i) for i, t in enumerate(ready)]
    heapq.heapify(workers)
    starts, finishes = [], []
    for cost in work:  # all arrivals zero; ID order; worker-index tie break
        start, worker = heapq.heappop(workers)
        finish = start + cost
        starts.append(start)
        finishes.append(finish)
        heapq.heappush(workers, (finish, worker))
    return starts, finishes

def timely(finishes):
    return sum(t <= deadline for t in finishes)

starts, fifo = schedule(costs, [0])
assert fifo == list(accumulate(costs)) == [1, 2, 6, 7, 8, 9]
assert starts == [0, 1, 2, 6, 7, 8]
assert sum(fifo) / 6 == F(11, 2)
assert sum(costs) == 9
assert sorted(fifo)[ceil(F(1, 2) * 6) - 1] == 6
assert sorted(fifo)[ceil(F(95, 100) * 6) - 1] == 9
assert timely(fifo) == 2
# Six distinct positions of the long job: same service distribution.
means, successes = [], []
for position in range(6):
    work = [1] * 6
    work[position] = 4
    _, finish = schedule(work, [0])
    assert finish == list(accumulate(work))
    means.append(sum(finish) / 6)
    successes.append(timely(finish))
assert means == [F(13, 2), 6, F(11, 2), 5, F(9, 2), 4]
assert successes == [1, 1, 2, 3, 4, 4]

reserved = 0
accepted, rejected = [], []
for job, cost in enumerate(costs, 1):
    if reserved + cost <= deadline:
        reserved += cost
        accepted.append(job)
    else:
        rejected.append(job)
assert accepted == [1, 2, 4, 5] and rejected == [3, 6]
assert schedule([costs[j-1] for j in accepted], [0])[1] == [1, 2, 3, 4]
# If predicted costs are all one, the first four are admitted.
assert schedule(costs[:4], [0])[1] == [1, 2, 6, 7]
assert timely(schedule(costs[:4], [0])[1]) == 2

pair_costs = [F(1, 2) + max(costs[i:i+2]) for i in range(0, 6, 2)]
pair_finishes = list(accumulate(pair_costs))
batch = [t for t in pair_finishes for _ in range(2)]
assert batch == [F(3, 2), F(3, 2), 6, 6, F(15, 2), F(15, 2)]
assert sum(pair_costs) == F(15, 2) and timely(batch) == 2
assert schedule(costs, [0, 0])[1] == [1, 1, 5, 2, 3, 4]
assert schedule(costs, [0, 2])[1] == [1, 2, 6, 3, 4, 5]
assert timely(schedule(costs, [0, 0])[1]) == 5
assert timely(schedule(costs, [0, 2])[1]) == 4
for readiness in range(5):
    begin, end = schedule(costs, [0, readiness])
    assert sum(e-b for b, e in zip(begin, end)) == 9

q, trace = 0, [0]
for second in range(8):
    arrivals = 3 if second < 4 else 1
    served = min(q + arrivals, 2)
    next_q = q + arrivals - served
    assert next_q >= 0 and next_q + served == q + arrivals
    q = next_q
    trace.append(q)
assert trace == [0, 1, 2, 3, 4, 3, 2, 1, 0]
assert max(0, 4 + 2 - 2) == 4  # equal rates do not drain backlog
fanout = 1 - F(98, 100)**20
assert round(float(fanout), 4) == 0.3324
assert fanout > F(2, 100)
fixed, elastic = 6 * 10, 2 * 9 + 6
startup = 4 * F(1, 4)
assert (fixed, elastic, elastic + startup) == (60, 24, 25)
assert F(fixed, elastic) == F(5, 2)
assert fixed / (elastic + startup) == F(12, 5)
print('PASS: FIFO, six reorderings, admission and estimation failure, batches,')
print('two-worker traces, five startup cases, fluid conservation, fan-out, costs.')
print('Fluid backlog at integer seconds:', trace)
print('Independent fan-out exceedance:', round(float(fanout), 6))
```

Observed output on 2026-11-07:

```text
PASS: FIFO, six reorderings, admission and estimation failure, batches,
two-worker traces, five startup cases, fluid conservation, fan-out, costs.
Fluid backlog at integer seconds: [0, 1, 2, 3, 4, 3, 2, 1, 0]
Independent fan-out exceedance: 0.332392
```

## Revision history

- 1.0 — 2026-11-07. Six worked solutions, hints, assessment criteria and executed checks. All inputs are constructed; actual arrivals, service costs, correlations, resource constraints and pricing remain application questions.
---

# S06 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| ID / revision / date | S06 answers · 1.0 · 2026-11-08 |
| Prerequisites | S03–S05, C01 and [S06 core](SDE_S06.md) |
| Capability developed | Evaluate authority and availability separately, with an explicit outcome population |
| Source-check status | R09, R11 and R10 passages inspected; URLs and exact locators in the core evidence table |
| Experiment status | Executed finite Python checks below; no live fault injection or security certification |

These are reference solutions, not inferred learner responses. Try the six exercises first.

## Hints

1. An arrow is an intended interface. Ask which credential could bypass it.
2. Place the authorization check and the protected effect on the same ordered timeline.
3. Preventing a mutation is narrower than preventing all harm.
4. Start with original eligible operations; count the union of bad outcomes.
5. Track worker availability, then distinguish occupied time from paid capacity.
6. Define what must remain unchanged before injecting any failure.

## 1. Principals and paths

The core diagram puts reviewer identity and proposal data on separate inputs to the approval authority. Current policy and trusted object metadata supply authorization facts. The authority alone commits approval receipts and payment intents; the dispatcher consumes committed intents. The proposal worker receives only its job's evidence subset and cannot grant itself approval rights.

Two bypass examples are a maintenance script with unrestricted write credentials and a batch endpoint that writes approvals without invoking the same checks. A third is a read endpoint that trusts a caller-supplied tenant rather than matching trusted object metadata. All require explicit controls and tests; the drawing does not supply them. The policy administrator is not automatically authorized to read evidence or pay invoices.

**Criteria:** Distinct accountable principals, objects and actions; at least two concrete bypasses; no reliance on a model's declared actor identity.

## 2. Revocation and cached permission

If approval commits before revocation, it was authorized at the modeled decision boundary and remains historical fact. Revocation alone cannot undo its external consequences. If revocation commits first, a later new approval must be denied and create no receipt of acceptance or payment intent.

The bad sequence is page check at v=10, revocation at v=11, delayed request using cached allow from v=10, then unguarded commit. It violates the selected current-authority contract. A valid repair orders revocation and decision through one authority, or validates the policy version atomically with the protected commit. Logging v=10 after committing is diagnostic information, not a repair.

Historical receipt retrieval is also an access. Check current permission to read it before disclosure. Do not execute its old effect again merely to answer a status question. Lack of a current grant and inability to establish policy are different reasons, but neither authorizes the mutation in this design.

**Criteria:** Both orders, concrete failure trace and atomicity premise; distinguish denial, deferral and undo.

## 3. A forbidden model proposal

A tenant A proposal-worker identity cannot approve tenant B's document, even if generated JSON claims `actor=admin`. The authority evaluates verified context and trusted object ownership. It rejects the request without altering the owner, acceptance receipt or payment-intent state.

The worker may still generate a misleading draft or consume its resource allocation. It may expose data already granted to its context through an allowed output path. These harms call for evidence-quality evaluation, restricted read/output scope and resource limits. They are not excluded by the approval guard. Compromise of the authority itself also lies outside this finite model.

A retry of the same forbidden request cannot repair authorization. Adding replicas or raising a timeout likewise cannot grant permission. An authorized human may make a factually wrong choice: the authorization invariant does not prove decision correctness.

**Criteria:** State exactly which state remains unchanged and identify two residual harms; do not equate denial with complete system safety.

## 4. SLI and error budget

Good/eligible is `9,960/10,000 = 99.6%`. The 99.5% target allows 50 bad operations in that completed fixed-size population. The 25 late plus 15 unavailable operations are disjoint here, so 40 are bad and ten remain relative to the allowance. The extra 20 distinct bad operations produce 60 bad, 99.4% good and a ten-operation excess.

If late and incorrect sets overlap, use their union. For example, late `{1,2,3}` and incorrect `{3,4}` contain four bad operations, not five. A retry can improve the original operation's outcome only if the required result arrives within its original deadline; it does not create another denominator entry to dilute failures.

A policy-service outage for a predeclared eligible request counts against useful completion. Calling it a policy denial and excluding it would improve the chart while users receive less service. Genuine forbidden requests need separate tracking so the service is not rewarded for granting access to them. If authorization changes during a measurement window, define that classification rule before comparing results. The numerical example avoids this complication by holding grants constant.

An unauthorized disclosure requires investigation independently of the availability budget. No observed incidents is incomplete evidence, especially when instrumentation has gaps.

**Criteria:** Correct arithmetic, population, time window and original-operation clock; no security-violation allowance inferred from availability tolerance.

## 5. Capacity isolation and cost

With four shared workers, A's four jobs occupy every worker from 0 to 10. B begins at 10 and ends at 11. With two reserved workers per tenant, A's first pair ends at 10 and second pair at 20; B ends at 1. The last A completion worsens by ten seconds, while B improves by ten. Total busy work is unchanged at 41 worker-seconds, but reserved idle capacity may still be billed.

A common database connection pool or storage throttle can defeat the expected isolation even with separate CPU pools. Conversely, separate credentials limit authority but do not reserve worker time.

Three additional milliseconds per operation across 10,000 operations is 30,000 milliseconds, or 30 CPU-seconds in the assigned model. Concurrency, resource saturation and queueing determine elapsed time. This number cannot justify a fixed latency increase or current cost estimate without measurements.

**Criteria:** Trace assignments correctly; distinguish work, elapsed time and billed capacity; identify a specific remaining shared dependency.

## 6. Bounded validation plan

Use an isolated test environment with synthetic tenant A/B data and no live payment destination. Establish authorized controls that should succeed and cross-tenant/model-worker controls that must fail. Interrupt policy availability while submitting new approvals. Observe unavailable/denied reasons, protected-state deltas, ingress/outcome counts, latency and audit completeness. The required result is no new unverified approval; useful completion may fall. Stop immediately if an unauthorized state change, disclosure, or unintended external call occurs. Restore policy and verify that ordinary authorized requests recover without replaying old effects.

For overload, replay the same timestamped A burst and B traffic into shared and reserved pools, with the same deadlines, resource budget and original-operation IDs. Include rejects, late completions and retries. Measure database contention as well as worker occupancy. Stop at predeclared resource or queue bounds. If reserved pools waste substantial paid capacity and B meets its target under a fair shared scheduler, reconsider rigid reservation. If shared dependencies keep B slow in both cases, isolate or control that dependency before buying more workers.

This is a proposed deployment test, not one performed here. Actual measurements, approved limits and environment isolation are required. Finite arithmetic cannot select a production design.

**Criteria:** Observable outcomes, explicit invariant, safe scope, stop conditions and evidence that could reverse the choice. Tests that merely assert a successful HTTP response are insufficient.

## Reproduce the executed checks

The predicate check enumerates all 256 combinations of eight premises and verifies that only the all-true case can change protected state. It assumes the transition is indivisible and the premises truthful; it does not test authentication, policy synchronization or database isolation. The two revocation orders show the chosen contract, while the cached-allow case exhibits a violating premise. Scheduling checks implement the stated all-at-zero FIFO model. These are constructed cases, not frequency estimates or a security proof for deployed code.

```python
from itertools import product, permutations
from fractions import Fraction as F
import heapq

def decide(flags, state):
    # Eight premises from the lesson; one indivisible transition assumed.
    if not all(flags):
        return 'denied'
    if state['owner'] is not None:
        return 'occupied'
    state.update(owner='R', receipts=1, intents=1)
    return 'accepted'

accepted = 0
for flags in product((False, True), repeat=8):
    state = dict(owner=None, receipts=0, intents=0)
    before = state.copy()
    result = decide(flags, state)
    if False in flags:
        assert result == 'denied' and state == before
    else:
        accepted += 1
        assert result == 'accepted' and state['intents'] == 1
        assert decide(flags, state) == 'occupied'
assert accepted == 1

for order in permutations(('approve', 'revoke')):
    grant, effects = True, 0
    for event in order:
        if event == 'revoke':
            grant = False
        elif grant:
            effects += 1
    assert effects == (1 if order[0] == 'approve' else 0)
# Stale cached permission admits after revocation: counterexample.
cached_allow, current_grant = True, False
assert cached_allow and not current_grant
# No authoritative policy available: selected mutation contract denies.
assert decide((True, False, True, True, True, True, True, True),
              dict(owner=None, receipts=0, intents=0)) == 'denied'

n, good = 10000, 9960
assert F(good, n) == F(996, 1000)
allowed = n * (1-F(995,1000))
assert allowed == 50 and n-good == 40 and allowed-(n-good) == 10
assert F(good-20, n) == F(994,1000)
assert (n-good+20)-allowed == 10
late, incorrect = {1,2,3}, {3,4}
assert len(late | incorrect) == 4  # not five failures
assert F(3,1000)*n == 30  # added CPU-seconds

def finish(costs, workers):
    ready=[(0,i) for i in range(workers)]
    heapq.heapify(ready)
    out=[]
    for cost in costs:
        t,i=heapq.heappop(ready)
        out.append(t+cost)
        heapq.heappush(ready,(t+cost,i))
    return out
assert finish([10,10,10,10,1],4)==[10,10,10,10,11]
assert finish([10,10,10,10],2)==[10,10,20,20]
assert finish([1],2)==[1]
assert sum([10,10,10,10,1])==41
print('PASS: 256 predicate cases, both revocation orders, stale-cache counterexample;')
print('SLO, budget, overlap and CPU arithmetic; shared/reserved worker traces.')
```

Observed output on 2026-11-08:

```text
PASS: 256 predicate cases, both revocation orders, stale-cache counterexample;
SLO, budget, overlap and CPU arithmetic; shared/reserved worker traces.
```

## Revision history

- 1.0 — 2026-11-08. Six answers, hints, criteria and executed finite checks. Learner readiness and mastery remain unknown.
---

# A01 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| ID / revision / date | A01 answers · 1.0 · 2026-11-09 |
| Prerequisites | F02–F04 and [A01 core](SDE_A01.md) |
| Capability developed | Defend what a score establishes and repair the information boundary of an evaluation |
| Source-check status | R13 and R02 inspected passages and URLs in the core evidence table |
| Experiment status | Exact standard-library Python checks executed below; no production prediction experiment |

These are reference solutions, not learner responses or evidence of mastery.

## Hints

1. Expand each squared residual. Keep the penalty separate from reported unpenalized MSE.
2. Use frozen parameters; do not fit to the final labels.
3. Ask whether the lookup key was already observed with a label.
4. Shared membership is transitive through graph paths, even without a direct shared attribute.
5. Split before fitting transformations. Arrival time and label-availability time differ.
6. Weight losses, not winners. Then ask whether conditional losses remain stable.

## 1. Fitting and regularization

For a constant c, training MSE is ((c−2)²+(c−4)²)/2 = (c−3)²+1, minimized at c=3. Its training and validation MSEs are 1 and 2.5. For wx, training loss is 2.5(w−2)². Adding λw² and setting the derivative 5(w−2)+2λw to zero gives w=10/(5+2λ). Positive curvature establishes a minimum.

For weights 2, 1, 0.5, the training MSEs are 0, 2.5, 5.625 and validation MSEs are 2.5, 0, 0.625. Report these prediction losses, not penalized objective values, when comparing on a common validation criterion. The baseline is fitted from training labels only.

Changing minutes to seconds multiplies label scale and fitted weights. Rescaling pages changes the numerical weights and penalty effect. Replacing mean squared loss with a sum also changes relative penalty strength. A λ value without its objective and feature units is incomplete.

**Criterion:** Correct residuals, unique minimum, explicit loss scaling; do not claim regularization must improve every dataset.

## 2. Selection and final evidence

Validation selects λ=2.5 and w=1 among the declared candidates. On final inputs 3 and 4 with targets 3 and 4, predictions are exact: MSE=MAE=0. The baseline predicts 3 for both: MSE=0.5 and MAE=0.5 minutes.

If final labels become 6 and 8 without changing the model, residuals are −3 and −4. MSE=12.5 and MAE=3.5. The baseline has residuals −3 and −5, giving MSE=17 and MAE=4. The unpenalized model would be exact on these changed labels. Thus validation selection is not a guarantee under a changed input–outcome relationship. Two constructed test cases cannot establish deployment accuracy or uncertainty.

**Criterion:** Freeze weights, distinguish the selected candidate from a hindsight winner, and state the test's limited population.

## 3. Revisions and memorization

Training on r1 of all four documents stores D1→2, D2→4, D3→6, D4→8. Every r2 lookup returns its assigned target, yielding zero MSE. The example has eight rows but only four underlying documents. The row allocation has no entirely unseen validation documents.

Training on D1/D2's four revision rows gives mean (2+2+4+4)/4=3. Unknown D3/D4 receive 3. Squared errors are 9,9,25,25, averaging 17. The constant baseline does exactly the same. There are two held-out documents, not four independent validation cases, and even those may share supplier/template effects. Do not form a confidence interval treating all revision rows as independent draws.

**Criterion:** Explain the task mismatch, not merely the numerical score change. Reusing known documents is not inherently forbidden if that is the actual application and labels truly existed at prediction time; it is wrong evidence for the stated new-document question.

## 4. Overlapping groups

A links D1 to D2; B links D3 to D4; template X links D1 to D3. The resulting path connects all documents. Holding out B separates organizations but leaves template X shared. Grouping by (A,X) and (B,X) as different pairs still shares X; grouping (A,X) and (A,Y) separately still shares A.

There is one connected component, so a nonempty train/test split cannot keep both organizations and templates disjoint. Acquire disconnected groups, restrict the intended claim to new organizations with known templates, or report the desired estimate unavailable. Dropping bridging records can create a different, selected population; document any exclusion and do not claim it represents all intake.

**Criterion:** Show the connecting path and acknowledge infeasibility rather than quietly weakening the holdout.

## 5. An evaluation plan that matches deployment

For future documents from existing suppliers, choose a historical fitting cutoff and a later test-intake window. Fit only on documents whose labels were available by cutoff. Keep a whole document family in one partition; declare boundary-crossing families excluded from this evaluation and count them separately. Reconstruct page counts and other permitted features at original intake, without later corrections. Track unknown suppliers separately from the intended existing-supplier population.

Within the pre-test period use earlier-to-later development splits with the same label-availability rule. Fit preprocessing and each candidate only on that fold's training data. Compare the training-mean baseline with the page predictor and predeclared penalty grid. Choose using development MSE, report MAE and severe underestimation, then freeze all choices. If refitting on development data, evaluate the actual refit on the untouched final period. Record failed/missing predictions and delayed labels under declared rules rather than dropping them.

For new suppliers with unseen templates, reserve entire disconnected organization/template components, keeping every document's revisions together. The development procedure must use analogous component holdouts. Add a time cutoff if future deployment is also part of the claim. Confirm enough separate components exist; this toy dataset fails that feasibility check. Report both case-weighted and, if relevant, organization-weighted outcomes with explicit denominators. More rows from one organization do not supply more independent organizations.

**Criterion:** Decision-time inputs, label maturity, group/time boundaries, training-only transformations, baseline and final lock. There is no compulsory 80/20 split: the number and representativeness of independent groups matter.

## 6. Workload change and the decision

Let r be routine share. P's loss is r+9(1−r)=9−8r; Q's is 4. P wins for r>5/8, ties at 5/8 and loses below it. At r=0.9 its MSE is 1.8; at r=0.5 it is 5.

Reweighting assumes unchanged subgroup losses. If reviewer tooling changes minutes per page within routine cases, the old conditional MSEs may no longer apply. Newly matured labels showing that within-group change would invalidate simple reweighting. Input drift without outcomes is an alert to investigate, not a measured error increase.

Better minute predictions do not by themselves prove better schedules. Queue policies, reviewer behavior and opportunity costs intervene. A controlled workflow evaluation using F03's unit, outcome and interference discipline is needed for a causal benefit claim.

**Criterion:** Correct threshold, a concrete failed assumption and separation of predictive quality from customer impact.

## Executed checks

The following uses Python's standard library. It checks the constructed arithmetic, the memorization counterexample, component feasibility and a metamorphic independence check: changing final labels cannot change selection that consumes only training/validation data. It does not estimate sampling uncertainty or validate a production data pipeline.

```python
from fractions import Fraction as F
from itertools import product

train = [(1,2),(2,4)]
valid = [(1,1),(2,2)]
test = [(3,3),(4,4)]
def mse(data, predict):
    return sum((predict(x)-y)**2 for x,y in data)/F(len(data))
def mae(data, predict):
    return sum(abs(predict(x)-y) for x,y in data)/F(len(data))
mean = sum(F(y) for x,y in train)/len(train)
assert mean == 3
assert (mse(train,lambda x:mean),mse(valid,lambda x:mean)) == (1,F(5,2))
lambdas = [F(0), F(5,2), F(15,2)]
weights = [F(10)/(5+2*l) for l in lambdas]
assert weights == [2,1,F(1,2)]
assert [mse(train,lambda x,w=w:w*x) for w in weights] == [0,F(5,2),F(45,8)]
assert [mse(valid,lambda x,w=w:w*x) for w in weights] == [F(5,2),0,F(5,8)]
for l,w in zip(lambdas,weights):
    assert 5*(w-2)+2*l*w == 0
    for d in [F(-1),F(-1,10),F(1,10),F(1)]:
        objective=lambda z:mse(train,lambda x:z*x)+l*z*z
        assert objective(w+d)>objective(w)
def select(validation):
    return min(weights,key=lambda w:mse(validation,lambda x:w*x))
w=select(valid)
assert w==1 and mse(test,lambda x:w*x)==mae(test,lambda x:w*x)==0
assert mse(test,lambda x:mean)==mae(test,lambda x:mean)==F(1,2)
changed=[(3,6),(4,8)]
assert mse(changed,lambda x:w*x)==F(25,2)
assert mae(changed,lambda x:w*x)==F(7,2)
# Final labels never enter selection, even under 25 alternate target pairs.
for y1,y2 in product(range(5),repeat=2):
    alternate_test=[(3,y1),(4,y2)]
    assert select(valid)==w

# doc, organization, template, revision, target; fixed two-page inputs.
docs=[('D1','A','X',2),('D2','A','Y',4),('D3','B','X',6),('D4','B','Z',8)]
rows=[(d,o,t,r,F(y)) for d,o,t,y in docs for r in [1,2]]
def lookup_mse(tr,va):
    memory={r[0]:r[4] for r in tr}
    fallback=sum(r[4] for r in tr)/len(tr)
    return sum((memory.get(r[0],fallback)-r[4])**2 for r in va)/len(va)
assert lookup_mse([r for r in rows if r[3]==1],[r for r in rows if r[3]==2])==0
tr=[r for r in rows if r[1]=='A'];va=[r for r in rows if r[1]=='B']
assert lookup_mse(tr,va)==17
assert not {r[0] for r in tr}&{r[0] for r in va}
assert not {r[1] for r in tr}&{r[1] for r in va}
assert {r[2] for r in tr}&{r[2] for r in va}=={'X'}
# Enumerate all 14 nonempty document partitions: none separates both axes.
feasible=[]
for mask in range(1,15):
    left=[d for i,d in enumerate(docs) if mask>>i&1]
    right=[d for i,d in enumerate(docs) if not mask>>i&1]
    if all(not {d[k] for d in left}&{d[k] for d in right} for k in [1,2]):
        feasible.append(mask)
assert feasible==[]
for r,expected in [(F(9,10),F(9,5)),(F(1,2),F(5)),(F(5,8),F(4))]:
    assert r+9*(1-r)==expected
print('PASS: fitting, penalties, validation/test arithmetic, 25 label changes,')
print('revision leakage, grouped MSE, all 14 group partitions and mixture threshold.')
```

## Revision history

- 1.0 — 2026-11-09. Six reference answers and executed exact checks; no learner performance inferred.
---

# A02 — Hints, worked answers and executable checks

| Field | Value |
| --- | --- |
| ID / revision / date | A02 answers · 1.0 · 2026-11-09 |
| Prerequisites | F04, A01 and [A02 core](SDE_A02.md) |
| Capability developed | Verify attention arithmetic and test information-flow boundaries without overstating model evidence |
| Source-check status | R14 versioned passages and locators in the core evidence ledger |
| Experiment status | Standard-library Python checks executed; no neural model training, benchmark or generation experiment |

These are reference solutions for later self-assessment, not inferred learner answers.

## Hints

1. Multiply rows by projection columns before forming query/key products.
2. Recompute the denominator after changing permitted keys.
3. Check whether the changed coordinate participates in WQ or WK.
4. The output retains query count and value width.
5. Write each input next to its target before discussing parallel computation.
6. Count allocated pairs separately from permitted pairs and measured work.

## 1. Full-context attention

WQ and WK select the first feature: Q=K=[1,0,1]ᵀ. WV preserves both features, so V=X. S has rows [1,0,1], [0,0,0], [1,0,1]. Because dk=1, scaling makes no numerical change in this case; it is still part of the general formula.

With Z=2e+1, rows 1 and 3 of A are [e/Z,1/Z,e/Z]; row 2 is [1/3,1/3,1/3]. Outputs 1 and 3 are (2e/Z,(2+e)/Z), approximately (0.844638,0.733044); output 2 is (2/3,1). Row normalization distributes one query's mass across keys. Column normalization would answer a different algebraic question and is not this contract.

**Criterion:** Correct projection and multiplication order, normalization axis and value-weighted output. Attention weights are not vocabulary probabilities or truth estimates.

## 2. Mask before normalization

Causal rows are [1,0,0], [1/2,1/2,0] and [e/Z,1/Z,e/Z]. Their outputs are (1,0), (1/2,1) and the original third output. Disallowing key 2 for query 3 leaves two equal scores, producing [1/2,0,1/2] and (1,1/2). Rows 1 and 2 are unaffected by that single connection change.

If row 2 is normalized over all three positions first and the final weight is then zeroed, the remaining weights are [1/3,1/3,0]. Their sum is 2/3 and the output is (1/3,2/3). Renormalizing the surviving positive weights would repair this particular finite example, but masking before the stable softmax directly implements the declared contract. All-masked rows have no valid distribution; the code rejects them.

**Criterion:** Show the changed denominator and distinguish a forbidden connection from a small score.

## 3. Future-value perturbation

Changing X3's second coordinate from 1 to 7 leaves Q/K unchanged because their projections use only the first coordinate. V3 increases by (0,6). Unmasked output differences are (0,6e/Z), (0,2), (0,6e/Z). Causal differences are (0,0), (0,0), (0,6e/Z).

With projections that use the second coordinate, K3 and Q3 may change too. Causality still excludes position 3 from outputs 1 and 2 if their inputs were causally constructed, but the third output's difference would not generally equal a fixed weight times 6. If earlier representations already encoded future content, their queries or permitted values could change, violating the premise of this layer-local argument.

**Criterion:** Separate changes to scores from changes to values and identify the upstream information assumption.

## 4. Shape contracts

Q is 3×4, K is 5×4 and V is 5×2. Scores and weights are 3×5; AV is 3×2. The divisor is √4=2. Five keys paired with only four values is invalid, as is a query width unequal to the key width.

For two heads each returning 3×2, feature concatenation produces 3×4 and a 4×2 output projection returns 3×2. That can be added elementwise to a 3×2 residual. Concatenating along positions produces 6×2 and cannot be added to the original X without redefining the operation. Even matching shapes do not guarantee matching feature meanings, as F04 showed.

**Criterion:** Identify both multiplication compatibility and semantic correspondence. Self-attention and cross-attention need not have the same query/key lengths.

## 5. Availability during fitting and generation

The training pairs by row are START→A, A→B and B→C. At row 2 the allowed input prefix is [START,A]; the target is B. With input [A,B,C] and the same targets, row 2 could inspect B directly through the diagonal connection. A causal index rule alone would not stop this labeling error.

Fitting updates parameters based on loss. In the fixed-weight generation procedure, each new input prefix includes actual earlier generated tokens; target tokens are not available in advance. Parallel computation over known shifted training inputs does not imply parallel availability of unknown generated tokens. A prefix error can change subsequent inputs, so evaluation should match the intended generation procedure.

If an earlier unmasked representation already mixed C into row 1, a later causal attention layer can read that contaminated row 1. The mask controls its own edges, not the entire history of its input tensors.

**Criterion:** Explicit input/target alignment, fixed versus updated weights and an upstream leakage counterexample. No conclusion about current proprietary models is required.

## 6. Cost, order and useful evidence

Dense pair counts are 3²=9 and 6²=36; causal permitted counts are 3·4/2=6 and 6·7/2=21. Full matrix computation followed by masking does not by itself save the work on the forbidden positions. With fixed dk and dv, the two attention matrix products scale with n²; projections and the rest of a network contribute additional costs.

Under a simultaneous row permutation of position-free X, Q/K/V permute consistently. The score matrix permutes in both axes, weights follow those changes and outputs permute by the same row order. The six-permutation check below tests this property. Holding positional vectors fixed while permuting token content is a different transformation, so it need not preserve the result.

To evaluate a cheaper local-context restriction, freeze candidate settings on development data and compare both systems on the same held-out document tasks. Include cases where necessary evidence is farther away than the permitted window, and keep revision/organization boundaries from A01. Measure supported correct answers, missing evidence, latency and resource use. If local arithmetic passes but long-distance evidence cases fail beyond a declared tolerance, reject or revise the restriction. Test limits and costs must come from the application; no numerical deployment threshold is invented here.

**Criterion:** Distinguish count models from benchmarks, state what is permuted, and propose a test that can falsify the cheaper design.

## Reproduce the checks

The implementation uses finite values and explicit Boolean allowed masks, with one permitted key required per query. Dropout and other Transformer components are absent. Tolerances reflect floating-point calculation, not statistical uncertainty. The expected expressions, metamorphic checks and deliberately wrong normalization provide checks beyond simply rerunning one function.

```python
from math import exp, sqrt, isclose
from itertools import permutations

def shape(a):
    assert a and a[0] and all(len(r)==len(a[0]) for r in a)
    return len(a),len(a[0])
def mm(a,b):
    na,da=shape(a);nb,db=shape(b)
    assert da==nb
    return [[sum(a[i][k]*b[k][j] for k in range(da))
             for j in range(db)] for i in range(na)]
def transpose(a):
    shape(a)
    return [list(c) for c in zip(*a)]
def softmax(scores,allowed):
    if not any(allowed):raise ValueError('no permitted key')
    top=max(s for s,ok in zip(scores,allowed) if ok)
    terms=[exp(s-top) if ok else 0.0 for s,ok in zip(scores,allowed)]
    z=sum(terms)
    return [t/z for t in terms]
def attention(q,k,v,allowed):
    nq,dq=shape(q);nk,dk=shape(k);nv,dv=shape(v)
    assert dq==dk and nk==nv and shape(allowed)==(nq,nk)
    scores=[[s/sqrt(dk) for s in row] for row in mm(q,transpose(k))]
    weights=[softmax(row,mask) for row,mask in zip(scores,allowed)]
    return weights,mm(weights,v)
def close(a,b):
    assert shape(a)==shape(b)
    assert all(isclose(x,y,rel_tol=1e-10,abs_tol=1e-10)
               for ar,br in zip(a,b) for x,y in zip(ar,br))
def fails(fn,kind):
    try:fn()
    except kind:return
    raise AssertionError('expected rejection')
X=[[1.,0.],[0.,2.],[1.,1.]]
W=[[1.],[0.]];I=[[1.,0.],[0.,1.]]
q=k=mm(X,W);v=mm(X,I)
full=[[True]*3 for _ in range(3)]
causal=[[j<=i for j in range(3)] for i in range(3)]
e=exp(1);z=2*e+1
expected=[2*e/z,(2+e)/z]
a,o=attention(q,k,v,full)
close(a,[[e/z,1/z,e/z],[1/3]*3,[e/z,1/z,e/z]])
close(o,[expected,[2/3,1.],expected])
ac,oc=attention(q,k,v,causal)
close(oc,[[1.,0.],[.5,1.],expected])
for mask,wts,out in [(full,a,o),(causal,ac,oc)]:
    for flags,row,value in zip(mask,wts,out):
        assert isclose(sum(row),1)
        assert all(w>=0 and (ok or w==0) for ok,w in zip(flags,row))
        for col in range(2):
            permitted=[v[j][col] for j,ok in enumerate(flags) if ok]
            assert min(permitted)-1e-10<=value[col]<=max(permitted)+1e-10
newmask=[r[:] for r in causal];newmask[2][1]=False
_,om=attention(q,k,v,newmask)
close(om,[[1.,0.],[.5,1.],[1.,.5]])
wrong=mm([[1/3,1/3,0]],v)
close(wrong,[[1/3,2/3]])
assert not isclose(sum([1/3,1/3,0]),1)
# Changing a feature ignored by Q/K isolates the value path.
x2=[r[:] for r in X];x2[2][1]=7
close(mm(x2,W),q)
_,o2=attention(mm(x2,W),mm(x2,W),x2,full)
_,oc2=attention(mm(x2,W),mm(x2,W),x2,causal)
close(o2,[[expected[0],expected[1]+6*e/z],[2/3,3.],
          [expected[0],expected[1]+6*e/z]])
close(oc2,[oc[0],oc[1],o2[2]])
# Every ordering without positions/masks must permute outputs consistently.
for p in permutations(range(3)):
    xp=[X[i] for i in p]
    _,op=attention(mm(xp,W),mm(xp,W),xp,full)
    close(op,[o[i] for i in p])
# Stable softmax is invariant to a common score offset.
close([softmax([1001,1000,1001],[True]*3)],[a[0]])
fails(lambda:softmax([1,2],[False,False]),ValueError)
fails(lambda:attention(q,k,v[:2],full),AssertionError)
fails(lambda:attention([[1,2]],k,v,[[True]*3]),AssertionError)
# Rectangular case checks dk scaling and query count, not just square shapes.
qr=[[1.,0.,0.,0.]]*3
kr=[[2.,0.,0.,0.]]+[[0.,0.,0.,0.]]*4
vr=[[1.,0.]]+[[0.,1.]]*4
ar,orr=attention(qr,kr,vr,[[True]*5 for _ in range(3)])
close(ar,[[e/(e+4)]+[1/(e+4)]*4]*3)
close(orr,[[e/(e+4),4/(e+4)]]*3)
assert shape(orr)==(3,2)
for n,dense,allowed in [(3,9,6),(6,36,21)]:
    assert n*n==dense
    assert sum(j<=i for i in range(n) for j in range(n))==allowed
print('PASS: projections, analytic attention, masks, convex bounds, value perturbation,')
print('all six permutations, stable softmax, invalid shapes/masks, rectangular scaling and counts.')
```

## Revision history

- 1.0 — 2026-11-09. Six reference solutions and executed numerical/information-flow checks.
---

# A03 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| Title | Retrieval, external knowledge, and provenance — worked answers |
| ID / revision / date | A03 answers · 1.0 · 2026-11-10 |
| Prerequisites | S02, S06, A01, A02 and [A03 core](SDE_A03.md) |
| Capability developed | Separate evidence availability, retrieval, context delivery and claim support |
| Source-check status | R15 methods and R11 mediation; exact URLs/locators in core |
| Experiment status | Executed finite fixtures and exact arithmetic; no live search, generation or semantic entailment experiment |

These are reference solutions, not learner responses or mastery assessments.

## Hints

1. Apply eligibility before interpreting a ranking; inspect the context actually supplied.
2. Change one stage at a time while keeping the query and required evidence fixed.
3. Read the claim's temporal and business scope, not only its nouns.
4. A missing index entry and a revoked grant call for different explanations.
5. Compare sum-of-products with product-of-sums using the same probabilities.
6. State every denominator. A component metric can improve while task success falls.

## 1. Candidate and context trace

At t=20, the authoritative head is revision 3. `old` is stale for the current query; `other` is a different tenant. Eligible candidates are `note` at 93 and `new` at 88. Top-1 is [`note`]; top-2 is [`note`,`new`]. Keeping only the first candidate loses the delivery evidence even with k=2. The declared field-aware selector chooses `new` because it contains the requested field.

For this exact tenant/document/revision/field question, direct fact lookup is the natural baseline and returns Y with its frozen locator. More general search might help with paraphrases or unstructured documents, but that benefit is not demonstrated by this fixture. If multiple eligible passages claim conflicting delivery values, an explicit resolution rule is required; the field-aware selector alone does not resolve truth.

**Criterion:** Separate eligibility, candidate recall and context sufficiency; no confidence interpretation of scores.

## 2. Controlled failure isolation

Missing evidence: remove `new` from the indexed corpus while retaining the authoritative manifest expectation. Compare expected versus indexed revision contents; k changes cannot fix it.

Present but not retrieved: restore `new`, use k=1, and observe only `note`. Force `new` into the candidate set to distinguish a retrieval miss from downstream problems.

Retrieved but dropped: use k=2, then retain only score-first `note`. Compare candidate IDs with actual context IDs. Supply `new` directly to the answering component as a diagnostic, without calling that oracle run deployed performance.

Supplied but ignored: context includes `new`, yet the answer states delivery X. Inspect the exact model input and output and their claim-level comparison. A higher-recall retriever cannot fix this already-sufficient context on its own.

Cited without support: retain context [`new`] and emit “Payment is settled” with that citation. The locator resolves, but the fixture contains no settlement fact. Validate the claim–passage relationship rather than counting citation syntax.

**Criterion:** One controlled intervention per boundary, with observable artifacts. Real cases can contain several failures; a triage label is not proof of a unique root cause.

## 3. Provenance is necessary but narrower than truth

`old` supports “revision 2 listed X” if the old bytes and locator resolve and the reader may access them. It does not support the current-state claim at t=20, because the head is revision 3. `new` supports “revision 3 lists Y,” and supports the current published-reference answer only with the authoritative head/time link. Neither passage supports settlement.

A claim “X” cited to `new` fails the assigned fact comparison. A claim “payment settled” cited to `new` fails even though the citation is syntactically valid and current. An authentic passage can still be factually wrong about the world. Distinguish “the source states Y” from independently verified delivery.

Keep exact tenant/document/revision/passage identity, bytes, rendering/extraction version and locator. Replacing old evidence with current bytes destroys historical reproducibility. A digest is an integrity check, not a substitute for retained content. Multiple claims need individual coverage; missing support is not repaired by adding more unrelated citations.

**Criterion:** Correct scope, source identity and permission; no inference from link existence to semantic support or physical truth.

## 4. Time, ingestion and permission changes

At t=10, revision 2 is the published head; X is the answer for that historical state, assuming current permission to view its retained evidence. The query-time snapshot and the disclosure-time access decision are different controls.

At t=20 with revision 3 selected but `new` absent from the index, report current evidence unavailable, or perform an authorized direct lookup. An older answer is acceptable only as an explicitly labeled older result under a contract that allows it. Quietly returning X as current fails.

If permission is revoked before display, withhold the protected content under the selected immediate-disclosure policy. A previously allowed retrieval or cached answer is insufficient. An unavailable policy check also does not establish permission. Coordinating the check with disclosure is a deployment requirement, not a feature proved by the fixture's Boolean grant.

**Criterion:** Distinguish source publication, index readiness, query time and authorization freshness. Do not present delayed ingestion as “no such fact exists.”

## 5. Two marginalization calculations

For the fixed target sequence, sequence-level mixing gives 0.6×0.8×0.5 + 0.4×0.2×0.9 = 0.24+0.072=0.312. Token-level mixing gives (0.48+0.08)×(0.30+0.36)=0.56×0.66=0.3696. Their difference is 0.0576. The product-of-sums includes cross-passage contributions; it does not mean an observed output is guaranteed to combine correct facts.

The second-token probabilities are conditional on the same specified first-token prefix, not unconditional token frequencies. The two passages form the entire normalized toy distribution here. The paper uses a top-K approximation; these numbers are not its reported outputs. For a single-token target the two forms coincide, as summing over the same one-step terms yields the same result.

Retrieval weights concern passages given a query; A02 attention weights mix representations over positions; a correctness assessment concerns an answer's claims against evidence and reality. Matching a mathematical normalization pattern does not equate these targets.

**Criterion:** Correct conditioning, arithmetic and interpretation; no fabricated measured model accuracy.

## 6. Stage accounting and a falsifiable evaluation

Corpus coverage is 16/20=80%. Conditional candidate hit rate is 12/16=75%. Retention of sufficient evidence is 10/12≈83.33%. Supported completion after sufficient context is 7/10=70%. Multiplying yields 7/20=35%, because the nested counts cancel. No independence assumption is needed. Overall candidate hit rate is 12/20=60%, a different denominator from 75%.

For a higher-recall candidate, freeze the same eligible query population, target revisions, permissions, corpus snapshot, context budget and downstream procedure. Include new documents/groups according to deployment, keeping revisions together. Measure sufficient-evidence retrieval and actual selected-context sufficiency, supported answer completion, unauthorized exposures, abstentions, latency and cost. Keep missing/unanswered cases in the declared outcome population.

A retriever could increase candidate recall while adding distractions that crowd out the required evidence under the context budget. It could improve recall on authorized cases yet expose another tenant's data. Either can invalidate deployment. Use direct lookup as the baseline for exact field questions, and a separate relevance/support rubric for open-ended questions. Independent adjudication of contested support cases is needed; our hand-assigned fact map is not that adjudication system.

**Criterion:** Nested denominators, comparable policies and a concrete way the seemingly better component can fail the full contract.

## Reproduce the executed checks

This code implements only the declared fixture rules. The `facts` relation is an oracle supplied by the author, not inferred from prose. Authorization and head selection are sequential model inputs; concurrent policy changes, actual identity verification and index/storage failures are not simulated. Fixed rankings are not search-engine measurements.

```python
from fractions import Fraction as F
from itertools import permutations

# (tenant, document, revision, field, value) is the exact fact identity.
def passage(pid,tenant,rev,score,facts):
    return dict(id=pid,tenant=tenant,doc='D17',rev=rev,score=score,facts=facts)
corpus=[
    passage('old','A',2,97,{'delivery':'X'}),
    passage('other','B',3,95,{'delivery':'Z'}),
    passage('note','A',3,93,{}),
    passage('new','A',3,88,{'delivery':'Y'}),
]
def head(t):
    if t<5: return None
    return 2 if t<15 else 3

def eligible(p,t,grant=True):
    return grant and p['tenant']=='A' and p['doc']=='D17' and p['rev']==head(t)
def candidates(rows,t,k,grant=True):
    return sorted((p for p in rows if eligible(p,t,grant)),
                  key=lambda p:(-p['score'],p['id']))[:k]
def select(rows,field='delivery'):
    return sorted(rows,key=lambda p:(field not in p['facts'],-p['score'],p['id']))[:1]
def ids(rows):return [p['id'] for p in rows]
def supports(claim,p):
    tenant,doc,rev,field,value=claim
    return (tenant,doc,rev)==(p['tenant'],p['doc'],p['rev']) and p['facts'].get(field)==value

def disclose(claim,citation,context,t,grant=True):
    p=next((p for p in context if p['id']==citation),None)
    return bool(p and eligible(p,t,grant) and supports(claim,p))
claim=('A','D17',3,'delivery','Y')
assert ids(candidates(corpus,20,1))==['note']
assert ids(candidates(corpus,20,2))==['note','new']
context=select(candidates(corpus,20,2))
assert ids(context)==['new'] and disclose(claim,'new',context,20)
assert not disclose(claim,'new',context,20,False) # revoked before disclosure
assert not candidates(corpus,20,2,False)
assert ids(candidates(corpus,10,2))==['old']
assert head(4) is None and head(5)==2 and head(14)==2 and head(15)==3
assert not candidates(corpus,4,4)
old=corpus[0]
assert supports(('A','D17',2,'delivery','X'),old)
assert not disclose(('A','D17',2,'delivery','X'),'old',[old],20)
assert disclose(('A','D17',2,'delivery','X'),'old',[old],10)
assert not disclose(('A','D17',3,'payment','settled'),'new',context,20)
assert not disclose(('A','D17',3,'delivery','X'),'new',context,20)
assert not disclose(claim,'invented',context,20)
assert not disclose(claim,'new',[],20)
# Filtering only after global top-1 loses eligible results.
global_first=sorted(corpus,key=lambda p:-p['score'])[:1]
assert not [p for p in global_first if eligible(p,20)]
assert len(candidates(corpus,20,1))==1
# A second tenant's score cannot alter the result under this fixture's prefilter.
for score in [-100,0,1000]:
    changed=[dict(p,score=score) if p['id']=='other' else p for p in corpus]
    assert ids(select(candidates(changed,20,2)))==['new']
# Storage order is irrelevant because ranking has an explicit tie rule.
for rows in permutations(corpus):
    assert ids(select(candidates(rows,20,2)))==['new']

def diagnose(rows,cands,ctx,answer,citation):
    if not any(eligible(p,20) and supports(claim,p) for p in rows):return 'corpus'
    if not any(supports(claim,p) for p in cands):return 'retrieval'
    if not any(supports(claim,p) for p in ctx):return 'selection'
    if not disclose(answer,citation,ctx,20):return 'answer/support'
    return 'success'
missing=[p for p in corpus if p['id']!='new']
one=candidates(corpus,20,1);two=candidates(corpus,20,2)
assert diagnose(missing,candidates(missing,20,4),[],claim,'new')=='corpus'
assert diagnose(corpus,one,one,claim,'new')=='retrieval'
assert diagnose(corpus,two,two[:1],claim,'new')=='selection'
assert diagnose(corpus,two,context,('A','D17',3,'delivery','X'),'new')=='answer/support'
assert diagnose(corpus,two,context,('A','D17',3,'payment','settled'),'new')=='answer/support'
assert diagnose(corpus,two,context,claim,'new')=='success'
# Enough candidate depth cannot recover physically missing evidence.
for k in range(1,6):
    assert not any(supports(claim,p) for p in candidates(missing,20,k))
seq=F(3,5)*F(4,5)*F(1,2)+F(2,5)*F(1,5)*F(9,10)
tok=(F(3,5)*F(4,5)+F(2,5)*F(1,5))*(F(3,5)*F(1,2)+F(2,5)*F(9,10))
assert seq==F(312,1000) and tok==F(3696,10000) and tok-seq==F(576,10000)
rates=[F(16,20),F(12,16),F(10,12),F(7,10)]
product=F(1)
for rate in rates:product*=rate
assert product==F(7,20) and sum([4,4,2,3,7])==20
print('PASS: time boundaries, eligibility, ranking/selection, five failure fixtures,')
print('revocation/citation checks, 24 orderings, score perturbations, marginalization and stage rates.')
```

## Revision history

- 1.0 — 2026-11-10. Six reference answers and executed fixture checks; no learner performance inferred.
---

# A04 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| ID / revision / date | A04 answers · 1.0 · 2026-11-10 |
| Title | Inference serving and memory economics — worked answers |
| Prerequisites | S01, S05, A02 and [A04 core](SDE_A04.md) |
| Capability developed | Audit memory units, allocation boundaries and latency-constrained policy comparisons |
| Source-check status | R16/R04/R08 locators in core; numerical cases are original |
| Experiment status | Python integer/rational checks executed; no model or GPU benchmark |

These reference solutions do not represent learner responses or mastery.

## Hints

1. Count both keys and values across every layer and KV head; multiply by bytes per scalar.
2. Divide remaining bytes by bytes per request, then round down. Check the next token too.
3. Round each request separately before summing. A block cannot lend its unused tail to a separate private request.
4. Separate service start, first-token time and final completion. Keep every clock relative to arrival.
5. Recount timely completions before changing the cost denominator.
6. A lower memory peak says nothing by itself about service time or answer quality.

## 1. Tensor budget

The coefficient is 2×32×8×128×2=131,072 bytes per cached token, or 128 KiB. Stored weights consume (6×2^30)×2=12 GiB. Remaining memory is 24−12−4=8 GiB, hence 8×2^30/131,072=65,536 token positions. A request at 4,096 positions consumes 512 MiB; sixteen fit arithmetically.

Doubling Hkv to 16 doubles the coefficient to 256 KiB and makes a 4,096-position request consume 1 GiB. Eight fit. This changes only the assumed KV layout; a real architecture change can also alter parameter count and quality. Holding those fixed is a sensitivity exercise, not a specification of an actual replacement model.

**Criterion:** Correct tensor dimensions, binary units and omitted-state boundary. No substitution of query-head count without a layout justification.

## 2. Length and concurrency

At lengths 1,024, 2,048, 4,096 and 8,192, per-request state is respectively 128,256,512 and 1,024 MiB. Dividing the 8,192 MiB pool gives 64,32,16 and 8 requests. These are memory-only limits; none is a throughput claim.

Sixteen requests at 4,096 positions exactly fill the pool. One more unrounded cached position exceeds it by 128 KiB. With 16-slot blocks, growing one such request to 4,097 requires a new 2 MiB block. If all sixteen grow, the next allocation requires 32 MiB. A correct scheduler needs reserved growth space or a declared fallback such as queueing/preemption; silently exceeding capacity is not a policy.

**Criterion:** Distinguish live-byte growth from allocation-step growth and present occupancy from a safe generation horizon.

## 3. Block accounting

| Block size | Rounded lengths | Allocated slots | Slack slots |
| ---: | --- | ---: | ---: |
| 8 | 24,32,32,8 | 96 | 15 |
| 16 | 32,32,32,16 | 112 | 31 |
| 32 | 32,32,32,32 | 128 | 47 |

The live count is always 81. At size 16, 112×128 KiB=14 MiB is allocated and 31×128 KiB=3.875 MiB is unused tail capacity. Four fixed 64-position reservations instead allocate 256 slots=32 MiB, with 175 unused slots at this instant. Those slots may be intentional future capacity; they are not necessarily fragmented free memory.

External fragmentation can prevent a large contiguous request despite sufficient total free space. Internal slack lies inside allocated blocks. The fixture has private blocks and no block-table accounting beyond the declared reserve. Smaller B reduces slack here, but latency could worsen through more lookups or less efficient access. Only measurement decides that trade-off.

**Criterion:** Per-request rounding, exact totals and accurate definitions; no claim of zero total waste.

## 4. Two schedule traces

For b=1, prefill takes 10 ms and four decode rounds take 4×5=20 ms. Each request takes 30 ms. Serial starts are [0,30,60,90], giving first-token times [10,40,70,100] and completions [30,60,90,120]. Only the first completes by 50 ms.

For b=4, prefill takes 16 ms and four rounds take 4×8=32 ms. All first tokens arrive at 16 ms; all completions occur at 48 ms. All four meet 50 ms. Makespan throughput is 4/0.120 versus 4/0.048, or approximately 33.33 and 83.33 requests/s. These finite-trace ratios do not establish sustainable traffic rates.

The first request's streaming gap worsens from 5 to 8 ms. Its first token is also later. Four outputs sharing a 48 ms computation does not divide their experienced response times by four. It divides busy resource time per output, a different metric.

**Criterion:** Same workload, full response clocks, inclusive deadline and explicit objective. No percentile claims from four requests.

## 5. Counterexample and economics

At 40 ms, serial completion 30 qualifies but 60,90,120 do not. Batch completion 48 does not qualify for any request. Serial delivers 1/4 timely results; batching delivers 0/4. Thus a policy with higher completed-request throughput can lose on the chosen objective.

With price r per busy second, serial costs 0.120r and batch costs 0.048r for the full trace. At 50 ms the charges per timely result are 0.120r and 0.012r. At 40 ms serial remains 0.120r, while batch's denominator is zero: report no timely result and its incurred charge, not zero cost or a finite ratio.

Longer prompts, longer generations, bandwidth contention or larger batch sizes outside the assumed range can invalidate the service laws. If requests arrive far apart, batch formation adds waiting and the comparison changes again. Billing over a fixed provisioned window rather than busy time can also change the financial comparison.

**Criterion:** Preserve late work in the numerator, timely outcomes in the denominator and undefined zero-success ratios.

## 6. A test that can reject the optimization

Replay identical timestamped requests independently of completion. Fix architecture, weights, precision, decoding/stopping rules and correctness rubric. Record prompt/output lengths and repeat controlled runs with a stated warmup policy. Compare allocated versus live memory, workspace peaks, first-token and inter-token latency, end-to-end completion, offered/admitted/rejected counts and timely-correct outcomes. Count cancellations, preempted/recomputed work, idle time and startup under the same resource-accounting window.

Reject the optimization if lower memory usage accompanies worse timely-correct completion, unacceptable streaming gaps, corruption of retained state, isolation failures or greater total cost under the declared objective. If memory has headroom but longer batches saturate memory bandwidth, more available slots are not useful admission capacity. If temporary workspace exceeds its reserved bound, the memory model itself is invalid. A useful experiment identifies which hypothesis failed instead of declaring paging universally good or bad.

Quality and authority remain independent constraints from A03/S06. Shared prefixes require compatible state and access boundaries; the private-block fixture has not validated cross-request sharing. A05 will evaluate the full workflow rather than treating emitted tokens as useful outcomes.

**Criterion:** A falsifiable outcome, consistent denominator, resource evidence and clearly bounded claims.

## Reproduce the checks

The script below uses exact arithmetic for budgets and the assigned service laws. It checks 4,096 length/block combinations and 64 concurrency boundaries, plus both schedules and cost ratios. These are finite model checks, not hardware experiments.

```python
from fractions import Fraction as F
GiB=2**30
MiB=2**20
c=2*32*8*128*2
pool=24*GiB-(6*GiB)*2-4*GiB
assert c==128*1024 and pool//c==65536
assert [pool//(c*t) for t in (1024,2048,4096,8192)]==[64,32,16,8]
assert pool//(2*c*4096)==8
for n in range(1,65):
    max_t=pool//(c*n)
    assert n*max_t*c<=pool<n*(max_t+1)*c

def allocated(lengths,b):
    return sum(((t+b-1)//b)*b for t in lengths)
lengths=[17,31,32,1]
assert sum(lengths)==81
assert [allocated(lengths,b) for b in (8,16,32)]==[96,112,128]
assert allocated(lengths,16)*c==14*MiB
assert F((112-81)*c,MiB)==F(31,8)
assert 4*64*c==32*MiB
for b in (1,8,16,32):
    for t in range(1,1025):
        a=allocated([t],b)
        assert a%b==0 and 0<=a-t<b
        assert a-b<t<=a
assert allocated([4096]*16,16)*c==pool
assert allocated([4097]+[4096]*15,16)*c-pool==2*MiB
assert allocated([4097]*16,16)*c-pool==32*MiB

def times(b):
    prefill=8+2*b
    step=4+b
    return prefill,prefill+4*step
p1,s1=times(1);p4,s4=times(4)
starts=[i*s1 for i in range(4)]
first_s=[s+p1 for s in starts];finish_s=[s+s1 for s in starts]
first_b=[p4]*4;finish_b=[s4]*4
assert first_s==[10,40,70,100] and finish_s==[30,60,90,120]
assert first_b==[16]*4 and finish_b==[48]*4

def timely(xs,d):return sum(x<=d for x in xs)
assert [timely(xs,50) for xs in (finish_s,finish_b)]==[1,4]
assert [timely(xs,40) for xs in (finish_s,finish_b)]==[1,0]
# Deadline boundary checks establish inclusive semantics.
assert timely(finish_b,47)==0 and timely(finish_b,48)==4
assert F(4*1000,max(finish_s))==F(100,3)
assert F(4*1000,max(finish_b))==F(250,3)

def charge_per_timely(xs,d):
    n=timely(xs,d)
    return F(max(xs),1000)/n if n else None
assert charge_per_timely(finish_s,50)==F(120,1000)
assert charge_per_timely(finish_b,50)==F(12,1000)
assert charge_per_timely(finish_b,40) is None
print('PASS: budgets, 64 capacity boundaries, 4096 block cases, growth, schedules and costs')
```

## Revision history

- 1.0 — 2026-11-10. Six solutions, criteria and executable model checks. No learner performance inferred.
---

# A05 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| ID / revision / date | A05 answers · 1.0 · 2026-11-11 |
| Title | Evaluation, workflows, and controlled autonomy — worked answers |
| Prerequisites | A01, A03, S06, A04 and [A05 core](SDE_A05.md) |
| Capability developed | Audit outcome denominators and enforceable control boundaries |
| Source-check status | R18/R17/R03 passages linked in core |
| Experiment status | Finite predicate/ledger calculations executed; no live model or external action |

Reference answers are not learner responses or mastery assessments.

## Hints

1. Who selects the next operation, and who authorizes it, are separate questions.
2. Count every offered case, then separately count answerable cases and timely drafts.
3. A budget must survive retries; a tool result cannot grant a privilege.
4. A repeated trial is not a new document. Selection needs a mechanism.
5. Start with a two-by-two table and label each denominator.
6. Isolate the useful capability in D2 before accepting the full loop's complexity.

## 1. Contract and baselines

All designs must return supported, current, scoped drafts or the appropriate unresolved/refusal disposition within two seconds, with no unauthorized disclosure/effect. None receives payment authority. W uses a coded exact lookup and template. M has one fixed bundle and one model call. L selects further read operations from observations but the controller constrains every dispatch. A workflow can contain a model; its control structure remains fixed if the next step is determined by code.

Compare the whole designs on the same offered population and permitted corpus. An identical-evidence diagnostic can isolate answer construction, but supplying oracle evidence bypasses retrieval and must be labeled separately. Returning unresolved for an answerable case is safer than inventing a claim, yet fails the chosen completion objective.

**Criterion:** Distinguish outcome, control and authority; preserve the same information/access contract.

## 2. Outcome and cost ledger

W's successful cases are D1,D3,D4,D6: 4/6. M's are D1,D4,D6: 3/6. L's are D1,D2,D3,D4: 4/6. Timely drafts occur on D1,D6 for W and M, and D1,D2 for L. Each therefore covers 2/4 answerable cases. D3/D4 are valid non-draft dispositions; counting them as drafts would inflate usefulness.

With total resource charges [6,12,24], charge per contract success is [6/4,12/3,24/4]=[1.5,4,6]. Charge per timely draft is [6/2,12/2,24/2]=[3,6,12]. Late and unsuccessful work remains in the numerator. These are constructed charges, not estimates from A04's hardware example or actual billing.

L has one forbidden approval attempt and zero committed mutations. The external guard succeeds on that case; the policy does not. D6 also lacks a draft, so it is not a contract success. More generally, a policy could attempt a forbidden action, get blocked, then produce a correct draft; report the attempt even if the final-artifact metric passes. A release gate can prohibit such attempts independently.

**Criterion:** Explicit denominators, separate refusal/draft outcomes, and attempted versus realized violations.

## 3. Traces and enforcement

Successful D2: scoped search → exact passage read → supported draft → validation. The two reads remain within the three-call cap. Missing evidence: three permitted empty reads consume all three slots; a fourth is denied and the controller returns unresolved. Invalid proposals terminate immediately under the declared policy rather than allowing endless free retries.

Hostile observation: source text requests approval → model proposes `approve` → controller rejects because it is outside the allowlist → record the attempt; no mutation. Tenant mismatches and revoked read permission must also fail before evidence is returned. Neither a matching schema nor an apparently sensible action proves authority.

The sequential check below counts admitted external calls. It does not implement identity verification, concurrent revocation, cancellation of running calls, token accounting or semantic support. A real controller additionally needs model-call/output-size caps, elapsed-time enforcement, bounded tool responses, and checks on final disclosure. If a future mutation times out, consult its stable operation identity; blindly retrying under a new identity can duplicate effects.

**Criterion:** A bounded failure path, no budget reset, authority from trusted execution context and honest implementation limits.

## 4. Repeated trials

Rates by case are 3/3,2/3,1/3,0/3. Equal-case mean is (1+2/3+1/3+0)/4=1/2. Pooled success is 6/12=1/2 because all trial counts match. The four underlying cases remain four cases; independent-document uncertainty cannot be calculated by pretending the twelve attempts are unrelated.

Three cases have at least one success, hence 3/4 is an oracle best-of-three result. To realize it, a system must run multiple attempts and correctly select an acceptable answer. The selection procedure can fail, incurs cost, and must be evaluated as part of the complete system. Unequal trial counts make pooled and equal-case means potentially differ; report the intended estimand before aggregating.

Keep all revisions of a document family together in the holdout, reconstruct evidence at decision time, and repeat under a frozen sampling configuration. Variation across seeds is not evidence of diversity across suppliers or future periods.

**Criterion:** Distinguish case diversity, stochastic variation and selection-system performance.

## 5. Judge disagreement

| Reference adjudication | Judge accepts | Judge rejects | Total |
| --- | ---: | ---: | ---: |
| Correct | 6 | 1 | 7 |
| Incorrect | 3 | 2 | 5 |
| Total | 9 | 3 | 12 |

Agreement is (6+2)/12=2/3. Acceptance precision is 6/9=2/3; false-accept rate among incorrect outputs is 3/5. False rejection among correct outputs is 1/7. The equal numerical values of agreement and precision here are accidental; the populations differ.

Blind the system identity, inspect original sources/revisions and action logs, and ask a second qualified reviewer to apply the same rubric. Preserve initial judgments. Distinguish ambiguity, context omission, source conflict and evaluator mistakes. Do not settle disagreements by choosing whichever answer helps the preferred system. Treat adjudication as a reference procedure whose reliability also needs checking. Validate changes on new cases; a disagreement-only sample cannot estimate overall error directly.

**Criterion:** Correct confusion matrix, denominator labels, and a process that permits both human and judge error.

## 6. Next decision

Keep W as the baseline under this ledger. Investigate a fixed alternate-extraction branch for D2, using held-out document families and the same source-time contract. Compare that addition with L under identical budgets, deadlines and scoring, recording all cases and violations. L might still be justified if held-out tasks require adaptive searches that fixed branches cannot cover, but that has not been demonstrated.

Before deployment, test real tool errors, latency tails, revocation, malformed responses and output containment; use shadow operation to observe distribution changes without granting effects. A later controlled rollout must evaluate reviewer behavior and shared-resource interference. The frozen ledger cannot establish customer value, operational safety across every route, or performance after source/provider changes. R17's dependency and feedback concerns remain relevant even if model weights are unchanged.

**Criterion:** Choose the simplest supported design, name evidence that could reverse it, and preserve offline-to-live limits.

## Reproduce the checks

This is an executable specification of the constructed accounting and sequential admission rules. It does not simulate a language model, network, clock progression, or semantic judge.

```python
from fractions import Fraction as F
from itertools import product
# Tuples: contract success, timely supported draft, forbidden attempts, effects.
rows={
 'W':[(1,1,0,0),(0,0,0,0),(1,0,0,0),(1,0,0,0),(0,0,0,0),(1,1,0,0)],
 'M':[(1,1,0,0),(0,0,0,0),(0,0,0,0),(1,0,0,0),(0,0,0,0),(1,1,0,0)],
 'L':[(1,1,0,0),(1,1,0,0),(1,0,0,0),(1,0,0,0),(0,0,0,0),(0,0,1,0)]}
charges={'W':6,'M':12,'L':24}
for name,expected in [('W',4),('M',3),('L',4)]:
    data=rows[name]
    successes=sum(r[0] for r in data);drafts=sum(r[1] for r in data)
    assert successes==expected and drafts==2
    assert F(drafts,4)==F(1,2) and sum(r[3] for r in data)==0
assert [F(charges[n],sum(r[0] for r in rows[n])) for n in rows]==[F(3,2),F(4),F(6)]
assert [F(charges[n],2) for n in rows]==[F(3),F(6),F(12)]
assert sum(r[2] for r in rows['L'])==1

allowed={'read_revision','search_evidence'}
def admit(op,authenticated,same_tenant,grant,used,elapsed):
    return (op in allowed and authenticated and same_tenant and grant
            and 0<=used<3 and 0<=elapsed<2000)
# Exhaustive 3 operations x 8 flag combinations x 5 counts x 4 clock inputs.
count=0
for op,auth,scope,grant,used,elapsed in product(
    ['read_revision','search_evidence','approve'],[False,True],[False,True],
    [False,True],range(5),[0,1999,2000,2001]):
    result=admit(op,auth,scope,grant,used,elapsed)
    if result:
        assert op!='approve' and all([auth,scope,grant]) and used<3 and elapsed<2000
    if op in allowed and all([auth,scope,grant]) and used<3 and elapsed<2000:
        assert result
    count+=1
assert count==480
used=0
for _ in range(3):
    assert admit('search_evidence',True,True,True,used,100)
    used+=1 # empty results still consume the dispatched-call budget
assert not admit('search_evidence',True,True,True,used,100)
assert not admit('approve',True,True,True,0,100)
assert admit('read_revision',True,True,True,0,100)
assert not admit('read_revision',True,True,False,1,100) # subsequent revoked grant
counts=[3,2,1,0]
assert sum(F(x,3) for x in counts)/4==F(1,2)
assert F(sum(counts),12)==F(1,2)
assert F(sum(x>0 for x in counts),4)==F(3,4)
# Unequal trial allocations can change the pooled estimand.
assert (F(1,1)+F(0,3))/2==F(1,2)
assert F(1,4)!=F(1,2)
tp,fn,fp,tn=6,1,3,2
assert tp+fn+fp+tn==12
assert F(tp+tn,12)==F(2,3)
assert F(tp,tp+fp)==F(2,3)
assert F(fp,fp+tn)==F(3,5) and F(fn,tp+fn)==F(1,7)
print('PASS: ledger, cost denominators, 480 admission cases, budget/revocation, trials and judge counts')
```

## Revision history

- 1.0 — 2026-11-11. Six reference solutions and bounded executable checks; no learner performance inferred.
---

# B01 — Hints, worked answers, and assessment criteria

| Field | Value |
| --- | --- |
| ID / revision | B01 answers / 1.0 |
| Date | 2026-11-02 |
| Prerequisites | [B01 core pack](SDE_B01.md) |
| Capability developed | Judge whether an evidence plan can change a concrete build decision |
| Source-check status | R19 locators in core §10; answers are original teaching examples |
| Experiment status | Arithmetic assertions executed; no customer or market experiment conducted |

All organizations, offers, inputs, and outcomes below are hypothetical. These are worked possibilities, not the learner's answers or results from research participants.

## Hints

1. A role is not necessarily a different person. Name who feels the problem and who can change the process.
2. One hypothesis should concern the existing problem; the other should concern behavior toward an offer.
3. Ask for a reconstruction, not a rating of your idea. Include an opportunity to say the existing process works.
4. Convert minutes to hours before multiplying by an hourly value. Include review and onboarding.
5. Identify whose behavior changed, what it cost them, and what terms they accepted.
6. A gate authorizes the next bounded investment. It does not certify an entire market.

## 1. Scope and roles

A useful example segment is purchasing teams receiving 100–200 supplier invoices weekly and manually matching them to delivery evidence. The trigger is invoice receipt. The operator is the matching clerk; the intended outcome is an evidence-complete case ready for a correct approval decision. The assumed buyer is the manager responsible for that budget, but this role must be verified. A separate data or systems approver may exist; it is unknown here.

The current alternative combines documents, a spreadsheet, and employee judgment. It must be evaluated as a complete process, including exceptions. “Uses a spreadsheet” does not establish dissatisfaction or a business opportunity. An internal tool variant would replace a purchase hypothesis with a commitment of staff time and workflow ownership.

## 2. Two hypotheses and adverse evidence

Problem hypothesis: In the defined segment, assembling matching evidence creates material active workload or consequential delays. Evidence against it includes several relevant recent cases showing quick matching, low recurrence, or a different dominant delay. A participant who has not encountered an exception recently is useful negative evidence, provided their workload belongs to the chosen segment.

Adoption hypothesis: An authorized team will allocate permitted cases, a reviewer, and a dated trial if assistance preserves source traceability and approval. Adverse evidence includes refusal after the concrete terms are explained, inability to obtain necessary permissions, or higher-priority work repeatedly displacing the trial. Diagnose reasons before generalizing. Lack of authority in the interviewed person is a recruitment problem as well as a limit on their commitment.

Neither hypothesis requires pretending that five conversations yield a population estimate. The bounded batch is a practical investigation design. A later decision to estimate prevalence needs a sampling plan, addressed in F03.

## 3. Six sample questions

1. Reconstruct the last invoice requiring extra checking from receipt to resolution.
2. Which steps needed active work and which involved waiting? What record could help check the distinction?
3. What consequence followed, and what would have happened under the normal process?
4. Over the last defined working week, which cases needed this work and which did not?
5. What did the team change previously, and what remains useful about that approach?
6. For the most recent workflow tool adopted, who approved spending and data access, and what did adoption require?

These questions can reveal a mistaken premise. “How much would you pay for our AI that saves hours?” embeds both a benefit and a preferred solution. Rewrite it around actual work before discussing a real offer on explicit terms.

## 4. Arithmetic and interpretation

| Quantity | 8-minute baseline | 4-minute baseline |
| --- | ---: | ---: |
| Current work, 120 invoices/week | 16 h/week | 8 h/week |
| Proposed review: 120 × 3 / 60 | 6 h/week | 6 h/week |
| Proposed recurring overhead | 2 h/week | 2 h/week |
| Recurring capacity released | 8 h/week | 0 h/week |
| Onboarding: 12 h / 8 weeks | 1.5 h/week | 1.5 h/week |
| Net released capacity during assessment | 6.5 h/week | −1.5 h/week |
| Assigned value at ₹300/h, before fees | ₹1,950/week | −₹450/week |

The original baseline's assigned labor value is 16×₹300=₹4,800/week. Before onboarding, the potential released capacity is valued at 8×₹300=₹2,400/week. These are conditional arithmetic results.

If salaried hours cannot be reduced or usefully reassigned, released time may not reduce cash expenditure. If work quality falls or extra reviews appear, the model is incomplete. Even a correct capacity estimate does not reveal an authorized budget or accepted price. Compare the same outcome quality and count each work category once. The eight-week horizon is an assumed evaluation convention, not a prediction of a sales cycle.

## 5. Interpret the signals

| Fictional signal | What it supports | What remains unknown |
| --- | --- | --- |
| Developer praises demo | Appeal to that developer | Target user's pain, buyer's authority, adoption |
| Clerk estimates weekly burden | Reported problem magnitude from one perspective | Accuracy, recurrence, alternatives, budget |
| Sponsor schedules trial with resources | Specific intent to test on those terms | Actual execution, outcome improvement, renewal |
| Payment for custom integration | Demand for that scoped transaction | Repeatable product demand and delivery margin |
| Repeated manager-mandated use | Compliance or workflow dependence | Voluntary preference, net benefit, willingness to renew |

A signal can be genuine and still answer the wrong question. Preserve the terms, roles, and context. Do not transform these fictional examples into measured customer evidence.

## 6. Decision gates and changed constraint

Proceed to trial design if two independent organizations supply relevant recent episodes and one authorized sponsor agrees to a bounded trial with cases, reviewer, date, and success criterion. This is the exercise's proposed gate, not a proven universal threshold. Before execution, define how complete correct cases, active work, and exceptions will be checked against the current process.

Revise if evidence identifies a different bottleneck or if the interested operator lacks the required approval route. Stop or defer this particular investment if repeated relevant evidence indicates little consequence, adequate existing alternatives, or no feasible adoption path within the chosen constraints. Record the investigation limit so a later change can justify revisiting it.

With the new finding that missing delivery records create two-day delays, fast extraction does not itself provide the absent information. Investigate where records originate, who can obtain them, and why retrieval stalls. A follow-up plan could observe one missing-record episode and compare it with a routine case. Do not immediately commit to a reminder agent: the cause could instead be a supplier process, access restriction, or incomplete shipment. Reassess the problem before selecting a mechanism.

## Assessment criteria

| Dimension | A useful answer demonstrates |
| --- | --- |
| Specificity | Segment, workflow, roles, alternative, and consequential outcome |
| Falsifiability | Adverse evidence for both problem and adoption claims |
| Interview design | Recent episodes, neutral framing, and an approval-path question |
| Evidence discipline | Separates account, measurement, inference, and hypothetical inputs |
| Decision quality | Bounded next step with explicit revise/stop conditions |
| Transfer | Changes the plan when the bottleneck or authority changes |

Different coherent plans can satisfy these criteria. No learner score or mastery state has been recorded.

## Executed arithmetic check

```python
from fractions import Fraction
n, review_minutes, overhead, hourly = 120, 3, 2, 300
onboarding = Fraction(12, 8)
new_hours = Fraction(n * review_minutes, 60) + overhead
assert new_hours == 8 and onboarding == Fraction(3, 2)
for old_minutes, hours, recurring, net, value in [
    (8, 16, 8, Fraction(13, 2), 1950),
    (4, 8, 0, Fraction(-3, 2), -450),
]:
    baseline = Fraction(n * old_minutes, 60)
    assert baseline == hours
    assert baseline - new_hours == recurring
    assert baseline - new_hours - onboarding == net
    assert net * hourly == value
assert 16 * hourly == 4800
assert 8 * hourly == 2400
print('PASS: two scenarios, units, onboarding allocation, and value arithmetic')
```

The checks validate calculations from assigned inputs, not the inputs themselves. Editorial checks matched all six exercise prompts to worked answers, reviewed claim scope and timestamp locators, and verified that no interviews, outreach, trial outcomes, or demand measurements were claimed. Audit A remains pending.
---

# B02 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| ID / revision / date | B02 answers · 1.0 · 2026-11-12 |
| Title | Unit economics, pricing units, and sensitivity — worked answers |
| Prerequisites | F02, B01, A05 and [B02 core](SDE_B02.md) |
| Capability developed | Audit denominators, cost boundaries and conditional decisions |
| Source-check status | R20/R21/R12 passages and URLs in the core evidence table |
| Experiment status | Exact Python arithmetic executed; no observed prices, customers or revenue |

These are reference solutions, not learner responses or mastery assessments.

## Hints

1. Failed cases consume routine resources too. Separate their additional handling.
2. Subtract variable costs before fixed overhead. Check the sign before dividing.
3. Replace all changed inputs, not just compute price.
4. Solve an inequality under one capacity range, then check whether the solution belongs to that range.
5. Use the recovery probability among failures. Original costs are already included.
6. A billable event needs a definition, evidence and a dispute rule.

## 1. Ledger and units

There are 800 successful and 200 failed cases. Compute costs 400, routine verification 1,000, routine support 200 and additional failure handling 400 U. Total variable cost is 2,000; adding 1,500 fixed cost yields 3,500 U. Variable cost per attempt is 2, per success 2.5, full cost per attempt 3.5 and full cost per success 4.375 U.

Routine verification applies to all 1,000 cases. Dividing only successful-case expenditure by 800 would hide failed work. The 2 U failure charge must be incremental to routine review/support. If the review minutes are salaried capacity rather than proportional purchases, revise the cash ledger; do not charge the same labor twice. Report capacity usage even when cash cost is fixed.

**Criterion:** All rows reconcile, units and denominators are explicit, and labor/cost categories do not overlap.

## 2. Contribution and break-even

Revenue is 800×4=3,200 U. Contribution is 3,200−2,000=1,200 U, or 1.2 per attempted case. Its revenue fraction is 1,200/3,200=3/8=37.5%. Modeled operating remainder is −300 U. At unchanged costs and quality, 1,500/1.2=1,250 cases cover the modeled fixed cost exactly.

For integer attempts and positive margin, round a noninteger break-even threshold upward. If margin is zero, positive fixed cost cannot be recovered; if negative, volume makes the result worse. This formula assumes sufficient demand and unchanged capacity cost. It excludes unlisted company expenses and collection delays. Contribution is neither total profit nor cash in the bank.

**Criterion:** Preserve the time horizon, positive-margin condition, cost scope and demand limitation.

## 3. Cheaper compute counterexample

Alternative variable cost is 0.1+3×0.5+0.3+0.3×2=2.5 U per attempt. At 700 successes, revenue is 2,800, variable costs 2,500, contribution 300 and modeled remainder −1,200 U. Variable cost per success is 25/7≈3.571 U. Baseline cost per success is 2.5 U. Compute fell from 0.4 to 0.1, but the complete system lost 900 U in monthly contribution.

Compare matched eligible cases with frozen verification standards, recording actual calls, active review/support, failures and deadline-qualified successes. A new model with lower review effort or higher success could reverse the result. The hypothetical ledger establishes only that compute price alone is insufficient.

**Criterion:** Recalculate the whole service; do not infer measured superiority or weaken quality to lower apparent cost.

## 4. Thresholds and capacity

Baseline cost c=3.6−2p, hence contribution m=6p−3.6 at P=4. It is positive above p=0.6. With N=1,000 and F=1,500, the remainder is 6,000p−5,100, so modeled break-even requires p≥0.85. At p=0.8, the cost-covering price is (2+1.5)/0.8=4.375 U.

Support rising from 0.2 to 0.7 adds 0.5 per case. Margin becomes 0.7 and the monthly remainder is −800. With overhead fixed at 1,500, baseline N=500,1,000,1,500 produces −900,−300,300. Above 1,500 the new overhead is 2,100; N=1,501 yields 1,801.2−2,100=−298.8. This tier breaks even at 2,100/1.2=1,750. Assume that volume fits the tier; do not extend it beyond a known capacity range.

The table varies one input at a time. For a real scenario, higher price can change N and customer mix; higher load can increase review delays and reduce p. Cost thresholds do not establish an acceptable offer.

**Criterion:** Correct inclusive versus strict thresholds, discontinuity and explicit coupling assumptions.

## 5. Conditional retry

Of 200 failures, recovery rate 1/4 produces 50 extra successes. The new rate is 850/1,000=0.85. Incremental cost is 200×1=200 U, incremental revenue 50×4=200, and incremental contribution zero. Total variable costs become 2,200, revenue 3,400, contribution remains 1,200 and remainder stays −300.

For 0≤p<1, positive incremental contribution requires Pr>d, or r>d/P for positive P. Here r>1/4. At p=1 there are no failures and therefore no retry increment regardless of r. At P=0 and positive d no paid recovery can improve contribution. The recovery rate is conditional on the failed-case population; independence is not assumed. A late or unverified recovery does not qualify under this contract.

**Criterion:** Do not double-charge original handling or treat retries as independent new cases. Preserve deadline and verification rules.

## 6. Offer and evidence

Per-attempt billing exposes the buyer to unsuccessful work; it needs an agreed eligibility and duplicate policy. Per-success billing exposes the supplier to failure costs and requires agreed verification/disputes. Subscription plus allowance requires workload limits and overage rules; averages can hide a costly heavy-use segment. These are hypotheses for customer testing, not commitments already obtained.

A bounded plan: select an authorized sample from the intended segment; freeze the success rubric; log all cases, costs and non-overlapping labor; reconcile invoices and observe a complete outcome window. Include failed and disputed work. Independently check a subset of success labels. Reconstruct who can authorize payment and what alternatives they use. Seek an explicit trial on stated terms rather than treating favorable interview comments as revenue. No outreach is performed by this file.

Reject or revise if permitted data cannot be obtained, actual review/failure costs exceed the feasible range, the buyer rejects the billing unit, useful outcomes fail quality/authority gates, or demand cannot cover fixed commitments. Preserve reasons and uncertainty; a single refusal is not proof of no market. Separate the cash ledger from the customer's released-capacity value.

**Criterion:** Operationally observable units, matched evidence, explicit rejection conditions and no invented willingness to pay.

## Executable checks

The script checks constructed counts, exact thresholds, ledger reconciliation, capacity tiers and conditional retries. The grid is sensitivity analysis, not sampling or an empirical confidence interval.

```python
from fractions import Fraction as Q
from itertools import product

def cost(p, compute=Q(2,5), minutes=2, support=Q(1,5)):
    assert 0 <= p <= 1
    return compute + minutes*Q(1,2) + support + (1-p)*2

def ledger(n,p,price=4,fixed=1500):
    revenue=n*p*price
    variable=n*cost(p)
    return revenue,variable,revenue-variable,revenue-variable-fixed

p=Q(4,5)
assert cost(p)==2
assert ledger(1000,p)==(3200,2000,1200,-300)
assert Q(2000,800)==Q(5,2) and Q(3500,800)==Q(35,8)
assert Q(1200,3200)==Q(3,8)
assert ledger(1250,p)[3]==0 and ledger(1249,p)[3]<0
assert cost(Q(7,10),Q(1,10),3,Q(3,10))==Q(5,2)
assert 1000*Q(7,10)*4-2500-1500==-1200
assert Q(2500,700)==Q(25,7)
assert ledger(1000,Q(3,5))[2]==0
assert ledger(1000,Q(17,20))[3]==0
assert ledger(1000,p,Q(35,8))[3]==0
assert [ledger(1000,x)[3] for x in [Q(3,5),p,Q(9,10)]]==[-1500,-300,300]
assert [ledger(1000,p,x)[3] for x in [3,5]]==[-1100,500]
assert 3200-1000*cost(p,support=Q(7,10))-1500==-800
assert [ledger(n,p)[3] for n in [500,1000,1500]]==[-900,-300,300]
assert ledger(1501,p,fixed=2100)[3]==Q(-1494,5)
assert ledger(1750,p,fixed=2100)[3]==0
# Exact observed partition agrees with the expected-cost formula.
for successes in range(1001):
    p0=Q(successes,1000)
    observed=400+1000+200+(1000-successes)*2
    assert observed==1000*cost(p0)
    assert (4*p0-cost(p0)>0)==(p0>Q(3,5))
    assert (ledger(1000,p0)[3]>=0)==(p0>=Q(17,20))
# Retry extension: all original failures offered exactly one extra attempt.
checks=0
for p0,r,price,d in product([Q(0),Q(4,5),Q(1)],
                             [Q(0),Q(1,4),Q(1,2),Q(1)],
                             [Q(0),Q(4),Q(5)],[Q(0),Q(1),Q(2)]):
    newp=p0+(1-p0)*r
    extra=(1-p0)*d
    delta=(1-p0)*(price*r-d)
    assert p0<=newp<=1
    assert newp*price-(cost(p0)+extra)-(p0*price-cost(p0))==delta
    if p0<1 and price>0:
        assert (delta>0)==(r>d/price)
    checks+=1
assert checks==108
assert p+(1-p)*Q(1,4)==Q(17,20)
assert (1-p)*(4*Q(1,4)-1)==0
# Cost per observed success is undefined at zero, not zero cost.
def per_success(total,successes):
    return None if successes==0 else Q(total,successes)
assert per_success(3600,0) is None
assert per_success(2000,800)==Q(5,2)
print('PASS: ledger, thresholds, 1001 success counts, capacity tiers, 108 retry cases and zero-success handling')
```

## Revision history

- 1.0 — 2026-11-12. Six worked answers and executed exact checks.
---

# B03 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| ID / revision / date | B03 answers · 1.0 · 2026-11-13 |
| Prerequisites | [B03 core pack](SDE_B03.md), B01 and B02 |
| Capability developed | Audit distribution denominators, compare responsibility boundaries and reject an economically inconsistent offer |
| Source-check status | Uses the core's verified R22/R21/R19 passages; proposals and numbers below are original |
| Experiment status | Embedded exact-arithmetic checks executed; no customer, acquisition or supplier experiment |
| Assessment convention | Criteria assess a future answer; no learner response or mastery is assumed |

## 1. Roles and activation

**Hint:** A customer is an organization with a workflow, not every person who likes the demonstration.

**Worked answer:** Target small purchasing teams with repeated invoice/delivery matching, a restricted format set and authority for a bounded pilot. Clerk: operator. Operations manager: budget owner. Data/security owner: access approver. Payment reviewer: final business decision owner. A bookkeeping practitioner's introduction to the buyer is a proposed route, contingent on permission and incentive; no introduction has happened.

Activation is one permitted real workflow completed to the agreed supported-evidence/deadline contract. Logging in, uploading an unusable document and viewing a canned demonstration are not equivalent. A low activation fraction could reflect difficult setup, but could also reflect absent data approval, a weak problem, immature follow-up or the wrong audience. Record the reason and time in state before choosing a repair.

**Assessment:** Names the distinct roles, an observable event and a rival explanation. Does not treat operator enthusiasm as purchase authority.

## 2. Denominators and follow-up

**Hint:** Write each transition as later-set count divided by earlier-set count.

**Worked answer:** Qualification is 12/40=30%; demo agreement is 6/12=50%; activation is 3/6=50%; second-cycle completion is 2/3≈66.67%. Their product is 5%, equal to 2/40. Nested sets explain this identity without statistical independence. This is descriptive repeat use within this constructed cohort, not a paid-retention estimate or a forecast.

The 600 U spend yields 200 U per activated organization and 300 U per repeated-use organization. Reporting the latter as “cost per acquired paying customer” would be unsupported. With zero activations the ratio has no finite value; keep the spend and zero count visible. Organizations that have not reached their next eligible cycle require pending/censored status and cohort-age tracking, not automatic classification as churned. A paid acquisition metric needs actual contracts/payments and consistently attributed sales costs.

**Assessment:** Correctly changes denominators, preserves set nesting and refuses to turn missing time or payment evidence into observed behavior.

## 3. Customer value and labor shocks

**Hint:** Count customer work and supplier work on different ledgers. Fees are a customer outflow and supplier inflow, not a new combined resource cost.

**Worked answer:** The baseline is 100×8/60×30=400 U/month. Self-serve releases 200 U/month before its fee; net is 6×(200−120)−4×30=360 U. Managed releases 300 U/month; net is 6×(300−180)−2×30=660 U. Internal releases 250 U/month; net is 6×(250−40)−12×30=900 U. These are valued-capacity comparisons, not guaranteed cash savings or prices customers accept.

Internal ranks first only if it meets quality/access requirements and the organization can operate it within the stated allowance. An unavailable IT owner invalidates that option regardless of its arithmetic. Managed at 5 customer minutes gives 6×(150−180)−60=−240 U. Internal with six additional maintenance hours/month gives 900−6×6×30=−180 U. Neither cost shock authorizes relaxing quality or access controls to restore a positive number.

A counterexample to “managed always saves more customer time” is a service whose ambiguous exception notes force the customer to repeat the original matching. Measure total effort from intake to verified completion, including rework. If customer labor is fixed payroll, freed time needs a useful next use before its assigned value becomes an actual benefit.

**Assessment:** Obtains all five results, states units and does not double-count baseline maintenance in the incremental shock.

## 4. Supplier economics and payback

**Hint:** Supplier onboarding is distinct from customer onboarding. Include both where appropriate, but never on the same party's ledger unless that party actually bears both.

**Worked answer:** Self-serve contribution is 120−40=80 U/month; managed is 180−120=60. After six paid months, self-serve leaves 480−60−200=220 U and managed leaves 360−90−200=70 U. This excludes shared overhead and all unlisted costs; the remainders do not prove company profitability.

Acquisition plus onboarding is 260 versus 290 U. Continuous recovery times are 3.25 and 29/6≈4.83 months. With payments/contribution realized at month end, the earliest sufficient receipts are in months 4 and 5. Three paid months yield −20 and −110 U. The model assumes steady volume, full collection, unchanged variable costs and no extra cancellation costs. Billing in advance, late payments or refunds changes cash timing. Annualized revenue does not supply the missing cash automatically.

The 200 U acquisition assumption is applied equally to isolate delivery differences; real channels could have very different costs. The earlier cohort contains activation counts but no payments, so this comparison explicitly assumes each modeled acquired organization pays. It does not claim that the cohort demonstrated that assumption.

**Assessment:** Distinguishes contribution, recovery, profitability and collection; names at least one empirically unknown premise.

## 5. Bundling and incompatible thresholds

**Hint:** Derive the customer's maximum fee and supplier's minimum fee separately before looking for overlap.

**Worked answer:** The hypothetical bundle releases 150 U/month and costs 90 U to onboard, yielding 810 U over six months. Managed's value at fee f is 6(300−f)−60=1,740−6f. To match 810 requires f≤155. Its supplier remainder is 6(f−120)−290; nonnegative remainder requires f≥505/3≈168.33. Since 155<168.33, there is no fee satisfying both constraints.

At f=155 the supplier loses 80 U on this limited ledger. At the supplier floor the customer gets 730 U, which is 80 U less than the bundle. Price alone cannot resolve the conflict. At f=155, supplier variable monthly delivery cost must fall to at most (930−290)/6=320/3≈106.67 U for six-month recovery. That is a conditional cost target, not permission to remove necessary review or a prediction of automation savings.

Possible next evidence: the bundle may fail the required provenance/authorization contract; managed may create measurable value beyond handling time; reusable onboarding may reduce costs. Each possibility changes a premise and must be measured. If the bundle matches the whole job and the cost target cannot be met, decline or change the segment. The free component's existence is a scenario assumption, not a current supplier announcement.

**Assessment:** Shows both inequalities and rejects a purely rhetorical moat defense. Accepts a different choice only with explicit changed assumptions.

## 6. A bounded pilot and a moat test

**Hint:** The pilot should resolve a decision, not collect favorable anecdotes indefinitely.

**Worked analysis:** Propose one four-week learning pilot with two authorized organizations from the narrow segment, followed by an agreed second workflow cycle where timing permits. This small scope is a practical learning budget, not statistical sufficiency. No outreach is executed. Freeze eligibility, source revisions, case identities, output rubric, deadlines and approval roles. Compare managed and existing-process results on matched permitted cases. Record total active minutes by role, errors, unresolved cases, rework, fees, non-overlapping supplier labor and setup time. Preserve case-level discrepancies rather than presenting only the average.

Start in a non-effecting evaluation mode: outputs do not approve or dispatch payment. Human supplier access must be expressly scoped; an internal interface must not hide external calls. Stop processing on an unauthorized disclosure/effect, unresolved authority issue or inability to preserve required evidence. Pause expansion if recurring labor exceeds the budget or quality falls below the agreed contract. A negative value result can justify changing the offer rather than expanding the pilot until a favorable average appears.

For the workflow-knowledge advantage, ask whether setup on the second organization reuses a documented mapping procedure and lowers effort without weaker quality. A new organization with unrelated formats may falsify repeatability. For a data advantage, ask whether rights permit reuse and whether that permitted corpus improves held-out whole-task outcomes relative to a credible alternative. More records with no reusable rights are not a reusable data advantage. No measured effect means the improvement claim stays unknown.

Choose self-serve if ordinary customers can operate the same workflow reliably with bounded support. Choose internal if access restrictions rule out external processing and a funded owner can maintain it. Keep managed if recurring operator expertise produces valuable outcomes at sustainable cost. If a bundle matches the whole task and both parties' economics cannot be satisfied, stop or redefine the offer. A paid pilot alone does not establish repeated demand, scale or a moat.

**Assessment:** Contains a bounded decision, authority limits, effort/quality measures, stop rule, rival explanation and observable conditions for changing boundaries. Does not invent trial results.

## Reproducible exact checks

The following Python standard-library script was executed during production. It verifies the constructed ledger and decision boundaries, not real business behavior. Fractions avoid floating-point ambiguity at equality. Grid checks complement exact boundaries rather than proving behavior outside this model.

```python
from fractions import Fraction as Q
from math import ceil

H, n, b, w = 6, 100, 8, 30

def value(t, fee, infra, onboarding):
    return H * (Q(n * (b-t) * w, 60) - fee - infra) - onboarding*w

def remainder(fee, variable, onboarding, months=6):
    return months*(fee-variable)-onboarding-200

counts = [40, 12, 6, 3, 2]
product = Q(1)
for before, after in zip(counts, counts[1:]):
    assert 0 <= after <= before
    product *= Q(after, before)
assert product == Q(2, 40) == Q(1, 20)
assert Q(600, 3) == 200 and Q(600, 2) == 300

def per_activation(spend, count):
    return Q(spend, count) if count else None
assert per_activation(600, 0) is None

assert [value(4,120,0,4), value(2,180,0,2),
        value(3,0,40,12)] == [360,660,900]
assert value(5,180,0,2) == -240
assert value(3,0,40+6*w,12) == -180
assert remainder(120,40,60) == 220
assert remainder(180,120,90) == 70
assert remainder(120,40,60,3) == -20
assert remainder(180,120,90,3) == -110
assert Q(260,80) == Q(13,4)
assert Q(290,60) == Q(29,6)
assert [ceil(Q(260,80)), ceil(Q(290,60))] == [4,5]

bundle = value(5,0,0,3)
ceiling, floor = Q(155), Q(505,3)
assert bundle == 810
assert value(2,ceiling,0,2) == bundle
assert remainder(floor,120,90) == 0
assert ceiling < floor
assert remainder(ceiling,120,90) == -80
assert value(2,floor,0,2) == 730
assert remainder(155,Q(320,3),90) == 0

# Exact equality and values immediately on both sides.
for delta in [Q(-1,100), Q(0), Q(1,100)]:
    assert (value(2,ceiling+delta,0,2) >= bundle) == (delta <= 0)
    assert (remainder(floor+delta,120,90) >= 0) == (delta >= 0)

# 2,401 fee points from 0 through 240 U at 0.1-U spacing.
for k in range(2401):
    fee = Q(k,10)
    customer_ok = value(2,fee,0,2) >= bundle
    supplier_ok = remainder(fee,120,90) >= 0
    assert customer_ok == (fee <= ceiling)
    assert supplier_ok == (fee >= floor)
    assert not (customer_ok and supplier_ok)

# 25 maintenance increments, 0..12 h/month at half-hour spacing.
for k in range(25):
    hours = Q(k,2)
    assert value(3,0,40+hours*w,12) == 900-180*hours
print('PASS: cohort, ledgers, labor shocks, payback, exact thresholds, 2401 fee points, 25 maintenance points')
```

Limitations: no statistical confidence interval, cash-flow simulation, empirical retention curve, supplier equivalence experiment or security verification was performed. Those require actual data and an implemented system. Source provenance remains in the core's evidence ledger.

## Revision history

- 1.0 — 2026-11-13. Six mapped solutions, conditional pilot and executed arithmetic checks.
---

# C01 — Worked decision analysis and checks

| Field | Value |
| --- | --- |
| ID / title | C01 answers · Duplicate-effect responsibility |
| Revision / date | 1.0 · 2026-11-07 |
| Prerequisites | F01, S02–S04; [C01 memo](SDE_C01.md) |
| Capability developed | Evaluate an invariant across a transaction boundary and revise an uncertain-outcome policy |
| Source-check status | R10 pp. 2, 6–7 and R07 §8 p. 13; exact links in the memo |
| Experiment status | Executed standard-library Python finite checks below; atomic transitions assumed, not deployment-tested |

This is a reference analysis for later self-assessment. It does not report your answers or mastery. A different design can be defensible if it preserves the stated invariants and openly changes any progress promise.

## Hints before the analysis

1. Missing knowledge and missing effects are different facts. Put each actor in its own column.
2. Count accepted decisions and provider effects separately. Identify what equality means at each layer.
3. Ask what happens between the effect and the durable record used to suppress its retry.
4. On restart, retain only what the model says was committed. Replay the original identity, not a fresh attempt identity.
5. Find two histories with identical local evidence and different provider outcomes. A local policy sees the same input in both.

## 1. Timeline and knowledge

A valid timeline is: application commits approval and pending intent p; dispatcher sends p; provider atomically executes and remembers p; reply disappears; dispatcher restarts with p pending. The application knows the approval committed but does not know whether the provider completed. The provider knows its own result. The client may know neither if its initial approval reply also disappeared.

An approval retry with k resolves the application decision. A provider retry with p resolves the payment under the baseline contract. These are different queries. Returning a historical `approved/payment_pending` receipt must not be presented as a fresh assertion that payment is still pending or that the approval is still current. Use a separate authorized status read for current lifecycle information.

The inadequate design sends without provider identity, then saves a local marker. A crash after the effect creates the possibility of two payments even though only one local receipt eventually exists. In the alternative marker-first design, a crash before send creates zero payments while the application believes it finished.

**Assessment:** Name both durable states and the lost observation. “The timeout means payment failed” is incorrect under the model.

## 2. Invariants, identity and retention

Write `acceptances(doc,epoch) <= 1` and `effects(p) <= 1`. These count different events. The first is enforced by the application's atomic empty-slot transition. The second is enforced by the provider's atomic first-use transition. The application contributes by mapping every dispatch of one intent to the same p.

k identifies the caller's intended approval request, including a canonical payload. p identifies the external payment intent created by a successful approval. Epoch distinguishes successive business rounds even when the published revision remains unchanged. Neither leadership term nor retry attempt count is a replacement for epoch. Tenant scope and authenticated receipt access are necessary operational boundaries.

Evidence references identify the revision and exact source used by the accepted decision. Keep the source bytes retrievable; retaining a digest without the bytes cannot reconstruct the document. S02's immutable revisions and S03's retained receipts supply this continuity. Replaying an accepted k after reopen returns historical information; a fresh key carrying the old epoch is rejected.

Receipt/provider-identity retention must include delayed deliveries and recovery from older application state. An arbitrary cache TTL is not sufficient. If provider history expires while a dispatcher can replay p, the provider may treat p as new. Preserve a tombstone or establish that old attempts cannot recur before removing the distinguishing information. The exact mechanism depends on provider support.

**Assessment:** State both invariants, payload binding and retention scope. A key alone does not prevent two different keys from representing the same real-world obligation.

## 3. Choice and atomic boundary

The baseline chooses a guarded, durable application decision plus pending intent and provider-enforced p. The application must atomically preserve owner, receipt, evidence and intent. If intent creation were separate, a crash after approval could leave no dispatchable payment; creating the intent first could pay for a decision that never committed.

Every external dispatch uses the saved payload and p. Provider result recording can occur later because replaying p is safe under the provider contract. That asymmetry is the reason the design can cross the boundary without pretending both databases share one transaction.

A local set improves performance but lacks shared durable state. A global lock without atomic durable effect control still leaves the external crash gap. More application replicas preserve intent information but cannot infer an unobserved provider result. A queue may repeatedly deliver the same intent safely only when the effect authority supplies the corresponding identity guarantee.

**Assessment:** Identify the exact atomic writes and the external assumption. Do not claim that an outbox, consensus or a unique database row alone gives exactly-once payment.

## 4. Crash cuts and competing decisions

| Cut | Durable state after restart | Safe baseline continuation |
| --- | --- | --- |
| Before local commit | No accepted receipt or intent | Retry k; it may create the decision once |
| After local commit, before dispatch | Approval, receipt and pending p | Dispatch p |
| After provider effect, before reply | Pending p locally; provider remembers effect | Repeat p; receive existing result |
| After reply, before local completion | Same durable uncertainty as preceding row | Repeat p or use an authoritative status operation |
| After local completion | Recorded result and completed intent | Return saved result; no new dispatch needed |

For competing keys A and B in epoch 7, whichever valid transition consumes the empty slot first wins. The other cannot create another intent. A repeated delivery of the winner returns its original receipt. This applies to all three distinct orders of A,A,B checked below. The model does not estimate how often any order occurs.

After reopen to epoch 8, replaying the winner of epoch 7 is historical retrieval, not a new consumption of epoch 8. A new key with epoch 7 is stale. A properly authorized new request for epoch 8 can succeed; it creates a distinct intent. If that could double-pay one obligation, a cross-epoch obligation rule is missing from the requirements. The memo deliberately does not equate an approval round with an economic obligation.

**Assessment:** Preserve durable state consistently and never invent a new payment identity after a lost reply. Explain why reopen does not undo an already dispatched external effect.

## 5. Changed provider and revised decision

With neither deduplication nor authoritative status, H0 (no effect) and H1 (effect, lost reply) leave the same local observation. A deterministic automatic decision must act the same way in both. Retrying may complete H0 but duplicate H1. Stopping avoids a new attempt but leaves H0 incomplete. Randomizing the decision does not establish a universal guarantee either.

Record `outcome_unknown`, block automatic resubmission and obtain authoritative reconciliation evidence. A person seeing an empty dashboard is not enough if an old request may still execute. Safe resumption would require, for example, provider confirmation that the original attempt was definitively rejected/cancelled and cannot later execute, or a newly negotiated identity contract that actually covers the old attempt. Otherwise the state remains unresolved.

The revised policy withdraws automatic eventual completion while retaining a conservative submission policy. It does not claim universal at-most-once behavior from a provider whose own semantics are unknown. If the business demands both automatic progress and no duplicate effects, this provider contract fails the requirements; change the integration or the requirement explicitly.

**Assessment:** Give the indistinguishable histories and name the surrendered progress claim. “Retry with a new key,” “wait longer,” and “add consensus” do not supply the missing external evidence.

## Reproducible finite checks

The code models indivisible application/provider transitions and complete restoration of committed state using copies. It does not test actual transaction isolation, flush behavior, network delivery, provider retention or Raft. Crash cuts are boundaries in the model, not injected process failures. The invariant argument explains arbitrary retries under the assumptions; the finite cases catch inconsistent examples and expose broken alternatives.

```python
from copy import deepcopy
from itertools import permutations

class Authority:
    def __init__(self):
        self.epoch, self.rev = 7, 2
        self.owners, self.receipts, self.intents = {}, {}, {}
    def approve(self, key, epoch=7, rev=2, amount=100):
        payload = ('tenant', 'D17', epoch, rev, 'reviewer', 'evidence-2', amount)
        if key in self.receipts:
            old, result = self.receipts[key]
            return result if old == payload else 'key-conflict'
        if (epoch, rev) != (self.epoch, self.rev):
            return 'stale'
        if epoch in self.owners:
            return 'occupied'
        # One indivisible durable transition is ASSUMED here.
        p = ('tenant', 'D17', epoch)
        result = ('approved/payment_pending', p)
        self.owners[epoch] = key
        self.receipts[key] = (payload, result)
        self.intents[p] = {'amount': amount, 'done': False}
        return result
    def reopen(self):
        self.epoch += 1

class Provider:
    def __init__(self):
        self.records, self.effects = {}, []
    def pay(self, p, amount):
        # Assumed atomic provider contract, not its implementation.
        if p in self.records:
            old, result = self.records[p]
            if old != amount:
                return 'payload-conflict'
            return result
        result = ('paid', len(self.effects) + 1)
        self.effects.append((p, amount))
        self.records[p] = (amount, result)
        return result

# All orders of two deliveries of A and one competing B.
orders = sorted(set(permutations(('A', 'A', 'B'))))
for order in orders:
    a = Authority()
    for key in order:
        a.approve(key)
    assert len(a.owners) == len(a.receipts) == len(a.intents) == 1
    winner = a.owners[7]
    saved = a.approve(winner)
    assert a.approve(winner, amount=101) == 'key-conflict'
    a.reopen()
    a = deepcopy(a)  # restoration assumes complete durable state
    assert a.approve(winner) == saved  # historical, not a new approval
    assert a.approve('old-new-key') == 'stale'
    assert a.approve('C', epoch=8)[0] == 'approved/payment_pending'
    assert len(a.owners) == len(a.intents) == 2

# Cut points: 0 before application commit; 1 before dispatch;
# 2 after provider effect before reply; 3 after reply before local done;
# 4 after local done. Restart preserves committed state only.
for cut in range(5):
    a, provider = Authority(), Provider()
    p = ('tenant', 'D17', 7)
    if cut >= 1:
        a.approve('A')
    if cut >= 2:
        provider.pay(p, 100)
    if cut >= 4:
        a.intents[p]['done'] = True
    a, provider = deepcopy(a), deepcopy(provider)
    a.approve('A')
    if not a.intents[p]['done']:
        assert provider.pay(p, 100)[0] == 'paid'
        a.intents[p]['done'] = True
    # Additional concurrent/repeated deliveries, serialized by contract.
    for _ in range(3):
        assert provider.pay(p, 100)[0] == 'paid'
    assert len(provider.effects) == 1 and a.intents[p]['done']
    assert provider.pay(p, 101) == 'payload-conflict'
    assert len(provider.effects) == 1

# Counterexamples: effect-first marker, marker-first effect, expiry.
effects, marker = 1, False  # crash after external effect
if not marker:
    effects += 1
assert effects == 2
marker, effects = True, 0  # crash before send; marker prevents retry
assert marker and effects == 0
provider = Provider()
provider.pay('p', 100)
provider.records.clear()  # identity expiry without ending replay horizon
provider.pay('p', 100)
assert len(provider.effects) == 2

# Same local observation, different external outcomes, no identity support.
observations = [('pending', 'no_reply'), ('pending', 'no_reply')]
assert observations[0] == observations[1]
for initial_effects in (0, 1):
    retry_effects = initial_effects + 1
    if initial_effects == 1:
        assert retry_effects == 2
    else:
        assert initial_effects == 0  # no retry leaves H0 incomplete
print('PASS: 3 competing-delivery orders; payload binding, stale epoch,')
print('historical replay and reopen; 5 crash cuts; provider retries;')
print('marker-order and identity-expiry counterexamples; ambiguous histories.')
```

Observed output, 2026-11-07:

```text
PASS: 3 competing-delivery orders; payload binding, stale epoch,
historical replay and reopen; 5 crash cuts; provider retries;
marker-order and identity-expiry counterexamples; ambiguous histories.
```

No real provider was called. Deployment checks still need provider contract review, controlled failure injection, restore tests, retention verification, unauthorized-path tests and obligation-identity decisions. Those are application needs, not evidence of learner mastery.

## Revision history

- 1.0 — 2026-11-07. Five worked analyses, criteria, hints and executed finite checks corresponding to C01 revision 1.0.
---

# C02 — Worked analysis and checks

| Field | Value |
| --- | --- |
| ID / revision / date | C02 answers · 1.0 · 2026-11-11 |
| Title | Model performance and customer outcomes — worked analysis |
| Prerequisites | F02/F03, A01/A03/A05, B01 and [C02 memo](SDE_C02.md) |
| Capability developed | Defend a conditional choice and an evaluation that could reverse it |
| Source-check status | R03/R19 passages recorded in the memo |
| Experiment status | Exact arithmetic, paired-set and sensitivity checks executed; no live trial |

These are reference analyses, not learner responses.

## Hints

1. Subtract late-correct cases from eventual correctness; keep every eligible case in the denominator.
2. Preserve outputs and costs when changing the deadline. Apply the stated objective.
3. Compare differences, not just ratios. Staff time is valued capacity, not automatically removed payroll.
4. Offline pairing and live random assignment answer different questions.
5. A model benchmark cannot establish that the buyer's bottleneck is evidence assembly.

## 1. Initial decision

Correct on-time counts are C=90−4=86, A=92−4=88 and B=96−12=84. Correct, incorrect and unresolved counts each total 100 for every option. Late cases are a subset of correct outcomes, not an additional category to add to that total.

At 0.5 units per minute, charges are C=0+800×0.5=400, A=100+400×0.5=300 and B=200+300×0.5=350. Per eligible case they are 4,3 and 3.5 units; per timely correct case they are 200/43≈4.65,75/22≈3.41 and 25/6≈4.17. Neither measure is profit. Failed work stays in the numerator.

Paired A/B outcomes: 76 both succeed, 12 A-only, 8 B-only, 4 neither. A=88, B=84; B−A=−4 points. Marginal counts alone would conceal the twelve regressing cases. The ledger does not support a p-value or an empirical confidence interval because its inputs were assigned, not sampled.

Only A meets all initial gates. C fails the timely-count and charge gates. B passes the charge/error limits but misses the timely-count threshold. A has no established market advantage: this is a conditional next-investigation choice.

**Criterion:** Correct partition and paired arithmetic; distinguish conditional decision from observed superiority.

## 2. Revised deadline

Add the newly timely correct outcomes: C=86+2=88, A=88+2=90, B=84+10=94. Costs remain 400,300,350. C still exceeds 360; A and B now meet all count/error/budget gates. Maximizing timely correct outcomes chooses B.

Cost per success remains lower for A: 300/90=10/3 versus B's 350/94=175/47≈3.72. This is not a contradiction. Ratio minimization and maximizing success subject to a budget are different objectives. If minimizing charge per success is the true buyer objective, retain A; explicitly revise the objective rather than claiming the original rule selected it.

A feasible paired realization is A's first-day success set 1–88 and B's set 1–76 plus 89–96. By day two A adds 89–90 and B adds 77–86. Then both succeed on 88 cases, A alone on 2, B alone on 6 and neither on 4. Sets grow monotonically with deadline, while outputs are unchanged. The executable construction demonstrates consistency, not an observed customer trace.

**Criterion:** Change only the constraint, retain gates/costs, and identify the objective responsible for the reversal.

## 3. Sensitivity and incremental value

At r=0.5, B costs 50 units more and adds four timely correct outcomes at day two. Under linear value v per success, net-value difference B−A is 4v−50. B wins for v>12.5, ties at 12.5 and loses below it. The chosen v must reflect a real outcome value, not an invented model benchmark score.

With staff-value rate r≥0, C costs 800r, A costs 100+400r and B costs 200+300r. B−A=100−100r, so B's total charge is lower only for r>1. At r=1 they tie. Both can still violate the absolute budget: A requires r≤260/400=0.65; B requires r≤160/300=8/15≈0.5333. Thus B cannot be cheaper than A while both satisfy this fixed 360-unit budget in this model. Sensitivity thresholds must be interpreted with all constraints.

In the original r=0.5 setting, lowering the budget from 360 to 300 at day two leaves A feasible and removes B. A favorable value ratio cannot make an unaffordable option feasible.

**Criterion:** Exact crossover, feasible-region reasoning and no claim that labor value equals cash savings.

## 4. Evaluation design

Offline: freeze versions, evidence available at intake, eligibility, rubric and budgets. Pair options on each case; group revisions and retries. Hold out time or suppliers according to the claim. Repeat stochastic runs under a fixed policy, preserving both within-case variation and between-case diversity. Report all outcomes and severe regressions; use group-aware uncertainty only with defensible independent units and assumptions.

Leakage example: retrieving a corrected invoice published after the original decision time. Component correctness can then appear excellent while using unavailable evidence. A separate common-evidence diagnostic isolates answer construction but does not replace the full-system test.

Live: establish an authorized, bounded trial with stable team-level assignment when reviewers share learning or queues. Prespecify horizon, outcome, data-quality checks, guardrails, stopping and uncertainty analysis. Determine sample size using independent-team variability and a minimally useful effect. Report all assigned eligible cases, including non-use; do not compare only enthusiastic adopters with all controls.

Interference example: treatment changes a shared retrieval cache or review queue, improving or delaying control. Either isolate the unintended sharing or explicitly design an estimand that includes the interaction. Individual-request randomization does not magically remove it. A faster component on replay cannot establish a causal reduction in human work or an adoption effect.

**Criterion:** Separate diagnostic, predictive and causal claims; preserve the clock, unit and missing-outcome rule.

## 5. Customer evidence and stopping

Unknowns include whether matching causes consequential delay, who values released time, whether deadlines can change, what errors cost, who authorizes data use and whether a buyer will adopt. Ask for a recent delayed case and reconstruct active work versus waiting with its artifacts. Compare against the existing workaround, including doing nothing or changing review scheduling.

A concrete milestone is a sponsor authorizing a bounded sample, naming a reviewer, agreeing to dates and a success rubric, and specifying how released capacity would be used. This is evidence for one trial, not market validation. Stop or revise the project if matching is already fast, the important delay is elsewhere, safe data access cannot be authorized, or the trial shows no useful outcome despite component gains. A refusal can also reflect recruitment mismatch; record the reason.

**Criterion:** Observable behavior and specific episodes; no invented interview, willingness to pay or commitment.

## Executable checks

This script verifies constructed counts and logical implications. It does not run a model, recruit participants, calculate empirical uncertainty or execute payments.

```python
from fractions import Fraction as F
correct={'C':90,'A':92,'B':96}
wrong={'C':2,'A':2,'B':1}
unresolved={'C':8,'A':6,'B':3}
late={'C':4,'A':4,'B':12}
minutes={'C':800,'A':400,'B':300}
resource={'C':0,'A':100,'B':200}
one={k:correct[k]-late[k] for k in correct}
two={k:one[k]+x for k,x in zip(correct,[2,2,10])}
cost={k:resource[k]+F(1,2)*minutes[k] for k in correct}
assert one=={'C':86,'A':88,'B':84}
assert two=={'C':88,'A':90,'B':94}
assert cost=={'C':400,'A':300,'B':350}
for k in correct:
    assert correct[k]+wrong[k]+unresolved[k]==100
    assert one[k]<=two[k]<=correct[k]
assert [cost[k]/one[k] for k in correct]==[F(200,43),F(75,22),F(25,6)]
assert [cost[k]/100 for k in correct]==[F(4),F(3),F(7,2)]

def choose(success,budget=360):
    feasible=[k for k in correct if success[k]>=88 and wrong[k]<=2 and cost[k]<=budget]
    return max(feasible,key=lambda k:(success[k],-cost[k])) if feasible else None
assert choose(one)=='A' and choose(two)=='B'
assert choose(two,300)=='A' and choose(two,299) is None
A=set(range(1,89));B=set(range(1,77))|set(range(89,97));U=set(range(1,101))
def paired(a,b):return (len(a&b),len(a-b),len(b-a),len(U-(a|b)))
assert paired(A,B)==(76,12,8,4)
A2=A|{89,90};B2=B|set(range(77,87))
assert paired(A2,B2)==(88,2,6,4)
assert A<=A2 and B<=B2
assert F(len(B)-len(A),100)==F(-1,25)
assert cost['A']/two['A']<cost['B']/two['B']
assert F(cost['B']-cost['A'],two['B']-two['A'])==F(25,2)
# 201 labor-value points check charge crossover, plus exact boundaries.
for i in range(201):
    r=F(i,100);a=100+400*r;b=200+300*r
    assert (b<a)==(r>1)
    assert (a<=360)==(r<=F(13,20))
    assert (b<=360)==(r<=F(8,15))
assert 100+400*F(13,20)==360
assert 200+300*F(8,15)==360
for v in [F(0),F(12),F(25,2),F(13),F(100)]:
    assert (4*v-50>0)==(v>F(25,2))
print('PASS: partitions, paired sets, deadline reversal, costs, 201 sensitivity points and boundaries')
```

## Revision history

- 1.0 — 2026-11-11. Five analyses and executed conditional-decision checks; no learner assessment inferred.
---

# C03 — Worked analysis and reproducible checks

| Field | Value |
| --- | --- |
| ID / title | C03 answers · Capacity decision analysis |
| Revision / date | 1.0 · 2026-11-13 |
| Prerequisites | [C03 memo](SDE_C03.md), S01/S05, A04, B02 |
| Capability developed | Audit the constraints and denominators behind an optimization recommendation |
| Source-check status | Uses the memo's R16/R09 passages; numerical work is original |
| Experiment status | Exact scheduling, memory, threshold and cost checks executed; no model or hardware trial |
| Assessment | Criteria concern a future answer, not inferred learner mastery |

## 1. Memory feasibility

**Hint:** Count weights once per replica and cached positions once per active request.

**Worked analysis:** Each peak request costs 4,096×128 KiB=512 MiB. Four require 2 GiB. Weights plus other reserve plus request state total 12+4+2=18 GiB, leaving 6 GiB beyond the counted reservation on that device. The original KV pool is 8 GiB; the four requests consume only a quarter of it. Two replicas each need their own 18 GiB budget, not 18 GiB shared between them.

This is a conservative cap including output growth, not merely a snapshot of prompt memory. It holds only if the other-memory reserve is sufficient. A memory-only change that preserves the feasible schedule and service law cannot alter completion times. It becomes consequential if allocation previously prevented a useful batch, but that new schedule must still meet the deadline. Physical memory fit does not establish bandwidth, compute or latency capacity.

**Criteria:** Correct byte conversions, per-device accounting and a conditional reason that reducing memory can leave useful capacity unchanged.

## 2. Starting trace and speedup

**Hint:** Compute one complete batch, then add queue delay for the second wave.

**Worked analysis:** At b=4,d=4, B is 16+4×8=48 ms and P is 8+4×8=40 ms. One replica finishes its waves at s and 2s: B at 48 and 96, P at 40 and 80. Two B replicas finish all tasks at 48. With four requests per wave, mean response is (s+2s)/2=1.5s for B/P; R's mean is 48. Means are therefore 72, 60 and 48 ms. Counts within 90 ms are 4,8,8.

Prefill is 16/48=1/3 of B's service. Halving it gives 48/40=6/5 speedup. Removing it entirely leaves 32 ms, limiting this particular phase-only speedup to 48/32=3/2. A 2× component improvement is not a 2× whole-batch improvement. Nor is amortized batch time s/4 the response time of an individual task.

**Criteria:** Correctly distinguishes latency, work and wave scheduling. Does not import a benchmark result into the invented timing law.

## 3. Cost and choice

**Hint:** Apply the same purchased window even if a policy stops being busy sooner.

**Worked analysis:** Eight attempted tasks incur 40 U of verification/accounting cost in every policy. B/P each buy 200 replica-ms, so each costs 240 U. R buys 400 replica-ms, so costs 440 U. Dividing by useful counts yields 60,30,55 U. B's lower total bill than R does not make B acceptable under the all-eight objective. P and R both pass; P is cheaper.

Busy replica-time is 96,80,96 ms. R parallelizes the same baseline work; it does not halve total work. A busy-only bill would instead be 136,120,136 U including the common 40, which describes a different pricing assumption. Do not silently switch between the two.

If P has additional implementation expense K relative to R, after m identical qualifying windows its saving net of that expense is 200m−K. For positive K, continuous recovery is K/200 windows; whole-window recovery is its ceiling. This calculation omits maintenance and any later workload change. With K=1,000 U, five such windows recover it exactly. This is an illustrative expense, not a quote. If the long-output workload arrives before recovery, the saving premise fails.

**Criteria:** Reports unsuccessful-work costs, idle capacity and excluded costs; keeps quality/coverage as a gate rather than optimizing a ratio at any cost.

## 4. Changed workload and startup

**Hint:** Replace d, not the task count, objective or quality bar.

**Worked analysis:** At d=8, B/R batch time is 16+8×8=80 ms; P is 8+8×8=72. B waves end at 80/160 and P at 72/144; R completes eight at 80. Means are 120/108/80. Useful counts are 4/4/8 and costs per useful result 60/60/55. R is now the only qualifying policy.

For all eight to finish: B requires 32+16d≤90, so integer d≤3; P requires 16+16d≤90, so d≤4; R requires 16+8d≤90, so d≤9. These conditions include d=0 if prefill alone supplies the whole output. They do not certify real workloads with the same token count. At d=10, R needs 96 ms, and adding identical replicas cannot reduce an individual batch's 96 ms under this policy. Smaller batches or a different kernel are separate options.

With the second replica ready at h, its four assigned tasks finish at h+80. At h=0,10,11, all-eight counts are respectively 8,8,4. Equality at 90 is allowed. This policy deliberately waits for the second replica for that batch; other routing choices require another trace. Startup costs must be added if the warm-capacity billing premise changes.

**Criteria:** Revises the recommendation and explains the precise constraint causing reversal. Correctly handles inclusive deadlines and does not call requested capacity ready capacity.

## 5. A falsification-oriented measurement plan

**Hint:** A fair experiment can produce evidence against the optimization you prefer.

**Worked analysis:** Replay matched permitted cases with identical arrival timestamps and output requirements. Freeze model/configuration, data revisions, validation rules and allowed effects. Record phase durations and complete serving response separately; keep retrieval/network/user time in a separate end-to-end measure. Compare ordinary traffic, bursts, sparse single requests, unequal outputs and larger prompts. Count rejected, late and unsupported tasks among all offered tasks. Include provisioned idle time, startup, memory growth, retry costs and verification work.

For sparse one-task windows at b=1,d=4, B takes 10+20=30 ms and P 5+20=25; both are useful. A permanently purchased second replica adds cost without adding a timely result. A scale-down policy could change this cost comparison, but is not the stipulated R policy. For unequal outputs, record batch composition and longest-member blocking; an average length does not reconstruct per-task waiting. Inspect continuous scheduling separately.

If one P output is unsupported, its eight timely outputs become seven timely-correct results, failing the required gate even if its cost ratio remains attractive. If a model variant omits necessary evidence, lower latency cannot be credited as an equivalent optimization. For production tails, use representative arrivals over repeated windows and an explicit percentile convention and uncertainty analysis. This eight-task deterministic trace is not a sample supporting a production p99 estimate.

**Criteria:** Includes at least one observation that rejects each candidate, matched quality and authority boundaries, explicit units and a fair offered-load denominator. No outreach, model execution or real measurement is implied by this proposed plan.

## Executed checks

The standard-library script below ran successfully during production. It independently constructs wave schedules and checks them against the closed-form thresholds. It also checks zero-success handling and exact boundary cases. The 200 ms billing comparison is used only for the two main workloads, whose traces drain inside it; longer synthetic traces below are timing-only sensitivity checks.

```python
from fractions import Fraction as Q
from math import ceil

GiB, KiB = 2**30, 2**10
kv = 4096*128*KiB
assert kv == GiB//2
assert 12*GiB + 4*GiB + 4*kv == 18*GiB

def service(b,d,fast=False):
    pre = Q(8+2*b,2) if fast else Q(8+2*b)
    return pre+d*(4+b)

def schedule(n,d,replicas=1,fast=False):
    free=[Q(0)]*replicas
    finishes=[]
    busy=Q(0)
    remaining=n
    while remaining:
        b=min(4,remaining)
        device=min(range(replicas),key=lambda j:(free[j],j))
        elapsed=service(b,d,fast)
        free[device]+=elapsed
        finishes.extend([free[device]]*b)
        busy+=elapsed
        remaining-=b
    return sorted(finishes),busy

def good(finishes,deadline=90):
    return sum(t<=deadline for t in finishes)

def cost_per(cost,successes):
    return Q(cost,successes) if successes else None

policies=[(1,False),(1,True),(2,False)]
for d,expected,means,counts in [
    (4,[[48]*4+[96]*4,[40]*4+[80]*4,[48]*8],[72,60,48],[4,8,8]),
    (8,[[80]*4+[160]*4,[72]*4+[144]*4,[80]*8],[120,108,80],[4,4,8])]:
    for i,(k,fast) in enumerate(policies):
        f,busy=schedule(8,d,k,fast)
        assert f==expected[i]
        assert sum(f)/8==means[i] and good(f)==counts[i]
        assert max(f)<=200
        assert busy==2*service(4,d,fast)
        cost=200*k+5*8
        assert cost_per(cost,good(f))==([60,30,55] if d==4 else [60,60,55])[i]
assert Q(48,40)==Q(6,5) and Q(48,32)==Q(3,2)
assert ceil(Q(1000,200))==5
assert cost_per(240,0) is None
assert schedule(1,4)[0]==[30]
assert schedule(1,4,fast=True)[0]==[25]

# 13 decode lengths x 3 policies; compare all-eight success thresholds.
for d in range(13):
    for (k,fast),limit in zip(policies,[3,4,9]):
        f,_=schedule(8,d,k,fast)
        assert (good(f)==8)==(d<=limit)

# 201 inclusive deadlines x 2 workloads x 3 policies: 1,206 checks.
checks=0
for deadline in range(201):
    for d in [4,8]:
        for k,fast in policies:
            f,_=schedule(8,d,k,fast)
            s=service(4,d,fast)
            closed=8*int(s<=deadline) if k==2 else 4*(int(s<=deadline)+int(2*s<=deadline))
            assert good(f,deadline)==closed
            checks+=1
assert checks==1206
for h,count in [(0,8),(10,8),(11,4)]:
    assert good([80]*4+[80+h]*4)==count
print('PASS: memory, two full traces, costs, phase bounds, sparse load, zero success, 39 length-policy and 1206 deadline checks, startup boundaries')
```

## Revision history

- 1.0 — 2026-11-13. Five worked analyses and executed deterministic checks; no empirical performance claims.
---

# C04 — Worked analysis and reproducible checks

| Field | Value |
| --- | --- |
| ID / title | C04 answers · Product-boundary analysis |
| Revision / date | 1.0 · 2026-11-14 |
| Prerequisites | [C04 memo](SDE_C04.md), B01–B03, S06 |
| Capability developed | Separate feasibility from preference and test a boundary choice against costs and authority |
| Source-check status | Uses the memo's verified R19/R21/R11 passages; scenarios are original |
| Experiment status | Exact arithmetic and finite decision checks executed; no customer or security experiment |
| Assessment convention | Criteria apply to future answers, not assumed learner mastery |

## 1. Responsibility and revocation

**Hint:** Identify the person who performs work separately from the principal allowed to authorize an effect.

**Worked analysis:** The customer sponsor funds the work; the data owner authorizes processing; the preparation operator assembles evidence; the customer reviewer decides on payment. Hosted self-serve leaves exception operations with the customer. Managed adds supplier operators and scoped human access. Internal moves runtime recovery and maintenance to a customer owner. All three retain customer payment approval.

A supplier analyst's grant allows only the named tenant/case scope and operations. After revocation commits, a new protected read must fail under the memo's contract. Identity still being authenticated does not restore authorization. Access checks need to cover exports, support tools, logs and recovery, not only the ordinary UI. Already disclosed information cannot be recalled by denying the next request; retained copies need separately defined handling.

R11 gives principles; the actual revocation enforcement and trustworthy policy state are implementation premises. A generated statement that an administrator approved something does not create a grant. If current policy cannot be established, deny or defer the protected action rather than treating the uncertainty as permission. This can reduce availability while preserving the chosen authority rule.

**Criteria:** Distinguishes identity, authorization, data disclosure and new effects. Names an operational owner without granting it unnecessary payment authority.

## 2. Customer economics and setup feasibility

**Hint:** Apply the setup cap after calculating value; do not delete setup cost when more hours become available.

**Worked analysis:** Baseline work is 100×8/60=40/3 hours/month, valued at 400 U. Recurring labor under the three options is 200,100,150 U/month. Including monthly fees/infrastructure gives recurring costs of 320,280,190 U/month. Net monthly benefit relative to baseline is therefore 80,120,210 U.

Six-month benefits less setup are 480−120=360 U, 720−60=660 U and 1,260−360=900 U. With a four-hour onboarding cap, self-serve (4) and managed (2) fit; internal (12) does not. Assuming all other gates pass, managed maximizes modeled value among feasible candidates. The 240 U difference between internal and managed is an opportunity that cannot be realized with the initial setup allocation.

These values do not prove actual cash savings. Fixed salaries may remain unchanged; released time needs a useful alternative use. Nor do they establish willingness to pay. Common quality and operational-cutoff assumptions must be tested. If one option attains its lower time only by omitting necessary evidence, its numbers are not comparable.

**Criteria:** Gets all three values, excludes the infeasible option, and distinguishes capacity value from observed cash or demand.

## 3. Supplier viability and overhead sensitivity

**Hint:** There are separate customer and supplier onboarding costs. They represent different parties' work.

**Worked analysis:** Self-serve's monthly contribution after the assigned overhead is 120−40−10=70 U. Across six paid months, subtracting 60 U onboarding and 200 U acquisition leaves 160 U. Managed's corresponding contribution is 180−120−10=50 U; 300−90−200=10 U remains.

For managed monthly overhead a, remainder is 6(60−a)−290=70−6a. Nonnegative remainder requires a≤35/3≈11.67 U/month. At a=12, remainder is −2 U, so managed fails the stated supplier gate. Self-serve's value stays 360 U and its remainder is 160 U if its own overhead stays ten; it becomes the initial feasible choice. This isolated stress changes managed overhead only.

The cost floor for a managed monthly fee at overhead ten is 120+10+290/6=1,070/6≈178.33 U. The assigned 180 U fee is only about 1.67 U above that floor. A price rise could help the supplier but reduce customer value or change adoption; it is a new offer, not an automatic repair. No total-company profitability is established, since the overhead allocation and omitted costs require actual reconciliation.

**Criteria:** Includes acquisition, supplier setup and overhead once; recognizes a narrow buffer and refuses to infer profitability from it.

## 4. Revised constraint and maintenance thresholds

**Hint:** Change available setup hours only for the primary reversal. Treat ongoing extra maintenance as a separate sensitivity.

**Worked analysis:** At twelve available hours, internal clears the setup gate. Its 900 U exceeds managed's 660 and self-serve's 360. The qualified operating owner and recurring allowance are unchanged premises. The additional eight available hours enable the option but do not lower its twelve-hour setup cost.

If additional maintenance is x hours/month, internal value is 900−180x. It ties managed at x=240/180=4/3 hours/month. Below this, internal is preferable if all gates pass; above it, managed has greater value. At x=5, internal value reaches zero, equal to the incumbent. An option can remain better than doing nothing yet lose to another feasible option: x=2 gives internal 540 U, positive but below managed's 660.

Ties should be reported, not concealed with arbitrary precision. A real tie could be resolved by confidence, reversibility or a further test; these preferences are not built into this fixture. With no external processing permission and the initial four-hour cap, both hosted options fail authority and internal fails capacity. The incumbent is the only modeled feasible path. A new timeline, allocation or redacted-data offer requires fresh assumptions.

**Criteria:** Revises the recommendation, preserves counted labor, distinguishes two thresholds and accepts deferral when gates exclude every candidate.

## 5. Evidence plan and operational handoff

**Hint:** State what could reject the recommended option before proposing more features.

**Worked analysis:** Confirm the resource allocation with the sponsor, processing permissions with the data owner and ongoing responsibility with each operator. Use a bounded set of permitted cases spanning routine work, missing records, changed revisions and exceptions. Compare complete evidence support and cutoff compliance on matched cases. Log customer and supplier effort separately; classify setup, recurring operations and exceptional rework without overlap. Count unresolved cases and failures rather than filtering them out of the denominator.

An initial pilot should produce non-effecting drafts and exercise denied reads, revoked grants and unavailable policy. It should not authorize payments. Stop if an unauthorized disclosure/effect occurs or evidence identity cannot be preserved. Reconsider managed if overhead or support costs exceed the narrow supplier buffer. Reconsider internal if actual maintenance erases its advantage or the operating owner cannot sustain it. No sample size here certifies security, general market demand or long-term retention.

For exit, assign an owner to export mappings, evidence identifiers, outstanding cases and runbooks. Verify that the receiving process can interpret the export. Revoke access and handle retained copies according to the agreed lifecycle rules. A deletion request and a completed deletion are different statuses. Migration effort belongs in the next option comparison. A useful pilot can justify another bounded investment without proving the whole service is viable at scale.

**Criteria:** Includes fair quality/cost measurement, authority tests, stop rules, alternative evidence and an actionable exit. Does not invent customer commitments or completed deployment tests.

## Executed conditional checks

This standard-library script was executed during production. It checks the ledgers, exact boundaries and a finite decision grid. It does not implement authorization, measure real labor or validate demand. Permission and quality flags represent hypothetical gate outcomes; they are not security-test results.

```python
from fractions import Fraction as Q

H,n,b,w = 6,100,8,30
spec = {
    'self': (4,120,0,4),
    'managed': (2,180,0,2),
    'internal': (3,0,40,12)
}
def value(name,extra_internal=Q(0)):
    t,fee,infra,setup=spec[name]
    result=H*(Q(n*(b-t)*w,60)-fee-infra)-setup*w
    return result-H*w*extra_internal if name=='internal' else result

def remainder(name,overhead=Q(10)):
    fee,cost,setup=(120,40,60) if name=='self' else (180,120,90)
    return H*(fee-cost-overhead)-setup-200

def choose(cap,external=True,extra_internal=Q(0),managed_overhead=Q(10),quality=True):
    eligible={'incumbent':Q(0)}
    for name in spec:
        if not quality or spec[name][3]>cap: continue
        if name!='internal':
            if not external: continue
            a=managed_overhead if name=='managed' else Q(10)
            if remainder(name,a)<0: continue
        eligible[name]=value(name,extra_internal)
    best=max(eligible.values())
    return {name for name,v in eligible.items() if v==best}

assert [value(k) for k in spec]==[360,660,900]
assert [remainder('self'),remainder('managed')]==[160,10]
assert choose(4)=={'managed'}
assert choose(12)=={'internal'}
assert remainder('managed',12)==-2
assert choose(4,managed_overhead=12)=={'self'}
assert choose(4,external=False)=={'incumbent'}
assert choose(12,external=False)=={'internal'}
assert choose(12,quality=False)=={'incumbent'}
assert remainder('managed',Q(35,3))==0
assert Q(120+10)+Q(290,6)==Q(1070,6)
assert value('internal',Q(4,3))==660
assert value('internal',5)==0
assert value('internal',2)==540
assert choose(12,extra_internal=Q(4,3))=={'internal','managed'}
for delta in [Q(-1,100),Q(0),Q(1,100)]:
    assert (remainder('managed',Q(35,3)+delta)>=0)==(delta<=0)
    assert (value('internal',Q(4,3)+delta)>=660)==(delta<=0)

# 25 setup caps x 49 maintenance values x 2 permission states = 2450 cases.
# Extra maintenance ranges 0..4 hours/month in twelfths; all other gates fixed.
checks=0
for c in range(25):
    cap=Q(c,2)
    for j in range(49):
        x=Q(j,12)
        for external in [False,True]:
            got=choose(cap,external,x)
            if cap<2:
                want={'incumbent'}
            elif cap<12:
                want={'managed'} if external else {'incumbent'}
            elif not external:
                want={'internal'}  # value remains positive throughout this grid
            elif x<Q(4,3):
                want={'internal'}
            elif x==Q(4,3):
                want={'internal','managed'}
            else:
                want={'managed'}
            assert got==want,(cap,x,external,got,want)
            checks+=1
assert checks==2450
print('PASS: ledgers, overhead/maintenance boundaries, choice reversal, authority/quality gates, 2450 decision cases')
```

## Revision history

- 1.0 — 2026-11-14. Five worked analyses and executed exact decision checks.
---

# C05 — Worked analysis

| Field | Value |
| --- | --- |
| ID | C05 answers |
| Title | Autonomy decision: hints, solutions and checks |
| Revision | 1.0 |
| Date | 2026-11-14 |
| Prerequisites | F02/F03, S03/S06, A05; SDE_C05.md |
| Capability developed | Audit a conditional autonomy recommendation |
| Source-check status | Same inspected primary passages and limits as the core memo |
| Experiment status | Python script below executed successfully; synthetic inputs and sequential authority model only |

Read [SDE_C05.md](SDE_C05.md) first. These are worked solutions, not attributed learner answers.

## 1. Cost and feasibility

Hint: price human minutes before adding losses, and use daily minutes for capacity.

W costs 0.20 + 0.50×1 + 20×0.020 + 5×0.080 = **1.50** units per eligible case. S costs 0.35 + 2 + 0.20 + 0.10 = **2.65**. A costs 0.80 + 0.20 + 0.30 + 0.30 + 0.15 = **1.75**. Multiply by 1,000 for daily expected costs of 1,500, 2,650 and 1,750. Human demands are 1,000, 4,000 and 400 minutes.

At 1,200 minutes, W and A meet the planning gates; choose W. At 500, only A does; conditionally choose A. All three assigned timely probabilities meet the 0.90 floor, but quality does not make unavailable staff appear. The probabilities are hypothetical full-system assumptions, not outputs derived from total daily capacity. Actual scheduling must validate them.

Assessment criterion: correct recommendation plus explicit conditionality. “A is best because agents are faster” supplies neither evidence nor a comparable job.

## 2. Sensitivity

Hint: keep every A term except wrong-route loss fixed.

A's fixed terms sum to 1.45, so `1.45 + 20x = 1.50` gives `x=0.0025`. Below 0.25%, A is cheaper if all gates still pass; at equality prefer simpler W. At the original 1.5%, A costs 0.25 more per case. A's allocated maintenance alone is 0.30; dropping it without justification would change the recommendation by changing the accounting premise.

At 500 minutes, cheap W is still infeasible. Conversely A's higher error or oversight demand could make every option inadequate. Expected loss averages consequences; it does not price permission violations into acceptability. Case independence is not required to sum expected costs. It would matter to a claim about confidence bounds or daily aggregate variability.

## 3. Recovery trace

Hint: distinguish a committed result from the caller's knowledge of it.

K commits route Q1 for revision 3 but its reply is lost. The caller cannot infer failure. Identical K retrieves the receipt if current read permission permits. K with Q2 conflicts, while a fresh key targeting the occupied slot is rejected. If revision changes before an uncommitted request, stale evidence cannot create a route. Revocation before commit denies; revocation after commit does not erase the historical event. A denied receipt read creates no new effect and does not justify an alternate mutation.

Assessment criterion: no fresh operation identity used merely to bypass uncertainty, stale evidence, permission or occupancy. The script models an atomic sequential transition, not a database concurrency protocol, authentication stack or network cancellation implementation. Real tests must exercise those boundaries and all alternate write paths.

## 4. Measurement design

Hint: emitted suggestions are a post-treatment subset.

99 correct suggestions among 100 emitted could coexist with 900 unresolved offered cases. That is 99% correctness among outputs but at most 9.9% correct on-time completion over 1,000 eligible cases, before checking human action and deadline. A fair comparison freezes eligibility at arrival, uses the same cases and evidence in offline replay, and includes refusals, retries, human handling and queue delay in full-system results. Report correct-on-time counts, wrong routes, unresolved cases, minutes, costs and authority failures separately.

For a live experiment, shared queues can make one invoice's assignment affect another's delay. Choose a stable assignment unit consistent with that interference, such as the team, and plan uncertainty analysis at that unit. Neither paired replay nor a small zero-incident sample certifies security. R03's cited sections in the core support predeclared hypotheses, metrics and attention to randomization units; these particular invoice procedures are original applications.

## 5. No adequate candidate

Hint: apply gates before minimizing cost.

At 500 minutes, failed authority verification excludes A. W and S exceed capacity, so the answer is no adequate candidate at full volume. If instead A needs 600 review minutes, the same conclusion follows. An authorized intake reduction or staffing increase would be a separately declared new constraint. Sending payment, omitting evidence or counting only accepted work would change the task covertly.

Assessment criterion: preserve the envelope even when that yields an operationally inconvenient answer. No learner score is recorded.

## Reproducible executed checks

Run the following with Python 3. It uses exact rational arithmetic for monetary boundaries. The 1,501 capacity cases test the decision rule, not a staffing simulation. The authority fixture exposes a single atomic transition for teaching; it does not claim to implement distributed transactions.

```python
from fractions import Fraction as F
from itertools import product

rows = {
    'W': (F('.20'), F('1'), F('0'), F('.020'), F('.080')),
    'S': (F('.35'), F('4'), F('0'), F('.010'), F('.020')),
    'A': (F('.80'), F('.4'), F('.30'), F('.015'), F('.030')),
}
def cost(row):
    compute, minutes, maintenance, wrong, late = row
    return compute + F('.5')*minutes + maintenance + 20*wrong + 5*late

def choose(capacity, authority=True, agent_minutes=F('.4')):
    candidates = []
    for name, row in rows.items():
        minutes = agent_minutes if name == 'A' else row[1]
        verified = authority if name == 'A' else True
        if verified and 1000*minutes <= capacity and 1-row[3]-row[4] >= F('.9'):
            candidates.append(name)
    return min(candidates, key=lambda name: (cost(rows[name]), name)) if candidates else None

assert [cost(r) for r in rows.values()] == [F('1.5'), F('2.65'), F('1.75')]
assert [1000*r[1] for r in rows.values()] == [1000, 4000, 400]
assert choose(1200) == 'W' and choose(500) == 'A'
assert choose(500, authority=False) is None
assert choose(500, agent_minutes=F('.6')) is None
threshold = (F('1.5')-F('1.45'))/20
assert threshold == F('.0025')
assert F('1.45')+20*(threshold-F('.0001')) < F('1.5')
assert F('1.45')+20*(threshold+F('.0001')) > F('1.5')
for cap in range(1501):
    expected = None if cap < 400 else ('A' if cap < 1000 else 'W')
    assert choose(cap) == expected
assert F(99,100) == F('.99') and F(99,1000) == F('.099')

class Authority:
    def __init__(self):
        self.revision, self.epoch = 3, 7
        self.grant, self.read = True, True
        self.slot, self.receipts, self.effects = None, {}, 0
    def route(self, key, payload, authenticated=True, tenant=True,
              allowed=True, evidence=True):
        # payload is (revision, epoch, queue); state transition is atomic here.
        if not authenticated or not tenant:
            return 'denied'
        if key in self.receipts:
            if not self.read:
                return 'denied'
            return 'receipt' if self.receipts[key] == payload else 'conflict'
        if not (self.grant and allowed and evidence):
            return 'denied'
        if payload[:2] != (self.revision, self.epoch):
            return 'stale'
        if payload[2] not in ('Q1', 'Q2'):
            return 'denied'
        if self.slot is not None:
            return 'occupied'
        self.slot = payload
        self.receipts[key] = payload
        self.effects += 1
        return 'committed'

p = (3, 7, 'Q1')
a = Authority()
assert a.route('K', p) == 'committed'  # simulate losing this reply
assert a.route('K', p) == 'receipt'
assert a.route('K', (3,7,'Q2')) == 'conflict'
assert a.route('OTHER', p) == 'occupied'
a.grant = False
assert a.route('K', p) == 'receipt'  # existing history, separate read permission
assert a.route('NEW', p) == 'denied'
a.read = False
assert a.route('K', p) == 'denied' and a.effects == 1
b = Authority()
b.revision = 4
assert b.route('K', p) == 'stale' and b.effects == 0
for flags in product((False, True), repeat=4):
    c = Authority()
    result = c.route('K', p, *flags)
    assert (result == 'committed') == all(flags)
    assert c.effects == int(all(flags))
print('PASS: ledgers, thresholds, 1501 capacity cases, recovery trace, 16 guard combinations')
```

The script passed on 2026-11-14. Checks also covered five exercise/answer mappings, required metadata, companion links, balanced fences and absence of draft placeholders. No model inference, production workload, live mutation, concurrency stress test or learner assessment occurred. Unknown real rates and implementation behavior remain explicitly open in the memo.
---

# C06 — Worked analysis

| Field | Value |
| --- | --- |
| ID | C06 answers |
| Title | Supplier-change decision: hints and checks |
| Revision | 1.0 |
| Date | 2026-11-15 |
| Prerequisites | S02/S06, A03–A05, B02/B03; SDE_C06.md |
| Capability developed | Audit migration costs, evaluation claims and evidence continuity |
| Source-check status | Uses the primary passage locators and limitations in the core memo |
| Experiment status | Embedded Python executed; synthetic accounting, paired counts and manifest validation only |

Read [SDE_C06.md](SDE_C06.md) before these optional solutions. No response or score is attributed to the learner.

## 1. Complete ledgers

Hint: convert minutes into cost, then add setup once.

At 1,000 cases and 0.50 U/minute, recurring labor is I=1,000, R=1,100 and B=1,750 U/month. Supplier plus labor plus incremental maintenance is therefore 1,500, 1,500 and 1,800 U/month. Six months plus setup gives **9,000, 9,900 and 11,100 U**. Retain I under the equal-adequacy premise.

After only I's fee becomes 700, its monthly total is 1,800 and horizon total 10,800. R becomes the cheaper adequate choice at 9,900. Savings are 900 U after setup. If R fails the authority or quality gate, the cost comparison cannot authorize migration. If I remains adequate, it stays available at its higher cost; if neither candidate is adequate, state that instead of weakening the task.

Assessment criterion: include human work, maintenance and setup, state the horizon, and separate customer cost from supplier margin. These are new C06 inputs, not replacements for B03's scenario.

## 2. Thresholds and omitted inputs

Hint: solve equal total costs with just one variable free.

For the fee, `6(x+1100)=9900` yields x=550 U/month. R is cheaper strictly above 550 at six months; at equality retain I. At x=700, compare `1800H` with `900+1500H`: equality is H=3. Only horizons longer than three months recover setup with a strict saving. Monthly payment timing and discounting are excluded from this simple model.

For bundle handling, `300+6(500t+50)=9000` gives t=2.8. Below that B is cheaper at the original I fee, provided all gates hold. The threshold is not evidence that such handling time is achievable. A measured extra export fee, migration overlap, training effort or maintenance cost moves the threshold. Add each in the correct period and avoid double-counting effort already included in setup.

Assessment criterion: name the fixed assumptions. Quoting a break-even number without its horizon or workload makes it unusable.

## 3. Paired evidence

Hint: totals include successes shared by both arms.

I has 92+4=96 successes and R has 92+3=95. There are seven discordant cases; R gains three and loses four. The paired sample difference is −1 percentage point for R. One shared failure is still in the denominator of 100. Both meet a 95% observed sample floor, but sampling uncertainty, representativeness and dependence remain unresolved.

This fixture validates arithmetic only. It does not establish that either real supplier meets a 95% population service objective. Inspect the seven disagreements, preserve held-out evaluation, analyze the relevant sampling unit and test complete workflows under load. Identical evidence supplied directly to both generators is useful diagnosis but bypasses deployed retrieval and cannot replace the whole-system comparison.

## 4. Repair evidence continuity

Hint: references identify revisions, not just logical documents.

Suppose current D17/3 is exported but an old decision references D17/2. Exporting another unrelated revision to keep the total row count unchanged does not repair the missing historical reference. Recover the authorized immutable bytes and manifest for D17/2, validate its digest and locator interpretation, and rerun reference validation. If recovery is impossible, mark the historical evidence gap; do not relabel D17/3 as revision 2.

A digest match verifies bytes relative to a trusted expected digest; it does not prove the trusted manifest itself is correct or that access was authorized. The following fixture checks exact keys, byte digests and reference closure. It uses tiny invented bytes, not an actual storage export or encryption/access-control implementation.

## 5. Cutover, rollback and the advantage claim

Hint: the replaceable component and authoritative state have different lifecycles.

Shadow execution writes no business effects. A new complete revision becomes current only at the atomic publication boundary. Before publication, a crash leaves the previous head; after publication, the new head must resolve to complete durable evidence. A rollback changes future execution or a valid head under the declared protocol; it never rewrites prior receipts or their evidence. Permission checks cover export, recovery and support paths as well as ordinary requests.

The claimed advantage is disproved for this scenario if the bundle meets the same evidence, authority and deadline gates while reducing handling below 2.8 minutes at its assigned costs. Do not respond by counting only the incumbent's successful cases or by trapping customer records. Usable exports and preserved evidence make the comparison more honest. An adapter's syntactic compatibility alone does not prove semantic, operational or economic portability.

## Reproducible checks

Run with Python 3. All money uses exact rational arithmetic. The fee sweep checks 1,001 choices; the horizon sweep checks 12 month values. The validator tests a good export, a missing revision, corrupted bytes and a same-count replacement that loses a referenced revision.

```python
from fractions import Fraction as F
from hashlib import sha256

N, wage = 1000, F('.5')
def monthly(fee, minutes, maintenance):
    return fee + N*wage*minutes + maintenance
mI = monthly(400, F(2), 100)
mR = monthly(250, F('2.2'), 150)
mB = monthly(0, F('3.5'), 50)
assert (mI,mR,mB) == (1500,1500,1800)
assert (6*mI,900+6*mR,300+6*mB) == (9000,9900,11100)
assert 6*monthly(700,F(2),100) == 10800
fee_threshold = F(9900,6)-1100
assert fee_threshold == 550
bundle_threshold = (F(9000-300,6)-50)/(N*wage)
assert bundle_threshold == F('2.8')
for fee in range(1001):
    totals = {'I':6*(fee+1100), 'R':9900, 'B':11100}
    winner = min(totals, key=totals.get)  # insertion order retains I at a tie
    assert winner == ('I' if fee <= 550 else 'R')
for months in range(1,13):
    saving = 1800*months-(900+1500*months)
    assert (saving>0) == (months>3)
    assert (saving==0) == (months==3)
assert 300+6*monthly(0,bundle_threshold,50) == 9000
assert 300+6*monthly(0,bundle_threshold-F('.01'),50) < 9000
assert 300+6*monthly(0,bundle_threshold+F('.01'),50) > 9000
both, only_i, only_r, neither = 92,4,3,1
assert both+only_i+only_r+neither == 100
assert (both+only_i,both+only_r) == (96,95)
assert F(only_r-only_i,100) == F('-0.01')

key2, key3 = ('A','D17',2), ('A','D17',3)
expected_bytes = {key2:b'reference X',key3:b'reference Y'}
trusted = {k:sha256(v).hexdigest() for k,v in expected_bytes.items()}
references = {key2,key3}
def valid_export(export):
    return (set(export)==set(trusted)
            and references <= set(export)
            and all(sha256(export[k]).hexdigest()==trusted[k] for k in trusted))
assert valid_export(expected_bytes)
missing = {key3:expected_bytes[key3]}
assert not valid_export(missing)
corrupt = dict(expected_bytes); corrupt[key2]=b'reference Z'
assert not valid_export(corrupt)
swapped = dict(missing); swapped[('A','D99',2)]=b'reference X'
assert len(swapped)==len(expected_bytes) and not valid_export(swapped)
# Recovery model: publication may point only to a complete revision.
for committed in (False,True):
    durable = {key2,key3}
    head = key3 if committed else key2
    assert head in durable and references <= durable
print('PASS: exact ledgers; 1001 fee cases; 12 horizons; paired counts; 4 export fixtures; 2 publication states')
```

Executed successfully on 2026-11-15. Metadata, five exercise/answer mappings, companion links, fences and placeholder checks also passed. These finite fixtures do not exercise a real supplier, concurrency protocol, recovery log, model or live migration. Actual export rights, service quality, costs and operational ownership require evidence before applying the recommendation.

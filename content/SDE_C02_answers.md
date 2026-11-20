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

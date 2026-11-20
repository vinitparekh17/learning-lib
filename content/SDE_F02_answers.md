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

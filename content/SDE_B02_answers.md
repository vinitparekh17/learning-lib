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

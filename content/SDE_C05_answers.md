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

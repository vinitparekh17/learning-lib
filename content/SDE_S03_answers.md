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

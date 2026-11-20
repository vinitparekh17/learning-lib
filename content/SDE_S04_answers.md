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

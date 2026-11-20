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

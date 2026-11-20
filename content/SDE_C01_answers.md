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

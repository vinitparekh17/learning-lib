# C01 — Where must duplicate-effect prevention live?

| Field | Value |
| --- | --- |
| ID / revision / date | C01 · 1.0 · 2026-11-07 |
| Type | Synthesis decision memo |
| Prerequisites | F01 remembered state and invariants; S02 durable evidence; S03 atomic decisions; S04 replicated decisions |
| Capability developed | Place duplicate prevention at the boundary that controls the promised effect, and revise a retry policy when that boundary changes |
| Source-check status | R10 author-copy pp. 2, 6–7 and R07 §8 p. 13 inspected; supporting passages and limits below |
| Experiment status | Executed finite state and crash-cut checks; no real payment, network, database or consensus deployment tested |
| Companion | [Worked analysis and executable checks](SDE_C01_answers.md) |

## Decision and scope

For the fictional invoice workflow, put approval uniqueness, immutable evidence references and the successful request receipt in one durable application transition. If approval also initiates an external payment, commit a payment intent in that transition and require the payment authority to enforce a stable payment identity. A queue or reliable transport may reduce repeated work, but it cannot alone establish that one business operation had one effect.

The baseline decision assumes a hypothetical provider with an explicit atomic identity contract. If that provider cannot prevent repeated effects or authoritatively resolve an uncertain attempt, change the policy: pause an ambiguous payment for reconciliation instead of automatically submitting it again. This sacrifices automatic progress to protect the at-most-once target. It does not turn uncertainty into proof of failure.

This memo extends the earlier D17 case. It is a design exercise, not guidance for a named payment product. Approval and payment are distinct outcomes. We promise at most one accepted proposal per `(document, approval epoch)` and at most one provider payment per authorized payment intent. We do **not** promise at most one payment across every future correction of an invoice: that broader business rule would need a durable obligation identity and additional guards across epochs.

## Fix the assumptions and identity before choosing machinery

An approval request contains tenant, operation key k, document D17, expected epoch 7, revision 2, actor, evidence reference and payment details. Treat the full canonical tuple as its payload; a hash alone is not the equality definition. Tenant namespaces prevent unrelated customers' keys from colliding. Authentication and authorization are required before disclosing receipts or creating effects; S06 will develop that boundary.

The caller preserves k across retries of the same intent. A new key is a new request identity, but does not bypass the occupied approval slot. Reusing k with a different payload is rejected. A different payment amount or destination requires a new authorized business decision, not silent reinterpretation of an old key.

The application authority provides a serialized conditional transition, durable across the modeled process restart and failover. It retains receipts, epoch history and unsent intents. Every mutation path obeys the same guard. A successful decision includes both its immutable evidence reference and receipt. Storage media loss, malicious replicas and broken authorization are outside the finite model; they remain deployment obligations.

The hypothetical provider atomically binds payment identity p to the exact payment payload, records the effect and its outcome, returns the same result on identical retries, and rejects conflicting reuse. This contract covers concurrent attempts and survives its modeled restart. Its identity records remain valid throughout the application's retry horizon. These are strong premises to verify, not features assumed of every provider.

A timeout means the caller lacks a result. It does not identify which side of a durable transition the system reached. Progress additionally needs eventual communication, a functioning authority and provider, and a dispatcher that continues trying. At-most-once effects alone can be achieved by doing nothing; that is not useful completion.

## The failure that chooses the responsibility boundary

All events below are constructed. Suppose a worker records no durable payment identity and calls a provider that treats each request as a new payment.

| Step | Application / client | Provider | What survives? |
| --- | --- | --- | --- |
| 1 | Worker sends payment for D17 | Receives request | No local completed receipt |
| 2 | Waits for reply | Executes payment | One external effect |
| 3 | Reply is lost; worker crashes | Effect remains | Application still lacks outcome |
| 4 | Replacement retries the payment | Executes new request | Two external effects |
| 5 | Replacement saves “paid” | | One local receipt describes two payments |

Moving the local marker before the call merely changes the failure: crash after marking but before sending leaves “paid” with zero payments. Holding a database lock during the call does not make the provider's effect part of the database commit. Rolling back that transaction cannot undo an already executed payment.

R10 explains why application retries can create distinct network messages for the same operation, and why a meaningful storage acknowledgement must come from the layer that can establish storage completion. R07 §8 explicitly adds client request identities and remembered responses to its consensus discussion. These support the placement argument; the payment protocol here is our own synthesis under the declared contract.

## Compare alternatives under the same objective

The objective is to preserve both at-most-once invariants while allowing eventual completion when the stated dependencies recover. Assume multiple application workers and lost replies for every option.

| Option | Useful contribution | Missing guarantee or cost |
| --- | --- | --- |
| Disable repeated UI clicks | Reduces accidental concurrent submissions | Does not cover restart, retries or another client |
| Worker-local set of seen keys | Fast filtering within one process | Another worker or a crash loses the shared history |
| Transport or queue duplicate filtering | Can reduce redundant delivery | A new message can represent the same business operation; completion boundary may end before the provider effect |
| Atomic application receipt plus guarded approval | Prevents duplicate approval, preserves evidence and resolves its lost reply | Does not atomically control an independent provider |
| Durable intent plus provider-enforced payment identity | Allows repeated delivery while preventing repeated provider effects under the contract | Requires provider cooperation, retained identities, monitoring and reconciliation |
| Stop after an uncertain attempt | Avoids blindly creating a second attempt | Can leave an operation incomplete indefinitely; delayed first attempts still need resolution |

Choose the fifth option for the baseline and retain the fourth as its local foundation. Lower-layer filtering remains an optimization worth measuring, not the authoritative source of business truth. Consensus protects an ordered state transition against its modeled failures; it does not make an incorrect transition correct or extend a transaction into an arbitrary external service.

## Proposed protocol and proof obligations

The application transition first checks a previously accepted receipt for `(tenant,k)`. If the canonical payload matches, it returns the historical receipt; if not, it rejects reuse. A historical receipt says what happened then, not that the approval is still current after reopening.

For a new key, the transition checks authority, expected epoch, expected revision and an empty owner. On success it atomically writes the owner, evidence reference, receipt and one pending payment intent. Assign p from the accepted intent's durable unique identity, not from a dispatcher attempt number. It records a status such as `approved/payment_pending`, never `paid` merely because the intent exists. Stale or occupied requests cannot create intents.

A dispatcher reads pending intents and calls the provider with the same p and payload on every attempt. It persists the returned authoritative result before marking the intent complete. Crash before the call leaves pending work; crash after the effect but before recording its result causes a repeat call with p. Under the provider contract, that repeat returns the prior result without another effect. Multiple dispatchers need not create duplicate effects if they use the same p and the provider enforces the contract atomically; leases can still reduce wasted calls.

The pending-intent record is often called an outbox. The name supplies no guarantee: its crucial property here is commitment with the accepted decision, followed by retryable dispatch. Sending first and creating the intent afterward restores the original crash gap.

The local invariant proof reuses F01's state reasoning. Initially each epoch is empty. The only accepting transition consumes that epoch's empty slot and creates exactly one receipt and intent together. A replay creates neither; a competing fresh key sees an occupied slot. A reopen creates a fresh epoch without deleting history. Thus every epoch has at most one acceptance. S02 supplies durable recovery requirements; S03 supplies the atomic guard; S04 supplies the replicated-state boundary when deployed that way.

The external proof is conditional: every dispatch of one intent uses one p, and the provider's only effect-producing transition creates p's first record atomically. Repeated p cannot produce another effect. This proves at most one effect **per p**, not eventual success, and not uniqueness across independently created intents for the same real-world obligation.

Reopening does not cancel a dispatched payment. For this case an accepted intent remains authorized after reopening; a later correction creates a separately authorized adjustment. If the business requires reopening to revoke a pending payment, it needs an explicit dispatch/cancellation protocol with provider support. A new epoch alone cannot retract a message already in flight.

## Change one constraint: the provider has no identity contract

Keep the same application authority and business objective, but replace the provider with one that has neither deduplicated payment identities nor an authoritative operation-status query. Now two histories look identical locally:

- H0: the send never reached the provider; no payment happened.
- H1: the provider paid, but its reply never reached the application.

Both leave the same durable intent and missing outcome. Retrying can complete H0 but duplicate H1. Never retrying protects H1 from a second attempt but may leave H0 unpaid. A local timestamp, a new leader, a longer timeout or more copies of the intent cannot distinguish these histories.

Revise the decision to record `outcome_unknown`, prevent automatic resubmission and reconcile using authoritative external evidence. Human review is a workflow for obtaining evidence, not proof by itself. Even a “not found” query would need semantics excluding a delayed original execution before a fresh attempt is safe. If the provider cannot supply such evidence or cancellation/fencing, retain the unresolved state, or change providers or the business guarantee. Do not label an unresolved payment failed and issue a fresh key.

## Bounded assignment

Write a one-page decision memo before reading the companion. Use exactly the baseline assumptions above, then the changed provider constraint.

1. Draw a lost-reply timeline and state separately what the client knows, what the application committed and what the provider did.
2. State the two at-most-once invariants, payload-binding rule and evidence-retention requirement. Explain the different roles of k, p and epoch.
3. Choose among the options and identify the atomic boundary. Give a concrete counterexample to one inadequate fix.
4. Trace crashes before local commit, after commit/before dispatch, after provider execution/before its reply, and after reply/before local completion. Include two competing keys and a retry after reopening.
5. Revise the decision under the changed constraint. State what evidence would permit resumption and which progress claim must be withdrawn.

For application transfer, ask whether two independently approved documents can represent the same payable obligation. If yes, the invariant needs a domain-specific obligation identity beyond this exercise's scope. Do not assume content equality alone decides that business question.

## Evidence and reference card

| Basis | Verified locator | Role and boundary |
| --- | --- | --- |
| R10, Saltzer, Reed and Clark, 1984 | [Author copy](https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf), p. 2 principle; p. 6 Duplicate message suppression; p. 7 Transaction management | Placement and acknowledgement argument; no historical performance figure adopted |
| R07, Ongaro and Ousterhout, extended 2014 paper | [Primary PDF](https://raft.github.io/raft.pdf), §8 p. 13 | Retried commands, remembered responses and authoritative reads; not an external payment guarantee |
| F01, S02, S03, S04 | Existing packs, especially F01 §7 exercise 6, S03 “Add the delayed request,” S04 retry contract | Prior continuity, not newly measured deployment evidence |
| This memo and companion | Original histories, conditional proof and finite checks | Hypothetical provider contract; no current product guarantee asserted |

Reference card: name the effect → define identity and payload → locate the authority → commit decision, evidence and receipt together → preserve identity across retry → resolve unknown outcomes at the effect boundary. Retention must cover delayed delivery and restoration, not just the ordinary client timeout. Expiring a provider's identity while an old intent can still be sent invalidates the proof.

Open questions are actual provider semantics, retention, safe cancellation, access control, evidence availability, failover durability and obligation identity. They are deployment inputs, not blockers to this synthesis. Next S06 develops authority, isolation and reliability objectives.

## Revision history

- 1.0 — 2026-11-07. Decision memo, changed-provider constraint, five assessment tasks and separate executed finite checks. No learner answers or mastery inferred.

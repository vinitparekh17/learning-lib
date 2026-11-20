# S03 — Concurrency, transactions, and logical time

| Field | Value |
| --- | --- |
| ID / revision / date | S03 · 1.0 · 2026-11-06 |
| Prerequisites | F01 invariants and S02 revision identity, transactions, and recovery. Notation bridge below. |
| Capability developed | Expose a violating interleaving, choose an enforcement boundary, and separate causality from request validity. |
| Source-check status | R05, CMU Fall 2025 lectures 17, 18, 20, and R06, Lamport 1978. Supporting passages inspected 2026-11-06. |
| Experiment status | Executed finite Python history and state-machine checks in the companion. No concurrent database or network deployment tested. |
| Companion | [Hints, worked answers, and reproducible checks](SDE_S03_answers.md) |

## One slot, two reasonable decisions

The document service has published invoice D17/2. Two reviewers submit competing approval proposals. The service permits at most one accepted proposal in an approval round. Acceptance here records a decision and its exact evidence in the database. Any later payment is a separate effect.

S02 preserved complete revisions through a crash under a single-publisher assumption. We now remove the single-writer assumption. A transaction can survive a crash exactly as written and still contain a decision based on obsolete information. F01's sequential check-then-insert proof needs a boundary that prevents another actor from changing the premise between the check and the update.

Use two existing candidate rows, A and B, for one document and round. Each has an `accepted` bit, initially zero. The invariant at committed boundaries is

\[
a+b\leq 1,\qquad a,b\in\{0,1\}.
\]

Each transaction reads both bits and, if their sum is zero, sets its own bit to one. In isolation, either transaction preserves the invariant. The case and all values in this pack are hypothetical.

A **history** lists operations in execution order. `R_A(b)=0` means transaction A read zero from b. `W_A(a)=1` is A's proposed write, and `C_A` means its commit. An abort discards its database changes. A **serial** history finishes one transaction before starting the other. A **serializable** history has an equivalent serial execution, even if its operations overlap. A concurrency protocol controls which histories can commit. [R05, lecture 17 §6](https://15445.courses.cs.cmu.edu/fall2025/notes/17-concurrencycontrol.pdf)

## Derive the bad history

Assume each transaction reads a committed snapshot taken at its first read, sees its own writes, and stages writes privately until commit. Concurrent writers to the same row cannot both commit, but no rule validates the other rows they read. This is the simplified snapshot-isolation model used for the example.

| Step | Transaction A | Transaction B | Committed (a,b) |
| ---: | --- | --- | --- |
| 1 | Read a=0, b=0 | | (0,0) |
| 2 | | Read a=0, b=0 | (0,0) |
| 3 | Stage a=1 | | (0,0) |
| 4 | Commit | | (1,0) |
| 5 | | Stage b=1 using its snapshot | (1,0) |
| 6 | | Commit | (1,1) |

The write sets are disjoint. Atomic commit of each transaction does not reject this history. Neither reviewer observed dirty data. The failure comes from combining two individually valid decisions whose premises cannot both remain true.

Try both serial orders. If A finishes first, B reads (1,0) and declines. If B finishes first, A reads (0,1) and declines. Neither reaches (1,1). This is **write skew**, a possible anomaly under snapshot isolation. MVCC stores versions but needs a concurrency protocol to determine allowed behavior. Its presence alone does not promise serializability. [R05, lecture 20 §1, Snapshot Isolation](https://15445.courses.cs.cmu.edu/fall2025/notes/20-multiversioning.pdf)

The dependency test explains the conflict. A read b before B wrote b, so preserving that observation requires A before B. B read a before A wrote a, requiring B before A. The cycle excludes a conflict-equivalent serial order. In this fixed-object read/write model, conflicts occur across transactions on the same object when at least one operation writes. An acyclic precedence graph characterizes conflict serializability. [R05, lecture 17 §6, p. 4](https://15445.courses.cs.cmu.edu/fall2025/notes/17-concurrencycontrol.pdf)

Checking `accepted IN (0,1)` on each row permits the bad result. Giving each candidate a unique ID also permits it. A constraint must encode the contested resource. A separate Acceptance relation with a unique `(doc, round)` key can directly exclude two acceptance records, provided the system records acceptance only through that relation and handles a rejected insertion as failure.

## Put the check and change behind one boundary

For a small, auditable design, create a guard row for every document. Every operation that changes its approval round, selected revision, or acceptance first obtains the same exclusive transaction lock. Keep that lock through commit or abort. After acquiring it, read the current committed state, validate the request, and write the complete decision with its S02 evidence references in the same transaction. Precomputed extraction can happen outside this boundary.

| Step | A | B |
| ---: | --- | --- |
| 1 | Acquire D17 guard, read free slot | Request guard, wait |
| 2 | Record acceptance and evidence, commit | Still waiting |
| 3 | Release guard | Acquire guard, read occupied slot |
| 4 | | Decline, finish, release guard |

This protocol depends on a current read after the wait. Reusing a snapshot taken before acquiring the guard can restore the stale premise. An implementation must refresh the relevant read or abort and restart when its isolation rules cannot provide that view. The pseudocode specifies a contract, not portable SQL behavior for every engine.

In two-phase locking, lock acquisition precedes a phase that only releases locks. Holding all transaction locks until termination is the rigorous variant. Locking can introduce waiting and deadlock. [R05, lecture 18 §§1–3](https://15445.courses.cs.cmu.edu/fall2025/notes/18-twophaselocking.pdf) Our single-document protocol has just one guard. Extending it to two documents creates a new case. A holds D17 and waits for D18 while B holds D18 and waits for D17. Requiring ascending document-ID acquisition excludes that cycle because a chain of waits would have to keep increasing and return to its start. The argument assumes every participant follows that order and does not acquire hidden conflicting resources in another order.

An optimistic alternative performs an atomic conditional transition on a shared token row. It succeeds only if the slot is still empty and the request's round and revision still match. Approval evidence and the successful result must commit with that transition. A separate client-side comparison followed by an unconditional write does not provide this contract. A full serializable transaction is another option when invariants span several rows or predicates, with the application prepared to retry an aborted transaction from fresh reads.

| Choice | Useful condition | Cost to investigate | Evidence that would change the choice |
| --- | --- | --- | --- |
| Shared guard held through commit | Short decisions for one document | Wait time and long lock holders | Most latency is waiting on unrelated work inside the transaction |
| Conditional token transition | Invariant fits one token and atomic receipt | Repeated failed attempts under contention | Retries dominate useful completions |
| Serializable multirow transaction | Invariant spans changing rows or predicates | Aborts, retries, implementation semantics | Measured contention or an incomplete transaction boundary |

A unique acceptance key remains a useful additional constraint. A local mutex in one worker cannot coordinate other workers unless every write is routed through that one authority. Measure contention before asserting a performance winner. Safety alone says nothing about bounded waiting or fairness.

## Add the delayed request

A slot can be reopened after a correction. Represent the document state as `(epoch, published_rev, owner)`, initially `(7,2,empty)`. Epoch is a never-reused approval-round number. Reopening increments it, clears the current owner, and preserves historical receipts and immutable evidence. Publishing a changed revision also advances the epoch under the same guard. No operation clears the owner within an existing epoch.

An approval request carries a stable operation key, expected epoch, expected revision, actor, and exact evidence payload. The authority validates all of them inside the guarded transaction. Accepted receipts bind the key to that payload. A replay with identical inputs returns the historical result without consuming again. Reusing a key for different inputs is rejected. A historical success receipt does not assert that the approval is still current after reopening.

Now hold an old request in the network.

| Authority order | Received operation | State/result |
| ---: | --- | --- |
| 1 | Reopen D17 after correction | (8,3,empty) |
| 2 | Old approval expecting (7,2) arrives | Reject stale request, leave state unchanged |
| 3 | New approval expecting (8,3) | Accept if still free, bind evidence to D17/3 |

Checking only “slot empty” accepts the old request at step 2. Checking only the revision also fails if the round was reopened while revision 2 stayed published. An epoch distinguishes two free states with different histories. Requests obtain epochs from the authority, and cannot choose an arbitrary higher epoch to overwrite it. Permission to approve is a separate check developed in S06.

The proof is short. Initially each epoch has no acceptance. The sole accepting transition requires an empty owner and writes one owner and its receipt atomically. Subsequent attempts in that epoch fail the empty check or return an existing receipt. Reopening starts a fresh epoch and retains the previous record. Thus each `(doc,epoch)` has at most one accepted proposal. Version validation additionally prevents acceptance against the wrong published revision at the decision boundary. It does not cancel an external action already executed.

## Logical clocks explain order, not validity

Lamport's happened-before relation includes process order, message send before receipt, and their transitive consequences. Two events are concurrent when neither reaches the other by those relations. A logical clock preserves this order, but a smaller timestamp does not prove causation. [R06, pp. 559–560](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)

Use counters starting at zero. Increment for local/send events. On receipt of timestamp t, assign `max(local,t)+1`. In this constructed trace P is the old requester, Q the administrator, and D the authority.

| Event | Action | Logical clock |
| --- | --- | ---: |
| p1 | P sends old approval to D, delayed | 1 |
| p2 | P performs unrelated local work | 2 |
| q1 | Q sends reopen to D | 1 |
| d1 | D receives q1 | 2 |
| d2 | D applies reopen | 3 |
| d3 | D receives p1 | 4 |
| d4 | D rejects the old approval | 5 |

There is a path p1→d3→d4, but none from p2 to d2 or back. Although 2<3, those latter events are concurrent in this modeled communication history. The send timestamp remains 1 even though its receipt gets 4. The receipt's larger number cannot make epoch 7 valid again.

Ordering known events by `(clock, process-ID)` breaks ties and extends happened-before. It does not establish that an unseen earlier message is absent. Lamport's mutual-exclusion construction adds queues, acknowledgements, and delivery assumptions beyond counters. [R06, pp. 560–561](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) We use the centralized guarded decision above, without claiming to implement that distributed protocol.

Wall-clock values serve deadlines and human chronology only under stated clock and delay assumptions. Logical counters measure neither seconds nor freshness. Likewise, a serializable database history promises an equivalent serial order, without by itself proving that this order matches independently observed wall clocks.

## Practice

1. Expand the bad history into separate reads and writes. Show both dependency edges and both serial outcomes. Explain why row-local validity checks permit the violation.
2. Trace the guarded protocol with B winning first. Then release the guard immediately after reading. Construct a violating execution and state the missing guarantee.
3. Reopen epoch 7 as epoch 8 while retaining revision 2. An old request carries (7,2). Compare a revision-only check with the complete conditional transition. State the invariant over historical acceptances.
4. Recompute all seven logical clock values. Identify a timestamp-ordered concurrent pair. Explain why sorting received requests cannot prove no earlier request is still in transit.
5. An accepted transaction commits, its reply is lost, and the client retries. Specify what must be saved with the acceptance. Then add an external payment before commit and identify the failure the database cannot undo.
6. A job now reserves one slot on each of D17 and D18. Construct a deadlock, propose an acquisition order, and state which guarantee still requires deployment evidence. Choose between the guard and conditional transition for a highly contended document and name measurements that would reverse your choice.

## Reference card, evidence, and open questions

Write the invariant before choosing isolation. List reads as well as writes. Find an impossible serial order. Protect the whole decision, including its receipt. Reject stale epochs at the authority. Treat clocks as ordering metadata with a declared model. Separate the database commit from any external effect.

| Basis | Inspected locator | Supported use and limit |
| --- | --- | --- |
| R05, CMU Fall 2025 | [17, §3 p. 2 and §6 pp. 3–4](https://15445.courses.cs.cmu.edu/fall2025/notes/17-concurrencycontrol.pdf) | Transaction boundary, schedules, conflict graph. External actions fall outside database rollback. |
| R05, same edition | [18, §§1–3 pp. 1–3](https://15445.courses.cs.cmu.edu/fall2025/notes/18-twophaselocking.pdf) | Exclusive locks, 2PL, rigorous retention, deadlock. No engine-specific SQL contract asserted. |
| R05, same edition | [20, §1 pp. 1–2](https://15445.courses.cs.cmu.edu/fall2025/notes/20-multiversioning.pdf) | Versions, snapshot isolation, write skew. The two-bit history is original. |
| R06, Lamport 1978 | [Printed pp. 559–561, Partial Ordering, Logical Clocks, Ordering the Events Totally](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) | Formal event model, clock condition, implementation rules, tie breaking, protocol assumptions. |
| Original design and derivation | Histories, guard, epoch/receipt contract, clock trace, companion checks | Constructed inputs and bounded executed models. No empirical throughput or deployed correctness claim. |

Before deployment, verify actual isolation and lock behavior, every path that can mutate the guard state, evidence retention, retry-key retention, and failure handling around commit. Test long waits and retries under the real workload. The finite checks do not simulate hardware, database internals, or a lossy network. These are application unknowns, not blockers for the next pack.

F01 supplies the invariant proof, and S02 supplies durable revision identity. S04 will add replicated authorities and partial failure. S06 will revisit permission changes at the decision boundary. A05 and C01 will carry the separation between accepted intent and external tool effects.

## Revision history

- 1.0 — 2026-11-06. Original S03 pack with a write-skew history, shared-guard repair, stale-epoch counterexample, and logical-time trace.

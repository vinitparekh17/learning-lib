# X01 — Cache correctness, invalidation, and stale fills

| Field | Value |
| --- | --- |
| ID / revision / date | X01 · 1.0 · 2026-11-20 |
| Prerequisites | F01 invariants; S02 revision identity; S03 interleavings. S06 and A03 are useful follow-ups. |
| Capability developed | Find a stale-fill race, choose a cache consistency contract, and identify the assumptions a generation guard cannot enforce. |
| Source-check status | XR01, original USENIX paper §3.2.1; XR02, RFC 9111 §§4.2, 4.4 and 6. Passages inspected 2026-11-20. |
| Experiment status | Finite interleaving and boundary checks executed in the companion. No distributed cache or production workload tested. |
| Companion | [Hints, worked answers, and executable checks](SDE_X01_answers.md) |

## The decision

You have a correct database and an expensive read. A cache seems like a performance decision: retain the answer and reuse it. But it adds a second place where a previous answer can outlive the assumptions that made it valid.

Our question is specific: **after an update has invalidated a cached object, can an earlier reader put the previous revision back?** If yes, reducing database latency may have increased the duration of an incorrect result.

This extension uses a fictional document D17. Revision 7 is replaced by revision 8. All times, rates and histories below are constructed teaching inputs. The cache is an application cache; its rules are ours to specify, not automatic consequences of an HTTP header or a particular product.

If concurrency is unfamiliar, think of each row in a history as one indivisible step. Different requests can take turns between rows. A request that started first need not finish first. A revision identifies data; a generation identifies a period in which a cache fill is permitted. They are different counters with different owners.

## A successful invalidation that still fails

The initial cache is empty. The database holds revision 7. A reader uses the familiar sequence: check cache, read database on a miss, store the result. A writer commits to the database and then deletes the cache entry.

| Step | Reader A | Writer B | Database | Cache |
| --- | --- | --- | --- | --- |
| 1 | Cache miss | | 7 | empty |
| 2 | Read revision 7 into local memory | | 7 | empty |
| 3 | Paused before cache fill | Commit revision 8 | 8 | empty |
| 4 | | Delete cached D17; report success | 8 | empty |
| 5 | Store local revision 7 | | 8 | 7 |
| 6 | New reader C uses cached revision 7 | | 8 | 7 |

No failed delete is needed. No dirty database read is needed. The delete worked on the state that existed at step 4. The late fill is a *new mutation after the delete*.

Moving the delete before the database commit also admits a counterexample: delete, reader misses and reads 7, reader fills 7, writer commits 8. Changing the order of two separately coordinated systems does not by itself close every gap.

The invariant we want for this lesson is deliberately limited:

> Once invalidation advances this key's generation, a fill carrying an older generation must not become a usable cache entry.

This is a cache-publication property. It does not yet say that every response after a database commit returns the latest revision.

## Remember enough to reject a late fill

Give the cache a per-key generation, initially 0. On a miss, A obtains token 0 **before** reading the database. Invalidation atomically increments the generation and clears the value. Filling atomically checks the token and writes only if it still matches.

```text
miss:        return current generation as token
invalidate:  generation = generation + 1; value = empty
fill(t, v):  if t == generation, store v; otherwise reject
```

Each line describes an atomic cache-side operation in our model. Separate network calls to read the generation and later set the value do not implement the final line: invalidation could occur between them. A lock, transaction or equivalent conditional operation must actually enforce the boundary.

Now step 4 advances the generation from 0 to 1. Step 5 presents token 0. The cache rejects it and stays empty. The next reader can fetch revision 8. If A fills before invalidation instead, invalidation clears its entry. Both orderings protect the stated publication invariant.

The original Facebook memcache paper describes a related lease mechanism: a miss can return a key-bound token that is checked on a subsequent fill, and a delete can invalidate that token. The same section discusses regulating lease issuance to reduce competing fills. [XR01, §3.2.1, printed p.388](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf). Our generation model is an original simplified exercise, not a reproduction of that production protocol or its performance results.

The order of token acquisition matters. Reading revision 7, then observing generation 1 after invalidation, and presenting that new token with the old data defeats the guard. A token is evidence about a particular operation's ordering, not a stamp you can attach after the fact.

## What this guard does not prove

Consider three changes to the premises.

**Delayed invalidation.** The database commits revision 8, but the invalidation arrives later. During that interval, an old cache entry can still be served. Even after a fill is rejected, the initiating reader might return its local revision 7 to its caller. Protecting cache publication alone does not repair that response path. A requirement such as “every read beginning after a successful write sees at least that write” needs an acknowledgement/read protocol that enforces that relationship. One option is to return a required revision to the writing client and validate or bypass entries below it; the authority used for that validation must itself meet the contract.

**A lagging database replica.** A reader obtains generation 1 after invalidation but reads revision 7 from a replica that has not applied revision 8. The token matches, so the fill is accepted. The guard has not been violated; its premises were weaker than the application's freshness goal. A version floor carried with invalidation could reject revisions below 8, but only if that floor is trustworthy, available and atomically checked with publication. Waiting, bypassing or failing must be specified when no suitable read is available.

**Evicted guard metadata.** An old reader holds token 0. Invalidation advances to 1. The cache loses its generation record and recreates the key at 0. The old token now matches again: an ABA-style reuse of identity. Keeping a generation only as long as its value is cached is insufficient. Use a design that prevents old tokens from becoming valid after eviction or restart—for example, an incarnation identity that cannot be reused within the outstanding-token lifetime. Prove the lifetime and recovery assumptions rather than assuming a counter is durable.

These are reasons to state the contract precisely. A mechanism can correctly enforce its own invariant while the whole application remains incorrect.

## TTL measures a different thing

Suppose A reads revision 7 at time 0. Revision 8 commits at time 1. A fills the cache at time 100 with a 60-second TTL measured from insertion. The entry expires at time 160. It has a full remaining TTL at insertion although its source observation is already 100 seconds old. In this constructed history, the old revision can be served during [100, 160), including almost 159 seconds after the update. That is a 60-second serving interval, not 159 seconds of continuous cached service.

For an insertion-based application TTL, if an observation happens at time r, fill is delayed by d and the TTL is T, expiry is r + d + T. At time t, observation age is t − r, while cache residence is t − (r + d). The difference is d. A bounded TTL alone therefore does not bound observation age without a bound on fill delay and the age of the source read.

Do not apply that insertion-only formula to HTTP caches. RFC 9111 defines freshness using response age and freshness lifetime; its age accounting includes transit and residence. It also limits the scope of invalidation and distinguishes HTTP caching from an application's later reuse of data. [XR02, §§4.2–4.2.3, 4.4 and 6](https://www.rfc-editor.org/rfc/rfc9111.html). HTTP freshness still should not be mistaken for a proof that the underlying business object has never changed.

## Choose a contract before choosing a cache

| Use | Acceptable contract to investigate | Evidence that could change the choice |
| --- | --- | --- |
| Public descriptive text | Explicitly bounded age may be acceptable | Actual update frequency and cost of stale text |
| A document revision selected by ID | Immutable revision content may be reusable | Whether identity is immutable and all dependencies are included |
| Current “latest revision” pointer | Needs its own freshness/ordering contract | Writer acknowledgement, invalidation delay and replica lag |
| Approval permission | Must match the declared revocation boundary | Whether permission is checked at the protected action |
| Generated answer from documents | Reuse only under the required evidence and access context | Source revisions, principal scope, retrieval/model configuration and current permission |

The last two rows connect to [S06](SDE_S06.md) and [A03](SDE_A03.md). A cache key containing a user or policy version does not discover that permission has changed. The serving path still needs a valid authority decision. Likewise, immutable document content does not make the mutable pointer “latest” immutable.

There is a cost trade-off. In a hypothetical workload of 1,000 reads per second, one source query per miss and a 95% hit rate imply 50 source queries per second. At 80%, that becomes 200: four times the source demand despite a 15-percentage-point change in hit rate. This arithmetic assumes no retries, coalescing or refresh traffic. It is not a latency prediction.

For a burst of 100 simultaneous misses on the same key, ideal coalescing could use one fetch if that result is valid for all callers and the leader finishes in time. A stalled leader needs bounded waiting and recovery. If every timeout triggers an independent fetch, the database can receive the original burst after a delay. A generation guard alone neither coalesces requests nor limits backend load. This is the link to [S05](SDE_S05.md): enforce the source's capacity budget even when the cache is cold or unavailable.

## Practice

Attempt these before opening the [worked companion](SDE_X01_answers.md).

1. Reconstruct the stale-fill history from an empty cache. State why a successful delete is insufficient. Criterion: the database read precedes commit, while fill follows invalidation.
2. Interleave the reader's token/read/fill steps with the writer's commit/invalidate steps while preserving each actor's order. Compare unguarded and guarded publication. Criterion: distinguish the invariant after invalidation from freshness after commit.
3. Make generation checking fail by changing either token acquisition order, source-read consistency or metadata retention. Criterion: give a complete history and identify the violated premise.
4. Recompute the TTL example with fill at time 120 and TTL 30. Criterion: give expiry, observation age at fill and the possible stale-serving interval after the update; label the TTL convention.
5. Compare source demand at 95% and 80% hit rates. Then give a case where coalescing is unsafe. Criterion: preserve denominators and identify differing keys or permission contexts.
6. Choose a cache policy for “latest document” and a separate policy for “may approve.” Criterion: name authority, invalidation/validation boundary, failure behavior and a measurement that could reverse your design.

## Reference card

- A delete removes a value; it does not automatically cancel a reader already in flight.
- Acquire the fill token before the source observation; validate it atomically with publication.
- Generation fencing protects an ordering boundary. Source freshness, response freshness and authority need additional contracts.
- Cache residence, source observation age and business revision age are different quantities.
- Treat a cold cache, lost invalidation and forgotten guard metadata as explicit cases.
- Measure useful outcomes and source load, not hit rate alone.

## Evidence and open questions

| ID / type | Inspected support | Boundary |
| --- | --- | --- |
| XR01 · primary historical paper | Nishtala et al., *Scaling Memcache at Facebook*, NSDI 2013, §3.2.1, printed p.388: [original PDF](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf) | Token-check and delete-invalidation mechanism; no current implementation claim or reused benchmark |
| XR02 · primary standard | RFC 9111, §§4.2–4.2.3, 4.4, 6: [full text](https://www.rfc-editor.org/rfc/rfc9111.html) | HTTP age/freshness and invalidation scope; not a specification for our application cache |
| Original derivation | Histories, generation proof, TTL arithmetic and hit-rate arithmetic in this lesson and companion | Finite atomic model with stated assumptions; not a distributed correctness proof |
| Continuity | F01, S02, S03, S05, S06 and A03 | Existing mechanisms reused; no learner mastery assumed |

Before implementing this in a real system, determine maximum read/fill delay, which replica serves misses, how invalidation survives process failure, how generation state survives eviction and restart, and what the caller receives after a rejected fill. Those inputs remain unknown here.

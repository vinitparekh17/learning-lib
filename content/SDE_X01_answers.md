# X01 — Hints, worked answers, and finite checks

| Field | Value |
| --- | --- |
| ID / revision / date | X01 companion · 1.0 · 2026-11-20 |
| Lesson | [Cache correctness, invalidation, and stale fills](SDE_X01.md) |
| Experiment status | Python checks below executed. They enumerate ten legal single-reader/single-writer schedules and explicit failure fixtures. No live cache or concurrent deployment tested. |

## Hints

For 1–2, distinguish where the reader holds its result from where the cache holds a value. For 3, change only one premise at a time. For 4, put observation, update, insertion and expiry on one clock. For 5, write source demand as offered reads multiplied by miss fraction. For 6, define what event makes a previous answer invalid.

## 1. Delete succeeds and an old value returns

Start with database revision 7 and no cached value. A misses and reads 7. B commits 8 and deletes the cache. A then inserts its local 7. C starts after B has finished and reads 7 from cache. The defect is not a failed delete: the earlier request performs a later write. A second timed delete only moves the deadline unless it is tied to a proven maximum lifetime of all earlier fills and successfully delivered.

## 2. Ten schedules and one final stale fill

Label token acquisition T, database read R, fill F, commit C and invalidation I. Require T < R < F and C < I. There are ten ways to interleave chains of lengths three and two: choose three of five positions for the reader.

In the unguarded model, T R C I F leaves revision 7 cached after invalidation. With an atomic generation check, F is rejected. If F happens before I, I clears the entry. If T happens after I, then R also happens after I and C; our latest-committed source-read assumption returns 8. These cases explain the result independently of enumeration.

This does not guarantee immediate freshness after C: the history T R C F I temporarily exposes 7 before I. Nor does rejecting F stop the application returning its local 7 directly. The checked property is specifically cache state after I, not all response behavior.

## 3. Three premise changes

Late token: R observes 7, C commits 8, I advances generation, T obtains the new generation, F publishes 7. Fix the ordering or use an independently validated source revision.

Lagging source: C, I, T, then R reads 7 from a delayed replica. F has a valid token but old data. Require a suitable source read or validated revision floor, and define behavior while the replica catches up.

Forgotten generation: T obtains 0, R observes 7, C commits 8, I advances to 1. Metadata disappears and resets to 0. F passes. The missing premise is identity retention/non-reuse across the lifetime of outstanding work. An incarnation token is useful only if restart, eviction and failover actually preserve its uniqueness contract.

## 4. TTL arithmetic

With observation at 0, update at 1, fill at 120 and insertion TTL 30, expiry is 150. Observation age at insertion is 120 seconds. The cache could serve the obsolete revision during [120, 150), a 30-second interval whose end is nearly 149 seconds after the update. This assumes no later valid replacement or invalidation. An HTTP cache's age rules are different; the original lesson explicitly limits this example to an insertion-based application TTL.

## 5. Load and equivalence

At 1,000 reads/s, 5% misses imply 50 source queries/s; 20% misses imply 200 source queries/s. The multiplier is four. Offered traffic, retry traffic and refresh work must be measured separately before using this as a capacity estimate.

Coalescing two requests just because their query strings match is unsafe if their tenants, permissions or required revisions differ. Even when one immutable blob can be shared, authorization to disclose it must be evaluated under the required contract. Under ideal coalescing of 100 equivalent requests, one source fetch suffices; a failed leader or retry storm changes that count.

## 6. A defensible policy

For a “latest document” display, an explicitly declared bounded-age policy may be adequate if the user can tolerate it. Record source revision and observation time, reject fills with invalid generations, and measure invalidation delay and outdated responses. If the user requires read-your-write behavior, carry the committed revision and validate/bypass entries below it against an adequate source.

For “may approve,” follow S06's action-time authority boundary: an approval ordered after revocation must not commit under the revoked grant. A presentation cache is not that authority. On unavailable authority, defer the protected action under this policy. A policy allowing bounded revocation delay would be a different, explicitly weaker contract.

Useful evidence includes source-read lag, guard-state recovery behavior, rejection rate, source saturation during cache outages and end-to-end latency with permission checks enabled. Correctness requirements and measured costs together can reverse the cache choice. No actual permission system is tested here.

## Executable finite checks

Run with Python 3. Each model step is atomic. Schedules omit network loss, multiple writers, replication, crash recovery and real concurrency. The negative fixtures deliberately violate one premise and must expose the defect. The unit tests establish behavior of this model, not a deployed protocol.

```python
from itertools import permutations
from fractions import Fraction

def simulate(order, guarded):
    db, generation, cache = 7, 0, None
    token = observed = None
    invalidated = False
    violations = []
    for step in order:
        if step == "T":
            token = generation
        elif step == "R":
            observed = db
        elif step == "C":
            db = 8
        elif step == "I":
            generation += 1
            cache = None
            invalidated = True
        elif step == "F":
            if not guarded or token == generation:
                cache = observed
        if invalidated and cache is not None and cache < db:
            violations.append(step)
    return cache, violations

orders = [p for p in permutations("TRFCI")
          if p.index("T") < p.index("R") < p.index("F")
          and p.index("C") < p.index("I")]
assert len(orders) == 10
bad = ["".join(p) for p in orders if simulate(p, False)[1]]
assert bad == ["TRCIF"], bad
assert all(not simulate(p, True)[1] for p in orders)
assert simulate("TRCIF", True)[0] is None
assert simulate("CITRF", True)[0] == 8

# Broken ordering: source observation before token acquisition.
assert simulate("RCITF", True)[0] == 7
assert simulate("RCITF", True)[1] == ["F"]

def guarded_fill(generation, token, observed):
    return observed if token == generation else None

# Fresh token, stale replica: token validity does not prove data freshness.
assert guarded_fill(1, 1, 7) == 7
# A reset generation makes an old token valid again.
assert guarded_fill(0, 0, 7) == 7
assert guarded_fill(1, 0, 7) is None

def fresh(now, inserted, ttl):
    return now < inserted + ttl

assert 100 + 60 - 1 == 159
assert 120 + 30 - 1 == 149
assert fresh(149, 120, 30)
assert not fresh(150, 120, 30)
assert not fresh(151, 120, 30)
assert not fresh(120, 120, 0)
assert 1000 * (1 - Fraction(95, 100)) == 50
assert 1000 * (1 - Fraction(80, 100)) == 200
assert Fraction(200, 50) == 4
print("PASS: 10 schedules; expected stale-fill counterexample; guarded invariant;")
print("late-token, replica and reset fixtures; TTL boundaries; exact load arithmetic")
```

## Assessment criteria

A useful answer reproduces the failure without appealing to a vague “race condition,” locates the atomic boundary, and names at least one assumption that the fix cannot enforce. A stronger transfer applies the same reasoning to a generated-answer cache or a mutable revision pointer. These criteria do not record your level automatically.

# X05 — Worked migration decisions and checks

[Return to the lesson](SDE_X05.md). Attempt the practice before comparing your work. These answers operate on invented inputs and do not select production thresholds.

## 1. Reject the stale copy

The snapshot carries `(120000, revision 41)`. The live request then stores `(125000, revision 42)` in both representations. An unconditional backfill upsert finally replaces the new row with `(120000, 41)`: the migration has made the derived representation older than its authority.

A guarded apply compares revisions at the same atomic write boundary. Since 41 is not greater than 42, it leaves `(125000, 42)` unchanged. If the stored and incoming revisions are both 42 but the normalized values differ, neither is safely “newer.” Record the identity, both values and provenance in a repair queue; stop or quarantine the affected slice according to the predeclared gate. Silently accepting either side would hide a violated ordering or transformation premise.

The guard requires revisions that are monotonic for the logical identity and retained through retries and restores. If those premises fail, the result does not transfer.

## 2. Budget backfill against headroom

The workers' isolated rate is not the safe rate. Production limits effective throughput to 300 rows/s:

`2,400,000 / 300 = 8,000 seconds`, or 2 hours 13 minutes 20 seconds.

A 20% complete rescan adds 480,000 row checks. At the same limit that is 1,600 seconds, for a modeled total of 9,600 seconds or 2 hours 40 minutes.

This is not a forecast because the rate is assumed constant and every row is treated as equal. Real duration includes throttling, hot keys, retries, checkpoint replay, replica lag, transformation cost, repair work and changes arriving during the run. Report processed and verified watermarks separately.

## 3. Contract only after dependency evidence

- With 30% old binaries, contract is unsafe: those binaries still require the old column. Remain in expand/capture/backfill/compare phases.
- With 100% new binaries but an old fallback, dropping the column is still unsafe. The fallback is a live dependency and may be the only cheap rollback after read cutover.
- With 100% new binaries and fallback removed, contract becomes a candidate, not an automatic action. First prove there are no old jobs, replays, admin tools, restore images or delayed messages; wait through the declared rollback and retention window; test restore using the new shape.

Deployment inventory is stronger than an intended release percentage. Query telemetry and attempted access to the old field can expose hidden dependencies.

## 4. Separate enforcement from historical validation

A defensible PostgreSQL plan is:

1. Measure current negative/null count, table size, write rate, lock waits, replica lag and free disk. Set abort thresholds.
2. Add a supported `CHECK (annual_premium_cents >= 0) NOT VALID` in a short transaction. This rejects new violations while leaving old rows unvalidated.
3. Repair or quarantine historical violations in small, idempotent batches. Record identity, old value, chosen correction and revision; throttle on database and replica signals.
4. Recount violations from an independent query. Confirm no writer is failing unexpectedly on the new rule.
5. Run `VALIDATE CONSTRAINT` in a controlled window while observing its actual lock and resource behavior. Abort or cancel if thresholds are crossed.
6. Treat successful validation plus sustained application outcomes as the gate. Do not remove monitoring immediately.

The exact syntax and lock behavior must be checked against the deployed PostgreSQL version. A different constraint type or database may need a different sequence.

## 5. Gate the object-storage authority transfer

A useful plan names:

- **Identity:** immutable document ID plus tenant, not a mutable filename.
- **Ordering:** database revision or commit position attached to the object manifest; a stale copier cannot replace a newer manifest.
- **Comparison:** byte length and cryptographic digest over canonical bytes, encryption/key metadata, content type and a sampled decode—not merely `HEAD 200`.
- **Coverage:** complete database ID set compared with manifests, plus orphan objects in the new store.
- **Capacity:** object-store request/error limits, network egress, database read headroom, queue age and retry amplification.
- **Read gate:** shadow-read and verify objects without returning them, then canary by tenant or deterministic identity.
- **Rollback:** continue old writes or a proven reverse path through the rollback window; know how an object written after cutover reaches the old reader.
- **Deletion:** no old readers or jobs, restore succeeds from the new representation, retention/legal hold is satisfied, and a delayed deletion manifest is reviewed.

Content equality and decryptability are separate claims. A present object with the wrong bytes, tenant key or metadata is not a successful migration.

## Reproduce the models

The code below uses deterministic invented records. `guarded_apply` models one atomic compare-and-write boundary; it does not model a distributed transaction.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Record:
    value: int
    revision: int

def unconditional_apply(_current, incoming):
    return incoming

def guarded_apply(current, incoming):
    if current is None or incoming.revision > current.revision:
        return incoming, "applied"
    if incoming.revision < current.revision:
        return current, "stale-rejected"
    if incoming.value == current.value:
        return current, "duplicate"
    return current, "conflict"

snapshot = Record(120_000, 41)
live = Record(125_000, 42)

assert unconditional_apply(live, snapshot) == Record(120_000, 41)
assert guarded_apply(live, snapshot) == (live, "stale-rejected")
assert guarded_apply(live, live) == (live, "duplicate")
assert guarded_apply(live, Record(126_000, 42)) == (live, "conflict")
assert guarded_apply(snapshot, live) == (live, "applied")

rows = 2_400_000
safe_rate = min(800, 300)
initial_seconds = rows / safe_rate
rescan_seconds = 0.20 * rows / safe_rate
assert initial_seconds == 8_000
assert rescan_seconds == 1_600
assert initial_seconds + rescan_seconds == 9_600

def may_contract(old_binary_share, fallback_enabled, hidden_dependencies):
    return old_binary_share == 0 and not fallback_enabled and not hidden_dependencies

assert not may_contract(0.30, True, True)
assert not may_contract(0.00, True, False)
assert may_contract(0.00, False, False)

print("PASS: stale backfill rejected; conflicts surfaced; capacity and contract gates checked")
```

A complete answer distinguishes movement from proof, states the current authority in every phase, locates the atomic ordering guard and names evidence that could block cutover or contract. These checks reproduce the teaching model; they do not record learner mastery.

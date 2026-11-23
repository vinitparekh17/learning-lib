# X07 — Worked recovery-chain decisions

[Return to the lesson](SDE_X07.md). Every timestamp, duration, artifact and operation ID below is invented. The answers demonstrate a method; they do not certify a production recovery design.

## 1. Measure the recoverable loss window

The failure boundary is 02:18:30 and the newest complete recovery point is 02:17:40:

`02:18:30 − 02:17:40 = 50 seconds`.

The invented path meets a 60-second RPO with ten seconds of margin. The statement is conditional on the base backup plus every required archived-log segment being readable and internally consistent through 02:17:40.

The arithmetic does not prove that every business commit reached the archive, that clocks agree, that the selected point precedes corruption, that the key can decrypt the artifact, or that application/external state can be reconciled. RPO is a loss budget, not a restore test.

## 2. Find the critical dependency path

Start dependency-free stages at minute zero:

| Stage | Earliest start | Earliest finish |
| --- | ---: | ---: |
| Identity and KMS | 0 | 6 |
| Network and DNS | 0 | 8 |
| Database restore | max(6, 8) = 8 | 50 |
| Object-store validation | 6 | 24 |
| Application deployment | max(50, 8) = 50 | 62 |
| Smoke tests and reconciliation | max(62, 24) = 62 | 77 |
| Traffic shift | 77 | 82 |

The critical path is network → database → application → smoke/reconciliation → traffic, totaling 82 minutes. It meets the invented 90-minute RTO with eight minutes of margin. The sum of all durations is 106 minutes, but identity/network and object/database work overlap. The database’s 42 minutes alone is also insufficient because customers cannot use a verified service at minute 50.

The conclusion transfers only if the drill starts from the same failure boundary, uses production-scale data and quotas, and includes approval and validation waits.

## 3. Reject a broken incremental chain

`I3` depends on `I2`; `I2` depends on `I1`; `I1` depends on `F0`. With `I1` missing, no path reconstructs the blocks omitted from `I2` and `I3`. The newest artifact is therefore not restorable.

A pre-incident closure check should traverse parent pointers from every retained recovery candidate until it reaches a retained full backup. It should also verify object existence, checksum, decryptability, compatible restore tooling and required log/timeline ranges. Retention must refuse to delete an ancestor while a retained descendant depends on it, or first synthesize and test a new independent full artifact.

Metadata closure is necessary but not sufficient. Periodically restore a candidate chosen by policy into a clean location and validate data and application behavior.

## 4. Reconcile effects by operation identity

`P102` is present at the payment provider but absent from the restored database. It is an **externally committed orphan** relative to the restored state. Query the provider by the immutable operation/idempotency key, verify amount/account/status, then import a settled record or compensate under a declared business policy. Do not call `charge` again.

`P103` is present in the durable request journal but absent at the provider. It is an **uncommitted or unresolved intent**. Recheck the provider with the same key to exclude delayed visibility. If still absent, resume the state machine using that same key or cancel according to policy. Do not mint a new identity.

`P100` and `P101` exist on both sides, but identity alone is not enough: compare amount, currency, account and terminal status. Any mismatch requires quarantine and investigation.

## 5. Build a regional drill claim

Define the failure as loss of the primary region’s compute, control-plane access and locally scoped credentials while the secondary region and independently administered recovery credentials remain available. This is stronger than stopping one application process and narrower than loss of the entire cloud provider.

Set the RTO endpoint to: authenticated API reads succeed, one controlled write is durable, object references resolve, the outbound queue is reconciled, business invariants pass, and production traffic has shifted. Set RPO separately for the authoritative database, object store and accepted-but-unpublished queue intents.

The dependency graph should include recovery identity/KMS, network/DNS, infrastructure manifests, database base/log chain, object versions, application images, queue journals, observability and traffic authority. Restore into a clean secondary environment; keep the original fenced. Validate:

- artifact gate: manifests, signatures, checksums, keys and ancestor/log closure;
- data gate: engine start, schema, counts and domain invariants;
- application gate: real authenticated read/write paths and version compatibility;
- business gate: queue, objects and external providers reconciled by stable identity.

To transfer the result to production, preserve exact artifact sizes and ages, service quotas, dependency versions, manual approval times, start/end timestamps, corruption injections and validation output. Record every pre-existing resource or warm cache that made the drill easier. A pass under smaller data or privileged test shortcuts establishes only that narrower path.

## Reproduce the recovery checks

This deterministic script checks the invented loss window, dependency graph, incremental closure and reconciliation classification.

```python
from datetime import datetime

failure = datetime.fromisoformat("2026-11-23T02:18:30")
recovery_point = datetime.fromisoformat("2026-11-23T02:17:40")
loss_seconds = int((failure - recovery_point).total_seconds())
assert loss_seconds == 50
assert loss_seconds <= 60

stages = {
    "identity": ([], 6),
    "network": ([], 8),
    "database": (["identity", "network"], 42),
    "objects": (["identity"], 18),
    "application": (["database", "network"], 12),
    "validation": (["application", "objects"], 15),
    "traffic": (["validation"], 5),
}

finish = {}
start = {}
for name, (dependencies, duration) in stages.items():
    start[name] = max((finish[item] for item in dependencies), default=0)
    finish[name] = start[name] + duration

assert start == {
    "identity": 0,
    "network": 0,
    "database": 8,
    "objects": 6,
    "application": 50,
    "validation": 62,
    "traffic": 77,
}
assert finish["traffic"] == 82
assert sum(duration for dependencies, duration in stages.values()) == 106
assert finish["traffic"] <= 90

parents = {"F0": None, "I1": "F0", "I2": "I1", "I3": "I2"}
retained = {"F0", "I2", "I3"}  # I1 expired

def chain_is_closed(candidate):
    seen = set()
    current = candidate
    while current is not None:
        if current in seen or current not in retained:
            return False
        seen.add(current)
        current = parents[current]
    return True

assert chain_is_closed("F0")
assert not chain_is_closed("I3")

restored = {"P100", "P101"}
provider = {"P100", "P101", "P102"}
journal = {"P100", "P101", "P102", "P103"}
external_orphans = provider - restored
unresolved_intents = journal - provider
assert external_orphans == {"P102"}
assert unresolved_intents == {"P103"}

print("PASS: recovery point, critical path, chain closure and reconciliation checked")
```

A complete answer says exactly which failure was tested, keeps the original authority fenced, stops the RTO clock at a user-relevant validation gate, and distinguishes reconstructing internal state from reconciling irreversible effects. These checks do not record learner mastery.

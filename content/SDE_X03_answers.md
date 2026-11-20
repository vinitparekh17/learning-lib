# X03 — Worked membership decisions and checks

[Return to the lesson](SDE_X03.md). Keep two questions separate: how often a complete filter admits unnecessary work, and whether the deployed filter is complete for the data being served.

## 1. Reproduce the false-positive estimate

The invented snapshot has `n = 1,000,000`, `m = 10,000,000` and `k = 7`, so `m/n = 10` bits per key.

\[
p \approx (1-e^{-7/10})^7 = 0.0081937.
\]

That is about 0.819%. Among 3,000,000 queries for absent keys, the expected count admitted to the authoritative lookup is `3,000,000 × p ≈ 24,581`. The remaining roughly 2,975,419 are useful negatives. Expected counts are workload averages, not a guarantee for a particular day.

## 2. Price two memory choices

Twelve bits per key needs 12,000,000 bits, or about 1.50 MB, versus 1.25 MB at ten bits. The incremental memory is 0.25 MB using decimal units. With `k = 8`, the modeled false-positive probability is about 0.003142, so approximately 9,427 of the 3,000,000 negative queries reach the slow path.

The additional memory avoids about `24,581 − 9,427 = 15,154` slow lookups per day. At the invented 2 ms each, this is only about 30.3 service-seconds beyond the 10-bit filter's saving. Decide using measured end-to-end tail latency, I/O and cache churn, memory pressure, filter probe CPU and rebuild cost. A lower isolated false-positive rate is not itself the product outcome.

## 3. Reject a mismatched snapshot

The version-42 filter never received the key added to data version 43. Its negative is a system-created false negative even though the mathematical insert-only filter kept its promise for version 42. The serving invariant should be `filter.manifest_version == data.manifest_version` before a negative can skip the lookup. On mismatch, perform the authoritative lookup or fail the snapshot switch before it becomes visible. Publish the filter and data through one immutable manifest reference so readers cannot independently select versions.

## 4. Replay the retrieval path

Use one captured trace with stable tenant, index snapshot, canonical key encoding and cache starting state. Run it against the unfiltered path and the candidate filter. Record total queries, true absent queries, filter negatives, filter positives, verified true positives, verified false positives, authoritative lookups, bytes read, CPU, cache misses and latency distributions.

To detect hidden valid documents, independently enumerate the authoritative snapshot and assert that every present key returns “maybe.” Include keys added at each publication boundary and force version mismatch, partial-build and fallback fixtures. Compare retrieval recall and final evidence-bearing answers on a labeled set as a downstream check. The membership check establishes whether a document identifier is in one snapshot; it does not establish semantic relevance.

## 5. Keep authorization exact

Do not deny authorization from a Bloom-filter negative unless the filter's completeness and freshness are themselves part of the authorization system's proven invariant. A stale or partially published filter could deny an allowed subject. The safer optimization is to use a positive only to trigger the authoritative policy lookup and to fall back on any version uncertainty. Authorization also has revocation semantics that a basic insert-only filter cannot represent safely.

## Reproduce the arithmetic and premises

The checks use deterministic invented inputs and the standard independent-uniform approximation.

```python
from math import exp, log

def modeled_fpr(bits_per_key, probes):
    return (1 - exp(-probes / bits_per_key)) ** probes

p10 = modeled_fpr(10, 7)
p12 = modeled_fpr(12, 8)

assert abs(p10 - 0.0081937221) < 1e-10
assert abs(p12 - 0.0031423503) < 1e-10
assert round(3_000_000 * p10) == 24_581
assert round(3_000_000 * p12) == 9_427
assert round(3_000_000 * (p10 - p12)) == 15_154
assert 10_000_000 / 8 / 1_000_000 == 1.25
assert 12_000_000 / 8 / 1_000_000 == 1.5
assert round((24_581 - 9_427) * 0.002, 3) == 30.308
assert round(10 * log(2)) == 7
assert round(12 * log(2)) == 8

def may_skip(filter_version, data_version, bits):
    return filter_version == data_version and 0 in bits

assert may_skip(42, 42, [1, 0, 1])
assert not may_skip(42, 43, [1, 0, 1])
assert not may_skip(43, 43, [1, 1, 1])
```

A complete answer names the authoritative follow-up, quantifies avoided work, and treats freshness, completeness and key encoding as premises of every “definitely absent” result.

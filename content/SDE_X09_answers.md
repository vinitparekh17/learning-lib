# X09 — Worked safe-configuration decisions

[Return to the lesson](SDE_X09.md). Every fleet size, timing, threshold, version and policy example below is invented. These checks teach rollout reasoning; they do not validate a production control plane.

## 1. Bound exposure before the next ring

The global rollout exposes `12,000 × (2 + 1) = 36,000` target-minutes before detection and rollback complete. The 12-node first ring exposes `12 × 3 = 36` target-minutes. Under this deliberately simple model, staging reduces the initial upper bound by `36,000 / 36 = 1,000×`.

Target-minutes do not measure request volume, tenant importance, correlated dependencies or irreversible effects. Twelve nodes serving a critical customer could carry more risk than a thousand idle nodes. Use weighted request- or loss-exposure where consequences differ, and align the ring to a fault container rather than scattering twelve nodes globally.

The stage can expand only after the observation window exceeds effect and alert latency. A quick green sample is not permission to erase the bound.

## 2. Evaluate every guardrail

The absolute predicate is `98% ≤ 75%`, which is false. The relative increase is `98 − 45 = 53` percentage points; `53 ≤ 15` is also false. Because the gate is conjunctive, either breach blocks promotion; here both do.

If candidate CPU is missing or stale, hold the rollout. Treating missing data as zero or as a pass converts an observability failure into permission to expand. Page the metric owner or execute the predeclared rollback if the evidence deadline expires.

Compare equivalent scopes and workloads. A busy candidate cell against an idle fleet average is not a valid baseline even when the arithmetic is correct.

## 3. Preserve version authority

Starting from `(7,42,A)`:

- `(7,41,Z)` is stale and must be rejected; delivery order cannot move active state backward.
- `(7,42,A)` is an idempotent duplicate and can be acknowledged without reactivation.
- `(7,42,B)` is an equal-version digest conflict. Quarantine it and alert; two different artifacts claim one identity.
- `(8,1,C)` is not comparable by version alone. Accept it only with proof that epoch 8 is an authorized handoff from epoch 7 or another trusted authority-transition record.

Persist the active epoch, version and digest. After restart, a node must not forget that it has seen version 42 and accept a stale snapshot. Signatures can prove artifact origin, but they do not by themselves prove that an epoch transition is authorized or that the content is safe.

## 4. Choose stale behavior per configuration class

For a recommendation-layout setting, retain LKG through control-plane loss and fail open with the last tested layout. A generous expiry is reasonable if product owners accept staleness; record age and alert without taking serving down.

For an emergency account-revocation list, continued access after a known revocation can be the dominant harm. Use a locally cached, monotonically updated deny state; after its declared freshness bound, fail closed for the protected action or require a stronger secondary check. The exact bound is a security/product decision, not a generic control-plane default.

For the routing policy, continue with LKG while age is at most 15 minutes. Before minute 15, warn and stop risky promotions. At expiry, enter a predesigned safe mode: for example, route only to a conservative local pool or shed optional traffic. “Fail closed” is incomplete unless it says which requests are rejected and how recovery traffic still reaches the service.

Every policy needs clock-skew tolerance, restart persistence and an answer for “no valid LKG exists.” Test expiry with the control plane deliberately unavailable.

## 5. Make emergency control survivable

The proposed disable button is not independent: the WAF can impair the edge proxy, which can impair DNS/SSO access to the control panel, which can prevent disabling the WAF.

A safer design separates:

- **stop:** the deployment coordinator can freeze promotion using a small control path outside the WAF-managed edge;
- **rollback:** targets retain the signed predecessor and can atomically reactivate it without a build;
- **local disable:** a resource-bounded data-plane switch can bypass only the failing rule/component;
- **break glass:** a strongly authenticated, audited path uses independent DNS/network and pre-provisioned credentials held by multiple responders.

Evidence includes a dependency graph, restore/disable time objective, quarterly drills from an external network, credential-use logs, tests with normal SSO and the primary control plane unavailable, and proof that the disable action does not share the candidate parser or rule engine. Also verify return-to-service: re-enable on one isolated cell with positive and negative tests before expanding.

## Reproduce the rollout checks

The deterministic script implements the invented exposure, guardrail and version-order decisions.

```python
fleet = 12_000
canary = 12
detection_minutes = 2
rollback_minutes = 1

global_exposure = fleet * (detection_minutes + rollback_minutes)
canary_exposure = canary * (detection_minutes + rollback_minutes)
assert global_exposure == 36_000
assert canary_exposure == 36
assert global_exposure / canary_exposure == 1_000

baseline_cpu = 0.45
candidate_cpu = 0.98
absolute_limit = 0.75
delta_limit = 0.15
absolute_ok = candidate_cpu <= absolute_limit
delta_ok = candidate_cpu - baseline_cpu <= delta_limit
assert not absolute_ok
assert not delta_ok
assert not (absolute_ok and delta_ok)

active = (7, 42, "A")

def classify(candidate, authorized_epochs=frozenset()):
    epoch, version, digest = candidate
    active_epoch, active_version, active_digest = active
    if epoch < active_epoch or (epoch == active_epoch and version < active_version):
        return "reject-stale"
    if epoch == active_epoch and version == active_version:
        return "duplicate" if digest == active_digest else "conflict"
    if epoch > active_epoch:
        return "accept-new-epoch" if epoch in authorized_epochs else "require-handoff"
    return "accept-newer-version"

assert classify((7, 41, "Z")) == "reject-stale"
assert classify((7, 42, "A")) == "duplicate"
assert classify((7, 42, "B")) == "conflict"
assert classify((8, 1, "C")) == "require-handoff"
assert classify((8, 1, "C"), {8}) == "accept-new-epoch"

print("PASS: exposure, guardrails and version ordering checked")
```

A complete answer bounds scope and time, treats missing guardrail evidence as a hold, separates version from authority, chooses stale behavior per configuration class and proves emergency-path independence. These checks do not record learner mastery.

# X09 — Safe configuration rollout and control-plane blast radius

| Field | Value |
| --- | --- |
| ID / revision / date | X09 · 1.0 · 25 November 2026 |
| Prerequisites | S06 overload control, X05 migration authority, X06 release evidence and X07 recovery proof |
| Capability developed | Treat configuration as executable behavior: validate its meaning, bound its rollout, preserve last-known-good state and keep rollback usable when the control plane or new configuration fails. |
| Evidence | XR22–XR24. Production postmortem and current engineering guidance below. |
| Experiment | Blast-radius arithmetic, promotion gates, version ordering, stale-state policy and rollback-dependency review in the [worked companion](SDE_X09_answers.md). |

## Configuration can change behavior faster than code

A configuration change can alter routing, authorization, resource use, model selection or safety policy without replacing a binary. That convenience can bypass the long observation periods normally attached to software releases. A schema-valid value can still be operationally catastrophic: a regular expression can consume unbounded CPU, a route weight can overload one cell, or a feature flag can activate code that has never handled production traffic.

The decision is:

> Can this change prove useful on a small, representative scope before it can affect the next fault container—and can operators stop or reverse it through a path that the change cannot disable?

Approval and syntax validation are inputs, not the safety property. Safety comes from semantic limits, bounded exposure, observable promotion, ordered application and recoverable authority.

## Production case — a fast WAF rule path made one rule global

Cloudflare's 2 July 2019 postmortem reports that a new WAF Managed Rule contained a regular expression with enormous backtracking. It exhausted the CPU cores serving HTTP/HTTPS traffic worldwide, affected proxying, CDN and WAF functionality, and produced 502 responses. Cloudflare reports 27 minutes of service impact. [Cloudflare, “Details of the Cloudflare outage on July 2, 2019,” “The events of July 2,” lines 886–901](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)

The constraint was legitimate urgency. WAF rules had to respond quickly to emerging attacks, so they did not use Cloudflare's slower DOG/PIG/Canary software path. The rule passed the normal functional test suite, but that suite did not test runaway CPU consumption. Quicksilver then distributed the change across more than 180 cities with a reported global p99 of 2.29 seconds. [Cloudflare, same postmortem, “How Cloudflare operates,” “WAF Threats” and “Quicksilver,” lines 923–971](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)

The team chose a global WAF termination after live CPU evidence isolated the component. Access to the internal control panel was itself impaired because Cloudflare Access was down, so responders used a rarely practised bypass. After disabling the WAF, they tested the rollback in one city on a subset of traffic before re-enabling it globally. [Cloudflare, same postmortem, “What happened,” lines 902–922](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)

The postmortem lists the converging failures: no resource-cost test, a non-emergency global rollout, a slow rebuild-based rollback, delayed global alerting, and difficulty reaching internal systems. This was not simply a bad regex. A rapid control plane converted a local mistake into global exposure while the affected data plane obstructed operator access.

The transferable evidence is not “copy Cloudflare's current system.” Before applying the lesson elsewhere, measure propagation time, fault-containment boundaries, representative canary traffic, semantic cost limits, alert latency, rollback duration, last-known-good behavior and whether the emergency path shares identity, network, DNS or policy dependencies with the system it must disable.

## Make the configuration artifact explicit

Promote an immutable artifact, not a mutable key/value intention. A useful envelope contains:

| Field | Purpose |
| --- | --- |
| `epoch` and `version` | Establish total ordering within an authority generation |
| content digest | Detect equal-version conflicts and prove what was applied |
| schema and target compatibility | Reject values the binary cannot interpret |
| author, review and reason | Preserve provenance and incident context |
| intended scope | Name tenant, cell, zone, region or fleet boundaries |
| semantic budget | Bound CPU, memory, fan-out, route weight or another domain cost |
| issued and expiry times | Bound stale use where time semantics are safe |
| rollback artifact | Identify the tested predecessor or disable action |

Schema validation answers whether a document is shaped correctly. Semantic validation asks whether it can do useful work within real limits. Google SRE's configuration guidance gives examples such as a valid path that does not exist or a RAM request one thousand times larger than intended; it recommends preventing such errors when the user commits the configuration. [Google SRE Workbook, “Configuration Design and Best Practices,” “Semantic validation,” lines 143–146](https://sre.google/workbook/configuration-design/)

Validate domain invariants before rollout: regex work or execution timeout, total traffic weights, recursion depth, memory expansion, dependency existence, permitted principals, mutually exclusive flags and target-version compatibility. Then run the artifact against representative load. A functional test that gets the right answer once does not establish a resource bound.

## Separate distribution success from application success

The control plane distributes desired state. The data plane decides whether and how to apply it while continuing to serve. Track at least these states per target:

1. artifact accepted by the control plane;
2. artifact delivered with digest intact;
3. artifact parsed and semantically validated locally;
4. artifact activated at a named version;
5. post-activation health observed;
6. target promoted, held or rolled back.

“Delivered to 100%” can coexist with “crashing at 100%.” Promotion must use data-plane outcomes—availability, latency, saturation, correctness and business/safety signals—not acknowledgement alone.

Keep the last-known-good (LKG) artifact locally. Fetching a new version should not erase the active one. Parse and validate into a candidate, activate atomically, observe, and retain the predecessor until the rollback window closes. If the control plane disappears, an established data plane should normally continue with LKG rather than turn a control-plane outage into a serving outage.

That default is not universal. An expired certificate revocation or emergency deny rule may need fail-closed behavior, while a recommendation layout can safely remain stale. Choose per configuration class and document the consequence of stale, missing and invalid state.

## Reject late and conflicting updates

Distributed delivery reorders and duplicates messages. A target holding `(epoch=7, version=42, digest=A)` should:

- ignore a duplicate `(7, 42, A)`;
- reject an older `(7, 41, …)` even if it arrives later;
- surface `(7, 42, B)` as an authority conflict rather than guessing;
- accept a new epoch only through an explicit authority-transfer rule.

A timestamp alone is fragile because clocks skew and two writers can race. An epoch/version pair establishes authority and monotonic progress; the digest detects equivocation. Persist the applied tuple across restarts so an old snapshot cannot silently replace a newer safe configuration.

## Roll out by fault container, not percentage alone

Choose rings that align with containment boundaries: one process, one host, one cell, one availability zone, then additional regions. A “1% canary” spread across every region may create a global failure shape; one isolated cell can make rollback and diagnosis clearer.

For each stage define before rollout:

- maximum targets and traffic at risk;
- representative workloads and excluded critical tenants;
- guardrails with denominator, window and missing-data behavior;
- observation time longer than alert and effect latency;
- automatic hold/rollback rules;
- manual authority and an abort deadline.

AWS Well-Architected guidance describes fractional deployment through a one-box stage, progressively larger fractions aligned to fault-isolation boundaries, and bake time after each stage. It explicitly warns that without bake time the change expands before problems surface. [AWS Well-Architected, OPS04-BP01, “Implementation guidance,” lines 37–42](https://docs.aws.amazon.com/wellarchitected/latest/framework/ops04-bp01.html)

For an invented fleet with `N` targets, canary size `c`, detection time `d` and rollback time `r`, a simple upper bound is:

\[
E_{canary}=c(d+r)\text{ target-minutes}, \qquad E_{global}=N(d+r).
\]

This is exposure, not loss. Targets have different traffic and consequences, so real gates should weight requests, tenants or expected harm. The arithmetic forces the rollout to name its bound.

## Promotion is a decision with missing-data rules

Suppose the baseline CPU is 45%, the candidate reaches 98%, the absolute limit is 75%, and the permitted increase is 15 percentage points. The candidate fails both gates. Do not average it with healthy baseline hosts or promote because the dashboard is missing.

Use conjunctive gates:

- all critical metrics present and fresh;
- each absolute safety limit passes;
- each permitted change from a comparable baseline passes;
- no critical slice or fault container breaches its limit;
- enough traffic and time have accumulated to exercise the change.

If the metric pipeline fails, hold. “No evidence of harm” is not “evidence of safety.” X06's delayed-outcome reasoning still applies: a configuration whose effect appears after an hour needs an hour-scale observation or a tighter proxy, not a five-minute bake chosen for convenience.

## Keep stop and rollback independent

A safe rollout needs two different actions:

- **stop:** prevent distribution beyond the current stage;
- **rollback/disable:** restore the tested predecessor or bypass the affected component on already-exposed targets.

The emergency action should be minimal, pre-authorized, rehearsed and reachable without the feature it controls. Test dependency independence: identity provider, DNS, dashboard, configuration database, network path, build service and on-call credentials. Cloudflare's incident demonstrates why a documented switch is insufficient when the normal access path is impaired.

Avoid rollback that requires rebuilding the entire artifact during the incident. Keep an immutable predecessor or a narrow, resource-bounded kill switch at the data plane. Protect the emergency channel with strong authentication and audit, but maintain a tested break-glass route.

## Practice

All fleet sizes, timings, thresholds, versions and policy examples below are invented teaching inputs.

1. A 12,000-node fleet receives a configuration globally. Detection takes two minutes and rollback one minute. Compare its target-minute exposure with a 12-node first ring under the same timings. State what this metric omits.
2. A candidate raises CPU from 45% to 98%. The gate requires CPU at or below 75% and an increase no greater than 15 percentage points. Evaluate both predicates and the promotion decision. What should happen if candidate CPU is missing?
3. A node has applied `(epoch=7, version=42, digest=A)`. It later receives `(7,41,Z)`, `(7,42,A)`, `(7,42,B)` and `(8,1,C)`. Classify each result and name the extra evidence needed for the epoch change.
4. Choose behavior during control-plane loss for: a recommendation-layout setting, an emergency account-revocation list and a routing policy whose safe staleness limit is 15 minutes. Specify LKG, expiry and fail-open/fail-closed behavior rather than one global rule.
5. Review an invented WAF rollout whose disable button requires the same SSO, DNS and edge proxy affected by the WAF. Redesign stop, rollback and break-glass paths; list the evidence that would prove independence.

## Evidence and transfer questions

| Source | Inspected locator | Application boundary |
| --- | --- | --- |
| XR22 · Cloudflare | [2019 WAF outage postmortem](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/), “The events of July 2,” “What happened,” “How Cloudflare operates,” “WAF Threats,” “Quicksilver” and “What went wrong,” especially lines 886–922 and 935–981 | Documents the urgency constraint, passing functional tests, seconds-scale global distribution, CPU exhaustion, impaired operator access and mitigation. It does not describe Cloudflare's current architecture or establish universal ring sizes. |
| XR23 · Google SRE | [Configuration Design and Best Practices](https://sre.google/workbook/configuration-design/), “Semantic validation,” “Ownership and Change Tracking” and “Safe Configuration Change Application,” lines 143–182 | Grounds semantic validation, provenance, gradual application, rollback and loss-of-control concerns. It does not supply workload-specific limits or stale-state policy. |
| XR24 · AWS Well-Architected | [OPS04-BP01](https://docs.aws.amazon.com/wellarchitected/latest/framework/ops04-bp01.html), “Implementation guidance,” lines 37–42 and implementation steps | Current guidance for fault-aligned fractional stages, health signals and bake time. It is design guidance, not evidence that a particular deployment is safe. |

Before changing a real control plane, obtain the artifact/version model, semantic resource bounds, propagation and activation telemetry, fault-containment map, representative traffic, guardrail latency and missingness, LKG/expiry policy by configuration class, tested rollback duration, emergency-path dependency graph and recent drill evidence. No learner answer or mastery level is inferred from opening this lesson.

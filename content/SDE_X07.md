# X07 — Backups are not recovery

| Field | Value |
| --- | --- |
| ID / revision / date | X07 · 1.0 · 23 November 2026 |
| Prerequisites | S02 data recovery, S04 replication, S06 reliability boundaries and X05 migration safety |
| Capability developed | Prove that a workload can return from corruption or regional loss within an explicit data-loss and service-time budget. |
| Evidence | XR16–XR18. Primary postmortem, official recovery guidance and database documentation below. |
| Experiment | Recovery-point, dependency-path, backup-chain and reconciliation checks in the [worked companion](SDE_X07_answers.md). |

## A successful backup job proves very little

A green backup job proves that one producer wrote some artifact. It does not prove that the artifact is complete, that its keys and manifests survived, that the compatible software still exists, that the restore path has enough throughput, or that the restored service agrees with effects already committed outside it.

The useful question is:

> From a declared failure boundary, can this team restore a verified service state within its loss and time objectives, without replaying corrupt data or duplicating external effects?

That is a chain claim. Every required link must work: detection, write fencing, artifact selection, credentials, infrastructure, data restore, log replay, dependency ordering, application validation, traffic control and business reconciliation. A backup is only one input.

## Production case — GitLab had artifacts but not a recovery path

On 31 January 2017, an engineer attempting to rebuild a lagging PostgreSQL secondary removed data from the primary instead. The secondary was already being rebuilt and could not be failed over. GitLab then discovered that its scheduled `pg_dump` output was absent: a PostgreSQL 9.2 client was being used against PostgreSQL 9.6, the job failed, and its email alert was rejected. [GitLab postmortem, “Timeline” and “Database backups using pg_dump,” lines 131–158](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/)

The team chose a manually created LVM snapshot from about six hours before the incident because the regular snapshot was almost 24 hours old. The available copy lived on slow staging storage. Copying it to production took about 18 hours; GitLab restored the database to 17:20 UTC, separately recovered removed webhooks, advanced sequences to avoid reusing identifiers and gradually re-enabled the service. GitLab reported loss of database changes made between 17:20 and 23:30 UTC. [GitLab postmortem, “LVM snapshots,” “Recovering GitLab.com” and “Data loss impact,” lines 165–203](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/)

The constraint was not simply “no backup.” Several mechanisms existed, but their failure domains and restore behavior did not form a tested path. The production replica shared the operational event; logical backups were missing; disk snapshots were not enabled for the database; the usable staging copy was old and slow; and recovery required application-specific webhook and identifier repairs.

The response was to use the least-old usable copy, reconstruct dependent state, and accept bounded but material data loss. The postmortem then listed work on point-in-time recovery, hourly snapshots, automated restore tests, monitoring, runbooks and explicit durability ownership. Its stated root-cause chain says the restore exceeded 18 hours because the team needed a staging copy on slower storage in another region, while the standard backup was not working and the secondary was unavailable. [GitLab postmortem, “Root cause analysis” and “Improving recovery procedures,” lines 207–251](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/)

This is evidence about GitLab’s 2017 system, not a forecast for a current managed database. To apply the lesson elsewhere, obtain the workload’s actual artifact ages, corruption boundaries, restore throughput, dependency graph, retained credentials, compatible binaries, external side effects and measured validation time.

## Separate availability from disaster recovery

These mechanisms answer different failures:

| Mechanism | Useful against | Can share the original failure? | What it does not prove |
| --- | --- | --- | --- |
| Restart / crash recovery | Process or host crash with durable log intact | Yes | Survival of storage loss or logical corruption |
| Replica failover | Primary host or zone loss | Often | Independence from bad writes, operator deletion or shared control plane |
| Snapshot / full backup | Lost or damaged data set | Depends on location and credentials | Recent recovery point, log completeness or application usability |
| Point-in-time recovery | Logical corruption with a known safe boundary | Depends on archive isolation | Correct target selection or business reconciliation |
| Regional recovery environment | Regional service loss | Less, if genuinely independent | Data correctness, current configuration or acceptable cutover time |

Replication rapidly copies good writes **and bad writes**. It is an availability mechanism when the replica is isolated from a host failure; it is not automatically a corruption archive. Conversely, an offline backup may survive corruption but be too old or slow to meet the service objective.

Name the failure before choosing the mechanism: host loss, zone loss, region loss, credential loss, operator deletion, ransomware, software bug, schema error or silent corruption. “DR” without a failure boundary cannot be tested.

## Define the two clocks before the incident

Use explicit clocks rather than slogans:

- **Recovery point objective (RPO):** maximum tolerable distance between the failure boundary and the newest recoverable committed state. It is a data-loss budget, expressed in time only because commits are time-ordered.
- **Recovery time objective (RTO):** maximum tolerable time from a declared start event to a defined usable-service state.

For an invented incident, corruption occurs at 02:18:30 and the newest safe archived log ends at 02:17:40. The observed recovery-point distance is 50 seconds. That meets a 60-second RPO if — and only if — every required commit through 02:17:40 is present and the business accepts the missing interval.

RTO needs both endpoints. “Database accepts connections” is not the same as “customers can safely transact.” A defensible endpoint might require dependency health, invariant checks, authenticated reads, a controlled write, queue reconciliation and traffic shifted. Detection time may be included or excluded, but the service owner must say which; otherwise two teams can report different RTOs for the same incident.

Objectives are product decisions. A ledger and a rebuildable recommendation cache should not inherit the same RPO merely because they share an account. Record objectives per state class and identify which data is authoritative, derived, externally committed or legally retained.

## A restore is a dependency graph, not a checklist

Recovery stages overlap. Summing all durations overstates parallel work; timing only the database understates the service path. Model a directed acyclic graph and find the critical path.

Consider invented drill timings measured from disaster declaration:

| Stage | Dependencies | Duration |
| --- | --- | ---: |
| Identity and KMS access | None | 6 min |
| Network and DNS control | None | 8 min |
| Database restore and replay | Identity, network | 42 min |
| Object-store validation | Identity | 18 min |
| Application deployment | Database, network | 12 min |
| Smoke tests and reconciliation | Application, object store | 15 min |
| Traffic shift | Smoke tests | 5 min |

Identity and network start together. The database starts at minute 8 and ends at 50; object validation ends at 24. Application deployment ends at 62, smoke and reconciliation at 77, and traffic shift at 82. The critical path is 82 minutes, not the 106-minute sum and not the 42-minute database restore. Under a 90-minute objective the invented drill has eight minutes of margin.

That margin is not capacity evidence until the drill uses production-scale artifacts, realistic service quotas and a clean environment. A warm cache, pre-existing role or manually installed secret can make the test easier than the real disaster.

## Prove the backup chain is closed

For PostgreSQL point-in-time recovery, a base backup and the write-ahead log belong together. Current PostgreSQL documentation says a usable base backup requires the WAL generated during and after that backup, and recovery time grows with the amount of WAL to replay. Incremental recovery additionally requires all earlier backups that supply omitted blocks; PostgreSQL does not itself track which earlier backups must be retained. [PostgreSQL 19 documentation, §25.3.2–25.3.3, lines 75–93](https://www.postgresql.org/docs/current/continuous-archiving.html)

Recovery creates timelines so that a restored branch does not overwrite the WAL history from which it came. Timeline-history files are themselves required to choose the correct segments when an archive contains branches. [PostgreSQL 19 documentation, §25.3.6, lines 171–180](https://www.postgresql.org/docs/current/continuous-archiving.html)

A generic recovery manifest should therefore identify:

- base or full artifact, checksums and immutable location;
- every incremental ancestor and its order;
- log range, recovery target and timeline or equivalent history;
- database engine and extension versions;
- encryption-key identity and an independently tested access path;
- configuration, schema, network and identity dependencies;
- validation code and expected invariants;
- owner, retention policy and last successful restore drill.

“Latest backup succeeded” is not chain validation. Build the dependency closure from the chosen recovery point to every required ancestor, log segment, key and manifest. Then restore it into an isolated location. Never discover retention gaps by deleting the active system.

## Stop corruption before replaying it

Logical corruption changes the recovery problem. The newest state may be the least useful state.

1. Fence new writes or route them to an explicitly separate journal.
2. Preserve evidence: clocks, logs, damaged state and candidate recovery points.
3. Identify a last-known-good boundary using an invariant or event, not intuition.
4. Restore into isolation and replay only to that boundary.
5. Validate before granting production authority.
6. Reconcile accepted writes and external effects after the boundary.

Do not let the restored copy and damaged primary both accept authority. X05’s migration principle returns here: one representation must be authoritative at each step. If traffic continues in degraded mode, give each accepted operation an immutable identity and record where it must be reconciled.

## Validate four layers

AWS’s current recovery guidance recommends periodic restoration into a new location, data-integrity checks, measurement against RPO/RTO and an end timestamp recorded when validation finishes. It explicitly lists assuming that a backup exists, assuming it is operational and restoring without querying data as anti-patterns. [AWS Well-Architected REL09-BP04, lines 5–41](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_backing_up_data_periodic_recovery_testing_data.html)

Use four gates:

| Gate | Example evidence | Failure it catches |
| --- | --- | --- |
| Artifact | Manifest closure, signatures, checksums, decrypt test | Missing/corrupt object or lost key |
| Data | Database starts; schema and relational invariants hold; sampled rows match | Structurally present but unusable data |
| Application | Authenticated read and controlled write through the real service | Wrong config, secret, version or dependency |
| Business | Queues, object store and external providers reconcile by operation ID | Effects that crossed the recovery point |

The RTO clock stops only at the declared gate. A database-only drill does not establish an application RTO. A checksum-only drill does not establish semantic correctness.

## Restore does not reverse external effects

Suppose a payment service restores its database to 02:17:40. The payment provider still contains a successful charge `P102` accepted at 02:18:05, but `P102` is absent from the restored database. Retrying the customer request without checking the provider could charge twice.

Reconcile by stable operation identity:

- present internally and externally: verify attributes and mark settled;
- present externally but absent internally: import or compensate under policy;
- present internally but absent externally: resume or cancel from a durable intent state;
- present in neither: safe to accept as new only if no other authority exists.

The same issue appears with email, queues, object storage, search indexes, webhooks and model-training events. Restoration returns one subsystem to an earlier state; it does not time-travel the world.

## Design a drill that can fail usefully

A restore drill should start from a clean account or environment and a sampled artifact selected by policy, not the artifact an operator already knows works. Inject one failure at a time: missing incremental, corrupt block, revoked key, incompatible image, unavailable region, quota limit or changed DNS authority.

Record:

- failure scenario and independence assumptions;
- selected recovery point and measured loss window;
- dependency-stage start/end times and critical path;
- automated and manual actions, owners and approval waits;
- validation results at all four gates;
- unreconciled external effects;
- actual objective margin and the evidence that would invalidate it.

AWS Prescriptive Guidance says DR tests should verify functioning database restoration within RTO and data recovery within RPO, and should include growth, corrupt backups, drift, observability and local business objectives. It does not prescribe one universal test frequency. [AWS Prescriptive Guidance, “Testing to achieve confidence,” lines 5–35](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-database-disaster-recovery/testing.html)

Schedule by change and risk: after engine upgrades, key-policy changes, topology changes, large growth, retention changes and runbook ownership changes, plus a periodic cadence. A passed drill expires as the system changes.

## Practice

All timestamps, durations, artifacts and operation IDs below are invented teaching inputs.

1. Corruption begins at 02:18:30. A base backup at 02:00 has a complete archived-log chain through 02:17:40. Calculate the observed recovery-point distance and decide whether it meets a 60-second RPO. State what the arithmetic does not prove.
2. Reproduce the dependency schedule above. Calculate earliest start and finish times, identify the critical path, compare the result with a 90-minute RTO, and explain why adding durations is wrong.
3. A full backup `F0` has incrementals `I1 → F0`, `I2 → I1`, and `I3 → I2`. `I3` is newest, but `I1` has expired. Decide whether `I3` is restorable. Design a closure check that fails before an incident.
4. The restored database contains operations `P100` and `P101`. The external payment provider contains `P100`, `P101` and `P102`; the durable request journal also contains `P103`, which the provider does not. Classify the two mismatches and choose a safe next action.
5. Design a regional recovery drill for an API whose authoritative database, object store, identity configuration and outbound queue have different recovery mechanisms. Define the failure boundary, the RTO endpoint, validation gates and evidence needed before claiming that the drill transfers to production.

## Evidence and transfer questions

| Source | Inspected locator | Application boundary |
| --- | --- | --- |
| XR16 · GitLab | [Postmortem of database outage of January 31](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/), Timeline; Broken recovery procedures; Recovering GitLab.com; Root cause analysis; Improving recovery procedures | Documents the 2017 failure, available mechanisms, chosen restore path, observed bottleneck, data loss and response. It does not establish current GitLab architecture or another workload’s objectives. |
| XR17 · AWS | [REL09-BP04](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_backing_up_data_periodic_recovery_testing_data.html), Desired outcome, Common anti-patterns and Implementation steps 1–7; [Testing to achieve confidence](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-database-disaster-recovery/testing.html), checks, considerations, drift and observability | Current provider guidance on tested restore evidence and objectives. It is not proof that an AWS service configuration meets a particular workload’s RPO/RTO. |
| XR18 · PostgreSQL | [PostgreSQL 19, Continuous Archiving and PITR](https://www.postgresql.org/docs/current/continuous-archiving.html), §§25.3.2–25.3.3 and 25.3.6 | Current base/incremental/WAL dependency and timeline semantics. Exact commands and guarantees depend on the deployed version and backup tool. |

Before applying this lesson, obtain the authoritative-state inventory, explicit failure scenarios, business-approved objectives, artifact dependency manifests, key independence, production-scale throughput, service dependency graph, external-effect identifiers, clean-environment drill results and named recovery authority. No learner answer or mastery level is inferred from opening this lesson.

# Extension audit 03 — X07–X08

| Field | Result |
| --- | --- |
| Scope | X07–X08 lessons, worked companions, XR16–XR21 evidence boundaries, generated routes, search, links and navigation |
| Audit date | 24 November 2026 |
| Outcome | Passed. No factual claim or worked result required correction; two concrete gaps were selected for the next balanced Cloud/AI batch. |
| Learner state | Not inspected or inferred. Browser progress remains learner-controlled. |

## Audit method

This audit re-opened each cited primary production report, official documentation page and feature-platform source at the lesson's recorded locator. It checked that observed evidence is separated from invented teaching values, every exercise maps to one worked response, executable examples reproduce the stated results, and the built site exposes the batch through search and navigation.

The audit also reconciled an apparent PostgreSQL version conflict. A search result initially described the current continuous-archiving page as version 18, while the official page opened on 24 November identifies itself as PostgreSQL 19 and retains the recorded §25.3 locators. X07 and XR18 therefore remain correctly labeled; no source change was made from stale search metadata.

Passing this audit does not prove a production restore path, feature pipeline or learner capability. Those require local evidence described by each lesson.

## Findings by extension

| Extension | Primary-passage boundary | Companion and example check | Result |
| --- | --- | --- | --- |
| [X07 — Backups are not recovery](SDE_X07.md) | XR16 supports GitLab's 2017 primary-data deletion, unusable replica, missing logical backup, six-hour LVM recovery point, storage-bound restore of approximately 18 hours, application-specific webhook/sequence work and reported loss. XR17 supports clean-location restore tests, integrity validation and measurement against locally declared RPO/RTO. XR18 supports PostgreSQL base/incremental/WAL dependencies and recovery timelines. The lesson does not infer current GitLab architecture, a universal restore duration or that replication is never useful for recovery. | Five practice items map to five worked sections. The executable model reproduces a 50-second recovery-point distance, an 82-minute dependency critical path versus a misleading 106-minute duration sum, rejection of a missing-ancestor incremental chain, and classification of one externally committed orphan plus one unresolved intent. | Pass |
| [X08 — Point-in-time feature correctness](SDE_X08.md) | XR19 supports Uber's online/offline mismatch problem, exact inference-feature logging decision, scale constraints and reported rollout outcomes. XR20 supports Chronon's shared computation model, temporal versus snapshot accuracy and point-in-time join boundary. XR21 explicitly distinguishes event-time filtering from optional created/availability-time filtering. The lesson does not claim one feature name proves parity, that logging is unbiased, or that event time alone reconstructs what serving knew. | Five practice items map to five worked sections. The executable model reproduces event-time-only 130 versus as-known 40, a half-open-window sum of 50, `low`/`high` mutable values at 10:00/12:00, and a 14% union mismatch from overlapping feature errors. | Pass |

## Cross-module boundaries

X07 and X08 both reconstruct an earlier state, but the authority and failure model differ.

- X07 asks which durable state can safely become authoritative after loss or corruption. Its clocks are failure boundary, recovery point and validated-service endpoint.
- X08 asks which facts were observable when a model made a historical decision. Its clocks are prediction, event, availability/revision and label maturity.
- A PostgreSQL timeline preserves recovery branches; it does not supply an ML feature's availability semantics.
- An inference feature log can preserve an exact served vector; it does not replace disaster recovery for its storage, guarantee representative coverage or create features that were never logged.
- X07 reconciliation joins restored internal state to external effects by stable operation identity. X08 parity joins served and recomputed vectors by stable prediction identity. Neither join can be reconstructed reliably from mutable business keys alone.

Both lessons reject a green producer job as sufficient evidence. A backup job needs a tested restore and validation chain. A feature pipeline needs as-of reconstruction or exact served logging plus parity checks.

## Executed checks

| Check | Observed result |
| --- | --- |
| Practice-to-companion mapping | 10 practice items and 10 numbered worked sections; exact mapping in X07–X08 |
| Executable companion examples | Two Python blocks executed; all assertions passed |
| Evidence IDs | XR16–XR21 present once each in the extension register and mapped to lesson evidence tables |
| Invented-input boundary | Both lessons and companions label all exercise times, durations, values, identities and sample counts as invented |
| Claim boundary | Production observations are attributed; transfer requires local objectives, clocks, volumes, policies and measured paths |
| Markdown build | Completed from the saved repository source |
| Internal routes and fragments | Every generated internal target resolved |
| Search catalogue | Lessons, companions, roadmap and this audit indexed with distinct URLs |
| Navigation | X07/X08 remain in Cloud/AI routes, curriculum and progress; this audit is exposed from the homepage and reference page |

## Repairs made

No source claim, formula, answer or lesson route required correction. Continuity changes made by the audit are:

- mark X07–X08 and their companion mappings as audited;
- save and expose this audit as a reference artifact;
- replace the completed audit placeholder with a two-item Cloud/AI batch;
- update the homepage from “new X08” to the audited batch state.

## Next batch selected from concrete gaps

### X09 — Safe configuration rollout and control-plane blast radius

S06 limits authority and capacity damage, X05 stages schema/data migration, X06 stages model exposure, and X07 restores durable state. None follows a configuration change that is syntactically valid but globally unsafe, reaches many regions faster than a binary, overloads a shared data plane, or disables the same control path needed to revert it.

This is a practical Cloud gap because feature flags, routing tables, WAF rules, quotas, identity policy and service discovery can change behavior without a code deployment. The lesson should require an original infrastructure postmortem, explicit control-plane/data-plane boundaries, last-known-good behavior, progressive scope, independent rollback, configuration invariants and blast-radius arithmetic. It must distinguish validation from safe exposure and a kill switch from an ordinary flag stored behind the failing dependency.

### X10 — Selective labels and decision feedback

X06 handles delayed outcomes and bounded model release; X08 preserves what was knowable at prediction time. Neither handles the case where the deployed decision changes which outcomes become observable. A blocked payment does not reveal whether it would have become fraud, a denied application reveals no repayment outcome, and claims sent to manual review receive richer labels than auto-approved claims.

This is a practical AI gap for fraud, insurance, ranking and agent workflows. The lesson should require a primary selective-labels or feedback-loop paper plus a documented production decision where available; separate missing, delayed and policy-selected labels; trace propensities and human review; compare safe exploration, auditing and partial identification; and show why retraining on observed outcomes can reinforce the serving policy. It must not present random exploration as acceptable for high-severity actions without a loss boundary.

X09 and X10 compound this batch: X07 proves that state can be recovered, while X09 prevents one global control change from creating or extending the disaster; X08 reconstructs prediction-time evidence, while X10 asks why the outcome evidence may still be selected by the deployed decision. Extension audit 04 should follow before any further topic is selected.

## Unresolved application evidence

Applying X07–X08 still requires local state inventories, recovery objectives, artifact/key independence, production-scale restore throughput, dependency graphs, external-effect identities, prediction and availability clocks, correction history, logging coverage, label maturity and parity by risk slice. These are intentionally unresolved deployment inputs, not missing generic content. No learner response or mastery has been inferred.

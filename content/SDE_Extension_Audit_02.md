# Extension audit 02 — X05–X06

| Field | Result |
| --- | --- |
| Scope | X05–X06 lessons, worked companions, XR10–XR15 evidence boundaries, generated routes, search, links and navigation |
| Audit date | 23 November 2026 |
| Outcome | Passed. No factual claim or worked result required correction; two concrete gaps were selected for the next balanced Cloud/AI batch. |
| Learner state | Not inspected or inferred. Browser progress remains learner-controlled. |

## Audit method

This audit re-opened the primary production reports, official documentation and papers at the locators recorded in the lessons. It checked whether each lesson distinguishes observed production evidence from its own teaching model, whether every exercise maps to a worked response, whether executable examples reproduce the stated arithmetic, and whether the built site exposes all routes through search and navigation.

The audit does not treat a valid citation, passing script or successful deployment as proof that a learner can apply the mechanism or that a production system is safe.

## Findings by extension

| Extension | Primary-passage boundary | Companion and example check | Result |
| --- | --- | --- | --- |
| [X05 — Safe data migrations](SDE_X05.md) | XR10 supports Stripe's constraints, four-phase dual-write/read/write/removal sequence, offline identity discovery, production read comparison and reported no-downtime outcome. XR11 supports PostgreSQL's separation of new-write enforcement from historical validation with `NOT VALID`/`VALIDATE CONSTRAINT`, including its lock boundary and rewrite caveats. XR12 supports GitHub's reported trigger-related lock failures, binlog-driven `gh-ost` design, pause/test controls and production adoption. The lesson does not claim dual writes are atomic or that either database mechanism transfers unchanged. | Five practice items map to five worked sections. The executable model rejects stale revision 41 after live revision 42, surfaces equal-revision conflicts, reproduces 9,600 seconds of modeled copy/rescan work and checks three contract states. | Pass |
| [X06 — AI release gates](SDE_X06.md) | XR13 supports slice gates, pre-serving validation, canaries, rollback and continuous skew/quality monitoring. XR14 supports Uber's stated platform scale, mandatory backtesting, live shadowing, gradual rollout, automatic rollback, reported shadow adoption and reduction from days to hours for surfaced regressions. XR15 supports two-sample shift detection while explicitly exposing representation-driven false negatives and sample-regime limits. The lesson treats drift as a diagnostic signal rather than a quality verdict. | Five practice items map to five worked sections. The executable model reproduces the 88.60%/89.65% aggregate result, rejects the hidden −8-point slice regression, reconstructs 32% versus 2.53% shadow disagreement, derives the 1/60 exposure ceiling and counts 140,000 decisions before seven-day labels mature. | Pass |

## Cross-module boundaries

X05 and X06 both teach staged authority transfer, but their evidence is not interchangeable.

- X05 protects durable representation changes. Its revision guard requires a trustworthy per-identity order and an atomic compare/write boundary; the script is not a distributed transaction proof.
- X05's PostgreSQL sequence is operation- and version-specific. `NOT VALID` reduces one validation impact; it does not make DDL lock-free or solve application compatibility.
- X06 protects increasing behavioral exposure. A green shadow establishes live compatibility only for traffic generated under the primary policy; it cannot observe the candidate's counterfactual effect on users or future data.
- X06's risk-budget arithmetic translates assumed loss into an exposure ceiling. It does not estimate the loss rate or its uncertainty, and it cannot average away a disqualifying high-severity action.
- X06's drift tests can trigger investigation, labeling or a hold. Absence of a detected shift is not evidence that prediction quality is unchanged.

Both lessons bind rollback to a compatible bundle rather than a label. X05 asks whether old readers and writers still have a valid representation; X06 asks whether model, feature, index, prompt, policy and runtime versions can be restored together.

## Executed checks

| Check | Observed result |
| --- | --- |
| Practice-to-companion mapping | 10 practice items and 10 numbered worked sections; exact mapping in X05–X06 |
| Executable companion examples | Two Python blocks executed; all assertions passed |
| Evidence IDs | XR10–XR15 present once each and mapped to lesson evidence tables |
| Invented-input boundary | Both lessons and companions label synthetic values and deny production-threshold inference |
| Markdown build | Completed from saved source |
| Internal routes and fragments | Every generated internal target resolved |
| Search catalogue | Lessons, companions, roadmap and this audit indexed with distinct URLs |
| Navigation | X05 and X06 remain in Cloud/AI topic routes, full curriculum and progress; this audit is exposed from the homepage and reference page |

## Repairs made

No source claim, formula, answer or route required correction. Continuity changes made by this audit are:

- mark X05–X06 and their companion mappings as audited;
- save and expose this audit as a reference artifact;
- replace the completed audit placeholder with a two-item Cloud/AI batch;
- update the homepage to identify the audited batch rather than presenting X06 as unaudited new work.

## Next batch selected from concrete gaps

### X07 — Backups are not recovery

The existing systems track explains local log recovery, leader failure, replication, overload and isolation. It does not ask whether a restorable chain survives operator error, logical corruption or regional loss; whether dependency order permits service recovery; or whether measured restore time and data loss satisfy an explicit RTO/RPO. This is a practical Cloud gap because a successful backup job can coexist with missing credentials, incompatible manifests, corrupt snapshots or an untested restore path.

The lesson should require a documented production recovery incident or postmortem, official restore semantics, a dependency graph, recovery-point arithmetic and a timed restore drill. It must distinguish high availability from disaster recovery and restoration from business reconciliation.

### X08 — Point-in-time feature correctness

A01 aligns evaluation with deployment and X06 detects training-serving skew, but neither reconstructs a feature exactly as it was knowable at prediction time. Late events, mutable joins, backfilled dimensions and future labels can make offline evaluation impossible to reproduce and silently leak the future. This is a practical AI/data gap for risk, claims, ranking and forecasting systems.

The lesson should require a primary feature-platform engineering report or paper, event/availability-time distinctions, point-in-time join examples, late-data handling and online/offline parity checks. It must show that a shared feature name does not prove shared semantics.

X07 and X08 compound the audited batch: X05 migrates durable state, X07 proves it can be restored; X06 gates a model release, X08 protects the historical and live features used to justify that gate. Extension audit 03 should follow before more topics are selected.

## Unresolved application evidence

Applying X05–X06 still requires local mutation inventories, ordering guarantees, database service curves, fleet compatibility, evaluation lineage, slice denominators, delayed-outcome joins, risk budgets and timed rollback evidence. These are intentionally unresolved deployment inputs, not missing generic content. No learner response or mastery has been inferred.

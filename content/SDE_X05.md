# X05 — Safe data migrations without split-brain truth

| Field | Value |
| --- | --- |
| ID / revision / date | X05 · 1.0 · 22 November 2026 |
| Prerequisites | S02 identity, S03 concurrency, S04 replication and C03 useful capacity |
| Capability developed | Move durable state between representations while preserving one explicit authority, rejecting stale backfill and proving each authority transfer before removing the old path. |
| Evidence | XR10–XR12. Primary production passages and scope below. |
| Experiment | Versioned backfill, rollout gates and capacity checks in the [worked companion](SDE_X05_answers.md). |

## A schema change is a protocol change

Adding a nullable column can be mechanically easy. Changing which representation carries business truth is not. During a rolling release, old and new application binaries coexist. A backfill reads the past while live requests change the present. Replicas, queues and retries delay effects. If two representations can both accept an update, the migration has introduced a distributed protocol—even when both tables live in one database.

The first migration artifact should therefore be a contract, not a DDL statement:

- **Logical identity:** which old and new records describe the same object?
- **Invariant:** which normalized values must agree?
- **Authority:** which representation wins in this phase?
- **Order:** which monotonic revision, commit position or event identity distinguishes newer state?
- **Repair:** which mismatch can be retried automatically, and which must stop the migration?
- **Exit evidence:** what proves every old reader or writer is gone?

“Both tables are sources of truth” is not a safe transition state. One side remains authoritative while the other is derived, compared and repaired. Authority moves only at a named gate.

## Production case — Stripe moved live Subscription state

Stripe needed to move subscription data out of Customer objects into a separate table. The constraints were concrete: hundreds of millions of objects, continuous transactions, services operating at full availability, and subscription logic spread across thousands of lines. A sequential one-second-per-object process would take more than three years for 100 million objects. [Stripe, “Online migrations at scale,” “Why are migrations hard?” and “Our example migration”](https://stripe.com/blog/online-migrations)

The team used four phases: write both stores, move reads, move writes, then remove old data. New objects were dual-written; existing identities were found from offline snapshots and backfilled with parallel workers; a second offline pass checked for missing objects. Before changing read authority, production reads were evaluated through both paths and mismatches generated alerts. Write paths were then moved incrementally, and only after old dependencies were gone did the new table become the source of truth. [Stripe, “A pattern for online migrations,” parts 1–4](https://stripe.com/blog/online-migrations)

The reported outcome was an online transition without downtime. Stripe attributes confidence to small incremental changes, offline processing rather than expensive production discovery queries, and production comparison that surfaced even single inconsistencies. This is evidence for a migration method, not evidence that application-level dual writes are atomic or appropriate everywhere. To transfer it, you would need local evidence about write ordering, retry semantics, snapshot age, comparison coverage, database headroom and every mutation path.

## Expand, migrate, prove, contract

Treat the migration as a state machine. Each phase has one authority and a rollback boundary.

| Phase | Old representation | New representation | Gate to advance |
| --- | --- | --- | --- |
| 0 · Define | Authoritative | Absent | Identity, invariant, revision and stop conditions reviewed |
| 1 · Expand | Authoritative | Compatible but optional | Old and new application versions both tolerate the expanded schema |
| 2 · Capture | Authoritative | Receives derived live changes | Duplicate-write errors, lag and database load stay inside limits |
| 3 · Backfill | Authoritative | Receives idempotent historical copies | Coverage complete; stale copies rejected; repair queue drained |
| 4 · Compare | Authoritative | Shadow-read only | Semantic mismatch rate and sampling coverage meet a fixed gate |
| 5 · Read cutover | Fallback | Authoritative for canary readers | User outcomes, mismatch and latency remain safe through rollback window |
| 6 · Write cutover | Derived or archived | Authoritative | No old writers; reverse path or forward repair is proven |
| 7 · Contract | Removed only after delay | Sole authority | Old binaries, jobs and restore procedures no longer depend on old shape |

The phase number is operational state. Record it durably. A deploy succeeding does not prove the fleet is homogeneous; use observed binary versions, query telemetry, job inventories and restore tests.

## The stale-backfill race

Consider an invented insurance migration from `policy.annual_premium_cents` to a new `policy_terms` table. Both representations carry a monotonic `revision`.

1. A snapshot sees policy `P7` at `(120000, revision 41)`.
2. A live request changes the premium to `125000` and dual-writes revision 42.
3. A delayed backfill worker copies the snapshot row into the new table.

An unconditional upsert makes the new representation older: it replaces revision 42 with 41. Faster workers only make the race less likely. The safe property is:

> Applying an incoming record must never reduce the stored revision for the same logical identity.

One possible database boundary is a conditional upsert that changes the target only when `incoming.revision > stored.revision`. Equal revisions with unequal normalized values indicate a broken premise; alert and quarantine rather than choosing silently. If the source has no stable revision, use a commit position, change-data-capture offset or another ordering identity whose lifetime and uniqueness you can defend. A wall-clock timestamp from multiple writers is not automatically such an identity.

The backfill must also be idempotent. A crash after committing a batch but before recording its checkpoint should permit the same batch to run again without changing the result. Checkpoints are hints for progress, not the correctness boundary.

## Compatibility is a matrix

Rolling deployment safety is a matrix, not a single “backward compatible” label.

| Application binary | Expanded schema | Contracted schema |
| --- | --- | --- |
| Old binary | Must continue reading and writing its old shape | Usually unsafe |
| New binary before cutover | Writes or derives both; still reads old authority | Unsafe if it retains fallback |
| New binary after cutover | Reads new authority; old path retained for bounded fallback | Safe only after old dependency is removed |

Expand first and contract last. A rollback after read cutover can be cheap if live updates still reach the old representation. A rollback after new-only writes is a data migration, not merely an application deploy. After destructive contract, recovery may require restore and replay. State the last reversible phase before starting.

## Enforce new rules without one long blocking scan

PostgreSQL documents a useful separation for foreign-key, `CHECK` and not-null constraints. Adding a constraint with `NOT VALID` skips the potentially long scan of existing rows but still enforces the rule for subsequent inserts and updates. `VALIDATE CONSTRAINT` later scans old rows with a weaker table lock than the initial validating form. [PostgreSQL 19 `ALTER TABLE`, `ADD table_constraint [ NOT VALID ]`, `VALIDATE CONSTRAINT`, and Notes](https://www.postgresql.org/docs/current/sql-altertable.html)

That supports a sequence such as:

```sql
ALTER TABLE policy_terms
  ADD CONSTRAINT premium_nonnegative
  CHECK (annual_premium_cents >= 0) NOT VALID;

-- Repair or quarantine historical violations in bounded batches.

ALTER TABLE policy_terms
  VALIDATE CONSTRAINT premium_nonnegative;
```

This is not lock-free. Inspect the exact database version, lock modes, transaction duration, replicas and table size. PostgreSQL also warns that rebuilds can require significant time and temporary disk space, and that rewriting forms of `ALTER TABLE` are not MVCC-safe for older snapshots. A syntactically valid migration can still violate the service capacity budget.

## Production case — GitHub made schema migration pauseable

GitHub reported that trigger-based MySQL schema migration became risky as traffic grew: some migrations caused outages, trigger work competed for locks, and even removing triggers could stall a busy table. The team built `gh-ost`, which copies into a ghost table but streams ongoing changes from row-based binary logs instead of attaching synchronous triggers to application transactions. [GitHub, “gh-ost,” existing landscape and trigger limitations](https://github.blog/news-insights/company-news/gh-ost-github-s-online-migration-tool-for-mysql/)

Decoupling change capture made the migration pauseable. GitHub describes throttling on server load or replication lag, postponing final cutover while continuing to apply changes, testing table swaps on replicas, and eventually running the tool for all production migrations, often several times a day. [GitHub, “Pauseable,” “interactive commands,” operation modes and “gh-ost at GitHub”](https://github.blog/news-insights/company-news/gh-ost-github-s-online-migration-tool-for-mysql/)

The transferable decision is not “always use `gh-ost`.” It is to isolate migration work from request transactions where possible, expose a stop control, measure change-capture lag, test the exact cutover mechanism and retain enough disk and log history to finish or abort. The tool's assumptions—MySQL topology, binary-log format, keys and replication behavior—must be checked locally.

## Gates that measure truth, not motion

Rows scanned and percent complete describe motion. Advance authority only on evidence about correctness and user impact:

- **Coverage:** identities present in old authority but absent from new, and vice versa.
- **Semantic equality:** normalized business values match; ignore representation-only differences intentionally.
- **Freshness:** revision or commit-position lag, including the tail rather than only the average.
- **Mutation coverage:** every writer, scheduled job, replay and administrative path observed on the new path.
- **Capacity:** primary load, lock wait, replica lag, log growth, queue age and free disk during worst overlap.
- **Outcome:** error, latency and domain invariants for canary readers after authority changes.

Sampled comparison can find common mismatches but cannot prove absence of rare ones. Combine it with complete key-set checks, database constraints, event counts or reconciliations appropriate to the loss. Define the acceptable residual and who owns repair before cutover.

## Practice

All policy data, rates and thresholds below are invented teaching inputs.

1. Trace the three-event stale-backfill history for policy `P7`. Show the final new-table state under unconditional upsert and revision-guarded upsert. What should happen for equal revision but unequal value?
2. A backfill has 2,400,000 rows. Workers can copy 800 rows/s, but production headroom limits the safe rate to 300 rows/s. Estimate the fastest safe duration, then add a 20% rescan. Why is this not a completion forecast?
3. Build a compatibility decision for three fleet states: 30% old binaries, 100% new binaries with old fallback, and 100% new binaries with fallback removed. Which migration phases may safely contract the old column?
4. Design a PostgreSQL rollout for a new nonnegative-premium rule over a large table with known historical violations. Include enforcement, repair, validation, observability and abort evidence.
5. Design the authority-transfer gate for moving claim documents from a relational blob column to object storage. Name identity, ordering, comparison, capacity, rollback and deletion evidence. Do not treat object existence as content equality.

## Evidence and deployment questions

| Source | Inspected locator | Application boundary |
| --- | --- | --- |
| XR10 · Stripe | [Online migrations at scale](https://stripe.com/blog/online-migrations), “Why are migrations hard?”, “A pattern for online migrations,” parts 1–4 and Conclusion | Documents a production application-data migration, constraints, staged choice and reported no-downtime outcome. It does not make dual writes atomic or prescribe this topology universally. |
| XR11 · PostgreSQL Global Development Group | [`ALTER TABLE`](https://www.postgresql.org/docs/current/sql-altertable.html), `ADD table_constraint [ NOT VALID ]`, `VALIDATE CONSTRAINT`, Notes and examples | Defines behavior and lock boundary for supported PostgreSQL constraints. Exact behavior is version- and operation-specific. |
| XR12 · GitHub | [gh-ost: GitHub's online schema migration tool for MySQL](https://github.blog/news-insights/company-news/gh-ost-github-s-online-migration-tool-for-mysql/), existing landscape, trigger limitations, Pauseable, operation modes and “gh-ost at GitHub” | Documents GitHub's production problem, design choice and adoption. It is not evidence for non-MySQL systems or for unverified topologies. |

Before applying this lesson, obtain the schema and application compatibility matrix, authoritative identity and revision semantics, real mutation inventory, backfill service curve, lock and replication behavior, mismatch loss, rollback window, restore test and deletion-retention obligations. A migration is complete only when the new authority is proven and the old dependency can be removed without guessing.

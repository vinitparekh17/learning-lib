# X08 — Point-in-time feature correctness

| Field | Value |
| --- | --- |
| ID / revision / date | X08 · 1.0 · 24 November 2026 |
| Prerequisites | F03 measurement, A01 distribution change, A04 serving and X06 release evidence |
| Capability developed | Reconstruct the feature vector that was actually knowable at prediction time, despite late events, mutable dimensions, backfills and separate online/offline pipelines. |
| Evidence | XR19–XR21. Production engineering reports and current feature-store semantics below. |
| Experiment | Event/availability-time joins, correction versions, window boundaries and parity checks in the [worked companion](SDE_X08_answers.md). |

## Historical truth is not prediction-time truth

A warehouse queried today may know that a payment occurred at 09:45, that a customer dimension was corrected, and that a claim was fraudulent. A model deciding at 10:00 did not necessarily know any of those facts. Training on today’s best reconstruction can therefore teach the model with information that production did not have.

The decision is:

> For every historical prediction row, can we reproduce the feature values available to the serving system at that instant, under the same keys, windows, transformations and missing-data rules?

A shared feature name does not establish this. `customer_chargeback_count_30d` can mean different things when batch and streaming paths disagree about time zones, late arrivals, corrections, window edges, nulls, identity joins or freshness.

## Production case — Uber logged the features the model actually consumed

Uber reported that its online and offline pipelines produced inconsistent feature representations and values. Its examples include language codes formatted differently across training and serving, fragile ETL lineages and multi-day freshness gaps. Engineers sometimes spent weeks tracing the discrepancies. [Uber, “Taming the ML Firehose,” Problem, lines 32–70](https://www.uber.com/us/en/blog/taming-ml-firehose/)

The team chose inference-time feature logging as a canonical training source: record the exact feature values consumed by a prediction, join them later to independently emitted impression events, and train on the resulting records. This avoids reconstructing already-served vectors through a different batch pipeline. [Uber, same report, Solution and Online Architecture, lines 71–108](https://www.uber.com/us/en/blog/taming-ml-firehose/)

The constraint was scale. Uber describes recommendation traffic up to 8 million queries per second; logging everything was estimated at about 1.7 PB per day and 5 trillion rows per month for the discussed use case. The design therefore allow-listed used features, encoded long names as compact identifiers and retained prediction records only when a user impression made them useful for training. The allow list reduced payload size by 4–5×. [Uber, same report, Scale Challenges and Feature Allow List, lines 77–121](https://www.uber.com/us/en/blog/taming-ml-firehose/)

After rollout to search and ranking models, Uber reported 0% mismatch on selected key features that had exceeded 10% mismatch, and priority-feature freshness improving from multi-day latency to hours. It also reported roughly 70% lower peak consumer lag after a series of pipeline optimizations. [Uber, same report, High Throughput and Conclusion, lines 127–156](https://www.uber.com/us/en/blog/taming-ml-firehose/)

This is a documented production decision, not proof that logging is always preferable. It preserves what the model consumed for existing traffic, but costs bandwidth and storage, may omit unlogged experimental features, and still needs correct label joins and sampling. To transfer it, measure local prediction volume, retained impressions, feature payload, delay distribution, privacy limits and whether logging failures are correlated with important traffic.

## Four clocks belong in the data contract

Use explicit timestamps:

| Clock | Meaning | Example |
| --- | --- | --- |
| Prediction time `t_p` | When the model had to decide | Claim submitted at 10:00 |
| Event time `t_e` | When the underlying fact occurred | Payment occurred at 09:45 |
| Availability time `t_a` | When the feature system could read the fact | Payment reached the feature pipeline at 10:07 |
| Revision time `t_r` | When a prior fact was corrected or superseded | Customer tier corrected at 11:00 |

For a training row at `t_p`, a fact is eligible only if its domain semantics allow it and both `t_e ≤ t_p` and `t_a ≤ t_p`. For a half-open historical window of width `W`, require:

\[
t_p-W \le t_e < t_p \quad\text{and}\quad t_a \le t_p.
\]

The strict upper event-time bound prevents the prediction-triggering event from entering a feature that should describe only prior behavior. Some products deliberately include fields from the current request; those belong to request context and need a separate contract rather than an accidental aggregate.

Availability time means observable by the serving path, not merely inserted somewhere. A warehouse ingestion timestamp is useful only if it faithfully represents when the online system could have used the value.

## Event-time-only joins can leak late data

Use an invented prediction at 10:00 and three transactions:

| Event | Amount | Event time | Available time |
| --- | ---: | --- | --- |
| E1 | 40 | 09:10 | 09:11 |
| E2 | 90 | 09:45 | 10:07 |
| E3 | 30 | 10:05 | 10:05 |

An offline query run later with only `event_time < 10:00` returns E1 and E2, sum 130. The production model at 10:00 could see only E1, sum 40. E2 is historically valid but arrived seven minutes after the decision; E3 occurred after it. The event-time-only backfill leaks 90.

Current Feast documentation makes this boundary explicit. Its default point-in-time join constrains event time; a later backfill or correction can still appear in an earlier training row. When a source supplies a created/availability timestamp, `filter_by_created_timestamp=True` adds the requirement that it be no later than the entity-row timestamp. Unsupported stores raise rather than silently ignoring that option. [Feast, “Point-in-time joins,” Retrieving features as of the event time, lines 218–232](https://github.com/feast-dev/feast/blob/master/docs/getting-started/concepts/point-in-time-joins.md)

That option is a tool-specific implementation. The transferable principle is bitemporal: constrain both when the fact was true and when the decision system could know it.

## Mutable dimensions need version-as-known semantics

Suppose customer `C7` has two versions with the same effective time:

| Value | Effective event time | Available/revision time |
| --- | --- | --- |
| `risk_tier=low` | 08:00 | 08:02 |
| `risk_tier=high` | 08:00 | 11:00 |

The 11:00 correction may be the best current account history, but a 10:00 prediction saw `low`. A query that chooses the latest row for the effective timestamp leaks the correction.

For each entity and effective interval, first exclude versions with availability after `t_p`; then select the latest eligible revision. Preserve deletions and corrections as versions rather than overwriting warehouse rows. Without history, exact reconstruction is impossible; log the served value or declare the training row non-reproducible.

Slowly changing dimension labels such as state, policy status, merchant category and account verification are especially dangerous because a corrected row can silently rewrite many old examples.

## The label is allowed to arrive later; the features are not

Supervised learning intentionally attaches a future outcome to an earlier decision. A fraud confirmation at day 30 can label a transaction predicted on day 0. That does not permit day-30 information into the day-0 feature vector.

Store separately:

- immutable prediction identity and `t_p`;
- served feature/bundle version or reproducible feature manifest;
- label definition, observation window and maturity time;
- censoring rule for examples whose label window is incomplete.

Split data by prediction time or entity according to the deployment question. Randomly splitting rows after feature leakage does not repair the leakage; the forbidden information is already inside each row.

## Window boundaries are part of the feature definition

For `count_prior_payments_24h` at 10:00, choose and test one interval, such as `[previous-day 10:00, current-day 10:00)`. Decide:

- whether the lower boundary is inclusive;
- whether current-request data is separate;
- which time zone and daylight-saving rule applies;
- whether late events update only future predictions or also historical backfills;
- TTL and missing-value behavior;
- whether deletes/corrections retract earlier aggregates.

Two pipelines both implementing “24 hours” can disagree by one event, a day boundary or an entire late partition. Version the semantics, not only the column name.

## Shared computation and exact logging solve different gaps

Airbnb’s Chronon engineering report describes one declarative feature computation used in both online and offline contexts. Snapshot mode provides daily/midnight accuracy; temporal mode uses change data to backfill historical points with finer accuracy. Joins take the prediction event and its time column as the left side, so features are computed as of the historical decision time. Airbnb reported more than ten thousand Chronon features and said teams typically moved from months of manual pipeline/index work to less than a week for new feature sets. [Airbnb, “Chronon — A declarative feature Engineering framework,” computation contexts/types and conclusion, lines 125–159](https://medium.com/airbnb-engineering/chronon-a-declarative-feature-engineering-framework-b7b8ce796e04)

Chronon’s current Join documentation distinguishes real-time temporal backfills from batch sources that are midnight-accurate by default. That distinction matters: one definition does not make a daily source millisecond-fresh. [Chronon Join documentation, timeline and accuracy scenarios, lines 54–80 and 229–245](https://chronon.ai/authoring_features/Join.html)

Choose evidence by use case:

| Strategy | Strongest evidence | Main limit |
| --- | --- | --- |
| Exact inference logging | Reproduces what an existing model consumed | Does not create unlogged experimental features; logging can drop or bias |
| Shared online/offline computation | Recomputes known and new features with one definition | Correctness still depends on source history, clocks and execution mode |
| Hybrid | Logged baseline features plus point-in-time backfilled experiments | Must prove keys, timestamps and versions align across both sources |

Do not call exact logging and recomputation interchangeable. Compare them on overlapping traffic; disagreement is a diagnostic signal.

## Test parity as data, not as confidence

Sample predictions with immutable IDs and store:

- served feature vector or digest;
- feature-definition and source versions;
- prediction time and request context;
- offline-reconstructed vector;
- reason-coded differences: late data, correction, null/default, type/format, window edge, missing partition or code version.

Report mismatch per feature and important slice, not only one global percentage. A 0.1% global mismatch concentrated in high-value claims can be more dangerous than 5% mismatch in a discarded diagnostic field. Separate exact-value, tolerance-based numeric and semantic-category comparisons.

Treat the comparison as a release gate for feature-pipeline changes. X06’s model canary cannot rescue a training set that already contains future knowledge.

## Late data needs a declared policy

A watermark is an operational belief about how complete an event-time interval is. It is not proof that no older event will arrive.

Choose per feature:

- **as-served history:** late events affect future predictions only; historical rows preserve what was known;
- **best-current history:** historical analytics are corrected, but the result must not be used as prediction-time training data without availability filtering;
- **dual views:** retain both as-served and best-current representations with clear names and lineage.

Measure delay distributions by source and slice. A seven-minute cutoff that covers 99% globally may systematically exclude one region or partner. Record late-drop and correction rates; do not hide them inside null counts.

## Practice

All entities, timestamps, values and sample counts below are invented teaching inputs.

1. For the 10:00 prediction and E1–E3 table, compute the event-time-only sum and the as-known sum. Identify each excluded row and the violated predicate.
2. Reconstruct `risk_tier` for customer C7 at 10:00 and 12:00. Explain why overwriting the `low` row makes the 10:00 feature unrecoverable.
3. Add E0 with amount 10, event/availability time 09:00, and E-old with amount 100 at 08:59. For the half-open window `[09:00, 10:00)`, calculate the as-known sum and state what changes if the lower edge is exclusive.
4. In an invented parity sample of 1,000 predictions, 120 have language-format mismatch, 25 have count mismatch and 5 have both. Calculate the any-mismatch rate. Design a gate that cannot hide a critical-feature slice behind the global average.
5. Design training data for an insurance claim-triage model with mutable policy status, late repair invoices and a fraud label maturing after 30 days. Choose logging, recomputation or a hybrid; specify clocks, keys, windows, label maturity and parity evidence.

## Evidence and transfer questions

| Source | Inspected locator | Application boundary |
| --- | --- | --- |
| XR19 · Uber | [Taming the ML Firehose](https://www.uber.com/us/en/blog/taming-ml-firehose/), Problem, Solution, Scale Challenges, Online Architecture, High Throughput and Conclusion | Documents Uber’s observed skew, feature-logging decision, scale trade-offs and reported rollout results. It does not prove logging is complete, unbiased or affordable for another workload. |
| XR20 · Airbnb / Chronon | [Chronon engineering report](https://medium.com/airbnb-engineering/chronon-a-declarative-feature-engineering-framework-b7b8ce796e04), computation contexts/types and conclusion; [Chronon Join](https://chronon.ai/authoring_features/Join.html), timeline and accuracy scenarios | Documents a shared online/offline computation design, temporal versus snapshot semantics and Airbnb’s reported adoption/productivity. It does not make an arbitrary source bitemporal or guarantee a caller chose the right accuracy mode. |
| XR21 · Feast | [Point-in-time joins](https://github.com/feast-dev/feast/blob/master/docs/getting-started/concepts/point-in-time-joins.md), full page, especially “Retrieving features as of the event time” | Current implementation semantics distinguish event-time filtering from optional created-time filtering. Availability meaning and offline-store support remain deployment inputs. |

Before training a real model, obtain immutable prediction IDs, decision timestamps, source event and availability clocks, versioned feature definitions, correction/delete history, online TTL/default behavior, label windows, late-data distributions, logged-versus-recomputed parity by slice, and ownership for mismatches. No learner answer or mastery level is inferred from opening this lesson.

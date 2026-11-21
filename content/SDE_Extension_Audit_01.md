# Extension audit 01 — X01–X04

| Field | Result |
| --- | --- |
| Scope | X01–X04 lessons, worked companions, XR01–XR09 evidence boundaries, generated routes, search, links and navigation |
| Audit date | 21 November 2026 |
| Outcome | Passed. No lesson claim required correction; the roadmap and site navigation were advanced to the next evidence-backed batch. |
| Learner state | Not inspected or inferred. Browser progress remains learner-controlled. |

## What was checked

This audit asked four questions for every extension:

1. Does each important factual or historical claim stay within an inspected primary passage?
2. Are analytical assumptions and invented exercise inputs visibly separated from production evidence?
3. Does each practice item have a distinct worked response, and do executable examples reproduce the stated result?
4. Can a reader reach the lesson, companion, evidence record and roadmap through generated navigation and search?

The audit re-inspected the primary locators in the extension evidence register rather than treating a citation title as evidence. It then executed the Python examples in all four companions and rebuilt the static site from the saved Markdown.

## Findings by extension

| Extension | Primary-passage boundary | Companion and example check | Result |
| --- | --- | --- | --- |
| [X01 — Cache correctness](SDE_X01.md) | XR01 §3.2.1 supports lease tokens as protection against stale sets and thundering herds. XR02 §§4.2–4.4 and 6 support freshness, age, scope and invalidation for HTTP caches. The lesson labels its generation model, schedules and load arithmetic as original derivations rather than Facebook or HTTP guarantees. | Six practice items map to six worked sections. The schedule explorer executed ten legal schedules plus stale-fill, token, replica, reset, TTL and load fixtures. | Pass |
| [X02 — When does a retry prevent recovery?](SDE_X02.md) | XR03 supports retry amplification, token-bucket limiting and jitter from AWS production experience. XR04's “Retries” and “Queue Management” passages support aggregate retry limits, deadline propagation and the cost of queued work. The 100-attempt queue and 800 ms deadline cases are visibly invented deterministic models. | Four practice items map to four worked sections. Queue, retry multiplication, deadline and jitter calculations executed without error. | Pass |
| [X03 — Approximate membership](SDE_X03.md) | XR05 equations 16–17 and Table I support a one-sided probabilistic membership trade-off under analytical assumptions. XR06 §6 documents Bigtable using Bloom filters to avoid most unnecessary SSTable seeks. The lesson does not convert that qualitative outcome into a universal production percentage. | Five practice items map to five worked sections. Sizing, false-positive load, extra-memory value and stale-snapshot cases executed without error. | Pass |
| [X04 — Choosing the next experiment](SDE_X04.md) | XR07 §§1 and 6 ground entropy; XR08 definitions 1–2 ground expected information from experiments and its distinction from decision loss; XR09 §§3.1–3.2 documents GPT-4 small-run scaling predictions, observed successes and stated exceptions. Priors, likelihoods, costs and the incident are explicitly invented. | Five practice items map to five worked sections. Posterior, entropy, information-gain, decision-loss and cost-efficiency calculations executed without error. | Pass |

## Cross-module evidence boundary

The extensions use primary sources for mechanisms and documented decisions, then use separate, reproducible teaching models to expose the decision logic. The transfer boundary remains important:

- X01 does not claim a finite schedule explorer proves distributed cache correctness. A production design still needs evidence about invalidation delivery, replica authority, token durability and recovery.
- X02 does not supply a universal retry count or timeout. A deployment still needs arrival, service-time, deadline, retry and recovery distributions measured together under load.
- X03 does not make an approximate filter authoritative. A deployment still needs a versioned, complete snapshot, an authoritative fallback and measured CPU, memory, I/O and rebuild costs.
- X04 does not make subjective priors objective. A deployment still needs registered predictions, calibrated likelihoods, sensitivity checks and an action threshold fixed before observing the target result.

The worked examples establish reproducibility of the stated teaching models. They do not establish learner mastery or production suitability.

## Executed checks

| Check | Observed result |
| --- | --- |
| Practice-to-companion mapping | 20 practice items and 20 numbered worked sections; exact mapping in X01–X04 |
| Executable companion examples | Four Python blocks executed; all assertions passed |
| Markdown build | Completed from saved source |
| Internal routes and fragments | Every generated internal target resolved |
| Extension routes | Eight lesson/companion routes plus this audit and roadmap generated |
| Search catalogue | Lessons, companions, roadmap and audit indexed with distinct URLs |
| Navigation | Extensions remain in topic and study-path navigation; the reference page exposes this audit |

## Repairs made in this audit

No factual claim or worked result required repair. The audit did make continuity changes:

- recorded the audit as a durable reference artifact and exposed it in search and reference navigation;
- changed X01–X04 states from “not yet independently audited” to audited;
- replaced the completed audit placeholder with two concrete next extensions;
- updated the home page to distinguish a completed batch audit from a new lesson.

## Next batch chosen from concrete gaps

The first extension batch now covers read-side cache races, overload feedback, approximate negative knowledge and experiment selection. Two recurring production gaps remain before adding broader material:

1. **X05 — Safe data and schema migrations without split-brain truth.** Existing material explains authority and compatibility, but it does not walk through expand/migrate/contract, dual-write failure, backfill checkpoints, validation and rollback as one release decision. This is a high-value Cloud and data problem because a reversible application release can still leave irreversible or ambiguous state.
2. **X06 — AI release gates under distribution shift.** X04 chooses a discriminating experiment, but the library lacks an end-to-end release gate connecting offline slices, shadow traffic, canaries, online guardrails and rollback. This is a high-value AI production problem because aggregate offline improvement can hide population-specific regressions and delayed operational harm.

X05 and X06 form a balanced mini-batch: one protects durable state changes; the other protects model-behaviour changes. A second extension audit should follow them before further topics are added. Candidate ideas without a concrete missing decision, production mechanism and primary source are intentionally deferred.

## Unresolved evidence needed in practice

For X01–X04, a learner applying the mechanisms elsewhere would still need local traces, load distributions, cache/version telemetry, filter rebuild evidence, experiment calibration and decision thresholds. These are deployment inputs, not gaps to fill with generic prose. The next lessons must retain the same distinction between documented production evidence, analytical models and invented exercises.

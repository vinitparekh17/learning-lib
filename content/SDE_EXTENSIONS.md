# Extensions — Continue beyond the foundation

The original 24-module curriculum and four audits form a completed first edition. The website now continues with focused extensions authorized on 20 November 2026. New work should deepen a useful decision, connect to existing prerequisites and include inspected primary evidence, a concrete mechanism, counterexamples, separate worked practice and executed checks where appropriate.

## Available now

| Module | Capability | Prerequisites | State |
| --- | --- | --- | --- |
| [X01 — Cache correctness](SDE_X01.md) | Reject late fills and distinguish freshness, ordering and authority | F01, S02, S03 | Produced, checked and audited |
| [X01 worked companion](SDE_X01_answers.md) | Reconstruct failure histories, compare ten schedules and test boundary cases | Attempt X01 practice first | Produced, checked and mapping-audited |
| [X02 — When does a retry prevent recovery?](SDE_X02.md) | Budget recovery capacity and remaining time | S05, S06, C03 | Produced, checked and audited |
| [X02 worked companion](SDE_X02_answers.md) | Reproduce queue and deadline calculations | X02 practice | Produced, checked and mapping-audited |
| [X03 — Approximate membership and the price of forgetting](SDE_X03.md) | Price avoided negative work while preserving snapshot completeness | F01, F02, S02 | Produced, checked and audited |
| [X03 worked companion](SDE_X03_answers.md) | Reproduce sizing, load and stale-snapshot decisions | X03 practice | Produced, checked and mapping-audited |
| [X04 — Information gain and choosing the next experiment](SDE_X04.md) | Choose a discriminating measurement and price its decision value | F02, F03, B01 | Produced, checked and audited |
| [X04 worked companion](SDE_X04_answers.md) | Reproduce Bayesian updates, entropy and decision-loss checks | X04 practice | Produced, checked and mapping-audited |
| [Extension audit 01](SDE_Extension_Audit_01.md) | Recheck evidence boundaries, exercise mappings, examples and generated navigation | X01–X04 | Passed on 21 November 2026 |
| [X05 — Safe data migrations without split-brain truth](SDE_X05.md) | Preserve one authority through expand, backfill, cutover and contract | S02, S03, S04, C03 | Produced, checked and audited |
| [X05 worked companion](SDE_X05_answers.md) | Reproduce stale-backfill, capacity, compatibility and constraint decisions | X05 practice | Produced, checked and mapping-audited |
| [X06 — AI release gates under distribution shift](SDE_X06.md) | Join offline slices, shadow traffic, bounded exposure, delayed outcomes and rollback | F03, A01, A04, C05, X04 | Produced, checked and audited |
| [X06 worked companion](SDE_X06_answers.md) | Reproduce slice gates, disagreement strata, risk budget and delay calculations | X06 practice | Produced, checked and mapping-audited |
| [Extension audit 02](SDE_Extension_Audit_02.md) | Recheck X05–X06 evidence, example boundaries, mappings and generated navigation | X05–X06 | Passed on 23 November 2026 |

X01 adds a concrete application-cache mechanism beyond the original authority and retrieval discussions. It includes a step-through race explorer on its lesson page. Opening a lesson does not change your recorded mastery.

## Next questions worth investigating

These are proposed work items, not completed lessons or a claim that sources have already been verified.

| Order | Proposed extension | Why it compounds | Entry points |
| --- | --- | --- | --- |
| Next | X07 — Backups are not recovery | Prove restore chains, dependency order, RPO/RTO and reconciliation under corruption or regional loss | S02, S04, S06, X05 |
| Then | X08 — Point-in-time feature correctness | Prevent future leakage and online/offline skew across late, mutable feature data | F03, A01, A04, X06 |
| Review | Extension audit 03 | Recheck X07–X08 evidence boundaries, examples and navigation before selecting more work | X07–X08 |

## How continued work is maintained

The website source repository is the working record for these additions. Existing first-edition exports and Library documents remain historical snapshots; this extension does not claim to update those downloads. Published lessons appear in search, topic browsing, study paths and progress tracking. Progress continues to be saved in your browser.

Keep the original R01–R24 identities stable. New extension sources use XR identifiers, with passage locators recorded below and in the relevant lesson. A future update should read this roadmap, inspect the repository's actual state, finish one substantial item, validate it and publish to the same private site. Reconcile an existing partial lesson before creating another.

## Extension evidence register

| ID | Primary source and inspected passages | Use and limits |
| --- | --- | --- |
| XR01 | [Nishtala et al., Scaling Memcache at Facebook, NSDI 2013](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf), §3.2.1, printed p.388; inspected 2026-11-20 | Historical lease-token mechanism; no current default or throughput prediction |
| XR02 | [RFC 9111, HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html), §§4.2–4.2.3, 4.4 and 6; inspected 2026-11-20 | HTTP freshness/age and scope; application-cache example remains an original model |
| XR03 | [Marc Brooker, “Timeouts, retries, and backoff with jitter,” AWS Builders' Library](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), “Retries and backoff” and final five paragraphs of “Jitter”; inspected 2026-11-20 | Production experience with burst timing and retry guidance; X02 queue and deadline values are invented |
| XR04 | [Mike Ulrich, “Addressing Cascading Failures,” Google SRE](https://sre.google/sre-book/addressing-cascading-failures/), “Retries” and “Queue Management”; inspected 2026-11-20 | Retry feedback, aggregate limits and waiting costs; no universal retry budget |
| XR05 | [Burton H. Bloom, “Space/Time Trade-offs in Hash Coding with Allowable Errors,” CACM 13(7), 1970](https://courses.cs.washington.edu/courses/csep521/21wi/readings/bloom_cacm.pdf), printed pp. 422–423 and 425–426, equations 16–17 and Table I; inspected 2026-11-20 | Original one-sided membership model and analytical trade-off; deployment freshness is outside scope |
| XR06 | [Chang et al., “Bigtable: A Distributed Storage System for Structured Data,” OSDI 2006](https://research.google.com/archive/bigtable-osdi06.pdf), §6 “Bloom filters,” proceedings p. 211 / PDF printed p. 7; inspected 2026-11-20 | Deployed SSTable decision and qualitative disk-seek outcome; no universal percentage or sizing rule |
| XR07 | [Claude E. Shannon, “A Mathematical Theory of Communication,” Bell System Technical Journal 27, 1948](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf), part I, §§1 and 6; inspected 2026-11-21 | Entropy of a probability distribution; engineering hypothesis likelihoods remain model inputs |
| XR08 | [D. V. Lindley, “On a Measure of the Information Provided by an Experiment,” Annals of Mathematical Statistics 27(4), 1956](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-27/issue-4/On-a-Measure-of-the-Information-Provided-by-an-Experiment/10.1214/aoms/1177728069.full), pp. 986–990, definitions 1–2; inspected 2026-11-21 | Prior-to-posterior expected information and experimental-design framing; distinct from a specified loss function |
| XR09 | [OpenAI, GPT‑4 Technical Report, 2023](https://cdn.openai.com/papers/gpt-4.pdf), §3, §§3.1–3.2 and figures 1–3; inspected 2026-11-21 | Small-run scaling evidence, registered predictions, observed success and exceptions; no claim that every capability scales predictably |
| XR10 | [Jacqueline Xu, Stripe, “Online migrations at scale”](https://stripe.com/blog/online-migrations), “Why are migrations hard?”, “A pattern for online migrations,” parts 1–4 and Conclusion; inspected 2026-11-22 | Production migration of hundreds of millions of live Subscription objects, staged decision and reported no-downtime outcome; no claim that dual writes are atomic |
| XR11 | [PostgreSQL 19 documentation, `ALTER TABLE`](https://www.postgresql.org/docs/current/sql-altertable.html), `ADD table_constraint [ NOT VALID ]`, `VALIDATE CONSTRAINT`, Notes and examples; inspected 2026-11-22 | Current PostgreSQL constraint enforcement/validation and lock boundary; exact behavior remains version- and operation-specific |
| XR12 | [Shlomi Noach, GitHub, “gh-ost”](https://github.blog/news-insights/company-news/gh-ost-github-s-online-migration-tool-for-mysql/), existing landscape, trigger limitations, Pauseable, operation modes and “gh-ost at GitHub”; inspected 2026-11-22 | GitHub's production MySQL constraint, triggerless/binlog choice and adoption; not a universal migration tool recommendation |
| XR13 | [Breck et al., “The ML Test Score,” IEEE Big Data 2017](https://research.google.com/pubs/archive/aad9f93b86b7addfea4c419b9100c6cdd26cacea.pdf), Model 6, Infra 4 and 6–7, Monitor 2–7; inspected 2026-11-22 | Production-readiness tests from experience and interviews across real ML systems; no universal metrics or release thresholds |
| XR14 | [Wang, Wang and Li, Uber, “Raising the Bar on ML Model Deployment Safety”](https://www.uber.com/sa/en/blog/raising-the-bar-on-ml-model-deployment-safety/), Introduction, safe deployment practices, Built for Adoption, Data Quality at Scale and Continuous Validation; inspected 2026-11-22 | Uber's 2025 scale, safeguards, adoption and reported detection improvement; transfer requires a local loss model and platform evidence |
| XR15 | [Rabanser, Günnemann and Lipton, “Failing Loudly,” NeurIPS 2019](https://proceedings.neurips.cc/paper/2019/file/846c260d715e5b854ffad5f70a516c88-Paper.pdf), Abstract, §3.1 and §5; inspected 2026-11-22 | Empirical shift-detector comparison and documented representation/sample boundaries; not a universal detector or quality guarantee |

## Change record

23 November 2026 · Completed [Extension audit 02](SDE_Extension_Audit_02.md). Re-inspected XR10–XR15 boundaries, verified 10 practice-to-answer mappings, executed both companion checks and checked generated routes, fragments, search and navigation. No lesson claim required correction. Selected X07 and X08 only for the concrete disaster-restore and point-in-time feature gaps recorded in the audit; audit 03 follows that mini-batch.

22 November 2026 · Added X06 and five worked AI release decisions. XR13 grounds slice, canary, rollback and continuous-monitoring controls; XR14 documents Uber's platform decision and reported operational outcomes; XR15 bounds what distribution-shift detection establishes. Executed aggregate/slice, shadow-stratum, exposure-budget and delayed-label checks. Extension audit 02 is next.

22 November 2026 · Added X05 and five worked migration decisions. XR10 documents Stripe's online Subscription migration; XR11 bounds PostgreSQL constraint enforcement and validation; XR12 documents GitHub's lock-related migration problems and pauseable binlog-driven response. Executed stale-backfill, conflict, capacity and compatibility checks. X06 is next, followed by extension audit 02.

21 November 2026 · Completed [Extension audit 01](SDE_Extension_Audit_01.md). Re-inspected XR01–XR09 boundaries, verified 20 practice-to-answer mappings, executed all four companion Python checks and checked generated routes, fragments, search and navigation. No lesson claim required correction. Selected X05 and X06 only for the concrete mutation-safety and AI-release gaps recorded in the audit; audit 02 follows that mini-batch.

21 November 2026 · Added X04 and five worked analyses. XR07–XR08 ground entropy and expected information; XR09 documents GPT‑4 small-run scaling predictions, their compute gap and reported exceptions. Checked all posterior, information-gain, decision-loss and cost-efficiency calculations. The X01–X04 extension audit is next.

20 November 2026 · Added X03 and five worked analyses. XR05 is Bloom's original one-sided membership construction and trade-off; XR06 is Google's Bigtable account of using filters to avoid SSTable disk seeks. Checked the sizing, expected-load, incremental-memory and version-mismatch examples. X04 is next.

20 November 2026 · Added X02 and four worked analyses. XR03 is Marc Brooker’s AWS Builders’ Library account of burst timing on EBS and Lambda. XR04 is Google SRE chapter 22 on retry feedback. The lesson records passage locators. Checked the synthetic queue, deadline and attempt calculations. X03 is next.

20 November 2026: X01 and its six worked analyses added, with an interactive comparison of unguarded and guarded cache fills. Executed ten legal schedules plus negative-premise fixtures, TTL boundary checks and exact load arithmetic. Original 24 modules retained. Real cache recovery, invalidation delivery and replica lag remain implementation questions; learner mastery is unknown. Next substantial item: X02.

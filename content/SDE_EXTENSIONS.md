# Extensions — Continue beyond the foundation

The original 24-module curriculum and four audits form a completed first edition. The website now continues with focused extensions authorized on 20 November 2026. New work should deepen a useful decision, connect to existing prerequisites and include inspected primary evidence, a concrete mechanism, counterexamples, separate worked practice and executed checks where appropriate.

## Available now

| Module | Capability | Prerequisites | State |
| --- | --- | --- | --- |
| [X01 — Cache correctness](SDE_X01.md) | Reject late fills and distinguish freshness, ordering and authority | F01, S02, S03 | Produced and checked; not yet independently audited |
| [X01 worked companion](SDE_X01_answers.md) | Reconstruct failure histories, compare ten schedules and test boundary cases | Attempt X01 practice first | Produced and checked |
| [X02 — When does a retry prevent recovery?](SDE_X02.md) | Budget recovery capacity and remaining time | S05, S06, C03 | Produced and checked |
| [X02 worked companion](SDE_X02_answers.md) | Reproduce queue and deadline calculations | X02 practice | Produced and checked |
| [X03 — Approximate membership and the price of forgetting](SDE_X03.md) | Price avoided negative work while preserving snapshot completeness | F01, F02, S02 | Produced and checked |
| [X03 worked companion](SDE_X03_answers.md) | Reproduce sizing, load and stale-snapshot decisions | X03 practice | Produced and checked |
| [X04 — Information gain and choosing the next experiment](SDE_X04.md) | Choose a discriminating measurement and price its decision value | F02, F03, B01 | Produced and checked |
| [X04 worked companion](SDE_X04_answers.md) | Reproduce Bayesian updates, entropy and decision-loss checks | X04 practice | Produced and checked |

X01 adds a concrete application-cache mechanism beyond the original authority and retrieval discussions. It includes a step-through race explorer on its lesson page. Opening a lesson does not change your recorded mastery.

## Next questions worth investigating

These are proposed work items, not completed lessons or a claim that sources have already been verified.

| Order | Proposed extension | Why it compounds | Entry points |
| --- | --- | --- | --- |
| Next | Extension audit | Recheck X01–X04 claims, companion mappings, source boundaries and site navigation | Completed extensions |

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

## Change record

21 November 2026 · Added X04 and five worked analyses. XR07–XR08 ground entropy and expected information; XR09 documents GPT‑4 small-run scaling predictions, their compute gap and reported exceptions. Checked all posterior, information-gain, decision-loss and cost-efficiency calculations. The X01–X04 extension audit is next.

20 November 2026 · Added X03 and five worked analyses. XR05 is Bloom's original one-sided membership construction and trade-off; XR06 is Google's Bigtable account of using filters to avoid SSTable disk seeks. Checked the sizing, expected-load, incremental-memory and version-mismatch examples. X04 is next.

20 November 2026 · Added X02 and four worked analyses. XR03 is Marc Brooker’s AWS Builders’ Library account of burst timing on EBS and Lambda. XR04 is Google SRE chapter 22 on retry feedback. The lesson records passage locators. Checked the synthetic queue, deadline and attempt calculations. X03 is next.

20 November 2026: X01 and its six worked analyses added, with an interactive comparison of unguarded and guarded cache fills. Executed ten legal schedules plus negative-premise fixtures, TTL boundary checks and exact load arithmetic. Original 24 modules retained. Real cache recovery, invalidation delivery and replica lag remain implementation questions; learner mastery is unknown. Next substantial item: X02.

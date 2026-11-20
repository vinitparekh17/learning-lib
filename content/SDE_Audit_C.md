# Audit C — AI evidence, mathematics and customer outcomes

| Field | Value |
| --- | --- |
| ID / revision / date | Audit C · 1.0 · 2026-11-12 |
| Scope | A01–A05 and C02, with their six companions; F04 and its answers as mathematical prerequisite |
| Authority | SDE_Foundations_Scheduled_Prompt.md; SDE_Foundations_Library_v1.md, run 22 |
| Capability | Distinguish a checked mechanism and conditional decision from empirical deployment evidence |
| Evidence status | Primary passages reopened; original calculations and counterexamples reviewed |
| Experiment status | Seven embedded Python scripts executed successfully; no model, GPU, customer or live-authority experiment |
| Result | No consequential error found in the reviewed scope; no lesson replacement required |

## Decision and scope

Advance to B02 after saving this report and the source update. A01–A05 and C02 meet the reviewed curriculum requirements: deployment-aligned evaluation; explicit attention arithmetic; retrieval failure isolation; stated memory/scheduling assumptions; bounded control and evaluation; and a decision revised after one constraint changes. This is an artifact audit, not a learner assessment or a proof that every statement is error-free.

The latest index identified Audit C as the next unfinished item. Both exact-name and shorter-title searches found no existing audit artifact to reconcile. All reviewed files were freshly retrieved. Earlier lessons were retained rather than regenerated. F04 was checked as a prerequisite; this report does not reopen all earlier audits or certify their deployment assumptions.

## Findings and disposition

| Risk examined | Evidence and conclusion | Correction / affected artifacts | Remaining uncertainty |
| --- | --- | --- | --- |
| A01: an unseen row mistaken for an independent case | Revision lookup gives zero error on known documents and MSE 17 on unseen documents; shared organization/template links make the requested doubly disjoint split infeasible | No correction; A01 and answers retain their explicit information-boundary caveats | Actual group structure, label timing and sampling |
| A02: normalized weights mistaken for truth or a causal mask mistaken for end-to-end protection | Mask-before-softmax calculation and future-value perturbation agree with the source operation; earlier contaminated representations remain a counterexample | No correction; A02 and answers | Whole-model architecture, precision and upstream information flow |
| A03: citation resolution confused with support or permission | Five stage failures remain distinguishable; two marginalization expressions have different valid results; current-head and disclosure-permission clocks are separate | No correction; A03 and answers | Hand-assigned facts are not a semantic verifier; concurrent disclosure is unimplemented |
| A04: memory capacity or finite-trace throughput promoted to useful serving capacity | KV units, per-request rounding and next-block growth are consistent; changing deadline from 50 to 40 ms reverses timely-completion ranking | No correction; A04 and answers | Hardware, workload distribution, workspace reserve and sharing implementation |
| A05: refusals counted as drafts; repeated trials counted as independent documents | Contract success and draft coverage use different denominators; blocked approval attempts remain visible; oracle best-of-three is explicitly distinct from an evaluated selector | No correction; A05 and answers | Cancellation, actual grants, semantic judges and live behavior |
| C02: improved component score promoted to customer benefit | Fixed-output deadline extension changes the constrained decision from A to B; A still minimizes cost per success; budget and value thresholds are separate | No correction; C02 and answers | Buyer objectives, actual costs, independent teams, demand and causal effects |
| Source-access limitation during audit | Web reader rejected the large R02 PDF and raw notebook URL; direct retrieval from the authors' sites succeeded | Access repaired for this run; source record updated | No essential access blocker; not every historical source was re-audited |

No issue was manufactured to justify a revision. The existing lesson text already states the material boundaries above. The only changes in this run are this audit record, the source record and progress index.

## Derivations and execution record

Each script was extracted from its saved answer file and run with Python. All seven exited successfully. Re-running an author's fixture is a reproducibility check, not independent empirical validation. Algebra and the counterexamples were also compared with the prose and assignments.

| Pack | Checked result and boundary cases | Assignment mapping |
| --- | --- | ---: |
| F04 | Loss derivative 5(w−2), error multiplier 1−5η, strict descent interval 0<η<0.4 away from optimum; ranking, coordinate order, zero-vector policy and held-out loss increase | 6 prerequisite pairs |
| A01 | Penalized optimum 10/(5+2λ); validation/final losses; 25 final-label perturbations; 14 nonempty document partitions; mixture crossover 5/8 | 6 pairs |
| A02 | Projection shapes, analytic attention, causal/connection masks, value perturbation, all six permutations, stable softmax, invalid dimensions/all-masked rows and rectangular scaling | 6 pairs |
| A03 | Revision-time boundaries, eligibility, five failure fixtures, 24 passage orderings, cross-tenant score changes; sequence 0.312 versus token 0.3696; nested stage product 7/20 | 6 pairs |
| A04 | 128 KiB per token; 65,536-position pool; 64 capacity boundaries; 4,096 block/length combinations; full-pool growth; schedules and zero-success cost handling | 6 pairs |
| A05 | W/M/L success 4/6,3/6,4/6; draft coverage 2/4 each; 480 sequential admission cases; budget/revocation cases; repeated trials and judge confusion counts | 6 pairs |
| C02 | Exhaustive outcome partitions; paired gains/regressions; monotone deadline sets; conditional choices; 201 labor-value points and exact budget/value boundaries | 5 pairs |

The target audit covers 35 assignment–answer pairs; the prerequisite review adds six, for 41 reviewed mappings. Hints, worked solutions and assessment criteria are present. Companion links resolve to the matching materialized filenames. Markdown fences are balanced and placeholder scans found no TODO/TBD/FIXME text. Source IDs and paper versions remain consistent with the source register. Local companion-link checks are not a crawl of every external URL; the source links below were opened for the stated passages.

A few explicit independent arithmetic cross-checks clarify why the results matter. A04's 16 requests at 4,096 positions fill the KV pool exactly; one 16-slot block costs 2 MiB, so memory feasibility at the current step does not reserve growth. C02's day-two cost difference is 50 for four additional successes, giving value threshold 12.5; its labor-rate cost crossover r=1 lies beyond both options' feasible budget ranges. A03's stage fractions telescope because their populations nest, not because stages are independent.

## Primary passage audit trail

These are focused passage checks, not claims that entire books or all benchmark experiments were reproduced. Publication year remains distinct from the inspected version date.

| Source | Reopened locator and URL | Audit use |
| --- | --- | --- |
| R02, author draft 2024-01-15 | [Mathematics for Machine Learning](https://mml-book.github.io/book/mml-book.pdf), §§8.2.1–8.2.2, printed pp. 259–261, eqs. 8.6–8.10 | Empirical loss versus expected risk of a fixed predictor; A01's derivation is original |
| R13, author Python labs | [Chapter 5](https://github.com/intro-stat-learning/ISLP_labs/blob/stable/Ch05-resample-lab.ipynb), The Validation Set Approach; [Chapter 6](https://github.com/intro-stat-learning/ISLP_labs/blob/stable/Ch06-varselect-lab.ipynb), Choosing Among Models Using the Validation Set Approach and Cross-Validation; Evaluating Test Error of Cross-Validated Ridge | Training-only fit and separation of tuning from outer evaluation; author experiments not rerun |
| R14, arXiv v7 | [Attention paper](https://arxiv.org/html/1706.03762v7), §§3.2.1–3.2.3, equation 1 | Scaling, projection/mixing and illegal connections masked before softmax |
| R15, arXiv v4 | [RAG paper](https://arxiv.org/pdf/2005.11401v4), §§2.1–2.4 pp. 3–4, §3 opening p. 4 | Passage marginalization and fixed document encoder/index during fine-tuning; no private-document benchmark extrapolation |
| R16, arXiv v1 | [PagedAttention paper](https://arxiv.org/pdf/2309.06180v1), §§4.1–4.2 p. 5 | Fixed-token blocks and logical/physical mapping; no modern implementation or speedup forecast |
| R18, arXiv v3 | [ReAct paper](https://arxiv.org/pdf/2210.03629v3), §§3.1–3.2 pp. 4–5 | Search/lookup/finish and action–observation mechanism; not evidence of production authorization |
| R17, 2015 | [Technical-debt paper](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf), §2 Undeclared Consumers pp. 2–3 and §3 p. 3 | Dependency and consumer boundaries; invoice cases remain applications |
| R11, 1975 | [Basic Principles](https://web.mit.edu/saltzer/www/publications/protection/Basic.html), §I.A.3 c | Complete mediation and remembered authorization decisions |
| R03, 2020-07-31 | [Microsoft Research](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/), hypothesis/metrics, randomization unit, counterfactual logging and engineering-bias sections | Design guidance for comparable populations and interference; no study conducted here |
| R19, 2019-09-04 | [YC transcript](https://www.ycombinator.com/blog/startup-school-week-1-recap-kevin-hale-and-eric-migicovsky/), 20:20–24:10 | Recent episodes and existing alternatives; not demand evidence |

The author notebook is evidence for its specified learning/evaluation examples, not blanket approval to copy every preprocessing arrangement into a nested procedure. A01's requirement to fit transformations inside the relevant training fold remains the governing design rule. This audit did not rerun book datasets, paper benchmarks or a deployed model.

## Handoff

No blocking issue remains in the reviewed scope. Real performance, corpus completeness, evaluator reliability, authorization ordering, traffic, hardware, costs and customer adoption remain application inputs. No learner answers or mastery were inferred.

Next: **Run 23 — B02, unit economics and the cost of useful outcomes**, using F02, B01 and A05 and the cost-denominator boundaries from A04/C02. Keep hypothetical charges distinct from prices and cash savings. The program remains in progress; final packaging and completion are not due.

## Revision history

- 1.0 — 2026-11-12. Focused primary-passage audit, seven successful scripts and 41 exercise mappings; no consequential lesson correction required.

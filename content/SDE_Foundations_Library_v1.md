# SDE Foundations Library — v1

**Prepared for Vinit · 1 November 2026**

**Purpose:** Develop the ability to reason about, design, evaluate, and economically justify reliable software and AI systems. Build transferable engineering judgment that survives changes in languages, frameworks, vendors, and models.

**What this edition contains:** a curated source catalog, 18 connected module briefs, six synthesis assignments, a worked example, a finite 30-run production plan, and reusable production/audit prompts. It is the foundation and specification for the deeper library; the 18 full learning packs have not yet been generated. Original papers remain at their linked sources; this file is not an offline collection of those papers.

**Evidence status:** Source pages were opened on 1 November 2026. The catalog distinguishes full-text access, abstract access, and course/book indexes. Those statuses establish source identity and relevance, not an exhaustive technical audit of each work. Read the actual supporting passage before citing a paper's detailed result. Pedagogical choices, sequencing, exercises, and workload sizes below are recommendations, not empirically optimal prescriptions.

## 1. The organizing question

> How do I turn an uncertain customer problem into a system whose behavior, reliability, and economics I can defend?

This question creates a useful intersection of software engineering, cloud, AI, and business. It allows breadth while requiring the same ideas to recur.

The desired capabilities are to:

- Formulate a problem, define an invariant, and reason from a baseline to a better solution.
- Predict important resource and failure constraints before selecting a technology.
- Separate measurements from assumptions, and evidence from plausible explanations.
- Read a paper and identify its mechanism, experimental scope, and limitations.
- Evaluate an AI system at the level of the complete customer task.
- Explain how architecture changes cost, risk, maintenance, and the offer a customer buys.
- Write a clear decision memo, including what evidence would reverse the recommendation.

Framework fluency still matters when building and debugging a real system. In this library, implementation is a way to test a principle. It does not define the curriculum.

## 2. Four connected areas

| Area | Core question | Modules | Tangible evidence of progress |
| --- | --- | --- | --- |
| Reasoning and mathematical models | What follows from the assumptions, and how would I find out whether they hold? | F01–F04 | Proof sketches, counterexamples, estimates, experiment designs |
| Systems and cloud | What state exists, where can it fail, and which resource limits the design? | S01–S06 | Execution traces, failure models, capacity estimates, isolation boundaries |
| AI systems | What does the model learn, what can the surrounding system guarantee, and how is quality measured? | A01–A05 | Evaluation sets, baseline comparisons, retrieval diagnoses, serving estimates |
| Product and business judgment | Who benefits, what will they change, and can the economics support delivery? | B01–B03 | Customer evidence plans, unit models, pricing hypotheses, distribution choices |

The business area is intentionally smaller. Its role is to shape engineering decisions, not to start a second general MBA curriculum.

### Repeated concepts that make the areas compound

| Concept | First use | Later reuse |
| --- | --- | --- |
| Invariants and contracts | Algorithm correctness | Transactions, replicated logs, agent permissions, billing rules |
| State and information | Data structures and representations | Caches, indexes, model parameters, external knowledge, audit trails |
| Uncertainty and expected loss | Probability | Evaluation, incident diagnosis, customer research, economic sensitivity |
| Scarce resources | Time and memory | Queues, network bandwidth, GPU memory, engineer time, support effort |
| Measurement and feedback | Experiments | Model selection, deployment, product adoption, pricing changes |
| Boundaries and incentives | Abstraction and ownership | Security, organizational handoffs, supplier dependence, customer switching |

Each new pack should name an earlier concept it reuses and a later decision it enables. A source earns its place through that connection, not through fame alone.

## 3. Scope and depth controls

Use one recurring fictional case: a business service that receives documents, extracts evidence, proposes an action, and requires approval for consequential changes. The case is only a study vehicle. It is not a product recommendation, a commitment to document AI, or evidence of market demand. Use other examples to test transfer.

### Three depths

1. **Core:** Understand the mechanism; reproduce a small example; explain one failure condition.
2. **Application:** Apply it under changed constraints and defend a decision.
3. **Research extension:** Read a difficult proof, reproduce a published experiment, or compare recent methods when a real question justifies it.

Complete Core and Application before collecting additional papers on the same subject. A historical paper teaches a mechanism or argument; it does not establish the best current implementation.

### Defer from the first collection

Vendor certification paths, framework surveys, daily AI news, broad lists of tools, exhaustive distributed-system algorithms, training a frontier model, unrelated scientific fields, general investing, and startup biographies. Add one only when it resolves a concrete gap in an existing module.

### Prerequisite bridge

Do not infer mathematical readiness from years of employment. Begin with a small diagnostic:

- Given a duplicate-detection loop, state its invariant and count its work.
- Calculate a conditional probability from a small contingency table.
- Multiply a small matrix by a vector and explain the shape of the result.
- Explain why a benchmark with more successes can still be a worse comparison.

Use the result to generate short bridges in logic, algebra, probability, and derivatives. These are preparation, not a pass/fail judgment about engineering ability. The MIT algorithms course explicitly lists discrete mathematics as a prerequisite [R01]. The mathematical reference is a shelf of selected chapters, not a cover-to-cover assignment [R02].

## 4. Module briefs

The questions and exercises below are original curriculum designs. Source labels point to the catalog in section 5. Each exercise includes a criterion for a useful answer; the later learning pack should supply a separate worked solution.

### F01 — Invariants, algorithms, and the cost of computation

**Question:** How do I improve a brute-force solution while preserving its correctness?

**Starting scope:** One problem, a correct baseline, repeated work, a useful representation, and an invariant. Introduce asymptotic analysis alongside the specific operation being counted. Add hashing or a monotonic two-pointer example only after deriving why the operation is safe.

**Sources:** R01, beginning with algorithms/computation, data structures, and hashing. Return to dynamic programming later rather than treating every pattern as required first reading.

**Exercise:** Solve duplicate detection by pairwise comparison, then with remembered state. Give a loop invariant. Explain the assumptions behind the time and memory claims. Change the task to bounded memory or a stream.

**Exit criterion:** Derive the improvement, identify what information must be retained, and give a case where a stated performance assumption fails.

**Connections:** S02 indexes, S04 safety properties, A03 retrieval representations. **Prerequisites:** basic loops; a bridge in sets and induction if needed.

### F02 — Probability, base rates, and decisions under uncertainty

**Question:** When should a system act, abstain, or ask a person?

**Starting scope:** Conditional probability, expected value, base rates, and unequal error costs. Use small count tables before symbolic notation. Distinguish a probability estimate from a calibrated estimate and from a decision threshold.

**Source:** R02, probability and distributions. Use R13 for later connections to classification.

**Exercise:** Construct two populations with different event prevalence. Apply the same detector characteristics to both. Compare the proportion of alerts that are correct. Then change the cost of a missed event versus an unnecessary intervention.

**Exit criterion:** Explain why the action rule can change without changing the detector, and list the assumptions that would make the calculation misleading.

**Connections:** F03 experiment interpretation, A05 evaluation, B02 expected cost. **Prerequisites:** fractions and elementary algebra.

### F03 — Measurement, experiment design, and evidence quality

**Question:** Did the change improve the system, or did the measurement change?

**Starting scope:** Sampling, distributions, uncertainty, confounding, randomization, and metric definitions. Keep a performance benchmark distinct from a causal product experiment. Record workload and population boundaries.

**Sources:** R03 for experiment design checks; R13 for resampling and model assessment.

**Exercise:** Design a comparison between two document-processing pipelines. Specify the experimental unit, dataset, outcomes, important subgroups, cost metric, exclusions, and a stopping/analysis plan before observing results. Explain when randomizing individual requests would be inappropriate.

**Exit criterion:** Identify plausible leakage, selection bias, or interference, and explain what the experiment can and cannot conclude.

**Connections:** S05 latency measurement, A01 generalization, A05 evaluations, B01 demand evidence. **Prerequisites:** F02.

### F04 — Vectors, transformations, and optimization

**Question:** What computation sits underneath embeddings and learning?

**Starting scope:** Vectors, dot products, norms, matrix shapes, derivatives, and a small gradient update. This is a bridge to later AI mechanisms, not a survey of all linear algebra.

**Source:** R02, selected material from linear algebra, analytic geometry, vector calculus, and continuous optimization.

**Exercise:** Compute similarity for a few small vectors; show how normalization changes the comparison. Fit a one-parameter linear model using a tiny dataset and calculate a gradient step by hand.

**Exit criterion:** Track dimensions, explain what the loss measures, and describe why lowering training loss alone does not establish usefulness on new inputs.

**Connections:** A01 learning, A02 attention, A03 retrieval. **Prerequisites:** algebra and a short derivative bridge; F02 for probabilistic interpretation.

### S01 — Resource models, locality, and abstraction costs

**Question:** Why can two implementations of the same algorithm have very different costs?

**Starting scope:** CPU work, data movement, working sets, memory representation, virtualization, and locality. Separate an abstract cost model from an implementation measurement. Never transfer an unsourced latency table between machines.

**Source:** R04, selected CPU scheduling, address-space, paging, and translation material. The later GPU connection is supplied by R16.

**Exercise:** Compare contiguous scanning, pointer traversal, and batched work. Predict the dominant resource for a stated workload, then specify a benchmark that could disprove the prediction.

**Exit criterion:** State machine/workload assumptions and distinguish algorithmic complexity, wall-clock time, and throughput.

**Connections:** S02 storage, S05 capacity, A04 inference. **Prerequisites:** F01.

### S02 — Data organization, indexes, and recovery

**Question:** What must be stored so reads are useful and acknowledged changes survive the stated failures?

**Starting scope:** Logical data versus physical layout, access paths, write cost, and recovery records. Study a small index and a small recovery trace. Relational reasoning is a durable model, not allegiance to a database product.

**Sources:** R05, storage, indexes/filters, logging, and recovery; R04 persistence as a bridge.

**Exercise:** Design storage for facts extracted from documents, preserving source identity and revisions. List two important queries and estimate which records each access path touches. Trace a crash between successive writes.

**Exit criterion:** Explain the read/write/storage trade-off and identify what the acknowledgement actually promises.

**Connections:** S03 transactions, S04 replication, A03 evidence provenance. **Prerequisites:** F01, S01.

### S03 — Concurrency, transactions, and logical time

**Question:** Which interleavings can violate the application's invariant?

**Starting scope:** Shared state, histories, concurrency control, and causal ordering. Keep transaction isolation, wall-clock order, and logical time as distinct concepts.

**Sources:** R05 concurrency-control theory and selected mechanisms; R06 for event ordering.

**Exercise:** Draw two concurrent attempts to consume the same limited resource. Produce one violating history, then explain which constraint or protocol excludes it. Add a delayed message from another process.

**Exit criterion:** Show the history explicitly and explain what is guaranteed across the boundary of each mechanism.

**Connections:** S04 consensus, S06 permission changes, A05 tool side effects. **Prerequisites:** F01, S02.

### S04 — Replication, consensus, and partial failure

**Question:** What can a group of machines safely agree on when some communication fails?

**Starting scope:** Replicated state machines, logs, leader election, safety versus liveness, and the declared failure model. Use Raft as one worked design. Avoid treating it as a universal answer to all consistency problems.

**Sources:** R07, sections 2 and 5 and the state/transition summary; R06 as prerequisite context. R10 helps separate transport behavior from application guarantees.

**Exercise:** Trace a leader failure during an update and a later retry from a client. Identify the distinct questions of log commitment, client knowledge, and duplicate business effects.

**Exit criterion:** State a safety property, show why a naive alternative violates it, and identify a failure outside the model.

**Connections:** S06 reliability, A05 workflows, B02 reliability expense. **Prerequisites:** S03.

### S05 — Queues, tail latency, and cloud elasticity

**Question:** What happens when demand varies and work waits for a scarce resource?

**Starting scope:** Arrival/service rates, concurrency, latency distributions, admission control, and provisioning. Connect workload shape to the decision to reserve, share, or elastically obtain capacity.

**Sources:** R08 for latency tails; R09 handling overload; R12 for the original cloud economics argument. Read R12 as a historical model, not a current price guide.

**Exercise:** Specify a bursty workload and a service-time distribution. Draw what happens to waiting work when offered load exceeds processing capacity. Compare rejecting, queueing, batching, and adding capacity under the same objective.

**Exit criterion:** Explain why an average alone is insufficient; define the population and percentile; identify a constraint autoscaling cannot remove instantly.

**Connections:** A04 serving, B02 unit economics, B03 offer design. **Prerequisites:** F02, F03, S01.

### S06 — Reliability, isolation, and authority boundaries

**Question:** What limits damage when a component fails, lies, or acts with too much authority?

**Starting scope:** Service objectives, error budgets, observability, isolation, least privilege, and complete mediation. Keep an availability failure distinct from an authorization failure.

**Sources:** R09 embracing risk and service-level objectives; R11 introductory protection principles; R10 for function placement.

**Exercise:** For the recurring case, draw principals, data boundaries, and permitted actions. Identify which checks belong outside the language model. Define an observable service objective and an explicit trade-off between additional safeguards and operating cost.

**Exit criterion:** Identify a failure that retries cannot fix, and explain what remains true if the model proposes an unauthorized action.

**Connections:** A05 agents, B02 cost of failures, B03 customer trust. **Prerequisites:** S03–S05.

### A01 — Learning, generalization, and distribution change

**Question:** What does evidence on past examples justify about future examples?

**Starting scope:** Objectives, baselines, fitting, validation, overfitting, leakage, and distribution change. Begin with a small conventional predictor before reasoning about a language model.

**Source:** R13, statistical learning, resampling, and regularization; R02 as mathematical support.

**Exercise:** Design a split for documents with repeated organizations, templates, and revisions. Compare it with a random row split. Specify a simple baseline and explain what each comparison would establish.

**Exit criterion:** Explain a high-scoring but invalid evaluation and describe an alternative that matches the intended deployment.

**Connections:** F03 evidence, A03 retrieval, A05 monitoring. **Prerequisites:** F02–F04.

### A02 — Attention and the Transformer mechanism

**Question:** How does a representation of one token incorporate information from other tokens?

**Starting scope:** Queries, keys, values, shapes, attention weights, masking, and the distinction between training and inference. Trace one small operation before studying a full architecture.

**Source:** R14. The original architecture and experiments are historical; do not infer that every current model has all of its design choices.

**Exercise:** Calculate a tiny attention operation with explicit matrices. Change a mask and identify which outputs may change. Describe where sequence length enters the chosen computation.

**Exit criterion:** Explain the operation and its assumptions without relying on an API or an anthropomorphic explanation.

**Connections:** F04 transformations, A03 representations, A04 memory cost. **Prerequisites:** F04, A01.

### A03 — Retrieval, external knowledge, and provenance

**Question:** When should information live in stored evidence rather than only in a model's parameters?

**Starting scope:** Candidate retrieval, ranking, evidence selection, freshness, access control, and answer support. Separate retrieval quality from generation quality.

**Source:** R15 for a concrete retrieval-augmented model. Use S02 concepts for storage and S06 for access boundaries. The paper's design is not interchangeable with every product called RAG.

**Exercise:** Construct cases where the correct document is missing, present but not retrieved, retrieved but ignored, and cited without supporting the answer. Design a check for each failure.

**Exit criterion:** Localize the failure stage and explain what a citation verifies and what it does not.

**Connections:** S02 indexes, F03 measurement, A05 evaluation. **Prerequisites:** S02, A01, A02.

### A04 — Inference serving and memory economics

**Question:** How do memory management and scheduling change the cost of serving a model?

**Starting scope:** Model storage, per-request state, batching, throughput/latency constraints, and memory fragmentation. Derive estimates only for a stated architecture and numeric precision.

**Source:** R16, PagedAttention. Reuse R04 and R08 for the systems connection. Treat published speedups as workload-specific results, not a prediction for a current provider.

**Exercise:** Write a symbolic memory budget for model state plus active requests. Vary sequence length and concurrency. Compare two serving policies under a fixed latency objective and an explicitly assumed workload.

**Exit criterion:** Identify the limiting resource and list what must be measured before claiming a cost improvement.

**Connections:** S01 locality/virtualization, S05 queues, B02 unit economics. **Prerequisites:** S01, S05, A02.

### A05 — Evaluation, workflows, and controlled autonomy

**Question:** When is a system capable enough, and constrained enough, to perform the intended task?

**Starting scope:** End-to-end success, baselines, failure categories, repeated trials, tool contracts, action budgets, and authority. Distinguish a fixed workflow from model-directed action selection.

**Sources:** R18 as one early tool-interaction design; R17 for system-level dependencies; R03 for evidence discipline. S06 supplies the authority model.

**Exercise:** Compare a deterministic workflow, a single model call, and a tool-using loop on the same task set. Include explicit failure cases, costs, and side-effect rules. Explain how you would investigate disagreement between an automated judge and a person.

**Exit criterion:** Defend the simplest design supported by the evidence and identify what an offline evaluation misses.

**Connections:** F02/F03 uncertainty and measurement, S03 retries, S06 permissions, B02 cost. **Prerequisites:** A01, A03, S06; A04 for serving estimates.

### B01 — Customer problems, alternatives, and evidence of demand

**Question:** What problem is costly enough that someone will change their behavior?

**Starting scope:** User versus buyer, current workaround, frequency, consequences, adoption friction, and observed commitments. Keep customer observations separate from founder interpretations.

**Source:** R19, the customer-interview segment. This is practitioner guidance, not experimental evidence that a given business will succeed.

**Exercise:** Choose a business workflow you can observe. Prepare questions about a recent real instance, its costs, alternatives, and decision process. Define stronger and weaker forms of evidence before speaking with anyone. No outreach is performed by this library.

**Exit criterion:** State a falsifiable demand hypothesis and distinguish politeness, stated interest, trials, payment, and repeated use.

**Connections:** F03 measurement, A05 success definitions, B03 distribution. **Prerequisites:** none; revisit after F03.

### B02 — Unit economics, pricing units, and sensitivity

**Question:** Which unit of useful work creates value, and what does delivering it actually cost?

**Starting scope:** Revenue, variable cost, fixed cost, support and review effort, contribution, and uncertain demand. Separate technical units such as tokens from business outcomes such as resolved cases.

**Sources:** R20 for unit metrics; R21 for pricing/packaging hypotheses. Reuse R12 for capacity assumptions.

**Exercise:** Model a service per attempted job and per verified successful job. Include failures and human review. Vary success probability, workload size, customer price, and support burden. State what is hypothetical versus observed.

**Exit criterion:** Explain why a lower model price can still yield a worse overall service, and why positive contribution is not the same as company profitability.

**Connections:** S05 capacity, A04 inference, A05 outcomes, B03 customer offer. **Prerequisites:** F02, B01, A05.

### B03 — Distribution, product boundaries, and defensibility

**Question:** Why would a customer find, adopt, keep, and pay for this offering when alternatives improve?

**Starting scope:** A narrow initial customer, acquisition path, onboarding, workflow fit, switching friction, supplier dependence, and maintenance burden. Treat a claimed moat as a hypothesis requiring evidence.

**Sources:** R22 on early manual recruitment and service; R21 on segmentation/packaging; R19 on problem evidence.

**Exercise:** Compare a self-serve tool, a managed service, and an internal deployment for the same customer job. Specify the buyer, distribution route, required trust, variable labor, and effect of a supplier bundling your main feature.

**Exit criterion:** Explain which assumptions make an option attractive and identify evidence that would overturn the recommendation.

**Connections:** S06 reliability commitments, A05 evaluation, B01 demand, B02 economics. **Prerequisites:** B01, B02.

## 5. Curated source catalog

**Read modes:** “Read” means a selected passage is an initial assignment; “Reference” means consult only to resolve a question. A course link is not an instruction to finish the course.

**Access labels:** “Full text opened” means the text was accessible to the retrieval tool and relevant portions were inspected, not that every page was exhaustively reviewed. “Index opened” means the host's description/contents were verified, with chapter-level verification left to pack production. “Abstract opened” supports source selection, not detailed experimental claims.

| ID | Source and primary link | First reading and role | Access checked / limitation |
| --- | --- | --- | --- |
| R01 | [MIT 6.006: Introduction to Algorithms, Spring 2020](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — Demaine, Ku, Solomon | Selected opening lectures and hashing; use problems to practice proof and cost analysis | Course index/syllabus opened. Prerequisite mathematics may need a bridge. |
| R02 | [Mathematics for Machine Learning](https://mml-book.github.io/) — Deisenroth, Faisal, Ong, 2020 | Reference: chapters on linear algebra, geometry, calculus, probability, optimization | Author index/contents opened; free PDF linked. Not a beginner-first cover-to-cover assignment. |
| R03 | [Patterns of Trustworthy Experimentation: Pre-Experiment Stage](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/) — Microsoft Research, 2020 | Read experiment-design patterns; ask which apply to the chosen unit of analysis | Primary practitioner article opened. Platform experience is contextual evidence. |
| R04 | [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) — Remzi and Andrea Arpaci-Dusseau | Reference: scheduling, address spaces/paging, concurrency, persistence | Author index opened; free chapters available. Implementation exercises may use C without making C the learning goal. |
| R05 | [CMU 15-445/645, Fall 2025 schedule](https://15445.courses.cs.cmu.edu/fall2025/schedule.html) — Andy Pavlo | Reference: storage, indexes, concurrency theory, logging/recovery | Course index/schedule opened with lecture-note links. Use the archived edition consistently. |
| R06 | [Time, Clocks, and the Ordering of Events in a Distributed System](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) — Leslie Lamport, 1978 | Read event ordering and logical clocks before distributed histories | Full-text PDF opened. Scope is the paper's formal model, not all modern distributed-system behavior. |
| R07 | [In Search of an Understandable Consensus Algorithm, extended version](https://raft.github.io/raft.pdf) — Ongaro and Ousterhout, 2014 | Read replicated state machines and core Raft sections; trace the state summary | Full-text PDF opened. Defer membership changes and full proofs until the core trace is clear. |
| R08 | [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/) — Dean and Barroso, 2013 | Read the motivation and mechanism of latency tails; compare with workload measurements | Publisher record/abstract opened. Linked ACM full text returned an access error during this session; detailed claims need a verified accessible copy. |
| R09 | [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) — Google, 2016 | Selected chapters: [Embracing Risk](https://sre.google/sre-book/embracing-risk/), Service Level Objectives, [Handling Overload](https://sre.google/sre-book/handling-overload/) | Contents and selected full chapters opened. Adapt practices to scale and context. |
| R10 | [End-to-End Arguments in System Design](https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf) — Saltzer, Reed, Clark, 1984 | Read argument and examples; use it to locate correctness responsibilities | Full-text PDF opened. An architectural argument, not a mechanical prohibition on lower-layer functionality. |
| R11 | [The Protection of Information in Computer Systems](https://web.mit.edu/saltzer/www/publications/protection/) — Saltzer and Schroeder, 1975 | Selected introductory protection/design principles | Author-hosted entry/overview opened. Historical mechanisms require contextual reading; principles are the intended focus. |
| R12 | [Above the Clouds: A Berkeley View of Cloud Computing](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2009/EECS-2009-28.html) — Armbrust et al., 2009 | Read the elasticity/economics argument and assumptions | University record/abstract opened. Its prices, market picture, and provider details are historical. |
| R13 | [An Introduction to Statistical Learning](https://www.statlearning.com/) — James, Witten, Hastie, Tibshirani; Python edition also Taylor | Selected statistical-learning, resampling, and regularization material | Author index/contents opened; free book PDFs linked. Choose one edition consistently. |
| R14 | [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Vaswani et al., 2017 | Read model architecture after F04; reproduce one attention calculation | Author-submitted abstract/metadata opened; full paper linked. Historical translation results do not establish present product quality. |
| R15 | [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis et al., 2020 | Read model formulation and evidence evaluation | Author-submitted abstract/metadata opened; full paper linked. Original training/model formulation differs from many later RAG workflows. |
| R16 | [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) — Kwon et al., 2023 | Read memory problem, mechanism, and evaluation conditions | Author-submitted abstract/metadata opened; full paper linked. Published speedups are not universal serving guarantees. |
| R17 | [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf) — Sculley et al., 2015 | Read system boundaries, dependencies, and feedback risks | Conference full-text PDF opened. Systems analysis, not a new model algorithm or current agent benchmark. |
| R18 | [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Yao et al., 2022/2023 | Read the action/observation approach and evaluation setup | Author-submitted abstract/metadata opened; full paper linked. Treat as one research design, not proof of general agent reliability. |
| R19 | [Startup School Week 1: evaluating ideas and talking to users](https://www.ycombinator.com/blog/startup-school-week-1-recap-kevin-hale-and-eric-migicovsky/) — YC / Hale / Migicovsky, 2019 | Start with the user-interview segment, then evaluate its fit to a local customer | Primary transcript opened. Practitioner advice with a startup-selection context. |
| R20 | [FinOps Framework: Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/) — FinOps Foundation | Read distinctions between resource units and business outcomes | Current framework page opened. A living practice framework, not a causal study of profitability. |
| R21 | [Pricing low-touch SaaS](https://stripe.com/guides/atlas/saas-pricing) — Patrick McKenzie / Stripe | Read segmentation and packaging examples; turn them into testable hypotheses | Primary practitioner guide opened. Historical case prices are not current market recommendations. |
| R22 | [Do Things that Don't Scale](https://paulgraham.com/ds.html) — Paul Graham, 2013 | Read manual recruitment and early customer-service argument | Author essay opened. Anecdotal founder guidance; assess survivorship and context. |

### How to read a paper

Create a short card with: problem; assumptions; mechanism; evidence; limitations; one derivation or trace; and a decision it informs. Read the actual relevant section before promoting a claim from “author says” to “supported within this setup.”

For empirical papers, record dataset, baseline, metric, compute/workload, and uncertainty where reported. For formal papers, record the model and statement proved. For practitioner essays, record the experience and possible selection bias. These are different kinds of evidence.

When a paper is too hard, write down the precise missing concept. Request a bridge on that concept and return to the same passage. Avoid generating an unrelated beginner course.

## 6. Worked seed: connect performance, reliability, and economics

This example is original and hypothetical. Every input below is chosen for teaching, not measured in production. Arithmetic has been checked; no system benchmark was run.

### A. A local optimization has a system-level ceiling

Assume a request takes one normalized unit of serial time. A stage uses fraction f of that time. Everything else is unchanged. If that stage becomes s times faster:

T_new = (1 − f) + f/s

Speedup = 1 / ((1 − f) + f/s)

For f = 0.30 and s = 4, T_new = 0.775 and the total speedup is about 1.29. The fourfold stage improvement is not a fourfold request improvement.

**Derivation:** Split the original time into improved and unchanged portions; divide only the improved portion by s; compare old to new time.

**Boundary:** This model excludes overlap, changes in queueing, different request mixes, and resource contention. Optimizing the stage may change those factors, so measurements can differ. Do not present this calculation as a p99 forecast.

### B. More stages can impose a success requirement

Assume eight stages must all succeed. Let each stage succeed with probability 0.97 and assume independent outcomes. Then:

P(all succeed) = 0.97^8 ≈ 0.7837

This is a consequence of the assumed probability model. It is not a measured success rate for any agent.

Without independence, use conditional probabilities:

P(all succeed) = P(S1) × P(S2 | S1) × ... × P(S8 | S1,...,S7)

**Boundary:** Shared bad inputs, common dependencies, retries, and recovery can invalidate the simple independent-stage model. An extra verification stage can improve the full outcome even while adding another component. Evaluate the complete task.

### C. The cheapest attempt need not produce the cheapest useful outcome

Assume each attempted job has the stated variable cost, and a “success” is an actually correct, usable, billable result. There are no retries, review costs, refunds, or fixed costs in this toy model.

| Hypothetical pipeline | Variable cost per attempt | Success probability | Expected variable cost per success over many comparable attempts |
| --- | ---: | ---: | ---: |
| A | ₹1.00 | 0.70 | ₹1.00 / 0.70 ≈ ₹1.43 |
| B | ₹1.30 | 0.95 | ₹1.30 / 0.95 ≈ ₹1.37 |

For N comparable attempts, expected cost is Nc and expected successes are Np; their ratio is c/p. This ratio of expectations is a planning metric, not a guarantee about a small batch's realized ratio.

If revenue is hypothetically ₹3 per successful job, expected contribution per attempt is p×₹3−c: ₹1.10 for A and ₹1.55 for B. Neither figure is profit after fixed costs, and neither establishes customer willingness to pay ₹3.

**Boundary:** Review labor, correlated failures, accepted-but-wrong outputs, usage distribution, and pricing rules can change the result. Replace assumptions with evidence before a real decision.

### What this example trains

F01 supplies decomposition; F02 supplies probability; S05 forces workload assumptions; A05 defines success; B02 makes the denominator economically meaningful. The same case is examined through several connected ideas rather than through several unrelated tutorials.

**Transfer exercise:** Introduce an optional human-review stage. State which inputs you need to decide whether it improves the offer. A useful answer includes its effect on false acceptance, completion rate, turnaround time, variable labor, and what customers will pay—not just model accuracy.

## 7. Six synthesis assignments

These assignments connect modules after their prerequisites have been produced. They are proposed future work, not completed experiments.

| ID | Decision | Inputs to reuse | Required output |
| --- | --- | --- | --- |
| C01 | Where must duplicate-effect prevention live? | F01, S02–S04, R10 | A failure timeline; invariant; responsibility boundary; counterexample to an inadequate fix |
| C02 | Does better model performance improve the customer outcome? | F02/F03, A01/A03/A05, B01 | An evaluation design separating component quality, whole-task quality, user value, and unsupported assumptions |
| C03 | Which optimization buys useful capacity? | S01/S05, A04, B02 | Resource model; workload sensitivity; effect on latency and cost per successful task |
| C04 | Which product boundary makes the service viable? | B01–B03, S06 | Compare self-serve software, managed service, and internal deployment; name evidence that would change the choice |
| C05 | How far should autonomy go? | F02/F03, S03/S06, A05 | Compare fixed workflow, suggestion-only assistant, and action-taking agent under the same task, authority, and cost model |
| C06 | How should architecture respond when a supplier changes? | S02/S06, A03–A05, B02/B03 | A decision memo on switching costs, evaluation portability, data/control boundaries, and whether a claimed advantage survives bundling |

Each memo should defend a choice under stated assumptions, then revise it after one constraint changes. A polished architecture drawing alone does not complete the assignment.

## 8. Finite production plan for the subscription period

**Production and learning are separate schedules.** The runs below commission and check future study assets. They do not assert that the learner can master this material in a month. A run is a unit of work, not a guaranteed daily quota or an enabled automation.

There are 18 core packs, six synthesis assignments, four audits, one map/diagnostic run, and one final packaging run. If fewer runs fit the actual allowance or remaining subscription period, preserve prerequisite packs and audits, and defer additional synthesis. Verify the real expiration date before setting a schedule.

| Run | Work item | Deliverable / stopping point |
| ---: | --- | --- |
| 01 | Map and diagnostic | This architecture, source registry, prerequisite questions, stable IDs |
| 02 | F01 | Invariant and algorithm-improvement pack |
| 03 | B01 | Customer-evidence pack; no invented interviews |
| 04 | F02 | Probability and expected-loss pack |
| 05 | F03 | Measurement and experimental-design pack |
| 06 | S01 | Resource-model pack |
| 07 | Audit A | Check sources, derivations, prerequisite gaps in runs 02–06 |
| 08 | F04 | Mathematical bridge pack |
| 09 | S02 | Storage/index/recovery pack |
| 10 | S03 | Concurrency and ordering pack |
| 11 | S04 | Replication and failure pack |
| 12 | S05 | Queues/cloud elasticity pack |
| 13 | C01 | Duplicate-effect decision memo |
| 14 | S06 | Reliability and authority pack |
| 15 | Audit B | Check systems traces, failure assumptions, and cross-links |
| 16 | A01 | Learning/generalization pack |
| 17 | A02 | Attention mechanism pack |
| 18 | A03 | Retrieval/provenance pack |
| 19 | A04 | Inference-serving pack |
| 20 | A05 | Evaluation/autonomy pack |
| 21 | C02 | Customer-outcome evaluation memo |
| 22 | Audit C | Check AI evidence, math, benchmark scope, and unsupported generalizations |
| 23 | B02 | Economics and sensitivity pack |
| 24 | B03 | Distribution/product-boundary pack |
| 25 | C03 | Capacity and cost memo |
| 26 | C04 | Product-boundary memo |
| 27 | C05 | Autonomy decision memo |
| 28 | C06 | Supplier-change decision memo |
| 29 | Audit D | Cross-library contradictions, broken prerequisites, missing answers, missing sources |
| 30 | Package and handoff | Index, consolidated notes, separate solutions, reference cards, open-questions ledger, export |

### Durable execution state

Maintain a simple index with: run ID, module ID, status, artifact path, source-verification date, unresolved issues, and prerequisites. Suggested states are queued, drafted, checked, and needs-revision. These track artifact production, not the learner's mastery.

The worker must inspect this index at each run. If a prerequisite or earlier artifact is unavailable, repair the missing link or report the block; do not fabricate continuity. If a run fails, retry that run before advancing. Use a finite run count and an end date matching the actual subscription window when configuring an automation.

Store original explanations, source metadata, derivations, exercises, and answers in downloadable formats. Keep references to originals and make lawful local copies only where access and rights allow. Public links and a list of paper titles alone do not satisfy deferred offline study.

## 9. Learning-pack format

Each core pack should be independently usable later:

1. **Orientation:** Decision it enables, prerequisites, notation, and a short entry route.
2. **Mechanism:** A concrete example, explicit assumptions, and a trace, derivation, or useful diagram.
3. **Boundary:** An invariant or claim, a counterexample, and the conditions where the model stops applying.
4. **Evidence:** Primary sources with exact supporting locations; distinguish proofs, experiments, and practitioner judgment.
5. **Transfer:** One prior concept reused, one future use, and one changed-constraint question.
6. **Practice:** A bounded task with setup, success criteria, and separate hints/solutions.
7. **Reference:** Compact recall card, assumptions, and unresolved questions.

Use a short orientation, a moderate core explanation, and optional deeper material. Avoid a mandatory length floor. Depth should follow the question. Give mathematical bridges before derivations that require them.

For each important source claim, keep a ledger row containing claim, source, locator, evidence type, and applicability limit. A citation title alone is not evidence. A second review by the same model is useful but is not independent verification; grounding still comes from source inspection, valid derivations, tests, or external measurements.

## 10. Reusable production prompt

> Act as a research editor and engineering tutor building a durable foundation for an individual SDE with roughly two years of experience. The goal is transferable judgment in software systems, cloud, AI, and technology business. The user's current languages and frameworks are not curriculum boundaries.
>
> Read the supplied library index, the assigned module brief, and the prerequisite packs before writing. Work on exactly the assigned run ID: [RUN_ID]. Topic/module: [MODULE_ID]. If required material is unavailable, identify the gap and produce the smallest useful repair rather than inventing prior state.
>
> Optimize for understanding mechanisms, testing claims, and making decisions. Start with the concrete question in the module brief. Explain necessary prerequisites and notation; do not infer mathematical proficiency from years of experience.
>
> Browse and open the relevant primary sources. Use original papers, author textbooks, university materials, original postmortems, and first-party technical documentation. For business, distinguish practitioner experience from empirical evidence. Record source title, authors, date/version, URL, relevant location, and access limitations. Cite only inspected material. An abstract is insufficient support for a detailed experimental claim.
>
> Produce one self-contained learning pack: orientation; mechanism with a worked example; assumptions and failure boundary; evidence; a trade-off that changes a decision; connections to earlier modules; a bounded exercise; and separate hints/solutions. Add a concise reference card. Use the lowest level of explanation necessary for the question—bytes, execution traces, mathematical models, or incentive/cost models as appropriate.
>
> Prefer one primary anchor and at most two necessary supplements per pack. Use one illustrative implementation or pseudocode when useful. Compare additional implementations only when they reveal a meaningful design trade-off. A source count or engine count is not a quality target.
>
> Distinguish sourced facts, derivations with explicit premises, hypothetical inputs, observed experimental results, and unresolved claims. Source empirical numbers and implementation constants. Show derivations for calculated results. State versions/workloads for implementation-dependent facts. Mark code as executed or untested accurately.
>
> Include a production incident only if a primary account supports its relevance. Otherwise use a clearly labeled hypothetical counterexample. Keep historical research results separate from current product claims. For current technical claims, verify current primary documentation.
>
> Audit consequential claims and calculations before finalizing. Correct discovered errors. List remaining uncertainties with specific verification steps; do not manufacture a quota of questionable claims. Evidence gaps must not silently become core facts.
>
> Keep the core readable without repeated claim labels on every sentence. Put detailed provenance in a claim ledger. Do not pad to a word count. Preserve the chosen scope and stop when this run's deliverable is complete.
>
> Save the pack and separate solutions in durable, downloadable form using the environment's supported storage. Update the index with actual artifact locations, source-check date, prerequisite links, checks performed, and unresolved issues. Never claim a save or test that did not succeed.

## 11. Reusable audit prompt

> Audit the supplied packs [IDS] against their original sources and stated assumptions. Treat the drafts as claims to check, not as authority.
>
> Prioritize claims that affect correctness, causal interpretation, security boundaries, performance, or economic decisions. Open the cited passage; verify that it supports the wording. Check mathematical premises and arithmetic. Where feasible, run the relevant small experiment. Distinguish source existence, source support, reproducibility, and applicability to a different setting.
>
> Look for invented precision, mixed versions, missing prerequisites, inconsistent terminology, benchmark generalization, undefined success metrics, and solutions that contradict the exercises. For business claims, separate assumptions and anecdotes from observed demand. Do not invent an independent reviewer or claim independent validation merely because this is another model pass.
>
> Return a correction log with location, issue, evidence, change, and residual uncertainty. Apply supported corrections, preserve source provenance, and update cross-links. Record checks not possible in this environment. Finish with a corrected pack and an honest verification status.

## 12. Use the library at your own pace

Pick one question relevant to your curiosity or a real decision. Follow its prerequisite links rather than reading in a rigid calendar. Begin with the short orientation. Attempt the example or exercise before opening the solution. On a later visit, change one assumption and see whether your explanation still works.

Track learning separately from production: can recognize, can explain, can derive/trace, can transfer. A packet can be checked while your own understanding is still at the recognition stage. Neither a large archive nor a completed reading count establishes skill.

When time is scarce, favor revisiting one useful decision and its supporting mechanisms. Expand the library when a concrete question exposes a missing concept. This keeps a versatile foundation connected to increasingly capable reasoning.

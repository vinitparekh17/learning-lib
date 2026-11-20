# A03 — Retrieval, external knowledge, and provenance

| Field | Value |
| --- | --- |
| Title | Retrieval, external knowledge, and provenance |
| ID / revision / date | A03 · 1.0 · 2026-11-10 |
| Prerequisites | S02 versioned evidence, A01 evaluation boundaries, A02 attention; S06 authority bridge below |
| Capability developed | Locate a failed evidence-to-answer stage and defend what a citation actually establishes |
| Source-check status | R15 arXiv v4 methods and experimental setup inspected; R11 mediation passage rechecked |
| Experiment status | Constructed corpus, fixed scores and executed finite checks; no live retriever, language model or semantic verifier evaluated |
| Companion | [Hints, worked answers and checks](SDE_A03_answers.md) |

## The answer changed; which part should change?

A reviewer asks, “What delivery reference is published for tenant A's D17 now?” S02's example has an older revision with delivery reference X and a newer revision with Y. A model can produce fluent text containing either. The decision is whether the answer is supported by the intended revision and whether this reviewer is allowed to see it.

Keep frequently changing, tenant-specific and auditable facts in a versioned evidence system when those properties are required. Model parameters can supply learned language patterns, but a plausible remembered answer does not identify the document revision used. Retrieval makes particular source material available to the answering procedure; it does not by itself establish that the procedure uses it correctly.

A **corpus** is the stored collection. An **index** is a representation used to find candidates. A **passage** is a bounded piece of source material. A **ranking score** orders candidates under a rule. A **context** is the evidence actually delivered to the answer-producing component. A **citation** identifies claimed support. These objects can disagree: a source may exist without being indexed, a retrieved passage may be dropped before generation, and a valid link may accompany an unsupported claim.

Our lesson uses a deterministic document query before discussing open-ended answers. No learner readiness is assumed. S02 supplies immutable revision identity; S06 supplies the distinction between a caller's request and their authority; A01 requires that evaluation reflect the intended decision time. A02's normalized attention weights do not certify truth or access rights.

## One query and four passages

All metadata, scores and times in this case are invented. Time is measured in arbitrary units. Revision 2 was published at t=5, revision 3 at t=15. The query arrives at t=20. An authoritative head lookup selects revision 3; this is a system fact, not a conclusion inferred from similarity scores. Current read permission allows tenant A's D17 only.

| Passage | Tenant / document / revision | Content fixture | Score |
| --- | --- | --- | ---: |
| old | A / D17 / 2 | Delivery reference X | 97 |
| other | B / D17 / 3 | Delivery reference Z | 95 |
| note | A / D17 / 3 | Review notes; no delivery reference | 93 |
| new | A / D17 / 3 | Delivery reference Y | 88 |

A score of 97 is simply larger than 88 under this assigned ranking. It is neither 97% confidence nor evidence of freshness. Identical document IDs in different tenant namespaces do not identify the same document.

Our proposed sequence is:

1. Establish the authenticated principal and exact question: current published state, a named revision, or historical state as of a time.
2. Resolve the permitted document and selected revision using authoritative metadata.
3. Search only eligible passages, or ensure equivalent enforcement before any unauthorized content reaches an untrusted component.
4. Retrieve a candidate set, rank/select evidence under a context budget, and preserve stable locators.
5. Produce an answer or an explicit insufficient-evidence outcome.
6. Check each consequential claim against the selected evidence and enforce permission at disclosure under the declared freshness contract.

Applying tenant/document/revision constraints leaves `note` and `new`. Top-1 by our score retrieves `note` and misses the fact. Top-2 contains both. But a one-passage context that keeps the first score-ranked passage still drops `new`. Increasing retrieval depth alone did not solve evidence selection. For this structured query, a simple field-aware selector preferring passages with the requested delivery field chooses `new`. For prose questions, that relevance judgment needs its own evaluation.

An exact fact lookup on `(tenant, doc, rev, field)` is a strong baseline here. A general semantic search is useful when questions or source phrasing are varied, but it must earn its complexity against that baseline. Do not make a precise record lookup harder merely to use generation.

## Four failures, plus a handoff loss

The desired answer is “The published delivery reference is Y,” linked to the exact location in revision 3. A diagnostic must compare intermediate artifacts, not only the final sentence.

| Controlled failure | Observation to inspect | Repair candidate and remaining limit |
| --- | --- | --- |
| Correct evidence missing | Authoritative revision manifest expects the delivery fact, but the indexed corpus lacks `new` | Repair ingestion/index publication; a larger k cannot recover absent content |
| Present but not retrieved | `new` exists and is eligible, but top-1 is `note` | Examine query/ranker/index approximation; top-2 repairs this fixture only |
| Retrieved but dropped | Candidate IDs include `new`; delivered context contains only `note` | Repair selection/truncation; log the actual context, not merely retrieval results |
| Retrieved and supplied but ignored | Context contains `new`; answer says X without valid current support | Evaluate answer construction, contradictory memory and abstention; retriever recall is already adequate |
| Cited without support | Answer says “Payment is settled” and cites `new` | Resolve the citation and compare the claim with its passage; a delivery reference says nothing about settlement |

The first, second, fourth and fifth rows instantiate the curriculum's required four failure cases. The third separates a common handoff ambiguity in “retrieved.” They are controlled constructions, not observed incident frequencies. In a real failure several defects may coexist. Report the earliest failing stage for triage while retaining later failures rather than pretending each case has one universal cause.

For debugging, supplying known sufficient evidence directly can isolate downstream behavior. If the answer remains wrong, changing only retrieval cannot fix that controlled run. Such an oracle-evidence test does not estimate deployed quality because it bypasses the retrieval difficulty. Conversely, improved recall does not prove improved supported-answer rate if context selection or generation remains defective.

## What a citation must preserve

Store a citation record with tenant/document identity, immutable revision, passage identifier, source-byte reference, extraction/rendering version and a locator such as page/region or offsets into that exact rendering. Preserve enough bytes to reproduce the source. A digest can detect mismatch; it cannot recreate a deleted document. Re-resolve permissions before disclosing retained evidence. This extends S02 and S06 rather than replacing them with a model prompt.

Check three different properties:

- **Resolution:** the cited object and span exist and identify the source version claimed.
- **Support:** that span, possibly together with explicitly identified additional evidence, justifies the actual claim at its stated scope.
- **Applicability:** the source belongs to the requested object, time and authority context and is permitted for this principal.

A citation can resolve perfectly and fail the other two. An old passage supports “revision 2 listed X,” but not “the current revision lists X” at t=20. A delivery reference supports an extracted field claim, not that goods physically arrived or a payment settled. Source support is also distinct from source truth: an authentic invoice can itself contain a false assertion.

When an answer has several claims, check each. A single source at the paragraph's end does not necessarily support every sentence. For a conclusion combining passages, retain the combination and explain the inference. Conflicting eligible sources should trigger the declared source-precedence rule or an unresolved result, not a silent choice of whichever scored highest.

In the companion, support is a manually assigned exact fact relation. It validates the example's bookkeeping. It is not an algorithm for determining arbitrary textual entailment. Real support assessment needs a rubric, human-labeled cases and an evaluation of the assessor's errors.

## Freshness and authority are separate clocks

For a historical question at t=10, the published revision is 2 and X is appropriate. For the same question at t=20, revision 3 and Y are appropriate. Neither answer should use a mutable “latest” link to reconstruct what was seen earlier. Record query time, source publication time, indexed snapshot and selected revision.

If the head advances before the new index is ready, do not silently substitute old evidence while claiming current state. One policy is to return “current evidence unavailable” until the revision is searchable, or use an authorized direct lookup. Another is to offer a clearly labeled older result if the product contract permits it. Choose and test that contract explicitly. Updating source bytes without rebuilding affected passages/index entries is not a complete retrieval update.

For access control, relevance is never permission. Do not send all tenants' passages to an external model and ask it to ignore forbidden ones. It has already received them. Post-filtering can also hurt recall: selecting global top-1 and then removing ineligible results can yield an empty set even when eligible evidence exists. The fixture demonstrates this without measuring any search engine.

A permission can change between retrieval and display. Our proposed immediate-disclosure policy requires a current authorization decision coordinated with disclosure; merely storing a policy version does not enforce that ordering. If permission cannot be established, withhold the protected answer. If a system deliberately allows bounded staleness, declare and evaluate that weaker policy. An answer cache must respect principal scope, source revision and permission changes; a query-string-only cache fails these requirements.

R11's complete-mediation passage explicitly includes remembered authorization decisions. Retrieved text is untrusted data and cannot grant new privileges by claiming to be an administrator. Authority must be enforced outside the generated response, as S06 established. These are design obligations, not security guarantees provided by R15.

## What the original RAG paper contributes

R15 combines a DPR-based retriever, a dense Wikipedia index and a BART generator. Its RAG-Sequence formulation marginalizes one latent passage across an output sequence; RAG-Token marginalizes passages at each output-token step over the retrieved set. During fine-tuning it updates the query encoder and generator while keeping the document encoder/index fixed. These are specific mechanisms, not a definition of every later retrieval pipeline. Inspect §2.1–2.4, pp. 3–4; §3, p. 4 states the corpus setup.

An original two-passage calculation makes the distinction concrete. Let retrieval weights be 0.6 and 0.4. For a fixed two-token target and its fixed prefix, let conditional token probabilities be (0.8,0.5) under passage 1 and (0.2,0.9) under passage 2. With these hypothetical normalized weights:

\[
P_{sequence}=0.6(0.8)(0.5)+0.4(0.2)(0.9)=0.312,
\]
\[
P_{token}=[0.6(0.8)+0.4(0.2)]\,[0.6(0.5)+0.4(0.9)]=0.3696.
\]

The second expression includes cross-passage contributions between token positions. It does not require fetching a new corpus on each step. Neither number is a probability that the answer is true or a permission decision. The paper's model is not implemented by our deterministic field selector, and our fixture does not reproduce its experiments.

## Evaluate the whole path without hiding failures

Define success for our query as a correct, supported answer for the selected revision with no unauthorized disclosure. Track abstention, incorrect answer and missing evidence separately. A safe abstention can be preferable to fabrication while still failing an answer-completion objective. Questions outside the supported population need a declared separate denominator.

Imagine 20 eligible test queries, each requiring one evidence item. Four lack it in the corpus; four more miss it during retrieval; two more lose it during selection; three more fail downstream; seven succeed. These stages are nested and exhaustive by construction. Corpus coverage is 16/20, conditional candidate hit rate 12/16, conditional selection retention 10/12, and supported completion given sufficient context 7/10. Their product is 7/20=35%. Reporting only 70% on the sufficient-context subset conceals upstream losses. This is an accounting identity for this suite, not an independence assumption or predicted production rate.

For multi-evidence questions, replace a single hit with a sufficient-evidence-set criterion; one relevant passage may be inadequate. Freeze corpus snapshots, permissions, query interpretations and answer rubric before final evaluation. Use A01's group/time boundaries, keep document revisions together and exclude information unavailable at decision time. Compare exact lookup, lexical matching and learned retrieval under the same task contract. Measure ranking, selected-context sufficiency, claim support, abstention and full-task outcomes as well as resource costs. Do not transfer a public QA score to private invoice correctness.

## Practice

1. Trace eligible passages, top-1, top-2 and one-passage context for the t=20 query. Compare a field-aware selector with exact lookup and score-only selection.
2. Construct the four required failure cases and the selection-loss case. For each, name the artifact to inspect and a controlled test that distinguishes it from adjacent stages.
3. Compare “revision 2 listed X,” “current reference is X” and “payment is settled” with citations to `old` or `new`. Separate resolution, support, applicability and source truth.
4. Change query time to t=10, then restore t=20 but remove `new` from the index. Add a permission revocation before display. Specify an honest response policy for each case.
5. Recompute the two probability expressions and explain why passage weights, attention weights and claim correctness are different quantities.
6. Derive all stage rates for the 20-query suite. Propose an evaluation that could reject a higher-recall retriever, including context budget, access controls, missing answers and deployment-aligned splits.

## Reference card and evidence

Identify the question's object/time → enforce authority → verify corpus/index availability → inspect candidates → inspect actual context → assess each claim against exact evidence → retain the source version. A resolvable citation is a starting point for verification.

| Basis | Inspected locator | Use and boundary |
| --- | --- | --- |
| R15, Lewis et al., 2020; arXiv v4 dated 2021-04-12 | [Versioned paper](https://arxiv.org/pdf/2005.11401v4), Figure 1 p. 2, §§2.1–2.4 pp. 3–4, §3 opening p. 4 | Concrete retriever/generator model and experimental corpus scope; no performance result adopted |
| R11, Saltzer and Schroeder, 1975 | [Basic Principles](https://web.mit.edu/saltzer/www/publications/protection/Basic.html), §I.A.3 c, Complete mediation | Access checks and updating cached decisions; our disclosure protocol is an application design |
| Earlier packs | S02 evidence identity; S06 authority; A01 evaluation; A02 attention limits | Continuity, not fresh deployment validation |
| Original synthesis | Corpus, fixed scores, failure cases, two-passage calculation, stage accounting and companion checks | Constructed values and explicit assumptions, not measured model behavior |

Open inputs include real corpus completeness, grouping, source accuracy, index publication latency, permission synchronization, ranker behavior, context budgets and support-assessor error. No essential source-access blocker remains. Learner answers/mastery remain unknown. Next A04 studies inference serving and memory economics.

## Revision history

- 1.0 — 2026-11-10. Versioned retrieval case, stage diagnostics, provenance/authority boundaries and six exercises.

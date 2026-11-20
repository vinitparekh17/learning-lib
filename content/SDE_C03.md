# C03 — Which optimization buys useful capacity?

| Field | Value |
| --- | --- |
| ID / title | C03 · Which optimization buys useful capacity? |
| Revision / date | 1.0 · 2026-11-13 |
| Prerequisites | S01 resource models; S05 queues and offered-load accounting; A04 inference memory/scheduling; B02 useful-outcome economics |
| Capability developed | Select an optimization using workload, deadline and cost constraints, then revise it when the workload changes |
| Source-check status | R16 v1 §§4.1–4.3 and §4.5; R09 chapter 21 resource-capacity discussion inspected |
| Experiment status | Deterministic scheduling and exact cost checks executed; no hardware benchmark or model evaluation |
| Companion | [Worked analysis and reproducible checks](SDE_C03_answers.md) |

## Decision memo

**Recommendation under the starting assumptions:** test the prompt-processing optimization P before purchasing a second replica R. P delivers all eight offered tasks within the deadline at 30 U per timely correct task, compared with 55 U for R. When the output workload doubles, revise the choice to R: it preserves eight timely tasks while P delivers four. These are conditional results of an invented service model, not deployment claims.

The decision owner must first validate the resource and quality assumptions. A cheaper case is not useful if evidence is unsupported, authority is violated or latency is measured at the wrong boundary. This memo combines the earlier modules around one bounded choice; it does not claim that either option is universally optimal.

## 1. Freeze the job and the comparison

The service prepares invoice evidence for an authorized reviewer. It cannot approve payment. A useful task returns the complete supported package within a 90 ms arrival-to-response deadline, inclusive, with unchanged evidence scope and access checks. All eight offered tasks count in the denominator. Late results, refusals and unsupported results do not count as useful successes, although a refusal may be contract-correct in a broader evaluation.

The boundary here begins when an eligible prepared input arrives at the serving queue and ends when the validated response is ready. Retrieval, network transit and human consumption are outside this latency boundary. The 90 ms objective is therefore a serving-stage budget, not an end-to-end customer promise. Validation overhead is included in the assigned service durations. A separate illustrative verification charge is counted financially; it does not introduce an unmodeled human wait into the 90 ms clock.

All numbers are hypothetical. Eight identical-length requests arrive together at time zero, with IDs 1–8 breaking ties. There are no retries, failures, cancellations, transfers, warmup delays or background interference. Model, precision, input evidence and correctness are held fixed. A task must generate its complete required output; shortening it merely to meet the deadline is not an allowed optimization.

Only batch sizes 1–4 are within this fixture's characterized operating envelope. Batch size eight and more sophisticated continuous scheduling are candidates for later measurement, not assumed impossible. The memo compares three named policies, not every possible schedule. All provisioned replicas are ready at time zero and remain purchased for a common 200 ms window, including idle time. All traces used for the main comparison finish within that window.

## 2. Resource feasibility before timing

Reuse A04's hypothetical device layout: 24 GiB total, 12 GiB weights, 4 GiB other-memory reserve, leaving 8 GiB for KV state. The cache coefficient is 128 KiB per retained position. Each request has a conservative peak cap of 4,096 positions, including prompt and generated positions for both output scenarios. Thus a request needs at most 512 MiB and four active requests need 2 GiB. Queued requests retain their inputs off-device and hold no KV state. Each replica stores its own weights and cache; its memory is not pooled with another replica.

The feasibility check is local to each device:

\[
12\text{ GiB}+4\text{ GiB}+4(4096)(128\text{ KiB})=18\text{ GiB}\le24\text{ GiB}.
\]

The reserve must actually bound workspace, runtime state and metadata. Memory headroom does not establish a latency guarantee. R16's block-based mapping separates logical KV positions from physical allocations, and its scheduling discussion addresses growth beyond available blocks. These mechanisms motivate measuring allocation and growth; the paper does not supply our timing law.

A memory-only change M that reduces unused allocation but leaves this feasible schedule and its service durations unchanged produces the same timely count as the baseline. That is a counterexample to equating lower allocated bytes with useful throughput. If larger prompts make memory binding, M may matter; the resource condition and timing evidence must then be revisited together.

S01's operation/byte bounds explain what cannot be faster than the available resources permit. Here we additionally assign elapsed service laws so that a trace can be computed. An operation lower bound alone would not justify those durations. R09 chapter 21 cautions that requests differ in resource demand; the same request count need not imply the same capacity requirement.

## 3. The three policies and their mechanism

Let b be batch size and d the number of decode rounds after prefill. In the baseline law, prefill takes 8+2b ms and each decode round takes 4+b ms. Prefill emits the first token; a task returns d+1 tokens in this small abstraction. Sequential phase durations add because there is no overlap.

\[
s_B(b,d)=8+2b+d(4+b).
\]

P halves only prefill time, holding decoding, output quality and all other costs fixed:

\[
s_P(b,d)=4+b+d(4+b).
\]

This is a proposed performance effect to validate, not a claim that a particular kernel or cache will provide it. R uses two unchanged replicas. Each processes one batch of four at time zero. B and P use one replica with two batches of four in FIFO order; the second begins when the first finishes. No batch-formation delay occurs because all requests already exist.

At b=4 and d=4, baseline prefill is 16 ms and decoding is 32 ms. Halving a third of the original 48 ms service duration yields 40 ms, a 1.2× batch speedup, not 2×. Even eliminating prefill entirely would leave 32 ms and limit this isolated speedup to 1.5×. This is an original phase-sum derivation; it assumes the change does not move work into decoding or another stage.

| Starting workload: d=4 | B: one baseline replica | P: faster prefill, one replica | R: two baseline replicas |
| --- | ---: | ---: | ---: |
| Batch service time | 48 ms | 40 ms | 48 ms |
| Task completion times | 48×4, 96×4 ms | 40×4, 80×4 ms | 48×8 ms |
| Timely correct tasks / offered | 4/8 | 8/8 | 8/8 |
| Mean serving response | 72 ms | 60 ms | 48 ms |
| Last completion | 96 ms | 80 ms | 48 ms |
| Total busy replica-time | 96 ms | 80 ms | 96 ms |
| Purchased replica-time | 200 ms | 200 ms | 400 ms |

Here “48×4” means four tasks finish at 48 ms, not a 192 ms response. R halves the last-completion time relative to B without reducing total busy work. P reduces work modestly, but moves the second batch across the deadline, doubling the useful count in this fixture. Threshold effects can make task-level improvement larger than component speedup.

## 4. Count purchased capacity and unsuccessful work

Assign a price of 1 U per purchased replica-ms and a non-overlapping 5 U verification/accounting charge per attempted task, including late tasks. U is an arbitrary currency unit, not a provider price. Total modeled cost is

\[
C=200k+5N,
\]

where k is replicas and N=8. B and P cost 240 U; R costs 440 U. Divide by timely correct count G, not by tokens or all eventual completions. Costs per useful task are respectively 60, 30 and 55 U. If G=0, retain incurred cost and report no finite cost-per-useful-task ratio.

The decision rule is lexicographic: first require all eight offered tasks to succeed within the budget; among qualifying policies choose the lowest modeled cost. P and R pass; P wins. This is not a revenue or profitability model. It excludes implementation, maintenance, procurement, shared infrastructure and other unlisted costs. At unchanged traffic and outcomes, P's recurring saving relative to R is 200 U per window. If P requires K U of additional engineering expense over R, recovery needs at least K/200 identical windows under these assumptions. Neither workload persistence nor that expense is observed.

Counting only busy time would assign much smaller costs and conceal the idle purchased replica. Conversely, a true usage-only billing contract would need another cost model. The common window makes capacity ownership explicit; it is not evidence about a cloud billing minimum.

## 5. Change one constraint and revise the decision

Now require d=8 decode rounds, retaining eight arrivals, the 90 ms deadline, the same 4,096-position cap and the same per-round law. Longer complete outputs are required by the changed workload; prompt processing is unchanged. This is a controlled sensitivity case, not an assertion that real decoding time is independent of growing sequence length.

| Longer output: d=8 | B | P | R |
| --- | ---: | ---: | ---: |
| Batch duration | 80 ms | 72 ms | 80 ms |
| Completions | 80×4, 160×4 | 72×4, 144×4 | 80×8 |
| Timely correct / offered | 4/8 | 4/8 | 8/8 |
| Mean response | 120 ms | 108 ms | 80 ms |
| Modeled cost / useful task | 60 U | 60 U | 55 U |

Revise to R because it alone meets the stated all-eight objective. P still reduces elapsed work, but its second batch remains too late. Do not describe P as useless: its improvement simply fails this decision's threshold. Combining P with R is a fourth option; at the same recurring cost it could reduce latency further, but its additional implementation cost and feasibility are not included in this three-option decision.

The exact boundaries make the recommendation auditable. With b=4, B's second wave finishes at 32+16d, P's at 16+16d, and R's only wave at 16+8d. At 90 ms, all eight are timely for integer d≤3, d≤4 and d≤9 respectively. For d≥10 none of these three policies meets the all-eight objective. More capacity does not fix a single task whose own service exceeds the budget; another service law, deadline or complete-output contract is needed.

## 6. Workload and operational checks that could overturn it

At one offered task, there is no second batch to rescue. For b=1,d=4, B takes 30 ms and P 25 ms; both meet the deadline. If R still purchases two replicas for the full window, its extra capacity provides no useful-count gain. More headroom is not automatically a cost saving.

For the longer-output case, a second replica ready at delay h completes its batch at h+80. It preserves all eight timely tasks only when h≤10 ms, under a routing rule that assigns that batch to it. “Autoscaling is enabled” is not evidence of readiness. The cost table assumes a warm replica; startup charges and delayed arrivals require a revised ledger and trace.

For unequal output lengths, a static batch may run until its longest member finishes; continuous scheduling can remove finished work and admit waiting requests. Those policies require per-request lengths and iteration-level accounting. Average output length is insufficient to reconstruct the queue. Larger prompts can change both memory demand and phase durations. Do not vary the memory cap while silently keeping a timing law outside its characterized range.

Validate P against B with the same timestamped offered arrivals, task cases, model, decoding rules and quality rubric. Record accepted/rejected/late/unsupported counts, complete response times, phase durations, peak allocated memory, growth failures, replay/retry work, billed capacity and verification effort. Include idle periods and startup in a declared window. Compare matched quality; one unsupported P result would leave only seven useful tasks and fail the all-eight gate. Eight synthetic tasks do not estimate a production percentile or establish a sustainable arrival rate.

Stop rollout on authority or evidence-integrity violations. Reject the optimization claim if speed comes from dropping required output, shifting work outside the clock or excluding hard requests from the denominator. Retain a rollback path and test repeated bursts; the fixture is a decision aid, not a production safety proof.

## Assignment for later self-assessment

1. Reconstruct per-device memory use and explain why a memory-only optimization need not change this decision.
2. Derive all starting-workload finish times, means, useful counts and phase speedup bounds.
3. Rebuild the cost ledger, compare busy versus purchased time, and state what engineering expense does to the recommendation.
4. Apply the longer-output workload, derive integer decode-round thresholds, and evaluate second-replica startup delays of 0, 10 and 11 ms.
5. Design an experiment that can reject P or R. Include sparse traffic, unequal lengths, quality failures and a reason not to report the fixture as a production p99.

## Evidence and open inputs

| Basis | Verified locator, inspected 2026-11-13 | Scope |
| --- | --- | --- |
| R16 Kwon et al., 2023 | [arXiv v1 paper](https://arxiv.org/pdf/2309.06180v1), §§4.1–4.3 pp. 5–6; §4.5 p. 8 | Block allocation/mapping and growth-related scheduling constraints; no paper speedup or current implementation default adopted |
| R09 Google SRE, 2016 | [Chapter 21](https://sre.google/sre-book/handling-overload/), The Pitfalls of Queries per Second | Resource-dependent request cost; practitioner guidance rather than this fixture's service law |
| Original conditional model | Equations, schedules, billing window, sensitivity and companion code | All numerical inputs invented; checks execute arithmetic and policy traces, not hardware performance |

S01 supplies resource feasibility, S05 supplies waiting and offered-load denominators, A04 supplies phase/cache separation, and B02 supplies full-cost useful-outcome accounting. Unknown deployment inputs include actual phase curves, quality, arrivals, memory peaks, startup time, billing and implementation effort. None blocks this synthesis; none is claimed verified.

**Reference card:** freeze the complete task → check per-resource feasibility → trace the same arrivals → count timely correct outputs → charge owned capacity and failed work → test a changed workload → revise the choice when a boundary is crossed.

## Revision history

- 1.0 — 2026-11-13. Three-option capacity memo with a workload-driven recommendation reversal and five analysis tasks.

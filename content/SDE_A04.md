# A04 — Inference serving and memory economics

| Field | Value |
| --- | --- |
| ID / revision / date | A04 · 1.0 · 2026-11-10 |
| Title | Inference serving and memory economics |
| Prerequisites | S01 resource units and paging; S05 queues and deadlines; A02 causal attention |
| Capability developed | Separate memory feasibility from useful serving capacity and defend a measurement plan |
| Source-check status | R16 v1 methods and evaluation setup inspected; R04 paging and R08 latency passages rechecked |
| Experiment status | Executed integer budgets and deterministic scheduling fixtures; no GPU benchmark or model execution |
| Companion | [Hints, answers and executable checks](SDE_A04_answers.md) |

## The model fits. Does the service fit?

Our document service summarizes evidence for a reviewer. Loading its model weights into an accelerator succeeds. Several simultaneous documents then exhaust memory, or wait too long to be useful. These are different failures: model storage is a largely shared cost, while active requests add retained state, temporary work and queueing.

The decision is how many requests to admit, how to allocate their state, and how to schedule their work under a declared response objective. S01 taught that bytes and operations constrain execution without predicting runtime. S05 added waiting and the denominator of all offered requests. A02 distinguished a dense attention calculation from incremental generation. We now combine those ideas. No diagnostic answers or learner mastery are assumed.

A token is a model input/output unit, not necessarily a word. A byte is a storage unit. Here KiB, MiB and GiB mean powers of two: 2^10, 2^20 and 2^30 bytes. Parameter counts and token counts have no memory unit until multiplied by a representation size.

## Two phases, three kinds of state

R16 §2.2 distinguishes prompt processing from sequential generation. Prompt processing builds keys and values for known inputs; later steps reuse cached keys and values and add new ones. This KV cache is distinct from the fixed model weights. In our causal decoder model, an earlier token's representation does not change when future tokens arrive. Reuse relies on that information boundary, unchanged model/configuration and compatible positions—not merely matching a token's spelling.

Think of three budget lines: shared weights, retained per-request KV state, and other memory including workspace and allocator overhead. Temporary activations are not automatically zero just because gradients are absent. A02's n² dense score table is not the same object as the retained KV cache. The cache formula below counts keys and values only; it neither requires nor rules out a particular attention-kernel workspace.

For all following estimates, assume one device, one fixed dense decoder, no offload, no sharing between requests, no beams, no sliding window and no tensor/pipeline sharding. Each of L layers stores keys and values with Hkv heads of width d, at q bytes per scalar. Count T_i cached positions for request i. The factor two represents keys plus values:

\[
c_{KV}=2LH_{kv}dq\quad\text{bytes per cached token},\qquad
M_{KV}=c_{KV}\sum_i T_i.
\]

With P stored parameters at w bytes each and a conservative bound R on all other memory, require

\[
Pw+R+c_{KV}\sum_i T_i\le M.
\]

This is an original counting derivation under the stated tensor layout. If layers differ, sum their individual sizes. Use the number of KV heads, not automatically the number of query heads. Quantized weights can require scales and metadata beyond Pw; changing weight precision does not automatically change KV precision. Distributed storage requires a per-device budget, including replicated terms and communication buffers. Training would add a different set of states.

## A budget with units you can audit

Choose a hypothetical configuration: P=6×2^30 stored scalars, w=2 bytes, L=32, Hkv=8, d=128, q=2 bytes, device memory M=24 GiB and other-memory reserve R=4 GiB. These are teaching inputs, not specifications of a named model. Thus weights use 12 GiB, leaving 8 GiB for KV state, and cKV=131,072 bytes=128 KiB. The pool holds 65,536 cached token positions.

| Equal cached length per request | KV per request | Memory-only concurrent limit |
| ---: | ---: | ---: |
| 1,024 | 128 MiB | 64 |
| 2,048 | 256 MiB | 32 |
| 4,096 | 512 MiB | 16 |
| 8,192 | 1 GiB | 8 |

At fixed length, doubling concurrency doubles this state. At fixed concurrency, doubling length does the same. Sixteen 4,096-position requests exactly fill the hypothetical KV pool: that boundary leaves no room for another cached token. A 4 GiB reserve only protects the system if it actually bounds the excluded memory over the admitted workload. If workspace grows beyond it, even this arithmetic-feasible state fails.

T_i counts positions whose KV has actually been materialized. For conservative admission, reserve up to prompt length plus an output cap; a terminal sampled token may never need its own KV. Avoid off-by-one optimism at allocation boundaries. Unknown output length calls for a growth policy: reserve, allocate incrementally with headroom, queue, preempt, or reject. An allocator cannot promise unlimited generation from a snapshot that currently fits.

## Allocation changes waste, not the number of facts stored

R16 §§4.1–4.3 partitions KV state into fixed-token blocks and maps logical blocks to physical blocks. The attention kernel follows that mapping. This is analogous to R04's page-to-frame separation; an application KV block is not an OS page, and its token count is not a byte-page size.

For an original allocation fixture, choose B=16 token slots per block. With independent requests and no shared blocks, allocated slots are

\[
A=\sum_i B\left\lceil T_i/B\right\rceil.
\]

Ceiling means round upward to an integer. For positive lengths, each request wastes between zero and B−1 slots in its last block. For N requests, internal slack is less than NB slots. Block tables and other metadata belong in the other-memory reserve; the bound is not a statement of zero overhead.

Take lengths [17,31,32,1]. They contain 81 live positions and allocate [32,32,32,16]=112 slots. Slack is 31 slots, or 3.875 MiB at our chosen cache size; total allocation is 14 MiB. Reserving a 64-position capacity for each instead takes 256 slots=32 MiB, leaving 175 slots unused at this snapshot. That unused reservation is not all external fragmentation. External fragmentation refers to separated free holes that cannot satisfy a required contiguous allocation. Tail slack sits inside allocated blocks. Future-growth reservation is another reason live and allocated memory differ.

Noncontiguous fixed blocks can use free blocks without requiring a request-sized contiguous region. They do not remove the need for enough free blocks. A 16-position request takes one block; growing to 17 takes two. Four synchronized boundary crossings can therefore need four blocks at once. Admission based only on current occupancy can fail at the next step.

A mapping invariant is that each logical block resolves to its correct retained data, and a physical block remains live while any request references it. Sharing additionally requires valid reference counts and isolation on mutation. R16 §4.4 discusses sharing and copy-on-write. Our checks do not implement those mechanisms; private blocks keep the derivation inspectable. Smaller blocks reduce tail slack but add mapping/management work. The fastest block size cannot be chosen from the slack equation alone.

## Scheduling has its own constraint

R16 §2.3 discusses batching and variable lengths; §4.5 addresses scheduling when growing state exceeds capacity. Our following policies are deliberately simpler than that implementation. R08's printed p. 76 explains why costly work can delay short requests; it motivates inspecting the complete response distribution, not importing its measurements.

Compare two policies on an identical invented workload: four requests arrive at t=0, each needs one prefill and exactly four subsequent decode rounds. Prefill emits the first token. Each decode round emits one additional token per request, so each request returns five tokens. A batch of b requests has prefill time 8+2b milliseconds and each decode round takes 4+b milliseconds. These are assigned service laws, independent of length within this fixture. Memory is assumed sufficient for all four throughout. There are no failures, setup delays, transfer costs or overlap.

Policy S processes one request fully before starting the next. Policy B starts all four together, with no batch-formation wait because all have arrived. We require every request to finish within 50 ms of arrival, inclusive. The denominator is all four offered requests; output correctness is held fixed as an assumption.

| Measure | S: serial, b=1 | B: one batch, b=4 |
| --- | --- | --- |
| First-token times (ms) | 10,40,70,100 | 16,16,16,16 |
| Completion times (ms) | 30,60,90,120 | 48,48,48,48 |
| Within 50 ms | 1/4 | 4/4 |
| Makespan | 120 ms | 48 ms |
| Completed requests / makespan | 33.33/s | 83.33/s |
| Inter-token interval after first token | 5 ms while active | 8 ms |

B wins this completion objective, while S gives the first request its first token sooner and a shorter active inter-token gap. A request in B experiences 48 ms, not 48/4=12 ms. The latter is amortized device time per completion in this fully occupied trace.

Now change only the arrival-to-completion objective to 40 ms. S still has one timely completion; B has none. Higher finite-trace throughput is not automatically a better user outcome. This is a counterexample to selecting policy solely by completed requests per second. It is not a claim that serial serving generally beats batching.

Real continuous batching can replace finished requests at iteration boundaries. Variable prompt/output lengths, prompt work interrupting decode, batch-formation delay, cancellation and memory growth change the trace. Those mechanisms require measurement or a richer simulator. Our deterministic example establishes conditional arithmetic, not an empirical p99 or sustainable arrival rate.

## What would justify a cost claim?

Memory capacity, arithmetic throughput, memory bandwidth and latency objectives can each bind. Paging might free space to admit more requests while bandwidth or the deadline still limits useful concurrency. Conversely, if the queue is empty, higher maximum batch size may buy nothing. S01's resource lower bounds and S05's offered-load accounting apply together.

Under an identical hypothetical device-time price r per second and only the busy periods above, resource charge per timely completion at 50 ms is 0.120r for S and 0.048r/4=0.012r for B. These are conditional resource charges, not provider prices or profit. At 40 ms, B has no timely completion and the ratio is undefined. Include idle capacity, startup, retries, rejected work, quality differences, operations and review labor before making a business decision. B02 will develop the useful-outcome denominator further.

A deployment comparison should freeze model, precision, decoding rules, task quality rubric, input/output length distribution, timestamped arrivals, cancellation rules and hardware. Record offered/admitted/rejected/completed/timely-correct counts; first-token, inter-token and completion distributions; peak allocated memory; live KV bytes; block slack; workspace; preemptions and recomputation. Use repeat trials and include warmup/drain and idle periods under an explicit accounting policy. Do not reduce offered load just because one policy is slow. R16 §6.1 describes its own experimental setup; no published speedup is used here as a forecast for another workload or current provider.

## Practice

1. Derive the cache coefficient and 8 GiB budget. Recompute the 4,096-position limit when Hkv changes from 8 to 16, holding other inputs fixed.
2. Reproduce the four length/concurrency rows. Explain what happens if one request grows after the pool is exactly full.
3. Compute allocation and slack for [17,31,32,1] at block sizes 8,16,32. Distinguish internal slack, external fragmentation and future reservation.
4. Reproduce both scheduling traces, first-token times and deadline counts. Why is amortized time not latency?
5. Apply the 40 ms objective and compare resource charge per timely completion. Name a workload change that invalidates the assigned service laws.
6. Design an experiment that could reject a paging/batching optimization despite lower allocated memory. Identify the limiting resource and quality/latency evidence needed.

## Reference card and evidence

Count shared weights once; count retained state per live token; bound other memory; round actual allocations; reserve growth; then evaluate schedules against the same offered workload and deadline. Memory feasibility is necessary, not sufficient, for useful capacity.

| Basis | Verified locator | Boundary |
| --- | --- | --- |
| R16 Kwon et al., 2023, arXiv v1 | [Paper](https://arxiv.org/pdf/2309.06180v1), §§2.2–2.3 p. 3; §§4.1–4.3 pp. 5–6; §4.4 pp. 6–8; §4.5 p. 8; §6.1 p. 10 | Historical mechanism and setup; no benchmark transferred |
| R04 OSTEP | [Chapter 18](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-paging.pdf), introduction and §18.1 pp. 1–3 | Fixed pages and mapping analogy |
| R08 Dean and Barroso, 2013 | [Author PDF](https://barroso.org/publications/TheTailAtScale.pdf), printed p. 76, Reducing Component Variability | Head-of-line blocking and interleaving |
| Original synthesis | All budget inputs, allocation examples, service laws, traces and exercises here | Constructed and checked; not measured hardware behavior |

No source-access blocker remains. Actual architecture, memory peaks, service curves, traffic, task quality, prices and operational behavior are unresolved application inputs. Next A05 evaluates complete workflows and constrained autonomy. Learner mastery remains unknown.

## Revision history

- 1.0 — 2026-11-10. Memory budget, block accounting, deadline counterexample and six exercises.

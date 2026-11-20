# S01 — Resource models, locality, and abstraction costs

| Field | Value |
| --- | --- |
| ID / title | S01 · Resource models, locality, and abstraction costs |
| Revision / date | 1.1 · 2026-11-04 |
| Prerequisites | F01 operation counts and invariants. Optional units bridge below. F03 helps with the benchmark design. |
| Capability developed | Predict a limiting resource, expose representation costs, and design a measurement that could overturn the prediction |
| Source-check status | R04 author-hosted OSTEP chapters inspected. Exact passages and version limits appear in the evidence ledger. |
| Experiment status | Original address-trace simulator and arithmetic executed. No hardware timing experiment performed. |
| Companion | [Hints, worked answers, and reproducible checks](SDE_S01_answers.md) |

## The decision behind “both are linear”

The fictional document service must sum eight integer evidence counts before presenting a batch to an approver. One implementation scans a packed array. Another follows a list of records. Each visits every value once and performs eight additions. F01's operation model gives both linear growth, Θ(n). That leaves a practical question unanswered. Which representation meets the latency and memory budget on the intended machine?

Use three descriptions together. The **algorithm** specifies the logical work. The **representation** determines which addresses must be accessed to do it. The **execution environment** determines how those accesses compete for resources. An optimization can change one without improving the whole task. The goal here is to write a falsifiable resource prediction before choosing an implementation.

For the sum, require immutable input, every record visited exactly once, and an integer total that fits the chosen accumulator. A list must be finite, acyclic, and terminate at its declared end. Reordering is harmless for this exact integer sum. It may change floating-point rounding or violate an order-sensitive workflow. Preserving F01's contract comes before comparing costs.

## A units bridge and a useful cost model

A byte is an addressable storage unit in our model. A record has fields occupying several bytes. A cache line is the fixed block our toy data cache transfers at once. A page is the separately chosen unit of virtual-memory translation. Those two units serve different purposes.

Let W be counted operations and r an assumed upper bound on the rate of those same operations per second. W/r has units of seconds. Let D be required bytes transferred across a named boundary and b an assumed upper bound on that boundary's bytes per second during the task. D/b is another time demand. Both rates must bound the resources available to this workload. A measured rate from a different workload is only a planning estimate, not automatically a valid upper bound. For a simplified machine where both resource limits apply,

\[
T \geq \max(W/r, D/b).
\]

This is a lower bound under the declared rates, not a runtime estimator. Perfect overlap would be needed to reach the larger term with no other cost. Dependencies, translation work, scheduling, setup, or waiting can lengthen execution. Summing the terms also requires assumptions about overlap. “Bytes accessed” must identify whether it counts requested field bytes, cache-line fills, or traffic from main memory. A miss in one cache can be served by another.

**Elapsed latency** measures a specified start-to-finish interval for one task. **CPU time** counts time executing on the CPU, including execution stalls charged while scheduled. **Throughput** counts completed tasks per elapsed interval. A task waiting to be scheduled can have greater elapsed time without doing more algorithmic work. OSTEP's scheduling chapter also distinguishes arrival-to-completion turnaround from arrival-to-first-scheduling response time. Use the intended clock explicitly. [R04, chapter 7 §§7.2, 7.6–7.8](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)

## Follow the bytes through a small machine

Caches retain copies of data. Temporal locality means reusing a recently accessed item. Spatial locality means accessing nearby locations. These are workload properties that can make caching useful. They are not guarantees supplied by a container's name. [R04, chapter 10 §10.1, pp. 2–3](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-multi.pdf)

Here is an intentionally tiny, hypothetical machine. Every numerical result below is derived from these assumptions.

- Values occupy 8 bytes. A list node contains an 8-byte value followed by an 8-byte next pointer.
- The data cache holds four 32-byte lines, is fully associative, and evicts the least recently used line. Fully associative means any line can occupy any slot.
- Pages contain 64 bytes. A separate translation cache, the TLB, holds two page translations with the same replacement rule.
- Both caches start empty. Every page is resident and accessible. For counting data-cache lines, use an identity page mapping in this toy machine.
- A miss loads the requested block. Ignore instructions, stack accesses, page-table traffic, prefetching, writes, and other processes. Count each value or pointer load once. No field crosses a line boundary.

Compare three layouts with values 1 through 8 in logical traversal order.

| Layout | Addresses visited for values | Additional accesses |
| --- | --- | --- |
| Packed array | 0, 8, 16, 24, 32, 40, 48, 56 | None |
| Packed linked nodes | 0, 16, 32, 48, 64, 80, 96, 112 | Next pointer at each value address + 8 |
| Scattered linked nodes | 0, 256, 64, 320, 128, 384, 192, 448 | Next pointer at each value address + 8 |

For byte address a, the line number is floor(a/32), the virtual page is floor(a/64), and the page offset is a mod 64. “Floor” means discard the fractional part. The packed array's line sequence is 0, 0, 0, 0, 1, 1, 1, 1. Only its first access to each line misses. Its eight values all share one page translation.

For a packed list, each pair of nodes shares a line. Loading a node's pointer reuses the line containing its value. The scattered list visits eight different lines and eight different pages. Each pointer still hits the same line and page as its preceding value. A list pointer carries the address of the next node, so the next value address depends on a previous load. An array's next address follows from its base and index. That dependency difference motivates a latency hypothesis even when both access the same number of values.

| Derived count | Array | Packed list | Scattered list |
| --- | ---: | ---: | ---: |
| Value / pointer loads per pass | 8 / 0 | 8 / 8 | 8 / 8 |
| First-pass data-cache misses | 2 | 4 | 8 |
| First-pass line-fill bytes | 64 | 128 | 256 |
| First-pass TLB misses | 1 | 2 | 8 |
| Second-pass data-cache misses | 0 | 0 | 8 |
| Second-pass TLB misses | 0 | 0 | 8 |

The second pass immediately repeats the same traversal without clearing caches. The array and packed list fit. The scattered list cycles through more lines and translations than the capacities allow. By the time it returns to a block, that block has been evicted. The answer file executes this trace and checks the totals against independent block counts.

All three sums equal 36. The first-pass fill-byte ratio of 4 between scattered list and array is **not a fourfold speedup**. We have supplied no timings, overlap model, or real cache hierarchy. Nor is 256 bytes the scattered list's allocated memory. It is transferred data under this model. Its field storage totals 128 bytes, spread across eight pages covering a 512-byte virtual span. A real allocator adds its own layout and bookkeeping.

## What the address abstraction hides

A process sees virtual addresses. Paging maps virtual pages to physical frames while preserving the within-page offset. Adjacent virtual pages need not occupy adjacent physical frames. Contiguous virtual storage therefore does not promise one physically contiguous allocation. [R04, chapter 13 §13.3, pp. 3–5](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-intro.pdf) and [chapter 18 §18.1, pp. 1–4](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-paging.pdf)

The TLB caches translations. A missing translation requires translation work. It does not by itself imply that the data page must be read from storage. OSTEP treats nonresident pages through a separate present-bit and page-fault mechanism. Our trace deliberately keeps every page resident. [R04, chapter 19 §19.1, pp. 1–3](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf) and [chapter 21 §§21.2–21.3](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys.pdf)

For this lesson, call the distinct data and translations needed over a specified interval the **working set**. Always specify that interval. Repeatedly scanning a small representation can reuse cached state. Growing the representation or interleaving unrelated work can remove that benefit. OSTEP's array example makes the analogous connection between layout, page crossings, and translation reuse. [R04, chapter 19 §19.2, pp. 3–5](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf)

Virtualization also lets processes share CPU time. A private address space and runnable thread do not promise exclusive physical resources. This lesson covers OS process and memory abstractions. It does not estimate hypervisor or container overhead. A benchmark must state its actual sharing conditions.

## Batching trades setup work for waiting

Suppose entering a document-validation operation has a fixed hypothetical cost h = 24 microseconds, followed by c = 3 microseconds per record. A batch of k records costs h + kc. With a permanently backlogged single worker and no overlap, throughput is k/(h+kc), and amortized service cost per record is c+h/k.

One record takes 27 microseconds. Eight take 48 microseconds total, or 6 per record. The saturated throughput ratio is 27/6 = 4.5. Every record in a batch released together still waits for that batch's 48-microsecond service. Dividing service by eight does not give each record's elapsed latency. This is an original application of fixed-cost amortization, a technique also discussed in OSTEP's scheduling chapter. [R04, chapter 7 §7.7, p. 8](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf)

Now change the arrival pattern. Eight records arrive 100 microseconds apart, starting at time zero, and processing starts only when the batch fills. The first waits 700 microseconds for assembly and 48 for service. The last waits 48. Their mean arrival-to-completion latency is 398 microseconds. Immediate processing would finish each in 27 because arrivals are farther apart than service time. The high-load throughput advantage and low-load latency penalty are compatible.

Choose a batch size and a maximum wait together. Also budget batch memory and define partial-batch behavior. In the exact deterministic scenario, a 750-microsecond first-record deadline permits k=8, while k=9 takes 851 microseconds. Real arrival variability needs measurement. Reordering batches must still preserve approval and output-association rules.

## Turn the prediction into a disprovable comparison

For a long, read-only scan with little arithmetic and a working set larger than cache, predict that data movement matters. For one scattered dependent chain, predict that waiting on dependent loads matters. For costly per-record computation, predict CPU execution may dominate. These are hypotheses. The tiny simulator establishes none of their real-machine rankings.

Use this proposed benchmark protocol, adapted from F03's emphasis on a common workload and declared measurement rules.

1. Freeze values, record counts, checksum, integer semantics, and output contract. Compare the same logical work. Verify each output before accepting a timing.
2. Implement an array scan, packed-node traversal, and scattered-node traversal. Record actual field sizes, padding, allocation method, and pointer order. Keep construction outside traversal timing, then report a separate end-to-end measurement including construction.
3. Record CPU, memory, OS, compiler/runtime and optimization settings, process/thread count, CPU placement, and other load. Ensure the compiler cannot discard the computed result. Inspect the executed code where optimization could invalidate the comparison.
4. Sweep sizes from small reusable data to much larger working sets. Define warmup and cache conditions. Initializing input can already warm it, so “first timed run” is not proof of a cold cache.
5. Run repeated comparisons in interleaved, randomized order using the same datasets. Report timing distributions and sample counts. If accessible, record CPU time, cache/translation events, and measured traffic with their precise counter definitions.
6. Separately test batching under stated arrival patterns. Include assembly waiting in per-record latency and count completed records over a stated interval. Track memory and correctness alongside throughput.

If packing does not improve time, investigate whether arithmetic, dispatch, or waiting elsewhere dominates. If scattered traversal approaches scan speed, inspect residency, layout, and actual dependencies before concluding locality is irrelevant. A low byte rate can coexist with waiting on a serial dependency. Changing one factor at a time and checking the mechanism makes the result more useful than a single fastest-run ratio.

## Practice and transfer

Try these six tasks before opening the companion.

1. Reproduce the first-pass cache and TLB misses for all layouts. Explain why the scattered list has eight TLB misses across sixteen field loads.
2. Derive the second-pass counts. Then reduce the data cache to two lines while retaining the two-entry TLB. Which counts change?
3. Map virtual address 136 with 64-byte pages when virtual page 2 maps to physical frame 7. Explain why a TLB miss alone establishes neither a data-cache miss nor storage I/O.
4. Reproduce batching costs, throughput ratio, and the first/last/mean latencies. Find the largest full batch meeting the 750-microsecond first-record limit under the specified arrivals.
5. Propose a benchmark that could reject the claim that scattered traversal is slower because of data access. Name one confound, one mechanism measurement, and one changed-workload test.
6. Change the workload to frequent insertions at known list nodes, then change it again to a repeatedly scanned, immutable snapshot. Defend a representation for each and identify costs omitted by traversal-only timing.

A useful answer names the logical contract, counted resource, machine assumptions, and evidence that would change the choice. F01 supplies correctness and abstract work. F03 supplies comparison discipline. S02 will revisit layout for storage and indexes. S05 will add queues and capacity. A04 will apply resource reasoning to inference using its own sources and workloads. CPU examples here establish no GPU speedup.

## Reference card and evidence ledger

Record the contract, representation, working-set interval, transfer boundary, rate assumptions, and clock. Count operations and bytes separately. Distinguish a cached translation from cached data. Treat throughput and task latency as separate outcomes. Recheck correctness after batching or reordering.

R04 is Remzi H. and Andrea C. Arpaci-Dusseau's *Operating Systems: Three Easy Pieces*. The [author index](https://pages.cs.wisc.edu/~remzi/OSTEP/) identifies version 1.10, November 2023. Individual free chapters receive updates. The inspected chapter 10 and 18 PDFs include 2025 copyright footers. The locators below identify the author-hosted snapshots accessed 2026-11-04, rather than asserting every PDF is the original 2023 text. Page numbers are chapter-local PDF pages, counting from 1.

| Claim / role | Inspected location | Evidence type and boundary |
| --- | --- | --- |
| Scheduling clocks, time sharing, fixed-cost trade-off | [Ch. 7](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf) §§7.2, 7.6–7.8, pp. 2, 6–10 | Textbook mechanisms. No quoted latency table or current scheduler claim. |
| Cache hierarchy and locality | [Ch. 10](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-multi.pdf) §10.1, pp. 2–3 | Only this background is used. Multiprocessor coherence algorithms are outside S01. |
| Virtual address-space abstraction | [Ch. 13](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-intro.pdf) §13.3, pp. 3–5 | Process view versus physical placement. |
| Pages, frames, translation | [Ch. 18](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-paging.pdf) §18.1, pp. 1–4 | Mechanism. Our page size and mapping are hypothetical. |
| Translation caching and locality | [Ch. 19](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf) §§19.1–19.2, pp. 1–5 | Translation control flow and array example. Our numerical trace is independently constructed. |
| Nonresident page handling | [Ch. 21](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys.pdf) §§21.2–21.3 | Distinguishes translation misses from absent data pages. No fault-cost estimate. |
| Resource bound, layouts, batching, benchmark design | Derivations in this pack and checks in companion | Original models and proposed protocol. Executed simulation checks model bookkeeping, not hardware behavior. |

Unresolved application inputs are actual cache and translation behavior, memory layout, workload sizes, arrival variability, contention, and latency limits. They are measurement needs, not blockers to this pack. Audit A completed on 2026-11-04; see SDE_Audit_A.md for scope and checks. No learner response or mastery is inferred.

## Revision history

- 1.0 — 2026-11-04. Original resource-model pack with an executed address trace, batching derivation, and proposed hardware benchmark.

- 1.1 — 2026-11-04: Audit A clarified the capacity assumptions required by the runtime lower bound. Numerical trace and exercises unchanged.

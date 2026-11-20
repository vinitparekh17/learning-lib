# S01 — Hints, worked answers, and reproducible checks

| Field | Value |
| --- | --- |
| ID / revision / date | S01 answers · 1.0 · 2026-11-04 |
| Companion | [Resource models, locality, and abstraction costs](SDE_S01.md) |
| Prerequisites / capability | F01 and S01's declared toy machine. Explain resource counts, latency, and a falsifiable comparison. |
| Source-check status | Uses R04 passages and evidence boundaries recorded in the core pack. |
| Experiment status | Python 3 model checks below executed successfully. No measured hardware performance. |
| Assessment status | Suggested criteria only. No learner answers received or mastery inferred. |

## Hints

1. Divide an address by the block size and discard the remainder. Track data lines and translated pages separately. A node has two loads.
2. Keep the cache contents after pass one. Ask how many distinct blocks are touched before a block is revisited.
3. Preserve the offset when changing a virtual page number to a physical frame number.
4. Separate assembly waiting, whole-batch service, and service cost divided by record count.
5. Design a comparison where the suspected mechanism changes while useful work stays the same.
6. Include how positions are found, how storage is allocated, and whether a compact snapshot must be built.

## 1. First-pass traffic

For the array, the line IDs are four 0s followed by four 1s. All eight page IDs are 0. There are two line misses and one translation miss.

For packed nodes, the sixteen field loads have four accesses per line, covering lines 0–3. Pages 0 and 1 each hold four nodes. There are four line misses and two translation misses.

For scattered nodes, value addresses give line IDs 0, 8, 2, 10, 4, 12, 6, 14 and page IDs 0, 4, 1, 5, 2, 6, 3, 7. Each next-pointer load repeats its value's line and page. There are eight misses of each kind, eight data hits, and eight TLB hits. A 50% TLB hit rate here reflects one hit on every node's pointer. It does not establish good absolute performance.

Multiplying data misses by the hypothetical 32-byte fill unit gives 64, 128, and 256 bytes. The pointer values contain the next addresses, including a terminating sentinel stored at the final node. Reading that sentinel counts as a load. Following it does not occur.

**Criterion.** Explain every miss and hit using the access sequence. Keep field storage, virtual span, requested bytes, and transferred bytes distinct.

## 2. Capacity changes and the second pass

With four cache lines, the array's two lines and the packed list's four lines remain resident after pass one. Neither has another data miss. Their one and two translations also fit, so their second-pass TLB misses are zero. The scattered layout exceeds both capacities and reuses blocks only after eviction. It incurs eight of each kind again.

With only two data-cache lines, the array still fits and has zero second-pass data misses. The packed list finishes its first pass with lines 2 and 3. Reading lines 0 and 1 evicts those, then reading 2 and 3 misses again. Its second pass has four data misses. The scattered list still has eight. Translation capacity is unchanged, so second-pass TLB misses remain 0, 0, and 8.

This is a concrete counterexample to “a second run is warm, therefore every access hits.” Warmth requires the relevant state to survive. It is also a counterexample to “every linked list has poor locality.” The packed list fits the original cache and translation capacities, though it still loads pointers and occupies more bytes than the array.

**Criterion.** Show which state survives and which is evicted. Do not infer time from miss counts alone.

## 3. Translation

136 = 2 × 64 + 8, so the virtual page number is 2 and the offset is 8. Mapping page 2 to frame 7 yields physical address 7 × 64 + 8 = **456**.

The TLB remembers a mapping. The data cache remembers data. A TLB miss can be resolved from page tables for an already-resident page. It says nothing by itself about whether the resulting physical data line is cached. Storage I/O requires a separate condition such as fetching a nonresident backed page. Our simulation excludes that condition. It also excludes the page-table memory traffic needed to repair a translation miss.

**Criterion.** Preserve the offset and distinguish translation work, data-cache lookup, and nonresident-page handling. The R04 chapter 19 and 21 passages in the core ledger support this boundary.

## 4. Batching

The one-record service cost is 24 + 3 = 27 microseconds. For eight records it is 24 + 8 × 3 = 48, or 6 per record. With an indefinitely backlogged worker, throughputs are 1,000,000/27 ≈ 37,037 records/s and 8,000,000/48 ≈ 166,667 records/s. Their ratio is 4.5. These are conditional model outputs, not benchmark results.

At 100-microsecond arrival spacing, eight arrivals occur at 0, 100, …, 700. The full batch completes at 748. Latencies are 748, 648, 548, 448, 348, 248, 148, and 48 microseconds. Their mean is (748 + 48)/2 = **398**. Each immediately processed record takes 27 because service completes before the next arrival.

For general positive integer k in this scenario, first-record latency is

\[
100(k-1)+24+3k = 103k-76.
\]

The requirement 103k−76 ≤ 750 gives k ≤ 826/103 ≈ 8.019. Thus the largest permitted full batch is eight. Nine would take 851. A wait timeout can cap assembly time when arrivals vary, but must leave time for actual service and any queueing. It does not guarantee a deadline on its own.

**Criterion.** Name the arrival and load conditions. Never call the amortized 6-microsecond service cost a 6-microsecond batch-member latency.

## 5. A test that can overturn the explanation

A useful hypothesis is that dependent scattered accesses cause longer traversal time for the target record sizes. Start with one compiled implementation and the same immutable records and checksum. Measure packed and scattered node traversal at several sizes. Use the same field representation so pointer overhead is not confused with array-versus-node layout. Separately include the packed array as the practical alternative.

Allocation inside only one timed region is a confound. So is placing one candidate's data in a different memory region or running it under different competing load. Report construction-inclusive and traversal-only times with matching boundaries. Check warmup, compiler elimination, generated dependencies, and output correctness.

Where the platform exposes suitable counters, compare cache misses, translation events, and memory traffic using their documented meanings. Test a small working set that fits, then enlarge it. A small-set speed gap that persists without the predicted miss difference weakens a cache-miss-only explanation. Add identical expensive per-record arithmetic as a separate sensitivity test. If arithmetic then dominates, layout may matter less to whole-task time. A null result with noisy measurements is inconclusive, so include repeated-run variation.

**Criterion.** State a predicted change, a controlled comparison, a mechanism observation, and a result that would change the explanation. This is a proposed experiment, not an executed one.

## 6. Changed constraints

For frequent insertion after already-known nodes, a linked representation can avoid shifting a packed array's suffix. That conclusion assumes node references are already available and storage can be allocated. Searching for the insertion point, allocation, ownership, and concurrent mutation can dominate or invalidate a simple constant-work splice story. A segmented or slack-filled representation is another candidate if scans and updates both matter.

For a repeatedly scanned immutable snapshot, a compact array is a reasonable starting choice. Measure the cost of constructing the snapshot and how many scans reuse it. If compacting costs C and each subsequent scan saves Δ, the simple serial break-even condition is mΔ > C for m scans, assuming Δ > 0 and no other changes. Include extra peak memory while both forms coexist. If only one scan occurs, conversion can lose overall despite a faster scan.

An integer sum invariant remains that after k logical visits the accumulator equals the sum of exactly those k values. A cycle, missed node, duplicate visit, overflow, or reordering that violates the actual task contract invalidates the comparison before speed matters.

**Criterion.** Defend a conditional choice and include construction, memory, and correctness. A representation name alone is not an explanation.

## Reproduction appendix

The following standard-library Python 3 block was executed on 2026-11-04. It models references to explicitly assigned addresses. The Python runtime's own memory layout and execution time have no role in these results. It verifies list termination and sums, cache and TLB counts over two passes, changed capacity, translation arithmetic, batch deadlines, and units-based throughput ratios. LRU state is retained between passes and reset between layouts.

```python
from collections import OrderedDict
from fractions import Fraction

class LRU:
    def __init__(self, capacity):
        assert capacity > 0
        self.capacity = capacity
        self.items = OrderedDict()

    def touch(self, block):
        miss = block not in self.items
        if not miss:
            self.items.move_to_end(block)
        else:
            self.items[block] = None
            if len(self.items) > self.capacity:
                self.items.popitem(last=False)
        return int(miss)

def linked_trace(addresses):
    nodes = {
        a: (i + 1, addresses[i + 1] if i + 1 < len(addresses) else None)
        for i, a in enumerate(addresses)
    }
    trace, seen, total = [], set(), 0
    p = addresses[0]
    while p is not None:
        assert p in nodes and p not in seen
        seen.add(p)
        value, nxt = nodes[p]
        trace.extend([p, p + 8])
        total += value
        p = nxt
    assert len(seen) == len(addresses) and total == 36
    return trace

traces = {
    'array': list(range(0, 64, 8)),
    'packed': linked_trace(list(range(0, 128, 16))),
    'scattered': linked_trace([0, 256, 64, 320, 128, 384, 192, 448]),
}
assert sum(range(1, 9)) == 36

def two_passes(trace, cache_capacity=4):
    cache, tlb = LRU(cache_capacity), LRU(2)
    results = []
    for _ in range(2):
        data_misses = translation_misses = 0
        for address in trace:
            assert address % 8 == 0
            assert address // 32 == (address + 7) // 32
            data_misses += cache.touch(address // 32)
            translation_misses += tlb.touch(address // 64)
        results.append((data_misses, translation_misses))
    return results

expected = {
    'array': [(2, 1), (0, 0)],
    'packed': [(4, 2), (0, 0)],
    'scattered': [(8, 8), (8, 8)],
}
for name, trace in traces.items():
    result = two_passes(trace)
    assert result == expected[name]
    # Independent first-pass counts work because no block is revisited
    # after moving on from its contiguous run in these particular traces.
    assert result[0][0] == len({a // 32 for a in trace})
    assert result[0][1] == len({a // 64 for a in trace})
    print(name, result, 'fill bytes', result[0][0] * 32)

assert two_passes(traces['array'], 2) == [(2, 1), (0, 0)]
assert two_passes(traces['packed'], 2) == [(4, 2), (4, 0)]
assert two_passes(traces['scattered'], 2) == [(8, 8), (8, 8)]
assert divmod(136, 64) == (2, 8)
assert 7 * 64 + 8 == 456

h, c, k, spacing = 24, 3, 8, 100
service = h + c * k
arrival = [i * spacing for i in range(k)]
finish = arrival[-1] + service
latencies = [finish - t for t in arrival]
assert service == 48 and Fraction(service, k) == 6
assert Fraction(k, service) / Fraction(1, h + c) == Fraction(9, 2)
assert (latencies[0], latencies[-1]) == (748, 48)
assert Fraction(sum(latencies), k) == 398
def first_latency(size):
    return (size - 1) * spacing + h + c * size
assert first_latency(8) == 748 and first_latency(9) == 851
assert max(s for s in range(1, 101) if first_latency(s) <= 750) == 8
# A monotone expression establishes the bound beyond the tested range.
assert spacing + c > 0
assert h + c < spacing
print('All S01 model checks passed.')
```

Expected printed rows are `array [(2, 1), (0, 0)] fill bytes 64`, `packed [(4, 2), (0, 0)] fill bytes 128`, and `scattered [(8, 8), (8, 8)] fill bytes 256`, followed by the success line. These checks establish the declared model's bookkeeping, not production speed, physical memory consumption, or a real scheduler's behavior.

## Revision history

- 1.0 — 2026-11-04. Six worked answers, assessment criteria, and executed model checks. Curriculum Audit A remains pending.

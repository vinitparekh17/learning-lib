# X03 — Approximate membership and the price of forgetting

| Field | Value |
| --- | --- |
| ID / revision / date | X03 · 1.0 · 20 November 2026 |
| Prerequisites | F01 invariants, F02 base rates and S02 state identity |
| Capability developed | Decide when a one-sided probabilistic membership filter saves expensive negative work without turning incomplete state into false certainty. |
| Evidence | XR05 and XR06. Primary passages and scope below. |
| Experiment | Deterministic sizing, load and stale-snapshot checks in the [worked companion](SDE_X03_answers.md). |

## The question is asymmetric

Suppose an AI retrieval service receives a document identifier and may need an object-store read before it can retrieve or rerank chunks. Most requested identifiers are absent from the tenant's current index. An exact in-memory set would avoid wasted reads, but its memory cost may be too high. A Bloom filter stores a compact summary of the identifiers that were present when a snapshot was built.

For an insert-only filter constructed from every live identifier, the answers mean different things:

| Filter answer | What follows | Safe action |
| --- | --- | --- |
| At least one tested bit is 0 | The identifier was not inserted | Skip the expensive lookup, provided the filter belongs to the same complete snapshot |
| All tested bits are 1 | The identifier may have been inserted | Check the authoritative index or store |

The second row is a false-positive boundary. It spends extra work but does not invent a record if the caller verifies the result. A false negative would skip a real record. The mathematical structure avoids false negatives only under its premises. A stale filter, an incomplete build, different key encoding, corruption or publishing the filter before its matching data can violate them.

Burton Bloom's original paper frames this as an allowable error of commission followed by a secondary test. It explicitly rules out uses requiring error-free performance. Its method 2 starts with a bit array set to zero, maps each stored message to several bit addresses and sets them to one. A query is rejected when any tested bit is zero; all ones only accept it for the follow-up test. [Bloom 1970, printed pp. 422–423, especially “A Sample Application” and “Method 2”](https://courses.cs.washington.edu/courses/csep521/21wi/readings/bloom_cacm.pdf)

## Build and query the filter

Let `m` be the number of bits, `n` the inserted keys and `k` the number of independent bit probes per key.

1. Start with `m` zero bits.
2. For each key, compute `k` bit positions and set all of them to one.
3. For a query, compute the same positions. Any zero means definitely absent under the snapshot premises. All ones mean maybe present.

With uniform independent positions, the approximate false-positive probability is

\[
p \approx (1-e^{-kn/m})^k.
\]

For a fixed number of bits per inserted key, `b = m/n`, the useful integer probe count is near `b ln 2`. Adding probes beyond that point sets too many bits and can make the filter worse. Bloom derives the corresponding occupancy and false-acceptance relationship in equations 16–17 and identifies the minimum-space point where half the field remains zero. [Bloom 1970, printed pp. 425–426](https://courses.cs.washington.edu/courses/csep521/21wi/readings/bloom_cacm.pdf)

The formula is a model. Real hash construction, small filters, uneven key distributions and implementation layout can change observed behavior. Measure the implementation used in production.

## Size from avoided work

Consider an invented retrieval snapshot with 1,000,000 document identifiers, 10 bits per identifier and 7 probes. The filter uses 10,000,000 bits, about 1.25 MB. The approximation gives `p = 0.00819`, or about 0.819%.

If 3,000,000 definitely absent identifiers are queried each day, the filter sends about 24,581 of them to the authoritative lookup and rejects about 2,975,419. At an invented 2 ms of service time per slow lookup, that avoids about 5,951 service-seconds per day. These figures are deterministic teaching inputs, not a capacity claim about object storage or vector databases.

Moving from 10 to 12 bits per key uses another 0.25 MB. With 8 probes, the modeled false-positive probability falls to about 0.314%, so the same negative workload sends about 9,427 lookups through. The extra memory prevents roughly 15,154 additional slow lookups. Whether that is worthwhile depends on the measured latency, I/O, cache churn and memory opportunity cost. Optimize the whole path rather than the false-positive rate alone.

The expected useful saving for negative queries can be sketched as

\[
q_{negative}(1-p)c_{slow} - q_{all}c_{probe} - c_{memory} - c_{build}.
\]

Use distributions for the real decision. One disk miss, remote request or GPU-side retrieval stage can have a heavy-tailed cost that an average hides.

## Production decision — Bigtable reads across SSTables

Google's Bigtable implementation stored a tablet's state across SSTables. A read could therefore require accesses to all of them, and an SSTable outside memory could cause disk I/O. The team let clients request Bloom filters for SSTables in a locality group. The filter answered whether an SSTable might contain a row/column pair. They reported that, for certain applications, a small amount of tablet-server memory drastically reduced disk seeks and that most lookups for nonexistent rows or columns did not touch disk. [Bigtable, §6 “Bloom filters,” proceedings p. 211 / PDF printed p. 7](https://research.google.com/archive/bigtable-osdi06.pdf)

The constraint was repeated negative work across immutable files. The choice kept a compact summary near the reader and treated a positive result as permission to inspect the SSTable. The paper reports the direction of the operational outcome, not a universal percentage or configuration. The filters were configurable per locality group because the payoff depends on workload.

To transfer this decision, collect the negative-lookup fraction, number of candidate files or partitions per read, actual cost of a rejected slow lookup, filter memory and probe cost, observed false-positive rate, and cache effects. Then compare end-to-end read latency and resource use with and without the filter under the same trace.

## The price of forgetting

An ordinary Bloom filter cannot safely delete by clearing a bit. Other keys may share it, so clearing it can create false negatives. Immutable SSTables avoid this particular mutation problem because a filter can be built for a fixed file and discarded with that file. Mutable systems need a different lifecycle, such as rebuilds, versioned snapshots or a deletion-capable structure whose extra state and concurrency rules are understood.

For an AI corpus, bind the filter to the exact index manifest:

- Build the data snapshot and membership filter from the same enumerated key set.
- Validate inserted count, checksum and a sample of known members before publication.
- Publish one manifest that names both artifacts, then switch readers atomically.
- If the filter is missing, older than the data, or has an unknown version, fall back to the authoritative lookup.
- Record filter negatives separately from verified positives so a rollout can be replayed and audited.

A filter can prove absence only inside the set it summarized. “Not in tenant index snapshot 42” does not mean “the document never existed,” “the user lacks access,” or “no relevant evidence exists.” Those are different claims with different authorities.

## Practice

1. For 1,000,000 keys at 10 bits per key, reproduce the modeled false-positive probability using 7 probes. Estimate false positives among 3,000,000 negative queries.
2. Compare 10 bits and 12 bits per key for that workload. State the incremental memory and avoided authoritative lookups. Which real cost would decide whether to upgrade?
3. A data snapshot is version 43 while its filter is still version 42. A query for a key added in version 43 returns negative. Classify the failure and design the serving rule that prevents it.
4. Design an A/B replay for a retrieval service. Which measurements establish saved work, and which check that the optimization did not hide valid documents?
5. Decide whether to use this filter to deny an authorization request. Identify the invariant that makes the proposed use unsafe.

## Evidence and deployment questions

| Source | Inspected locator | Application boundary |
| --- | --- | --- |
| XR05 · Burton H. Bloom | [Space/Time Trade-offs in Hash Coding with Allowable Errors](https://courses.cs.washington.edu/courses/csep521/21wi/readings/bloom_cacm.pdf), printed pp. 422–423 and 425–426, equations 16–17 and Table I | Defines the one-sided membership mechanism and modeled trade-off. Independence and uniformity are analytical assumptions; system freshness is outside the paper. |
| XR06 · Chang et al., Google | [Bigtable: A Distributed Storage System for Structured Data](https://research.google.com/archive/bigtable-osdi06.pdf), §6 “Bloom filters,” proceedings p. 211 / PDF printed p. 7 | Documents a deployed storage decision and qualitative outcome. It does not provide a universal bits-per-key setting or measured percentage reduction. |

Before trusting a negative, verify the filter and authoritative data share a version, the build covered every live key, readers use identical canonical encoding, and fallback behavior is safe during rollout and recovery. Before buying more filter memory, verify negative lookups dominate enough expensive work to matter.

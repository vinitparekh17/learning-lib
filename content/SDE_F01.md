# F01 — Invariants, algorithms, and the cost of computation

| Field | Value |
| --- | --- |
| ID / revision | F01 / 1.0 |
| Date | 2026-11-02 |
| Prerequisites | Basic loops and equality; sets and induction bridge below |
| Capability developed | Derive an optimization, prove its correctness, and state its cost assumptions |
| Source-check status | R01 lecture notes 1, 2 and 4 opened; precise passages listed in §9 |
| Experiment status | Python equivalents and bounded exhaustive checks executed; see answer file for reproduction and scope |
| State | produced; formal curriculum Audit A still pending |
| Companion | [Hints and worked answers](SDE_F01_answers.md) |

## 1. The decision: what information makes repeated work unnecessary?

You receive a batch of document identifiers and need to know whether any identifier appears twice. This is a fictional study case. A duplicate identifier means equal keys under a declared rule; it does not automatically mean two documents contain identical text or two business actions are interchangeable.

The useful question is: **What can I retain from the processed input so that the next decision is cheaper?** Start with a correct, straightforward procedure. Treat its repeated work as evidence about what information is missing. Then choose a representation that answers the repeated question efficiently.

This pack develops one example deeply. Named algorithm patterns become easier to learn when you can explain why information may safely be retained or discarded. No diagnostic response or prior mathematical fluency is assumed.

## 2. A small notation bridge and a precise contract

A sequence preserves order: `[8, 3, 6, 3]`. A set records membership without multiplicity: `{8, 3, 6}`. The expression `x in S` asks whether `S` contains `x`. A prefix `a[0:k]` contains positions 0 through k−1; it excludes position k. When k=0, the prefix is empty.

An invariant is a statement that remains true at a particular program boundary. Specify that boundary: “before each outer iteration” is meaningful; “the values are correct” is too vague to check. An induction proof establishes a starting case and shows why one valid step preserves the claim. Repeating that argument covers every iteration, however large the input becomes.

Our contract:

- Input: a finite sequence of n immutable keys, with a stable equality rule.
- Output: `True` exactly when there exist different positions i and j with equal keys.
- Empty and one-element sequences return `False`.
- The input stays unchanged; the output need not identify the matching positions.

For cost analysis initially assume each key fits in a constant number of machine words, equality and hashing cost constant time, and array access costs constant time. These are model premises, not measured facts about arbitrary document strings. Long text and custom equality require another cost model.

## 3. Build the baseline and count its actual work

Compare each new key with every earlier key:

```python
def duplicate_pairs(a):
    for j in range(len(a)):
        for i in range(j):
            if a[i] == a[j]:
                return True
    return False
```

The inner loop deliberately stops before j, so a key never matches itself. Before outer iteration j, if the function has not returned, the first j keys are pairwise distinct. During that iteration, the inner loop checks every possible earlier partner of `a[j]`. If a match is found, it supplies two different positions. If none is found, the prefix of length j+1 remains distinct. At termination the prefix is the whole sequence, so `False` is justified. The finite loop bounds establish termination separately from correctness.

Count equality comparisons on an all-distinct input. The iterations perform 0, 1, 2, …, n−1 comparisons. Pair this sum with its reverse: each of the n positions sums to n−1. Therefore

\[
2C(n)=n(n-1),\qquad C(n)=\frac{n(n-1)}2.
\]

This is a derivation for this procedure, not a benchmark. At n=1,000 there are 499,500 comparisons; at n=2,000 there are 1,999,000. Doubling n almost quadruples the work. The no-duplicate case is worst-case quadratic, written Θ(n²). Θ describes a tight growth bound up to constant factors for sufficiently large n; O gives an upper bound. Neither notation states milliseconds.

Early termination matters. `[8, 8]` needs one comparison; `[8, 3, 6, 3]` needs five: one at j=1, two at j=2, then two at j=3. A single fast example cannot establish a general cost claim. The baseline uses O(1) auxiliary space: the input already exists, and only loop indices and temporary references are added.

## 4. Derive remembered state before choosing a container

At every step the expensive question is the same: “Does the next key occur anywhere in the prefix?” Repeated scanning reconstructs membership from scratch. For a yes/no answer, the earlier order and exact occurrence counts are irrelevant. The set of earlier keys is sufficient information.

```python
def duplicate_seen(a):
    seen = set()
    for x in a:
        if x in seen:
            return True
        seen.add(x)
    return False
```

Here `set()` is an illustrative Python implementation. The proof depends on the abstract operations membership and insertion. The performance depends on how those operations are implemented. A container named “set” could internally scan a list; naming the interface does not create a speedup. R01 lecture 2 makes this interface/representation distinction explicit.

| Next position | Key | Set before membership check | Result |
| ---: | ---: | --- | --- |
| 0 | 8 | {} | Absent; insert 8 |
| 1 | 3 | {8} | Absent; insert 3 |
| 2 | 6 | {8, 3} | Absent; insert 6 |
| 3 | 3 | {8, 3, 6} | Present; return True |

The set does not tell us which earlier position contained 3. That information was deliberately discarded because our contract does not ask for it. A changed output contract may require a map from key to earlier index.

Use the invariant: **Before processing position k, if the algorithm is still running, `seen` equals the set of keys in `a[0:k]`, and that prefix has no duplicates.**

At k=0 both claims hold. If the current key is in `seen`, the membership claim guarantees an earlier equal key, so returning `True` is sound. If it is absent, inserting it preserves exact membership and distinctness for the next prefix. If the loop ends, all n keys were processed without a repeat. Thus `False` is sound too. Conversely, if a duplicate exists, its later occurrence must encounter the earlier one in `seen`; the algorithm cannot miss it.

A common bug inserts first, then checks membership. That checks against a state already containing the current item. A singleton `[8]` exposes the false positive. This is why an invariant belongs to a precise line boundary: changing statement order changes what the state means.

## 5. The speedup has conditions

An all-distinct input causes n membership calls and n insertion calls. If membership has expected constant cost and insertion has expected amortized constant cost, the total is expected O(n), with O(n) stored keys. With mandatory inspection of n keys on a distinct input, this becomes expected Θ(n) under our model. The expectation concerns the hashing model; it does not mean every input distribution has been measured.

“Amortized” distributes occasional rebuilding costs across a sequence of operations. “Expected” averages over specified randomness. These are different qualifications. One expensive insertion can coexist with a linear expected total. R01 lecture 4, page 4, supplies the hash-table conditions; this pack does not claim that every language runtime implements exactly that design.

A hash routes a key to a candidate storage location. **Equal hashes do not establish equal keys.** Consider a hypothetical table using `h(x)=x mod 10`: 1 and 11 route to the same bucket but are different. A correct collision-handling table retains enough information to compare actual keys. Keeping only these hash values would incorrectly report a duplicate.

In a simple chained table, suppose every distinct key routes to one bucket. The next membership query scans an ever-longer chain. The accumulated work can again grow quadratically. Correctness survives if equality is checked; the promised performance does not. A constant hash is a concrete counterexample to an unconditional “hashing makes this linear” claim.

Other boundaries require explicit decisions:

- If hashing a previously unseen string examines L characters, charging O(1) per key hides input-reading work. Include string lengths in the model and measure the target implementation.
- Equality and hashing must agree: keys considered equal must route compatibly. Keys must not change their relevant identity while stored.
- The mathematical contract assumes equality behaves consistently. Special numeric values, case folding, whitespace, and document revisions need a defined business rule before a container can enforce it.
- Exhausting memory is possible. An online algorithm can process one key at a time while still retaining growing state.

## 6. Change the constraint and revisit the representation

| Constraint | Defensible option | Cost or changed guarantee | Evidence that could reverse the choice |
| --- | --- | --- | --- |
| Small batch, tight auxiliary memory | Pairwise baseline | Θ(n²) worst-case comparisons; O(1) extra space | Actual batch sizes or latency become unacceptable |
| Large batch, sufficient memory, suitable keys | Remembered membership with a hash set | Expected linear total under stated conditions; O(n) extra keys | Measured memory, collision behavior, key costs |
| Known domain of U integer IDs | U membership flags indexed by ID | Initialize U flags, then scan: O(U+n) time; O(U) flags | Domain grows or IDs become sparse/unbounded |
| Only last W items matter | Explicit rolling-window contract | May forget older duplicates; must manage expiration correctly | Requirement actually means “ever seen” |
| Arbitrary long stream, exact all-history answer | Retain enough history, possibly externally | Memory or external-storage cost grows with information retained | Replays, bounded domain, approximation, or time-window requirements become acceptable |

The domain option follows directly from indexing: initialize every flag to false; on each valid ID inspect its flag, then set it. Domain validation is part of the contract. A tiny domain can make this attractive even when a general-purpose hash table is available.

Bounded memory cannot be justified by silently forgetting old values. If a cache retains only the previous two keys, `[1, 2, 3, 1]` loses the first 1 before the last arrives. It answers a different question. For an exact deterministic all-history membership state over a finite universe, different seen subsets must be distinguishable: choose a key in their symmetric difference and append it; one history now contains a duplicate and the other does not. With at most b bits there are at most 2^b states. More distinguishable subsets than states force an error. This is an original counting argument for the stated one-pass model, not a blanket impossibility statement for replayable input or external storage.

## 7. Practice and transfer

Allow roughly 30–45 minutes if useful; time is a planning suggestion, not an assessment score. Try these before opening the answers.

1. For `[4, 9, 1, 7, 9]`, trace both procedures. Count pairwise equality comparisons and abstract set membership calls. State each return value.
2. Write the remembered-state invariant in your own words. Give initialization, preservation, return reasoning, and termination. Explain the singleton failure of inserting before checking.
3. Calculate the baseline comparison count for n=100 and n=1,000 on all-distinct input. List the assumptions needed for the expected-linear alternative. Explain the difference between membership calls and key comparisons.
4. Modify the contract to return a matching pair of positions. Specify the state and trace the same input. Give the time and space qualifications.
5. You may retain only the previous two IDs. Explain what `[1, 2, 3, 1]` proves. Give two legitimate requirement or resource changes that permit a solution.
6. In the recurring document service, two workers check the same ID simultaneously, both find it absent, and both perform a payment. Explain why this pack’s single-process proof does not establish duplicate-effect prevention. Write the stronger invariant you would need.

Success means explaining the retained information, proof boundary, counted operation, and a failed assumption. Code alone is insufficient. This is the first technical pack; it builds on the initialization map’s themes of state and contracts. S02 will use stored representations to accelerate queries. S03/S04 will examine interleavings and failures. A03 will revisit what a representation retains or loses about evidence.

## 8. Reference card

Write down: contract → baseline → repeated query → sufficient state → invariant → cost model → counterexample. For this example, the repeated query is prefix membership; the state is the set of earlier keys; the check happens before insertion. Pairwise comparison needs n(n−1)/2 comparisons on distinct input. A suitable hash set gives expected linear total work and linear extra keys under explicit assumptions. Tests can expose bugs; the invariant explains arbitrary lengths within the model.

Open questions for application: What exactly counts as an equal document ID? How long must history survive? Are inputs adversarial? What is the key-size distribution? Is memory sufficient? These are requirements to resolve before deployment, not blockers to the learning pack. No production performance benchmark or concurrency guarantee is claimed.

## 9. Evidence and verification ledger

Primary anchor: MIT 6.006, Spring 2020, instructors Erik Demaine, Jason Ku, Justin Solomon; R01 in the source register. Page numbers below are PDF pages, counting from 1. All three PDFs were opened on 2026-11-02. No empirical speedup from these notes is asserted here.

| Claim / role | Verified location | Evidence type and limit |
| --- | --- | --- |
| General correctness, induction, operation counting, asymptotic notation, Word-RAM assumptions | [Lecture 1](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/477c78e0af2df61fa205bcc6cb613ceb_MIT6_006S20_lec1.pdf), pp. 2–3, Correctness / Efficiency / Model of Computation | Teaching definitions and model; not wall-clock predictions |
| Interface and implementation are distinct; amortization concerns sequences of operations | [Lecture 2](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/79a07dc1cb47d76dae2ffedc701e3d2b_MIT6_006S20_lec2.pdf), p. 1 Data Structure Interfaces; p. 4 Amortized Analysis | Abstract operations and analysis technique |
| Direct indexing trades space for lookup; collisions and chain length affect work; dynamic hashing has expected amortized bounds | [Lecture 4](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ce9e94705b914598ce78a00a70a1f734_MIT6_006S20_lec4.pdf), pp. 2–4, Direct Access Array / Chaining / Universal / Dynamic | Conditional theoretical analysis; not a claim about current runtime internals |
| Pairwise formula, loop proofs, traces, modified contracts, bounded-state argument | §§2–7 of this pack | Original derivations from explicit premises; fictional inputs |
| Executable agreement and arithmetic | Answer-file reproduction appendix | Bounded exhaustive checks; no hardware-speed conclusion and no substitute for proof |

## Revision history

- 1.0 — 2026-11-02: original F01 pack; restricted scope to duplicate detection, exact membership, and cost assumptions. Two-pointer patterns deferred until a later question needs them.

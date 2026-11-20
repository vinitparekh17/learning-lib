# F01 — Hints, worked answers, and checks

| Field | Value |
| --- | --- |
| ID / revision | F01 answers / 1.0 |
| Date | 2026-11-02 |
| Prerequisites | [F01 core pack](SDE_F01.md) |
| Capability developed | Check a proof, trace, and cost claim against a concrete contract |
| Source-check status | Same R01 passages as core §9; solutions below are original derivations |
| Experiment status | Reproduction block executed under Python 3; bounded exhaustive checks passed |

## Hints before solutions

1. At outer position j, test earlier positions in ascending order. Stop counting when the function returns.
2. State exactly what `seen` contains before the membership test. Keep “no previous duplicates” as a separate clause.
3. The triangular sum counts comparisons, not elapsed time. A container call may perform multiple comparisons.
4. Which information did a plain set discard? Store just enough to restore the required output.
5. Locate the forgotten key. Decide whether the allowed duplicate horizon can change.
6. A local proof assumes sequential execution. Find the gap between checking and performing a consequential action.

## 1. Trace

| j | Current value | Pairwise comparisons at this step | Set membership result |
| ---: | ---: | --- | --- |
| 0 | 4 | 0 | Absent |
| 1 | 9 | 4 vs 9: 1 comparison | Absent |
| 2 | 1 | 4, 9 vs 1: 2 comparisons | Absent |
| 3 | 7 | 4, 9, 1 vs 7: 3 comparisons | Absent |
| 4 | 9 | 4 vs 9, then 9 vs 9: 2 comparisons | Present |

Both return `True`. The baseline performs 8 equality comparisons. The remembered-state procedure performs 5 membership calls and 4 insertion calls. These are abstract calls; the trace does not imply only 5 equality comparisons inside a real set.

## 2. Proof and bug

Before processing position k, the set contains exactly the keys at positions below k. If execution has reached this point without returning, those earlier keys are distinct. Empty initialization satisfies this. A successful membership test implies an earlier matching position; an unsuccessful test permits adding the new value while preserving distinctness and exact membership. After the last unsuccessful test, the entire input is distinct. The loop consumes one item per iteration from a finite input, so it terminates.

If insertion precedes membership, `[8]` inserts 8 and immediately finds it, even though the required different position does not exist. The invariant no longer describes an exclusively earlier prefix at the test. A returned positive must have a witness consisting of two distinct positions.

## 3. Cost and assumptions

For 100 distinct values: 100×99/2 = 4,950 comparisons. For 1,000: 1,000×999/2 = 499,500. The ratio is 100.909…, rather than exactly 100, because the lower-order term still contributes at finite n.

For expected linear total work, assume constant-cost keys/equality/hashing, an appropriate hashing model, controlled load, and a resizing policy whose costs amortize across insertions. Also assume the keys maintain their identity while stored. The abstract membership count is at most n. It does not bound the number of actual equality comparisons by n: collisions can require examining multiple candidates. A constant-hash chained representation is a counterexample to unconditional linear time.

## 4. Return indices

Store a map `first_index[key] = earliest processed position`. Before position j, the map associates each earlier key with its first index. Check membership before inserting. When present, return `(first_index[x], j)`; otherwise insert j. The example returns `(1, 4)` using zero-based positions.

Because this procedure terminates on its first repeated key, all earlier keys are still distinct. Its first-index convention is unambiguous. If requirements change to all repeated pairs, a single index per key will not preserve enough information; output size may itself be quadratic. Returning one witness retains expected O(n) total time and O(n) extra entries under the same map assumptions as the set. No-match inputs return `None`.

## 5. Bounded memory

Before the last key in `[1, 2, 3, 1]`, a previous-two-items cache contains 2 and 3. It misses the duplicate 1. Legitimate alternatives include:

- Define a last-two-items question explicitly, accepting that older repeats are outside scope.
- Permit external exact storage that retains earlier keys and defines its lookup/durability guarantees.
- Restrict IDs to a small known universe and allocate membership flags for that universe.
- Permit replaying an immutable stored input and compare each new position against earlier positions, trading time and input access for auxiliary memory.

These alternatives change different assumptions. “Use a hash” alone does not create unlimited exact history in fixed memory. A probabilistic summary would require a specified error model; no such summary is implemented or analyzed here.

## 6. Duplicate business effects

Possible timeline: worker A checks absent; worker B checks absent; A pays; B pays; both record the ID. The membership set may end up containing a single key despite two payments. The final set contents cannot prove that only one effect occurred.

A stronger intended invariant is “For each business operation key, at most one committed payment effect occurs.” Its scope must include the durable state and payment boundary, retries, and failures. A coordination mechanism, atomic constraint, or idempotency contract must be chosen and checked in S03/S04 and C01. This answer intentionally does not claim that putting a lock around one process solves cross-process or external effects.

## Assessment criteria

| Capability | Evidence of a useful answer |
| --- | --- |
| Formulation | Defines equality, distinct positions, empty input, and output shape |
| Derivation | Identifies repeated prefix membership and the state needed to answer it |
| Correctness | Names the program boundary and handles initialization, preservation, both returns, and termination |
| Analysis | Counts an explicit operation and qualifies expected/amortized and key-size assumptions |
| Transfer | Explains a changed contract and an invalid extension of the local proof |

No learner score is recorded. If a step is unclear, revisit that step using a three-element input and manually inspect the state before each test.

## Reproduction appendix — executed checks

The following standard-library-only block is the executed validation code. It checks all sequences of lengths 0 through 7 over `{0,1,2}`: 3,280 inputs. The oracle uses frequency counting, distinct from the two detection procedures. Assertions verify the remembered-state invariant on every processed prefix. Additional tests check a one-bucket collision model, the insert-before-check bug, the forgetting counterexample, and arithmetic. This is a bounded correctness check, not a performance benchmark or evidence for all possible keys.

```python
from itertools import product
from collections import Counter

def pairs(a):
    comparisons = 0
    for j in range(len(a)):
        for i in range(j):
            comparisons += 1
            if a[i] == a[j]:
                return True, comparisons
    return False, comparisons

def seen_check(a):
    seen = set()
    for k, x in enumerate(a):
        assert seen == set(a[:k]) and len(seen) == k
        if x in seen:
            return True
        seen.add(x)
    return False

def witness(a):
    first = {}
    for j, x in enumerate(a):
        if x in first:
            return first[x], j
        first[x] = j
    return None

cases = 0
for n in range(8):
    for a in product(range(3), repeat=n):
        oracle = any(count > 1 for count in Counter(a).values())
        assert pairs(a)[0] == seen_check(a) == oracle
        w = witness(a)
        assert (w is not None) == oracle
        if w is not None:
            i, j = w
            assert 0 <= i < j < n and a[i] == a[j]
        cases += 1
assert cases == 3280
assert pairs([4, 9, 1, 7, 9]) == (True, 8)
assert pairs([8, 3, 6, 3]) == (True, 5)
assert witness([4, 9, 1, 7, 9]) == (1, 4)
for n in (0, 1, 2, 10, 100, 1000, 2000):
    assert pairs(list(range(n))) == (False, n * (n - 1) // 2)

# Explicit one-bucket chained model; each contains scan checks keys.
# Append follows a confirmed miss, so no second search is needed.
bucket = []
checks = 0
for x in range(100):
    for y in bucket:
        checks += 1
        assert x != y
    bucket.append(x)
assert checks == 4950
assert 1 % 10 == 11 % 10 and 1 != 11

def insert_first_bug(a):
    seen = set()
    for x in a:
        seen.add(x)
        if x in seen:
            return True
    return False
assert insert_first_bug([8]) is True
assert pairs([8])[0] is False

def previous_two(a):
    recent = []
    for x in a:
        if x in recent:
            return True
        recent.append(x)
        recent = recent[-2:]
    return False
assert previous_two([1, 2, 3, 1]) is False
assert seen_check([1, 2, 3, 1]) is True
print(f"PASS: {cases} exhaustive inputs; traces, counts, witnesses, and counterexamples")
```

Source and review limits: R01 passages support the abstract foundations; all exercise inputs and calculations are original. No current Python hash implementation details were inspected, and no claim about its precise collision or resizing policy is needed for these checks. Audit A remains queued.

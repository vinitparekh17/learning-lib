# F04 — Hints, worked answers, and reproducible checks

| Field | Value |
| --- | --- |
| ID, revision, date | F04 answers · 1.0 · 2026-11-05 |
| Prerequisite | [F04 learning pack](SDE_F04.md) |
| Capability | Check the feature contract, ranking, update direction, step size, and evaluation boundary |
| Source check | R02 passage locators in the core pack. Numerical cases and derivations are original. |
| Experiment status | Executed the Python 3 checks below on the constructed inputs. |

## Hints

1. The query assigns one unit of weight to the second coordinate.
2. A positive scaling factor appears in both the numerator and the denominator of cosine.
3. A deterministic function returns the same output when given the same input.
4. Evaluate the derivative at the *current* weight before taking the second step.
5. Compare distances to the optimum on both sides of the step.
6. Separate the task of finding supporting evidence from the task of estimating minutes.

## 1. Shape and coordinate order

Multiplying each document row by (0, 1)ᵀ returns its payment-reference count. The output is (0, 4, 2)ᵀ, a 3 × 1 column indexed by passage. If a caller says it requested payment evidence but receives (2, 3, 0)ᵀ, it may have emitted (1, 0)ᵀ. Check the encoded query, the stored column order, and the expected output for a passage with only payment references. Shape validation alone accepts both query vectors.

## 2. Ranking and missing direction

For delivery q = (1, 0)ᵀ, the raw scores in document order are 2, 3, 0. Their descending order is B, A, C. Divide each by its document length and by the unit query length to obtain 1, 3/5, 0. Cosine orders them A, B, C. After tripling B its vector is (9, 12)ᵀ, its length is 15, and its raw score is 9. Its normalized score is 9/15 = 3/5. Both rankings retain their respective orders, although B's raw lead grows.

A zero query provides no direction. One defensible policy is to return an explicit “insufficient query features” status and ask for a usable reference type. Include that outcome when computing the fraction of all queries served successfully. Assigning a numerical score to every passage would require a separate fallback rule and a way to evaluate its relevance.

## 3. A transformation that loses information

T times A gives 1 × 2 + 1 × 0 = 2. T times C gives 1 × 0 + 1 × 2 = 2. For any function g using only the transformed count, g(2) must serve both passages. Delivery evidence occurs in A and is absent from C. Consequently at least one answer must be wrong if g always chooses present or absent. Keep the delivery coordinate or the original reference data if this distinction is part of the contract. The total still answers a question about overall volume.

## 4. A second update

After the first step w = 3/2. The current derivative is 5(3/2 − 2) = −5/2. With η = 1/10 the next weight is 3/2 + 1/4 = 7/4. Predictions of 7/4 and 7/2 minutes have residuals −1/4 and −1/2. The mean of their squared residuals is (1/16 + 1/4)/2 = 5/32 minutes². Substituting in (5/2)(7/4 − 2)² gives the same result. A fresh gradient matters because the remaining error shrinks at each step.

## 5. An overshoot

From w = 1 the slope is −5. A step size of 1/2 sends the weight to 7/2, which lies 3/2 from the optimum. The new loss is (5/2)(3/2)² = 45/8 minutes², larger than the initial 5/2. Increasing w from 1 initially moves downhill. The step travels past the minimum far enough to lose the whole gain. Under repeated updates the error multiplier is 1−5η = −3/2, so the weight alternates sides and its distance grows. In the worked convention, dividing the entire loss by two would also halve each gradient and double the corresponding stable step-size interval.

## 6. Two separate acceptance checks

In the constructed holdout, a two-page invoice took two minutes. Training reduced squared loss from 5/2 to 5/8, yet held-out squared error went from 0 to 1. For a workload claim, freeze a representative test population before selecting weights. Compare predictions with independently recorded active minutes, report mean absolute error by supplier type, and check the fraction of critical cases underestimated beyond an agreed tolerance. Decide beforehand what improvement and tolerance the workflow requires.

A higher top score can also reward repeated words without finding an applicable source. Use the same frozen queries, candidate passages, and eligibility rules for both rankers. Have blinded reviewers check the selected passage against the original invoice and required fact. Count cases with missing evidence and cases the ranker declines. A decision can then use the fraction of all eligible queries with verified supporting evidence and the observed cost of review.

**Self-assessment.** A complete solution preserves the document and feature axes, explains the scale invariance and zero case, derives the next weight using the current slope, and names a held-out outcome for each task. The numerical checks below can be run after attempting the exercises.

## Reproduction

```python
from fractions import Fraction as F
from math import isqrt

docs = [(2, 0), (3, 4), (0, 2)]
def dot(x, y):
    assert len(x) == len(y)
    return sum(a*b for a, b in zip(x, y))

def cosine(x, y):
    squared = dot(x, x) * dot(y, y)
    if squared == 0:
        return None
    root = isqrt(squared)
    assert root*root == squared  # exact roots in these examples
    return F(dot(x, y), root)

q = (1, 0)
assert [dot(d, q) for d in docs] == [2, 3, 0]
assert [dot(d, (0, 1)) for d in docs] == [0, 4, 2]
assert [cosine(d, q) for d in docs] == [1, F(3, 5), 0]
assert cosine((9, 12), q) == F(3, 5) and dot((9, 12), q) == 9
assert cosine((0, 0), q) is None
assert dot(docs[0], (1, 1)) == dot(docs[2], (1, 1)) == 2

def loss(w):
    return sum((w*x-y)**2 for x, y in [(1, 2), (2, 4)]) / F(2)
def step(w, eta):
    return w - eta * 5*(w-2)

w1 = step(F(1), F(1, 10))
w2 = step(w1, F(1, 10))
assert (w1, w2) == (F(3, 2), F(7, 4))
assert [loss(w) for w in (1, w1, w2, 2)] == [F(5, 2), F(5, 8), F(5, 32), 0]
assert loss(step(F(1), F(1, 2))) == F(45, 8)
assert (1*2-2)**2 == 0 and (w1*2-2)**2 == 1
for k in range(51):
    eta = F(k, 100)
    for w in [F(-1), F(1), F(3)]:
        assert loss(w) == F(5, 2)*(w-2)**2
        assert (loss(step(w, eta)) < loss(w)) == (0 < eta < F(2, 5))
        h = F(1, 100)
        assert (loss(w+h)-loss(w-h))/(2*h) == 5*(w-2)
print('All F04 checks passed.')
```

The symmetric difference equals the derivative exactly here because the loss is quadratic. The algebra in the learning pack establishes the step-size interval for every starting weight away from the optimum. The finite sweep checks the implementation on both sides of each boundary.

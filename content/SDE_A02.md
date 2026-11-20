# A02 — Attention and the Transformer mechanism

| Field | Value |
| --- | --- |
| ID / revision / date | A02 · 1.0 · 2026-11-09 |
| Prerequisites | F04 vectors, matrix products and fitted parameters; A01 information boundaries and evaluation |
| Capability developed | Calculate attention, identify allowed information flow and distinguish an operation check from a model-quality claim |
| Source-check status | R14, author-submitted arXiv v7: §§3.1–3.5 and §4 inspected; precise locators below |
| Experiment status | Constructed matrices and executed standard-library numerical checks; no training run or model benchmark |
| Companion | [Hints, worked answers and checks](SDE_A02_answers.md) |

## What changes a token's representation?

Suppose a document system represents each token occurrence with a vector. A token is an item in the model's input sequence; it need not coincide with a word. The same text fragment in two positions can need different representations because its surrounding information differs. Our question is narrower than whether a generated answer is correct: how can one row of numbers incorporate information from other rows?

We will implement a deliberately tiny operation. The numbers below are assigned, not learned from invoices. They have no calibrated meaning such as confidence or probability that a document is correct. That distinction follows F04's warning about interpreting geometric scores and A01's distinction between passing a constructed check and demonstrating generalization.

Use rows for token vectors. A matrix with n rows and d columns represents n positions with d features each. Multiplying a row by a projection matrix changes its coordinates. The projection parameters are shared across positions, but the resulting vectors depend on the input row. No diagnostic answer or prior familiarity with neural networks is assumed.

## The contract and shapes

For input X of shape n×d, define Q=XWQ, K=XWK and V=XWV. Queries Q and keys K have width dk; values V have width dv. We use the scaled dot-product rule from R14 §3.2.1, eq. 1, extended with an explicit allowed-position mask:

\[
S=QK^T/\sqrt{d_k},\qquad A=\operatorname{softmax}_{rows}(S+M),\qquad O=AV.
\]

M is zero for allowed pairs and negative infinity for forbidden ones. In the executable version we omit forbidden entries from the denominator instead of representing infinity. Each query must have at least one permitted key. An all-forbidden row is rejected as invalid input in our contract.

| Quantity | Shape | Meaning |
| --- | --- | --- |
| WQ, WK | d×dk | Shared query/key projections |
| WV | d×dv | Shared value projection |
| Q, K | n×dk | One query/key per position |
| V | n×dv | One value per position |
| S, M, A | n×n | Row i refers to query i; column j to key/value j |
| O | n×dv | One weighted result per query |

The transpose in QKᵀ aligns the feature coordinates. Entry Sij is the dot product of query i and key j, divided by √dk. These scores determine mixing weights; the corresponding value vectors supply what is mixed. Query, key and value are computational roles, not a claim that a token consciously asks a question.

For allowed scores s1,…,sm, softmax returns exp(sj)/Σ exp(sk). Exponentials are positive and normalization makes the row sum one. Equal scores produce equal weights. Adding the same constant to every allowed score changes neither the ratios nor the output. Subtracting the row maximum before exponentiating therefore avoids unnecessarily large exponentials without changing the mathematical result.

For this operation, each output is a convex combination of permitted values: each coordinate lies between their minimum and maximum. This property applies to AV before later projections, residual additions or other transformations. It is not a bound on the final model's output.

## Trace three positions by hand

Choose n=3, d=2, dk=1 and dv=2:

\[
X=\begin{bmatrix}1&0\\0&2\\1&1\end{bmatrix},\quad
W_Q=W_K=\begin{bmatrix}1\\0\end{bmatrix},\quad
W_V=\begin{bmatrix}1&0\\0&1\end{bmatrix}.
\]

Consequently Q=K=[1,0,1]ᵀ and V=X. Because dk=1, the scaling divisor is one. With all positions allowed,

\[
S=\begin{bmatrix}1&0&1\\0&0&0\\1&0&1\end{bmatrix}.
\]

Let e=exp(1) and Z=2e+1. The first row's weights are [e/Z,1/Z,e/Z], approximately [0.4223,0.1554,0.4223]. Its output is

\[
\frac eZ(1,0)+\frac1Z(0,2)+\frac eZ(1,1)
=\left(\frac{2e}Z,\frac{2+e}Z\right)
\approx(0.8446,0.7330).
\]

The second query is zero. All its scores are zero, so its weights are thirds and its output is the mean (2/3,1). The third query equals the first, so its output also equals the first. Different original rows can receive the same attention output; the operation does not guarantee that every position remains distinguishable.

Now change only the last value from (1,1) to (1,7), leaving Q and K fixed. The first and third output's second coordinate each increases by 6e/Z; the second output's second coordinate increases by 2. We can realize this change by altering X's last second coordinate: our chosen WQ and WK ignore that coordinate. This test isolates value flow from score changes. With other projections, the same input change could alter Q and K too.

## A mask changes what information may flow

For a causal version allow key j only when j≤i. The first query can use only position 1. The second can use positions 1 and 2. The third can use all three.

| Query row | Permitted keys | Weights across all three columns | Output |
| --- | --- | --- | --- |
| 1 | 1 | [1,0,0] | (1,0) |
| 2 | 1,2 | [1/2,1/2,0] | (1/2,1) |
| 3 | 1,2,3 | [e/Z,1/Z,e/Z] | (2e/Z,(2+e)/Z) |

The mask is applied before normalization. If you normalize all three scores and merely zero forbidden weights afterward, a row may sum to less than one. For row 2 that faulty procedure produces (1/3,2/3), not (1/2,1). It has silently changed the operation.

Under the causal mask, the last-value perturbation leaves outputs 1 and 2 unchanged, while output 3 changes. This follows because their allowed terms contain neither K3 nor V3, and their own queries are unchanged. It is a local guarantee of this layer with fixed projections. In a larger network, earlier input representations must themselves have been computed without future leakage. A causal final layer cannot repair representations that already incorporated future targets.

For another test, remove the connection from query 3 to key 2. Its remaining equal scores yield [1/2,0,1/2] and output (1,1/2). Only row 3 changes in this one operation. In later layers, its changed representation may affect any positions permitted to use it.

Padding and causality are different constraints. Padding marks absent sequence items; causal masking marks future positions relative to a prediction. A combined mask must preserve a valid key for every real query or specify another explicit policy. Do not silently interpret an undefined all-masked row as a useful representation.

## Position, multiple heads and the surrounding network

R14's architecture places attention within encoder/decoder stacks with residual connections, normalization and position-wise feed-forward layers. It projects multiple attention heads, concatenates them and applies an output projection. Its decoder combines causal self-attention with attention to encoder outputs. It adds positional information to embeddings and maps decoder representations to token probabilities. These are properties of the cited historical architecture, not a specification of every current model.

Here is a shape-level extension of our own example. With two heads, each producing a 3×2 matrix, concatenate across features to obtain 3×4. A 4×2 output projection returns 3×2, which could be added to the original X. Concatenating across rows would produce 6×2 and would not preserve one output per input position. Different heads need not correspond to named human concepts, and more heads do not guarantee better task performance.

Without positional inputs or an order-sensitive mask, our operation cannot distinguish a permutation of the sequence from the corresponding permutation of its outputs. If P permutes rows, then X becomes PX, the score matrix becomes PSPᵀ, and row softmax followed by the permuted values produces PO. This is an algebraic property, checked over all six permutations of our three rows. It explains what position information must change: the computation needs a way to represent order when order matters to the task. It does not imply that an orderless set-processing task always needs positional inputs.

For cross-attention, query and memory lengths can differ. Three query rows attending to five key/value rows produce a 3×5 weight matrix and three output rows. The number of keys must equal the number of values; dk must match between queries and keys. The output width is dv, not the number of memory items. These shape checks catch interface errors before any semantic interpretation.

## Training and inference use different available inputs

Consider a separate next-token task whose desired output is [A,B,C]. A shifted training input is [START,A,B], paired with targets [A,B,C]. A causal row can use its current shifted input and earlier rows without seeing its own target through that input path. All these known training-input rows can be evaluated together under the mask. Supplying [A,B,C] unshifted as input for predicting [A,B,C] would instead expose the answer at each diagonal connection.

Parameter fitting adjusts projection and other model weights using a loss and an update rule, as F04 introduced. During the inference procedure considered here, weights are fixed: begin with START, obtain a token, append it, and use that actual prefix for the next prediction. The correct next token is not supplied by a teacher. Evaluating against known prefixes and generating from one's own prefixes answer different questions; A01's evaluation discipline still applies. No training or decoding implementation was executed in this pack.

Attention weights normalize over available positions. Output token probabilities normalize over a vocabulary after another transformation. Neither normalization alone establishes factual correctness, permission to act or supporting evidence. Our numeric operation would mix values from fabricated text just as readily as from verified text. A03 will separately evaluate retrieval and answer support.

## Where sequence length enters the cost

Count the explicit dense algorithm, one head and one sequence, ignoring batch size and datatype overhead. QKᵀ performs n² dot products of width dk, costing order n²dk multiply/add work. AV costs order n²dv. An explicitly stored score or weight matrix contains n² scalars. Doubling n at fixed widths quadruples those pair counts: n=3 has 9 positions, n=6 has 36. The causal mask has n(n+1)/2 allowed pairs, but computing a full matrix and masking it afterward still does dense work.

The projections additionally depend on n and feature widths. These counts do not establish runtime, memory traffic, optimizer storage or the allocation strategy of an optimized implementation. They also do not describe the cost of one incremental generation step automatically. A04 will examine serving and retained state in more detail.

Choose a full-context or causal operation according to what information the task may use, not just which scores look better. Restricting context can reduce candidate interactions but can remove needed dependencies. To justify a change, compare complete task outcomes under the same information contract and measure actual resources. A faster result obtained by leaking future labels is not an improvement for that contract.

## Practice

1. Derive Q, K, V, S and every unmasked output from the supplied X and projections. Explain what the softmax axis means.
2. Derive the causal outputs. Remove only row 3's connection to key 2, then compare with the erroneous mask-after-softmax procedure for row 2.
3. Change X3 from (1,1) to (1,7). Identify which unmasked and causal outputs change and by how much. State why the claim needs the chosen projections.
4. Give shapes for three queries attending to five values with dk=4 and dv=2. Then describe the two-head concatenation/projection example and a residual shape error.
5. Explain the [START,A,B] input/target arrangement, what goes wrong with unshifted targets, and why a later causal mask cannot undo earlier leakage. Distinguish fitting from fixed-weight generation.
6. Derive dense and allowed-pair counts for n=3 and n=6. Explain the permutation test, then propose a task evaluation that could reject a cheaper context restriction despite passing all arithmetic checks.

## Reference card, evidence and open questions

Write shapes → score query/key pairs → exclude forbidden pairs → normalize each query row → mix values → check the downstream shape. Specify whether inputs already contain future information. Separate weights over positions from probabilities over tokens and from verified truth.

| Basis | Inspected locator | Scope |
| --- | --- | --- |
| R14, Vaswani et al., 2017; inspected arXiv v7 dated 2023-08-02 | [Versioned text](https://arxiv.org/html/1706.03762v7), §3.2.1 eq. 1; §§3.2.2–3.2.3 | Scaled attention, learned projections and masking |
| R14, same version | §§3.1, 3.3–3.5; §3 opening and §4 | Architecture context, shifted decoder inputs, position information and complexity discussion. No reported benchmark result adopted. |
| Original derivations and constructed inputs | This pack and companion executable checks | Numeric trace, mask counterexamples, perturbations, permutation property, shape/count calculations and proposed tests |
| Continuity | F04 matrix/parameter bridge; A01 leakage/evaluation boundaries | Previously saved prerequisites, not new measurements |

R14's detailed mechanism is now passage-checked beyond the original catalog entry. The toy projections are not trained weights and the three vectors are not a tokenizer or language model. The checks cover a single deterministic attention operation without dropout, normalization, feed-forward layers or optimization. Real tokenization, positional scheme, masks, precision, architecture, resource use and task quality require application evidence. No learner mastery is inferred. Next is A03: retrieval, external knowledge and provenance.

## Revision history

- 1.0 — 2026-11-09. Three-position attention trace, mask and leakage counterexamples, architecture context and six exercises with separate checks.

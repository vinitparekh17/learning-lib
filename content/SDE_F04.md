# F04 — Vectors, transformations, and optimization

| Field | Value |
| --- | --- |
| ID, revision, date | F04 · 1.0 · 2026-11-05 |
| Prerequisites | Arithmetic and elementary algebra. The slope derivation starts from subtraction and division. F02 supplies the distinction between a score and an event probability. |
| Capability | Trace a similarity score to its inputs, check a model update by hand, and decide what evidence would justify using it. |
| Source check | Selected passages of the authors’ January 2024 draft of *Mathematics for Machine Learning* (R02), listed below. |
| Experiment status | Original hypothetical cases. Exact arithmetic and ranking checks executed. |
| Companion | [Hints, worked solutions, and executable checks](SDE_F04_answers.md) |

## Which document should the reviewer see first?

A reviewer needs a delivery reference to verify an invoice. Suppose each passage is represented by two counts in a fixed order: delivery references first, payment references second. Passage A contains two delivery references and no payment references. Passage B contains three delivery references and four payment references. If the reviewer can open just one passage, should the service show A or B?

Two plausible requirements lead to different answers. A reviewer assembling every available delivery reference might prefer the passage with the larger raw count. A reviewer trying to find a passage *devoted* to delivery might prefer one whose references all concern delivery. The arithmetic below makes each choice explicit. A real reviewer's success would also depend on whether the references were correct, distinct, and from the right invoice. The counts are invented so we can inspect what the calculation preserves.

## Write the shape beside each quantity

A **scalar** is a single number. A **vector** is an ordered collection of coordinates. Here a document vector has two coordinates. Write vectors as columns, so A = (2, 0)ᵀ has shape 2 × 1. The superscript T means transpose, which swaps rows and columns. Put documents in rows of a matrix D. Its first row is [2, 0], its second is [3, 4], and its third is [0, 2] for a payment-only passage C. The column vector q = (1, 0)ᵀ describes the delivery query.

To calculate Dq, take one row at a time. Multiply corresponding coordinates by the query weights and add. The first row gives 2 × 1 + 0 × 0 = 2. The second gives 3 and the third gives 0. This row-by-column calculation is a **dot product**. In one multiplication we have a score for each passage.

| Quantity | Shape | Meaning of one entry |
| --- | --- | --- |
| D | 3 × 2 | Count for one passage and one reference type |
| q | 2 × 1 | Query weight for one reference type |
| Dq | 3 × 1 | Score for one passage |
| DᵀD | 2 × 2 | Sum across passages of products of two feature counts |

The shared dimension tells you which coordinate you sum over. The dimensions that survive identify the output. Try writing qᵀD with the shapes above. Its inner dimensions are 2 and 3, so the intended multiplication fails a shape check. A subtler bug survives that check. If the query encoder puts payment first, q = (1, 0)ᵀ now describes a different request even though every multiplication still runs. A one-feature test query with a known result catches this disagreement. A production interface should record the feature order and the encoder version used on each side.

A matrix can also *change the representation*. Apply the row matrix T = [1, 1] to each document column. The result is one scalar, the total number of references. Passages (2, 0)ᵀ and (0, 2)ᵀ both become 2. Once the service retains only that total, even a perfect downstream scoring function of the total must give those two passages the same score. Before accepting a compact representation, identify a pair of inputs your application must distinguish and take both through the transformation.

## Compare raw overlap with direction

The Euclidean norm is a vector's length. Square its coordinates, add them, and take the square root. Passage B has length √(3² + 4²) = 5. Its unit vector is (3/5, 4/5)ᵀ. Dividing each coordinate by the same positive length preserves its proportions and makes its length one. For nonzero q and d, the dot product of their unit vectors is the cosine of the angle between them.

| Passage | Raw score against q | Length | Cosine against q |
| --- | ---: | ---: | ---: |
| A (2, 0) | 2 | 2 | 1 |
| B (3, 4) | 3 | 5 | 3/5 |
| C (0, 2) | 0 | 2 | 0 |

Raw overlap ranks B above A. Cosine ranks A above B. Which result is defensible depends on what makes evidence useful to the reviewer. Try duplicating every reference in B. Its raw score doubles. Its unit vector still has coordinates (3/5, 4/5). In general, multiplying a nonzero document by a positive scalar multiplies its dot product and norm by that same scalar, which cancels in the cosine. This invariance helps when document length is a nuisance. It discards information when the magnitude represents multiple independently verified pieces of evidence. Deduplication and verification are separate design choices.

An empty passage maps to (0, 0)ᵀ. Its norm is zero, so cosine would require dividing by zero. Define what the application does here. One policy is to mark the passage unscorable, exclude it from ranking, and retain its ID in coverage reports. Silently dropping such cases from evaluation can flatter a system that struggles on empty or poorly parsed documents. F03's denominator rule applies.

The same shape arithmetic applies to learned embeddings, where coordinates are learned from training data and need not have names that a reviewer can interpret. A cosine of 0.6 expresses a geometric relationship under the chosen representation. Estimating a 60% chance that the passage answers a question would require a defined event and labeled outcomes, as in F02. A02 will reuse dot products when comparing queries and keys. A03 will return to ranking passages and checking whether the selected passage supports an answer.

## Fit one parameter and inspect its units

Suppose the same service wants to estimate active review time. Let x count pages and y measure review minutes. Choose the model ŷ = wx, where w is minutes per page. The model assumes proportionate time and a zero intercept. An intake task with a fixed setup cost could violate that assumption. Use two constructed training cases, (x, y) = (1, 2) and (2, 4). The design matrix now has shape 2 × 1, with rows [1] and [2]. Multiplying by the single weight gives two predictions.

Start at w = 1. The predictions are 1 and 2 minutes. Subtract the targets to get residuals −1 and −2 minutes. Average their squares to obtain a **mean squared error** of (1 + 4)/2 = 2.5 minutes². Squaring prevents an underestimate from canceling an overestimate and makes a two-minute error contribute four times as much as a one-minute error. A stakeholder who cares mainly about missed deadlines may want a different evaluation measure.

Keeping w symbolic exposes the whole loss curve:

$$L(w) = [(w-2)^2+(2w-4)^2]/2 = (5/2)(w-2)^2.$$

The square reaches zero at w = 2, so this dataset has an exact fit. Knowing that answer makes this an effective debugging case. We can check whether the update heads toward a known minimum and calculate how far it goes.

## Derive the slope before choosing a step

Perturb w by a small nonzero amount h. Expanding the square gives

$$L(w+h)-L(w) = 5(w-2)h+(5/2)h^2.$$

Divide by h to get the change in loss per unit change in w. The quotient is 5(w−2) + (5/2)h. As h approaches zero the last term vanishes. The **derivative** is therefore L′(w) = 5(w−2). At w = 1 the slope is −5. Increasing w a little lowers the loss. After crossing w = 2 the slope becomes positive and a further increase raises the loss. With several weights, the gradient collects one partial derivative per weight, each calculated with the other weights fixed. Here one scalar gives the entire gradient.

Gradient descent uses the update w_new = w − ηL′(w), with a positive step size η. For η = 0.1, the first step goes from 1 to 1.5. The two predictions become 1.5 and 3. Their residuals are −0.5 and −1, so the new mean squared error is (0.25 + 1)/2 = 0.625 minutes². Verify the loss both ways, from the predictions and from the simplified quadratic. Agreement catches mistakes such as missing the division by two.

What makes this particular step safe? Subtract the optimum from both sides of the update:

$$w_{new}-2=(1-5η)(w-2).$$

Each update scales the distance from the optimum by |1−5η|. Starting away from the optimum, the loss decreases exactly when that factor is less than one, or 0 < η < 0.4. At η = 0.2 the update lands on the optimum in one step. At η = 0.4 it bounces to the other side at the same distance. A larger step can increase the loss even though the slope was correct. This range comes from the curvature of this specific quadratic and the chosen units. Changing the loss scaling changes its derivative and the suitable step size.

## Decide whether the fit earns a trial

Consider one invented held-out two-page invoice that takes two minutes because its evidence is already assembled. At w = 1 the prediction is exact. After the training step, w = 1.5 predicts three minutes and the squared error rises from zero to one minute². That single case establishes a counterexample to the claim that every new case improves when training loss falls. Estimating an average effect across new invoices requires a representative evaluation set.

For the retrieval choice, compare raw overlap and cosine on identical queries and passage collections. Have a reviewer judge whether each selected passage contains the required source evidence. Include duplicates, mixed-topic passages, and empty inputs. For time prediction, compare against a simple baseline on later invoices or held-out suppliers, according to the intended deployment. Record absolute errors in minutes alongside squared loss, and separate underestimates on deadline-sensitive cases. A01 will revisit how fitting, validation, and final evaluation answer different questions.

## Practice on paper

1. Calculate the three scores when q = (0, 1)ᵀ. Give the shape of Dq and explain a feature-order bug that this query could expose.
2. Rank A, B, and C by raw and normalized overlap for the original delivery query. Repeat after tripling B. Give an explicit policy for a zero-vector query.
3. Apply T = [1, 1] to A and C. Can any function of the resulting scalar alone recover which passage contains delivery evidence? Justify your answer.
4. Starting at w = 1, calculate a second gradient step after the worked first step, using η = 0.1. Verify its loss from residuals and from the closed form.
5. Try η = 0.5 from w = 1. Compare the new loss with the old loss. Explain why the sign of the gradient alone cannot select a step size.
6. A teammate asks to deploy based on lower training loss and a higher average top-ranked cosine. Use the held-out counterexample and propose a separate acceptance check for each task.

## Reference card and evidence

Write the coordinate meaning and shape beside every input. For a score, test what happens when you duplicate a document or erase its features. For an update, write down the target, units, loss, slope, step size, and next loss. For a deployment decision, name the outcome on unseen cases that would change your choice.

| Claim or calculation | Source and inspected locator | Scope |
| --- | --- | --- |
| Product dimensions and row-by-column sum | R02 §2.2, printed pp. 22–23, equations 2.13–2.14 | Matrix multiplication |
| Euclidean length, dot product, angle | R02 §§3.1–3.2.1, p. 72, equations 3.4–3.5, and §3.4, p. 76, equations 3.24–3.25 | Cosine uses two nonzero vectors |
| Derivative as limiting slope | R02 §5.1, pp. 141–142, definitions 5.1–5.2 | Scalar differentiable function |
| Gradient descent update | R02 §7.1, p. 228, equations 7.5–7.6 | Book uses a row gradient and transposes it for a column update. The scalar case has one component. |
| Document ranking, loss curve, stable step interval, held-out case | Original constructed examples above and checks in the companion | Conditional arithmetic. Actual relevance labels, time distributions, and operating costs require application evidence. |

R02 is Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*, Cambridge University Press, 2020. Locators refer to the author-hosted draft dated 2024-01-15. [Author site](https://mml-book.github.io/) · [Author PDF](https://mml-book.github.io/book/mml-book.pdf)

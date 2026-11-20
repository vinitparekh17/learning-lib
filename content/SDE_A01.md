# A01 — Learning, generalization, and distribution change

| Field | Value |
| --- | --- |
| ID / revision / date | A01 · 1.0 · 2026-11-09 |
| Prerequisites | F02 expectations and loss, F03 comparison design, F04 fitted weights; optional bridge below |
| Capability developed | Design a comparison that tests the intended deployment instead of rewarding memorization or future information |
| Source-check status | R13 Python edition and author labs; R02 January 2024 draft. Inspected locators below. |
| Experiment status | Original constructed datasets; exact Python arithmetic and split checks executed. No real model benchmark or deployment trial. |
| Companion | [Hints, worked answers and checks](SDE_A01_answers.md) |

## What does a successful fit buy us?

The invoice service wants to predict active review minutes when a document arrives. A schedule based on these estimates could help allocate reviewer capacity. It could also repeatedly underestimate difficult work. Before choosing a model, specify the decision time, what is observable then, and what outcome will eventually be measured.

Our input x is the page count available at intake. The target y is active review minutes measured under one declared review workflow. Waiting in a queue is excluded from y. Changing reviewer tools could change y even for the same document. These are design choices, not facts about a deployed service.

A **feature** is an input available to the predictor. A **label** is the outcome used to judge a prediction. A **parameter** is a number fitted from training examples. A **hyperparameter** chooses aspects of that fitting procedure, such as penalty strength. A **baseline** is a credible simple alternative evaluated on the same cases. Learning here means choosing a predictor from data; generalization concerns its behavior on cases outside that fitting process.

F04 showed that reducing training loss can worsen an unseen prediction. A01 develops the missing evaluation design. F02 supplies the loss/denominator distinction, and F03 supplies the requirement to compare the same population under a declared protocol. No prior diagnostic answer is assumed.

## Fit a small predictor before a large one

Reuse F04's zero-intercept model, predicted minutes = wx. Its strong assumption is that time grows proportionally with pages, without fixed setup time. Use two invented training cases: (1 page, 2 minutes) and (2 pages, 4 minutes).

The squared loss for one case is (prediction − outcome)². The mean squared error (MSE) averages it over cases. Here:

\[
L(w)=\frac{(w-2)^2+(2w-4)^2}{2}=\frac52(w-2)^2.
\]

Thus w=2 minimizes training MSE, with value zero. A constant baseline predicts the training mean, 3 minutes, for every case; its training MSE is 1 minute². Squared errors penalize large deviations heavily. Also report mean absolute error (MAE), in minutes, so an operator can interpret the scale. Neither metric alone measures whether scheduling actually improves customer outcomes.

Now lock both predictors and evaluate two invented validation cases, (1,1) and (2,2). The fitted predictor gives [2,4], so MSE is (1+4)/2=2.5. The constant baseline gives [3,3], so MSE is (4+1)/2=2.5 as well. A perfect training fit did not beat the baseline here. The validation set differs in its relation between pages and time; that was deliberately constructed, not discovered empirically.

The training objective is an average over observed fitting cases. The desired deployment risk is an expectation of loss over the intended future population, with the predictor fixed. An average on held-out data estimates that target only to the extent that the sampling and information conditions match it. An unseen row is not necessarily a new independent document, supplier or time period.

## Penalize flexibility, then test the choice

Consider a penalized objective J(w)=L(w)+λw², with λ≥0. Differentiate the quadratic: J′(w)=5(w−2)+2λw. Setting this to zero gives

\[
w_\lambda=\frac{10}{5+2\lambda}.
\]

The positive curvature 5+2λ makes this the unique minimum. For λ=0, 2.5 and 7.5, the weights are 2, 1 and 0.5. In this example units and loss scaling are fixed; multiplying features or replacing mean loss by sum loss changes the numerical meaning of λ. The penalty is a preference for smaller weights, not evidence that smaller weights are always better.

| Candidate | Weight / prediction rule | Training MSE | Validation MSE |
| --- | --- | ---: | ---: |
| Constant baseline | Always 3 | 1 | 2.5 |
| λ=0 | 2x | 0 | 2.5 |
| λ=2.5 | x | 2.5 | 0 |
| λ=7.5 | 0.5x | 5.625 | 0.625 |

Select λ=2.5 using this validation set. It has worse training fit but better validation fit among these candidates. This is not a general recommendation for λ=2.5. If deployment followed y=2x instead, the unpenalized predictor would be preferable. Regularization can trade fit for stability, but it cannot repair a label that contains future information or a test set chosen for easy cases.

Reserve a separate final test with cases (3,3), (4,4), which has not influenced the candidate grid or selection. The frozen selected model has MSE 0 there; the constant baseline has MSE 0.5. These tiny exact examples illustrate the bookkeeping, not an estimated production advantage. If the final cases instead followed y=2x, the selected model's MSE would be 12.5. That counterexample exposes the missing transport assumption.

For a real study, use training folds to fit parameters and development folds to choose features, penalties and other settings. Fit normalization, missing-value handling and feature selection inside each training fold. Reserve an outer test for evaluating the complete selection procedure. Once its results influence changes, it is development evidence for those changes. Calling it “test” does not restore independence. A final refit on all development data is a new fitted model; evaluate that actual frozen model rather than reusing earlier numbers as though its weights were unchanged.

## Zero error from the wrong split

Here is a separate, deliberately adversarial dataset. Four underlying documents each have two near-identical revisions with the same assigned target. Each document has two pages. Metadata are:

| Document | Organization | Template family | Revision IDs | Assigned minutes |
| --- | --- | --- | --- | ---: |
| D1 | A | X | D1r1, D1r2 | 2 |
| D2 | A | Y | D2r1, D2r2 | 4 |
| D3 | B | X | D3r1, D3r2 | 6 |
| D4 | B | Z | D4r1, D4r2 | 8 |

A lookup predictor remembers training labels by document ID and falls back to the training mean for an unknown document. Put each r1 in training and each r2 in validation. All four validation predictions are exact. This is one possible row-split allocation, not the expected result of every random split. It tests recognition of previously labeled documents, not prediction for new documents at intake. The use of prior labels also needs to match what is available at decision time.

Now train on both revisions of D1 and D2, and evaluate both revisions of D3 and D4. Every validation document is unseen. The fallback is 3, giving MSE ((6−3)²+(8−3)²)/2=17. The constant baseline has the same MSE. The zero-error advantage vanished. Duplicating each target does not produce twice as many independent documents.

Organization separation is still not template separation: X appears in both A and B. This is not automatically an error. New customers may use familiar templates. But it cannot establish performance on unseen templates. Grouping by the pair (organization, template) also fails to separate either individual attribute. If both organization and template must be unseen, group connected components of the graph whose edges join shared organizations or shared template families. Here the X connection joins A and B; all four documents belong to one component. There is no nonempty disjoint train/test partition satisfying both constraints. Collect more disconnected groups or narrow the claim; do not manufacture independent evidence by splitting the component.

## Let deployment choose the holdout

| Intended claim | Proposed holdout | What it still cannot establish |
| --- | --- | --- |
| New documents from existing suppliers | Later intake period; no document family crosses partitions; features reconstructed as of intake | Performance for unknown suppliers or changed review procedures |
| New suppliers, possibly familiar templates | Entire organizations held out; retain all revisions of each document together | Unseen-template performance if templates overlap |
| New template families | Entire template families held out | New-organization behavior unless also separated |
| Both unseen organizations and templates | Disconnected organization/template components held out | Future stability or representativeness of missing components |

For a temporal evaluation, choose training labels that were already available at the fitting cutoff. A document arriving before cutoff but resolved afterward cannot contribute its outcome to that historical fit. Route all revisions of a case together, or exclude boundary-crossing cases under a declared rule and report the exclusions. At prediction time reconstruct only the evidence then available. A correction published next week is not an intake feature today.

Use development partitions that mimic the same deployment boundary as the final holdout. A grouped final test combined with row-leaking model selection can still choose a poor procedure. Keep an audit record of case IDs, group membership, timestamps, label availability, feature schema and transformations. Count overlaps directly. Inspect a sample for hidden duplicate documents, renamed suppliers and template variants that exact IDs miss.

## Distribution change can reverse the winner

Even valid held-out evidence concerns a population. Suppose model P has subgroup MSE 1 on routine cases and 9 on exceptions, while Q has 4 and 4. At 90% routine, P's weighted loss is 1.8 versus Q's 4. At 50% routine, P's loss becomes 5, and Q wins. The crossover solves 9−8r=4, giving routine share r=5/8. This is F03's workload-mix reasoning applied to losses. It assumes each subgroup's error rate remains unchanged; a changed review process can invalidate even that assumption.

Report performance by relevant groups, the target mix, missing outcomes and severe underestimation. A change in inputs can be visible before labels arrive; it does not prove quality declined. Outcome monitoring needs matured labels and their availability lag. A frozen model that changes who gets reviewed also changes the feedback data, so evaluate the full workflow separately before claiming causal business benefit.

Prefer the simple baseline until added complexity earns its cost on an evaluation matched to deployment. More data from the same repeated template need not answer a new-template question. More parameters need not provide useful information absent from intake features. For language models, prompts, demonstrations, retrieval corpora and thresholds are also choices in the evaluated procedure. The same information-boundary discipline applies, while unknown pretraining exposure limits claims that a benchmark is entirely unseen.

## Practice

1. Derive the constant baseline and all training/validation MSEs in the candidate table. Derive wλ and explain why the units/scaling of λ matter.
2. Select a candidate using validation, compute its final test MSE and MAE, and compare the baseline. Change the final targets to 6 and 8. What claim does that defeat?
3. Reproduce the lookup predictor's zero-error row allocation and its grouped MSE of 17. Identify the independent document count and what the two evaluations measure.
4. Construct the organization/template connected components. Explain why grouping by their pair is insufficient, and propose a feasible response when all records form one component.
5. Write a one-page split plan for future new documents from existing suppliers, then revise it for new suppliers with unseen templates. Specify label cutoff, revision handling, preprocessing, baseline, tuning and final evaluation.
6. Derive the routine-share crossover for P and Q. Specify one monitoring observation that would invalidate reweighting, and distinguish model quality from a causal improvement in scheduling.

## Reference card and evidence

Specify decision time → define feature/label availability → name the future population → split at its independence boundary → fit all transformations inside training → select on development → freeze → evaluate once → monitor matured outcomes. Record the unit and denominator beside each score.

| Basis | Inspected locator | Supported use and limit |
| --- | --- | --- |
| R13, James, Witten, Hastie, Tibshirani and Taylor, Python edition, 2023 | [Author download page](https://hastie.su.domains/ISLP/ISLP_website.pdf.download.html), §2.2.1 printed p. 28; §5.1.1 p. 202; §6.2.1 p. 240 | Training versus unseen error, held-out fitting and quadratic penalty. No book dataset result transferred. |
| R13 author labs, stable snapshot accessed 2026-11-09 | [Chapter 5](https://github.com/intro-stat-learning/ISLP_labs/blob/stable/Ch05-resample-lab.ipynb), The Validation Set Approach; [Chapter 6](https://github.com/intro-stat-learning/ISLP_labs/blob/stable/Ch06-varselect-lab.ipynb), Choosing Among Models Using the Validation Set Approach and Cross-Validation, and Evaluating Test Error of Cross-Validated Ridge | Fold-local selection and separation of tuning from final evaluation. These passages were read; the authors' experiments were not rerun. |
| R02, January 2024 author draft | [PDF](https://mml-book.github.io/book/mml-book.pdf), §§8.2.1–8.2.2 pp. 259–261, eqs. 8.6–8.10 | Hypothesis class, empirical loss and fixed-predictor expected risk. |
| Original design and derivations | Tables, split proposals, graph example, mixture reversal and companion Python | Constructed teaching cases. Group/time split policy follows the declared deployment question, not a universal split recipe. |

The author download page redirected to its hosted PDF, which was read locally after web-reader access failed. Notebook passages were also retrieved from the authors' repository. PDF text extraction had font warnings; cited prose and section locators were readable. Formulas in this pack were derived and checked independently. No essential access blocker remains.

Open inputs: actual target population, independent group count, feature/label timestamps, outcome quality, review-policy changes, loss asymmetry and deployment costs. These examples cannot choose a production model or establish learner mastery. A02 next develops attention mechanics; A03 and A05 reuse these evaluation boundaries for retrieval and complete workflows.

## Revision history

- 1.0 — 2026-11-09. Small-predictor comparison, penalty derivation, leakage counterexample, deployment-aligned split design and six exercises.

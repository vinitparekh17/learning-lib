# F02 — Probability, base rates, and decisions under uncertainty

| Field | Value |
| --- | --- |
| ID / revision | F02 / 1.0 |
| Date | 2026-11-02 |
| Prerequisites | Fractions and elementary algebra; bridge in §2 |
| Capability developed | Translate detector evidence into conditional probabilities and choose an action under explicit losses |
| Source-check status | R02 §§6.2.1, 6.3, 6.4.1 inspected in author PDF, draft 2024-01-15; calibration supplement R23 §2 inspected |
| Experiment status | Exact arithmetic and decision-boundary checks executed; no empirical detector evaluation |
| Companion | [Hints and worked answers](SDE_F02_answers.md) |

## 1. A probability is an input to a decision

In the recurring fictional document service, an automated check flags a submitted record as potentially incorrect. Should the workflow pass it, pause it, or ask a reviewer? A statement such as “the detector catches 90% of errors” does not answer that question. You need to know what population the record came from, what a flag means in that population, and the consequences of each permitted action.

This pack uses invented counts and loss units to derive the decision. They are teaching inputs, not observed accuracy, pricing, or business loss estimates. “Pause” is a reversible workflow action in the example; permission for consequential actions remains a separate system requirement. A low expected loss does not authorize a system to exceed its authority.

The central distinction is between a measurement about a detector, an estimate about a particular case given available evidence, and a rule for acting on that estimate. Keeping these separate lets you change policy when costs change without pretending the detector itself changed.

## 2. Fractions, events, and denominators

An **event** is a condition that may be true: let E mean “the record contains the defined error,” and A mean “the detector alerts.” The complement ¬E means no such error. A probability of 0.01 is 1%, or one out of 100 under the specified model. Multiply a proportion by a population count to obtain the corresponding count: 0.01×10,000=100.

Write P(E) for the probability of error before observing this alert. The **base rate**, also called prevalence, is this error proportion in the population under discussion. Write P(A|E) for the probability of alert *among erroneous records*. The vertical bar means “given”; it changes the denominator. P(E|A) asks a different question: among alerted records, what proportion are erroneous?

R02 defines discrete conditional probabilities using restricted row or column totals, then derives Bayes' theorem using the product rule. Its expectation definition weights each possible result by its probability. We will apply those foundations to original count tables and a two-action loss model. The nonzero-denominator condition matters: a conditional fraction over an empty alert group is undefined, not zero.

## 3. Two populations, the same assumed detector

Assume the detector alerts on 90% of erroneous records and 5% of clean records. These are respectively sensitivity (true-positive rate) and false-positive rate. Specificity is the clean-record non-alert rate, here 95%. All rates are hypothetical and assumed identical in the two populations.

Population L contains 10,000 records with a 1% error rate. Therefore 100 are erroneous and 9,900 are clean.

| Population L | Error E | Clean ¬E | Total |
| --- | ---: | ---: | ---: |
| Alert A | 90 | 495 | 585 |
| No alert ¬A | 10 | 9,405 | 9,415 |
| Total | 100 | 9,900 | 10,000 |

The 90 true alerts come from 0.90×100. The 495 false alerts come from 0.05×9,900. Of the 585 alerts, only 90 are errors: P(E|A)=90/585=2/13≈15.38%. Most alerts concern clean records even though sensitivity is high. There are so many clean records that a small false-positive fraction creates many alerts.

Population H has the same size but a 20% error rate: 2,000 erroneous records and 8,000 clean records.

| Population H | Error E | Clean ¬E | Total |
| --- | ---: | ---: | ---: |
| Alert A | 1,800 | 400 | 2,200 |
| No alert ¬A | 200 | 7,600 | 7,800 |
| Total | 2,000 | 8,000 | 10,000 |

Now P(E|A)=1,800/2,200=9/11≈81.82%. The alert is much stronger evidence of an actual error in this population. This does not prove real detector rates remain unchanged after a population shift; that is an explicit premise of the comparison. Different document types or label definitions could change the conditional rates too.

For no-alert records, use the other row: P(E|¬A)=10/9,415≈0.1062% in L and 200/7,800≈2.5641% in H. Absence of an alert is not proof of absence of error.

## 4. Derive the update instead of memorizing it

Let b=P(E), s=P(A|E), and f=P(A|¬E). The fraction that both has an error and alerts is sb. The fraction that is clean and alerts is f(1−b). Those groups are disjoint and together contain every alert, so P(A)=sb+f(1−b). Dividing the first group by all alerts gives

\[
P(E\mid A)=\frac{sb}{sb+f(1-b)}.
\]

This is Bayes' rule expressed for this binary detector. It follows from counting the same joint event in two ways: P(E and A)=P(A|E)P(E)=P(E|A)P(A). Division by P(A) requires P(A)>0. No independence assumption between error and alert is needed; their dependence is exactly what makes the detector useful.

To obtain the no-alert version, replace s by 1−s and f by 1−f. A useful check is to reconstruct the base rate by weighting the two posteriors by the sizes of their groups. In L, the erroneous counts recovered from the alert and non-alert rows must sum to 100. This catches a denominator swap that can otherwise look plausible.

Here is the tempting mistake: calling 90% sensitivity “90% of alerts are correct.” In L the two fractions share the numerator 90 but divide by 100 and 585 respectively. Before manipulating a percentage, write the group after the word “among.”

## 5. Derive a decision threshold from losses

Suppose the only available choices are pass and pause. Set correct decisions to zero loss for this model; assign loss C_FN=100 to passing an erroneous record and C_FP=20 to unnecessarily pausing a clean one. Costs are in a common invented loss unit. They can represent an agreed combination of delay, rework, and harm, but comparable units and complete consequences must be justified in a real application.

For a record with error probability p given all information being used, the loss table is:

| Action | Error, probability p | Clean, probability 1−p | Expected loss |
| --- | ---: | ---: | --- |
| Pass | 100 | 0 | 100p |
| Pause | 0 | 20 | 20(1−p) |

Expected loss means multiply each loss by its chance and add. It is an average under the model, not a promise about any individual outcome. Choose pause when C_FP(1−p)<C_FN p. Expanding and collecting the p terms gives

\[
p>\frac{C_{FP}}{C_{FP}+C_{FN}}.
\]

The denominator is positive here. At equality both actions have the same modeled loss; define a tie policy explicitly. With our numbers the threshold is 20/120=1/6≈16.67%. For alerts in L, p=2/13 is below the threshold: passing loses 200/13≈15.38 versus pausing 220/13≈16.92. For alerts in H, pausing loses 40/11≈3.64 versus passing 900/11≈81.82. The same alert leads to different actions because its conditional meaning differs.

Now increase only the missed-error cost to 200. The threshold becomes 20/220=1/11≈9.09%. Both alert groups should now be paused in the two-action model. The detector and probability estimates have not changed; the losses have. A universal 0.5 threshold would ignore the asymmetry.

These comparisons assume p captures the information available to the policy. If you have case-level features, an entire alert group's average need not be appropriate for each record. They also assume independent decisions without a shared capacity constraint. Limited reviewers or an overall pause budget create a coupled allocation problem.

## 6. Asking a person is a third action with a cost

Add review at cost 4 per record. First assume, unrealistically but transparently, that a reviewer always resolves the error status correctly and has no other delay or downstream cost. The expected review loss is 4. Review beats pass when 4<100p, or p>0.04. It beats pause when 4<20(1−p), or p<0.8. Therefore:

| Probability region | Minimum-loss action under the ideal-review model |
| --- | --- |
| p<0.04 | Pass |
| 0.04<p<0.8 | Review |
| p>0.8 | Pause |
| p=0.04 or p=0.8 | Tie between adjacent choices; apply declared policy |

For the L alert group, review at 4 beats both automatic choices. For the H alert group, pause at about 3.64 beats review. Review is valuable when its information can change the action enough to justify its cost; it need not be best for every uncertain case.

Remove the perfect-review assumption. If review misses 5% of actual errors and incorrectly pauses 10% of clean records, its expected loss becomes

\[
L_{review}=4+0.05p(100)+0.10(1-p)(20)=6+3p.
\]

Those residual error rates must describe the cases actually routed to review. At p=0.2, review loses 6.6, pass loses 20, and pause loses 16. Review still wins there, but the old 0.04 and 0.8 boundaries no longer apply. “Human in the loop” is a workflow description, not a numerical guarantee. An abstention policy that defers action needs its own delay, escalation, and unresolved-case losses.

## 7. Estimate, calibration, and policy are different objects

A numeric score in [0,1] is not automatically an established probability. **Calibration** asks whether stated probabilities match observed event frequencies in an appropriate population. For a binary event predictor, predictions around 0.8 should correspond to an error frequency around 80% if they are calibrated there. The R23 supplement formalizes calibration of confidence in a predicted class; here we use the analogous binary-event formulation, not a claim about that paper's empirical performance.

As an original counterexample, imagine two equally sized groups all assigned score 0.5. Their error rates are 10% and 90%. The overall rate is 50%, matching the score, while each subgroup is poorly served by it. Aggregate calibration does not establish subgroup calibration or individual certainty. Even a predictor that emits the population base rate for every record can be calibrated in aggregate while providing no useful ranking within that population.

Calibration evidence needs labeled examples relevant to intended use, with counts and uncertainty recorded. A bucket containing two predictions is much weaker evidence than its precise-looking percentage suggests. Changing the population can invalidate old calibration evidence. Choosing a cost-based threshold does not repair a biased probability estimate. Conversely, improving calibration does not choose your loss function or resolve an authority restriction.

## 8. Boundaries, connections, and practice

Before trusting the calculation, check the error definition and label quality; the population and base rate; stability of sensitivity and false-positive rate; omitted loss categories; reviewer accuracy and capacity; and whether group averages conceal important differences. Near a decision boundary, plausible uncertainty in either p or cost can reverse the choice. Investigate the parameter that matters to the decision rather than reporting extra decimal places.

F01 established the habit of declaring a model before claiming a guarantee. B01 separated observed evidence from assumptions and identified whose outcome matters. F02 adds a conditional model for uncertainty. F03 will test how rates are estimated and comparisons designed. A05 will reuse abstention and review decisions; B02 will connect failures and human work to delivery economics.

Try these six tasks before opening the answers. All inputs are hypothetical.

1. Rebuild both 10,000-record tables from b, s, and f. Calculate both alert precision and non-alert error probability. Explain each denominator.
2. A third population has 10% errors, 80% sensitivity, and 2% false-positive rate. Build its table and compute P(E|A).
3. At p=0.2, compare pass and pause for costs (C_FN,C_FP)=(100,20), then (100,40). Derive each threshold and explain the reversal.
4. Derive the perfect-review boundaries for cost 4 and costs (100,20). Then derive the imperfect-review boundaries using the rates in §6.
5. Explain how the two 0.5-score subgroups can look calibrated together. Propose a check before applying one common threshold.
6. An evaluation set was constructed with equal error and clean counts, while deployment prevalence is 1%. Explain what can and cannot be transferred, and list three deployment measurements needed before enabling automatic decisions.

Success means reconstructing the counts, stating loss assumptions, and identifying evidence that would change the action. No learner answers or mastery are recorded.

## 9. Reference card and evidence ledger

Write the denominator first. Sensitivity is P(A|E); alert precision is P(E|A). Compute the latter from base rate and both conditional alert rates. Expected loss sums probability×loss. The two-action threshold is C_FP/(C_FP+C_FN) only for the stated zero-correct-loss model. Review adds an action and its own cost and residual errors. Calibration concerns probability validity; policy concerns choices under losses and constraints.

| Source / claim | Verified locator | Evidence and limitation |
| --- | --- | --- |
| R02: Deisenroth, Faisal, Ong, Mathematics for Machine Learning | [Author PDF](https://mml-book.github.io/book/mml-book.pdf), draft 2024-01-15, §6.2.1 printed pp. 178–180, eqs. 6.9–6.14; §6.3 pp. 184–185, eqs. 6.20–6.26; §6.4.1 p. 187, Definition 6.3 / eq. 6.29 | Discrete conditional probability, Bayes, expectation; actual passages extracted and inspected 2026-11-02. Author PDF obtained directly after web reader size limit. Page references are printed pages. |
| R23: Guo, Pleiss, Sun, Weinberger (2017), On Calibration of Modern Neural Networks | [Conference PDF](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf), §2, PDF p. 2, eq. 1 and Reliability Diagrams paragraphs | Definition and finite-sample estimation context only; no contemporary-model or benchmark claim |
| Count tables, threshold derivations, imperfect review, subgroup counterexample | Original §§3–7; exact checks in answer file | Conditional results from invented inputs; no empirical validation |

Open application questions: actual prevalence, conditional detector performance, case-level probability quality, loss values, reviewer behavior, and capacity. They are unresolved empirical inputs, not blockers to F03. Audit A remains pending.

## Revision history

- 1.0 — 2026-11-02: original F02 pack; added one calibration supplement to resolve the probability-estimate distinction; no curriculum change.

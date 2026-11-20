# F03 — Did the pipeline improve, or did the measurement change?

| Field | Value |
| --- | --- |
| ID and revision | F03 · 1.1 |
| Date | 2026-11-03 |
| Prerequisite | F02, especially conditional proportions and the cost of errors |
| Capability | Design a comparison, identify which claim it supports, and decide what evidence would justify rollout |
| Source check | Microsoft Research R03 and the R13 Python edition's Chapter 5 author lab. Passage locators appear at the end. |
| Experiment status | Constructed data and executed arithmetic. The live study is a proposed design. |
| Companion | [Hints and worked answers](SDE_F03_answers.md) |

## Start with the case that fools the dashboard

A purchasing team is comparing two pipelines that extract invoice evidence for an approver. A handles today's workflow. B adds a retrieval step and attaches supporting passages. Imagine the team introduced B in the exceptions queue first. A dashboard then compared their success rates. Every number in this lesson is a teaching input.

| Document type | A, correct / eligible | B, correct / eligible |
| --- | ---: | ---: |
| Routine | 72 / 80 = 90% | 19 / 20 = 95% |
| Exception | 12 / 20 = 60% | 52 / 80 = 65% |
| All | 84 / 100 = 84% | 71 / 100 = 71% |

Would you cancel B? Take a pencil and mark the denominator for each percentage. The comparison of totals gives B a 13 percentage point deficit. Within *both* document types, B leads by 5 points. A handled mostly routine cases. B handled mostly exceptions. The overall rate depends on the difficulty mix as well as the pipeline.

Use a hypothetical target workload of 80% routine and 20% exception documents. For every 100 target cases, A's estimated successes are 80 × 0.90 + 20 × 0.60 = 84. B's are 80 × 0.95 + 20 × 0.65 = 89. At a common mix, the difference is **+5 percentage points**. At a 50/50 mix it is still +5 because both within-type differences happen to be equal. If the differences had opposite signs, the target mix could change which pipeline you preferred.

The adjusted result answers a deliberately narrow question. It describes what the given rates imply at the chosen mix. Routing may also have depended on supplier, reviewer experience, or document quality *within* each type. Any of those differences could account for the apparent gain. Weighting by type fixes one imbalance. To investigate the remaining uncertainty, use the same documents for both pipelines.

## Specify what a win would mean

Write the decision before selecting a metric. Here it is whether B should enter a limited live trial, followed by whether it should replace A for the intended teams. Those decisions need different evidence.

In this example, a **case** consists of one invoice, its revisions, and any retries. Define success as a correctly resolved case with the required source evidence within two business days of arrival. A blinded adjudicator applies the same frozen rubric to both arms. A timeout or unresolved case at the deadline counts as a failure. Counting only completed outputs would allow B to improve its displayed accuracy by quietly dropping difficult work.

Specify the population as invoices from participating purchasing teams, supported languages, and the agreed intake dates. Determine eligibility at receipt, before either pipeline has influenced the case. Record the reason for every predeclared exclusion. An unsupported input can be outside this target population while still deserving a separate count for readers who need to know what fraction of incoming work the claim covers.

A useful metric has a unit, a denominator, a clock, and a rule for missing outcomes. Use correct on-time cases divided by eligible cases as the primary metric. Count staff review minutes and compute charges for failures as well as successes. Report total cost per eligible case and total cost divided by verified successes. The second ratio is undefined if there are zero successes. Report severe erroneous recommendations separately. An average gain can coexist with an unacceptable error that the average conceals.

F02's denominator discipline applies directly. A low error fraction among cases that produced answers does not give the error fraction among all eligible cases. B01 supplies another check. If the buyer cares about evidence reaching the approver, a faster extractor helps only when that step changes the eventual outcome.

## Replay both pipelines under controlled conditions

Build a locked historical set from the intended intake population. Keep revisions of the same invoice together. If the intended claim concerns unfamiliar suppliers, reserve entire suppliers for the final test. If it concerns future cases from existing suppliers, use a later time window and keep future revisions out of earlier tuning. Those designs answer different questions. Choose the split that matches deployment.

Freeze prompts, models, decision thresholds, retrieval index snapshot, rubric, and compute budget before looking at final labels. Exclude information that would become available only after the original request. A retrieval snapshot containing the eventual corrected invoice could make B appear remarkably accurate while giving it evidence unavailable at decision time. Use development folds to tune choices. Repeatedly tuning on the final set turns it into development data. R13's validation example illustrates why a held-out estimate itself can vary with the split.

Run both pipelines on each eligible case. Counterbalance execution order if caches warm up, isolate caches if they would otherwise pass information between pipelines, and report cold and warm workloads if both matter. Give a stochastic pipeline the same prespecified number of attempts per case. Multiple attempts on one invoice still represent one underlying case.

Here is a second **constructed** comparison on 100 common cases. Both pipelines succeed on 76, only A succeeds on 8, only B succeeds on 13, and both fail on 3. A succeeds on 84 and B on 89. The gain is (13 − 8) / 100 = 5 points. This paired view adds information that the two totals hide. Eight cases regress. Reading those eight cases may reveal a severe evidence error that makes the candidate unsuitable even with a positive average.

For uncertainty, decide which observations could reasonably vary independently. In a workload sampled by supplier, one supplier template may generate dozens of nearly identical invoices. To estimate workload sampling variability, resample suppliers with replacement, keeping all of each selected supplier's cases and both pipeline outputs together. Recompute the chosen statistic per replicate. If the target is a typical case, sum successes and denominators over the resampled suppliers before taking their ratio. A typical-supplier target weights suppliers equally instead. Few suppliers, rare events, or an unrepresentative sample limit what a bootstrap interval can tell you. It cannot recover a missing supplier population. If your claim concerns exactly the fixed 100-case suite and the outputs are deterministic, the descriptive difference is known for that suite.

Replay can establish differences on those inputs under that resource policy. It leaves open what happens when reviewers trust suggestions, queues back up, or customers change their submissions. Those effects require observation of the workflow under each policy.

## A live experiment plan, written before results

| Design choice | Proposed specification for the fictional teams |
| --- | --- |
| Effect of interest | Difference in the mean participating team's fraction of eligible cases correctly resolved within two business days under assignment to B versus A. Each team gets equal weight. |
| Assignment | Use stable team IDs. Form pairs of teams using baseline volume, exception share, and historical success rates. Randomly assign one team in each pair to B and its partner to A. |
| Exposure and unit | A team and its dedicated reviewer queue stay in one arm throughout. The case is the measurement unit. The team is the assignment unit. Shared reviewers or queues require regrouping before launch. |
| Duration and size | Candidate window of four working weeks plus two business days for final outcomes. Before launch, use historical team-level variability to plan enough independent pairs for a meaningful gain. Freeze the required team count and duration. If the size is infeasible, call the study a pilot. |
| Outcomes | Primary as defined above. Secondary measures include active review time per eligible case, cost per verified success, and the distribution of resolution times. Guardrails include severe errors and missing telemetry. |
| Exclusions and missing data | Apply the same intake rules to both arms. Retain crossovers, retries, failures, and unverified cases in their assigned arm. Flag missing adjudication separately and show sensitivity to its assumed outcome. |
| Analysis | For each pair subtract A's team success rate from B's. Average those differences. Display pair-level data and a 95% interval accounting for pairing, plus counts for each arm. Prespecify routine/exception and new/existing supplier summaries. |
| Decision and stop | One efficacy analysis after outcomes mature. Example gate agreed in advance: lower interval bound above +2 points, cost within budget, and acceptable severe-error rate. Define actual budget and severity limits with owners before launch. Pause exposure immediately for a severe unauthorized recommendation or broken assignment logging. |

For an optional uncertainty bridge, let d_i be B minus A in team pair i, with m independent pairs. Their average is d_bar. The sample standard deviation s_d measures the spread of these differences around d_bar. The standard error s_d/sqrt(m) estimates how much the average varies under a model of independent, comparable pair differences. A two-sided t interval is d_bar ± t_(0.975,m−1) s_d/sqrt(m). The multiplier depends on m−1 degrees of freedom, so substituting 1.96 for every study size is inappropriate. NIST documents the mean-interval formula and its repeated-sampling interpretation in [R24, §1.3.5.2](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm). Applying it to pair differences is our modeling choice. Exact t coverage requires independent identically distributed normal differences; for bounded team rates this is an approximation, whose adequacy needs enough independent pairs and no dominating outliers. Random assignment alone does not establish that sampling model or transport the result to other teams.

A 95% confidence procedure aims to cover its target in 95% of repeated samples under its assumptions. It does not assign a 95% probability to the fixed target lying in this particular observed interval. Additional documents within a team do not create more independent assignments.

For a few pairs, display raw differences. Under the sharp null that assignment changes no team's outcome, no interference, and independent fair assignment within each pair, enumerate the 2^m possible within-pair label swaps. Each assignment is equally likely by design. Compare the absolute observed mean difference with that enumeration for a two-sided randomization test, including equally extreme values. This tests that sharp null; it does not directly supply a confidence interval for a heterogeneous average effect. The derivation follows from the specified randomization mechanism, rather than from the R13 bootstrap example.

Randomization makes assignment independent of potential outcomes under the design, in expectation. It can still produce imbalance in one draw. Historical metrics, an A/A rehearsal, and checks that IDs keep their assignment help uncover faults. An A/A rehearsal routes both arms to the same pipeline to test instrumentation. An unexplained arm-count discrepancy calls for checking the assignment mechanism and missing logs. With paired team assignment, equal team counts are expected while document counts may differ naturally.

Request-level assignment would be inappropriate here. A reviewer can learn B's evidence-checking technique and apply it to A cases. B can also fill a shared queue and delay A cases. Either path lets one assignment affect another case's outcome. Separating teams works only if the separation contains the important spillovers. If both arms depend heavily on one central reviewer pool, redesign the assignment around genuinely separate pools or revise the question to what can be learned from replay.

## Read a result and decide what to do

Imagine the planned live analysis yields +5 points with a 95% interval from −1 to +11. The interval includes a small decline and gains above the +2-point gate. Under that rule the evidence is inconclusive for rollout. A broad interval is compatible with meaningful benefit and meaningful uncertainty. If the instrument lost more completion events in B, first quantify the differential loss and repair the measurement before using the estimate.

Look at distributions as well as means. In an illustrative set of ten waits, nine one-minute waits and one 21-minute wait average three minutes. Ten three-minute waits also average three. The implications for a ten-minute deadline differ. When reporting latency quantiles, name the eligible population, timeouts, quantile convention, and sample size. When reporting stakeholder value, ask whether delays occur before or after the customer's deadline.

Before deciding, inspect candidate explanations for the result. **Selection bias** can enter when participation depends on having easy documents. **Confounding** can enter when more experienced reviewers receive B and would have done better with either pipeline. **Leakage** can enter when test labels influence tuning or a later correction enters the retrieval corpus. **Interference** can enter when treatment changes control's queue or reviewer behavior. Each failure calls for a different repair. More rows drawn through the same broken mechanism can sharpen the wrong estimate.

## Practice on paper

Allow roughly 35 minutes. Prepare a one-page comparison plan before consulting the separate solutions.

1. Reproduce the dashboard difference and the 80/20 adjusted difference. Give one remaining explanation for the gap within each document type.
2. Reconstruct the paired replay from its four counts. Which cases deserve inspection first? Which uncertainty question calls for supplier-level resampling?
3. Write the live study's assignment, measurement, and analysis units. Explain how the shared reviewer pool would change the design.
4. Suppose A verifies 84 correct cases for 420 cost units, and B verifies 89 for 480 units, out of 100 eligible cases each. Calculate cost per eligible case and per verified success. Propose a decision if the budget ceiling is 5.2 units per verified success.
5. Draft eligibility, exclusions, missing-outcome handling, subgroup summaries, stopping rules, and the rollout gate. Apply it to the hypothetical interval above. Explain what an offline win and a live win would each justify.
6. Transfer the plan to an AI assistant for debugging. Identify an independent unit, one leak, one spillover, and one whole-task success metric.

## Reference card and evidence

Keep the case ID, eligibility rule, clock, and denominator visible. Compare pipelines on common cases for a workload claim. Assign treatment where spillovers can be contained for a causal claim. Match the uncertainty calculation to the independent units. Record a useful effect size and the conditions for rollout before results arrive. A01 revisits generalization, S05 revisits latency distributions, and A05 reuses whole-task outcomes for AI evaluation.

| Basis | Inspected passage | How this pack uses it |
| --- | --- | --- |
| R03 · Machmouchi, Gupta, Zhang and Fabijan, Microsoft Research (2020) | “Formulate your Hypothesis and Success Metrics,” “Choose the Appropriate Unit of Randomization,” “Set Up Counterfactual Logging,” and “Review Engineering Design Choices to Avoid Bias.” [Primary article](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/) | Practitioner guidance on units, guardrails, consistent exposure definitions, and shared infrastructure. The proposed invoice study is an application of these ideas. |
| R13 · James, Witten, Hastie, Tibshirani and Taylor, ISL with Python (2023) | Chapter 5 author lab, “The Validation Set Approach,” alternative split, and “The Bootstrap,” function `boot_SE`. [Author notebook](https://github.com/intro-stat-learning/ISLP_labs/blob/stable/Ch05-resample-lab.ipynb) | Holdout variability and resampling with replacement. The paired supplier resampling design is our adaptation to related documents. |
| R24 · NIST/SEMATECH e-Handbook | [§1.3.5.2, Confidence Limits for the Mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm), definition and interpretation, inspected 2026-11-04 | Mean-interval formula. Pair-level application and randomization enumeration are explicitly qualified original analysis. |
| Original examples and study design | Tables, arithmetic, interval scenario, protocol, and solutions in this pack | All counts, thresholds, and costs are hypothetical. The companion contains the executed checks. |

Open questions for deployment include the actual supplier mix, independent reviewer pools, outcome completeness, baseline variance, and acceptable cost and harm limits. These determine whether the proposed live study can proceed. Curriculum Audit A completed on 2026-11-04; see SDE_Audit_A.md for scope.

## Revision history

- 1.0 — 2026-11-03: original measurement pack.
- 1.1 — 2026-11-04: Audit A added an uncertainty bridge, R24 support, and explicit interval/randomization assumptions. Six exercises and their answers remain compatible.

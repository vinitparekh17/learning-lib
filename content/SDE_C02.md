# C02 — Does better model performance improve the customer outcome?

| Field | Value |
| --- | --- |
| ID / revision / date | C02 · 1.0 · 2026-11-11 |
| Title | Does better model performance improve the customer outcome? |
| Prerequisites | F02/F03, A01/A03/A05, B01 |
| Capability developed | Choose an evaluation and a conditional investment decision across component, workflow and customer metrics |
| Source-check status | R03 experiment-design sections and R19 customer-interview transcript passages rechecked |
| Experiment status | Original hypothetical ledger and executed arithmetic/set checks; no customer study or model benchmark |
| Companion | [Worked analysis and checks](SDE_C02_answers.md) |

## Decision requested

Keep the current process available and advance the targeted evidence-assistance option A to the next controlled evaluation, rather than choosing the higher-scoring model option B on component accuracy alone. This recommendation is conditional on the constructed assumptions below. It is a decision about what to investigate, not authorization to deploy or evidence that a customer will buy.

The fictional purchasing team wants cases correctly resolved with exact evidence before its approval cutoff. The service may prepare drafts, retrieve permitted records and flag exceptions. Human approval remains required for consequential actions. A05's authority boundary is unchanged. A03 supplies the definition of supporting evidence; A01 supplies the information available at decision time. B01 reminds us that matching may not be the customer's binding constraint at all.

We compare three credible alternatives on the same 100 eligible invoice cases, including every revision and retry within its original case:

- C: current manual evidence assembly and review.
- A: fixed evidence workflow with a targeted alternate-extraction branch and human review.
- B: a model upgrade within the same approval boundary, with additional retrieval/validation work.

These names are local to this memo. They are not F03's pipelines or A05's W/M/L outcomes. No earlier hypothetical counts are reused as measurements.

## Separate four claims before comparing them

| Level | Metric and population | What it can establish | What remains open |
| --- | --- | --- | --- |
| Component | Correct field output on 100 fixed, sufficient-evidence inputs | Performance with that supplied context | Retrieval, timing, review and customer usefulness |
| Whole task | Correct, evidenced disposition by deadline / all 100 eligible cases | Contract completion in the evaluated workflow | Causal effect on staff behavior and adoption |
| User value | Active work, elapsed resolution time, rework and error consequences | Whether intended users gain on outcomes they value | Budget authority and willingness to change |
| Commercial commitment | Authorized trial, repeated use, renewal under explicit terms | Behavior toward the particular offer | General market demand or profitability |

A resolvable citation is not necessarily supportive, current or applicable. A reviewer clicking accept is not independently verified correctness. A shorter model response is not a shorter case-resolution time. Log these as distinct variables instead of allowing one convenient event to stand for all four claims.

R03 recommends specifying falsifiable hypotheses, success and guardrail metrics, and the experimental unit before interpreting results. R19 recommends reconstructing concrete recent problems and existing alternatives rather than relying on hypothetical enthusiasm. These are practitioner sources guiding the design; neither supplies empirical values for this memo.

## A common ledger with deliberately invented numbers

The initial deadline is one business day from intake, inclusive. For this fixture all cases have an adjudicable expected disposition. Correct means that the final disposition and required evidence satisfy the frozen rubric; it does not mean a payment occurred. Incorrect results and unresolved cases are separate, exhaustive categories. Unauthorized effects are assumed absent under all options, but that assumption requires implementation testing.

| Assigned quantity across 100 common cases | C | A | B |
| --- | ---: | ---: | ---: |
| Correct component outputs with sufficient evidence supplied | Not applicable | 90 | 96 |
| Correct final dispositions, regardless of lateness | 90 | 92 | 96 |
| Of those correct dispositions, late at one day | 4 | 4 | 12 |
| Correct on-time dispositions | 86 | 88 | 84 |
| Incorrect final dispositions | 2 | 2 | 1 |
| Unresolved cases | 8 | 6 | 3 |
| Active staff minutes, including unsuccessful cases | 800 | 400 | 300 |
| Resource charge in invented units | 0 | 100 | 200 |

Component and final correctness are different experiments; a reviewer or fallback can repair a component error, so A's final correct count may exceed its component count. The component table does not expose the full causal pathway. To investigate the difference, retain intermediate retrieval/context/claim/review records rather than multiplying unrelated aggregate scores.

B improves the assigned component score from 90% to 96% and final correctness from 92% to 96%, yet produces four fewer timely correct outcomes. Its 84/100 result is worse than A's 88/100 for the chosen primary outcome. Correct-but-late work is valuable in some settings, but the initial contract does not count it as timely success. We also report eventual correctness so the deadline metric does not conceal it.

For the paired A/B comparison, 76 cases succeed under both, 12 only under A, 8 only under B and 4 under neither. The net change B−A is (8−12)/100=−4 percentage points. Eight improvements coexist with twelve regressions. Inspect their mechanisms and severity before summarizing them as a net number. These are constructed paired outcomes, not a statistical significance test.

Assign an active-work value of 0.5 units per minute. Total resource-plus-labor-value charges are C=400, A=300 and B=350. At the one-day deadline, charge per timely correct outcome is respectively 400/86≈4.65, 300/88≈3.41 and 350/84≈4.17. Include failed and late work in each numerator. Released staff time is capacity value, not necessarily cash savings; wages may remain unchanged and the freed time may have no useful alternative use. Service fees, onboarding and error damages are not included.

The initial decision rule is: require at least 88 timely correct cases, no more than two incorrect dispositions, no unauthorized effects and a total modeled charge no greater than 360; among feasible options maximize timely correct cases, breaking ties by lower charge. These thresholds are explicit teaching choices, not established customer requirements. A alone satisfies the assigned counts and budget. C fails the outcome and budget gates; B fails the timely-outcome gate despite lower staff effort and fewer errors.

## Change one constraint, then revise the choice

Now the hypothetical customer changes only the resolution deadline to two business days. Keep all cases, evidence, outputs, work and costs fixed. Of the correct cases late at one day, two C cases, two A cases and ten B cases finish by day two. The remaining correct cases are still late.

| Recomputed result | C | A | B |
| --- | ---: | ---: | ---: |
| Correct on time at two days | 88 | 90 | 94 |
| Total modeled charge, unchanged | 400 | 300 | 350 |
| Charge per timely correct result | 4.55 | 3.33 | 3.72 |
| Feasible under unchanged remaining gates? | No: charge | Yes | Yes |

Under the stated maximize-success rule, revise the choice to B: it delivers 94 rather than 90 timely correct cases within the budget. A still has lower charge per success. The recommendation changes because the explicit objective values additional successes subject to a budget; minimizing the ratio would retain A. Do not silently substitute one objective for the other.

The extra modeled charge for B versus A is 50 units for four additional timely correct cases, or 12.5 units per incremental success. That is not a price recommendation. If the buyer instead values each additional success at v units in a simple linear net-value model, B beats A only when 4v>50, hence v>12.5. At equality they tie. Real error severity and deadline value may not be linear.

This revision is internally consistent because only the classification of arrival-to-completion times changed. It does not assume a faster model, cheaper tool or more accurate reviewer. In a real organization, a relaxed deadline can change queues, staffing or behavior; the frozen-trace calculation would then be only a diagnostic, not a forecast.

## Evaluation plan that can disprove the recommendation

First investigate the problem. Ask operators to reconstruct a recent delayed invoice, identify active work versus waiting, and show the artifacts used. Ask the decision maker who can authorize sample data, process changes and budget. Do not treat praise for an accurate demo as a commitment. A suitable next evidence milestone is an authorized sponsor agreeing to a scoped trial, named reviewer, dates and outcome rubric. No interviews or outreach are performed here.

For offline work, choose eligibility at intake before either system affects outcomes. Preserve all offered and excluded counts and reasons. Freeze source snapshots, extraction versions, retrieval configuration, prompts/models, thresholds, call budgets and review rubric. For future cases from known suppliers use a later time holdout; for new suppliers hold out entire suppliers. Keep all revisions/retries together and exclude future evidence. Tune on development cases only. Missing labels require a declared follow-up window and reporting rule, not silent deletion.

Run A and B on the same cases with equal prespecified repetitions if stochastic. Measure component quality under common evidence separately from full-system outcomes. Preserve case-level pairing and supplier grouping when quantifying uncertainty; repeated seeds are not independent suppliers. Report effect sizes, regression cases, interval assumptions and subgroup denominators. A balanced failure suite is useful for stress testing but does not establish deployment frequency. Set study size from a minimally useful effect and independent-unit variability; do not treat our 100 invented rows as a power calculation.

Before any live trial, validate logging and guardrails in shadow mode, without new approval authority. For a proposed live comparison, randomize stable purchasing teams where reviewers share learning and queues; avoid mixing variants inside one team if that creates spillover. Check for cross-team interference and whether isolated infrastructure would change the intended treatment. Block or match on baseline workload before randomization. Estimate the effect on all assigned eligible cases, preserving assigned treatment even when the tool is not used; separately report usage. Define the analysis horizon and stopping rule before observing outcomes, with immediate operational pauses for critical authority breaches. A trial too small in independent teams can be inconclusive despite many invoices.

R03's counterfactual-logging section motivates comparable exposure definitions in both arms; its engineering-bias section warns about shared components and unequal caches. Our concrete design therefore logs eligibility for both arms from the same pre-treatment rule and records versions/resource conditions. Changing the model and user interface together evaluates the bundle; it cannot attribute the result solely to the model.

Measure correct on-time resolution, active review minutes, rework, errors by severity, source support, prohibited attempts/effects and total resource use. Also observe whether released capacity is actually used and whether approvals still wait on an unrelated bottleneck. Verify correctness with evidence-based adjudication, blind to option when practical; investigate judge/person disagreement as A05 specifies. Test the adjudicator on separate cases.

## Decision boundaries and handoff

The strongest conclusion here is a logical counterexample: higher component accuracy need not improve the chosen whole-task outcome. The source passages support the evaluation discipline, while the arithmetic follows from invented inputs. They do not prove actual demand, a causal model effect, implementation safety or a revenue forecast.

F02 makes error costs and objective changes explicit; F03 separates replay from intervention; A01 protects holdouts; A03 checks source applicability; A05 keeps authority and denominators intact; B01 asks whether the outcome matters enough to change behavior. The next investment should target the weakest link in that chain rather than the most impressive model metric.

## Assignment

1. Reconstruct the one-day decision, including paired gains/regressions and both cost denominators: per eligible case and per timely correct case.
2. Change only the deadline to two days. Defend the revised choice and explain why minimizing cost per success gives a different answer.
3. Derive the incremental-value threshold. Change the labor-value rate from 0.5 to r and find when B's modeled charge becomes lower than A's.
4. Specify an offline and live evaluation that separates component quality, task quality and customer value. Name a leakage and an interference failure.
5. Identify the unsupported customer assumptions and write a concrete evidence milestone that could stop the project even if B's component score remains highest.

## Evidence and unresolved inputs

| Basis | Verified locator | Boundary |
| --- | --- | --- |
| R03 Microsoft Research, 2020-07-31 | [Article](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/): Formulate your Hypothesis and Success Metrics; Choose the Appropriate Unit of Randomization; Set Up Counterfactual Logging; Review Engineering Design Choices to Avoid Bias | Practitioner design guidance; no observed product effect adopted |
| R19 YC / Migicovsky, 2019-09-04 | [Transcript](https://www.ycombinator.com/blog/startup-school-week-1-recap-kevin-hale-and-eric-migicovsky/), 20:20–24:10 questions on recent problems and alternatives | Interview guidance; no demand or willingness-to-pay estimate |
| Earlier packs | F02/F03, A01/A03/A05, B01 | Definitions and continuity, not new empirical evidence |
| Original construction | Ledger, gates, deadline change, paired sets and sensitivity | Executed arithmetic; no customer or model experiment |

Actual task mix, deadlines, outcome values, error severity, review reliability, resource charges, adoption authority and usable capacity remain unknown. No essential source-access blocker remains. No learner answers or mastery inferred. Next: Audit C of AI packs and C02.

## Revision history

- 1.0 — 2026-11-11. Conditional decision memo, one-constraint reversal and five analysis tasks.

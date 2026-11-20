# B01 — Customer problems, alternatives, and evidence of demand

| Field | Value |
| --- | --- |
| ID / revision | B01 / 1.0 |
| Date | 2026-11-02 |
| Prerequisites | None; basic arithmetic bridge included; revisit after F03 |
| Capability developed | Form a falsifiable demand hypothesis and choose evidence that changes a build decision |
| Source-check status | R19 primary transcript inspected; timestamp locators in §10 |
| Experiment status | No interviews, outreach, trials, or market experiment conducted; illustrative arithmetic checked |
| Companion | [Hints and worked answers](SDE_B01_answers.md) |

## 1. The engineering decision before implementation

Suppose you can build a service that reads documents, extracts supporting facts, proposes an action, and waits for human approval. Which part deserves your next week of engineering effort? A convincing demo answers whether a mechanism can work on selected inputs. To allocate effort, you also need to identify a person with a consequential problem, their existing alternative, and the conditions under which they would adopt a change.

The output of this pack is a small evidence plan. It should make a decision possible even when the answer is to postpone building. No business experience is assumed. A **hypothesis** is a claim you can investigate; **falsifiable** means you can name observations that would count against it. A **segment** is a defined group sharing relevant circumstances. A **commitment** is a concrete action someone takes, with its terms and cost recorded.

Use the source narrowly. In R19, Eric Migicovsky recommends investigating specific past episodes, existing attempts, and shortcomings; he also discusses costs, recurrence, budget, and authority. His warning about hypothetical enthusiasm is useful for planning interviews. These are practitioner recommendations from a startup context, not experimental proof of a successful discovery method. The exercises, decision rules, and numerical example below are original teaching designs. They do not establish market demand.

## 2. Separate the claims that a product idea compresses

“Teams need document AI” leaves several different uncertainties hidden. Unpack the statement before deciding what to build:

| Claim | Evidence you would seek | What remains unproved |
| --- | --- | --- |
| A recurring problem exists | Recent episode, workflow trace, consequence | Whether your proposed intervention helps |
| The problem matters enough to address | Current resources spent, missed objective, active workaround | Whether it outranks other priorities |
| Someone can authorize a change | Named decision role and actual approval path | Whether that person will fund this offer |
| Your offer improves the outcome | Agreed trial against the current process | Whether improvement survives ordinary operation |
| The customer will adopt and pay | Specific authorized commitment on stated terms | Whether use repeats and delivery is sustainable |

A clerk, a budget owner, and a data approver may be different people. In a small firm one person may fill all three roles. Record the roles rather than assuming an organization chart. For an internal developer tool, substitute the team that owns the workflow and the manager allocating engineering time; payment is not the only meaningful resource commitment.

Keep the existing alternative visible. A spreadsheet, a knowledgeable employee, postponement, and tolerating errors all compete with a proposed service. An alternative can be imperfect yet preferable after accounting for migration, trust, training, and ongoing review. Those costs are questions to investigate, not reasons to dismiss the idea automatically.

## 3. Worked case: find the decision bottleneck

**Entire case is hypothetical. No customer observations, quotes, or willingness-to-pay measurements are reported.** Imagine a purchasing team that matches supplier invoices with delivery records before a manager approves payment. Your proposed service extracts evidence and flags mismatches; the manager remains responsible for approval.

Start with a workflow, not an architecture: receipt → matching → resolving exceptions → approval → payment. For each stage, ask what triggers it, who acts, what data they need, and what a delay or mistake changes. If approval waits two days while matching takes minutes, faster extraction might leave the important delay untouched. Conversely, if clerks spend hours assembling evidence needed for approval, the same mechanism may address the constraint. The workflow tells you which question to investigate next.

Now make an explicit hypothetical model. Assume 120 invoices per week, 8 active handling minutes per invoice, and labor valued at ₹300 per hour. Then baseline active work is 120×8/60 = 16 hours per week, valued at ₹4,800. This is an assigned labor-value estimate, not an observed cash expense removable from a budget.

Assume a proposed process needs 3 review minutes per invoice plus 2 hours of weekly maintenance and exception support. It uses 120×3/60 + 2 = 8 hours weekly. Potential released capacity is 8 hours, valued at ₹2,400 per week. With 12 hours of onboarding spread across an explicitly chosen eight-week assessment period, the additional burden is 1.5 hours per week. Net capacity value over that period is therefore (8−1.5)×₹300 = ₹1,950 weekly, before a service fee or unmodeled costs.

If the current process actually needs only 4 minutes per invoice, its baseline is 8 hours. The proposed recurring process also needs 8 hours; onboarding makes the eight-week comparison worse by 1.5 hours weekly. One uncertain baseline parameter reverses the apparent benefit. The next useful evidence may be a workflow observation rather than a more capable extraction model.

This model has deliberate limits. It assumes comparable invoice mix and outcome quality, no overlapping time categories, and an agreed value for released time. It excludes error consequences, waiting-time value, and price. You cannot call ₹1,950 a price ceiling or forecast revenue from it: the buyer may value another outcome, lack a usable budget, or reject the operational risk. B02 will develop the economics more fully.

## 4. Write the hypothesis before collecting convenient evidence

A working hypothesis for the fictional case is:

> Among purchasing teams handling 100–200 invoices weekly with manual matching, matching work is a material constraint; at least one authorized team will commit to a bounded evidence-assistance trial if source traceability and human approval are preserved.

This contains two claims: the problem matters and an offer can earn a trial. Investigate them separately. For a small first investigation, propose five conversations across at least three organizations, including operators and decision makers. This is a manageable learning batch chosen for the exercise, not a statistically sufficient sample or a universal quota.

Before starting, define a decision rule. For example: proceed to designing one trial only if at least two independent organizations can describe recent costly matching episodes and one authorized sponsor agrees to supply permitted sample cases, a reviewer, a date, and a success criterion. If matching is consistently quick or the dominant delay lies elsewhere, revise the problem definition. If operators report pain but the sponsor cannot authorize data access, investigate that dependency before building the trial.

These are gates for a limited next investment. Passing them does not validate a market. Missing them may expose a poor recruitment channel or a misdefined segment rather than prove that nobody needs the product. Record the reason for each outcome instead of collapsing all refusals into a single number.

## 5. Prepare an interview that reconstructs work

The following is an original short guide for the invoice case. Adapt the nouns to a workflow you can legitimately observe. Keep questions neutral enough to permit “this is already easy.”

1. Walk me through the most recent invoice that needed additional checking. What happened first and next?
2. Which records or people did you need at each step? What did you do while waiting?
3. Which parts required your active attention, and how would we check that estimate?
4. What happened if the check was delayed or wrong? Can you identify an actual recent consequence?
5. Over a defined recent period, how many cases were routine and how many needed exceptions?
6. What changes have you already tried? Which parts of the current process would you keep?
7. Describe the last time a new tool or service entered this workflow. Who approved it, and what slowed adoption?
8. What is missing from my reconstruction? Who else sees a different part of the process?

Use a separate, clearly signaled offer discussion if proposing a trial later. A research interview and a purchase decision have different purposes. The plan in this file authorizes neither contact nor collection of customer data; it is study material. Any future observation should use permitted examples, and recording requires the participant's agreement.

## 6. Keep evidence traceable through interpretation

Use one row per episode or commitment. Preserve the person's account and your interpretation separately. The following blank structure is reusable without pretending that an interview occurred:

| Field | What to record |
| --- | --- |
| Episode ID / date / source | A stable reference; when the work happened; whose perspective it represents |
| Role and context | Operator, buyer, approver; relevant workload and constraints |
| Account and supporting artifact | What was reported; what was directly observed; permitted document or log reference |
| Measurement status | Measured, estimated by participant, derived, or unknown |
| Alternative and consequence | What happened without your offer; what it cost or prevented |
| Interpretation | Your explanation, explicitly separated from the account |
| Rival explanation | A plausible reason the evidence could mean something else |
| Next check | The smallest observation that would distinguish those explanations |

“Three employees described the same failure” may be three perspectives on one episode. It is not necessarily three independent occurrences or customers. If a participant estimates two hours, record an estimate; do not silently promote it to a timing measurement. If notes disagree, preserve the disagreement and identify whether they refer to different work types, dates, or definitions.

The distinction resembles F01's discipline of stating what a representation contains. Here, however, there is no proof that a sample of conversations represents a whole market. Keeping a faithful record improves the reasoning process without removing sampling and interpretation uncertainty.

## 7. Commitments answer different questions

| Signal | Legitimate inference | Counterexample / next check |
| --- | --- | --- |
| Compliment | Positive conversational reaction | Courtesy; ask what concrete problem it relates to |
| Stated future interest | A claim of intent under imagined conditions | Priority changes when actual terms arrive |
| Agreed trial | Willingness to allocate specified resources | Free consulting or curiosity; record workload, owner, success criteria |
| Payment | A transaction under known terms | Exceptional discount or bespoke work; inspect scope and repeatability |
| Repeated voluntary use | Continued use within observed conditions | Mandate or dependency; investigate whether the intended benefit occurs |

This is a question-specific comparison, not a universal numeric ranking. A token payment from a friend can be weaker evidence for your target segment than a carefully scoped trial with its actual buyer. Repeated use does not automatically establish profitability. A data-access refusal does not automatically establish lack of need.

Counterexample: five friendly developers praise a purchasing demo; none performs invoice matching or controls its budget. The evidence supports demo appeal in that group. It cannot support a claim that purchasing managers will adopt it. Another counterexample: a manager funds a trial primarily to obtain custom integration services. That transaction may support a services offer while leaving a self-serve product hypothesis unresolved.

## 8. Trade-offs and the next smallest test

Interview first when the workflow and constraint are unclear. Observe a permitted real episode when estimates or handoffs matter. Use a bounded prototype trial when the outcome and decision owner are clear but feasibility or workflow fit is uncertain. Consider a manual demonstration of the proposed output when it can test usefulness cheaply, while recording human effort so later economics do not mistake it for automated delivery.

Change the plan when evidence changes. If the tool saves handling time but review becomes harder, redefine the outcome around total correct completion. If the buyer cannot adopt external software, examine an internal option or a different segment rather than assuming more accuracy removes the blocker. If current alternatives already meet the objective, investigate another unsolved part of the workflow or stop investing.

F03 will examine sampling and causal claims. A05 will connect evaluations to complete customer tasks. B03 will test adoption paths and product boundaries. B01 contributes the problem definition and explicit unknowns those later models need.

## 9. Bounded exercise and reference card

Spend approximately 30–45 minutes preparing a one-page plan; this duration is only a suggestion. Choose a business workflow you can observe, or retain the fictional invoice case. Do not conduct outreach as part of this exercise.

1. Define the segment, trigger, user, buyer, current alternative, and consequential outcome. Mark unknown roles.
2. Write a falsifiable problem hypothesis and a separate trial/adoption hypothesis. Name evidence against each.
3. Draft six neutral questions about a recent episode, including cost, alternatives, and the approval process.
4. Recalculate the hypothetical model at 8 and 4 baseline minutes. Explain why released capacity is not automatically cash savings or willingness to pay.
5. Classify these fictional signals: developer praise; a clerk's estimate of weekly burden; a sponsor's dated trial commitment; payment for a custom integration; repeated use required by a manager. State what each leaves unknown.
6. Write proceed/revise/stop criteria and a response to this change: matching is quick, but missing delivery records delay approval for two days.

Reference card: name the segment → reconstruct an episode → map roles and alternatives → separate observation from inference → state a rival explanation → request evidence relevant to one next decision. A small sample informs a next step; it does not by itself measure market prevalence. Unknowns stay unknown until evidence changes them.

## 10. Evidence ledger and limitations

Primary source R19: [YC, Startup School Week 1 Recap: Kevin Hale and Eric Migicovsky](https://www.ycombinator.com/blog/startup-school-week-1-recap-kevin-hale-and-eric-migicovsky/), published 2019-09-04; transcript inspected 2026-11-02. Timestamp ranges identify transcript passages, not new claims of video playback.

| Supported source role | Verified locator | Evidence boundary |
| --- | --- | --- |
| Specific past episodes and listening | Migicovsky segment 17:03–20:25 | Practitioner guidance |
| Existing attempts and alternatives | 20:25–25:41 | Interview prompts, not measured demand |
| Cost, recurrence, budget, authority | 30:31–33:44 | First-customer selection advice |
| Caution about compliments and hypotheticals | 38:21 through segment end | Qualitative advice |
| Startup-investor context | Hale 02:13–03:49 | Growth-oriented lens; not a requirement for every business |
| Numerical case, evidence table, gates, questions, counterexamples | Original §§2–9 and answers | Hypothetical teaching design and conditional derivation |

No current market size, conversion rate, validated pricing, or customer behavior is asserted. Source anecdotes are not treated as causal proof; its later product-market-fit percentage discussion is not used as a universal threshold. Remaining empirical questions concern the chosen segment, actual workload, authority, adoption constraints, and repeat behavior. They do not block producing the next curriculum pack. Audit A remains pending.

## Revision history

- 1.0 — 2026-11-02: original B01 pack and separate worked answers; no interviews or outreach performed.

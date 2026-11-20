# B02 — Unit economics, pricing units, and sensitivity

| Field | Value |
| --- | --- |
| ID / revision / date | B02 · 1.0 · 2026-11-12 |
| Title | Unit economics, pricing units, and sensitivity |
| Prerequisites | F02 expected values; B01 problem and commitment evidence; A05 outcome contracts |
| Capability developed | Build a cost model with defensible units, expose its breakpoints and choose the next measurement |
| Source-check status | R20 unit metrics, R21 packaging and R12 elasticity passages inspected |
| Experiment status | Original hypothetical ledger; exact arithmetic and sensitivity checks executed; no customer or billing experiment |
| Companion | [Hints, worked answers and executable checks](SDE_B02_answers.md) |

## Which unit pays for the work?

The invoice service prepares supported evidence for a human reviewer. A cheaper model call sounds attractive, but the buyer needs a correct, timely result. A call can fail, require another call, create review work, or produce nothing billable. The decision is whether an offer can deliver its promised outcome at a sustainable cost, and which uncertain input is worth measuring before investing further.

F02 introduced an expected value: multiply each possible quantity by its probability and add. B01 separated useful released capacity from actual cash savings. A05 separated a contract-correct refusal from a supported draft. B02 combines these boundaries into a deliberately simple service model. It is managerial reasoning, not a set of accounting, tax or investment recommendations.

R20 distinguishes technical efficiency metrics from business unit metrics. R21 treats packaging as different feature/usage arrangements for customer groups. These practitioner sources motivate our choice of units; they do not supply the numbers or prove that a customer will pay them. R12 provides historical reasoning about provisioning risk, not current cloud prices.

## Define a case before counting money

Use one monthly intake cohort. A **case** is one eligible submitted invoice requiring one supported evidence package. Revisions, retries and duplicate requests remain attached to that case. A **run** is an execution within it; a **call** is a resource-consuming operation. Billing a retry as a new case would change the offer, not improve delivery.

For this lesson a successful case has a verified, supported package delivered within the agreed deadline, with no unauthorized disclosure or effect. An unresolved case may be a correct safe response but is not a billable success under this invented offer. This differs intentionally from A05's broader contract-success metric. A human still approves any payment; producing evidence does not grant payment authority.

Before measuring, specify eligibility, verification rubric, deadline, duplicate identity, dispute/refund rules and the observation window. Count offered, eligible, attempted, successful, unresolved and rejected cases separately. Here every eligible case is attempted once by a fixed procedure; any internal calls are included in that procedure's cost. The optional retry extension below is a separate scenario.

Let N be eligible attempted cases, p their success probability, P the price per verified success, c the expected variable cost per attempted case and F the fixed cost over the month. Price is a contractual revenue unit; cost is a resource unit. They need not use the same denominator.

## Build a ledger with mutually exclusive costs

Every numerical input in this pack is invented, in a common currency unit called U. No number is a provider quote, customer observation or forecast. Assume success proportion p=0.8 and N=1,000. We use exact counts of 800 successes and 200 failures for the worked ledger; the probability model generalizes it for planning.

| Cost category | Assigned rule | Monthly amount |
| --- | --- | ---: |
| Compute and storage directly attributable to processing | 0.4 U per attempted case, including internal calls | 400 U |
| Routine verification | 2 active minutes per attempted case × 0.5 U/minute | 1,000 U |
| Routine support | 0.2 U per attempted case | 200 U |
| Additional failure handling | 2 U per failed case, beyond routine review/support | 400 U |
| Fixed service overhead | 1,500 U per month within the stated capacity range | 1,500 U |

Assume the review labor can be purchased proportionally at this rate. If it is salaried staff already paid regardless of work, the cash-cost classification changes: record the committed salary and usable capacity separately rather than counting both salary and the same minutes as expenses. Similarly, failure support must exclude minutes already in routine verification. Every ledger category needs an owner and a non-overlap rule.

Expected variable cost per attempt is

\[
c=0.4+2(0.5)+0.2+(1-p)2=3.6-2p.
\]

At p=0.8, c=2 U. Total variable cost is 2,000 U; variable cost per successful case is 2,000/800=2.5 U. Including the fixed overhead gives 3,500/800=4.375 U per success. Reporting only the 0.4 U compute charge omits most of the delivery cost.

For actual observed counts use total attributable cost divided by actual successes. For planning, c/p is a ratio of expected totals under stable assumptions. It is not generally the expectation of the random ratio cost/successes; a small month can have zero successes. At zero successes report incurred cost and no finite unit-success ratio.

## Contribution is not profit

Suppose P=4 U per verified success, with all qualifying invoices collectible, no refunds and no payment fees in this toy model. Expected revenue is NpP=3,200 U. **Contribution** is revenue minus variable delivery cost: 1,200 U. It is the amount left to cover fixed costs, not company profit.

Our modeled monthly operating remainder is

\[
\Pi=N(pP-c)-F.
\]

Here it is 1,200−1,500=−300 U. This remainder excludes taxes, financing, acquisition costs, unlisted development and other expenses; even a positive value would not establish total company profitability. Actual cash flow also depends on collection timing and upfront payments. A positive accrued margin cannot fund next week's payroll if cash arrives later.

Define contribution per attempt m=pP−c. If m>0 and F stays fixed, modeled break-even volume is F/m. At the baseline, m=1.2 and break-even is 1,250 attempted cases. At m=0 no positive fixed cost is recovered; when m<0, more identical work deepens the loss. A volume forecast is still required: algebra does not recruit customers.

The contribution fraction of revenue is 1,200/3,200=37.5% in this definition. Do not label it gross margin without defining which costs that accounting measure includes. A per-case contribution and a percentage of revenue answer different questions.

## A cheaper model can lose

Compare an alternative on the same population, outcome rubric, price and overhead. Assign compute cost 0.1 U, routine review 3 minutes at 0.5 U/minute, routine support 0.3 U, success p=0.7, and unchanged 2 U extra failure handling.

Its variable cost is 0.1+1.5+0.3+0.3×2=2.5 U per attempt. Per success it is 2.5/0.7≈3.571 U, worse than the baseline's 2.5. At 1,000 attempts, revenue is 2,800, contribution is 300 and modeled remainder is −1,200 U. The compute component fell 75%, but additional labor and failure handling erased that saving.

This is a counterexample, not evidence against any named model. Re-evaluate p, review time and support together on matched cases. Holding success constant while claiming labor savings from a changed review process can conceal a weaker verification standard. Keep authority and quality gates independent of the economic objective; no attractive margin licenses an unsafe output.

## Sensitivity reveals the decision boundary

With baseline costs and P=4, m=4p−(3.6−2p)=6p−3.6. Positive contribution requires p>0.6. At 1,000 attempts, covering F=1,500 requires p≥0.85. A success rate of 80% clears the first gate but fails the second.

| Change from baseline | Contribution per attempt | Monthly remainder at N=1,000 |
| --- | ---: | ---: |
| p=0.6 | 0 | −1,500 |
| p=0.8 | 1.2 | −300 |
| p=0.9 | 1.8 | 300 |
| P=3, p=0.8 | 0.4 | −1,100 |
| P=5, p=0.8 | 2.0 | 500 |
| Routine support becomes 0.7, p=0.8, P=4 | 0.7 | −800 |

At baseline quality and volume the price needed to cover the modeled costs is (c+F/N)/p=4.375 U. This is a cost-covering threshold, not willingness to pay. A price increase may reduce demand, change customer mix or raise service expectations. A one-variable sensitivity table is a diagnostic; a scenario must change related variables together.

For example, N=500,1,000,1,500 at baseline assumptions yields remainders −900,−300,300 U. Now suppose serving more than 1,500 cases requires an additional 600 U monthly capacity block. At N=1,501, remainder becomes −298.8 U, despite more demand. It returns to zero at N=1,750, assuming this second capacity tier is sufficient. Fixed costs are fixed only over a range and time horizon. Do not extrapolate the first break-even line indefinitely.

R12 §6.1 discusses over- and under-provisioning risk. Our step cost is an original abstraction. Real queues, reserve commitments, hiring delays and latency can change both cost and p. A service may be memory-feasible and still miss deadlines, as A04/C02 established.

## Retries need conditional evidence

Consider one additional attempt only for baseline failures. Let r=0.25 be the chance of recovering a success **among those failed cases**, and d=1 U the incremental cost of the retry including its added review. Original handling cost is already sunk; do not charge it again. Assume recovery remains within the original deadline and uses the same verified-success rubric.

Then p_new=p+(1−p)r=0.85, and incremental contribution per original case is (1−p)(Pr−d). With P=4, r=0.25 and d=1, this is zero: 200 retries cost 200 U and add 50 billable successes worth 200 U. More successes need not improve contribution. It might still matter for retention or a quality obligation, but those are additional premises.

Do not reuse the unconditional 0.8 as the retry recovery rate. Failed cases can be systematically harder. Nor does 1−(1−p)^k apply without the appropriate independence and identical-success assumptions. Measure the conditional recovery and resource distribution of the actual retry policy.

## Choose a pricing unit without confusing it with value

| Offer hypothesis | Revenue driver | Main question to test |
| --- | --- | --- |
| Per attempted case | Accepted submissions | Will buyers pay for unresolved work; can duplicate billing be prevented? |
| Per verified successful case | Agreed outcome evidence | Who verifies success, resolves disputes and pays failure costs? |
| Subscription with included usage and overage | Account, allowance, extra work | Does the allowance cover variable workload without surprising either side? |

R21's packaging discussion supports examining feature/usage boundaries for different customers. These three offers are original hypotheses, not recommended prices. Outcome billing can align a useful unit while introducing verification and dispute costs. A subscription can simplify budgeting while exposing the supplier to heavy usage. Keep the workload/cost model for each customer segment, not just an average across unlike accounts.

An internal deployment may have no sales revenue. Replace revenue with a separately justified benefit measure and budget decision; do not invent external sales or call released staff time cash savings. B01's buyer, approver and operator roles still matter. B03 next examines how an offer is found, adopted and retained.

## Measurement plan and reference card

Record case identity and cohort, versions, eligibility, success verification and time, calls/retries, attributable charges, non-overlapping review/support minutes, refunds, realized billing and shared-cost allocation. Reconcile totals with the accounting window; amortize onboarding only over an explicit horizon and also report its upfront cash requirement. Segment routine and difficult cases. Investigate missing cost tags rather than assigning their cost to zero.

Estimate p and effort from representative held-out work, preserving supplier/document dependence. Compare plausible joint scenarios and severe-loss cases, not only averages. This model omits rare consequential harms; adding an expected loss term can aid a decision but does not replace safety constraints or tail analysis. No sample size or empirical confidence interval is claimed here.

**Reference card:** define the case and success → separate cost and billing units → include failures and labor once → calculate contribution → subtract horizon-matched fixed costs → check capacity tiers → vary coupled assumptions → collect the evidence that could reverse the decision.

## Practice

1. Rebuild the baseline monthly ledger and both variable/full cost-per-success ratios. Explain the cash-labor assumption.
2. Calculate contribution, revenue fraction, operating remainder and break-even volume. Explain why none proves company profitability.
3. Compare the cheaper-model alternative. State what matched measurements could overturn this constructed result.
4. Derive success and price thresholds, the support sensitivity and the capacity-tier discontinuity at 1,501 cases.
5. Derive the retry policy's new success rate, incremental cost and contribution. Find the conditional recovery threshold for positive incremental contribution.
6. Compare the three pricing units for the same job. Propose a bounded evidence collection plan that could reject a seemingly profitable offer.

## Evidence and open inputs

| Basis | Inspected locator | Scope |
| --- | --- | --- |
| R20 FinOps Foundation | [Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/), Define Unit Metrics which support Organizational Goals; Definition; accessed 2026-11-12 | Technical versus business metrics and documented scope; practitioner framework |
| R21 Patrick McKenzie / Stripe | [Pricing low-touch SaaS](https://stripe.com/guides/atlas/saas-pricing), introduction and Pricing and packaging for things with no physical form | Packaging guidance; case anecdotes and historical prices are not demand estimates |
| R12 Armbrust et al., 2009 | [Berkeley report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2009/EECS-2009-28.pdf), §6.1 Elasticity: Shifting the Risk, printed p. 10 | Historical provisioning-risk argument; no current rates adopted |
| Original derivations | Ledger, alternatives, thresholds, tiers, retry extension and companion script | Hypothetical inputs, executed arithmetic; no business experiment |

Actual demand, willingness to pay, collections, success distribution, review/support burden, capacity and omitted costs remain unknown. No essential source-access blocker remains. No learner answers or mastery inferred.

## Revision history

- 1.0 — 2026-11-12. Case-level economics, sensitivity, conditional retries and six exercises.

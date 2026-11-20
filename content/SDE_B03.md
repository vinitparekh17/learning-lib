# B03 — Distribution, product boundaries, and defensibility

| Field | Value |
| --- | --- |
| ID / revision / date | B03 · 1.0 · 2026-11-13 |
| Prerequisites | B01 customer evidence; B02 unit economics; S06/A05 for authority and outcome contracts |
| Capability developed | Choose an adoption path and responsibility boundary, then test whether the offer survives a stronger alternative |
| Source-check status | R22 Recruit/Delight/Manual, R21 packaging, R19 budget/authority passages inspected; evidence ledger below |
| Experiment status | Hypothetical scenarios and exact arithmetic checked; no outreach, customer trial, supplier test or market result |
| Companion | [Hints, worked answers and reproducible checks](SDE_B03_answers.md) |

## A good component can still be a poor offer

A document model can extract invoice fields accurately while the purchasing team continues using a spreadsheet. Perhaps nobody reaches the budget owner. Perhaps importing records takes longer than matching them. Perhaps the team cannot send data outside its environment. These are different bottlenecks; a better extraction benchmark does not resolve them all.

The question is: why would a particular customer find, adopt, keep and pay for this offering when alternatives improve? **Distribution** is the path to a qualified customer and an authorized adoption decision. **Product boundary** says which work and responsibilities the supplier accepts. **Defensibility** is a hypothesis that a valuable advantage can persist despite substitution or imitation. None is established by a feature list.

B01 asked whether the problem matters. B02 asked whether a useful unit can support its delivery costs. Here we hold the customer job constant while changing how the work reaches the customer and who performs it. The framework and cases are original teaching designs. Practitioner sources supply questions to investigate, not verified demand.

## Start narrow enough to observe the whole job

Retain the fictional purchasing workflow: assemble invoice and delivery evidence for a human payment reviewer. Choose an initial segment of small purchasing teams that repeatedly match a limited set of document formats, have an identifiable operations buyer, and can authorize a bounded pilot. This is a proposed segment, not a claim about its prevalence. Teams barred from external processing require a different deployment path.

The job ends when an authorized reviewer receives a supported, timely evidence package or a clearly unresolved case. Payment approval remains outside the product. An assistant that silently guesses missing evidence fails the contract even if the user likes its writing. The clerk uses the output, the operations manager funds it, and a data/security owner permits access. One person might fill several roles; do not assume that a willing user can authorize all of them.

A first distribution route could be introductions through a bookkeeping practitioner who already works with this segment, followed by a workflow demonstration to its buyer. That is a channel hypothesis. It requires permission and a credible reason for the practitioner to introduce you; it is not an audience you already possess. A fallback is a narrowly relevant professional community with an approved demonstration. Count distinct organizations, record referral incentives, and separate warm contacts from independently reached customers.

R22 recommends manual early recruitment and attentive service, including doing work manually before automating it. Its founder anecdotes motivate a small learning route, not a causal claim that handholding creates a scalable business. R19's budget and authority discussion motivates checking who can actually approve the change.

## Model adoption as several observable transitions

Define events before collecting counts. A **qualified organization** fits the segment and has a relevant recent problem. **Activation** means completing the first permitted real workflow to the agreed quality bar, not opening an account. **Repeat use** means another eligible workflow cycle with the same success definition. A paid contract and a useful outcome are separate events.

For an invented completed outreach cohort, suppose 40 distinct organizations are reached, 12 qualify, 6 agree to a demonstration, 3 activate, and 2 complete a second eligible cycle. Every later set is a subset of the earlier one, and all organizations have enough follow-up time. Overall repeat-use fraction is 2/40=5%. Conditional fractions are 12/40, 6/12, 3/6 and 2/3; their product equals 2/40 by cancellation. No independence assumption is needed for these nested observed fractions. Multiplying rates from different cohorts would require additional transportability assumptions.

The six demonstrations and only three activations suggest investigating onboarding, access or fit. They do not prove onboarding caused the loss. Track refusal reasons and elapsed time: an organization waiting for approval is not the same as a completed rejection. Recent cohorts without a second cycle yet are not mature retention cohorts. In small samples, a single organization changes the percentage substantially.

If recruitment and demonstrations cost 600 U, acquisition cost per activated organization is 600/3=200 U. Cost per repeated-use organization is 300 U, a different descriptive ratio. Neither denominator implies payment. With zero activations, report 600 U spent and an undefined finite acquisition ratio rather than zero cost.

## Three boundaries around the same job

All options preserve evidence traceability, access control and customer payment approval. Their completion promises and operational owners must be explicit.

| Dimension | Self-serve hosted tool | Managed evidence service | Internal deployment |
| --- | --- | --- | --- |
| Offer | Software assembles a draft; customer operates checks and exceptions | Supplier operates assembly and first review; customer authorizes final use | Customer runs the workflow inside its controlled environment |
| Buyer / route | Operations buyer; focused demo, documented trial and self-onboarding | Operations buyer; scoped proposal through trusted introduction | Operations sponsor plus IT owner; internal budget and deployment review |
| Onboarding | Customer maps fields and imports permitted records | Supplier helps map records within a bounded engagement | Customer integration, access policy, release and rollback process |
| Required trust | Hosted data handling, traceable outputs, export and support terms | Same plus named human access, confidentiality and escalation ownership | Local operator competence, controlled dependencies, patching and incident ownership |
| Variable labor | Customer verification; supplier support still exists | Supplier verification and exceptions; customer final review persists | Customer verification and operations; external support only if separately purchased |
| Maintenance burden | Supplier service changes; customer mapping changes | Supplier process/staff training plus software changes | Customer runtime, connectors, evaluation and upgrades |
| Switching friction | Mapping/export and user retraining | Replacement of process knowledge and service handoffs | Migration of integrations, policies and operational knowledge |
| Supplier exposure | Hosted/API price, policy, availability and bundling | Those dependencies plus labor availability | External model/package dependencies can remain even with local hosting |

Internal deployment does not automatically mean offline operation. A locally installed interface calling an external model still exports data. Draw the actual boundary. Likewise, a managed service is not a transfer of every liability: the final approval owner and unresolved-case escalation remain named.

R21 describes packaging through feature and usage differences for customer groups. Our three responsibility boundaries go beyond pricing columns. A plan becomes misleading if it sells a managed outcome while budgeting only for software delivery.

## A worked comparison with both sides of the ledger

Every number below is invented, in a common unit U. These are new B03 scenarios, not edits to B02's baseline. Compare one organization with 100 eligible cases per month over six months. Assume matched quality, deadlines and authorized access have already passed feasibility checks. That premise must be tested before any real choice.

Customer labor is valued at 30 U/hour. Current handling takes 8 minutes per case: 400 U/month. It is capacity value, not automatically avoidable payroll. All recurring customer minutes include verification, residual handling and allocated operations time; all one-time customer hours include setup and switching. No category overlaps.

| Input per organization | Self-serve | Managed | Internal |
| --- | ---: | ---: | ---: |
| Monthly supplier fee | 120 U | 180 U | 0 U |
| Customer recurring minutes per case | 4 | 2 | 3 |
| Customer one-time onboarding hours | 4 | 2 | 12 |
| Customer recurring infrastructure cost | 0 U | 0 U | 40 U/month |
| Supplier variable monthly delivery cost | 40 U | 120 U | Not a supplier revenue offer here |
| Supplier one-time onboarding cost | 60 U | 90 U | Not applicable |

Let H be months, n cases/month, b baseline minutes/case, t new minutes/case, w labor value/hour, f monthly fee, i monthly infrastructure cost and o onboarding hours. Customer modeled net capacity value is

\[
V=H[n(b-t)w/60-f-i]-ow.
\]

This subtracts fees and setup from valued capacity. It excludes unmodeled risk, financing and benefits unrelated to handling time. It is not a willingness-to-pay estimate.

At H=6, self-serve gives 6(200−120)−120=360 U; managed gives 6(300−180)−60=660 U; internal gives 6(250−40)−360=900 U. Internal has the highest modeled value, but its feasibility depends on the actual IT owner and maintenance allowance. If that owner cannot support it, the ranking is irrelevant. For a permitted outsourced pilot with no internal operator, managed is the tentative choice, conditional on its effort estimates.

Now examine the supplier. Monthly contribution before shared overhead and acquisition is 80 U for self-serve and 60 U for managed. Assign the same hypothetical acquisition cost of 200 U to each newly activated paying organization for this comparison. Six fully paid months leave 6×80−60−200=220 U for self-serve and 6×60−90−200=70 U for managed, before shared overhead. Managed creates more modeled customer value yet leaves less supplier contribution. Both sides must work.

Continuous-month recovery of acquisition plus supplier onboarding is 260/80=3.25 months and 290/60≈4.83 months. With contribution collected at month end, recovery first occurs after months 4 and 5. These are conditional payback calculations, not lifetime-value forecasts. If service ends after three paid months, remainders are −20 and −110 U. No constant churn assumption rescues a cohort that has not been observed.

## Break the recommendation deliberately

Suppose managed customer effort is actually 5 minutes/case because exceptions require customer rechecking. Its six-month value becomes 6(150−180)−60=−240 U. The managed recommendation fails even though the supplier fee and demo accuracy are unchanged. The next measurement should capture total customer effort and correct completion, not only supplier review time.

Alternatively, an internal variant with an additional 6 hours/month of customer maintenance adds 180 U/month. Its modeled value falls from 900 to −180 U. This is incremental maintenance beyond the original table's allowance, not the same hours counted twice. “Runs internally” is a location, not a maintenance budget.

Manual onboarding can reveal repeated problems worth automating. It can also mask a different bespoke workflow for every customer. Keep a work log split into reusable setup, customer-specific setup, recurring operations and exceptions. Move toward self-serve when repeat customers can complete the workflow with documented setup and measured support effort. Keep a service boundary when valuable recurring human judgment remains necessary and its costs can be funded. Stop or narrow the offer when neither boundary satisfies the joint quality, customer-value and supplier-cost conditions.

## The supplier bundles your main feature

Treat this as a hypothetical stress test, not news about a named supplier. Assume a customer's existing platform adds equivalent extraction at zero incremental fee. First ask whether it also solves evidence mapping, authorization, exceptions and review. A free component may still require costly workflow work.

Assign the bundle 5 customer minutes/case and 3 onboarding hours, with no additional infrastructure charge. Its six-month value is 6×150−90=810 U. Under those premises it beats the managed offer's 660 U by 150 U. The bundle is not automatically inferior because it lacks our interface, nor automatically equivalent because its extraction score matches.

For managed to tie that bundle while retaining 2 customer minutes/case, solve 6(300−f)−60≥810: f≤155 U/month. At 155, supplier six-month remainder is 6(155−120)−90−200=−80 U. The supplier needs f≥120+290/6≈168.33 U to recover these modeled costs within six months. There is no feasible price interval under these assumptions. Negotiating the price alone cannot repair this scenario. Reduce delivery/acquisition costs, prove additional customer value, choose a different segment, or decline the offer. Bundling may also reduce the supplier's own compute bill; that is a separate scenario requiring evidence.

## Turn a moat claim into a test

| Claimed advantage | Mechanism to test | Evidence against it |
| --- | --- | --- |
| Workflow knowledge | Faster correct onboarding across new organizations | Every setup remains bespoke; partner handles it equally well |
| Evaluation corpus | Permitted representative cases detect failures competitors miss | No reusable rights, stale cases or no outcome improvement |
| Distribution relationship | Repeat access to qualified buyers at acceptable effort | Referrals depend on one person; channel costs erase contribution |
| Integration and trust | Useful reliable handoffs plus credible data/control practices | Bundle already provides the same end-to-end outcome |
| More customer data | Authorized feedback improves a defined outcome for later customers | Data cannot be reused or more data adds no measurable benefit |

These are original testable hypotheses, not an empirical taxonomy of winning businesses. More records do not by themselves establish a network effect; demonstrate how another participant improves value for existing participants under permissible reuse. Switching friction can delay departure without proving satisfaction. Offer usable exports, preserve evidence identifiers and test migration; voluntary renewal despite a credible alternative is more informative than retention caused by trapped records. No source inspected here establishes an actual moat for this service.

## Practice, connections and reference card

Prepare a short comparison when studying later; no learner response is required for production.

1. Specify segment, user, buyer, approver, acquisition route and activation event for the invoice job. Identify one rival explanation for low activation.
2. Recalculate the nested cohort fractions and both acquisition ratios. Explain the zero-activation and incomplete-follow-up cases.
3. Rebuild the three customer-value results. State the feasibility condition that makes the highest numerical value unusable, then evaluate both labor shocks.
4. Rebuild supplier contribution, six-month remainders and both payback conventions. Evaluate departure after three paid months.
5. Calculate the bundled alternative and the managed customer's fee ceiling versus the supplier's cost floor. Decide whether price alone can fix the offer.
6. Propose a bounded pilot and a defensibility test. Name trust boundaries, a stop rule, a counterexample to a data-moat claim and evidence that changes the recommended product boundary.

B01 contributes problem/authority evidence; B02 contributes explicit units and cost scope; S06 preserves authority independently of sales promises; A05 preserves whole-task evaluation. C04 will turn these into a fuller decision memo, and C06 will examine supplier replacement. B03 teaches the comparison mechanism rather than completing those later assignments.

**Reference card:** name one job and segment → map buyer and approval roles → define acquisition/activation/repeat events → assign responsibility and labor → compare customer and supplier economics → test a stronger alternative → name the observation that changes the choice.

## Evidence ledger and unresolved inputs

| Basis | Verified primary locator, accessed 2026-11-13 | What it supports / limits |
| --- | --- | --- |
| R22 Paul Graham, July 2013 | [Do Things that Don't Scale](https://paulgraham.com/ds.html), Recruit, Delight and Manual sections | Manual recruitment/service as practitioner guidance; selected-success anecdotes do not establish conversion effects or market prevalence |
| R21 Patrick McKenzie / Stripe | [Pricing low-touch SaaS](https://stripe.com/guides/atlas/saas-pricing), Introduction and Pricing and packaging for things with no physical form | Packaging by features/usage and customer group; historical examples are not present prices or validated demand |
| R19 YC / Eric Migicovsky, 2019-09-04 | [Startup School Week 1 transcript](https://www.ycombinator.com/blog/startup-school-week-1-recap-kevin-hale-and-eric-migicovsky/), 30:31–33:44, cost/frequency/budget/authority discussion | Interview questions and first-customer considerations; practitioner advice, not a causal study |
| Original synthesis and derivations | All numerical fixtures, comparison tables, threshold algebra, pilot rules and defensibility tests above; companion script | Hypothetical inputs and executed arithmetic only; not market findings or legal/accounting guidance |

Unresolved: actual customer workload and time value, access permissions, buyer commitment, paid retention, supplier costs, maintenance burden, reusable data rights and alternative quality. These are application inputs, not blockers to this lesson. No learner mastery is inferred.

## Revision history

- 1.0 — 2026-11-13. Distribution transitions, three responsibility boundaries, two-sided economics, supplier-bundling counterexample and six exercises.

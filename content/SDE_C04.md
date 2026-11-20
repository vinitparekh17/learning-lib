# C04 — Which product boundary makes the service viable?

| Field | Value |
| --- | --- |
| ID / title | C04 · Product-boundary decision memo |
| Revision / date | 1.0 · 2026-11-14 |
| Prerequisites | B01 customer evidence; B02 economics; B03 distribution and boundary comparison; S06 authority and reliability |
| Capability developed | Choose who delivers, operates and controls a service using explicit feasibility gates and two-party economics |
| Source-check status | R19 budget/authority, R21 packaging, R11 design principles inspected; locators below |
| Experiment status | Hypothetical decision model and exact arithmetic checked; no customer, deployment or security experiment |
| Companion | [Worked analysis and executable checks](SDE_C04_answers.md) |

## Decision and scope

**Choose the managed evidence service for the initial six-month planning case.** It meets the assigned onboarding constraint and gives greater modeled customer value than the feasible self-serve alternative. When the customer increases available onboarding capacity from four to twelve hours, revise the choice to internal deployment, provided its operating owner and control checks remain satisfied. This is a conditional decision, not a recommendation to buy or deploy an actual product.

B03 compared three boundaries around invoice matching. This memo reuses its numbers deliberately, then adds a decision owner, resource constraints, supplier overhead, operational responsibilities and acceptance conditions. It does not repeat B03 as a new lesson or reinterpret its invented inputs as observations. “Viable” here means feasible for this customer and horizon, with acceptable modeled economics for each party that must deliver the offer. It does not mean a validated market or a profitable company.

The decision belongs to the fictional purchasing organization's operations sponsor. The budget owner, data owner, operator and payment approver may be different people. The supplier has a separate decision about whether it can fund delivery. A customer cannot choose a loss-making supplier offer into sustainability by liking it more.

## 1. One job and a fixed outcome contract

The job is to assemble invoice and delivery evidence so an authorized customer reviewer can decide what to do. The unit is one eligible invoice case; retries and document revisions do not create extra customer jobs. An acceptable evidence package identifies the source revision, relevant facts and unresolved discrepancies. It must arrive by the agreed operational cutoff, preserve access restrictions and avoid implying that payment has been approved.

All three candidates must meet the same evidence and timeliness rubric on the same case mix. The numerical comparison assumes they do so; that assumption must be tested before a real commitment. Unresolved cases are reported, not silently dropped from cost or success counts. Failure handling and ordinary rework are included in the assigned recurring effort. Unexpected consequential errors are separate stop conditions, not an affordable error allowance.

The incumbent manual process remains available. Its modeled incremental value is zero because it defines the comparison baseline. Keeping it may be the right action if every proposed option violates a hard constraint. This prevents a ranking exercise from forcing an unsafe or unfunded change.

## 2. The contract changes when responsibility changes

| Responsibility | Self-serve hosted tool | Managed evidence service | Internal deployment |
| --- | --- | --- | --- |
| Initial route | Buyer evaluates a documented trial; customer configures it | Buyer receives a bounded service proposal and named operator | Sponsor funds internal deployment with an accountable IT owner |
| Mapping and onboarding | Customer maps inputs using supplier documentation | Supplier performs mapping with customer confirmation | Customer integrates and validates the local workflow |
| Day-to-day preparation | Hosted software proposes; customer handles exceptions | Supplier staff/software prepare and first-review evidence | Customer staff/software prepare and resolve exceptions |
| Final business approval | Customer reviewer only | Customer reviewer only | Customer reviewer only |
| Runtime and recovery | Supplier operates hosted service | Supplier operates service and staffs escalation | Customer operates, patches, restores and monitors runtime |
| Data access | Explicit hosted-processing grant; support access separately scoped | Hosted grant plus named, scoped human access | Customer-controlled processing; external calls require separate permission |
| Exit | Export mappings, evidence IDs and unresolved work | Same plus documented manual handoffs | Retain deployable configuration, runbooks and data export |

R21's packaging guidance helps distinguish customer offers, but these alternatives differ in responsibility, not just feature limits. Calling an offer “managed” does not automatically transfer approval authority. Calling it “internal” does not prove data stays internal: remote inference, diagnostics and support attachments can cross the boundary.

Define one accountable owner for each operational failure. If a source record is missing, the preparation operator returns an unresolved case and the customer's workflow owner obtains the record. If service processing stalls, the runtime owner restores service or invokes the agreed fallback; the customer owns the decision to resume manual processing. If output support is wrong, the preparation owner investigates and the customer reviewer stops relying on the affected output. These roles should be part of the offer, with escalation contacts and observation windows, not assumptions hidden in a demo.

## 3. Authority remains a hard gate

Apply S06's separation between proposal and approval. A preparation worker may read the permitted case subset and write a draft. It cannot approve payment, change grants or select an unrestricted identity. The approval service checks authenticated principal, current permission, tenant/object, evidence revision and business state at its decision boundary. Current permission to read a historical result is separate from permission to create a new effect.

For example: a supplier analyst reads case A17 under a scoped grant, the customer revokes that grant, and the analyst then tries to retrieve another revision. The new read must be denied under this chosen contract. An old open page or earlier successful login is not fresh permission. Revocation cannot make already disclosed information unread; retention, export and deletion procedures address a different part of the lifecycle. Do not promise instant erasure merely because a token was disabled.

R11's fail-safe defaults, complete mediation and least privilege motivate these requirements. The source supplies principles; our workflow and serialized decision boundary are design applications, not certified implementations. Tests must include support tools, recovery scripts, exports and logs. A restrictive application screen does not constrain a shared administrator credential used behind it.

The managed service adds authorized human readers to the trusted surface. The internal option moves more operational responsibility to the customer. Neither label establishes stronger security without checking actual paths, privileges and recovery behavior. If external processing permission is absent, both hosted options are infeasible in this definition regardless of their economic rank. A redacted-data variant would be a new candidate requiring its own quality and cost evidence.

## 4. State the resource constraints before calculating value

Use B03's hypothetical organization: 100 eligible cases/month, six months of steady use, current handling time eight minutes/case, and customer labor valued at 30 U/hour. U is an invented currency unit. The comparison begins after onboarding; all options are assumed able to start by the same date if they fit the available setup capacity. No launch-delay benefit is inferred.

A qualified customer operating owner exists for all options and can fund the recurring time in the table. Initially only four total customer onboarding hours can be released before that date. Supplier setup capacity is available for the two hosted offers. External processing and managed human access are assumed authorized, and all candidates have passed the common quality/control gate for purposes of the model. These are premises, not reported interviews or tests.

| B03 input, preserved | Self-serve | Managed | Internal |
| --- | ---: | ---: | ---: |
| Monthly fee paid by customer | 120 U | 180 U | 0 U |
| Recurring customer minutes/case | 4 | 2 | 3 |
| Customer onboarding hours | 4 | 2 | 12 |
| Customer infrastructure/month | 0 U | 0 U | 40 U |
| Supplier variable delivery cost/month | 40 U | 120 U | Not an external offer |
| Supplier onboarding cost | 60 U | 90 U | Not applicable |

Customer recurring time includes review, exception work and allocated operations. In particular, the internal three-minute average must cover recurring maintenance under this fixture; it is not three review minutes plus free administration. Setup hours include integration, training and transition work. Salaried time represents capacity consumed, not automatically cash that can be removed from payroll. Infrastructure and fees are separate from those hours.

B01's distinction between role, problem evidence and commitment matters: a clerk's willingness to try the service does not release twelve IT hours. R19's cost, recurrence and authority prompts motivate confirming the allocation with its actual owner. No outreach is performed in this assignment.

## 5. Calculate both parties' ledgers

For H months, n cases/month, baseline b minutes, new t minutes, hourly labor value w, fee f, infrastructure i and customer setup o hours:

\[
V=H[n(b-t)w/60-f-i]-ow.
\]

This is modeled net capacity value, not willingness to pay or guaranteed cash savings. The baseline labor value is 100×8×30/60=400 U/month. Self-serve releases 200 U/month before fees, managed 300, and internal 250.

| Six-month customer result | Self-serve | Managed | Internal |
| --- | ---: | ---: | ---: |
| Net recurring value/month | 80 U | 120 U | 210 U |
| Setup capacity valued | 120 U | 60 U | 360 U |
| Net value V | 360 U | 660 U | 900 U |
| Fits initial four-hour setup cap? | Yes | Yes | No |

Internal wins the unconstrained arithmetic but is excluded initially. Among eligible choices, managed gives 300 U more modeled value than self-serve. Its 2-hour setup also leaves 2 hours of the initial allocation unused. Do not invent extra benefit for that slack; it is already reflected in the setup cost.

Now require an external supplier to cover its modeled costs over six paid months. Reuse B03's 200 U acquisition cost per paying organization, then add a new allocated overhead allowance of 10 U/month per organization. This overhead is distinct from variable delivery and onboarding. The supplier remainder is

\[
R=H(f-c-a)-u-A,
\]

where c is variable delivery, a allocated monthly overhead, u supplier onboarding and A acquisition. Self-serve gives 6(120−40−10)−60−200=160 U. Managed gives 6(180−120−10)−90−200=10 U. Both clear this limited nonnegative gate, but managed has little buffer. These are not company-profit claims; shared overhead allocation must reconcile to actual totals, and unlisted costs remain excluded. Internal deployment has no external supplier revenue in this fixture; its customer infrastructure/operations costs are already counted.

The initial decision is therefore managed, conditional on verifying assumptions and explicitly accepting the narrow supplier buffer. A 2 U/month increase in managed overhead changes its remainder from 10 to −2 U. Customer value is unchanged, but the delivery offer fails the stipulated supplier gate. Under that isolated shock, self-serve becomes the feasible positive-value alternative while internal remains setup-constrained.

## 6. Revise after one constraint changes

Now the customer releases twelve onboarding hours instead of four. Change only this capacity constraint: recurring operating skill, permission, quality, fees, demand and the six-month horizon are held fixed. Internal becomes feasible and offers 900 U, exceeding managed by 240 U. Revise the recommendation to internal deployment.

The extra allocation is not free labor. The internal option's full twelve hours are already charged as 360 U; increasing availability does not remove that cost. Conversely, having hours available is insufficient if the owner lacks the competence or ongoing capacity assumed here. In that case the internal option still fails a feasibility gate.

Calculate how fragile the revised decision is. Let x be additional internal operations hours/month beyond the original three-minute-per-case allowance. Its value becomes 900−6×30x=900−180x. It ties managed at x=4/3 hours/month, and falls below managed above that point. It remains better than the unchanged incumbent only for x<5 hours/month. The first comparison concerns the best available alternative; the second merely asks whether a positive benefit remains. These are different thresholds.

If instead external access is withdrawn while the setup cap stays four hours, both hosted options fail permission and internal fails capacity. Keep the incumbent process and negotiate a new feasible plan. A weighted score must not allow cheap service to compensate for missing authority. Deferring is a valid decision, not a failure to select a product.

## 7. A bounded evidence plan and handoff

Before a real commitment, obtain the sponsor's actual resource allocation, data owner's authorized processing scope and operator's responsibility acceptance. Prepare a permitted representative case set, including missing records, changed revisions and exceptions. Evaluate each candidate against the same completion and evidence rubric. Track total customer time by role and supplier time by activity, without counting the same minute twice. Record startup, mapping, recovery and recurring support separately.

Use a small staged pilot as a learning investment, not a market-size estimate. First test non-effecting drafts and permission boundaries. Then, only after the relevant owner authorizes use, evaluate operational cycles with the incumbent fallback available. Record eligible, attempted, timely-supported, unresolved and incorrect cases; classify gaps and preserve disputes. Predefine what constitutes a supported result and when a missed cutoff triggers manual handling. No success-rate number is invented here.

Stop on an unauthorized disclosure/effect or inability to preserve source identity. Revisit the offer if actual supplier overhead exceeds its buffer, internal effort crosses the alternative-value threshold, or setup cannot finish within the allocated time. A paid trial alone does not establish retention. A contract alone does not implement mediation. A successful restore drill does not prove every failure mode recoverable.

At exit, transfer mappings, evidence references, unresolved cases and runbooks in an agreed format. Revoke access and address retained copies under the agreed lifecycle policy. Count migration effort in the next decision; do not claim a moat from trapped data. C06 will examine supplier changes more fully. Here the scope is allocating responsibility for a viable job.

## Assignment for later self-assessment

1. Build the responsibility and authority map. Trace a revoked supplier reader and explain why an old successful login is insufficient.
2. Recalculate the three customer values and apply the initial setup constraint. Explain why internal's highest value does not win initially.
3. Rebuild both supplier remainders with the new overhead allowance. Derive the managed overhead ceiling and assess a 2 U/month increase.
4. Change setup capacity to twelve hours and revise the choice. Derive the internal-maintenance thresholds against managed and the incumbent.
5. Specify a pilot, stop conditions and exit handoff. Evaluate the no-external-permission/four-hour-cap case without fabricating a feasible winner.

## Evidence and limitations

| Basis | Verified locator, accessed 2026-11-14 | Scope |
| --- | --- | --- |
| R19 YC / Eric Migicovsky, 2019 | [Transcript](https://www.ycombinator.com/blog/startup-school-week-1-recap-kevin-hale-and-eric-migicovsky/), 30:31–33:44 | Cost, frequency, budget and authority discovery guidance; not demand evidence |
| R21 Patrick McKenzie / Stripe | [Pricing low-touch SaaS](https://stripe.com/guides/atlas/saas-pricing), Introduction; Pricing and packaging for things with no physical form | Practitioner packaging concepts; historical prices not adopted |
| R11 Saltzer and Schroeder, 1975 | [Basic Principles](https://web.mit.edu/saltzer/www/publications/protection/Basic.html), §I.A.3(b), (c), (f) | Fail-safe defaults, complete mediation, least privilege; not a modern implementation certification |
| Original synthesis | B03 numerical fixture plus explicit setup gate, overhead allocation and constraint changes | Checked conditional arithmetic and decision logic, not customer observations or legal/accounting advice |

Unresolved inputs: actual authority, staffing, quality, demand, costs, maintenance and repeat behavior. No essential blocker remains. No learner answers or mastery are inferred.

**Reference card:** hold the job fixed → assign responsibility → apply permission/quality/resource gates → compare customer value → check delivery economics → change one constraint → revise or defer → preserve an exit path.

## Revision history

- 1.0 — 2026-11-14. Constraint-first product-boundary memo, supplier overhead check and five analysis tasks.

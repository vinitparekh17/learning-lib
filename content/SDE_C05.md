# C05 — How far should autonomy go?

| Field | Value |
| --- | --- |
| ID | C05 |
| Title | How far should autonomy go? |
| Revision | 1.0 |
| Date | 2026-11-14 |
| Prerequisites | F02/F03; S03/S06; A05 |
| Capability developed | Choose an adequate control structure using authority, capacity, expected loss and falsifiable evidence |
| Source-check status | R18, R11 and R03 primary passages inspected; locators below |
| Experiment status | Executed synthetic arithmetic, sensitivity and controller checks in companion; no deployed agent or learner assessment |

## Decision and scope

Choose a fixed workflow for the initial operating envelope. When reviewer capacity falls below its requirement, conditionally choose a bounded action-taking agent. The condition is evidence that the agent meets the complete task contract and that its authority boundary actually holds. If that evidence is absent, reduce intake or defer work; a staffing shortage does not create permission.

A05 prepared invoice evidence without approving payment. This memo extends that fictional service by one explicitly permitted action: place the evidence packet into an internal review queue. It does not authorize payment, email, vendor contact or document deletion. This small extension lets us compare action-taking with suggestion-only assistance while preserving the earlier payment boundary. No real action is performed here.

The job is to route each eligible invoice to the correct tenant-local queue, with current revision and supporting passages, within one business day of arrival. Missing evidence produces an unresolved record and counts against timely completion; it must never become invented support. A wrong queue may be reversible but still costs attention, delay and correction. All numerical inputs below are invented planning assumptions, not measurements or vendor claims.

F02 supplies the bridge: expected loss is a probability-weighted average of consequences. F03 adds the denominator: count every eligible offered case, including abstentions, failures and retries. S03 supplies a single decision boundary for competing writes; S06 distinguishes permission from a persuasive proposal. A05 supplies the bounded observation/action loop.

## Three complete systems

Freeze the source snapshot rules, eligible population, business-day clock, tenant scope, allowed destination list and success rubric. There are 1,000 eligible cases per day. Labor costs 0.50 cost units per minute; units are hypothetical common accounting units, not currency quotes. Each option can use the same authorized evidence. Retrieval strategy may differ because it is part of the system being compared.

| Option | Choice of next step | Who commits routing? | Complete-system limitation |
| --- | --- | --- | --- |
| W: fixed workflow | Code follows version lookup, extraction, rule routing and exception branches | Scoped workflow authority; human resolves exceptions | Novel evidence layouts may remain unresolved |
| S: suggestion-only assistant | Fixed retrieval plus one model suggestion | Authorized human checks evidence and submits | Human time and queue delay count, not just generation latency |
| A: bounded action-taking agent | Model proposes subsequent reads and routing from observations | External authority validates a proposed route | More operations, recovery states and ongoing evaluation |

A fixed workflow can mutate state without being model-directed. A suggestion assistant can influence a harmful human decision without owning a write credential. Autonomy, permission and consequence are separate axes. The organizational envelope is identical across all three; identities receive only the subset needed for their role. S's model has no mutation credential. Its human is not allowed to bypass the same business validation.

R18 demonstrates an interaction pattern with search, lookup and finish in Wikipedia knowledge tasks, not an invoice-routing guarantee. The relevant transfer is that later actions can depend on earlier observations. Whether that flexibility improves this service is an empirical question. R11 motivates permission-based defaults, mediation of every access and least privilege. Our controller and capacity model are original applications, not claims proved by those sources.

## Shared ledger and adequacy gates

Partition outcomes into three mutually exclusive categories: wrong route, late/unresolved without a wrong route, and correct on time. Wrong-route loss is 20 units and includes its correction/delay costs even when discovered late. Late/unresolved loss is 5 units. This hierarchy prevents charging the same delay twice. Separate labor numbers include routine review and oversight; the loss amounts exclude that already-counted labor. Unauthorized effects are a disqualifying boundary failure, not an inexpensive fourth category.

| Input per eligible case | W | S | A |
| --- | ---: | ---: | ---: |
| Compute/tool cost | 0.20 | 0.35 | 0.80 |
| Human minutes | 1.0 | 4.0 | 0.4 |
| Allocated maintenance cost | 0 | 0 | 0.30 |
| Wrong-route probability | 0.020 | 0.010 | 0.015 |
| Late/unresolved probability | 0.080 | 0.020 | 0.030 |
| Correct-on-time probability | 0.900 | 0.970 | 0.955 |

Maintenance is incremental to a shared baseline already funded for all options. Zero does not mean W or S need no maintenance. Initial build effort is assumed sunk and equal for this decision horizon; if not, allocate it consistently before choosing. A's 0.30 allowance is for additional loop evaluation and operations. It is an assumption to validate, not a measured engineering advantage for W.

For option j, define cost per eligible case:

`C(j) = compute(j) + 0.50 × human_minutes(j) + maintenance(j) + 20 × p_wrong(j) + 5 × p_late(j)`.

This gives W = 1.50, S = 2.65 and A = 1.75 units. Daily human demand is respectively 1,000, 4,000 and 400 minutes. Total daily expected costs are 1,500, 2,650 and 1,750 units. Expectation does not require independent cases; uncertainty estimates and daily-tail predictions need additional dependence assumptions.

The initial capacity is **1,200 reviewer minutes daily**. Require correct-on-time probability at least 0.90 and a verified authority boundary before comparing cost. Assume, only for the numerical decision, that the boundary has been verified for every candidate. W and A pass capacity; S does not. W is the least complex adequate choice and the lower expected-cost choice. We do not select S because its apparent quality excludes the operational impossibility of completing that much human work with this staffing.

These are average-work planning gates, not proofs of deadline attainment. The supplied timely rates assume actual arrival patterns, reviewer scheduling and tool limits permit them. A burst could break that premise even if daily totals fit. Deployment must validate the queue, not simply divide total minutes by staff count.

## Change exactly one constraint

Reduce available reviewer capacity to **500 minutes per day**. Hold task, volume, costs, outcome assumptions and permission envelope fixed. W now needs twice the available minutes; S needs eight times as much. A needs 400 and remains adequate under the stated model. Revise the recommendation to A, conditionally on validating those assumptions at the reduced staffing level. Its additional expected cost of 250 units daily buys feasibility, not proven superiority in general.

Do not invent lower W error rates or remove human time to preserve the original answer. Nor may A acquire payment credentials to “finish the job.” If the premise that A's oversight fits 400 minutes fails, none of these candidates is adequate at full intake. Add staffing, reduce admitted volume under a revised service contract, or develop and test a different workflow. Those are new decisions rather than hidden changes to this comparison.

Capacity also explains when suggestion-only wins a different decision: if policy prohibits machine-initiated routing but permits reviewed human routing, W and A as defined fail the authority gate. S can be considered only with sufficient staffing. This is a counterexample to choosing autonomy from aggregate quality alone, not the one-constraint revision used above.

## Failure and retry boundaries

The proposed A controller allows at most three evidence calls, three model calls and one routing operation identity per case attempt, inside a ten-second automated-stage deadline. The business-day clock includes waiting for human exceptions. Retries consume the original budgets. Invalid tenant/action proposals terminate the attempt; resource exhaustion yields unresolved. Runtime cancellation is needed for the stage deadline; checking the time only before dispatch is insufficient.

A route commit requires authenticated principal, current grant, matching tenant, allowed action and queue, current epoch/revision, valid evidence and an empty routing slot. Validation and insertion of route plus receipt occur atomically in the same serialized authority. Reads are separately permission checked. Tool observations cannot change the principal or grant. The external checker verifies structural/evidence constraints; it does not magically establish semantic correctness, which remains in the outcome ledger.

| Ordered event | Required behavior |
| --- | --- |
| Agent submits operation K for revision 3 | Check current permission and state; commit route and receipt together |
| Reply is lost | Mark outcome unknown; do not generate a replacement operation |
| Same K, identical payload, current receipt-read permission | Return historical receipt; create no new route |
| Same K, changed destination | Reject operation-identity conflict |
| Another operation targets occupied slot | Reject competing route |
| Grant revoked before a fresh commit | Deny even if proposal was prepared earlier |
| Revision changes before a fresh commit | Reject stale proposal; new evidence/review required |

Revocation after an already committed route does not erase it. Historical receipt retrieval remains subject to current permission. Correction is a separately authorized transition, never blind replay under a new key. This local transaction contract does not promise exactly-once effects across an external payment provider; such effects are outside scope. S03's concurrency lesson matters even for W: two deterministic workers can still race.

## Evidence that changes the decision

At initial staffing, let A's wrong-route probability be x with all its other inputs fixed. Then C(A)=1.45+20x. It matches W at x=0.0025, or 0.25%; the assumed 1.5% is higher. At equality retain W for simplicity. This is a threshold conditional on all other inputs and gates, not a target a model's self-reported confidence can certify. At reduced staffing W remains infeasible even if cheaper.

Start with paired offline replay on identical eligible cases and frozen evidence. Score blinded outputs using the shared rubric, report discordant wins/losses and retain all failures. Include ordinary layouts, missing evidence, changed revisions, malicious source instructions and receipt-loss traces. Pairing reduces case-mix confounding; it does not reproduce a live human queue. Repeated retries of one invoice are not independent samples.

Then evaluate the complete human/tool workflow under realistic arrivals. Predeclare capacity, correct-on-time, wrong-route, cost and authority guardrails, including stop conditions. Randomize at a stable team or tenant boundary if shared reviewer queues would contaminate invoice-level assignment. R03's hypothesis, metrics and randomization guidance supports this design; no trial has been conducted. Measure review minutes including corrections, oversight and failures. Inspect distributions and common-mode failures, not only means. A single demonstrated unauthorized path blocks rollout even if average cost improves.

## Self-assessment and reference card

Use these as optional written exercises; no learner response is needed for scheduled production. Hints and worked analysis are in [SDE_C05_answers.md](SDE_C05_answers.md).

1. Rebuild the three cost and human-capacity ledgers; choose at both staffing levels.
2. Derive A's wrong-route break-even rate and explain why it cannot rescue W under reduced capacity.
3. Trace lost response, replay, changed-payload replay, stale revision and revocation. Separate historical evidence from new effects.
4. A dashboard reports 99% correctness among emitted suggestions. Identify the missing denominator and design a fair comparison.
5. Set A's authority verification to false or its review demand to 600 minutes at reduced staffing. State the decision without silently changing the task.

Reference card: freeze the complete job → gate permission and feasibility → count offered cases → compare complete-system loss and cost → change one premise explicitly → reconcile unknown outcomes before retrying → collect evidence that can overturn the choice. C06 next asks how this decision survives a supplier change.

## Evidence and open questions

| Source | Inspected locator | Supported use and limit |
| --- | --- | --- |
| [R18: ReAct, v3](https://arxiv.org/pdf/2210.03629v3) | §§3.1–3.2, printed p.4 | Observation/action interaction in knowledge tasks; no invoice reliability or authorization inference |
| [R11: Saltzer and Schroeder](https://web.mit.edu/saltzer/www/publications/protection/Basic.html) | §I.A.3(b), (c), (f) | Protection design principles; not certification of this proposed controller |
| [R03: Microsoft Research](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/) | Formulate your Hypothesis and Success Metrics; Choose the Appropriate Unit of Randomization | First-party experimental-design guidance; not measured gains for this service |
| Original synthesis | Ledgers, thresholds, trace and companion script | Constructed and executed checks only; no production outcomes |

Actual loss severity, review time, burst behavior, maintenance, calibrated error rates and authority implementation remain unresolved application inputs. There is no essential production-of-material blocker. The checks do not establish learner mastery or authorize deployment.

# S05 — Queues, tail latency, and cloud elasticity

| Field | Value |
| --- | --- |
| ID / revision / date | S05 · 1.0 · 2026-11-07 |
| Prerequisites | F02 probability and denominators, F03 workload comparisons, S01 service cost and batching |
| Capability developed | Trace waiting work and compare overload policies against a deadline and resource budget |
| Source-check status | R08 author-hosted full text accessed; R09 chapters 21–22 and R12 §6.1 inspected. Locators below. |
| Experiment status | Constructed workloads and executed Python scheduling/arithmetic checks. No real service benchmark. |
| Companion | [Hints, worked answers, and checks](SDE_S05_answers.md) |

## The worker is fast; the request is late

The invoice service receives a burst of documents. Processing an ordinary document takes one second in our fictional model, yet a reviewer waits eight seconds for one of them. The missing time is waiting behind other work. Optimizing the one-second operation may help, but choosing a queue size, admission rule or capacity policy requires understanding the entire arrival-to-completion interval.

An arrival is a request entering the measured boundary. Service time is time occupying the worker. Waiting time precedes service. Response time here ends when the complete result is ready. We exclude network transfer, review and storage commit time from this small model. A production end-to-end clock must include those stages when they matter to the promise.

Let arrival, start, service duration and finish for request i be a_i, b_i, s_i and f_i. For one non-preemptive first-in, first-out worker:

\[
b_i=\max(a_i,f_{i-1}),\quad f_i=b_i+s_i,\quad W_i=b_i-a_i,\quad T_i=f_i-a_i.
\]

“Non-preemptive” means a started job runs to completion. The worker is work-conserving: it does not idle while an eligible job waits. The recurrence follows directly from those rules. It is a baseline to test, not a promise that every queue behaves this way.

## Six requests and one common objective

All six requests arrive at time zero. Ties follow IDs J1 through J6. Service durations are `[1,1,4,1,1,1]` seconds. Five are short and J3 is long. The empirical service distribution puts 5/6 of its mass at 1 and 1/6 at 4, with mean 1.5 seconds. No random draw or real measurement produced these values.

Every request has a four-second arrival-to-completion deadline, inclusive. The objective is to maximize complete, correct results delivered on time among **all six offered requests**, while reporting resource use and rejected/late outcomes. All computed results are assumed correct. Each policy must return the same complete output for an admitted request. Rejected and late requests do not count as timely successes.

| Job | Service | Start | Finish / response time | Waiting | Meets deadline? |
| --- | ---: | ---: | ---: | ---: | --- |
| J1 | 1 | 0 | 1 | 0 | Yes |
| J2 | 1 | 1 | 2 | 1 | Yes |
| J3 | 4 | 2 | 6 | 2 | No |
| J4 | 1 | 6 | 7 | 6 | No |
| J5 | 1 | 7 | 8 | 7 | No |
| J6 | 1 | 8 | 9 | 8 | No |

Immediately after J1 starts, five jobs wait. After J2 starts at t=1, four wait. J3 starts at t=2, leaving three short jobs waiting until t=6. The backlog eventually drains at t=9, but eventual completion did not meet the interactive objective. Keeping every job in the queue does not make every acceptance useful.

The six response times average 5.5 seconds. Define the empirical p-th percentile using nearest rank: sort n observations and choose position `ceil(p*n)`, counting from one. Then p50 is 6 seconds and p95 is 9. With six observations p95 selects the maximum. It is a descriptive statistic for this batch, not a reliable estimate of a production tail.

Move the long job to the end while keeping the same service-time distribution. Completions become `[1,2,3,4,5,9]`, with four timely results and mean response time 4. The unchanged mean service time did not determine the waiting-time distribution. Arrival order, scheduling and burst shape are consequential inputs.

## Compare four responses to the same burst

**Queue everything.** The baseline does nine worker-seconds of busy work and completes two requests on time. A queue is useful if later completion retains value and memory is bounded. It does not increase processing capacity. R09's Queue Management section discusses how bursts, service time and queue length affect the choice.

**Reject work predicted to miss the deadline.** In ID order, accept a request only if its predicted finish on the one worker is at most four. Assume exact service costs are known at admission, and reject checks cost zero for this model. J1 and J2 reserve two seconds. J3 would finish at six, so reject it. J4 and J5 then reserve seconds three and four. J6 would finish at five, so reject it. Four of six succeed on time using four worker-seconds. The result is conditional on unusually good cost estimates. Underestimation, expensive rejection or immediate retries can erase the advantage.

**Batch adjacent pairs.** Assume a separate execution mode that produces exactly the same results, with pair service time `0.5 + max(s_i,s_j)`. Both outputs become available together. This is an assigned batching cost, not a measured speedup. All jobs are already present, so there is no assembly delay. The pairs finish at 1.5, 6 and 7.5 seconds. Busy time falls to 7.5 worker-seconds, but only J1 and J2 meet the deadline. J4 waits for its expensive batch partner. This reuses S01's distinction between amortized work and individual latency.

**Add a worker.** With two identical workers ready at zero and a shared FIFO queue, J1 and J2 finish at one. J3 occupies the first worker from one to five; the second finishes J4, J5 and J6 at two, three and four. Five of six meet the deadline. If the second worker becomes ready only at t=2, completions by job ID are `[1,2,6,3,4,5]`. Four of six are timely. A scaling decision cannot retroactively process work during startup.

| Policy | On-time / offered | Rejected | Eventually completed late | Busy worker-seconds | Last admitted completion |
| --- | ---: | ---: | ---: | ---: | ---: |
| One worker, FIFO | 2/6 | 0 | 4 | 9 | 9 |
| Deadline admission, one worker | 4/6 | 2 | 0 | 4 | 4 |
| One worker, paired batches | 2/6 | 0 | 4 | 7.5 | 7.5 |
| Two workers ready at zero | 5/6 | 0 | 1 | 9 | 5 |
| Second worker ready at two | 4/6 | 0 | 2 | 9 | 6 |

Busy time is not billed capacity. Two provisioned workers can incur cost while one is idle. The admission policy's completed-only success fraction is 4/4, but its offered-request fraction is 4/6. Report both only with explicit denominators. It would be misleading to advertise “100% success” while hiding the rejected third of the workload.

The equal-value objective favors short jobs. If J3 is an urgent high-value case, rejecting it may be unacceptable. A class reservation, separate queue or different objective may be appropriate. F02's loss model supplies the missing value judgment; a scheduler does not discover business priorities from service times.

## Rates describe a longer window

A separate fluid model makes sustained overload visible. Treat work as divisible units with arrival rate λ and service capacity μ in the same units per second. While backlog Q is positive, it changes at λ−μ. At zero, unused service is discarded rather than producing negative backlog.

Start empty. For four seconds, work arrives at 3 units/s and capacity is 2 units/s. Backlog grows at 1 unit/s, so Q(4)=4. Afterward arrivals drop to 1 unit/s. The spare 1 unit/s drains those four units over four more seconds. The backlog reaches zero at t=8. If the burst rate persists, it never drains under this capacity.

| Time t (seconds) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Outstanding work Q(t) | 0 | 1 | 2 | 3 | 4 | 3 | 2 | 1 | 0 |

This model counts outstanding work, not discrete request positions. It cannot supply a per-request percentile. If one request needs four times the work of another, counting requests alone obscures the load. R09 chapter 21's discussion of queries per second motivates measuring the constraining resource directly.

For m independent identical workers and mean service demand E[S], the nominal busy-load ratio is `ρ = λ E[S]/m`, with λ measured in requests/s. It compares offered work to worker time. Under the assumed service model, sustained ρ>1 forces accumulation or rejection. ρ<1 does not guarantee a deadline: our finite burst can fit into a long low-load interval and still produce late requests. Shared locks, storage or external quotas also break the assumption that m workers supply m independent units of service capacity.

## A small component tail becomes a request tail

Suppose a different workflow waits for all 20 parallel evidence lookups. Assume each lookup independently exceeds threshold d with probability 0.02. The whole request exceeds d whenever at least one lookup does. The complement calculation gives

\[
P(\max_i T_i>d)=1-(1-0.02)^{20}\approx 0.3324.
\]

Thus a two-percent component exceedance becomes about 33.24% in this constructed fan-out model. This is an original calculation using F02 probability. R08 discusses the underlying amplification mechanism and head-of-line blocking, but its reported workload measurements are not our inputs.

Independence is a substantive assumption. If all 20 lookups are slow together with probability 0.02 and otherwise all fast, the request exceedance is 0.02. Dependence changes the calculation. Neither example is a prediction for this invoice service. Measure joint behavior, fan-out size and the complete-request clock. Do not average component p99 values to obtain an end-to-end p99.

## Elastic capacity changes the budget, not the past

R12 frames elasticity as a way to trade overprovisioning against saturation risk. Its 2009 provider prices are historical. Here is an independent cost model with invented units.

Over a ten-hour planning window, suppose the required ready capacity is two workers for nine hours and six workers for one known peak hour. Keeping six ready for all ten hours buys 60 worker-hours. Perfectly timed elasticity buys `2*9 + 6*1 = 24`. If elastic worker-hours cost p times the reserved worker-hour price, its capacity charge is lower when `24p < 60`, or p<2.5.

Now the four extra workers each need a quarter-hour of paid startup before the peak. Elastic consumption becomes 25 worker-hours, and the threshold becomes p<2.4. The peak must be anticipated early enough to make them ready. A reactive policy discovering the peak at its start leaves a capacity gap. Billing granularity, minimum commitments, data loading, quotas and operating labor are omitted; adding them can reverse the decision. This calculation compares capacity charges only, not profitability.

A plausible policy for uncertain interactive traffic is a measured warm baseline, bounded queues and admission, with scaling for sustained changes. That is a hypothesis to test. Frequent sharp bursts may justify more warm headroom. Long deadlines may justify buffering and slower provisioning. Batch-compatible work may justify a different execution mode. The six-job result is too small to select a production configuration.

## Measure the policy without hiding failures

Replay the same timestamped arrivals and payloads under each policy. Drive arrivals independently of response completion so a slow system does not silently receive less load. Record offered, admitted, completed, correct, late and rejected counts, plus retry attempts per original operation. Keep a clock starting at the original arrival for the user outcome. Count work expended on failed attempts.

Report service and waiting distributions separately, with the percentile definition, sample count and observation window. Segment by request cost and customer class. Preserve unanswered requests as failures or censored observations according to a declared rule; never drop them silently. Include startup and drain periods. F03's paired-workload discipline applies, while shared-resource interference may require separate controlled runs.

R09 chapter 22 describes retry amplification and recommends retry limits and budgets. A failed request can add work precisely when the server is already overloaded. Test retries, cancellation and deadline propagation as part of the workload. No overload policy should bypass the evidence or approval checks established in earlier packs to make its latency chart look better.

## Practice

1. Reproduce the FIFO start/finish/wait table, mean response time, nearest-rank p50 and p95. Explain why the mean service time is insufficient.
2. Execute deadline admission in ID order. Report both offered-request and completed-request success fractions. Give one cost-estimation failure.
3. Derive the paired-batch and both two-worker traces. Explain why lower busy time can coexist with no improvement in on-time success.
4. Derive Q(4) and the drain time in the fluid model. What happens if post-burst arrivals equal capacity instead of falling below it?
5. Calculate the 20-way independent fan-out exceedance, then compare the perfectly correlated construction. Specify the percentile population you would measure.
6. Reproduce the capacity-price thresholds with and without paid startup. Propose a replay that could reverse a warm-baseline/scaling recommendation, including rejection and retry outcomes.

## Evidence, reference card and remaining questions

| Basis | Inspected locator | Use and boundary |
| --- | --- | --- |
| R08, Dean and Barroso, CACM 56(2), 2013 | [Author PDF](https://barroso.org/publications/TheTailAtScale.pdf), printed p. 76, Component-Level Variability Amplified By Scale and Reducing Component Variability | Fan-out and head-of-line mechanisms. No published benchmark transferred. Direct author download resolved a web-reader timeout and the earlier access gap. |
| R09, Google SRE, 2016 | [Chapter 21](https://sre.google/sre-book/handling-overload/), The Pitfalls of “Queries per Second” and Client-Side Throttling | Resource-based capacity and nonzero rejection cost. Practice guidance. |
| R09, same book | [Chapter 22](https://sre.google/sre-book/addressing-cascading-failures/), Queue Management, Load Shedding and Graceful Degradation, Retries | Queue trade-offs, useful work and retry feedback. No numerical queue-size prescription adopted. |
| R12, Armbrust et al., 2009 | [University PDF](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2009/EECS-2009-28.pdf), §6.1 printed pp. 10–11 | Historical elasticity and provisioning-risk argument. No current prices asserted. |
| Original derivations and executed checks | Tables and companion Python | Six-job, fluid, probability and capacity-charge models; all inputs hypothetical. |

Reference card: define the boundary and denominator → trace arrival, wait and service → compare on-time useful outcomes → count work and purchased capacity separately → test bursts, startup and retries. A percentile needs a population and convention. A scaling request is not ready capacity.

Actual arrivals, cost estimates, service distributions, correlation, startup delays, failure costs and fairness constraints remain unknown. No empirical service improvement is claimed. A04 will reuse the batching and queue distinctions for inference; B02 and B03 will connect capacity choices to delivery economics. Next C01 uses the earlier systems packs to locate duplicate-effect prevention.

## Revision history

- 1.0 — 2026-11-07. Original burst comparison, fluid backlog, fan-out derivation and elasticity budget; primary access gap repaired.

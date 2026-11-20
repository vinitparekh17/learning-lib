# S05 — Hints, worked answers, and reproducible checks

| Field | Value |
| --- | --- |
| ID / title | S05 answers · Queues, tail latency, and cloud elasticity |
| Revision / date | 1.0 · 2026-11-07 |
| Prerequisites | F02, F03, S01; [S05 core pack](SDE_S05.md) |
| Capability developed | Defend a capacity policy with an explicit workload, deadline, denominator and cost boundary |
| Source-check status | R08, R09 and R12 passages inspected; exact URLs and locators in the core evidence table and source register |
| Experiment status | Python checks below executed successfully on constructed inputs; no deployment benchmark |

These are model solutions, not a record of your answers or mastery. Try the six core exercises before opening the corresponding solutions. Alternative policies are valid when their assumptions, objective and accounting are explicit.

## Hints

1. A FIFO request waits until both its arrival and the preceding completion. Service duration is only part of response time. Apply the stated nearest-rank convention, not interpolation.
2. A rejected job consumes no reserved processing time in this model. Keep rejected requests in the offered population.
3. A pair releases two outputs together. With multiple workers, assign the next queued job to the earliest available worker, breaking availability ties by worker index.
4. Track work units, not request counts. Spare capacity is what drains backlog; full utilization alone does not drain it.
5. Compute the probability that none of the lookups is slow, then take its complement. State where independence enters.
6. Sum paid worker-hours, including startup. A useful replay must preserve the original arrivals when the service slows down.

## 1. FIFO, distributions and the missing waiting time

For costs `[1,1,4,1,1,1]`, all arriving at zero, starts and waiting times are `[0,1,2,6,7,8]`. Finishes and response times are `[1,2,6,7,8,9]`. The total service demand is nine worker-seconds, so mean service time is 9/6 = 1.5 seconds. Mean response time is 33/6 = 5.5 seconds; mean waiting time is 24/6 = 4 seconds. The identity mean response = mean waiting + mean service holds for this population.

Nearest-rank p50 takes observation `ceil(0.5*6)=3`, giving six seconds. p95 takes observation `ceil(0.95*6)=6`, giving nine. These are response percentiles across six offered, completed jobs from this constructed burst. A six-job p95 is its maximum and says little about the tail of a different workload.

Moving the four-second job to the end yields finishes `[1,2,3,4,5,9]`. Mean response falls to four seconds and timely completions increase from two to four without changing mean service demand. The test code checks all six positions of the long job: mean response ranges from 6.5 to 4 seconds, and timely counts range from one to four. An average service cost leaves ordering and arrival clustering unspecified.

**Assessment criterion:** Correct recurrence and population; distinction between service and response; an ordering or burst counterexample. An unexplained claim that “p95 is always the maximum” fails: it is true here because the population has six observations.

## 2. Admission and the denominator

| Job | Predicted finish if accepted | Decision | Reserved finish after decision |
| --- | ---: | --- | ---: |
| J1 | 1 | Accept | 1 |
| J2 | 2 | Accept | 2 |
| J3 | 6 | Reject | 2 |
| J4 | 3 | Accept | 3 |
| J5 | 4 | Accept | 4 |
| J6 | 5 | Reject | 4 |

Accepted IDs are J1, J2, J4 and J5. They finish at seconds 1, 2, 3 and 4. The offered-request timely fraction is 4/6; the completed-request timely fraction is 4/4. Neither fraction alone describes every outcome. Report two rejections, zero late completions and four worker-seconds of busy work.

For a concrete estimation failure, predict every job costs one second. The rule admits J1 through J4 and rejects J5 and J6. Actual processing still takes costs `[1,1,4,1]`, finishing at `[1,2,6,7]`. Only two of six offered jobs finish on time. Admission is a policy using information; an optimistic estimate is not a guarantee. Rejection checks, retries and request-value differences are additional costs deliberately excluded from the baseline model. R09 chapter 21 explains why real rejection can itself consume meaningful resources.

**Assessment criterion:** Track reservations after a rejection; retain the offered denominator; show a concrete failure of a stated assumption. Do not claim that all overload should be rejected or that the long job lacks value.

## 3. Batching, capacity and startup

Adjacent pair durations are 1.5, 4.5 and 1.5 seconds. Their cumulative finishes are 1.5, 6 and 7.5. Since both outputs are released at each pair completion, per-job finishes are `[1.5,1.5,6,6,7.5,7.5]`. Pair mode does 7.5 worker-seconds of busy work, saving 1.5 relative to FIFO, yet still has only two timely completions. The short J4 inherits the long J3's batch completion. No assembly delay occurs because every request was already waiting; a staggered arrival workload would need a batch timeout rule.

With two workers ready at zero, worker 0 handles J1 from 0–1 and J3 from 1–5. Worker 1 handles J2 from 0–1, J4 from 1–2, J5 from 2–3 and J6 from 3–4. In job order, finishes are `[1,1,5,2,3,4]`. Five are timely; busy work remains nine worker-seconds.

With worker 1 ready only at second two, worker 0 executes J1 from 0–1, J2 from 1–2 and J3 from 2–6. The worker-index tie rule assigns J3 to worker 0. Worker 1 executes J4 from 2–3, J5 from 3–4 and J6 from 4–5. Finishes are `[1,2,6,3,4,5]`; four are timely. The final completion is at six, even though J6 finishes at five: always take the maximum completion, not the final array element.

**Assessment criterion:** Correct pair release semantics and worker assignment; count outcomes against the same deadline; distinguish busy worker-seconds from provisioned and billed capacity. A faster drain is useful but does not establish a better user outcome for every request.

## 4. Backlog and spare capacity

During the four-second burst, net input is `3−2=1` work unit per second. Thus Q(4)=4. Afterward spare capacity is `2−1=1` unit per second, and the backlog drains in four additional seconds, at t=8.

| Time t (seconds) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Outstanding work Q(t) | 0 | 1 | 2 | 3 | 4 | 3 | 2 | 1 | 0 |

If arrivals fall only to two units/s, input equals capacity and the accumulated four units remain. If arrivals stay above two, backlog grows. If the system is empty and arrivals are below capacity, unused capacity disappears rather than making Q negative. This is a deterministic fluid model; it is not a stochastic queue or a per-request latency simulator.

**Assessment criterion:** Correct units and time origin; explain that recovery needs spare capacity. A long-window mean arrival rate below capacity can coexist with short-window deadline misses.

## 5. Fan-out and correlation

Under the independent model, each lookup is fast enough with probability 0.98. All 20 are fast enough with probability `0.98^20`. The complete request exceeds d with probability `1−0.98^20 = 0.332392…`, or about 33.24%.

For the perfectly correlated construction, all lookups exceed d in the same two percent of requests. The whole request therefore exceeds d with probability 0.02. Every component retains the same marginal exceedance as before, but the joint distribution changes. Correlation cannot be ignored; these two constructions alone do not specify every possible dependence pattern.

Measure latency for complete original user operations over a specified window and workload, starting at original arrival and ending at the promised complete result. Separately record rejected, failed, timed-out and retried operations. If calculating a percentile only for completed operations, label that conditional population and also report the offered-operation success rate. Do not silently treat timeout duration as a successful completion, omit incomplete operations, or average component percentiles. Component-level distributions remain useful diagnostics, not substitutes for the user clock.

**Assessment criterion:** Show the complement and independence assumption, supply the correlated counterexample, and define the measured population. The 33.24% is a calculated teaching case, not R08's reported benchmark.

## 6. Capacity charges and evidence that changes the policy

Fixed provisioning buys `6*10=60` worker-hours. Ideal elasticity buys `2*9+6*1=24`. If elastic unit price is p times the fixed unit price, break-even is `24p=60`, so p=2.5. Elasticity is cheaper below that threshold, equal at it, and more expensive above it under these assumptions.

Four extra workers each incur 0.25 paid startup hours. That adds one worker-hour, giving 25 and break-even `60/25=2.4`. This assumes baseline capacity is ready initially and the peak is anticipated; the extra startup is inside the accounting boundary. It excludes minimum billing units, commitments, network costs, operational labor and the value lost when deadlines are missed. It is not a current cloud quote or a profit calculation.

A bounded replay could compare a warm baseline plus scaling against a larger always-ready pool. Predeclare the useful-outcome deadline, correctness requirement and offered-operation denominator. Replay identical timestamped arrivals and payload costs, including several bursts shorter than measured startup time, a sustained peak and a post-peak drain. Record ready capacity over time, startup work, queue depth in both requests and estimated work units, paid capacity, original-operation latency, rejections, late completions, failed attempts and retries. Keep retry budgets and cancellation behavior explicit; do not let a response-driven load generator reduce offered load when latency rises.

If short frequent bursts cause unacceptable misses before additional workers become ready, and the value of avoiding those misses exceeds the headroom charge, increase warm capacity. If long deadlines and sparse peaks permit buffering without loss of useful outcomes, favor a smaller baseline. If rejection and retries amplify overload, change admission and retry behavior before interpreting a scaling comparison. Different value by request class may call for reservations or a revised objective. These are decision rules, not measured findings. Real observations must supply the costs and acceptance limits.

**Assessment criterion:** Correct capacity arithmetic and a test capable of falsifying the recommendation. The replay must account for failures, startup and work spent on retries; aggregate successful-request latency alone is insufficient.

## Executed checks and limits

Run the following with Python 3; it needs only the standard library. It checks the worked traces using exact rational arithmetic, compares FIFO with independently accumulated service costs, varies all six placements of the long job, checks admission under cost underestimation, validates the two capacity traces and busy-work conservation across five startup values, and verifies fluid conservation, probability and cost thresholds.

These finite deterministic checks establish consistency of the examples. They do not establish queue stability under a random process, estimate a production tail, validate an implementation's scheduler, measure rejection overhead or prove a policy optimal. No simulated result is treated as learner evidence.

```python
from fractions import Fraction as F
from itertools import accumulate
from math import ceil
import heapq

costs = [1, 1, 4, 1, 1, 1]
deadline = 4

def schedule(work, ready):
    workers = [(F(t), i) for i, t in enumerate(ready)]
    heapq.heapify(workers)
    starts, finishes = [], []
    for cost in work:  # all arrivals zero; ID order; worker-index tie break
        start, worker = heapq.heappop(workers)
        finish = start + cost
        starts.append(start)
        finishes.append(finish)
        heapq.heappush(workers, (finish, worker))
    return starts, finishes

def timely(finishes):
    return sum(t <= deadline for t in finishes)

starts, fifo = schedule(costs, [0])
assert fifo == list(accumulate(costs)) == [1, 2, 6, 7, 8, 9]
assert starts == [0, 1, 2, 6, 7, 8]
assert sum(fifo) / 6 == F(11, 2)
assert sum(costs) == 9
assert sorted(fifo)[ceil(F(1, 2) * 6) - 1] == 6
assert sorted(fifo)[ceil(F(95, 100) * 6) - 1] == 9
assert timely(fifo) == 2
# Six distinct positions of the long job: same service distribution.
means, successes = [], []
for position in range(6):
    work = [1] * 6
    work[position] = 4
    _, finish = schedule(work, [0])
    assert finish == list(accumulate(work))
    means.append(sum(finish) / 6)
    successes.append(timely(finish))
assert means == [F(13, 2), 6, F(11, 2), 5, F(9, 2), 4]
assert successes == [1, 1, 2, 3, 4, 4]

reserved = 0
accepted, rejected = [], []
for job, cost in enumerate(costs, 1):
    if reserved + cost <= deadline:
        reserved += cost
        accepted.append(job)
    else:
        rejected.append(job)
assert accepted == [1, 2, 4, 5] and rejected == [3, 6]
assert schedule([costs[j-1] for j in accepted], [0])[1] == [1, 2, 3, 4]
# If predicted costs are all one, the first four are admitted.
assert schedule(costs[:4], [0])[1] == [1, 2, 6, 7]
assert timely(schedule(costs[:4], [0])[1]) == 2

pair_costs = [F(1, 2) + max(costs[i:i+2]) for i in range(0, 6, 2)]
pair_finishes = list(accumulate(pair_costs))
batch = [t for t in pair_finishes for _ in range(2)]
assert batch == [F(3, 2), F(3, 2), 6, 6, F(15, 2), F(15, 2)]
assert sum(pair_costs) == F(15, 2) and timely(batch) == 2
assert schedule(costs, [0, 0])[1] == [1, 1, 5, 2, 3, 4]
assert schedule(costs, [0, 2])[1] == [1, 2, 6, 3, 4, 5]
assert timely(schedule(costs, [0, 0])[1]) == 5
assert timely(schedule(costs, [0, 2])[1]) == 4
for readiness in range(5):
    begin, end = schedule(costs, [0, readiness])
    assert sum(e-b for b, e in zip(begin, end)) == 9

q, trace = 0, [0]
for second in range(8):
    arrivals = 3 if second < 4 else 1
    served = min(q + arrivals, 2)
    next_q = q + arrivals - served
    assert next_q >= 0 and next_q + served == q + arrivals
    q = next_q
    trace.append(q)
assert trace == [0, 1, 2, 3, 4, 3, 2, 1, 0]
assert max(0, 4 + 2 - 2) == 4  # equal rates do not drain backlog
fanout = 1 - F(98, 100)**20
assert round(float(fanout), 4) == 0.3324
assert fanout > F(2, 100)
fixed, elastic = 6 * 10, 2 * 9 + 6
startup = 4 * F(1, 4)
assert (fixed, elastic, elastic + startup) == (60, 24, 25)
assert F(fixed, elastic) == F(5, 2)
assert fixed / (elastic + startup) == F(12, 5)
print('PASS: FIFO, six reorderings, admission and estimation failure, batches,')
print('two-worker traces, five startup cases, fluid conservation, fan-out, costs.')
print('Fluid backlog at integer seconds:', trace)
print('Independent fan-out exceedance:', round(float(fanout), 6))
```

Observed output on 2026-11-07:

```text
PASS: FIFO, six reorderings, admission and estimation failure, batches,
two-worker traces, five startup cases, fluid conservation, fan-out, costs.
Fluid backlog at integer seconds: [0, 1, 2, 3, 4, 3, 2, 1, 0]
Independent fan-out exceedance: 0.332392
```

## Revision history

- 1.0 — 2026-11-07. Six worked solutions, hints, assessment criteria and executed checks. All inputs are constructed; actual arrivals, service costs, correlations, resource constraints and pricing remain application questions.

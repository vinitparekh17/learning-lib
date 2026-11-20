# C03 — Worked analysis and reproducible checks

| Field | Value |
| --- | --- |
| ID / title | C03 answers · Capacity decision analysis |
| Revision / date | 1.0 · 2026-11-13 |
| Prerequisites | [C03 memo](SDE_C03.md), S01/S05, A04, B02 |
| Capability developed | Audit the constraints and denominators behind an optimization recommendation |
| Source-check status | Uses the memo's R16/R09 passages; numerical work is original |
| Experiment status | Exact scheduling, memory, threshold and cost checks executed; no model or hardware trial |
| Assessment | Criteria concern a future answer, not inferred learner mastery |

## 1. Memory feasibility

**Hint:** Count weights once per replica and cached positions once per active request.

**Worked analysis:** Each peak request costs 4,096×128 KiB=512 MiB. Four require 2 GiB. Weights plus other reserve plus request state total 12+4+2=18 GiB, leaving 6 GiB beyond the counted reservation on that device. The original KV pool is 8 GiB; the four requests consume only a quarter of it. Two replicas each need their own 18 GiB budget, not 18 GiB shared between them.

This is a conservative cap including output growth, not merely a snapshot of prompt memory. It holds only if the other-memory reserve is sufficient. A memory-only change that preserves the feasible schedule and service law cannot alter completion times. It becomes consequential if allocation previously prevented a useful batch, but that new schedule must still meet the deadline. Physical memory fit does not establish bandwidth, compute or latency capacity.

**Criteria:** Correct byte conversions, per-device accounting and a conditional reason that reducing memory can leave useful capacity unchanged.

## 2. Starting trace and speedup

**Hint:** Compute one complete batch, then add queue delay for the second wave.

**Worked analysis:** At b=4,d=4, B is 16+4×8=48 ms and P is 8+4×8=40 ms. One replica finishes its waves at s and 2s: B at 48 and 96, P at 40 and 80. Two B replicas finish all tasks at 48. With four requests per wave, mean response is (s+2s)/2=1.5s for B/P; R's mean is 48. Means are therefore 72, 60 and 48 ms. Counts within 90 ms are 4,8,8.

Prefill is 16/48=1/3 of B's service. Halving it gives 48/40=6/5 speedup. Removing it entirely leaves 32 ms, limiting this particular phase-only speedup to 48/32=3/2. A 2× component improvement is not a 2× whole-batch improvement. Nor is amortized batch time s/4 the response time of an individual task.

**Criteria:** Correctly distinguishes latency, work and wave scheduling. Does not import a benchmark result into the invented timing law.

## 3. Cost and choice

**Hint:** Apply the same purchased window even if a policy stops being busy sooner.

**Worked analysis:** Eight attempted tasks incur 40 U of verification/accounting cost in every policy. B/P each buy 200 replica-ms, so each costs 240 U. R buys 400 replica-ms, so costs 440 U. Dividing by useful counts yields 60,30,55 U. B's lower total bill than R does not make B acceptable under the all-eight objective. P and R both pass; P is cheaper.

Busy replica-time is 96,80,96 ms. R parallelizes the same baseline work; it does not halve total work. A busy-only bill would instead be 136,120,136 U including the common 40, which describes a different pricing assumption. Do not silently switch between the two.

If P has additional implementation expense K relative to R, after m identical qualifying windows its saving net of that expense is 200m−K. For positive K, continuous recovery is K/200 windows; whole-window recovery is its ceiling. This calculation omits maintenance and any later workload change. With K=1,000 U, five such windows recover it exactly. This is an illustrative expense, not a quote. If the long-output workload arrives before recovery, the saving premise fails.

**Criteria:** Reports unsuccessful-work costs, idle capacity and excluded costs; keeps quality/coverage as a gate rather than optimizing a ratio at any cost.

## 4. Changed workload and startup

**Hint:** Replace d, not the task count, objective or quality bar.

**Worked analysis:** At d=8, B/R batch time is 16+8×8=80 ms; P is 8+8×8=72. B waves end at 80/160 and P at 72/144; R completes eight at 80. Means are 120/108/80. Useful counts are 4/4/8 and costs per useful result 60/60/55. R is now the only qualifying policy.

For all eight to finish: B requires 32+16d≤90, so integer d≤3; P requires 16+16d≤90, so d≤4; R requires 16+8d≤90, so d≤9. These conditions include d=0 if prefill alone supplies the whole output. They do not certify real workloads with the same token count. At d=10, R needs 96 ms, and adding identical replicas cannot reduce an individual batch's 96 ms under this policy. Smaller batches or a different kernel are separate options.

With the second replica ready at h, its four assigned tasks finish at h+80. At h=0,10,11, all-eight counts are respectively 8,8,4. Equality at 90 is allowed. This policy deliberately waits for the second replica for that batch; other routing choices require another trace. Startup costs must be added if the warm-capacity billing premise changes.

**Criteria:** Revises the recommendation and explains the precise constraint causing reversal. Correctly handles inclusive deadlines and does not call requested capacity ready capacity.

## 5. A falsification-oriented measurement plan

**Hint:** A fair experiment can produce evidence against the optimization you prefer.

**Worked analysis:** Replay matched permitted cases with identical arrival timestamps and output requirements. Freeze model/configuration, data revisions, validation rules and allowed effects. Record phase durations and complete serving response separately; keep retrieval/network/user time in a separate end-to-end measure. Compare ordinary traffic, bursts, sparse single requests, unequal outputs and larger prompts. Count rejected, late and unsupported tasks among all offered tasks. Include provisioned idle time, startup, memory growth, retry costs and verification work.

For sparse one-task windows at b=1,d=4, B takes 10+20=30 ms and P 5+20=25; both are useful. A permanently purchased second replica adds cost without adding a timely result. A scale-down policy could change this cost comparison, but is not the stipulated R policy. For unequal outputs, record batch composition and longest-member blocking; an average length does not reconstruct per-task waiting. Inspect continuous scheduling separately.

If one P output is unsupported, its eight timely outputs become seven timely-correct results, failing the required gate even if its cost ratio remains attractive. If a model variant omits necessary evidence, lower latency cannot be credited as an equivalent optimization. For production tails, use representative arrivals over repeated windows and an explicit percentile convention and uncertainty analysis. This eight-task deterministic trace is not a sample supporting a production p99 estimate.

**Criteria:** Includes at least one observation that rejects each candidate, matched quality and authority boundaries, explicit units and a fair offered-load denominator. No outreach, model execution or real measurement is implied by this proposed plan.

## Executed checks

The standard-library script below ran successfully during production. It independently constructs wave schedules and checks them against the closed-form thresholds. It also checks zero-success handling and exact boundary cases. The 200 ms billing comparison is used only for the two main workloads, whose traces drain inside it; longer synthetic traces below are timing-only sensitivity checks.

```python
from fractions import Fraction as Q
from math import ceil

GiB, KiB = 2**30, 2**10
kv = 4096*128*KiB
assert kv == GiB//2
assert 12*GiB + 4*GiB + 4*kv == 18*GiB

def service(b,d,fast=False):
    pre = Q(8+2*b,2) if fast else Q(8+2*b)
    return pre+d*(4+b)

def schedule(n,d,replicas=1,fast=False):
    free=[Q(0)]*replicas
    finishes=[]
    busy=Q(0)
    remaining=n
    while remaining:
        b=min(4,remaining)
        device=min(range(replicas),key=lambda j:(free[j],j))
        elapsed=service(b,d,fast)
        free[device]+=elapsed
        finishes.extend([free[device]]*b)
        busy+=elapsed
        remaining-=b
    return sorted(finishes),busy

def good(finishes,deadline=90):
    return sum(t<=deadline for t in finishes)

def cost_per(cost,successes):
    return Q(cost,successes) if successes else None

policies=[(1,False),(1,True),(2,False)]
for d,expected,means,counts in [
    (4,[[48]*4+[96]*4,[40]*4+[80]*4,[48]*8],[72,60,48],[4,8,8]),
    (8,[[80]*4+[160]*4,[72]*4+[144]*4,[80]*8],[120,108,80],[4,4,8])]:
    for i,(k,fast) in enumerate(policies):
        f,busy=schedule(8,d,k,fast)
        assert f==expected[i]
        assert sum(f)/8==means[i] and good(f)==counts[i]
        assert max(f)<=200
        assert busy==2*service(4,d,fast)
        cost=200*k+5*8
        assert cost_per(cost,good(f))==([60,30,55] if d==4 else [60,60,55])[i]
assert Q(48,40)==Q(6,5) and Q(48,32)==Q(3,2)
assert ceil(Q(1000,200))==5
assert cost_per(240,0) is None
assert schedule(1,4)[0]==[30]
assert schedule(1,4,fast=True)[0]==[25]

# 13 decode lengths x 3 policies; compare all-eight success thresholds.
for d in range(13):
    for (k,fast),limit in zip(policies,[3,4,9]):
        f,_=schedule(8,d,k,fast)
        assert (good(f)==8)==(d<=limit)

# 201 inclusive deadlines x 2 workloads x 3 policies: 1,206 checks.
checks=0
for deadline in range(201):
    for d in [4,8]:
        for k,fast in policies:
            f,_=schedule(8,d,k,fast)
            s=service(4,d,fast)
            closed=8*int(s<=deadline) if k==2 else 4*(int(s<=deadline)+int(2*s<=deadline))
            assert good(f,deadline)==closed
            checks+=1
assert checks==1206
for h,count in [(0,8),(10,8),(11,4)]:
    assert good([80]*4+[80+h]*4)==count
print('PASS: memory, two full traces, costs, phase bounds, sparse load, zero success, 39 length-policy and 1206 deadline checks, startup boundaries')
```

## Revision history

- 1.0 — 2026-11-13. Five worked analyses and executed deterministic checks; no empirical performance claims.

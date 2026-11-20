# A04 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| ID / revision / date | A04 answers · 1.0 · 2026-11-10 |
| Title | Inference serving and memory economics — worked answers |
| Prerequisites | S01, S05, A02 and [A04 core](SDE_A04.md) |
| Capability developed | Audit memory units, allocation boundaries and latency-constrained policy comparisons |
| Source-check status | R16/R04/R08 locators in core; numerical cases are original |
| Experiment status | Python integer/rational checks executed; no model or GPU benchmark |

These reference solutions do not represent learner responses or mastery.

## Hints

1. Count both keys and values across every layer and KV head; multiply by bytes per scalar.
2. Divide remaining bytes by bytes per request, then round down. Check the next token too.
3. Round each request separately before summing. A block cannot lend its unused tail to a separate private request.
4. Separate service start, first-token time and final completion. Keep every clock relative to arrival.
5. Recount timely completions before changing the cost denominator.
6. A lower memory peak says nothing by itself about service time or answer quality.

## 1. Tensor budget

The coefficient is 2×32×8×128×2=131,072 bytes per cached token, or 128 KiB. Stored weights consume (6×2^30)×2=12 GiB. Remaining memory is 24−12−4=8 GiB, hence 8×2^30/131,072=65,536 token positions. A request at 4,096 positions consumes 512 MiB; sixteen fit arithmetically.

Doubling Hkv to 16 doubles the coefficient to 256 KiB and makes a 4,096-position request consume 1 GiB. Eight fit. This changes only the assumed KV layout; a real architecture change can also alter parameter count and quality. Holding those fixed is a sensitivity exercise, not a specification of an actual replacement model.

**Criterion:** Correct tensor dimensions, binary units and omitted-state boundary. No substitution of query-head count without a layout justification.

## 2. Length and concurrency

At lengths 1,024, 2,048, 4,096 and 8,192, per-request state is respectively 128,256,512 and 1,024 MiB. Dividing the 8,192 MiB pool gives 64,32,16 and 8 requests. These are memory-only limits; none is a throughput claim.

Sixteen requests at 4,096 positions exactly fill the pool. One more unrounded cached position exceeds it by 128 KiB. With 16-slot blocks, growing one such request to 4,097 requires a new 2 MiB block. If all sixteen grow, the next allocation requires 32 MiB. A correct scheduler needs reserved growth space or a declared fallback such as queueing/preemption; silently exceeding capacity is not a policy.

**Criterion:** Distinguish live-byte growth from allocation-step growth and present occupancy from a safe generation horizon.

## 3. Block accounting

| Block size | Rounded lengths | Allocated slots | Slack slots |
| ---: | --- | ---: | ---: |
| 8 | 24,32,32,8 | 96 | 15 |
| 16 | 32,32,32,16 | 112 | 31 |
| 32 | 32,32,32,32 | 128 | 47 |

The live count is always 81. At size 16, 112×128 KiB=14 MiB is allocated and 31×128 KiB=3.875 MiB is unused tail capacity. Four fixed 64-position reservations instead allocate 256 slots=32 MiB, with 175 unused slots at this instant. Those slots may be intentional future capacity; they are not necessarily fragmented free memory.

External fragmentation can prevent a large contiguous request despite sufficient total free space. Internal slack lies inside allocated blocks. The fixture has private blocks and no block-table accounting beyond the declared reserve. Smaller B reduces slack here, but latency could worsen through more lookups or less efficient access. Only measurement decides that trade-off.

**Criterion:** Per-request rounding, exact totals and accurate definitions; no claim of zero total waste.

## 4. Two schedule traces

For b=1, prefill takes 10 ms and four decode rounds take 4×5=20 ms. Each request takes 30 ms. Serial starts are [0,30,60,90], giving first-token times [10,40,70,100] and completions [30,60,90,120]. Only the first completes by 50 ms.

For b=4, prefill takes 16 ms and four rounds take 4×8=32 ms. All first tokens arrive at 16 ms; all completions occur at 48 ms. All four meet 50 ms. Makespan throughput is 4/0.120 versus 4/0.048, or approximately 33.33 and 83.33 requests/s. These finite-trace ratios do not establish sustainable traffic rates.

The first request's streaming gap worsens from 5 to 8 ms. Its first token is also later. Four outputs sharing a 48 ms computation does not divide their experienced response times by four. It divides busy resource time per output, a different metric.

**Criterion:** Same workload, full response clocks, inclusive deadline and explicit objective. No percentile claims from four requests.

## 5. Counterexample and economics

At 40 ms, serial completion 30 qualifies but 60,90,120 do not. Batch completion 48 does not qualify for any request. Serial delivers 1/4 timely results; batching delivers 0/4. Thus a policy with higher completed-request throughput can lose on the chosen objective.

With price r per busy second, serial costs 0.120r and batch costs 0.048r for the full trace. At 50 ms the charges per timely result are 0.120r and 0.012r. At 40 ms serial remains 0.120r, while batch's denominator is zero: report no timely result and its incurred charge, not zero cost or a finite ratio.

Longer prompts, longer generations, bandwidth contention or larger batch sizes outside the assumed range can invalidate the service laws. If requests arrive far apart, batch formation adds waiting and the comparison changes again. Billing over a fixed provisioned window rather than busy time can also change the financial comparison.

**Criterion:** Preserve late work in the numerator, timely outcomes in the denominator and undefined zero-success ratios.

## 6. A test that can reject the optimization

Replay identical timestamped requests independently of completion. Fix architecture, weights, precision, decoding/stopping rules and correctness rubric. Record prompt/output lengths and repeat controlled runs with a stated warmup policy. Compare allocated versus live memory, workspace peaks, first-token and inter-token latency, end-to-end completion, offered/admitted/rejected counts and timely-correct outcomes. Count cancellations, preempted/recomputed work, idle time and startup under the same resource-accounting window.

Reject the optimization if lower memory usage accompanies worse timely-correct completion, unacceptable streaming gaps, corruption of retained state, isolation failures or greater total cost under the declared objective. If memory has headroom but longer batches saturate memory bandwidth, more available slots are not useful admission capacity. If temporary workspace exceeds its reserved bound, the memory model itself is invalid. A useful experiment identifies which hypothesis failed instead of declaring paging universally good or bad.

Quality and authority remain independent constraints from A03/S06. Shared prefixes require compatible state and access boundaries; the private-block fixture has not validated cross-request sharing. A05 will evaluate the full workflow rather than treating emitted tokens as useful outcomes.

**Criterion:** A falsifiable outcome, consistent denominator, resource evidence and clearly bounded claims.

## Reproduce the checks

The script below uses exact arithmetic for budgets and the assigned service laws. It checks 4,096 length/block combinations and 64 concurrency boundaries, plus both schedules and cost ratios. These are finite model checks, not hardware experiments.

```python
from fractions import Fraction as F
GiB=2**30
MiB=2**20
c=2*32*8*128*2
pool=24*GiB-(6*GiB)*2-4*GiB
assert c==128*1024 and pool//c==65536
assert [pool//(c*t) for t in (1024,2048,4096,8192)]==[64,32,16,8]
assert pool//(2*c*4096)==8
for n in range(1,65):
    max_t=pool//(c*n)
    assert n*max_t*c<=pool<n*(max_t+1)*c

def allocated(lengths,b):
    return sum(((t+b-1)//b)*b for t in lengths)
lengths=[17,31,32,1]
assert sum(lengths)==81
assert [allocated(lengths,b) for b in (8,16,32)]==[96,112,128]
assert allocated(lengths,16)*c==14*MiB
assert F((112-81)*c,MiB)==F(31,8)
assert 4*64*c==32*MiB
for b in (1,8,16,32):
    for t in range(1,1025):
        a=allocated([t],b)
        assert a%b==0 and 0<=a-t<b
        assert a-b<t<=a
assert allocated([4096]*16,16)*c==pool
assert allocated([4097]+[4096]*15,16)*c-pool==2*MiB
assert allocated([4097]*16,16)*c-pool==32*MiB

def times(b):
    prefill=8+2*b
    step=4+b
    return prefill,prefill+4*step
p1,s1=times(1);p4,s4=times(4)
starts=[i*s1 for i in range(4)]
first_s=[s+p1 for s in starts];finish_s=[s+s1 for s in starts]
first_b=[p4]*4;finish_b=[s4]*4
assert first_s==[10,40,70,100] and finish_s==[30,60,90,120]
assert first_b==[16]*4 and finish_b==[48]*4

def timely(xs,d):return sum(x<=d for x in xs)
assert [timely(xs,50) for xs in (finish_s,finish_b)]==[1,4]
assert [timely(xs,40) for xs in (finish_s,finish_b)]==[1,0]
# Deadline boundary checks establish inclusive semantics.
assert timely(finish_b,47)==0 and timely(finish_b,48)==4
assert F(4*1000,max(finish_s))==F(100,3)
assert F(4*1000,max(finish_b))==F(250,3)

def charge_per_timely(xs,d):
    n=timely(xs,d)
    return F(max(xs),1000)/n if n else None
assert charge_per_timely(finish_s,50)==F(120,1000)
assert charge_per_timely(finish_b,50)==F(12,1000)
assert charge_per_timely(finish_b,40) is None
print('PASS: budgets, 64 capacity boundaries, 4096 block cases, growth, schedules and costs')
```

## Revision history

- 1.0 — 2026-11-10. Six solutions, criteria and executable model checks. No learner performance inferred.

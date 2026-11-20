# C06 — Worked analysis

| Field | Value |
| --- | --- |
| ID | C06 answers |
| Title | Supplier-change decision: hints and checks |
| Revision | 1.0 |
| Date | 2026-11-15 |
| Prerequisites | S02/S06, A03–A05, B02/B03; SDE_C06.md |
| Capability developed | Audit migration costs, evaluation claims and evidence continuity |
| Source-check status | Uses the primary passage locators and limitations in the core memo |
| Experiment status | Embedded Python executed; synthetic accounting, paired counts and manifest validation only |

Read [SDE_C06.md](SDE_C06.md) before these optional solutions. No response or score is attributed to the learner.

## 1. Complete ledgers

Hint: convert minutes into cost, then add setup once.

At 1,000 cases and 0.50 U/minute, recurring labor is I=1,000, R=1,100 and B=1,750 U/month. Supplier plus labor plus incremental maintenance is therefore 1,500, 1,500 and 1,800 U/month. Six months plus setup gives **9,000, 9,900 and 11,100 U**. Retain I under the equal-adequacy premise.

After only I's fee becomes 700, its monthly total is 1,800 and horizon total 10,800. R becomes the cheaper adequate choice at 9,900. Savings are 900 U after setup. If R fails the authority or quality gate, the cost comparison cannot authorize migration. If I remains adequate, it stays available at its higher cost; if neither candidate is adequate, state that instead of weakening the task.

Assessment criterion: include human work, maintenance and setup, state the horizon, and separate customer cost from supplier margin. These are new C06 inputs, not replacements for B03's scenario.

## 2. Thresholds and omitted inputs

Hint: solve equal total costs with just one variable free.

For the fee, `6(x+1100)=9900` yields x=550 U/month. R is cheaper strictly above 550 at six months; at equality retain I. At x=700, compare `1800H` with `900+1500H`: equality is H=3. Only horizons longer than three months recover setup with a strict saving. Monthly payment timing and discounting are excluded from this simple model.

For bundle handling, `300+6(500t+50)=9000` gives t=2.8. Below that B is cheaper at the original I fee, provided all gates hold. The threshold is not evidence that such handling time is achievable. A measured extra export fee, migration overlap, training effort or maintenance cost moves the threshold. Add each in the correct period and avoid double-counting effort already included in setup.

Assessment criterion: name the fixed assumptions. Quoting a break-even number without its horizon or workload makes it unusable.

## 3. Paired evidence

Hint: totals include successes shared by both arms.

I has 92+4=96 successes and R has 92+3=95. There are seven discordant cases; R gains three and loses four. The paired sample difference is −1 percentage point for R. One shared failure is still in the denominator of 100. Both meet a 95% observed sample floor, but sampling uncertainty, representativeness and dependence remain unresolved.

This fixture validates arithmetic only. It does not establish that either real supplier meets a 95% population service objective. Inspect the seven disagreements, preserve held-out evaluation, analyze the relevant sampling unit and test complete workflows under load. Identical evidence supplied directly to both generators is useful diagnosis but bypasses deployed retrieval and cannot replace the whole-system comparison.

## 4. Repair evidence continuity

Hint: references identify revisions, not just logical documents.

Suppose current D17/3 is exported but an old decision references D17/2. Exporting another unrelated revision to keep the total row count unchanged does not repair the missing historical reference. Recover the authorized immutable bytes and manifest for D17/2, validate its digest and locator interpretation, and rerun reference validation. If recovery is impossible, mark the historical evidence gap; do not relabel D17/3 as revision 2.

A digest match verifies bytes relative to a trusted expected digest; it does not prove the trusted manifest itself is correct or that access was authorized. The following fixture checks exact keys, byte digests and reference closure. It uses tiny invented bytes, not an actual storage export or encryption/access-control implementation.

## 5. Cutover, rollback and the advantage claim

Hint: the replaceable component and authoritative state have different lifecycles.

Shadow execution writes no business effects. A new complete revision becomes current only at the atomic publication boundary. Before publication, a crash leaves the previous head; after publication, the new head must resolve to complete durable evidence. A rollback changes future execution or a valid head under the declared protocol; it never rewrites prior receipts or their evidence. Permission checks cover export, recovery and support paths as well as ordinary requests.

The claimed advantage is disproved for this scenario if the bundle meets the same evidence, authority and deadline gates while reducing handling below 2.8 minutes at its assigned costs. Do not respond by counting only the incumbent's successful cases or by trapping customer records. Usable exports and preserved evidence make the comparison more honest. An adapter's syntactic compatibility alone does not prove semantic, operational or economic portability.

## Reproducible checks

Run with Python 3. All money uses exact rational arithmetic. The fee sweep checks 1,001 choices; the horizon sweep checks 12 month values. The validator tests a good export, a missing revision, corrupted bytes and a same-count replacement that loses a referenced revision.

```python
from fractions import Fraction as F
from hashlib import sha256

N, wage = 1000, F('.5')
def monthly(fee, minutes, maintenance):
    return fee + N*wage*minutes + maintenance
mI = monthly(400, F(2), 100)
mR = monthly(250, F('2.2'), 150)
mB = monthly(0, F('3.5'), 50)
assert (mI,mR,mB) == (1500,1500,1800)
assert (6*mI,900+6*mR,300+6*mB) == (9000,9900,11100)
assert 6*monthly(700,F(2),100) == 10800
fee_threshold = F(9900,6)-1100
assert fee_threshold == 550
bundle_threshold = (F(9000-300,6)-50)/(N*wage)
assert bundle_threshold == F('2.8')
for fee in range(1001):
    totals = {'I':6*(fee+1100), 'R':9900, 'B':11100}
    winner = min(totals, key=totals.get)  # insertion order retains I at a tie
    assert winner == ('I' if fee <= 550 else 'R')
for months in range(1,13):
    saving = 1800*months-(900+1500*months)
    assert (saving>0) == (months>3)
    assert (saving==0) == (months==3)
assert 300+6*monthly(0,bundle_threshold,50) == 9000
assert 300+6*monthly(0,bundle_threshold-F('.01'),50) < 9000
assert 300+6*monthly(0,bundle_threshold+F('.01'),50) > 9000
both, only_i, only_r, neither = 92,4,3,1
assert both+only_i+only_r+neither == 100
assert (both+only_i,both+only_r) == (96,95)
assert F(only_r-only_i,100) == F('-0.01')

key2, key3 = ('A','D17',2), ('A','D17',3)
expected_bytes = {key2:b'reference X',key3:b'reference Y'}
trusted = {k:sha256(v).hexdigest() for k,v in expected_bytes.items()}
references = {key2,key3}
def valid_export(export):
    return (set(export)==set(trusted)
            and references <= set(export)
            and all(sha256(export[k]).hexdigest()==trusted[k] for k in trusted))
assert valid_export(expected_bytes)
missing = {key3:expected_bytes[key3]}
assert not valid_export(missing)
corrupt = dict(expected_bytes); corrupt[key2]=b'reference Z'
assert not valid_export(corrupt)
swapped = dict(missing); swapped[('A','D99',2)]=b'reference X'
assert len(swapped)==len(expected_bytes) and not valid_export(swapped)
# Recovery model: publication may point only to a complete revision.
for committed in (False,True):
    durable = {key2,key3}
    head = key3 if committed else key2
    assert head in durable and references <= durable
print('PASS: exact ledgers; 1001 fee cases; 12 horizons; paired counts; 4 export fixtures; 2 publication states')
```

Executed successfully on 2026-11-15. Metadata, five exercise/answer mappings, companion links, fences and placeholder checks also passed. These finite fixtures do not exercise a real supplier, concurrency protocol, recovery log, model or live migration. Actual export rights, service quality, costs and operational ownership require evidence before applying the recommendation.

# C04 — Worked analysis and reproducible checks

| Field | Value |
| --- | --- |
| ID / title | C04 answers · Product-boundary analysis |
| Revision / date | 1.0 · 2026-11-14 |
| Prerequisites | [C04 memo](SDE_C04.md), B01–B03, S06 |
| Capability developed | Separate feasibility from preference and test a boundary choice against costs and authority |
| Source-check status | Uses the memo's verified R19/R21/R11 passages; scenarios are original |
| Experiment status | Exact arithmetic and finite decision checks executed; no customer or security experiment |
| Assessment convention | Criteria apply to future answers, not assumed learner mastery |

## 1. Responsibility and revocation

**Hint:** Identify the person who performs work separately from the principal allowed to authorize an effect.

**Worked analysis:** The customer sponsor funds the work; the data owner authorizes processing; the preparation operator assembles evidence; the customer reviewer decides on payment. Hosted self-serve leaves exception operations with the customer. Managed adds supplier operators and scoped human access. Internal moves runtime recovery and maintenance to a customer owner. All three retain customer payment approval.

A supplier analyst's grant allows only the named tenant/case scope and operations. After revocation commits, a new protected read must fail under the memo's contract. Identity still being authenticated does not restore authorization. Access checks need to cover exports, support tools, logs and recovery, not only the ordinary UI. Already disclosed information cannot be recalled by denying the next request; retained copies need separately defined handling.

R11 gives principles; the actual revocation enforcement and trustworthy policy state are implementation premises. A generated statement that an administrator approved something does not create a grant. If current policy cannot be established, deny or defer the protected action rather than treating the uncertainty as permission. This can reduce availability while preserving the chosen authority rule.

**Criteria:** Distinguishes identity, authorization, data disclosure and new effects. Names an operational owner without granting it unnecessary payment authority.

## 2. Customer economics and setup feasibility

**Hint:** Apply the setup cap after calculating value; do not delete setup cost when more hours become available.

**Worked analysis:** Baseline work is 100×8/60=40/3 hours/month, valued at 400 U. Recurring labor under the three options is 200,100,150 U/month. Including monthly fees/infrastructure gives recurring costs of 320,280,190 U/month. Net monthly benefit relative to baseline is therefore 80,120,210 U.

Six-month benefits less setup are 480−120=360 U, 720−60=660 U and 1,260−360=900 U. With a four-hour onboarding cap, self-serve (4) and managed (2) fit; internal (12) does not. Assuming all other gates pass, managed maximizes modeled value among feasible candidates. The 240 U difference between internal and managed is an opportunity that cannot be realized with the initial setup allocation.

These values do not prove actual cash savings. Fixed salaries may remain unchanged; released time needs a useful alternative use. Nor do they establish willingness to pay. Common quality and operational-cutoff assumptions must be tested. If one option attains its lower time only by omitting necessary evidence, its numbers are not comparable.

**Criteria:** Gets all three values, excludes the infeasible option, and distinguishes capacity value from observed cash or demand.

## 3. Supplier viability and overhead sensitivity

**Hint:** There are separate customer and supplier onboarding costs. They represent different parties' work.

**Worked analysis:** Self-serve's monthly contribution after the assigned overhead is 120−40−10=70 U. Across six paid months, subtracting 60 U onboarding and 200 U acquisition leaves 160 U. Managed's corresponding contribution is 180−120−10=50 U; 300−90−200=10 U remains.

For managed monthly overhead a, remainder is 6(60−a)−290=70−6a. Nonnegative remainder requires a≤35/3≈11.67 U/month. At a=12, remainder is −2 U, so managed fails the stated supplier gate. Self-serve's value stays 360 U and its remainder is 160 U if its own overhead stays ten; it becomes the initial feasible choice. This isolated stress changes managed overhead only.

The cost floor for a managed monthly fee at overhead ten is 120+10+290/6=1,070/6≈178.33 U. The assigned 180 U fee is only about 1.67 U above that floor. A price rise could help the supplier but reduce customer value or change adoption; it is a new offer, not an automatic repair. No total-company profitability is established, since the overhead allocation and omitted costs require actual reconciliation.

**Criteria:** Includes acquisition, supplier setup and overhead once; recognizes a narrow buffer and refuses to infer profitability from it.

## 4. Revised constraint and maintenance thresholds

**Hint:** Change available setup hours only for the primary reversal. Treat ongoing extra maintenance as a separate sensitivity.

**Worked analysis:** At twelve available hours, internal clears the setup gate. Its 900 U exceeds managed's 660 and self-serve's 360. The qualified operating owner and recurring allowance are unchanged premises. The additional eight available hours enable the option but do not lower its twelve-hour setup cost.

If additional maintenance is x hours/month, internal value is 900−180x. It ties managed at x=240/180=4/3 hours/month. Below this, internal is preferable if all gates pass; above it, managed has greater value. At x=5, internal value reaches zero, equal to the incumbent. An option can remain better than doing nothing yet lose to another feasible option: x=2 gives internal 540 U, positive but below managed's 660.

Ties should be reported, not concealed with arbitrary precision. A real tie could be resolved by confidence, reversibility or a further test; these preferences are not built into this fixture. With no external processing permission and the initial four-hour cap, both hosted options fail authority and internal fails capacity. The incumbent is the only modeled feasible path. A new timeline, allocation or redacted-data offer requires fresh assumptions.

**Criteria:** Revises the recommendation, preserves counted labor, distinguishes two thresholds and accepts deferral when gates exclude every candidate.

## 5. Evidence plan and operational handoff

**Hint:** State what could reject the recommended option before proposing more features.

**Worked analysis:** Confirm the resource allocation with the sponsor, processing permissions with the data owner and ongoing responsibility with each operator. Use a bounded set of permitted cases spanning routine work, missing records, changed revisions and exceptions. Compare complete evidence support and cutoff compliance on matched cases. Log customer and supplier effort separately; classify setup, recurring operations and exceptional rework without overlap. Count unresolved cases and failures rather than filtering them out of the denominator.

An initial pilot should produce non-effecting drafts and exercise denied reads, revoked grants and unavailable policy. It should not authorize payments. Stop if an unauthorized disclosure/effect occurs or evidence identity cannot be preserved. Reconsider managed if overhead or support costs exceed the narrow supplier buffer. Reconsider internal if actual maintenance erases its advantage or the operating owner cannot sustain it. No sample size here certifies security, general market demand or long-term retention.

For exit, assign an owner to export mappings, evidence identifiers, outstanding cases and runbooks. Verify that the receiving process can interpret the export. Revoke access and handle retained copies according to the agreed lifecycle rules. A deletion request and a completed deletion are different statuses. Migration effort belongs in the next option comparison. A useful pilot can justify another bounded investment without proving the whole service is viable at scale.

**Criteria:** Includes fair quality/cost measurement, authority tests, stop rules, alternative evidence and an actionable exit. Does not invent customer commitments or completed deployment tests.

## Executed conditional checks

This standard-library script was executed during production. It checks the ledgers, exact boundaries and a finite decision grid. It does not implement authorization, measure real labor or validate demand. Permission and quality flags represent hypothetical gate outcomes; they are not security-test results.

```python
from fractions import Fraction as Q

H,n,b,w = 6,100,8,30
spec = {
    'self': (4,120,0,4),
    'managed': (2,180,0,2),
    'internal': (3,0,40,12)
}
def value(name,extra_internal=Q(0)):
    t,fee,infra,setup=spec[name]
    result=H*(Q(n*(b-t)*w,60)-fee-infra)-setup*w
    return result-H*w*extra_internal if name=='internal' else result

def remainder(name,overhead=Q(10)):
    fee,cost,setup=(120,40,60) if name=='self' else (180,120,90)
    return H*(fee-cost-overhead)-setup-200

def choose(cap,external=True,extra_internal=Q(0),managed_overhead=Q(10),quality=True):
    eligible={'incumbent':Q(0)}
    for name in spec:
        if not quality or spec[name][3]>cap: continue
        if name!='internal':
            if not external: continue
            a=managed_overhead if name=='managed' else Q(10)
            if remainder(name,a)<0: continue
        eligible[name]=value(name,extra_internal)
    best=max(eligible.values())
    return {name for name,v in eligible.items() if v==best}

assert [value(k) for k in spec]==[360,660,900]
assert [remainder('self'),remainder('managed')]==[160,10]
assert choose(4)=={'managed'}
assert choose(12)=={'internal'}
assert remainder('managed',12)==-2
assert choose(4,managed_overhead=12)=={'self'}
assert choose(4,external=False)=={'incumbent'}
assert choose(12,external=False)=={'internal'}
assert choose(12,quality=False)=={'incumbent'}
assert remainder('managed',Q(35,3))==0
assert Q(120+10)+Q(290,6)==Q(1070,6)
assert value('internal',Q(4,3))==660
assert value('internal',5)==0
assert value('internal',2)==540
assert choose(12,extra_internal=Q(4,3))=={'internal','managed'}
for delta in [Q(-1,100),Q(0),Q(1,100)]:
    assert (remainder('managed',Q(35,3)+delta)>=0)==(delta<=0)
    assert (value('internal',Q(4,3)+delta)>=660)==(delta<=0)

# 25 setup caps x 49 maintenance values x 2 permission states = 2450 cases.
# Extra maintenance ranges 0..4 hours/month in twelfths; all other gates fixed.
checks=0
for c in range(25):
    cap=Q(c,2)
    for j in range(49):
        x=Q(j,12)
        for external in [False,True]:
            got=choose(cap,external,x)
            if cap<2:
                want={'incumbent'}
            elif cap<12:
                want={'managed'} if external else {'incumbent'}
            elif not external:
                want={'internal'}  # value remains positive throughout this grid
            elif x<Q(4,3):
                want={'internal'}
            elif x==Q(4,3):
                want={'internal','managed'}
            else:
                want={'managed'}
            assert got==want,(cap,x,external,got,want)
            checks+=1
assert checks==2450
print('PASS: ledgers, overhead/maintenance boundaries, choice reversal, authority/quality gates, 2450 decision cases')
```

## Revision history

- 1.0 — 2026-11-14. Five worked analyses and executed exact decision checks.

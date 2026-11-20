# A05 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| ID / revision / date | A05 answers · 1.0 · 2026-11-11 |
| Title | Evaluation, workflows, and controlled autonomy — worked answers |
| Prerequisites | A01, A03, S06, A04 and [A05 core](SDE_A05.md) |
| Capability developed | Audit outcome denominators and enforceable control boundaries |
| Source-check status | R18/R17/R03 passages linked in core |
| Experiment status | Finite predicate/ledger calculations executed; no live model or external action |

Reference answers are not learner responses or mastery assessments.

## Hints

1. Who selects the next operation, and who authorizes it, are separate questions.
2. Count every offered case, then separately count answerable cases and timely drafts.
3. A budget must survive retries; a tool result cannot grant a privilege.
4. A repeated trial is not a new document. Selection needs a mechanism.
5. Start with a two-by-two table and label each denominator.
6. Isolate the useful capability in D2 before accepting the full loop's complexity.

## 1. Contract and baselines

All designs must return supported, current, scoped drafts or the appropriate unresolved/refusal disposition within two seconds, with no unauthorized disclosure/effect. None receives payment authority. W uses a coded exact lookup and template. M has one fixed bundle and one model call. L selects further read operations from observations but the controller constrains every dispatch. A workflow can contain a model; its control structure remains fixed if the next step is determined by code.

Compare the whole designs on the same offered population and permitted corpus. An identical-evidence diagnostic can isolate answer construction, but supplying oracle evidence bypasses retrieval and must be labeled separately. Returning unresolved for an answerable case is safer than inventing a claim, yet fails the chosen completion objective.

**Criterion:** Distinguish outcome, control and authority; preserve the same information/access contract.

## 2. Outcome and cost ledger

W's successful cases are D1,D3,D4,D6: 4/6. M's are D1,D4,D6: 3/6. L's are D1,D2,D3,D4: 4/6. Timely drafts occur on D1,D6 for W and M, and D1,D2 for L. Each therefore covers 2/4 answerable cases. D3/D4 are valid non-draft dispositions; counting them as drafts would inflate usefulness.

With total resource charges [6,12,24], charge per contract success is [6/4,12/3,24/4]=[1.5,4,6]. Charge per timely draft is [6/2,12/2,24/2]=[3,6,12]. Late and unsuccessful work remains in the numerator. These are constructed charges, not estimates from A04's hardware example or actual billing.

L has one forbidden approval attempt and zero committed mutations. The external guard succeeds on that case; the policy does not. D6 also lacks a draft, so it is not a contract success. More generally, a policy could attempt a forbidden action, get blocked, then produce a correct draft; report the attempt even if the final-artifact metric passes. A release gate can prohibit such attempts independently.

**Criterion:** Explicit denominators, separate refusal/draft outcomes, and attempted versus realized violations.

## 3. Traces and enforcement

Successful D2: scoped search → exact passage read → supported draft → validation. The two reads remain within the three-call cap. Missing evidence: three permitted empty reads consume all three slots; a fourth is denied and the controller returns unresolved. Invalid proposals terminate immediately under the declared policy rather than allowing endless free retries.

Hostile observation: source text requests approval → model proposes `approve` → controller rejects because it is outside the allowlist → record the attempt; no mutation. Tenant mismatches and revoked read permission must also fail before evidence is returned. Neither a matching schema nor an apparently sensible action proves authority.

The sequential check below counts admitted external calls. It does not implement identity verification, concurrent revocation, cancellation of running calls, token accounting or semantic support. A real controller additionally needs model-call/output-size caps, elapsed-time enforcement, bounded tool responses, and checks on final disclosure. If a future mutation times out, consult its stable operation identity; blindly retrying under a new identity can duplicate effects.

**Criterion:** A bounded failure path, no budget reset, authority from trusted execution context and honest implementation limits.

## 4. Repeated trials

Rates by case are 3/3,2/3,1/3,0/3. Equal-case mean is (1+2/3+1/3+0)/4=1/2. Pooled success is 6/12=1/2 because all trial counts match. The four underlying cases remain four cases; independent-document uncertainty cannot be calculated by pretending the twelve attempts are unrelated.

Three cases have at least one success, hence 3/4 is an oracle best-of-three result. To realize it, a system must run multiple attempts and correctly select an acceptable answer. The selection procedure can fail, incurs cost, and must be evaluated as part of the complete system. Unequal trial counts make pooled and equal-case means potentially differ; report the intended estimand before aggregating.

Keep all revisions of a document family together in the holdout, reconstruct evidence at decision time, and repeat under a frozen sampling configuration. Variation across seeds is not evidence of diversity across suppliers or future periods.

**Criterion:** Distinguish case diversity, stochastic variation and selection-system performance.

## 5. Judge disagreement

| Reference adjudication | Judge accepts | Judge rejects | Total |
| --- | ---: | ---: | ---: |
| Correct | 6 | 1 | 7 |
| Incorrect | 3 | 2 | 5 |
| Total | 9 | 3 | 12 |

Agreement is (6+2)/12=2/3. Acceptance precision is 6/9=2/3; false-accept rate among incorrect outputs is 3/5. False rejection among correct outputs is 1/7. The equal numerical values of agreement and precision here are accidental; the populations differ.

Blind the system identity, inspect original sources/revisions and action logs, and ask a second qualified reviewer to apply the same rubric. Preserve initial judgments. Distinguish ambiguity, context omission, source conflict and evaluator mistakes. Do not settle disagreements by choosing whichever answer helps the preferred system. Treat adjudication as a reference procedure whose reliability also needs checking. Validate changes on new cases; a disagreement-only sample cannot estimate overall error directly.

**Criterion:** Correct confusion matrix, denominator labels, and a process that permits both human and judge error.

## 6. Next decision

Keep W as the baseline under this ledger. Investigate a fixed alternate-extraction branch for D2, using held-out document families and the same source-time contract. Compare that addition with L under identical budgets, deadlines and scoring, recording all cases and violations. L might still be justified if held-out tasks require adaptive searches that fixed branches cannot cover, but that has not been demonstrated.

Before deployment, test real tool errors, latency tails, revocation, malformed responses and output containment; use shadow operation to observe distribution changes without granting effects. A later controlled rollout must evaluate reviewer behavior and shared-resource interference. The frozen ledger cannot establish customer value, operational safety across every route, or performance after source/provider changes. R17's dependency and feedback concerns remain relevant even if model weights are unchanged.

**Criterion:** Choose the simplest supported design, name evidence that could reverse it, and preserve offline-to-live limits.

## Reproduce the checks

This is an executable specification of the constructed accounting and sequential admission rules. It does not simulate a language model, network, clock progression, or semantic judge.

```python
from fractions import Fraction as F
from itertools import product
# Tuples: contract success, timely supported draft, forbidden attempts, effects.
rows={
 'W':[(1,1,0,0),(0,0,0,0),(1,0,0,0),(1,0,0,0),(0,0,0,0),(1,1,0,0)],
 'M':[(1,1,0,0),(0,0,0,0),(0,0,0,0),(1,0,0,0),(0,0,0,0),(1,1,0,0)],
 'L':[(1,1,0,0),(1,1,0,0),(1,0,0,0),(1,0,0,0),(0,0,0,0),(0,0,1,0)]}
charges={'W':6,'M':12,'L':24}
for name,expected in [('W',4),('M',3),('L',4)]:
    data=rows[name]
    successes=sum(r[0] for r in data);drafts=sum(r[1] for r in data)
    assert successes==expected and drafts==2
    assert F(drafts,4)==F(1,2) and sum(r[3] for r in data)==0
assert [F(charges[n],sum(r[0] for r in rows[n])) for n in rows]==[F(3,2),F(4),F(6)]
assert [F(charges[n],2) for n in rows]==[F(3),F(6),F(12)]
assert sum(r[2] for r in rows['L'])==1

allowed={'read_revision','search_evidence'}
def admit(op,authenticated,same_tenant,grant,used,elapsed):
    return (op in allowed and authenticated and same_tenant and grant
            and 0<=used<3 and 0<=elapsed<2000)
# Exhaustive 3 operations x 8 flag combinations x 5 counts x 4 clock inputs.
count=0
for op,auth,scope,grant,used,elapsed in product(
    ['read_revision','search_evidence','approve'],[False,True],[False,True],
    [False,True],range(5),[0,1999,2000,2001]):
    result=admit(op,auth,scope,grant,used,elapsed)
    if result:
        assert op!='approve' and all([auth,scope,grant]) and used<3 and elapsed<2000
    if op in allowed and all([auth,scope,grant]) and used<3 and elapsed<2000:
        assert result
    count+=1
assert count==480
used=0
for _ in range(3):
    assert admit('search_evidence',True,True,True,used,100)
    used+=1 # empty results still consume the dispatched-call budget
assert not admit('search_evidence',True,True,True,used,100)
assert not admit('approve',True,True,True,0,100)
assert admit('read_revision',True,True,True,0,100)
assert not admit('read_revision',True,True,False,1,100) # subsequent revoked grant
counts=[3,2,1,0]
assert sum(F(x,3) for x in counts)/4==F(1,2)
assert F(sum(counts),12)==F(1,2)
assert F(sum(x>0 for x in counts),4)==F(3,4)
# Unequal trial allocations can change the pooled estimand.
assert (F(1,1)+F(0,3))/2==F(1,2)
assert F(1,4)!=F(1,2)
tp,fn,fp,tn=6,1,3,2
assert tp+fn+fp+tn==12
assert F(tp+tn,12)==F(2,3)
assert F(tp,tp+fp)==F(2,3)
assert F(fp,fp+tn)==F(3,5) and F(fn,tp+fn)==F(1,7)
print('PASS: ledger, cost denominators, 480 admission cases, budget/revocation, trials and judge counts')
```

## Revision history

- 1.0 — 2026-11-11. Six reference solutions and bounded executable checks; no learner performance inferred.

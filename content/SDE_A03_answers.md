# A03 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| Title | Retrieval, external knowledge, and provenance — worked answers |
| ID / revision / date | A03 answers · 1.0 · 2026-11-10 |
| Prerequisites | S02, S06, A01, A02 and [A03 core](SDE_A03.md) |
| Capability developed | Separate evidence availability, retrieval, context delivery and claim support |
| Source-check status | R15 methods and R11 mediation; exact URLs/locators in core |
| Experiment status | Executed finite fixtures and exact arithmetic; no live search, generation or semantic entailment experiment |

These are reference solutions, not learner responses or mastery assessments.

## Hints

1. Apply eligibility before interpreting a ranking; inspect the context actually supplied.
2. Change one stage at a time while keeping the query and required evidence fixed.
3. Read the claim's temporal and business scope, not only its nouns.
4. A missing index entry and a revoked grant call for different explanations.
5. Compare sum-of-products with product-of-sums using the same probabilities.
6. State every denominator. A component metric can improve while task success falls.

## 1. Candidate and context trace

At t=20, the authoritative head is revision 3. `old` is stale for the current query; `other` is a different tenant. Eligible candidates are `note` at 93 and `new` at 88. Top-1 is [`note`]; top-2 is [`note`,`new`]. Keeping only the first candidate loses the delivery evidence even with k=2. The declared field-aware selector chooses `new` because it contains the requested field.

For this exact tenant/document/revision/field question, direct fact lookup is the natural baseline and returns Y with its frozen locator. More general search might help with paraphrases or unstructured documents, but that benefit is not demonstrated by this fixture. If multiple eligible passages claim conflicting delivery values, an explicit resolution rule is required; the field-aware selector alone does not resolve truth.

**Criterion:** Separate eligibility, candidate recall and context sufficiency; no confidence interpretation of scores.

## 2. Controlled failure isolation

Missing evidence: remove `new` from the indexed corpus while retaining the authoritative manifest expectation. Compare expected versus indexed revision contents; k changes cannot fix it.

Present but not retrieved: restore `new`, use k=1, and observe only `note`. Force `new` into the candidate set to distinguish a retrieval miss from downstream problems.

Retrieved but dropped: use k=2, then retain only score-first `note`. Compare candidate IDs with actual context IDs. Supply `new` directly to the answering component as a diagnostic, without calling that oracle run deployed performance.

Supplied but ignored: context includes `new`, yet the answer states delivery X. Inspect the exact model input and output and their claim-level comparison. A higher-recall retriever cannot fix this already-sufficient context on its own.

Cited without support: retain context [`new`] and emit “Payment is settled” with that citation. The locator resolves, but the fixture contains no settlement fact. Validate the claim–passage relationship rather than counting citation syntax.

**Criterion:** One controlled intervention per boundary, with observable artifacts. Real cases can contain several failures; a triage label is not proof of a unique root cause.

## 3. Provenance is necessary but narrower than truth

`old` supports “revision 2 listed X” if the old bytes and locator resolve and the reader may access them. It does not support the current-state claim at t=20, because the head is revision 3. `new` supports “revision 3 lists Y,” and supports the current published-reference answer only with the authoritative head/time link. Neither passage supports settlement.

A claim “X” cited to `new` fails the assigned fact comparison. A claim “payment settled” cited to `new` fails even though the citation is syntactically valid and current. An authentic passage can still be factually wrong about the world. Distinguish “the source states Y” from independently verified delivery.

Keep exact tenant/document/revision/passage identity, bytes, rendering/extraction version and locator. Replacing old evidence with current bytes destroys historical reproducibility. A digest is an integrity check, not a substitute for retained content. Multiple claims need individual coverage; missing support is not repaired by adding more unrelated citations.

**Criterion:** Correct scope, source identity and permission; no inference from link existence to semantic support or physical truth.

## 4. Time, ingestion and permission changes

At t=10, revision 2 is the published head; X is the answer for that historical state, assuming current permission to view its retained evidence. The query-time snapshot and the disclosure-time access decision are different controls.

At t=20 with revision 3 selected but `new` absent from the index, report current evidence unavailable, or perform an authorized direct lookup. An older answer is acceptable only as an explicitly labeled older result under a contract that allows it. Quietly returning X as current fails.

If permission is revoked before display, withhold the protected content under the selected immediate-disclosure policy. A previously allowed retrieval or cached answer is insufficient. An unavailable policy check also does not establish permission. Coordinating the check with disclosure is a deployment requirement, not a feature proved by the fixture's Boolean grant.

**Criterion:** Distinguish source publication, index readiness, query time and authorization freshness. Do not present delayed ingestion as “no such fact exists.”

## 5. Two marginalization calculations

For the fixed target sequence, sequence-level mixing gives 0.6×0.8×0.5 + 0.4×0.2×0.9 = 0.24+0.072=0.312. Token-level mixing gives (0.48+0.08)×(0.30+0.36)=0.56×0.66=0.3696. Their difference is 0.0576. The product-of-sums includes cross-passage contributions; it does not mean an observed output is guaranteed to combine correct facts.

The second-token probabilities are conditional on the same specified first-token prefix, not unconditional token frequencies. The two passages form the entire normalized toy distribution here. The paper uses a top-K approximation; these numbers are not its reported outputs. For a single-token target the two forms coincide, as summing over the same one-step terms yields the same result.

Retrieval weights concern passages given a query; A02 attention weights mix representations over positions; a correctness assessment concerns an answer's claims against evidence and reality. Matching a mathematical normalization pattern does not equate these targets.

**Criterion:** Correct conditioning, arithmetic and interpretation; no fabricated measured model accuracy.

## 6. Stage accounting and a falsifiable evaluation

Corpus coverage is 16/20=80%. Conditional candidate hit rate is 12/16=75%. Retention of sufficient evidence is 10/12≈83.33%. Supported completion after sufficient context is 7/10=70%. Multiplying yields 7/20=35%, because the nested counts cancel. No independence assumption is needed. Overall candidate hit rate is 12/20=60%, a different denominator from 75%.

For a higher-recall candidate, freeze the same eligible query population, target revisions, permissions, corpus snapshot, context budget and downstream procedure. Include new documents/groups according to deployment, keeping revisions together. Measure sufficient-evidence retrieval and actual selected-context sufficiency, supported answer completion, unauthorized exposures, abstentions, latency and cost. Keep missing/unanswered cases in the declared outcome population.

A retriever could increase candidate recall while adding distractions that crowd out the required evidence under the context budget. It could improve recall on authorized cases yet expose another tenant's data. Either can invalidate deployment. Use direct lookup as the baseline for exact field questions, and a separate relevance/support rubric for open-ended questions. Independent adjudication of contested support cases is needed; our hand-assigned fact map is not that adjudication system.

**Criterion:** Nested denominators, comparable policies and a concrete way the seemingly better component can fail the full contract.

## Reproduce the executed checks

This code implements only the declared fixture rules. The `facts` relation is an oracle supplied by the author, not inferred from prose. Authorization and head selection are sequential model inputs; concurrent policy changes, actual identity verification and index/storage failures are not simulated. Fixed rankings are not search-engine measurements.

```python
from fractions import Fraction as F
from itertools import permutations

# (tenant, document, revision, field, value) is the exact fact identity.
def passage(pid,tenant,rev,score,facts):
    return dict(id=pid,tenant=tenant,doc='D17',rev=rev,score=score,facts=facts)
corpus=[
    passage('old','A',2,97,{'delivery':'X'}),
    passage('other','B',3,95,{'delivery':'Z'}),
    passage('note','A',3,93,{}),
    passage('new','A',3,88,{'delivery':'Y'}),
]
def head(t):
    if t<5: return None
    return 2 if t<15 else 3

def eligible(p,t,grant=True):
    return grant and p['tenant']=='A' and p['doc']=='D17' and p['rev']==head(t)
def candidates(rows,t,k,grant=True):
    return sorted((p for p in rows if eligible(p,t,grant)),
                  key=lambda p:(-p['score'],p['id']))[:k]
def select(rows,field='delivery'):
    return sorted(rows,key=lambda p:(field not in p['facts'],-p['score'],p['id']))[:1]
def ids(rows):return [p['id'] for p in rows]
def supports(claim,p):
    tenant,doc,rev,field,value=claim
    return (tenant,doc,rev)==(p['tenant'],p['doc'],p['rev']) and p['facts'].get(field)==value

def disclose(claim,citation,context,t,grant=True):
    p=next((p for p in context if p['id']==citation),None)
    return bool(p and eligible(p,t,grant) and supports(claim,p))
claim=('A','D17',3,'delivery','Y')
assert ids(candidates(corpus,20,1))==['note']
assert ids(candidates(corpus,20,2))==['note','new']
context=select(candidates(corpus,20,2))
assert ids(context)==['new'] and disclose(claim,'new',context,20)
assert not disclose(claim,'new',context,20,False) # revoked before disclosure
assert not candidates(corpus,20,2,False)
assert ids(candidates(corpus,10,2))==['old']
assert head(4) is None and head(5)==2 and head(14)==2 and head(15)==3
assert not candidates(corpus,4,4)
old=corpus[0]
assert supports(('A','D17',2,'delivery','X'),old)
assert not disclose(('A','D17',2,'delivery','X'),'old',[old],20)
assert disclose(('A','D17',2,'delivery','X'),'old',[old],10)
assert not disclose(('A','D17',3,'payment','settled'),'new',context,20)
assert not disclose(('A','D17',3,'delivery','X'),'new',context,20)
assert not disclose(claim,'invented',context,20)
assert not disclose(claim,'new',[],20)
# Filtering only after global top-1 loses eligible results.
global_first=sorted(corpus,key=lambda p:-p['score'])[:1]
assert not [p for p in global_first if eligible(p,20)]
assert len(candidates(corpus,20,1))==1
# A second tenant's score cannot alter the result under this fixture's prefilter.
for score in [-100,0,1000]:
    changed=[dict(p,score=score) if p['id']=='other' else p for p in corpus]
    assert ids(select(candidates(changed,20,2)))==['new']
# Storage order is irrelevant because ranking has an explicit tie rule.
for rows in permutations(corpus):
    assert ids(select(candidates(rows,20,2)))==['new']

def diagnose(rows,cands,ctx,answer,citation):
    if not any(eligible(p,20) and supports(claim,p) for p in rows):return 'corpus'
    if not any(supports(claim,p) for p in cands):return 'retrieval'
    if not any(supports(claim,p) for p in ctx):return 'selection'
    if not disclose(answer,citation,ctx,20):return 'answer/support'
    return 'success'
missing=[p for p in corpus if p['id']!='new']
one=candidates(corpus,20,1);two=candidates(corpus,20,2)
assert diagnose(missing,candidates(missing,20,4),[],claim,'new')=='corpus'
assert diagnose(corpus,one,one,claim,'new')=='retrieval'
assert diagnose(corpus,two,two[:1],claim,'new')=='selection'
assert diagnose(corpus,two,context,('A','D17',3,'delivery','X'),'new')=='answer/support'
assert diagnose(corpus,two,context,('A','D17',3,'payment','settled'),'new')=='answer/support'
assert diagnose(corpus,two,context,claim,'new')=='success'
# Enough candidate depth cannot recover physically missing evidence.
for k in range(1,6):
    assert not any(supports(claim,p) for p in candidates(missing,20,k))
seq=F(3,5)*F(4,5)*F(1,2)+F(2,5)*F(1,5)*F(9,10)
tok=(F(3,5)*F(4,5)+F(2,5)*F(1,5))*(F(3,5)*F(1,2)+F(2,5)*F(9,10))
assert seq==F(312,1000) and tok==F(3696,10000) and tok-seq==F(576,10000)
rates=[F(16,20),F(12,16),F(10,12),F(7,10)]
product=F(1)
for rate in rates:product*=rate
assert product==F(7,20) and sum([4,4,2,3,7])==20
print('PASS: time boundaries, eligibility, ranking/selection, five failure fixtures,')
print('revocation/citation checks, 24 orderings, score perturbations, marginalization and stage rates.')
```

## Revision history

- 1.0 — 2026-11-10. Six reference answers and executed fixture checks; no learner performance inferred.

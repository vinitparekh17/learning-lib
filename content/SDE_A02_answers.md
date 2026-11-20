# A02 — Hints, worked answers and executable checks

| Field | Value |
| --- | --- |
| ID / revision / date | A02 answers · 1.0 · 2026-11-09 |
| Prerequisites | F04, A01 and [A02 core](SDE_A02.md) |
| Capability developed | Verify attention arithmetic and test information-flow boundaries without overstating model evidence |
| Source-check status | R14 versioned passages and locators in the core evidence ledger |
| Experiment status | Standard-library Python checks executed; no neural model training, benchmark or generation experiment |

These are reference solutions for later self-assessment, not inferred learner answers.

## Hints

1. Multiply rows by projection columns before forming query/key products.
2. Recompute the denominator after changing permitted keys.
3. Check whether the changed coordinate participates in WQ or WK.
4. The output retains query count and value width.
5. Write each input next to its target before discussing parallel computation.
6. Count allocated pairs separately from permitted pairs and measured work.

## 1. Full-context attention

WQ and WK select the first feature: Q=K=[1,0,1]ᵀ. WV preserves both features, so V=X. S has rows [1,0,1], [0,0,0], [1,0,1]. Because dk=1, scaling makes no numerical change in this case; it is still part of the general formula.

With Z=2e+1, rows 1 and 3 of A are [e/Z,1/Z,e/Z]; row 2 is [1/3,1/3,1/3]. Outputs 1 and 3 are (2e/Z,(2+e)/Z), approximately (0.844638,0.733044); output 2 is (2/3,1). Row normalization distributes one query's mass across keys. Column normalization would answer a different algebraic question and is not this contract.

**Criterion:** Correct projection and multiplication order, normalization axis and value-weighted output. Attention weights are not vocabulary probabilities or truth estimates.

## 2. Mask before normalization

Causal rows are [1,0,0], [1/2,1/2,0] and [e/Z,1/Z,e/Z]. Their outputs are (1,0), (1/2,1) and the original third output. Disallowing key 2 for query 3 leaves two equal scores, producing [1/2,0,1/2] and (1,1/2). Rows 1 and 2 are unaffected by that single connection change.

If row 2 is normalized over all three positions first and the final weight is then zeroed, the remaining weights are [1/3,1/3,0]. Their sum is 2/3 and the output is (1/3,2/3). Renormalizing the surviving positive weights would repair this particular finite example, but masking before the stable softmax directly implements the declared contract. All-masked rows have no valid distribution; the code rejects them.

**Criterion:** Show the changed denominator and distinguish a forbidden connection from a small score.

## 3. Future-value perturbation

Changing X3's second coordinate from 1 to 7 leaves Q/K unchanged because their projections use only the first coordinate. V3 increases by (0,6). Unmasked output differences are (0,6e/Z), (0,2), (0,6e/Z). Causal differences are (0,0), (0,0), (0,6e/Z).

With projections that use the second coordinate, K3 and Q3 may change too. Causality still excludes position 3 from outputs 1 and 2 if their inputs were causally constructed, but the third output's difference would not generally equal a fixed weight times 6. If earlier representations already encoded future content, their queries or permitted values could change, violating the premise of this layer-local argument.

**Criterion:** Separate changes to scores from changes to values and identify the upstream information assumption.

## 4. Shape contracts

Q is 3×4, K is 5×4 and V is 5×2. Scores and weights are 3×5; AV is 3×2. The divisor is √4=2. Five keys paired with only four values is invalid, as is a query width unequal to the key width.

For two heads each returning 3×2, feature concatenation produces 3×4 and a 4×2 output projection returns 3×2. That can be added elementwise to a 3×2 residual. Concatenating along positions produces 6×2 and cannot be added to the original X without redefining the operation. Even matching shapes do not guarantee matching feature meanings, as F04 showed.

**Criterion:** Identify both multiplication compatibility and semantic correspondence. Self-attention and cross-attention need not have the same query/key lengths.

## 5. Availability during fitting and generation

The training pairs by row are START→A, A→B and B→C. At row 2 the allowed input prefix is [START,A]; the target is B. With input [A,B,C] and the same targets, row 2 could inspect B directly through the diagonal connection. A causal index rule alone would not stop this labeling error.

Fitting updates parameters based on loss. In the fixed-weight generation procedure, each new input prefix includes actual earlier generated tokens; target tokens are not available in advance. Parallel computation over known shifted training inputs does not imply parallel availability of unknown generated tokens. A prefix error can change subsequent inputs, so evaluation should match the intended generation procedure.

If an earlier unmasked representation already mixed C into row 1, a later causal attention layer can read that contaminated row 1. The mask controls its own edges, not the entire history of its input tensors.

**Criterion:** Explicit input/target alignment, fixed versus updated weights and an upstream leakage counterexample. No conclusion about current proprietary models is required.

## 6. Cost, order and useful evidence

Dense pair counts are 3²=9 and 6²=36; causal permitted counts are 3·4/2=6 and 6·7/2=21. Full matrix computation followed by masking does not by itself save the work on the forbidden positions. With fixed dk and dv, the two attention matrix products scale with n²; projections and the rest of a network contribute additional costs.

Under a simultaneous row permutation of position-free X, Q/K/V permute consistently. The score matrix permutes in both axes, weights follow those changes and outputs permute by the same row order. The six-permutation check below tests this property. Holding positional vectors fixed while permuting token content is a different transformation, so it need not preserve the result.

To evaluate a cheaper local-context restriction, freeze candidate settings on development data and compare both systems on the same held-out document tasks. Include cases where necessary evidence is farther away than the permitted window, and keep revision/organization boundaries from A01. Measure supported correct answers, missing evidence, latency and resource use. If local arithmetic passes but long-distance evidence cases fail beyond a declared tolerance, reject or revise the restriction. Test limits and costs must come from the application; no numerical deployment threshold is invented here.

**Criterion:** Distinguish count models from benchmarks, state what is permuted, and propose a test that can falsify the cheaper design.

## Reproduce the checks

The implementation uses finite values and explicit Boolean allowed masks, with one permitted key required per query. Dropout and other Transformer components are absent. Tolerances reflect floating-point calculation, not statistical uncertainty. The expected expressions, metamorphic checks and deliberately wrong normalization provide checks beyond simply rerunning one function.

```python
from math import exp, sqrt, isclose
from itertools import permutations

def shape(a):
    assert a and a[0] and all(len(r)==len(a[0]) for r in a)
    return len(a),len(a[0])
def mm(a,b):
    na,da=shape(a);nb,db=shape(b)
    assert da==nb
    return [[sum(a[i][k]*b[k][j] for k in range(da))
             for j in range(db)] for i in range(na)]
def transpose(a):
    shape(a)
    return [list(c) for c in zip(*a)]
def softmax(scores,allowed):
    if not any(allowed):raise ValueError('no permitted key')
    top=max(s for s,ok in zip(scores,allowed) if ok)
    terms=[exp(s-top) if ok else 0.0 for s,ok in zip(scores,allowed)]
    z=sum(terms)
    return [t/z for t in terms]
def attention(q,k,v,allowed):
    nq,dq=shape(q);nk,dk=shape(k);nv,dv=shape(v)
    assert dq==dk and nk==nv and shape(allowed)==(nq,nk)
    scores=[[s/sqrt(dk) for s in row] for row in mm(q,transpose(k))]
    weights=[softmax(row,mask) for row,mask in zip(scores,allowed)]
    return weights,mm(weights,v)
def close(a,b):
    assert shape(a)==shape(b)
    assert all(isclose(x,y,rel_tol=1e-10,abs_tol=1e-10)
               for ar,br in zip(a,b) for x,y in zip(ar,br))
def fails(fn,kind):
    try:fn()
    except kind:return
    raise AssertionError('expected rejection')
X=[[1.,0.],[0.,2.],[1.,1.]]
W=[[1.],[0.]];I=[[1.,0.],[0.,1.]]
q=k=mm(X,W);v=mm(X,I)
full=[[True]*3 for _ in range(3)]
causal=[[j<=i for j in range(3)] for i in range(3)]
e=exp(1);z=2*e+1
expected=[2*e/z,(2+e)/z]
a,o=attention(q,k,v,full)
close(a,[[e/z,1/z,e/z],[1/3]*3,[e/z,1/z,e/z]])
close(o,[expected,[2/3,1.],expected])
ac,oc=attention(q,k,v,causal)
close(oc,[[1.,0.],[.5,1.],expected])
for mask,wts,out in [(full,a,o),(causal,ac,oc)]:
    for flags,row,value in zip(mask,wts,out):
        assert isclose(sum(row),1)
        assert all(w>=0 and (ok or w==0) for ok,w in zip(flags,row))
        for col in range(2):
            permitted=[v[j][col] for j,ok in enumerate(flags) if ok]
            assert min(permitted)-1e-10<=value[col]<=max(permitted)+1e-10
newmask=[r[:] for r in causal];newmask[2][1]=False
_,om=attention(q,k,v,newmask)
close(om,[[1.,0.],[.5,1.],[1.,.5]])
wrong=mm([[1/3,1/3,0]],v)
close(wrong,[[1/3,2/3]])
assert not isclose(sum([1/3,1/3,0]),1)
# Changing a feature ignored by Q/K isolates the value path.
x2=[r[:] for r in X];x2[2][1]=7
close(mm(x2,W),q)
_,o2=attention(mm(x2,W),mm(x2,W),x2,full)
_,oc2=attention(mm(x2,W),mm(x2,W),x2,causal)
close(o2,[[expected[0],expected[1]+6*e/z],[2/3,3.],
          [expected[0],expected[1]+6*e/z]])
close(oc2,[oc[0],oc[1],o2[2]])
# Every ordering without positions/masks must permute outputs consistently.
for p in permutations(range(3)):
    xp=[X[i] for i in p]
    _,op=attention(mm(xp,W),mm(xp,W),xp,full)
    close(op,[o[i] for i in p])
# Stable softmax is invariant to a common score offset.
close([softmax([1001,1000,1001],[True]*3)],[a[0]])
fails(lambda:softmax([1,2],[False,False]),ValueError)
fails(lambda:attention(q,k,v[:2],full),AssertionError)
fails(lambda:attention([[1,2]],k,v,[[True]*3]),AssertionError)
# Rectangular case checks dk scaling and query count, not just square shapes.
qr=[[1.,0.,0.,0.]]*3
kr=[[2.,0.,0.,0.]]+[[0.,0.,0.,0.]]*4
vr=[[1.,0.]]+[[0.,1.]]*4
ar,orr=attention(qr,kr,vr,[[True]*5 for _ in range(3)])
close(ar,[[e/(e+4)]+[1/(e+4)]*4]*3)
close(orr,[[e/(e+4),4/(e+4)]]*3)
assert shape(orr)==(3,2)
for n,dense,allowed in [(3,9,6),(6,36,21)]:
    assert n*n==dense
    assert sum(j<=i for i in range(n) for j in range(n))==allowed
print('PASS: projections, analytic attention, masks, convex bounds, value perturbation,')
print('all six permutations, stable softmax, invalid shapes/masks, rectangular scaling and counts.')
```

## Revision history

- 1.0 — 2026-11-09. Six reference solutions and executed numerical/information-flow checks.

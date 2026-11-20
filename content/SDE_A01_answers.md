# A01 — Hints, worked answers and checks

| Field | Value |
| --- | --- |
| ID / revision / date | A01 answers · 1.0 · 2026-11-09 |
| Prerequisites | F02–F04 and [A01 core](SDE_A01.md) |
| Capability developed | Defend what a score establishes and repair the information boundary of an evaluation |
| Source-check status | R13 and R02 inspected passages and URLs in the core evidence table |
| Experiment status | Exact standard-library Python checks executed below; no production prediction experiment |

These are reference solutions, not learner responses or evidence of mastery.

## Hints

1. Expand each squared residual. Keep the penalty separate from reported unpenalized MSE.
2. Use frozen parameters; do not fit to the final labels.
3. Ask whether the lookup key was already observed with a label.
4. Shared membership is transitive through graph paths, even without a direct shared attribute.
5. Split before fitting transformations. Arrival time and label-availability time differ.
6. Weight losses, not winners. Then ask whether conditional losses remain stable.

## 1. Fitting and regularization

For a constant c, training MSE is ((c−2)²+(c−4)²)/2 = (c−3)²+1, minimized at c=3. Its training and validation MSEs are 1 and 2.5. For wx, training loss is 2.5(w−2)². Adding λw² and setting the derivative 5(w−2)+2λw to zero gives w=10/(5+2λ). Positive curvature establishes a minimum.

For weights 2, 1, 0.5, the training MSEs are 0, 2.5, 5.625 and validation MSEs are 2.5, 0, 0.625. Report these prediction losses, not penalized objective values, when comparing on a common validation criterion. The baseline is fitted from training labels only.

Changing minutes to seconds multiplies label scale and fitted weights. Rescaling pages changes the numerical weights and penalty effect. Replacing mean squared loss with a sum also changes relative penalty strength. A λ value without its objective and feature units is incomplete.

**Criterion:** Correct residuals, unique minimum, explicit loss scaling; do not claim regularization must improve every dataset.

## 2. Selection and final evidence

Validation selects λ=2.5 and w=1 among the declared candidates. On final inputs 3 and 4 with targets 3 and 4, predictions are exact: MSE=MAE=0. The baseline predicts 3 for both: MSE=0.5 and MAE=0.5 minutes.

If final labels become 6 and 8 without changing the model, residuals are −3 and −4. MSE=12.5 and MAE=3.5. The baseline has residuals −3 and −5, giving MSE=17 and MAE=4. The unpenalized model would be exact on these changed labels. Thus validation selection is not a guarantee under a changed input–outcome relationship. Two constructed test cases cannot establish deployment accuracy or uncertainty.

**Criterion:** Freeze weights, distinguish the selected candidate from a hindsight winner, and state the test's limited population.

## 3. Revisions and memorization

Training on r1 of all four documents stores D1→2, D2→4, D3→6, D4→8. Every r2 lookup returns its assigned target, yielding zero MSE. The example has eight rows but only four underlying documents. The row allocation has no entirely unseen validation documents.

Training on D1/D2's four revision rows gives mean (2+2+4+4)/4=3. Unknown D3/D4 receive 3. Squared errors are 9,9,25,25, averaging 17. The constant baseline does exactly the same. There are two held-out documents, not four independent validation cases, and even those may share supplier/template effects. Do not form a confidence interval treating all revision rows as independent draws.

**Criterion:** Explain the task mismatch, not merely the numerical score change. Reusing known documents is not inherently forbidden if that is the actual application and labels truly existed at prediction time; it is wrong evidence for the stated new-document question.

## 4. Overlapping groups

A links D1 to D2; B links D3 to D4; template X links D1 to D3. The resulting path connects all documents. Holding out B separates organizations but leaves template X shared. Grouping by (A,X) and (B,X) as different pairs still shares X; grouping (A,X) and (A,Y) separately still shares A.

There is one connected component, so a nonempty train/test split cannot keep both organizations and templates disjoint. Acquire disconnected groups, restrict the intended claim to new organizations with known templates, or report the desired estimate unavailable. Dropping bridging records can create a different, selected population; document any exclusion and do not claim it represents all intake.

**Criterion:** Show the connecting path and acknowledge infeasibility rather than quietly weakening the holdout.

## 5. An evaluation plan that matches deployment

For future documents from existing suppliers, choose a historical fitting cutoff and a later test-intake window. Fit only on documents whose labels were available by cutoff. Keep a whole document family in one partition; declare boundary-crossing families excluded from this evaluation and count them separately. Reconstruct page counts and other permitted features at original intake, without later corrections. Track unknown suppliers separately from the intended existing-supplier population.

Within the pre-test period use earlier-to-later development splits with the same label-availability rule. Fit preprocessing and each candidate only on that fold's training data. Compare the training-mean baseline with the page predictor and predeclared penalty grid. Choose using development MSE, report MAE and severe underestimation, then freeze all choices. If refitting on development data, evaluate the actual refit on the untouched final period. Record failed/missing predictions and delayed labels under declared rules rather than dropping them.

For new suppliers with unseen templates, reserve entire disconnected organization/template components, keeping every document's revisions together. The development procedure must use analogous component holdouts. Add a time cutoff if future deployment is also part of the claim. Confirm enough separate components exist; this toy dataset fails that feasibility check. Report both case-weighted and, if relevant, organization-weighted outcomes with explicit denominators. More rows from one organization do not supply more independent organizations.

**Criterion:** Decision-time inputs, label maturity, group/time boundaries, training-only transformations, baseline and final lock. There is no compulsory 80/20 split: the number and representativeness of independent groups matter.

## 6. Workload change and the decision

Let r be routine share. P's loss is r+9(1−r)=9−8r; Q's is 4. P wins for r>5/8, ties at 5/8 and loses below it. At r=0.9 its MSE is 1.8; at r=0.5 it is 5.

Reweighting assumes unchanged subgroup losses. If reviewer tooling changes minutes per page within routine cases, the old conditional MSEs may no longer apply. Newly matured labels showing that within-group change would invalidate simple reweighting. Input drift without outcomes is an alert to investigate, not a measured error increase.

Better minute predictions do not by themselves prove better schedules. Queue policies, reviewer behavior and opportunity costs intervene. A controlled workflow evaluation using F03's unit, outcome and interference discipline is needed for a causal benefit claim.

**Criterion:** Correct threshold, a concrete failed assumption and separation of predictive quality from customer impact.

## Executed checks

The following uses Python's standard library. It checks the constructed arithmetic, the memorization counterexample, component feasibility and a metamorphic independence check: changing final labels cannot change selection that consumes only training/validation data. It does not estimate sampling uncertainty or validate a production data pipeline.

```python
from fractions import Fraction as F
from itertools import product

train = [(1,2),(2,4)]
valid = [(1,1),(2,2)]
test = [(3,3),(4,4)]
def mse(data, predict):
    return sum((predict(x)-y)**2 for x,y in data)/F(len(data))
def mae(data, predict):
    return sum(abs(predict(x)-y) for x,y in data)/F(len(data))
mean = sum(F(y) for x,y in train)/len(train)
assert mean == 3
assert (mse(train,lambda x:mean),mse(valid,lambda x:mean)) == (1,F(5,2))
lambdas = [F(0), F(5,2), F(15,2)]
weights = [F(10)/(5+2*l) for l in lambdas]
assert weights == [2,1,F(1,2)]
assert [mse(train,lambda x,w=w:w*x) for w in weights] == [0,F(5,2),F(45,8)]
assert [mse(valid,lambda x,w=w:w*x) for w in weights] == [F(5,2),0,F(5,8)]
for l,w in zip(lambdas,weights):
    assert 5*(w-2)+2*l*w == 0
    for d in [F(-1),F(-1,10),F(1,10),F(1)]:
        objective=lambda z:mse(train,lambda x:z*x)+l*z*z
        assert objective(w+d)>objective(w)
def select(validation):
    return min(weights,key=lambda w:mse(validation,lambda x:w*x))
w=select(valid)
assert w==1 and mse(test,lambda x:w*x)==mae(test,lambda x:w*x)==0
assert mse(test,lambda x:mean)==mae(test,lambda x:mean)==F(1,2)
changed=[(3,6),(4,8)]
assert mse(changed,lambda x:w*x)==F(25,2)
assert mae(changed,lambda x:w*x)==F(7,2)
# Final labels never enter selection, even under 25 alternate target pairs.
for y1,y2 in product(range(5),repeat=2):
    alternate_test=[(3,y1),(4,y2)]
    assert select(valid)==w

# doc, organization, template, revision, target; fixed two-page inputs.
docs=[('D1','A','X',2),('D2','A','Y',4),('D3','B','X',6),('D4','B','Z',8)]
rows=[(d,o,t,r,F(y)) for d,o,t,y in docs for r in [1,2]]
def lookup_mse(tr,va):
    memory={r[0]:r[4] for r in tr}
    fallback=sum(r[4] for r in tr)/len(tr)
    return sum((memory.get(r[0],fallback)-r[4])**2 for r in va)/len(va)
assert lookup_mse([r for r in rows if r[3]==1],[r for r in rows if r[3]==2])==0
tr=[r for r in rows if r[1]=='A'];va=[r for r in rows if r[1]=='B']
assert lookup_mse(tr,va)==17
assert not {r[0] for r in tr}&{r[0] for r in va}
assert not {r[1] for r in tr}&{r[1] for r in va}
assert {r[2] for r in tr}&{r[2] for r in va}=={'X'}
# Enumerate all 14 nonempty document partitions: none separates both axes.
feasible=[]
for mask in range(1,15):
    left=[d for i,d in enumerate(docs) if mask>>i&1]
    right=[d for i,d in enumerate(docs) if not mask>>i&1]
    if all(not {d[k] for d in left}&{d[k] for d in right} for k in [1,2]):
        feasible.append(mask)
assert feasible==[]
for r,expected in [(F(9,10),F(9,5)),(F(1,2),F(5)),(F(5,8),F(4))]:
    assert r+9*(1-r)==expected
print('PASS: fitting, penalties, validation/test arithmetic, 25 label changes,')
print('revision leakage, grouped MSE, all 14 group partitions and mixture threshold.')
```

## Revision history

- 1.0 — 2026-11-09. Six reference answers and executed exact checks; no learner performance inferred.

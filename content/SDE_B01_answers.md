# B01 — Hints, worked answers, and assessment criteria

| Field | Value |
| --- | --- |
| ID / revision | B01 answers / 1.0 |
| Date | 2026-11-02 |
| Prerequisites | [B01 core pack](SDE_B01.md) |
| Capability developed | Judge whether an evidence plan can change a concrete build decision |
| Source-check status | R19 locators in core §10; answers are original teaching examples |
| Experiment status | Arithmetic assertions executed; no customer or market experiment conducted |

All organizations, offers, inputs, and outcomes below are hypothetical. These are worked possibilities, not the learner's answers or results from research participants.

## Hints

1. A role is not necessarily a different person. Name who feels the problem and who can change the process.
2. One hypothesis should concern the existing problem; the other should concern behavior toward an offer.
3. Ask for a reconstruction, not a rating of your idea. Include an opportunity to say the existing process works.
4. Convert minutes to hours before multiplying by an hourly value. Include review and onboarding.
5. Identify whose behavior changed, what it cost them, and what terms they accepted.
6. A gate authorizes the next bounded investment. It does not certify an entire market.

## 1. Scope and roles

A useful example segment is purchasing teams receiving 100–200 supplier invoices weekly and manually matching them to delivery evidence. The trigger is invoice receipt. The operator is the matching clerk; the intended outcome is an evidence-complete case ready for a correct approval decision. The assumed buyer is the manager responsible for that budget, but this role must be verified. A separate data or systems approver may exist; it is unknown here.

The current alternative combines documents, a spreadsheet, and employee judgment. It must be evaluated as a complete process, including exceptions. “Uses a spreadsheet” does not establish dissatisfaction or a business opportunity. An internal tool variant would replace a purchase hypothesis with a commitment of staff time and workflow ownership.

## 2. Two hypotheses and adverse evidence

Problem hypothesis: In the defined segment, assembling matching evidence creates material active workload or consequential delays. Evidence against it includes several relevant recent cases showing quick matching, low recurrence, or a different dominant delay. A participant who has not encountered an exception recently is useful negative evidence, provided their workload belongs to the chosen segment.

Adoption hypothesis: An authorized team will allocate permitted cases, a reviewer, and a dated trial if assistance preserves source traceability and approval. Adverse evidence includes refusal after the concrete terms are explained, inability to obtain necessary permissions, or higher-priority work repeatedly displacing the trial. Diagnose reasons before generalizing. Lack of authority in the interviewed person is a recruitment problem as well as a limit on their commitment.

Neither hypothesis requires pretending that five conversations yield a population estimate. The bounded batch is a practical investigation design. A later decision to estimate prevalence needs a sampling plan, addressed in F03.

## 3. Six sample questions

1. Reconstruct the last invoice requiring extra checking from receipt to resolution.
2. Which steps needed active work and which involved waiting? What record could help check the distinction?
3. What consequence followed, and what would have happened under the normal process?
4. Over the last defined working week, which cases needed this work and which did not?
5. What did the team change previously, and what remains useful about that approach?
6. For the most recent workflow tool adopted, who approved spending and data access, and what did adoption require?

These questions can reveal a mistaken premise. “How much would you pay for our AI that saves hours?” embeds both a benefit and a preferred solution. Rewrite it around actual work before discussing a real offer on explicit terms.

## 4. Arithmetic and interpretation

| Quantity | 8-minute baseline | 4-minute baseline |
| --- | ---: | ---: |
| Current work, 120 invoices/week | 16 h/week | 8 h/week |
| Proposed review: 120 × 3 / 60 | 6 h/week | 6 h/week |
| Proposed recurring overhead | 2 h/week | 2 h/week |
| Recurring capacity released | 8 h/week | 0 h/week |
| Onboarding: 12 h / 8 weeks | 1.5 h/week | 1.5 h/week |
| Net released capacity during assessment | 6.5 h/week | −1.5 h/week |
| Assigned value at ₹300/h, before fees | ₹1,950/week | −₹450/week |

The original baseline's assigned labor value is 16×₹300=₹4,800/week. Before onboarding, the potential released capacity is valued at 8×₹300=₹2,400/week. These are conditional arithmetic results.

If salaried hours cannot be reduced or usefully reassigned, released time may not reduce cash expenditure. If work quality falls or extra reviews appear, the model is incomplete. Even a correct capacity estimate does not reveal an authorized budget or accepted price. Compare the same outcome quality and count each work category once. The eight-week horizon is an assumed evaluation convention, not a prediction of a sales cycle.

## 5. Interpret the signals

| Fictional signal | What it supports | What remains unknown |
| --- | --- | --- |
| Developer praises demo | Appeal to that developer | Target user's pain, buyer's authority, adoption |
| Clerk estimates weekly burden | Reported problem magnitude from one perspective | Accuracy, recurrence, alternatives, budget |
| Sponsor schedules trial with resources | Specific intent to test on those terms | Actual execution, outcome improvement, renewal |
| Payment for custom integration | Demand for that scoped transaction | Repeatable product demand and delivery margin |
| Repeated manager-mandated use | Compliance or workflow dependence | Voluntary preference, net benefit, willingness to renew |

A signal can be genuine and still answer the wrong question. Preserve the terms, roles, and context. Do not transform these fictional examples into measured customer evidence.

## 6. Decision gates and changed constraint

Proceed to trial design if two independent organizations supply relevant recent episodes and one authorized sponsor agrees to a bounded trial with cases, reviewer, date, and success criterion. This is the exercise's proposed gate, not a proven universal threshold. Before execution, define how complete correct cases, active work, and exceptions will be checked against the current process.

Revise if evidence identifies a different bottleneck or if the interested operator lacks the required approval route. Stop or defer this particular investment if repeated relevant evidence indicates little consequence, adequate existing alternatives, or no feasible adoption path within the chosen constraints. Record the investigation limit so a later change can justify revisiting it.

With the new finding that missing delivery records create two-day delays, fast extraction does not itself provide the absent information. Investigate where records originate, who can obtain them, and why retrieval stalls. A follow-up plan could observe one missing-record episode and compare it with a routine case. Do not immediately commit to a reminder agent: the cause could instead be a supplier process, access restriction, or incomplete shipment. Reassess the problem before selecting a mechanism.

## Assessment criteria

| Dimension | A useful answer demonstrates |
| --- | --- |
| Specificity | Segment, workflow, roles, alternative, and consequential outcome |
| Falsifiability | Adverse evidence for both problem and adoption claims |
| Interview design | Recent episodes, neutral framing, and an approval-path question |
| Evidence discipline | Separates account, measurement, inference, and hypothetical inputs |
| Decision quality | Bounded next step with explicit revise/stop conditions |
| Transfer | Changes the plan when the bottleneck or authority changes |

Different coherent plans can satisfy these criteria. No learner score or mastery state has been recorded.

## Executed arithmetic check

```python
from fractions import Fraction
n, review_minutes, overhead, hourly = 120, 3, 2, 300
onboarding = Fraction(12, 8)
new_hours = Fraction(n * review_minutes, 60) + overhead
assert new_hours == 8 and onboarding == Fraction(3, 2)
for old_minutes, hours, recurring, net, value in [
    (8, 16, 8, Fraction(13, 2), 1950),
    (4, 8, 0, Fraction(-3, 2), -450),
]:
    baseline = Fraction(n * old_minutes, 60)
    assert baseline == hours
    assert baseline - new_hours == recurring
    assert baseline - new_hours - onboarding == net
    assert net * hourly == value
assert 16 * hourly == 4800
assert 8 * hourly == 2400
print('PASS: two scenarios, units, onboarding allocation, and value arithmetic')
```

The checks validate calculations from assigned inputs, not the inputs themselves. Editorial checks matched all six exercise prompts to worked answers, reviewed claim scope and timestamp locators, and verified that no interviews, outreach, trial outcomes, or demand measurements were claimed. Audit A remains pending.

# SDE Foundations — Reference Cards

Use this page for recall. Open the linked note for derivations, counterexamples and sources.

## Foundations

| Module | Question | Recall cue |
| --- | --- | --- |
| [[SDE_F01|F01]] | Is the algorithm correct and under what model? | Invariant → progress → termination → cost → counterexample |
| [[SDE_F02|F02]] | What should we do under uncertainty? | Denominator → conditional probability → consequence → expected loss |
| [[SDE_F03|F03]] | Did the system improve or the measurement change? | Population → unit → assignment → missing outcomes → uncertainty |
| [[SDE_F04|F04]] | What computation sits underneath learning? | Shape → transformation → loss → derivative → held-out check |

## Systems

| Module | Question | Recall cue |
| --- | --- | --- |
| [[SDE_S01|S01]] | Why do equivalent algorithms cost differently? | Operations, bytes, locality, working set and abstraction boundary |
| [[SDE_S02|S02]] | How do we preserve trustworthy history? | Immutable revision → complete manifest → atomic head → recovery |
| [[SDE_S03|S03]] | How do concurrent valid actions violate a global rule? | Read set → write set → serialization → epoch/revision → receipt |
| [[SDE_S04|S04]] | What survives failures and partitions? | Quorum intersection → log freshness → commit rule → client result |
| [[SDE_S05|S05]] | What happens when demand meets finite capacity? | Offered load → queue → admission → startup → fan-out dependence |
| [[SDE_S06|S06]] | Where do reliability and authority meet? | Principal → grant → object/action → decision boundary → SLI |

## AI systems

| Module | Question | Recall cue |
| --- | --- | --- |
| [[SDE_A01|A01]] | Will the learned behavior generalize? | Deployment unit → leakage groups → tune/test boundary → shift |
| [[SDE_A02|A02]] | What does attention compute? | Projections → scaled scores → mask → softmax → weighted values |
| [[SDE_A03|A03]] | Is the answer supported by current permitted evidence? | Corpus → eligibility → retrieval → context → claim → disclosure |
| [[SDE_A04|A04]] | What limits inference serving? | Weights + KV + workspace; prefill/decode; schedule and deadline |
| [[SDE_A05|A05]] | How should an agent be evaluated and bounded? | Complete contract → baselines → action envelope → retries → judges |

## Technology business

| Module | Question | Recall cue |
| --- | --- | --- |
| [[SDE_B01|B01]] | Is there a recurring problem and authorized commitment? | Segment → episode → current workaround → cost → owner → commitment |
| [[SDE_B02|B02]] | Does each useful outcome fund its work? | Case → success → non-overlapping cost → contribution → sensitivity |
| [[SDE_B03|B03]] | Can customers find, adopt and keep the offer? | Acquisition → activation → repeat → boundary → bundle → moat test |

## Synthesis decisions

| Module | Decision | Key boundary |
| --- | --- | --- |
| [[SDE_C01|C01]] | Where must duplicate-effect prevention live? | At the authoritative effect boundary, with stable identity |
| [[SDE_C02|C02]] | Does better model quality improve customer outcome? | Component score versus complete timely supported result |
| [[SDE_C03|C03]] | Which optimization buys useful capacity? | Resource feasibility, same workload, deadline and full cost |
| [[SDE_C04|C04]] | Which product boundary is viable? | Customer feasibility plus supplier sustainability and authority |
| [[SDE_C05|C05]] | How far should autonomy go? | Least complex adequate choice under external authority |
| [[SDE_C06|C06]] | How should architecture respond to supplier change? | Own evidence/control, port evaluation, retest complete behavior |

## Five boundary checks

1. What is the denominator?
2. Where does the protected transition commit?
3. Which identity survives retries and revisions?
4. Which work or failure was excluded from the clock or cost?
5. What evidence would reverse the decision?


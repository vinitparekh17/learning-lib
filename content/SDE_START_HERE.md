# SDE Foundations — Start Here

This vault is a decision-making curriculum for a software engineer. Its recurring question is:

> How do I turn an uncertain problem into a system whose behavior, reliability, and economics I can defend?

The library is complete as an authored and audited collection. That does **not** mean you have completed it as a learner. Use this page as the home screen; the index tracks artifacts, while your own learning belongs in [[STUDY_PROGRESS]].

## The easiest way to use this vault

1. Install Obsidian on your computer or iPhone.
2. Extract the vault archive.
3. Open the extracted `SDE_Foundations_Vault` folder as a vault.
4. Pin this note and [[STUDY_PROGRESS]].
5. Read one core note, attempt its exercises without opening the answer note, then compare with the companion.

No community plugins are required. Search, backlinks, graph view, math and Mermaid work with Obsidian's built-in features. If you sync through iCloud, keep the whole folder inside the Obsidian iCloud directory. Avoid opening the same vault through two sync systems at once.

## Recommended route: high ROI first

This route emphasizes reasoning you can transfer immediately to backend work, cloud systems and AI-assisted engineering.

| Stage | Read | What it changes |
| --- | --- | --- |
| 1. Define the decision | [[SDE_F01|F01]], [[SDE_F02|F02]], [[SDE_F03|F03]] | Invariants, expected loss, denominators and fair comparisons |
| 2. Defend state changes | [[SDE_S02|S02]], [[SDE_S03|S03]], [[SDE_S04|S04]] | Durable identity, concurrency, ordering and replication |
| 3. Defend operations | [[SDE_S05|S05]], [[SDE_S06|S06]] | Queues, overload, permission, revocation and SLO boundaries |
| 4. Use AI with evidence | [[SDE_A01|A01]], [[SDE_A03|A03]], [[SDE_A05|A05]] | Generalization, retrieval/provenance and bounded autonomy |
| 5. Price the complete outcome | [[SDE_B01|B01]], [[SDE_B02|B02]], [[SDE_B03|B03]] | Customer evidence, cost per useful result and product boundaries |
| 6. Integrate judgment | [[SDE_C01|C01]], [[SDE_C03|C03]], [[SDE_C05|C05]], [[SDE_C06|C06]] | Effects, capacity, autonomy and supplier-change decisions |

Read [[SDE_CONSOLIDATED_NOTES]] before starting and revisit it after every stage. Use [[SDE_REFERENCE_CARDS]] when you need a quick refresher.

## Full curriculum route

The full route preserves prerequisites:

1. Foundations: [[SDE_F01|F01]] → [[SDE_F02|F02]] → [[SDE_F03|F03]] → [[SDE_F04|F04]]
2. Systems: [[SDE_S01|S01]] → [[SDE_S02|S02]] → [[SDE_S03|S03]] → [[SDE_S04|S04]] → [[SDE_S05|S05]] → [[SDE_S06|S06]]
3. AI systems: [[SDE_A01|A01]] → [[SDE_A02|A02]] → [[SDE_A03|A03]] → [[SDE_A04|A04]] → [[SDE_A05|A05]]
4. Technology business: [[SDE_B01|B01]] → [[SDE_B02|B02]] → [[SDE_B03|B03]]
5. Synthesis: [[SDE_C01|C01]] → [[SDE_C02|C02]] → [[SDE_C03|C03]] → [[SDE_C04|C04]] → [[SDE_C05|C05]] → [[SDE_C06|C06]]

The sequence is a dependency order, not a daily quota. Pause to build a prerequisite bridge when an exercise exposes a gap. The answer notes are indexed in [[SDE_SOLUTIONS_INDEX]].

## Topic routes

### Cloud and distributed systems

Read [[SDE_F01|F01]], [[SDE_S01|S01]], [[SDE_S02|S02]], [[SDE_S03|S03]], [[SDE_S04|S04]], [[SDE_S05|S05]], [[SDE_S06|S06]], then [[SDE_C01|C01]] and [[SDE_C03|C03]].

### AI engineering and LLM judgment

Read [[SDE_F02|F02]], [[SDE_F03|F03]], [[SDE_F04|F04]], [[SDE_A01|A01]], [[SDE_A02|A02]], [[SDE_A03|A03]], [[SDE_A04|A04]], [[SDE_A05|A05]], then [[SDE_C02|C02]], [[SDE_C05|C05]] and [[SDE_C06|C06]].

### Gujarati-business-meets-engineering route

Read [[SDE_B01|B01]], [[SDE_F02|F02]], [[SDE_F03|F03]], [[SDE_B02|B02]], [[SDE_B03|B03]], then [[SDE_C02|C02]], [[SDE_C04|C04]] and [[SDE_C06|C06]]. The emphasis is on evidence, unit economics and responsibility boundaries rather than startup folklore.

## A study session that produces action

Use a 45–60 minute block:

- 5 minutes: write the decision the note is supposed to improve.
- 20–25 minutes: read the mechanism and trace the worked example by hand.
- 10–15 minutes: attempt one exercise without the answer.
- 5 minutes: compare with the companion and identify the first incorrect assumption.
- 5 minutes: write one transfer to your work or project in [[STUDY_PROGRESS]].

If you only have 15 minutes, read one section and write a single “boundary statement”: what the result assumes, what it proves and what it cannot prove.

## How to judge your own progress

Do not mark a topic learned because the prose feels familiar. Use four levels:

1. **Recognize** — explain the vocabulary.
2. **Reproduce** — rebuild the trace or calculation without looking.
3. **Transfer** — apply it to a different system and state changed assumptions.
4. **Defend** — name the counterexample and evidence that would reverse your decision.

The library records no learner answers. Your progress file starts blank by design.

## Library map

- [[SDE_CONSOLIDATED_NOTES]] — the cross-cutting mental model.
- [[SDE_REFERENCE_CARDS]] — compact module reminders.
- [[SDE_SOLUTIONS_INDEX]] — all companion answer notes.
- [[SDE_OPEN_QUESTIONS]] — real inputs the fictional examples cannot settle.
- [[SDE_Foundations_Complete]] — one continuous reading export without worked solutions.
- [[SDE_Foundations_Solutions]] — the separate consolidated solution export.
- [[SDE_SOURCES]] — source identities, passage checks and limitations.
- [[SDE_INDEX]] — production history, dependencies, revisions and stable Library links.
- [[SDE_Audit_A|Audit A]], [[SDE_Audit_B|Audit B]], [[SDE_Audit_C|Audit C]], [[SDE_Audit_D|Audit D]] — what was checked and repaired.

The individual notes remain the canonical study units because they keep exercises, sources and revisions close to the topic.


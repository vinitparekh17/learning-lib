# Scheduled task prompt: Build the SDE Foundations Library

Use the following as the task's instructions. Make `SDE_Foundations_Library_v1.md` accessible to the scheduled task. Set the cadence, end date, and model in the task configuration separately. This document does not create a schedule.

---

Act as my research engineer, technical editor, and curriculum architect. Build a durable Markdown knowledge library that I can study later at my own pace.

## Mission and curriculum

Develop my transferable reasoning and engineering judgment across mathematical foundations, software systems, cloud, AI, and technology business. I am an SDE with roughly two years of experience. Do not organize the curriculum around my current languages, frameworks, employer, or certifications. Explain prerequisites rather than assuming mathematical fluency.

Use `SDE_Foundations_Library_v1.md` as the curriculum authority. Its Library reference is `libfile_5d05587b7cd481918fb66c263ba6df00`. Read the actual file, especially the module briefs, source catalog, and 30-run plan. Treat its source list as a researched starting point, not as proof that every paper has already been fully read or every claim verified.

The central question is: How do I turn an uncertain problem into a system whose behavior, reliability, and economics I can defend?

## Resume and choose the work

At the start of every run, read the curriculum, `SDE_INDEX.md`, and the relevant existing artifacts. Rely on saved files, not assumed chat memory or a persistent scratch directory.

On the first run, initialize the index and source register from the curriculum. Include the planned run sequence, module dependencies, and diagnostic questions; no learner response is required to proceed. When readiness is unknown, include optional prerequisite bridges. Never invent my diagnostic answers or learning progress.

On subsequent runs, complete the next unfinished work item in this sequence:

01 Map/index; 02 F01; 03 B01; 04 F02; 05 F03; 06 S01; 07 Audit A; 08 F04; 09 S02; 10 S03; 11 S04; 12 S05; 13 C01; 14 S06; 15 Audit B; 16 A01; 17 A02; 18 A03; 19 A04; 20 A05; 21 C02; 22 Audit C; 23 B02; 24 B03; 25 C03; 26 C04; 27 C05; 28 C06; 29 Audit D; 30 Final packaging.

Repair a blocking error or missing prerequisite before advancing. Reuse existing completed work. If saving was interrupted, reconcile existing artifacts before creating duplicates. If essential input is inaccessible, report the specific block; do not replace the agreed curriculum with an invented one.

Complete one substantial work item per execution. A difficult item may continue across executions: save a clear checkpoint, identify what remains, and resume it next time. Do not silently truncate a lesson or claim the whole sequence is finished because 30 executions have elapsed.

## Research and evidence

Open and inspect primary sources: original papers, author textbooks, university material, first-party documentation, and original incident reports. Use a few strong sources per topic, adding others only when they resolve a meaningful question or contradiction.

For consequential factual claims, provide a supporting URL and precise section, page, theorem, figure, or other verified locator. Distinguish sourced facts, derived results, hypothetical inputs, measured results, practitioner judgment, and unresolved claims. Keep empirical findings within their reported workload, population, and experimental conditions. Verify current details when a claim depends on present implementations.

An abstract is insufficient evidence for detailed experimental claims. When access fails, seek an accessible primary alternative or mark the limitation. Historical papers teach mechanisms; their prices and benchmark results are not current forecasts. Business anecdotes are not proof of demand.

Show premises for derivations and label invented example numbers. Check arithmetic and consequential technical claims. Accurately distinguish executed experiments from untested code. Write original synthesis and link to source material; respect access and reproduction rights.

## Structured outputs with teaching freedom

Use stable filenames:

- `SDE_INDEX.md`: curriculum progress, artifact links/IDs, dependencies, revisions, and next action.
- `SDE_SOURCES.md`: source register and access/verification status.
- `SDE_<MODULE_ID>.md`: each core pack or synthesis assignment.
- `SDE_<MODULE_ID>_answers.md`: hints, worked answers, and assessment criteria where applicable.
- `SDE_Audit_<A|B|C|D>.md`: audit findings and corrections.
- `SDE_START_HERE.md`: final reading routes and handoff.

Each pack begins with a compact metadata table: ID, title, revision, date, prerequisites, capability developed, source-check status, and experiment status. Keep detailed claim provenance in an evidence table, not repetitive labels on every sentence.

For a core pack, cover:

1. The question and decision this knowledge enables, with a short orientation and prerequisite bridge.
2. A substantial explanation of the mechanism, using a worked example, derivation, or execution trace.
3. Assumptions, invariants where applicable, failure conditions, and a counterexample.
4. Meaningful trade-offs and the evidence that would change the choice.
5. Connections to earlier concepts and later applications.
6. A bounded exercise plus application questions, with separate hints and worked answers.
7. A compact reference card, supporting sources, and unresolved questions.

You may reorder, combine, or rename sections and choose prose, equations, tables, pseudocode, or Mermaid diagrams. Use byte-level detail when it explains the mechanism; use mathematical, system, or economic models when those are more appropriate. Add a small prerequisite appendix if necessary. State a significant scope adjustment and its reason in the index. Keep the overall curriculum intact.

Make the core independently understandable. Aim roughly for 1,500–2,500 words when justified, with no minimum and no padding. Put optional depth in an appendix. Avoid compressing several difficult ideas into an impressive but unexplained survey. An actual production incident or comparison of several engines is optional, never a quota.

For synthesis items, use a decision memo suited to the assigned question. Combine the specified earlier modules, compare credible options under the same assumptions, defend a choice, and revise it after a constraint changes. Include a separate worked analysis for later self-assessment.

## Audit and continuity

On audit runs, inspect the relevant original passages, recheck derivations, and examine counterexamples. Look for unsupported precision, mixed versions, missing prerequisites, misleading benchmarks, inconsistent terminology, and mismatches between exercises and answers. Record the original issue, evidence, correction, affected artifacts, and remaining uncertainty. Apply supported corrections to the existing files while preserving their identities and revision history. A second model pass is not independent validation.

Track artifact states as `queued`, `in_progress`, `produced`, `audited`, or `needs_revision`. These describe the files, not my mastery. Preserve useful open questions without treating every minor uncertainty as a blocker. Repair consequential errors before dependent material uses them.

Save outputs in durable storage available to future runs, then update the index with actual artifact links or identifiers. Preserve existing files and avoid overwriting unrelated work. Mark an item produced only after the required files are successfully saved. If durable saving is unavailable, report it and retain the completed draft where possible; do not claim persistence.

## Completion and run report

After the planned work and blocking repairs are complete, produce `SDE_START_HERE.md`, verify the index and answer links, and provide a downloadable archive or consolidated Markdown export if supported. Mark the program complete. Future triggers should report completion without generating filler or restarting the curriculum. Disable the task only if that capability is available and authorized by its setup.

End every run with a short report: item completed or checkpointed; saved file links; checks performed; material uncertainties or blocks; and the next item. Produce the actual Markdown files, not only a plan or a chat essay.

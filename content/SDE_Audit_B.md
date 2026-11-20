# Audit B — Systems traces, failure assumptions and continuity

| Field | Value |
| --- | --- |
| ID / revision / date | Audit B · 1.0 · 2026-11-08 |
| Scope | S01–S06 and C01, including all seven answer companions |
| Authority | SDE_Foundations_Library_v1.md, Run 15; SDE_Foundations_Scheduled_Prompt.md |
| Basis | Latest saved artifacts, targeted primary passages, manual trace review and rerun embedded Python checks |
| Result | One test-coverage wording correction in S04 answers; no remaining blocking finding in this scope |
| Experiment status | Seven existing check blocks executed in separate Python processes; corrected S04 block rerun. No live hardware, distributed-system, provider or security test |
| Learner status | Unknown; artifact audit does not establish learner readiness or mastery |

## Decision and scope

The systems sequence is internally consistent within its declared models after correcting one coverage description. Continue to A01 once the corrected companion, this report and source register have saved successfully and the index records them. Preserve the existing S04 answer identity; do not regenerate the seven core packs.

The review follows the curriculum's Run 15 focus: execution traces, failure assumptions and cross-links. It reuses Audit A's S01 rate-bound clarification and checks that later lessons do not turn modeled resource counts into hardware speed claims. It examines 14 core/companion files, 41 exercise-to-answer mappings and selected original passages. It is a targeted technical audit, not an exhaustive rereading of every source or an independent implementation certification. F04 is not newly audited here: none of these systems conclusions requires its matrix or gradient derivations. Its recorded availability remains relevant to the next A01 item.

The latest index selected Audit B. Exact-title lookup and a shorter-name search found no existing Audit B report to reconcile; the latter returned other program artifacts, not an Audit B identity. Previously completed work was reused.

## B-01 — Synthetic predicate inputs were described too strongly

**Original issue.** SDE_S04_answers.md revision 1.0 labeled its loop as exhausting truthful match-index combinations. The loop applies two term values and 27 index triples to the same six-entry log. That log contains a term-3 entry even when the supplied current term is 2. Some inputs therefore cannot be a valid Raft leader state. The assertions also check output conditions of one helper, not the reachability of inputs or the protocol's state transitions.

**Evidence.** The actual loop is `term in (2,3)` and `product(range(4,7), repeat=3)`, giving 54 synthetic cases. R07 Figure 2, p. 4, specifies monotonic current terms and the leader commitment condition; §§5.1 and 5.4 explain their protocol context. This distinguishes an algebraic input sweep from legal distributed histories.

**Correction.** Revised the comment, introductory test boundary and closing explanation to identify synthetic cases, explicitly include unreachable states and limit the claim to the commitment predicate's output conditions. The condition still requires trustworthy durable acknowledgements when used as a real commitment decision; the helper does not establish them. Added revision history and changed only this companion to revision 1.1. Executable assertions and all six exercise answers are unchanged, so S04 core revision 1.0 remains compatible.

**Check.** Extracted the corrected block again and executed it successfully. Its 109 quorum pairs, log operations, predicate checks and receipt checks still pass. This correction changes what the test demonstrates, not a numerical result. No claim of complete Raft simulation is justified.

## Results by pack

| Pack | Mechanism, counterexample and boundary reviewed | Executed result |
| --- | --- | --- |
| S01 | Line/page counting, working-set retention, address translation and batching. The two-line cache defeats “second pass means hits.” Audit A's rate bounds remain explicit; a miss count is not elapsed time. | Array/packed/scattered first-pass fills: 64/128/256 bytes; second-pass behavior, traversal, translation to 456 and batch/deadline checks passed. |
| S02 | Immutable evidence versus current head, scan/index page accounting and atomic publication. Premature home-page installation defeats the stated NO-STEAL recovery model. Retaining a reference alone does not retain source bytes. | SQLite query/publication results, page counts, three uncommitted prefixes, four committed home-write combinations and repeated recovery passed. No real disk crash was injected. |
| S03 | Read dependencies, write skew, guard duration, epoch versus revision, receipts and clock direction. Disjoint writes can violate capacity; a revision-only guard cannot distinguish reopening. | All 20 modeled snapshot histories: 18 violate capacity, two serial orders preserve it. Two guarded orders and 24 reopen/request orders preserve the invariant. Payload, replay and clock checks passed. |
| S04 | Quorum overlap plus election/log rules, local append versus commitment versus reply, current-term restriction, suffix repair and historical receipt replay. A majority count alone is not the protocol. | 109 quorum pairs, freshness and append/repair examples, 54 synthetic predicate inputs and receipt cases passed. Coverage description corrected by B-01. |
| S05 | Same offered workload/deadline across policies, exact-cost admission premise, startup, busy versus purchased capacity, and percentile population. Underestimated cost and correlated fan-out invalidate stronger interpretations. | FIFO and six reorderings, admission failure, batching, two worker traces, five startup cases, fluid conservation and capacity thresholds passed. Fan-out calculation gives 0.332392 under independence. |
| C01 | Approval uniqueness versus provider effect, stable payload-bound identities, durable intent, restoration and retention. Marker-before-call can lose an effect; marker-after-call can duplicate it. Unknown external outcomes cannot be resolved by more local replicas. | Three competing delivery orders, stale/payload cases, historical replay, five crash cuts, provider repeats, identity expiry and indistinguishable local histories passed. Provider behavior remains an assumed contract. |
| S06 | Current authority at commit, historical receipt access, revocation ordering, useful-outcome denominator and resource versus privilege isolation. Cached permission can violate the chosen revocation rule; a correct authorization predicate does not establish trustworthy inputs. | 256 Boolean cases, both revocation orders, stale-cache counterexample, SLI/budget/union/CPU arithmetic and shared/reserved worker traces passed. |

Every original reproduction block exited with code 0 and empty stderr in a separate process. The S04 rerun after the comment/prose repair also exited 0. These are bounded checks of constructed examples. The proposed hardware benchmark in S01, workload replay in S05 and live failure-injection plans in S06 were not performed.

## Cross-pack contracts and teaching continuity

The same invoice case evolves without silently merging distinct identities. Evidence revision identifies data; approval epoch identifies a business round; request key identifies one caller intent; payment identity identifies the provider effect; leadership term identifies protocol leadership. None substitutes for all the others. Historical acceptance is not current approval state, and reopening does not undo a payment already sent.

S02's recovery example assumes a complete ordered durable log prefix and NO-STEAL. S03 adds indivisible guarded decisions; S04 adds replicated-log assumptions; C01 adds a separate external authority. These are successive premises, not evidence that the previous toy model implements the next layer. S06 makes authorization and current permission for receipt disclosure explicit. The audit found no claim that consensus or a database rollback alone controls the provider's effect.

Receipt policies differ in a documented way: S04's example remembers command results, including rejection, while C01's receipt-first rule concerns previously accepted requests. Their shared guarantee is that replay of an accepted identity cannot create another accepted effect. Do not infer a universal rejected-request caching policy from either example; a deployed API must specify it.

Resource terminology is likewise consistent. S01 separates requested bytes from transfer bytes and throughput from task latency. S05 separates service from response time, offered outcomes from completed-only fractions, and busy work from paid capacity. S06 keeps the request-count error budget distinct from time availability and from authority invariants. The S05 and S06 workloads differ deliberately; their numbers are not benchmark comparisons between modules.

The worked answers match all 41 numbered tasks: six each in S01–S06 and five in C01. Manual review checked the changed-constraint responses and counterexamples, not only numbering. Companion filenames resolve in both directions; Markdown code fences balance. The 14 file identities match the index entries used to retrieve them. Relative companion links require the files to remain together in an offline export; native file links in the index provide individual access.

## Primary passages inspected for this audit

Page numbers below are PDF/printed page numbers as specified, not browser line numbers. These targeted checks supplement prior passage records without claiming every prior source was refreshed.

| Source | URL and exact locator | Audit use |
| --- | --- | --- |
| R04, OSTEP | [Chapter 19](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf), §19.1, Figure 19.1, chapter-local pp. 1–2 | Translation-cache lookup and page-table fallback; distinguishes translation state from application data. |
| R05, CMU Fall 2025 | [Lecture 21](https://15445.courses.cs.cmu.edu/fall2025/notes/21-logging.pdf), §2 pp. 1–2 and §6 pp. 4–5 | Buffer policies, log ordering and commit acknowledgement boundary for S02. |
| R05, same course | [Lecture 20](https://15445.courses.cs.cmu.edu/fall2025/notes/20-multiversioning.pdf), §1 pp. 1–2 | Snapshot isolation and write skew; MVCC alone is not a serializability claim. |
| R06, Lamport 1978 | [Author PDF](https://lamport.azurewebsites.net/pubs/time-clocks.pdf), printed p. 560, Logical Clocks and Clock Condition | Causal precedence implies increasing clocks; ordered clock values alone do not establish causality. |
| R07, extended May 2014 paper | [Primary PDF](https://raft.github.io/raft.pdf), Figure 2 p. 4; §5.4.1–5.4.2 pp. 8–9; §8 p. 13 | Election/log and current-term rules, B-01 coverage distinction, client retry identities and authoritative-read precautions. |
| R09, Google SRE | [Chapter 22](https://sre.google/sre-book/addressing-cascading-failures/), Queue Management and Load Shedding and Graceful Degradation | Backlog costs, burst-dependent choices and useful-work objective; no queue-size recommendation transferred. |
| R09, same book | [Chapter 3](https://sre.google/sre-book/embracing-risk/), Forming Your Error Budget and Benefits | Risk/release framework; S06's target and numbers remain original examples. |
| R10, Saltzer, Reed and Clark | [Author copy](https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf), p. 2 principle and p. 6 Duplicate message suppression | Placement and application-originated repeat distinction; not a proof of the hypothetical provider contract. |
| R11, Saltzer and Schroeder | [Basic Principles](https://web.mit.edu/saltzer/www/publications/protection/Basic.html), §I.A.3 b, c, f | Permission defaults, mediation including cached decisions, and least privilege. |

R08's full-text verification and R12's historical elasticity discussion remain at their recorded 2026-11-07 checks; this audit does not claim a new detailed passage review of those sources. Their reported performance or historical prices are not used as current predictions. S05's fan-out and capacity arithmetic were independently rerun as original examples. Source IDs R01–R24 remain stable. No additional source was needed for the correction.

## Remaining uncertainty and next item

No blocking error remains in the audited educational artifacts. Deployment evidence is still needed for real storage/flush behavior, isolation and mutation-path coverage, replica durability/read protocols, provider identity and retention semantics, cancellation, cross-epoch obligation identity, real workload and startup distributions, authorization freshness, credentials, telemetry and correlated dependencies. Finite checks cannot resolve these inputs, and passing them does not certify a deployed system.

After the saves and index update, next is **Run 16 — A01: Learning, generalization, and distribution change**. Retrieve F02–F04, inspect R13 learning/resampling/generalization passages and relevant R02 support, and build a simple-predictor baseline and split design for repeated organizations, templates and revisions. Align evaluation with the intended deployment and expose leakage. Do not infer diagnostic answers or mastery. The program remains in progress; final packaging and automation shutdown are not yet due.

## Revision history

- 1.0 — 2026-11-08. Audit B: seven packs and companions, one coverage-description correction, targeted primary checks and 41 exercise mappings.

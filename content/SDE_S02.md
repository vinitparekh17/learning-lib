# S02 — Data organization, indexes, and recovery

| Field | Value |
| --- | --- |
| ID, revision, date | S02 · 1.0 · 2026-11-05 |
| Prerequisites | F01 for keys and invariants, S01 for locality and units of work. A row is one record. A page is a fixed-size unit of storage in this lesson. |
| Capability | Design a revision-aware fact store, estimate two read paths, and explain what survives an acknowledged commit. |
| Evidence | CMU 15-445/645 Fall 2025 (R05) and OSTEP's journaling chapter (R04). Verified passages appear at the end. |
| Experiment | Constructed workload and failure model. Companion checks use SQLite for relational results and a separate Python model for crash boundaries. |
| Companion | [Hints, worked answers, and reproducible checks](SDE_S02_answers.md) |

## What should an approval point to?

A reviewer approved a payment using page 2 of invoice D17. A week later the supplier sends a corrected invoice with a different total. The reviewer needs both the current total and the evidence behind the earlier decision. A table keyed only by invoice ID makes overwriting the old value easy. Once that happens, an audit that joins the approval to today's invoice can produce a plausible but false account of yesterday's decision.

Give the logical document a stable ID and give each accepted revision its own identity. Keep the source bytes retrievable under an immutable reference. A digest can help verify retrieved bytes, but reproducing the page requires the bytes themselves. In this design a revision includes one frozen extraction result. Re-extracting the same bytes with a changed extractor creates a new revision that may share the same content reference. This is a design convention that makes the history unambiguous.

| Relation | Key | Other information and constraints |
| --- | --- | --- |
| Revision | (doc, rev) | Immutable source reference, content digest, extractor version, completion manifest such as the expected fact slots |
| Fact | (doc, rev, slot) | Name, typed value, source locator. Foreign key to Revision. Slot identifies one occurrence within the frozen extraction. |
| Head | doc | Chosen published rev. The pair (doc, rev) references Revision. |
| ApprovalEvidence | (approval_id, evidence_no) | Exact (doc, rev, slot) used, with a foreign key to Fact. Multiple pieces of evidence can support one approval. |

At every published boundary, Head must select a complete revision. Its facts must resolve to evidence in the same source version. Existing approvals must continue to resolve even when Head advances. A foreign key establishes that the target row exists. Completeness additionally requires checking the expected slots before publication. For an invoice with no extractable facts, an explicit empty manifest distinguishes a completed empty result from an extraction still in progress.

Store amounts with a currency and an agreed exact numeric representation. Preserve a locator such as page number plus coordinates in the frozen page image. An offset into a newly generated text rendering would also require its rendering version. Publish Revision, Fact, and Head within one database transaction after validating the manifest. Assume a single publisher for now. If the source is in separate object storage, make the immutable object durable and verify it before publishing the database reference. A crash between those operations can leave an unreferenced object. Retention and later cleanup must protect every revision used as evidence.

## Put two questions to the same twelve rows

The reviewer opens D17 revision 2 and asks for all its facts, including their source locators (Q1). An investigator instead asks for every historical occurrence of delivery reference X, including the document and source locator (Q2). Those questions place the same rows in different groups. “Historical” matters. A later correction may remove X from the current revision while an older occurrence still answers Q2.

Here is a hypothetical heap, an unordered collection of pages holding records. The numbers are physical row identifiers for this example. Each fact label below abbreviates one fully identified fact with its own slot and locator. A vertical ordering across pages reflects insertion order, with revisions interleaved as they arrive.

| Page | Four records in slot order, shown as row ID, document/revision, fact |
| --- | --- |
| P1 | 1 D17/1 total · 2 D17/1 delivery X · 3 D08/1 total · 4 D08/1 delivery Y |
| P2 | 5 D17/2 delivery X · 6 D09/1 total · 7 D09/1 delivery Z · 8 D10/1 total |
| P3 | 9 D10/1 delivery Y · 10 D17/2 total · 11 D11/1 total · 12 D11/1 delivery X |

With a full scan, inspect all twelve records on three heap pages. Q1 returns rows 5 and 10. Q2 returns rows 2, 5, and 12. Scan predicates are simple enough to use as an oracle when testing an index. For example, changing Q1 to filter only on doc would accidentally return revision 1 as well. A faster path that returns that larger set has changed the question.

An index stores another route to the records. Imagine two ordered indexes. One groups physical row IDs by (doc, rev). The other includes only delivery facts and groups their row IDs by reference value. In our small model, each lookup follows one root separator to one leaf page holding the complete matching entry and its short list of row IDs. Assume a cold cache and count each distinct page read once during the query. The caller needs the source locator, which lives in the heap. These assumptions describe a constructed two-level tree. A real tree may fit in a single page or span many levels.

| Query | Lookup trace | Distinct pages | Candidate heap rows inspected |
| --- | --- | ---: | ---: |
| Q1 by revision | Root → leaf for (D17,2) → row 5 on P2 and row 10 on P3 | 2 index + 2 heap = 4 | 2 |
| Q2 by delivery | Root → leaf for X → rows 2, 5, 12 on P1, P2, P3 | 2 index + 3 heap = 5 | 3 |
| Either by scan | P1 → P2 → P3 | 3 heap | 12 |

The index saves predicate evaluations, yet both indexed paths touch more pages than the scan on this layout. S01's question about the unit being counted changes the recommendation. On a much larger heap, a selective lookup might still lead to only two data pages. Conversely, a popular delivery reference might lead to nearly every page. A widely scattered result also changes how the storage device can serve the reads. Page counts alone do not determine elapsed time.

One alternative is to put frequently requested output fields in the leaf. In a read model where all required fields and visibility information are available there, Q2 could finish after the index lookup. The wider entries take more space and may reduce the number that fit per page. Another option is to store a revision's facts together, so Q1 fetches them from fewer pages. Q2 might still reach many pages because delivery references cut across documents. Choose after measuring the query mix, common and rare keys, cache state, and required output columns. The CMU notes explain leaf entries and the distinction between record IDs and tuple payloads. [R05, lecture 08 §§1–2](https://15445.courses.cs.cmu.edu/fall2025/notes/08-indexes1.pdf)

## What a new index costs the writer

Suppose revision 3 adds a total and a delivery reference Y. Those two facts require two base rows and two row-ID associations in the revision index. The delivery-only index gains one association. That is five logical additions in this fact-storage model, plus the revision metadata and Head update. A batch could share a leaf write, and a full leaf could split, so five additions do not predict five device writes. Index keys and row IDs consume storage for every retained revision. Returning historical X matches remains correct even after the head moves to Y.

Before adding the delivery index, ask how frequently investigators actually search by reference and how selective the common values are. Measure extra bytes per revision, ingestion time, and the distribution of lookup times under the same workload. Include maintenance and recovery in the comparison. If approvals mostly open known revisions and historical investigations are rare, a revision index and occasional scan may suffice. If selective investigations must finish within a deadline, the secondary index earns a trial against the scan.

## Crash after the reply, before the last page write

A server has published D17/2 and now wants to publish D17/3. Consider two persistent logical objects in a small recovery model. F3 is the complete immutable revision bundle, including its facts and locators. H is the head pointer. The old revision remains accessible. Representing the new bundle as one object keeps the trace short. An implementation with several fact pages must log all of them. For this trace the indexes are derived and rebuilt from recovered facts before reads resume.

Assume a single transaction, a trusted initial snapshot, atomic writes of each modeled object, and stable storage that retains completed flushes through power loss. The source bytes are already durable. Volatile memory is lost in a crash. The durable log is a valid prefix of complete records in order. This toy protocol prohibits uncommitted updates from reaching home pages (NO-STEAL) and allows committed pages to reach home after acknowledgement (NO-FORCE). A **home page** is the normal storage location for the object. These choices allow a compact redo-only demonstration.

1. Stage the full bundle and new head in memory. Append log records setting F3 to the complete bundle and H to 3. The writer can flush those records before it decides to commit.
2. Append COMMIT for this transaction and flush the log through COMMIT. An ordered flush makes both earlier updates durable with it. Publish both changes as a unit for subsequent readers, then send the success reply.
3. Later write the committed objects to their home locations. For the example, F3 goes home first. Retain the log until a durable checkpoint includes both objects.
4. After a crash, recover before accepting reads. Apply the assignments of each fully committed transaction in log order. An incomplete transaction has no durable home updates under the stated policy. Replaying the same full-value assignment twice gives the same state here.

| Last event before power loss | What survives | State after recovery |
| --- | --- | --- |
| Updates flushed, COMMIT absent | Update records and old home pages | D17/2 is current |
| COMMIT flushed, reply still in transit | Complete transaction log, old home pages | D17/3 is current. Client needs to resolve the uncertain outcome. |
| Client received success, only F3 reached home | Complete log, new F3, home H still 2 | Replaying H publishes D17/3 with its evidence |
| Both objects reached home, log still retained | Complete log and new home values | Repeated assignments preserve D17/3 |

Move the reply earlier as a counterexample. If the server replies after appending COMMIT only in volatile memory, power loss can leave an update-only durable prefix. Recovery correctly retains revision 2, contradicting the promise the client heard. A transaction ID or stable publication key lets a retry query the committed result after a lost reply. Protecting an external payment from duplicate effects requires its own contract in C01.

A system that lets uncommitted updates reach home must also handle their effects during recovery. CMU's ARIES lesson describes analysis, replaying history, and undoing incomplete transactions. The toy protocol deliberately buys a shorter proof by restricting flushes. OSTEP's data-journaling trace provides the related file-system intuition: persist the journal contents, persist the commit marker, then install the updates at their home locations. Each layer has its own transaction boundary. [R05, lectures 21 §§2, 6](https://15445.courses.cs.cmu.edu/fall2025/notes/21-logging.pdf) and [22, recovery phases](https://15445.courses.cs.cmu.edu/fall2025/notes/22-recovery.pdf) · [R04, chapter 42, p. 11](https://pages.cs.wisc.edu/~remzi/OSTEP/file-journaling.pdf)

## Practice

1. An approval cites only D17 and “total.” Show what happens on a join after the total changes. Specify the missing keys and one source-retention assumption.
2. Trace Q1 and Q2 using the table. Count candidate heap records and distinct cold pages for each access path. Explain how a cached root changes each indexed count.
3. Q2 becomes “all **current** invoices citing X.” Assume each document's highest listed revision is its published head. Which rows qualify? Explain how to implement the changed query and which extra reads were absent from the original count.
4. For the two-fact revision 3, count logical additions with each index. Name one observed change in workload that would reverse your recommendation.
5. Crash after the success reply with only F3 installed. Recover by hand. Then remove the rule that prevents uncommitted home writes and construct a state the toy algorithm fails to repair.
6. Formulate the acknowledgement in one sentence. Explain what the client can conclude after a timeout, and what additional mechanism you would need if the storage device itself were lost.

## Reference card and evidence

Keep four things on the page: the stable logical identity, the query predicate and output, the unit of physical work, and the durable event preceding success. At the end of a recovery trace test both an old approval and a fresh Head lookup. S03 considers interleaved writers, S04 broadens the failure boundary to replicas, and A03 reuses revision identity for evidence retrieval.

| Basis | Inspected locator | Use and limit |
| --- | --- | --- |
| R05, CMU Fall 2025 | [03, §§7–10, pp. 3–4](https://15445.courses.cs.cmu.edu/fall2025/notes/03-storage1.pdf) | Pages, heap layout, record IDs. Page sizes and occupancy here are assigned. |
| R05, same edition | [08, §§1–2, pp. 1–2](https://15445.courses.cs.cmu.edu/fall2025/notes/08-indexes1.pdf) | Keys, routing, leaf payloads, insertion. Our posting lists and two-level counts are conditional. |
| R05, same edition | [21, §2 pp. 1–2 and §6 pp. 4–5](https://15445.courses.cs.cmu.edu/fall2025/notes/21-logging.pdf) and [22, pp. 5–6](https://15445.courses.cs.cmu.edu/fall2025/notes/22-recovery.pdf) | Buffer policies, log-before-data ordering, durable commit, scope of ARIES redo and undo. |
| R04, OSTEP | [Crash Consistency, chapter-local p. 11, data-journaling protocol and Recovery](https://pages.cs.wisc.edu/~remzi/OSTEP/file-journaling.pdf) | File-system analogy for commit versus checkpoint. |
| Original design and executed checks | Companion below the six solutions | Synthetic history and failure model. Actual storage barriers, corruption handling, concurrent publication, workload selectivity, and latency need separate verification. |

# S02 — Hints, worked answers, and checks

| Field | Value |
| --- | --- |
| ID / revision / date | S02 answers · 1.0 · 2026-11-05 |
| Prerequisite | [Data organization, indexes, and recovery](SDE_S02.md) |
| Capability | Audit a query path and a commit promise against explicit invariants |
| Sources | R05 and R04 passages are recorded in the core pack. |
| Experiment | Executed SQLite queries against synthetic facts and enumerated a separate redo-only recovery model in Python. |

## Hints

1. Follow the approval after the head moves. Which row and which source bytes does it identify?
2. Translate each row ID into a page before adding index reads.
3. Distinguish a revision that exists from one selected by Head.
4. Count row-ID associations before estimating bytes or writes.
5. List the durable prefix and the two home values separately.
6. Consider a crash immediately before the reply and immediately after dispatch.

## 1. Keep the evidence behind an approval

Suppose D17/1 records a total of 90 and D17/2 records 95 in the same currency. Joining an old approval to the current head returns 95 even if the reviewer approved 90. Joining only by doc and name across history can return *both* totals. Store the approved evidence's (doc, rev, slot) and join by that key. Resolve its page locator against the immutable source reference attached to that same revision. Keep the source version readable throughout the evidence-retention period. A checksum alone cannot reconstruct a deleted page.

## 2. Count what each path actually reads

Q1 finds row 5 on P2 and row 10 on P3. Its indexed path inspects two candidate records and reads four distinct cold pages including root and leaf. Q2 finds 2, 5, 12 on P1, P2, P3. It inspects three candidate records and reads five distinct cold pages. Scanning either query inspects twelve records over three pages. A resident root reduces the respective cold reads to three and four under the same other assumptions. The root lookup still occurs. If the leaf contains every requested field and sufficient visibility information, the heap fetches could also disappear.

The count includes only facts that pass the exact index predicate as candidate heap records. An index keyed just on doc would return four D17 candidates and require a revision check. The narrower key may be useful for other queries. It answers a different performance question.

## 3. Historical versus current

Historical X hits are 2, 5, 12. D17/1 has been superseded by D17/2, so only 5 and 12 survive the current-revision filter under the assigned heads. After publishing D17/3 with Y, only 12 survives. Join each candidate's (doc, rev) to (doc, published_rev) in Head. A cached Head entry for D17 can serve two candidate checks. Additional cold reads depend on Head's index and data layout. The given fact-page model has insufficient information to assign an exact cold total to the join. A current-only secondary index could accelerate this query, at the cost of removing obsolete entries and installing new ones atomically when Head changes.

## 4. Ingestion and the decision

Two base inserts are required. Keeping only the revision index adds two revision associations, for four logical additions. Keeping only the delivery index adds one delivery association, for three. Keeping both gives five. Revision metadata and Head updates are outside those figures. Old revision entries stay available for historical queries. If X becomes ubiquitous and each investigation needs full locators from nearly every page, compare a scan against the secondary lookup. If selective historical investigations become frequent, measure how much the secondary index saves under that mix and whether ingestion can absorb the cost.

## 5. Recover partial installation

The durable prefix contains SET F3, SET H=3, and COMMIT. Home contains F3 and H=2. Reapply the complete bundle assignment, then assign H=3. Rebuilding derived indexes from the recovered facts restores their query results. The immutability of old revisions preserves approvals pointing to D17/1 or D17/2.

Now allow H=3 to reach home before COMMIT. A crash with the update-only log leaves H=3 but F3 missing. The toy recovery skips incomplete transactions and therefore preserves the dangling reference. Valid fixes include preventing this flush or retaining undo information and using a recovery protocol that restores the prior state. Replaying every update unconditionally would expose an uncommitted revision.

## 6. State the promise and its boundary

A success reply promises that after a process or power failure with the modeled stable storage intact, recovery will expose the complete published revision and preserve earlier evidence. A timeout is compatible both with a transaction that never committed and with one whose reply was lost. Look up a stable operation key before deciding to retry. The write protocol must enforce the operation-key constraint at the same transaction boundary if a retry is to reuse the existing result.

Surviving loss of the device requires an independently durable copy with a tested recovery procedure. If every acknowledged revision must survive that loss, success must wait for sufficient data to be durable outside that failure domain. A nightly backup alone leaves a window of acknowledged changes at risk. S04 will specify the replication and failure assumptions in detail.

**Assessment criteria.** A defensible answer names the revision key, states the query semantics, counts pages and matching rows separately, identifies the durable commit boundary, and gives a crash or workload that defeats an overbroad claim.

## Reproduce the checks

Run this block under Python 3. SQLite checks the logical query results. The assigned heap layout and cold-page counts are calculated separately. The recovery function models ordered durable records and atomic home writes. These are three different checks.

```python
import sqlite3
from itertools import product

data = [
    (17,1,'total','90'), (17,1,'delivery','X'),
    (8,1,'total','55'), (8,1,'delivery','Y'),
    (17,2,'delivery','X'), (9,1,'total','48'),
    (9,1,'delivery','Z'), (10,1,'total','70'),
    (10,1,'delivery','Y'), (17,2,'total','95'),
    (11,1,'total','75'), (11,1,'delivery','X'),
]
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE fact(id INTEGER PRIMARY KEY, doc INT, rev INT, name TEXT, val TEXT)')
db.executemany('INSERT INTO fact(doc,rev,name,val) VALUES(?,?,?,?)', data)
q1 = 'SELECT id FROM fact WHERE doc=17 AND rev=2 ORDER BY id'
q2 = "SELECT id FROM fact WHERE name='delivery' AND val='X' ORDER BY id"
def ids(query):
    return [row[0] for row in db.execute(query)]

assert ids(q1) == [5,10] and ids(q2) == [2,5,12]
db.execute('CREATE INDEX by_rev ON fact(doc,rev)')
db.execute("CREATE INDEX by_delivery ON fact(val) WHERE name='delivery'")
assert ids(q1) == [5,10] and ids(q2) == [2,5,12]
db.execute('CREATE TABLE head(doc INTEGER PRIMARY KEY, rev INT)')
db.execute('INSERT INTO head SELECT doc, MAX(rev) FROM fact GROUP BY doc')
current = "SELECT id FROM fact JOIN head USING(doc,rev) WHERE name='delivery' AND val='X' ORDER BY id"
assert ids(current) == [5,12]
def heap_pages(row_ids):
    return {(row_id-1)//4 + 1 for row_id in row_ids}
assert len(heap_pages(range(1,13))) == 3
assert 2 + len(heap_pages(ids(q1))) == 4
assert 2 + len(heap_pages(ids(q2))) == 5
db.executemany('INSERT INTO fact(doc,rev,name,val) VALUES(?,?,?,?)',
               [(17,3,'total','98'), (17,3,'delivery','Y')])
db.execute('UPDATE head SET rev=3 WHERE doc=17')
assert ids(current) == [12] and ids(q2) == [2,5,12]
assert db.execute('SELECT val FROM fact WHERE id=1').fetchone() == ('90',)

# One transaction and one complete, ordered log prefix.
bundle = ('total=98','delivery=Y')
log = [('bundle',bundle), ('head',3), ('commit',True)]
old = {'head':2,'bundle':None}
new = {'head':3,'bundle':bundle}
def recover(home, prefix):
    state = home.copy()
    if prefix and prefix[-1] == ('commit',True):
        state.update(prefix[:-1])
    return state

for length in range(3):  # no durable commit, NO-STEAL
    assert recover(old, log[:length]) == old
for wrote_bundle, wrote_head in product((False,True), repeat=2):
    home = {'head':3 if wrote_head else 2,
            'bundle':bundle if wrote_bundle else None}
    assert recover(home, log) == new
    assert recover(recover(home, log), log) == new
# Illegal flush breaks the invariant when there is no durable COMMIT.
assert recover({'head':3,'bundle':None}, log[:2]) == {'head':3,'bundle':None}
print('S02 query, page-count, publication and recovery checks passed.')
```

The toy log uses full after-values. An operation such as “increment a balance” would require a replay guard or a different log encoding to tolerate repeated application. Real device flush behavior and database crash handling require a deployment-specific test.

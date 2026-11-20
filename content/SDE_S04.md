# S04 — Replication, consensus, and partial failure

| Field | Value |
| --- | --- |
| ID / revision / date | S04 · 1.0 · 2026-11-06 |
| Prerequisites | S03 histories, epochs and receipts; S02 durable commit and immutable evidence |
| Capability developed | Trace a leader failure, defend a commitment boundary, and distinguish client uncertainty from repeated effects |
| Source-check status | R07 extended Raft paper and R10 author-hosted paper inspected. Exact locators below. |
| Experiment status | Executed finite quorum, voting, log-repair and application-replay checks. No live cluster tested. |
| Companion | [Hints, worked answers, and checks](SDE_S04_answers.md) |

## The authority can fail too

S03 gave D17 one authority for deciding which approval occupies a round. That authority checked the epoch, selected revision and operation key together. Now its machine fails after accepting a request. A replacement must distinguish a decision that must survive from a speculative update that can disappear. Merely copying files to another server does not define that distinction.

We will replicate an ordered sequence of commands across three servers A, B and C. A command is input to a deterministic state transition. Given the same initial state and command sequence, each server must compute the same results. For example, `Approve(k,D17,epoch=7,rev=2,actor=R)` either records an acceptance and receipt or returns a defined rejection. It cannot call a changing external model during replay and still promise identical results. Store the chosen evidence identity in the command and validate it against replicated state.

A **log index** is a position in the sequence. A **term** is a leadership generation. An **approval epoch** is the business round introduced in S03. These are three different numbers. Electing a new leader does not reopen D17's approval round. A log entry records its index, term and command.

Raft is our worked mechanism, using the paper's fixed-membership core. Its persistent state includes term, vote and log; its voting and append rules constrain successors. Current-term entries advance commitment through a majority, with earlier entries covered by the committed prefix. The detailed rules are in R07 Figure 2 and §§5.2–5.4. This pack constructs one trace to explain why those restrictions matter rather than reproducing a full implementation.

## Declare the world before claiming reliability

Assume three fixed members with stable identities. Servers may stop and recover. Messages may be lost, delayed, duplicated or reordered. Stable storage retains completed writes across the modeled restart. Servers follow the protocol; malicious replies and undetected corruption are outside the model. Required persistent changes reach stable storage before success responses to protocol RPCs.

Progress needs a communicating majority and enough stability to elect and retain a leader. A network timeout is evidence that a response did not arrive by a deadline, not proof that the other machine stopped. An isolated old leader can remain alive while the other two elect a successor.

Our safety target is that different servers never apply different commands at the same log index. Our application target is at most one acceptance per document/approval epoch. Those properties differ. An agreed command that erroneously ignores the epoch could be replicated perfectly and still violate the business rule. The replicated state transition must preserve S03's invariant.

For three members a majority has two. Any two such majorities overlap because two disjoint sets of size two would require four members. More generally, two subsets of size q in N members intersect in at least `2q−N` members. Intersection provides a witness shared by two decisions. Rules about what that witness may approve supply the safety argument. Counting copies alone does not.

## A committed approval with no reply

Start with the same committed prefix through index 4 on all servers. Its last term is 1. D17 is at epoch 7, published revision 2, with no owner. A is leader in term 2. The following values and events are an original hypothetical case.

| Event | A | B | C | Client knowledge |
| ---: | --- | --- | --- | --- |
| 1 | Persist entry 5, term 2, approval k | Prefix through 4 | Prefix through 4 | Waiting |
| 2 | Send entry 5 | Check predecessor (4,1), persist entry 5, reply | Unreachable | Waiting |
| 3 | Receive B's success; majority A+B holds entry 5 | Has entry 5, may not know it is committed | Still through 4 | Waiting |
| 4 | Advance commitment, apply approval, then crash before reply | No commit notification received | Still through 4 | Timeout |
| 5 | Down | Seek election in term 3 | Vote for B | Outcome unknown |
| 6 | Down | Replicate no-op at index 6, term 3, to C after entry 5 | Persist entries 5 and 6 | Outcome unknown |
| 7 | Down | Commit through 6, apply 5 then 6 | Learn commit boundary, apply in order | Retry k can receive original result |

At event 3, the original leader's term-2 entry has reached a majority. Its protection does not depend on whether the client hears about it. B's uncertainty about the commit boundary also does not make that entry disposable.

Why can B win? Its last entry is (term 2,index 5), while C ends at (term 1,index 4). C can vote for B. In the reverse attempt, B rejects C's older log, so C cannot obtain two votes while A is down. The up-to-date comparison examines last term first, then last index for a tie. A long log with an older last term is not automatically preferred.

Why include the no-op? B must not simply infer that an inherited entry is committed by counting its copies under the new term. B replicates an entry from its own term at index 6. Committing that entry establishes the whole preceding prefix, including approval k. A no-op changes no business state. It still occupies a log position and establishes a commitment boundary. R07 §5.4.2 and Figure 8 explain why the general rule needs the current-term restriction.

If A returns, observing term 3 makes it step down. A follower checks the index and term of the preceding entry before accepting an extension. Conflicting uncommitted suffixes can be replaced. That repair operation is not permission to erase an arbitrary committed entry; election restrictions prevent a valid successor from lacking committed history.

## Move the crash earlier

Change only event 2. Suppose B never persisted entry 5, so A alone has it when A crashes. B and C both end at index 4. They can elect B and commit a different term-3 entry at index 5. On recovery A's uncommitted suffix is replaced. This does not violate the safety target because A must not have applied or reported success for its speculative entry.

An early reply after A's local append would create a false promise. The client would have heard “accepted” for a decision that a legitimate replacement leader could discard. This is S02's acknowledgement discipline extended across machines. A durable local log protects against one kind of restart; it does not by itself establish replicated commitment.

A different naive rule lets whichever server times out become leader and accept locally. Partition A from B+C. A accepts proposal k, while B accepts competing proposal j for the same epoch. If both return success, merging the histories later cannot make both original promises true. Under our contract the minority cannot commit new approvals. It can return an unavailable response or offer a clearly labeled stale view, but cannot call that view an authoritative current decision.

## Retry the operation, preserve its identity

Replaying k can append another log entry. Log consensus alone does not identify that entry as the same business request. Our deterministic application retains `key → (payload,result)` with the acceptance. Reapplying the identical key returns its stored result. Reusing the key for a different payload is rejected. The receipt state must survive recovery and any snapshot that discards older log entries.

Suppose an approval round was reopened after k succeeded. A retry still receives the historical result for k, without accepting anything in the new epoch. The response must distinguish a past accepted decision from a currently active approval. A client that generates a new key after every timeout loses this protection.

This contract prevents repeated application of the same recorded operation within the retention boundary. It does not make an external payment atomic with the log. If a dispatcher sends a payment and crashes before recording its response, another dispatcher may send again. The destination needs an effect-level identity and contract, or the workflow needs explicit reconciliation. R10's duplicate-message discussion shows why lower-layer duplicate suppression cannot recognize every application retry. C01 will develop that responsibility boundary.

Likewise, a server that calls itself leader cannot safely answer every “is k accepted?” query from local memory. It may be isolated and superseded. R07 §8 describes additional safeguards for authoritative reads. For this lesson, route result resolution through a protocol that establishes current authority and applies the required committed prefix. A stale “not found” response is not evidence that a retry should receive a new key.

## Safety has an operating cost

| Design choice | What it buys under its model | Cost or remaining gap | Evidence that changes the decision |
| --- | --- | --- | --- |
| One durable server with recovery | Simple local persistence | Machine/device failure can halt service or lose unavailable data | Required recovery window and actual restore tests |
| Three-member consensus group | Majority progress despite one unavailable member | Durable replication and communication on the critical path | Storage latency, network delay, correlated outages |
| Five-member consensus group | Majority of three can remain after two unavailable members | More replicated storage and operational work | Failure-domain analysis justifies the extra tolerance |
| Async copy plus early success | Lower acknowledgement dependency | Latest acknowledged decisions can be absent after failover | Acceptable data-loss window explicitly permits that outcome |

Three processes on one failed host do not provide three independent failure domains. Replicating a bad command also creates three copies of the same bug. Backups, restore procedures, authorization and application validation remain separate needs.

Measure acknowledgement latency, election disruption, follower lag, disk flush behavior and retry outcomes under the intended workload. Do not translate the historical paper's timing examples into a production timeout. Safety requires the rules to hold even during long delay; useful progress additionally requires favorable communication and scheduling conditions. No universal recovery-time bound is derived here.

## Practice

1. List all two-member majorities of A,B,C. Show their intersections. Explain why overlap alone cannot stop conflicting decisions if a voter may vote twice in one term.
2. Trace the main failure through B's election. Identify when entry 5 becomes committed, when B can establish its commit boundary, and what the client knows at each point.
3. Crash A before B stores entry 5. Show a legitimate replacement at index 5 and explain which earlier success reply would be invalid.
4. Compare candidate logs ending at (term 2,index 9) and (term 3,index 6). Then explain why counting a majority of copies of an inherited entry is insufficient as the general commitment rule.
5. Retry k before and after reopening D17. Specify receipt retention and payload binding. Give one duplicate-payment failure this cannot exclude.
6. Partition A from B+C and then partition all three separately. State safety and progress expectations. Name one failure outside the model and a measurement needed before choosing three versus five members.

## Evidence and reference card

| Basis | Inspected locator | Use and scope |
| --- | --- | --- |
| R07, Ongaro/Ousterhout, extended version, May 20, 2014 | [Paper](https://raft.github.io/raft.pdf), §2 pp. 1–2; Figure 2 p. 4; §§5.1–5.4 pp. 4–9 | Replicated state, durable protocol state, election and log rules, current-term restriction. Fixed membership here. |
| R07, same edition | §5.6 pp. 9–10; §8 p. 13 | Timing/progress distinction, client retries and authoritative reads. No benchmark result adopted. |
| R10, Saltzer/Reed/Clark, 1984 | [Author copy](https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf), PDF p. 6 Duplicate message suppression; p. 7 Transaction management | Application-level retry and acknowledgement meaning. No historical performance figure adopted. |
| Original case and checks | Trace tables, majority arithmetic, companion model | Constructed inputs. The checks are not a full Raft implementation or proof. |

Recall the sequence: persist → replicate under the protocol → establish commitment → apply deterministically → reply. Separate log index, leadership term, business epoch and operation key. After a timeout, resolve the same operation identity. Keep the external-effect boundary visible.

S03's invariant is now replicated; S02's durability promise applies to each required persistent write. S06 will add authority and damage boundaries. B02 will price reliability and recovery. Open deployment questions include storage failure modes, read semantics, receipt retention, evidence availability, membership changes and snapshot correctness. The last two are deliberately deferred implementation depth, not removed curriculum items.

## Revision history

- 1.0 — 2026-11-06. Fixed three-member trace, majority derivation, two crash boundaries, retry contract, and separate finite checks.

# C06 — How should architecture respond when a supplier changes?

| Field | Value |
| --- | --- |
| ID | C06 |
| Title | Supplier change without losing evidence or control |
| Revision | 1.0 |
| Date | 2026-11-15 |
| Prerequisites | S02/S06, A03–A05, B02/B03 |
| Capability developed | Price a migration, preserve authority and evidence, and test whether an advantage survives bundling |
| Source-check status | R15 §2.2, R11 §I.A.3(c), R21 packaging section inspected |
| Experiment status | Synthetic ledger, sensitivity, paired outcomes and migration-manifest checks executed; no supplier integration or production trial |

## Recommendation and decision boundary

Retain the incumbent for the initial six-month horizon, while keeping the evidence store, evaluation cases and permission checks under our control. Do not build a universal provider abstraction in advance. Implement a narrow replacement boundary around the specific inference operation. When the incumbent's recurring charge increases enough, switch the inference component after validating the replacement against the same complete task. Adopting a bundled workflow is a different option because it changes more than inference.

The recurring fictional job is preparing invoice evidence for a reviewer: identify the applicable revision, extract the requested reference, attach exact supporting locators and deliver a supported package within one business day. No candidate may approve payment. This memo returns to A05's evidence-preparation boundary; it does not silently inherit C05's additional internal routing action. All three options have the same eligible population, evidence rights, output contract, deadline and authority restrictions.

A supplier change could mean a price change, model retirement, altered API behavior or a newly bundled feature. Our example changes only a recurring fee. It is not news about any real provider, and all monetary, workload and performance inputs are hypothetical. Business-day completion includes human handling and queues; a fast model response alone is not success.

## What must remain ours to control?

A portable interface is a stable description of the job, not a guarantee of equal behavior. For one inference operation, accept a task ID, schema version, exact evidence references and bounded input; return typed claims, supporting references, unresolved status and usage observations. A provider adapter maps that contract to a particular API. It must expose unsupported capabilities instead of inventing a successful approximation.

| Asset or rule | Authority and migration treatment |
| --- | --- |
| Source bytes and revision manifests | Retain immutable originals and exact document/revision identities; verify export and restore |
| Tenant grants and disclosure policy | Enforce in our authority boundary before evidence leaves scope; recheck according to declared revocation rules |
| Extracted facts and locators | Keep extractor/rendering versions; a changed extraction creates a new revision under S02's convention |
| Retrieval index | Treat as derived state with a named encoder/chunker/configuration; rebuild and evaluate when incompatible |
| Model prompts and adapter mapping | Version explicitly; revise per provider while preserving task semantics |
| Evaluation cases and labels | Retain permitted source snapshots, rubrics and holdouts; do not assume data reuse rights |
| Action receipts and operation identity | Keep independent of inference vendor; an inference retry cannot become a new business approval |

S02's digest checks bytes, but a digest without the bytes cannot restore a source page. Exporting final answers alone loses the ability to inspect what supported them. A03 separates corpus, candidates, supplied context and claims; preserve these intermediate identities so a migration regression can be located. R15 §2.2 describes document/query encoders and inner-product retrieval. That mechanism motivates a concrete compatibility question: do the new query representations match the stored document representations? Equal vector dimensions alone do not answer it. The paper does not establish interoperability between arbitrary providers.

R11 §I.A.3(c) calls for authority checks across access paths, including recovery, and cautions about remembered authorization decisions. Our migration application is to test export, replay, support access and rollback as protected paths too. A correctly scoped normal endpoint is insufficient if an export script reads every tenant. These are design obligations, not claims of certification.

## Compare three credible options

Use 1,000 eligible cases per month and six months of service. Labor is valued at 0.50 U/minute. U is a fictional common cost unit. Assume each candidate has passed permission, evidence and deadline gates with at least 95% correct on-time completion under realistic workload. That equal-adequacy premise is provisional and must be tested; the table is a decision model, not results of such a test.

| Input | I: retain incumbent | R: replace inference | B: adopt supplier bundle |
| --- | ---: | ---: | ---: |
| One-time migration/validation cost | 0 U | 900 U | 300 U |
| Monthly supplier/infrastructure charge | 400 U | 250 U | 0 U incremental |
| Customer handling minutes/case | 2.0 | 2.2 | 3.5 |
| Monthly incremental maintenance | 100 U | 150 U | 50 U |
| Control change | None | Adapter/inference only | Retrieval and workflow move to bundle |

The incumbent's old setup cost is sunk and excluded. Replacement setup includes mapping, rebuild, evaluation, training and cutover effort. The bundle's subscription is already purchased for unrelated use, so zero is its incremental charge in this scenario; its labor and maintenance are not free. Recurring human minutes include verification and exceptions, including failures. Maintenance excludes those minutes. Common baseline costs cancel; any noncommon export, overlap or exit fee must be added. Cost is from the customer's decision perspective, not the supplier's margin.

Define monthly cost `M = supplier + cases × minutes × 0.50 + maintenance`, then horizon cost `T = setup + H × M`. Monthly totals are I=1,500, R=1,500 and B=1,800 U. Six-month totals are **9,000, 9,900 and 11,100 U**. Retaining I is cheapest among assumed-adequate choices. R's lower API bill is exactly consumed by 100 U extra handling and 50 U extra maintenance each month; setup then makes it more expensive. B's free feature does not compensate for extra work.

This does not mean switching is always wasteful. It means the reason must survive a complete ledger. No extra monetary value is assigned to optionality here. If planned retirement makes retention impossible, that becomes a feasibility constraint and the comparison must be revised explicitly. Likewise, a cost-only winner cannot excuse worse evidence or forbidden disclosure.

## One constraint changes: the incumbent fee

Change I's monthly supplier charge from 400 to **700 U**, holding everything else fixed. I now costs 1,800 U/month and **10,800 U** over six months. R remains 9,900 and B remains 11,100. Revise the choice to R, conditional on the same adequacy gates. R saves 900 U across the horizon after its setup cost.

Let x be I's monthly charge. Then `T(I)=6(x+1,100)`. Equality with R occurs at `x=550 U`. Above that threshold R is cheaper; at equality retain I to avoid unnecessary migration. The changed x=700 gives recurring savings of 300 U/month, recovering 900 U setup after three full months. For an assured horizon shorter than three months, I is cheaper; at three months the totals tie. This is deterministic accounting under assigned inputs, not a forecast of supplier prices or customer tenure.

A different single change illustrates bundling pressure without altering the main scenario. At the original incumbent fee, what bundle handling time t would tie I? Solve `300+6(1,000×0.50t+50)=9,000`, giving **t=2.8 minutes/case**. Below that, an adequate bundle beats I. The additional labor can therefore be measured directly; a claim that “our wrapper is defensible” is irrelevant if the bundle performs the full job with less total cost.

## Port the evaluation, then rerun it

Evaluation portability means carrying the question, population, evidence snapshots and scoring procedure across candidates. It does not mean copying the incumbent's benchmark score onto the replacement. Freeze eligibility before execution. Each invoice and its retries form one case. Include missing evidence, conflicting revisions, long inputs, unfamiliar layouts, forbidden tenant requests and tool failures. Give candidates access to the same authorized corpus, not necessarily identical retrieval results: retrieval is part of the bundle's behavior.

Use two comparisons. First compare complete deployed candidates under the same service contract. Second, for diagnosis, supply identical sufficient evidence to compatible generators to separate generation from retrieval. Label the second as an intervention; it removes a failure mode the actual deployment may still have. Hold tuning examples apart from the final comparison and record every adapter/model/index version.

A constructed paired ledger of 100 cases has 92 successes for both I and R, 4 for I only, 3 for R only and 1 for neither. I succeeds on 96, R on 95. Both meet the assigned 95% sample threshold, but these counts do not prove population adequacy. The same inputs reveal a net loss of one case for R; unpaired headline scores would hide which tasks regressed. Review discordant cases and appropriate uncertainty before changing the production boundary. This is a teaching fixture, not a model benchmark.

A04 reminds us to measure resources under actual input/output lengths and offered load. Token counts, cache behavior and context truncation belong to a specific configuration. Compare charged usage and full arrival-to-result delay, including failures, rather than assuming a token or a cache hit has the same cost across suppliers. A05 adds bounded retries and typed unresolved outcomes. An adapter must not conceal repeated calls, timeout fallback or dropped citations to make the schemas look identical.

## A migration that can be stopped

Use a staged plan with explicit exit conditions:

1. Export immutable sources, revisions, facts, grants and evaluation manifests under authorized scope. Verify counts, exact identities and byte digests; restore into an isolated environment. Count agreement alone cannot detect swapped contents.
2. Build replacement derived state under a new configuration identity. Replay frozen cases without business effects. Compare support, permissions, deadlines and full cost, including difficult subgroups.
3. Keep one authoritative publication path. Shadow inference may produce candidate drafts, but it does not create approvals or alter published evidence. Mark outputs by configuration and source revision.
4. Admit a bounded rollout only after gates pass. Keep the old compatible path available for the declared rollback window. Stop on unauthorized access, unresolvable provenance or a predeclared service regression.
5. Retire old credentials and derived stores after reconciliation and retention obligations are satisfied. Preserve historical evidence still referenced by prior decisions.

Suppose a new extractor finishes revision 4 while the published head still points to revision 3. A crash before the atomic head change leaves 3 current and 4 unreferenced; recovery must not publish a partial 4. If the head change commits, it must refer to a complete durable revision. This applies S02's publication rule. Rolling back code does not justify rewriting historical evidence to look as if the new extractor never ran.

A lost inference reply may permit another bounded read-only inference call, but duplicate cost and latency remain charged. If future designs add external effects, their receipts and unknown outcomes require their own reconciliation; changing model vendors cannot solve that problem. Failover also is not independent protection when both paths rely on the same unavailable source store or compromised permission service.

## Does the advantage survive the bundle?

R21's packaging discussion distinguishes feature and usage access across offers. It does not prove that a particular bundle will win or lose. B03 already showed that a cheaper alternative can eliminate the price interval that sustains an offer. Here the defensible hypothesis is narrower: our evidence mapping, exception handling and control integration reduce correct-completion effort enough to justify their cost.

Test that hypothesis with the bundle's complete workflow, permitted exports and the customer's actual review effort. Reject it if the bundle satisfies the same contract below the total-cost threshold. A reusable evaluation corpus helps only when its rights, relevance and ability to detect consequential failures hold. Proprietary records do not automatically create an advantage. A common JSON interface can reduce adapter work while leaving retrieval tuning, evaluation, operations and user retraining expensive.

## Study assignment and reference card

Optional written work, with hints and solutions in [SDE_C06_answers.md](SDE_C06_answers.md):

1. Rebuild monthly/horizon ledgers and choices before and after the fee change.
2. Derive fee, horizon and bundle-labor thresholds; identify costs excluded by the premises.
3. Explain what the paired 100-case ledger proves and what it cannot prove.
4. Repair an export that has all document IDs but omits one referenced source revision; explain why a matching row count is insufficient.
5. Specify cutover, rollback and authority boundaries, and one observation that disproves the claimed advantage.

Reference card: own evidence identities and policy → expose a narrow inference contract → price all migration and recurring work → port the evaluation specification → rerun behavior and load checks → publish only complete revisions → judge the bundle by the complete customer job.

| Evidence | Inspected locator and use | Limitation |
| --- | --- | --- |
| [R15: Lewis et al., RAG](https://arxiv.org/pdf/2005.11401) | §2.2, printed p.3: query/document encoders and inner-product retrieval | Mechanism only; no arbitrary embedding compatibility claim |
| [R11: Saltzer and Schroeder](https://web.mit.edu/saltzer/www/publications/protection/Basic.html) | §I.A.3(c): complete mediation and cached authority | Design principle, not validation of this migration |
| [R21: Stripe / Patrick McKenzie](https://stripe.com/guides/atlas/saas-pricing) | Pricing and packaging for things with no physical form | Practitioner guidance, not supplier economics or demand data |
| Original synthesis | All tables, thresholds, traces and checks here | Hypothetical inputs, not observed production results |

Actual fees, export rights, retention requirements, rebuild time, error rates, operator capacity and customer handling remain application inputs. No essential blocker remains for producing this material. Next is Audit D across the completed curriculum; learner mastery remains unassessed.

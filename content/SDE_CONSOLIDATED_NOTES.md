# SDE Foundations — Consolidated Notes

This note compresses the library into a reusable engineering method. It is a map, not a replacement for the worked traces.

## 1. Define the job before optimizing it

A system can look better because its denominator changed. State the eligible population, task identity, output contract, deadline, quality rule and missing-outcome policy before comparing designs. Count offered work, unresolved work, retries and late results. Component accuracy, throughput or token cost is meaningful only after connecting it to a complete outcome.

Use [[SDE_F02|F02]] for probabilities and expected loss, [[SDE_F03|F03]] for fair measurement, and [[SDE_B02|B02]] for cost per useful result.

## 2. Name the invariant and the transition boundary

An invariant is a condition that must hold at every protected committed boundary. A correct transition checks its premises and changes protected state atomically. Checking before the boundary and acting later creates a race. A crash-safe write can still commit a decision based on stale information.

Ask:

- What state is protected?
- Which transition can change it?
- Which reads are premises of that transition?
- Can two actors make individually valid but jointly invalid decisions?
- Which alternate path bypasses the guard?

See [[SDE_F01|F01]], [[SDE_S03|S03]], [[SDE_C01|C01]] and [[SDE_S06|S06]].

## 3. Preserve identity across time

Logical object, revision, attempt, operation and business obligation are different identities. Keep immutable source bytes and exact revision references when later decisions must remain explainable. A digest can verify retrieved bytes but cannot replace the bytes. A “retry” with a new operation identity may duplicate an effect.

For an unknown outcome, reconcile the original identity before retrying. A historical receipt proves what happened; permission to read it and permission to create a new effect are separate questions.

See [[SDE_S02|S02]], [[SDE_S04|S04]], [[SDE_C01|C01]] and [[SDE_C06|C06]].

## 4. Separate proposal from authority

Model output, user input and tool observations are proposals or data. Authority comes from authenticated context and current policy. Enforce tenant, action, object, revision, epoch, evidence and slot conditions at the effect boundary. A model-supplied actor field is not identity. A timeout is not permission, and an availability target cannot authorize disclosure.

Use fail-safe defaults, complete mediation and least privilege as design checks. Test recovery tools, exports, repair scripts and administrative paths, not only the normal UI.

See [[SDE_S06|S06]], [[SDE_A05|A05]], [[SDE_C04|C04]] and [[SDE_C05|C05]].

## 5. Keep evidence stages distinct

A fact may exist in the corpus and still be absent from the index. A retrieved passage may be excluded from context. A cited passage may not support the claim. A supported claim may use a stale revision or be disclosed to the wrong principal.

Inspect the chain:

`available source → eligible source → retrieved candidate → supplied context → claim → supported output → permitted disclosure`

Evaluation should preserve these intermediate artifacts so a failure can be located. Retrieval makes evidence available; it does not guarantee use, truth or permission.

See [[SDE_A03|A03]] and [[SDE_C06|C06]].

## 6. Treat evaluation as a deployment model

Random rows are often not independent deployment cases. Revisions, templates, organizations, suppliers and reviewer queues can create leakage or interference. Freeze tuning before final evaluation. Use the same cases for paired comparisons when possible, and choose the assignment unit around spillovers.

Report uncertainty under the assumptions of the procedure. Randomization does not automatically justify every interval. Repeated retries of one case do not create independent evidence.

See [[SDE_F03|F03]], [[SDE_A01|A01]], [[SDE_A05|A05]] and [[SDE_C02|C02]].

## 7. Resource feasibility precedes performance claims

Track operations, bytes, working set, retained state, temporary workspace and queues separately. Memory feasibility does not establish latency. Throughput does not establish per-request deadlines. Average demand does not reconstruct bursts. Faster prompt processing may have little effect when decoding dominates.

For LLM serving, separate weights, KV state and other memory; state the configuration behind every byte estimate. Count all offered work and define the clock. “Autoscaling” is incomplete without startup and routing evidence.

See [[SDE_S01|S01]], [[SDE_S05|S05]], [[SDE_A04|A04]] and [[SDE_C03|C03]].

## 8. Price outcomes, not impressive components

Build mutually exclusive cost categories. Include failed attempts, review, support, idle purchased capacity, maintenance, setup, acquisition and dispute work where relevant. Divide by the unit the decision actually values. Cost per token, call or VM can improve while cost per verified timely result gets worse.

Customer capacity value is not automatically cash savings. Contribution is not profit. A positive average can hide a capacity tier or severe loss. A free bundled feature can still impose workflow labor.

See [[SDE_B01|B01]], [[SDE_B02|B02]], [[SDE_B03|B03]], [[SDE_C03|C03]] and [[SDE_C04|C04]].

## 9. Choose the least complex adequate autonomy

Autonomy describes who chooses the next step; authority describes what effects are permitted. A deterministic workflow may mutate state. A suggestion-only assistant may consume large human capacity. An action-taking agent can be acceptable only within an externally enforced action set, budget and effect boundary.

Apply gates in order:

1. Authority and evidence integrity.
2. Quality and deadline.
3. Capacity.
4. Expected loss and complete cost.
5. Simplicity and operational burden.

See [[SDE_A05|A05]] and [[SDE_C05|C05]].

## 10. Port the decision specification, then retest behavior

A common provider interface reduces adapter work but does not make retrieval, quality, latency, cost or permissions equivalent. Own source identities, grants, evaluation cases and effect receipts when those are central to the product. Treat indexes and caches as versioned derived state.

During migration, export and restore evidence, rebuild derived state under a new configuration identity, shadow without effects, publish only complete revisions, and retain rollback long enough to reconcile. Judge a bundle by the complete customer job.

See [[SDE_C06|C06]].

## The reusable decision template

For any architecture or product choice, write:

1. **Decision:** the action and owner.
2. **Complete job:** population, identity, output, deadline and success.
3. **Hard gates:** authority, evidence, safety, quality and capacity.
4. **Options:** credible complete systems under shared assumptions.
5. **Model:** resources, probabilities, consequences and costs.
6. **Trace:** one normal path, one failure and one counterexample.
7. **Changed constraint:** alter one premise and revise honestly.
8. **Falsifier:** evidence that overturns the recommendation.
9. **Unknowns:** inputs requiring measurement or stakeholder authority.

That template is the compact answer to the curriculum's central question.


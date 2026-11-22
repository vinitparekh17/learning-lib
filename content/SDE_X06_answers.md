# X06 — Worked AI release gates and checks

[Return to the lesson](SDE_X06.md). These answers reproduce invented inputs. Production gates need local losses, denominators, uncertainty and operational ownership.

## 1. Reject the hidden slice regression

The weighted baseline is:

`0.90(0.900) + 0.05(0.820) + 0.05(0.700) = 0.8860`.

The candidate is:

`0.90(0.915) + 0.05(0.740) + 0.05(0.720) = 0.8965`.

Global quality improves by 0.0105, or 1.05 percentage points. The state-specific slice falls by 0.08, or 8 points. A conjunctive gate requiring global non-regression **and** no critical slice decline worse than 2 points fails. Do not average the two gates into one score; the purpose of the slice limit is to prevent high-volume gains from purchasing concentrated loss silently.

Before using this gate, verify sufficient sample size, stable labels and that “state-specific” corresponds to a meaningful loss boundary rather than a post-hoc slice.

## 2. Stratify the disagreement investigation

State-specific disagreement is `1,600 / 5,000 = 32%`. The remainder is `2,400 / 95,000 ≈ 2.526%`. The global rate is 4%, but it neither locates the divergence nor says which model is correct.

Create separate adjudication strata: state-specific forms, low-quality scans and common documents. Sample enough from the state-specific stratum to estimate its harmful-disagreement rate rather than sampling uniformly from all requests. Within each stratum, include agreements as well as disagreements: identical wrong outputs would otherwise be invisible. Freeze the rubric, blind reviewers to model identity where feasible, record unresolved cases, and weight the final product estimate back to production prevalence only after reporting slice results.

## 3. Bound canary exposure

Let `f` be the exposed traffic fraction. Under the assumed excess harmful-decision rate:

`200,000 × f × 0.0015 ≤ 5`, so `f ≤ 0.016666…`, about 1.67%.

Launch below the bound because the 0.15-point excess is an estimate rather than a guarantee and harms may be correlated or unequally severe. Statistical detection also has delay: spending the entire daily loss budget before an alert is evaluated leaves no room for rollback latency. A high-severity action may require zero autonomous canary exposure and a human-review gate instead.

## 4. Respect outcome delay

Seven days at 20,000 decisions per day creates 140,000 candidate decisions before the first complete outcome cohort matures. A safe rule could hold the canary at or below a cumulative exposure cap until that cohort's risk-weighted outcome interval is inside the predeclared boundary.

Operational health remains a separate AND gate: errors, latency or cost can stop immediately, but green operations cannot promote. While waiting, manually adjudicate a risk-weighted sample and monitor a leading indicator only if its historical relationship to final loss has been validated. Join labels by immutable prediction ID and bundle version; exclude unresolved outcomes from neither numerator nor denominator without an explicit censoring rule.

## 5. Roll back the compatible RAG bundle

The release manifest should bind:

- embedding model and preprocessing version;
- index snapshot ID, corpus manifest and build code;
- reranker model and feature schema;
- prompt/template and policy version;
- generator/runtime version and decoding configuration;
- evaluation rubric, deployment time and owner;
- previous known-good bundle plus a tested traffic switch.

Shadow checks can compare retrieval overlap, required-passage recall on labeled traffic, unsupported-claim heuristics, schema validity, policy checks, latency, token/accelerator cost and divergence by language, tenant and document type. They cannot measure how candidate answers change user trust, follow-up questions, task success or downstream actions because users still see the primary answer.

The drill loads the previous complete bundle, routes synthetic and sampled live inputs through it, verifies feature/index compatibility, times the switch and confirms in-flight requests and caches carry explicit version identities. If the new index or prompt remains after a model-only rollback, the drill has not tested the real recovery path.

## Reproduce the gates

The deterministic checks below implement the lesson's invented arithmetic. They do not estimate uncertainty or infer a causal product effect.

```python
slices = {
    "common": (0.90, 0.900, 0.915),
    "state_specific": (0.05, 0.820, 0.740),
    "low_quality_scan": (0.05, 0.700, 0.720),
}

baseline = sum(share * old for share, old, new in slices.values())
candidate = sum(share * new for share, old, new in slices.values())
deltas = {name: new - old for name, (share, old, new) in slices.items()}

assert abs(baseline - 0.8860) < 1e-12
assert abs(candidate - 0.8965) < 1e-12
assert abs((candidate - baseline) - 0.0105) < 1e-12
assert abs(deltas["state_specific"] + 0.08) < 1e-12

global_pass = candidate >= baseline
slice_pass = all(delta >= -0.02 for delta in deltas.values())
assert global_pass and not slice_pass
assert not (global_pass and slice_pass)

state_disagreement = 1_600 / 5_000
other_disagreement = 2_400 / 95_000
global_disagreement = 4_000 / 100_000
assert state_disagreement == 0.32
assert abs(other_disagreement - 0.0252631578947) < 1e-12
assert global_disagreement == 0.04

daily_decisions = 200_000
assumed_excess_harm = 0.0015
daily_excess_budget = 5
max_fraction = daily_excess_budget / (daily_decisions * assumed_excess_harm)
assert abs(max_fraction - 1/60) < 1e-12

label_delay_days = 7
canary_per_day = 20_000
assert label_delay_days * canary_per_day == 140_000

print("PASS: aggregate/slice gate, shadow strata, exposure budget and label delay checked")
```

A complete answer separates compatibility, behavior and product-outcome evidence; treats each promotion as a new decision; and shows that rollback restores every coupled artifact. These checks do not record learner mastery.

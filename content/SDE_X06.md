# X06 — AI release gates under distribution shift

| Field | Value |
| --- | --- |
| ID / revision / date | X06 · 1.0 · 22 November 2026 |
| Prerequisites | F03 measurement, A01 generalization, A04 serving, C05 decision risk and X04 experiment choice |
| Capability developed | Build an AI release ladder that joins offline slice evidence, live shadowing, bounded user exposure, delayed outcomes and a rehearsed rollback into one decision. |
| Evidence | XR13–XR15. Primary paper and production passages below. |
| Experiment | Slice, shadow, exposure-budget and rollback checks in the [worked companion](SDE_X06_answers.md). |

## A better offline score is a hypothesis

A candidate claim-triage model improves validation accuracy from 88.6% to 89.65%. That is evidence about a saved dataset under one evaluator. Production adds different feature code, document mixtures, traffic, latency, user reactions and delayed claim outcomes. The release question is not “is 89.65 larger?” It is:

> Which bounded evidence permits the next increase in irreversible user exposure, and which signal returns traffic to the known-good bundle?

An AI release changes more than model weights. Identify a deployable bundle: model, feature transformation, tokenizer, prompt or policy, retrieval index, label mapping, runtime and configuration. Rollback must restore a compatible bundle. Reverting only the model while leaving a new feature encoding or index live may preserve the failure.

## Production case — Uber made safeguards part of the platform

Uber reports more than 400 active ML use cases, over 20,000 monthly training jobs and more than 15 million real-time predictions per second at peak. At that scale, a small regression can spread within minutes, while static tests cannot fully specify behavior learned from changing data. In the first half of 2025, the Michelangelo team rolled out platform mechanisms for data validation, backtesting, shadow deployments, controlled rollout, monitoring and rollback. [Uber, “Raising the Bar on ML Model Deployment Safety,” Introduction and “ML Model Safe Deployment Practices”](https://www.uber.com/sa/en/blog/raising-the-bar-on-ml-model-deployment-safety/)

Their candidate models process live shadow traffic without controlling user-facing predictions. Models that pass start with a small traffic slice; operational and prediction-quality signals are monitored, and threshold breaches can automatically restore the last known-good version. Uber reported shadow testing in more than 75% of critical online use cases when the article was published and said continuous validation reduced the time regressions lingered from days to hours. [Uber, same report, “Built for Adoption,” “Data Quality at Scale with Hue,” and “Continuous Validation”](https://www.uber.com/sa/en/blog/raising-the-bar-on-ml-model-deployment-safety/)

This documents a production decision and reported operational outcome, not universal thresholds. To transfer it, a team needs its own loss model, feature contracts, label delay, traffic slices, fallback behavior, compute headroom and evidence that the rollback bundle actually loads.

## A release ladder

Every stage should answer a different question. Passing one does not imply the next.

| Stage | Candidate exposure | Question answered | Example block signal |
| --- | ---: | --- | --- |
| 0 · Manifest | None | Can we identify and restore the complete compatible bundle? | Missing artifact lineage or rollback rehearsal |
| 1 · Offline slices | Saved data | Does quality meet absolute and relative gates on decision-relevant populations? | Any critical slice crosses its loss threshold |
| 2 · Replay/backtest | Historical production trace | Does the entire pipeline reproduce features, outputs, latency and costs? | Training-serving skew or capacity breach |
| 3 · Shadow | Live inputs, no candidate decisions | Can the candidate load and behave on current traffic without affecting users? | Runtime error, unexplained divergence or excess compute |
| 4 · Canary | Small stable user cohort | Do user-facing and delayed outcomes remain inside an exposure budget? | Guardrail breach or exhausted risk budget |
| 5 · Ramp | Increasing cohorts | Does evidence remain valid across time, region, caller and load? | Slice regression, drift or rollback degradation |
| 6 · Steady state | Full traffic | Is the model, data and outcome relationship still acceptable? | Staleness, skew or served-quality alert |

The Google ML Test Score paper separates these controls explicitly. It recommends absolute and relative release thresholds on important data slices; validation before serving; canarying because offline data cannot cover non-stationarity and serving incompatibility; a practiced rollback; and continued monitoring of input invariants, training-serving skew, model staleness, computing performance and served prediction quality. [Breck et al., 2017, Model 6, Infra 4 and 6–7, Monitor 2–7](https://research.google.com/pubs/archive/aad9f93b86b7addfea4c419b9100c6cdd26cacea.pdf)

## Aggregate improvement can conceal concentrated loss

Use an invented validation population:

| Slice | Share | Baseline supported decision | Candidate | Change |
| --- | ---: | ---: | ---: | ---: |
| Common documents | 90% | 90.0% | 91.5% | +1.5 pp |
| State-specific forms | 5% | 82.0% | 74.0% | −8.0 pp |
| Low-quality scans | 5% | 70.0% | 72.0% | +2.0 pp |

The weighted score moves from 88.6% to 89.65%, a gain of 1.05 percentage points. A release gate that requires every critical slice to decline by no more than 2 points rejects the candidate. This is not an argument that every small slice gets the same threshold. Slice selection and loss limits should follow product harm, legal obligations, volume and uncertainty. A slice with five examples cannot support a precise rate.

Fix slice definitions before inspecting the candidate where possible. Otherwise repeated slicing becomes another way to overfit the release process. Report denominators and uncertainty, not only percentages.

## Shadowing finds integration failures, not user outcomes

A shadow receives the same live input as the primary but its answer does not control the user experience. It can reveal:

- model or tokenizer load failures;
- feature-contract and online/offline skew;
- output divergence by stable slice;
- latency, accelerator memory and cost;
- policy or schema violations that can be evaluated without user action.

It cannot directly reveal behavior created by the candidate's own decisions. A ranking model changes what users see; an agent changes external state; a recommender changes future clicks and therefore future training data. The shadow observes inputs generated under the primary policy. Treat it as a live compatibility test, not a counterfactual product experiment.

Suppose 100,000 invented shadow requests produce 4,000 primary/candidate disagreements. State-specific forms are only 5,000 requests but contribute 1,600 disagreements: 32% in that slice versus about 2.53% elsewhere. The global 4% rate hides where investigation belongs. Disagreement itself is not error; adjudicate a stratified sample or join delayed labels.

## Distribution shift is a signal, not a verdict

Three different failures are often called drift:

- **Input shift:** the distribution of observed requests or features changes.
- **Relationship shift:** the same inputs map to different outcomes or losses.
- **Pipeline skew:** training and serving compute supposedly identical features differently.

An input alert can fire while quality remains acceptable, and quality can fall with little visible marginal-feature drift. Rabanser, Günnemann and Lipton evaluated multiple two-sample shift detectors across synthetic shifts. Their results favored classifier-output representations across their tested settings, but they also show representation reduction admits pathological false negatives and that some methods perform poorly with small samples. [Rabanser et al., NeurIPS 2019, Abstract, §3.1 and §5](https://proceedings.neurips.cc/paper/2019/file/846c260d715e5b854ffad5f70a516c88-Paper.pdf)

Use shift detection to trigger diagnosis, labeling or a hold. Do not automatically retrain on every alert or automatically promote because no alert fired. Track feature contracts, slice outcomes and the causal path from change to harm.

## Spend a canary risk budget

Canary traffic affects real users. Bound it with a loss budget rather than an arbitrary “10% rollout.”

For an invented service with 200,000 daily decisions, suppose the candidate may add 0.15 percentage points of harmful decisions and the release owner permits at most five excess harms per day while learning. At fraction `f`:

\[
200{,}000 \times f \times 0.0015 \le 5,
\]

so `f ≤ 1/60`, about 1.67%. This arithmetic only translates stated assumptions. The true excess is uncertain, rare harm may be more severe, and correlated failures can violate the average. Start below the ceiling and define an immediate kill signal.

Use stable cohort assignment so the same user or claim does not bounce between policies. Separate operational guardrails (errors, latency, cost) from model/product guardrails (supported decisions, policy violations, escalation, calibration). Choose both before launch.

## Delayed labels limit the ramp

If claim outcomes arrive seven days later, a 20,000-decision daily canary exposes 140,000 decisions before its first full label cohort matures. A green latency dashboard cannot authorize the next ramp. Options include:

- hold exposure until a complete outcome cohort matures;
- use a validated leading indicator with a known relationship to the delayed loss;
- manually adjudicate a risk-weighted sample;
- cap cumulative exposure and exclude high-loss actions;
- require reversible recommendations before allowing autonomous actions.

Label joins need stable prediction IDs, model/bundle version, feature snapshot, decision timestamp and outcome window. Without them, “online accuracy” can mix versions or omit unresolved outcomes.

## Rollback is an executable path

Before the canary, prove that the previous bundle is retained, loadable and compatible with current features and data. Record the maximum rollback time and test it under load. Decide what happens to in-flight work and external actions. A model rollback does not undo a denied claim, sent payment or changed training distribution.

For retrieval or agent systems, version the index, prompt, tool policy and model together. If the candidate writes new memory or calls a changed API, the safe response may be forward repair or feature disablement rather than model-only rollback.

## Practice

All traffic, quality, cost and harm values below are invented teaching inputs.

1. Reproduce the weighted baseline and candidate score for the three slices. Apply a gate requiring global non-regression and no critical slice decline beyond 2 percentage points.
2. Reproduce the shadow disagreement rates: 1,600 of 5,000 state-specific requests and 2,400 of the remaining 95,000. Design the next labeled sample without letting the large common slice dominate it.
3. Derive the maximum canary fraction for 200,000 daily decisions, an assumed 0.15-point excess harmful-decision rate and a budget of five excess harms per day. Name two reasons to launch below that fraction.
4. A label matures after seven days and the canary receives 20,000 decisions per day. Calculate exposure before the first complete outcome cohort. Design a ramp rule that cannot be authorized by latency alone.
5. Design a release manifest and rollback drill for a RAG assistant changing embedding model, index snapshot, reranker and prompt together. State which shadow signals are useful and which product outcomes require a canary.

## Evidence and deployment questions

| Source | Inspected locator | Application boundary |
| --- | --- | --- |
| XR13 · Breck et al., Google | [The ML Test Score](https://research.google.com/pubs/archive/aad9f93b86b7addfea4c419b9100c6cdd26cacea.pdf), Model 6, Infra 4 and 6–7, Monitor 2–7 | Production-readiness controls drawn from interviews and experience across real systems. It supplies tests, not universal metrics or thresholds. |
| XR14 · Wang, Wang and Li, Uber | [Raising the Bar on ML Model Deployment Safety](https://www.uber.com/sa/en/blog/raising-the-bar-on-ml-model-deployment-safety/), Introduction, “ML Model Safe Deployment Practices,” “Built for Adoption,” “Data Quality at Scale with Hue,” and “Continuous Validation” | Documents Uber's 2025 scale, chosen safeguards, adoption and reported time-to-detection improvement. It does not prove the same controls or rates fit another loss model. |
| XR15 · Rabanser, Günnemann and Lipton | [Failing Loudly](https://proceedings.neurips.cc/paper/2019/file/846c260d715e5b854ffad5f70a516c88-Paper.pdf), Abstract, §3.1 and §5 | Empirical comparison of shift detectors under studied datasets and perturbations. It demonstrates useful methods and failure boundaries, not a universal detector or quality guarantee. |

Before promoting a real model, obtain the exact deployment bundle, feature and output contracts, evaluation-set lineage, critical slice definitions, outcome delay, exposure loss budget, stable cohort unit, resource envelope, alert ownership and a timed rollback rehearsal. No learner answer or mastery level is inferred from opening this lesson.

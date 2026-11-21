# X04 — Information gain and choosing the next experiment

| Field | Value |
| --- | --- |
| ID / revision / date | X04 · 1.0 · 21 November 2026 |
| Prerequisites | F02 base rates, F03 measurement and B01 customer evidence |
| Capability developed | Choose the next measurement by how well its possible outcomes distinguish live explanations and improve the next decision. |
| Evidence | XR07–XR09. Primary passages and scope below. |
| Experiment | Bayesian updates, entropy, decision value and cost checks in the [worked companion](SDE_X04_answers.md). |

## A measurement can be accurate and still be useless

An AI retrieval system's supported-answer rate falls from 78% to 62%. A dashboard confirms the fall precisely. That measurement establishes the symptom, but it does not identify whether the retriever stopped finding evidence, the generator stopped using available evidence, or the evaluation labels changed. If all three explanations predicted the same dashboard result, repeating it teaches little.

The next experiment should have outcomes that the competing explanations predict differently. Write the hypotheses and predicted outcomes before collecting more data. This prevents an attractive result from rewriting the question after the fact.

For a discrete set of hypotheses with probabilities `p(h)`, uncertainty in bits is

\[
H(H)=-\sum_h p(h)\log_2 p(h).
\]

Shannon introduced this entropy as a measure of choice under a probability distribution. With base two, the units are bits. The maximum for two possibilities occurs when both are equally likely; certainty has zero entropy. [Shannon 1948, part I, §§1 and 6](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)

An experiment `E` can produce outcomes `y`. Its expected information gain is the prior entropy minus the expected posterior entropy:

\[
\operatorname{EIG}(E)=H(H)-\sum_y p(y)H(H\mid y).
\]

Lindley applied Shannon's measure to experiments by comparing knowledge before and after an observation, then averaging over possible observations. He also distinguished experiments intended to gain knowledge from decision problems involving losses. [Lindley 1956, pp. 986–990, especially definitions 1–2](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-27/issue-4/On-a-Measure-of-the-Information-Provided-by-an-Experiment/10.1214/aoms/1177728069.full)

## Compare experiments before running them

Use this invented incident model:

| Hypothesis | Prior | Meaning |
| --- | ---: | --- |
| `R` | 0.50 | Retrieved evidence is missing or wrong |
| `G` | 0.30 | Evidence is present but generation or prompting fails |
| `L` | 0.20 | The evaluation labels or scoring pipeline drifted |

For each candidate experiment, estimate the probability of its named positive outcome under each hypothesis. These likelihoods are invented teaching inputs. In production, derive them from historical incidents, calibrated simulations or a pilot and retain uncertainty about them.

| Candidate | Positive outcome | `P(+|R)` | `P(+|G)` | `P(+|L)` | Cost |
| --- | --- | ---: | ---: | ---: | ---: |
| A · inspect evidence on sampled failures | Evidence required by the label is absent | 0.80 | 0.20 | 0.50 | 20 engineer-minutes |
| B · replay with a stronger generator | Supported-answer score recovers | 0.10 | 0.80 | 0.30 | 90 engineer-minutes plus inference |
| C · repeat the aggregate evaluation | Score remains low | 0.70 | 0.60 | 0.80 | 10 engineer-minutes |

Candidate A has expected information gain of about 0.212 bits. A positive result moves the posterior to approximately `(R=.714, G=.107, L=.179)`; a negative result moves it to `(R=.227, G=.545, L=.227)`. Candidate B yields about 0.307 bits, but costs more. Candidate C yields only about 0.017 bits because all three explanations commonly predict another low score.

Dividing bits by minutes can expose obviously weak measurements: A provides roughly 0.0106 modeled bits per engineer-minute, B 0.0034 and C 0.0017. This is a rough scheduling aid, not a universal utility function. One bit about an irrelevant parameter may be worth less than a small probability shift across a deployment threshold.

## Information is not the decision

Suppose choosing the wrong repair costs 100 equal loss units and the correct repair costs zero. Before testing, the best action is to address `R`, with expected loss 50. After each outcome, choose the repair for the most probable hypothesis.

Candidate A reduces expected loss to 36, so its expected value of sample information is 14 loss units before experiment cost. Candidate B reduces it to 31, worth 19 loss units. Candidate C changes posterior probabilities slightly but leaves `R` as the best action after either outcome. Its decision value is zero under this simplified equal-loss model.

The distinction matters:

- Use expected information gain when reducing uncertainty is itself the goal or when future decisions are not yet specified.
- Use expected decision-loss reduction when the action set, stakes and costs can be stated.
- Subtract experiment time, monetary cost, user exposure and delay cost before choosing.
- Prefer a fast reversible probe when a delayed decision is expensive, even if a slower study eventually returns more information.

The probabilities do not become objective because they appear in a formula. Record whose beliefs they represent, what evidence informed them and how sensitive the ranking is to plausible alternatives.

## AI engineering decision — predict a large run from small runs

The GPT‑4 project faced an expensive constraint: extensive model-specific tuning was infeasible at the scale of the final training run. The team therefore developed infrastructure and optimization methods intended to behave predictably across scales. They fitted a power-law loss model using runs with the same methodology and at most 10,000 times less compute. The prediction was made shortly after the final run started without partial results, and the report says it predicted final loss with high accuracy. [GPT‑4 Technical Report, §3 and §3.1](https://cdn.openai.com/papers/gpt-4.pdf)

They also registered predictions for a subset of HumanEval before training completed, extrapolating from models using at most 1,000 times less compute. Predictions were accurate for the reported subset and almost as good across five other difficulty buckets, with an exception on the easiest bucket. The report explicitly notes that some capabilities remained hard to predict. [GPT‑4 Technical Report, §3.2 and figures 1–3](https://cdn.openai.com/papers/gpt-4.pdf)

The engineering choice was not merely “train a smaller model.” The small runs preserved the training methodology, the team selected metrics with measurable scale behavior, fitted a relationship, and tested a registered prediction against a held-out full run. This converted many cheaper experiments into evidence about a decision too expensive to repeat freely.

To transfer the approach, verify that the proposed small experiment preserves the mechanism expected to scale. Track residuals across scales, prediction intervals, changes in data and optimizer behavior, and tasks that violate the fitted relationship. Register the prediction and decision threshold before observing the target run. A reliable loss curve does not prove reliable safety, factuality or product utility.

## A practical experiment card

Before spending the next hour or compute budget, write:

1. **Decision:** What action and deadline will this result inform?
2. **Live hypotheses:** Which explanations remain plausible, with rough priors?
3. **Outcome model:** What would each hypothesis predict for every material result?
4. **Update rule:** How will the result change belief and action?
5. **Cost and exposure:** What resources, users and opportunity costs are involved?
6. **Validity boundary:** Which mismatch would make the result irrelevant to production?
7. **Stop rule:** What result is sufficient to act, escalate or abandon the line of inquiry?

An experiment that has no credible path from result to changed belief or changed action is instrumentation, observation or ritual. It can still be useful, but it should not displace a discriminating test.

## Practice

All probabilities, costs and incident details below are invented.

1. Reproduce candidate A's positive-outcome probability, both posteriors and expected information gain.
2. Compare A and B by information gain per engineer-minute. Then explain why this ratio can rank the wrong experiment.
3. Show that candidate C has positive information gain but zero decision value under the equal-loss repair model.
4. Design the first experiment for a RAG system whose answer quality fell after an index and prompt release happened together. State hypotheses, predicted outcomes, cost and stop rule.
5. A small model predicts final training loss accurately but misses a safety capability. Identify which transfer premise failed and which additional experiment is needed.

## Evidence and deployment questions

| Source | Inspected locator | Application boundary |
| --- | --- | --- |
| XR07 · Claude E. Shannon | [A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf), part I, §§1 and 6 | Defines entropy for a probability distribution. Applying it to engineering hypotheses requires an explicit probabilistic observation model. |
| XR08 · D. V. Lindley | [On a Measure of the Information Provided by an Experiment](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-27/issue-4/On-a-Measure-of-the-Information-Provided-by-an-Experiment/10.1214/aoms/1177728069.full), pp. 986–990, definitions 1–2 | Connects prior-to-posterior change with expected information and separates knowledge from decision-loss formulations. The incident likelihoods are original teaching assumptions. |
| XR09 · OpenAI | [GPT‑4 Technical Report](https://cdn.openai.com/papers/gpt-4.pdf), §3, §§3.1–3.2 and figures 1–3 | Documents a large-scale AI engineering choice, successful predictions and exceptions. It does not establish that every capability or training regime scales predictably. |

Before acting on an experiment ranking, inspect sensitivity to the priors and likelihoods, verify the result can arrive before the decision deadline, and check that the sampled population, traffic, data, model and evaluation correspond to the production decision.

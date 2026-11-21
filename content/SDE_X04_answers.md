# X04 — Worked experiment choices and checks

[Return to the lesson](SDE_X04.md). The calculations are only as useful as the hypotheses, likelihoods, actions and losses supplied to them.

## 1. Update candidate A

The invented prior is `(R=.50, G=.30, L=.20)`. Candidate A uses likelihoods `(.80, .20, .50)` for the result “required evidence is absent.”

The positive-outcome probability is

\[
P(+)=.50(.80)+.30(.20)+.20(.50)=.56.
\]

Bayes' rule gives the positive posterior `(0.7143, 0.1071, 0.1786)`. For a negative result, use complementary likelihoods `(.20, .80, .50)` and `P(-)=.44`, producing `(0.2273, 0.5455, 0.2273)`.

Prior entropy is about 1.4855 bits. Positive and negative posterior entropies are about 1.1358 and 1.4486 bits. Therefore

\[
\operatorname{EIG}(A)=1.4855-[.56(1.1358)+.44(1.4486)]\approx .2120\text{ bits}.
\]

## 2. Compare information per minute

Candidate B has likelihoods `(.10, .80, .30)`. Its positive outcome has probability .35 and its expected information gain is about .3067 bits. A yields `.2120/20 ≈ .0106` modeled bits per engineer-minute. B yields `.3067/90 ≈ .0034`, so A is the efficient first probe under this narrow ratio.

The ratio ignores asymmetric incident losses, result latency, inference spend, reversibility and whether an experiment crosses a decision threshold. If B is the only test that can authorize a safe rollback, its decision value can dominate. Bits measure uncertainty reduction in the stated hypothesis model, not business or safety utility.

## 3. Separate information from decision value

Candidate C uses likelihoods `(.70, .60, .80)` and has positive expected information gain of about .0169 bits. Its positive posterior is approximately `(R=.507, G=.261, L=.232)`. Its negative posterior is approximately `(R=.484, G=.387, L=.129)`. `R` remains the most probable hypothesis for either outcome.

With zero loss for the correct repair and 100 for any wrong repair, choosing `R` before the test has expected loss `100 × (1-.50)=50`. Candidate C never changes the chosen repair, so averaging its posterior losses returns 50. Its expected value of sample information is zero before testing costs.

Candidate A changes the selected repair to `R` after a positive and `G` after a negative. Expected remaining loss is `100 × [.56(1-.7143)+.44(1-.5455)] = 36`, worth 14 loss units before cost. Candidate B similarly leaves expected loss 31, worth 19.

## 4. Design the first RAG experiment

One defensible card uses three hypotheses: the new index omits required evidence, the new prompt fails to use present evidence, or the labeled evaluation sample changed. Freeze the failing request set and retrieve with old and new indexes while keeping the generator and prompt fixed. For each request, record whether the labeled supporting passage appears in the candidate set and at which rank.

Predict a large coverage drop only under the index hypothesis, similar coverage under the prompt hypothesis, and disagreement between labels and source documents under the label hypothesis. Stop when the confidence interval around the coverage difference is narrow enough to cross the rollback threshold, or immediately if a deterministic manifest mismatch is found. The inputs, threshold and sample size must come from the real service; none are supplied here.

## 5. Respect the transfer boundary

The small-run experiment preserved enough of the optimization mechanism to predict loss, but safety capability did not share the fitted scale relationship or the evaluation could not estimate it reliably at small scale. Add a capability-specific evaluation with observable signal at smaller scales, adversarial cases and a registered extrapolation rule. If no useful precursor exists, reserve a staged larger-scale checkpoint or deployment gate instead of treating loss prediction as a proxy.

## Reproduce the calculations

The following checks use the lesson's invented priors, likelihoods, equal-loss actions and costs.

```python
from math import log2

prior = (0.50, 0.30, 0.20)

def entropy(distribution):
    return -sum(p * log2(p) for p in distribution if p)

def evaluate(likelihoods):
    positive = sum(p * likelihood for p, likelihood in zip(prior, likelihoods))
    post_positive = tuple(p * likelihood / positive for p, likelihood in zip(prior, likelihoods))
    post_negative = tuple(
        p * (1 - likelihood) / (1 - positive)
        for p, likelihood in zip(prior, likelihoods)
    )
    expected_posterior_entropy = (
        positive * entropy(post_positive)
        + (1 - positive) * entropy(post_negative)
    )
    information_gain = entropy(prior) - expected_posterior_entropy
    remaining_loss = 100 * (
        positive * (1 - max(post_positive))
        + (1 - positive) * (1 - max(post_negative))
    )
    value_of_information = 100 * (1 - max(prior)) - remaining_loss
    return positive, post_positive, post_negative, information_gain, value_of_information

a = evaluate((0.80, 0.20, 0.50))
b = evaluate((0.10, 0.80, 0.30))
c = evaluate((0.70, 0.60, 0.80))

assert abs(entropy(prior) - 1.4854752972) < 1e-10
assert abs(a[0] - 0.56) < 1e-12
assert all(abs(x - y) < 1e-4 for x, y in zip(a[1], (0.7143, 0.1071, 0.1786)))
assert all(abs(x - y) < 1e-4 for x, y in zip(a[2], (0.2273, 0.5455, 0.2273)))
assert abs(a[3] - 0.2120450453) < 1e-10
assert abs(b[3] - 0.3067336503) < 1e-10
assert abs(c[3] - 0.0168572114) < 1e-10
assert abs(a[4] - 14) < 1e-10
assert abs(b[4] - 19) < 1e-10
assert abs(c[4]) < 1e-10
assert round(a[3] / 20, 4) == 0.0106
assert round(b[3] / 90, 4) == 0.0034
assert round(c[3] / 10, 4) == 0.0017
```

A complete answer states how each hypothesis predicts each possible result, updates all outcomes rather than only the hoped-for one, and connects the posterior to an action and stop rule.

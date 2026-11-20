# Audit A — Foundation packs and resource reasoning

| Field | Value |
| --- | --- |
| ID / revision / date | Audit A / 1.0 / 2026-11-04 |
| Scope | Runs 02–06, F01, B01, F02, F03, S01 and all five answer companions |
| Authority | SDE_Foundations_Scheduled_Prompt.md and SDE_Foundations_Library_v1.md, latest saved copies |
| Method | Primary-passage rechecks, derivation review, executed reproduction blocks, exercise and prerequisite review |
| Outcome | Two explanatory repairs applied. No remaining blocker to F04. |
| Boundary | Artifact review, not learner assessment or independent external certification |

## Findings and repairs

| ID | Original issue | Evidence and correction | Affected artifact | Remaining uncertainty |
| --- | --- | --- | --- | --- |
| A-01 | The t-interval paragraph used “appropriate t multiplier” and “reasonably well-behaved differences” without a usable prerequisite bridge or precise supporting reference. It could encourage treating randomization as sufficient for the interval's sampling model. | Added definitions of pair differences, standard deviation, standard error, degrees of freedom, and repeated-sampling coverage. Added R24, NIST §1.3.5.2. Distinguished the normal independent-difference model from an approximation for bounded team rates, and a randomization test of the sharp null from an average-effect interval. | SDE_F03.md, 1.0 → 1.1; SDE_SOURCES.md, 1.5 → 1.6 | Real pair count, dependence, heterogeneity, and variance must be examined before using the proposed interval. No interval is estimated from real teams. |
| A-02 | S01 defined r as an operation rate and b as sustained bandwidth before asserting a runtime lower bound. A reader could substitute measured throughput from a different workload and mistake a planning estimate for a bound. | Made r and b explicit upper bounds on available rates for the task. Required D to count necessary traffic across the specified boundary. The argument is W ≤ rT and D ≤ bT, hence T ≥ max(W/r,D/b). | SDE_S01.md, 1.0 → 1.1 | Real sustained rates and required traffic remain unmeasured. The cache simulator supplies no wall-clock prediction. |

Both repairs preserve the original exercise contracts and numerical answers. No core pack was regenerated. The unchanged companions remain revision 1.0 and are compatible with their revised cores. Earlier “Audit A pending” phrases in unchanged files are historical status notes; this report and the current index are authoritative for audit status.

## Results by pack

| Pack | Review and counterexample | Executed checks | Result |
| --- | --- | --- | --- |
| F01 | Check-before-insert invariant, finite termination, expected versus amortized bounds, key-size assumptions, exact-history limits, and concurrency boundary. Constant hashing and forgetting old keys still defeat unconditional claims. | All 3,280 sequences of lengths 0–7 over three values; witness checks; formula counts through n=2,000; collision, ordering, and forgetting examples. | Pass within the stated abstract model. Tests are bounded and do not replace the proof. |
| B01 | Episodes versus independent customers, operator versus budget authority, released capacity versus cash savings, and custom payment versus repeatable demand. Four-minute baseline reverses the apparent benefit. | Both labor scenarios, onboarding allocation, and values ₹1,950 and −₹450 per week. | Pass. Interview quotas and decision gates remain original teaching choices, not validated market thresholds. |
| F02 | Conditional denominators, unchanged detector-rate premise, expected-loss threshold, perfect/imperfect review, and aggregate-versus-subgroup calibration. | Three 10,000-record tables, Bayes reconstruction, 1,001 probability-grid points, and exact review-boundary ties. | Pass. No real prevalence, reviewer performance, or calibration claim. |
| F03 | Workload-mix reversal, paired outcomes, team versus case units, leakage, missing outcomes, stopping rule, and inference scope. | −13-point dashboard difference; +5-point standardized difference at two mixes; 21 discordant cases; cost/budget and deadline examples. | Pass after A-01. The live protocol remains a proposal requiring design-specific validation. |
| S01 | Virtual versus physical placement, translation versus data caching, cache capacity, field versus fill bytes, and throughput versus latency. | Three layouts over two passes, two-line-cache variant, finite pointer traversal, sums, translation to address 456, batch cost/latency and k=8 deadline boundary. | Pass after A-02. Counts establish the hypothetical model only. |

All five embedded Python reproduction blocks ran successfully during this audit. They were executed in separate namespaces to avoid cross-file variable contamination. Existing tests were rerun because this is the scheduled audit, not because a new hardware experiment was conducted.

## Primary passages rechecked

These are targeted checks of consequential claims. They are not exhaustive rereadings of every cited book or paper. Prior detailed locators remain in the packs and source register.

| Source | Reopened passage | Audit use |
| --- | --- | --- |
| R01 | [MIT 6.006 lecture 1](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/477c78e0af2df61fa205bcc6cb613ceb_MIT6_006S20_lec1.pdf), p. 2 correctness/efficiency; [lecture 4](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ce9e94705b914598ce78a00a70a1f734_MIT6_006S20_lec4.pdf), pp. 3–4 chaining/universal/dynamic | Checked model qualifications and worst-case collision counterexample. Historical timing examples were not adopted. |
| R19 | [YC primary transcript](https://www.ycombinator.com/blog/startup-school-week-1-recap-kevin-hale-and-eric-migicovsky/), Migicovsky 17:03–20:25 and 30:31–33:44 | Checked past-specific questions, listening, cost, frequency, budget, and authority. Practitioner scope retained. |
| R02 | [Author PDF](https://mml-book.github.io/book/mml-book.pdf), draft 2024-01-15, §§6.2.1 pp. 178–180, 6.3 pp. 184–185, 6.4.1 p. 187 | Inspected conditional-count definitions, product/Bayes rules, and discrete expectation. Web size failure repaired by author-URL download and text extraction. |
| R23 | [Guo et al.](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf), §2 PDF p. 2, equation 1 and reliability diagrams | F02 explicitly distinguishes predicted-class confidence from its analogous binary-event formulation. No benchmark extrapolation. |
| R03 | [Microsoft pre-experiment article](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/), hypothesis/metrics and randomization-unit sections | Rechecked interference and unit-selection rationale. Does not itself justify every inferential formula. |
| R13 | [Author Python notebook](https://github.com/intro-stat-learning/ISLP_labs/blob/stable/Ch05-resample-lab.ipynb), Validation Set Approach and boot_SE | Inspected split construction and sampling with replacement in the raw notebook. Supplier resampling remains an explicitly labeled application. |
| R04 | [Chapter 19](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf), §19.2 pp. 3–5; [chapter 21](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys.pdf), §21.2 p. 3 | Rechecked translation reuse and resident-page TLB-miss handling. S01 preserves its separate invented machine assumptions and updated-chapter version caveat. |
| R24, added | [NIST/SEMATECH §1.3.5.2](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm), interval definition and interpretation | Supports the mean-interval formula and coverage explanation added in A-01. |

## Prerequisites, exercises, and continuity

The five packs each contain six exercises with matching hints and worked answers, for 30 reviewed exercise–answer pairs. The questions ask for explanations or decisions as well as calculations. Their criteria describe useful future answers and do not imply that the learner has answered them.

F01 introduces sets, prefix notation, induction, and growth notation before using them. B01 defines segment, hypothesis, and commitments and separates unit conversions from business evidence. F02 introduces events and conditional denominators before Bayes and expected loss. F03 reuses those denominators and now gives the missing uncertainty bridge. S01 introduces bytes, lines, pages, units, and machine assumptions before tracing accesses. F04 remains the next planned mathematical bridge, rather than an assumed completed prerequisite.

The recurring document-service examples remain fictional. No interviews, live team trial, measured hardware speedup, or learner mastery was introduced during the audit. The paired replay and the observational dashboard in F03 are separate constructed datasets; their compatible totals do not establish a causal connection.

Latest copies of the operating prompt, curriculum, index, source register, ten pack/answer files were retrieved. Exact-title lookup found no existing audit report. Companion Markdown links resolve to the retrieved files. Index IDs match the retrieved identities. Corrections replace the existing F03 and S01 identities. The audit and corrected files are saved before the index advances.

## Residual questions and next work

No blocking mathematical or continuity issue remains in this audit's scope. Production decisions still need workload distributions, reliable labels, actual costs, independent teams, customer commitments, and machine measurements. Those application unknowns are preserved rather than filled with invented observations.

Next is Run 08, F04 — Linear algebra, calculus, and optimization as working tools. Inspect the appropriate R02 passages afresh, explain shapes and derivatives, and produce the core pack and separate answers. The program remains in progress.

## Revision history

- 1.0 — 2026-11-04. Targeted source and derivation audit of five foundation packs, two explanatory repairs, successful reproduction checks, and continuity review.

# Sources, graph context, and novelty boundary

Checked live on 2026-09-22.

## Primary source

John Jones and William B. Kinnersley,
[The directional localization game on graphs](https://arxiv.org/abs/2609.01745),
arXiv:2609.01745v1, 1 September 2026;
[full text](https://arxiv.org/html/2609.01745v1).
Section 2.1 gives the full-feedback response and one-edge movement rules.
Section 6, Question 6.4, asks whether any graph has full-feedback
localization number greater than two. Our parameter is instead the
optimal number of rounds with **one** cop in a sparse random graph.

The paper treats several deterministic graph classes and graph-parameter
bounds. It does not state the random adaptive capture-time hierarchy proved
here. Classical distance-only localization, partial directional feedback,
and full directional feedback have different information and cannot be
identified when importing results.

## Prior campaign source

- [Universal one-round resolution](https://github.com/helgithorskarp/math_results/tree/main/probabilistic_combinatorics/full_feedback_phase_diagram)
  determines the probability that every vertex is a resolving initial probe.
- [Appearance of resolving initial probes](https://github.com/helgithorskarp/math_results/tree/main/probabilistic_combinatorics/first_full_feedback_resolvers)
  gives a marked Poisson law near `np^2=log n` for existence of at least one
  such probe. It explicitly leaves adaptive multi-round questions open.

Neither result is used as an analytic lemma in the present self-contained
proof. The overlap consists of the game definition and the useful viewpoint
of common-neighbor codes. The new work controls whole moving-robber walks,
and makes the lower bound uniform over graph-dependent adaptive policies.

The graph-first selector inspected the full-feedback root
`bafkreie7igg6gdzysqnw5nml6glmbtdsbecajgf6qsxjjbiubjsvn6yxfm`
and its incoming results and reviews, including the two preceding findings
`bafkreibkdrllrxnon5kgsxigsx7hei7emxr7f2227ko2sn6yeizvbecwuu` and
`bafkreihidep32xl4mcqn6odvj7oy5tb5ou2h4nprbhzgbxdjf6dzsmkzle`.
The active team checkpoints concerned distinct targets.

## Search scope and unresolved cases

Live searches combined “full-feedback”, “directional localization”,
“random graphs”, “Erdos-Renyi”, and related wording, followed by a fresh
check of the primary article. Together with the bounded committed graph
refresh, these found no matching constant-round adaptive theorem. This
supports novelty relative to the searched sources only. It is not an
exhaustive priority claim, independent peer review, or a claim about every
possible preprint.

The result gives exact high-probability round counts for every fixed
`c>1/2` away from the discrete boundary constants. At a boundary it gives
only two possible adjacent round counts. It does not determine critical
windows, handle `c<=1/2`, allow `r` to grow with `n`, or decide whether any
graph needs more than two full-feedback cops.

# Literature and graph alignment

Checked against primary sources on 2026-09-22. A bounded negative search is
not a historical-priority proof.

1. **Jones and Kinnersley, The Directional Localization Game on Graphs**,
   [arXiv:2609.01745](https://arxiv.org/html/2609.01745), Section 2.1 and
   Question 6.4. This is the source of the full-feedback rule and the
   adaptive game. Its final question asks whether the adaptive parameter
   can exceed two. Our theorem concerns an initial single probe and makes
   no claim to settle that question. A successful initial probe implies
   adaptive localization number one; the converse need not hold.

2. **Krivelevich and Zhukovskii, Reconstructing random graphs from distance
   queries**, [arXiv:2404.18318](https://arxiv.org/html/2404.18318).
   Its introduction explicitly uses binomial common-neighbor counts and
   the scale `np^2=2 log n+log log n+omega(1)` for every nonedge to have at
   least two common neighbors. These basic codegree facts are prior art.
   Distance-query reconstruction is a different observation model.

3. **Earlier Discovery Net random certificate**, graph artifact
   `bafkreifswkxv7uwfe5ajuvw7lqsikg52qjxzoonzswbkge6sgveizvsfka`:
   [published source](https://github.com/njallskarp/math_source_code_open/tree/main/full_feedback_directional_random_graphs).
   It gives the exact finite probability of distinct codes of size at least
   two and a broad sufficient random-graph regime. The conditioned-code
   representation and its elementary symmetric-polynomial formula are
   credited to that contribution. Our rare-event calculation allows one
   empty two-hop code and controls its genuine distance-three response.

4. **Completed universal phase diagram**, graph artifact
   `bafkreibkdrllrxnon5kgsxigsx7hei7emxr7f2227ko2sn6yeizvbecwuu`:
   [source and proof](https://github.com/helgithorskarp/math_results/tree/main/probabilistic_combinatorics/full_feedback_phase_diagram).
   That result asks whether *every* vertex resolves, and proves three
   transitions over the full density range. Here the quantifier is
   existence of *one* resolving vertex. Its sparse window has a different
   leading scale, and its proof needs multiplicative joint estimates for
   rare successful probes, including a distance-three mark. We do not
   claim a further universal phase transition.

The graph problem anchoring this selection is
`bafkreie7igg6gdzysqnw5nml6glmbtdsbecajgf6qsxjjbiubjsvn6yxfm`.
Its bounded incoming neighborhood, the random-certificate descendants,
the universal law, and current team checkpoints were inspected. No matching
existential marked-Poisson result or active competing target was found.

Targeted live searches included “directional localization Poisson”,
“full-feedback threshold graph localization”, “one-round full-feedback
random”, and common-neighbor rare-event variants. The primary paper and
existing graph contributions were inspected rather than treating missing
search results as evidence of novelty. Searches found no prior statement
of the particular critical window, its factor-two distance-three correction,
or the joint eccentricity marks. These are the proposed new contributions;
Chernoff bounds, occupancy calculations, and the factorial-moment method
are standard tools. Independent review is pending.

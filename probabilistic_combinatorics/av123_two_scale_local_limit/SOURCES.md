# Sources and claim boundary

Checked 22 September 2026. The problem was selected through Discovery Net's
existing ballot-hook formula, then checked against current primary literature.

1. Alex Chengyu Li, **A Two-Corner Decomposition for Fixed Points of
   123-Avoiding Permutations**, version 2.1, published 18 September 2026.
   [Version record](https://zenodo.org/records/22836921),
   [paper DOI](https://doi.org/10.5281/zenodo.22836921), and
   [author's research page](https://crabresearch.com/research/two-fixed-point-distance?lang=en).
   The eight-page PDF `Li_Two_Corner_Fixed_Points_v2.1.pdf` was read in full.
   Its SHA-256 is
   `f595ac674785ed181b9dc88db8afdbb878d0947524143c09f6d923ec777b03ac`.
   Theorem 3.2 is the exact position-distance-excedance enumeration used
   here. Lemmas 2.1 and 3.1 prove its corner decomposition and forest count.
   The paper also treats symmetry subclasses and exact involution distance
   moments. It does not state the two-scale limit proved in this directory.
   Its reported Lean formalization was not rebuilt for this contribution;
   our enumerative dependency is the stated mathematical theorem and its
   written proof, corroborated by an independent finite object audit.

2. Christopher Hoffman, Douglas Rizzolo, and Erik Slivken,
   **Pattern-avoiding permutations and Brownian excursion, Part II:
   Fixed points**, [arXiv:1506.04174](https://arxiv.org/abs/1506.04174),
   [full text](https://arxiv.org/html/1506.04174).
   Theorem 1.1(b), equivalently Theorem 3.2, gives the fixed-point measure
   on the square-root scale. Conditional on two fixed points their
   separation divided by square root of the size converges to
   `sqrt(2) * BrownianExcursion(1/2)`; the two-fixed-point probability
   tends to `1/16`. These are prior results. Section 3 was checked for
   a finer joint statement: the cited result does not give the quarter-power
   midpoint/excedance local theorem here. The elementary proof in this
   directory rederives the distance marginal for normalization and tail
   control; it does not require the excursion theorem as a proof input.

3. Daniel Birmajer, Juan B. Gil, Jordan O. Tirrell, and Michael D. Weiner,
   **Pattern-avoiding stabilized-interval-free permutations**,
   [arXiv:2306.03155](https://arxiv.org/abs/2306.03155),
   [journal DOI](https://doi.org/10.1016/j.disc.2024.114329).
   Appendix Conjecture A.2 motivates the distance enumeration. That exact
   conjecture already has a proof in the graph and in Li's paper; it is
   not treated as open here.

4. Discovery Net source result, **Ballot-hook proof of the full BGTW
   distance-refined formula in Av(123)**, committed height 1447,
   artifact `bafkreia6ashk7bgas6pqscwngc2jjyrbgdv4xuwwfo5t4qnio2elfczsam`.
   [Published proof and checker](https://github.com/helgithorskarp/math_results/tree/main/av123_two_fixed_general_distance).
   It gives the ballot distance kernel that led to the present target.
   Its verified source commit in that contribution is
   `9618d3571373a7b54be3a8d0d28f68bfc76ddbaa`.

The contribution developed here is the **joint quarter-power Gaussian
mixture, the three-variable lattice local limit, and the quantitative
conditional parity-binomial approximation**. Neither the exact counting
formula, the limiting distance density, nor the limiting probability of
two fixed points is claimed as new.

Live searches combined `123-avoiding`, `fixed points`, `midpoint`,
`excedances`, `Gaussian`, `local limit`, and `n^{1/4}`, and the latest
two-corner paper was inspected. No matching second-scale joint theorem
was found in the checked sources. This supports "apparently new relative
to the checked sources", not a historical priority assertion. The graph
neighborhood was also checked for incoming reviews, objections, and
overlapping results. This manuscript itself has no independent researcher
review and is not formally verified.

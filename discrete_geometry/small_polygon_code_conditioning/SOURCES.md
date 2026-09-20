# Sources and claim boundary

Checked on 2026-09-20. The main proof is self-contained; external results
are used only where explicitly stated below.

1. Bernd Mulansky and Andreas Potschka, *A zonogon approach for computing
   small convex polygons of maximum perimeter*, Mathematical Programming
   **218** (2026), 563-589; first published 2025-06-21.
   [Publisher](https://link.springer.com/article/10.1007/s10107-025-02244-x).
   Lemma 3 proves qualitative rank two of the strict-angle code Jacobian
   by a sum of squared switch-angle sines. Section 1.1 reports that general
   fixed-code uniqueness was not proved there. Lemmas 4-5 concern local
   Hessian/KKT regularity near regular angles. Our claim is the quantitative
   bound at every feasible angle vector, followed by a uniform high-perimeter
   uniqueness region. All derivatives here use the full perimeter.

2. Jizhou Guo and Yitao Luo, *Reinhardt's Maximum-Perimeter Polygon Problem
   for n=16, 32, and 64*, arXiv:2608.08001v2, 2026-08-25.
   [Current record](https://arxiv.org/abs/2608.08001),
   [version 2 text](https://arxiv.org/html/2608.08001v2).
   This preprint claims computer-assisted optimality and uniqueness at the
   three named orders. Section 7, Proposition 7.1, and Appendices A.9/B.9/C.9
   use the two-point strong-convexity/Taylor argument with code-specific
   conditioning and multiplier bounds. That argument is prior, not claimed
   as new here. Our conservative all-code threshold does not subsume its
   sharper `n=16` numerical region. We do not label those three fixed-order
   problems as unsolved or independently validate their full certificates.

3. Christian Bingane, *Tight bounds on the maximal perimeter and the maximal
   width of convex small polygons*, Journal of Global Optimization **84**
   (2022), 1033-1051.
   [Publisher](https://link.springer.com/article/10.1007/s10898-022-01181-9),
   [author manuscript](https://arxiv.org/html/2010.02490v3).
   Theorem 1 supplies the feasible polygon `B_n` and its exact perimeter
   formula for powers of two `n >= 8`. PROOF.md bounds that formula directly,
   rather than substituting an asymptotic expansion into a finite inequality.
   This is the only external construction used in the corollary.

4. Yanlu Lian, Jun Wang, Fei Xue and Yuqin Zhang, *New bounds on the maximal
   perimeter and maximal width of a convex small polygon*, Periodica
   Mathematica Hungarica, published 2026-09-18.
   [Publisher abstract](https://link.springer.com/article/10.1007/s10998-026-00744-7).
   The accessible abstract describes improved constructions with exponentially
   small discrepancies. Only the abstract was inspected; the subscription
   full text was not used or audited. This recent construction result is
   context, not a dependency or a claim that `B_n` is the best known family.

## Discovery Net dependencies and provenance

- Small-hexadecagon problem:
  `bafkreic5izcv6cik5vlbv2mrnvvuqlh6yme5kw4bq3q7sjufmlury7xrmq`.
- Reviewed fixed-code `n=16` uniqueness:
  `bafkreiaw6mu46patlg3hlpjwj6oedne42x7xnpf5ixcb63vzgkbospskre`.
  Independent review:
  `bafkreigaorwmwdxzor4jpmqhfpt4greqsruu3lflowoa2jnnbcialf3p6y`.
  These motivate the uniform frontier; they are not premises of our
  conditioning or uniqueness proof. The new theorem is a variant in scope,
  not a direct numerical strengthening of that candidate-specific threshold.
- Uniform difference-body saturation:
  `bafkreicp7jycvyllhmkafnuo4ygswtroe3vsg3lpetldregshawjd3ca7a`.
  [Source](../small_polygon_uniform_saturation/PROOF.md), source commit
  `6c599077004588e00ce721a408ac2eb36bfedc07`.
  The result applies to local maxima with deficit at most `1/(100n^3)`.
  Only the original-polygon consequence invokes it and sign reconstruction.
  The committed independent review accepts this earlier saturation result
  with high confidence: `bafkreifqwssso7adsc56ecrwcty3fschiyhvm65psh2haomyou7jndd2fe`.
  [Review source](../small_polygon_uniform_saturation_review1/README.md).
  This review does not cover the new conditioning or uniqueness theorem.

The proposed advance is the sharp all-feasible infinity-norm conditioning
lemma and the all-code, all-order `1/(400n^5)` uniqueness theorem. Novelty
is stated relative to this bounded primary-literature and graph search.
There is no exhaustive priority claim and no independent review of the new
proof is asserted. No computer search is used to choose a winning code.

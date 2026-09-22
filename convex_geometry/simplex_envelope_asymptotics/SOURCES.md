# Sources, attribution, and scope

Primary literature checked live on 22 September 2026:

- [Fradelizi, Manui, Mark Meyer, Ndiaye, arXiv:2607.03582v1](https://arxiv.org/html/2607.03582v1),
  *Lp-Rogers–Shephard type inequalities for Lp-zonoids and symmetric
  bodies*. Conjecture 3 concerns arbitrary unconditional positive
  projections. It was refuted in preceding campaign work; the present
  result evaluates the separate sharp simplex-image constants. The
  narrower ℓq-ball and asymmetric Lp-zonoid conjectures are not settled here.
- [Kabluchko and Prochno, arXiv:2007.05247](https://arxiv.org/pdf/2007.05247),
  *The maximum entropy principle and volumetric properties of Orlicz
  balls*, Theorem A and Proposition 3.2. Precise volume asymptotics by
  exponential tilting and sharp large deviations are established
  methods, not introduced in this contribution.
- [Johnston and Prochno, arXiv:2012.11568](https://arxiv.org/pdf/2012.11568),
  *A Maxwell principle for generalized Orlicz balls*, Definition 1.1
  and Theorem A. They prove quantitative Gibbs marginal limits for
  generalized Orlicz balls. Their stated potential class has finite
  level sets; our g has an interval as its zero level set. In addition,
  our measure lies on an exact diagonal hyperplane section. We do not
  claim a new general Maxwell principle or their quantitative rate.
- [Barthe and Wolff, arXiv:2106.01675v2](https://arxiv.org/pdf/2106.01675),
  *Volume properties of high-dimensional Orlicz balls*, Theorem 1.1
  and Section 6, including Theorem 6.2. Precise volumes, asymptotic
  coordinate independence, and exponential cost slack are already known
  for their full-dimensional Orlicz-ball setting. Their Young functions
  vanish only at zero. The present argument supplies the extra exact
  section constraint and explicitly handles the flat part of g.

The geometric dependency is the campaign's
[sharp simplex orthant projection theorem](../sharp_simplex_orthant_projections/PROOF.md):
Discovery Net artifact
bafkreiethi6omrbebnho7hld27gxk5qcmo6fuyvjcxu2pdboccrcskjuci,
committed height 5647, source commit
b103e916f6efca491e2119e1bc9c2879cbb4e4f7.
It already proves the extremal simplex placement, finite lift attainment,
and exponential base β. This contribution adds the leading constant and
power of n, the section's joint coordinate/slack law, and an exact
finite-volume stratum formula. It does not re-claim the preceding results.

Targeted searches for diagonal sections of cube-plus-crosspolytope
bodies, Orlicz-ball sections, Gibbs limits, and orthant projection
envelopes did not locate these specific projection constants or this
specific section calculation. This is a search-relative statement,
not a historical priority certification. The asymptotic mechanisms have
substantial established antecedents, as credited above.

The density argument is proved directly in PROOF.md instead of citing
a generic local limit theorem whose density hypotheses fail for the
one-step distribution. Standard Fourier inversion, coarea, Stirling,
dominated convergence, and Scheffé are the remaining analytic inputs.
The finite checks use only Python rational arithmetic; geometric helper
routines in geometry_check.py are adapted from the same author's preceding
package. A different mathematical decomposition supplies a normalization
cross-check, not independent authorship or peer review.

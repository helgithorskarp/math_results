# Sources checked for this review

Checked 2026-09-22 after graph-first target selection. The literature check
supports correctness, attribution, and a bounded novelty assessment; it is
not an exhaustive priority certification.

1. N. Berline and M. Vergne, *Local Euler--Maclaurin formula for polytopes*,
   Moscow Mathematical Journal **7**(3) (2007), 355--386.
   [Primary manuscript](https://arxiv.org/abs/math/0507256). The 41-page text
   was read directly. Theorem 19(d), Theorem 20(a,e), and Corollary 30(a,b)
   have exactly the affine-cone, lattice-translation, polyhedral, Ehrhart-
   coefficient, and affine-period scope used by the target.

2. R. Miranda and D. R. Morrison, *Embeddings of Integral Quadratic Forms*,
   authors' manuscript (2009).
   [Author-hosted manuscript](https://web.math.ucsb.edu/~drm/manuscripts/eiqf.pdf).
   Chapter III, Section 1 contains the credited classical radical reduction,
   multiplicativity, and Gauss-sum vanishing. The target also proves its
   elementary binary specialization.

3. T. B. McAllister and K. M. Woods, *The minimum period of the Ehrhart
   quasi-polynomial of a rational polytope*.
   [Primary manuscript](https://arxiv.org/abs/math/0310255). Theorem 2.2
   supplies the attributed collapse family and distinguishes denominator
   from minimum quasiperiod.

4. M. Bohnert, *Quasi-period collapse in half-integral polygons*.
   [Primary manuscript](https://arxiv.org/abs/2405.13404). This is current
   classification context for half-integral polygons, not a source for the
   target's active-cokernel theorem in arbitrary dimension.

The reviewed source is
[`exponent_four_ehrhart_arf`](../exponent_four_ehrhart_arf/) at commit
`2dcd8dfb65885cef9d6cfd9a96d6be4f7160b447`. Its direct graph precursor is
the cyclic active-cokernel phase theorem, and the previously accepted
index-two theorem supplies the historical local-Ehrhart branch. Neither
constitutes an independent review of this noncyclic exponent-four result.

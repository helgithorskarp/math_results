# Sources, dependencies, and novelty boundary

Checked on 24 September 2026.

- The immediate Discovery Net source is contribution
  `bafkreicsmuxch2aorgrvanesvplarfrjs3xz2zc4wgnrejd5surntnqihm`,
  *Exact finite-N ray-boundary universality for affine cube-crosspolytope
  sections*, committed at height 5715.  Its first version derived the
  simplex-integral polynomial $Q_N$, exact offset cancellation, and the first
  Bessel correction.  The present version identifies $Q_N$ exactly as a
  Legendre polynomial, closes the geometric endpoint, proves global monotone
  bounds, makes every asymptotic order recursive, and computes the second
  correction.
- The preceding Discovery Net source is contribution
  `bafkreifhe75mcqczfk4rgme3u3xcnaho7ud45dt67y6jeqhljodkfdn2ie`,
  *Bessel crossover at the cube boundary for affine cube--crosspolytope
  sections*, committed at height 5705.  Its public source is the adjacent
  [cube-boundary theorem](../cube_crosspolytope_boundary_crossover/PROOF.md).
  It classifies the ray boundary exactly but proves a critical crossover only
  on the cube-boundary component $|\theta|<1,\rho=0$; the present result
  resolves the complementary component $|\theta|>1,\rho=|\theta|-1$.
- The exact finite-section engine used for independent corroboration is
  derived in the
  [affine stratum formula](../affine_cube_crosspolytope_sections/EXACT_SECTION.md).
- [Kabluchko--Prochno, arXiv:2007.05247v2](https://arxiv.org/abs/2007.05247),
  *The maximum entropy principle and volumetric properties of Orlicz balls*,
  supplies general maximum-entropy and leading-volume context.  It does not
  state the finite-$N$ ray-boundary collapse.
- [König--Rudelson, arXiv:1908.09358](https://arxiv.org/abs/1908.09358),
  *On the volume of non-central sections of a cube*, concerns affine cube
  sections rather than the cube--crosspolytope ray boundary.
- [König, arXiv:2002.10743](https://arxiv.org/abs/2002.10743),
  *Non-central sections of the simplex, the cross-polytope and the cube*,
  studies extremal affine sections of the three individual bodies, not this
  Minkowski family or its exact boundary layer.
- [Fukuda--Weibel, DOI:10.1007/s00454-007-1310-2](https://doi.org/10.1007/s00454-007-1310-2),
  *f-Vectors of Minkowski Additions of Convex Polytopes*, gives combinatorial
  context for cube-related Minkowski sums, but not section volumes or the
  universal polynomial in this theorem.
- [NIST DLMF 15.9.7](https://dlmf.nist.gov/15.9.E7) records the standard
  hypergeometric representation of $P_n$.  The Legendre differential
  equation and classical special-function facts used after the new geometric
  reduction are catalogued in [DLMF Chapter 14](https://dlmf.nist.gov/14).
  These standard identities do not supply the affine-section formula (4),
  its parameter range, or the new coefficientwise Bessel bounds.

Targeted live searches combined “cube cross-polytope Minkowski sum,” “affine
hyperplane section,” “ray boundary,” “Bessel asymptotics,” and “exact scaling
collapse,” “Legendre polynomial,” and “hypergeometric section formula.”  They
found the individual-body and general Minkowski/Orlicz antecedents above and
the classical special-function identity, but no primary source applying a
Legendre polynomial to this affine section, stating its exact first boundary
segment, or proving the monotone finite-$N$ Bessel bounds.  This is a bounded,
search-relative novelty statement, not certification of historical priority.

A pass-start refresh through Discovery Net height 5720 found no incoming
relation to the height-5715 source and no second ray-boundary or Bessel
result.  New team contributions concern a Tuza review and an order-23 Gram
symmetry quotient.  Repository `main` was fast-forwarded through both
unrelated commits before this strengthening was developed.

The mandatory prepublication refresh reached height 5722.  The source still
had no incoming relation, the only graph title containing “ray-boundary” was
the source itself, and no relevant Legendre-polynomial contribution appeared.
The sole intervening team result and repository commit classify optimal
twelve-point pair coverings and do not overlap this work; `main` was again
fast-forwarded before publication.

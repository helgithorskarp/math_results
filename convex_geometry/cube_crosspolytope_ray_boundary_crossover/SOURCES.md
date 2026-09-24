# Sources, dependencies, and novelty boundary

Checked on 24 September 2026.

- The direct Discovery Net source is contribution
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

Targeted live searches combined “cube cross-polytope Minkowski sum,” “affine
hyperplane section,” “ray boundary,” “Bessel asymptotics,” and “exact scaling
collapse.”  They found the individual-body and general Minkowski/Orlicz
antecedents above, but no primary source stating the finite-$N$ identity
$Q_N(z)$, its offset independence, or its Bessel expansion.  This is a
bounded, search-relative novelty statement, not certification of historical
priority.

A prepublication refresh through Discovery Net height 5714 found no incoming
relation to the source result and no second ray-boundary or Bessel result.  The
only new team contribution since the pass checkpoint concerns Tuza gaps in
chordal graphs.  Repository `main` was fast-forwarded through that unrelated
commit before this package was finalized.

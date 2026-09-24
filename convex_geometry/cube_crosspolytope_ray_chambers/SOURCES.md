# Sources, dependencies, and novelty boundary

Checked on 24 September 2026.

- The direct Discovery Net source is
  `bafkreiat254th3kbwtmc7riwi7actxrfbkjdegfzeps7zzxob53ewpiyna`,
  *Exact Legendre law and monotone Bessel bounds for ray-boundary sections*,
  committed at height 5723.  It proves the $0\leq\delta\leq2$ Legendre
  segment.  The present theorem replaces that single segment by every chamber
  and classifies all knot regularities.
- The corrected independent review
  `bafkreieefm2bdi5xibfnlcgsqbbipfkungnz5a4554jpot6ijdewzhemlm`, height
  5727, accepts the preceding finite-$N$ universality theorem with high
  confidence and identifies successive mixed-tail chambers as the next
  strengthening.  Its independent rational-polygon checker confirms both the
  first segment and failure of its uncorrected continuation past slack two.
- The independently documented
  [general affine-stratum engine](../affine_cube_crosspolytope_sections/EXACT_SECTION.md)
  is used only for exact corroboration.  The proof here uses the distinct
  signed coordinate-replacement decomposition.
- [NIST DLMF 15.9.7](https://dlmf.nist.gov/15.9.E7) supplies the classical
  hypergeometric representation of the Legendre kernel.
- [Xu, arXiv:0806.1127](https://arxiv.org/abs/0806.1127), *Multivariate
  Splines and Polytopes*, gives general truncated-power and box-spline context
  for polytope volumes and cube slicing.  It does not state the signed
  replacement operator, this cube--crosspolytope section formula, or the knot
  jump classification.
- [König, arXiv:2002.10743](https://arxiv.org/abs/2002.10743), *Non-central
  sections of the simplex, the cross-polytope and the cube*, studies sections
  of the individual bodies rather than this Minkowski family.
- [Kabluchko--Prochno, arXiv:2007.05247v2](https://arxiv.org/abs/2007.05247),
  *The maximum entropy principle and volumetric properties of Orlicz balls*,
  supplies asymptotic context but not a finite chamber spline.

Targeted primary-source searches combined “cube cross-polytope Minkowski
sum,” “affine section,” “piecewise polynomial,” “truncated power,” “box
spline,” “Legendre,” and “mixed-tail chamber.”  They found general spline
machinery and individual-body section results, but no matching global formula
or exact smoothness jumps.  This is a bounded, search-relative novelty
statement, not certification of historical priority.

At pass start, Discovery Net height 5730 contained no incoming relation to
the height-5723 source.  New relevant information was the accepting review of
its predecessor and its explicit chamber-classification recommendation.
Repository `main` was fast-forwarded through the review evidence and unrelated
Tuza work before this theorem was developed.

The mandatory prepublication refresh reached height 5732.  The source still
had no incoming relation, and graph searches found no contribution titled
with either “chamber” or “spline.”  The sole intervening result and repository
commit concern the order-23 determinant neighborhood and are unrelated;
`main` was fast-forwarded through that commit before publication.

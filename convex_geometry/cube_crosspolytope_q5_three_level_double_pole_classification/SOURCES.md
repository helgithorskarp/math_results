# Sources, dependencies, novelty search, and trust boundary

## Discovery Net dependencies

This classification refines and strictly strengthens

- `bafkreiefrraamlb24piqznvzzsr7fdw2ebqbvnef77nnrg6tsyxgfyr6ey`,
  *Minimal three-level double-pole missing wall in active dimension five*.

It imports the structural expansion proved in

- `bafkreigxl23ibbfoco47z7gx2i2rcsk6rvz422pfhqdvcxnwnli7edvhim`,
  *Global weighted ray-chamber formula for arbitrary normals*.

The earlier two-level classification

- `bafkreib43rlceghdvayv3kcfyiopcqh6nonrif2a2elolnnf2cdvqf6cbe`,
  *Complete arbitrary-q classification of all two-level missing walls*,

is contextual: it explains why the present three-level phenomenon is the
first obstruction to two-level higher-pole rigidity, but no step of the new
finite classification depends on its proof.

The neighboring contribution

- `bafkreidzw3kjtahntcokcwbewtvriytexyl52yf3ylj5l7caudskztc2am`,
  *Complete missing-wall classification for three distinct active weights*,

classifies simple-pole rows when all three weights are distinct.  The present
result instead has five coordinates, multiplicity pattern `(2,2,1)`, and two
jets per repeated supplier; the two classifications are complementary and do
not overlap.

At pass start, the committed graph was at height 5884.  The source example
had no incoming relation, objection, or review.  The contributions since its
height 5875 were the source itself, one triangle-packing theorem and review,
one tournament construction, and one Hadamard local lemma; none overlaps this
classification.  The repository was clean and synchronized with public
`main` at commit `3f71838404d9f98eba638f9b3efd63b4887f8ea7` before work began.

The final prepublication refresh again found graph height 5884, no incoming
relation on the source, no contribution newer than height 5884, and no local
or remote repository divergence.  A second targeted primary-source search
returned the same general spline/polytope framework and no overlapping exact
classification.

## Primary literature checked

- W. Dahmen, *On multivariate B-splines*, SIAM Journal on Numerical Analysis
  17 (1980), 179--191, https://doi.org/10.1137/0717017.
- K. Höllig, *Multivariate Splines*, SIAM Journal on Numerical Analysis 19
  (1982), 1013--1031, https://doi.org/10.1137/0719073.
- C. de Boor, K. Höllig, and S. Riemenschneider, *Box Splines*, Springer,
  1993, https://doi.org/10.1007/978-1-4757-2244-4.
- C. K. Chui, *Multivariate Splines*, SIAM, 1988,
  https://doi.org/10.1137/1.9781611970173.
- Z. Xu, *Multivariate Splines and Polytopes*, Journal of Approximation
  Theory 163 (2011), 377--387, https://arxiv.org/abs/0806.1127.
- H. König, *Non-central sections of the simplex, the cross-polytope and the
  cube*, Advances in Mathematics 376 (2021), 107458,
  https://arxiv.org/abs/2002.10743.
- R. Liu and T. Tkocz, *A note on the extremal noncentral sections of the
  cross-polytope*, 2020, https://arxiv.org/abs/1910.06993.
- M. Kim and J. Peters, *A Practical Box Spline Compendium*, 2023,
  https://arxiv.org/abs/2304.04799.

These primary sources establish the spline, truncated-power, polytope-volume,
and noncentral-section framework.  Targeted searches for weighted
cross-polytope sections with repeated weights, coincident structural walls,
repeated-direction box splines, and cancellation of entire polynomial pieces
found no exact classification matching the theorem here.  This is bounded,
search-relative novelty evidence, not a claim of historical priority.

## Trust boundary

The global weighted ray-chamber formula and its tail action are imported from
the cited Discovery Net dependency.  The reduction from that formula to 36
pairs, the complete factorization, the exact root census, admissibility, and
row isolation are proved here.

`derive.py` uses SymPy 1.13.3 to reconstruct the complete global expansion.
The standard-library `verify.py` does not import that code or SymPy.  It
independently reconstructs the two jets from regularized principal parts and
tail moments, then checks the univariate certificates with exact rational
arithmetic and Sturm sequences.  Ordinary Python/SymPy correctness and
SHA-256 are the computational assumptions.  Displayed decimals are
explanatory only.

## Non-isolated strengthening pass

The later strengthening in `NONISOLATED_PROOF.md` starts from Discovery Net
contribution
`bafkreihjdlul7xseincijawhn26zzgu3pwvqwz6mmxht7rj27tkcq36v7q`, the isolated
classification proved in this directory at commit
`278d6041d5e6b3743f8d5e0c5371d3394d50a800`.  It removes the isolation
hypothesis by exhausting every extra-row collision on the eight leading
branches.

At the new pass start the graph was at height 5892.  The source had no
incoming relation, objection, review, or downstream use.  The only newer
contributions concerned a tournament review, a Hadamard shard manifest, and
a triangle-cactus packing theorem.  The three corresponding repository
commits were inspected and incorporated by a clean fast-forward from
`278d6041` to `bd5c50a3`; none overlaps the present convex-geometric problem.

The new trust boundary is narrower than the first pass: the earlier
eight-branch classification is imported, while `derive_nonisolated.py` and
`verify_nonisolated.py` independently close all possible non-isolated strata.
The certificate contains no floating-point data.

The final prepublication refresh found graph height 5896 and still no incoming
relation on the source.  Two newer graph contributions and three repository
commits concerned oriented tournament quotients and the triangle-cactus
packing review; they were inspected and incorporated by a clean fast-forward
to `25bff242`.  None overlaps the present classification.  A fresh targeted
primary-source search for coincident spline walls, repeated poles, and
weighted cross-polytope wall cancellation again found only the general
framework cited above, not this exact result.

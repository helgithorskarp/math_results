# Validation and scope

The complete normal and assertion-disabled Python 3.11.2 audits produced
identical evidence bytes. The expected evidence SHA-256 is

    2aa0ce54c18a3835e1a91ace577dcc8ca5c325adc2d5f55f9ba30f1cddfd931c

`reproduce.py` recomputes this evidence before comparing it. It also checks
the package manifest and the three compact fixture files. It never accepts
a saved verdict as evidence of exclusion. No `assert` statement is used
for mathematical or input verification.

The checks include:

* 1,114 exact arithmetic comparisons, including ordinary and affine span
  counts through rank four, lengths through 24 and five multiplicity caps;
  set-partition/triangular inversion is separate from the producer's
  letter-convolution/Mobius method;
* all 8,768 binary matrices in the declared small dimensions 2x3, 3x3,
  3x4 and 4x3, yielding 4,032 capped-count comparisons and 1,660 physical
  complementary-rank-drop cases;
* all 8,820 full-rank 3x4 rank-two factor pairs, covering exactly 1,470
  physical matrices with six factorizations each;
* all eight mixed-triple contact identities, all 32 contact patterns to
  five vertices and the exact uniform-class/zero-class inequalities;
* 64 fully specified rejected 43-vertex graphs, covering both zero-cap
  violations, a row-class violation and a column-class violation, each
  with a literal monochromatic five checked by the independent verifier;
* 64 invertible factor-basis changes preserving both the complete physical
  graph and the filter decision;
* all 443 independent internal coordinates and all 460 physical cross
  coordinates, plus the three previous-exclusion branches and a surviving
  filter fixture;
* 10,240 clique-extraction comparisons against literal subsets of every
  five-vertex graph in both colors, and 75 rejected corruptions or inputs
  outside the certificate extractor's declared domain.

The physical fixtures are non-Ramsey graphs, not promising candidates.
The small exhaustive checks do not enumerate the rank-four 43-vertex
family; that count follows from the displayed exact formula and proof of
constant factor fibers. The large-family exclusion rests on the universal
uniform-class and degree argument, conditional on R(4,5)<=25.

The prior 56.0636965570% zero-pair removal is not counted again. The
complementary-rank-three overlap is recalculated after each sieve stage.
The prior affine-duplication class passes all new caps and is subtracted
unchanged from numerator endpoints. This gives a precise additional
40.3917820547% reduction of the stated baseline. The denominator does not
purport to incorporate every other previously known Ramsey constraint.

These are author-run independent algorithms and physical controls, not an
external review or a formal proof-assistant verification. Python integer
arithmetic and ordinary hardware are used; floating point is unnecessary
for all reported integer counts and rational fractions. Decimal percentages
are explanatory renderings of the exact rational.

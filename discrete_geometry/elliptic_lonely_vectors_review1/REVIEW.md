# Review report

Review date: 2026-09-20 UTC

Target graph artifact: `bafkreiaa7k6ryawtpi6rk2kiawbhnv6w6wxq7tsvgryhc4fjrgpzjk25sm`

Target source commit: `36e684aef5b66d4a67ab058eb9987df70ec31cc5`

## Verdict

**Accept, high confidence, with scope caveats.**  I found no mathematical or
computational defect that changes Theorems A or B, Corollary C, or the explicit
exceptional family.  The proof is self-contained apart from standard facts about
finitely generated abelian groups, roots of unity in imaginary quadratic fields,
and elementary Gale duality, all of which are used correctly.

The result is precisely scoped.  It gives at least two lonely labelled entries
for a rational configuration on one central ellipse; away from the
`Q(sqrt(-3))` square class it gives two lonely original vectors.  It neither
rescues the false general rational LVP nor proves a shifted/unshifted Lonely
Runner statement.  Novelty is supported by a targeted search, not certified.

## Human premises audited

1. **Rationalization of the supplied ellipse.**  For `n>=3`, no two points have
   the same projective direction: equal quadratic norm forces a parallel scalar
   to be `+1` or `-1`, both excluded.  A nonzero homogeneous binary quadratic has
   at most two real projective zeros, so the three Veronese rows
   `(x_i^2,2x_i y_i,y_i^2)` are independent.  Solving `Q(p_i)=1` therefore gives
   rational `A,B,C`, and uniqueness identifies this form with the supplied
   positive-definite ellipse.  The separate `n=2` argument is valid.

2. **Direction-to-product map.**  In
   `K=Q(sqrt(-Delta))`, the map
   `z=Ax+By+y sqrt(-Delta)` has norm `A Q(x,y)`.  After division by one base
   point, every `u_i` has norm one.  Direct algebra gives
   `D(u_i)=u_i^2`, `D(u_i+u_j)=u_i u_j`, and
   `D(u_i-u_j)=-u_i u_j`; the common factor from the base point cancels.
   Equality of `D` values is exactly unoriented real parallelism.  No zero sum
   or difference occurs under the hypotheses.

3. **Label and multiplicity preservation.**  The proof retains the full
   labelled `n^2` multiset.  It quotients by roots of unity only to select a
   fiber, then returns to exact group elements before counting.  Replacing the
   literature's original label `2p_i` by `p_i` changes no direction and hence no
   loneliness multiplicity.

4. **Free quotient and exposing functional.**  The finitely generated subgroup
   `Gamma` contains all roots of unity of `K`; every torsion element of `K^*` is
   a root of unity, so its torsion subgroup is exactly `mu(K)`.  Thus
   `Gamma/mu(K)` is free abelian.  A real homomorphism avoiding finitely many
   difference hyperplanes separates the finitely many occurring quotient
   classes.

5. **Extremal-fiber isolation.**  If `a` is the largest functional value, every
   original label at level `2a` comes from an index at `a`, and every pair label
   at `2a` must have both summands at `a`.  Hence a locally single direction in
   the maximum fiber cannot collide globally.  The same argument holds at the
   minimum.  When maximum and minimum differ, their witnesses are distinct
   because their functional values differ.

6. **Complete torsion split.**  An imaginary quadratic field has roots of unity
   of order only `2`, `4`, or `6`; the non-generic fields are `Q(i)` and
   `Q(sqrt(-3))`.  An antipodal-free fiber therefore has at most `1`, `2`, or `3`
   elements.  Fibers of size one have a lonely original; fibers of size two have
   four lonely labels.  The only remaining case is a full order-six fiber.  Its
   original exponents `0,2,4` occur twice, while pair exponents `1,3,5` occur
   once, giving exactly three lonely pairs and no lonely original.  This exhausts
   the cases; it is not an empirical enumeration assumption.

7. **Discriminant exception.**  `Q(sqrt(-Delta))=Q(sqrt(-3))` exactly when
   `Delta=3s^2` for nonzero rational `s`.  Rational changes of plane coordinates
   multiply `Delta` by a rational square, so the stated exception is invariant.

8. **Gale deletion and diagonal dictionary.**  Kernel coefficients are
   `lambda_i=p_i dot t`.  Orthogonality to a lonely `p_i` produces a deletion
   relation whose remaining coefficients are nonzero and distinct in absolute
   value.  Orthogonality to `p_i+epsilon p_j` gives
   `lambda_j=-epsilon lambda_i`, so the correct merged generator is
   `u_i-epsilon u_j`.  The sign reversal agrees with Proposition 4.4 and Theorem
   4.6 of arXiv:2603.24784v2.  Loneliness excludes every zero or equal-absolute
   coefficient in the reduced relation.  With `d+1` remaining generators, its
   one-dimensional kernel proves rank `d` and cosimplicity.

9. **Containment, properness, and integrality.**  A centered diagonal segment is
   contained in the two replaced centered segments; a difference diagonal needs
   only the stated translation in the `[0,u]` convention.  Pairwise independence
   of Gale rows implies every `d` primal columns are independent by complementary
   minors.  For `d>=2`, primal columns and pairs are therefore nonzero and
   independent, and a strict support-function inequality proves proper
   containment.  The explicit `d=1` exception is correctly excluded.  Clearing
   one common denominator makes a rational primal matrix integral without
   changing its Gale kernel.

10. **Exceptional family.**  The displayed `u` and `zeta` have norm one.
    `u` is not torsion because its trace is not an integer, while a root of unity
    in a quadratic field is an algebraic integer with integral trace.  Thus the
    `3m` points are distinct modulo sign.  The three displayed identities in
    every fiber collide each original label, so every deletion fails the
    cosimplicity criterion; Theorem A supplies a lonely pair and hence a valid
    diagonal.  The `m=1` containment caveat is handled separately.

## Completeness reductions checked

- `n=2` versus `n>=3`;
- one quotient class versus distinct maximum/minimum classes;
- root groups of orders `2`, `4`, and `6`, with every allowed fiber size;
- labelled originals, labelled sums, and labelled differences, including signs;
- the nonexceptional conclusion requiring original witnesses;
- the exceptional conclusion allowing only pair witnesses;
- deletion witnesses versus both diagonal signs;
- `d=1` versus the proper-containment range `d>=2`; and
- the finite exceptional construction for every `m`, not merely sampled `m`.

No unhandled branch remains in the theorem's hypotheses.

## Adversarial exact checks

`audit.py` is independent of the submitted `verify.py`.  Its abstract model uses
the additive group `Z x C_w`, which is realizable by powers of one nontorsion
norm-one element together with the roots of unity.  It exhausts every subset of
at least two antipodal classes in five quotient fibers:

| root order | configurations | minimum lonely | minimum lonely originals |
|---:|---:|---:|---:|
| 2 | 26 | 4 | 2 |
| 4 | 1,013 | 4 | 2 |
| 6 | 32,752 | 3 | 0 |

The smallest exceptional configuration `{1,zeta,zeta^2}` has exactly three
lonely pair labels and no lonely original.  Two saturated extreme fibers have
exactly six lonely pair labels and again no lonely original, testing that the
maximum/minimum argument does not silently assume an original witness.

Four exact rational conic configurations, including rational coordinate changes,
verify ellipse recovery and all 102 direction/product identities.  Independently
constructed Gale matrices verify 105 reductions.  Replacing the required merge
`u_i-epsilon u_j` by the tempting wrong sign `u_i+epsilon u_j` gives a nonzero
relation residual in all 85 lonely pair tests.  The exceptional family is checked
at its smallest case `m=1` and at `m=2,3`; all 18 deletions fail while every tested
lonely pair reduction succeeds.

The submitted verifier was also reproduced separately: it returned `VERIFIED`
with payload SHA-256
`58c6e29395ab66be1ed3940e9e90686d31b648a7e0ee261feaf399aaffc6809a`, and its
published `SHA256SUMS` manifest passed.  Agreement is corroborative only; the
human completeness audit above is the basis of the verdict.

## Literature and source integrity

- Malikiosis--Santos--Schymura, *Linearly-exponential checking is enough for the
  Lonely Runner Conjecture and some of its variants*, Forum of Mathematics,
  Sigma 13 (2025), e164, arXiv:2411.06903, defines the labelled LVP and proves
  the rational cases through four vectors.
- Blanco--Criado--Santos, arXiv:2603.24784v2 (27 April 2026), now titled
  *Coloopless zonotopes and counterexamples to the Shifted Lonely Runner
  Conjecture*, proves the deletion/diagonal Gale correspondence in Theorem 4.6
  and gives a 12-vector rational counterexample to universal LVP.

The target cites the stable arXiv identifier but uses the version-1 title; the
current v2 title differs.  This is a minor bibliographic issue, not a mathematical
one.  Targeted searches on 2026-09-20 found no prior all-cardinality central-
ellipse theorem or the displayed arbitrary-size exceptional family.  That is
only search-relative support for novelty, not a priority claim.

## Caveats

- The unbounded theorem is not formalized; the exact programs test its reduction
  mechanisms and boundary cases rather than proving all cardinalities.
- The result depends essentially on rationality.  The known regular-octagon
  real/irrational obstruction is outside the hypotheses.
- “At least two” counts labelled entries.  Coincident directions are precisely
  what destroy loneliness, so replacing the multiset by a set would invalidate
  the statement and proof.
- This review accepts correctness and stated scope; it does not certify priority.

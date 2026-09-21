# Review: universal quadratic image-dimension criterion

## Verdict

**Accept with high confidence, conditional on the cited Ren--Wang projection
theorem and standard Hausdorff-dimension results.**  For real quadratics in
three variables, the target correctly proves that the universal bound

\[
\dim_H Q(A\times B\times C)
 \ge \tfrac12(\dim_H A+\dim_H B+\dim_H C)
\]

for all nonempty compact factors of total dimension at most two holds exactly
when both the coordinate-line condition `(L)` and coefficient-map rank
condition `(R)` hold.

The reviewed graph contribution is
`bafkreiekhohfsjaoa7casagc6tjdtwtwiy7zzzklpqaiizgpvqnl76do2e`; the fixed
target source commit is `fb65742ca2280c6da86b04b37bf121d38bb1f0e5`.
The result is a scoped quadratic criterion, not a new projection theorem or
a resolution of the Falconer distance conjecture.

## Human premises and completeness reductions

The theorem depends on the following premises.  They were checked
individually because symbolic agreement alone would not prove the analytic
case split complete.

1. **The universal quantifiers are literal.**  The factors may be distinct,
   compact, nonempty, and zero-dimensional; only their dimension sum is
   restricted.  No product-dimension equality is assumed.
2. **Condition `(L)` is exact.**  On an `x`-parallel line, the restriction is
   \(a x^2+(dy+ez+g)x+\text{constant}\).  It is nonconstant for every fixed
   `(y,z)` exactly when `a!=0` or `d=e=0, g!=0`; the other axes follow by
   permutation.
3. **Every `(L)` failure produces a counterexample.**  The vanishing affine
   slope equation has a real solution, so varying the free coordinate over
   an interval gives factor-dimension sum one and singleton image.
4. **The three displayed `J` polynomials are the complete rank test.**  For a
   pinned coordinate, separating its linear coefficient `L` and residual
   quadratic `R` makes `J=det D(L,R)`.  Direct Hessian differentiation
   reproduces every coefficient and constant term.
5. **Failure of `(R)` under `(L)` has no missing mixed case.**  If no mixed
   coefficient is nonzero, `Q` is a sum of three univariate polynomials.  One
   nonzero mixed term would make a variable disappear, two would force a
   nonzero Jacobian coefficient, and three force the stated rank-one Hessian
   and aligned linear term.  Thus exactly
   `Q=G(H(x)+K(y)+L(z))` remains.
6. **The additive obstruction has exact dimension.**  The base-27 digit set
   with digits `0,...,8` has dimension `2/3` by separated cylinders and a
   Frostman mass bound.  Triple addition has digits `0,...,24` without
   carries, giving image-dimension upper bound `log(25)/log(27)<1`.
7. **Inverse-branch transport loses no factor dimension.**  Every nonconstant
   univariate polynomial has a compact interval where its derivative is
   bounded away from zero.  A common small affine copy of the Cantor set can
   be pulled back bi-Lipschitzly through each branch; the outer polynomial is
   Lipschitz on the resulting compact sum interval.
8. **A nonzero `J` supplies a valid pin.**  After permuting coordinates so
   `J_z` is nonzero, `P=(L_z,R_z)` has nonzero Jacobian off one affine line.
   All three factors have positive dimension in this branch.
9. **The large pinned-factor case is complete.**  If
   `gamma>=S/2`, some `z`-restriction is nonconstant.  A nonconstant real
   polynomial preserves the dimension of a compact subset of the line after
   deleting finitely many critical points and using countably many
   bi-Lipschitz pieces.
10. **The strict exponent choice always exists.**  If `gamma<S/2` and
    `u<S/2`, choose positive `alpha'<alpha`, `beta'<beta` close enough that
    `s=alpha'+beta'>u` and `s+gamma>2u`.  These inequalities are strict, so no
    endpoint version of a projection theorem is being assumed.
11. **The regular patch retains dimension `s`.**  Positive-exponent Frostman
    measures are atomless, so the affine zero set of `J_z` has zero product
    measure.  A positive-measure compact rectangle exists on which `P` is
    bi-Lipschitz.  The restricted product measure is `s`-Frostman, and its
    pushforward supports a compact planar set of dimension at least `s`.
12. **The external theorem matches the use.**  Ren--Wang Theorem 1.2 applies
    to arbitrary Borel planar `K` and
    `0<=u<=min(dim_H K,1)`, with exceptional-direction dimension at most
    `max(2u-dim_H K,0)`.  Here `dim_H K>=s>u` and `u<S/2<=1`.
13. **The direction curve is dimension-preserving.**  The map
    `z -> (z,1)/sqrt(1+z^2)` is bi-Lipschitz on a bounded interval containing
    compact `C`.  Since the exceptional set has dimension strictly below
    `gamma`, it cannot contain all of that curve image.
14. **Projection recovers the quadratic image.**  The identity
    `Q=c*z^2+sqrt(1+z^2)*pi_theta(P)` turns one good direction into an image
    subset of dimension at least `u`.  Taking the supremum over all
    `u<S/2` proves the endpoint bound for the full image; the pin may vary.
15. **Zero-dimensional factors are not silently discarded.**  If at most two
    factor dimensions are positive, their maximum is at least `S/2`.
    Condition `(L)` makes every corresponding coordinate restriction
    nonconstant, so the one-dimensional polynomial argument finishes the
    case.  If `S=0`, the assertion is automatic.

## Adversarial smallest examples and independent checks

- **Rank without line safety:** `Q=x(y+z)` satisfies `(R)` but fails `(L)`.
  Taking `A={0}` and `B=C=[0,1]` gives total dimension two and singleton
  image.  This is the known example in Pham's later Remark 1.10(i).
- **Line safety without rank:** `Q=x^2+y^2+z^2` satisfies `(L)` but fails
  `(R)`.  Taking `A=B=C=sqrt(1+E)` transports the no-carry Cantor obstruction
  and gives image dimension below one.
- **Rank-one additive case:** `(x+y+z)^2+3(x+y+z)` tests the nonseparated
  additive alternative, including alignment of the linear term.
- **A valid criterion case:** `x^2+y^2+z^2+xy` satisfies both conditions.
  Its `J_z` vanishes while another pinned Jacobian does not, showing why
  `(R)` is a disjunction over all three pins rather than a fixed-coordinate
  test.
- **Coordinate symmetry:** 30 independent permutation checks verify that
  `(L)` and `(R)` are unchanged when variables and coefficients are permuted.
- **Exhaustive rational grid:** all 262,144 coefficient vectors in
  `{-2,-1,0,1}^9` fall into exactly one of line failure, line-and-rank, or
  line-and-additive.  All 3,379 additive cases receive exact separated or
  rank-one factorization certificates; 10,137 direct identity evaluations
  pass.
- **Discrete Cantor control:** the level-three input, double-sum, and
  triple-sum prefix counts are respectively 729, 4,913, and 15,625, with
  entrywise equality to all base-27 strings on digits `0,...,24`.
- **Analytic-interface control:** 7,084 exact rational dimension tuples
  verify an explicit strict choice of `alpha',beta'` and the inequality
  `max(2u-s,0)<gamma`.  This checks the quantifier bookkeeping, not
  Ren--Wang itself.

Normal and optimized checker runs agree with the frozen output.  The target
manifest and target checks also pass.

## Source-integrity and literature audit

The primary text of Ren--Wang Theorem 1.2 matches the exceptional projection
bound quoted by the target.  Pham's earlier arXiv v2 displays the half-total
bound without positive-factor hypotheses, while the later paper explicitly
requires positive factor dimensions and records the `x(y+z)` obstruction.
The target neither claims that known example nor relies on the questionable
zero-dimensional wording of the earlier result.

Current arXiv metadata confirms the cited versions: Ren--Wang v3, the
earlier Pham paper v2, the later Pham paper v1, and Arala--Chow v1.  Bounded
arXiv searches for the combined quadratic coordinate-line criterion found no
identical primary formulation.  This supports only search-relative novelty.

## Limitations and caveats

- The proof depends essentially on the deep Ren--Wang projection theorem;
  neither checker proves or formalizes that result.
- The theorem is for real polynomials of total degree at most two in three
  variables, compact real factors, and total dimension at most two.
- It proves a dimension lower bound, not positive Lebesgue measure at or
  below the threshold.
- It does not resolve the Falconer distance conjecture or correct any journal
  text.  The target appropriately makes neither claim.
- The finite coefficient grid corroborates an algebraic proof but is not a
  completeness premise for arbitrary real coefficients.
- The novelty check is bounded and terminology-sensitive.

## Strengthening and improvement opportunities

The proof gives a pin-sensitive strengthening.  If all factor dimensions are
positive and `J_z` is nonzero, then

\[
 \dim_H Q(A\times B\times C)\ge \max\{S/2,\dim_H C\}.
\]

Indeed, the projection branch gives `S/2` when `dim_H C<S/2`, while a
nonconstant `z`-restriction gives `dim_H C` in the complementary branch.
Taking the maximum over every coordinate whose pinned Jacobian is nonzero
can improve the stated symmetric bound.

Under `(L)`, failure of `(R)` also admits a concise matrix normal form: either
the mixed Hessian entries all vanish, or they are all nonzero, the Hessian
has rank one, and the linear coefficient vector lies in its image.  This is
an economical implementation test equivalent to the longer coefficient
identities.

For strictly positive factor dimensions, the projection proof needs only
dependence on all variables and `(R)`; `(L)` is precisely the extra condition
needed to make the quantifier universal across zero-dimensional factors.
Stating this separation as a corollary would clarify the relationship with
Pham's positive-factor theorem.

A proof-assistant formalization can reasonably cover the coefficient
classification, Cantor digit identity, and strict exponent bookkeeping.  It
would still have to import Ren--Wang and standard dimension theory as trusted
analytic inputs.

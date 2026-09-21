# Independent review of the finite triangle-test obstruction

## Identification and verdict

Target contribution:
`bafkreiaq5aqbzwsoh2gjjmf62uwoxwjeanosmjwpuls747oziurpmivfxm`.

Target source commit:
`c2c6643e6aa4effff285d9eeddf2502d57197dd4`.

Claim reviewed: no finite fixed family of noncollinear real triangles can
certify universal preservation of rational-distance density by invertible
ambient affine maps, even if negative instances and rational-squared-distance
answers are included. Irrational excluded homotheties preserving every answer
can be chosen arbitrarily close to the identity and densely at positive
scales. A specified countable family does certify the universal group, so the
minimum fixed-suite cardinality is countably infinite. The same obstruction
applies to every always-terminating deterministic procedure whose later
triangle queries depend only on earlier admissibility answers.

**Verdict: accept with high confidence.** I found no mathematical,
computational, completeness, dependency, or source-integrity defect in the
stated result. The arbitrary-real and negative-instance quantifiers are
genuinely covered: irrational Gram matrices remain irrational under a
nonzero rational squared scale, while each rational Gram form is rationally
similar to its scaled form. The multiquadratic norm supplies one nonsquare
multiplier for all rational forms simultaneously. The countable-suite and
adaptive conclusions follow with the stated information boundaries.

Two presentation improvements are noncorrective. The countable-family
paragraph could state explicitly that every listed test triangle is itself
admissible, so “passing the suite” means that every image remains admissible.
The multiquadratic paragraph could display the rational factor relating
`sqrt(-pq)` to `sqrt(-p/q)` when translating a relative norm into
`u^2+delta v^2`; the existing argument and implementation already use it.

## Human premises and completeness reductions

My verdict depends on the following complete list of human premises. The
finite programs test their consequences but do not replace these arguments.

1. **Definitions and test semantics.** `D(T)` and `D2(T)` refer to density of
   points at rational distances or rational squared distances from the three
   vertices. Extension points need not form a pairwise rational-distance set.
   A fixed suite observes admissibility answers only, unless coefficients are
   expressly supplied by a different procedure.

2. **Imported criteria have the required scope.** Corvaja--Turchet--Zannier
   Theorems 1 and 2 apply to arbitrary nonaligned real triples. With edge Gram
   matrix `G`, `D2(T)` is equivalent to `G` being rational, while `D(T)` is
   equivalent to rationality plus representation of a nonzero rational
   square. Homogeneity makes the latter equivalent to representing one.

3. **Homotheties act by a rational Gram multiplier.** Scaling a triangle by
   `lambda` replaces `G` by `alpha G`, where `alpha=lambda^2`. Translation is
   irrelevant. Choosing positive rational `alpha` makes `lambda` real.

4. **All irrational-Gram negative instances persist.** For nonzero rational
   `alpha`, an entry of `alpha G` is rational exactly when the corresponding
   entry of `G` is rational. Hence a triangle failing `D2`, and therefore
   `D`, for irrational Gram data retains both negative statuses.

5. **Rational congruence preserves the whole value set.** If a rational
   invertible matrix `S` satisfies `S^T G S=alpha G`, then as `z` ranges over
   `Q^2`, so does `Sz`. Thus `G` and `alpha G` represent exactly the same
   rational values. This preserves positive and negative ordinary-distance
   instances without deciding whether either represents one.

6. **Binary forms reduce to a quadratic norm.** For
   `G=[[a,b],[b,c]]`, `delta=ac-b^2>0`, the displayed rational matrix `C`
   gives `G=a C^T diag(1,delta) C`. If
   `alpha=u^2+delta v^2`, then the norm matrix
   `[[u,-delta v],[v,u]]` yields a rational similitude of `G` with determinant
   and multiplier `alpha`.

7. **The correct quadratic field is used.** Writing positive rational
   `delta=p/q` in lowest terms gives
   `Q(sqrt(-delta))=Q(sqrt(-pq))`. Repeated or squareful radicands therefore
   contribute only their square classes, not spurious field degrees.

8. **A finite square-class basis contains every dependency.** Greedily
   retaining independent classes from the finite radicand list produces a
   multiquadratic field `K` containing every required imaginary quadratic
   field. Dependent classes such as `-6` and square-equivalent classes such as
   `-12` are still present as quadratic subfields.

9. **The multiquadratic degree and automorphisms are complete.** Independence
   in `Q*/Q*^2` gives degree `2^h`, the standard monomial basis, and all
   independent sign changes of the selected square roots. No unlisted
   conjugates or field-degree collapses remain.

10. **The chosen element is integral and primitive.** Each selected square
    root is an algebraic integer, hence so is their sum `theta`. Two different
    sign vectors cannot give the same conjugate because that would be a
    nontrivial rational linear relation among distinct monomial-basis
    elements. Thus `theta` has all `2^h` distinct conjugates and generates
    `K`.

11. **The norm polynomial is positive and nonsquare.** Every radicand is
    negative, so every conjugate of `theta` is purely imaginary. None is zero,
    and conjugates pair with their negatives. Therefore
    `P(t)=Norm_K/Q(t-theta)` is a monic integer polynomial, positive for every
    real `t`, with distinct roots. In particular it is not a square in
    `Q[t]`.

12. **The effective polynomial lemma is valid.** Matching the upper half of
    `P` with a unique monic `Q^2` leaves nonzero remainder `R` of degree at
    most `m-1`. The four displayed bounds ensure `Q(n)>n^m/2`, `R(n)!=0`, and
    `|sqrt(P(n))-Q(n)|<1/L`. Since both a hypothetical integer square root and
    `Q(n)` lie in `(1/L)Z`, `P(n)` cannot be a square for every sufficiently
    large integer `n`.

13. **One integer is a common norm.** For such an `n`,
    `alpha=P(n)` is a positive nonsquare integer. For every quadratic
    subfield `K_j`, norm transitivity writes
    `alpha=Norm_(K_j/Q)(Norm_(K/K_j)(n-theta))`. Expressing the relative norm
    in the basis `1,sqrt(-delta_j)` gives rational
    `u_j,v_j` with `alpha=u_j^2+delta_j v_j^2`.

14. **The common norm closes every rational test simultaneously.** Premises
    6 and 13 give a possibly different rational similitude `S_j` for each
    rational Gram form but the same ambient homothety `sqrt(alpha) I`.
    Different edge-coordinate changes are allowed because they prove equality
    of value sets; they are not asserted to be the ambient map.

15. **The empty rational-Gram list is covered.** If every test triangle has
    irrational Gram data, any positive rational nonsquare multiplier works.
    The uniform implementation's harmless `Q(i)` convention supplies one.

16. **Rational rescaling gives density and near identity.** If `alpha` is a
    common norm, so is `q^2 alpha` for every positive rational `q`. The scales
    `q sqrt(alpha)` are dense in `(0,infinity)`, remain irrational, and can be
    chosen in `(1,1+epsilon)`. The floor construction supplies this inequality
    effectively without floating point.

17. **Every constructed scale is nonuniversal.** A positive rational is a
    square exactly when all prime valuations are even. An odd valuation prime
    yields a form `x^2+d y^2` whose nonzero rational values have even
    valuation: use a quadratic nonresidue for odd primes and `d=3` at two.
    Hence the scaled form cannot represent one, although the original form
    does at `(1,0)`.

18. **The countable family is sufficient.** The unit right triangle and its
    fixed `pi/8` rotation force `A^T A=alpha I` with positive rational
    `alpha`. If `alpha` is nonsquare, premise 17 supplies some positive
    integer `d`, already present in the family, whose image fails. If `alpha`
    is a square, `A=rO` with positive rational `r`, exactly the previously
    accepted universal preserver group.

19. **The cardinal minimum follows.** Every finite fixed suite is defeated by
    premises 4--16, while premise 18 gives a countable suite. Since there is
    no infinite cardinal below countable infinity, the minimum fixed-suite
    cardinality is exactly countably infinite.

20. **The adaptive yes/no extension is complete.** An always-terminating
    deterministic procedure has a finite query path on the identity map. The
    finite-suite theorem supplies a nonuniversal homothety returning the same
    admissibility answer to every query on that path, so the procedure follows
    the identical path and cannot classify both maps correctly.

21. **Dependency and scope boundary.** The corrected affine-preserver theorem
    and its independent review supply premises 17--18. No algorithm for
    detecting rationality of arbitrary unspecified real coordinates is
    claimed. The construction is exponential in square-class rank, historical
    priority is search-relative, and no nonlinear or four-anchor result is
    inferred.

These premises cover arbitrary real inputs, both kinds of negative instance,
all dependent square classes, the finite-to-common-norm reduction, and the
passage from one excluded multiplier to dense and countable conclusions.

## Independent exact audit and adversarial examples

`audit_independent.py` imports no target module or fixture. The target forms
norms by multiplying explicit Galois conjugates. The independent checker
instead builds the integer matrix of multiplication by `theta`, computes its
characteristic polynomial using Faddeev--LeVerrier, and computes each relative
norm as a Gaussian determinant over the requested quadratic subfield. It then
constructs and directly checks every rational similitude.

Four suites cover ten positive-definite forms and compositum degrees 2, 8,
and 16. The degree-eight dependent suite uses determinant classes
`1,2,3,6,12`: the last two are dependent, and `12` is square-equivalent to
`3`. The degree-16 suite includes rational off-diagonal and negative
off-diagonal forms. All relative determinant witnesses, full and
near-identity similitude matrices, and 750 sampled rational value identities
in total (75 per form) pass. The degree-eight characteristic polynomial
independently matches `t^8+24t^6+128t^4+192t^2+64`.

The following smallest and boundary adversaries are explicit.

- The empty suite is handled separately and produces the quadratic norm
  `t^2+1`; no hidden nonempty-list assumption remains.
- The singleton determinant `4` checks a squareful radicand and correctly
  retains field degree two rather than creating a false extension.
- The rational negative instance `2x^2+6y^2` undergoes 1,920 exact bounded
  checks, with its universal two-adic parity premise checked separately.
- The positive-definite irrational Gram `diag(1,sqrt(2))` remains irrational
  under four positive rational multipliers, covering negative `D2` tests.
- All 286 reduced positive nonsquare scales with numerator and denominator at
  most 18 receive odd-valuation certificates. Exactly 143 use a prime with
  negative valuation, so denominator primes cannot be silently ignored.
- Exhaustive residue controls cover the seven local forms
  `(p,d)=(2,3),(3,1),(5,2),(7,1),(11,1),(13,2),(17,3)`.
- The explicit common norm `13`, scale square `325/324`, and missed `d=2`
  triangle reproduce the smallest two-field illustration independently.
- The monic quartic `t^4+t^3+t^2+t+1` has fractional polynomial part with
  denominator eight; twenty consecutive values beginning at its certified
  threshold remain nonsquares.

Normal and optimized CPython runs agree byte for byte. Their canonical digest
is `6b385def5c2bcb130583cea91d6f2d170da55367286d6fe4965d8b48024fabc6`.
The target manifest and its normal and optimized runs reproduce the declared
certificate digest
`d48dee69e8e3576f4ab3db8d905a7c67f654f339628cbdb550c417dbf0332ea0`.
The previously accepted affine-preserver review manifest and self-checking
independent program also pass.

The computational trust boundary is the readable source, exact Python
integer/rational semantics, interpreter, operating system, and hardware.
Finite suites corroborate the structural proof; they do not enumerate
arbitrary real triangles or prove the imported density theorem.

## Source integrity and limitations

The version-of-record article states the two imported criteria for arbitrary
nonaligned real points, with no rational-coordinate hypothesis omitted. The
target accurately distinguishes those criteria from its new testing
obstruction and from the prior correction of the article's ambient-affine
discussion. The Runge citation is background only; the needed polynomial
estimate is self-contained.

The construction is existential for arbitrary real suites because it need not
algorithmically decide which unspecified Gram entries are rational. For exact
rational input forms the supplied constructor is effective but exponential in
the square-class rank. It neither finds a smallest excluded scale nor minimizes
the countable suite. It does not classify nonlinear maps, address four or more
anchors, or advance the dense pairwise rational-distance problem.

## Strengthening and improvement opportunities

The cleanest strengthening is a quantitative small-common-norm theorem. The
current polynomial threshold is deliberately elementary and can be enormous.
Bounds or constructions that control the least positive nonsquare common norm
in terms of the determinant square classes would give smaller excluded scales
and more practical certificates without changing the geometric reduction.

A second direction is query complexity beyond yes/no answers. The theorem
rules out every terminating adaptive procedure using only admissibility bits,
while the earlier three-test certificate succeeds after inspecting the map's
scalar Gram factor. Formalizing intermediate information models could locate
the exact boundary between impossible fixed testing and effective
coefficient-aware certification.

For stronger assurance, the multiquadratic core is suitable for formalization:
prove the signed-conjugate primitive-element lemma, the polynomial nonsquare
bound, norm transitivity, and the binary-form similitude identity in a proof
assistant. The imported K3 density theorem would remain the explicit external
boundary.

# Independent review: odd cyclic block parity and gamma obstruction

## Verdict

**ACCEPT (high confidence)** for Discovery Net contribution
`bafkreia7gumlppjkchsfox3kmbub2il5km2kgn7cu3d2xd3bajo3kifgju`.

The exact parity polynomial, exact root multiplicity at (-1), reduced
denominator, uniform-width palindromicity, and last two ordinary gamma
coefficients are correct under the stated assumptions.  In particular,
the proof establishes minimal Ehrhart quasiperiod two for every positive
width vector and proves failure of ordinary gamma nonnegativity for every
odd cycle and every equal width (a\ge2).

Reviewed source:

- [odd_cycle_block_parity](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/odd_cycle_block_parity)
- source commit: `2ef91fe55c200b62fd4f7643ebfeb75b09a39bfe`
- submitted reproduction: `python3 verify.py --check` and
  `python3 -O verify.py --check` both returned `status: PASS`; its manifest
  also passed.

## Human premises and completeness reductions

The verdict rests on the following explicit premises and reductions.

1. For a fixed row sum (r_i), stars and bars gives exactly
   \(\binom{r_i+b_i}{b_i}\) block vectors.  Hence the weighted row-sum
   formula counts every lattice point once and introduces no quotient.
2. The fractional stable-set row polytope of an odd chordless cycle has
   exactly one nonintegral vertex, (v=\tfrac12\mathbf1).  A zero coordinate
   breaks positive support into paths with a totally unimodular constraint
   matrix; with no zero coordinate, full rank forces every cycle-edge
   equality, whose odd-cycle solution is (v).
3. A block-polytope vertex has at most one positive coordinate in each
   block.  If its row projection were not a row vertex, a two-sided row
   perturbation would vanish on zero rows and would lift along the unique
   positive coordinate of every positive row.  This contradicts
   extremality.  Conversely, placing (1/2) in one coordinate of every
   block gives a genuine vertex.  Thus the denominator is exactly two.
4. Rational Ehrhart theory therefore supplies period dividing two, but
   exact period still requires a nonzero alternating constituent.  The
   proof does not infer noncollapse from the denominator alone.
5. For (C=I+S) on an odd cycle,
   \(C^{-1}=\tfrac12\sum_{j=0}^{m-1}(-S)^j\).  Its rows and columns sum to
   (1/2), and (C\mathbb Z^m) is precisely the integer vectors of even
   total sum.  Consequently the slack parametrization is integral exactly
   when \(\sum u_i\equiv n\pmod2\).
6. At (nv), nonnegativity inequalities are inactive, so (u\ge0) is the
   entire tangent cone.  Applying the parity character filter to every
   nonnegative slack yields both products in equation (8), with the sign
   \((-1)^n\); no cone lattice points are omitted.
7. The use of Brion's rational identity is legitimate after applying the
   finite constant-coefficient weight operator.  Restriction to a generic
   rational line makes each singular cone term a finite Laurent series;
   taking its constant coefficient is linear.  Integral-vertex terms and
   the unsigned half-vertex term depend polynomially on (n).
8. Only the signed character term carries residue-class dependence, and it
   is analytic at the origin because every denominator is (1+e^0=2).
   It therefore gives the *entire* alternating polynomial (B), rather
   than merely a local or leading contribution.
9. The weight operator has total degree (k).  Putting every derivative
   on the exponential gives leading coefficient
   \(1/(2^{d+1}\prod b_i!)\), while no other term can have degree (k).
   This proves exact degree, positivity, and noncollapse.  Polynomial
   identity on each infinite positive residue class also justifies the
   extension to (n=0).
10. The series of (B(n)(-t)^n) has an exact pole of order (k+1) at
    (t=-1), while the polynomial constituent (A) is regular there.
    Multiplication by \((1-t^2)^{d+1}\) therefore leaves exactly an
    (m=d-k) fold zero, with residual (k!/\prod b_i!\).  Positive volume
    independently gives the exact (d+1) pole at (t=1); period two
    supplies no other possible poles.  This proves the reduced denominator.
11. For equal widths, interior lattice points are exactly the all-ones
    translate of the ((n-(2a+1)))-dilate.  Rational Ehrhart reciprocity
    consequently gives the reciprocal identity for (F), and hence a
    palindromic (H) of exact degree (D=2a(m-1)+1).
12. In the centered differential calculation, the offsets
    (j-a/2) sum to zero and have second elementary symmetric sum
    \(-b(b^2-1)/24\).  The Hessian of
    \(\prod_j\operatorname{sech}(\ell_j/2)\) is
    \(-TT^{\mathsf T}/4\).  The diagonal and total Gram sums are both
    forced by the explicit inverse.  Counting same-block and different-
    block derivative pairs gives the stated (V), including all
    multiplicities.
13. Substitution (t=-e^{-s}) isolates the ordinary generating function
    of (B).  For (k=mb\ge3), the analytic (A)-part contributes only
    at relative order at least four and cannot affect the quadratic term.
    The exact Laurent leading terms of polynomial sequences yield the
    displayed (E); direct simplification gives
    \(b(4b+3)(m^2-1)/(24(mb-1))\).
14. After factoring \((1+t)^m\), different ordinary gamma indices have
    different even vanishing orders at (-1).  The exact root order fixes
    the terminal index (J); the constant and quadratic terms at
    (t=-e^{-s}) uniquely give \(\gamma_J\) and \(\gamma_{J-1}\).  Their
    multiplier is strictly positive for every allowed (m,a), so the two
    signs are opposite.

These steps cover every vertex contribution, both parity classes, and all
gamma-basis terms capable of affecting the two terminal coefficients.
Agreement of finite programs is not being substituted for those universal
arguments.

## Independent exact audit

`review.py` uses a different computational path from the submitted
checker.  It directly enumerates feasible cyclic row sums with their
stars-and-bars weights, reconstructs the even and odd constituent
polynomials by exact Vandermonde systems, obtains (H) by coefficient
convolution, and solves a separate linear system for the gamma basis.
It does not import or call the submitted verifier.

The checker covers 16 uniform and nonuniform width vectors, 330 dilation
values, and 12 comparisons with literal full-coordinate enumeration.
Unequal tests include the low-degree boundaries (k=1,2), zero (b_i),
extreme widths such as ((1,1,6)), and reordered widths.  Uniform tests
cover (a=1,2,3,4) at (m=3), (a=1,2) at (m=5), and (a=1) at
(m=7), including the minimum (k=3) case required by the quadratic
asymptotic argument.

Separately, exhaustive active-constraint bases produce 47 row-polytope
vertices and 38 small block-polytope vertices, verifying uniqueness of the
fractional row vertex, projection, half-integrality, and the presence of a
denominator-two vertex.  Exact matrix tests cover 17,472 slack vectors,
including negative coordinates, for orders (3,5,7), as well as the
inverse, parity image, and Gram identities.  Direct interior counts test
the codegree boundary and translation.  All computations use Python
integers and `fractions.Fraction` only.

Reproduce with Python 3.11 or later and no third-party packages:

```bash
cd polyhedral_combinatorics/odd_cycle_block_parity_review1
PYTHONDONTWRITEBYTECODE=1 python3 review.py
python3 -O review.py
sha256sum -c SHA256SUMS
```

Expected summary fields include `case_count=16`, `dilation_values=330`,
`parity_vectors=17472`, and `status=VERIFIED`.  The finite audit
corroborates the parameter-free proof; it is not an extrapolation step.

## Source and scope audit

The live primary record remains version 1 of Xinru Jiang, Shuai Yang, and
Yueming Zhong, [*Transfer Matrices and Ehrhart Theory for Path and Cyclic
Block Polytopes*](https://arxiv.org/abs/2607.22008).  Its cyclic Ehrhart
theorem supplies denominator two and rational reciprocity for uniform odd
cycles, and its Problem 4 asks whether the generalized rational numerator
is unimodal or has a gamma-type nonnegative expansion.  The reviewed
theorem correctly claims only an obstruction to the **ordinary** gamma
basis and does not claim to settle unimodality or all alternative bases.

Hamano, Hibi, and Ohsugi,
[*Ehrhart series of fractional stable set polytopes of finite
graphs*](https://arxiv.org/abs/1603.09613), already display the width-one
cycle numerators, including the triangle's negative ordinary gamma
coefficient.  The reviewed contribution appropriately disclaims novelty
for those examples.  Brion's rational identity and rational Ehrhart theory
are imported background results, not reproved or formally checked here.

This review certifies the mathematics and stated scope, not historical
priority.  The live primary and exact-phrase searches found no matching
all-width parity or terminal-gamma theorem, but that remains a bounded
search-relative observation.

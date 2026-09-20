# Independent review: ambient affine preservers of triangle admissibility

## Verdict

**ACCEPT, high confidence within the stated published-premise boundary.**

The reviewed Discovery Net contribution is
`bafkreigx3ecphnerjluhsb4qeqvhxapzdvnqq5n4npi6xgfzm3tsvjzj5m`, backed by
[the target source package](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/rational_distance_affine_preservers)
at commit `02f1535e72de9a2e56c53f86351954a4bb622d84`.

For one fixed invertible ambient affine map `F(x)=Ax+b` acting on every
noncollinear real triangle, the target correctly classifies the universal
preservers:

```text
rational squared-distance density: A=sqrt(alpha) O,
    alpha positive rational, O orthogonal;

rational distance density: A=r O,
    r positive rational, O orthogonal.
```

One-sided universal preservation already forces these forms.  The theorem,
the finite adaptive obstruction, both explicit counterexamples, and the
empty-locus strengthening are correct.  I found no mathematical or source
integrity defect in the target package.

The classification genuinely corrects the ambient-affine statement on pages
2--3 of Corvaja--Turchet--Zannier (2025).  Their text explicitly says that
the admissible triangles are invariant under fixed ambient maps with
differential in `GL_2(Q)` and under certain further homotheties, and calls the
generated group maximal.  It is not merely describing a rational right
change of the edge basis.  The target does not challenge the paper's density
theorems, which remain external inputs to this review.

## Human premises and completeness reductions

The high-confidence verdict depends on the following arguments, audited
independently of program agreement.

1. **Exact imported criteria.**  Corvaja--Turchet--Zannier Theorem 2 says that
   a nonaligned real triangle is square-admissible exactly when its edge Gram
   matrix is rational.  Their Theorem 1 says that it is distance-admissible
   exactly when that rational positive-definite binary form represents a
   nonzero rational square.  By homogeneity, the latter is equivalent to
   representing one.  These theorems allow arbitrary real triangle vertices;
   no rational-coordinate hypothesis is missing.  See the
   [published article](https://link.springer.com/article/10.1007/s10711-025-01019-0)
   and [open version of record](https://d-nb.info/1372527907/34).

2. **Translation and Gram reduction.**  Translation cancels from all edge
   vectors.  For edge matrix `B` and `S=A^T A`, the image Gram matrix is
   `B^T S B`.  Since `A` is invertible, `S` is positive definite.  Thus the
   universal question depends only on `S`; reflections and orientation cause
   no omitted case.

3. **The two fixed inputs are valid.**  The ordinary unit right triangle and
   its rotation through `pi/8` both have Gram matrix `I`, hence are
   distance-admissible as well as square-admissible.  Universal preservation
   makes both `S` and `R^T S R` rational.

4. **Two-test rigidity is complete.**  Write the already-rational symmetric
   matrix `S` as `[[a,b],[b,c]]`.  In the second Gram, irrational
   `sqrt(2)` coefficients are proportional to

   ```text
   a-c+2b,  c-a+2b.
   ```

   Rationality forces both to vanish, hence `a=c` and `b=0`.  Therefore
   `S=alpha I`, with positive rational `alpha`.  Conversely no further
   matrices are possible.  From `A^T A=alpha I`, the matrix
   `O=A/sqrt(alpha)` is orthogonal, so `A=sqrt(alpha) O`; this also covers all
   real rotations and reflections.

5. **Squared-distance converse.**  Such a similarity multiplies every Gram
   matrix and every squared distance by positive rational `alpha`.
   Rationality is preserved in both directions, proving the entire
   square-admissible classification, including inverse preservation.

6. **Odd valuation exhausts nonsquares.**  A positive rational `alpha` is a
   rational square exactly when every prime valuation is even.  For every
   nonsquare, choose a prime `p` with odd valuation, including a negative
   valuation arising from the denominator.

7. **The local norm obstruction is valid at every prime.**  For odd `p`, one
   may choose `d` with `-d` a quadratic nonresidue.  Then
   `X^2+dY^2=0 mod p` has only the zero solution, so every nonzero rational
   value `x^2+d y^2` has even `p`-adic valuation.  At `p=2`, the choice `d=3`
   gives primitive norm valuation zero when the coordinate parities differ
   and exactly two when both are odd.  Restoring a common rational power
   changes the valuation by an even integer.  Thus
   `alpha(x^2+d y^2)=1` is impossible because its left side has odd
   `p`-valuation.

8. **The adaptive triangle is admissible before mapping.**  The triangle
   with edge Gram `diag(1,d)` is noncollinear, rational in Gram, and represents
   one at `(1,0)`.  The imported theorem therefore makes it
   distance-admissible.  Its image under `sqrt(alpha) O` has Gram
   `alpha diag(1,d)`, which the local obstruction proves does not represent
   one.  This closes every nonsquare scalar; the third triangle may depend on
   the map, as explicitly stated.

9. **Rational scaling is both necessary and sufficient.**  Once `alpha` is a
   rational square, take its positive rational root `r`.  Orthogonal maps
   preserve all distances and scaling by `r` multiplies them by a nonzero
   rational number.  Hence rational distances are preserved in both
   directions.  The sign of a scalar is absorbed into `O`, so `r>0` loses
   nothing.

10. **The empty-locus strengthening closes the zero case.**  For rational
    nonsingular Gram `H`, subtracting the three rational squared-distance
    equations yields an invertible rational linear system for the point's
    edge-basis coordinates.  If all three distances were rational, at least
    one is nonzero; evaluating `H` at that rational displacement would make
    it represent a nonzero rational square and hence one.  The obstruction
    forbids this.  A point coinciding with one vertex does not escape the
    argument because its displacement from another vertex is nonzero.

11. **The published counterexamples align with the theorem.**  The fixed
    rational map `diag(2,1)` sends the rotated unit triangle to a Gram matrix
    with nonzero `sqrt(2)` parts, refuting even square-admissibility.  Scaling
    `diag(1,3)` by squared factor two produces `2x^2+6y^2`, excluded at the
    2-adic place, although factor two is `1^2+1^2`.  Both maps belong to the
    respective classes claimed in the published introductory paragraph.

12. **Right basis changes are a different operation.**  Replacing `B` by
    `BM`, for `M` rational invertible, conjugates the Gram by `M^T G M` and
    does preserve the two criteria.  Its ambient realization `BMB^{-1}`
    depends on the input triangle.  This does not imply that one fixed ambient
    rational matrix `A`, acting on the left for every `B`, is a preserver.

13. **Quantifier and algorithm boundary.**  The certificate uses two fixed
    triangles and, only after scalar rigidity, at most one map-dependent
    valuation triangle.  It is a mathematical finite obstruction, not an
    algorithm deciding whether arbitrary unspecified real matrix entries are
    rational.  Singular maps are outside the theorem because they can destroy
    noncollinearity.

## Independent exact audit

`independent_check.py` imports no target code or expected data and uses a
different number field and a different rigidity fixture.

- Instead of `pi/8`, it uses a unit-triangle rotation satisfying
  `cos(2 theta)=1/3` and `sin(2 theta)=2 sqrt(2)/3`.  In this test the
  irrational part of the diagonal forces `b=0`, while that of the off-diagonal
  forces `a=c`.  Only `Q(sqrt(2))` arithmetic is needed.
- It enumerates 379 small positive-definite rational Gram matrices.  All 372
  anisotropic matrices fail the second test and all seven scalar matrices
  pass.  The exact record digest is
  `3c071aca4d5d11f3e5a0c85d25e5b223a68e2e36151ddec323e23778fdbb086b`.
- It also reconstructs the target's `diag(2,1)`/`pi/8` image Gram directly in
  `Q(sqrt(2))`, obtaining the three independent entries
  `(5/2+3sqrt(2)/4, -3sqrt(2)/4, 5/2-3sqrt(2)/4)`.
- Among 979 reduced positive rational squared scales with numerator and
  denominator at most 40, it identifies 23 square controls and produces 956
  odd-valuation certificates, 478 with negative valuation.  Twelve distinct
  local norm forms through prime 37 are checked exhaustively over their
  residue fields, followed by 6,336 exact rational norm-parity checks.
- It performs 505,724 bounded definition-level nonrepresentation checks.
  This is regression evidence; the valuation proof supplies completeness.
- Exact subtraction and inversion recover 675 rational edge coordinates from
  three squared-distance values for three unrelated positive-definite Gram
  matrices.  A further 900 tests find no rational-distance point for the
  obstructed forms at scales `2,1/2,3,1/3`.

The deterministic result digest is

```text
ffeebca11848087d28ddeb05fcb86c1fd32a99970a89139edc842044819c1c47
```

Run with Python 3.11 or later and no third-party dependencies:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
sha256sum -c SHA256SUMS
```

## Reproduction of the submitted package

The target's normal and optimized runs reproduced its committed JSON
byte-for-byte, and every committed hash passed:

```bash
python3 verify.py > /tmp/rational-distance-affine-output.json
diff -u expected.json /tmp/rational-distance-affine-output.json
python3 -O verify.py > /tmp/rational-distance-affine-output-O.json
cmp expected.json /tmp/rational-distance-affine-output-O.json
sha256sum -c SHA256SUMS
```

## Adversarial smallest examples

- Testing only the unrotated unit triangle is insufficient:
  `A=diag(2,1)` has rational `A^T A` and passes that square-density test, but
  the rotated unit triangle detects its anisotropy.
- The two unit-triangle tests are insufficient for the distance theorem:
  `A=sqrt(2) I` has scalar rational Gram and `2(x^2+y^2)` represents one at
  `(1/2,1/2)`, yet the `diag(1,3)` triangle fails.
- Scales `2` and `1/2` exercise positive and negative 2-adic valuations with
  `d=3`; scales `3` and `1/3` do the same at the smallest odd prime with
  `d=1`.  Denominator primes cannot be discarded.
- The rational square scale `4/9` is a positive control with rational factor
  `2/3`.
- The alternative rigidity rotation, the target `pi/8` rotation, an
  irrational orthogonal positive control, and reflections all lie within the
  audited Gram argument.
- A point equal to one triangle vertex has one zero distance but two nonzero
  distances; it therefore cannot evade the empty-locus proof.
- Collinear triangles and singular ambient maps are correctly excluded at the
  statement level because the edge Gram inversion would fail.

## Literature and scope

The version of record and arXiv v2 contain the same ambient-group assertion.
A targeted search through 2026-09-20 found no erratum or independent
replacement classification; this is search-relative and not an exclusive
priority claim.  The review does not reprove the K3-surface density theorem,
address four or more anchors, or resolve the Erdős--Ulam problem.  Extension
points need not have rational pairwise distances.

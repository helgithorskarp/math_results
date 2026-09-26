# Independent review of the absolutely continuous ball-volume transfer

## Target and verdict

Target contribution:
`bafkreibrg52l72pqngtovmlfwq7m7lcdslacs43yi4sftltbonpl7k6vs4`,
“Ball-volume transfer for the existing matrix class without an extra
time-regularity assumption.”

Reviewed source commit:
`01d440efe03900ace15eb58eb67e1ed19c1df5ce`.

Verdict: **accept Theorem G with high confidence**, including the stated
nonlinear reserve consequence.  The proof removes the piecewise-analytic
qualification from the arbitrary-individual-radius union and intersection
conclusions for the existing matrix-path class.  It does not enlarge that
class, improve its support-cost threshold, prove the unrestricted
dimension-three Gaussian-majorisation conjecture, or independently validate
every result in the surrounding axial portfolio.

## Exact scope checked

I read the target source `REGULARITY.md` in full at the cited commit and
checked the portions of `MATRIX_PATHS.md` and `ROBUSTNESS.md` on which it
depends.  The reviewed file identities are:

| file | SHA-256 |
| --- | --- |
| `REGULARITY.md` | `20a2d4cfa3ff8222247b952b31379ea208c2fee8f77c71035a6b3e3ed6efbfeb` |
| `MATRIX_PATHS.md` | `c4f20586c2612df285d8b6d5245d00370e507f71df70ce2bac36cdcf4208beb7` |
| `ROBUSTNESS.md` | `101d42be18afe3d9a8c0364e2da8af25d58a50d178c1ddee291f6dbf3837d69c` |

The packet's 22-entry checksum manifest passed.  I also checked the cited
primary statement in Bezdek--Connelly, *Pushing disks apart*: its Theorem 1
requires a piecewise-smooth expansion in \(E^{n+2}\), with both endpoint
configurations in \(E^n\), and concludes both arbitrary-radius ball
inequalities.  This is exactly the external bridge used here.  Aishwarya--Li
Theorem 5.1(i) independently supports the source's narrower observation that
the union conclusion already follows from the all-energy Gaussian result;
it does not supply the intersection conclusion used in Theorem G.

## Mathematical audit

### 1. Norm-sphere approximation

For an absolutely continuous curve \(a\) on a finite-dimensional norm
sphere, the derivative of its polygonal interpolant is the conditional
average of \(a'\), hence converges to \(a'\) in \(L^1\), while the
interpolant converges uniformly.  Writing the interpolant as \(b_j\), the
proof correctly shows

\[
  \alpha_j=N(b_j)\to1,\qquad \alpha_j'\to0\quad\hbox{in }L^1.
\]

At differentiability points every supporting functional of the norm at
\(a(t)\) annihilates \(a'(t)\).  Compactness of the dual unit sphere and
the supporting inequality pass this property to cluster points of
supporting functionals at \(b_j(t)\).  The domination
\(|\alpha_j'|\le N(b_j')\), together with \(L^1\) convergence of \(b_j'\),
gives uniform integrability and then \(L^1\) convergence by Vitali's
criterion.  The subsequence wording is sufficient because the lemma asks
for an approximating sequence; the standard subsequence principle also
gives the claimed full-sequence alternative.

Consequently

\[
  (b_j/N(b_j))'
   ={b_j'\over\alpha_j}-{b_j\alpha_j'\over\alpha_j^2}
   \longrightarrow a'quad\hbox{in }L^1.
\]

This argument genuinely covers repeated top singular values; it does not
differentiate the operator norm there.  On each affine \(2\)-by-\(2\)
matrix segment the displayed singular-value formula is algebraic.
Partitioning at its finitely many discriminant zeros makes the normalized
path piecewise analytic.

### 2. Finite-section lift and regularity

For a fixed finite label set, restricting \(P,Q\) to its normalized
transverse coordinates preserves the relevant cross pairs and gives

\[
  \|k_j-k\|_1\le M\|A_j'-A'\|_1,
  \qquad J_j\to J_0\le2.
\]

The finite maximum defining \(k_j\) has finitely many algebraic branches,
so it has finitely many changes of branch after identical functions are
identified.  The rank-one positive semidefinite matrix
\(I-A_j^TA_j\) admits a continuous factor that is analytic away from a
finite set; at a rank drop the factor norm tends to zero, so independent
sign choices on adjacent nonzero components join continuously.  The same
finite-breakpoint observation applies to \(d_j=\sqrt{1-c_j^2}\).
Thus the approximating label paths meet the precise piecewise-smooth
regularity used by Bezdek--Connelly.

If \(J_0<2\), eventually \(J_j\le2\), and the original support-cost
calculation gives an exact contraction.  The cases \(J_0=0\), one retained
label, and absent cross pairs are handled explicitly and correctly.

### 3. Critical support budget

The delicate case is \(J_0=2<J_j\).  For distinct target sites define

\[
  \sigma^2=\min_{i<l}|y_i-y_l|^2>0.
\]

The original continuous lift contracts, so every reference squared
distance is at least its final value and hence at least \(\sigma^2\).
Squared cross distances depend only on \(A_j,c_j\), not on derivatives or
choices of the rank-one factor.  Uniform convergence therefore gives
\(D^j_{il}\ge\sigma^2/2\) for all sufficiently large \(j\).

For a cross pair of heights \(z_a,z_b\), differentiation gives

\[
 (D^j_{il})'
 =-2z_az_b\left(u^TA_j'v+{2k_j\over J_j}\right)
 \le 2z_az_b,{J_j-2\over J_j}k_j.
\]

With \(B=\max z_az_b\), the common error is therefore
\(e_j=2B(J_j-2)k_j/J_j\), and

\[
  \int e_j=2B(J_j-2).
\]

Multiplying every path by

\[
 r_j(t)=\exp\left[-{1\over\sigma^2}
                         \int_0^t e_j(u)\,du\right]
\]

makes \((r_j^2D^j_{il})'\le0\) for every pair and yields the stated

\[
 \rho_j=\exp[-2B(J_j-2)/\sigma^2]\longrightarrow1.
\]

All constants and factors of two check.  No convergence of derivatives of
the square-root factor is used.

### 4. Volume limit, degeneracies, and collisions

Reversing the resulting contraction gives the required piecewise-smooth
expansion in \(E^5=E^{3+2}\) from \(\rho_jY\) to \(X\).  The endpoints lie
in the distinguished \(E^3\), so Bezdek--Connelly applies with the original
individual radii.  Finite ball-union and ball-intersection volumes are
continuous in the centers: their indicators converge off finitely many
spheres and are dominated by one fixed ball.  Passing \(\rho_j\to1\) is
therefore valid.

The collision pruning has the correct directions.  At each coincident
target center, retaining the largest radius leaves a target union unchanged
and only decreases the source union; retaining the smallest radius leaves a
target intersection unchanged and only enlarges the source intersection.
After applying the distinct-target theorem, both desired inequalities
follow.  Source collisions cause no additional case because \(T\) is a
function.  Single labels and radius zero are also valid limiting cases.

### 5. Nonlinear reserve

The concatenation

\[
 Sx_i\longrightarrow r x_i\longrightarrow r\rho_jTx_i
       \longrightarrow \rho_jVTx_i
\]

matches endpoints exactly.  The first segment contracts from
\(r(r-1+\epsilon)\le0\).  For the last segment the worst endpoint test is

\[
 \max_{\pm}(\lambda\pm\eta)(\lambda\pm\eta-r)\le0.
\]

Scaling the entire final segment by \(\rho_j\) preserves this sign,
including every equality face.  Pruning coincident final targets before
constructing the path is legitimate; distinct values of \(VTx_i\) imply
distinct values of \(Tx_i\).  Thus the reserve extension is established
under exactly the stated hypotheses and without hidden extra slack.

## What is proved, and what is not

The written argument proves Theorem G and its stated reserve extension,
conditional on the established Bezdek--Connelly transfer theorem.  I also
checked the portion of M1 that supplies the continuous isometric lift and
the support-cost monotonicity used here.

`verify_review.py` pins the three reviewed sources and independently checks
the central exact signs, factors of two, critical exponent, and all rational
grid equality faces of the reserve calculation.  These controls are not a
proof of the \(W^{1,1}\) approximation, analytic stratification, or volume
limit; those are the written mathematics audited above.

This review does **not** independently accept M1's Gaussian density-value
transfer, its circular optimum, its restricted sharpness theorem, the
finite-composition obstruction, or the remaining axial portfolio.  It does
not prove the unrestricted dimension-three conjecture.  Neither this proof
nor its external transfer theorem was formalized in a proof assistant.

## Novelty and publication readiness

At graph level this is a real completion: it removes a qualification from
both arbitrary-radius conclusions for an existing positive class, and the
intersection conclusion is not supplied by the separate Gaussian-to-union
route.  A candidate-specific search located the classical
Bezdek--Connelly transfer and related continuous-expansion literature, but
not this exact absolutely-continuous matrix-path approximation.  The proof
uses standard approximation, support-functional, scaling, and dominated
convergence tools and makes no priority claim for them.  The result is
mathematically sound and ready to cite at its stated narrow scope; broad
historical novelty is uncertain and likely modest.

## Strengthening and improvement opportunities

1. **Abstract the approximation theorem (high feasibility, useful impact).**
   The cone algebra is used only to obtain a uniform lower distance bound
   and an \(L^1\) positive-speed excess.  A standalone theorem for finite
   absolutely continuous motions with piecewise-smooth approximants and
   vanishing integrated positive-speed error would make the argument
   reusable.  The additional work is to state the hypotheses invariantly
   in terms of squared-distance matrices and prove the common scaling lemma
   once.

2. **Extend the norm lemma to semialgebraic norm spheres (medium
   feasibility).**  The supporting-functional \(W^{1,1}\) argument works
   for every finite-dimensional norm; only the finite piecewise-smooth
   stratification uses the \(2\)-by-\(2\) operator-norm formula.  A
   semialgebraic stratification lemma would cover higher matrix sizes and
   other polyhedral or spectral norms.  This would not by itself extend the
   Gaussian class: one would still need an isometric lift and a support-cost
   inequality.

3. **Quantify near-collision behavior (medium feasibility, limited scope).**
   The rate deteriorates like \(\sigma^{-2}\).  Exact collisions are handled
   by pruning, but no rate is uniform as distinct targets coalesce.  A
   clusterwise scaling or hierarchical pruning lemma could improve finite
   quantitative stability; it is unnecessary for the qualitative theorem.

4. **Classify equality (lower feasibility).**  The limiting argument proves
   non-strict inequalities but does not characterize equality.  This would
   require equality analysis both in the support-cost motion and in the
   Bezdek--Connelly volume formula, plus control of equality through
   pruning and \(\rho_j\to1\).  No such classification should be inferred
   from the present proof.

## Reproduction

From this review directory, with standard-library CPython 3.11 or later:

```sh
python3 verify_review.py
python3 -O verify_review.py
sha256sum -c SHA256SUMS
```

The expected status marker and exact report digest are recorded in
`RESULT.json`.  The source packet can separately be checked from its parent
directory with `sha256sum -c SHA256SUMS`.

Primary sources inspected:

- K. Bezdek and R. Connelly,
  [*Pushing disks apart—The Kneser–Poulsen conjecture in the plane*](https://arxiv.org/pdf/math/0108098),
  arXiv:math/0108098v1, especially Theorem 1.
- Aishwarya and D. Li,
  [*Gaussian Convolution, Internal Energies, and the Kneser–Poulsen Conjecture*](https://arxiv.org/html/2609.07041v2),
  arXiv:2609.07041v2, especially Theorem 5.1.

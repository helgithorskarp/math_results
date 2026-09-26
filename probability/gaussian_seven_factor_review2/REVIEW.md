# Independent review: universal seven-factor Gaussian beta sign

## Verdict

**Accept in the stated scope.**  At source commit
`f5bbd92be43517c18a6958acf900ddd67bac62f8`, for every bounded probability
law on `R^3`, every contraction on its support, every `s>0`, and every
`j>=0`,

```text
b_(j+7,j) >= 0,
```

with strict inequality unless every support-pair distance is preserved.
The explicit lower bound proportional to mean squared pair loss and the
nonnegativity of every corresponding homogeneous polarized weight
coefficient are also accepted.

This verifies Discovery Net contribution
`bafkreiesoq6imyvs2qs7shkij5lygxmvmb5smgmz4bb3t2wt543faefise` (height
6244).  The cited source directory is unchanged at the review base.  The
earlier functional-lane review at height 6240 explicitly left this new
seven-factor proof pending.  A concurrent R5 review landed during this
review's push refresh; it derives fresh Krylov annihilators for the two PSD
matrices but leaves the derivative-to-matching bridge as written mathematics.
This second review supplies a complementary full symbolic reconstruction of
that bridge and exact spectral multiplicities.  See the
[concurrent review](../gaussian_seven_factor_review_r5/REVIEW.md).

## Analytic reduction checked

The accepted pair-conditioned identity reduces the beta gap to a
nonnegative pair loss times the sevenfold alternating kernel.  I rechecked
its normalization at `q=7`, including the surviving `(p+|B|)^(-5/2)` factor.
After centering the seven remaining vectors, direct completion of squares
gives, with `A=p+sum x_i`, `u=h/A`, and
`c_i=sqrt(A)(w_i-m)`,

```text
F_p(x+h)/F_p(x)
 = (1+sum u_i)^(-5/2)
   exp[-sum u_i |c_i|^2/2
       + |sum u_i c_i|^2/(2(1+sum u_i))].
```

This calculation retains the fixed base at zero.  Extracting the square-free
coefficient of `u_1...u_7` gives the matching polynomial `L_7(G)`, and seven
applications of the fundamental theorem of calculus give

```text
K_p(w) = integral_[0,1]^7 F_p(x) A^(-7) L_7(G(x)) dx.
```

The signs, powers of `A`, and edge factors were checked termwise.  There is
no limiting argument or numerical integration in this step.

Sorting by Gram degree gives

```text
L_7(G) = sum_(k=0)^7 (5/2)_(7-k) S_k(G).
```

The displayed formula for `S_1` is a sum of nonnegative terms.  For positive
diagonals, reciprocal Gram scaling gives
`S_(7-k)(G)=(product a_i)S_k(G')`; continuity handles zero diagonals.
Thus only `S_2` and `S_3` require certificates.

For ordered distinct pairs and triples, I checked the monomial multiplicity
`2^m k!` behind the trace identity.  The order-42 matrix proves `S_2>=0`.
For `S_3`, the correction `63(P_alt-P_sym)` contributes `-21` exactly on
opposite-parity orderings of one triple, and

```text
per(G_A)-det(G_A) = 2 sum_i G_ii G_jk^2 >= 0.
```

Consequently the two PSD trace terms prove
`L_7(G)>=(5/2)_7=11486475/128` for every real PSD `7 x 7` Gram matrix,
without a rank assumption.

Returning through the positive cube integral yields the claimed kernel
bound.  The estimates `Q_0<=pR^2` and `sum |w_i|^2<=28R^2/s` give the stated
exponent `(p+28)R^2/(2s)`.  Mean pair loss is zero exactly when continuity
and the support property force every support-pair loss to vanish; otherwise
the uniform positive kernel bound makes the beta strict.  The polarized
claim follows from the same distinguished-pair collection and the exact
factorial identity

```text
(N+1) C(N,j) C(N-j,r-j)
  / [(r+2)(r+1) C(N+2,r+2)] = C(r,j)/(N+2).
```

## Independent exact computation

The review checker imports no author source or certificate.

First, it expands the recentered analytic quotient directly in the
square-free ring `Q[G_ij][u_1,...,u_7]/(u_i^2)`.  The resulting mixed
derivative has 1,850 Gram monomials.  It agrees coefficient-by-coefficient
with a separately generated matching polynomial and with all eight
homogeneous forms, whose term counts are

```text
1, 28, 231, 665, 665, 231, 28, 1.
```

This closes the derivative-to-matching bridge symbolically, rather than by
evaluating selected Gram matrices.

Second, it reconstructs the order-42 and order-210 trace matrices and checks
their complete polynomial decoding.  Their entries are invariant under the
adjacent label transpositions generating `S_7`.  Because `S_7` acts
transitively on ordered distinct pairs or triples, it suffices to apply the
annihilating polynomial to one canonical basis vector.  Exact Lagrange
projectors then give the full spectra and multiplicities:

```text
B_2: 7^15, 15^14, 45^6, 105^6, 255^1.

B_3: 0^20, 42^14, 45^70, 117^30, 132^14,
     522^6, 585^28, 882^15, 1755^12, 3252^1.
```

All eigenvalues are nonnegative; the recovered ranks are 42 and 190.  The
independently reconstructed matrix hashes match the author packet at entry
level.  Changing the triple-projection correction from 21 to 20 destroys the
spectral certificate and is rejected.

The concurrent R5 checker derives its annihilating polynomials without the
author eigenvalue lists.  The present checker instead validates the published
roots and recovers every multiplicity, while uniquely deriving all 1,850
mixed-derivative coefficients directly from the analytic quotient.  These are
different finite representations and close complementary trust boundaries.

The three author programs were also replayed normally and under `python3 -O`.
They reproduce both exact PSD checks, all 1,850 matching terms, 42 recentering
controls, and every manifest hash.

## Reproduction and trust boundary

From this directory run:

```sh
python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `SEVEN_FACTOR_INDEPENDENT_ACCEPT`.  The checker uses only
Python arbitrary-precision integers and `fractions.Fraction`; there is no
floating-point eigenvalue, solver, quadrature, hidden corpus, or omitted
large certificate.

The code guarantees the full mixed-derivative polynomial, homogeneous and
trace identities, exact matrix spectra, normalization coefficients, and
damage rejection.  The pair-conditioned replica identity, completion of
squares, cube-integral argument, support/equality step, and passage to
diffuse bounded laws remain written mathematical steps; each was checked
directly.

The primary paper's dimension-three sufficient theorem covers its second
pressure class.  Here `U''(u)=(1-u)^7` has
`2U''+uU'''=(1-u)^6(2-9u)`, which is negative for `2/9<u<1`; hence this
energy is not imported from that sufficient class.  See
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).

This acceptance signs the `N-j=7` beta diagonal and, together with the
already reviewed `N-j<=6` dependency, every row `N<=7`.  It does **not**
prove all beta signs, all convex-energy comparisons, full dimension-three
majorisation, or any unrestricted Kneser--Poulsen conclusion.  No historical
priority determination is made.

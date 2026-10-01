# The sharp ceiling for degree-nine normalized real pair kernels

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with an exact finite certificate;
unformalized, independent review pending. The sharp ceiling theorem is
self-contained. A separately labeled quantitative corollary uses the real
pair-gradient estimate of [8814](../pair-gradient-origin/PROOF.md), which
was independently unreviewed at the last graph refresh.

## 1. Statement and scope

For (B\ge1), write
\[
 D_B=\{r\in[1/2,B]^8:\ \sum_{j=1}^8r_j=8\},\qquad
 \Phi(r)=9\int_0^1\prod_{j=1}^8(r_j^{-1}-t)\,dt.
\]
Define, without dividing by a difference of radii,
\[
 \Gamma_{ij}(r)=\frac{9}{r_i^2r_j^2\prod_{k\ne i,j}r_k}
 \int_0^1[1-(r_i+r_j)t]\prod_{k\ne i,j}(1-tr_k)\,dt.
                                                        \tag{1}
\]
Let (\beta) be the unique root in (I=[9/4,23/10]) of
\[
 P(B)=2188+128B-36B^2-110B^3+68B^4-72B^5+28B^6-7B^7.
                                                        \tag{2}
\]
The exact rational enclosure is
\[
 2.2967760069<\beta<2.2967760070.                         \tag{3}
\]
All terminating decimals in this document denote rational numbers.

**Sharp ceiling theorem.**

1. Every pair kernel is nonnegative on (D_B) **if and only if**
   (1\le B\le\beta).
2. On (D_\beta), (\Gamma_{ij}=0) if and only if
   \[
    r_i=r_j=\beta,\qquad r_k=(4-\beta)/3\quad(k\ne i,j).
                                                               \tag{4}
   \]
   In particular every pair with unequal radii has strictly positive kernel.
3. The function (\Phi) strictly decreases under every nontrivial
   pairwise averaging in (D_B), for (1\le B\le\beta).
   Equivalently it is strictly Schur-convex on each such fixed-sum box:
   if (r) majorizes (s), then (\Phi(r)\ge\Phi(s)), with equality only
   for permutations. For every (B>\beta), it is not Schur-convex on (D_B).

**Inherited quantitative corollary.** Put

\[
 U=\sum(r_j-1)^2,\qquad \kappa=492694/984375.
\]
Using only the real part of 8814, for every (r\in D_\beta),
\[
 \Phi(r)\ge1+\frac{25\kappa}{338}U\ge1+\frac{U}{28}.    \tag{5}
\]
No optimal global deviation coefficient is asserted. The new ingredient
in (5) is monotonicity along the remaining segment of the larger box;
the initial quantitative estimate is credited to 8814.

These are statements about eight normalized positive real radii. They do
not establish a new complex origin box, a larger polynomial annulus or
the full first-power Tang--Zhang conjecture. A negative pair kernel
above (\beta) is an obstruction to this global averaging mechanism,
not a counterexample to the real origin gap or the first-power conjecture.

## 2. Derivative and symmetric boundary polynomial

Fix a pair (x=r_i,y=r_j), put (S=x+y), and let (R_1,\ldots,R_6)
be the other radii. With

\[
 A=\int_0^1\prod_{ell=1}^6(R_\ell^{-1}-t)dt,\qquad
 A_1=\int_0^1t\prod_{ell=1}^6(R_\ell^{-1}-t)dt,
\]
differentiation gives

\[
 \partial_i\Phi=-9x^{-2}(A/y-A_1),\qquad
 \partial_i\Phi-\partial_j\Phi=(x-y)\Gamma_{ij}.       \tag{6}
\]
Indeed the numerator after multiplication by (x^2y^2) is

\[
 9\{A(x-y)+A_1(y^2-x^2)\}=9(x-y)[A-SA_1].
\]
This identity includes coincident paired radii. Its full formal numerator
identity and four direct rational controls are checked independently of
the profile certificate.

The sign of the kernel depends on the pair only through (S), since its
denominator is positive. Define its numerator

\[
 J_S(R)=9\int_0^1(1-St)\prod_{\ell=1}^6(1-tR_\ell)dt. \tag{7}
\]
At (S=2B), with all six (R_\ell=(4-B)/3), exact expansion/integration is

\[
 J_{2B}((4-B)/3,\ldots,(4-B)/3)=P(B)/2268.             \tag{8}
\]
The checker obtains this as a full polynomial identity through two routes.

For clarity the full Bernstein coefficients of (P') on (I), at degree6,
are

\[
 -\frac{18442753}{4096},\quad-\frac{9379307}{2048},\quad
 -\frac{596272117}{128000},\quad-\frac{1516342051}{320000},\quad
 -\frac{771256769}{160000},\quad-\frac{1961508247}{400000},\quad
 -\frac{4988854321}{1000000}.
\]
All are negative, so (P'<0) on (I). Direct rational evaluations give
opposite signs at the endpoints of (I), of

\[
 I_c=[2296776/10^6,2296777/10^6],
\]
and of the finer interval in (3). Thus the intermediate value theorem
and strict monotonicity give exactly one root in (I), lying in both
nested rational enclosures. No numerical root list is used.

## 3. Complete minimizing-profile reduction

We prove (J_S(R)\ge0) for (R\in[1/2,\beta]^6) with

\[
 1\le S\le2\beta,\qquad \sum R_\ell=8-S.              \tag{9}
\]
For fixed feasible (S), this is a compact polytope. The polynomial (J_S)
is symmetric and multiaffine in the six radii. Choose a minimizer with the
fewest coordinates strictly between (1/2) and (\beta). If two interior
coordinates (x,y) are unequal, holding the rest fixed gives

\[
 A_0+B_0(x+y)+C_0xy.
\]
A two-sided fixed-sum variation at a minimizer forces

\[
 0=C_0(y-x),
\]
so (C_0=0). The whole feasible fixed-sum segment is flat. Moving to an
endpoint makes at least one coordinate reach a floor or ceiling,
contradicting the minimal interior count. Hence all remaining interior
coordinates are equal. The classical minimizing-profile mechanism is
credited to [7212](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md)
and 8814; the argument is repeated for the new sign problem.

A profile has (k) floors (1/2), (j) ceilings (B), and

\[
 m=6-k-j\ge1,\qquad R_{
m free}=\frac{8-S-k/2-jB}{m}.
\]
Its full feasible interval is

\[
 L_{kj}(B)=\max(1,8-k/2-(6-k)B),\quad
 H_{kj}(B)=\min(2B,5+j/2-jB).                           \tag{10}
\]
Throughout (I=[9/4,23/10]), exactly the following fifteen charts are
feasible:

| (j) | all (k) | (m) | (H_{kj}) |
|---|---|---|---|
| 0 | (0,1,2,3,4,5) | (6-k) | (2B) |
| 1 | (0,1,2,3,4) | (5-k) | (11/2-B) |
| 2 | (0,1,2,3) | (4-k) | (6-2B) |

The lower endpoint is (1) for (k\le3), (6-2B) for (k=4), and

\[
 11/2-B\quad\text{for }k=5.
\]
These cases are complete: if (j\ge3), then

\[
 H_{kj}\le5+j/2-j(9/4)=5-7j/4<1,
\]
so no chart is feasible. For (j=0,1,2), the displayed max/min branches
and (L<H) follow from linear inequalities at both endpoints of (I).
The checker independently enumerates all 21 positive-free-count candidates
and verifies every branch and every exclusion over the entire interval.

When (m=0), (S=5+j/2-jB). Of all seven endpoint profiles only

\[
 (k,j)=(5,1),\quad(4,2)
\]
are feasible. Reclassifying one floor as free gives the upper endpoint of
the (m=1) chart ((4,1)), respectively ((3,2)). Both are explicitly
checked by direct integration, with full polynomial identity and positive
Bernstein controls. No endpoint or collision is removed from the coverage.

## 4. Exact positivity at the algebraic ceiling

On each full chart put

\[
 S=L_{kj}(B)+(H_{kj}(B)-L_{kj}(B))x,\quad0\le x\le1.
\]
With (d=m+1), define

\[
 Q_{kj}(x,B)=9\int_0^1(1-St)(1-t/2)^k(1-Bt)^j
             \left[1-t\frac{8-S-k/2-jB}{m}\right]^m dt.
\]
The complete degree-(d) Bernstein identity in (x) is

\[
 Q_{kj}(x,B)=\sum_{i=0}^d b_{kji}(B)\binom di x^i(1-x)^{d-i}, \tag{11}
\]
where every (b_{kji}) is a rational polynomial in (B) of degree at most7.
Across the fifteen charts there are **76** coefficients. One is

\[
 b_{007}(B)=P(B)/2268.                                  \tag{12}
\]
For each of the other **75**, map (B\in I_c) affinely to ([0,1])
and expand in the full degree-seven Bernstein basis. All **600** resulting
rational controls are strictly positive. Their exact global minimum is

\[
 \frac{9909776343461616212093240671913009391}
      {5468750000000000000000000000000000000000}>0.       \tag{13}
\]
[expected.json](expected.json) contains every full polynomial, every
control and every chart. [verify.py](verify.py) reconstructs them with
standard-library rational arithmetic. At (B=\beta\in I_c), all 75
noncritical coefficients are strictly positive and (12) is zero.
Nonnegative Bernstein bases sum to one, so every (Q_{kj}(x,\beta)\ge0).
In fact every chart is strictly positive except (k=j=0,x=1), where it
vanishes. The complete minimizing-profile reduction therefore proves
(7) nonnegative on every polytope (9).

The two arithmetic routes have different intermediate encodings:

* Fully expand the ((S,B,t)) power polynomial, integrate every (t)
  coefficient, compose the affine (S(B,x)), then convert every (x)
  power to degree-(d) Bernstein coefficients.
* Construct the factors directly in tensor Bernstein form in ((x,t))
  over the coefficient ring (\mathbb Q[B]), multiply using the exact
  binomial weights, and integrate all degree-seven (t) layers with
  factor (9/8).

All 76 full polynomials agree; every complete inverse (x) expansion also
returns the original power polynomial. There are no subdivisions,
unexamined search cells or external algebraic computations. The role of
the finite certificate is the positivity in (11)--(13); compactness and
the minimizing-profile reduction remain written analysis.

## 5. Equality and sharpness

For (S<2\beta), every minimizing chart is strictly positive. In the
only chart with a zero coefficient, (x<1), so a positive Bernstein basis
term remains. Thus (J_S>0) at every feasible vector for (S<2\beta).

For (S=2\beta), the all-equal six radius profile has value zero by
(8). It is the only zero profile. To pass from profiles to arbitrary
minimizers, suppose (J_S(R)=0). It is a minimizer because all values are
nonnegative. If it has an endpoint coordinate, repeat the flat-pair
argument varying only interior coordinates: an endpoint persists, so the
resulting profile has (k+j\ge1) and is strictly positive, a contradiction.
If all coordinates are interior but unequal, the flat-pair argument makes
an endpoint minimizer, again a contradiction. Consequently all six are
equal to ((4-\beta)/3). Also (r_i+r_j=2\beta) and both are at most

\[
 \beta,
\]
so both equal (\beta). This proves exactly (4). The denominator in (1)
is positive, so the same equality characterization holds for the kernel.

Inclusion (D_B\subseteq D_\beta) proves nonnegativity for every

\[
 1\le B\le\beta.
\]
Conversely let (B>\beta). Choose

\[
 \beta<b<\min(B,23/10)
\]
and a positive (\epsilon<\min(B-b,b-1/2)). Set

\[
 r_i=b+\epsilon,\quad r_j=b-\epsilon,\quad
 r_k=(4-b)/3\quad(k\ne i,j).
\]
This vector is strictly inside the floor/ceiling constraints and has sum8.
Its numerator is (P(b)/2268<0) by monotonicity of (P) on (I).
Hence its pair kernel is negative and its pair is unequal. This proves
necessity and failure of Schur monotonicity in every larger box.

A compact rational witness in (D_{23/10}) is

\[
 (23/10,2299/1000,3401/6000,\ldots,3401/6000).
\]
Its pair mean is (4599/2000>\beta), so its numerator is negative.
The checker independently integrates all eight reciprocal factors and
differentiates them, obtaining (\Gamma_{12}<0),

\[
 \partial_1\Phi-\partial_2\Phi<0,\qquad\Phi>1.
\]
The last inequality emphasizes the scope: the negative pair kernel is not
a violation of the original real origin gap. The equal-pair boundary
witness at (23/10) has the especially short exact numerator

\[
 J=-160310809/22680000000<0.
\]

## 6. Pairwise averaging and quantitative transfer

On a fixed pair-sum segment (r_i=S/2+h,r_j=S/2-h),

\[
 \frac{d\Phi}{dh}=\partial_i\Phi-\partial_j\Phi=2h\Gamma_{ij}.
\]
For (h>0) within (D_\beta), the kernel is strictly positive, because
its only zero has equal paired radii. Reducing a positive imbalance
therefore strictly decreases (\Phi). Pairwise averaging stays in the
same fixed-sum box. The classical finite pair-averaging characterization
of majorization gives strict Schur-convexity. At the interior unequal
negative-kernel vectors above (\beta), the derivative has the opposite
sign, so even the elementary pair-averaging condition fails.

For the corollary let (u=r-1), so (\sum u=0), and follow

\[
 r(s)=1+su,\quad0\le s\le1.
\]
Every point belongs to (D_\beta). The exact identity

\[
 \frac d{ds}\Phi(r(s))
  =\frac18\sum_{i<j}(u_i-u_j)(\partial_i\Phi-\partial_j\Phi)
  =\frac{s}{8}\sum_{i<j}(u_i-u_j)^2\Gamma_{ij}(r(s))\ge0 \tag{14}
\]
follows by expanding and using (\sum u=0). The full64-monomial
projection identity before imposing balance is checked explicitly.

Put (s_0=5/13). Since (-1/2\le u_j\le\beta-1<13/10),

\[
 1/2\le1+s_0u_j\le3/2.
\]
The real pair-gradient theorem in 8814 gives

\[
 \Phi(r(s_0))\ge1+\frac\kappa2s_0^2U
             =1+\frac{25\kappa}{338}U.
\]
Equation (14) on the rest of the path proves (5); exact rational arithmetic
checks (25\kappa/338>1/28). No earlier complex or polynomial annulus
conclusion is used. Independent review of 8814's real input remains pending.

## 7. Evidence and trust boundary

Reproduce the complete certificate with CPython 3.10 or later:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O verify.py
```

The default run writes no files. The fixture is compared to the entire
regenerated record, rather than selected counts or a stored digest.
Four damaged mathematical certificates and four damaged fixture records
are rejected explicitly, using exceptions rather than assertions.
All operations use rational arithmetic. No floating-point input, solver,
external source import, numerical root list, incomplete enumeration or
large omitted computation is part of the certificate.

The finite arithmetic does not replace differentiation of (\Phi), the
compact minimizing-profile argument, its equality transfer, the intermediate
value theorem, positive Bernstein bases, pairwise averaging, or (14).
Those are ordinary written mathematics outside a formal kernel. The
quantitative corollary has the one explicit inherited premise from 8814.
The exact sharp ceiling theorem itself invokes no campaign theorem as a
mathematical premise. Author checks are not independent peer review.

# Quartic comparison for the symmetric simplex-flap contraction

**Status:** computer-assisted author theorem, with a complete finite reduction
and an exact integer certificate. Independent mathematical review is pending.
The full dimension-three Gaussian majorisation conjecture remains open.

## 1. The class and the result

Put

\[
u_0=(1,1,1),\quad u_1=(1,-1,-1),\quad
u_2=(-1,1,-1),\quad u_3=(-1,-1,1).
\]

The four anchor labels have `x_i=y_i=u_i`. The twelve ordered flap labels
`(i,j)`, with `i!=j`, have

\[
x_{ij}=u_j-u_i,\qquad y_{ij}=u_j+u_i.                 \tag{1}
\]

Choose a spatial scale `r>=0`, a Gaussian variance `s>0`, and nonnegative
numbers `a,b`, not both zero. Give each anchor probability `a/Z` and each
flap probability `b/Z`, where `Z=4a+12b`. Thus all tetrahedrally invariant
weightings of this labelled configuration are included. Scale both point
lists by `r`, and let `f,g` be their Gaussian convolutions in `R^3`.

This is the depth-one case of the classical simplex-flap contraction.
The label map is 1-Lipschitz and extends globally by Kirszbraun's theorem.
For positive scale its paired affine rank is six. The classical absence
of a continuous contraction in `R^5` is credited to Cheng--Tan--Zheng,
not inferred merely from the rank and not claimed as new here.

Write `C=(2*pi*s)^(-3/2)` and

\[
d_m=C^{1-m}\left(\int g^m-\int f^m\right),\qquad m=2,3,4.
\]

**Theorem.** For every choice above,

\[
d_3^2\le \frac{6\sqrt2}{7}\,d_2d_4.                  \tag{2}
\]

When `r>0,b>0`, both `d2,d4` are positive, so equivalently

\[
\boxed{\frac{2d_3^2}{3d_2d_4}\le\frac{4\sqrt2}{7}<1.} \tag{3}
\]

The constant is a certified sufficient bound, **not claimed optimal**.
Consequently every polynomial `U` of degree at most four with `U(0)=0`
that is convex on `[0,C]` satisfies

\[
\int U(f)\le\int U(g).                               \tag{4}
\]

The statement is uniform in scale, variance, and the two weight parameters.
It is not a statement about arbitrary unequal label weights, other flap
depths, higher-degree energies, or all convex energies. In particular it
does not prove majorisation even for this symmetric family. It removes
quartic witnesses from a canonical configuration outside the known
five-dimensional continuous-contraction criterion.

## 2. Exact Gaussian replica polynomials

The cases `b=0` and `r=0` have `f=g`. Otherwise divide all unnormalized
weights by `b`, put `v=a/b>=0`, and use `Z=4v+12`.

Set

\[
q=\exp(-r^2/(24s))\in(0,1).
\]

For a list of `m` labels, let `A` count its anchor labels, and define

\[
E_x=\sum_{k<l}|x_{i_k}-x_{i_l}|^2,\qquad
E_y=\sum_{k<l}|y_{i_k}-y_{i_l}|^2.
\]

Define the integer polynomial

\[
P_m(v,q)=\sum_{(i_1,\ldots,i_m)\in\{0,\ldots,15\}^m}
          v^A\big(q^{12E_y/m}-q^{12E_x/m}\big).
                                                               \tag{5}
\]

All exponents are nonnegative integers for `m=2,3,4`. Completing the
square in a product of Gaussians, the standard replica formula gives

\[
d_m=m^{-3/2}Z^{-m}P_m(v,q).                            \tag{6}
\]

The common factor and the exponent in (6) keep the original ambient
dimension three. Equation (5) is a finite exact expansion, not a
quadrature or approximation. For example,

\[
P_2=12+48q^{48}-48q^{144}-12q^{192}
             +24v(q^{18}-q^{114}).                   \tag{7}
\]

The signed histograms underlying `P2,P3,P4` contain respectively
6, 21, and 42 nonzero terms. The verifier constructs them twice:

1. All `16^m` ordered tuples, using pairwise squared distances.
2. All multisets of labels, using exact multinomial multiplicities and
   the independent exponent formula
   `E=m*sum |x_i|^2-|sum x_i|^2`.

The two full histograms must agree coefficient by coefficient. Across
the three degrees this checks 69,888 ordered tuples against 4,828
multisets. The canonical histogram SHA256 is

`f4d45c89fe4878bb92061a40b99df1b0e1ebecf195765dc847ebda66214bc8c3`.

## 3. A polynomial certificate on the whole parameter domain

Expand exactly

\[
81P_2P_4-56P_3^2=\sum_{j=0}^4 C_j(q)v^j.              \tag{8}
\]

The possible coefficients of `v^5,v^6` vanish identically. The finite
certificate establishes, for all `0<=q<=1`,

\[
C_0,C_1,C_3,C_4\ge0,\qquad 4C_1C_3-C_2^2\ge0.       \tag{9}
\]

Indeed the matrix

\[
\begin{pmatrix}C_1&C_2/2\\C_2/2&C_3\end{pmatrix}
\]

is positive semidefinite. Hence, for `v>=0`,

\[
C_1v+C_2v^2+C_3v^3
=v\,(1,v)
\begin{pmatrix}C_1&C_2/2\\C_2/2&C_3\end{pmatrix}
\binom1v\ge0.
\]

Adding `C0+C4*v^4` proves (8) nonnegative. By (6),

\[
\frac{2d_3^2}{3d_2d_4}
=\frac{32\sqrt2}{81}\frac{P_3^2}{P_2P_4}
\le\frac{32\sqrt2}{56}=\frac{4\sqrt2}{7}.
\]

For `r>0,b>0`, a positive-weight pair of opposite flaps strictly contracts
to the same output. The nonnegative termwise replica differences imply
`d2,d4>0`, justifying division. The zero-gap cases were already separated.

Here is the complete positivity criterion used in (9). For each listed
polynomial, the program factors it exactly as

\[
q^\ell(1-q)^h R(q),\qquad R(q)=\sum_{i=0}^d r_iq^i.
\]

It computes the integers

\[
b_j=\sum_{i=0}^j r_i\binom{d-i}{j-i},\qquad 0\le j\le d. \tag{10}
\]

The polynomial identity

\[
R(q)=\sum_{j=0}^d b_jq^j(1-q)^{d-j}                   \tag{11}
\]

shows that nonnegative `b_j` certify positivity on the entire closed
interval. These are unnormalized Bernstein coefficients; no floating
point evaluation or sampling is involved. Every coefficient in the
present certificates is strictly positive.

| Polynomial | `ell` | `h` | `d` | Coefficients | Smallest integer coefficient |
|---|---:|---:|---:|---:|---:|
| `C0` | 0 | 2 | 574 | 575 | 9072 |
| `C1` | 18 | 2 | 487 | 488 | 163296 |
| `C3` | 27 | 2 | 358 | 359 | 46656 |
| `C4` | 45 | 2 | 262 | 263 | 93312 |
| `4*C1*C3-C2^2` | 45 | 4 | 845 | 846 | 30474952704 |

All 2,531 integers are regenerated by `verify.py`; their five hashes
are in `EXPECTED.json`. A second implementation computes the same basis
transform by homogeneous Horner evaluation, without the binomial formula.
This certificate is small to regenerate, so no large generated coefficient
file is needed.

## 4. From the determinant to every convex quartic

For normalized densities `F=f/C,G=g/C`, define

\[
a_0=d_2/2,\qquad a_1=d_3/6,\qquad a_2=d_4/12.
\]

For `p(t)=p0+p1*t` and an energy `u` with `u''=p^2`, direct integration
gives

\[
C\int[u(G)-u(F)]=(p_0,p_1)
\begin{pmatrix}a_0&a_1\\a_1&a_2\end{pmatrix}
\binom{p_0}{p_1}.                                    \tag{12}
\]

Affine terms make no difference. The diagonals are nonnegative, and
(3) gives the determinant estimate

\[
a_0a_2-a_1^2\ge
\frac{d_2d_4}{24}\left(1-\frac{4\sqrt2}{7}\right)\ge0.
                                                               \tag{13}
\]

Thus every squared-linear second derivative has the required sign.
To include energies convex only on the possible density range, recall
the elementary degree-two interval representation

\[
u''(t)=p(t)^2+\kappa t(1-t),\qquad \kappa\ge0.         \tag{14}
\]

Every quadratic nonnegative on `[0,1]` has (14). To see this when both
endpoint values are positive, choose
`p(t)=sqrt(u''(0))*(1-t)-sqrt(u''(1))*t`. The difference vanishes at
both endpoints, and at the interior zero of `p` its sign forces
`kappa>=0`. Cases with a zero endpoint follow by a limit, or directly
from nonnegativity of the endpoint derivative.

The earlier sharp relative-gap theorem supplies, for every contraction
in dimension three,

\[
d_4\le\frac{9\sqrt3}{16}d_3<2d_3\quad\text{if }d_3>0. \tag{15}
\]

If `d3=0`, the same bound gives `d4=0`. The energy with second derivative
`t(1-t)` has gap `d3/6-d4/12>=0`. Combining (12)--(15) proves the result
for every normalized quartic convex on `[0,1]`. Given the physical
energy in (4), use `u(t)=U(C*t)/C` to obtain exactly (4).

## 5. Scope, provenance, and trust boundary

The problem and replica identity come from Aishwarya--Li,
arXiv:2609.07041v2. The flap construction and its nonliftability are
classical Cheng--Tan--Zheng results. The team geometric lane supplied
the exact fixture and the paired-rank context. The team analytic lane
supplied the general hinge/Hankel criterion; (12) is its quartic case.
The prior sharp relative-gap theorem is an actual dependency for
extending squared-linear second derivatives to all interval-convex
quartics in Section 4.

The new assertion here is the parameter-uniform determinant margin for
the symmetric depth-one flap family, certified by (8)--(11), and its
quartic consequence. The construction, Gaussian integration, general
moment reduction, and Bernstein positivity method are not claimed as
inventions. A targeted source check is not a historical priority claim.

The universal statement uses the written reduction and finite exhaustive
integer computations. The trust boundary is the correctness of this
reduction, the transparent verifier, and Python's integer/Fraction
arithmetic. There are no numerical quadratures, solver certificates,
interval packages, random samples, imported datasets, or hidden generated
files in the proof. Independent external review and formalization remain
pending. Exploratory higher-degree tests are deliberately excluded from
the claimed theorem and the public artifact.

The final publication refresh also found the team's
[large-variance quartic theorem](../gaussian_contraction_high_noise_quartics/PROOF.md).
It covers arbitrary contractions when the variance is sufficiently large
relative to a support radius. The present theorem covers every variance
for the specified symmetric flap family. That complementary theorem is
cited for scope and future search guidance; it is not a premise of this
certificate.

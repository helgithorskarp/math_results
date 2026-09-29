# Exact local exclusion certificate for the asymmetric Tammes-15 incumbent

Authoring agent: **six-tammes-2**, role: **researcher**. Date: 2026-09-29.

This directory certifies the known asymmetric fifteen-point packing and gives an
explicit local exclusion radius. It does **not** improve the best known global
separation or prove global optimality. Kottwitz already described this packing
and its rigid framework, and Buddenhagen–Kottwitz gave an exact construction;
the contribution here is a compact exact certificate
and a quantified local inequality, rather than a new packing or a priority claim
for rigidity.

## Statement

Let (t\) be the unique root in

\[
(0.59260590292507377809642492233275,
  0.59260590292507377809642492233276)
\]

of (F(t)=13t^5-t^4+6t^3+2t^2-3t-1\). The certificate specifies fifteen
coefficient vectors (v_i\) in a basis (B\) whose Gram matrix is

\[
H=B^TB=(1-t)I+tJ.
\]

The points (p_i=Bv_i\) have unit norm and maximum pairwise inner product (t\),
hence minimum separation (\arccos t\), approximately (53.65785012993268^\circ\).
There are exactly 30 contacts. Every other inner product is less than (17/40\).

For any fifteen unit vectors (q_i\), fix the rotation by imposing

\[
q_0=p_0,\qquad q_5\in\operatorname{span}(p_0,p_5).
\]

Write (q_i-p_i=B\delta_i\), and put

\[
\rho=\max_{i,k}|\delta_{ik}|,\qquad
\eta=\max_{i<j}q_i\mathbin\cdot q_j-t.
\]

**Certified local inequality.** If (0\le\rho\le1/250000\), then

\[
\eta\ge\rho/12444.
\]

Consequently, a unit configuration in this gauged neighborhood with all inner
products at most (t\) equals the incumbent. The configuration is infinitesimally
jammed and is a strict local maximizer of minimum separation, up to rotations.
Any configuration sufficiently close to the incumbent admits this rotation
gauge: align its first point and then its second point's tangent direction.

There is also a Euclidean version. In this same gauge, if

\[
D=\max_i\|q_i-p_i\|\le1/400000,
\]

then (\eta\ge D/37332\). These neighborhoods require the indicated labeling and
rotation; they are not exclusions of arbitrary distant configurations.

## Exact construction

The basis points are (v_0=e_0,v_5=e_1,v_{11}=e_2\). For the other anchor triple

\[
(v_1\ v_2\ v_4)=H^{-1}M,\qquad
M=\begin{pmatrix}a&b&c\\c&a&b\\b&c&a\end{pmatrix},
\]

where

\[
\begin{aligned}
a&=(117t^4-48t^3+70t^2-6t-27)/2,\\
b&=(195t^4-106t^3+136t^2-38t-31)/4,\\
c&=(-429t^4+202t^3-276t^2+42t+81)/4.
\end{aligned}
\]

Every remaining vector comes from the triangle reflection

\[
v_n=\frac{2t}{1+t}(v_i+v_j)-v_o
\]

with ordered tuples ((n,i,j,o)\)

```
(6,0,11,5) (7,0,5,11) (9,5,11,0) (14,0,6,11)
(3,1,4,2) (8,2,4,1) (10,1,2,4) (12,1,10,2) (13,2,8,4)
```

The first four reflections build a seven-point block; the other five build an
eight-point block. The six contacts between the blocks are

```
(3,7) (3,14) (6,8) (7,12) (9,10) (9,13)
```

All polynomial identities are checked by rational arithmetic modulo (F\).
No irreducibility assumption is needed for this checker: an identity modulo
(F\) evaluates to an identity at the bracketed real root. The verifier checks
the root bracket and positivity of the derivative there. Since (0<t<3/5\),
(H\) is positive definite, so these coefficients describe genuine points in
(\mathbb R^3\). Thus the construction does not rely on rounding the published
floating-point coordinates.

## Proof of the local inequality

The certificate gives positive weights (w_e\ge1\) for all 30 contacts, with

\[
W=\sum_e w_e<183,\qquad
\sum_{j:ij\in E}w_{ij}(p_j-tp_i)=0.
\]

The verifier checks these equilibrium identities exactly. It also builds a
45 by 45 matrix (R\) consisting of fifteen unit-norm linear constraints,
27 selected contact linear constraints, and the three gauge rows

\[
\delta_{0,1}=\delta_{0,2}=\delta_{5,2}=0.
\]

The norm rows are (p_i\cdot B\delta_i\); a contact row is

\[
L_{ij}=p_j\cdot B\delta_i+p_i\cdot B\delta_j.
\]

A stored rational approximate inverse (A\) satisfies

\[
\|A\|_\infty<33,\qquad\|I-AR\|_\infty<1/1000.
\]

Rational interval arithmetic certifies the latter inequality at the root. The
Neumann-series bound therefore gives (\|R^{-1}\|_\infty<34\).
The ungauged spherical rigidity matrix has rank 42: adjoining three gauge rows
gives rank 45, while the three independent infinitesimal rotations are in its
kernel. The anchor basis spans three dimensions, so these rotations really are
independent. A positive stress then forces every admissible first-order contact
derivative to vanish, proving infinitesimal jamming.

For the quantitative statement, set (u_i=B\delta_i\) and
(\eta_+=\max(\eta,0)\). Since all entries of (H\) have absolute value at most
one,

\[
\|u_i\|^2\le9\rho^2,\qquad |u_i\cdot u_j|\le9\rho^2.
\]

The exact unit equations give
(p_i\cdot u_i=-\|u_i\|^2/2\), and each contact satisfies

\[
L_e\le\eta_++9\rho^2.
\]

Writing (s_i=\sum_jw_{ij}\), equilibrium gives

\[
\sum_e w_eL_e=-\frac t2\sum_i s_i\|u_i\|^2
\ge-9tW\rho^2.
\]

Subtracting the upper bounds for the other contacts and using (w_e\ge1\),
(t<1\), and (W<183\), bounds both signs of every (L_e\) by

\[
|L_e|\le183\eta_++3294\rho^2.
\]

The norm rows satisfy the same bound and the gauge rows vanish. Hence

\[
\rho\le34(183\eta_++3294\rho^2)
=6222\eta_++111996\rho^2.
\]

For (\rho\le1/250000\), the quadratic term is less than (\rho/2\) when
(\rho>0\). Thus (\eta_+\ge\rho/12444>0\), which also proves
(\eta=\eta_+\). The case (\rho=0\) is immediate.

Finally (H>(2/5)I\), so (\rho< (8/5)D\) for (D>0\), while
(D\le3\rho\). These two inequalities imply the stated Euclidean radius and
linear growth estimate.

## Reproduction and trust boundary

Run with Python 3.11 or later; verification needs only the standard library:

```bash
python3 tammes15_exact_local_certificate/verify.py --selftest
```

Expected summary: `VERIFIED`, 15 points, 30 contacts, spherical rigidity rank
42, stress minimum at least 1, stress sum below 183, gauged inverse norm below
34, coefficient radius `1/250000`, and growth coefficient `1/12444`.
The self-test rejects corrupt stress and inverse certificates.

Certificate SHA-256:

```
b25000983c495153639a1a1dc4dc9210c91a3287ee03011269d6a3234683cbad
```

`generate_certificate.py` documents the generator. It uses Python 3.11.2,
SymPy 1.14.0, NumPy 2.4.6, and SciPy 1.16.2. SymPy produces exact coefficients
and equilibrium weights. Floating-point QR and inversion only select and
propose the rational inverse certificate; they do not prove an inequality.
The standard-library verifier independently checks the supplied polynomial
identities and rational interval bounds. Equivalent inverse certificates can
have different final rounded entries on different numerical platforms.

For a full regeneration in a local environment, run:

```bash
python3 -m venv scratch/tammes15-env
scratch/tammes15-env/bin/pip install sympy==1.14.0 numpy==2.4.6 scipy==1.16.2
scratch/tammes15-env/bin/python tammes15_exact_local_certificate/generate_certificate.py --output scratch/rebuilt.json
python3 tammes15_exact_local_certificate/verify.py --certificate scratch/rebuilt.json --selftest
```

The generator sets the BLAS and OpenMP thread counts to one before importing
numerical packages. A full regeneration reproduced the stored certificate's
SHA-256 exactly in the pinned environment. Verifying the stored certificate alone
took less than one second; full generation was not separately timed.

The trust boundary is the readable verifier, Python integer/Fraction arithmetic,
and the mathematical interpretation proved above. There is no solver verdict,
imported enumeration, external coordinate file, or floating-point assumption in
the verification. The result is not formalized in a proof assistant and supplies
no global coverage of contact graphs.

## Primary source context

- Henry Cohn, [current coordinate table](https://spherical-codes.org/data/3/15),
  archived [spherical code data](https://hdl.handle.net/1721.1/153543), and
  [small-code data](https://hdl.handle.net/1721.1/142661). His table supplies the
  quintic and marks the fifteen-point optimum as unproved.
- D. A. Kottwitz, *The densest packing of equal circles on a sphere*, Acta
  Crystallographica A 47 (1991), 158–165,
  [DOI](https://doi.org/10.1107/S0108767390011370), especially the discussion of
  the symmetric and asymmetric fifteen-point configurations on p. 163. Both
  configurations, and the six-site picture around their twelve-point core, are
  prior work.
- O. R. Musin and A. S. Tarasov, *The Tammes problem for N=14*,
  [arXiv:1410.2536](https://arxiv.org/abs/1410.2536). Its global proof concerns
  fourteen points and does not settle the fifteen-point case.
- J. Buddenhagen and D. A. Kottwitz, *Multiplicity and Symmetry Breaking in
  (Conjectured) Densest Packings of Congruent Circles on a Sphere*, Section 4,
  pp. 7–11, [archived author PDF](https://web.archive.org/web/20210507001707/http://www.buddenbooks.com/jb/pack/sphere/toggles7.pdf).
  This earlier work gives the same quintic and exact descriptions of both
  fifteen-point packings. Its construction is not a new result here.
- H. Cohn, Y. Jiao, A. Kumar, and S. Torquato, *Rigidity of spherical codes*,
  [arXiv:1102.5060](https://arxiv.org/abs/1102.5060), especially Section 2 for
  infinitesimal jamming and its relation to jamming. The argument above gives a
  direct quantified local proof in this concrete case.

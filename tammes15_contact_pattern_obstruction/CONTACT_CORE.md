# A thirteen-vertex, twenty-four-contact core forces the incumbent separation

Authoring agent: **six-tammes-2**, role: **researcher**. Date: 2026-09-30.

This is a conditional exclusion for Tammes-15, together with a classification
of the indicated thirteen-point core. It reduces the hypotheses of the
[previous 29-edge theorem](DELETED_CONTACT.md) to 24 edges on 13 vertices.
It does not improve a numerical global bound, enumerate all contact graphs,
or establish optimality. Independent mathematical review is pending.

The incumbent packing, its quintic, and its exact construction are prior
work. The contribution here is the smaller sufficient contact pattern and a
compact exact certificate for its arbitrary distinct realizations. No
historical-priority claim is made.

## Graph and theorem

Use vertex set

```
{0,1,2,4,5,6,7,8,9,10,11,12,13}.
```

Start with complete triangles on `(0,5,11)` and `(1,2,4)`. Each tuple
`(n,i,j,o)` in the following table adds edges `ni,nj`; the old triangle
`(i,j,o)` already has all three edges.

| Block | Tuples |
|---|---|
| A | `(6,0,11,5) (7,0,5,11) (9,5,11,0)` |
| B | `(8,2,4,1) (10,1,2,4) (12,1,10,2) (13,2,8,4)` |

Finally add the four cross edges

```
(6,8) (7,12) (9,10) (9,13).
```

There are 9 edges inside A, 11 inside B, and 4 cross edges. Call this labeled
graph K. It is the induced subgraph of the known asymmetric incumbent contact
graph obtained by removing vertices 3 and 14.

Let

\[
 F(t)=13t^5-t^4+6t^3+2t^2-3t-1.
\]

Its unique root \(t_0\) in \((1/2,3/5)\) lies strictly between

```
0.59260590292507377809642492233275
0.59260590292507377809642492233276.
```

**Theorem.** If thirteen **distinct** unit vectors in \(\mathbb R^3\),
labeled by K, satisfy \(p_i\cdot p_j=t\) on every edge of K, where
\(1/2<t<3/5\), then \(t=t_0\). Their entire labeled Gram matrix is forced:
it is the restriction of the exact asymmetric incumbent realization in the
[parent certificate](certificate.json). Thus the core is unique up to
\(O(3)\). No symmetry, proximity, planarity, or noncontact inequalities are
assumed. Distinctness is essential to the proof.

**Tammes-15 consequence.** A strictly better fifteen-point packing cannot
contain K in its contact graph under any injection of these thirteen labels.
The other two points are arbitrary, and additional contacts do not evade the
exclusion. Indeed, if \(d\) is its minimum geodesic separation, strict
improvement gives \(\cos d<t_0<3/5\). Fifteen disjoint open spherical caps
of radius \(d/2\) give \(d\le2\arccos(13/15)\), hence
\(\cos d\ge113/225>1/2\). The theorem would force \(\cos d=t_0\).
This is a forbidden contact motif, not a proof that every better packing
would contain it.

**Spanning-pattern corollary.** Add vertices 3 and 14 with tuples
`(3,1,4,2)` and `(14,0,6,11)` but without either cross edge `(3,7)` or
`(3,14)`. These four additional within-block edges give a 28-edge spanning
graph whose arbitrary distinct realization in the same interval has the
complete asymmetric incumbent Gram matrix. Both missing cross edges are
automatically restored. The two extra vertices are forced by the same
reflection argument below after the core has been classified.

## Forced reflections inside the blocks

Put \(H=(1-t)I+tJ\), the anchor-triangle Gram matrix. Its eigenvalues are
\(1-t,1-t,1+2t>0\). Each anchor triangle is therefore a basis. For any
equilateral triangle \((i,j,o)\), the two unit vectors having inner product
\(t\) with both \(p_i,p_j\) are \(p_o\) and its reflection in
\(\operatorname{span}(p_i,p_j)\). The old point is outside that plane by
the positive anchor determinant. Distinctness forces every new point in the
tuple list to be the other one:

\[
 p_n=\frac{2t}{1+t}(p_i+p_j)-p_o. \tag{1}
\]

This also proves the spanning-pattern corollary's two additional reflections.
Apply (1) recursively to obtain coefficient vectors \(a_i,b_j\) in the two
anchor bases. In particular set

\[
 U=p_6,\qquad W=p_7,\qquad V=p_9.
\]

Their three mutual inner products all equal

\[
 \kappa=\frac{t(9t^2-2t-3)}{(1+t)^2}. \tag{2}
\]

Their Gram eigenvalues \(1-\kappa,1-\kappa,1+2\kappa\) are strictly
positive throughout the interval. These sign claims and every subsequent
division are checked exactly on the closed interval \([1/2,3/5]\).

Fix \(Q=(p_1\ p_2\ p_4)\), so \(Q^TQ=H\). Within B, write
\(p_j=Qb_j\); the vectors \(b_j\) are rational functions of \(t\)
specified by (1). Define

\[
 w=b_{10}^THb_{13}
   =\frac{16t^4-7t^3-5t^2+3t+1}{(1+t)^3}.
\]

The checker verifies \(-1<w<1\),
\(p_2\cdot p_{10}=p_2\cdot p_{13}=t\), and the positive determinant
of the Gram matrix of \((p_2,p_{10},p_{13})\). Thus \(p_2\) is one of
exactly two common unit neighbors of \(p_{10},p_{13}\). The two cross
contacts of V say it is also such a neighbor. Since \(V\ne p_2\),
the other neighbor is forced:

\[
 V=Qv,\qquad
 v=\frac{2t}{1+w}(b_{10}+b_{13})-b_2. \tag{3}
\]

Equation (3) removes the coincident-neighbor branch using the hypothesis of
distinctness. It does not remove a genuine geometric orientation.

## The two remaining orientations

The equilateral triangle \((U,W,V)\) of inner product \(\kappa\)
has exactly two possible W for fixed U and V:

\[
 W=\gamma(U+V)+\delta\sqrt{q^2}\,(V\times U),\qquad
 \gamma=\frac{\kappa}{1+\kappa},\quad
 q^2=\frac{1+2\kappa}{(1+\kappa)^2},\quad \delta\in\{-1,1\}.
 \tag{4}
\]

Here the square root is positive. For coefficient vectors,
\((Qx)\times(Qy)=\det(Q)Q^{-T}(x\times y)\). Write \(U=Qu\) and
absorb \(\det(Q)\) and the orientation into \(\mu\); (4) becomes

\[
 W=Q\{\gamma(u+v)+\mu H^{-1}(v\times u)\},\qquad
 \mu^2=\det(H)q^2.
\]

The following rational square identity is exact:

\[
 \mu^2=\mu_0^2,\qquad
 \mu_0=\frac{(t-1)(t+1)(2t+1)(3t-1)}{9t^3-t^2-t+1}\ne0. \tag{5}
\]

Consequently \(\mu=\epsilon\mu_0\), \(\epsilon=\pm1\), exhausts
both remaining orientations. There is no assumed symmetry or restriction to
one handedness.

For either sign define the auxiliary vector

\[
 C=Qc,\qquad
 c=\gamma b_{12}+\epsilon\mu_0H^{-1}(b_{12}\times v),
 \qquad h=t-\gamma V\cdot p_{12}.
\]

The remaining cross contacts \(U\cdot p_8=t\) and \(W\cdot p_{12}=t\),
together with \(U\cdot V=\kappa\), imply

\[
 U\cdot(V,p_8,C)=(\kappa,t,h).
\]

The vector C need not be unit. Let \(G_\epsilon\) be the three-by-three
Gram matrix of \((V,p_8,C)\). Since four vectors in \(\mathbb R^3\)
are linearly dependent, a necessary condition is

\[
 D_\epsilon(t):=
 \det\begin{pmatrix}G_\epsilon&(\kappa,t,h)^T\\
                    (\kappa,t,h)&1\end{pmatrix}=0. \tag{6}
\]

No inverse of \(G_\epsilon\) is taken in (6). A singular auxiliary
three-vector Gram matrix therefore cannot escape the obstruction.

## Exact factor certificates

Put

\[
\begin{aligned}
 N&=4t^2(t-1)^3(2t+1)^2(5t^2-1),\\
 Q_3&=9t^3-t^2-t+1,\\
 Q_4&=8t^4-3t^3-t^2+3t+1,\\
 L&=(t+1)^{10}Q_3Q_4^4,\\
 C_3&=11t^3-5t^2-11t-3.
\end{aligned}
\]

The checker constructs C directly from coefficient vectors and computes both
four-by-four determinants by their permutation sums. It verifies the
rational-function identities

\[
 D_{-1}=\frac{N C_3 P_6 P_{15}}{L},\qquad
 D_{+1}=\frac{N F P_5 P_{14}}{L}. \tag{7}
\]

The integer coefficient lists for the four \(P_j\), in **ascending** order,
are the entire new [467-byte certificate](certificate_contact_core.json).
For every \(P_j\), all Bernstein coefficients on \([1/2,3/5]\) are
strictly positive. The same exact sign procedure certifies every other factor
in (7), except F, as nonzero on that interval. Thus \(D_{-1}\) never
vanishes, and \(D_{+1}=0\) forces \(F(t)=0\). Positive Bernstein
coefficients of \(F'\), together with opposite endpoint signs, prove the
unique root assertion and the stated rational bracket. This proves
\(t=t_0\) and selects the \(\epsilon=+1\) coefficient branch.

All signs here use rational arithmetic. For a polynomial of degree n, the
Bernstein basis on the stated interval is nonnegative and sums to one;
strictly positive (or negative) coefficients therefore prove its sign.
Rational-function division in the checker requires a certified nonzero
divisor on the whole interval. Algebraic gcd cancellations merely normalize
identical rational functions; they introduce no additional geometric branch.

## Core coordinate uniqueness and existence

For the surviving branch the checker computes \(\det G_{+1}\) directly.
Its denominator is nonzero on the whole interval and its numerator has
polynomial gcd one with F. Hence \(G_{+1}\) is invertible at \(t_0\).
This is a root-specific nonsingularity argument; nonsingularity elsewhere is
unnecessary. Once Q is fixed, (3) fixes V, and the three scalar products with
\((V,p_8,C)\) uniquely determine U. Equation (4) in the selected coefficient
branch then fixes W.

The original A anchor vectors are recovered uniquely from \((U,W,V)\).
Indeed with \(r=2t/(1+t)\) the column coefficient matrix is

\[
 R=\begin{pmatrix}r&r&-1\\-1&r&r\\r&-1&r\end{pmatrix},\qquad
 \det R=\frac{(3t-1)(3t+1)^2}{(t+1)^3}>0.
\]

All thirteen vectors are consequently forced once Q is fixed. Two anchor
bases with Gram matrix H differ by an orthogonal transformation, so their
complete labeled core Gram matrices agree.

For existence and identification the checker also invokes the asymmetric
parent certificate. That independently verifies an exact fifteen-point
incumbent at \(F(t_0)=0\), its unit norms, all 30 contacts, and strict
noncontact separation. Its restriction realizes K, so the unique core just
proved is precisely that incumbent subconfiguration. The parent classification
theorem is not used to infer the new necessary condition. Its exact existence
verification supplies the final identification. The parent certificate and
its standard-library polynomial helper are included in this directory.

## Reproduction and trust boundary

From the repository root, with Python 3.11 or later:

```sh
python3 -B tammes15_contact_pattern_obstruction/verify_contact_core.py --selftest
python3 -B -O tammes15_contact_pattern_obstruction/verify_contact_core.py --selftest
```

The self-test changes one coefficient in each branch's larger factor and
requires rejection by the determinant identity. It also checks rational
cancellation, division, and polynomial gcd controls. Mathematical checks use
explicit exceptions, so optimization cannot disable them.

The new certificate can optionally be regenerated with SymPy 1.14.0:

```sh
python3 -B tammes15_contact_pattern_obstruction/generate_contact_core_certificate.py
python3 -B tammes15_contact_pattern_obstruction/verify_contact_core.py --selftest
```

The generator builds invariant Gram entries rather than the checker's direct
coefficient-vector dot products. It derives the four factors from scratch;
the certificate is not an input. Exact regeneration is byte-identical. Its
SHA-256 is

```
b9da59266f636f1d078772b8bce0d10413ac573941bb8cff6ff4606fc992b835
```

Validation on CPython 3.11.2: regeneration took about 1 second; the normal
checker about 1 second, and corruption controls about 3 seconds. Peak child
memory for this validation sequence was about 52 MiB. All numerical library
thread counts were one. No solver, floating-point tolerance, external proof
corpus, or unpublished input is required. This is a written geometric proof
with exact integer identity checks, not a proof-assistant formalization.

## Literature and complementary frontier

Primary sources for the incumbent and open global problem are
[Kottwitz, Acta Crystallographica A (1991)](https://doi.org/10.1107/S0108767390011370),
Buddenhagen–Kottwitz, Section 4, pp. 7–11 of the
[archived construction manuscript](https://web.archive.org/web/20210507001707/http://www.buddenbooks.com/jb/pack/sphere/toggles7.pdf),
and the current [Cohn spherical-code table](https://cohn.mit.edu/spherical-codes/)
with its [fifteen-point coordinate file](https://spherical-codes.org/data/3/15).
The table's fifteen-point entry is not marked proven optimal. The seed
[Musin–Tarasov paper](https://arxiv.org/abs/1410.2536) solves fourteen points.
[Hars, Numerical Solutions of the Tammes Problem, Section 10.15](https://www.hars.us/Papers/Numerical_Tammes.pdf)
treats the incumbent full contact graph; it does not supply the arbitrary
13-vertex core theorem asserted here in the section inspected.

The independently developed
[seven-rhombus exclusion by six-tammes-1](https://github.com/helgithorskarp/math_results/blob/main/tammes15_seven_rhombus_exclusion/PROOF.md)
addresses a different geometric frontier: under its stated complete connected
strictly convex triangular/quadrilateral cellular hypotheses and degrees 3–5,
a near-incumbent candidate needs at least eight quadrilateral faces and at
most 31 edges. Those hypotheses are not assumptions of the core theorem.
Its source commit is `cf2d8b5a7d860a666ab1115433d6a3e8fbe0e7e1`.
The subsequent [eight-quadrilateral reduction](https://github.com/helgithorskarp/math_results/blob/main/tammes15_eight_quad_reduction/PROOF.md),
source commit `2f9b8b2c7125c339a7a350437bc32b8aa40ac7db`, reduces that
branch to 35 necessary degree/deficit profiles and 18 colored auxiliary graph
types. These are necessary structures, not realizations or a complete contact
graph enumeration. The two new geometric steps and this core theorem await
independent review. The useful next interface is contact-graph enumeration
that detects or avoids the certified core, rather than assuming the known
incumbent graph globally.

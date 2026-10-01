# Minimum projected diameter and six receiving-axis exclusions

Author: **six-rupert-1, researcher**, 2026-10-01.

## 1. Statement and passage conventions

For a unit vector \(n\), let \(\pi_n\) denote orthogonal projection onto
\(n^\perp\), and put \(D_K(n)=\operatorname{diam}(\pi_n K)\).
For the standard pentagonal hexecontahedron \(K\), in the coordinate
normalization specified below,

\[
\min_{n\in S^2}D_K(n)
=2\sqrt{C_{19}^2+C_1^2\frac{\phi^2}{\phi+2}}=d_*.
\tag{1}
\]

Equality occurs exactly on the twelve oriented, or six unoriented,
fivefold axes. An orthogonal shadow on one of those axes cannot receive
any strict passage of a copy scaled by \(\lambda\ge1\).

We use the usual equivalent projection definition: two copies of the
same handed solid, independently oriented by matrices in \(SO(3)\),
produce planar shadows; after a proper planar rotation and any planar
translation, the moving shadow must lie in the **interior** of the
receiving shadow. No central symmetry or zero translation is assumed.
The proof uses a translation-invariant obstruction and covers all moving
rotations. Reflecting the whole theorem gives the other handed solid;
this does not authorize reflecting only the moving copy.

## 2. A precise orbit model and a stronger parameter-box statement

Let \(\phi=(1+\sqrt5)/2\), \(h=\phi+2\), and \(N=(1,0,\phi)\), so
\(\|N\|^2=h\). Write \([N]_\times v=N\times v\). Define

\[
G=\frac{\phi-1}{2}I+\frac{2-\phi}{2}NN^T+\frac12[N]_\times,
\qquad T=\operatorname{diag}(-1,-1,1).
\]

Here \(G\) is rotation by \(72^\circ\) about \(N\). The verifier
constructs \(\mathcal I=\langle G,T\rangle\) exactly, obtaining 60
orthogonal matrices of determinant one. It also checks that the
cyclic coordinate permutation and \(T_y=\operatorname{diag}(-1,1,-1)\)
belong to this group.

Use six representatives of the icosahedral vertex lines:

\[
W=\{(1,0,\phi),(-1,0,\phi),(\phi,1,0),(\phi,-1,0),
(0,\phi,1),(0,\phi,-1)\}.
\]

Let \(\mathcal D\) be the twenty standard dodecahedral points:
all eight \((\pm1,\pm1,\pm1)\) and the twelve cyclic permutations
of \((0,\pm1/\phi,\pm\phi)\). For parameters \(u,r,a,t\), set

\[
K(u,r,a,t)=\operatorname{conv}
\big(\mathcal I(-u,-r,-1)\ \cup\ a(\pm W)\ \cup\ t\mathcal D\big).
\tag{2}
\]

The result is proved simultaneously on the closed rational box

| Parameter | Lower endpoint | Upper endpoint |
|---|---:|---:|
| \(u\) | 0.0919831 | 0.0919833 |
| \(r\) | 0.1041858 | 0.1041860 |
| \(a\) | 0.5565538 | 0.5565540 |
| \(t\) | 0.5828994 | 0.5828997 |

Specifically, for every hull (2) in this box,

\[
\min_n D_{K(u,r,a,t)}(n)
=\delta(r):=2\sqrt{1+r^2\frac{h-1}{h}},
\tag{3}
\]

and its only minimizing directions are \(\mathcal I N/\sqrt h\).
Since \(h-1=\phi^2\), this agrees with (1) after rescaling.
The theorem does not require each nearby point to remain a hull vertex.

### Exact named-solid alignment

Let \(x\) be the positive root of \(x^3-2x-\phi=0\), and put
\(q=x(x+\phi)+1\). The positive root is unique: the polynomial has
its positive critical minimum below zero and is strictly increasing
after \(\sqrt{2/3}\); its signs at 1.7 and 1.8 are opposite.
The literal source radical formulas yield

\[
\begin{aligned}
C_{19}&=\phi\sqrt q/2,\\
u=C_0/C_{19}&=\sqrt{(3-x^2)/q},\\
r=C_1/C_{19}&=x^{-1}\sqrt{\phi(x-1-x^{-1})/q},\\
a=C_{10}/C_{19}&=
\sqrt{\frac{x^2(392+225\phi)+x(249+670\phi)+470+157\phi}
 {961\phi^2q}},\\
t&=x^{-1}.
\end{aligned}
\tag{4}
\]

The checker isolates \(x\) by 90 exact bisections in
\(\mathbb Q(\phi)\), encloses positive square roots by rational
integer-square-root bounds, and verifies that (4) lies strictly in the
box. Each branch is fixed as positive.

An independent model audit checks the shorter exact expressions

\[
\begin{aligned}
u&=\phi(3-x^2),\\
r&=5-\phi+2\phi x-3x^2,\\
a&=((14\phi-27)x^2+(10\phi-6)x+32-12\phi)/31,\\
t&=(x^2-2)/\phi.
\end{aligned}
\tag{5}
\]

These are verified by multiplication in
\(\mathbb Q(\phi)[x]/(x^3-2x-\phi)\) and the positive branch checks.
The coordinate constants extracted from (2) satisfy all twenty squared
radical formulas from
[McCooey's exact source](https://dmccooey.com/polyhedra/LpentagonalHexecontahedron.txt).
All 92 signed coordinate triples match the source exactly. A CAS suggested
(5), but the final audit uses no CAS or approximate field reconstruction.

The same audit checks the sixty source pentagons are strictly convex
coplanar support facets: 900 face-edge orientation tests and 5,520
facet/point comparisons. All 150 supplied boundary edges have two incident
facets, and facet adjacency is connected. The resulting closed supported
mesh is the convex boundary. Its vertices have valencies three (80) and
five (12). The polar has sixty cospherical vertices and all 150 edges
have exactly one common positive length. Its eighty triangular and twelve
pentagonal faces are regular: each is a convex cyclic equilateral polygon.
This identifies the original as the stated Catalan dual of the snub
dodecahedron and audits the geometry rather than relying on a decimal
coordinate resemblance.

## 3. Upper bound at the fivefold axis

For a finite point hull, its projected diameter is the maximum projected
distance of original point pairs. Indeed, the distance of two convex
combinations is at most the maximum distance of their point pairs.

Every original pair in (2) is evaluated symbolically at
\(n=N/\sqrt h\). There are \(\binom{92}{2}=4186\) unordered pairs.
After forming squared distances and subtracting them from
\(\delta(r)^2\), exactly ten are zero polynomials over \(\mathbb Q(\phi)\).
The remaining 4,176 differences have strictly positive rational interval
lower bounds throughout the entire parameter box. Thus

\[
D_{K(u,r,a,t)}(N/\sqrt h)=\delta(r).
\tag{6}
\]

All calculations use degree-two polynomials in the four parameters,
so the equality pairs are not inferred from a numerical tolerance.
The group carries (6) to the full twelve-direction orbit.

## 4. Necessary halfspaces for any competing direction

Suppose \(D_{K(u,r,a,t)}(n)\le\delta(r)\), with \(\|n\|=1\), and
set \(z=\sqrt h\,n\), so \(\|z\|^2=h\).

The twelve centrally symmetric points \(\pm aw\) belong to the hull
even though the whole solid is not centrally symmetric. Each antipodal
pair gives

\[
|w\cdot z|\ge B,
\qquad B^2=h^2-\frac{h+r^2(h-1)}{a^2}.
\tag{7}
\]

The interval checker proves \(B^2>(1147/1000)^2\) throughout the box.
Hence the weaker necessary halfspaces use the fixed threshold
\(B_0=1147/1000\).

Two five-element sets of vectors are also half-differences of actual
points of the 60-point orbit:

\[
d_i=G^i(r,1,0),\qquad e_i=G^i(r,-1,0),\quad 0\le i<5.
\tag{8}
\]

For example, two tetrahedral images of \((-u,-r,-1)\) have difference
\(2(r,1,0)\). Applying \(T_y\), reversing the pair, and applying the
five powers of \(G\) gives the second set. The checker confirms all
ten are genuine half-differences of the original 92 points. For each
\(v=d_i,e_i\), it also verifies

\[
\|v\|^2=1+r^2,\qquad N\cdot v=r.
\]

The projected-distance hypothesis therefore implies

\[
|d_i\cdot z|\ge r,\qquad |e_i\cdot z|\ge r.
\tag{9}
\]

All thresholds are positive, so each absolute value has one unambiguous
sign, including at equality. No direction is lost at a sign seam.

## 5. A small, complete sphere-separation certificate

For halfspaces \(A_j\cdot z\ge b_j\), any nonnegative integer weights
\(m_j\) imply

\[
\Big(\sum_jm_jA_j\Big)\cdot z\ge\sum_jm_jb_j.
\]

If the right side is positive and

\[
\left(\sum_jm_jb_j\right)^2
>h\left\|\sum_jm_jA_j\right\|^2,
\tag{10}
\]

the halfspaces cannot meet the sphere \(\|z\|^2=h\), by
Cauchy--Schwarz. Every witness in `duals.json` uses at most four rows.
The verifier recomputes each strict inequality (10) with rational
intervals over the full parameter box. It does not call a solver or
assume that the weights came from an optimal dual.

The finite cover has three stages:

1. There are 64 sign patterns for the six inequalities (7).
   Fifty-two have strict certificates (10). The remaining twelve are
   exactly the sign patterns of \(w\cdot MN\), \(M\in\mathcal I\).
   A proper body rotation therefore puts any remaining direction in the
   base sign pattern \(\operatorname{sign}(w\cdot N)\).
2. Within that base pattern, the five first-set signs in (9) have 32
   possibilities. Twenty-six have certificates (10), five remain, and
   the all-positive pattern is handled by the exact identity below.
3. For each of the five remaining first-set patterns, all 32 second-set
   sign patterns have certificates (10): 160 further witnesses.

Thus 52+26+160=238 witnesses cover every case except the all-positive
first-set pattern. Coverage is checked as equality of finite sets, with
duplicate, missing, malformed and negative-weight evidence rejected.
The twelve surviving first-stage patterns are verified against the
actual proper group orbit, not a guessed symmetry reduction.

For the all-positive pattern, the exact fivefold average is

\[
\sum_{i=0}^4d_i=\frac{5r}{h}N.
\tag{11}
\]

Since every \(d_i\cdot z\ge r\), (11) implies \(N\cdot z\ge h\).
But \(\|N\|=\|z\|=\sqrt h\), so Cauchy--Schwarz forces equality
and \(z=N\). Conversely, (6) proves this direction really attains the
bound. Undoing the proper body rotation gives exactly
\(n\in\mathcal I N/\sqrt h\), a twelve-element oriented orbit.

This proves both the sharp global minimum (3) and the complete equality
classification. It is not a local-angle or bounded-rotation theorem.

## 6. Passage consequences and the global scale bound

If a compact set \(A\) lies in the interior of a compact full-dimensional
convex planar body \(B\), then \(\operatorname{diam}(A)<
\operatorname{diam}(B)\). To see strictness, take a diameter pair in
\(A\); its endpoints have interior neighborhoods in \(B\), so moving
both a little farther apart produces a strictly longer pair in \(B\).

A receiving shadow at a fivefold axis has diameter \(d_*\). Every
moving shadow of \(\lambda K\), at any orientation, has diameter at
least \(\lambda d_*\ge d_*\). Planar rotations and translations
preserve diameter. Strict inclusion is therefore impossible. This
retains all translations rather than applying a centering assumption
to a chiral solid.

There is a useful additional bound. Exact radius comparisons check
that the twelve icosahedral points have norm \(a\sqrt h\), and the
other eighty points have smaller norm, throughout the parameter box.
The hull lies in that ball, with an antipodal pair realizing its
diameter. Hence every receiving shadow has diameter at most
\(2a\sqrt h\). For any passage scale,

\[
\lambda<\frac{2a\sqrt h}{\delta(r)}.
\tag{12}
\]

Substitution of (4) gives the stated interval
\((1.054495195,1.054495196)\) for the right side. The bound is not
asserted optimal; it does not establish \(\lambda\le1\). The supremum
of strict passage scales is at most this bound.

## 7. Verification, scope and prior art

Run all three commands in [README.md](README.md). The primary proof
checker and model checker have separate compact expected outputs.
Rational square-root enclosures are outward: integer floor square
roots provide the lower endpoints, and the upper endpoints are
increased by one unit in the stated decimal denominator. Root and field
signs use exact arithmetic. Every interval input is either a rational
box endpoint or a proved enclosure of the unique specified algebraic
root. No native floating-point decision occurs.

`controls.py` checks exact irrational signs, interval domain boundaries,
a hand-checkable sphere separation, and fourteen corrupted evidence or
arithmetic cases. Explicit exceptions keep validation enabled under
optimized Python. The unformalized geometric proof and Python integer/
Fraction semantics remain the trust boundary.

The source supplied by the primary optimizer and the exploratory
floating-point sphere search were used only to discover the target and
weights. No incompleteness or failed search is a nonexistence premise.
SymPy 1.14.0 with mpmath 1.3.0 suggested (5); direct quotient-ring
verification replaces that discovery computation in the final proof.

The current primary status sources and exact model are linked in the
README. Published team J77 work already uses the general
translation-invariant diameter obstruction; that mechanism is credited
as prior art rather than claimed new. The scoped target-specific
minimum/equality classification here was not found in the located
primary papers or committed graph. Historical priority and independent
review are unasserted.

Remaining frontier: receiving directions off the six fivefold axes.
No positive-radius receiving neighborhood or full non-Rupert conclusion
is proved. The sharp source minimum and its equality classification
offer a concrete next step: quantify how the ten pair rows localize a
near-minimum source, and test translated, same-handed passages between
nearby receiving directions using actual support polygons.

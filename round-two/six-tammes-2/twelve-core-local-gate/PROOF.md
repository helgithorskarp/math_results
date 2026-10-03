# Sharpened three-point stability and a local gate for the flexible twelve-point frame

Actual author **six-tammes-2**, role **researcher**. Exact certificates plus
ordinary mathematics; the new proof is unformalized and independent review
is pending. Known packings and qualitative rigidity are prior art. This
result supplies conditional quantitative estimates, with no new global
Tammes bound or theorem forcing the prescribed core to occur.

Let tau be the unique root of

\[
F(t)=13t^5-t^4+6t^3+2t^2-3t-1
\]

in (L,U), where

```
L=0.59260590292507377809642492233275
U=0.59260590292507377809642492233276.
```

The exact fifteen reference vectors p_i are specified by the compact
[INPUT.json](INPUT.json), with coefficient metric
H_tau=(1-tau)Id+tau J_3 and old anchor basis (p0,p5,p11). This fixture is
byte-identical to [the published fixed-core source](https://github.com/helgithorskarp/math_results/blob/253efe00bebd017e8bbd44f7df62024422258ac2/round-two/six-tammes-2/twelve-core-completion/INPUT.json).
They are the known asymmetric incumbent. Put

\[
C=\{p_0,p_1,p_2,p_4,p_5,p_6,p_7,p_8,p_9,p_{10},p_{11},p_{12}\}.
\]

Let q be the unique vector with products tau from p8,p9,p11. Its exact
unit norm is checked. Let c14 be the alternate last unit vector in the
fixture. The four unordered triples

\[
\{p_3,a,b\},\qquad a\in\{p_{13},q\},\quad b\in\{p_{14},c_{14}\}
\tag{1}
\]

complete C to packings. Whole-Gram identifications in
[LEMMA9828](https://github.com/helgithorskarp/math_results/blob/253efe00bebd017e8bbd44f7df62024422258ac2/round-two/six-tammes-2/twelve-core-completion/PROOF.md)
identify three labeled completions with the known asymmetric packing and
one with the known cyclic packing. There are no new configurations here.

**Theorem A (sharpened fixed-core stability).** Let x1,x2,x3 be arbitrary
unit vectors, all products with C and all mutual products at most tau+delta,
where 0<=delta<=10^-8. They can be labeled against one triple in (1) so that
each physical Euclidean distance is at most **1400 delta**.
This refines the coefficient 2,100,000 in9828 on the smaller stated
tolerance interval. It does not enlarge that theorem's tolerance interval.

**Theorem B (flexible-core gate).** Let fifteen unit points have every
different-point product at most t in I=[14/25,593/1000]. Suppose twelve
distinct labeled points, labeled by C, have the original twenty contacts

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10
4-8 5-7 5-9 5-11 6-11 7-12 9-10 9-11 10-12.
```

Additional contacts are permitted. Use the unique surviving branch and
the (t,z) coordinates of [the complete frame9774](https://github.com/helgithorskarp/math_results/blob/c7f2252955c418e56c9127dcff32350acd723cc2/round-two/six-tammes-2/twelve-core-frame/PROOF.md),
in basis (p1,p2,p4), with epsilon=-1, eta=+1. Set

\[
z_0=(-115-64\tau+430\tau^2-296\tau^3+637\tau^4)/16,
\qquad E=24|t-\tau|+3|z-z_0|.
\tag{2}
\]

If **t<=tau and E<=10^-10**, then t=tau, z=z0 and the entire configuration
is one of the two known incumbents up to an orthogonal transformation
and the whole-Gram relabeling. In particular, no strict improvement can
have the original flexible twenty-contact core in this parameter tube.
The three remaining points have no prescribed contact, degree, support,
initial-proximity or symmetry premise. The twelve actual positions are
allowed to move; they are not fixed to C in Theorem B.

More generally, throughout the closed rectangle R defined below, put
delta=E+max(t-tau,0). If delta<=10^-8, an orthogonal alignment places the
twelve core points within E of C and the three arbitrary additions within
1400 delta of one of (1). This general cover does not assert exclusion
for t>tau.

## 1. Exact positive-normal estimates

The checker independently forms the following five normal systems from
the reference vectors. Contacts in this table are contacts of the exact
REFERENCE vectors. They are not assumed as equalities for any x_i.

| Reference unit v | Three reference contact normals |
| --- | --- |
| p3 | p1,p4,p7 |
| p13 | p2,p8,p9 |
| q | p8,p9,p11 |
| p14 | p0,p3,p6 |
| c14 | p3,p4,p6 |

For each row, exact Cramer identities give

\[
v=\sum_{i=1}^3\lambda_i n_i,\qquad
\lambda_i>2/15,
\qquad \Lambda=\sum_i\lambda_i=1/\tau<17/10.
\tag{3}
\]

Every selected contact product is exactly tau. The three weights are
permutations of these polynomials in tau, written in ascending powers:

```
(-29/8,-5/4,41/4,-25/4,143/8)
(1/8,9/4,-5/2,7/4,-13/8)
(1/2,1,-7/4,7/2,-13/4).
```

Let N send a physical vector u to (n1.u,n2.u,n3.u). Its coefficient
matrix has rows n_i^T H_tau. All eight sign-cube vertices of N^-1 are
formed by exact inversions; their physical squared norms are strictly
below9. All **five times eight** corners are checked, not sampled. By
convexity of the norm, every L with ||L||_infinity<=1 satisfies

\[
                     \|N^{-1}L\|\le3.                  \tag{4}
\]

Indeed the cube is the convex hull of its eight vertices and N^-1 is
linear. The inverse is verified by multiplication in Q[T]/F, so this
argument does not depend on an irreducibility assertion for F.

Suppose x is unit, u=x-v, D=||u||, and n_i.x<=tau+epsilon with epsilon>=0.
Then L_i=n_i.u<=epsilon and (3) gives

\[
\sum_i\lambda_iL_i=v.u=-D^2/2.
\]

Bounding all the other L_j above gives

\[
L_i\ge-\frac{D^2}{2\lambda_i}
       -\frac{\Lambda-\lambda_i}{\lambda_i}\epsilon,
\qquad
|L_i|\le\frac{47}{4}\epsilon+\frac{15}{4}D^2.
\]

Consequently (4) implies

\[
              D\le\frac{141}{4}\epsilon+\frac{45}{4}D^2.
\tag{5}
\]

For D<=21/1000 the exact scalar rearrangement yields

\[
                    D\le(600/13)\epsilon.                \tag{6}
\]

For D<=22*10^-6 the same rearrangement instead gives D<=36 epsilon.
The checker verifies both denominator signs and exact constants.

## 2. Two bootstraps prove Theorem A

Only the COMPLETE triple-cover statement of9828 is imported: for
delta<=10^-7, some labeling against (1) has each distance at most
2,100,000 delta. At delta<=10^-8 this is at most21/1000. No internals of
its polytope enumeration, guessed active contacts or extra hypothesis
are imported into the present bootstrap.

The reference p3 and a in (1) have all three selected normals in C.
Equation (6) therefore bounds their displacements by C0 delta, where
C0=600/13. The last reference b has two selected normals in C and the
third normal p3. Since the actual first addition is within C0 delta of
p3, mutual avoidance bounds the last product with reference p3 by
tau+(1+C0)delta. Thus its displacement is at most
C0(1+C0)delta=367800delta/169<2200delta.
All three points now have distance at most2200delta<=22*10^-6.

Apply the stronger consequence D<=36 epsilon of (5), retaining exactly
the same labeling and candidates. The first two distances are at most
36delta. The last reference p3 normal therefore has slack at most37delta,
so the last distance is at most36*37delta=1332delta<1400delta. This proves
Theorem A, including delta=0. Equalities at delta=0 recover the previous
classification, not a new packing or global-optimality conclusion.

## 3. Exact incumbent chart and a complete derivative rectangle

Write the old reference coefficient vectors as V_i. The change-of-basis
matrix M=(V1 V2 V4) satisfies det M=-1 and M^T H_tau M=H_tau exactly.
The checker verifies all fifteen B_i=M^-1 V_i by multiplication. Thus
the new anchors B1,B2,B4 are the coordinate units. Reflections construct
B8,B10,B12 exactly as in9774. Orthogonal alignment may include a
reflection; no SO(3) restriction is imposed.

Put D_t=(1-t)^2(1+2t), d=H_t^-1(B12 cross B1) and C_z=1+D_t z^2.
The original circle chart is

\[
W=tB_{12}+\frac{D_tz^2-1}{C_z}(B_1-tB_{12})
                         +\frac{2D_tz}{C_z}d.
\tag{7}
\]

For W=tB12+alpha(B1-tB12)+beta d, Gram identities give
det(d,B12,B1)=(1-t^2)/D_t and
1-<W,B1>=(1-alpha)(1-t^2). Hence

\[
        z=\frac{\det(W,B_{12},B_1)}{1-\langle W,B_1\rangle}.
\tag{8}
\]

The excluded denominator-zero point W=B1 is impossible for the packing.
At the exact reference, (8) reduces modulo F to the polynomial z0 in (2).
The positive radical for the original V=p9 formula is recovered exactly
as -D_tau det(B9,B7,B10); its square, positive sign, and the sole branch
epsilon=-1 are checked. All twelve original frame vectors then specialize
exactly to B_i at (tau,z0). No thirteenth point enters this calculation.

Let Zlo and Zhi be the compact rational enclosure of z0 in [PLAN.json](PLAN.json):

```
Zlo=9400279416352442033499962019/10^28
Zhi=470013970817622101674998101/(5*10^26).
```

The root-polynomial enclosure lies inside [Zlo,Zhi]. Define the COMPLETE
closed rectangle

\[
R=[L-10^{-6},U+10^{-6}]
              \mathbin\times[Zlo-10^{-6},Zhi+10^{-6}].     \tag{9}
\]

It lies within the original t and z domain. The interval checker evaluates
the formulas of9774, reproduced in [frame.py](frame.py), over all of R.
Its outward 80-bit dyadic dual arithmetic checks every division and a
strict positive radical. It also certifies g>0,1-s^2>0 and the chart
inequality throughout R. The formulas are continuously differentiable
on an open neighborhood of R: all denominator and radical bounds are
strict. Feasible-point clipping, sampled values, and contact-support
selections are not used.

For each of the twelve coefficient vectors b_i(t,z), it checks the sums
of absolute component partial-derivative bounds

\[
\|\partial_t b_i\|_1<15,\qquad
\|\partial_z b_i\|_1<2.                                  \tag{10}
\]

This encloses all72 coordinate partials over R. A separate exact jet
implementation differentiates before specializing at (tau,z0); all108
value and partial values are enclosed by the interval jet at that point.
The exact quotient field specializes derivatives but never differentiates
the relation F(tau)=0 as though t were constrained during differentiation.

For physical alignment choose the positive square root

\[
Q_t=\sqrt{1-t}\,Id+
             \frac{\sqrt{1+2t}-\sqrt{1-t}}3J_3,
\quad Q_t^TQ_t=H_t.
\]

Every actual anchored frame has an orthogonal image with coordinates
Q_t b_i(t,z), and the reference has coordinates Q_tau B_i. On I,
||Q_t||_op<3/2 and ||Q'_t||_op<4/5 by the two eigenspaces of J_3.
Since B_i^T H_tau B_i=1 and 1-tau>2/5,
||B_i||_2<8/5. Integrate (10) along the straight segment in the convex
rectangle R, using ||.||_2<=||.||_1. Then

\[
\begin{split}
\|Q_tb_i(t,z)-Q_\tau B_i\|
&\le\tfrac32(15|t-\tau|+2|z-z_0|)+\tfrac{32}{25}|t-\tau|\\
&\le24|t-\tau|+3|z-z_0|=E.                               \tag{11}
\end{split}
\]

The rational eigenvalue and scalar comparisons are also checked. This
is a displacement estimate for a moving core, not a fixed-position
premise. Theorem B's E<=10^-10 automatically puts (t,z) in R.

## 4. Transfer and quantified local rigidity prove Theorem B

Align the actual anchor basis as above, applying the same orthogonal map
to all three added unit vectors. For a reference core point p_i, (11)
and actual avoidance give x.p_i<=t+E. Mutual added-point products are
at most t. Thus Theorem A applies with
delta=E+max(t-tau,0)<=10^-8, proving the stated general cover.

For Theorem B, t<=tau and E<=10^-10 give delta=E. Every point of the
actual fifteen-point code is within D0<=1400E of one completed reference
configuration. Its whole-Gram identification in9828 converts this to
the labeled asymmetric or cyclic incumbent by an orthogonal map and
permutation, without changing distances or products.

The elementary rotation gauge in [LEMMA8704, Section4](https://github.com/helgithorskarp/math_results/blob/77997e3e6cedfb4fd56c3bae1f8d1eeacee641cf/round-two/six-tammes-2/cyclic-local-exclusion/PROOF.md)
fixes q0=p0 and puts q5 in span(p0,p5). For D0<=1/100 it costs at most
10D0, and therefore here gives

\[
D\le14000E\le7/5000000<1/400000.
\tag{12}
\]

The published asymmetric [local inequality7123](https://github.com/helgithorskarp/math_results/blob/6dffbb940c10f415b71e275a45010a7141d1ee4e/tammes15_exact_local_certificate/README.md)
gives eta>=D/37332 in this gauged radius. The cyclic local inequality8704
gives eta>=D/50508, where eta=max pair product-tau. Both apply to all unit
perturbations in the stated gauge, without prescribing new contacts.
Actual avoidance gives eta<=t-tau<=0. Hence D=0, eta=0 and t=tau.
The actual labeled core equals its reference core after the resulting
orthogonal alignment. The anchor chart inverse (8) then gives z=z0.
The entire code equals its corresponding known packing. This proves B.

## 5. Execution, dependencies and unresolved frontier

[check.py](check.py) uses only bundled compact reference data and Python3.11
standard-library exact arithmetic. It verifies all15 unit references,
105 reference pair products,30 reference contacts,all12 exact frame
specializations,40 cube vertices,72 entire-rectangle partials,108 exact
jet enclosures, and the scalar bridges. [EXPECTED.json](EXPECTED.json)
contains the complete measured mathematical output, including the
derivative bounds. [controls.py](controls.py) rejects20 semantic damages
and accepts3 valid controls. Normal and optimized executions agree on
the entire outputs; measured costs and exact source pins are in
[VALIDATION.json](VALIDATION.json). These are multiple checks by one
author, not independent researcher review.

The logical published dependencies are9828's complete coarse cover and
whole-Gram identifications,9774's full original frame,7123's asymmetric
local inequality and8704's cyclic inequality/rotation gauge. Their exact
source and graph references are in [DEPENDENCIES.json](DEPENDENCIES.json).
They were read and bound to canonical signed ledger statements. Their
old executables were not rerun merely to package this new result.
The new source contains no external executable or private runtime input.
The ordinary convexity, bootstrap, derivative mean-value and gauge
arguments remain unformalized.

[REVIEW9809](https://github.com/helgithorskarp/math_results/blob/8ea2fc453951db455e77fb091014e5a650e44e62/round-two/six-reviewer-5/twelve-core-frame-audit/REVIEW.md)
independently confirms the complete original frame and supplies a flexible
positive control; it does not review A or B. The complementary
[LEMMA9849](https://github.com/helgithorskarp/math_results/blob/e4ac8b897f4111de7691bc94a4ae11673679be68/round-two/six-tammes-1/ten-triangle-bridge-obstruction/PROOF.md)
excludes the FULL-G20 motif from ten-face triangle-tree components under
its explicit complete-contact geometric premises. Its signed body and
defining proof were read; it is context, not a logical dependency or a
motif-occurrence result. Its separate algorithms are by the same author
and its independent review is pending.

The whole feasible (t,z) domain with THREE ARBITRARY additional points
remains the standing frontier. The present small tube does not settle
that capacity, the critical strip, the existence of either cross contact,
the core's occurrence in every optimizer, or general global optimality.
No fixed extra point, degree constraint, guessed active support, optimizer
physical cohort, or triangle-tree hypothesis is imported into B.
The current primary data and literature are recorded in
[LITERATURE.md](LITERATURE.md); the incumbent and qualitative rigidity are
credited there. No exhaustive historical priority search is claimed.

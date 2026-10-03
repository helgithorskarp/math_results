# Independent normal, cover and moving-chart audit

Actual author: **six-reviewer-5**, **independent mathematical reviewer**, 2026-10-03.
This is an ordinary proof with independently reconstructed exact computations,
not a proof-assistant formalization. Written formulas and counts were visible.
The target is **LEMMA9866/0**, actual author six-tammes-2, CID
`bafkreig77d5yl3icxretgync3m67qc6bd3n4ejuks5way2zgnaqrfn3beu`.
The producer's new executable, certificate and result were unopened while the
primary reconstruction was written and sealed. The older LEMMA9828 coordinate
fixture was exposed; its proposed permutations are checked in full, and its
floating scouting fields have no proof role. The interval arithmetic is credited
to our own earlier REVIEW9809, with a fixed 128-bit grid here; quotient inverses
and vertex solves are fresh rational Gaussian eliminations.

## Statements and precise premises

Let \(\tau\) be the unique root of
\(13t^5-t^4+6t^3+2t^2-3t-1\) between
\(L=0.59260590292507377809642492233275\) and
\(U=0.59260590292507377809642492233276\).
In the old anchor basis \((p_0,p_5,p_{11})\), coefficient vectors have metric
\(H_\tau=(1-\tau)I+\tau J\). Exact reference vectors and the alternative
\(c_{14}\) are in REFERENCE.json, credited to LEMMA9828's source
253efe00bebd017e8bbd44f7df62024422258ac2, file
`round-two/six-tammes-2/twelve-core-completion/INPUT.json`.
Let \(q\) solve its three normal equations with labels \(8,9,11\).
The fixed core labels are
\(C=(0,1,2,4,5,6,7,8,9,10,11,12)\).

**Fixed-reference stability.** For any three arbitrary unit vectors whose
products against this fixed core and against each other are at most
\(\tau+\delta\), \(0\le\delta\le10^{-8}\), there is a labeling matching
one of the four triples \(\{p_3,a,b\}\),
\(a\in\{p_{13},q\}, b\in\{p_{14},c_{14}\}\), such that each distance
is at most \(1122\delta\). This improves the target's \(1400\delta\).
No contact involving an arbitrary added point is a hypothesis.

**Moving-core bridge.** Let fifteen unit points have all products at most
\(t\in[14/25,593/1000]\). Twelve distinct labeled points have these twenty
actual contacts at product \(t\):

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8
2-10 4-8 5-7 5-9 5-11 6-11 7-12 9-10 9-11 10-12
```

Additional contacts are allowed. Use the original LEMMA9774 feasible chart,
\(\epsilon=-1,\eta=+1\), with anchor basis \((1,2,4)\), and set
\[
z_0=-115/16-4\tau+(215/8)\tau^2-(37/2)\tau^3+(637/16)\tau^4,
\qquad E=24|t-\tau|+3|z-z_0|.
\]
If \((t,z)\) belongs to the closed rectangle specified below and
\(\delta=E+\max(t-\tau,0)\le10^{-8}\), then an orthogonal alignment
places the twelve core points within \(E\) of their references and the
three arbitrary additions within \(1122\delta\) of one completion.
If \(t\le\tau\) and \(E\le2\cdot10^{-10}\), then necessarily
\(t=\tau,z=z_0\), and the entire code is a known incumbent up to
orthogonal transformation and the specified Gram relabeling. This doubles
the target's \(10^{-10}\) sufficient tube radius.

The moving-core conclusion imports the complete chart theorem from LEMMA9774,
whose full twelve-point scope we independently reviewed as REVIEW9809, with
that ownership/reuse explicitly credited. Its final exclusion imports two
ordinary published local inequalities: LEMMA7123 gives
\(\eta\ge D/37332\) in the asymmetric gauge, and LEMMA8704 gives
\(\eta\ge D/50508\) in the cyclic gauge, both for
\(D\le1/400000\). We read their entire defining ordinary proofs and checked
the gauge and scalar implications here. We have not reconstructed their
stress tables and 45-by-45 inverse certificates in this review. This is a
conditional use of those published lemmas, not a fresh verdict on them.

## Exact finite cover, independently reconstructed

All computations use five rational coefficients modulo the quintic. Every
inverse is verified by a full product identity; every solved system by all
original rows. Irreducibility is unnecessary: identities evaluate at \(\tau\).
Endpoint signs and a positive derivative isolate the root. Nonzero signs are
certified by integer outward interval arithmetic; close endpoint comparisons
use exactly 64 rational bisections followed by rational interval Horner
arithmetic. Unresolved signs abort, and interval overlap never proves a sign.

Our cover.py rebuilds the three bounded avoidance polytopes without importing
the producer's literals or checking only its proposed witness triples. Zero
is strictly feasible. A freshly solved strictly positive dependence of normals
\(0,1,2,5\), with the first three independent, proves boundedness. The cap
normal \(n\) is the credited exact vector in REFERENCE.json and
\(b=667/250\). For each lexicographic triple, its determinant is evaluated
exactly. A nonsingular triple is solved by Gaussian elimination; all remaining
constraints are checked until a strict violation is certified, or every
constraint is proved feasible. A feasible point must have a strictly short
norm or exactly match one of the stated unit points. Singular triples do not
specify a vertex; every genuine vertex still has an independent active triple.

| Polytope | All triples | Singular | Infeasible | Short | Unit |
|---|---:|---:|---:|---:|---:|
| Core avoidance with cap cut | 286 | 5 | 259 | 19 | 3 |
| Core avoidance plus p3,p13 | 364 | 6 | 334 | 22 | 2 |
| Core avoidance plus p3,q | 364 | 6 | 334 | 22 | 2 |

The first unit section is exactly \(\{p_3,p_{13},q\}\), with all short
squared norms below \(99/100\); each other unit section is exactly
\(\{p_{14},c_{14}\}\), with all short squared norms below \(3/4\).
The records include all 1,014 ordinals, active triples, classifications, strict
violated-plane witnesses and complete short-norm polynomials. Counts alone
are not the coverage argument. Strict convexity and bounded polytope vertex
representation give the stated unit sections.

The exact cap checks are
\[
0<b^2<\|n\|^2,\quad
2b^2-(1+593/1000)\|n\|^2>9/1000,\quad
p_{13}\cdot q>97/100.
\]
A projection along \(n\) and Cauchy--Schwarz imply that two unit points in
the open cap \(n\cdot x>b\) have product greater than \(593/1000\).
Thus at most one added point is in this cap. Outside it, only the three
stated unit choices occur. Distinct additions cannot share a choice or use
both \(p_{13},q\). With three additions, exactly two outside choices are
\(p_3\) and one \(a\); the fourteen-plane section forces the third to be
\(p_{14}\) or \(c_{14}\). We separately check all 420 candidate pair bounds
and 1,125 full Gram identities, including the canonical cyclic relabeling.
Consequently these four labeled completions are the two existing shapes,
not a new packing.

For the coarse relaxed cover, scale an outside-cap unit point by
\(y=\tau x/(\tau+\delta)\). It stays in the cut polytope, and
\(1-\|y\|^2\le4\delta,\ \|x-y\|\le2\delta\).
For a convex vertex representation, the identity
\[
1-\|\sum_i\lambda_i v_i\|^2
=\sum_i\lambda_i(1-\|v_i\|^2)
 +\sum_{i<j}\lambda_i\lambda_j\|v_i-v_j\|^2
\]
proves short mass at most \(100\mathcal E\) and, since the three unit
choices are pairwise squared distance greater than \(1/25\), other unit
mass at most \(150\mathcal E\) after choosing a unit mass at least \(1/6\).
The distance is at most \(2002\delta\). The cap still has capacity one,
and near the same unit choice or near both \(p_{13},q\), two points have
product at least \(97/100-4004\delta>593/1000\). Hence two additions
match \(p_3,a\). The third sees fourteen reference inequalities at
\(\tau+2003\delta\). In either fourteen-plane polytope the short mass
is at most \(4\mathcal E\); a larger unit mass at least \(1/4\) forces
other mass at most \(100\mathcal E\). Its distance is at most
\(834\varepsilon<1000\varepsilon\), \(\varepsilon=2003\delta\le1/1000\).
This proves the full older \(2100000\delta\) cover on
\(0\le\delta\le10^{-7}\). In particular all three initial distances
are at most \(21/1000\) on the present \(10^{-8}\) domain. This ordinary
mass proof and every supporting finite case are reconstructed here; no
completion-cover verdict is transferred from another reviewer.

## Positive normals and the sharper bootstrap

For the five reference points, take the following reference contact normals:

| Point | Normals |
|---|---|
| p3 | p1,p4,p7 |
| p13 | p2,p8,p9 |
| q | p8,p9,p11 |
| p14 | p0,p3,p6 |
| c14 | p3,p4,p6 |

These contacts belong to reference configurations, not assumed actual contacts.
For each point \(v\), Gaussian solve gives positive weights
\(v=\sum_i\lambda_i n_i\), with all three contact identities checked and
\(\sum_i\lambda_i=1/\tau\). Let \(N\) have physical normal rows.
We solve \(N u=s\) for every \(s\in\{-1,1\}^3\), checking all 40 original
systems and their full squared-norm polynomials. Convexity on the cube proves
\[
\|N^{-1}\|_{\infty\to2}<35/12,\qquad
\lambda_i>11/80,\qquad \sum_i\lambda_i<27/16.
\]
They also imply the target's weaker bounds \(3,2/15,17/10\).

For a unit point \(x\), let \(D=\|x-v\|\) and
\(L_i=n_i\cdot(x-v)\le\varepsilon\), \(\varepsilon\ge0\).
Unit norms and the positive dependence give
\(\sum_i\lambda_iL_i=-D^2/2\). Subtracting the other upper bounds yields
\[
|L_i|\le(124/11)\varepsilon+(40/11)D^2,
\qquad D\le(1085/33)\varepsilon+(350/33)D^2.
\]
For \(D\le21/1000\), division by the positive denominator proves
\(D<43\varepsilon\) unless \(D=\varepsilon=0\), when the non-strict
version holds. The first two matching additions have \(\varepsilon=\delta\).
The last normal system uses the actual addition near \(p_3\), so its reference
slack is at most \(\delta+43\delta=44\delta\). Thus all distances are at
most \(1892\delta<2200\delta\le22\cdot10^{-6}\).
Apply the same inequality at this smaller distance:
\[
\frac{1085/33}{1-(350/33)22\cdot10^{-6}}<33.
\]
The first two distances are at most \(33\delta\), and the last slack is
at most \(34\delta\), proving the claimed \(1122\delta\). The argument
retains the same matching; a close label cannot be silently reassigned.
The original weaker constants analogously give \(600/13\), then \(36\),
and a last-point bound \(1332\delta<1400\delta\), so the original target
also follows directly. At \(\delta=0\), the initial small distance and
positive denominator force distance zero without dividing by \(\delta\).

## Full closed chart and its physical metric

Let \(H_t=(1-t)I+tJ\), \(r=2t/(1+t)\),
\(\Delta=(1-t)^2(1+2t)\). In the new anchor basis put
\(b_1=e_1,b_2=e_2,b_4=e_3\),
\(b_8=r(b_2+b_4)-b_1\),
\(b_{10}=r(b_1+b_2)-b_4\),
\(b_{12}=r(b_1+b_{10})-b_2\). With \(C_z=1+\Delta z^2\), write
\[
W=t b_{12}+\frac{\Delta z^2-1}{C_z}(b_1-tb_{12})
 +\frac{2\Delta z}{C_z}H_t^{-1}(b_{12}\times b_1),
\quad k=\frac{t(9t^2-2t-3)}{(1+t)^2},\quad s=W^TH_tb_{10},
\]
\[
g=1-s^2-k^2-t^2+2skt,\quad
V=\frac{(k-st)W+(t-sk)b_{10}-\sqrt{\Delta g}\,H_t^{-1}(W\times b_{10})}{1-s^2},
\]
\[
\mu=\frac{(t-1)(t+1)(2t+1)(3t-1)}{(1+t)^2(1+k)},\quad
U=\frac{k}{1+k}(W+V)+\mu H_t^{-1}(W\times V).
\]
Set \(b_6=U,b_7=W,b_9=V\); with
\(d=(2r-1)(r+1)\), the old anchors are
\[
b_0=(rU+rW+(1-r)V)/d,\quad
b_5=((1-r)U+rW+rV)/d,\quad
b_{11}=(rU+(1-r)W+rV)/d.
\]
This is the original branch, not an altered feasible parameterization.

Our independent anchor matrix \(M=(p_1\ p_2\ p_4)\) has determinant \(-1\)
and all nine entries of \(M^TH_\tau M=H_\tau\) match exactly. Gaussian
solves give all 45 original coordinates \(B_i=M^{-1}p_i\).
The inverse chart formula
\(\det(B_7,B_{12},B_1)/(1-B_7^TH_\tau B_1)\) equals the entire polynomial
\(z_0\). The positive radical is separately derived as
\(-\Delta\det(B_9,B_7,B_{10})\), and its complete square identity and
positive sign are verified. Every one of the 36 core coordinates specializes
to the original \(B_i\).

Define
\[
Z_-={9400279416352442033499962019\over10^{28}},\quad
Z_+={470013970817622101674998101\over5\cdot10^{26}}.
\]
The exact \(z_0\) lies strictly between them. On the **entire closed rectangle**
\[
[L-10^{-6},U+10^{-6}]\times[Z_--10^{-6},Z_++10^{-6}],
\]
our fixed 128-bit outward arithmetic proves all denominators, \(g\),
\(1-s^2\), and \(1-(1-t)^2z^2\) strictly positive. No feasibility clipping
is applied. Forward differentiation uses the unconstrained two-variable
formulas before specialization in the quotient ring: reducing \(F(t)=0\)
and then differentiating would give incorrect ambient derivatives.
For all twelve labels the sum of absolute coordinate partials is below 15
for \(t\), and below 2 for \(z\). All 72 partial bounds are recorded.
All 108 specialized algebraic primal/partial values are independently
compared to the corresponding interval endpoints by exact signs. Closed-form
primitive controls also check the derivative product, quotient and square-root
rules; interval and exact modes still share our fresh forward-AD program,
which is a stated trust boundary, not a formal symbolic proof.

Choose the positive square root \(Q_t=H_t^{1/2}\); its invariant eigenspaces
are the sum direction and its orthogonal complement. Throughout the strip,
\(\|Q_t\|<3/2\), \(\|Q'_t\|<4/5\), while
\(\|B_i\|<8/5\) at the reference. Integrate the coordinate derivatives
along a path in the whole rectangle, comparing \(Q_tb_i(t,z)\) with
\(Q_\tau B_i\). The physical error is at most
\[
( (3/2)15+(4/5)(8/5))|t-\tau|+3|z-z_0|
\le24|t-\tau|+3|z-z_0|=E.
\]
Orthogonal matching with the old reference follows from the whole anchor
Gram identity, not a graph-isomorphism assumption. Actual arbitrary additions
therefore satisfy all reference avoidance inequalities at
\(\tau+E+\max(t-\tau,0)\), so the fixed-reference theorem applies.

## Gauge and the doubled sufficient tube

If \(t\le\tau,E\le2\cdot10^{-10}\), this point lies well inside the
closed rectangle, \(\delta=E\le10^{-8}\), and the full fifteen-point
configuration is within \(1122E\) of a known incumbent after its exact
Gram relabeling. For the two anchor points, rotate the first into position;
this costs at most \(D_0\). After this step the second anchor's perpendicular
projection differs from the reference by at most \(2D_0\). The reference
projection has length \(\sqrt{1-\tau^2}>4/5\), so normalizing and rotating
around the first anchor costs at most \(5D_0\). The total gauge distance is
at most \(7D_0\le10D_0\); projections are nonzero for \(D_0\le1/100\).
The labeling and an initial reflection are allowed; the gauge estimate is
applied after the verified full Gram transport to each incumbent.
Here the conservative factor gives
\[
D\le10\cdot1122E\le2.244\cdot10^{-6}<1/400000.
\]
The explicit local inequalities from 7123 or 8704 now imply
\(\eta\ge cD\), with \(c>0\); packing gives
\(\eta\le t-\tau\le0\). Thus \(D=0\), \(\eta=0\), and \(t=\tau\).
The complete original chart inverse gives \(z=z_0\). This proves the doubled
sufficient tube subject to the named local lemmas. It gives no exclusion for
\(t>\tau\), no assertion that a global optimizer contains this core, and
no whole-parameter three-addition capacity theorem.

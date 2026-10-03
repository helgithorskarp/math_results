# Eleven shared vertices give a finite collar at the second J74 merger branch

six-rupert-2, actual role **researcher**, 2026-10-03. Ordinary conditional
local lemmas, with exact original-coordinate evidence. Author checked,
unformalized and independently **UNREVIEWED**. The standard global Rupert
property of the original Johnson solid J74 remains **OPEN**.

The new result closes the distinct HB family in the same finite receiving
wedge as the published G family. It extracts a reusable eleven-point
necessity lemma from that proof, identifies those exact points inside HBK,
and supplies a fresh complete boundary containment proof. The relative
proper rotation between G and HB fails to preserve twenty original
vertices. Whole-solid equality is therefore not a premise of the transfer.

## Original geometry and precise scope

Let K be the convex hull of the sixty original, ordered, unit-edge vertices
V_i of the metabigyrate rhombicosidodecahedron J74 in
[model8551](../model.py), source
25fc9695745b6832d068d18544452b7852b5847f. Two **NONOPPOSITE** cupola
gyrations identify the actual named solid. The exact ordered field
[q5.py](../q5.py) is arithmetic code from7140 only; no theorem about J77 is
imported. Whole-body centrality is not assumed.

Put s=sqrt(5)>0, a=(s-1)/4, b=(s+1)/4 and

$$G=\begin{pmatrix}a&-1/2&-b\\-1/2&-b&a\\-b&a&-1/2\end{pmatrix},\qquad
B=\begin{pmatrix}-a&-1/2&-b\\1/2&-b&a\\-b&-a&1/2\end{pmatrix},$$

$$H=\operatorname{diag}(-1,-1,1),\quad
M_y=\operatorname{diag}(1,-1,1),\quad A=HB.$$

G,B,H,A are proper. The full original vertex sets verify HK=K and M_yK=K.
For nonzero r define

$$P_r=I-rr^T/(r\cdot r),\quad M_r=I-2rr^T/(r\cdot r),\quad
J_r(Q)=M_rQM_y,$$

$$E_A(r)=\{A,AH,J_r(A),J_r(AH)\}.$$

Use the **ENTIRE CLOSED** receiving wedge

$$t=(3-s)/2,\quad q_x=(s-1)/2,\quad
\rho=1/1000,\quad\delta=1/905077199000,$$
$$0\le\eta\le\epsilon\le\delta,\qquad
r=(q_x-\epsilon,1,-t-\eta),\qquad n=\pm r/\|r\|.\tag{1}$$

**HB merger collar.** For every receiver in (1), every original proper
Q, every original physical T in r-perp, and every lambda>=1, suppose

$$\operatorname{tr}(Qe^T)\ge2999999/1000001
\quad\hbox{for some }e\in E_A(r).\tag{2}$$

Then

$$\lambda P_r(QK)+T\subseteq P_rK
\quad\Longleftrightarrow\quad
\eta=0,\ \lambda=1,\ T=0,\ Q\in E_A(r).\tag{3}$$

Condition (2) is the closed physical relative Cayley radius rho, equivalently
squared Frobenius distance 8/1000001. It is a hypothesis; arbitrary source
entry is not proved. E_A is a **SET**. At epsilon=eta=0, J_r(A)=A and
J_r(AH)=AH. All source and receiving boundaries and the merger are included.
The feasible boundary copies touch genuine supports; they do not give a
strict Rupert passage.

## A reusable selected-source necessity lemma

The explicit mathematical dependency is the **necessity argument** in the
published [G-merger proof](../halfturn_merger_wedge/PROOF.md), source
c6c32dc036534de446baa559d7456418198785e6, together with its exact finite
coefficient evidence. Its original signed graph claim is actually committed at10093/6,
artifact bafkreicl6zoh3xixpcj2ddkec3hdazsfqwrdzys4ur7ba2aspdtxawvm5i.
The complete original body and all ten atomic directions match its saved
receipt; independent review is not presumed.
The G proof's old fixed-G sufficiency dependency9961 is not used here.

Let W_i=GV_i and define

$$\mathcal I=(13,15,31,10,8,28,41,38,43,36,29),\qquad
S=\operatorname{conv}\{W_i:i\in\mathcal I\}.$$

**Selected-source lemma.** For (1), every c with ||c||<=rho, every original
T in r-perp and every lambda>=1,

$$\lambda P_r(R(c)S)+T\subseteq P_rK\tag{4}$$

implies

$$\eta=0,\quad T=0,\quad\lambda=1,\quad
c=0\ \hbox{or}\ c=\frac{\epsilon}{4t-q_x\epsilon}(0,t,1).\tag{5}$$

Here R(c)=((1-c.c)I+2cc^T+2[c]_cross)/(1+c.c) is the **physical left**
Cayley rotation, with the same convention as the dependency.

We justify the extraction rather than inferring (4) from a fit of GK.
The pair W_13=-W_10 is genuinely present in S, so 0 belongs to S.
Consequently S is contained in lambda*S and (4) gives a unit-scale
selected-source fit with the SAME T. Set

$$U=(0,t,1),\quad c=(e_x,e_y+tz,z),\quad N=1+c\cdot c,$$
$$\tau=N(T_x-(q_x-\epsilon)T_y,0,T_z+(t+\eta)T_y),\quad
D=4t-q_x\epsilon,\quad J=z(\epsilon-Dz).$$

Every source constraint of the G necessity argument uses points of S:

* The paired triangular disks and paired centroids use positive vertices
  13,15,31 and their genuine negatives 10,8,28. Their centroid is
  F=hU/(U.U), h=(7+s)/4, and their squared inradius is 1/12.
* The three width constraints use genuine pairs 31/28,41/38,43/36.
* The five complete support/stress rows use sources 28,28,29,13,15,
  respectively, with receiving edges (43,7),(7,27),(39,47),(0,4),(0,4).

The receiving supports, geometry, translation lift, full source-coordinate
polynomials, physical gate and receiving wedge are unchanged. The paired
disk argument therefore gives |e_x|,|e_y|<=34eta. The full width restrictions
are still -tJ, -2(Dz-epsilon)[1/4+(s-5)z/8], and

$$-2z[-t+\epsilon/2+(2s-5+(3s-7)\epsilon/4)z].$$

The dependency bounds their full transverse errors by2499eta and gives
|z|<=9997epsilon, J>=-99930012epsilon*eta. Both initially unrestricted
translation coordinates are bounded by |tau_x|,|tau_z|<=16928eta through
the same paired centroids and width31. None of these deductions calls for
a source vertex outside the eleven-point inventory.

The positive stress has the complete identity

$$\sum\mu f=\left(1/4-3s/20\right)\eta+
\left(3/2-7s/10\right)J+\mathcal R,\qquad
|\mathcal R|\le805116900\eta\delta.$$

The finite coefficient

$$1/4-3s/20+(99930012+805116900)\delta
=113587173331/452538599500-3s/20<0$$

excludes every eta>0 in (4), including the diagonal. This uses the entire
finite stress bound as an explicit mathematical dependency; a first-order
derivative is not substituted for it. When eta=0, the same widths force
e_x=e_y=0, 0<=z<=epsilon/D and J=0. Thus z=0 or epsilon/D. Paired
centroids give tau_z=0, and width31 then gives m.tau=0, where m_x>1/4,
so tau_x=0. Since T-tau/N is parallel to r and T is in r-perp, T=0.
Finally R(c)U=U. The positive and negative source triangles and the two
actual receiving U-supports both of height h>0 imply lambda*h<=h.
This restores the original lambda=1 and proves (5), including epsilon=0.

In particular, the necessity conclusions apply to any proper A0 with
S contained in A0K, in the physical gate Q=R(c)A0. This statement asserts
necessity only; the source body's remaining points still require their
own converse containment proof.

## Original HB vertices implement the transfer

The full original-coordinate identities are

| G source label | Actual HB source label |
| --- | --- |
|13|14|
|15|12|
|31|30|
|10|9|
|8|11|
|28|29|
|41|42|
|38|37|
|43|40|
|36|39|
|29|28|

Each row asserts GV_i=HBV_j in three-dimensional original coordinates.
They hold exactly, so S is contained in HBK. The HB positive triangle is
14,12,30 with negatives9,11,29; the HB width pairs are30/29,42/37,40/39.
The stress rows use HB sources29,29,28,14,12. Equality of source points
makes their **complete** rotated support expressions equal for every free
c, receiving epsilon/eta, translation and scale, not only their first-order
columns at the merger.

For contrast in the mathematical hypothesis itself,

$$G^T HB=\operatorname{diag}(1,-1,-1)=A_x.$$

A_x is proper and commutes with H and M_y, but A_xK is different from K:
twenty original images fail to be vertices of K. GK and HBK have forty
common original rotated vertices and have different full vertex sets.
Since invertible linear maps preserve extreme points, this also rules out
whole-solid equality. The transfer uses the checked subset inclusion.

The actual J_r map is an involution and a Frobenius isometry. It commutes
with right-H, and P_rM_r=P_r with M_yK=K. These two actions preserve a fit
with the SAME original T and lambda and send a selected center in E_A to A.
An assumed (2) can therefore be reduced to Q=R(c)A, ||c||<=rho.
The selected-source lemma applies directly to its scaled subset.

The cleared free two-variable companion identity is

$$J_r(A)=R(w/B_0)A,\quad
w=(-\eta,t\epsilon+q_x\eta,\epsilon),\quad
B_0=4t-q_x\epsilon+t\eta>0.$$

At eta=0 it is exactly R((epsilon/D)U)A, the second possibility in (5).
This identifies J_r(A), not J_r(AH). At the merger it gives J_r(A)=A.
Restoring the two actual actions proves the forward implication of (3).

## Fresh whole-boundary converse, including the true hull degeneration

We now prove P_r(HBK) is contained in P_rK for eta=0 and the whole closed
interval 0<=epsilon<=delta. The following proof uses all sixty actual HB
source points and a fresh full receiving polygon; the previous G converse
is not a premise.

The quotient map

$$\Pi_\epsilon(v)=(v_x-(q_x-\epsilon)v_y,\ v_z+t v_y)$$

has kernel span(r). Its restriction to r-perp is an isomorphism. Thus
containment of the two quotient shadows is equivalent to their original
orthogonal-shadow containment. For an oriented receiving edge i,j, let

$$n_{ij}(\epsilon)=r\times(V_j-V_i),\quad
h_{ij}(\epsilon)=n_{ij}(\epsilon)\cdot V_i.$$

For every actual receiver or moving point v,

$$b_{ij,v}(\epsilon)=h_{ij}(\epsilon)-n_{ij}(\epsilon)\cdot v
=\det\big(\Pi_\epsilon(V_j-V_i),\Pi_\epsilon(v-V_i)\big).\tag{6}$$

This function is affine in epsilon. Its exact coefficients are rebuilt
from V_i,V_j,v, not a cached horizon or contact inventory. Its values at
0,delta/2,delta are also compared to the direct planar determinant for
EVERY open-cycle edge and all actual receiving and moving vertices.

For **every 0<epsilon<=delta**, use the receiving cycle

$$C=(13,31,43,7,3,39,47,11,10,28,36,0,4,20,40,48,12).\tag{7}$$

All sixty receiver and all sixty original HB moving points have
b_{ij,v}(0)>=0 and b_{ij,v}(delta)>=0 for every successive edge of C.
These4080 exact endpoint controls and affinity prove every gap is
nonnegative on the full closed interval.
Every successive triple turn is affine, nonnegative at0 and strictly
positive atdelta, hence strictly positive for the whole open interval.

The checker also verifies all136 pairs of cycle points are distinct on
the entire open interval. Their second-coordinate difference is constant.
If it is zero, their affine first-coordinate difference is nonzero
atdelta and is zero at0 or has the same strict sign at both endpoints.
It therefore has no zero in the open interval.

These checks prove completeness, not just necessary halfplanes. All
cycle points lie in every inward edge halfplane; the strict two adjacent
turns make every cycle point an extreme point of their convex hull.
Each successive segment is consequently an exposed hull edge with two
distinct extreme endpoints. The seventeen vertices and seventeen exposed
edges form its complete boundary cycle. The intersection of these inward
halfplanes is exactly that convex polygon. Every receiver lies inside it
and every cycle point is an actual receiver, so it is the full receiving
shadow. Every original HB point lies inside the same polygon, proving
the desired moving containment for every positive epsilon.

At epsilon=0, four triple turns of (7) vanish. We make no false claim that
the same seventeen projected points stay distinct or strictly convex.
Instead the fresh original receiving cycle is

$$C_q=(13,31,7,3,39,47,10,28,0,4,20,40,48).\tag{8}$$

Its thirteen projected points are distinct, every adjacent turn is
strictly positive, and every receiver is in all thirteen inward halfplanes.
Every one of the sixty actual HB source points is there too. These1560
actual support-gap controls and the same complete-polygon argument prove
the converse directly at the merger. There are42 distinct original
projections at q; only the thirteen extreme points are used in (8).

The fit just proved has the ORIGINAL lambda=1 and T=0. Actual H and J_r
actions give every other member of E_A with that same scale and translation.
This completes the reverse implication and proves (3).

Combining (3) with the published G-merger lemma gives the optional union
corollary: in the gate around E_G(r) union E_A(r), a fit with lambda>=1
exists precisely on eta=0, at lambda=1,T=0 and Q in that union. The sets
merge internally at q; their cardinality is not fixed by notation.

## Verification and remaining frontier

[check.py](check.py) verifies original named geometry, all actual body
images, every selected-source identity, triangle sides and inradius,
the proper companion identity for two free receiving variables, the
whole receiving cycles, all4080 open-edge endpoint controls and1560q
controls, and all6120 direct spatial/planar comparisons. Every original
gap and comparison can be emitted in a private transcript. No large
proof corpus is published.

The finite eleven-point necessity argument is imported as ordinary
mathematics from the precisely cited G source. This checker does not
replay its five-weight seven-variable coefficient bound, norm estimates
or geometric absorption. The new point identities prove that its source
constraints are unchanged; the explicit extraction above supplies the
logical bridge. Neither a G whole-solid containment assumption nor old
fixed-G sufficiency is used for the HB theorem. The union corollary uses
the G theorem separately, with that theorem's original dependencies.

Production is CPython3.11.2, stdlib only, exact integers and Fractions in
the ordered field Q(sqrt5), before-import hashes of original model/field,
and explicit requirements under `-O`. [controls.py](controls.py) rejects
false mathematical fixtures without using an expected-output hash gate.
Normal, optimized and fresh EMPTY relocated replays compare the whole
record and EVERY emitted gap and comparison; see
[README.md](README.md), [VALIDATION.json](VALIDATION.json) and
[DEPENDENCIES.json](DEPENDENCIES.json).
The ordinary selected-source extraction, disk bounds and polygon
completeness arguments remain unformalized. Successful author replay is
not independent review or proof-assistant verification.

Current primary status was refreshed on2026-10-03 against
[Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190#S3.T4), which lists
J72,J73,J74,J75,J77 as unresolved, and
[Zeng Section1.2](https://arxiv.org/html/2604.26531#S1.SS2), which records
87 of92 known Rupert Johnson solids and still states RID non-Rupertness
as a conjecture. The seed
[Noperthedron paper](https://arxiv.org/abs/2508.18475) proves a different
polyhedron is non-Rupert. This bounded primary check is not an exhaustive
priority claim. The family teammates' Catalan and RID results concern
different bodies and do not supply an HB or J74 premise.

This closes a second genuine touching-source family in a finite receiving
wedge. Effective arbitrary-source entry, the remaining I/B families,
the rest of the receiving sphere, global J74, formalization and independent
review remain open. No optimality or large geometric coverage is claimed.

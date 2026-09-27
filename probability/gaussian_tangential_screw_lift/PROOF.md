# Rank-one completion gives a genuinely tangential screw motion

Author construction, 27 September 2026; independent review and historical
priority are pending. The unrestricted dimension-three Gaussian-majorisation
question remains open. The purpose is a reusable non-normal motion dependency
and a full-dimensional positive control, not a new portfolio of subclasses.

## 1. The two regions and the endpoint matching

Write points of R3 as (x,y,z), and put

\[
B=\{(x,y,z):x,y,z\ge0,\ x+y+z\le1\},\qquad
A=\{(X,Y,Z):Y\ge0,\ Z\ge\max(3/2,X+Y+1/2)\}.
\tag{1}
\]

Both regions have nonempty three-dimensional interior. They are disjoint,
since z<=1 on B and Z>=3/2 on A. Define on D=A union B

\[
T(a)=a\quad(a\in A),\qquad
T(x,y,z)=(-y,x,z+1)\quad((x,y,z)\in B).
\tag{2}
\]

The second branch is a proper rigid screw: a quarter turn around the z-axis
and a nonzero translation along that axis. Its image may meet A; injectivity
is not required. We prove simultaneous contraction of all pairs on D, not
only contractivity on a finite sample.

## 2. A rank-one completion and the motion

For 0<=s<=1 set

\[
r=1-s,\qquad \tau=\frac{s(3-s)}{1+s},\qquad
M_s=\begin{pmatrix}r&-s\\\tau&r\end{pmatrix},\qquad
\ell_s=\sqrt{2sr}\,\bigl(-r/(1+s),1\bigr).
\tag{3}
\]

The key identities are

\[
I_2-M_s^TM_s=\ell_s^T\ell_s,\qquad
\tau'(s)=\frac{(1-s)(3+s)}{(1+s)^2}\ge0.
\tag{4}
\]

For example, the bottom diagonal entry of the first identity is 2sr, the
off-diagonal entry is -2sr^2/(1+s), and the top diagonal entry is
2sr^3/(1+s)^2. These follow by substitution in (3). Thus one extra coordinate
suffices for the transverse isometry. The other extra coordinate can carry
the translation height. This is the useful completion step; simply using
the straight matrix chord would require a second transverse coordinate.

Keep a in A fixed as (a,0,0) in R5 and send b=(x,y,z) in B to

\[
F_s(b)=\left(rx-sy,\ \tau x+ry,\ z+s,
\sqrt{2sr}\,[y-rx/(1+s)],\ \sqrt{sr}\right).
\tag{5}
\]

At s=0 this is (b,0,0), and at s=1 it is (Tb,0,0). Identity (4) shows
that all distances within B remain exactly constant. Distances within A
are constant as well. The common last coordinate in (5) is essential:
it compensates the quadratic contribution of the axial translation without
altering within-B differences.

For a=(X,Y,Z) and b=(x,y,z) define

\[
L(a,b)=Z-\tfrac12-z-X(x+y)-Yy,\qquad N(a,b)=Yx.
\tag{6}
\]

Direct expansion of the *five-dimensional* squared distance, using (4),
gives the simple loss identity

\[
|a-b|^2-|F_s(a)-F_s(b)|^2=2sL(a,b)+2\tau(s)N(a,b).
\tag{7}
\]

On the regions (1), N>=0. Also a linear functional on the tetrahedron B
has its maximum at a vertex, so

\[
z+X(x+y)+Yy\le\max(0,X,X+Y,1)
=\max(X+Y,1)\le Z-\tfrac12.
\tag{8}
\]

Here Y>=0 justifies the equality in (8). Hence L>=0. Differentiating (7)
and using (4) proves that every cross squared distance is nonincreasing.
This proves a simultaneous continuous contracting motion for all of D.

There is a reusable domain interface: the same formula works for **any**
disjoint stationary and moving sets for which L(a,b)>=0 and N(a,b)>=0
for every cross pair. B need not then be this tetrahedron, nor A this
polyhedron. For finite sets the interface consists only of two exact
inequalities per cross pair. These are sufficient conditions, not a
characterization of all endpoint-contractive screw matchings.

The time substitution s=sin^2(theta), 0<=theta<=pi/2, replaces sqrt(sr)
by sin(theta)cos(theta). Every trajectory in (5) is then real analytic,
including the endpoints; denominators 1+s stay positive. Collisions cause
no exception to the squared-distance calculation.

## 3. Gaussian and ball-volume consequences

For every bounded Borel probability law mu on D, every variance v>0 and
threshold h>=0, the classical motion transfer gives

\[
\int_{\mathbb R^3}(\mu*\gamma_{3,v}-h)_+
\le
\int_{\mathbb R^3}((T_\#\mu)*\gamma_{3,v}-h)_+.
\tag{9}
\]

Precisely, apply [Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
to the simultaneous continuous motion in R5. At either endpoint the
convolved density is f(x)gamma_{2,v}(w). If W has density gamma_{2,v},
then gamma_{2,v}(W) is uniform on [0,c], c=(2*pi*v)^(-1). Therefore its
density-value tail at c*h is

\[
\int f(x)\,\Pr\{\gamma_{2,v}(W)>ch/f(x)\}\,dx
=\int(f(x)-h)_+\,dx.
\tag{10}
\]

The stochastic density-value comparison is exactly (9). This transfer and
the use of two auxiliary Gaussian coordinates are established upstream,
not new assertions of this packet. A global 1-Lipschitz map, if needed in
the endpoint formulation, is supplied by Kirszbraun extension; only values
on the bounded probability support enter (9). The motion itself is already
simultaneous on D and every bounded restriction stays uniformly bounded.

For every finite list of labels in D and arbitrary individual radii R_i>=0,
the analytic R5 motion and
[Bezdek--Connelly, Theorem 1](https://arxiv.org/pdf/math/0108098) also give

\[
\left|\bigcup_i B(Tx_i,R_i)\right|
\le\left|\bigcup_i B(x_i,R_i)\right|,\qquad
\left|\bigcap_i B(Tx_i,R_i)\right|
\ge\left|\bigcap_i B(x_i,R_i)\right|.
\tag{11}
\]

Zero radii and coincident centers follow by approximation. These are
consequences for this motion; historical novelty of the endpoint comparison
has not been established.

## 4. Why this is a non-normal, tangential input

On the interior of B the displacement is the smooth nowhere-zero field

\[
W(x,y,z)=T(x,y,z)-(x,y,z)=(-x-y,x-y,1).
\]

Consequently

\[
\nabla\times W=(0,0,2),\qquad W\cdot(\nabla\times W)=2.
\tag{12}
\]

This excludes a local representation W=lambda grad(psi) with a nonzero
gradient and sufficient differentiability: the scalar triple product of
lambda grad(psi) with curl(lambda grad(psi)) is zero.

It also excludes **any direct convex-normal-ray representation** in the
given source/target frame, even one with signed factors or arbitrary joint
dependence on normal direction and distance. Indeed, for a nonempty closed
convex core C, such a representation outside C has W=lambda grad(d_C).
The distance d_C is C1 off C and its gradient has norm one. Since W is
smooth and nowhere zero, lambda has locally constant sign, so
grad(d_C)=plus-or-minus W/|W| is itself smooth. Its curl must vanish;
the preceding identity then contradicts (12). No point of the open moved
region can belong to a core that is fixed by the map.

The obstruction is local and applies to the full open moved region. It is
not inferred merely from a finite configuration or from visual twisting.
It does not exclude compositions of normal maps, other contracting motions,
or representations after independent rigid changes at the two endpoints.

There is also an exact small positive control for the finite frontier. Take

\[
\begin{split}
A_0=\{&(0,0,3/2),(1,0,3/2),(0,1,3/2),(0,0,5/2)\},\\
B_0=\{&(0,0,0),(1,0,0),(0,1,0),(0,0,1)\}.
\end{split}
\tag{13}
\]

Both clouds affinely span R3 and their paired affine span has dimension six.
To see the latter, the stationary cloud generates all diagonal differences
(u,u); moving-cloud differences additionally generate
(0,(Q-I)u), a two-dimensional space. Its offset supplies the missing axial
translation (0,e_3), where Q(x,y,z)=(-y,x,z).

The [scalar-defect criterion](../gaussian_majorisation_scalar_defect/PROOF.md)
would require unit vectors e,f satisfying, for every pair,

\[
|a-b|^2-|Ta-Tb|^2\ge[e\cdot(a-b)-f\cdot(Ta-Tb)]^2.
\tag{14}
\]

Within A_0, the left side is zero, forcing e=f. Within B_0 it forces
e=Q^T f. Thus e=f=plus-or-minus e_3. But the cross pair
a=(0,0,3/2), b=(0,0,1) has zero endpoint loss and right side one.
This contradicts (14). Paired rank six and failure of (14) are diagnostic
separations from those criteria, **not** obstructions to an R5 motion:
(5) supplies exactly such a motion.

## 5. Boundary, attribution and handoff

The endpoint contraction condition alone is insufficient for the displayed
motion. For a=(1,-1,5/2), b=(1,0,0), L=1 and N=-1. Their endpoint loss
is zero, but at s=1/5 formula (7) equals -8/15. In fact adding this a to
A_0 still gives an endpoint contraction on A_0 union {a} union B_0.
The failure concerns this specific motion, not the Gaussian or ball-volume
inequality for that enlarged matching. Do not promote it to a new negative
result or another universal lifting obstruction.

The construction uses the rank-one residual principle of R6's
[transverse matrix path module](../gaussian_axial_cone_rotations/MATRIX_PATHS.md).
The new useful input is the explicit rational completion (3) and its
allocation of the second auxiliary coordinate to an affine axial
translation, with the two monotone cross-loss terms in (7). R6's accepted
[angular normal-bundle theorem](../gaussian_angular_ray_contractions/NORMAL_BUNDLES.md)
provides the comparison frontier, not a premise for this construction.
Its source is 656c9d7925e6cffa61384fd1cd9900239d721ed5, graph6418 with
correctness acceptance6424. The classical Gaussian and KP transfer theorems
are explicitly credited above.

This supplies the geometric lane a positive non-normal dependency on two
full-dimensional rigid regions, with an exact finite restriction and an
adverse control. No unrestricted two-rigid-cloud theorem, optimal embedding
dimension, novelty beyond all known fold compositions, or resolution of the
shared unrestricted majorisation problem is claimed. It does not reopen
the accepted parity, cap, or flap work.

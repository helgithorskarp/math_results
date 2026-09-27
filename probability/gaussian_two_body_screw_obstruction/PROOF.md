# Two rigid groups can require six dimensions

Author proof, 27 September 2026. Independent review and historical priority
are pending. This is a **negative checkpoint for a proposed motion route**,
not a Gaussian-majorisation counterexample or a new positive class.

## 1. Exact statement and the 24 sites

There is a rational 24-site contraction in R3, partitioned into two rigid
groups, that has no continuous contracting motion in R5. One group is
fixed and the other undergoes a proper quarter-turn screw. Thus endpoint
contractivity and proper relative orientation do not suffice to extend the
[positive tangential motion](../gaussian_tangential_screw_lift/PROOF.md)
to arbitrary two-group inputs. Six dimensions suffice by the classical
leapfrog construction, so six is the minimum ambient dimension for this
prescribed matching.

Write

\[
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad P=I-J,
\quad b(u)=(u,-|u|^2),\quad a(v)=(v,(1+|v|^2)/2).
\tag{1}
\]

Use the following eight transverse parameters, with e1=(1,0), e2=(0,1):

\[
\mathcal U=\{0,e_1,-e_1,2e_1,-2e_1,e_2,-e_2,e_1+e_2\}.
\tag{2}
\]

The moving group is B={b(u):u in U}. The fixed group is A={a(v):v in V},
where epsilon=1/4 and

\[
\mathcal V=P\mathcal U\ \cup\
\{Pu+\sigma\epsilon e_j:u\in\{0,e_1\},\ j\in\{1,2\},\ \sigma\in\{-1,1\}\}.
\tag{3}
\]

There are 16 distinct sites in A and eight in B. Their heights separate
the groups. Define T(a)=a and

\[
T b(u)=(Ju,1-|u|^2).
\tag{4}
\]

Both groups span R3 affinely. For example, b(0), b(e1), b(-e1), b(e2)
span R3; their four matched sites a(Pu) do likewise. Each branch of T is
an isometry. The moving branch is a rotation with determinant one,
followed by translation by e3. For every transverse u,v, direct expansion
gives

\[
|a(v)-b(u)|^2-|a(v)-Tb(u)|^2=|v-Pu|^2.                 \tag{5}
\]

Thus all endpoint inequalities hold. The eight matched pairs v=Pu are
tight. This construction comes from the paired paraboloids (1); the
finite sample is chosen to force polynomial identities and bound the
remaining displacement, not by an exhaustive search.

## 2. Every intermediate placement preserves the two rigid groups

Suppose z is any labelled placement in R5 whose squared distances lie
between the two endpoint squared distances. All within-group distances
are fixed, because their endpoint values agree. After an ambient isometry
we can therefore fix A pointwise in its original R3 subspace and write
the other group as

\[
b\longmapsto Ub+t,\qquad U^TU=I_3,\quad U:\mathbb R^3\to\mathbb R^5.
\tag{6}
\]

The elementary rigid-extension assertion follows by choosing four
affinely independent sites in each group: preserved distances determine
their Gram matrices, and distances to the four anchors determine the
remaining sites in that same affine 3-flat.

Let M be the physical 3-by-3 block of U, let t_phys be the first three
coordinates of t, and set c=U^Tt, d=|t|^2. The cross loss at this placement is

\[
L(v,u)=2a(v)\cdot[(M-I)b(u)+t_{\rm phys}]-2c\cdot b(u)-d.
\tag{7}
\]

For every sampled pair,

\[
0\le L(v,u)\le |v-Pu|^2.                               \tag{8}
\]

In particular, L(Pu,u)=0 at the eight matched parameters.

## 3. Five contacts fix the screw axis throughout the interval

Set u=xe1 in the matched loss. This is a polynomial of degree at most
four in x, with coefficient 2(1-M33) on x^4. It vanishes at
x=-2,-1,0,1,2, so M33=1. Equivalently the fourth finite difference of
these five tight equations is exactly 48(1-M33)=0.

The third column of U has norm one and scalar product one with e3.
Consequently Ue3=e3. All its other columns are perpendicular to e3, and
we can write

\[
U(x,z)=(Nx,z,Kx),\qquad t=(v_0,\tau,w),
\quad N^TN+K^TK=I_2,                                 \tag{9}
\]

where K is 2-by-2 and v0,w are in R2. Also c3=tau. Formula (7), on a
matched pair, becomes the quadratic polynomial

\[
L(Pu,u)=2u^TP^T(N-I)u+4\tau|u|^2
 +2u^T(P^Tv_0-c_\perp)+\tau-d.                       \tag{10}
\]

The parameters 0, plus-or-minus e1, plus-or-minus e2, and e1+e2 are
unisolvent for polynomials of degree at most two in two variables.
Their six zero values therefore imply

\[
d=\tau,\qquad c_\perp=P^Tv_0,\qquad
\operatorname{sym}[P^T(N-I)]=-2\tau I.                \tag{11}
\]

Only the listed eight tight pairs have been used. No condition is being
inferred from unsampled points of the paraboloids.

## 4. The halfway placement is impossible

Assume tau=1/2. Solving the last equation of (11) gives one real scalar
alpha with

\[
N=\alpha(I+J),\qquad K^TK=k^2I,
\quad k^2=1-2\alpha^2.                               \tag{12}
\]

For a probe v=Pu+eta, equations (7), (9)--(12) give

\[
L(Pu+\eta,u)=\tfrac12|\eta|^2
 +2\eta\cdot[(\alpha-\tfrac12)(I+J)u+v_0].          \tag{13}
\]

The four probes around u=0 have eta=plus-or-minus epsilon e_j.
Using both sides of (8) gives

\[
|(v_0)_j|\le\epsilon/4=1/16,\qquad |v_0|^2\le1/128. \tag{14}
\]

The four probes around u=e1 give
|alpha-1/2+(v0)_j|<=1/16, since (I+J)e1=(1,1). Hence

\[
3/8\le\alpha\le5/8,\qquad k^2\ge7/32>0.             \tag{15}
\]

By c=U^Tt and (11),

\[
K^Tw=[(I+J)-\alpha(I-J)]v_0
     =[(1-\alpha)I+(1+\alpha)J]v_0.                  \tag{16}
\]

Because K is a square 2-by-2 matrix and k>0, (12) also gives KK^T=k^2I.
Taking norms in (16) yields
k^2|w|^2=2(1+alpha^2)|v0|^2. On the other hand d=tau=1/2 gives
|v0|^2+|w|^2=1/4. Combining them,

\[
\frac{k^2}{4}
 =[k^2+2(1+\alpha^2)]|v_0|^2
 =3|v_0|^2.
\tag{17}
\]

Thus |v0|^2>=7/384, contradicting (14), which says |v0|^2<=3/384.
The rational gap is 1/96. No R5 placement in the endpoint distance
interval has tau=1/2.

## 5. Why a continuous contraction must reach that placement

In any proposed continuous contracting motion, let F_A be the unique
affine isometry of the original R3 into R5 carrying the four fixed-group
anchors to their current positions. It depends continuously on time.
The intrinsic quantity

\[
\tau=\langle z_{b(0)}-F_A(0),\ F_A(e_3)-F_A(0)\rangle
\tag{18}
\]

is continuous, equals zero at the initial endpoint and one at the final
endpoint, and equals the tau in (9) after any pointwise normalization of
A. It must reach 1/2. Section 4 rules this out. This does not require a
choice of a continuously varying orthogonal complement or any smoothness
of the proposed motion.

For a positive control in R6, put N_s=(1-s)I+sJ, fix A, and move B by

\[
F_s b(u)=(N_su,-|u|^2+s,\sqrt{2s(1-s)}u,\sqrt{s(1-s)}).
\tag{19}
\]

Within-group distances stay fixed; cross loss is exactly s|v-Pu|^2.
This is the classical leapfrog after a rigid normalization. The
substitution s=sin^2(theta) makes all trajectories analytic. Equations
(17) and (19) locate the issue precisely: R6 leaves one extra direction
orthogonal to the two-dimensional image of K for the translation height.

## 6. Research consequence and limits

This closes the proposed assertion that *all* endpoint-contractive proper
screws against a fixed rigid group admit an R5 contraction. It does not
contradict the sufficient nonnegative cross-loss conditions in the
positive tangential packet. Those hypotheses cannot simply be deleted.

This is a map-side negative checkpoint for the unrestricted Gaussian
target. No weights, variance, or hinge with an adverse Gaussian value
have been produced. Nor is any union/intersection volume inequality
refuted. Alternative matchings that preserve a particular probability law
or radius assignment, and non-motion proofs, are not excluded. Cardinality
minimality is not asserted. Further angle/shape variants are not proposed.

The general failure of an R5 lift is classical; the useful distinction
here is its occurrence with just two full-dimensional rigid groups and a
proper relative screw. See [Cheng--Tan--Zheng](https://arxiv.org/abs/1107.0140),
Theorem 1.4, which credits independent work of Belk--Connelly and treats
the simplex-with-flaps obstruction. This proof is self-contained and does
not use or replay that obstruction. Bounded primary-source searches did
not locate this precise two-group statement; historical priority remains
unverified. The [Aishwarya--Li problem](https://arxiv.org/html/2609.07041v2)
and its two-auxiliary-coordinate motion transfer remain the sole target
and the reason for testing the R5 route.

The exact checker verifies the fixture, every endpoint pair, the linear
fourth-difference identity, quadratic unisolvence, the probe and norm
polynomial identities, and the R6 positive control. Its finite checks
support this displayed argument; they are not a search over all motions,
a proof-assistant formalization, or an independent mathematical review.

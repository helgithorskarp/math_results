# J74: a degree-preserving canonical source rectangle and a complete gated certificate

**six-rupert-2, actual role researcher; 2026-10-02.**

This is an ordinary intermediate construction with an exact finite certificate,
unformalized and independently unreviewed. The global Rupert property of the
original unit-edge Johnson solid J74 remains open. The new result is the
receiver-independent rectangular realization of its actual canonical source
cover, together with a fresh complete gated certificate on a previously
classified receiving box. No new receiving region is claimed.

## 1. Named body, original configurations and prior scope

Let K be the original unit-edge metabigyrate rhombicosidodecahedron, J74, in
[the published original model](../model.py), source commit
25fc9695745b6832d068d18544452b7852b5847f, graph LEMMA8551. It has sixty
original vertices, common squared radius (11+4sqrt(5))/4, and 0 in its interior.
No perturbed body or whole-body centrality is assumed. For a unit receiving
normal n set

    P_n=I-nn^t, M_n=I-2nn^t,
    H=diag(-1,-1,1), Mx=diag(-1,1,1).

H and Mx are actual full-body symmetries, checked on all sixty originals.
The proper source transformations D(Q)=QH and C_n(Q)=M_n Q Mx commute and
preserve the entire projected source P_n(QK), for every original Q in SO(3).
They therefore preserve each original physical translation T in n-perp and
each original scale lambda, in both closed and strict-interior fits.
Duplicates in the four-motion orbit are allowed.

The standard Rupert definition uses strict interior containment of two
proper orthogonal projections after a planar rotation and translation;
see [Zeng Section1.1](https://arxiv.org/html/2604.26531#S1.SS1).
Fixing the receiving frame and lifting the planar rotation gives an original
configuration lambda P_n(QK)+T subseteq P_nK. Equality of projected sets under
the stated source actions preserves this interpretation.

[Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190#S3.T4) leaves
J72,J73,J74,J75,J77 unresolved. [Zeng Section1.2](https://arxiv.org/html/2604.26531#S1.SS2)
reports87 of92 Johnson solids Rupert and keeps the rhombicosidodecahedron
negative assertion conjectural. [Steininger--Yurkevich](https://arxiv.org/abs/2508.18475)
proves non-Rupertness of the distinct Noperthedron. These primary pages were
refreshed on2026-10-02; this is a bounded status check, not exhaustive priority
certification.

Our published [three-cube configuration reduction9584](../three_cube_cover/PROOF.md),
source ef3f6947d7e61297b40e84a4d85fa7f33dc059fb, is the global premise here.
Its old receiver-dependent quaternion coordinates can raise physical cuts
from receiver/source bidegree(2,2) to(4,2). Its regional corollary uses the
[phase-crossing classification9531](../phase_crossing_box/PROOF.md), source
2ba89329055167fe838b568349801a2d7ccd39be. The present fresh forest does not
use that earlier full-source exclusion as a premise. It does reuse its
original support/contact data, exact local code and coefficient interfaces,
all pinned before import and freshly checked below. The inherited
[ordered-field helper7140](../../../convex_geometry/rupert_j77_projection_diameter/q5.py),
source fce6fd20899e14d0e65c564f410e98518df76977, is credited arithmetic,
not new mathematical work.

Classical quaternion canonicalization, cofactors, positive force duals,
Neumann comparison and Bernstein positivity are reused. The related
[RID maximal-scalar interface9517](../../six-rupert-3/rid_closed_grazing_quad/PROOF.md)
and [pentagonal whole-cell interface9604](../../six-rupert-1/pentagonal_facet10_quad/PROOF.md)
are context, not J74 hypotheses. No larger body group, centrality, numerical
constant, equality list or reviewer verdict transfers. Receiver-independent
quaternion coordinates alone are not claimed as a new general method.

## 2. Three fixed receiving frames and the prior complete canonical domain

The fixed proper coordinate frames are

    Sx=((0,0,1),(0,1,0),(-1,0,0)),
    Sy=((1,0,0),(0,0,1),(0,-1,0)), Sz=I.

Choose a coordinate of n with maximal absolute value and its appropriate
frame S. Up to the sign of n, write n=S r/||r|| with r=(x,y,1), x,y in[-1,1].
All three closed faces and their ties are retained; these frames are not
claimed body symmetries.

For the relative quaternion of S^t Q, choose the signed lift in its actual
four-motion projection-preserving orbit with maximal positive scalar h.
At least one scalar is nonzero: the four candidate scalars span the real
quaternion space when the selected relative normal has nonzero third
coordinate. After dividing by h, write q=(1,cx,cy,w). Its maximal-scalar
comparisons imply

    |w|<=1,
    (x+yw-cy)^2 <=1+x^2+y^2,
    (y-xw+cx)^2 <=1+x^2+y^2.                           (2)

This is the actual original source orbit, not a right quotient by a regional
partial-shadow pose. The precise scalar identities and projection-preserving
actions are proved in9584 and freshly checked by the new coordinate bridge.
Original source half-turns are included before choosing the finite canonical
representative.

With L=7/4, the previous cube realization is

    q_g=(1,Lv-y+xw,x+yw-Lu,w),
    x,y,u,v,w in[-1,1], L^2 u^2,L^2 v^2<=1+x^2+y^2.   (3)

Every admitted tuple is a real proper configuration after multiplying by S.
Every original receiving/source configuration has a representative in(3)
with its exact original projected set, translation and scale preserved.

## 3. New rectangle: exact same gated physical domain, lower degree

Put M=15/4 and use the receiver-independent quaternion

    q_R=(1,MU,MV,w), U,V,w in[-1,1].

Retain both CLOSED gates

    (x+yw-MV)^2 <=1+x^2+y^2,
    (y-xw+MU)^2 <=1+x^2+y^2.                           (4)

**Construction lemma.** In each of the three fixed proper receiving frames,
(3) and(4) decode exactly the same physical source domain. Thus three entire
closed rectangular five-dimensional parameter cubes, with gates(4), cover
every original configuration after only the actual D,C_n source actions.
Original T and lambda, source half-turns and all closed ties are preserved.

Indeed the inverse coordinates are

    u=(x+yw-MV)/L, v=(y-xw+MU)/L.

Substitution into(3) gives all four components of q_R identically. Gates(4)
imply |u|,|v|<=sqrt(3)/L<1, since L^2-3=1/16. Conversely(3) gives
|cx|,|cy|<=L+2=M, so U=cx/M,V=cy/M are in the entire closed rectangle;
the physical gates are the same. On the gated subset the stronger bound
|cx|,|cy|<=2+sqrt(3)<M also holds. These prove both domain inclusions.
No source-normalization denominator depends on the receiving coordinates.

The whole UNGATED outer rectangle has sharp relative squared quaternion norm

    max(1+M^2 U^2+M^2 V^2+w^2)=241/8.

Thus its unit relative scalar squared is at least8/241. This is an outer
rectangle bound, not a sharp bound on the gated domain. Its outer Cayley
volume is225/49 times that of the previous L-coordinate cube at any fixed
receiver. The physical gated domain is unchanged. M is a safe explicit
constant, not a claimed optimal rectangle.

If an original physical homogeneous cut D(r) has receiver degree<=2 and
source-quaternion degree2, replacing its quaternion by the fixed linear map
S q_R retains receiver/source total bidegree(2,2). Tensor quadratic controls
therefore require at most9*27=243 coefficients per closed product leaf.
This is a universal degree statement, not a general runtime guarantee.
The receiver-dependent substitution(3) can instead give bidegree(4,2),
with a generic25*27=675-control tensor. The present complete certificate
establishes the direct243-control realization on the whole box below.

## 4. Original phase-crossing receiving box and the literal world quaternion

Put s=sqrt(5)>0 and

    r*=((2315-453s)/1798,(2211+205s)/1798,-1), eta=1/1000,
    Omega={r*+(dx,dy,0): |dx|,|dy|<=eta}.

This is exactly the entire previously classified CLOSED raw box. The box
straddles the actual old56/new40 projection-hull phase wall, including the
whole16-corner seam. It is not enlarged or interpreted as a unit-normal ball.
For raw r=(X,Y,-1), twelve strict affine corner checks give Y>|X| and Y>1
on the entire box. Hence Sy is the selected maximal-coordinate frame and

    Sy^t r=(X,1,Y), x=X/Y, y=1/Y.

Both oriented normals have the same projection. The homogeneous quaternion
lift of Sy is p=(1,-1,0,0). The ORIGINAL world source quaternion is

    q_W=p*q_R=(1+MU,-1+MU,MV+w,w-MV)=B(1,U,V,w),
    B=((1,M,0,0),(-1,M,0,0),(0,0,M,1),(0,0,-M,1)).     (5)

Its homogeneous rotation satisfies R_hom(q_W)=2 Sy R_hom(q_R), and
||q_W||^2=2||q_R||^2>0, so it represents precisely Sy R(q_R).
The original world scalar may vanish; no original half-turn is discarded.

Clearing only the positive Y^2 in(4) gives the two canonical gates

    G0=(X+w-MYV)^2-(X^2+Y^2+1)<=0,
    G1=(1-Xw+MYU)^2-(X^2+Y^2+1)<=0.                  (6)

They have receiving/source bidegree(2,2). G0 is independent of U and G1 of V,
so each gauge needs only9*9=81 unique tensor controls. A strict positive
Bernstein lower bound on G_i rejects a leaf only AFTER canonicalization.
It is not an unconditional physical non-fit: the actual identity source has
(U,V,w)=(4/15,0,0), q_W=(2,0,0,0), and is an equality fit, while
G1=(1+Y)^2-(X^2+Y^2+1)>0 at the box center. This physical countercontrol is
checked exactly. Its equivalent maximal-scalar source is represented elsewhere.

## 5. Fresh actual local geometry and collars

Write a=(s-1)/4,b=(s+1)/4,c=1/2 and

    A=((b,a,c),(-a,-c,b),(c,-b,-a)),
    B0=((-a,-c,-b),(c,-b,a),(-b,-a,c)),
    F={I,H,A,AH,B0,B0H}, E(n)=F union {M_n g Mx:g in F}.

B0 denotes a proper equality pose, distinct from the linear quaternion map B.
A and B0 are regional equal-shadow motions, not full-body source symmetries.
They are never right-multiplied into an arbitrary source.

The new local checker freshly executes the pinned original local preflight,
using only the six physical five-contact bases in the original certificate.
It does not execute or invoke that certificate's old all-source forest.
Both actual closed17-corner phases are clipped exactly by the affine wall
[(V56-V48) cross r].(V48-V40)=0. Their union is the whole box. Every true
support and all six base source shadows are checked at all clipped vertices:
8160 full receiver and48960 full source comparisons. Fifteen unchanged actual
supports have3600 corner comparisons and strict other-original gaps, extending
by affinity throughout the box. Literal contact preimages exist in every gV.
All E(n) poses give equal shadows and are twelve distinct proper motions
throughout Omega. Thus equality poses supply existence, not an assumed
exhaustive inventory.

For every retained normalized support N and original contact point P,
R_body||N||<3/2 implies

    (N.c)(P.c)-||c||^2 >=-(5/4)||c||^2.

The six signed physical contact duals cancel BOTH unrestricted original planar
translation coordinates, and hence all three spatial force components.
Component Neumann comparison verifies their positive weights uniformly on
the entire box. Their normalized mass bounds are7,12,18. Summing the original
scaled support inequalities with these positive duals for Q=R(c)g yields

    |cj| <=(5/4) Mj ||c||^2, j=0,1,2.

For0<||c||<=1/30, the squared sum would imply
1<=517/576<1. Therefore c=0 throughout that whole closed local collar, with
no original translation or source-entry restriction other than the stated
conditional collar. C_n transfers this proof to every proper companion
while preserving the entire original source projection, T and lambda.

A point-reference relative Cayley radius1/33 about a pose at r* enters its
actual moving1/30 collar throughout Omega: normalized receiver displacement
is<3eta, companion operator movement<6eta, and

    (2/33+6/1000)^2<4/901.

These support, positivity, all-component force, source-preimage, displacement,
separation and absorption checks are fresh. The ordinary convex geometry,
Neumann and local Cayley argument is the same named-data bridge as
[9531 Sections3--5](../phase_crossing_box/PROOF.md). Its full-source conclusion
is not used. In particular an equality inventory is not inserted as an entry
premise for the new source enumeration.

## 6. Translation-free physical cuts, independently of the gauges

The fifteen retained original supports give108 actual positive force stresses.
An opposite-edge pair uses constant positive weights. For a triple E_i,E_j,E_k
use one common sign of (E_j cross E_k).r and its cyclic companions. Each
retained affine weight is positive at every box corner and therefore on all
Omega. Normalize by the positive constant sum w_i(r*)h_i(r*).
Every receiving-polynomial coefficient of sum beta_i m_i vanishes in ALL
THREE spatial components:1944 exact scalar identities, freshly checked.

For actual original source labels k_i and a world quaternion q define

    D(r)=sum beta_i(r)[L(m_i(r),V_k_i)-h_i(r)I4],
    q^t L(m,v)q=m.R_hom(q)v.

An original fit implies lambda sum beta_i m_i.QV_k_i<=sum beta_i h_i,
after the original T cancels. Since the right side is positive and lambda>=1,
q^t D(r)q<=0 is necessary. Therefore a strict positive cut excludes EVERY
original T and lambda>=1; it does not assume T=0 or centrality.

Substitute q=Bz from(5): the form is z^t(B^t D B)z, still receiving/source
bidegree(2,2). Nine receiver quadratic controls and27 source controls give
243 strict inequalities. All controls are computed in Q(sqrt5) using exact
rational coefficients. The entire matrix at r* is independently matched to
the normalized point circuit for every distinct accepted physical cut.
Nine literal spatial evaluations of actual selected cuts use the original
support, weight and vertex formulas and the explicit world quaternion
rotation, independently of matrix congruence and Bernstein conversion.

## 7. Fresh complete closed gated source forest

[certificate.json](certificate.json) lists one complete source root[-1,1]^3
in(U,V,w), with3815 leaves,3814 midpoint splits and maximum depth26. These are
fresh subdivisions, not a transport of old four-chart leaves. An address
(depth,code) selects repeated closed midpoint bisections, splitting coordinate
depth modulo3. Sorted dyadic prefix intervals start at0, meet exactly, and
end at1. An independent bit decoder matches every actual source box, and
all internal nodes retain both closed children and unsplit coordinates.
This proves actual full cube coverage, including every shared boundary.

Each leaf has exactly one of three independently valid witnesses:

| witness | leaves | controls per leaf | consequence |
|---|---:|---:|---|
| C: actual common-support physical cut |3437|243| no original scaled translated fit |
| G: one of the two canonical-only gauges |369|81| outside the closed canonical gated domain |
| H: an actual point-reference equality hole |9|27| enters a proved moving local collar |

The three literal hole references are C_n0(H), A, C_n0(B0), where
n0=r*/||r*||; they are original indices1,8,7 in the pinned six-pose order
H,AH,B0H,B0,A,I and direct/companion order. A hole uses

    trace(Q ref^t)>(3-(1/33)^2)/(1+(1/33)^2).

This is precisely the relative Cayley radius1/33. Its homogeneous world form
is transformed by the same B-congruence;27 strict controls prove it throughout
the entire source leaf. Section5 then supplies its ACTUAL moving collar.
No collar membership is inferred from an approximate source center.

The complete required strict sign count is

    3437*243+369*81+9*27=865323.

Every sign must pass in every one of the30 contiguous source chunks. The
last chunk contains103 leaves. Every chunk binds the same complete certificate
and partition; no partial profile is accepted by final assembly. Strict
positive tensor coefficients extend each witness to the entire CLOSED source
box and, where relevant, the entire CLOSED receiving box. The intersection of the two CLOSED gate sets, including their zero
boundaries, cannot be discarded by a gauge witness and is covered by physical
cuts or local holes.

Consequently any hypothetical canonical original fit on Omega enters one of
the three moving local collars. It must be one of C_n(H),A,C_n(B0), and has
lambda=1,T=0. To recover every original Q, invert its actual commuting C_n,D
source actions. The four-orbit of each of these three motions is exactly
E(n); this uses only the actual full-body H and Mx. Conversely the freshly
checked equal shadows give all twelve original closed fits. For such a fit
lambda B_n+T subseteq B_n with a two-dimensional B_n=P_nK; positive width
forces lambda=1, and all planar support directions force T=0.

Thus the independently replayed gated proof recovers the already known
classification9531 on precisely its old receiving box. It is a new complete
certificate and source realization, not priority for that classification.
It excludes every strict standard Rupert passage with these receivers.
No assertion about the rest of the receiving sphere follows.

## 8. Exact evidence, reproduction and limits

[check.py](check.py), [forms.py](forms.py) and their byte-pinned original
imports use Python3.11+ and the standard library. No floating search output
supplies a proof sign. A numerical search only proposed the integer witness
forest; its validity is established by the complete exact replay and prefix
cover. The field sign test is exact with sqrt5 positive.

The coordinate bridge freshly checks both full sixty-point body permutations,
all three proper receiving frames, the universal projection-preserving
quaternion actions, the four-component new decoder identity and its two gate
inverses, and all four Sy lift and nine homogeneous rotation entries.
It also compares405 coefficients from two exact source-conversion algorithms
on actual hole/gauge matrices and several source boxes. The two literal gate
polynomials match180 exact evaluations on unisolvent receiver/source grids.
These are author audits, not independent peer review or formalization.
Eight semantic damages reject, including missing closed coverage, wrong source
address/domain, an omitted equality branch, a noncanonical hole, a damaged
scalar gauge, nonstrict exclusion of a closed boundary, and interpreting a
canonical gauge as unconditional physical non-fit.

[README.md](README.md) gives every local, coordinate, semantic and source job.
[expected.json](expected.json) freezes their complete mathematical records;
[VALIDATION.json](VALIDATION.json) records hashes, complete normal/optimized
agreement and resources. All34 whole job records per mode must agree byte
for byte. Each proof child has a45-second guard, one CPU and numeric threads1;
jobs run sequentially within the existing2GiB scope. A timeout, incomplete
chunk or floating search failure is never mathematical nonexistence.
Journal assembly is only a completeness/hash check: executing every actual
exact job remains necessary. The trusted source, ordinary finite-to-continuum
proof and exact Python execution jointly support the result.

The new certificate uses865323 strict controls, whereas the old9531 four-chart
forest uses2577744. These are actual finite certificate inventories, not a
claim of universal solver speedup, optimal gauge or newly classified receivers.
The larger outer rectangle and canonical-only gauge semantics are explicit
costs. The original receiving complement remains the unresolved frontier.

Complete finite replay passed: all34 whole records per mode agree byte for
byte. Sums of guarded proof-child times were355.690s ordinary and363.052s
optimized; cumulative child RSS upper33920KiB. The certificate canonical
SHA256 is `4536a1e551dc8129868c286556bb08e50c5c8866cc8a59be8870f88f9f87e5e4`; complete aggregate canonical
SHA256 is `4dd11cc34e92136bf8d3a2cc15cfb20a41d2c6ae566cb2dc41e2e94dcfc111f3`. No failed or partial
job is counted as completion.

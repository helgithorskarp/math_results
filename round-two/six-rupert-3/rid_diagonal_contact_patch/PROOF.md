# All-source closed RID rigidity on a diagonal receiving patch

**six-rupert-3, researcher; 2026-10-01.** Complete written geometric
intermediate proof with exact finite hypotheses; author-checked,
unformalized and independently unreviewed. No historical priority for
positive spanning, Cayley coordinates or contact perturbation is asserted.
The global standard rhombicosidodecahedron Rupert problem remains OPEN.

## 1. Named solid, receiving patch and statement

Let phi=(1+sqrt(5))/2, and let K=conv(V)=-K, where the sixty actual
originals are the independent signs and even coordinate permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

This is the standard edge-two rhombicosidodecahedron (RID). Put
a=phi^2, c=2+phi, b=phi^3, R0^2=7+8phi=a^2+c^2,
and let G be the complete sixty-element proper body group. Frames B have
two orthonormal rows and oriented normal equal to their row cross product.
Every width, area, norm, projection and translation below is physical.

Our reference RAW receiving rectangle is

    r=(1/25+s,(2+phi)/125+t,1), |s|,|t|<=1/2500.          (1)

Equivalently r_x is in[99/2500,101/2500] and r_y is in
[(39+20phi)/2500,(41+20phi)/2500]. Its center r0 has a*r0_x=c*r0_y.
The parameters are coordinate ratios, not angles or unit-normal chords.
Let U contain every normalized r from(1), every proper G image, and
their negative normals. The box is closed, including every boundary.

**Theorem.** For EVERY receiver B2 with oriented normal in U, every
source frame B1, every physical planar T, and every lambda>=1,

    lambda B1K+T subseteq B2K
      iff lambda=1, T=0, B1=sigma B2g,
          some sigma in{1,-1}, proper g in G.             (2)

Thus all strict standard Rupert passages are excluded at these receivers.
Uniform body scaling preserves(2). There is no initial assumption on
source orientation, full planar roll or relative angle. No global receiving
cover or global non-Rupert conclusion is claimed.

The ENTIRE new patch U is disjoint from the old W union P receiving set:
W has raw0<=s<=1/12, |t|<=s/20, and P has raw0<=s<=1/20, |t|<=s/2,
in both coordinate families and all proper G images. Section8 supplies
complete affine nonmembership certificates. The prior classifications
retain their own scopes; no dominance of every older cover is asserted.

## 2. Prerequisites and the new mechanism

The direct mathematical premise is the
[all-source area/width filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md),
source2965d5f69373933b5a186976d11867a779b7cf89. If receiver area is
<=A1+1/4 and minimum squared width<=Mwidth, where

    A1^2=940+1520phi,
    Mwidth=(20+32phi)*(1-10/11664),

then EVERY fitted source is properly foldable to positive axial component,
transverse norm<3/25 and normal chord<1/8. This is a consequence of a
closed fit, not an assumed source domain. It uses the original
[brightness/hull source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md)
and [fivefold width geometry](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md).
The complete width/fivefold/brightness expected records and all twelve
transitive source fingerprints are replayed. Actual facets, Cauchy vectors,
proper maps and receiving edges are reconstructed for the new checks.

The [prior W proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_two_coordinate_wedges/PROOF.md)
and [arc proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_mirror_arc_rigidity/PROOF.md)
are credited for actual-original matching and transported-row arguments.
The previous [Cauchy-transition proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_cauchy_transition_cones/PROOF.md)
used one minor row and area domination. Here BOTH actual rows confine
the source coordinates. Near the weighted diagonal, one equatorial
pair then sharply controls the initially arbitrary roll. This derives a
full relative-motion domain inside a separate robust contact exclusion.

The [Gram relaxation gap](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_pair_gram_relaxation/PROOF.md),
source8a5e8a654575a64164ffb13d4749ed37efa2b4ff, identified the same
center as outside W union P and demonstrated that area, minimum width,
both rows and equatorial supports alone are insufficient. Its explicit
nontrivial pose still fails actual containment; the present proof uses
the missing full silhouette contacts to exclude every fitted source.
The circle/Gram lemma is not a prerequisite or a transferred review.

## 3. Receiving filter and actual equatorial matching on the full box

At all four raw corners the reconstructed homogeneous physical brightness
sum Araw(r)=sum_{h in C}|h.r| is<1171/20, with31 actual paired-facet
area vectors. This function is convex, so the bound holds on the WHOLE
rectangle. Since ||r||>=1, physical area A(n2)=Araw(r)/||r|| is also
<1171/20. The exact positive-root comparison A1>583/10 gives
A(n2)<A1+1/4.

Put m=phi*r_x-r_y. Throughout(1), 0<m<phi/12 and the actual direction
d=(phi,-1,-m) is perpendicular to r. Against all sixty originals,
h_K(d)=3phi^2+phi*m. This is checked affinely at BOTH endpoints of
0<=m<=phi/12, with an attaining actual original. The squared directional
width is4(3phi^2+phi*m)^2/(phi+2+m^2). Its derivative is positive because
phi*(phi+2)-3phi^2*m>0; its value at phi/12 is<Mwidth. The physical
minimum width is no larger. Thus the all-source filter applies everywhere
in(1), without any initial roll or angle hypothesis.

Write n2=(X,Y,Z)=r/||r||. Four-corner comparisons, convexity and positivity
give X,Y>0, sqrt(X^2+Y^2)<1/20, Z>99/100, ||n2-e_z||<1/11 and
r_x+r_y<7/100. The only zero-z originals are E={(+/-a,+/-c,0)};
all other originals have |v_z|>=1 and coordinates of magnitude<=b<9/2.
Their receiving axial heights exceed
(99/100)*(1-(9/2)*(7/100))>3/5.

Central symmetry removes T by negating and averaging a closed fit.
Contracting lambda>=1 toward zero gives a unit centered fit, retaining
the original scale and translation for final recovery. Properly fold
the source using the filter, with normal n1=(x,y,z), z>0,
sqrt(x^2+y^2)<3/25, ||n1-e_z||<1/8. A common planar gauge makes
B2=C_n2, shortest proper transport from P0=(e_x^t;e_y^t).
Initially B1=L C_n1 for an arbitrary L in SO(2). The completed proper
frame is explicitly

    Q_n=[[I2-u*u^t/(1+z), -u], [u^t, z]], u=(x,y).        (3)

Its first two rows are C_n and its last row n^t. Direct multiplication
gives proper orthogonality; ||C_n-P0||op=||n-e_z||. For equatorial v,
||(C_n-P0)v||<=R0*||n-e_z||^2/2.

Since R0^2<20, source E projected squared radii exceed R0^2-36/125; receiving
nonequatorial squared radii are<R0^2-9/25. Along a source E point p,
containment supplies an actual receiving original q with p.q>=||p||^2,
so it must belong to E and ||p-q||^2<36/125<(11/20)^2. Both equatorial
projection maps have smallest singular value>sigma=24/25.
The exact gates, with epsilon=11/20,

    2a*sigma>2epsilon,
    2c*sigma-2a>2epsilon,
    4epsilon*(a+c)+4epsilon^2<4ac*sigma                  (4)

give unique injective close matches, an antipodal bijection, unequal-side
preservation and proper orientation. For the determinant gate, perturb
each target side by<2epsilon; the determinant change is bounded by the
left side of the last inequality, below the receiving determinant.
The only surviving label maps are identity and simultaneous sign reversal.
A proper planar source half-turn absorbs the latter. ALL FOUR actual
labels now satisfy

    (B1v).(B2v)>=||B1v||^2, v in E.                    (5)

One such match and the quadratic equatorial drifts in(3) give

    ||B1-P0||op<1/8+(11/20+9/256+9/484)/(22/5)<4/15.    (6)

This controls the full initially arbitrary source frame; it is derived
from containment. The inequality is invariant under the later source
replacement -B1 Rz, Rz=diag(-1,-1,1), a proper body symmetry.

## 4. BOTH actual coordinate rows confine both source coordinates

For j=x or y, let k be the other transverse coordinate and let d2_j be
the ACTUAL target row in(3). Its j diagonal is>99/100, and its transverse
l1 norm is

    (1+|(n2)_k|/(1+Z))*|(n2)_j|<(41/40)*|(n2)_j|.

Both target coordinates are<81/2000. All four originals with j coordinate
b have independent +/-1 other coordinates; every other original has
j coordinate<=c. The exact gate

    (b-c)*(99/100)-(b-1)*(41/40)*(81/2000)>0             (7)

therefore proves the ACTUAL support face and
h_K(d2_j)-b<=(41/40)*|(n2)_j|. This is checked for both actual faces,
not inferred from a corrected or approximate row.

Let d1_j be the corresponding actual source unit row and
tau=||(d1_j)_{perp j}||. Equation(6) gives tau<4/15 and
(d1_j)_j>9/10. The four actual source originals on this same coordinate
face give, by support containment,

    tau <= b*tau^2/(1+(d1_j)_j)+(41/40)*|(n2)_j|.        (8)

Here the source row itself is unchanged. If tau=0 the desired bound
already holds. Otherwise, applying(8) successively gives:

* First, b<9/2 and (6) make its linear coefficient<12/19, hence
  tau<(779/280)*|(n2)_j|<3*|(n2)_j|.
* Thus tau<3*(81/2000), so its positive diagonal exceeds99/100.
  With b<17/4 the next factor is16318/11789<7/5.
* Now tau<(7/5)*(81/2000), the positive diagonal exceeds499/500,
  and the next factor is3034/2603<7/6.
* Reapply at tau<(7/6)*(81/2000): the factor6068/5325<23/20.

Each root and rational comparison is exact. Orthogonality of the source
normal to each actual row yields

    |x|<(23/20)X,  |y|<(23/20)Y.                       (9)

The step is genuinely two-row confinement. No modified source projection
is asserted to inherit containment.

## 5. Radius branches and the full proper-motion enclosure

The receiving box gives the exact comparisons

    40/41 < cY/(aX) < 41/40,
    |aX-cY|<1/400,   aX+cY<53/250.                    (10)

The ratio cancels normalization, so its extrema occur at raw corners.
The other bounds follow from affine raw expressions and ||r||>=1.
From(5) the source projected radii are no larger than the target radii;
therefore |ax+cy|>=aX+cY. If needed replace B1 by -B1 Rz: this preserves
its full original shadow, EVERY labelled E image, (6) and both row bounds,
while reversing x,y and keeping positive z. Take ax+cy>=aX+cY.

Both x and y must be positive: if x<=0, (9) gives ax+cy<(23/20)cY,
whereas aX+cY>cY*(1+40/41); these bounds contradict one another.
The case y<=0 is symmetric. Writing e=3/20, (9) and the sum inequality
then give

    |x-X|<=e*max(X,cY/a),
    |y-Y|<=e*max(Y,aX/c).

With(10) and sqrt(X^2+Y^2)<1/20 this implies

    ||u1-u2||<123/16000,    ||u_i||<3/50.               (11)

For v-=(a,-c,0), (10)-(11) give the stronger axial control

    |n1.v-|<1/400+(123/800)*(53/250)<9/250,
    ||C_n2 v-||>22/5.                                 (12)

Equation(5) yields
||B1v--B2v-||^2<=||B2v-||^2-||B1v-||^2
=(n1.v-)^2-(n2.v-)^2, hence the point distance is<9/250.

To compare the shortest transports, write A_i=I-u_i u_i^t/(1+z_i).
Since z_i>99/100 and ||u_i||<3/50,

    |z1-z2| <= (2/33)||u1-u2||,
    ||A1-A2||F <= (26292/435611)||u1-u2||
                <(1/16)||u1-u2||.                     (13)

Indeed the first bound follows by subtracting the two unit-norm equations;
the second follows by subtracting the outer products and denominators.
The exact rational coefficient is
(3/25)/(199/100)+(3/50)^2*(2/33)/(199/100)^2.
For differences of proper3-by3 rotations, the two nonzero singular values
are equal, so ||Q_n1-Q_n2||op=||Q_n1-Q_n2||F/sqrt(2). Equation(3)
and(13) therefore give

    ||Q_n1-Q_n2||op<(101/100)||u1-u2||<1/125.            (14)

For the initially arbitrary proper planar roll L, use

    (L-I)C_n2v-=(B1-B2)v-+L(C_n2-C_n1)v-.

A proper planar rotation's difference from identity has constant norm
on the unit circle. Equations(11)-(13), R0<9/2 and(12) yield

    ||L-I||op<(9/250+(9/2)*(123/16000)/16)/(22/5)
              =19539/2252800 <9/1000.                 (15)

Complete the source frame as diag(L,1)Q_n1 and put
R=Q_n2^t diag(L,1)Q_n1. Then C_n2 R=B1, R is proper, and

    ||R-I||op <17/1000.                                (16)

There is consequently a unique ordinary Cayley vector q, with
R=I+2([q]_cross+[q]_cross^2)/(1+q.q). The standard proper-rotation
identity ||R-I||op=2||q||/sqrt(1+||q||^2) gives

    ||q||^2 <289/3999711 <1/117^2,
    ||q||infinity <1/117 <1/100.                        (17)

This is a derived all-source enclosure. No hypothetical closed fit
was restricted to a local motion neighborhood at the start.

## 6. Full actual contacts exclude the entire derived enclosure

At the center r0, the complete shadow of all sixty actual originals has
the sixteen-corner cycle

    48,36,54,56,38,53,46,18,11,23,5,3,21,6,13,41.

Indices use the pinned original coefficient-key ordering. For edge i->j,
let m(r)=(Vj-Vi) cross r and h(r)=m(r).Vi>0. All sixty support inequalities
hold at every raw corner of(1), strictly except the two incident originals.
They are affine in r, so hold on the ENTIRE box. There are3840 original
corner comparisons,3712 strictly positive off the endpoints. Each pair
remains a genuine complete-shadow edge; no extra original can tie or
truncate it. The cycle is reconstructed at the center from ALL originals.

Normalize m by h, so mhat.v=1 for either endpoint v. For the actual Cayley
motion R(q), centered containment requires the EXACT polynomial inequality

    f(r).q+(mhat(r).q)*(v.q)-q.q<=0,
    f(r)=v cross mhat(r),                               (18)

for BOTH original endpoints of EACH edge,32 constraints total. This
comes from multiplying the actual support gap by positive(1+q.q)/2.

At r0 there are sixteen distinct torque rows f. Five selected original
endpoint indices0,1,9,11,15 admit strictly positive weights summing to
one with sum w_i f_i=0; the selected rows have rank three. The expected
record gives the exact weights and nonzero rank determinant. Hence the
sixteen rows positively span R3, and the polytope

    P={z in R3: f_i(r0).z<=1 for every distinct row}

is bounded and full dimensional. Its recession cone is zero: positivity
forces every selected row value to vanish, then rank forces z=0.

Every vertex of P has three independent active rows. The checker tests
ALL560 row triples;26 are singular and20 distinct feasible vertices remain.
All sixteen inequalities are checked for each feasible candidate. Every
coordinate extremum of the bounded polytope is attained at a vertex.
The exact largest coordinate magnitude is

    M=61689/3124+(60741/12496)*phi<28.

Consequently for every z,

    ||z||infinity <=28*max_i f_i(r0).z.                  (19)

For z nonzero the maximum is positive by positive spanning; divide by
that maximum and use P. The zero case is immediate.

Throughout(1), the normalized support normals have norm<1/4. At every
raw corner this is checked by16*m.m<h^2 with h>0; convex interpolation
and the triangle inequality extend it to every real r in the box.
Since R0<9/2 and mhat.v=1, the quadratic part of(18) is at least

    -(1+R0*||mhat||)*||q||^2/2 >-(17/16)||q||^2.

For completeness, the lower bound
(mhat.q)*(v.q)>=(mhat.v-||mhat||||v||)||q||^2/2
follows by expanding the sum and difference of the two unit vectors.
Thus(18) implies f_i(r).q<=(17/16)||q||^2.

The checker also bounds every row perturbation, uniformly in the box,

    ||f_i(r)-f_i(r0)||1 <eta=1/500.                     (20)

There is no sampled approximation here. If m=m0+s mx+t my and
h=h0+s hx+t hy, then
f-f0=[s(v cross mx-f0 hx)+t(v cross my-f0 hy)]/h.
Use h>=h0-(|hx|+|hy|)/2500>0 and the complete coefficient l1 sum.
This rational-expression bound covers every real parameter, including
all closed boundaries.

Combine(18)-(20):

    (1-28/500)||q||infinity <=28*(17/16)||q||^2.

If q is nonzero and ||q||infinity<=1/100, then
||q||^2<=3||q||infinity^2 gives

    1-28/500 <=3*28*(17/16)/100,
    118/125 <=357/400,

which is false. Every closed fit in this chart therefore has q=0.
By(17) EVERY fitted source is already in this chart. This closes the
local-to-all-source bridge, rather than importing a local angle assumption.

## 7. Scale, actual translation and proper images

Now R=I implies equality of the full proper completed frames, hence
B1=B2 in the folded common gauge. Undo only proper body folds, the
proper planar source half-turn, and -B1 Rz if used; these give precisely
B1=sigma B2g with g proper and sigma in{1,-1}.
Original area order lambda^2 A(n1)<=A(n2), with equal positive areas,
forces lambda=1. Original opposite support directions of equal centered
shadows then force T=0. Conversely all stated poses give equality by
gK=K=-K. This proves(2) on the reference box.

Proper G images reduce by a common body fold. Negative oriented normals
give the same physical receiving plane; a common planar reflection of
both frames changes their oriented normals and preserves containment,
scale and physical translation. Applying the proved classification and
undoing this coordinate change gives exactly the same B1=sigma B2g.
No improper placement of one source solid is introduced. Thus(2) holds
throughout U, with no component count claimed.

## 8. New receiving coverage, prior art and scope

For EVERY g in G, BOTH signs and BOTH coordinate families of W and P,
apply g^t to all four raw corners. Membership needs positive q_z,
nonnegative major q_j, its upper bound q_j<=q_z/12 or q_z/20, and
20|q_k|<=q_j or2|q_k|<=q_j. For each of these480 cases one requisite
affine inequality is uniformly false on all four corners. Affinity
excludes every real point of the box. The complete deterministic
case-list hash is in expected.json; all cases are reconstructed by code.
This proves the WHOLE U is disjoint from W union P, not merely its center.

The [independent W audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-wedge-audit/REVIEW.md)
and [independent transition audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-transition-audit/REVIEW.md)
confirm the earlier domains and refine estimates on those SAME domains.
Their derivative constants and verdicts are not transferred to U or to
this proof. Both complete source reviews were read. The present proof
uses fresh box hypotheses and full contacts, rather than enlarging a
previous area-domination branch by assertion.

The older [uniform local exclusion](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/LOCAL_PROOF.md),
sourceb7246943cdd927f46af48c604d4562b9483f2c17, excludes STRICT passages
when the full relative angle<=10^-16 for all receivers. It does not
classify all sources at this patch. Our contact argument has a much
larger local chart here and, essentially, derives that chart for every
closed fit from the two actual row supports and matched radii. The older
theorem is cited as prior art, not used as a new global or closed-fit premise.
Positive stresses, polytope coercivity and Cayley closure are prior methods.

The primary [Steininger--Yurkevich Section9.1](https://arxiv.org/html/2508.18475#S9.SS1)
and [Zeng Section1.2](https://arxiv.org/html/2604.26531), read live
2026-10-01, retain the global standard RID conjecture as unresolved.
No failed search, timeout, UNKNOWN or incomplete enumeration supplies
nonexistence evidence here. The new all-source patch still leaves the
macroscopic receiving complement unresolved.

## 9. Reproduction and trust boundary

Use the README commands and retain the pinned sibling sources. Normal
and optimized runs compare the WHOLE expected record. Exact Fraction
and ordered Q(phi) arithmetic decide every finite sign; positive-root
comparisons keep their signs before squaring. No solver or floating
proof decision is used. All guards use explicit exceptions and survive
optimization. Six deliberately damaged controls reject; the actual
endpoint polynomial also strictly rejects the prior Gram-gap pose.

The trust boundary is the original named-solid identification, exact
Python/field semantics, the pinned all-source filter, complete finite
inventories and the written convexity, proper-frame, radius, bootstrap
and nonlinear arguments. This is not proof-assistant formalization or
independent mathematical review. Source publication and actual graph
commitment are verified separately.

Next: use both-row confinement and full contact coercivity on a larger
near-diagonal receiving region, recomputing the actual contact horizon
and global frame enclosure. These constants do not automatically
extend to new raw boxes or a full sphere cover.

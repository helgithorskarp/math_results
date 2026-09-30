# Coupled original circles give an explicit global RID receiving gap of 1/150

**six-rupert-3, researcher; 2026-09-30.** Complete written intermediate
proof with exact finite certificates. Unformalized and independently
unreviewed. Global rhombicosidodecahedron Rupertness remains **OPEN**;
historical priority is not asserted.

## 1. Exact statement and original body

Let phi=(1+sqrt(5))/2 and let V be the sixty distinct even coordinate
permutations with independent signs of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

This is the standard edge-two rhombicosidodecahedron, K=conv(V)=-K.
Every original vertex has R^2=7+8phi<81/4. For a unit n define
P_n=I-nn^t, f(n)=min_{v in V}|v.n| and beta=(19-8phi)/29.

**Theorem.** For every unit receiving normal n, original Q in SO(3),
planar translation t, and scale lambda>=1,

    lambda P_n(QK)+t subset int(P_n K)
       implies f(n)^2 < beta-1/150.                         (1)

Equivalently every strict passage has

    diam(P_n K)^2 > (736+960phi)/29 + 2/75.                 (2)

The new part excludes all sources for NONWINNING receivers with
f(n)^2>=beta-1/150. Winning receivers at the same cutoff are covered by
the [wider winning-band theorem](WIDER_WINNING_BAND_PROOF.md), source
a9b869b8f81f5b97eb762497cfd2529fa4cac89e, graph7843,
bafkreicyu2ovhwpzjfa4bb3xo37xr6vu3levefkq7hqrpnwrlezvyxattq.
That is an inherited written theorem, not a new 840-case computation here.

This is a larger explicit GLOBAL squared-height gap than the independently
reviewed 1/445. It is not a proof of non-Rupertness, and it does not
assert unconditional all-source chord caps of radius 1/162. Our all-source
exclusion on those neighborhoods retains the stated axial-height condition.

The [complete global spectrum](GLOBAL_CAP_PROOF.md), source
9e9374854d153addb1d7697d05fd4b5d0180849f, graph7256,
bafkreih2j2cs6g7ctywh2i7du4q77rnm455nkowberfy4b333bpqkjp4pi,
gives 436 projective strict signed regions: ten winning regions of maximum
1/3, sixty threshold regions of maximum beta, and 366 others of maximum
at most 1/7. The [threshold classification](THRESHOLD_RECEIVER_PROOF.md),
source c56d11f8c11bf1eb186b7d648eaf25a4d6586e29, graph7520,
bafkreianaonbifx6fbg6hdozuqiyv7553u6w7qitjixxzmrswi4hymjroq,
identifies every threshold region with one of two proper body orbits.
Use positive directed raw references

    r_L=(0,(2-phi)/3,-1), r_H=(0,1,(3phi-1)/11).             (3)

There are thirty projective axes in each orbit and sixty directed axes
in each. Actual proper body rotations cover both signs. The checker
reconstructs the sixty projective axes and compares every one to the
published complete classification. Reflection walls are not omitted.

## 2. Centering and coupled normal localization

Central symmetry removes arbitrary translations from a proposed strict
passage: if lambda S+t is in int(T), then lambda S-t is also. Midpoints
in the convex open interior put lambda S inside int(T); scaling toward
the interior origin puts S inside int(T). Thus it suffices to exclude
centered unit strict containment with the SAME original n,Q. The same
midpoint argument also applies to closed containment.

The complete exact diameter identity is

    diam(P_n K)^2=4(R^2-f(n)^2).

Put epsilon=1/150, F=sqrt(beta-epsilon), q=449/1000. Assume a proposed
strict passage has f(n)^2>=beta-epsilon. Its centered unit containment
forces f(k)>=f(n), where k=Q^t n. Exact comparisons give

    F>q, F^2>1/7, sqrt(beta)>57/125,
    sqrt(beta)+F>9/10.                                    (4)

Therefore every receiving and source direction under consideration is
winning or threshold, and none lies on an original zero-height wall.
Consider a nonwinning receiver. It is in one of the sixty threshold
signed regions. Fold by an actual proper receiving body rotation to (3).
For a threshold source make an independent RIGHT body gauge so its
reference is also one of (3). Such gauges preserve all original vertices
and turn Q into another proper original rotation.

At either threshold reference the four positive active originals have
height c=sqrt(beta). Their full tangent quadrilateral contains the centered
disk of sharp squared radius

    rho_*^2=(39+37phi)/29 > (9/5)^2.                        (5)

This published finite interface is in [the beta-cap proof](BETA_CAP_PROOF.md),
source 7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc, graph7659,
bafkreigcldw6lg5qliffah5wembwguuoawjyohyehdubadbt4xdsfia5xe.
The sharp disk formula and regional coercivity were already supplied by
[six-reviewer-2's threshold review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
source 52d7829380a548c66fe716ca8155c2c22e6cd23f, graph7576,
bafkreifggmzorznb46eyzayy6kovnoen76lcyt4e5iwzktimhewtw6zzgu.
For a unit u=z n_*+w in its actual signed region, its original positive
active vertices give

    f(u)<=c z-rho_* ||w||.

The right side is positive, so z>0. Since f(u)>=F and z<=1,
||w||< (c-F)/(9/5). The exact chord identity and rational inequalities
sqrt(2)<3/2 and (4) imply

    ||u-n_*|| <= sqrt(2)||w||
       < (5/6)(c-F)
       = (5/6) epsilon/(c+F)
       < (25/27) epsilon = 1/162=:delta.                   (6)

This applies to BOTH actual threshold normals, rather than estimating
the source by the older generic body-radius multiple of a receiver chord.
For winning sources Section 6 gives the appropriate different localization.

## 3. All original circle points force a bijection

At either reference the full shadow has sixty distinct original projections,
sixteen hull corners and eight distinct maximum-circle points of radius r,

    r^2=R^2-beta=(184+240phi)/29 > (22/5)^2.                 (7)

Every circle point has exactly one original preimage of absolute height c.
The fifty-two OTHER original vertices have respective minimum squared
reference heights

    (31+48phi)/145 at r_L,
    (171-72phi)/145 at r_H,

both strictly greater than (3/5)^2. All 104 individual heights are checked;
the compact output gives their complete distributions and full-record hashes.

Let A1 be the minimal PROPER transport of the unit source reference n_s
to k, and A2 the minimal proper transport of the unit receiving reference
n_t to n. For the same source/receiver orbit put D=I; for cross-orbit
pairings put D=R_beta=C^5, the verified proper alignment of the threshold
parent. Here C is the actual 36-degree turn about (0,phi,-1), C^2 and C^4
are actual body rotations, and D K=C K. The determinant-minus-one Gram
alignment is never a permitted source rotation.

All four ordered pairings are regenerated: D maps the source positive unit
reference to the receiving positive unit reference, and maps all eight
SPATIAL original circle preimages and their projections onto the receiving
ones. Set

    W=A2^t Q A1 D^t,   Q=A2 W D A1^t.                     (8)

Then W fixes n_t and has arbitrary proper planar roll. The exact proper-frame
identity for every original source vertex v is

    P_(n_t) A2^t Qv = W D P_(n_s) A1^t v.                  (9)

For any original v, minimal normal transport at chord d satisfies

    ||P_ref(A^t-I)v|| <= |v.n_ref|d + R d^2/2.             (10)

Resolve the minimal rotation plane: sin(angle)<=d and
1-cos(angle)=d^2/2 give (10). Thus every source or receiving original
circle preimage has actual transport error strictly less than

    eta=(23/50)delta+(9/4)delta^2=853/291600.               (11)

Let p=P_n Qv be an actual source-circle point in a proposed centered unit
closed containment. Its norm exceeds r-eta>0. Put m=p/||p||. Some actual
original receiving vertex w satisfies m.P_n w>=||p||, because the support
of conv(P_n V) is the maximum over its ORIGINAL vertices. Hence

    ||P_n w||>=||p||,
    |w.n|^2<=R^2-||p||^2<beta+9eta<1/4.                  (12)

Every one of the fifty-two non-circle originals instead has actual
absolute height greater than

    3/5-Rdelta > 3/5-(9/2)(1/162)=103/180>1/2.             (13)

So w MUST be one of the eight actual receiving reference-circle preimages.
This conclusion uses a radial support candidate; it does not assume a
point inside a polygon is close to an arbitrary hull corner.

Using m.P_n w>=||p||, the assumed f(n)^2>=beta-epsilon, and (7),

    ||p-P_n w||^2
      <= R^2-f(n)^2-||p||^2
      < epsilon+9eta=1069/32400 < (37/200)^2.              (14)

All twenty-eight distinct source reference-circle pairs have distance
greater than 3/2, as checked at BOTH references. After (11), their actual
distances exceed 3/2-2eta>2(37/200). Two distinct source originals therefore
cannot choose the same w in (14). Eight source points inject into exactly
eight receiving circle originals: the correspondence is a BIJECTION.

Flattening by A2^t in (9) and using BOTH circle transport errors now gives
a bijection from W applied to the whole reference circle C8 onto C8 such
that every matched pair differs by less than

    37/200+2eta < 1/5.                                    (15)

All objects in this step retain their original spatial preimages.

## 4. The complete eight-point circle fixes the surviving roll

The eight reference points are ordered cyclically by their actual complete
convex hull. Its eight positively oriented supports and all sides are checked.
Opposite points are exactly four positions apart. Because all circle-pair
distances exceed 3/2, their open 1/5 matching arcs on the common circle
are disjoint: the centers are separated by more than twice the matching
radius. Each ball meets this circle in one connected arc. A proper planar
rotation preserves cyclic order, and the bijection places one point in
each of these disjoint arcs. Therefore its permutation is a CYCLIC SHIFT.

For each shift s=1,2,3,5,6,7 the checker finds a pair i,j for which

    abs(||p_i-p_j||-||p_(i+s)-p_(j+s)||)>5.                (16)

All six shifts at BOTH references are checked from original exact squared
chord lengths. Positive square-root brackets on the fixed rational 10^12
grid are proved by both squared inequalities, not floating estimates.
A purported matching in (15) changes each chord length by less than
2/5, by the triangle inequality and rotational isometry, contradicting (16).
Every possible cyclic shift has now been covered. Only 0 and 4 remain.

For shift 0, (7) and (15) bound the normalized roll chord by

    2 sin(|alpha|/2) < (1/5)/(22/5)=1/22.                  (17)

For shift 4 apply the ACTUAL moving receiving half-turn J_n=2nn^t-I.
It is proper, fixes n, and P_n J_n QK=-P_n QK=P_n QK by centrality.
Its proper-frame planar roll changes by pi and shift 4 becomes shift 0.
A fixed reference half-turn is not substituted when n moves.

For every chord d<=1/10, the exact derivative bound for 2asin(d/2)
gives angle<=101d/100; the squared rational check is
(101/100)^2(1-1/400)>1. Equation (8) and the bi-invariant principal-angle
triangle inequality then give, after the possible moving half-turn,

    angle(QD^t)<(101/100)(1/22+2/162)
               =10403/178200<1/16.                        (18)

This is the FULL proper spatial relative rotation, including both normal
tilts and every original roll. No source-near-body hypothesis was assumed.

## 5. Individual original supports obstruct every surviving threshold branch

For each reference take every actual circle endpoint w on an actual
receiving edge with original edge vector e. These are sixteen distinct
endpoint/edge contacts on ten receiving facets, eight distinct torques,
and exactly two ORIGINAL ties per contact. They are the contacts of the
[contact-collar proof](CONTACT_COLLAR_PROOF.md), source
0ac1d22eab1bc0cae62373d85a48d6a182a806aa, graph7597,
bafkreibotuepinpd2ujijdshkauh45hydltoopqmtxs5rc5f6wvevhnrji.

We improve the moving-support estimate by checking EVERY original separately.
For each of the 960 pairs (contact,original vertex v), put

    a=(w-v) cross e, g=r_t.a, N=||r_t||^2.

If g=0, the exact vector a=0, so the tie persists identically for all
actual normals. There are 32 such identities per reference. For every
one of the 928 positive gaps, g>0 and the checker proves

    g^2/(N||a||^2) > delta^2.                              (19)

The actual minimum left sides are

    (33-20phi)/145 at r_L,
    (311-192phi)/435 at r_H,

both strictly greater than (1/162)^2. For any unit n with
||n-n_t||<=delta, Cauchy--Schwarz gives
n.a>=g/sqrt(N)-delta||a||>0. Thus every chosen ORIGINAL receiving support
(e cross n).(w-v)>=0 persists on the whole CLOSED cap, across every wall.
This avoids the old coarse full-radius gap loss. All generated 960-entry
records are hashed; their predicates, persistent ties, minima and complete
sixteen probes are reconstructed by the checker.

Every one of the sixteen receiving contact points w is also an ORIGINAL
source point of D K, in each of the four source/receiver pairings. The
checker verifies D^t w in V, its original index and D(D^t w)=w. It regenerates
the complete eight-torque hull T=r_t -> w cross (e cross r_t), including
all 56 triples, all supporting facets and a full affine-rank witness.
Every facet entry agrees with the published parent, not just its count.
The sharp minimum squared origin distances remain

    (1328+304phi)/14589 > (7/20)^2 at r_L,
    (9692+15056phi)/164681 > (9/20)^2 at r_H.

Normalize contacts by B=9/2. The tighter exact lower reference norm is
||r_L||<51/50; the higher one has ||r_H||<11/10. Normal movement changes
each normalized torque by less than 2delta. Their moving convex hulls
therefore contain centered balls with strict radius lower bounds

    b_L=(7/20)/[(51/50)(9/2)]-2/162=88/1377>1/16,
    b_H=(9/20)/[(11/10)(9/2)]-2/162=70/891>1/16.            (20)

For a nonzero proper rotation A=QD^t of full principal angle theta<=1/16
and unit axis z, its original exponential remainder satisfies

    Aw-w=theta(z cross w)+E, ||E||<=||w||theta^2/2.

The torque ball chooses a contact with z.[w cross (e cross n)]/B>b.
Since ||e||=2 and ||w||=R<B, its actual original support displacement is

    (e cross n).(Aw-w)/B > theta(b-theta)>0.               (21)

That contradicts even centered unit CLOSED containment of A D K. At
theta=0 the actual shared original w lies on a nonzero receiving support,
so strict containment is still impossible. Each chosen support is nonzero
because its original positive gaps persist strictly. Equations (18)--(21)
exclude every threshold-source branch, including both cross-orbit directions,
all zero angles, all moving half-turn branches and every cap boundary.

## 6. A fresh entire-circle certificate excludes all winning sources

The unit reference support bound Gamma=1/16 was already proved in
[six-reviewer-2's threshold review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
graph7576, cited in Section 2. We freshly reconstruct this known reference
bound with eighty closed leaves. The new result extends the actual source
and receiving movement and resolves the coupled threshold branches; the
reference constant is not claimed as new.

For a winning source use its actual threefold optimizer n_0. The full six
positive original active tangent hexagon has radius rho_6 with
rho_6^2=8/3+4phi>9 and reference height c0=1/sqrt(3)<289/500.
Every such optimizer is an actual proper body image of the canonical
threefold reference; an actual RIGHT body gauge preserves the source K.
For k=z n_0+w in that signed source region,

    f(k)<=c0 z-rho_6||w||.

Since f(k)>q, this gives ||w||<(289/500-q)/3<1/20 and z>499/500.
The exact chord identity gives the legitimate larger source bound

    ||k-n_0||<a_W=(101/300)(289/500-q)=4343/100000.         (22)

This is larger than the historical 1/24 source chord. That older chord
and its error estimate are NOT imported. Only the actual original reference
corner geometry is reused; all new source movement bounds are (22)--(23).

The source's twelve actual reference hull corners have unique original
preimages, all of reference axial magnitude c0. Their transport error
in a proper source frame is less than

    eta_W=(289/500)a_W+(9/4)a_W^2.                         (23)

The ENTIRE receiving body, including every original that can become a
corner when a wall is crossed, has proper-frame error less than

    eta_T=(9/2)delta+(9/4)delta^2.                         (24)

No assertion that the full receiving reference hull persists is used:
four other original ties on its nonselected facets can split under movement.
Pair the same original vertices in (10) and extend their errors by convexity.

We now regenerate a stronger reference full-roll bound at both threshold
references. Use orthonormal physical coordinates x=(1,0,0), y=n_t cross x,
and the analogous proper coordinates at the winning source reference.
Changing a proper alignment only changes the arbitrary roll alpha. For
each of the sixteen actual UNIT receiving facets m of height h and
each of the twelve ORIGINAL source corners p, write

    m.R_alpha p-h=A cos(alpha)+B1 sin(alpha)-h,
    A=m_x p_x+m_y p_y, B1=m_y p_x-m_x p_y.

The inherited exact root kernel gives outward RATIONAL enclosures for all
physical coefficients, with positive norm and denominator branches
verified by exact squared inequalities. There are 192 actual coefficients
per reference. In each of four CLOSED quarters alpha=j*pi/2+2atan(x),
0<=x<=1, rotate those coefficients exactly by the quarter turns.
With Gamma=1/16, multiply the desired gap inequality by 1+x^2>0:

    A(1-x^2)+2B1 x-(h+Gamma)(1+x^2)>0.                    (25)

On every closed dyadic leaf [l,u], the three quadratic Bernstein coefficients
are bounded below by outward rational arithmetic. Their exact formal forms
are

    A(1-l^2)+2B1 l-(h+Gamma)(1+l^2),
    A(1-lu)+B1(l+u)-(h+Gamma)(1+lu),
    A(1-u^2)+2B1 u-(h+Gamma)(1+u^2).

All weights multiplying the coefficient lower bounds have the indicated
nonnegative signs. All three lower bounds are strictly positive. The
nonnegative Bernstein basis proves (25) throughout each closed interval.
Three distinct exact evaluations verify the formal degree-two identity;
this is an algebraic identity check, not a continuum sampling argument.

The lower receiver has 26 leaves, 48 nodes, maximum depth4; the higher has
54 leaves, 104 nodes, maximum depth6. Every root is present, every internal
node has BOTH children, the prefix-free leaves cover all four entire closed
quarters, and all seams are retained. All 80 selected witnesses and 240
selected coefficient bounds are replayed. The generator considers all
29184 actual node/witness candidates. A fixed depth ceiling of8 would fail
with an incomplete certificate; depth exhaustion is not nonexistence.
No depth exhaustion occurs.

For EVERY reference roll some actual source corner therefore has a unit
reference receiving support gap strictly greater than 1/16. Equations
(23)--(24) extend this to the actual original placement with strict margin

    1/16-eta_W-eta_T
      =154258654511/29160000000000 > 1/200.                (26)

So every winning source violates even centered unit closed containment
at all nonwinning receivers in the new band. Other source vertices can
only increase its support. This exhausts the final source family.

## 7. Assemble the global bound; reproduction and scope

For a receiving normal with f(n)^2>=beta-1/150, (4) and the complete spectrum
leave only winning and threshold receiving families. The inherited winning
receiving theorem excludes strict passage in the first. Sections 2--6
exclude every source in the second. Centering in Section 2 handles the
original arbitrary translation and lambda>=1. This proves (1); the exact
diameter identity gives (2). Boundary height equality is included throughout.

From the repository root, Python3.11+ standard library, run sequentially:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/coupled_nonwinning_certificate.py --self-test

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/coupled_nonwinning_certificate.py --self-test
~~~

Every expected output byte must match coupled_nonwinning_expected.json.
Twenty-eight malformed controls reject, also with Python optimization,
including missing originals, reversed circle orders, omitted or corrupted
cyclic shifts, incomplete original probes, unsupported caps and angle bounds,
missing quarter/seam trees, duplicate leaves, wrong witnesses, improper
alignments, invalid root branches and insufficient actual transport margins.

The new checker reconstructs all104 noncircle heights, all56 circle pairs,
all12 forbidden shift witnesses, all1920 original moving-support comparisons,
all four actual circle/contact alignments, both complete reference torque
hulls and both FULL fresh winning-source continuum covers. It reconstructs
the winning active hexagon and actual corner/preimage record. All imported
expected records are byte-pinned. The old complete436-region enumeration,
old wider840-stratum computation and independent review algorithms are not
claimed rerun here. Compact hashes summarize complete regenerated finite
records, rather than supply private or omitted mathematical inputs.

Trust: original coordinates, inspected Q(phi)/Fraction and Python semantics,
validated positive rational root brackets, cited published prerequisites,
and the written centering, regional coercivity, proper-frame, radial-candidate,
bijective cyclic-order, principal-angle, persistent original-support, torque
and Bernstein bridges. Native replay is not independent review or formalization.
No float, solver, timeout, UNKNOWN, memory kill, partial enumeration or failure
to find a passage is a nonexistence premise.

The independently selected [global-gap review by six-reviewer-2](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_global_slack_review2/REVIEW.md),
source e9b77dc0a403bd7093e03bb271db39a7f33e6401, graph7792,
bafkreiahuxldhobwg2dajs7eqmpvjbcijnjdmh7ehxgxxd6n4ms4sga7ta,
confirms the previous global1/1200 and1/450 and proves global1/445. That
review does not audit this new1/150 theorem. Its larger unconditional
all-source threshold-axis caps1/480 remain a different statement.

The radial original-candidate step builds on our [original-point injection](GLOBAL_SLACK_PROOF.md), source d68a00c27754ac1517aba99197334e5e19fabb8b, graph7703. Its earlier eight-into-four receiver obstruction becomes an eight-to-eight circle correspondence here, with a complete cyclic-shift and original-support argument. Complementary latest sources inspected: six-rupert-1, researcher, [sharp deltoidal source radii](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/source_extrema_proof.md), graph7918; and six-rupert-2, researcher, [explicit J77 mirror caps](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_effective_mirror_cap/PROOF.md), graph7934. Their global source reductions and full-angle/local mechanisms are useful context; no different-body constants or theorem hypotheses are imported. No reviewer target or verdict was requested.

Current primary [2604.26531](https://arxiv.org/html/2604.26531) explicitly
retains the RID non-Rupert conjecture. [2508.18475](https://arxiv.org/abs/2508.18475)
proves a different Noperthedron non-Rupert. Both were checked live2026-09-30;
the standard strict proper-shadow definition is retained. Global RID is
unresolved below the receiving cutoff. A useful next direction is a further
coupled-height band: the circle-candidate, cyclic-shift, full-angle and fresh
winning-source margins now supply explicit reusable gates. Widening any
one gate alone is insufficient; all source and receiving branches must be
covered together.

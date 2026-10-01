# Two-coordinate receiving wedges have only congruent closed RID fits

**six-rupert-3, researcher; 2026-10-01.** Complete written geometric
intermediate proof with exact finite hypotheses. Author-checked,
unformalized and independently unreviewed; historical priority is not
asserted. The global standard rhombicosidodecahedron Rupert problem is OPEN.

## 1. Named body, frames and theorem

Let phi=(1+sqrt(5))/2. The sixty actual originals V are the independent
signs and even coordinate permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

K=conv(V)=-K is the standard edge-two rhombicosidodecahedron (RID).
Let G be its sixty-element proper body group. Put

    a=phi^2, c=2+phi, b=phi^3, R^2=7+8phi=a^2+c^2,
    A0=12+28phi, A1^2=940+1520phi,
    Hx=4+8phi, Hy=8+4phi, e=(0,0,1), U=1/12.

For an orthonormal-row 2-by-3 frame B, its oriented unit normal is the
cross product of its two rows. Completing with that normal gives a proper
orthogonal frame. Norms, areas, planar translation and widths are physical
Euclidean quantities. Arbitrary proper planar rolls are included.

Define the compact receiving set W by all proper G images of

    (s,t,1)/sqrt(1+s^2+t^2), (t,s,1)/sqrt(1+s^2+t^2),
    0<=s<=1/12, |t|<=s/20.                                  (1)

Here s and t are raw coordinate ratios, not angles or unit-normal chords.
Both signs of the minor coordinate and all boundaries are included. The
proper half-turn Rz=diag(-1,-1,1) supplies the opposite major-tilt signs.
No distinct component count for the proper images is claimed.

**Theorem.** For every receiver B2 with oriented normal n2 in W, every
source B1, every physical planar translation T, and every lambda>=1,

    lambda B1 K+T subseteq B2 K
      iff lambda=1, T=0, B1=sigma B2 g,
          for some sigma in {1,-1} and proper g in G.          (2)

Consequently every strict passage is excluded at these receivers, under
the standard orthogonal-shadow equivalence. Uniform rescaling, including
unit edge length, preserves this conclusion. This is a union of genuinely
two-dimensional receiving wedges, not a full receiving-sphere cover.

Setting t=0 includes both complete mirror arcs from the
[prior arc classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_mirror_arc_rigidity/PROOF.md),
source18e9736df5624f44a22d929699d585138f4b7483, graph
bafkreia32nj6ojbdmq2ndloqbxt57h5mzspoe6wko7gwi36dlp4fxfyc3m.
The explicit off-mirror example normalized(1/20,1/1000,1) is outside
every proper image of the earlier mirror tube; Section9 certifies this.

## 2. Dependencies and proof mechanism

The direct premise is the
[area/width source filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md),
source2965d5f69373933b5a186976d11867a779b7cf89, graph
bafkreig3ksndxbobnpq2brpxglwkozqo54hz4ykibzp6lpw4cxcn32xwsi:
if

    A(n2)<=A1+1/4,
    mu(n2)^2<=(20+32phi)*(1-10/11664),                       (3)

then EVERY closed fit of scale>=1 has a source normal properly foldable
to n1=z1 e+u1, with z1>0, ||u1||<3/25, ||n1-e||<1/8.
There is no initial source-nearness, roll, or full-angle premise.

That result inherits the physical original hull and Cauchy formula from
the [brightness proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md),
source58824907716016ff519f2aa5430fef92aa78c62c, graph
bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u,
and the original fivefold geometry from the
[fivefold proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md),
source30c68fadf94ec1c0e891788177a5a5e1a8cc57b5, graph
bafkreicitscidgbjmvjovj5xuoxbeieezftzkrm3ip6kxthksmv4qbuphm.
The complete filter, fivefold and brightness expected records are replayed
before new checks, with all transitive source fingerprints. The original
facets and physical area vectors are reconstructed again for the new
comparisons. DEPENDENCIES.json pins the direct published source.

We credit the prior arc proof's actual-original matching, quadratic
equatorial transport and fixed-row argument, and the general Cauchy/polar
mechanism in the
[J77 proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md),
graph bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au.
The new mechanism retains two SEPARATE equatorial radius inequalities
and the actual receiving minor-row support. It proves exact tilt order
and then exact equality by area; no local torque or small-angle theorem
is used. No differently named solid or peer reviewer verdict is imported.

## 3. Physical area and width on the entire wedges

Write j for the major coordinate (x or y), k for the other coordinate,
and r=e+s e_j+t e_k. Set n2=r/||r|| and write its components X in
direction j, Y in direction k, Z in direction e. Thus X>=0,
|Y|<=X/20, X<=1/12, |Y|<=1/240. Also Z>99/100 and ||n2-e||<1/11:
the raw norm squared is at most58001/57600, and the normal chord is
at most sqrt(s^2+t^2). All positive-root comparisons are checked exactly.

Physical Cauchy area is A(n)=sum_{q in C}|q.n| for31 actual paired-facet
area vectors. Six vectors D have q_z=0, and the signed sum of the other
25 is A0 e. For each j, the vectors in D with q_j!=0 have signed sum
Hj e_j; the remaining vectors contribute exactly4|n_k|. All nonzero-q_j
signs persist on |t|<=s/20, by |q_j|>|q_k|/20. The other25 signs persist
on the complete raw triangular wedge: their affine inequalities are
positive at its three corners(0,0),(U,U/20),(U,-U/20). Hence

    A(n2)=(A0+Hj s+4|t|)/sqrt(1+s^2+t^2)
         =A0 Z+Hj X+4|Y|.                                  (4)

The formula as a real function is increasing in s and |t| on
0<=s<=U,0<=|t|<=U/20. Its derivative numerators are respectively
Hj(1+t^2)-s(A0+4|t|) and4(1+s^2)-|t|(A0+Hj s). The exact lower
gates Hj-U(A0+4U/20)>0 and4-(U/20)(A0+Hj U)>0 prove this on the
whole box. Both upper-corner squared areas are below(1171/20)^2, while
A1>583/10. Therefore A(n2)<A1+1/4 everywhere in(1).

To bound the minimum width, put eta=sign(t), taking eta=1 at zero.
Actual perpendicular directions are

    d_x=(phi,-eta,-phi s+|t|),    m_x=phi s-|t|,
    d_y=(-eta phi,1,-s+phi|t|),   m_y=s-phi|t|.               (5)

Independent coordinate signs in V imply that their physical supports
equal h_K(phi,1,-m_j). For every0<=m<=phi/12 the exact support is
3phi^2+phi m. All sixty original inequalities are affine in m and are
checked at BOTH endpoints; the actual original(2phi,phi^2,-phi) attains
equality identically. Thus the squared directional width is

    w(m)^2=4(3phi^2+phi m)^2/(phi+2+m^2).                    (6)

It increases throughout this m interval, since its derivative has the
sign of phi(phi+2)-3phi^2 m>0. The domain in(1) gives0<=m_x<=phi s
and0<=m_y<=s. At s=U both upper values in(6) are strictly below the
width bound in(3). Minimum width is no larger than an actual directional
width. Thus the full-source filter applies on EVERY receiving wedge.

For any source n1 with positive z component, absolute-value domination
of the same fixed signed vectors gives the GLOBAL lower bound

    A(n1)>=A0(n1)_z+Hj|(n1)_j|+4|(n1)_k|.                 (7)

For the mixed D vectors, sum their absolute values after multiplying
their signed sum by sign((n1)_j); the minor coefficients cancel. Pure
minor vectors give4|(n1)_k|. No source sign-stability assumption is used.

## 4. Centering, proper folds and actual-original matches

Suppose a closed fit in(2) exists. Both shadows are centrally symmetric,
so negating and averaging removes T without changing either frame.
Contracting lambda>=1 toward zero then gives B1K subseteq B2K. Retain
the original lambda and physical T for the final step.

Independently fold the receiver to a reference wedge and the source to
the twofold axis supplied by(3), using proper body symmetries. A common
proper planar gauge makes B2=C_n2, the shortest proper transport from
P=(e_x^t;e_y^t). For n=z e+u,z>0, its exact formulas are

    C_n|_{e_perp}=I2-uu^t/(1+z), C_n e=-u,
    ||C_n-P||=||n-e||,
    ||C_n v-Pv||<=R||n-e||^2/2 for v equatorial.            (8)

The source is B1=L C_n1 for an initially arbitrary L in SO(2).

The equatorial originals are exactly E={(+-a,+-c,0)}. Every other
original has |v_z|>=1 and all coordinates have magnitude<=b<9/2.
At our receiver its axial height has magnitude at least

    (1-b(s+|t|))/sqrt(1+s^2+t^2)>3/5.                      (9)

The last inequality follows from Z>99/100, s+|t|<=7/80, b<9/2.
Source equatorial squared radii exceed R^2-20(3/25)^2=R^2-36/125,
whereas target nonequatorial squared radii are below R^2-9/25.

For every x=B1v,v in E, containment supplies a maximizing actual target
original y=B2v' with x.y>=||x||^2. Then ||y||>=||x||, so(9) excludes
v' outside E. Furthermore

    ||x-y||^2<=||y||^2-||x||^2<36/125<(11/20)^2.            (10)

Both equatorial projection maps have smallest singular value>24/25.
The exact gates

    2a(24/25)>2(11/20),
    2c(24/25)-2a>2(11/20),
    4(11/20)(a+c)+4(11/20)^2<4ac(24/25)                    (11)

make the close matches unique and injective, hence an antipodal bijection;
forbid exchanging the unequal rectangle side types; and forbid reversing
the projected orientation. For the last gate, perturb the two target
side vectors by errors of norm<2(11/20), and expand their determinant.
Their original projected determinant is at least4ac(24/25). The only
surviving labels are identity and simultaneous sign reversal. A proper
planar source half-turn absorbs the latter. Thus ALL FOUR matches now
use the SAME ACTUAL ORIGINAL labels, with

    (B1v).(B2v)>=||B1v||^2, for every v in E.              (12)

By(8), one such match and R>22/5 bound the initially arbitrary roll:

    ||L-I||<(11/20+9/256+9/484)/(22/5),
    ||B1-P||<1/8+(11/20+9/256+9/484)/(22/5)<4/15.          (13)

The receiver drift uses its new chord1/11 bound. This argument controls
the full row frame; it does not assume a small source angle.

## 5. Actual minor-row support confines the source minor coordinate

Let r1 be the source unit row in minor direction k. Equation(13) gives
(r1)_k>9/10 and q=||(r1)_perp k||<4/15. The actual target row r2 has

    (r2)_k=1-Y^2/(1+Z), (r2)_j=-XY/(1+Z), (r2)_z=-Y.

Its minor-coordinate diagonal exceeds99/100, and its transverse l1 norm
is (1+X/(1+Z))|Y|<(21/20)|Y|<=7/1600 unless Y=0, when it is zero.

The four originals with coordinate b in direction k have independent
signs +-1 in the other coordinates. All other originals have k
coordinate<=c. The exact positive gate

    (b-c)(99/100)-(b-1)(7/1600)>0                          (14)

therefore proves the ACTUAL target support formula

    h_K(r2)=b(r2)_k+|(r2)_j|+|(r2)_z|,
    h_K(r2)-b<=(21/20)|Y|.                                (15)

Support containment and the four actual source originals give

    q<=sum_{i!=k}|(r1)_i|
      <=b(1-(r1)_k)+(21/20)|Y|
      =b q^2/(1+(r1)_k)+(21/20)|Y|.                        (16)

For q>0 its quadratic coefficient is<12/19 times q, using b<9/2,
q<4/15 and(r1)_k>9/10. Thus q<(399/140)|Y|<3|Y| when Y!=0;
when Y=0,(16) forces q=0. Since n1.r1=0, decompose e_k into its
component along r1 and the orthogonal remainder of norm q. This gives

    |(n1)_k|<=q, hence |(n1)_k|<3|Y|<=1/80 if Y!=0,
    (n1)_k=0 if Y=0.                                      (17)

No corrected source frame or invented containment is used.

## 6. Separate radius inequalities force exact two-coordinate order

Write gamma_x=a,gamma_y=c and rho=gamma_k/gamma_j. Let the source major
and minor components initially be x,y. If x<0 replace B1 by -B1 Rz.
This uses a proper body symmetry and proper planar half-turn, preserves
the original shadow and every E projection (Rz v=-v for v in E), and
changes both transverse normal signs while preserving positive z.
Consequently(12) and(17) still hold; take x>=0 from now on.

From(12), the matched projected radii satisfy||B1v||<=||B2v||.
All originals have equal spatial norm R, so the two opposite-pair
conditions give SEPARATELY

    |gamma_j x+gamma_k y|>=|gamma_j X+gamma_k Y|,
    |gamma_j x-gamma_k y|>=|gamma_j X-gamma_k Y|.            (18)

If X>0, target dominance gamma_j X>gamma_k|Y| follows from|Y|<=X/20.
The wrong source branch gamma_j x<=gamma_k|y| would make the smaller
left side in(18) at most gamma_k|y|<=3gamma_k|Y|. But both right sides
are at least gamma_j X-gamma_k|Y|>3gamma_k|Y|, because the checked
constant gamma_j>gamma_k/5 gives gamma_j X>4gamma_k|Y|. This is a
contradiction. Hence both left linear forms are positive. Removing the
absolute values in(18) now yields

    x>=X+rho|y-Y|.                                        (19)

If X=0, then Y=0,(17) gives y=0, and(19) follows from x>=0 directly.
Thus(19) includes the zero-tilt receiver, without dividing by X.
Summing(18) before choosing its branches would lose the information
that makes(19) possible.

## 7. Physical area order forces equality of both normal components

On the rectangle0<=v<=3/25,|w|<=1/80 define

    F_j(v,w)=A0 sqrt(1-v^2-w^2)+Hj v+4|w|.                 (20)

The positive root exceeds24/25 throughout this rectangle. The exact
gates Hj-A0/8>7 and4+A0(1/80)/(24/25)<5 show that F_j increases in
v with derivative>7, and has minor-coordinate Lipschitz constant<5.
The latter bound includes w=0: apply it on either side and join there.
These are analytic bounds on the WHOLE rectangle, not sampled values.

The source and target lie in this comparison rectangle by the filter,
(17) and(1). Equation(7) gives A(n1)>=F_j(x,y), whereas(4) gives
A(n2)=F_j(X,Y). Equation(19), the derivative bounds and the exact
positive constant7rho-5 give

    F_j(x,y)-F_j(X,Y)>=7(x-X)-5|y-Y|
                      >=(7rho-5)|y-Y|>=0.                 (21)

If y!=Y the final inequality is strict. If y=Y and x>X the first
comparison is strict. Containment also gives A(n1)<=A(n2). Therefore
y=Y and x=X. Positive z components imply n1=n2 exactly. This includes
s=t=0. For the two families rho=c/a=3-phi or a/c=(2+phi)/5,
and BOTH satisfy7rho>5.

## 8. Recover the full frame, scale and physical translation

Since n1=n2, each identically labeled pair in(12) now has equal norm.
The identity||B1v-B2v||^2=2||B1v||^2-2(B1v).(B2v) forces B1v=B2v.
Two independent equatorial originals have independent projected images,
because the equatorial singular value is positive. Together with the
same oriented normal this forces the full proper row frames B1=B2.
Equivalently, their remaining relative proper planar rotation fixes a
nonzero projected vector, so it is identity.

The ORIGINAL scaled containment gives lambda^2 A(n1)<=A(n2)=A(n1)>0,
hence lambda=1. The centered shadows are equal; the original support
inequalities in every planar direction give T=0. Undoing the independent
proper body folds, common gauge and source half-turns yields exactly
B1=sigma B2g in(2). Conversely gK=K=-K gives equality for every stated
sigma,g at lambda=1,T=0. This proves both directions, including all
receiving wedge boundaries and all initially arbitrary proper rolls.

## 9. Exact off-mirror example and prior-cover comparison

The checker independently computes the physical Cauchy area and direct
projected-original monotone-hull area at raw(1/20,1/1000,1). They agree
exactly; the original shadow has18 corners. This receiver belongs to(1).

For each of the60 proper g and both COMPLETE mirror families, put
q=g^t(1/20,1/1000,1) and maximize

    (q_z+s q_j)/(||q||sqrt(1+s^2)), 0<=s<=1/12.

The derivative numerator is q_j-s q_z. Endpoints and every admissible
critical parameter s=q_j/q_z contain all maxima. Only positive signed
numerators are squared. The exact largest squared cosine is
1002500/1002501, attained at the x-mirror parameter1/20. The positive
squared comparison with(1-d^2/2)^2 proves that its chord distance from
the ENTIRE proper mirror union exceeds1/2000. In particular it lies
outside the earlier radius1/2000000
[uniform mirror tube](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_uniform_mirror_arc_tube/PROOF.md),
source4cbe9d147d678d0311b1955bd85849f31e7a419b, graph
bafkreicrfdsjypd4mpepvaescy3vb4devd2g6gmymwhgwbrxpwqvn3od54.

Separate exact all-proper-image checks place it outside the specified
[twofold1/270 caps](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_quadratic_twofold_caps/PROOF.md),
the fivefold1/1500 caps and the
[endpoint1/15000 caps](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_endpoint_contact_caps/PROOF.md).
Its minimum original height is below the83/200 threshold of the earlier
[height-band exclusion](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md).
These are explicit comparisons with those named covers, not a claim that
every older published receiving region has been enumerated. Their theorem
scopes and reviewer status are not transferred to this new result.

## 10. Reproduction, trust boundary and remaining frontier

From the repository root, Python3.11+ standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_two_coordinate_wedges/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_two_coordinate_wedges/check.py
```

Both outputs must byte-match the entire expected.json. Explicit exception
guards survive optimization. Six damaged controls omit an actual original,
widen the tangent-sign domain, invalidate a physical support witness,
break the matching budget, enlarge the minor derivative domain, or weaken
the area domination below what the y-family needs; all must reject.
Affine endpoint checks have stated continuum reasons above. The new
checker replays the complete source filter and its prerequisites; it is
a finite-hypothesis certificate of this written geometric proof, not an
independent review or proof-assistant formalization.

The current primary seeds
[Steininger--Yurkevich](https://arxiv.org/abs/2508.18475) and
[Zeng](https://arxiv.org/html/2604.26531), read live2026-10-01 this pass,
retain standard RID as unresolved. A bounded fresh primary-literature
search located no global resolution; no exhaustive search or priority
claim is inferred. The macroscopic receiving complement remains open.
A useful next step is to analyze the next actual support/sign transition
outside these wedges, retaining separate original-pair constraints and
checking when physical area domination or the full-source filter fails.
No floating search failure, timeout or incomplete enumeration is used as
mathematical nonexistence evidence.

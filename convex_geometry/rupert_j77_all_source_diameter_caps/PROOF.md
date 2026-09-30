# Five explicit J77 receiver caps exclude every source orientation

Author: **six-rupert-2**, role **researcher**, 2026-09-30.

Let K be the standard unit-edge paragyrate diminished rhombicosidodecahedron,
Johnson solid J77, in the independently reconstructed 55-vertex model.
Put s=sqrt(5), phi=(1+s)/2,

    A=(0,phi,1),  D=(0,-1,(7+s)/2),  n0=D/||D||.

Let R be the verified body rotation through 72 degrees about A, and
let X=diag(-1,1,1), the verified body mirror fixing D. For a unit vector n,
write P_n=I-nn^T and M_n=I-2nn^T. The generated body group is C5v.

**All-source receiver theorem.** Suppose

    min_{k=0,...,4; sigma=+/-1} ||n-sigma R^k n0|| <= 1/2000.

For every proper rotation Q, every planar translation t, and every
lambda>=1,

    lambda P_n(QK)+t subset P_n(K)

implies lambda=1, t=0, and

    Q=R^k  or  Q=M_n X R^k,  for some k=0,...,4.             (1)

Conversely, each form in (1), with scale one and zero translation, gives
exact equality of the shadows. Thus these **five unoriented receiver caps**
admit **no strict Rupert passage for any source orientation or roll**.
The theorem puts no initial restriction on the full relative rotation.
It classifies closed containment throughout the caps.

This proves a restricted receiver-domain result, not global non-Rupertness.
J77's global Rupert property remains unresolved. All finite hypotheses below
are checked exactly with standard-library Python. The geometric implications
are unformalized, and no independent review or formal verification is claimed.

## 1. Exact diameter optimizers and a gap to other axial regions

The [diameter proof](../rupert_j77_projection_diameter/PROOF.md), source
fce6fd20899e14d0e65c564f410e98518df76977, constructs K as a centrally symmetric
50-vertex core C, with five restored gyrated-cap vertices. All 55 vertices
have common squared radius

    r^2=(11+4s)/4.

Choose representatives a_i of the core's 25 antipodal pairs and define

    f(n)=min_i |a_i.n|,  ||n||=1,
    B=(65+10s)/596,  L^2=r^2-B.

Every shadow of K has diameter at least 2L, since its core antipodal pairs
give diameter at least 2 sqrt(r^2-f(n)^2). At D the full 55-vertex diameter
is 2L. The new equality audit proves that the **complete projective optimizer
set**, for both f^2 and the full-body minimum diameter, consists of exactly

    [R^k D],  k=0,...,4.                                    (2)

It also proves a quantitative bound for every other axial sign region:

    f(n)^2 <= beta=(5-s)/20.                                (3)

Here an axial sign region fixes all 25 signs of a_i.n. Its boundary has
f=0. To justify (3), maximize f on the closed spherical region. If the
maximum is positive, the maximizer is interior to that sign region.
Its active signed vectors b_i have equal norm r. Their tangent gradients
b_i-f(n)n balance positively. A minimal Caratheodory representation uses
one, two or three vectors. Its direction is respectively parallel to

    a_i,
    a_i+epsilon a_j,
    (a_i-epsilon a_j) cross (a_i-eta a_k),
        epsilon,eta in {+1,-1}.                            (4)

For two vectors, equal norms and equal active heights force equal weights,
so their sum is the appropriate direction. With three, minimality makes
the two differences independent. These are all 9,825 candidates from the
preceding finite reduction. The same argument applies to every maximizer,
not just to one attained global maximum.

The checker generates all candidates. For each, it either finds a core
pair with squared axial height at most beta, or verifies exact maximum B
and membership in the five-axis orbit. There are exactly **20 maximizing
candidate occurrences**, giving exactly five distinct projective axes.
The value beta is itself attained among the candidates, at
a_1-a_2 in the ordered representative indexing. Three hand-solvable
orthogonal-basis controls exercise all branches of (4).

All 1,485 full vertex-pair distances are checked at each of the five axes:
**7,425** comparisons. Hence no additional full-body diameter minimizer
has been lost by passing through the core lower bound. Indeed any such
minimizer must have f^2=B and therefore already occur in (2).

If a sign region has maximum B, its maximizer is one of the directed
representatives of (2), lying strictly inside that unique sign region.
Every other sign region has maximum at most beta by the candidate audit.
This establishes (3) without enumerating sampled normals or assuming a
quantitative distance rate.

## 2. Diameter and axial coercivity near D

At D the four diameter-attaining pairs are the antipodal pairs

    (8,15), (11,12), (29,32), (30,31).

Every nonantipodal pair has a positive squared-distance gap, with minimum

    g=(901-125s)/1490 > 0.                                 (5)

All **1,460** nonantipodal pairs are checked. The squared projected length
of a difference z changes by at most 2||z||^2||n-n0|| under a change of
unit normal. Compare a nonantipodal pair with any one critical antipodal
pair; each difference has norm at most 2r. For ||n-n0||<=d, their squared
length difference changes by at most 16r^2 d. Therefore

    16r^2 d<g

makes the full-body diameter equal to its core antipodal diameter:

    diam(P_n K)^2=4(r^2-f(n)^2).                            (6)

This holds for d=1/2000. It does not assume the asymmetric full shadow is
centrally symmetric.

At n0 exactly four core pairs attain f(n0)=c0=sqrt(B). Their signed
representatives, with positive D height, have fixture indices 8,11,29,30
and height (5+s)/4. Write

    b_i=c0 n0+g_i,  g_i perpendicular to n0.

The convex hull of these four tangent vectors contains the centered disk
of radius rho, with

    rho^2=(233-10s)/596 > 1/4.                              (7)

The checker regenerates the complete four-vertex tangent hull and all
supporting edges. Positive edge offsets put the origin inside. For each
edge its squared distance from the origin is checked, with minimum (7).
Thus rho>1/2 is a disk-containment statement, not a sampled directional
estimate.

For any n in n0's signed axial region, the active signs remain valid, so

    f(n) <= c0(n.n0)-rho ||P_n0 n||.                        (8)

A positive f(n) forces n.n0>0. Body rotation and sign reversal transport
this inequality to the other nine directed optimizer representatives.

Consider an arbitrary unit-scale closed passage with receiver within
chord d of n0. Formula (6) and diameter containment imply

    f(n_source) >= f(n_receiver) >= c0-r d.                 (9)

The last inequality is the r-Lipschitz property of f. The checked bounds

    3/8<c0<2/5,  r<9/4,  B-(9/5)d>beta

give f(n_source)^2>beta. Consequently its sign region is one of the ten
winning directed regions from Section 1. Applying (8)-(9) there gives

    ||P_n* n_source|| <= r d/rho < (9/2)d.

Its dot product with the directed optimizer n* is positive. The tangent
sine is less than 1/10, so that dot product exceeds 99/100. The chord/sine
identity and 200/199<(101/100)^2 then give

    ||n_source-n*|| <= (101/100)||P_n* n_source|| <5d.       (10)

No source orientation was initially assumed close to an optimizer.

## 3. Body gauges, proper frame completions and shadow error

Use orthonormal-row frames B1,B2 for the source and receiver, with oriented
normals given by the cross products of their rows. Such frames include all
source orientation and planar roll parameters.

A common planar reflection can change both normal signs without changing
containment. A common proper body rotation therefore reduces the receiver
cap to +n0. For the source winning representative n*=sigma R^k n0 use
the body symmetry

    S=R^k          if sigma=+1,
    S=R^k X        if sigma=-1.

Right-multiply the source frame by S. Its projected set is unchanged
because SK=K. The frame's cross-product normal becomes det(S) S^T n_source,
and hence lies within chord 5d of n0 in both cases, since X fixes D.

This step does **not** assert that QS is proper when S is a reflection.
Complete each two-row frame by its cross-product normal. Both completed
frames are proper orthogonal matrices, so their relative matrix is proper.
This is the justified projection-frame gauge even for an improper body
symmetry.

Let A1,A2 be the minimal proper transports from n0 to the gauged source
normal and receiver normal. Their operator chords are at most 5d,d.
With a common reference frame B0 of normal n0, there is U in SO(2) such that

    B1'=U B0 A1^T,  B2=B0 A2^T.

If B1'K+t is contained in B2K, transport each source and receiver point
to the reference shadow T=B0K. Since every body point has norm at most r,

    U T+t subset T+e D2,
    e=r(5d+d)<14d,                                        (11)

where D2 is the closed unit disk. Translation remains present.
The reference shadow has seventeen uniquely lifted extreme vertices,
with the full cyclic hull verified against all 55 vertices. Its proper
planar rotation group has order one, and its full planar isometry group
has order two. An independent check tests all 34 cyclic or reversed
vertex correspondences with the exact physical metric and vertex centroid.
In particular, no source half-turn symmetry is assumed.

Subtract two points of (11). For the difference body W=T-T, translation
cancels and W=-W:

    U W subset W+2e D2.                                   (12)

The half-turn of W allows reducing the roll **only in (12)** modulo pi,
to a residue alpha in [-pi/2,pi/2]. The full source T is asymmetric.
The possible pi branch is separately rejected in Section 5.

## 4. A complete quadratic certificate for the remote roll interval

Let m_i be the reference seventeen outward edge probes, normalized by
m_i.v_i=1. They are perpendicular to D, support all 55 vertices, and satisfy

    ||m_i||<M=51/100.                                     (13)

For either orientation m=+/-m_i, the support of W is exactly

    H_W(m)=max_v m.v-min_v m.v.

A source difference vertex w=v_j-v_k gives a necessary support test for
(12). Put q=sign(alpha), x=tan(|alpha|/2) in [0,1]. Its support displacement
numerator is

    p(x)=(m.w-H_W(m))
          +2q [m.(D cross w)/||D||] x
          -(m.w+H_W(m)) x^2.                              (14)

The actual displacement is p(x)/(1+x^2). The only new radical is ||D||.
The fixture provides a rational interval [l,h] with l^2<D.D<h^2, checked
exactly over Q(sqrt(5)). These endpoints are

    l=2362532429473/500000000000,
    h=4725064858947/1000000000000.

For z=q m.(D cross w), replace z/||D|| by z/h when z>=0 and by z/l when
z<0. This gives a coefficientwise lower quadratic p_-(x) for x>=0.
No floating-point radical or coefficient is used by the checker.

For each roll sign, six closed rational interval pieces cover

    1/50 <= x <= 1.

On each piece, one actual source difference vertex and one actual outer
probe produce three quadratic Bernstein coefficients at least

    Gamma=1/70.                                          (15)

All twelve pieces, including both signs and every endpoint, are checked
for exact coverage and exact positivity. The 36 coefficients are checked
by an independent power-basis reconstruction of the Bernstein identity.
Thus p(x)>=p_-(x)>=Gamma throughout each interval.

Condition (12) would instead require

    p(x)<=2e ||m||(1+x^2)<=4e M<4*14d M.

For d=1/2000,

    Gamma-4*14d M=1/175000>0.                              (16)

This excludes the entire closed remote interval. Hence the original full
roll U is within angle strictly less than

    2 arctan(1/50)<1/25

of either identity or the planar half-turn. This argument is a continuum
certificate, not a sample of rotation angles.

## 5. A positive translation-balanced stress rejects the half-turn branch

The reference probes with cycle positions **2,5,12** have positive weights

    w2=w5=(351-97s)/482,
    w12=(-110+97s)/241.

They sum to one and balance all three physical normal coordinates:

    sum w_i m_i=0.

Their weighted opposite support excess is exactly

    sum w_i (H_T(-m_i)-1)=(-151+74s)/241>1/20.              (17)

These identities are replayed from the actual 55 vertices and reference
probes. They do not assume central symmetry or a centered translation.

If U were within angle 1/25 of the half-turn, select for each probe a
vertex attaining H_T(-m_i). Rotating it by U rather than by the exact
half-turn changes its support by at most r(1/25)||m_i||. Sum its necessary
inequalities from (11). The translation cancels exactly. Equations
(13), (17) would require

    1/20 < M(e+r/25)
          < M(14d+(9/4)/25).

The checked opposite margin is

    1/20-M(14d+(9/4)/25)=53/100000>0.                     (18)

This is impossible. The full source roll, rather than merely the
difference-body roll residue, is therefore within angle 1/25 of identity.

## 6. Small full rotation and the closed-equality classification

Lift the reference planar roll U to the proper rotation fixing n0.
The relative proper matrix between the gauged frames has factors A2,
the lifted roll, and A1^T. A rotation with operator chord z<=1/10 has
angle at most (101/100)z: differentiate 2arcsin(z/2) and use
(101/100)^2(1-1/400)>1. Both transport chords satisfy this domain bound.

The proper rotation-angle triangle inequality therefore gives

    angle(Q') < 1/25+(101/100)(6d)
               =4303/100000 <3/20.                       (19)

The triangle inequality follows, for example, by multiplying unit
quaternions: for factor angles b,c with b+c<pi, the product's scalar part
is at least cos((b+c)/2)>0. Apply this twice. Thus (19) controls full
relative rotation, including roll.

The receiver chord d<=1/200 and (19) are within the explicit
[translated local theorem](../rupert_j77_translated_local_exclusion/PROOF.md),
source 3ae881c42e58af21905e26f6cdace6215e2e8487. That theorem includes
closed containment at every scale lambda>=1, and concludes

    lambda=1,  Q'=I,  t=0.                                (20)

To obtain the alignment estimates above, any original scaled closed
containment can first be reduced to unit scale, with translation t/lambda,
because 0 is in the interior of K. All body and frame gauges leave the
projected source set unchanged. After the rotation Q' is known to satisfy
(19), apply the local theorem to the **original** scaled containment.
This proves (20), without assuming the original scale was already one.

At the base receiver cap, (20) means B1 S=B2. If S is proper, the
orthogonal matrix QS fixes the receiver plane pointwise and has determinant
one; hence QS=I and Q=R^{-k}. If S is improper, QS has determinant minus
one and fixes that plane pointwise; hence QS=M_n and

    Q=M_n S^{-1}=M_n X R^{-k}.

Transporting the receiver cap by the common body rotation merely permutes
the five proper and five improper group elements. Changing the normal's
sign leaves M_n unchanged. This yields exactly the forms (1) throughout
all five unoriented caps.

Conversely, R^kK=K and XR^kK=K, while P_n M_n=P_n. Each form in (1)
therefore gives the same projected set. Since every closed containment
in the caps is exact equality, none is strict. This establishes the
all-source theorem with arbitrary roll, translation and scale.

## 7. Replay, dependencies and remaining research

From the repository root, use Python 3.11+ and its standard library:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    python3 -B convex_geometry/rupert_j77_all_source_diameter_caps/verify.py --self-test

Retain the sibling diameter and translated-local directories. Fourteen
files are byte-pinned by dependencies.json. The translated-local
certificate is replayed and compared with its published expected output.
The old diameter script's debug-only check is not imported: the present
checker performs its own explicit-exception candidate and equality audit,
and also works under Python -O.

The new fixture is 1,373 bytes. The checker verifies all 9,825 candidates,
55,886 axial comparisons, 7,425 full-body diameter pairs, 1,460
nonantipodal gaps, the complete four-point tangent hull, all reference
supports, all planar dihedral correspondences, the half-turn stress,
and all twelve closed roll intervals. It records 66,358 new sign
inequalities and audits 3,231 distinct signs independently using rational
enclosures of sqrt(5). Eight new malformed controls and four inherited
ones are rejected. expected.json gives the deterministic output.
Canonical fixture SHA256:

    981c10bc080e74291f0c4fa65ddcc79355b202ecac25272990c2d5e3246fc081

The earlier [uniform J77 local exclusion](../rupert_j77_uniform_local_exclusion/PROOF.md)
is a complementary result with an existential angle for all receivers.
Its angle is not used as a numerical cutoff here. The present theorem
uses the explicitly quantified D local theorem and independently
eliminates all remote source and roll parameters in the receiver caps.

The frame-transport and winning-region idea is complementary to
**six-rupert-3**'s [adaptive RID receiver criterion](../../rhombicosidodecahedron_mirror_cluster_obstruction/ADAPTIVE_RECEIVER_PROOF.md),
source 53e57de0ba3c38d4ee789e7bbd5fbb031347a267. J77 requires the difference
body and a separate translation-balanced half-turn stress; the RID
centering and full-shadow half-turn symmetry are unavailable.
**six-rupert-1**'s [deltoidal uniform local result](../../geometry/rupert_deltoidal_symmetry/twofold_area_proof.md),
source 58ec651cdd077243b556287369b6f56132735f6d, supplies complementary
current nonlocal-frontier context for a different named solid.
The pre-publication refresh also found six-rupert-3's
[axial-height transport refinement](../../rhombicosidodecahedron_mirror_cluster_obstruction/DIRECTIONAL_TRANSPORT_PROOF.md),
source 30c9c86753797307cc17b56ffd76aa88d94987df, graph
bafkreihl44hhtwxjrezrxurevchfwpfgkeojhbl2ctkimksjg4efia346u.
Its vertex-height transport inequality is a useful next-step method;
the present proof uses the independently checked coarser bound (11).

Live primary literature checked 2026-09-30:
[Gosain–Grimmer Table4](https://arxiv.org/html/2509.08190),
[standard projection criteria](https://arxiv.org/abs/2112.13754),
[Scott definitions](https://arxiv.org/html/2208.12912),
and the required [2604.26531](https://arxiv.org/html/2604.26531) /
[2508.18475](https://arxiv.org/abs/2508.18475) seeds.
The checked list retains J72,J73,J74,J75,J77. A bounded search found no
later J77 resolution and supports no priority claim.

The complementary receiver domain remains open. A useful next step is
an adaptive receiver criterion using actual diameter pairs and translated
roll bounds, followed by certified receiver polygons extending outside
these five caps. An unsuccessful numerical passage search, timeout or
incomplete enumeration would not prove global nonexistence.

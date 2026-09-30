# Directional all-source receiver domains for Johnson solid J77

Author: **six-rupert-2**, role **researcher**, 2026-09-30.

Let K be the standard unit-edge paragyrate diminished rhombicosidodecahedron,
Johnson solid J77, in the independently reconstructed 55-vertex model.
Put s=sqrt(5), phi=(1+s)/2 and

    A=(0,phi,1),  D=(0,-1,(7+s)/2),  n0=D/||D||.

Let R be the verified 72-degree body rotation about A and
X=diag(-1,1,1), the verified body mirror fixing D. Write
P_n=I-nn^T and M_n=I-2nn^T for a unit normal n.
The letter r below denotes the body radius, not the matrix R.

**Explicit receiver-domain theorem.** Each of the following receiver domains
excludes a strict Rupert passage from every source orientation and planar
roll, with arbitrary translation and scale at least one:

1. Every closed unoriented unit-normal chord cap of radius **1/200** about
   an axis R^kD, k=0,...,4.
2. Every ray through the **entire closed triangle** with corners

       D,
       L=(0,-13/12,(7+s)/2),
       C=(1/100,-25/24,(7+s)/2),

   and all its images under the verified C5v body symmetries and reversal
   of the normal. The L ray has chord distance strictly greater than
   **1/60** from n0, so this triangle extends beyond the radius-1/200 caps.

More precisely, for every receiver normal in these domains, every
Q in SO(3), every planar translation t and every lambda>=1,

    lambda P_n(QK)+t subset P_n(K)

forces lambda=1, t=0, and

    Q=R^k  or  Q=M_n X R^k,  for some k=0,...,4.           (1)

Conversely, each form in (1) gives equal shadows. No initial restriction
on the full relative rotation is imposed. The closed equalities are retained.

The cap radius is ten times the preceding all-source radius 1/2000.
It is seven times the independently proved radius 1/1400 in
**six-reviewer-1**'s [review of that preceding theorem](../rupert_j77_all_source_review1/README.md),
source e78fafefba916f04dc61ec7e2f9556e1469776a1, graph
bafkreialgb2n4e3yjo77r7gkgmaclia4evw2zkww7rgrzsw3ywznxopfum.
That review arrived during the pre-publication refresh. It independently
confirms the parent source reduction, geometry, local stresses and closed
classification. Its stronger endpoint bound is not needed here.
The main mechanism is a receiver-adaptive criterion using actual vertex
heights and actual receiver supports. The triangle is a continuum result,
not the result of checking only its three corners. J77's **global** Rupert
question remains open. This is an unformalized analytic proof with exact
finite hypotheses; no independent review or proof-assistant verification
is claimed.

## 1. Inherited exact geometry and source coercivity

The [preceding all-source certificate](../rupert_j77_all_source_diameter_caps/PROOF.md),
source 97ce8ace4dd4398a9f397428ccc9758ed5e1b028, proves and exactly checks:

    r^2=(11+4s)/4,
    f(n)=min_{a in the 50-vertex antipodal core}|a.n|,
    B=(65+10s)/596,  c0=sqrt(B),
    beta=(5-s)/20,
    rho^2=(233-10s)/596>1/4.

The complete projective maximizer set of f^2 consists of the five D-orbit
axes. There are ten directed winning axial sign regions. Every other region
has f^2<=beta. This is based on all 9,825 equal-radius active-set candidates,
not on sampled normals. The complete full-body minimum-diameter optimizer
set is also the D orbit, with all 7,425 vertex-pair comparisons checked.

In a winning directed region with optimizer n*, the active tangent hull
contains a disk of radius rho, so

    f(n)<=c0(n.n*)-rho||P_n* n||.                          (2)

Consider any receiver for which its ACTUAL full-body diameter satisfies

    diam(P_nK)^2=4(r^2-F^2),  F=f(n),  F^2>beta.          (3)

Any unit-scale closed source containment has source diameter at most that
of the receiver. Its antipodal core supplies the lower bound
4(r^2-f(source)^2). Thus f(source)>=F and its axial sign region is winning.
Equation (2) forces its dot product with the directed optimizer to be
positive and its tangent sine to be at most (c0-F)/rho.

Define

    delta=||n-n0||,
    a=(101/100)(c0-F)/rho,
    epsilon=1/25,
    Theta=epsilon+(101/100)(a+delta).                      (4)

When a<=1/10, the tangent sine is less than 1/10. Its positive optimizer
dot product therefore exceeds 99/100. The chord/sine identity and
200/199<(101/100)^2 give source chord at most a.
This is a proved necessary estimate for every possible source normal.

Use the body/frame gauges from the preceding proof. For source optimizer
sigma R^k n0, right-multiply its two-row frame by S=R^k when sigma=+1
and by S=R^k X when sigma=-1. The projected set is unchanged because
SK=K. Its cross-product normal becomes det(S)S^T n_source, within chord
a of +n0 in either case. Complete each two-row frame by its cross-product
normal; the completed frames are proper even when S is improper.
No improper body symmetry is mislabeled as a proper relative rotation.

For minimal proper normal transports A1,A2, and a common orthonormal-row
reference frame B0 of normal n0, the frames can be written

    B1'=U B0 A1^T,  B2=B0 A2^T,  U in SO(2),              (5)

with transport chords at most a,delta. Translation remains present.

## 2. Minimal transport and actual support heights

For a minimal rotation A taking n0 to a unit n, write
n=cos(theta)n0+sin(theta)t, with t unit and perpendicular to n0.
Decompose v=zeta n0+chi t+omega(n0 cross t). Direct rotation gives

    P_n0(A^T-I)v={(cos(theta)-1)chi-sin(theta)zeta}t.

With normal chord x=2sin(theta/2), sin(theta)<=x and
1-cos(theta)=x^2/2. Hence

    ||B0(A^T-I)v||<=|v.n0|x+||v||x^2/2.                 (6)

This also holds at x=0. For a difference of body vertices the quadratic
coefficient is at most r, while for a single vertex it is at most r/2.
The first-order coefficient is its actual axial height, rather than r.
This elementary transport method is credited to **six-rupert-3**'s
[directional RID proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/DIRECTIONAL_TRANSPORT_PROOF.md),
source 30c9c86753797307cc17b56ffd76aa88d94987df, graph
bafkreihl44hhtwxjrezrxurevchfwpfgkeojhbl2ctkimksjg4efia346u.
No RID centering or full-shadow half-turn symmetry is used for J77.

Let T=B0K and W=T-T. Let m_j be the seventeen normalized reference edge
probes from the preceding certificate, m_j.v_j=1 and m_j perpendicular
to D. For a difference z=v_i-v_k write

    H_W(m_j)=max_v m_j.v-min_v m_j.v,
    G_j(z)=H_W(m_j)-m_j.z>=0.

For each probe used by the remote-roll cover, set kappa_j to the maximum
|z.n0| among its reference width-support ties. All 3*55^2=9,075 difference
pairs are checked. For every pair with height greater than kappa_j,
the exact gap checks establish

    G_j(z)>=||m_j||(|z.n0|-kappa_j) delta0,
    delta0=1/20.                                         (7)

There are 5,166 excess-height comparisons. Ties and smaller heights are
also included in the full pair audit. The three actual kappas are all

    ((5/2)+(11/10)s)/||D||,

whose outward upper enclosure is about 1.049653.
Using (6)-(7), for every delta<=delta0 the actual receiver difference
support obeys

    h_(B2K-B2K)(m_j)
       <=H_W(m_j)+||m_j||(kappa_j delta+r delta^2).        (8)

This follows for all original differences. It does not assume that the
center supporting ties persist or that the full shadow keeps its topology.

For the three half-turn stress probes, cycle indices 2,5,12, put
kappa_i^+ = max |v.n0| over the actual reference maximum-support ties.
All 165 probe/vertex pairs, including 120 excess-height comparisons, give
the analogous single-vertex bound

    h_(B2K)(m_i)<=1+||m_i||(kappa_i^+ delta+(r/2)delta^2)
             for delta<=delta0.                          (9)

All heights, gaps, ties and normal norms are regenerated from all 55
model vertices. Rational square-root enclosures make the checks outward.

## 3. Receiver-adaptive remote-roll criterion

Subtract two source-containment inequalities to eliminate translation.
The difference body W=-W allows reducing roll modulo pi only at this
stage. Write its residue alpha in [-pi/2,pi/2], q=sign(alpha), and
x=tan(|alpha|/2). The [inherited closed cover](../rupert_j77_all_source_diameter_caps/certificates.json)
has six rational interval pieces per sign covering all x in [1/50,1].
Each piece selects an actual source difference w_j, an actual reference
probe m_j, and an upper endpoint b_j. Its support numerator is

    p_j(x)=(m_j.w_j-H_W(m_j))
           +2q[m_j.(D cross w_j)/||D||]x
           -(m_j.w_j+H_W(m_j))x^2.                       (10)

The sign-aware radical lower bound and quadratic Bernstein calculation
from the preceding proof give p_j(x)>=gamma_j on its entire closed piece,
where gamma_j is the minimum of its three exact Bernstein coefficients.
All gamma_j>=1/70. Every polynomial identity is independently reconstructed
in the power basis. No sampled angles enter this cover.

Put h_j=|w_j.n0|. Equations (5)-(6) control the ACTUAL chosen source
difference; (8) controls the actual receiver difference support.
Necessary containment therefore gives

    p_j(x)<=(1+x^2) E_j,
    E_j=||m_j||[h_j a+kappa_j delta+r(a^2+delta^2)].       (11)

Thus every remote roll is excluded whenever all twelve inequalities

    gamma_j>(1+b_j^2) E_j                                (12)

hold. A single coarse Hausdorff error is not substituted for (11).
For example, the pair in the first positive-roll piece is (29,54),
with h_j about 0.058496, substantially smaller than a generic body bound.
The negative-roll counterpart is (31,51). Their actual preimages are
used, including after every body/frame gauge.

Consequently the full U is within angle less than
2arctan(1/50)<epsilon of either identity or the half-turn. The asymmetric
full shadow does not admit a half-turn quotient. That branch is handled next.

## 4. The translated half-turn stress with directional errors

The inherited probes with cycle indices 2,5,12 have strictly positive
weights

    w2=w5=(351-97s)/482,
    w12=(-110+97s)/241.

They sum to one and satisfy sum w_i m_i=0 in all three physical coordinates.
Their opposite-support excess is

    g_pi=sum w_i(h_T(-m_i)-1)=(-151+74s)/241>0.            (13)

For each probe choose an actual minimum-support vertex v_i^- of smallest
axial height and put xi_i=|v_i^-.n0|. The selected vertices are 29,31,24.
If U is within angle epsilon of the half-turn, (6), the roll perturbation
bound r epsilon and the receiver bound (9) give, after summing its necessary
inequalities and canceling translation exactly,

    g_pi<=E_pi,
    E_pi=sum w_i||m_i||[
             xi_i a+kappa_i^+ delta+(r/2)(a^2+delta^2)+r epsilon]. (14)

Therefore

    g_pi>E_pi                                            (15)

rejects the half-turn branch, with arbitrary translation retained.
The full roll now lies within epsilon of identity.

For a normal transport of chord z<=1/10, its angle is at most
(101/100)z. Differentiate 2arcsin(z/2) and check
(101/100)^2(1-1/400)>1. The proper relative frame rotation in (5) has
three factors: A2, the lifted reference roll, and A1^T.
Their proper rotation-angle triangle inequality gives

    angle(Q')<Theta.                                     (16)

This is a FULL three-dimensional relative-angle bound, including roll.
For the domains here a,delta<=1/10, so the factor angle sum is less than
one; the ordinary unit-quaternion proof of the triangle inequality applies.

## 5. Actual receiver supports close the local rotation argument

The [translated local certificate](../rupert_j77_translated_local_exclusion/PROOF.md),
source 3ae881c42e58af21905e26f6cdace6215e2e8487, supplies 34 probes p_l
with designated vertices v_l and, for all Cartesian coordinates k and
signs sigma, strictly positive weights a_l^(k,sigma) such that

    sum a_l (v_l cross p_l)=sigma e_k,
    sum a_l p_l=0,
    sum a_l<C=61/10,  r||p_l||<M=9/8.                   (17)

Every p_l is perpendicular to n0. At an ACTUAL receiver set
p_l'=P_n p_l. We require the finite receiver support predicates

    p_l'.(v_l-v)>=0  for every l and every body vertex v. (18)

These suffice even with support ties; uniqueness is not needed.
They can be checked directly, rather than requiring the old uniform
receiver cap of radius 1/200.

Transport preserves translation balance exactly:
sum a_l p_l'=0. Its torque error is less than CM delta, since
||p_l'-p_l||<=||p_l||delta. For nonzero angle theta of Q', choose k,sigma
with sigma times its axis coordinate at least 1/sqrt(3).
The exponential remainder has operator norm at most theta^2/2.
The weighted necessary support inequalities from (18) would have left
side strictly greater than

    theta[1/sqrt(3)-CM(delta+theta/2)].                   (19)

They must instead sum to a nonpositive value. Hence the checked condition

    3[CM(delta+Theta/2)]^2<1                             (20)

forces Q'=I. Its translation is then zero because a bounded positive-area
shadow cannot contain a nonzero translate of itself.

This also treats lambda>=1: reduce any purported scaled containment to
unit scale with translation t/lambda, using 0 in the interior of K.
The unit case gives Q'=I and t=0; positive diameter forces lambda=1 in
the original containment. No centering or central symmetry was assumed.

**Directional receiver criterion.** Conditions (3), delta<=delta0,
a,delta<=1/10, all twelve (12), (15), (18) and (20) imply the closed
classification (1). Indeed Q'=I means B1 S=B2. The orthogonal QS fixes
the receiver plane pointwise. For proper S, QS=I; for improper S,
QS=M_n. Undoing the actual C5v gauges gives exactly (1).
Conversely every form in (1) has equal shadows because R^kK=K,
XR^kK=K and P_n M_n=P_n.

## 6. Whole triangle: normalized bounds and quadratic continuum coverage

For a convex combination u of D,L,C, use n=u/||u||. All 50 core vertices
have a common strict axial sign at these three corners. Let F_* be the
minimum of their corner f values, and delta_* the maximum corner chord
from n0. Their positive signed linear heights give

    signed a.u>=F_* sum t_j||u_j||>=F_*||u||.

Thus f(n)>=F_* throughout the triangle. Likewise, with the positive
c=1-delta_*^2/2, the corner inequalities
n0.u_j>=c||u_j|| imply n0.u>=c||u||. Therefore delta<=delta_*.
These arguments concern the normalized rays of the ENTIRE triangle.
All error expressions in Sections 3-5 are increasing in nonnegative
a,delta, so it suffices to use their resulting uniform upper bounds.

The actual support predicates (18) have homogeneous quadratic numerators

    S_l,v(u)=(p_l.(v_l-v))(u.u)-(p_l.u)(u.(v_l-v)).       (21)

For every 34*54 pair, all six degree-two triangular Bernstein coefficients
are strictly positive: **11,016** exact coefficients.
Hence (18) holds throughout the CLOSED triangle. The probes and their
projection vary together; corner supports alone would not establish this.

The critical core vertex is V11. For every nonantipodal pair difference z,
the comparison of its projected squared length with the V11 antipodal pair
has homogeneous numerator

    J_z(u)=(4r^2-z.z)(u.u)+(z.u)^2-4(V11.u)^2.           (22)

All six coefficients for each of the 1,460 nonantipodal pairs are strictly
positive: **8,760** exact coefficients. Thus each is shorter than this
one antipodal pair throughout the triangle. The maximum core antipodal
diameter is at least that pair and equals 2sqrt(r^2-f(n)^2), so (3)'s
full-body diameter formula holds. It is unnecessary to assume V11 remains
the only core axial minimizer.

For any homogeneous quadratic J with associated symmetric bilinear form
j, its value at u=sum t_j u_j is

    sum t_j^2 J(u_j)+2 sum_(j<k) t_j t_k j(u_j,u_k).

These are exactly the six Bernstein coefficients, with the nonnegative
degree-two Bernstein weights summing to one. This proves the continuum
coverage, including edges and corners. The checker builds coefficients
from cached linear evaluations and independently replays every polynomial
at the barycenter using actual projected normals or physical diameters:
**3,296** independent replays. The barycenter evaluations audit the algebra;
the full coefficient signs provide continuum positivity.

Outward corner enclosures and the directional criterion certify the
whole triangle. The enclosed source chord is below 0.017438 and full
relative angle below 0.074955 radians. Exact positive margins are in
expected.json; decimals here only describe their sizes. The exact
area in the fixed-z affine chart is 1/2400. No spherical-area claim is made.
An outward LOWER chord enclosure proves the L ray's chord exceeds 1/60.
The whole triangle therefore extends beyond the new uniform caps.

## 7. Complete radius-1/200 caps

Let d=1/200 and ||n-n0||<=d. For each core vertex its base axial height
h is at least c0. Its tangent norm is sqrt(r^2-h^2), at most
L0=sqrt(r^2-B). Since the receiver dot product is positive, the reverse
triangle inequality gives

    |v.n|>=h cos(theta)-sqrt(r^2-h^2)sin(theta)
          >=c0 cos(theta)-L0 sin(theta)
          >=c0(1-d^2/2)-L0 d=:F_d.                       (23)

The last bound uses the normal chord, rather than the coarser r-Lipschitz
bound. Its outward lower enclosure is 0.3718512784424027, with square
strictly greater than beta. This small positive margin is checked exactly.

The inherited nonantipodal squared diameter gap is
g=(901-125s)/1490. The checked inequality 16r^2d<g gives the full-body
core diameter formula over the complete cap. The original translated-local
probe gap g_local>1/80 and r||p_l||<9/8 ensure (18), since

    2(9/8)d<1/80.

Use delta=d, F>=F_d, and the consequent upper source chord in the
directional criterion. Every remote-roll, half-turn and torque inequality
is strictly satisfied. The enclosed full angle is below 0.063933 radians,
also below the old 3/20 full-angle bound. Thus the ENTIRE CLOSED cap has
classification (1). Proper rotations and normal reversal give all five
unoriented caps. Body symmetry similarly transports the triangle.

## 8. Replay, status and remaining frontier

From the repository root, use Python 3.11+ and its standard library:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    python3 -B convex_geometry/rupert_j77_directional_receiver_domains/verify.py --self-test

Keep the preceding all-source directory and its diameter/translated-local
siblings. Seven direct dependency files are pinned, with fourteen further
files pinned transitively. The ENTIRE preceding checker is replayed and
compared with its published expected output. Python -O gives the same
complete output. The new compact fixture is 264 bytes.

Square roots of exact nonnegative Q(sqrt(5)) quantities are enclosed on a
fixed rational grid of denominator 10^12. Integer bisection finds adjacent
grid values; exact squaring verifies both inequalities. Every use of a root
chooses the outward endpoint with the required sign. No floating-point
root is a proof input. Exact endpoint controls cover 0,1,4,1024; malformed
radical intervals and unsupported domains are rejected. All new signs are
also audited using an independent rational enclosure of sqrt(5).

Eight new malformed controls and twelve inherited ones are rejected.
They include a missing or reversed triangle, a wrong root grid, a
nonantipodal critical vertex, a wider triangle failing winning-region
coercivity, an unsupported transport range, and invalid root bounds/domain.
Failure of a sufficient criterion does not imply a receiver admits passage.

The continuous trust boundary consists of the equal-radius active-set and
winning-region facts in the preceding proof, the displayed transport,
source/frame gauges, actual-pair support inequalities, translation-balanced
stress, proper rotation-angle and torque arguments, and convex/Bernstein
continuum coverage. Finite computations use exact Python integers/Fraction,
the pinned ordered Q(sqrt(5)) kernel and complete generators. No solver
verdict, floating passage search, sampled receiver cover, private input or
omitted proof corpus is used.

The earlier [uniform local J77 gap](../rupert_j77_uniform_local_exclusion/PROOF.md),
source d23b45ee6e2d2704087e42b6a4faef698c53b14d, remains a complementary
qualitative local closure. Its existential angle is not a numerical cutoff.
**six-rupert-1**'s [deltoidal uniform local result](../../geometry/rupert_deltoidal_symmetry/twofold_area_proof.md),
source 58ec651cdd077243b556287369b6f56132735f6d, likewise concerns a different
solid. Both global questions remain open, as emphasized by the orchestrator.

The final source refresh also read **six-rupert-1**'s
[global deltoidal area and all-source cap proof](../../geometry/rupert_deltoidal_symmetry/global_area_proof.md),
source 5596212ab31932f7dd8b90cf6f1ad73c66afbe16, graph
bafkreigpe3pe5qqrekltisoss3zikl3znyydtso7utxsvag2yu2ykz3tsm, and
**six-rupert-3**'s
[actual RID torque-hull simplex proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/ACTUAL_TORQUE_HULL_PROOF.md),
source 684f35df160134d1fefb14da75f5948ce8ac00ce, graph
bafkreiepyjhiavm5s4reqzgverqayeq6dhmjsof4g4xutfnsw7a6wafipm.
The former supplies a different global projection invariant; the latter
certifies all possible actual torque facets on all simplex boundary strata.
They are useful next-frontier methods, not premises of this J77 theorem.
Their central-symmetry reductions do not remove J77's translations.

Primary status refreshed 2026-09-30 against
[Gosain–Grimmer Table4](https://arxiv.org/html/2509.08190),
[Zeng's named-solid discussion](https://arxiv.org/html/2604.26531), and the
required [non-Rupert construction](https://arxiv.org/abs/2508.18475).
The checked Johnson unresolved list retains J72,J73,J74,J75,J77.
The bounded live search found no later J77 resolution and supports no
historical priority claim.

The complementary receiver sphere remains open. Extend the adaptive
criterion toward the winning axial-region boundary using other actual
receiver probe families, or find a structural source/receiver pair suitable
for an exact strict passage. Regions with F^2<=beta need a different
source-coercivity argument. Failed searches, timeouts and incomplete
enumerations do not establish global nonexistence.

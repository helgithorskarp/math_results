# A full-roll reduction on the minimum-area caps of J77

Author: **six-rupert-2**, role **researcher**, 2026-09-30.
Complete author-checked written intermediate proof with exact finite
hypotheses; unformalized. Independent review and historical priority are
not asserted. **Global Rupert property of J77 remains OPEN.**

Let K be the standard unit-edge paragyrate diminished
rhombicosidodecahedron, Johnson solid J77, with the 55 original vertices
in the hash-pinned model. Put s=sqrt(5)>0,

    e=(1,0,0), a=(0,(1+s)/2,1), c=(s-1)/4,
    Rv=cv+(1-c)(a.v)a/||a||^2+(a cross v)/2,
    E={+/-R^j e : 0<=j<5}.

R is the actual proper order-five body rotation. P_n is orthogonal
projection onto n-perp for a unit receiver n. The principal full angle
of Q in SO(3) is in [0,pi]. All angle bounds below are in radians.
Translation is arbitrary in the receiving plane.

**Theorem.** Suppose dist(n,E)=delta<=1/1000 and

    lambda P_n(QK)+v subseteq P_n K, Q in SO(3), lambda>=1.       (1)

If delta>0, there is an actual **right** body factor h=R^j such that

    angle(Qh)<15 delta<=3/200.                                  (2)

In a receiving body frame near e, the gauged original source normal
is in the directed +e branch, with chord less than (1385/448)delta.
After the two minimal proper transports, the entire surviving planar
roll has half-angle tangent satisfying

    |tan(phi/2)|<5 delta.                                      (3)

The directed -e source branch and all other full rolls are excluded.
If delta=0, the direct parent proves exactly lambda=1, v=0,
Q in <R>; these are equal shadows. No strict passage or numerical
receiving-cap exclusion is asserted by this theorem. Equation (2)
reduces all original source rotations on these caps to a specific
small full-angle problem; it does not close that problem.

The direct parent is the [physical-area and polar source-budget proof](../rupert_j77_projection_area/PROOF.md),
source **cd0088c8aa1e308657b17d759bc5600c7b8b2b34**, graph
**bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au**,
actually committed at7801. Its complete checker is replayed and every
expected output byte is compared. Its seven source files and the seven
original-model files it pins are byte-pinned by the two manifests. The
parent's old diameter/receiver-region enumerations are not replayed or
used as premises. New normal balances, full-circle intervals and every
roll and angle inequality below are checked afresh.

## The global area budget and proper moving frames

The parent proves the physical projection-area minimum
A0=(49+25s)/8, attained exactly at the five projective axes E. For every
unit original source k and 0<eta<=9/1000 it proves the global implication

    A(k)<=A0+eta => dist(k,E)<5eta/14.                           (4)

At eta=0, k belongs to E. No nearness, centrality or diameter premise
is required. On the entire closed receiver cap at e, actual facet sign
gates and the tangent area zonotope give, for delta>0,

    A(n)<A0+(277/32)delta.                                    (5)

The same estimate holds on the body and reversed-normal images.
Containment (1) gives lambda^2 A(Q^T n)<=A(n) even with arbitrary v.
Thus (4) first derives a signed source axis. Since
(277/32)/1000<9/1000, its chord alpha satisfies

    alpha<(1385/448)delta<1/300.                               (6)

If the source has minimum area, alpha=0, still strictly below the right
side when delta>0. The parent identifies the actual body rotations,
so this is a right body gauge, not an improper moving source.

For clarity first work with n near e. If Q^T n is near epsilon R^j e,
epsilon in {+1,-1}, put Q_g=Q R^j. Its source normal
k=Q_g^T n is near epsilon e by the same chord alpha.
Let A be the minimal proper transport e->n and B the minimal proper
transport epsilon e->k. Then

    F3=A^T Q_g B, F3 e=epsilon e, F3^T e=epsilon e.             (7)

Its restriction F to e-perp is in O(2), with determinant epsilon.
Neither its angle nor its directed branch has been assumed small.
The source flattened to the fixed receiving plane is exactly

    P_e A^T Q_g K = F P_e B^T K.                              (8)

All original vertices have common radius
r=sqrt((11+4s)/4)<9/4. Minimal proper transports have operator
distances ||A-I||=delta and ||B-I||=alpha. Pair the **same actual original
vertices** in each rotated copy and extend the paired error by convexity.
With S=P_e K in its (y,z) coordinates, the receiving polygon
Y=P_e A^T K is at Hausdorff distance at most r delta from S, and the
source X=F P_e B^T K is at distance at most r alpha from FS.

Origin-interiority of K is proved by three independent antipodal core
pairs, so 0 belongs to Y. Flattening (1) and dividing by lambda gives

    X+v'/lambda subseteq Y/lambda subseteq Y.

This removes scale only as a **necessary unit containment** and retains
arbitrary translation. No symmetry of K or S is assumed. Combining the
paired errors gives a necessary translated approximate containment

    FS+t subseteq S+E_actual B2,
    E_actual<=r(delta+alpha)<39/4000,
    E_actual<C delta, C=16497/1792.                            (9)

B2 is the closed unit disk. The two outward budgets follow from (6),
r<9/4 and delta<=1/1000; the uniform one also uses alpha<1/300:

    (9/4)(1/1000+1/300)=39/4000,
    (9/4)(1+1385/448)=16497/1792.

These are explicit bounds on every original placement, rather than an
existence assertion about approximate containment.

## A finite certificate for the full O(2) roll

The parent constructs S from all55 original projections:29 distinct
points and10 strict extreme vertices. The new checker reconstructs
them and performs550 support comparisons against all55 originals.
Their chosen original preimages in cyclic order are

    24,18,3,1,22,16,0,2,23,17.                               (10)

Several other originals have the same projections; (10) always selects
a real original vertex. It is not an antipodal-core surrogate.

Let p_i be these ten cyclic projected vertices. For receiving edge i set

    m_i=(p_(i+1),z-p_i,z, p_i,y-p_(i+1),y),
    H_i=m_i.p_i>0.

These are outward unnormalized normals. The checker proves
m_i.P_e V<=H_i for every original V. The supplied rational bounds U_i
satisfy U_i>0 and U_i^2>=||m_i||^2 by exact field signs.

For any selected positive weights w_i with sum_i w_i m_i=0, every
necessary approximate containment FS+t subseteq S+E B2 gives, using
any selected **actual original projected source** q_i,

    sum_i w_i(m_i.Fq_i-H_i)-E sum_i w_i U_i<=0.                (11)

The translation cancels in both components. Indeed each individual
receiving support has allowance E||m_i||<=EU_i. Two opposite normals
or three spanning normals give the fixed stresses. The checker derives
all weights from the actual normals, requires strict positivity, then
checks both zero normal sums and normalization. It does not trust a
floating linear-program output. Only three edge sets are used:
(0,5), (1,5,8), (1,4,7).

For x in [-1,1] define

    T(x)=[ [1-x^2,-2x], [2x,1-x^2] ]/(1+x^2),
    H=diag(1,-1).

Four families cover **all** O(2): T(x), -T(x), H T(x), -H T(x).
Each proper family covers a closed semicircle; their shared endpoints
are included. The other two cover the complete determinant-minus-one
branch. Reducing modulo pi is invalid for the asymmetric S, and is not
done. In this order the families are numbered0,1,2,3.

Multiplying (11) by the positive 1+x^2 gives a quadratic c0+c1 x+c2 x^2
over Q(s). If on a closed interval [a,b] its three quadratic Bernstein
coefficients

    f(a), f(a)+(b-a)f'(a)/2, f(b)                             (12)

are strictly positive, the necessary inequality fails everywhere on
that interval. To see this, substitute x=a+(b-a)z and express f as
B0(1-z)^2+2B1 z(1-z)+B2 z^2; these nonnegative basis weights sum to one.

The compact [certificate](certificates.json) supplies a fixed midpoint
tree on each of these five closed roots:

| Family | Closed root | Complete terminal paths |
| --- | --- | --- |
|0|[-1,-1/50]|0,1|
|0|[1/50,1]|0,1|
|1|[-1,1]|00,01,100,101,11|
|2|[-1,1]|000,001,01,10,11|
|3|[-1,1]|00,01,10,11|

There are18 terminal leaves,31 total nodes, depth at most3. The reader
checks prefix-free uniqueness and **both** children of every internal
node independently of the adaptive discovery policy. Intervals are
reconstructed with exact rational midpoints. Fixed edge and original
source ids on each leaf are in certificates.json. All54 coefficients
in (12) are strictly positive with E=39/4000. In fact all exceed1/50.
The complete reconstructed leaf-record hash, including intervals,
positive weights, quadratics and Bernstein coefficients, is

    caada5b8490ccc0b95a8ac7423e2ac246adc3e90f29e0c22b76a4bec9a9664f5.

The exact minimum coefficient is

    -150909277/496000000 + (3617762081/24800000000)s.

Every new polynomial identity is also checked directly from the full
2x2 matrix at x=-1,0,1. These54 checks determine the degree-two identities;
the Bernstein signs and complete trees, not sampling, prove the
continuous exclusion. Therefore (9) forces the directed **+e** source
branch, F=T(x), and the strict open guard |x|<1/50. This derives the
small proper roll from all original full rolls.

## A roll bound proportional to receiver distance

The actual opposite normal pair0,5 has m_5=-2m_0. Its positive weights
are(2/3,1/3). The weighted receiving height and rational norm bound are

    H0=(11+5s)/6, N=769421/375000.

For a positive near roll use the real sources V24,V16; for a negative
near roll use V18,V0. They are actual zero-roll contacts. The outward
linear torques are respectively

    L_+=8/3+s, L_-=7/3+s.

For x=|tan(phi/2)| and the larger allowance C delta, either signed
branch in (11) consequently requires

    g_sign(x,delta)=L_sign x-2H0 x^2-CN delta(1+x^2)<=0.        (13)

For d=1/1000 and b=1/50, the reader proves all four exact margins

    5L_sign-CN-25(2H0+CN d)d>0,
    L_sign b-(2H0+CN d)b^2-CN d>0.                            (14)

Their exact field values are printed in [expected.json](expected.json).
For every0<delta<=d, the first line is a strict lower bound on
g_sign(5delta,delta)/delta; the second is a strict lower bound on
g_sign(b,delta). The polynomial is concave in x because H0,N,C,delta
are positive. Thus it is strictly positive on the whole closed interval
[5delta,b], including both endpoints. The remote guard and (13) force
x<5delta, proving (3). No unspecific root selection or square-root
branch is involved.

The initial exploratory attempt to use the smaller fixed remote guard
1/250 had two insufficient near-identity witnesses under the uniform
39/4000 allowance. That failed sufficient test was not nonexistence
evidence. The fixed18-leaf guard plus the actual moving C delta budget
in (13)-(14) is the proof given here.

## Full proper angle and body images

In the surviving directed branch B transports e->k, and F3 fixes e
properly, with principal angle2atan x. From (7), Q_g=A F3 B^T.
The principal-angle triangle inequality therefore gives

    angle(Q_g)<=2asin(delta/2)+2asin(alpha/2)+2atan x.

For chords at most1/300, beta=1001/1000 bounds the arcsine derivative,
since beta^2(1-1/360000)>1. Integrating gives
2asin(q/2)<=beta q. Also atan x<=x. With (6) and (3),

    angle(Q_g)<[beta(1+1385/448)+10]delta
              =(902119/64000)delta<15delta.                  (15)

All inequalities use their positive branches. The principal-angle
triangle inequality can equally be derived by multiplying the positive
unit quaternions of the three small rotations: their scalar component
is bounded below by the cosine of the sum of half-angles. The remote
guard already keeps that sum strictly below pi, so there is no wraparound.

For a receiver near epsilon0 R^ell e, reverse n when necessary and
conjugate the whole placement by U=R^(-ell). The receiver becomes near e,
K is preserved, and the original rotation is Q'=U Q U^T. A right factor
R^j for Q' commutes with U, so Q'R^j=U(QR^j)U^T. Conjugation preserves
principal full angle. Thus (15) gives exactly the actual right body
factor in (2) for every cap image. At delta=0 use the parent's full
original-orientation classification; no strict inequality with a zero
right side is asserted.

## Equal shadows and the next unresolved local problem

The new checker verifies that the actual body reflection
M_e=diag(-1,1,1) permutes all55 originals and fixes exactly22,23,24.
For every unit receiver n put M_n=I-2nn^T. The proper rotation

    Q0=M_n M_e

satisfies P_n(Q0K)=P_nK, because P_n M_n=P_n and M_eK=K. As n tends
to e these equal-shadow rotations tend to identity. They are not strict
passages. Any further local theorem must retain this genuine family.

The earlier [uniform qualitative local-angle proof](../rupert_j77_uniform_local_exclusion/PROOF.md),
source **d23b45ee6e2d2704087e42b6a4faef698c53b14d**, graph
**bafkreiar5zgul6vfndfhkjkvg5cpkuewkkipybatfsbeo6iqojlbeqtbci**
at7330, handles five critical mirror axes by a singular first-order
cone and second-order system. It supplies an existential uniform angle,
with no numerical15/1000 guard. The present checker establishes the
exact axis identity

    (5-3s,5-s,-2s)=-(10-2s)R^4 e.

Thus the new area axes are that same critical mirror-axis family.
The present full-angle reduction makes its singular local remainder
the concrete next problem. Its qualitative angle cannot be assigned
the numerical value in (2) without a new proof. Ten edge-on facet walls
meet at e; fixed receiving supports must not be assumed to persist
across those walls. Whole-cap strict exclusion would require an exact
moving-support stratification and quantitative second-order argument,
including equality branches and boundary ties. The receiver complement
and orientations away from all established regions remain the global
frontier as well.

Complementary **six-rupert-1, researcher**'s newly read
[deltoidal two-thirds wedge proof](../../geometry/rupert_deltoidal_symmetry/two_thirds_wedge_proof.md),
source **3276bf5919f10ad27d159578b6c17175cc078485**, graph
**bafkreicl6wlxycuxhyvmpsmj4qf4mz4t3jg5hun3ccsecopv3ytoffigyy**
at7805, repairs four signed source witnesses and closes a complete torque
cover on a larger receiving triangle. Its centrality and nonsingular
torque-ball premises do not hold automatically at these asymmetric J77
mirror axes. It informs certificate selection, without transferring
constants or proof hypotheses. The earlier
[J77 translated north-triangle proof](../rupert_j77_directional_north_triangle/PROOF.md),
source a2c00c148381a36cb840571ca5b82d98e274fc35, graph7735, is a different
diameter-axis receiving domain; its constants are not premises here.

The prepublication refresh also read **six-rupert-3, researcher**'s
[wider winning RID band proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/WIDER_WINNING_BAND_PROOF.md),
source **a9b869b8f81f5b97eb762497cfd2529fa4cac89e**, graph
**bafkreicyu2ovhwpzjfa4bb3xo37xr6vu3levefkq7hqrpnwrlezvyxattq**
at7843. It classifies all original source rotations on a larger winning
receiving band using actual source-to-receiver transport and a complete
torque hull. Its centrality, nonzero active height and nonsingular ball
are different hypotheses; none is transferred to these J77 mirror axes.
Its citation of the area parent is context, not an independent review.

## Reproduction and proof boundary

From repository root, Python3.11+ standard library only, run sequentially:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B convex_geometry/rupert_j77_area_axis_roll/verify.py --self-test
python3 -B -O convex_geometry/rupert_j77_area_axis_roll/verify.py --self-test
```

Both modes compare **every byte** of expected.json. The complete area
prerequisite is replayed and all13,231 parent expected bytes are compared;
its13 malformed controls also run. The new20 malformed controls reject
missing directed roots, open endpoints, incomplete/prefix-colliding trees,
false source and edge ids, unbalanced normals, wrong fixed witnesses,
undersized norm or error bounds, too small roll/angle ratios and a missing
negative near branch. All distinct field signs, including the parent's,
are independently audited by rational sqrt(5) enclosures, with its Pell
and kernel controls. Optimized Python retains all require checks.

The exact original coordinate/cupola model, ordinary Python Fraction
semantics, the two byte-pinned source directories, and the written
continuous area, proper-frame, paired Hausdorff, support-balance,
Bernstein, concavity and full-angle arguments remain the trust boundary.
No floating search, incomplete enumeration, solver verdict, timeout,
unspecified local radius or omitted large proof corpus is a premise.
Measured final checker receipts and hashes are in README.md.

Primary status was refreshed against
[Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190), which retains
J72,J73,J74,J75,J77 as unresolved Johnson solids.
[2604.26531](https://arxiv.org/html/2604.26531) retains87/92 known Johnson
examples and the rhombicosidodecahedron conjecture;
[2508.18475](https://arxiv.org/abs/2508.18475) proves a different constructed
non-Rupert body. The standard strict proper-projection equivalence is in
[Steininger--Yurkevich](https://arxiv.org/abs/2112.13754). No primary
resolution of J77 was located in the bounded refresh. This is a new
exact intermediate full-orientation reduction, not a global Rupert
verdict or a repeated proof of the parent's area minimum.

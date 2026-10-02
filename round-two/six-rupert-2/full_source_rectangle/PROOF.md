# All-source closed J74 fits on an entire nonminimal receiving rectangle

**six-rupert-2, researcher; 2026-10-02.** Complete ordinary geometric proof
and exact finite certificate. All twelve bounded coefficient chunks,
the full local bridge and the independent conversion/damage controls pass
in both ordinary and optimized execution with entire records equal.
Author verification is not an independent review or formalization. The
global Rupert property of J74 remains **OPEN**.

## 1. Original named body, receiving domain and statement

Let `s=sqrt(5)>0`, and let `K=conv(V)` be the original unit-edge,
60-vertex **metabigyrate rhombicosidodecahedron, J74**. The exact
[model.py](../model.py) and [geometry proof](../PROOF.md), source
`25fc9695745b6832d068d18544452b7852b5847f`, committed LEMMA8551,
construct the named body by two nonopposite 36-degree cupola gyrations.
Every original has squared radius `R^2=(11+4s)/4`. Three independent
literal antipodal pairs put zero in the interior. The whole body is
not assumed centrally symmetric.

Put

    u0=((16s-26)/44, (53-15s)/44, (-11-s)/44),
    r0=((101s-183)/58, (329-109s)/58, -1)=u0/(-u0_z),
    eta=1/1000,
    r=(r0_x+dx,r0_y+dy,-1), |dx|<=eta, |dy|<=eta.

Define the ENTIRE CLOSED projective receiving set

    Gamma={n=+/-r/||r|| : |dx|<=eta, |dy|<=eta}.          (1)

The halfwidth in (1) is a **raw coordinate halfwidth**, not a unit-normal
chord or an angle. Every rectangle side, vertex and choice of oriented
normal is included. Write `P_n=I-n n^t`, `M_n=I-2n n^t`.

Set `a=(s-1)/4`, `b=(s+1)/4`, `c=1/2`, giving matrices by ROWS:

    H=diag(-1,-1,1),
    A=(( b, a, c), (-a,-c, b), ( c,-b,-a)),
    B=((-a,-c,-b), ( c,-b, a), (-b,-a, c)),
    F={I,H,A,AH,B,BH},  Mx=diag(-1,1,1),
    E(n)=F union {M_n g Mx: g in F}.                     (2)

All six g are proper. Mx is an actual improper symmetry of the full
original K. Thus every member of E(n) is proper. Exactly twelve distinct
motions occur throughout Gamma. The full-body symmetries and the
partial shadow symmetries must both be retained.

**Theorem.** For EVERY n in
Gamma, EVERY Q in SO(3), EVERY ORIGINAL physical translation `T in n^perp`,
and EVERY scale `lambda>=1`,

    lambda P_n(QK)+T subseteq P_n K
        iff lambda=1, T=0, Q in E(n).                   (3)

All these fits are equal shadows. There is no source-normal, roll,
relative-Cayley, quaternion-component or translation entry hypothesis.
No strict standard Rupert passage has a receiver in Gamma. This is a
receiving-region theorem; it does not cover the receiving sphere.

The earlier [all-source cap proof](../full_source_cap/PROOF.md), source
`dc5c677266b22d09baafa372894dd6cfbf59d3b0`, committed LEMMA9345/0,
classifies the closed projective unit-normal chord cap of radius
`delta=1/1000000000` about `n0=u0/||u0||`. Section 7 proves that this
entire cap is contained in Gamma, so (3) strengthens that theorem's
receiving coverage while retaining every source and physical quantifier.

In fact Gamma contains the ENTIRE CLOSED projective unit-normal chord
cap of radius 1/9000 about n0. Section 7 proves this conservative
inscribed-cap corollary with the same twelve motions and all physical
quantifiers. It is a chord radius, unlike the raw halfwidth eta in (1).

Primary literature was refreshed on 2026-10-02.
[Gosain--Grimmer, Table 4](https://arxiv.org/html/2509.08190) lists the
five unresolved Johnson entries J72,J73,J74,J75,J77.
[Zeng, Sections 1.1--1.2](https://arxiv.org/html/2604.26531) uses proper
rotations and strict projected containment, reports 87 of 92 Johnson
solids as Rupert, and retains rhombicosidodecahedron non-Rupertness as
a conjecture. The distinct
[Steininger--Yurkevich Noperthedron theorem, v2](https://arxiv.org/abs/2508.18475)
does not settle J74. No failed floating search is treated as a theorem
and no historical priority for the methods below is asserted.

## 2. Complete actual receiver supports and persistent equal shadows

The exact monotone hull of ALL sixty projected originals at r0 has
the literal cyclic original indices

    16,0,36,28,10,11,47,55,27,7,43,31,13,12,48,56,20.    (4)

For a successive pair i,j in (4), put

    d_i=Vj-Vi, m_i(r)=d_i cross r,
    h_i(r)=m_i(r).Vi, N_i(r)=m_i(r)/h_i(r).              (5)

Both m_i and h_i are affine in dx,dy, and m_i.r=0. At EACH of the
four exact receiver corners, [local.py](local.py) checks positive
support heights and all 60 actual-original support inequalities
`m_i.Vk<=h_i`. This is 4,080 comparisons. The two endpoints satisfy
equality identically. Corner positivity and corner inequalities imply
the same facts on the whole closed rectangle, by affine interpolation.

The six exact matrices in F are bound literally to the named matrices
(2), not merely to a list of alleged poses. Their properness and the
actual symmetry Mx are checked by the inherited exact local verifier.
For EVERY receiving corner Vi in (4) and every g in F, there is a
literal SPATIAL preimage among its actual original source vertices:
`g Vk=Vi`. At all four receiver corners, for every g and every edge,
each source image p other than its two literal spatial endpoints has

    m_i(r).(Vi-p)>0.                                   (6)

All 23,664 strict offendpoint comparisons are rebuilt. Each gap is
affine, so (6) holds on the entire rectangle, including its boundaries.
In particular g=I proves that the 17 consecutive endpoint segments
are the complete convex projected boundary. They form the same closed
cycle, are nondegenerate by h_i>0, and every nonendpoint lies strictly
inward. Their halfplanes therefore intersect in their convex polygon.
All original source images satisfy these halfplanes, and every polygon
corner has its literal source preimage. Consequently

    P_n(gK)=P_n K, g in F, n in Gamma.                  (7)

Full-body preservation is unnecessary in (7). In this inventory I and
H preserve all original vertices, while A,AH,B,BH preserve the present
shadow. The latter four cannot be discarded as irrelevant source poses.
Since Mx K=K and P_n M_n=P_n, all six proper companions in (2) also
give equal shadows.

Let h_i^- be the least of the four positive corner heights. Convexity
of squared norm gives `||m_i(r)||^2` at most its largest corner value,
and affine interpolation gives h_i(r)>=h_i^-. The exact finite checks
prove, for every selected actual edge,

    R^2 max_corner ||m_i||^2/(h_i^-)^2 <9/4.            (8)

Thus R||N_i(r)||<3/2 throughout the entire closed rectangle.

## 3. Componentwise Neumann repair of the actual contact duals

The prior [pose/contact certificate](../full_source_cap/certificate.json)
contains, for each g in F and each signed coordinate +/-e_j, five
literal actual source contacts p=g Vk. At a receiver r, form the
five-by-five basis B(r) whose columns are

    (p cross m_i(r), m_i(r)_x, m_i(r)_y).                (9)

The original exact point weights are first converted from normalized
supports to raw weights w0 by dividing by h_i(r0). Their exact target
identity is `B0 w0=(+/-e_j,0,0)`. All inherited point support, torque,
force and original-contact identities are replayed. There are 36 dual
families and seven distinct exact affine bases.

Write B(r)=B0+dx Bx+dy By, and compute and verify the exact inverses
of B0. Put

    Kx=B0^-1 Bx, Ky=B0^-1 By,
    D=eta*(|Kx|+|Ky|), rho=||D||infinity,
    b=eta*(|Kx w0|+|Ky w0|), e=(I-D)^-1 b.              (10)

Absolute values in (10) are componentwise. The inverse product of I-D
is also checked exactly, and its entries are nonnegative. The finite
comparison for all seven bases gives `rho<1/20`. For every point of
the rectangle, Delta=dx Kx+dy Ky has |Delta|<=D and ||Delta||<1.
The convergent Neumann series defines the unique real raw weight vector
`w(r)=(I+Delta)^-1 w0`. Subtract w0 and majorize every term to obtain

    |w(r)-w0| <= sum_{k>=0} D^k b = e.                 (11)

This proves the whole continuum bound without replacing actual normals
by fixed normals or sampling the dual at receiver corners. The exact
record proves `min(w0-e)>1/2000` for every dual. Hence every repaired
weight is strictly positive.

Each raw height is `h_i=h_i0+dx hx_i+dy hy_i`. Using (11), its normalized
contact mass M(r)=sum_i w_i(r)h_i(r) is at most

    sum_i w0_i h_i0
       +sum_i [e_i h_i0
                +eta*(w0_i+e_i)*(|hx_i|+|hy_i|)].        (12)

For the three signed coordinate families, the exact bounds in (12)
are strictly below 6,7,8, respectively. The five-dimensional target
identity provides zero x,y force. Since every m_i.r=0 and r_z=-1,
zero x,y force implies zero z force as well. Thus each repaired dual
satisfies the FULL actual spatial identities

    sum_i w_i(p_i cross m_i)=+/-e_j,
    sum_i w_i m_i=0.                                  (13)

This cancels every ORIGINAL physical translation; centrality is not used.

For a contact N.p=1, the smallest eigenvalue of the symmetric product
form `(Np^t+pN^t)/2` is `(1-||N||||p||)/2`. Subtracting ||q||^2 and
using (8) gives the uniform elementary inequality

    (N.q)(p.q)-||q||^2 >= -(5/4)||q||^2.                (14)

Suppose a closed fit has Q=R(q)g, where g in F and

    R(q)=I+2([q]_cross+[q]_cross^2)/(1+q.q).

Multiply its literal contact inequalities by a repaired raw dual.
By (13), translation cancels and
`lambda sum w_i m_i.R(q)p_i <= sum w_i h_i = M`.
With lambda>=1, the unit-scale weighted contact change is nonpositive.
Using (13), (14) and the exact Cayley formula, the two signed families
for each coordinate give

    |q_x|<=(5/4)*6*||q||^2,
    |q_y|<=(5/4)*7*||q||^2,
    |q_z|<=(5/4)*8*||q||^2.                            (15)

On the CLOSED Euclidean Cayley gate ||q||<=1/16, a nonzero q would imply

    1 <= (5/4)*sqrt(149)/16 <1,
    squared upper bound =3725/4096 <1.                 (16)

Thus q=0. This is so far a conditional local theorem. Sections 4--6
derive entry into this gate for EVERY fitted source.

For a companion `gbar(n)=M_n g Mx`, replace Q by Q'=M_n Q Mx. It is
proper, and its ENTIRE projected source and ORIGINAL lambda,T are
unchanged, since Mx K=K and P_n M_n=P_n. Furthermore
`Q'g^t=M_n[Q gbar(n)^t]M_n`; conjugation preserves the relative rotation
angle and hence its Cayley Euclidean norm. The same local theorem
therefore holds about all twelve actual proper motions in E(n).

## 4. Receiver-dependent stresses give actual force balance everywhere

At r0, the deterministic original-support circuit enumeration gives
168 positive normalized point circuits: five pairs and 163 triples.
[forms.py](forms.py) lifts EACH of these to the entire rectangle.
Every pair comes from exactly opposite SPATIAL edge directions; its
raw weights can both be 1. For a triple of actual directions d_i,d_j,d_k,
use the common sign that makes all three affine weights positive:

    w_i(r)=(d_j cross d_k).r,
    w_j(r)=(d_k cross d_i).r,
    w_k(r)=(d_i cross d_j).r.                           (17)

Every weight is strictly positive at each receiver corner, and hence
throughout the whole closed rectangle. The classical cofactor identity
(valid also for singular triples) gives

    sum w_i(r)d_i=det(d_i,d_j,d_k)r,
    sum w_i(r)m_i(r)=0.                               (18)

Normalize by the positive CONSTANT `T0=sum w_i(r0)h_i(r0)` and put
beta_i(r)=w_i(r)/T0. The normalization is not recomputed at moving r;
beta is affine. The code checks that beta_i(r0)h_i(r0) is literally
the inherited normalized point weight. It also independently checks
ALL 3,024 force-component identities: all six coefficients of degree
at most two in dx,dy, in all three spatial components, for all 168
circuits. This is full vector force balance, not a planar determinant
assertion made without its spatial premises.

For ANY actual chosen original indices k_i, define the homogeneous
quaternion rotation, z=(h,v)!=0,

    R(z)=[(h^2-v.v)I+2vv^t+2h[v]_cross]/(z.z),
    L(m,p)=((m.p,(p cross m)^t),
             (p cross m,mp^t+pm^t-(m.p)I)),
    D(r)=sum_i beta_i(r)[L(m_i(r),Vki)-h_i(r)I4].         (19)

The actual-original identity is

    z^t D(r) z
       =(z.z) sum_i beta_i(r)[m_i(r).R(z)Vki-h_i(r)].    (20)

D has receiver degree two and quaternion degree two. The entire
receiver-center matrix is also compared literally with the original
normalized point construction, for every distinct chosen form.

Strict positivity of (20) EXCLUDES a closed scaled translated fit:
such a fit would give
`lambda sum beta_i m_i.R(z)Vki <= sum beta_i h_i` by (18).
The right side is positive. A positive unit-scale gap stays contradictory
for every lambda>=1. Every chosen Vki is an actual original; no floating
argmax value, alleged facet or centered translation is a proof input.

The affine cofactor interface was independently written here following
the useful handoff from six-rupert-1, and is explicit in that researcher's
[pentagonal all-source receiving-cell proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_all_source_horizon_cell/PROOF.md),
source `24788145d2c3870eca974bc694f0dfba506e1d3b`, LEMMA9363/0,
`bafkreicmrcx72imoy5ppmxgohpb4dicte7uaz5m4yr7ekt5wo62jdel2ae`.
This is classical force equilibrium, not a new general Farkas theorem.
That different body's group quotient, constants, equality inventory,
centrality and review status are not used as premises for J74.

## 5. Complete closed source charts and joint Bernstein coefficients

For every nonzero real homogeneous quaternion, choose a largest absolute
component, change the common sign and divide by that component. This
places it in at least one of the FOUR CLOSED cubes `z_j=1`, all other
components in [-1,1]. These cubes cover every proper rotation, including
the original half-turns h=0. No body-group quotient or closeness to an
equality pose is assumed.

The verified [compact forest](certificate.json) has 8,925 leaves, with
chart counts 2,391,2,258,2,082,2,194 and maximum depth 22. At level d
the binary code bisects coordinate d mod 3. Exact sorted prefix intervals
prove a gapless cover of the ENTIRE closed cube in each chart; no leaf
is a prefix of another. Child boundaries and overlapping chart faces
are retained. There are 8,848 cut leaves and 77 equality-neighborhood
leaves. The discovery program supplied only integer split paths and
actual source/stress labels, not mathematical signs.

For a cut, expand the actual matrix in (19) as

    D(r)=D0+dx Dx+dy Dy+dx^2 Dxx+dx dy Dxy+dy^2 Dyy.

The nine receiver Bernstein control matrices, indexed i,j=0,1,2, are

    D_ij=D0+eta[(i-1)Dx+(j-1)Dy]
       +eta^2[sigma_i Dxx+(i-1)(j-1)Dxy+sigma_j Dyy],
    sigma_0=sigma_2=1, sigma_1=-1.                      (21)

Indeed dx=eta(2t-1), dy=eta(2u-1), and the degree-two Bernstein
controls for (2t-1)^2 are 1,-1,1. The negative middle control is
essential; its value is not the square of its first-degree control.

On a source subcube, write a free component as x=l+w t. Its degree-two
first and second moment controls, at I=0,1,2, are

    first=l+w I/2,
    second=l^2+l w I+w^2 I(I-1)/2.                     (22)

The fixed quaternion component has both moments 1. For a symmetric
matrix B, each of its 27 source tensor coefficients is therefore

    sum_i Bii second_i +2 sum_{i<j} Bij first_i first_j. (23)

Equations (21)--(23) produce 9*27=243 EXACT joint coefficients per cut
leaf. This direct moment implementation differs from the inherited
power-to-Bernstein implementation. On the complete ten-element
symmetric-matrix basis, four charts and two exact cubes, the two
algorithms agree in all 2,160 coefficient comparisons. The six
receiver monomial basis controls in (21) are independently reexpanded
in the ordinary power basis, giving 54 exact coefficient identities.

Each tensor basis is nonnegative on its whole closed cube and sums
to one. Strict positive coefficients consequently imply (20)>0 on
the entire receiver/source product, including all sides and vertices.
Every one of the 8,848 cut leaves requires all 243 coefficient signs;
every equality leaf requires the 27 signs described next. The whole
forest verifies 2,152,143 strict exact coefficient signs, evaluated
with ordered Q(sqrt(5)) arithmetic and rational dyadic endpoints.

The finite verifier is divided into twelve contiguous bounded chunks
of at most 768 leaves. EVERY chunk, the complete local bridge and
the partition checks are required. A passing prefix, completed
floating proposal, incomplete journal, timeout or killed process
does not prove (3). [expected.json](expected.json) records each entire
ordered chunk's coefficient-stream SHA256, exact minima and ranges,
and the SHA256 of the ordered complete compact chunk records.
The latter is not mislabeled as a concatenated coefficient-stream hash.
The canonical forest SHA256 is
`56467904ce9c0daf031e8ed100ad01eb75b259691a3fd603d0fe472b1ccdaf54`;
the ordered complete compact chunk-record SHA256 is
`92b14214d34e29944c67e8f65f3911c2d3f3c3b3c624fd495fe19c55285d6277`.
All twelve whole chunk streams and the complete local mathematical
record match in ordinary and optimized execution. The author runs
sum to 616.944 and 616.019 seconds of sequential verified child wall
time; the observed cumulative child peak upper bound is 42,700 KiB.
The optimized continuation's tool session was interrupted after three
complete chunks; frozen successful receipts were retained and the
remaining nine chunks were replayed before complete assembly. No
conclusion was inferred from an incomplete run.

## 6. Equality leaves enter the actual moving local gates

The twelve point references are `g` and `M_n0 g Mx`, for all g in F.
For a leaf marked as an equality neighborhood, every one of the 27
exact coefficients of

    (z.z)[trace(R(z)ref^t)-tau] >0,
    tau=(3-(1/17)^2)/(1+(1/17)^2),                      (24)

is checked positive on its whole closed source cube. For a proper
relative rotation with finite Cayley vector q,
`trace=(3-q.q)/(1+q.q)`. Inequality (24) forces a finite relative
Cayley norm strictly below 1/17; it also excludes a relative half-turn.
The original source can still be a half-turn, already included by
the four charts.

For r in (1), the normalization inequality gives

    ||n-n0|| <=2||r-r0||/||r0|| <3eta,                  (25)

choosing the negative-z oriented normal. Thus
`||M_n-M_n0||op<=2||n-n0||<6eta`. For a fixed g, its point gate
1/17 is already inside the closed local gate 1/16. For a companion,
the ACTUAL relative operator distance is at most

    2/17+6eta,
    (2/17+6eta)^2 <4/257.                              (26)

For a proper relative rotation, operator distance from identity is
`2||q||/sqrt(1+||q||^2)`. At ||q||=1/16 its square is exactly 4/257.
Consequently (26) derives ||q_actual||<1/16 about the moving companion
M_n g Mx. The conditional local theorem (16), with the original scale
and translation preserved, now applies to every source in every
equality leaf. The complete cover excludes all other sources by (20).
Hence any actual fit has Q in E(n).

By (7), such a source shadow equals the receiver. Applying a positive
planar width to the ORIGINAL inclusion yields lambda<=1, so lambda=1.
For every planar direction a, equal-shadow support inequalities then
give a.T<=0; if T were nonzero, choose a=T to contradict this. Thus
the ORIGINAL T=0. Conversely every motion in E(n) gives an equal shadow
at scale 1 and translation 0. The full finite replay supporting the
cover is complete, so this proves the iff (3).

## 7. Distinct branches, nonminimality and containment of the old cap

The exact pairwise squared Frobenius distance of the twelve point
poses is greater than 1/100. Each companion varies in Frobenius norm
by at most `2sqrt(2)||n-n0||<9eta`, using (25). Any pair loses at most
18eta<1/10 of its point distance. Thus all twelve branches remain
distinct on the whole rectangle. Negating n leaves P_n,M_n unchanged.

The six named global minimum-area receiving axes are x,y and
`(1,+/-phi,+/-phi^2)/(2phi)`, with phi=(1+s)/2. The exact point checks
give absolute unit dot product below 119/128 with each axis. Hence
each projective unit-normal chord exceeds 3/8. By (25), the whole
rectangle has projective chord greater than `3/8-3eta>1/3` from all
six axes. No minimum-area-axis local conclusion is imported here.

The exact center has n0_z<-1/2. For any oriented normal with
`d=||n-n0||<=1/9000`, choose the negative-z oriented representative.
Since 1/9000<1/6, we have |n_z|>1/3.
Its raw coordinates are `r_i=-n_i/n_z`, so for i=x,y,

    |r_i-r0_i|
      <= |n_i-n0_i|/|n_z|
           +|n0_i| |n_z-n0_z|/(|n_z||n0_z|)
      <=3d+6d=9d<=1/1000=eta.                          (27)

Thus the ENTIRE CLOSED projective unit-normal chord cap of radius
1/9000, both orientations and its boundary, is contained in Gamma and
inherits (3). The much smaller old radius-delta cap is contained as
well, because 9delta<eta. This proves the claimed strengthening of
LEMMA9345's receiving scope. No optimal inscribed chord radius is claimed.
The earlier
[negative receiving-strip theorem](../negative_gap_strips/PROOF.md),
LEMMA9261, and [minimum-area cap theorem](../quantitative_minimum_caps/PROOF.md),
LEMMA8891, concern other receiving domains. Neither entire domain is
claimed contained in Gamma.

## 8. Reproduction and trust boundary

[check.py](check.py), [local.py](local.py), [forms.py](forms.py) and the
compact [certificate.json](certificate.json) are standard-library exact
source and finite evidence. [DEPENDENCIES.json](DEPENDENCIES.json) pins
all six inherited source files BEFORE import, including the actual
named model and ordered field arithmetic. The arithmetic is credited
to the prior [J77 source](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/q5.py),
source `fce6fd20899e14d0e65c564f410e98518df76977`; it is not new work.
The inherited full-source cap's already proved theorem is a precise
prior result, while its literal geometry and point-contact data are
rechecked here. Its cap's source-cut coefficient signs are not imported
as signs on the larger rectangle.

See [README.md](README.md) for the twelve-chunk exact replay and
[VALIDATION.json](VALIDATION.json) for actual author runs. The discovery
search and its floating arrays are absent from the mathematical checker.
Generated journals, caches and the multi-million-coefficient records
remain private generated scratch. All source labels, dyadic covering
paths and exact signs needed for independent replay are reproducible
from the compact public source.

The eight semantic damaged controls cover a missing cube, an omitted
half-turn chart, wrong actual source labels, wrong named pose, false
point force balance, receiver enlargement without proof, unsupported
moving-hole radius and a false quadratic middle control. The exact
algebra audits described in section 5 test different conversion paths.
Optimized execution must reproduce all complete ordinary-execution
records; explicit checker exceptions, not Python assertions, enforce
the proof gates.

The trust boundary is ordinary named-model identification and convex
support geometry, ordered-field Python arithmetic, exact inverse and
Neumann comparison semantics, the geometric Cayley/force-balance bridges,
closed quaternion covering and tensor-Bernstein reasoning written here.
No proof assistant or independent reviewer acceptance is claimed.
Source publication and graph commitment establish provenance.

The next frontier is extension toward an actual receiver support-phase
wall, with the full equality inventory and joint positive stresses
continued there, or classification of an adjacent phase. The receiving
sphere outside the stated region is still unclassified by this result.
No exact passage construction or global named-solid non-Rupert theorem
has been obtained.

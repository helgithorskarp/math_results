# All-source closed fits on a high-area RID receiving triangle

**six-rupert-3, researcher; 2026-10-02.** Ordinary geometric proof with a complete exact finite certificate. Author-checked, unformalized and independently unreviewed. The global rhombicosidodecahedron Rupert question remains open.

## 1. Statement in the standard physical coordinates

Let phi=(1+sqrt(5))/2 and let V be the sixty signed cyclic permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

These are the standard edge-length-two rhombicosidodecahedron originals. Write K=conv(V)=-K and let G be the proper sixty-element body group reconstructed in [field.py](field.py) and [geometry.py](geometry.py). Every original has squared radius 7+8phi. No auxiliary or perturbed source vertices occur.

Let Delta be the ENTIRE CLOSED raw receiving triangle with vertices

    r0=(9/100,(3+2phi)/100,1),
    r1=(11/100,(3+2phi)/100,1),
    r2=(1/10,(5+2phi)/100,1).

For any r in Delta put n=r/||r||, P_n=I-nn^t and H_n=2nn^t-I. The third raw coordinate is one, so this normalization is always defined. All edges and all three corners belong to the theorem.

**Lemma.** For every such n, every R in SO(3), every original physical translation t in n-perp and every original scale lambda>=1,

    lambda P_n R K+t subseteq P_n K

holds if and only if

    lambda=1, t=0, and R belongs to G union H_n G.        (1)

The same statement holds for n=+/-g r/||r||, r in Delta and g in G. There is consequently no strict Rupert passage with a receiver normal in this region. There is no restriction on the original source orientation, roll, translation or half-turn quaternion chart. The receiving region does not exhaust the sphere.

Moreover every receiver in Delta has actual physical shadow area

    A(n)>A2, where A2^2=960+1536phi.                     (2)

Thus the published subthird RID source filter9333 does not provide source entry in this region. Equation (1) is established by a complete source proof here, without applying that filter outside its scope.

The equivalence between arbitrary oriented orthogonal projection frames and the displayed physical fit is standard: an isometry of the receiving plane makes the relative source frame a proper R and retains its original scale and translation. The [standard strict-projection definition](https://arxiv.org/html/2604.26531#S1.SS1) uses interior containment. A theorem classifying every closed fit as equality therefore excludes every such strict passage in its specified receiving region.

## 2. Prior status and precise reuse

The primary literature refreshed on 2026-10-02 still treats RID non-Rupertness as a conjecture; the seed is not a theorem. [Zeng, arXiv2604.26531, Section1.2](https://arxiv.org/html/2604.26531#S1.SS2) explicitly lists that conjecture. [Steininger–Yurkevich, arXiv2508.18475v2, revised January2026](https://arxiv.org/abs/2508.18475) proves non-Rupertness of the Noperthedron, rather than RID. The standard RID coordinates are discussed in its [Section9.1](https://arxiv.org/html/2508.18475#S9.SS1).

The unresolved named list in [arXiv2509.08190, Tables2–4](https://arxiv.org/html/2509.08190) is RID, snub cube, snub dodecahedron; deltoidal and pentagonal hexecontahedron; and Johnson J72,J73,J74,J75,J77. Failed numerical searches in that paper establish no nonexistence theorem. A bounded current primary-literature search found no later global resolution of RID. This artifact proves only (1) on Delta and its body images.

The exact named geometry and ordered-field module were published in RID lemma8555, source58824907716016ff519f2aa5430fef92aa78c62c, [original model proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md). Its field module is copied verbatim and hash-pinned before import; the present program freshly reconstructs the actual proper group, source quotient, supports and all finite signs.

The existing [RID source filter9333](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_parametric_source_filter/PROOF.md), sourcebb28d1f8f375bc11fefb3419d60ae53476253f3c, has a different receiving scope. The existing [closed RID contact sector9273](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_wider_diagonal_sector/PROOF.md) supplies related local-contact method context. Neither theorem is declared generalized or independently reviewed by this artifact.

The binary-icosahedral inventory and dodecahedral closest-orientation cell are classical; see [R. James Purser, NCEP Office Note489 (2017), Section2(d)](https://repository.library.noaa.gov/view/noaa/15765/noaa_15765_DS1.pdf). Their coordinate orientation is rebuilt for the actual RID. No novelty is claimed for the quaternion double cover, convex centering or Bernstein positivity.

The ordinary three-tetrahedron frustum partition is credited to the complete [pentagonal-hexecontahedron closed-cell proof9363](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_all_source_horizon_cell/PROOF.md), source24788145d2c3870eca974bc694f0dfba506e1d3b. Its full published proof and original committed body were read. The [J74 all-source cap9345](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/full_source_cap/PROOF.md), sourcedc5c677266b22d09baafa372894dd6cfbf59d3b0, is further whole-source and original-translation context. The bodies, constants, equality branches and receiving domains differ. Only the stated ordinary interfaces are reused; no peer numerical premise, centrality or review verdict transfers.

The latest complementary [joined pentagonal receiving-cell lemma9406](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_adjacent_horizon_cell/PROOF.md), sourcecfe8043ca4565f830a0251bd33d75de05421a7f0, extends its earlier closed pentagonal cell across an actual grazing wall to a convex quadrilateral. Its entire public proof and original committed body were read and matched. It is receiving-interface context for future RID extensions; its other-body theorem and constants are not premises of the present triangle certificate.

## 3. Original translation and scale are retained

Fix a hypothetical original fit. Both P_n R K and P_n K are central. If x is in lambda P_n R K, then x+t and -x+t lie in P_n K. Centrality of the receiver gives x-t in P_n K, and convexity gives x in P_n K. Hence

    lambda P_n R K subseteq P_n K,
    P_n R K subseteq P_n K.                             (3)

The second inclusion uses lambda>=1 and 0 in K. This is a necessary implication from the original fit, rather than an assumed zero translation or a changed scale.

An equivalent literal cut pairs support N/original v with support -N/original -v. Equal nonnegative weights1/2 cancel the original t and imply lambda N.Rv<=1. A strict unit violation N.Rv>1 thus excludes EVERY original t and lambda>=1. These antipodal pairs use actual RID originals and supports.

## 4. Complete body and central-shadow quaternion reduction

The binary lift B consists of eight signed coordinate unit quaternions, sixteen independently signed half-coordinate quaternions and the96 signed EVEN four-coordinate permutations of

    (0,1/2,phi/2,(phi-1)/2).

The checker verifies all120 are unit and contain both signs. Their quaternion rotation matrices are exactly the freshly generated60 proper body matrices; the latter preserve all60 originals and are closed under the two actual generating rotations. The opposite parity fails the actual named-body comparison. The standard quaternion double cover and both signs give closure of B; no unsupported group or imported orientation is assumed.

For any unit source quaternion, right multiplication by B is an actual body motion. The eight coordinate lifts guarantee that the largest absolute scalar among those representatives is at least1/2. Taking its positive sign gives h>0 and finite Cayley c=v/h, including when the ORIGINAL source quaternion had scalar zero. Write

    R(c)=[(1-c.c)I+2cc^t+2[c]_cross]/(1+c.c).

The twelve nearest comparisons, with lifted scalar phi/2, define the bounded polytope D with normals kv and height1-phi/2. Opposite spanning normals establish boundedness and zero is interior. All220 boundary triples are considered exactly. The complete20 feasible vertices are

    eight signed (2phi-3,2phi-3,2phi-3),
    twelve signed cyclic (2-phi,0,5-3phi).

Every vertex has three incident faces and every face has five vertices. ALL120 full body comparisons |k0+kv.c|<=1 hold at ALL20 vertices. Affinity and bounded-polytope vertex coverage show that D is the full closest-body cell, not merely a sampled outer bound. Its vertices all satisfy

    c.c=39-24phi.                                      (4)

To retain all equal shadows, body folding alone is insufficient. Left multiplication by the proper half-turn H_n preserves the entire projected source:

    P_n H_n R K=-P_n R K=P_n R K.

It also retains original lambda,t. Select the largest absolute scalar among the full finite orbit

    {R g,H_n R g:g in G}.                              (5)

Left and right actions commute by associativity, without asserting that H_n and g commute as matrices. With pure unit quaternion p=(0,n), p^2=-1 and signed B ensure this orbit is closed under both actions. Coordinate lifts still give h>=1/2. The selected representative lies in D and obeys every central comparison h>=|scalar(p q k)|.

The universal Hamilton identity, verified through all48 trilinear basis coefficients, is

    scalar((0,r)(1,c)k)=-L_k(r,c),
    L_k=r.kv+(k0*r+kv cross r).c.

Clearing only positive h and ||r|| gives60 sign-paired necessary conditions

    L_k(r,c)^2<=r.r.                                  (6)

They constrain a selected closest representative, rather than every original source pose. Equations (5),(6) remove no physical fit.

At the interior receiving point r*=(1/10,(2+phi)/50,1), c*=(-r*_y,r*_x,0) is nonzero and lies inside the body-only D. Exact all-original projected sets give R(c*)=H_n* Rz, with Rz=diag(-1,-1,1) in G, and equal shadows. The comparison k=(0,0,0,1) rejects this particular representative by (6). It folds to identity through (5). This actual countercase prevents a false body-only origin-isolation argument and prevents omission of H_n G from (1).

## 5. Whole closed receiving triangle and actual supports

The literal receiving ring in the coefficient-ordered original V labels is

    48,36,54,56,38,53,46,18,11,23,5,3,21,6,13,41.

For each successive original endpoint pair Vi,Vj define

    E_i=Vj-Vi, m_i(r)=E_i cross r,
    h_i(r)=m_i(r).Vi, N_i(r)=m_i(r)/h_i(r).

The point model independently verifies actual edge squared length4, positive heights, polar endpoints and every original support comparison. Throughout Delta, h_i>0 and every off-endpoint original has m_i.(Vi-v)>0: all2784 linear endpoint-gap coefficients at the three receiver vertices are strictly positive. Affinity proves the inequalities on the ENTIRE closed triangle. The same16-edge convex boundary and exactly two literal contacts per support persist, including on every closed receiving edge/corner.

The96 degree-two receiving Bernstein coefficients of

    (25/16)h_i(r)^2-(7+8phi)||m_i(r)||^2

are strictly positive. Consequently R_body||N_i(r)||<5/4 throughout Delta, where R_body=sqrt(7+8phi). Normals are true physical polars, not projections into auxiliary cylinders.

Let S=(1/2)sum Vi cross Vj around the actual ordered ring. The physical projected area is S.r/||r|| and S.r>0. The six quadratic receiver coefficients of

    (S.r)^2-(960+1536phi)(r.r)

are positive. This proves (2) at all closed boundaries and interiors. The unnormalized field test introduces no sign ambiguity or mistaken physical-area scaling.

## 6. Uniform local source collar through actual cubic duals

For EACH signed coordinate, three literal endpoint torques f=v cross N_i are used. The actual (support-index,source-index) triples are:

| target | actual contacts |
| --- | --- |
| -e0 | (0,36),(4,53),(5,53) |
| +e0 | (6,18),(4,38),(7,18) |
| -e1 | (1,36),(3,38),(4,38) |
| +e1 | (4,53),(5,53),(7,18) |
| -e2 | (1,54),(4,53),(6,18) |
| +e2 | (1,36),(5,53),(0,48) |

For a fixed row put d_i(r)=v_i cross m_i(r) and D(r)=[d_0,d_1,d_2]. Each d_i is linear in raw r. For target z=+/-ej, Cramer's rule gives the literal torque weights

    mu_i(r)=h_i(r) z.(d_j(r) cross d_k(r))/det D(r),

where (i,j,k) is cyclic. Thus sum mu_i f_i=z in ALL THREE spatial components. The identity is the adjugate identity, rather than a two-dimensional balance or an assumed translation model.

The determinant, each of three numerators, and M_j det D minus the sum of numerators are homogeneous cubics after multiplication by the fixed determinant sign at r*. Their ten simplex Bernstein coefficients are checked exactly for every row:300 total coefficients. They are strictly positive. Division uses a certified positive denominator. Every weight is positive throughout Delta and the coordinate masses satisfy

    M0<10, M1<16, M2<6.                               (7)

For an actual endpoint N.v=1, the Cayley support identity reads

    (1+c.c)(N.R(c)v-1)
      =2(v cross N).c+2(N.c)(v.c)-2c.c.

The minimum eigenvalue of (Nv^t+vN^t)/2 is (1-R_body||N||)/2. The whole-triangle bound R_body||N||<5/4 therefore gives

    (N.c)(v.c)-c.c>=-(9/8)c.c.

Every unit centered hypothetical fit in (3) satisfies f.c<=(9/8)||c||^2. Positive signed-coordinate duals give |cj|<=(9/8)Mj||c||^2. If 0<||c||<=1/25, then

    1 <= (9/8)sqrt(392)||c|| <= (9/8)sqrt(392)/25 <1,
    squared closing factor =3969/5000<1.              (8)

Hence the only fit in the ENTIRE CLOSED Cayley Euclidean collar1/25 is c=0, uniformly for every receiver in Delta. This local implication alone is conditional; source entry is supplied next by the complete forest.

## 7. Exact closed source-shell coverage

Set alpha=1/11. Convexity and (4) give

    max_{c in alpha D}||c||^2=(39-24phi)/121<1/625.

The whole closed omitted core therefore lies inside the proved collar. The remaining closed shell D minus int(alpha D) is partitioned from the actual12 pentagonal faces of D. Each face cycle is freshly reconstructed: every other face vertex is strictly on the same oriented side of every successive edge. The unique positively oriented cycle is triangulated from its least-index vertex into three complete closed triangles. This yields36 radial face triangles.

For independent face vectors A,B,C, the frustum is represented by xA+yB+zC with x,y,z>=0 and alpha<=x+y+z<=1. Define L1=x+y+alpha z and L2=x+alpha y+alpha z. Since L1>=L2, its three closed regions L1<=alpha, L1>=alpha>=L2, and L2>=alpha are exactly the tetrahedra

    (alpha A,alpha B,alpha C,C),
    (alpha A,alpha B,B,C),
    (alpha A,A,B,C).

For example, the first tetrahedron's barycentric coordinates are x/alpha, y/alpha, (alpha-L1)/(alpha(1-alpha)), (x+y+z-alpha)/(1-alpha). The middle tetrahedron uses x/alpha, (alpha-L2)/(alpha(1-alpha)), (L1-alpha)/(1-alpha), z. The last uses (1-x-y-z)/(1-alpha), (L2-alpha)/(1-alpha), y, z. All are nonnegative exactly in their stated regions and sum to one. This proves full closed coverage, including every seam; volume identities alone are not treated as a coverage proof.

All108 resulting RID tetrahedra are nondegenerate and lie in the actual D. Their determinant-volume identities are also independently checked. The readable [certificate.txt](certificate.txt) starts with exactly108 explicitly numbered roots. Its960 literal edge bisections split a closed tetrahedron into both closed midpoint children. Prefix consumption checks every child, root and token; orphan, missing and duplicate entries reject. This produces1068 leaves and covers the ENTIRE source shell, not a sampling of source points or receiver normals.

## 8. Joint receiver/source coefficients and exclusions

A support/original cut uses the polynomial

    F_i,v(r,c)=(1+c.c)(m_i(r).R(c)v-h_i(r))
      =(m_i.v-h_i)+2(v cross m_i).c
        +2(m_i.c)(v.c)-(m_i.v+h_i)c.c.

It has receiver/source degree at most(1,2). With positive h_i, F>0 is an actual unit physical-support violation, so Section3 excludes the original lambda,t. Antipodal deduplication leaves480 possible literal support cuts, each retaining an actual source and support index.

A central comparison cut uses

    G_k(r,c)=L_k(r,c)^2-r.r,

of degree(2,2); G>0 contradicts (6) for the selected closest representative. All60 sign-paired comparisons are available. It is not asserted that such a cut violates a physical support for the original unfurled source.

On a receiving triangle and a source tetrahedron, a quadratic in each barycentric variable has six receiving and ten source Bernstein controls. The tensor basis is nonnegative and sums to one on the ENTIRE closed product. For receiving vertices ra,rb and source vertices ci,cj, a support's coefficient is the average of the two receiver-vertex source polarizations. A gauge coefficient is

    (L_k(ra,ci)L_k(rb,cj)+L_k(ra,cj)L_k(rb,ci))/2-ra.rb.

The exact checker independently reconstructs these from actual edge vectors and originals, rather than importing the proposal's matrices. Selected complete60-control support and gauge cases are additionally compared with literal Cayley/Hamilton evaluations using midpoint polarization in EACH variable. The universal support identity and all48 Hamilton coefficients justify the polynomial correspondence for every cut.

There are993 support leaves and75 gauge leaves. ALL1068*60=64080 exact tensor coefficients are positive; their actual minimum is

    1343/50-(83/5)phi >3/5000>0,

at source root25, path1100, actual support cut54. The whole computed minimum and every leaf sign are checked in the ordered field. Thus no admissible hypothetical fit in the complete quotient can remain on any outer-shell leaf. Combined with Section6 and the inner-core coverage, every selected source representative has c=0.

## 9. Recovering all original equal shadows

Undoing (5) now shows that the ORIGINAL R belongs to G union H_n G. Both sets are proper motions. For g in G, P_n gK=P_n K, and P_n H_n gK=-P_n K=P_n K. They are all actual equal shadows. No other partial-shadow branch survives the complete source argument.

Consequently the ORIGINAL inclusion becomes lambda B+t subseteq B with B=P_n K. The projected convex body has positive width. Comparing any positive width gives lambda<=1, hence original lambda=1. Comparing supports in every planar direction gives u.t<=0 for every u, hence original t=0. Conversely these exact scale/translation values and every stated equal-shadow branch give the closed fit. This proves (1). Conjugating by actual g in G, or changing n to -n, preserves the argument and gives its stated receiving images.

## 10. Reproduction and trust boundary

Run [verify.py](verify.py) with Python3.11+ and its standard library. It rebuilds the actual originals, proper group, binary lift, bounded D, face cycles, supports, whole-triangle cubics, complete source roots and every tensor coefficient. It consumes the checked compact forest and compares the WHOLE mathematical output with [expected.json](expected.json). Explicit gates use exceptions, so optimized Python retains all checks. [README.md](README.md) gives the commands and [DEPENDENCIES.json](DEPENDENCIES.json) pins the named original field source and records precise prior scope.

The compact forest has8394 bytes and SHA256

    dd0a0afe62abe6befefe98fd656a715c806cc009755f1ae1f84c8083e1b33b7d.

Normal public replay passed in14.164s and optimized replay in12.632s, with peak memory26152/30336KiB respectively, each under the existing separate20s guard. The complete mathematical records match. The optional NumPy1.24.2 [propose.py](propose.py), with all numeric threads one and unchanged10000-node/12s soft/20s external guards, regenerates the SAME8394-byte certificate in6.061s. Its floating signs establish no theorem; only the standard-library exact replay is used in the proof. Private exploratory forests and timing logs are omitted.

Six damaged or false controls reject: omitted entire source root, omitted closed leaf child, duplicated leaf, substitution of an actual antipodal source for the same witness, unsupported half-unit local collar, and dropping central-shadow comparisons or equality companions. The latter uses the actual all60-point equal-shadow countercase at r*. The named opposite lifted parity is also independently rejected by actual body-matrix comparison. The checker performs literal two-stage polarization checks and replays every exact sign; no timeout, numerical absence or incomplete enumeration is interpreted as nonexistence.

The remaining trust boundary is ordinary real convex geometry, quaternion/SO(3) correspondence, adjugate identities, Bernstein coverage and execution of this finite Python checker. There is no proof-assistant formalization and no independent review is asserted. The RID global question and all receiving directions outside the stated body images remain unresolved by this artifact.

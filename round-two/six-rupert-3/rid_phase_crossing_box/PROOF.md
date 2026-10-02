# RID closed-fit rigidity across a genuine receiving-hull phase change

**six-rupert-3, researcher; 2026-10-02.** Complete ordinary geometric intermediate proof with an exact finite certificate. Author checked, unformalized and independently unreviewed. Global RID Rupert status remains **OPEN**.

## 1. Precise named body, closed box and retained region

Let phi=(1+sqrt(5))/2. The standard edge-two rhombicosidodecahedron is K=conv(V)=-K, where V is the sixty signed CYCLIC permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

Every original has squared radius7+8phi. Let G be its actual proper60-element body group, freshly rebuilt and checked in [field.py](field.py) and [geometry.py](geometry.py). Set

    q=(3/50+2phi/25,1/25+phi/50,1), epsilon=1/1000,
    W={q+(x,y,0): -epsilon<=x<=epsilon, -epsilon<=y<=epsilon},
    r0=(9/100,(3+2phi)/100,1),
    r1=(11/100,(3+2phi)/100,1),
    r2=(1/10,(5+2phi)/100,1),
    Omega=conv(r0,r1,q,r2), Xi=Omega UNION W.

The union is literal; no unproved convex hull of the union is included. Every region is CLOSED, including all corners, the phase seam and the whole overlap. These are raw third-coordinate-one receivers, not spherical chords or angular coordinates. Write n=r/||r||, P_n=I-nn^t and H_n=2nn^t-I.

**Lemma.** For every r in Xi, every ORIGINAL R in SO(3), every ORIGINAL physical t in n-perp and every ORIGINAL lambda>=1,

    lambda P_n R K+t subseteq P_n K
       iff lambda=1, t=0, R belongs to G union H_n G.       (1)

The same holds for n=+/-g*r/||r|| for every actual g in G. Arbitrary roll, original source half-turns, all central equal shadows and every closed receiving boundary are retained. There is no source-localization premise or asserted count of distinct equal-shadow poses.

All receiving shadows in Xi have actual physical area>A2, A2^2=960+1536phi. Thus the older area-based source filter supplies no entry. The new region contains the actual16/18-corner phase change and strictly enlarges the entire parent9517 receiving-image region, even after all signed/projective body images. The proof below establishes W from fresh receiving supports and a complete source certificate; the explicit parent theorem supplies only the retained Omega.

## 2. Dependencies, prior art and current status

The formal old-piece dependency is [RID lemma9517](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_closed_grazing_quad/PROOF.md), graph `bafkreibtct26qyhmepagxmaqyojejluebvasx5bprexdz2gj7tzk2vaeja`, source `e3738c3f8729df6a87f9efcaafddddca2b400663`. Its complete public proof and original committed body were read. It proves (1) and area>A2 on the ENTIRE Omega. We use that conclusion only when taking the literal union; no old source sign is presumed valid on W.

The actual named model and exact ordered-field interface originate in [8555](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md), source `58824907716016ff519f2aa5430fef92aa78c62c`. The field, group/quotient builder and literal forest parser are copied from9517; the triangle collar engine is copied as [triangles.py](triangles.py). All new phase pieces, local cubics, roots, complete source signs and controls are freshly rebuilt. [DEPENDENCIES.json](DEPENDENCIES.json) pins six runtime modules before import and records precise reuse.

The strict proper-projection definition appears in [Zeng Section1.1](https://arxiv.org/html/2604.26531#S1.SS1); [Section1.2](https://arxiv.org/html/2604.26531#S1.SS2) retains RID non-Rupertness as a conjecture. [Steininger–Yurkevich2508.18475v2](https://arxiv.org/abs/2508.18475), revised28 January2026, proves the distinct Noperthedron theorem. [Gosain–Grimmer Tables2–4](https://arxiv.org/html/2509.08190) retain RID/snub cube/snub dodecahedron, deltoidal/pentagonal hexecontahedron and J72/J73/J74/J75/J77 as unresolved named solids in the located primary list. These sources and a bounded current arXiv search were refreshed2026-10-02. This is not an exhaustive priority survey; failed searches are not nonexistence proofs.

[RID9333](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_parametric_source_filter/PROOF.md) supplies no entry above A2. [RID9273](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_wider_diagonal_sector/PROOF.md) has a separate receiving domain. Both are context. The ordinary closed frustum interface is credited to [pentagonal9363](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_all_source_horizon_cell/PROOF.md). Complementary receiving joins [9406](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_adjacent_horizon_cell/PROOF.md), [9442](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_chamber_boundary_cell/PROOF.md), [9498](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_principal_axis_cell/PROOF.md), [J74rectangle9430](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/full_source_rectangle/PROOF.md), and the freshly fully read [J74phase-box9531](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/phase_crossing_box/PROOF.md), source `2ba89329055167fe838b568349801a2d7ccd39be`, are other-body context only. No other body's centrality, constants, source quotient, equal-shadow inventory or review transfers. Our selected supports actually change across the seam, whereas9531 uses unchanged supports; its theorem is not a RID premise. The fresh fully read [pentagonal facet40 quad9558](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_facet40_quad/PROOF.md), source `4f89c33fb8e4828f97f4b68481e15a15db51faa4`, was published while these new RID source replays were completing. It extends its own same-handed closed region with different five-coordinate duals; it is additional context, with no RID premise or transferred constant.

[Purser, NCEP ON489 (2017), Section2(d)](https://repository.library.noaa.gov/view/noaa/15765/noaa_15765_DS1.pdf) records classical closest binary-icosahedral orientation cells. Quaternion double cover, convex centering, Cramer/adjugate identities, compactness, closed polytope/frustum coverage and Bernstein positivity are credited rather than claimed new. The ordinary interfaces in Sections3,4,6,7,9 are adapted from the credited parent, with every new finite hypothesis replayed here.

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

At the interior receiving point q=(3/50+2phi/25,1/25+phi/50,1), c*=(-q_y,q_x,0) is nonzero and lies inside the body-only D. Exact all-original projected sets give R(c*)=H_n Rz, with Rz=diag(-1,-1,1) in G, and equal shadows. The comparison k=(0,0,0,1) rejects this particular representative by (6). It folds to identity through (5). This actual countercase prevents a false body-only origin-isolation argument and prevents omission of H_n G from (1).

## 5. Actual closed16/18-corner receiver partition

Let

    ell(r)=2(1-phi)rx+2phi*ry,
    s=2-phi, ell(q)=0,
    a=q+(-epsilon,-epsilon,0), b=q+(epsilon,-epsilon,0),
    c=q+(epsilon,epsilon,0), d=q+(-epsilon,epsilon,0),
    u=q+(epsilon,s*epsilon,0), v=q+(-epsilon,-s*epsilon,0).

Because0<s<1, the true phase seam is the ENTIRE closed segment[v,u] on ell=0. The exact clipping algorithm in [domain.py](domain.py) yields

    Wplus =conv(u,c,d,v) =W intersect{ell>=0},
    Wminus=conv(a,b,u,v) =W intersect{ell<=0},
    W=Wplus UNION Wminus.

Both are closed convex quadrilaterals. Their full fan triangles from the first displayed vertex give FOUR closed triangles, with all fan diagonals and the shared phase seam retained.

The actual ordered old16 boundary is

    48,36,54,56,38,53,46,18,11,23,5,3,21,6,13,41.

The actual new18 boundary inserts original19 between18/11 and original40 between41/48:

    48,36,54,56,38,53,46,18,19,11,23,5,3,21,6,13,41,40.

On the seam the true hull has sixteen corners;19 and40 are noncorner collinear boundary contacts. The full60-original chart hull is freshly constructed at ALL clipped polygon vertices. This chart (vx-rx*vz,vy-ry*vz) has kernel r, hence preserves projection incidence, but no metric is inferred from it.

For every true consecutive phase edge Vi->Vj, set E=Vj-Vi, m=E cross r, h=m.Vi. The checker verifies h>0 and m.(Vi-w)>=0 for ALL60 originals at ALL phase corners:3840 comparisons on Wplus and4320 on Wminus. Affinity gives the supports throughout the whole closed polygons. Noncollapse follows from h>0. Their ordered projected edge cycles remain convex boundaries by these support inequalities and continuity from the exact corner hulls; turns can become collinear on the seam, where the two extra vertices are retained in the edge cycle. No other originals can escape these supporting sides. Thus the16/18 rings give the actual physical shadow boundary on the respective pieces, with weak collinear contacts included.

For source obstruction and local duals, use only sixteen actual supports per phase. On Wplus use all old16 edges. On Wminus replace ONLY selected slot7=(18,11) by(18,19) and slot15=(41,48) by(41,40); the other selected edges persist. These selected16 constraints are necessary physical supports on the new18 boundary; they are not claimed to be its complete boundary. The omitted actual sides are unnecessary for the exclusion. The old slot7 is genuinely false at a new-phase box corner: original19 has a strictly negative old gap, explicitly checked. Therefore old support signs cannot be continued through the wall by assumption.

On EACH complete fan triangle, the selected supports have positive heights and all2784 weak offendpoint corner gaps. All96 quadratic controls of (25/16)h^2-(7+8phi)||m||^2 are positive. Four triangles give384 norm controls and imply R_body||N||<5/4 everywhere, with N=m/h. The contact cubics are checked on those same whole pieces in Section6.

The physical area uses the TRUE full phase ring, including all18 edges on Wminus. Set S=(1/2)sum Vi cross Vj around that ring. Every fan corner has S.r>0. All24 quadratic controls over the four triangles of

    (S.r)^2-(960+1536phi)(r.r)

are positive. Since actual area=(S.r)/||r||, EVERY receiver in W has physical area>A2, including the closed seam. The two area formulas agree on the seam because subdividing a projected edge by a collinear contact does not change area.

Strict enlargement is checked after saturation by actual body images. Let qplus=q+(1/2000,0,0), an interior receiver of Wminus. For each of the60 actual proper g, put w=g^t*qplus. If w_z=0 it is not an old raw receiver; otherwise w/w_z accounts for both projective signs. Each fails an oriented side inequality of the exact old Omega. Thus qplus is outside ALL60 signed/projective parent images. Retaining Omega and adding W strictly enlarges the full old receiving-image theorem; no spherical fraction is guessed.

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

The determinant, each of three numerators, and M_j det D minus the sum of numerators are homogeneous cubics after multiplication by the fixed determinant sign at q. Their ten simplex Bernstein coefficients are checked exactly for every row on EACH of the four fan triangles:1200 total coefficients over the whole box. They are strictly positive. Division uses a certified positive denominator. Every weight is positive throughout each complete fan piece, hence throughout W and the coordinate masses satisfy

    M0<10, M1<16, M2<6.                               (7)

For an actual endpoint N.v=1, the Cayley support identity reads

    (1+c.c)(N.R(c)v-1)
      =2(v cross N).c+2(N.c)(v.c)-2c.c.

The minimum eigenvalue of (Nv^t+vN^t)/2 is (1-R_body||N||)/2. The whole-piece bound R_body||N||<5/4 therefore gives

    (N.c)(v.c)-c.c>=-(9/8)c.c.

Every unit centered hypothetical fit in (3) satisfies f.c<=(9/8)||c||^2. Positive signed-coordinate duals give |cj|<=(9/8)Mj||c||^2. If 0<||c||<=1/25, then

    1 <= (9/8)sqrt(392)||c|| <= (9/8)sqrt(392)/25 <1,
    squared closing factor =3969/5000<1.              (8)

Hence the only fit in the ENTIRE CLOSED Cayley Euclidean collar1/25 is c=0, uniformly for every receiver in W. This local implication alone is conditional; source entry is supplied next by the complete forest.

## 7. Exact closed source-shell coverage

Set alpha=1/11. Convexity and (4) give

    max_{c in alpha D}||c||^2=(39-24phi)/121<1/625.

The whole closed omitted core therefore lies inside the proved collar. The remaining closed shell D minus int(alpha D) is partitioned from the actual12 pentagonal faces of D. Each face cycle is freshly reconstructed: every other face vertex is strictly on the same oriented side of every successive edge. The unique positively oriented cycle is triangulated from its least-index vertex into three complete closed triangles. This yields36 radial face triangles.

For independent face vectors A,B,C, the frustum is represented by xA+yB+zC with x,y,z>=0 and alpha<=x+y+z<=1. Define L1=x+y+alpha z and L2=x+alpha y+alpha z. Since L1>=L2, its three closed regions L1<=alpha, L1>=alpha>=L2, and L2>=alpha are exactly the tetrahedra

    (alpha A,alpha B,alpha C,C),
    (alpha A,alpha B,B,C),
    (alpha A,A,B,C).

For example, the first tetrahedron's barycentric coordinates are x/alpha, y/alpha, (alpha-L1)/(alpha(1-alpha)), (x+y+z-alpha)/(1-alpha). The middle tetrahedron uses x/alpha, (alpha-L2)/(alpha(1-alpha)), (L1-alpha)/(1-alpha), z. The last uses (1-x-y-z)/(1-alpha), (L2-alpha)/(1-alpha), y, z. All are nonnegative exactly in their stated regions and sum to one. This proves full closed coverage, including every seam; volume identities alone are not treated as a coverage proof.

All108 resulting RID tetrahedra are nondegenerate and lie in the actual D. Their determinant-volume identities are also independently checked. The readable [certificate.txt](certificate.txt) starts with exactly108 explicitly numbered roots. Its1596 literal edge bisections split a closed tetrahedron into both closed midpoint children. Prefix consumption checks every child, root and token; orphan, missing and duplicate entries reject. This produces1704 leaves and covers the ENTIRE source shell, not a sampling of source points or receiver normals.

## 8. Complete continuum source exclusion using affine phase controls

For an actual physical support and original source v, use

    F_i,v(r,c)=(1+c.c)(m_i(r).R(c)v-h_i(r))
      =(m_i.v-h_i)+2(v cross m_i).c
        +2(m_i.c)(v.c)-(m_i.v+h_i)c.c.

The receiver/source degree is at most(1,2). Its ten quadratic source-simplex controls at source vertices ci,cj, i<=j, are

    (m.v-h)-(m.v+h)(ci.cj)
     +(m.ci)(v.cj)+(m.cj)(v.ci)+(v cross m).(ci+cj).

For a fixed source control this is AFFINE in raw receiver r. Every point of a phase quadrilateral is a convex combination of its FOUR corners. Hence forty corner/source controls suffice on one whole closed phase product; both pieces require EIGHTY controls per physical leaf. No arbitrary triangulation interpolant or sampled receiver is used. Positive F gives a literal unit support violation, excluding every original lambda,t by Section3.

For the central fold use G_k(r,c)=L_k(r,c)^2-r.r, degree(2,2). The ten source controls at a fixed r are L_k(r,ci)L_k(r,cj)-r.r. On the ENTIRE W write r=r00+x*dx+y*dy, 0<=x,y<=1, dx=(2epsilon,0,0),dy=(0,2epsilon,0). For each source control expand

    p(x,y)=p00+p10*x+p01*y+p20*x^2+p11*x*y+p02*y^2.

Its nine tensor Bernstein controls, u,v in{0,1,2}, are

    p00+(u/2)p10+(v/2)p01+[u(u-1)/2]p20
          +(uv/4)p11+[v(v-1)/2]p02.

The degree-two basis in each coordinate is nonnegative and sums to one on the ENTIRE closed square. Combined with the source-simplex basis this gives NINETY controls per central gauge leaf. Positive G contradicts a necessary closest-representative comparison from Section4. It need not violate a physical support for the original unfurled source.

All480 literal antipodally deduplicated support cuts and60 signed-paired central gauges retain the actual data/cut index correspondence. [kernel.py](kernel.py) derives exact controls from originals and edge vectors, not numerical proposal matrices. In each of six root parts, a support case is independently checked by literal cleared Cayley evaluation and source midpoint polarization at all eight actual receiver corners. A gauge case is checked by literal Hamilton evaluation, source polarization and two receiver midpoint transforms on the full3x3 box grid. That gives170 comparisons per part,1020 per whole replay. Part2 has no gauge leaf, so its gauge polynomial identity is checked on an actual source root without asserting that it is a positive exclusion leaf. All48 universal trilinear Hamilton coefficients are freshly checked.

The literal forest has1596 midpoint nodes and1704 leaves, comprising1598 physical-support leaves and106 central-gauge leaves, with no local leaves. ALL

    1598*80+106*90=137380

exact controls are positive. Their global minimum is

    -97789243/1936000000+(3793429/121000000)phi >1/5000>0,

at root55,path001011,gauge480,coefficient89 (zero based). Every minimum comparison and sign is exact in the ordered field Q(phi). Thus no closest hypothetical fit remains on any closed outer-shell leaf; the whole inner core lies in the uniform closed collar and has only c=0.

All108 roots are replayed in SIX DISJOINT18-root parts. Each independently rebuilds the same whole named geometry, phase partition, support/cubic prerequisites and full literal forest structure, then consumes EVERY node and tensor in its own roots. The fixed [expected.json](expected.json) stores the entire common mathematical record once and every complete part record, including coefficient-stream hashes and semantic controls. Assembly requires exactly one of each part, all whole records equal, and the complete137380-sign/1704-leaf count. Missing/duplicate parts, altered coefficient records and an altered closed receiving-seam record reject. A completed part alone gives no whole-source theorem.

Each part also passes eight mathematical/coverage controls: missing root, missing closed child, duplicate leaf, wrong antipodal original, unsupported collar1/2, the genuine central companion, obsolete old-phase support7, and falsely using a16-corner full new boundary for area. These reject in both normal and optimized execution. The source pins are checked before import; explicit exceptions, not assertions disabled by optimization, enforce the proof gates.

## 9. Recovering all original equal shadows

Undoing (5) now shows that the ORIGINAL R belongs to G union H_n G. Both sets are proper motions. For g in G, P_n gK=P_n K, and P_n H_n gK=-P_n K=P_n K. They are all actual equal shadows. No other partial-shadow branch survives the complete source argument.

Consequently the ORIGINAL inclusion becomes lambda B+t subseteq B with B=P_n K. The projected convex body has positive width. Comparing any positive width gives lambda<=1, hence original lambda=1. Comparing supports in every planar direction gives u.t<=0 for every u, hence original t=0. Conversely these exact scale/translation values and every stated equal-shadow branch give the closed fit. This proves (1) on the ENTIRE closed W. Conjugating by actual g in G, or changing n to -n, preserves the argument and gives its stated receiving images.


The complete conclusion on Omega is the explicit parent9517 theorem. Taking the literal closed union Xi=Omega UNION W gives(1) on every receiver in Xi, without extending the old forest or adding the convex hull of the union. All common boundaries are covered by the corresponding closed proofs. The exact qplus test proves strict enlargement even after all signed body images. This gives the precise GENERALIZES9517 and DEPENDS_ON9517 meanings.

## 10. Reproduction, execution evidence and scope

Run from this source directory with Python3.11+ and the standard library:

```bash
python3 reproduce.py
python3 reproduce.py --optimized --compare .generated/normal/complete.json
```

The driver runs six18-root children STRICTLY SEQUENTIALLY, each with a20-second guard, and checks every fixed whole mathematical record. All numerical threads are one; the unchanged scope is1CPU2GiB. [VALIDATION.json](VALIDATION.json) records the actual completed normal/optimized executions, complete mathematical-record equality, four damaged assemblies, and deliberate copied-source pin controls. Generated coefficient streams, caches, private proposal data, keys and ledgers are not publication artifacts or runtime inputs.

The compact [certificate.txt](certificate.txt), SHA256 `9b92954a06fc8c5fafc07f0d67e364cb0a41d314c90c5528c8433c42cc4ba5c3`, is a literal proof object. A bounded private NumPy proposal helped find repairs after the old forest failed on W; exact all-source replay provides the mathematical evidence. Floating positivity, a failed cut or a timeout establishes no exclusion by itself. The source-only checker uses no numerical package or private prior source. Normal child-wall sum60.288s, optimized58.999s, largest child11.453s, childRSS upper38952KiB; all twelve children completed within their20s guards. The complete mathematical-record SHA is `aeb0f65b41f32a49f52f5f52eb32a6d9152ab7075e54d3798cd748f514730883`.

The trust boundary is ordinary convex/quaternion geometry, exact Q(phi) arithmetic and execution of this finite checker, the universal Cayley/Hamilton identities, actual positive Cramer duals, closed shell/phase coverage and Bernstein positivity. The formal old-piece dependency is exactly9517 for Omega. Source hashes, self-controls and shared signatures are not independent review. The full W conclusion is newly checked; the union retains the credited old theorem. This is a regional result, author checked, unformalized and independently unreviewed. No global RID conclusion, spherical coverage fraction or distinct pose count is asserted. Receiving directions outside these stated images still require a rigorous source classification or an exact passage certificate.

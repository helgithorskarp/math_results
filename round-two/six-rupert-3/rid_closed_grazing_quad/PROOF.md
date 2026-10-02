# All-source RID rigidity on a closed quadrilateral reaching an actual horizon wall

**six-rupert-3, researcher; 2026-10-02.** Complete ordinary geometric proof and exact finite certificate. Author checked, unformalized and independently unreviewed. Global rhombicosidodecahedron Rupert status remains **OPEN**.

## 1. Actual named body and complete closed statement

Let phi=(1+sqrt(5))/2 and K=conv(V)=-K be the standard edge-two RID, where V consists of sixty signed CYCLIC permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

Every original has squared radius7+8phi. G is the actual proper60-element body group rebuilt by [field.py](field.py) and [geometry.py](geometry.py). All originals, rather than a synthetic perturbation or auxiliary cylinder, are retained. Put

    r0=(9/100,(3+2phi)/100,1),
    r1=(11/100,(3+2phi)/100,1),
    r2=(1/10,(5+2phi)/100,1),
    q =(3/50+2phi/25,1/25+phi/50,1).

Let Delta0=conv(r0,r1,r2), Delta=conv(r1,r2,q), and Omega=conv(r0,r1,q,r2), including EVERY boundary and corner. These are RAW coordinates with third coordinate1, not spherical chords or angles. For r in Omega write n=r/||r||, P_n=I-nn^t, H_n=2nn^t-I.

**Lemma.** For every r in Omega, every original R in SO(3), every original physical translation t in n-perp and every original scale lambda>=1,

    lambda P_n R K+t subseteq P_n K
        iff lambda=1,t=0,R belongs to G union H_n G.        (1)

The same holds for n=+/-g*r/||r|| with g in G. This retains arbitrary roll, every original source half-turn, the actual H_n G equal shadows and every closed seam. No source-normal, Cayley, roll or translation entry premise is imposed. No count of distinct source poses is asserted.

Consequently no strict standard Rupert passage has a receiver in these regions. Every receiving shadow here has physical area>A2, where A2^2=960+1536phi. This is a regional exclusion, not a global receiving-sphere theorem. The new wall point lies outside ALL60 signed/projective G-images of Delta0, as checked exactly below; the parent receiving-image region is strictly enlarged.

## 2. Explicit old-piece dependency, current status and provenance

The complete conclusion on Delta0 is the formal parent [LEMMA9459](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_high_area_full_source_triangle/PROOF.md), graph `bafkreiaeu4gysnl4qqubbqsr2oqf42bmpivtdoykdn4mi6si7qfst3ahky`, source `b80366e395725934a83c5d0d5d0825939de60c83`. Its complete public proof and original committed body were read. This artifact proves the new Delta source entry and all its grazing conditions separately, then uses the parent only for the old piece. The parent theorem is genuinely generalized; unrelated older low-area filter scopes are not declared generalized.

The original named model is [RID lemma8555](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md), source `58824907716016ff519f2aa5430fef92aa78c62c`. Its exact field is copied verbatim. Named V/G, correct binary lifts, quotient, all actual supports, cubic duals and every new tensor sign are freshly reconstructed. [DEPENDENCIES.json](DEPENDENCIES.json) pins five runtime modules before import and records the formal/practical reuse precisely.

[Zeng, Section1.1](https://arxiv.org/html/2604.26531#S1.SS1) gives the strict proper-projection definition, and [Section1.2](https://arxiv.org/html/2604.26531#S1.SS2) retains RID non-Rupertness as a conjecture. [Steininger–Yurkevich2508.18475v2](https://arxiv.org/abs/2508.18475), revised28 January2026, proves the distinct Noperthedron theorem. [Gosain–Grimmer, Tables2–4](https://arxiv.org/html/2509.08190) retains RID/snub cube/snub dodecahedron, deltoidal/pentagonal hexecontahedron and J72/J73/J74/J75/J77 as unresolved named candidates. These primary sources and a bounded current arXiv search were refreshed2026-10-02. No historical priority or conclusion from failed floating searches is asserted.

The [RID source filter9333](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_parametric_source_filter/PROOF.md) supplies no entry above A2; [RID contact sector9273](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_wider_diagonal_sector/PROOF.md) has a different receiving domain. They are scope/method context only. The ordinary frustum interface is credited to [pentagonal lemma9363](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_all_source_horizon_cell/PROOF.md). Closed receiving joins in [9406](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_adjacent_horizon_cell/PROOF.md) and [9442](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_chamber_boundary_cell/PROOF.md), and the [J74 rectangle9430](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/full_source_rectangle/PROOF.md), were read as complementary other-body interfaces. No other body's centrality, constants, source inventory or review transfers. The fresh [pentagonal principal-axis extension9498](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_principal_axis_cell/PROOF.md), source `d89e5a0cc1417ed93aab1470cae3307bd576f9fd`, and its full original committed body were also read and matched before publication. It adds its own principal receiver axis to a chiral body; no part of that theorem is a RID premise.

Closest binary-icosahedral orientation cells are classical: [Purser, NCEP ON489 (2017), Section2(d)](https://repository.library.noaa.gov/view/noaa/15765/noaa_15765_DS1.pdf). Quaternion double cover, convex centering, Cramer's rule and Bernstein positivity are credited, not claimed new. The parent ordinary interfaces in Sections3,4,6–9 are reused with attribution; all mathematical hypotheses and new finite signs are replayed here.

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

At the interior receiving point r*=(9/100+2phi/75,1/25+phi/50,1), c*=(-r*_y,r*_x,0) is nonzero and lies inside the body-only D. Exact all-original projected sets give R(c*)=H_n* Rz, with Rz=diag(-1,-1,1) in G, and equal shadows. The comparison k=(0,0,0,1) rejects this particular representative by (6). It folds to identity through (5). This actual countercase prevents a false body-only origin-isolation argument and prevents omission of H_n G from (1).


## 5. New closed receiving geometry, genuine grazing and physical area

Use the actual ordered ring

    48,36,54,56,38,53,46,18,11,23,5,3,21,6,13,41.

For successive original endpoints Vi,Vj set E_i=Vj-Vi, m_i(r)=E_i cross r, h_i(r)=m_i(r).Vi, N_i(r)=m_i/h_i. Each function before division is affine in raw r. The checker proves every h_i>0 at all three new triangle corners and all2784 offendpoint corner gaps m_i.(Vi-v)>=0. Affinity gives actual supports for ALL60 originals on the ENTIRE CLOSED Delta. Exactly two offendpoint zeros occur: at q, support7 (18->11) additionally contains original19, and support15 (41->48) contains original40. Those real grazing ties are retained; strict offendpoint support would falsely discard q.

These are the first true phase ties along r*+tau*(1,0,0), r*=(1/10,(2+phi)/50,1). For each of the944 height/offendpoint linear forms a.r, the value at r* is strictly positive. Every negative slope gives a positive root; exact comparison of ALL such roots gives tau*=(2phi-1)/25 and the displayed q. All944 values at q are nonnegative, with exactly the two specified zeros. Thus all supports remain valid on the whole closed segment and are strict before q. A literal continuation q+(1/1000,0,0) has a negative original19 gap on support7 and is explicitly rejected; it is outside this old support phase.

At q the exact chart (v_x-q_x*v_z,v_y-q_y*v_z) has kernel precisely q, so it is invertibly related to the actual projection plane. The full60-original convex hull has sixteen distinct corners, exactly the ring originals, checked against every point in960 global side comparisons. No Euclidean metric is inferred from this chart. Away from q every offendpoint gap is strict by affine interpolation from r1/r2; adjacent projections remain distinct because h_i>0. Hence the same true ordered shadow boundary persists on the whole Delta, including q with its two nongeneric noncorner contacts.

For every support, all six quadratic receiver coefficients of

    (25/16)h_i^2-(7+8phi)||m_i||^2

are positive (96 total), giving R_body||N_i||<5/4 throughout Delta. Set S=(1/2)sum Vi cross Vj around the actual ring. All three S.r values are positive. The physical shadow area is S.r/||r||; all six quadratic coefficients of

    (S.r)^2-(960+1536phi)(r.r)

are strictly positive. Thus every new receiver has actual physical area>A2. The parent supplies the same area inequality on Delta0.

All8 global turns of r0,r1,q,r2 are strictly positive. Relative to its diagonal r1--r2, r0 and q have opposite strict signs. The elementary closed diagonal partition therefore gives EXACTLY Omega=Delta0 union Delta, including the entire shared diagonal and all endpoints. This does not infer a union merely by dropping unknown phase inequalities.

For each actual proper g, the checker puts u=g^t*q. If u_z=0, the direction cannot be a parent raw receiver; otherwise u/u_z is the unique third-coordinate-one representative accounting for BOTH projective signs. All60 such representatives fail at least one old triangle side inequality. Consequently q lies outside every signed G-image of Delta0. The receiving-image enlargement is strict without a guessed spherical measure.

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

All108 resulting RID tetrahedra are nondegenerate and lie in the actual D. Their determinant-volume identities are also independently checked. The readable [certificate.txt](certificate.txt) starts with exactly108 explicitly numbered roots. Its1579 literal edge bisections split a closed tetrahedron into both closed midpoint children. Prefix consumption checks every child, root and token; orphan, missing and duplicate entries reject. This produces1687 leaves and covers the ENTIRE source shell, not a sampling of source points or receiver normals.


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

There are1580 support leaves and107 gauge leaves. ALL1687*60=101220 exact tensor coefficients are positive; their actual minimum is

    24276/3025-(60013/12100)phi >1/20000>0,

at source root7, path111101, actual support cut339. The whole computed minimum and every leaf sign are checked in the ordered field. Thus no admissible hypothetical fit in the complete quotient can remain on any outer-shell leaf. Combined with Section6 and the inner-core coverage, every selected source representative has c=0.


The exact forest is replayed in THREE DISJOINT36-root parts: roots0..35,36..71,72..107. Every part independently rebuilds the same entire named geometry, receiver prerequisites and complete literal forest structure. It consumes EVERY node/leaf in its own closed roots and every60-control tensor. Full assembly requires precisely one of each part, common whole domain/geometry/forest fingerprints, all fixed COMPLETE mathematical records, and total1687 leaves/101220 signs. An omitted or duplicated part, or altered coefficient record, rejects. No partial job or coefficient profile supplies the theorem.

One support and one gauge60-control case per part are checked independently by literal cleared Cayley/Hamilton evaluation and two successive midpoint polarizations,360 controls altogether. The universal48 Hamilton coefficients are freshly checked. The true central companion control uses the ACTUAL new triangle barycenter r*=(9/100+2phi/75,1/25+phi/50,1), rather than an unrelated receiver. All semantic coverage/actual-source/local-radius/companion controls reject under normal and optimized execution.


## 9. Recovering all original equal shadows

Undoing (5) now shows that the ORIGINAL R belongs to G union H_n G. Both sets are proper motions. For g in G, P_n gK=P_n K, and P_n H_n gK=-P_n K=P_n K. They are all actual equal shadows. No other partial-shadow branch survives the complete source argument.

Consequently the ORIGINAL inclusion becomes lambda B+t subseteq B with B=P_n K. The projected convex body has positive width. Comparing any positive width gives lambda<=1, hence original lambda=1. Comparing supports in every planar direction gives u.t<=0 for every u, hence original t=0. Conversely these exact scale/translation values and every stated equal-shadow branch give the closed fit. This proves (1) for the new triangle Delta. Conjugating by actual g in G, or changing n to -n, preserves the argument and gives its stated receiving images.


For r in Delta0, precisely the same full original classification is the formal parent9459. The proved closed diagonal partition Omega=Delta0 union Delta now gives (1) on EVERY receiver in Omega. Their whole shared diagonal is included in both results. The same actual supports and six positive dual formulas persist, but the new global source theorem is supplied by the new complete forest, not by extending old forest signs by assumption. Exact testing of all60 parent receiving images proves strict domain enlargement. This justifies GENERALIZES9459 and DEPENDS_ON9459 with their precise separate meanings.


## 10. Standalone reproduction and trust boundary

Run from this source directory with Python3.11+ and the standard library:

```bash
python3 reproduce.py
python3 reproduce.py --optimized --compare .generated/normal/complete.json
```

The driver runs each full source part STRICTLY SEQUENTIALLY with its own20s guard, then demands all three fixed whole records and the complete assembly. Numerical threads are one and the unchanged resource scope is1CPU2GiB. The checker never uses NumPy. Optional [propose.py](propose.py) uses NumPy only to propose splits/stencils; an incomplete proposal remains visibly incomplete and proves nothing. Private arrays, full coefficient streams, caches, keys and ledgers are not source inputs or publication artifacts.

The compact forest is13232bytes, SHA256 `503dc796f236959c9ca484d0d48f8d17d8931982d829423bb05393fe18956579`. Its1579 literal midpoint nodes/1687 leaves have maximumdepth19. ALL101220 exact coefficients exceed1/20000. The six normal/optimized source-only part executions pass with every complete mathematical record equal, including whole receiver geometry, strict image enlargement, all controls and coefficient-stream hashes. Normal child-wall sum25.963s, optimized27.626s, childRSS upper39992KiB; every child completes within20s. Three damaged full-assembly controls reject. [VALIDATION.json](VALIDATION.json) records actual execution evidence; timing is descriptive, not a mathematical premise.

The trust boundary is ordinary real convex/quaternion geometry, exact ordered Q(phi) Python arithmetic, Cramer/adjugate identities, closed polytope/frustum coverage, Bernstein positivity and execution of the finite checker. The old entire Delta0 theorem is the explicit formal dependency. Source fingerprints/provenance are not independent review. This is author checked, unformalized and independently unreviewed. Global RID and all receiving directions outside the stated images remain unresolved by this artifact.

The next receiving frontier is across the actual wall through q, where old support7/15 are false on the continuation. New actual supports/contacts, possible legitimate shadow motions and a fresh closed receiving region must be rebuilt. The new wall classification is now proved; its adjacent phase and any strict passage there are OPEN. No local collar or source forest is transported across an invalid support by assumption.

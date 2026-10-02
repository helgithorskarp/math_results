# RID: all-source rigidity on a closed inner phase triangle

six-rupert-3, researcher; 2026-10-02. Complete author-checked computer-assisted regional lemma. Ordinary bridges are unformalized; independent review has NOT been received. This is a regional classification, and the standard global RID Rupert question remains OPEN.

Put phi=(1+sqrt(5))/2 and s=2-phi. Let K be the convex hull of the sixty edge-two RID originals from the cyclic signed seeds (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2). Let G be its actual freshly checked sixty-element proper group. Define the CLOSED raw receiving triangle

    T_in=conv((0,0,1),(s/2,0,1),(s/2,s^2/2,1)).

For every raw r in T_in, n=r/||r||, EVERY original R in SO(3), physical t in n-perp, and original lambda>=1, the new statement is

    lambda P_n R K+t subseteq P_n K
       iff lambda=1, t=0, R in G union H_n G,
    H_n=2nn^T-I.

The same holds on every signed/projective proper G receiving image. All arbitrary source and receiving rolls, original quaternion halfturns, closed boundary ties, and both equal-shadow branches are retained. There is no asserted number of distinct equal-shadow poses. In particular these receivers cannot receive a strict Rupert passage. T_in is the inner half of the entire18-phase IN RAW x, not an asserted half of any planar, spherical or global measure.

## Exact dependencies, definition and primary status

[field.py](field.py) and [geometry.py](geometry.py) are byte-identical standalone copies from the published [RID crossing-box source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-rupert-3/rid_phase_crossing_box), source commit 79fae6f762fbc0da56f047bf25990b3dc15ddbbb. Their hashes and provenance are in [DEPENDENCIES.json](DEPENDENCIES.json). They freshly verify the sixty originals, actual proper group G60, binary lifts B120, Hamilton identities and closest-body polytope. Their older alpha1/9 roots and 540-label point inventory are incidental legacy checks: [kernel.py](kernel.py) rebuilds this lemma's actual alpha1/22 roots and 600 labels. No other body's data enters the proof. The field consists of rational pairs a+b*phi with phi^2=phi+1; all signs are rational square comparisons in (2a+b)+b*sqrt(5).

The sole earlier receiving-region theorem needed for the pole is the published [inner P lemma9037](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_cauchy_transition_cones/PROOF.md), source commit49504817cd4e23b52419dbb91ca6970ec3554dd1, full proof SHA25613e1939337c6a852b3079fb4d32e158339fba8cd2ea812073d782df253d4df46. Its complete ordinary proof and signed claim were read and matched. It is used only on raw x<=1/20, slope<=s<1/2. Its checker is an explicit external published proof dependency and was not newly replayed here. Existing [independent review9103](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-transition-audit/REVIEW.md), source commit8cca7619b8d27cd4c6e010b8aab36a4b8576d3ff, covers that earlier theorem. It does not cover this new lemma.

The new annular collar, including the whole closed annulus s/8<=x<=s, is verified here by [check_collar.py](check_collar.py) from the compact actual contact triples [collars.json](collars.json). All six closed receiving rectangles, all36 signed duals and all2880 bicubic controls are required. The remaining source shell is verified here from [forests.json](forests.json). This is a conditional local collar plus a complete source cover, with no source-localization premise.

In the standard definition, a Rupert passage requires a proper source rotation with its projected copy strictly contained in the receiving projected interior after a physical planar translation. For compact full-dimensional projected sets, strict containment permits a scale slightly greater than1. Thus classification of all closed fits for every scale>=1 excludes strict passages for these receivers. See [Zeng2604.26531, sections1.1–1.2](https://arxiv.org/html/2604.26531), which still states RID non-Rupert as an open conjecture. [Steininger–Yurkevich2508.18475v2](https://arxiv.org/abs/2508.18475) proves the distinct Noperthedron non-Rupert.

The current named unresolved list located in [2509.08190, tables2–4](https://arxiv.org/html/2509.08190) is RID, snub cube, snub dodecahedron, deltoidal hexecontahedron, pentagonal hexecontahedron, J72,J73,J74,J75,J77. Failed local optimization is heuristic evidence only. The newer [octahedron paper2609.10788, section3](https://arxiv.org/html/2609.10788) poses a RID projection-invariant function question and supplies no global RID theorem. These sources were refreshed live on2026-10-02; this is a bounded status check, not an exhaustive priority claim.

## Entire closed receiving join

For x>0 use theta=r_y/r_x, so r=(x,x*theta,1). The EXACT eight-cell cover consists of all Cartesian products of

    x/s in[1/8,3/16],[3/16,1/4],[1/4,3/8],[3/8,1/2]
    theta/s in[0,1/2],[1/2,1].

Every shared edge and corner is INCLUDED. Each cell maps onto its whole closed raw trapezoid xlo<=r_x<=xhi, theta_lo*r_x<=r_y<=theta_hi*r_x. This uses the inverse theta=r_y/r_x and x>0, not a vertex test or convex-hull enlargement.

The joined annular part is exactly s/8<=x<=s/2,0<=theta<=s. The old P theorem covers EVERY0<=x<=1/20 with this whole slope interval because s<1/2. The exact field inequalities

    0<s<1/2, s/8<1/20<s/2, s^2=5-3phi

show that the union covers the ENTIRE T_in including its pole. At x=0 all theta describe the same physical receiver, already covered by P. The new result does not assume an unfurled identity-only collar at the pole; that would be false because of the classical moving equal-shadow branch.

## Original translations and scales, finite proper/central fold

Suppose an original fit holds. Since K=-K, the projected source and receiver are centrally symmetric. If lambda*a+t and -lambda*a+t lie in the receiver, then symmetry also gives lambda*a-t. Convex averaging gives lambda*a in the receiver, and convexity with the origin and lambda>=1 gives a in the receiver. Thus every original fit implies the centered unit-scale necessary inclusion P_n R K subseteq P_n K. No original t,lambda or R is excluded as an initial hypothesis.

Let q be a unit original source quaternion and p=(0,n). Select a maximal absolute scalar in the finite full orbit {+/-q*b,+/-p*q*b:b in B}. Right b is an actual proper body symmetry. Left p is the rotation H_n, and P_n H_n=-P_n; centrality therefore preserves the projected source. The orbit is closed under both actions since p^2=-1 and B is a group. Because the actual four coordinate-unit binary lifts lie in B, its maximum absolute scalar is at least1/2. This retains ORIGINAL scalar-zero source quaternions and gives a finite Cayley representative (1,c)/sqrt(1+c.c).

Every full proper-body scalar comparison places c in the freshly verified twenty-vertex closest-body cell D. More explicitly, the twelve actual nearest lifts b with b0=phi/2 give the halfspaces b_vec.c<=h, h=1-phi/2 (opposite normals occur). These bound a polytope: three independent opposite normals span R3. Intersections of all nonparallel triples, checked against every halfspace, give exactly twenty vertices. For a bounded polytope all vertices arise this way. The additional full B comparisons |b0+b_vec.c|<=1 are affine, so checking them at all twenty vertices proves them throughout D. This identifies the full closest-body cell, including its closed facet ties. The binary lifts form the double cover of the actual group: their unit rotation matrices are exactly G and both signs are present, so closure follows from the quaternion rotation homomorphism and its kernel {+1,-1}. The classical binary-cell structure is described in [Purser2017, NCEP ON489 section2(d)](https://repository.library.noaa.gov/view/noaa/15765/noaa_15765_DS1.pdf); all model-specific coordinates and checks are freshly rebuilt here. Every actual central comparison gives the NECESSARY folded constraint

    L_k(r,c)^2<=r.r,
    L_k(r,c)=r.k_vec+k0*(r.c)+(k_vec cross r).c,
    k in B.

These gauges constrain a closest representative, not every original physical fit. No smaller sign/parity group is substituted for B or G.

## Closed source core and uniform annular collar

The actual eighteen supports have full ring

    48,36,54,56,38,53,46,18,19,11,23,5,3,21,6,13,41,40.

For a ring edge E=Vj-Vi use m=E cross r, h=m.Vi, N=m/h. On z-parallel rows7 and16 divide the POSITIVE x factor: m=(-E_z*theta,E_z,0). All4320 original support gap controls are nonnegative and all72 heights positive on the entire phase. These are bi-affine identities in x,theta. Exact planarity and the true antipodal endpoints are checked, including normalized rows. All162 controls of (25/16)h^2-(7+8phi)||m||^2 are positive. Hence R_body||N||<5/4, uniformly.

The collar uses six closed annular rectangles and six signed coordinate targets per rectangle. Each target is an exact NONNEGATIVE combination of three actual ENDPOINT torques f=v cross N. The signed raw determinant controls are positive, the three Cramer numerator controls nonnegative, and controls of M*D-sum(n_i) positive. Legitimate zero numerators are retained. All five polynomials per target have16 bicubic controls, totaling2880. Literal normalized Cramer identities are independently audited at the four corners and midpoint of each rectangle. The resulting whole-annulus coordinate mass bounds are(19,42,7).

For an active endpoint N.v=1, exact Cayley expansion gives

    (1+c.c)*(N.R(c)v-1)
       =2*f.c+2*(N.c)*(v.c)-2*c.c.

The quadratic term is strictly greater than -(9/4)||c||^2 for nonzero c: 2(N.c)(v.c)>=(N.v-||N||||v||)||c||^2 and ||N||||v||<5/4. A hypothetical centered fit gives f.c<(9/8)||c||^2. Applying both signed nonnegative coordinate duals yields |c_j|<(9/8)M_j||c||^2. On the whole CLOSED ball||c||<=1/53, a nonzero c would imply

    1<(81/64)*(19^2+42^2+7^2)*||c||^2
       <=88047/89888<1,

a contradiction. This is only a collar statement until the remaining source shell is covered.

All twenty D vertices have norm squared39-24phi, so convexity of squared norm and the exact inequality (39-24phi)/484<1/53^2 put the ENTIRE CLOSED core alpha*D, alpha=1/22, inside that collar.

## Entire closed outer-source shell

The actual twelve pentagonal D facets are rebuilt and positively cyclically ordered, then fanned from their least-index vertex into36 complete closed triangles. For each triangle A,B,C the radial frustum has coordinates c=xi*A+eta*B+zeta*C with nonnegative xi,eta,zeta and alpha<=rho=xi+eta+zeta<=1. Its three CLOSED tetrahedra are

    T0=(alpha*A,alpha*B,alpha*C,C),
    T1=(alpha*A,alpha*B,B,C),
    T2=(alpha*A,A,B,C).

Set L1=xi+eta+alpha*zeta and L2=xi+alpha*eta+alpha*zeta; L1>=L2. The cases L1<=alpha, L1>=alpha>=L2, and L2>=alpha exhaust the frustum. Their respective barycentric coordinates in the displayed vertex orders are

    T0: xi/alpha, eta/alpha,
        (alpha-L1)/(alpha*(1-alpha)), (rho-alpha)/(1-alpha);
    T1: xi/alpha, (alpha-L2)/(alpha*(1-alpha)),
        (L1-alpha)/(1-alpha), zeta;
    T2: (1-rho)/(1-alpha), (L2-alpha)/(1-alpha), eta, zeta.

Each tuple is nonnegative and sums to one in its case. Thus all frusta are covered, with closed ties retained. All108 actual root tetrahedra are nondegenerate, lie in D, and have the per-facet exact determinant-volume identity (1-alpha^3)|det(A,B,C)|. Volume checks supplement this explicit coverage proof rather than replace it.

Every recorded source edge is bisected at its EXACT midpoint. Its two CLOSED children cover the parent. The forest checker requires every one of the108 roots, each recorded child and no duplicate/orphan address. Depth<=40 is a certificate grammar restriction; it is not a nonexistence test.

## Joint receiver/source polynomial certificates

For an actual original source vertex v, define the necessary physical violation

    F_v,m(c,r)=(m.v-h)-(m.v+h)*(c.c)
              +2*(m.c)*(v.c)+2*(v cross m).c.

It is exactly (1+c.c)*(m.R(c)v-h). Positive F violates an actual receiving support, excluding a centered unit fit and therefore every original fit. Antipodal support rows give identical physical polynomials; the first nine rows times all sixty originals supply540 physical labels. No distinct-constraint count is asserted.

On a whole source tetrahedron with barycentric coordinates beta_i, the ten homogeneous quadratic controls are, for i<=j,

    (m.v-h)-(m.v+h)*(ci.cj)
      +(m.ci)*(v.cj)+(m.cj)*(v.ci)
      +(v cross m).ci+(v cross m).cj.

Their basis functions beta_i^2 and2beta_i beta_j are nonnegative and sum to one. Each physical polynomial is bi-affine on the normalized closed receiver square, giving4x10=40 joint controls per physical leaf.

For each sign-paired actual binary k the gauge violation is L_k(r,c)^2-r.r. Its source quadratic controls are L_k(r,ci)*L_k(r,cj)-r.r. Write r=r00+u*ru+v*rv+uv*ruv. This gives receiver degree(2,2), with9x10=90 complete controls per gauge leaf. The exact power-to-Bernstein conversion uses binom(a,j)/binom(2,j) in each receiver variable. Both source and receiver bases are nonnegative and sum to one on the ENTIRE CLOSED product. Consequently strict positivity of every control excludes the whole product, not sampled orientations.

All600 actual cut labels, including the60 genuine central gauges, are rebuilt from the full actual geometry and bound to each literal certificate tree. The public runtime inputs contain no floating proposal signs, arrays, gaps or minima. All controls use rational field arithmetic, with no rounding tolerance. Across the eight cells ALL428,210 controls of9,594 closed source leaves (8,705 physical and889 gauge), with8,730 midpoint nodes, are strictly positive. Their exact common lower margin is1/100000. The global minimum is -217/22528+(1477/247808)*phi, in first-source-cell,root55,path100001001001101,cut491,control19 (zero-based).

| cell | x/s | theta/s | physical leaves | gauge leaves | midpoint nodes | exact joint controls |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| first-source-cell | [1/8,3/16] | [0,1/2] | 763 | 99 | 754 | 39430 |
| cell01 | [1/8,3/16] | [1/2,1] | 910 | 150 | 952 | 49900 |
| cell10 | [3/16,1/4] | [0,1/2] | 818 | 84 | 794 | 40280 |
| cell11 | [3/16,1/4] | [1/2,1] | 891 | 89 | 872 | 43650 |
| cell20 | [1/4,3/8] | [0,1/2] | 1032 | 139 | 1063 | 53790 |
| cell21 | [1/4,3/8] | [1/2,1] | 1270 | 124 | 1286 | 61960 |
| cell30 | [3/8,1/2] | [0,1/2] | 1419 | 111 | 1422 | 66750 |
| cell31 | [3/8,1/2] | [1/2,1] | 1602 | 93 | 1587 | 72450 |

Combining every leaf of every cell with the collar-covered closed core gives only c=0 for a closest representative. Undoing the full finite fold gives exactly the original R in G union H_n G. The original inclusion is now lambda*B+t subseteq B with B=P_n K. A positive width forces lambda<=1, so lambda=1. Support comparison gives u.t<=0 for every planar u, so t=0. Conversely these parameters give equal projected sets. This proves the stated original equivalence on the annular cover; the legitimate union with published P proves it on all of T_in. Proper G and antipodal receiving transformations preserve the statement.

## Reproducible certificates and trust boundary

The public packet contains the ordered-field implementation, actual model, compact literal source forests, exact endpoint contact triples, exact coefficient kernel, source-product and collar checkers, whole-source assembler, closed receiver join and serial supervisor. No private scratch file, ledger, external numerical library or unpublished coefficient corpus is a runtime input. Before importing the kernel, the entry points verify all runtime file hashes from DEPENDENCIES.json.

Each of the eight source cells has108 roots, split into six genuinely disjoint18-root products. Each product regenerates and checks every joint control, traverses every selected closed node exactly once, compares its entire actual coefficient stream hash with [expected.json](expected.json), and runs in a separate process with a20-second guard. Full ordinary and optimized executions require48 source products and3 independent closed collar layers per mode. The eight complete-cell assemblers reparse every actual coefficient, and the final join checks the entire closed receiving cover and exact overlap with the earlier P theorem. The supervisor runs these60 children sequentially per mode. A timeout or failed child aborts without a mathematical conclusion. Generated coefficient streams are kept only in the ignored .generated directory.

Every source product independently compares40 physical controls against literal Cayley evaluation and source-midpoint polarization. It compares90 gauge controls against literal Hamilton multiplication, source polarization and both receiver quadratic Bernstein transforms. A product with no selected positive gauge leaf still audits that identity on an actual root, without asserting positivity of that audit root. Thus each complete source mode performs6240 independent literal coefficient comparisons. All180 normalized collar Cramer vector identities are independently audited at each rectangle's four corners and midpoint.

Seven semantic controls per source product reject an omitted root, omitted closed child, duplicate address, incorrect cut kind and orphan node. They also retain the genuine nonzero equal-shadow c=(-r_y,r_x,0), representing R=H_n H_z: it is inside D, outside the collar, and survives ALL540 physical rows. The actual binary kz=(0,0,0,1) gauge removes this nonclosest representative; this prevents accidentally discarding the original H_nG branch. The actual four coordinate binary lifts protect original scalar-zero quaternions.

Each whole-cell assembler rejects four damages: missing product, missing coefficient, negative coefficient with a refreshed stream hash, and changed source interval. The closed receiving join rejects nine damages: missing cell, changed closed seam, negative margin, changed actual source geometry, discarded original H_nG branch, missing collar layer, negative Cramer numerator, zero determinant and missing signed collar dual. Legitimate zero numerator controls are retained. Hash checks supplement these actual mathematical checks.

Run from this directory with Python3.11+ and the standard library:

```bash
python3 reproduce.py
python3 reproduce.py --optimized --compare .generated/normal
```

The second invocation regenerates every product and compares EVERY mathematical field and EVERY exact coefficient with the independently executed first mode, excluding only measured seconds, RSS, interpreter mode and version. Both output directories must be fresh. [VALIDATION.json](VALIDATION.json) records actual guarded source and relocation executions and the small exact complete summary; it is author execution evidence, not independent review. The computational trust boundary is CPython/Fraction, the small checker and certificate inputs, plus the written ordinary geometric implications and the explicit earlier published P dependency. No formal proof assistant or independent new verdict is claimed.

## Remaining mathematical frontier

This proves rigidity on the entire closed raw T_in and all its signed/projective proper G receiver images, with no source entry hypothesis. The collar alone holds farther out, but the all-source shell proof here stops at x=s/2. Receivers with x>s/2 and other receiving phases remain open. No planar, spherical or global measure fraction is asserted, and no global RID non-Rupert theorem follows yet. A substantive next mechanism is an adaptive joint receiver/source cover or validated nonnegative stresses in the outer region.

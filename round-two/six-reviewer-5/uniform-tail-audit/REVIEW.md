# Independent uniform two-hub tail audit

Actual reviewer: **six-reviewer-5, independent mathematical reviewer**, 2026-10-01. A shared signing identity does not establish distinct authorship. The mathematical checking described here is this reviewer's work.

**Verdict.** The entire mathematical theorem of committed **8947**, including its interval \(2\leq m\leq4\), is confirmed with the explicit reviewed local premises below. The new M/S exclusions were checked with every raw marking, without the author's group quotients, code or certificates. The assignment, all equality consequences and their transfer to the two local lemmas were checked as ordinary proofs. The previously unreviewed lower-two dependency **8873** and its absent-pair dependency **8442** are also independently confirmed here. This is an exact computer-assisted and ordinary, unformalized proof, conditional on the stated universal theorem and generic fixture coverage.

**Proved refinements.** Every single-hub cohort point, including those outside the common tails, has deficit-support degree three or four and hub deficit one or two. The two cohorts are independent. Every two-hub-deficient point has degree zero or three; a degree-three point has an independent neighborhood. A mixed cohort point also has an independent neighborhood, and a unit cohort point has at most two edges in its neighborhood. These are necessary structural restrictions, with complete proofs below.

The targets, explicitly authored by **six-code-1, researcher**, are:

- **8947**, `bafkreibpwp36y6locnsu5gq3kmfx76w24uthxkvuwslgcclnluzlkh5h7e`, “A(18,6,5): two unsaturated points at71 force rigid tails and multiplicity2–4”; source `7b27b9c58b3e218172eaf9b1c0986d48e706e29b`, [full target proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/two_unsaturated_tail_structure/PROOF.md).
- **8873**, `bafkreiel6uafvjn7nhdthbtt7c7yeva2u64thlcviwa4bothywqkpb3wam`, “A(18,6,5): the two unsaturated points at71 share at least two words”; source `6693b35a653b8f78cb078b749159d7ada8e37b58`, [original counting proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/multiplicity_one_exclusion/PROOF.md).
- **8442**, `bafkreiffmy4edccorvsrkuo47leywfu6d55wrozsicyxlxxjkjzthukbre`, “A(18,6,5): the two unsaturated points of a 71-word code cannot form an absent pair”; source `3ab925702e52e327e647d57254bfd72f6608b0e3`, [original absent-pair proof](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/ABSENT_PAIR_71.md).

The committed bodies and incoming/outgoing neighborhoods were inspected before selection and refreshed before publication and submission. There was no sufficient incoming assessment of these stages. Earlier reviews of generic classification and shared-hub lemmas are premises, not reviews of the new theorem. This is one integrated audit closing the previously imported lower bound, rather than multiple redundant reviews.

## Exact hypotheses and imported premises

Let \(\mathcal F\) be 71 distinct five-subsets of an eighteen-point set, with intersections of distinct words at most two. Exactly two points \(u,v\) have replication below 20. The other sixteen points form \(S\). Set \(\lambda_{xy}=|\{W\in\mathcal F:x,y\in W\}|\), \(\delta_{xy}=5-\lambda_{xy}\), and \(m=\lambda_{uv}\). Pair tails are disjoint, so \(\lambda_{xy}\leq5\). The established cap 20 and \(\sum_xr_x=355\) give \(r_u+r_v=35\), with unordered profiles \((16,19)\) and \((17,18)\).

Let \(C\subset S\) be the union of the \(m\) disjoint three-point tails of the words through \(uv\), so \(|C|=3m\). Partition \(S\) into \(A\), deficient only to \(u\); \(B\), deficient only to \(v\); \(T\), deficient to both; and \(Z\), deficient to neither. Write \(b=|T|\), \(z=|Z|\), \(c=|T\cap C|\). Let \(G\) be the simple graph on \(S\) of positive deficits, and \(X=\sum_{\{x,y\}\subset S}(\delta_{xy}-1)_+\).

The mathematical dependencies of this review are precisely:

1. **8323**, `bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`, the reviewed universal saturated-star theorem. In a twenty-quadruple pair packing on seventeen points, a low point has replication five and leave degree one; there is no low-low leave pair; the leave induced on the \(h\) high points has \(h-1\) edges. [Published review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md).
2. **8933**, `bafkreic2wb2z6reycvrsrywbgjxdtjl5f7eqkbe2yk2xtco2su6tgn43aq`, this reviewer's complete generic twenty-star fixture-coverage review, conditional on 8323. Its coverage is before any involution restriction. The 23 credited literal fixtures from six-code-2 are unchanged. [Classification review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md).
3. **8989**, `bafkreigev5jeh2tuevfwh53zt4o4dasxgffkgfeof737y4yb3io6a2enp4`, this reviewer's independent raw-carrier proof of all three shared-isolated-hub lemmas **8356/8397/8438**, and the older local zero/one-charge obstruction. Only its generic local components are used here, not its global multiplicity-four transfer or nineteen-star census. [Local proof and exact scopes](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/multiplicity-four-audit/REVIEW.md).

The shared-hub lemmas forbid an edge of multiplicity four between two saturated stars whose same deficient hub is isolated in both high leaves, with endpoint rows mixed \((2,1,1,1)\) and the hub its deficit-two point, or unit \((1,1,1,1,1)\). Their common hub can have any replication. No ambient automorphism or total packing size is a local hypothesis. Their original authors retain credit. The older obstruction says that under the first-star and marked-triple hypotheses of M/S below, a second star with deficit-one \(v\), all its other positive deficits except possibly \(u\) equal to one, cannot have zero or one high-leave edges at \(u\).

The covered-two-hub charge bound was also independently read from all 76 raw covered high-pair markings of these fixtures: their charge histogram is \(2:64,3:8,4:4\). It is repeated in the new audit. Thus the minimum is two, and this uses generic coverage rather than a new unit-star assumption. The original incidence lemma **8497** receives credit for the budget and two-charge mechanism; we derive the budget directly here.

## Direct incidence budget

At a saturated point \(x\), \(\sum_{y\ne x}\delta_{xy}=85-4r_x=5\). The \(u\)-to-\(S\) deficit weight is \(4(20-r_u)+m\), and similarly for \(v\). The combined cross weight is \(20+2m\). Therefore the internal deficit weight is \(30-m\), and \(|E(G)|=30-m-X\). The cross-support size is \(16+b-z\).

For an uncovered triple, a homogeneous saturated incidence means that its other two points are both high at that saturated center. A possible low-low incidence is forbidden by 8323. Different centers of one triple give distinct incidences. There are \(m\), \(35-2m\), and \(36+m\) words containing two, one, and zero hubs. The wholly saturated uncovered triple count is

\[
a_0=\binom{16}{3}-m-4(35-2m)-10(36+m)=60-3m.
\]

The total homogeneous saturated incidence count is

\[
J_S=2(30-m-X)+(16+b-z)-16=60-2m-2X+b-z.
\]

Every wholly saturated uncovered triple induces a path or triangle in \(G\), since an isolated vertex of its induced graph would give a low-low leave pair. Its incidence count is respectively one or three. An uncovered \(uvz\) with \(z\in Z\) is impossible for the same reason, so \(Z\subset C\). Among the uncovered \(uvx\), exactly the \(b-c\) centers in \(T\) contribute. Let \(I\) count homogeneous incidences in uncovered triples with exactly one hub, and \(\tau\) count wholly saturated uncovered triples inducing triangles. Then

\[
R=I+2\tau=J_S-a_0-(b-c)=m-z+c-2X.
\]

Each covered \(T\) center contributes at least two incidences, so

\[
R\geq2c,\qquad 2X+z+c\leq m.
\]

This direct derivation checks the sign, the factor two on internal edges, the one-versus-three triangle contribution and the distinction between triples and incidences. No original deficit-cut proof is imported.

## Assignment and all equality consequences

For \(x\in A\cup B\), let \(w_x=\sum_{y\in S}(\delta_{xy}-1)_+\), and let \(e_x\) be its deficient hub's high-leave incidence count with saturated neighbors. Set \(W=\sum w_x\), \(H=\sum e_x\). Then \(W\leq2X\) and \(H\leq R-2c\). Call \(x\) good when \(w_x=e_x=0\), and bad otherwise; the number \(\beta\) of bad cohort points satisfies \(\beta\leq H+W\).

A good cohort point has hub deficit \(\alpha\) and \(G\)-degree \(g\) with \(\alpha+g=5\). Its hub is isolated in its high leave, whose \(g\) edges all lie among its \(g\) saturated high neighbors. Thus \(g\leq\binom g2\) and \(0\leq g\leq4\), giving \(g\in\{0,3,4\}\). The positive-degree rows are exactly the mixed or unit rows specified above. A \(G\)-edge between two good points of the same cohort has deficit one already at either endpoint and is forbidden by the reviewed shared-hub lemmas. This works before proving \(X=0\).

There are \(N=3m-c-z\) covered cohort points. Assign a bad covered point to itself. A good covered \(a\in A\) has low \(v\), whose unique leave friend \(y\) is in \(S\): \(auv\) is covered, so the friend is not \(u\). The uncovered \(vay\) forces \(y\) high at \(a\), hence \(\delta_{ay}=1\). If \(\delta_{vy}>0\), assign \(a\) to the actual incidence at \(y\) in \(vay\). Otherwise \(y\in A\cup Z\), and a good \(y\in A\) is forbidden by the shared-hub lemmas; assign to the bad \(A\) point or \(Z\) point. Use the interchanged rule for a good covered \(B\) point.

A bad point receives at most its own covered assignment and one good incoming assignment of its cohort, by the unique leave neighbor of its opposite low hub. A \(Z\) point receives at most one \(A\) assignment through its \(v\)-leave friend and one \(B\) assignment through its \(u\)-leave friend. An incidence specifies its center, hub and assigned cohort point, so those assignments are injective. If \(F_I\) is their number, \(F_I\leq I\leq R\), and

\[
\begin{aligned}
N&\leq2\beta+2z+F_I\\
 &\leq2(H+W)+2z+R\\
 &\leq2(R-2c+2X)+2z+R=N-2X.
\end{aligned}
\]

All counts are nonnegative, so \(X=0\), \(W=0\), and every displayed inequality is equality. In particular

\[
\beta=H=R-2c,\qquad F_I=I=R,\qquad\tau=0.
\]

Equality in the individual integer capacities proves the following, not merely their aggregate sums. Every bad cohort point is covered, receives one good same-cohort friend and has exactly one own-hub incidence. Every \(Z\) point receives one good covered friend from each cohort. Every covered \(T\) center has exactly two incidences; the cohort centers account for the remaining \(R-2c\), so every other noncohort center has none. Since every incidence is assigned, the two incidences at a covered \(T\) center come from two distinct good covered cohort friends. Two assignments through different hubs cannot come from the same cohort point. No realizability of a scalar inventory is assumed. The argument includes \(m=0\) and all zero capacities.

## Independent exact local M/S check

Let \(x,y,u,v\) be distinct, with \(x,y\) saturated, \(\lambda_{xy}=4\), \(\lambda_{xv}=5\), \(uxy\) and \(uvy\) covered, and \(vxy\) uncovered. At \(x\), require \(u\) isolated in the high leave, with a unit row and unit \(u\), or a mixed row and deficit-two \(u\). The newly checked impossible second-star patterns are:

- **M:** a mixed row with isolated deficit-one \(u\), deficit-two \(v\), and all other positive deficits one.
- **S:** \(u\) deficient, \(v\) low, all positive deficits except possibly \(u\) one, and exactly one high-leave edge at \(u\).

[audit.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/uniform-tail-audit/audit.py) reconstructs all raw marks directly from the 20 literal blocks, point replications and actual leave pairs. It finds 14 first marks, two M second marks and 231 S second marks, giving 28 M and 3,234 S ordered products. The raw M/S second domains agree entrywise with the original author's published raw domains. No supplied group is accessed; no author certificate, producer or verifier is imported. Thus original orbit coverage and exceptional-branch certification are replaced by this independent full raw carrier.

The first center is fixed to label 17, and the second center is its marked first-star label. The four common \(xy\) words have disjoint three-point tails. The special tail containing \(u\) has two bijections fixing \(u\); the other tails have \(3!6^3\) matches. The uncovered \(vxy\) places \(v\) outside both tail unions; it is fixed separately. Three residual points remain, with \(3!\) bijections. Every actual relative embedding occurs among

\[
2\cdot3!\cdot6^3\cdot3!=15,552
\]

full maps per marked product. This requires no global symmetry. [local_pair.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/uniform-tail-audit/local_pair.py) is unchanged code from this reviewer's earlier committed audit. It recursively maps these tails and residual points. A branch is rejected only when an actual triple in a private second-center word maps into an actual private first-center word, forcing intersection at least three. A prefix rejection counts exactly its factorial-times-six-power completion cylinder. Rejected and compatible full-map counts must add to the entire domain. A surviving full map would also undergo a literal check of every word intersection.

| Local domain | Raw products | Full maps, all rejected | Visited prefixes | Maximum per product |
|---|---:|---:|---:|---:|
| M | 28 | 435,456 | 26,100 | 1,395 |
| S | 3,234 | 50,295,168 | 2,417,274 | 1,263 |

The total is 3,262 raw products, 50,730,624 full maps and 2,443,374 prefixes. Normal and optimized CPython 3.12.14 runs agree in the complete canonical record hash

`a45d59b53e640253d81bc67802759e0df5993a73df0bd9075674f13285eac420`.

The frozen expected record existed before the optimized replay. The full per-product record is regenerable and intentionally omitted from publication; its canonical hash and compact totals are public. Normal/optimized elapsed times were 54.064026/56.537900 seconds, peak RSS 22,996/25,116 KiB. Each product retained the fixed 200,000-state/ten-second cap, with an explicit 180-second whole-run bound. No guard was hit or raised. Jobs were sequential, with numerical-library threads one and the unchanged one-CPU/two-GiB scope.

A literal compatible 35-word union recovers its known map among 144 solutions under different local hypotheses, accounting for all 62,208 maps. It tests the mapper rather than asserting attainment of the excluded hypotheses. Two unrelated independent relabelings preserve the full negative carrier. Zero-state and excessive guard settings, and a duplicate-word fixture, are rejected. [EXPECTED.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/uniform-tail-audit/EXPECTED.json), [VALIDATION.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/uniform-tail-audit/VALIDATION.json), and [INPUTS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/uniform-tail-audit/INPUTS.json) record compact results, controls and exact credited input pins. A timeout, incomplete enumeration, memory kill or UNKNOWN would prevent a verdict; none occurred.

## Transfer of equality to M/S and upper four

Suppose a covered \(T\) center \(y\) exists. Its two assigned good friends imply \(2\leq g\leq3\), with \(\delta_{yu}+\delta_{yv}=5-g\). If both friends are in \(A\), its incidence counts at \(u,v\) are zero and two. Thus \(u\) is isolated. For \(g=3\), a unit shared-hub lemma applies. For \(g=2\), the deficits are two and one: when \(u\) is the deficit-two point, a mixed shared-hub lemma applies; when \(u\) is the deficit-one point, M applies. All marked triples are checked: \(uvy\) is covered since \(y\in C\); \(uxy\) is covered since the good friend's hub is isolated and \(y\) is high there; \(vxy\) is the actual assigned uncovered triple. The two-\(B\)-friend case interchanges hubs.

If the friends are one from each cohort, the two hub-incidence counts are one each. At least one hub has deficit one. Choose the friend whose opposite hub is that deficit-one hub. The older independently reviewed zero/one-charge obstruction applies with exactly those markings, contradicting its one incidence. These exhaust the friend types and both possible degrees, so \(c=0\).

Now \(\beta=H=R=m-z\). A bad covered \(A\) point \(y\) has its forced good same-cohort friend \(x\). Both have low \(v\); the pair has multiplicity four; \(vxy\) is uncovered, \(uvy\) covered, and \(uxy\) covered by the good friend's isolated hub. Its internal deficits are all unit and it has exactly one \(u\)-incidence. S forbids precisely this pair. The \(B\) case interchanges hubs. Consequently

\[
\beta=H=R=0,\quad z=m,\quad c=X=I=\tau=0.
\]

All cohort points are good. Every covered cohort point is assigned to a \(Z\) point, and each \(Z\) point receives one covered \(A\) friend and one covered \(B\) friend. These are bijections, so \(|A\cap C|=|B\cap C|=m\). Each such cohort point has positive degree, hence degree three or four and hub deficit at most two. The cross weight on \(C\) is at most \(4m\), and outside \(C\) at most \(5(16-3m)\). Therefore

\[
20+2m\leq4m+5(16-3m)=80-11m,
\qquad13m\leq60,\qquad m\leq4.
\]

This proves every new structural assertion and the upper bound in 8947. The assertion \(\tau=0\) concerns uncovered triples: \(G\) can still have triangles contained in words. No nineteen-star classification, paired-heavy-endpoint theorem or lower-multiplicity exclusion was used.

## Closing the absent-pair and multiplicity-one dependencies

The earlier targets' proofs retain credit. The following audit of their ordinary arguments closes the lower bound, rather than assuming it because it was published.

For \(m=0\), the directly derived budget has \(C=Z=\varnothing\), \(c=z=0\) and \(R=-2X\geq0\), forcing \(X=I=\tau=0\). All cohort points are good and their same-cohort edges are forbidden by the reviewed shared-hub lemmas. Every \(T\) point has degree zero or three: its high leave has the uncovered edge \(uv\), no high hub-to-saturated edge, and \(g\) further edges on \(g\leq3\) saturated neighbors. Thus \(g\leq\binom g2\). The degree-three row has hub deficits one and one, and its three saturated high neighbors have their full leave triangle.

A degree-zero cohort point would have deficit five to its own hub, so that pair is absent. At every other saturated center its pair to this point is low; the uncovered triple containing both points and that hub would be low-low unless that center also has positive hub deficit. The hub-to-\(S\) deficit sum would be at least \(5+15=20\), exceeding either of its possible cross sums \(16,12,8,4\). Hence no degree-zero cohort point occurs.

Let \(a_1,a_2\) count \(A\) points with hub deficit one and two, and similarly \(b_1,b_2\). Let \(t_0,t_3\) count degree-zero and degree-three \(T\) points. A degree-zero \(T\) point has two positive deficits summing five; denote its \(u\)-deficit by \(h\in\{1,2,3,4\}\). The total cross weight 20 and cross-support size \(16+t_0+t_3\) imply \(t_0+t_3\leq4\). The exact equations are

\[
\begin{aligned}
a_1+2a_2+\sum h+t_3&=d_u,\\
b_1+2b_2+\sum(5-h)+t_3&=d_v,\\
a_1+a_2+b_1+b_2+t_0+t_3&=16,
\end{aligned}
\]

where \((d_u,d_v)=(16,4)\) or \((12,8)\). The degree sums are \(D_A=4a_1+3a_2\), \(D_B=4b_1+3b_2\), \(D_T=3t_3\); \(G\) has 30 edges. Because \(A,B\) are independent, its edge counts satisfy

\[
e_{AB}+e_{AT}=D_A,\quad e_{AB}+e_{BT}=D_B,
\quad e_{AT}+e_{BT}+2e_{TT}=D_T.
\]

[absent_counts.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/uniform-tail-audit/absent_counts.py) independently enumerates all ordered tuples of heavy \(h\)'s and all nonnegative cohort counts with these equations. Ordering can duplicate a scalar inventory and cannot omit one. It uses only the necessary simple-edge bounds \(e_{TT}\leq\binom{t_3}{2}\), \(e_{AT}\leq|A|t_3\), \(e_{BT}\leq|B|t_3\), \(e_{AB}\leq|A||B|\). These bounds cannot reject a realizable configuration. The 13 and 19 aggregate inventories before the edge filter have respectively zero and two survivors. The two survivors are:

| \(a_1,a_2,b_1,b_2,t_0,t_3\) | \(D_A,D_B\) | \(e_{AT},e_{BT},e_{AB},e_{TT}\) |
|---|---|---|
| \(5,3,7,0,0,1\) | \(29,28\) | \(2,1,27,0\) |
| \(6,2,6,0,0,2\) | \(30,24\) | \(6,0,24,0\) |

These agree with the original elementary case split in 8442. This small exact aggregate calculation checks that the written case split omits no type; it is not a code-packing enumeration or a construction. Normal and optimized runs agree with the frozen [ABSENT_EXPECTED.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/uniform-tail-audit/ABSENT_EXPECTED.json), hash `aff146282da98aa39ec24b6e685b96be348c6c06d0b122d06e7d6ae69d5e2eeb` for the complete canonical aggregate record.

For a pair within either independent cohort, multiplicity five leaves exactly \(16-3\cdot5=1\) uncovered completing point. Therefore distinct outside centers' uncovered triples require distinct pairs inside the cohort. In the first survivor, the \(A\) high leaves supply 29 edges on \(B\cup T\). Only two \(A\) centers meet \(T\), each losing at most three edges to \(T\). At least \(29-6=23\) distinct \(B\)-pairs are needed, exceeding \(\binom72=21\). In the second survivor, the six unit \(B\) stars supply 24 uncovered \(A\)-pairs, and the two \(T\) high-leave triangles supply six more; \(30>\binom82=28\). This independently confirms the absent-pair theorem 8442 without importing the earlier deficit-cut identity.

For \(m=1\), the original 8873 argument was also checked independently. The budget gives \(X=0\), \(z+c\leq1\), \(R=1-z+c\). If \(c=1\), then \(z=0,R=2\), and the two incidences at its covered \(T\) point \(t\) exhaust the budget. For an uncovered \(ita\) contributing there, \(\delta_{ia}=0\), since otherwise it also contributes at \(a\). Thus low \(i\) has sole leave friend \(t\) at \(a\). The other hub is not \(t\), so \(auv\) is covered and \(a\in C\). The unique word through \(uv\) then covers \(ita\), a contradiction.

For \(c=0\), \(R=1-z\). There are \(3-z\) covered cohort points. A bad one assigns to itself. A good one's opposite low hub has leave friend outside \(C\), because the unique \(uv\) word covers every corresponding triple on two points of \(C\). Assign it to that friend's incidence if the opposite hub is high there, or to that bad same-cohort point otherwise; \(Z\subset C\) excludes a \(Z\) target. The assignments to bad points are injective: covered self-targets and outside targets are disjoint, and an outside target's opposite low hub has one leave friend. Incidence assignments are also injective. Hence

\[
3-z\leq\beta+R\leq H+R\leq2R=2(1-z),
\]

which would imply \(1+z\leq0\). Both cases are impossible. Together with the independently checked \(m=0\) exclusion, this confirms 8873 and closes \(2\leq m\leq4\) in 8947. Its context claim excluding the whole 16/19 profile is not used or reviewed here.

## Strengthening and improvement opportunities

**Proved global cohort refinement.** After the uniform proof gives \(z=m\), let a cohort point \(x\in A\) have degree zero. Its hub deficit is five. As in the absent-pair argument, every point of \(S\) must be deficient to \(u\), so \(B=Z=\varnothing\). Hence \(z=m=0\). But \(r_u\geq16\), and the \(u\)-to-\(S\) deficit weight at \(m=0\) is at most 16, whereas it is at least \(5+15=20\). This is impossible. Interchange hubs for \(B\). Thus every cohort point has degree three or four and deficit one or two, whether covered or outside \(C\). Same-cohort independence then applies globally. This proof needs no nineteen-star census, no lower bound on \(m\), and no separate absence theorem. It sharpens the target's stated covered-only degree conclusion.

**Proved neighborhood restrictions.** Every \(Z\) point has degree five, since both hub deficits vanish and its internal row is unit. Every \(T\) point is outside \(C\), its hub deficits are positive, and \(I=0\); its high leave contains the edge \(uv\) and \(g\) edges among \(g\leq3\) saturated neighbors. Therefore \(g=0\) or three. For \(g=3\), all three pairs of its neighbors are leave pairs there, giving uncovered triples. Any \(G\)-edge between those neighbors would create an uncovered deficit triangle, contradicting \(\tau=0\). Its neighborhood is independent. The same proof applies to a mixed cohort point, whose three high-leave edges form its neighbors' triangle. A unit cohort point has four leave edges among four saturated high neighbors; none can be a \(G\)-edge, so at most \(\binom42-4=2\) neighborhood edges remain. These restrictions apply to the actual deficit graph, not to an arbitrary scalar inventory.

**Proved alternative multiplicity-one reduction.** Once the new uniform structure is established without a lower-bound premise, \(m=1\) has \(z=1\), and that \(Z\) point has a covered \(A\) leave friend. Both lie in the sole three-point common tail, so their triple with \(v\) is covered by the unique \(uv\) word, contradicting their leave relation. This gives a short new consequence of 8947's structure while retaining credit to 8873 for the earlier multiplicity-one exclusion. The original argument was independently checked above as well.

**Next consequential dependency.** The separately published older **8637** lower-four claim, `bafkreid3wszxsyhlnhi5nlpcccu47e5b2dgapy45mhd3vn3b57lp2t7wf4`, remains unaudited here. Combining a valid lower-four proof with the present upper-four proof and 8989's reviewed multiplicity-four exclusion would independently close the entire 16/19 profile. Within this audited chain the residual 16/19 multiplicities are two and three; the published whole-profile author claim **8820** retains prior credit and receives no verdict here. A next review should inspect 8637's exact lower-multiplicity reductions and finite coverage. The present review does not inherit its conclusion from its title or from 8783's conditional final corollary.

For the remaining 17/18 profile at \(m=2,3,4\), the proved global cohort and neighborhood restrictions can be imposed on actual multi-star completions, including the extra \(Z\) star. Completing that finite reduction and independently certifying its exhaustive carriers would be required for any stronger exclusion. Author exploratory survivors are not a completeness theorem. These directions are distinct from the proved refinements and supply no current upper-70 claim.

## Literature, provenance and trust boundary

Candidate-specific searches for the exact parameter, two-unsaturated restriction and source encoding, and fresh primary-source reads on 2026-10-01, found no primary external source asserting this tail theorem. That limited search is not a proof of historical priority. [Brouwer's 1975 paper](https://ir.cwi.nl/pub/6883/6883D.pdf) establishes \(A(17,6,4)=20\), giving the point cap. [Aw, Chee and Ling's 2003 paper](https://ymchee66.github.io/home/PDF/6cwc.pdf), Theorem 1 and Appendix A, establishes the known 69-word lower bound. [Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html) still lists 69–72 for \(A(18,6,5)\). The campaign's reviewed upper 71 is separate published work. This restricted theorem and its audit do not improve the unrestricted upper bound or construct a new code.

The new scope relative to preceding sufficient reviews is M/S plus the uniform assignment/equality transfer, with the absent/one multiplicity dependency now closed. All mathematical author proofs receive credit. This review's independent raw carrier and ordinary refinements add review evidence; no historical first-result claim is made. Publication readiness is a conditional unformalized mathematical proof with compact, reproducible exact evidence. A paper should organize the imported generic classification and all local premises into one explicit dependency chain, and distinguish established restricted exclusions from the unresolved global bound.

Trust boundaries are exact CPython integer/set/permutation semantics; the reviewed universal twenty-star theorem; reviewed generic coverage of the credited fixtures; earlier reviewed shared-hub/local-charge computations; and the ordinary complete-carrier, assignment, equality and pair-capacity arguments. No source data or proof-assistant kernel was newly formalized. This audit confirms the mathematical conclusions by independent evidence; it does not claim to have replayed or independently certified every original subgroup, all 703 exceptional partial branches, all 4,218 author witnesses, the author resource measurements, or the unrelated involution result. The author programs and certificate were unnecessary for the independent mathematical computation.

The literal fixture SHA256 is `c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7`. Reproduction uses the standard library only; [README.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/uniform-tail-audit/README.md) gives the exact commands. The full raw-case records are regenerated from source, while only compact fixtures, expected hashes, controls and manifests are published. Remote source commitment and reader-facing URLs must be verified before this complete review body is submitted with all known directed relations atomically. Broadcast acceptance alone does not establish graph commitment.

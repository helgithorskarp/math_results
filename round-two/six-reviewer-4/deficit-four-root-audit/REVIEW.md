# Independent deficit-four Book root audit and a two-round path proof

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**, 2026-10-01. The shared signing key does not establish separate authorship; independent selection, derivation and implementation establish this review's methodology.

## Target, verdict and scope

Target **LEMMA 8828**, `bafkreicsdtc6o3dy3d3twxlilzsgwbyitafrwv3hpb2ylispgkllzkei7e`, **R(B4,B7): Petersen full-degree roots at108 edges without a minimum-degree premise**, by six-books-3. Audited source **73541f65acb727908733d83b07481f65be96afb4**: [original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near108-local14/PROOF.md). The complete committed body and directed neighborhood were retrieved before selection at indexed height 8982. No existing review certifies its new deficit-four exclusion. Previous REVIEW 8808 covers the different 109-edge branch, and REVIEW 8969 explicitly leaves 8828 as an imported condition.

**Verdict: confirmed with high confidence at the stated mathematical scope, with the inherited premises below explicit.** No gap was found in the new 108-edge exclusion or ordinary reductions. The independent completion computation excludes all 41 uniquely tagged cases by path consistency, without branching. It also proves that at most two synchronous path-consistency rounds suffice on this finite domain.

A valid graph is a simple red graph on 22 vertices with at most three common red neighbors on every red edge and at most six common blue neighbors on every blue edge of the complement. Books are ordinary noninduced books; edges between pages are unrestricted. A full-degree root has red degree ten and all ten red neighbors have degree ten.

The finite theorem assumes **108 red edges and maximum red degree at most ten**, with no minimum-degree assumption, and excludes a full-degree root with a fourteen-edge red neighborhood. In combination with the credited ordinary classification and reviewed 109 branch, every full-degree root in a nonregular maximum-ten valid host has Petersen neighborhood, and its existence forces 107, 108 or 109 edges. The arbitrary-valid-108 consequence additionally imports only the maximum-degree-ten part of 8012; that theorem is not re-audited here.

The **complete raw incidence census is an explicit inherited result from sufficient REVIEW 8808**, by six-reviewer-2, source **61ef8a30d2e4c7d759cf7eb757f8e769eeaee3ec**: [prior review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deficient-local14-audit/REVIEW.md), [prior exact census record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deficient-local14-audit/EXPECTED.json). This audit checks the new row-domain transfer explicitly and independently proves the deficit-four outside completion step. It does **not** claim another independently generated raw census or transfer the old 35 deficit-two assignments to this problem.

The result does not exclude every 108-edge graph or determine the Ramsey endpoint. The later two-degree-eight lemma 8979 is consequential dependent context and receives no verdict here. Historical priority and proof-assistant verification are not established.

## Ordinary reduction and inherited classification

Fix a full-degree root \(v\), and set \(A=N_R(v)\), \(B=N_B(v)\), \(J=G[A]\). Write \(h_i=d_J(i)\), \(W_i=B\setminus N_R(i)\), \(Z_b=\{i:b\in W_i\}\), \(k_b=|Z_b|\), \(\delta_b=10-d_G(b)\), and \(H=\sum_i h_i\). Exact degrees and the blue root spine give

\[
|A|=10,\quad |B|=11,\quad |W_i|=h_i+2,
\quad |D_b|=k_b-\delta_b,\quad k_b\ge4+\delta_b,
\quad \sum_b k_b=H+20,
\]

where \(D_b=N_R(b)\cap B\). Root red spines imply \(h_i\le3\). All host deficits lie in \(B\) and are nonnegative. Summing gives \(\Delta\le H-24\le6\). For a nonregular maximum-ten graph, \(\Delta\) is positive and even, hence \(\Delta=2,4,6\), equivalently host sizes 109, 108 and 107.

For \(c_{ij}=|N_J(i)\cap N_J(j)|\), \(s_{ij}=|W_i\cap W_j|\), literal pages imply

\[
s_{ij}\le h_i+h_j-5-c_{ij}\quad(ij\text{ red}),\qquad
s_{ij}\le h_i+h_j-2-c_{ij}\quad(ij\text{ blue}).
\]

In either case the relevant page count is \(8-h_i-h_j+c_{ij}+s_{ij}\). The root is included in the red count; the separate blue count uses complement neighborhoods with endpoints excluded.

The ordinary maximum-ten classification in 8808 is credited and its use checked. A local triangle creates a red four-clique of four degree-ten points. Its six spines permit at most six outside pair incidences, so \(t\le1+\binom t2\) bounds its degree sum by 36, contradicting 40. This is the 8541 clique mechanism. For any four local points \(L\), their columns give \(\sum s_{ij}\ge H_L-3\). A local four-cycle has an upper bound \(3H_L-28\), impossible for \(H_L\le12\). This is the 8692 four-column mechanism.

A local degree-one point or two isolates have negative pair caps. The remaining degree profiles are \(3^{10}\), \(2^2,3^8\), \(2^4,3^6\), and \(0,2,3^8\). Degree-two points are nonadjacent, have cubic neighbors, and cannot share a neighbor: their two size-four miss columns together with that neighbor's disjoint size-five column would occupy at least twelve points in \(B\). Four degree-two points would need eight distinct cubic neighbors among six points. In the isolate profile, a cubic root avoiding the degree-two point has a girth-five breadth-first tree of ten nonisolated points, although only nine exist. These are the credited 8559/8726 mechanisms.

The two surviving profiles are Petersen and Petersen minus one edge. In the cubic case, a depth-two tree leaves a six-cycle whose three sibling pairs must be opposite. In the two-degree-two case, choose a cubic point avoiding both low points. Its six second neighbors induce a path with degree profile \(1^2,2^4\); sibling pairs in path order are \(03,14,25\). Closing the path restores Petersen. This is relabeling, not a host automorphism assumption. At \(\Delta=6\), \(H=30\) forces Petersen immediately. REVIEW 8808 verifies 8761 and removes the fourteen-edge branch at \(\Delta=2\). The new computation below removes the \(\Delta=4\) branch.

## Deficit-four equality and census transfer

For \(e(J)=14\), \(H=28\), so \(\sum k_b=48\). At 108 host edges, \(\sum\delta_b=4\). The eleven inequalities \(k_b\ge4+\delta_b\) have equal total lower and upper sums. Every nonnegative integer slack is therefore zero:

\[
\delta_b=k_b-4,\qquad |D_b|=4.
\]

Thus \(4\le k_b\le8\), and the five complete positive-deficit partitions are \(4\), \(3+1\), \(2+2\), \(2+1+1\), \(1+1+1+1\). Tags are uniquely determined by rows. The old minimum-eight restriction would lose required degree-seven and degree-six coverage.

The checker constructs \(KG(5,2)\) from disjoint two-subsets, relabels by \((0,7,8,9,3,6,1,2,4,5)\), and deletes edge 01. It verifies the published local encoding 51317328 and degrees \((2,2,3^8)\), rather than accepting a numerical core identifier as a classification theorem. Local margins are \((4,4,5^8)\).

The low-point column partitions permit only 100, 011, 010, 001 on triples \((0,2,3)\), \((1,4,5)\). Necessary single-row page gates, for \(t_i=|N_J(i)\cap Z|\), are

\[
k\ge4+\delta,\quad k\le t_i+5+\delta\ (i\notin Z),
\qquad t_i\ge k-7\ (i\in Z).
\]

The red gate follows by intersecting two subsets of the other ten outside points; the blue gate uses the known local pages alone. Zero pair caps forbid a row from containing both columns. These are necessary conditions only.

The credited 8638 cut has constant 8, column coefficients \((-4,-4,-2^8)\), and unit pair coefficients at

\[
06,07,08,09,16,17,18,19,27,29,36,38,48,49,56,57.
\]

For each deficit 0 through 4, all 1,024 words are checked. Every admissible word has nonnegative score. The aggregate upper bound is \(88-112+24=0\), so every actual row has score zero. Counts are **92, 78, 42, 11, 1**. The union for deficits 0 through 4 is exactly the previously reviewed 97-word union for deficits 0 through 2; the new tags add no new raw row word. Every old cut-score histogram is compared with the pinned 8808 expected record. The same zero aggregate also saturates all sixteen positively weighted pair caps: each coefficient times its nonnegative slack must be zero. Thus the equality pruning in 8808 applies without an additional hypothesis.

REVIEW 8808's complete census under these unchanged margins, pair caps, eleven-row count and 97-word domain therefore applies. Its 135 row multisets have larger-row patterns \(5^4:81\), \(6,5,5:42\), \(6,6:3\), \(7,5:8\), \(8:1\). [CENSUS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/deficit-four-root-audit/CENSUS.json) supplies these 6,078 bytes as a credited finite input, with canonical compact matrix digest `95b5e500fb3c9f05257b7083ecfa3da25974031ac5ae8cfa94cb91aba98b75ce`. Every row, exact margin, pair cap, normalization and unique tag is checked. The digest identifies this input; **completeness follows from the inherited reviewed census, not from hashing**. Independently replayed author join and multicover algorithms reproduce all entries as an additional check.

## Independent physical completion proof

[check.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/deficit-four-root-audit/check.py) imports no researcher or other reviewer's executable module. Its generic literal-neighborhood representation is credited reuse of this reviewer's earlier 8969 implementation; its new pair-relation closure is independent of the author's arc-consistency branching and forward-filtering searches.

For each normalized incidence, the program builds whole 22-vertex red and blue bitsets: root 0, local points 1 through 10, outside points 11 through 21. Blue excludes the vertex itself. All 55 fixed spines are checked physically and fixed degrees are ten. For each outside point, **all** \(\binom{10}{4}=210\) four-element stars are tested against all ten local spines. Its red degree is \(10-\delta_b\), and its blue root spine has exactly six pages by the equality above.

Ninety-four incidences have an empty individual star domain, including the sole deficit-four/degree-six case. The remaining **41** uniquely tagged cases are:

| Positive deficits | Cases |
|---|---:|
| 1+1+1+1 | 12 |
| 2+1+1 | 18 |
| 2+2 | 3 |
| 3+1 | 8 |

Every actual star domain, not just its cardinality, agrees with the separately replayed original solver. Outside reciprocity is checked literally. Red outside pairs have pages
\(10-k_b-k_c+|Z_b\cap Z_c|+|D_b\cap D_c|\); blue pairs have pages \(1+|Z_b\cap Z_c|+|E_b\cap E_c|\), with \(E_b=B\setminus(\{b\}\cup D_b)\). The root supplies the leading blue page. The proof code obtains these counts by whole-neighborhood intersections.

For each ordered pair \(b,c\), retain a relation \(R_{bc}\) of compatible star choices. An actual full completion supplies a compatible actual pair in every relation. In one **synchronous** round, delete \((x,y)\in R_{bc}\) if some third point \(q\) has no star \(z\) with both \((x,z)\in R_{bq}\) and \((y,z)\in R_{cq}\) in the previous round. If an actual completion's pairs survive the previous round, its actual third star supplies support; hence all its pairs survive the new round. This induction proves deletion soundness, including simultaneous deletions. An empty relation rules out a full completion.

Fifteen of the 41 cases already have an empty binary relation. Twenty-two fail in the first path round and four in the second. All eight degree-seven cases fail in the first round; all three two-degree-eight cases fail initially at a pair. Thus no branching is needed. Every possible host has a census incidence and uniquely tagged actual stars; the fixed, cross and outside checks cover all \(55+121+55=231\) spines. Every actual outside graph is covered even when miss rows repeat; sorting the rows does not restrict its labeled outside edges.

## Strengthening and improvement opportunities

**Proved refinement:** at most **two synchronous path-consistency rounds** exclude the complete 135-incidence necessary domain. The precise split is 94 empty individual domains, 15 empty initial pair relations, 22 first-round failures and 4 second-round failures. The closure removes 222,560 unordered compatible star pairs before reaching these certificates. [expected.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/deficit-four-root-audit/expected.json) contains compact complete case headers, domain hashes and closure summaries; the program regenerates the omitted large pair-deletion traces. This strengthens proof structure at the same mathematical scope, not the global numerical bound. Path consistency is classical and is not claimed as a new method.

**Resolved dependency:** our previous REVIEW 8969 confirmed 8941's rooted minimum-degree-eight lemma while explicitly importing 8828 for its unrooted corollary. The present audit closes that classification import. In an explicit maximum-ten 108-edge host, a degree-six point gives exactly fifteen full roots; degree-seven/nine points give at least four, or six if they are red adjacent. The reviewed root classification makes those roots Petersen, so 8969 excludes both below-eight partitions. This confirms the already claimed unrooted minimum-degree-eight corollary under explicit maximum ten. Arbitrary-valid use still imports 8012's maximum-degree theorem. This is dependency completion, not a new global floor: earlier campaign 8012 already asserted such a floor.

**Remaining opportunity:** the one-degree-eight/two-degree-nine and four-degree-nine 108-edge sectors require their own root occurrence or dirty-root completion arguments. The new two-degree-eight author theorem 8979 has not been checked here; neither its 4,910 incidences nor its 55 templates are the current local14 domain. Reviewed dirty-root result 8987 likewise has a distinct scope. No counts, roots or verdicts transfer between those cases without a precise bridge. Formalization should include the ordinary classification, census import, unique-tag equality and path-deletion induction, not just output digests.

## Validation, trust boundaries and primary literature

CPython 3.11 standard-library unbounded integer arithmetic is used. Normal and optimized Python regenerate identical complete own records and pass explicit if/raise guards. The own checker takes about 3.8 seconds in this environment; exact timings and peak RSS are recorded in VALIDATION.json. All jobs are serial, all native/BLAS/OpenMP thread limits one, with the unchanged 1 CPU / 2 GiB scope and fixed 60-second process guards. A fixed path-round guard raises an incomplete-result error; no guard was hit. A timeout, incomplete enumeration or absence of a found example supplies no exclusion.

The path algorithm is checked against all **4,096** binary three-variable relation networks, with all eight literal assignments independently enumerated. It correctly excludes all 1,699 unsatisfiable networks and refuses exclusion for 2,397 satisfiable ones. A callback makes **7,608 actual-solution preservation checks** during their relation updates. Separately, all 1,024 six-point graph controls supply 7,168 literal spine counts and reject 1,024 asymmetric stars. The credited known 21-point Ramsey fixture's ten actual stars and completion pass, and 196 degree-preserving asymmetric damages fail. The fixture has 93 red edges, 117 blue edges and page maxima 3/6.

The optional [compare.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/deficit-four-root-audit/compare.py) checks all 135 original incidence entries, 41 unique tags and exact physical star domains, and rejects eight altered inputs including a false minimum-eight restriction, a wrong tag preserving the total deficit and a Boolean tag. Both normal and optimized comparisons pass. Separately, all five original programs pass under normal and optimized Python: producer 89 completion-search nodes, literal checker 897 nodes and multicover 10,101 nodes, with the nine native damaged-input controls. Native algorithm replay is additional evidence, not the new independent path proof.

The trust boundary comprises ordinary unformalized mathematics, the explicitly inherited 8808 census/classification/109 exclusion, the checked cut, small hash-identified census input and exact Python execution. No old minimum-degree theorem, regular-host exclusion, Hall classification, solver status, all-full-root Petersen assumption or floating-point decision is used in the finite deficit-four proof. The global corollary separately inherits 8012's maximum-degree bound.

Current located primary tables retain \(22\le R(B_4,B_7)\le23\): [Lidicky–McKinley–Pfender–Van Overberghe, Table 1](https://arxiv.org/pdf/2407.07285), [Radziszowski, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf). The [original 21-vertex construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt) is prior art; its live bytes match the pinned original fixture. Candidate-specific Petersen/local-degree/Book22 searches do not establish historical priority. The original new 108-edge result belongs to six-books-3; this reviewer supplies the new independent transfer/completion audit and path-depth refinement. The global upper flag certificate is not replayed.

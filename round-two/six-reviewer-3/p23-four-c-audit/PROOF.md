# Independent P23 isolated-row support proof and equality rigidity

Actual author **six-reviewer-3**, role **independent mathematical reviewer**, 2026-10-03.
The written target10042 proof, tables and aggregate counts were exposed. This reconstruction is **NOT BLIND**. This proof and the two primary algorithms were completed before opening the current target executable, certificate or EXPECTED file. All ordinary packing/flow bridges remain unformalized.

Let \(F\) be71 distinct five-subsets of18 points, intersecting pairwise in at most2, with replication profile \((18,19,19,19,20^{14})\). Hubs are \(H=\{0,1,2,3\}\), heavy hub0, and saturated points \(S\) have size14. Let \(\lambda_{xy}\) count words through a pair. Assume \(P=\sum_{ab\subset H}\lambda_{ab}=23\) and no word contains three hubs (\(T=0\)). Put \(\delta_{sa}=5-\lambda_{sa}\), \(D_a=\sum_{s\in S}\delta_{sa}\), \(N_a=|\{s:\delta_{sa}>0\}|\) and \(K=\sum_aN_a\).

The only imported mathematical premise is the universal no LOW--LOW leave edge theorem in twenty-block quadruple pair packings, independent REVIEW8323, exact reference `bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`, source02c1569568854e575f8b176ea07d552737a7da84. Its two-anchor certificate is **not replayed here**. The argument does not import an inventory of saturated stars, the earlier P22 exclusions, or the full upper71 proof.

A C row is a saturated point s whose shortened twenty-block star has exactly four HIGH points, just one a hub a, with \(\delta_{sa}=2\) and a isolated in the HIGH-induced leave. HIGH means positive deficit; LOW means zero deficit. We prove:

1. Four or more C rows imply \(K\ge17\), confirming the target.
2. If four or more C rows and \(K=17\), precisely four C rows exist. After relabeling the three light hubs, the special pair is01 and, up to exchanging2,3,
   \[
   D=(9,5,6,6),\quad N=(6,3,5,3),\quad m=(3,0,1,0).
   \]
   Here m counts **all** C rows. The light C row has all HH leave edges12,02,23. The three heavy C rows each have exactly two HH leave edges: one uses01,02, the other two01,03. All three use01; no surplus HH leave edges are possible.
3. The six positive saturated entries of heavy column0 have deficits \((2,2,2,1,1,1)\), and each of its three C centers is joined by an uncovered triple with hub0 to every other positive entry. All those SAT pairs have replication5. The light C column has deficit multiset \((2,1,1,1,1)\), and its C center similarly has all four other positive entries as saturated friends. These are necessary structures, **not realizations or impossibility certificates**.

## Packing and reversal bridges

Three-point tails through a fixed pair are disjoint: two words sharing another point would intersect in at least3. Thus \(\lambda_{xy}\le5\), with every deficit nonnegative. Shortening at any s in S gives20 pair-disjoint quadruples on17 other points. The leave degree at x is \(16-3\lambda_{sx}=1+3\delta_{sx}\). The total deficit is5 because \(17\cdot5-4\cdot20=5\).

A C hub has leave degree7, all its neighbors LOW. Write d for its other hub neighbors and f for saturated neighbors. Then \(d+f=7\), \(d\le3\). For a saturated friend t, \(\lambda_{st}=5\); the same uncovered triple ast becomes a leave edge sa at the twenty-block star t. There s is LOW, so the imported theorem makes a HIGH: \(\delta_{ta}>0\). All f distinct friends lie among column a's positive entries other than s. Hence
\[
N_a\ge5,\qquad d\ge8-N_a.
\]
The other three hubs are LOW at s, so no leave edge joins them. Every HH leave edge in this row is incident to a. For selected C counts m, distinct centers use distinct positive slots and one excess token each, giving
\[
m_a\le N_a,\qquad m_a\le D_a-N_a.
\]
If there are at least four rows, select any four; all necessary inequalities persist. No local witness frequency is used as a global multiplicity bound.

## The two carriers and low-support obstruction

T0 forces each pair-of-hubs tail into S, so \(\lambda_{ab}\le\lfloor14/3\rfloor=4\). P23 means exactly one pair has replication3, all others4. Relabeling equal-replication light roles gives two **role carriers**, not an assumed automorphism: A with special01, or B with special12. Hub incidence yields
\[
D_a=70-4r_a+\sum_{b\ne a}\lambda_{ab},\quad L_{ab}=14-3\lambda_{ab}.
\]
The D vectors are A:(9,5,6,6), B:(10,5,5,6); L is5 on the special pair and2 elsewhere. Each L counts actual distinct uncovered triples abs; selected rows consume this capacity.

In the hub-a shortened star the total leave degree is \(272-12r_a\), namely56 for0 and44 for light hubs. The \(14-N_a\) zero-deficit saturated vertices are degree1; all other \(N_a+3\) vertices are HIGH. Their degree sum is \(42+N_a\) or \(30+N_a\), at most
\[
(N_a+3)(N_a+2)+(14-N_a).
\]
This excludes heavy \(N_0\le3\) and light \(N_a\le1\), without importing no LOW--LOW for a nineteen-block star. If a light \(N_a=2\), equality32 forces all ten HIGH-HIGH edges and no LOW-LOW edge: writing j for LOW matching edges, the HIGH sum is \(2e+12-2j\), so \(e-j=10\) and \(e\le10\) force \(e=10,j=0\). The two positive SAT entries therefore leave an uncovered triple with a and every other hub b.

When \(\lambda_{ab}=4\), these two entries exhaust L_ab=2. A C row centered at b has deficit zero at a, hence is a different SAT point and cannot use HH edge ab. This is an actual triple-capacity restriction. A light C center b has D_b in{5,6}; N_b>=5 and one excess token force D_b=6,N_b=5, with all its incident HH pairs replication4. Its d is3, so it uses all three HH edges. Every other light column must consequently have support at least3.

## Four-row argument and equality

In A, hub1 cannot carry C; each of2,3 carries at most one. Four heavy C would force N0=5 and d=3 each, violating a capacity2 edge. Thus either three heavy plus one light, or two heavy plus two light.

In the first case slot/excess gives N0<=6; N0=5 violates capacity2 again, so N0=6. The C light column has support5 and the other light supports are at least3, giving K>=6+5+3+3=17. In the second case N0>=5, both C light supports are5, and the remaining light support>=3, giving K>=18.

In B only hub3 can carry a light C, at most one. Four heavy C force N0<=6; their demand>=8 exceeds the total heavy-edge capacity6. With three heavy and one light C, N0=5 violates capacity2; at N0=6 the heavy demand6 plus the light use of03 exceeds6. Thus N0>=7 and K>=7+5+3+3=18.

K17 therefore has carrier A, N and selected counts as stated. A whole C count cannot exceed three at0 or one at the support5 light column, while neither support3 column can carry C. Thus exactly four exist. For the light center2, its three HH edges consume02 once. Heavy rows can then use01 at most3 times (one per row),02 at most1,03 at most2. Their total demand6 saturates every one of these bounds; each row has exactly two HH edges and the stated multiset follows. Their five SAT friends exhaust the other five positive heavy entries. Deficit excess3 at0 and1 at2 is exhausted by the C centers, forcing all remaining positive entries to have deficit1. The friend conclusions follow from the reversal argument, preserving actual SAT labels.

## Complete independent finite evidence

produce.py builds carriers from the literal replication/pair counts and traverses every tuple 0<=N_a<=D_a and every four-part composition m of4. For admissible scalar cases it assigns distinct physical incident HH edges to four labeled C rows recursively, retaining one witness and exhaustively retaining all K17 witnesses. Choosing exactly max(0,8-N_a) edges is a necessary relaxation: delete surplus edges from a genuine row.

check.py imports no producer. It reconstructs all case indices and tests all sixteen subsets of the four physical row vertices. If U is such a subset, its total demand must not exceed \(\sum_e\min(L_e,\#\{j\in U:e\text{ allowed at }j\})\). These are all cuts of the integral row/edge flow after eliminating edge vertices. Integer augmenting paths or integral max-flow/min-cut make them sufficient for this finite relaxation. It independently validates every positive literal witness and reconstructs all equality products with tuple sets.

The full199920-byte defining yes/no stream and all39 positive records agree; carriers have102900 and97020 cases. Both K17 support patterns have exactly3 labeled HH assignments. Complete normal/O output comparison and semantic corruption rejection are required by validation.py. Neither matching counts nor native corroboration substitutes for the ordinary completeness bridges above. The min17 witnesses belong only to the relaxation, not F. Case indexing retains all roles and selected-row multiplicities, with no code symmetry quotient.

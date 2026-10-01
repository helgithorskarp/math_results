# Independent dirty-root Book108 audit and a seven-root occurrence bound

Actual author **six-reviewer-2**, role **independent mathematical reviewer**, 2026-10-01. Target selection and verdict are independent. Shared signing identity does not establish separate authorship. The target is six-books-1's committed lemma8939, **R(B4,B7): rootless108 occurrence split and fourteen dirty-root neighborhood types**, reference `bafkreie3qf4riaoqbnnzarcfswufog6glhcghahfvaptehf3ia7iis6uji`, source commit `5c04d6aaa9cedc7d8dda6082ef5ac7ae60cc40ae` and [original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md).

**Verdict: confirmed within the stated hypotheses.** The ordinary root-occurrence argument is correct. An independently written third generator, literal marked isomorphism checks and every subset packing cut reproduce all fourteen necessary neighborhood types. The three-low occurrence bound can be strengthened from four to **seven** under exactly the same hypotheses; the ordinary proof appears below. This is a scoped review and refinement, with high confidence subject to the explicit written-proof and implementation trust boundaries. It does not decide existence at108 edges or the Ramsey endpoint.

## Exact scope and definitions

A valid host is a simple red graph \(G\) on22 vertices: each red edge has at most three common red neighbors; each blue nonedge has at most six common blue neighbors. These are ordinary subgraph books: edges between pages are unrestricted. Write \(d(v)=d_G(v)\). A full root has degree ten and all ten red neighbors of degree ten. A one-nine root has degree ten, exactly one degree-nine red neighbor and nine degree-ten red neighbors.

Both target theorems assume \(e(G)=108\) and \(\Delta(G)\le10\). These are explicit hypotheses. Set \(\delta_v=10-d(v)\), so \(\delta_v\ge0\) and \(\sum_v\delta_v=4\).

Theorem A additionally assumes no full root. It concludes that the positive deficits are \((2,1,1)\) or \((1,1,1,1)\). There is a one-nine root unless the four deficient vertices are independent and every other vertex has exactly two deficient red neighbors. In that exceptional sector, the multiplicities of the three opposite low-pair types have unordered signature \((1,4,4)\), \((2,3,4)\) or \((3,3,3)\). The target's assertion of at least four one-nine roots in the three-low sector is valid and is strengthened here to seven.

Theorem B assumes a one-nine root \(u\), without assuming rootlessness or a minimum outside degree. Its marked red neighborhood \(J=G[N_R(u)]\), with the degree-nine neighbor marked, must be one of fourteen classes. This is a necessary local list; passing its cuts does not supply a host extension. Both thirteen-edge types remain in the list. The independent-four-low exception also remains unresolved.

## Ordinary audit of the occurrence split

Let \(L=\{v:\delta_v>0\}\), \(H=V(G)\setminus L\), \(\ell=|L|\), and \(q=e(G[L])\). Every high vertex has a low red neighbor, because otherwise it is a full root. Thus

\[
22-\ell\le e(H,L)=10\ell-4-2q.
\]

This excludes \(\ell=1,2\). The positive deficits sum to four, so \(\ell=3,4\), giving exactly the asserted partitions and deriving minimum degree eight in this rootless sector. No pre-existing global lower-degree result is used.

Let \(n_t\) count high vertices having exactly \(t\) low red neighbors. For \(\ell=3\), \(|H|=19\) and \(e(H,L)=26-2q\), whence

\[
n_1=12+2q+n_3.
\]

If \(z\) is the degree-eight vertex and \(\ell_z=d_{G[L]}(z)\), at most \(8-\ell_z\) singleton high vertices have sole low neighbor \(z\). Consequently at least \(4+2q+n_3+\ell_z\ge4\) are one-nine roots. This reproduces the author's original bound before improving it below.

For \(\ell=4\), \(|H|=18\) and \(e(H,L)=36-2q\), giving

\[
n_1=2q+n_3+2n_4.
\]

Any singleton is a one-nine root. If there is no singleton, nonnegativity forces \(q=n_3=n_4=0\); all high vertices have pair types and the four degree-nine low vertices are independent. If \(x_{ij}\) counts type \(\{i,j\}\), then \(\sum_{j\ne i}x_{ij}=9\). Each low blue pair has two low common blue pages and \(x_{ij}\) high common blue pages, so \(0\le x_{ij}\le4\). The four degree equations imply

\[
x_{01}=x_{23}=a,\quad x_{02}=x_{13}=b,\quad x_{03}=x_{12}=c,
\qquad a+b+c=9.
\]

The upper bound four forces all three numbers positive. There are ten ordered triples and the three stated unordered signatures. Low-label permutations induce every permutation of the three opposite pairings, so unordered signatures have precisely the claimed meaning. This argument specifies only low-high incidence; no existence conclusion is made for the remaining high graph.

## Exact reduction to the marked finite domain

At a one-nine root put \(A=N_R(u)\), \(|A|=10\), and \(B=N_B(u)\), \(|B|=11\). Label the mark0. For \(i\in A\), let \(h_i=d_J(i)\), \(\eta_i=1(i=0)\), and \(W_i=\{b\in B:ib\text{ is blue}\}\). For \(b\in B\), write \(k_b=|N_B(b)\cap A|\). Literal degrees give

\[
h_i\le3,\quad |W_i|=h_i+2+\eta_i,\quad
d_{G[B]}(b)=k_b-\delta_b,
\quad \sum_{b\in B}\delta_b=3,
\quad \sum_{b\in B}k_b=\sum_{i\in A}h_i+21.
\]

The first inequality is the red spine \(ui\). The blue spine \(ub\) has \(10-d_{G[B]}(b)\) common blue pages, giving \(d_{G[B]}(b)\ge4\). Therefore \(\sum h_i\ge26\), while \(\sum h_i\le30\). Thus \(e(J)\in\{13,14,15\}\). Only nonnegative deficits and their sum three were used; outside deficit partitions \((3)\), \((2,1)\), \((1,1,1)\) are all allowed in Theorem B.

The neighborhood is triangle-free. A triangle with \(u\) would make a red four-clique \(T\) of global degree sum at least39. For any red four-clique, its eighteen outsiders have red incidences \(r_x\) with \(T\). Its six spines already have two internal pages, so \(\sum_x\binom{r_x}{2}\le6\). Since \(r\le1+\binom r2\) for every integer \(r\ge0\), the clique degree sum is at most \(12+18+6=36\), contradiction. This rederives the prerequisite rather than assuming a regular host.

For \(c_{ij}=|N_J(i)\cap N_J(j)|\), direct page counts give pair bounds

\[
|W_i\cap W_j|\le\lambda_{ij}=\begin{cases}
h_i+h_j+\eta_i+\eta_j-5-c_{ij},&ij\text{ red},\\
h_i+h_j-2-c_{ij},&ij\text{ blue}.
\end{cases}
\]

A red pair has \(1+c_{ij}\) pages in \(\{u\}\cup A\), and \(11-|W_i|-|W_j|+|W_i\cap W_j|\) in \(B\). A blue pair has \(8-h_i-h_j+c_{ij}\) pages in \(A\), none at \(u\), and \(|W_i\cap W_j|\) in \(B\). These establish the formulas including the marked column's extra unit. Full-root all-five-column row restrictions would be unjustified here.

Every four-cycle in \(J\) is induced. For its four vertices \(Q\), write \(S_Q=\sum_{i\in Q}h_i\), \(D_Q=\sum_{i\in Q}\eta_i\). The eleven row restrictions have total incidence \(S_Q+8+D_Q\). Summing \(\binom t2\ge t-1\) gives a lower bound \(S_Q+D_Q-3\) on their total pair intersections. The four red cycle pairs and two blue opposite pairs have summed upper bound \(3S_Q+2D_Q-28\); each opposite pair has at least two local common neighbors. Hence

\[
2S_Q+D_Q\ge25.
\]

Since \(S_Q\le12\) and \(D_Q\le1\), the cycle contains the mark and every cycle vertex has local degree three. Thus \(F=J-\{0\}\) is a nine-vertex subcubic graph with no triangles or four-cycles. Only \(F\), not all of \(J\), is required to have girth at least five.

For every column subset \(T\), the eleven row counts \(t_b\in\{0,\ldots,|T|\}\) sum to \(Q_T=\sum_{i\in T}|W_i|\). Writing \(Q_T=11q+r\), \(0\le r<11\), gives

\[
\sum_{i<j\in T}|W_i\cap W_j|
=\sum_{b\in B}\binom{t_b}{2}
\ge11\binom q2+rq.
\]

Moving an incidence from a row exceeding another by at least two strictly decreases the cost; the minimum has rows \(q,q+1\). A contradiction follows if the summed \(\lambda_{ij}\) is smaller. The checker computes this minimum independently by the cheapest marginal costs \(0,1,\ldots,|T|-1\), each repeated eleven times, and uses literal local page counts to reconstruct pair capacities.

## Independent complete enumeration and certificates

[audit.py](audit.py) imports no author module or external graph catalogue. It prescribes every nonincreasing degree sequence in \(\{0,1,2,3\}^9\) with even sum, then completes vertices in order using their residual neighbor demand. Future edges are absent before their endpoint is processed. A prospective edge is forbidden exactly when it closes an existing path of length at most three; two new neighbors must be nonadjacent and have no old common neighbor. These tests prevent precisely the triangles and four-cycles newly created at that step. Residual-degree upper bounds only remove impossible completions.

The only generation symmetry pruning is within future vertices of the same target degree and identical current adjacency. They are literal twins in the partial graph, so arbitrary permutations of each cell preserve the state and target degrees while fixing every processed vertex. Choosing a prefix of each cell retains a representative of every possible neighbor choice, and hence of every completion orbit. Relabeling future vertices within such cells does not change the preceding rows. Induction on completed rows proves coverage; every completed leaf is separately checked for its prescribed degree and graph domain. This differs from both the author's vertex-augmentation/refinement generator and edge-augmentation generator.

Final deduplication uses equivariant tuple colors to restrict a complete adjacency/nonadjacency-preserving bijection search. Refinement is only a necessary filter. Every returned map is checked literally, and the mark has a unique color in marked comparisons; no heuristic canonical label supplies a premise.

All110 even degree sequences complete in4450 search nodes and388 valid leaves before final isomorphism reduction, producing183 classes. The edge-count distribution for0 through12 is

\[
(1,1,2,4,7,13,23,34,40,34,18,5,1).
\]

There is no thirteen-edge class. Since adding the mark contributes at most three edges, only the24 classes with at least ten edges matter:18 at ten, five at eleven and one at twelve. Adding the mark to every independent subset of at most three vertices of degree below three, and retaining total edges13..15, gives292 raw additions and179 marked isomorphism classes. Every admissible \(J\) appears: deleting its mark gives such an \(F\), and its marked neighbors satisfy exactly these conditions. Allowing marked four-cycles creates no gap because the extension requires triangle-freeness only.

The179 stored classes in [MODEL.json](MODEL.json) are untrusted candidate data. All179 match the independent output bijectively through actual marked isomorphisms. Keys encode the45 vertex pairs in lexicographic order, bit0 for \((0,1)\), and vertex0 is marked. Metadata is checked against literal degrees. For each class the checker evaluates **all1013 subsets** of sizes2..10: **181327 exact packing inequalities**. All165 stored rejection witnesses are verified, and an independently selected witness for each rejected class is recorded in [EXPECTED.json](EXPECTED.json). Every survivor passes every cut; its survival only concerns these necessary inequalities.

The fourteen keys and local degree patterns are:

| Edges | Local degrees | Mark degree | Keys |
| --- | --- | --- | --- |
| 13 | \(0,2,3^8\) | 3 | 710617334208 |
| 13 | \(1,2,2,3^7\) | 3 | 6790396772737 |
| 14 | \(2^2,3^8\) | 2 | 191556510080 |
| 14 | \(2^2,3^8\) | 3 | 57382871488, 114509291968, 116837913024, 629012763072, 637086015936, 837888582080, 1189572272514, 1224871651776, 2277877551552, 6609586119042 |
| 15 | \(3^{10}\) | 3 | 704564769216 |

The fifteen-edge case is independently identified with the classical Petersen graph \(KG(5,2)\): literal two-subsets of five points, adjacent when disjoint. This identification was already in8869 and is credited, not a new classification of the Petersen graph. The complete cut transcript SHA256 is `59920d6f02e0ca9e675c333a277d5ddaeb29718c35cf86b045f8eb7192e161e1`.

## Validation and trust boundaries

[controls.py](controls.py) exhausts all33864 labeled graphs on3..6 vertices. The accepted girth-five subcubic counts are7,38,298,3268, and each matches exactly one independently generated class, with class counts3,6,10,20. It also brute-forces120 small bounded-row incidence minima, checks358 separately relabeled marked graphs and16110 transported pair capacities, and uses a marked-path role distinction and a four-cycle negative control. Eleven damaged model tables are rejected by the actual mathematical table audit, not merely by a hash mismatch. These include missing/duplicate classes, bad keys/degrees and changed/erased cut evidence.

The primary authors'21-point matrix was fetched anew as [PRIMARY21.txt](PRIMARY21.txt). Its numeric matrix is decoded independently and complemented off the diagonal. All441 entries match the original baseline convention; the graph has93 red edges and page maxima3 and6. The trailing search metadata is separate from the mathematical matrix. This is a known positive control, not a new construction.

The frozen author's two programs were also replayed separately. The vertex producer's full output and the edge checker's full output match their original expected records; the latter also passes with Python optimization enabled, including its eight integrity controls. They are credited author algorithms, and their replay is separate from the reviewer's independently generated proof computation.

Python3.11.2 standard-library integers suffice. The reviewer's normal and optimized runs produce byte-identical EXPECTED and CONTROLS records. Each local mathematical job ran separately with native thread counts one and an upfront90-second guard; the largest observed replay time was7.245 seconds and the maximum observed peak RSS was22104KiB. The independent generator has a fixed2000000-node guard; exceeding it raises an incomplete-enumeration error. No limit was reached, no solver or floating result is a proof premise, and no operational resource setting was changed. Compact [VALIDATION.json](VALIDATION.json), [PROVENANCE.json](PROVENANCE.json) and [SHA256SUMS](SHA256SUMS) record the inputs and results.

The ordinary finite reduction, generator induction and implementation correspondence are written and unformalized. No proof-assistant theorem is claimed. The reviewer covers Theorems A/B of8939; whole prerequisite claims8869,8012, concurrent8915 and subsequent host-completion claims receive no new verdict. In particular the explicit maximum-degree hypothesis is retained rather than asserting an unrestricted consequence of8012.

## Strengthening and improvement opportunities

**Proved refinement: at least seven one-nine roots in the three-low sector.** In the rootless deficit pattern \((2,1,1)\), label the low vertices \(z,a,b\) with degrees8,9,9. Let \(y\) count high vertices whose low type is exactly \(\{a,b\}\), let \(t\) count triple types, and let \(e_{ij}\in\{0,1\}\) indicate a red low edge. Put \(\ell_z=e_{za}+e_{zb}\). Among the19 high vertices, precisely \(8-\ell_z\) are red neighbors of \(z\). Every remaining high vertex has low type \(\{a\}\), \(\{b\}\) or \(\{a,b\}\). The first two types are exactly the one-nine roots, so their number \(R\) is

\[
R=11+\ell_z-y.
\]

The common red neighbors of \(a,b\) number \(y+t+e_{za}e_{zb}\). If \(ab\) is red this is at most3. If it is blue, its common blue count is \(20-d(a)-d(b)+c_R(a,b)=2+c_R(a,b)\), so its common red count is at most4. Uniformly,

\[
y+t+e_{za}e_{zb}\le4-e_{ab}.
\]

Consequently, under exactly the original hypotheses,

\[
\boxed{R\ge7+\ell_z+e_{ab}+e_{za}e_{zb}+t\ge7.}
\]

This is an ordinary combinatorial proof, independent of the neighborhood enumeration. The separate incidence check enumerates all132 abstract low/high type models satisfying low degrees, high coverage and low-pair page caps; each obeys the displayed inequality. Its minimum seven occurs, for example, with no low edges, singleton counts \((5,5,2)\), pair counts \((0,3,4)\) for \((za,zb,ab)\), and no triple. This proves sharpness only in that abstract incidence relaxation; it does not construct a valid22-point host or prove seven sharp there.

**Immediate equality consequence, with credit to the target's identities:** if a one-nine neighborhood has thirteen edges, \(\sum k_b=47\), \(\sum\delta_b=3\), and \(\sum d_{G[B]}(b)=44\). Since every outside degree in \(G[B]\) is at least four, \(G[B]\) is four-regular. All eleven blue spines \(ub\) then have exactly six blue pages. This is a useful necessary completion restriction, not an exclusion of either thirteen-edge type or an independent priority claim.

**Concrete remaining bridge:** an exclusion of a surviving type needs actual binary columns, exact outside deficits, reciprocal outside adjacencies and every mixed/outside page cap. Subset packing bounds alone do not ensure realizability. The independent-four-low signatures similarly require a compatible18-vertex high graph. These are the consequential completion frontiers. A formalized residual-degree generator could reduce the implementation trust boundary; additional packing inequalities may shorten completion work, but no stronger exclusion is claimed here.

## Literature, attribution and publication readiness

The primary [Lidicky--McKinley--Pfender--Van Overberghe paper](https://arxiv.org/pdf/2407.07285), Table1, and the current [Small Ramsey Numbers survey](https://www.cs.rit.edu/~spr/ElJC/sur.pdf), TableIXa, give the located interval \(22\le R(B_4,B_7)\le23\). The [primary companion matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt) supplies the positive control. Sources were checked live2026-10-01. The published upper-bound flag certificate was not replayed here.

The rootless degree/low-pair mechanisms and cubic Petersen case are credited to [8869](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_structure/PROOF.md), `bafkreibptgfpwfzyroiimshpps7hz4bjsbxd3bfoax6xhq4wbtbvwv36eq`. The four-clique degree-sum mechanism is in [8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md), `bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a`; the column interface is in [8726](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/irregular_full_roots/PROOF.md), `bafkreieztrfin22gkvvmkydq45n2xgtx6hkzrkvx6fd2g5ckkgjcc6zjwm`. My earlier [review8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md), `bafkreibpw6tonyn6gmqzxrbnfbver7owldb76uzn2icx5w24g52sr6d4se`, supplies the weighted four-column obstruction but did not audit these dirty-root classes. The standard integer incidence minimum also appears in concurrent [8915](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_free_seven_108/PROOF.md), `bafkreia2iulhnpbdgetm5j5yzyvwhzydip6gnb633ue5lrrrjmns4qwffa`, at another root size. [8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md), `bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`, is relevant to a separate maximum-degree bridge, which is not a premise of this conditional review.

Target-specific live searches for rootless108, dirty one-nine/fourteen neighborhoods and the strengthened seven-root count located no separate primary source for this particular refinement. This bounded search does not establish historical priority. Convex incidence minima, residual-degree enumeration, graph isomorphism methods and the Petersen graph are known tools. The mathematical increment is independent validation of the scoped target and the proved seven-root bound. The compact source is ready for reproducible scrutiny; global host completion and an unrestricted Ramsey conclusion remain open.

Reproduction commands and expected outputs are in [README.md](README.md). Publication provenance records the original fixed input commit separately from the reviewer's source commit, which is supplied with the graph review after remote verification.

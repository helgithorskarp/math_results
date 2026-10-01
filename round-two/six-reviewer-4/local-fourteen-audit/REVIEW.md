# Independent local-fourteen Book Ramsey audit

Actual author **six-reviewer-4**, role **independent mathematical reviewer**, 2026-10-01. The campaign's shared signing identity does not establish distinct authorship. The original claim and its nine integer cuts are by **six-books-3**, researcher.

**Verdict: verified exact computer-assisted intermediate theorem, with the dependency split below.** No defect was found in committed lemma 8638, “R(B4,B7): all regular red edges have codegree three; complete local-fourteen exclusion,” reference **bafkreidkxsdjhx2pheg3xcq5ujblspc2l4gi5fftsj623vb7pmb2g47we4**. The audited author source commit is **0efb5185b1880be9a29f76ae05f206a8baf60368**; its [full proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-exclusion/PROOF.md) and [source directory](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-books-3/local14-exclusion) give the original implementation.

The independent checker reconstructs all relevant local cores and all 130 residual incidence matrices. It imports no author program. A further proved refinement replaces the final enumeration of 29,166 outside stars with **130 scalar rank-sum inequalities: 128 use two columns, two use three columns**. The earlier finite incidence reduction is retained. These are obstruction certificates for necessary local data, not a census of full 22-point graphs.

This review establishes the local exclusion independently and checks the global consequence using credited, already reviewed premises. It does not establish nonexistence of every ten-regular host, exclude irregular hosts, determine the Ramsey endpoint, or audit a subsequent Petersen/classification argument. The proof is ordinary written mathematics plus exact Python computation, without proof-assistant formalization.

## Exact hypotheses and dependency boundary

Let \(G\) be a simple ten-regular graph on 22 vertices. Edges are red and nonedges are blue. Every red edge has at most three common red neighbors, and every blue edge has at most six common blue neighbors. These are the ordinary, noninduced \(B_4/B_7\) restrictions: edges between book pages are unrestricted. No connectedness, host automorphism, cyclic construction, or other symmetry assumption is made.

The independently checked local statement is:

> No root \(v\) has red neighborhood \(J=G[N_R(v)]\) with degree sequence \(2^2,3^8\).

The packing argument and necessary nine-core classification from lemma 8559, **bafkreihrw6fz7nozp5m5g2s5hnmeqkyte6taxfejvjk6gowwkepulvc4z4**, are rederived below and independently enumerated. Credit remains with six-books-3; see its [packing proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-disjoint/PROOF.md), source **16d5b8169e841574508035993da91cecfaf5d422**. The extra global cycle corollaries of 8559 are outside this audit.

Triangle-freeness of \(J\) follows from six-books-1's lemma 8541, **bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a**, whose easy \(K_4\) counting argument is repeated below. The [original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md) has source **53fa7ea66251df9d255b7d0ff9d0ff309580d42a**. This reviewer's completed [independent audit 8577](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/regular-blue-codegree-audit/REVIEW.md), **bafkreich276kxjdsgbgndtmpctthoykvyki2b4toml5mkdrmrv47q67yfa**, source **710624deff8eda46bc6e251bb5d37e0f13a8bbce**, covers that predecessor's stronger statement; that stronger statement is unnecessary here.

The global red-codegree-three consequence additionally uses:

| Credited premise | Exact contribution reference | Existing independent review |
|---|---|---|
| [Positive red codegrees 8120](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_positive_codegrees/PROOF.md): every red codegree is two or three | bafkreid6vw7ktqeizndog5fdazervle4elnf6gvf7iqcjvsqdczxioidum | [8190, six-reviewer-4](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_regular110_review4/REVIEW.md), bafkreibbeq3kihqadwgfm3h2ibmnrcplfesad6xxcdch2ieiaqjcfws7la |
| [Neighborhood floor 8218](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_neighborhood_floor14/PROOF.md): every neighborhood spans fourteen or fifteen edges | bafkreibi6eg2kkh6nzmndut76ivzzmqu3oj57mop5h324lbumakrw5pefu | [8244, six-reviewer-2](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_floor14_review2/REVIEW.md), bafkreigdhyv664kaqz6wy2zsvsp2zc6picodx3z75daxbgzaehpr4ebday |
| [Maximum degree ten 8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md), used only for the 110-red-edge application | bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi | [8060, six-reviewer-1](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_gram_review1/REVIEW.md), bafkreibor5a5i6qhsljhbabkuqgahgoy5ou3ts6gpnw27sexbiwtizzm2m |

The original premise commits, respectively, are **7400e3949d93733d2050118e0557d94a8a8f1625**, **d00a13612475ea701786203b280200c11a105106**, and **ce3177a731086284ee89f18a8a3948b672b3c64e**. Existing review commits, respectively, are **2188810844c37533ed2cea41b55a0838993459ab**, **653b98c3992de1cfe47ef27226c40207b17de471**, and **b3e45c1ca194e1becece046ed2e4695f9692406c**. Their complete committed bodies and relevant incoming review evidence were read. Their older 46,411-, 1,747,161-, and 68,895-state enumerations were not rerun in this pass. Accepting those credited results is an explicit trust boundary of the global and 110-edge corollaries; none is a premise of the explicit local exclusion.

No earlier cap-six or two-six computation is imported: every surplus-four pattern is covered directly. The author's optional floating-point cut discovery is also unnecessary. The copied cuts are treated as untrusted integer certificate inputs, checked on complete regenerated domains.

## Literal incidence reduction and packing

Fix \(v\), put \(A=N_R(v)\), \(B=N_B(v)\), so \(|A|=10\), \(|B|=11\). Write \(h_i=d_J(i)\), \(c_{ij}=|N_J(i)\cap N_J(j)|\), \(W_i=B\setminus N_R(i)\), and \(Z_b=A\setminus N_R(b)\). A row word \(z_b\) is the binary indicator of \(Z_b\). Ten-regularity gives

\[
t_i=|W_i|=h_i+2,\qquad |Z_b|=d_{G[B]}(b),\qquad \sum_b|Z_b|=48.
\]

Let \(S_{ij}=|W_i\cap W_j|\). For a red pair in \(J\), its common red pages comprise the root, \(c_{ij}\) points of \(A\), and \(11-t_i-t_j+S_{ij}\) points of \(B\). For a blue pair, there are \(8-h_i-h_j+c_{ij}\) blue pages in \(A\), \(S_{ij}\) in \(B\), and none at the root. Therefore

\[
S_{ij}\le U_{ij}=\begin{cases}h_i+h_j-5-c_{ij}&ij\text{ red},\\h_i+h_j-2-c_{ij}&ij\text{ blue}.\end{cases}
\]

These are necessary bounds, not assertions that arbitrary matrices below extend to a host. The checker reconstructs them from literal page baselines rather than importing a Gram matrix formula.

The two low points \(x,y\), of degree two in \(J\), are nonadjacent: a red low pair has negative \(U\). A red low--cubic pair has \(U=-c_{ij}\), so its two miss columns are disjoint. If \(x,y\) had a common neighbor \(p\), then \(W_p\) would be disjoint from both size-four low columns, while \(|W_x\cap W_y|\le2-c_{xy}\). Their union would have at least \(4+4+5-(2-c_{xy})=11+c_{xy}>11\) points. Thus their neighbor pairs are disjoint.

If \(N_J(x)=\{p,q\}\), the two size-five columns \(W_p,W_q\) lie in the seven-point complement of \(W_x\), hence intersect in at least three points. A red \(pq\) would have \(U_{pq}\le0\), impossible. For the blue pair, \(c_{pq}\ge1\) and \(U_{pq}=4-c_{pq}\le3\). Equality forces \(c_{pq}=1\), \(|W_p\cap W_q|=3\), and \(W_p\cup W_q=B\setminus W_x\). The outside vertices consequently partition into \(W_x\), \(W_p\cap W_q\), \(W_p\setminus W_q\), \(W_q\setminus W_p\), of sizes \(4,3,2,2\).

Normalize only labels: low points are 0,1, their respective neighbor pairs are \(\{2,3\},\{4,5\}\). Every row on each triple \((0,2,3)\), \((1,4,5)\) has one of the four patterns \(100,011,010,001\). The pairs \(2,3\) and \(4,5\) are nonedges with no common neighbor in the eight-point remainder \(F\). This label normalization assumes no automorphism of the host.

For completeness, the credited \(K_4\) exclusion has a short count. A red \(K_4\) sends 28 red incidences to the other 18 vertices. Each of its six edges already has two pages within the clique, so the total outside pair-incidences is at most six. If an outside vertex has \(r\) red incidences to the clique, it contributes \(\binom r2\ge r-1\). Summing gives at least \(28-18=10\), a contradiction. Thus \(G\) is \(K_4\)-free and every \(J\) is triangle-free.

## Independent coverage of the nine local cores

The remainder \(F\), on labels \(2,\ldots,9\), has degrees \(2^4,3^4\) and ten edges. Its mask uses lexicographically ordered unordered pairs on eight labels, with a shift of two into \(A\).

The independent implementation chooses the first remainder vertex's two neighbors in all \(\binom72=21\) ways, then visits every weight-eight word on the other 21 edges. This visits **4,273,290 fixed-weight words**, including graphs subsequently rejected by degree constraints. The fixed-weight successor routine visits every word once; it makes no mathematical pruning assumption. Necessary terminal tests give:

| Test retained | Count |
|---|---:|
| Required remainder degrees | 6,057 |
| The two prohibited pair edges absent | 3,871 |
| All literal joint-miss capacities nonnegative | 3,660 |
| The two neighbor pairs satisfy the packing restriction | 1,440 |
| The complete ten-point \(J\) is triangle-free | 672 |

This raw 6,057 count starts with a larger domain than the author's 3,871 count, which already imposes the prohibited pair edges. At every matching stage the counts agree. The complete 672-mask stream SHA256 is **a79ef5d8047a18c433f415b48bf75f4ceadda24bf9bc622ea7e99c6e71e782f7**, agreeing with the credited census.

Generic full-ten-vertex color refinement and bijection backtracking check that every retained graph maps to one of the following nine representatives. Every returned map is checked against all 100 adjacency entries. The representatives are pairwise nonisomorphic. The algorithm does not import the author's 192 alignment permutations or restrict an unknown host by symmetry.

| Remainder mask | Aligned graphs covered | Integer cut upper bound |
|---:|---:|---:|
| 30083408 | 96 | -1 |
| 51316320 | 24 | -1 |
| 51317328 | 24 | 0 |
| 54986080 | 96 | -1 |
| 54987088 | 192 | -1 |
| 55740996 | 96 | -1 |
| 126126276 | 48 | -5 |
| 126158020 | 48 | -4 |
| 126158146 | 48 | -1 |

The complete stream of literal isomorphism maps has SHA256 **a100aeaf2962e9a29473be0c8fe3a86b40048a558f2fdfd598f5f7362c2ac1de**. Hash agreement records provenance; the exhaustive labeled domain and checked maps supply the coverage argument.

## Row domains, integer cuts, and all surplus patterns

The blue spine \(vb\) has \(10-|Z_b|\) blue pages, so \(|Z_b|\ge4\). Eleven such rows and total size 48 leave surplus four. Consequently the exhaustive size patterns are

\[
8,4^{10};\quad7,5,4^9;\quad6,6,4^9;\quad6,5,5,4^8;\quad5^4,4^7.
\]

Distinct outside vertices may have identical miss rows. Every algorithm allows those multiplicities, including in high rows. Sorting rows merely relabels \(B\).

The checker scans all 1,024 binary row words. It imposes the two forced four-state triples, avoids pairs with \(U_{ij}=0\), and counts necessary \(A\)--\(b\) pages. With \(k=|Z|\), a red \(ib\) has \(|N_J(i)\setminus Z|\) pages in \(A\) and at least \(\max(0,k-t_i)\) in \(B\). A blue \(ib\) has \(k-1-|N_J(i)\cap Z|\) pages in \(A\). These tests retain 200 rows per core, with size counts **79,76,39,6,0** for sizes four through eight. Their common sorted-row stream SHA256 is **833d28771d4b1051559410a6a6b1d7f8cacf13486d245fdcb3c4b431773868b4**. Size eight is explicitly tested and absent, rather than silently omitted.

The nine records in [cuts.json](cuts.json) are the original author's coefficients, copied exactly and credited. For each record define

\[
f(z)=\gamma+\sum_i\alpha_i z_i+\sum_{i<j}\beta_{ij}z_i z_j.
\]

All coefficients are checked as integers, weighted pairs are unique, and every listed \(\beta_{ij}\) is strictly positive. Absent weights mean zero. The complete row domain is checked for \(f(z)\ge0\). Every host would obey

\[
0\le\sum_b f(z_b)\le 11\gamma+\sum_i\alpha_i t_i+\sum_{i<j}\beta_{ij}U_{ij}=V.
\]

The table's eight strictly negative \(V\)'s exclude eight cores. No floating solver assertion supplies an exclusion. The sole zero case is mask 51317328. Equality forces every row to have score zero and every positively weighted pair to saturate its capacity. There are 92 zero rows: 19 of size four, 36 of size five, 31 of size six, six of size seven. Sixteen pair equations are saturated.

The independent residual algorithm is integer multicover, distinct from both the author's multiset join and its rational rank-17 reconstruction. It loops over every surplus-four partition and every nondecreasing high-row multiset, with repetition. It rejects only an exceeded nonnegative column or pair capacity. For the remaining four rows, its feature vector contains the ten columns, sixteen saturated pairs, and the row count: **27 equations in 19 nonnegative integer multiplicities**.

Completeness follows by induction on unsatisfied equations. A type touching an equation with residual zero cannot occur again. Choose a positive equation; every completion assigns nonnegative multiplicities to its remaining incident types, whose sum equals that residual. The routine visits all such assignments, including zero and repeated types, bounded by their other nonnegative residuals. Saturating this equation then removes exactly its incident types; every possible completion is preserved in one child. The row-count feature prevents an unconstrained positive multiplicity. When every residual is zero, all remaining multiplicities must be zero. All returned vectors satisfy all 27 equations literally; the remaining pair inequalities are then checked. Memoization identifies identical subproblems and makes no completeness assumption about rank or free variables.

| High sizes | Raw multisets | Capacity-admissible high multisets | Full matrices |
|---|---:|---:|---:|
| 5,5,5,5 | 82,251 | 1,935 | 81 |
| 6,5,5 | 20,646 | 814 | 42 |
| 6,6 | 496 | 27 | 3 |
| 7,5 | 216 | 32 | 4 |
| 8 | 0 | 0 | 0 |

There are 103,609 raw high multisets and **130** full matrices. Their sorted row words agree entrywise with every author certificate matrix, comprising **14,300 binary incidence entries**, not merely matching counts or hashes. The full matrix stream SHA256 is **7e9c728b3c4e2fb0ad768e43f5a2aaffb543a4036b2e727f3ec14e652cfdb194**. All nine row/core profiles and all capped high-multiset counts also agree.

## Proved compression of the final outside obstruction

For one outside vertex \(b\), write \(Z=Z_b\), \(k=|Z|\), and \(r_i=|N_J(i)\cap Z|\). Its unknown red neighbors in \(B\) form a set \(C\subseteq B\setminus\{b\}\) of size \(k\). Put \(X_i=\sum_{c\in C}z_{ci}\). The exact red-page count for \(i\notin Z\) is

\[
h_i-r_i+k-X_i.
\]

The exact blue-page count for \(i\in Z\) is

\[
(k-1-r_i)+(t_i-1-X_i)=k+h_i-r_i-X_i.
\]

The root supplies no page in either case. Thus all ten \(A\)--\(b\) caps imply

\[
X_i\ge L_i:=k+h_i-r_i-3-3\mathbf1_{i\in Z}.
\]

For every subset \(T\subseteq A\), sum these inequalities. Since \(C\) contains exactly \(k\) distinct other outside vertices,

\[
\sum_{i\in T}L_i\le\sum_{c\in C}|Z_c\cap T|
\le\text{sum of the }k\text{ largest values among }\{|Z_c\cap T|:c\ne b\}.
\]

If the left side strictly exceeds the last quantity, no outside star can satisfy the caps. The final inequality is elementary selection of the largest \(k\) numbers; no novelty is claimed for that general principle. It remains valid if some individual \(L_i\) is negative.

For every one of the 130 reconstructed matrices, [cover-cuts.json](cover-cuts.json) gives a row index \(b\) and a two- or three-column subset word \(T\). The checker recomputes both sides and requires a strict integer contradiction. There are **128 two-column certificates and two three-column certificates**, with 124 margins of one and six margins of two. The certificate order is tied to the independently regenerated sorted incidence stream. No author empty-star marker, outside-star search, or asserted infeasibility is imported.

Examples use zero-based row and column indices, with a subset encoded by its set bits:

| Matrix index | Sorted row words | Chosen row | Columns | Demand | Maximum supply |
|---:|---|---:|---|---:|---:|
| 0 | 60,60,195,209,326,372,654,728,771,801,936 | 7 | 0,2 | 6 | 5 |
| 63 | 60,209,209,252,326,326,650,650,801,801,828 | 3 | 0,1,4 | 9 | 8 |
| 71 | 60,209,209,326,326,380,650,650,700,801,801 | 5 | 0,1,2 | 9 | 8 |

These three matrices are necessary-data cases, not valid host examples. Indices 63 and 71 are exactly the two cases requiring a triple in the published pair-first certificate construction. No claim is made that arbitrary larger subsets, alternate necessary filters, or a different proof cannot shorten them further.

This excludes every possible outside star for at least one row of each full incidence matrix. Other \(B\)--\(B\) edges and their page caps need never be assigned. All nine local cores therefore fail, proving the explicit local theorem.

## Global consequence, reproducibility, and confidence

Using credited positive red codegrees and the floor theorem, each local degree sequence is \(2^2,3^8\) or \(3^{10}\). The former has just been excluded. Thus every red edge has exactly three common red neighbors, each neighborhood is cubic and triangle-free with fifteen edges, and the host has \(22\cdot10/2=110\) red edges and \(110\cdot3/3=110\) red triangles. The degree-two defect graph is empty. With the credited maximum-degree-ten theorem, any valid 110-red-edge host is ten-regular by the degree sum, so the same necessary conclusion applies. This remains an intermediate statement, not a host nonexistence theorem.

[audit.py](audit.py) uses CPython **3.11.2**, standard library, exact integers, one process, and no solver or numerical library. Normal and optimized executions with complete author-data comparison passed in **24.980961 s** and **21.777903 s**; the measured cumulative child RSS upper bound was **29,220 KiB**. Disabling Python assertions does not disable validation: failed guards raise exceptions explicitly.

Three independently damaged inputs were rejected under optimized Python: removing a core certificate leaves an uncovered necessary graph; a negative pair weight violates the cut's sign requirement; a well-formed but false two-column certificate fails the strict rank-sum inequality. Additionally, 252 ten-regular circulants supply **5,544 actual and hypothetical outside stars and 55,440 literal full-22-point page identities**, and exhaustive small arrays check the top-\(k\) identity through length seven. Control graphs may violate the book caps and are not a census of valid hosts.

The original author's optimized generator, independent-within-author verifier, and six damaged-object controls were also replayed, taking **2.156551 s**, **5.086417 s**, and **4.930065 s**. All passed, including the original 29,166-star exclusion. Their cumulative child RSS upper bound was **22,596 KiB**. These native replays corroborate reproducibility; the independent core/multicover/rank-sum argument provides the distinct audit methodology. The 21-point primary fixture reproduced 93 red edges and page maxima three/six; it is credited baseline data.

The 13 pinned author files were fetched and matched against their exact Git blob identifiers. This review publishes only compact source, integer inputs, expected records, and 130 small obstruction certificates. It need not publish or trust a large enumeration dump. File hashes and measured validation records are in [SHA256SUMS](SHA256SUMS) and [VALIDATION.json](VALIDATION.json); reproduction commands are in [README.md](README.md).

The principal trust boundary is the written normalization/counting/completeness bridge and the small Python programs. No timeout, memory kill, UNKNOWN, floating-point infeasibility, external catalogue, or incomplete enumeration is used as a mathematical premise. The global consequence's older credited finite premises are distinguished above. The exact computation and ordinary proof have not been formalized.

## Literature status and publication readiness

Primary literature checked live on 2026-10-01 includes [Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2), [Radziszowski, Small Ramsey Numbers DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf), and the [original books-and-wheels companion repository](https://github.com/gwen-mckinley/ramsey-books-wheels). The located published interval is \(22\le R(B_4,B_7)\le23\). The published upper-bound flag-algebra certificate was not replayed here.

A bounded candidate-specific search for the regular 22-point/codegree-three and local-fourteen statements did not locate an earlier exact result. This does not establish historical priority. The original local exclusion and its credited predecessors are potentially useful campaign advances within the regular branch. The present publication is a substantive independent review with a specific proof compression; it is not a new Ramsey bound. A conventional paper would need to integrate the dependency proofs, make their finite data equally accessible, and assess literature priority more fully. The supplied evidence is ready for a scoped exact computational intermediate result, subject to the stated unformalized trust boundary.

## Strengthening and improvement opportunities

**Proved refinement:** the final outside-star enumeration is replaced by 130 short two/three-column inequalities, with independently regenerated complete incidence coverage. This narrows the verification burden and expresses the contradiction as explicit integer counting. It does not eliminate the core census, the row reduction, or the residual incidence enumeration.

**Proved reusable necessary filter:** before a full incidence matrix is known, any row \(Z\), pair \(i,j\), and its required lower demands satisfy

\[
L_i+L_j\le\min\{2k,\ k+U_{ij}-z_i z_j,\ t_i+t_j-z_i-z_j\}.
\]

Indeed \(X_i+X_j\le2k\); each selected row contributes at most one plus its joint miss, so \(X_i+X_j\le k+S_{ij}-z_i z_j\le k+U_{ij}-z_i z_j\); and selected rows cannot exceed the two complete miss columns after removing \(b\). Combine these with \(X_i+X_j\ge L_i+L_j\). This classical counting consequence can sharpen future row domains without specifying all other rows. No additional finite-domain count or exclusion is claimed from it in this publication.

**High-value next bridge:** the surviving local-fifteen branch consists of triangle-free cubic neighborhoods on ten points. The incidence/selection inequalities apply there as well, with all miss columns of size five. A further structural obstruction or complete neighborhood classification plus a rigorously verified host bridge is needed to exclude that branch. The current review has not checked any downstream Petersen or literature-classification argument.

**Beyond regularity:** an unrestricted Ramsey decision still needs coverage of irregular 22-point hosts, with exact degree-dependent miss identities and all degree cases justified. Merely removing “ten-regular” from this statement is unsupported. Formalizing the short rank-sum lemma and then the finite normalization bridge is feasible, but would require checked encodings of graph isomorphisms, integer cuts, and multicover completeness rather than reliance on matching output hashes.

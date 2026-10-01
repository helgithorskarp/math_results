# Independent regular Book22 audit and an elementary Petersen obstruction

Actual author **six-reviewer-4**, role **independent mathematical reviewer**, 2026-10-01. The original contribution is by **six-books-3**, researcher. Shared graph signatures do not establish distinct authorship.

**Verdict: verified the scoped theorem and its 109-edge consequence; no gap found.** The target is committed lemma **8692**, “R(B4,B7): no regular22-vertex host; universal109-red-edge bound,” reference **bafkreihb6tdhducvwx2wkxazbv76lb5k4qgorz2wdzhye4j6hgs6qqv7bi**. The audited author commit is **8f1d8fad8a130c3b01fced51959147dc79e6b28c**; see the [original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/regular110-exclusion/PROOF.md) and [companion source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-books-3/regular110-exclusion).

The new original four-column packing, elementary Petersen recognition, connectedness argument, and exact application of Hall's existing classification all check. This review additionally proves a short special-case replacement for the historical classification:

> **Elementary refinement.** No simple graph on 22 vertices is locally Petersen. This follows from 21 explicitly classified necessary incidence multisets and ordinary counting, without assuming connectedness or importing Hall's classification.

The written refinement below gives complete case coverage without relying on a computer census. The independent exact checker reconstructs the same cases from all binary common-neighbor subsets and all high-row multisets, then checks 20 pair inequalities and one degree/page contradiction. The number 21 is **5+15+1**; a provisional arithmetic count of 31 was corrected before publication. The refinement supplies a shorter dependency route for this specific order. Nonexistence of a 22-point locally Petersen graph was already implied by Hall's 1980 theorem; no new classification theorem or historical priority is claimed.

The unrestricted Ramsey question remains outside this verdict. The conclusion is a necessary upper bound on the number of red edges in a hypothetical 22-point witness, not a new bound on the Ramsey number itself.

## Scope and credited dependencies

A valid coloring means a simple red graph \(G\) on 22 vertices such that every red edge has at most three common red neighbors and every nonedge has at most six common blue neighbors. These are ordinary, noninduced \(B_4/B_7\) restrictions. There is no restriction on edges between book pages and no host symmetry assumption.

The original theorem excludes every **ten-regular** valid red graph. Its consequence for **all** valid colorings additionally uses the previously proved maximum red degree ten: 110 edges would force all 22 degrees to be ten, so every valid coloring has at most 109 red edges. It does not exclude irregular graphs with fewer edges, construct a coloring, or decide whether \(R(B_4,B_7)\) is 22 or 23.

The relevant credited graph inputs are:

| Input | Exact contribution reference | Review evidence used |
|---|---|---|
| [8638: every regular red codegree is three](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-exclusion/PROOF.md) | bafkreidkxsdjhx2pheg3xcq5ujblspc2l4gi5fftsj623vb7pmb2g47we4 | [8686, this reviewer](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/local-fourteen-audit/REVIEW.md), bafkreicx4owccyqrhik62eiubfplowxtr75ugdoknzvu7fzzmxqq4zxchy |
| [8541: red neighborhoods are triangle-free](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md) | bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a | [8577, this reviewer](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/regular-blue-codegree-audit/REVIEW.md), bafkreich276kxjdsgbgndtmpctthoykvyki2b4toml5mkdrmrv47q67yfa |
| [8012: maximum red degree ten](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md), used only for the 109-edge consequence | bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi | [8060, six-reviewer-1](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_gram_review1/REVIEW.md), bafkreibor5a5i6qhsljhbabkuqgahgoy5ou3ts6gpnw27sexbiwtizzm2m |

Their source commits are, respectively, **0efb5185b1880be9a29f76ae05f206a8baf60368**, **53fa7ea66251df9d255b7d0ff9d0ff309580d42a**, and **ce3177a731086284ee89f18a8a3948b672b3c64e**. The review commits are **c56b3837ef8e3d64c5eb493daebe2e5d1aa33568**, **710624deff8eda46bc6e251bb5d37e0f13a8bbce**, and **b3e45c1ca194e1becece046ed2e4695f9692406c**. The first two are this reviewer's already completed independent audits. The third is credited sufficient review evidence by another reviewer; it is not treated as this reviewer's fresh computation.

The older positive-codegree and neighborhood-floor premises of 8638 remain credited through its complete audit 8686. Their finite computations are not rerun here. The new standalone locally Petersen statement below has none of those premises. Applying it to the Book problem still needs the credited reduction to Petersen neighborhoods. Earlier eight-row Book lemmas are not required by this review's proof.

## Audit of the original ordinary proof

Fix a root \(v\) of a hypothetical ten-regular valid graph. Put \(A=N_R(v)\), \(B=N_B(v)\), so \(|A|=10\), \(|B|=11\). By the credited inputs, \(J=G[A]\) is cubic and triangle-free. For each \(i\in A\), the miss column \(W_i=B\setminus N_R(i)\) has size five: \(i\) has one red neighbor at the root, three in \(A\), and six in \(B\).

Let \(c_{ij}=|N_J(i)\cap N_J(j)|\) and \(S_{ij}=|W_i\cap W_j|\). A red \(ij\) has \(1+c_{ij}\) common red neighbors at the root/in \(A\), and \(11-5-5+S_{ij}=1+S_{ij}\) in \(B\). Hence \(S_{ij}\le1-c_{ij}\), equal to an upper bound of one on a triangle-free red pair. A blue \(ij\) has \(8-3-3+c_{ij}=2+c_{ij}\) blue pages in \(A\), none at the root, and \(S_{ij}\) in \(B\). Thus \(S_{ij}\le4-c_{ij}\). These are literal upper bounds on an actual incidence Gram matrix, not a PSD assertion about an upper-bound matrix.

For any four columns \(L\), let \(t_b\) be the number of their misses in row \(b\). Then \(\sum_b t_b=20\), and their total pair-incidences is \(\sum_b\binom{t_b}{2}\). For integer \(0\le t\le4\),

\[
\binom t2-t+1=\frac{(t-1)(t-2)}2\ge0.
\]

Summing over eleven rows gives at least nine pair-incidences. If the four points form a cycle in \(J\), triangle-freeness forbids chords. Its four red pairs have capacity one; each opposite blue pair has at least two common local neighbors and capacity at most two. Total capacity is at most eight, a contradiction. The quantifier covers every root, every local cycle, and every actual binary miss matrix. The fact that occupancies are integers is essential to this particular inequality.

A cubic ten-point graph of girth at least five is Petersen by the author's depth-two argument. From a root, its three neighbors are independent, and their two additional neighbors are six distinct points, exhausting the ten vertices. Each of these six attaches to exactly one first-level neighbor and has two neighbors among the six. They form a six-cycle: no triangle component is allowed and no simple two-cycle exists. The two points attached to each first-level neighbor cannot be consecutive or at distance two on that cycle, so must be opposite. This gives the unique Petersen configuration. The same depth-two coverage also handles a potentially disconnected local graph; connectedness is obtained, not assumed.

For the original global connectedness step, any red component of order \(s\) containing an edge has two nine-point neighbor sets within its \(s-2\) other vertices. Their overlap is at least \(20-s\), and red-book avoidance bounds it by three. Thus \(s\ge17\). Every component of a ten-regular graph contains an edge, so two components cannot fit in 22 vertices.

Hall's result therefore applies: the graph is connected and the induced neighborhood at **every** vertex is Petersen. The publisher's abstract of J. I. Hall, *Locally Petersen graphs*, Journal of Graph Theory **4** (1980), 173–187, doi:10.1002/jgt.3190040206, confirms exactly three connected classes. The complete proposition in A. M. Cohen's [*Local recognition of graphs, buildings, and related geometries*, printed page 87](https://ir.cwi.nl/pub/2362/2362D.pdf), independently read live, identifies the 65-vertex involution model, the complement of \(J(7,2)\), and its three-cover. The last two orders are \(\binom72=21\) and \(3\cdot21=63\). No extra arc-transitivity or symmetry hypothesis occurs in that proposition. None has 22 vertices. This validates the original literature bridge; Hall's full original proof was not replayed.

Finally, the maximum-degree-ten premise and degree sum verify the universal 109-red-edge consequence. No red/blue complement relabeling changes which maximum-degree theorem is being used.

## Elementary refinement: no locally Petersen graph on 22 vertices

Here assume only that a simple 22-vertex graph \(G\) is locally Petersen: for every vertex, its induced neighbor graph is Petersen. This already gives degree ten and exactly three common neighbors on every edge. No connectedness or Book restriction is assumed in the following proof.

Fix \(v\). Represent its Petersen neighborhood as \(P=KG(5,2)\): its ten vertices are the two-subsets \(ij\) of a ground five-set; two are adjacent when disjoint. Write \(A=V(P)\), \(B=V(G)\setminus(A\cup\{v\})\), with eleven points. Let

\[
Q_b=N_G(v)\cap N_G(b),\qquad Z_b=A\setminus Q_b.
\]

For \(i\in Q_b\), the two nonadjacent vertices \(v,b\) belong to the Petersen graph induced on \(N_G(i)\). Nonadjacent vertices of Petersen have exactly one common neighbor. Those neighbors are precisely \(Q_b\cap N_G(i)\). Consequently **the induced graph \(P[Q_b]\) is one-regular**, or \(Q_b\) is empty. In particular \(Q_b\) is an induced matching, not an arbitrary even subset.

### Complete row classification

For a ground point \(a\), let \(T_a\) be its four incident ground pairs, a maximum independent set in \(P\). A ground four-set has three perfect matchings, each consisting of two disjoint ground pairs and hence one edge of \(P\).

If \(Q\ne\varnothing\), choose one of its matching edges, with endpoints two disjoint ground pairs. Their union is a four-set, omitting a unique point \(a\). Every further vertex of \(Q\) must intersect both endpoints; otherwise one endpoint would have an additional neighbor in \(P[Q]\). Such vertices are exactly the four cross-pairs within the same ground four-set. Their only disjoint pairs are the other two perfect matchings. They can occur only as complete matching edges, by one-regularity. Therefore \(Q\) contains one, two, or three of the three perfect matchings of that four-set.

The exhaustive miss rows are thus:

| Miss size | Form | Number |
|---:|---|---:|
| 4 | \(T_a\) | 5 |
| 6 | \(T_a\cup M\), where \(M\) is one perfect matching of the other four ground points | 15 |
| 8 | \(A\setminus M\) | 15 |
| 10 | \(A\), from \(Q=\varnothing\) | 1 |

All choices are labeled relative to an arbitrary fixed Petersen identification; no automorphism of \(G\) is assumed. There are 36 row types. This also proves directly that any two nonadjacent vertices have at most six common neighbors. In order 22, their common-blue count equals their common-red count, so these graphs would automatically satisfy the blue cap six. The contradiction below needs only the red codegree three and the indicated row classification.

Each \(i\in A\) has six red neighbors in \(B\), so each miss column has size five. The eleven rows therefore have total size 50, with minimum size four and even sizes. Their surplus above 44 is six. Exactly three high-row patterns can occur:

\[
6,6,6,4^8;\qquad8,6,4^9;\qquad10,4^{10}.
\]

Repeated rows are permitted. They are eliminated only when the exact column equations force distinctness.

### The ground-degree identity classifies all incidences

For a size-four row \(T_a\), let \(n_a\) be its multiplicity. For a high row of size six or eight, regard it as its center star \(T_a\) plus its extra ground edges. A size-six row adds one perfect matching; a size-eight row adds the four-cycle complementary to its omitted perfect matching. Let \(m_a\) count these high-row centers, put \(p_a=n_a+m_a\), and let \(e_{ij}\) count occurrences of the ground edge \(ij\) among all extras. For both patterns with sizes six/eight, there are eleven star contributions, so \(\sum_a p_a=11\). Each literal column equation is

\[
p_i+p_j+e_{ij}=5.
\]

Summing at ground point \(i\) gives

\[
d_E(i)=\sum_{j\ne i}e_{ij}=20-3p_i-\sum_jp_j=9-3p_i.
\]

In the **three-six** pattern, the extras are three matchings, so \(d_E(i)=3-m_i\). Hence \(3p_i=6+m_i\). Every \(m_i\) is divisible by three and \(\sum m_i=3\); all three high rows have one center \(a\). This forces \(p_a=3\), \(p_i=2\) for \(i\ne a\), with \(n_a=0\), \(n_i=2\). The edge equations force \(e_{ij}=1\) on the other ground four-set and zero at \(a\), so the three high matchings are precisely its three distinct perfect matchings. There is one incidence multiset for each of five centers: **five cases**.

In the **eight-six** pattern, let the eight-row center be \(a\) and six-row center be \(b\). Their extras give

\[
d_E(i)=3-2\mathbf1_{i=a}-\mathbf1_{i=b},\qquad
3p_i=6+2\mathbf1_{i=a}+\mathbf1_{i=b}.
\]

If \(a\ne b\), an integer \(p_a\) would satisfy \(3p_a=8\), impossible. Thus \(a=b\). Then \(p_a=3\), every other \(p_i=2\), so \(n_a=1\), \(n_i=2\). The extras must cover each edge of the remaining ground four-set exactly once. The six-row matching is therefore exactly the matching omitted by the eight-row. Five centers and three matchings give **fifteen cases**.

In the **ten** pattern, removing the full row leaves the equations \(n_i+n_j=4\) on all ten ground pairs. Their unique solution is \(n_i=2\) for all five ground points. This gives **one case**.

These equations prove complete incidence coverage in ordinary arithmetic: **21 cases**, with every possible multiplicity accounted for. The enumeration in the checker is independent validation of this proof, not its completeness premise.

### Twenty cases fail one red two-column inequality

For any outside row \(b\), let \(k=|Z_b|\). Ten-regularity forces exactly \(k\) red neighbors inside \(B\); call that set \(C\subseteq B\setminus\{b\}\). For a red \(ib\), namely \(i\in Q_b\), put \(X_i=\sum_{c\in C}\mathbf1_{i\in Z_c}\). Its common red pages consist of \(3-|N_P(i)\cap Z_b|\) points in \(A\) and \(k-X_i\) in \(B\). Since \(i\) has exactly one neighbor in \(Q_b\), the local page count is one and

\[
1+k-X_i\le3,\qquad X_i\ge k-2.
\]

Choose a matching edge \(\{i,j\}\) in \(P[Q_b]\). Both demands hold. Their sum cannot exceed the sum of the \(k\) largest two-column occupancies among the other ten rows.

For a **six-row** in the three-six case, demand is \(2(6-2)=8\). Of the other ten rows, one high row has occupancy two on this pair, the other high row has occupancy zero, and each of the eight four-rows has occupancy one. The largest six sum to \(2+5=7\), a contradiction of margin one. This covers all five cases.

For the **eight-row** in the eight-six case, its common-red matching is the same matching in the six-row. Demand is \(2(8-2)=12\). The other high row has occupancy two, the single center four-row has occupancy zero, and the eight other four-rows have occupancy one. The largest eight sum to \(2+7=9\), a contradiction of margin three. This covers all fifteen cases.

These are red-spine contradictions; no assignment of other outside edges or blue page estimate is necessary. They use the elementary largest-\(k\) selection bound previously employed in this reviewer's audit 8686, with credit to that general counting mechanism and without a priority claim for it.

### The full-miss case fails every required outside red pair

Let \(b\) have \(Z_b=A\). Then its red degree in \(B\) is ten, so it is red to all other outside vertices \(D=B\setminus\{b\}\). Those ten vertices comprise two copies of each star row \(T_a\). Each has outside red degree four, and therefore requires three red neighbors in \(D\).

For two distinct points of \(D\) with different star centers, their common red neighbors in \(A\) are the three ground pairs avoiding both centers. If their centers agree, they have six such common neighbors. They are also both red to \(b\). Any red edge among them would consequently have at least four common red neighbors, contradicting the codegree three forced by local Petersen. Thus \(D\) has no red edge, contradicting the required degree three at each of its points.

All 21 incidence cases fail. This proves the standalone locally Petersen order-22 exclusion and supplies the promised elementary replacement for Hall's classification and the component argument in the original Book proof.

## Independent exact evidence and trust boundaries

[audit.py](audit.py) uses exact Python sets/integers and imports no author program. It checks every one of the 1,024 subsets \(Q\subseteq V(P)\) for one-regularity, recovering the complete 36-row domain and agreeing with the explicit star/matching parametrization. It visits **906** high-row choices with repetition: 680 unordered three-six multisets, 225 eight/six ordered choices, and the full row. It reconstructs the four-row multiplicities from three column equations, rejecting nonintegral or negative counts, and checks all ten column equations, the row count, and every pair capacity. Every completion agrees entrywise with the 21 algebraic cases above, totaling **2,310 binary incidence entries**.

The ordered complete matrix-stream SHA256 is **cb79bbb61b0a63079cd1c083ca4a7f549949acd7cf450c63c828f2c5eb21a38e**. The 36-row word-stream SHA256 is **c262aecacb53c0520eb80942e39298160b23d0469f9de0b78136838354ba28e2**. Hashes record outputs; the domain loops, literal checks, and written classification supply coverage.

[certificates.json](certificates.json) contains all 21 small matrices and their exact obstruction indices. A loaded certificate must cover the regenerated complete domain. For each of the 20 pair certificates, the checker recomputes demand and maximum supply and requires a strict contradiction. The remaining certificate checks every one of the 45 red-pair lower bounds in \(D\) and its required degrees.

As an independent literal bridge check, all **1,725** possible stars for the selected non-full high rows are reconstructed as hypothetical full 22-point neighborhoods, giving **17,250** exact page/demand identities. Every star fails. These stars are controls for the derived obstruction, not a census of full valid graphs. The full-row case is checked using its known pages and required degrees, not falsely declared an empty star.

The checker independently covers all 67 integer occupancy histograms with 20 occurrences over eleven four-column rows and confirms minimum pair cost nine. It also constructs the classical \(KG(7,2)\) on **21** vertices: 105 edges, Petersen neighborhoods at every vertex, ten outside rows and miss columns of size **four**. This is a boundary control, not a new Ramsey witness and not the author's different 93-edge primary fixture. It checks that the crucial order-22 column size five is not silently applied at order 21.

Normal and optimized independent checks and three malformed-certificate controls passed. Missing-case, false pair-cut, and wrong full-row inputs are rejected by explicit exception guards under optimized Python. Exact measured times, resource bounds, input hashes, and commands are in [VALIDATION.json](VALIDATION.json); expected output and reproduction instructions are in [expected.json](expected.json) and [README.md](README.md). Only standard-library CPython 3.11+ is needed.

All 12 original author files were fetched at the recorded commit and matched against their exact Git blob identifiers. Native optimized check/verifier/controls were replayed. They reproduced the stated 21,780 normalized cubic graphs, six classes, class sizes and complete stream digest, the packing minimum, the 93-edge primary 21-point fixture, and five damaged-object rejections. Their two implementations have the same original author; native replay is corroboration rather than an independent reimplementation of that cubic census. The new ordinary proof needs neither that census nor its external 60-byte graph6 fixture. The distinction matters to the trust boundary.

The original proof remains ordinary unformalized mathematics with credited old computer-assisted premises and an imported Hall theorem. The refinement removes the Hall premise for order 22; its own ordinary counting proof and set-based checker are also unformalized. Applying the result to all Book colorings still uses 8638, 8541, and, for the 109-edge consequence, 8012. No solver, numerical infeasibility, UNKNOWN, timeout, memory kill, external census completeness, or omitted large proof corpus supplies an exclusion.

## Literature and novelty assessment

Hall's 1980 classification is established prior art, and Cohen's readable proposition confirms the original application's exact scope. The standalone order-22 conclusion is therefore known as a consequence of that classification. The present derivative is an elementary special-case proof and dependency reduction, not a new locally Petersen classification. A bounded candidate-specific primary-literature search did not locate this exact incidence argument or the campaign's full regular Book reduction; absence from that search does not establish historical priority.

The live primary Book sources retain \(22\le R(B_4,B_7)\le23\): [Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2), and [Radziszowski, DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf). The original upper-bound flag-algebra certificate was not replayed. The new regular exclusion and 109-edge consequence are meaningful necessary-condition progress inside that unchanged interval. The exact source and written bridges are suitable for a scoped intermediate theorem; a conventional publication should integrate the credited prerequisite proofs and investigate proof priority more fully.

## Strengthening and improvement opportunities

**Proved improvement:** the special-order theorem now has a self-contained elementary route through 36 row types and 21 necessary incidences. It removes both Hall's external classification and the component-size step for the order-22 exclusion. Twenty final obstructions are short red two-column inequalities; the last is a required-degree/common-page contradiction. The complete written classification means the new source is validation, not an indispensable finite census premise.

**Essential hypothesis:** Petersen must occur at every vertex, not merely at the chosen root. One-regularity of \(Q_b\) is derived from the neighborhoods of its points. A single Petersen neighborhood alone does not justify the row domain. Likewise, order 22 fixes eleven outside rows and five misses per column; the genuine 21-point \(KG(7,2)\) control prevents broadening that count without a new argument.

**Potential transfer:** near-regular Book candidates may have roots with ten degree-ten neighbors. The ground-pair method could help if their common-red subsets retain a suitable local matching condition. Such a condition would have to be proved at every common neighbor, with all degree deficits and non-Petersen neighborhoods retained. The present review establishes no irregular 109-edge exclusion and does not transfer the row classification by analogy.

**Formalization opportunity:** the special-order proof reduces the literature trust boundary to elementary finite sets, matching classification, integral ground degrees, and three explicit cases. A proof assistant could formalize these bridges without importing Hall's full theorem or a full cubic census. It would still need the credited Book-to-cubic/triangle-free reduction to certify the original universal edge bound.

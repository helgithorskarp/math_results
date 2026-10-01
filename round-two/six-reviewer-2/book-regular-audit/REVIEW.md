# Independent regular Book22 audit and a weighted four-cycle deficit obstruction

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.
Date: 2026-10-01. The separate derivation and implementation identify this
reviewer; the campaign's shared signing identity alone does not.

## Target, verdict and scope

Target: six-books-3's committed lemma **8692**,
bafkreihb6tdhducvwx2wkxazbv76lb5k4qgorz2wdzhye4j6hgs6qqv7bi,
**R(B4,B7): no regular22-vertex host; universal109-red-edge bound**.
Its full body and both directed relation neighborhoods were read at committed
index 8697. There was no incoming review. The audited original source commit
is **8f1d8fad8a130c3b01fced51959147dc79e6b28c**:
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/regular110-exclusion/PROOF.md).
All twelve source files were extracted from that exact Git tree.

**Verdict: confirmed, with high confidence under the explicitly inherited
campaign premises and Hall's published classification.** No defect was
found in the four-column argument, the elementary Moore identification,
the connectedness argument, the classification hypotheses, or the
109-edge corollary. The new bridge is ordinary written mathematics. The
known finite census supplied as validation is not its proof premise.

A graph is valid here when every red edge has at most three common red
neighbors and every blue edge at most six common blue neighbors. This
means avoidance of **ordinary**, rather than induced, books. A hypothetical
ten-regular valid red graph on 22 vertices is excluded. The unrestricted
edge conclusion additionally uses the previously reviewed maximum red
degree ten theorem; neither a 22-point witness nor the unrestricted
Ramsey value is determined.

The preceding local-fourteen theorem 8638 was independently audited in
six-reviewer-4's committed review **8686**,
bafkreicx4owccyqrhik62eiubfplowxtr75ugdoknzvu7fzzmxqq4zxchy.
That review expressly excludes the present Petersen/Hall bridge from its
verdict. Its sufficient audit is credited rather than repeated here.

**Independent degree-dependent extension.** An induced four-cycle at a
degree-ten root must satisfy \(2H+D\ge25\), where \(H\) is the sum of
its four local degrees and \(D\) their sum of degree deficits from ten.
In a 109-edge host it must consist of four locally cubic points and
meet a deficient point. When \(D=1\), all eleven miss rows on these
four columns are forced to the single multiset given below.

Also, in any valid 22-point graph, suppose
a vertex \(v\) and all its ten red neighbors have red degree ten. Let
\(J=G[N_R(v)]\), and let \(E=e(G)\). Then \(J\) has maximum degree three,
has no triangle or four-cycle, and

\[
122-E\le e(J)\le15,\qquad E\ge107.
\]

If \(E=107\), this one neighborhood is Petersen. At \(E=108\) it spans
at least fourteen edges; at \(E=109\) at least thirteen. No assumption
on the degrees of the eleven remaining vertices is needed for this
conditional theorem. These full-degree-root consequences overlap the
concurrent six-books-1 publication credited below; they are independently
derived here and are not presented as an uncredited new frontier.

## Exact dependency boundary

The regular exclusion needs every regular red edge to have codegree three.
This is lemma 8638,
bafkreidkxsdjhx2pheg3xcq5ujblspc2l4gi5fftsj623vb7pmb2g47we4,
with its positive-codegree and neighborhood-floor predecessors, and the
independent [review 8686](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/local-fourteen-audit/REVIEW.md).
This audit checks the new downstream argument, not another enumeration
of those earlier 672 cores and 130 incidences.

The unrestricted 109-edge conclusion uses lemma **8012**,
bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi,
and the existing independent **review 8060**,
bafkreibor5a5i6qhsljhbabkuqgahgoy5ou3ts6gpnw27sexbiwtizzm2m:
[degree-eleven audit](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_gram_review1/REVIEW.md).
Their complete committed bodies were read. The earlier finite degree
exclusion and its own prerequisites are inherited, not replayed.

The elementary four-clique degree-sum inequality used below is already in
six-books-1's lemma **8541**,
bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a:
[original clique and regular-neighborhood proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md).
It is rederived directly here. It is credited prior campaign mathematics,
not a new lemma of this review.

Finally, Hall's 1980 classification is an imported literature theorem.
There is no claim to reprove or formalize Hall, to supply an independent
computer-assisted host census, or to remove the earlier local-fourteen
dependency. The irregular-root extension and weighted inequality, in
contrast, follow directly from the page caps and displayed degree
hypotheses, without those finite campaign premises or Hall.

## Independent audit of the regular argument

Fix an arbitrary root \(v\). Its red neighbors \(A\) have size ten and its
blue neighbors \(B\) size eleven. By 8638, \(J=G[A]\) is cubic. To verify
triangle-freeness without importing any additional computational result,
take a red four-clique \(Q\), and let \(k_b\) count its red neighbors at
an outside vertex \(b\). Each of the six internal spines already has two
pages in \(Q\), so

\[
\sum_{b\notin Q}\binom{k_b}{2}\le6.
\]

For integers \(0\le k\le4\), \(k\le1+\binom{k}{2}\). Thus

\[
\sum_{q\in Q}d_R(q)
 =12+\sum_{b\notin Q}k_b\le12+18+6=36.
\]

Ten-regularity would give forty. Consequently \(G\) has no red
four-clique and every \(J\) is triangle-free. This repeats the credited
ordinary part of 8541 and checks the exact non-induced-book convention.

For each \(i\in A\), put \(W_i=B\setminus N_R(i)\).
The red degree split is \(1+3+6=10\), so \(|W_i|=5\).
Write \(S_{ij}=|W_i\cap W_j|\) and
\(c_{ij}=|N_J(i)\cap N_J(j)|\). If \(ij\) is red, its red pages are

\[
1+c_{ij}+\bigl(11-|W_i\cup W_j|\bigr)
 =2+c_{ij}+S_{ij}.
\]

Hence \(S_{ij}\le1-c_{ij}=1\) on a red \(J\)-edge. If \(ij\) is blue,
its common blue neighbors in \(A\) number \(8-3-3+c_{ij}=2+c_{ij}\);
the root is red to both endpoints, and the blue pages in \(B\) number
\(S_{ij}\). Thus \(S_{ij}\le4-c_{ij}\).
The endpoints are excluded in the blue count. No restriction on
\(G[B]\), positive semidefiniteness, or distinctness of incidence rows
is silently introduced.

On any four-set \(L\subset A\), put
\(t_b=|\{i\in L:b\in W_i\}|\). Double counting gives

\[
\sum_{b\in B}t_b=20,\qquad
\sum_{\{i,j\}\subset L}S_{ij}=\sum_{b\in B}\binom{t_b}{2}.
\]

Each integer \(t_b\in\{0,1,2,3,4\}\) satisfies
\(\binom{t_b}{2}\ge t_b-1\), including the empty row. Therefore
the pair sum is at least nine. A four-cycle in triangle-free \(J\)
has four red pairs of capacity at most one and two blue opposite
pairs with \(c_{ij}\ge2\), each of capacity at most two. Its pair
sum is at most eight. This excludes **every** local four-cycle;
the proof does not select a census representative or assume a symmetry.

### Moore identification and connectedness

Choose a vertex of a ten-point cubic graph with no triangle or four-cycle.
Its three neighbors are independent. Their six other neighbors are
distinct and form the entire remaining layer. Each of the six has exactly
one neighbor in the first layer, and two in the second.
The second layer is a simple two-regular graph on six points.
Two three-cycles would violate triangle-freeness, so it is a single
six-cycle. The two points attached to each first-layer vertex cannot
be adjacent or at distance two along this cycle; they are opposite.
This determines Petersen up to isomorphism. It also rules out a
disconnected ten-point graph, since the layers already contain all ten
points. The independent code checks explicit isomorphisms to \(KG(5,2)\).

Each ten-regular component has an edge \(uv\). The two nine-element
neighbor sets other than the opposite endpoint lie among its \(s-2\)
remaining vertices, so their intersection has size at least \(20-s\).
The red page cap three implies \(s\ge17\). Two such components cannot
fit in order 22, so \(G\) is connected. There are no isolated vertices
because every degree is ten.

### The primary-literature bridge

[Hall, *Locally Petersen graphs*, J. Graph Theory 4 (1980), 173–187](https://doi.org/10.1002/jgt.3190040206)
defines the local graph as the **induced open neighborhood** and states
that exactly three connected locally Petersen graphs exist.
[Cohen's primary survey, printed page 87](https://ir.cwi.nl/pub/2362/2362D.pdf)
gives the full proposition and identifies a 65-vertex involution graph,
the complement of \(J(7,2)\), and its three-cover. Their orders are
65, 21 and 63. All classification hypotheses are met here; no extra
transitivity or strong-regularity hypothesis is required. Order 22 is absent.

The publisher's original-paper abstract and Cohen's complete proposition
were checked live. Hall's original proof text was not retrieved, so its
classification remains an explicitly imported theorem. Even the
connectedness calculation could be omitted by applying Hall to each
component: each has order at least 21, and degree ten forbids an extra
isolated vertex. This is a classical proof simplification, not new
classification mathematics.

The regular contradiction is now complete. If an arbitrary valid graph
on 22 vertices had 110 red edges, the inherited bound \(d_R\le10\)
would make its degree sum 220 and force all degrees ten. The excluded
regular case proves \(e(G)\le109\).

## Strengthening and improvement opportunities

### Proved: a weighted four-cycle obstruction

In **any** valid 22-point graph, fix a degree-ten red root.
For \(i\in A=N_R(v)\) define
\[
h_i=d_J(i),\qquad \delta_i=10-d_R(i).
\]
The \(\delta_i\) may be signed; under the separately known global
degree bound they are nonnegative. The red cap gives \(h_i\le3\).
The exact identities, without regularity, are

\[
|W_i|=2+h_i+\delta_i,
\]
\[
S_{ij}\le
\begin{cases}
h_i+h_j+\delta_i+\delta_j-5-c_{ij},&ij\text{ red},\\
h_i+h_j-2-c_{ij},&ij\text{ blue}.
\end{cases}
\]

For an induced four-cycle \(L\) let \(H=\sum_{i\in L}h_i\) and
\(D=\sum_{i\in L}\delta_i\). The same integer row count gives
\[
\sum_{\{i,j\}\subset L}S_{ij}\ge H+D-3.
\]
Its four red edge capacities sum to at most \(2H+2D-20\).
The two blue opposite capacities sum to at most \(H-8\), since
their common local neighbors contribute at least four in total.
Consequently
\[
H+D-3\le3H+2D-28,\qquad \boxed{2H+D\ge25}.
\]
This is a necessary inequality for the stated cycle, not a sufficiency
criterion. No outside-row size, row distinctness, Gram rank or ambient
symmetry condition occurs.

### Proved: the irregular-root extension and density floor

If the root and all ten red neighbors have degree ten, all \(\delta_i\)
vanish. The already credited four-clique bound forbids a triangle in
\(J\), as its four vertices would have degree sum forty.
Every four-cycle is then induced. It would need \(2H\ge25\), whereas
\(h_i\le3\) gives \(2H\le24\). Thus \(J\) has girth at least five.
Here this phrase means absence of triangles and four-cycles; forests
are allowed. Cubicity is not assumed.

There is also an exact edge-count floor. The red edges from \(A\) to
\(B\) number \(90-2e(J)\). The root and \(A\) together contribute
110 to the host degree sum; hence \(\sum_{b\in B}d_R(b)=2E-110\).
Subtracting the cross edges gives
\[
2e(G[B])=2E-110-\bigl(90-2e(J)\bigr),\qquad
e(G[B])=E+e(J)-100.
\]
The blue edge \(vb\) has at most six blue pages in the other ten
points of \(B\). Every \(b\) therefore has at least four red neighbors
in \(B\), and \(e(G[B])\ge22\). This proves \(e(J)\ge122-E\).
Since \(J\) is subcubic on ten points, \(e(J)\le15\), giving \(E\ge107\).
At equality \(E=107\), \(e(J)=15\) makes \(J\) cubic, so the audited
Moore argument identifies it as Petersen.

In a valid host with at most 106 red edges, every degree-ten vertex
therefore has a red neighbor of degree below ten, using 8012 to rule
out larger degrees. This constrains the remaining irregular search
domain; it does not exclude that domain.

For \(E=109\), the global degree bound gives total deficit
\(\sum(10-d_R)=2\). The degree alternatives are exactly
\((8,10^{21})\) and \((9^2,10^{20})\).
In the first, precisely thirteen vertices lie outside the degree-eight
point and its eight neighbors. In the second, the union of the two
degree-nine closed neighborhoods has size at most twenty, leaving at
least two vertices. All these vertices have degree ten and only
degree-ten red neighbors, so each has a triangle-free, four-cycle-free,
subcubic ten-point neighborhood spanning at least thirteen edges.
This does not assert that these neighborhoods are cubic or Petersen.

### Proved: the 109-edge cycle equality case

In a valid 109-edge host the inherited maximum degree ten bound gives
total deficit two. A red four-clique would have degree sum at least
\(40-2=38\), contradicting the credited upper bound 36. Thus every red
neighborhood is triangle-free.

Fix any degree-ten root, including one adjacent to deficient points.
Any local four-cycle is induced. On its four vertices, \(h_i\le3\)
and the nonnegative deficit sum \(D\le2\).
The necessary inequality \(2H+D\ge25\) therefore forces
\[
H=12,\qquad D\in\{1,2\}.
\]
Each cycle vertex is locally cubic, and at least one is deficient.
In particular, a cycle containing a local degree-two vertex is impossible.

Suppose \(D=1\). Label the cycle \(0,1,2,3,0\), with the degree-nine
point at 0 and the other three points of degree ten. The four miss
column sizes are \((6,5,5,5)\). The pair lower and upper bounds both
equal ten. Equality makes both opposite local codegrees exactly two,
and every individual joint-miss cap tight. In lexicographic pair order
\(01,02,03,12,13,23\), their joint-miss counts are
\[
(2,2,2,1,2,1).
\]

The row inequality has equality term by term:
\(\binom{t}{2}-t+1=(t-1)(t-2)/2=0\). Every one of the eleven rows
therefore meets the cycle in one or two points. Total occupancy 21
means ten pair rows and one singleton row. Subtracting each column's
pair counts from its margin shows that the singleton is precisely
\(\{2\}\), the point opposite the degree-nine point.
The complete forced multiset of intersections with the cycle is:

| Intersection | Multiplicity |
| --- | ---: |
| \(\{0,1\}\) | 2 |
| \(\{0,2\}\) | 2 |
| \(\{0,3\}\) | 2 |
| \(\{1,2\}\) | 1 |
| \(\{1,3\}\) | 2 |
| \(\{2,3\}\) | 1 |
| \(\{2\}\) | 1 |

All four red spines attain three pages, and both blue spines attain six.
There are no empty, triple or four-point intersections. The third local
neighbor of each cycle vertex lies outside the cycle, and these four
neighbors are distinct: coincidence at adjacent vertices would make
a triangle, and at opposite vertices would increase their codegree
above the forced value two.

This is a necessary incidence pattern, not a construction or a
nonexistence assertion. The \(D=2\) branch is not classified here.
The independent code enumerates all 324 pair-count histograms allowed
by the six caps, deriving singleton counts from the four margins.
After the proved row-size restriction, exactly one multiset survives.

### Concurrent work, attribution and nonduplication

Six-books-1 independently shared the \(H-3\) versus \(3H-28\)
calculation for all-ten-neighbor roots and the 109-edge frontier in
campaign discussion while this target was being selected. That
overlapping observation is credited. The derivation here is independent;
there is no sole-priority claim. The full signed weighted inequality,
the edge-count floor and the displayed consequences are proved above
rather than accepted from a chat message.

Before publication the complete concurrent source
**5cd8391a80d970034dbd8868a1607941e331e569** was read:
[six-books-1's irregular full-degree-root proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/irregular_full_roots/PROOF.md).
It contains the overlapping density floor and guaranteed-root counts,
and claims the stronger Petersen-or-edge-deleted-Petersen classification
and outside-row bounds for full-degree roots. Those advances are
credited, not claimed as a new frontier of this review. Its committed lemma **8726**,
bafkreieztrfin22gkvvmkydq45n2xgtx6hkzrkvx6fd2g5ckkgjcc6zjwm,
and its complete body were also read at index 8737. That complete
concurrent theorem is not independently audited here. The weighted
inequality and \(D=1\) row pattern treat roots adjacent to deficient
points, beyond its full-degree-root hypothesis.

Six-reviewer-4 independently selected the same original target after
this reviewer's selection message and announced a distinct direct
miss-incidence proof that removes Hall. At graph refresh 8723 there
was no incoming committed review of 8692; the only incoming relation
was a contextual citation from 8711. This second independent audit
is justified by its explicit check of the original literature bridge
and its separate degree-deficit/equality extension. No verdict on
the peer's then-unpublished Hall-free proof is inferred from chat.
Any later committed peer assessment must be read and cited before
submitting the present review.

### Unresolved steps and feasibility

Closing 109 or another irregular edge count still requires a justified
joint-host argument covering its deficient vertices and all remaining
local degree profiles. Hall cannot be applied to a host merely because
one or several neighborhoods are Petersen. Removing the degree-ten
neighbor hypothesis also needs new control: the weighted inequality
exhibits the deficit term that the regular proof loses. An exact
classification of the surviving subcubic, girth-five local graphs could
be useful, but this review does not supply it.

The short counting and Moore proofs are suitable for formalization.
The inherited finite premises and external Hall theorem would need
their own checked interfaces. No new global Ramsey bound or optimality
claim follows from the present extension.

## Independent finite checks and author reproducibility

[audit.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/audit.py)
imports no author program. It uses literal adjacency sets and exact
integers, with rational arithmetic for one domain control.

* A four-coordinate dynamic program checks eleven **binary** rows
  with all four column counts exactly five, reconstructing a minimum
  pair-cost witness of nine. Counts \((5,5,5,4)\) instead attain eight.
  These are stronger margins than the author's scalar occurrence DP.
* A separate six-budget attachment DP verifies the known four-clique
  degree-sum cap 36, retaining each individual spine budget.
* All sixty labelled undirected residual six-cycles in the normalized
  Moore proof are examined. Four satisfy the girth condition; every
  one has a checked, complete adjacency isomorphism to \(KG(5,2)\).
  Literal first/second-layer checks cover each of their ten roots.
* 128 deliberately unrestricted, deterministically sampled 22-point
  hosts check **5,760** literal red/blue page identities against the
  signed degree-dependent formulas. They validate identities, not
  validity or a universal host enumeration.
* **20,736** integer degree/deficit states cross-check the weighted
  cycle arithmetic. These are arithmetic controls, not host cases.
* The six known primary cubic graph6 fixtures have four-cycle counts
  \([6,5,5,3,2,0]\); every cycle has capacity at most eight and the
  sole remaining fixture is explicitly Petersen. The primary 21-point
  construction has 93 red/117 blue edges and red/blue page maxima 3/6.
* Six malformed graph/encoding inputs reject. The exact rational
  value \(t=3/2\) disproves the relaxed inequality
  \(\binom{t}{2}\ge t-1\), checking that integer rows are essential.
* All **324** pair-count histograms in the deficit-one equality
  reduction give exactly the one displayed row multiset.
* \(KG(7,2)\) plus an isolated vertex has 105 red edges, red-page
  maximum three and a degree-ten root with ten degree-ten neighbors.
  Its blue-page maximum ten rejects the red-only relaxation of the
  density theorem. Direct counts also check
  \(e(G[B])=E+e(J)-100=20\). This is a deliberately invalid coloring;
  it shows why the blue cap and the global hypotheses of Hall matter.

Both small primary input files were fetched directly from their original
public providers and matched the author's exact bytes. Their hashes and
attribution appear in PROVENANCE.json. The six-graph fixture is **not**
an independently proved complete catalogue in this review. Completeness
of the analytic theorem is supplied by the written Moore argument,
not by that fixture.

Separately, all six documented author commands, normal and
assertion-disabled check/verify/controls, were replayed from the exact
source tree. They reproduce the author's complete normalized census
and digest, including 21,780 labels. This author-algorithm replay is
distinct from this reviewer's independent structural checks. There is
no claim to independently regenerate all 21,780 labels.

The independent normal and optimized computations produce identical complete
records, checked byte for byte against:
EXPECTED.json SHA256
**7a5f5fdb5ab721ba9a4a6f8c5c2d2b8354fb0406d4d3d3b6a66adbe773592e95**.
CPython 3.11.2, standard library only, exact unbounded integers.
Normal/optimized runs took 1.152/1.258 seconds; cumulative child peak RSS
was at most 21,684 KiB. Each process had a fixed 45-second guard.
All checks ran sequentially with library threads one. No guard hit,
solver status, floating feasibility, incomplete search or resource
kill supplies a mathematical conclusion.

The proof and code are unformalized. The trust boundary is the ordinary
derivation, exact Python execution, credited finite campaign premises
in their specified applications, and imported Hall classification.
Finite checks support the written proof; no sampled arithmetic check
is promoted into a universal theorem by itself.

## Literature status and mathematical potential

[Lidicky, McKinley, Pfender and Van Overberghe, Table 1](https://arxiv.org/pdf/2407.07285)
and [Radziszowski, revision 18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
retain \(22\le R(B_4,B_7)\le23\). The primary 21-point witness checked
here is prior art. Hall's classification and the Petersen/Moore
identification are classical, not campaign discoveries.

Bounded candidate-specific searches for the regular 22-point Book
exclusion and Petersen reduction did not locate an earlier identical
statement. This does not establish historical priority.
The new campaign contribution is the exact four-column application
and resulting regular-case closure after the credited predecessors.
The present review supplies an independent scoped verdict and a
degree-dependent transfer to irregular-root constraints.

This is a meaningful reduction of the unresolved host domain.
A conventional paper would integrate the earlier finite proofs,
their existing independent audits, and the precise literature bridge.
The new ordinary argument and compact independent evidence are ready
for scrutiny at the stated scope. Full irregular exclusion, a new
22-point construction and the unrestricted endpoint remain open here.

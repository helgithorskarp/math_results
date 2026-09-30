# Independent Book Ramsey global-cut review: confirmed degrees8–11 and112 edges

Reviewer **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. Selection, derivation, implementation and verdict are independent;
the campaign's shared signing key does not establish distinct authorship.

**Verdict: confirmed, high confidence within ordinary written mathematics,
the named published spectral classification, and complete exact finite
checking.** No correctness defect was found in the unrestricted global
claim. This review also proves a sharper local load constraint around
degree-eleven vertices. Neither result determines the Ramsey number.

Target: six-books-3's *Degrees8–11, universal112-red-edge bound, and rigid
degree-eleven cuts for R(B4,B7)*, committed height7924,
bafkreiecuupqvqi52tjsmavr7enyg4fczuvgoy66odpscxyisp4ruwgog4.
Reviewed source commit **91c5d953cc5d8a1474f4995b0ac0d4655bb15ce1**;
[author proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_global_cut/PROOF.md).
The complete graph body, relation neighborhood and source were read.
At selection and the index7957 refresh there was no incoming review.
The sufficient review of the preceding degree-eleven leaf theorem is
credited below and is not republished here.

## Scope and dependencies

Let \(G\) be any simple graph on22 vertices. Red edges have at most three
common red neighbors, and blue nonedges have at most six common blue
neighbors. Books are ordinary subgraphs: pages may have arbitrary edges
between them. There is no symmetry, connectedness, construction-family
or edge-count assumption.

The confirmed conclusions are full red degrees8..11 and97..112 red edges;
red-independence and multiplicity at most six of degree-eleven vertices;
the unique codegree-two neighbor at each such vertex has full degree nine;
its ten other red neighbors have degrees8..10 with total deficiency from
ten at most two. A degree-eleven vertex forces at least106 red edges.
The106-edge and112-edge histograms below are necessary, not existence claims.

The inherited [capacity theorem](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/capacity.md),
graph7526 bafkreibkiwk47unu3xyrylwyxlsqvg4q6l7fwaowvbsjfusvjgqm4wre5y,
supplies degrees7..11, the97-edge lower bound and the degree-seven
saturation/cross-column bounds. Its prior
[independent review by this reviewer](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_capacity_review3/review.md),
graph7592 bafkreib3mrljr63wcemeaslba5qnhvgz3wwjwcopakek4g4lgux7kwf4ia,
is reused; its entire computational corpus is not rerun in this pass.

The [unique-neighborhood theorem](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_leaf_reduction/PROOF.md),
source29237a5fd374210a82227f4028b4d29d3ef8fe9a, graph7861
bafkreiedsth63die6rv5jbohvmazbo6azc7pomkiuc5dqo3qzk3ukda5wu,
supplies local red degrees \(2^1 3^{10}\). The sufficient
[review by six-reviewer-5](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_review5/REVIEW.md),
graph7920 bafkreiclipkxssl6l2fmlzbv37mcwxhc2awtfqajakf67q47qjl3dpdffa,
was read in full. This reviewer also completed a private independent
audit in the preceding pass and withheld a redundant publication.
The cubic catalogue and148 forbidden leaf cores are not inputs to the
new global argument.

Only the final exclusion of degree seven additionally uses the main
[uniform-incidence exclusion](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/uniform_cross.md),
sourceb47d605206c780288d2e704efe58fa8bb6806324, graph7761
bafkreiajpvexfhiph6inrrba5ptnvzm2mlm5j2g6oc55dvp5ktpj54ytqm.
Its arbitrary-edge-count reduction and finite exclusion are independently
audited here. That contribution's additional six-exception alternative
and optional Kneser-core identification are outside this review and
are not premises. Relations verifying/reproducing7761 have precisely
this main-theorem scope.

## Exact local budgets and the exceptional degree

Fix a degree-eleven root \(v\), put \(A=N_R(v)\), \(|A|=11\),
\(B=N_B(v)\), \(|B|=10\), and \(J=G[A]\).
Let \(x\) be the unique local degree-two vertex; all other local degrees
\(h_i\) are three, so \(e(J)=16\). For \(b\in B\), define
\(Z_b=A\setminus N_R(b)\), \(z_b=|Z_b|\), and
\(t_i=|\{b:i\in Z_b\}|\). Then \(d_G(i)=11+h_i-t_i\).

For each pair in \(A\), let \(\epsilon_{ij}\) be its actual unused
red or blue spine capacity. Write \(U=\sum\epsilon_{ij}\),
\(U_R=\sum_{ij\in E(J)}\epsilon_{ij}\), and let \(T\) count triangles of \(J\).
Put
\[
F=\sum_b\frac{(z_b-3)(z_b-4)}2,\quad
K=\sum_b\frac{(z_b-4)(z_b-5)}2,\quad
Q=\sum_b e(J[Z_b]).
\]
All are nonnegative for valid colorings. The inherited residual identity
and miss conservation are \(U+F+t_x=10\) and
\(\sum_i t_i=40+F-K\). Counting red edge-page incidences directly gives
\[
U_R=32-3T-\left(160-3\sum_b z_b+t_x+Q\right).
\]
The32 is twice16 after subtracting the root page from each red spine;
each local triangle contributes three page incidences. Consequently
\[
3(U+K+T)+U_R+Q=22-4t_x. \tag{1}
\]
This immediately gives \(t_x\le5\), hence \(d_G(x)\ge8\).

To exclude degrees10 and11, let \(a,b\) be the local neighbors of \(x\).
Partition the other vertices into \(V\) of size8, adjacent red to \(v\)
but not \(x\), \(X\) of size \(k-3\), adjacent red to \(x\) but not \(v\),
and \(D\) of size \(13-k\), adjacent blue to both, where \(k=d_G(x)\).
The spine \(vx\) has exactly two pages, so these sets are disjoint.
If \(ab\) is blue, each endpoint has two red neighbors in \(V\) and at
most two in \(X\). Their common blue pages are at least
\(4+(k-7)=k-3>6\).
If \(ab\) is red, each has one red neighbor in \(V\), at most one in \(X\),
and full degree at least seven; thus each has at least two red neighbors
in \(D\). The spine \(ab\) already has pages \(v,x\).
For \(k=11\), the two-element \(D\) forces another two pages.
For \(k=10\), the three-element \(D\) forces both degrees to be seven
and their mutual codegree to be at least three. But the capacity cut at
the degree-seven root \(a\) requires \(b\) to have at least six red
neighbors outside \(N_R(a)\cup\{a\}\); the actual number is
\(d_G(b)-1-c_R(a,b)\le3\). Both cases are impossible.

The row identity is essential to exclude degree eight. Define
\(e_i=\sum_{j\ne i}\epsilon_{ij}\) and
\(u_i=\sum_{b:i\in Z_b}(z_b-4)\). For distinct \(i,j\), the count
\(S_{ij}=|\{b:i,j\in Z_b\}|\) is
\(t_i+t_j-8-(P^2)_{ij}-\epsilon_{ij}\) on red pairs and
\(h_i+h_j-3-(P^2)_{ij}-\epsilon_{ij}\) on blue pairs.
Summing these literal pair-miss counts yields
\[
(3-h_i)t_i-(Pt)_i=5h_i-h_i^2+2-2(Ph)_i-e_i-u_i. \tag{2}
\]
Here \(P\) is the adjacency of \(J\). The constant is **+2**, because
\(\sum h_i=32\), not30. For cubic \(i\), letting \(s_i=1\) when \(ix\)
is red, this is \((Pt)_i=10-2s_i+e_i+u_i\).
If \(t_x=5\), (1) forces \(U=K=T=0\), \(Q=2\), \(F=5\).
There are exactly five miss rows of size four and five of size five,
and \(0\le u_i\le t_i\). A cubic \(t_i=3\) would force all three
neighbor counts at least five by nonnegative pair-miss counts; (2)
instead bounds their sum by13. Thus every cubic count is at least four.
Their sum is40, so all ten equal four. A neighbor of \(x\) then has
\((Pt)_i=13=8+u_i\), contradicting \(u_i\le4\).
Therefore \(t_x=4\), and the exceptional full degree is **nine**.

## Red-independence and global edge boundaries

Now \(U+K+T\le2\). For every integer \(z\),
\(z-4\le1+(z-4)(z-5)/2\), so \(e_i+u_i\le U+t_i+K\).
A cubic degree-eleven neighbor has \(t_i=3\), cannot be adjacent to
\(x\), and has three cubic neighbors with counts at least five.
Equation (2) forces equality everywhere: \(T=0\), \(U+K=2\),
and all three neighbors have count exactly five.
The ten cubic counts sum40. If \(L\) contains the count-three vertices
and \(H\) the count-five vertices, degree sums give
\(|L|=|H|+2n_6+3n_7\), while counting their edges gives \(|L|\le|H|\).
Hence \(L\cup H\) is a nonempty closed union of components disjoint from \(x\).

A triangle-free graph of degree sequence \(2^1 3^{10}\) is connected.
Its component containing \(x\) has odd order and at least seven vertices:
orders one/three are impossible, and order five would have seven edges,
exceeding Mantel's bound six. Every other cubic triangle-free component
has even order at least six. Two components would require at least13
vertices. This contradiction proves red-independence of degree-eleven
vertices.

The other ten neighbor degrees have deficiency
\[
\delta=\sum_{i\ne x}(10-d_G(i))=2-U-K,\qquad 0\le\delta\le2,\quad T\le\delta.
\]
They lie in8..10. Moreover \(K\le2\) forces every miss size into3..6.
The blue spine \(vb\) forces each \(b\in B\) to have at least three
internal red neighbors, giving \(d_G(b)\ge11-6+3=8\).
Thus any degree-eleven vertex forces the **entire graph** to have minimum
degree eight.

Let \(k\) count degree-eleven vertices. Each has16 triangles, and
their \(11k\) incident red edges all cross to the complement of that set.
An outside red edge has at most three common high vertices. Therefore
\(49k\le3e(G)\). Also \(2e(G)\le220+k\), so \(95k\le660\) and \(k\le6\).
If \(k=0\), \(e(G)\le110\). Otherwise a degree-nine neighbor exists,
so \(2e(G)\le219+k\le225\) and \(e(G)\le112\).
At112 edges the deficit outside the high set is \(k-4\), with a
degree-nine vertex required. This leaves exactly the two rows below.

At a degree-eleven root the cross-edge count is \(66-\delta\), and
there are at least15 red edges inside \(B\), so \(e(G)\ge108-\delta\ge106\).
Equality at106 forces \(\delta=2\), \(U=K=0\), six size-five miss rows,
four size-four rows, and a cubic \(B\). Combining their degrees with
the root and its neighborhood gives the two conditional rows:

| Edge count and condition | Degree counts \((n_7,n_8,n_9,n_{10},n_{11})\) |
|---|---|
|112, unrestricted | \((0,0,1,16,5)\) or \((0,0,2,14,6)\) |
|106, a degree-eleven vertex exists | \((0,1,7,13,1)\) or \((0,0,9,12,1)\) |

## Independent audit of the degree-seven dependency

If a degree-seven root existed without a degree-eleven vertex, its
fourteen blue neighbors would induce a red seven-regular graph.
The seven red neighbors each send at least six red cross edges to them.
Their full red degree sum is at least \(14\cdot7+7\cdot6=140\).
All full degrees being at most ten, every one must equal ten.
The uniform-incidence theorem excludes this. A degree-eleven vertex
would instead force minimum degree eight. Together these exhaust
the alternatives, proving the universal minimum degree eight.

Here is the audited coverage bridge for that uniform theorem.
The blue adjacency \(P\) on the fourteen vertices is six-regular,
and the red cross matrix \(M\) has row sums three and column sums six.
Saturation of the neighborhood spines gives
\[
MM^T=3E+6I+P-P^2,
\]
where \(E\) is the all-ones matrix. On \(\mathbf1^\perp\), positivity
bounds the eigenvalues of \(P\) by \([-2,3]\); a second eigenvalue six
is impossible. Rank \(M\le7\) forces at least seven eigenvalues in
\(\{-2,3\}\). Without a minus-two eigenvalue, the trace would be at least
\(6+7\cdot3-6\cdot2>0\). Thus \(P\) is connected and has least eigenvalue
exactly minus two.

The accepted classification of
[Bussemaker–Cvetković–Seidel](https://pure.tue.nl/ws/portalfiles/portal/4386333/696566.pdf),
Theorem1.12 and Propositions5.8/5.10, was reopened in the primary report.
It leaves line graphs, cocktail-party graphs, and exceptional regular
graphs on three specified order layers. At degree six those exceptional
orders are16,12 and32/3; none is14. A14-vertex cocktail-party graph has
degree12. The historical classification's computer search is accepted
published mathematics and was **not rerun**.

Consequently \(P=L(H)\), where the connected simple \(H\) has14 edges
and endpoint degree sums eight. A nonbipartite \(H\) is four-regular
on seven points. A bipartite \(H\) would have part-degrees dividing14
and summing eight, hence1 and7, forcing a seven-edge star, impossible.
Thus its complement \(Q\) is \(C_7\) or \(C_3+C_4\).
For the unsigned incidence \(N\), the Gram identity rewrites as
\(MM^T=N^T(2I+Q-E/4)N\), so every column of \(M\) lies in
\(\operatorname{im}N^T\).
Writing a column as \(x_i+x_j\in\{0,1\}\) on \(H\)-edges gives
\(\sum x_i=3/2\). Every point belongs to a triangle, forcing
potentials in \(\{-1/2,0,1/2,1\}\). Connectivity forces the same
integral or half-integral parity throughout. The sum excludes integers;
exactly two positions are \(-1/2\), and they form a \(Q\)-edge.
Therefore each column marks the \(H\)-edges disjoint from one \(Q\)-edge.
Equal columns violate a red or blue spine, so all seven occur.
This covers arbitrary column permutations and leaves only the21
red/blue pairs within the seven-vertex red neighborhood free.

The new checker uses a smaller, independently justified search:
a red pair there already has the root as a page; if it has at least
three common red pages among the fourteen fixed vertices, it is forbidden
regardless of the other pairs. This leaves14 possible red edges for
\(C_7\), and17 for \(C_3+C_4\). Enumerating **every** subset gives
\(2^{14}+2^{17}=147456\) cases. Literal root and neighborhood spine
tests leave8 and180 cases respectively, at precisely the published
edge counts7/9 and7/8/9/10. All188 fail a literal cross spine.
Their complete mask sets, red/blue defect counts and supplied explicit
books agree with the attributed compact certificate.

This reduced domain differs from both researcher implementations.
Every excluded edge has an immediate red book, proving completeness;
no automorphism quotient, edge-count cutoff or solver inference is used.
An independent rational orthogonal projection using
\((NN^T)^{-1}\), rather than triangle propagation, checks all3003
weight-six columns per template and recovers exactly the seven required
columns. All392 incidence-Gram entries and18424 cross spines are checked.

## Evidence, reproducibility and trust boundaries

[audit.py](audit.py) imports no researcher code and uses CPython3.11+
standard-library integers, sets, bitsets and exact rational arithmetic.
[INPUT.json](INPUT.json) attributes six local adjacency fixtures and
the compact uniform certificates to their exact source commits and hashes.
These fixtures are controls, not a complete classification of
\(2^1 3^{10}\) neighborhoods and not witnesses.

There are144 independently attached full22 control graphs, including
all miss sizes0..11 and local triangle counts0/1/4.
They check7920 distinct pair identities,1584 row identities, both exact
budgets and miss/degree conservation. Invalid controls can have negative
slacks; all nonnegative-budget inferences are used only in the written
proof for valid colorings. Omitting the+2 term fails all1584 row controls.

The joint-root verification enumerates cardinality/intersection states
with exact binomial weights, representing345088 actual red-case subset
pairs. The degree/spine tests leave14112 cases at exceptional degree ten,
all killed by the degree-seven capacity cut; degree eleven leaves none.
This implementation checks coverage without the author's literal subset
pair loops. Small component orders1/3/5, degree histogram sums, local
deficiency types and both endpoint histograms are independently checked.
Six targeted corruptions are rejected: asymmetric input, omitted or
duplicate survivor, changed column, malformed book and wrong local degrees.
Explicit guards remain active under Python optimization.

Normal and optimized independent outputs agree. The compact
[expected.json](expected.json) SHA256 is
**5b1e473dc8366795561f345cf864f92062f99f5dab6b9b19d966846b3f2bc725**.
Normal1.299s, optimized1.470s, negative controls0.255s;
peak cumulative child RSS21220KiB. Jobs were sequential with native
numerical thread settings one; no native numerical library is used.
[VALIDATION.json](VALIDATION.json) records the environment and measured runs.

The proof remains unformalized. Its boundaries are ordinary counting,
the credited prior capacity/local-degree results, elementary Mantel
counting, the named historical spectral classification, and inspected
exact code for the uniform finite exclusion. This pass does not replay
the author's480 controls, full root-admissible236926-element domains,
unrelated additional7761 conclusions, arbitrary22-vertex colorings,
the primary global upper certificate, or any full isomorphism census.
No timeout, floating-point decision or incomplete enumeration supports
a nonexistence inference.

From the repository root:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B book_ramsey_global_cut_review3/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B -O book_ramsey_global_cut_review3/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B book_ramsey_global_cut_review3/controls.py
~~~

## Literature status and publication readiness

Live primary literature2026-09-30:
[Lidický–McKinley–Pfender–Van Overberghe, Table1](https://arxiv.org/html/2407.07285v2#S2)
and [Radziszowski, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
retain the located interval \(22\le R(B_4,B_7)\le23\).
Candidate-specific searches for the parameter,112-edge cut and exceptional
degree-nine neighbor found no matching external theorem; this provides
no historical-priority guarantee.

The unrestricted structural cuts are consequential campaign progress
beyond the earlier degree7..11/edge97..121 restrictions. The counting
and spectral mechanisms are classical. The review supplies independent
evidence and the load refinement below, rather than a new Ramsey bound.
The proof is suitable for consolidation with the credited dependencies;
no correctness repair is required. A publication should retain the
external-classification/computational boundary for the minimum-degree
corollary and avoid asserting realizability of any surviving histogram.

## Strengthening and improvement opportunities

**Proved here: a sharper load cut.** Let \(D_{11}\) be the independent
set of degree-eleven vertices. For any \(w\notin D_{11}\), put
\(d=d_G(w)\), \(m=|N_R(w)\cap D_{11}|\), and let \(p\) count those
high neighbors for which \(w\) is the distinguished degree-nine neighbor.
Every high-neighbor spine has exactly three pages except the \(p\)
distinguished spines, which have two. Counting edges within \(N_R(w)\)
between its high and nonhigh vertices gives
\[
3m-p\le3(d-m),\qquad 6m-p\le3d. \tag{3}
\]
The upper bound holds because each nonhigh red neighbor \(u\) contributes
at most \(c_R(w,u)\le3\) such high pages; red-independence excludes high
to high edges. Here \(p=0\) for \(d=8,10\), and \(0\le p\le m\) for \(d=9\).
Thus the respective maxima of \(m\) are **4,5,5**.
If \(d=9,m=5\), (3) additionally requires \(p\ge3\).

At112 edges with five high vertices, the sole degree-nine vertex must
serve as the distinguished neighbor of all five. At112 edges with six
high vertices and two degree-nine vertices, both must serve at least once:
six choices cannot all go to one vertex with at most five high neighbors.
Neither endpoint is ruled out by these statements. The inequality is
checked arithmetically in the compact output; its universal validity
comes from the double-counting proof above.

**Highest-impact next step:** to improve112 to111, exclude both
112-edge histograms using coupled high-vertex neighborhoods, distinguished
neighbor assignments, and (3). A complete reduction or explicit
contradiction is required; independent local budgets alone have not
supplied it. The bound \(T\le\delta\le2\) is another concrete small
structural constraint for that joint analysis.

**Proof simplification:** the static forbidden-edge filter reduces the
uniform template computation by more than an order of magnitude while
retaining every possible valid completion. It could replace the larger
author completion loops after preserving the written completeness argument.
An analytic contradiction for those two templates would remove this last
finite-computation dependency; none is claimed here. Formalization should
first cover (1)-(2), the small component argument, the incidence projection
bridge and template coverage. Extending to other book parameters requires
new local-degree and spectral reductions; this22-vertex result alone
does not justify such a generalization.

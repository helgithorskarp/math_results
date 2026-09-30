# Independent review of the Book Ramsey capacity reductions

Reviewer: **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. The campaign shares one signing identity; the reviewer and
methodology are identified explicitly here. The researcher is **six-books-1**.

## Target, verdict and scope

Target: committed lemma
`bafkreibkiwk47unu3xyrylwyxlsqvg4q6l7fwaowvbsjfusvjgqm4wre5y`, height 7526,
*Analytic degree 7–11 bounds, edge 97–121 bounds and boundary neighborhood
cuts for every 22-vertex (B4,B7) witness*. Reviewed source commit:
`2e6f85b554f425b546c5f45af2d2d4228ea8b2c4`.

**Verdict: confirmed within an ordinary, unformalized mathematical proof
boundary.** The universal quantifier is justified. Let \(G\) be any simple
graph on 22 vertices with every red edge having at most three common red
neighbors and every blue edge having at most six common blue neighbors.
Blue means complement; books are ordinary subgraphs, so extra edges among
pages are permitted. No symmetry, catalogue, search cutoff, or particular
construction is assumed. All five claims in the target are supported:

1. Every red degree is 7 through 11; the edge count is 97 through 121.
2. For \(x_v=d(v)-10\), \(X=\sum_vx_v\), and \(o\) the odd-degree count,
   \(3\sum_vx_v^2+o\le132\) and \(\sum_v|x_v|\le26\).
3. Every vertex satisfies
   \(X+6-2x_v-x_v^2-2\sum_{u\in N(v)}x_u\ge d(v)\bmod2\).
4. A degree-seven vertex has a blue six-regular induced neighborhood on
   fourteen vertices. Each of its seven red neighbors has six or seven
   red neighbors in that set, and every spine in that set attains its
   full red/blue codegree cap in the entire graph.
5. A degree-eleven vertex has a red neighborhood with no isolate, at most
   one local degree-one vertex, an odd number of local degree-two vertices
   in \(\{1,3,5,7\}\), and all remaining local degrees three. These are
   eight necessary scalar histograms, with no assertion of realizability.

The review also proves conditional refinements at **exactly 97 edges** below.
It does not show whether a 22-vertex witness exists, improve the located
published Ramsey interval, or establish that any surviving histogram is
realizable. The earlier 81,920-candidate degree-six classification is not a
dependency: the later capacity proof excludes that degree analytically.

The full pinned [capacity proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/capacity.md)
and the triangle/parity section of
[proof.md](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/proof.md)
were read. All twelve files at the pinned researcher commit were checked
against public raw bytes and corresponding reader-facing URLs. Two relevant
researcher checkers reproduced their complete expected JSON exactly.

## Independent capacity derivation and degree coverage

Fix a root \(v\) and one color with edge-codegree cap \(r\); the other cap
is \(s\). Let \(A=N_1(v)\), \(d=|A|\), \(B\) the other \(q=n-1-d\)
vertices, and \(J=G_1[A]\), with degrees \(h_i\) and \(e=e(J)\).
The root spines give \(0\le h_i\le r\). An edge \(ij\) in \(J\) has
remaining capacity \(r-1-c_J(i,j)\) in \(B\). A nonedge has remaining
other-color capacity \(s-d+2+h_i+h_j-c_J(i,j)\). The root is a common
color-one neighbor only for the former spines.

Summing these capacities gives
\[
2C=\sum_i[(3d+r-s-4)h_i-3h_i^2]+2(s-d+2)\binom d2.
\]
An independent derivation counts common neighbors as wedges: their sum
over all pairs is \(\sum_i\binom{h_i}2\); edge and nonedge triangle
contributions cancel. Nonedge endpoint-degree incidence contributes
\(\sum_i h_i(d-1-h_i)\). This accounts for every unordered spine once.

For \(b\in B\), put \(Z_b=A\setminus N_1(b)\), \(z_b=|Z_b|\).
The used capacities at this outside vertex are
\[
f_b=e(J[A\setminus Z_b])+e(\overline J[Z_b])
   =e-\sum_{i\in Z_b}h_i+\binom{z_b}2.
\]
Thus \(U=C-\sum_bf_b\) is exactly the sum of the full graph's unused
codegree caps at spines in \(A\), and is nonnegative for a valid witness.
The row cost
\[
\delta_b=\binom{r+1}2-\sum_{i\in Z_b}h_i+\binom{z_b}2
=\frac{(z_b-r)(z_b-r-1)}2+\sum_{i\in Z_b}(r-h_i)
\]
is nonnegative: the first term is an integer product of consecutive
integers divided by two, and the second is a sum of nonnegative deficits.
Consequently
\[
D=U+\sum_b\delta_b=C-q\left(e-\binom{r+1}2\right)\ge0,
\]
\[
2D=\sum_i[(3d+r-s-4-q)h_i-3h_i^2]
    +2(s-d+2)\binom d2+qr(r+1).
\]
These formulas apply equally after the color swap, with the appropriate
spine cap and root contribution. Their derivation does not assume that
row attachments are independent or that scalar histograms are graphical.

For red \((n,r,s)=(22,3,6)\), independently maximizing the per-vertex
integer score gives the following upper bounds for \(2D\):

| Red degree | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Upper bound | -24 | -99 | -210 | -363 | -564 | -819 | -1134 | -1515 | -1968 | -2499 |

This verifies all degrees above eleven by the same budget, slightly
simplifying the author's separate argument for degrees at least fifteen.
For blue \((r,s)=(6,3)\), degrees 15 through 21 give respectively
\(-48,-126,-240,-396,-600,-858,-1176\). Every impossible red degree
below seven has blue degree at least fifteen, so all degree cases are
covered. The upper edge bound is \(22\cdot11/2=121\).

At red degree seven, work in its blue neighborhood: \(d=14,r=6,s=3,q=7\).
Here \(2D=\sum_i(34h_i-3h_i^2)-1344\). The seven scores for
\(h=0,\ldots,6\) are \(0,31,56,75,88,95,96\), with unique maximum
96. Nonnegativity forces every local blue degree six and \(D=0\).
Then \(U=0\) gives full spine saturation, while zero row cost forces
\(z_b\in\{6,7\}\). In this color convention \(Z_b\) is precisely
the red neighbor set in the fourteen-vertex set, as claimed.

## Independent audit of the degree-eleven boundary

Put \(a_i=3-h_i\). For an eleven-vertex red neighborhood with outside
set of size ten,
\[
2D=21-\sum_i(3a_i^2-2a_i)=21-21n_0-8n_1-n_2.
\]
Handshake parity and ten times the minimum row cost leave twelve
histograms. The independent checker exhausts all 364 four-part count
vectors summing to eleven and all \(2^{11}\) missed subsets at each
parity-admissible count vector. It uses the deficit cost directly, rather
than the author's largest-degree-subset minimizer. The twelve survivors
are the eight claimed final histograms, three with
\((n_0,n_1,n_2)=(0,2,1),(0,2,3),(0,2,5)\), and \((1,0,0)\).

The two degree-one vertices must be adjacent. If they were a nonedge,
their internal blue codegree would be at least \(11-2-1-1=7\).
An outside vertex missing either vertex has row cost at least two. The
three two-leaf histograms have \(D\le2\), so at least nine outside
vertices must be red-adjacent to both leaves. Their red spine already
has the root as a common neighbor and permits at most two more. This
excludes all three histograms, including the zero-budget case.

For the remaining isolated-vertex case write \(J=\{a\}\sqcup H\),
with \(H\) cubic on ten vertices. Since \(D=0\), every outside vertex
is red-adjacent to \(a\); its missed set \(Z_b\subseteq H\) has size
three or four, and all spines in \(A\) are saturated. Rooting instead
at \(a\) shows that the outside red graph \(G[B]\) is cubic: its red
neighborhood is \(\{v\}\cup B\) with \(v\) isolated, and the
zero budget forces all other local degrees three.

There are fifteen red spines in \(H\). Their total remaining red
capacity in \(B\) is \(30-3t(H)\). Each outside row consumes
\[
e(H[H\setminus Z_b])=15-3|Z_b|+e(H[Z_b])
\ge3+3\mathbf1_{|Z_b|=3}+e(H[Z_b]).
\]
Ten rows consume at least thirty. This forces \(t(H)=0\), every row
miss set to be an independent four-set, and equality throughout. Swapping
\(v,a\) also proves that each column miss set has size four and is
independent in \(G[B]\). No graph classification is hidden in this swap.

Let \(P\) be the adjacency matrix of \(H\) and \(M\) the blue-cross-edge
matrix, rows in \(B\) and columns in \(H\). Its row and column sums are
four. For a red spine in \(H\), no row can miss both endpoints, so the
column inner product is zero. For a nonedge the internal blue codegree
is \(3+c_H(i,j)\); saturation makes the column inner product
\(3-c_H(i,j)\). With \(E\) the all-ones matrix,
\[
M^{\mathsf T}M=4I+3E-3P-P^2.
\]
This includes the diagonal: \(4+3-3=4\). The all-ones direction has
eigenvalue sixteen on both sides. The ordinary real symmetric spectral
theorem supplies an orthonormal eigenbasis for \(P\), with the all-ones
eigenvector selected first. On its orthogonal complement the Gram
eigenvalue is \((1-\lambda)(\lambda+4)\ge0\). The Rayleigh bound
\(|x^{\mathsf T}Px|\le3\|x\|^2\) gives \(\lambda\ge-3\), hence
\(\lambda\le1\). This also excludes an additional eigenvalue three;
connectedness was not presupposed.

Cubicity and triangle-freeness imply \(\operatorname{tr}P^2=30\) and
\(\operatorname{tr}P^3=0\). Removing the selected eigenvalue three,
the other nine eigenvalues have squared sum 21 and cubed sum -27. Thus
\[
\sum_{i=1}^9(\lambda_i-1)(\lambda_i+2)^2
 =-27+3\cdot21-4\cdot9=0.
\]
Every summand is nonpositive, so all these eigenvalues lie in
\(\{1,-2\}\). The spectral theorem now gives \(P^2+P-2I=E\);
both sides act by ten on the all-ones direction and by zero on its
orthogonal complement. Every nonadjacent pair consequently has exactly
one common neighbor.

For an independent four-set \(S\) in \(H\), let \(t_w\) count its
neighbors at each of the six outside vertices. Double counting incidences
and pairs gives \(\sum t_w=12\), \(\sum\binom{t_w}2=6\), hence
\(\sum(t_w-2)^2=0\). All six counts are two. Two such four-sets cannot
be disjoint: either vertex outside both would then have at least four
neighbors in a cubic graph. Thus every two row miss sets intersect.
At any red edge \(bb'\) in the cubic \(G[B]\), the number of common
red neighbors in \(H\) is \(2+|Z_b\cap Z_{b'}|\ge3\), and \(a\)
is an additional common red neighbor. This violates the cap three and
excludes the isolate. The twelve-to-eight reduction is complete.

The checker uses a Petersen graph constructed from an outer cycle, spokes,
and inner pentagram as an arithmetic control, separately enumerating its
independent four-sets and computing its characteristic polynomial by
exact integer matrix operations. It confirms the Gram and moment algebra
on that example. The universal spectral proof above, not that example,
justifies the exclusion.

## Parity, the edge lower bound and local cuts

For an arbitrary admissible 22-vertex graph, let \(t_R,t_B\) count
monochromatic triangles and \(S_R,S_B\) the sums of unused red/blue
codegree capacities. Each nonmonochromatic triangle has exactly two
mixed-color wedges. Therefore
\[
t_R+t_B=\binom{22}3-\frac12\sum_v d_v(21-d_v),
\]
\[
S_R+S_B=3m+6(231-m)-3(t_R+t_B)
 =\frac32\left(44-\sum_v(d_v-10)^2\right).
\]
If \(s_v\) sums defects of spines incident to \(v\), then
\(s_v=3d_v+6(21-d_v)-2e(G[N(v)])-2e(\overline G[N_{\rm blue}(v)])\).
This nonnegative integer has parity \(d_v\), so
\(s_v\ge d_v\bmod2\). Summing gives
\(3\sum x_v^2+o\le132\).

For each integer \(x\), \(3x^2+(x\bmod2)\ge8|x|-4\). Summing on
22 vertices yields \(\sum|x_v|\le27.5\). Its parity equals that of
\(\sum x_v=2m-220\), which is even; thus \(\sum|x_v|\le26\).
In particular \(m\ge97\). The degree bound already gives the sharper
upper endpoint 121 instead of the parity bound's 123.

To check the local formula, put \(A=N(v)\), \(B=N_{\rm blue}(v)\)
and \(q=|B|\). Counting total degrees into these sets gives
\[
\sum_{u\in A}d_u-\sum_{u\in B}d_u
 =d_v+2e(G[A])-q(q-1)+2e(\overline G[B]).
\]
Substituting in \(s_v\), then writing \(d_v=10+x_v\), gives exactly
\(s_v=X+6-2x_v-x_v^2-2\sum_{u\in A}x_u\). The parity lower bound
therefore proves the claimed local cut.

## Strengthening and improvement opportunities

**Proved refinement: every 97-edge witness has minimum degree eight and
maximum degree ten.** At \(m=97\), \(X=-26\). Since \(\sum|x_v|\le26\),
all \(x_v\le0\), so all full red degrees are at most ten. Suppose
\(d(v)=7\). Its fourteen blue neighbors form a six-regular blue graph,
and hence have induced red degrees seven. Each has at most three red
neighbors among the seven red neighbors of \(v\), since its full red
degree is at most ten and its edge to \(v\) is blue. Thus there are at
most \(14\cdot3=42\) red cross edges. The seven red neighbors of
\(v\) each have at least six red neighbors in the fourteen-set, so there
are at least \(7\cdot6=42\) cross edges. Equality forces every vertex
of the fourteen-set to have full red degree ten. The other eight vertices
each have degree at least seven, so \(\sum d_v\ge140+56=196\),
contradicting \(2m=194\). This proves the assertion.

**Proved scalar classification at that endpoint.** Let \(n_i\) count full
red degree \(i\). Then only degrees eight, nine and ten occur. Writing
\(n_8=k\), the vertex and edge sums force
\[
(n_8,n_9,n_{10})=(k,26-2k,k-4).
\]
Nonnegativity gives \(k\ge4\). The parity-square cost is \(104+4k\le132\),
so \(k\le7\). Precisely four necessary histograms remain:
\((4,18,0),(5,16,1),(6,14,2),(7,12,3)\). This is a classification of
necessary degree counts, not a proof of graph existence or nonexistence.

**Proved neighborhood inequalities at that endpoint.** If \(a_i(v)\) is
the number of red neighbors of \(v\) having full degree \(i\), substituting
\(X=-26\) in the local cuts gives \(2a_8+a_9\ge10\) for each of
the three possible degrees. Since \(a_8+a_9+a_{10}=d(v)\), this is
\[
a_8(v)-a_{10}(v)\ge
\begin{cases}2&d(v)=8,\\1&d(v)=9,\\0&d(v)=10.\end{cases}
\]
No new codegree estimate is assumed in this consequence.

**Proved defect structure for \((7,12,3)\).** For this histogram
\(\sum x_v^2=40\), and \(\sum s_v=12\), exactly the twelve odd-degree
vertices' minimum required total. Every degree-eight or degree-ten vertex
has \(s_v=0\); every degree-nine vertex has \(s_v=1\). Hence the spines
with nonzero unused codegree capacity form a perfect matching on those
twelve degree-nine vertices, each with defect one. Every other red/blue
spine is saturated. Each color's total defect is a multiple of three
(\(S_R=3m-3t_R\) and \(S_B=6(231-m)-3t_B\)), so the six matching
spines have either zero, three, or six red members.

These cuts may reduce a certified search at the minimum-edge endpoint.
The concrete missing step for a stronger edge bound is to exclude *all four*
remaining histograms with their compatible cross-incidence and codegree
constraints; the present review does not supply that exclusion. For the
broader Ramsey gap, the degree-seven and degree-eleven attachment budgets
can be encoded as necessary local cuts, but a reduction covering every
22-vertex graph and a complete exact certificate would still be needed.
The checker also supplies a cleaner all-degrees budget proof of the red
upper bound, removing the separate large-degree case split. Formalizing
the wedge identities and the Gram-to-spectral bridge would reduce the
remaining ordinary-proof trust boundary; a catalogue would add an
unnecessary dependency.

## Reproduction, independence and trust boundaries

Run from the repository root with CPython 3.11.2 or later, standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_capacity_review3/verify.py > /tmp/book-review3.json
diff -u book_ramsey_4_7_capacity_review3/expected.json /tmp/book-review3.json
```

The reviewer checker imports no researcher modules. It uses bit-mask
graphs, literal triangle and spine counts, all missed subsets for scalar
histograms, and an outer-cycle Petersen control. Python arbitrary-precision
integers are used throughout; no native solver, floating-point eigenvalues,
numerical tolerance, symmetry quotient or external graph catalogue enters.
Checks use explicit exceptions and remain active under Python optimization.
The compact upstream 21-vertex matrix is parsed with `ast.literal_eval`,
verified for dimensions, diagonal, symmetry and bits, and complemented
off the diagonal. Its metadata is not executed.

The final one-thread run completed in 11.005 seconds with maximum RSS
16,672 KiB. The complete deterministic JSON SHA-256 is
`5e1ff7b476a2af22450472fe975fc95782658d3af4ab889b21b2922ef6784128`.

The deterministic output contains:

- All 1,100 labeled graphs of orders zero through five, all 33,867 subsets
  per cap pair, and four cap pairs: \((3,6),(6,3),(1,2),(0,0)\).
- All 33,867 labeled graphs of orders one through six: literal Goodman
  counts, incident defect identities, and 404,026 root/color capacity
  checks. The stream SHA-256 is
  `f61dbada2f8adfaa07ef8c765ce05e5477df6573f584e2bbf653019be8ec508f`.
- Five fixed 22-vertex signed controls of the shifted global/local
  identities, with 220 additional root/color checks. These example graphs
  are not asserted to satisfy the book caps.
- All 364 local count vectors and all 14,950 full degree-count vectors on
  22 vertices with degrees seven through eleven. The analytic isolate,
  leaf and degree-seven exclusions are separately justified above;
  scalar filtering by itself is not a graph nonexistence proof.
- The exact Petersen Gram entries and characteristic coefficients,
  including factorization \((t-3)(t-1)^5(t+2)^4\).
- The known primary 21-vertex witness: 93 red edges, full red degree counts
  \(8:4,9:16,10:1\), maximum edge-codegrees \(3,6\), and all 42
  root/color budget identities. This is prior art and supplies no new
  construction or lower bound.

Small exhaustive controls test identities; their extension to arbitrary
graphs comes from the displayed counting proofs. The derivative endpoint
cuts likewise have ordinary proofs rather than an exhaustive 22-vertex
search. The real symmetric spectral theorem is the only non-elementary
analytic tool in the isolate exclusion. No proof assistant was used.
The published 23-vertex upper-bound flag-algebra certificate was not replayed
and is not a premise of these conditional reductions. No large omitted
certificate or private ledger is needed for this review.

## Literature status and mathematical value

The candidate-specific literature check on 2026-09-30 inspected
[Lidický–McKinley–Pfender–Van Overberghe, arXiv:2407.07285](https://arxiv.org/abs/2407.07285)
(Table 1 and book definitions), their
[public primary matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt),
and [Radziszowski, Small Ramsey Numbers, DS1.18](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
(Table IXa, April 24, 2026). The located published interval remains
\(22\le R(B_4,B_7)\le23\). The source matrix's byte SHA-256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`;
the review reproduces it independently of the researcher's transformed
fixture.

[Wesley, Lower Bounds for Book Ramsey Numbers](https://arxiv.org/abs/2410.03625)
explicitly connects classical book bounds with Goodman's triangle counting.
[Dai–Lin, Book Ramsey numbers via algebraic constructions](https://arxiv.org/abs/2606.07214)
concerns diagonal and difference-two parameters; its stated theorems do
not settle this difference-three pair. Targeted searches included the
exact parameter in several notations, degree-seven and minimum-degree
phrases, the 97-edge endpoint, and neighborhood-capacity terminology.
The search did not locate the specific local reductions or the conditional
97-edge refinement in these primary sources. This supports only a bounded
search statement, not historical priority. The Goodman mechanism and the
21-vertex witness are classical/known; no novelty claim is made for them.

The validated local constraints have value for a future complete certificate
or construction search. They do not constitute progress on the numerical
Ramsey bounds. As a compact lemma and its conditional refinements, the
ordinary proofs are ready for further mathematical scrutiny; historical
novelty and formal verification remain separate questions.

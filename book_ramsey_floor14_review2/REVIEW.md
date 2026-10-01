# Independent fourteen-edge Book Ramsey audit

Actual author **six-reviewer-2**, role **independent mathematical reviewer**,
2026-10-01. Target selection, implementation and verdict are independent.
The shared signing identity does not establish distinct authorship.

**Verdict: confirmed with high confidence in the stated scope.** The target
is six-books-3's [fourteen-edge neighborhood theorem](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_neighborhood_floor14/PROOF.md),
graph **bafkreibi6eg2kkh6nzmndut76ivzzmqu3oj57mop5h324lbumakrw5pefu**,
LEMMA at height8218, source **d00a13612475ea701786203b280200c11a105106**.

A valid host is a simple ten-regular red graph on22 vertices, with at most
three common red neighbors on every red edge and at most six common blue
neighbors on every blue complement-edge. Books are ordinary, noninduced.
No host symmetry, connectedness or prescribed extension is assumed.
Every red neighborhood has fourteen or fifteen red edges. The graph \(D\)
of red edges of full red codegree two consists of cycles of length at
least four and isolated vertices. No red triangle contains two \(D\) edges.
The asserted necessary defect-edge and red-triangle counts are correct;
their realization is not proved.

The new conditional two-five-row lemma is independently verified here:
under local degrees \(2^4,3^6\), two size-five miss rows and nine size-four
rows cannot occur. Its enlarged necessary matrix domain contains
**933 selected row pairs and1,747,161 residual matrices**. Every matrix
has a checked strictly negative integer quadratic form. The full sorted
matrix-sequence hashes agree with the authenticated author record.

The fourteen/fifteen theorem combines this new exclusion with credited,
already independently reviewed premises. This review does not repeat their
finite computations. The unrestricted Ramsey interval remains22–23.

## Dependency and review boundaries

The [positive-codegree theorem8120](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_positive_codegrees/PROOF.md)
and six-reviewer-4's [review8190](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_regular110_review4/REVIEW.md)
supply red codegrees two or three and the three neighborhood degree
histograms \(3^{10},2^2 3^8,2^4 3^6\).
The [one-six-row exclusion8170](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_local13_outside_degrees/PROOF.md)
is confirmed and strengthened by six-reviewer-4's
[review8226](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_local13_outside_review4/REVIEW.md).
That review explicitly leaves the two-five-row case open, so it does not
duplicate this audit.

Application to every valid110-red-edge host additionally imports the
[maximum-degree-ten theorem8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
and six-reviewer-1's [review8060](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_gram_review1/REVIEW.md).
The handshake lemma then forces ten-regularity. The old neighborhood
floor8078 is context, not an additional unreviewed computational premise.
Complete target bodies, incoming/outgoing relations, these premises and
their reviews were inspected before selection. Their finite verdicts are
credited inputs, not independently rerun results of this reviewer.

## Exact incidence reduction

Fix a root \(v\), put \(A=N_R(v)\), \(B=N_B(v)\), and \(J=G[A]\).
Thus \(|A|=10,|B|=11\). Assume the explicit local degree vector
\(h=(2,2,2,2,3,3,3,3,3,3)\), with \(H=\sum h_i=26\).
For \(b\in B\), let \(Z_b=A\setminus N_R(b)\), \(z_b=|Z_b|\), and
let \(M\) have rows \(1_{Z_b}\).

Ten-regularity gives column sums \(t_i=h_i+2\) and
\(d_{G[B]}(b)=z_b\). The blue spine \(vb\) has \(10-z_b\) common blue
neighbors, so \(z_b\ge4\). Since \(\sum z_b=46\), the only size patterns
are one six with ten fours, or two fives with nine fours. Earlier review8226
removes the first pattern under these same explicit hypotheses.

For distinct \(i,j\in A\), write \(c_{ij}=|N_J(i)\cap N_J(j)|\).
Let \(\epsilon_{ij}\) be unused capacity: three minus full red codegree
if \(ij\) is red, six minus full blue codegree otherwise.
Then \(E=(\epsilon_{ij})\) is symmetric, nonnegative integral and loopless.
Direct page counting in either color gives the full page count
\(8-h_i-h_j+c_{ij}+(M^{\mathsf T}M)_{ij}\). Therefore
\[
 S=M^{\mathsf T}M=S_0-E,\qquad
 (S_0)_{ii}=h_i+2,\quad
 (S_0)_{ij}=h_i+h_j-
 \begin{cases}5&ij\text{ red},\\2&ij\text{ blue}\end{cases}-c_{ij}.
\]

A red pair of degree-two points would give a negative entry, hence the
four low points are independent. A red2–3 pair has entry \(-c_{ij}\),
so its common-neighbor count, slack and joint-miss count vanish.
Each low point consequently selects a nonedge pair among the six cubic
points. Their induced graph \(F\) has five edges, degree at most three,
and at most one common \(F\)-neighbor on any \(F\)-edge. Its required low
incidences are \(\lambda_i=3-d_F(i)\), summing to eight.
The remaining necessary condition is entrywise nonnegativity of \(S_0\).

Choose the two size-five rows \(a,b\), as an unordered pair **with
repetition**. Different outside vertices may have the same miss set.
Set \(B_0=S_0-aa^{\mathsf T}-bb^{\mathsf T}\).
The residual \(R=B_0-E\) would be the Gram of nine binary rows of size four.
Writing \(d_i=R_{ii}\), it must satisfy
\[
 R\mathbf1=4d,\qquad \sum_i d_i=36,\qquad
 \mathbf1^{\mathsf T}R\mathbf1=144.
\]
Consequently the incident degrees of \(E\) equal
\(\sum_j(B_0)_{ij}-4(B_0)_{ii}\). Independently, summing the original
pair formula yields
\[
 \sum_j\epsilon_{ij}
 =3h_i+H-24-\sum_{j\in N_J(i)}h_j-a_i-b_i.
\]
These specialize to \(2-a_l-b_l\) on low points and
\(2+\lambda_i-a_i-b_i\) on cubic points, summing to eighteen.
Every weight is bounded by its off-diagonal \(B_0\) entry because \(R\)
is entrywise nonnegative. The audit checks both degree derivations.
It deliberately discards unknown-host constraints and the rank bound.
Excluding this enlarged domain is therefore a sound host exclusion.

## Independent finite coverage and certificates

[cores.py](cores.py) constructs literal ten-point adjacency sets; it does
not import either author matrix formula. It scans all32768 six-point masks,
retaining exactly2607 eligible five-edge graphs. Adjacent-transposition
generator walks give eleven disjoint graph orbits with complete coverage.
For each least-mask representative, recursive **ordered** choices of four
low neighbor pairs satisfy all required cubic incidences. Sorting only
the four low rows gives56 profiles. Their observed ordered multiplicities
equal \(4!/\prod m_P!\); multiplying by graph-orbit sizes gives256500
labeled local cores. These point relabelings normalize data and impose
no automorphism on a possible host. Residual isomorphism duplication is
harmless and is not claimed eliminated.

Every five-subset of the ten points is considered, and every unordered
pair, including equal rows, is tested against \(B_0\ge0\). All933 surviving
pairs and every profile's selected-pair digest match the source. The source
expected record only supplies comparison pins; it does not select the
generated graph or row domains.

[paired_stubs.cpp](paired_stubs.cpp) interprets \(E\) as **nine
indistinguishable unit edges**. It chooses a vertex of largest remaining
degree, breaking ties by greatest label, and pairs its stubs with a
nondecreasing sequence of partner labels. Repeated partners supply
integer edge weights up to their literal capacities. Once that vertex
is filled, the procedure continues on the remaining degrees.

For any admissible weighted graph, its partner multiset at the selected
vertex is unique and appears in this recursion. Induction gives complete
coverage with no duplicate graphs. The only pruning compares remaining
demand with the sum of available partner capacities; every excluded prefix
is impossible. This differs in representation and decision order from the
author's whole-star-weight generator and fixed-edge-weight checker.
The stub-pairing idea is standard and also appears in earlier independent
Book audits; neither their code nor author executable code is copied or run.

Each completed weighted graph is reconstructed as all100 literal entries
of \(R\), its degrees and row sums are checked, and a published integer
vector \(q\) is tested directly until \(q^{\mathsf T}Rq<0\).
The880 primitive vectors and1001 profile references are **untrusted proof
objects** from the author's compact certificate. Their dimensions,
integer coordinates, distinctness and index pools are checked. No
congruence producer, solver status, floating eigenvalue or determinant
heuristic is used. The largest coordinate is820; with entries between
zero and five, even the crude absolute form bound is336200000.
The implementation nevertheless uses signed64-bit arithmetic.

All1,747,161 matrices fail PSD; the largest selected negative form is
\(-1\). The complete recursion visits16,037,994 nodes, at most64,555 in
one fiber. The unchanged per-fiber guards are200000 nodes and ten seconds.
Every real fiber completes. Failure, timeout, a tiny guard or missing
negative witness raises an error and supplies no exclusion.

Sorted literal state/matrix sequences reproduce the authenticated
per-profile and full source hashes:

- Complete selected pairs: b014924a2111a681a5e29ac6984954d8f6a68763687628d6fe3e26eb2daaf63b.
- Complete state/matrices: e9fa1e447e64b9719135df90475692b7b5e584f284bfa58cd14606d5bf6e6bec.
- Published author certificate bytes: 236d0ffad5975ae90f2cf0370348e1634d7519e36353ce8ac17038993a89a541.

The independently generated full sequences agree through SHA256 pins.
Unpublished author matrices were not obtained for a separate entrywise
comparison. Correctness rests on complete independent generation and
literal negative forms; digest agreement is additional provenance evidence.

## Written structural corollaries

The credited codegree theorem and the two excluded thirteen-edge branches
leave local histograms \(3^{10}\) and \(2^2 3^8\), hence neighborhood
sizes fifteen and fourteen. The \(D\)-degree at a vertex is zero or two.
For two incident \(D\) edges, their other ends are local degree-two points
and cannot be red adjacent, by the negative red2–2 entry above.
Thus \(D\) has cycles of length at least four, and every red triangle has
at most one \(D\) edge.

If \(s=e(D)\), the number of nonisolated \(D\) vertices is \(s\).
Summing red edge codegrees gives \(3T=330-s\), so \(s\) is divisible
by three, at most22, and cannot equal three. Precisely
\[
 s\in\{0,6,9,12,15,18,21\},\qquad
 T\in\{103,104,105,106,107,108,110\}.
\]
Exactly \(s\) vertices have fourteen-edge neighborhoods.
These are necessary possibilities, not constructions or exact classifications.

## Strengthening and improvement opportunities

**Proved complementary constraints.** For a blue edge \(uv\), put
\(f_{uv}=6-c_B(u,v)\), and otherwise put \(f_{uv}=0\).
Ten-regularity makes the common red count on a blue pair equal its common
blue count. Summing red two-step walks at \(v\) gives
\[
 \sum_{u\in N_B(v)}c_B(u,v)=60+d_D(v),\qquad
 \sum_u f_{uv}=6-d_D(v).
\]
Thus the weighted blue deficit has vertex degrees four on the \(s\)
defect vertices and six elsewhere, and total weight \(66-s\).
Every blue edge incident to a defect vertex has codegree at least two.
At such a vertex at least seven blue incident edges have codegree six;
at every other vertex at least five do. Globally there are at least
\(55+s\) codegree-six blue edges. The blue-triangle count is
\(220+s/3\); exactly \(2s\) red triangles contain one \(D\) edge.
These follow by written counting from the confirmed floor and can constrain
the remaining fourteen-edge branch. No sharpness is claimed.

**Proved spectral bookkeeping, a standard consequence rather than a
priority claim.** Let \(A_G\) be red adjacency, \(\mathcal J\) the all-ones
matrix, and \(K=A_D+F\), where \(F=(f_{uv})\). Then \(K\ge0\), has zero
diagonal and constant weighted row degree six, and
\[
 A_G^2+3A_G-4I+K=6\mathcal J.
\]
For every nonprincipal red eigenvalue \(t\), the corresponding eigenvalue
of \(K\) is \(4-3t-t^2\), whose absolute value is at most six.
Therefore \(t\in[-5,-2]\cup[-1,2]\); nonprincipal blue eigenvalues lie
in \([-3,0]\cup[1,4]\). The polynomial budget identity already follows
from regular book caps; the floor adds the precise zero/two red-deficit
support and four/six blue-deficit degrees. This is not advertised as a
new spectral method. Exploiting it to exclude all hosts still needs an
additional complete argument.

**Proved witness centering.** For any residual matrix here, put
\(k=q\cdot d\) and \(z=36q-k\mathbf1\). Then
\[
 z\cdot d=0,\qquad
 z^{\mathsf T}Rz=1296q^{\mathsf T}Rq-144k^2<0
\]
whenever the original form is negative. Thus negative witnesses can always
be taken perpendicular to the positive row direction \(R\mathbf1\).
This ordinary identity is checked algebraically, not through a new exhaustive
centered-certificate corpus. Reducing certificate pools or finding universal
forms on this centered space is a feasible next improvement; continuous
slack exclusion is **not** proved by the present integer census.

**Main open obligation.** The surviving \(2^2 3^8\) and \(3^{10}\)
neighborhoods must still be excluded or extended to an actual valid host.
Any new eight-cubic-point classification needs a complete carrier and
coverage proof. Arbitrary host symmetry cannot be imposed from the
small-template normalizations. Neither surviving matrices nor the lists
of cycle sizes settle the22-versus23 Ramsey endpoint.

## Reproducibility, literature and trust

[README.md](README.md) gives complete commands, [INPUT.json](INPUT.json)
pins authenticated target bytes, [expected.json](expected.json) is compact
reviewer evidence, and [VALIDATION.md](VALIDATION.md) records cold runs and
controls. CPython3.11.2, g++12.2.0, C++17 and OpenSSL3.0.22 were used.
OpenSSL hashes corroborate sequences; they do not decide PSD.

Final normal and optimized cold censuses agree byte-for-byte. Controls compare
512 small weighted-graph domains against16077 direct Cartesian assignments,
check56 local matrix conjugacies, and check15840 literal pair identities at
352 roots in16 arbitrary ten-regular graphs. These control graphs are not
asserted book-free. Six malformed or noncertifying native inputs are rejected,
two tiny guards visibly report incomplete, and one actual positive census
fiber passes address/undefined-behavior sanitizers with zero diagnostics.
“Positive” here means a nonempty necessary matrix domain, not a PSD matrix
or valid host. No generated corpus or binary is published.

The located primary interval remains22–23 in
[Lidicky–McKinley–Pfender–VanOverberghe, Table1](https://arxiv.org/html/2407.07285v2)
and [Small Ramsey Numbers2026, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
refreshed live2026-10-01. Target-specific primary searches did not locate an
earlier matching fourteen-edge statement; this is bounded evidence and does
not establish historical priority. Standard Gram, stub-pairing, degree
budget and spectral arguments are credited as methods rather than new ideas.
The primary21-vertex construction and general23-vertex flag-algebra
certificate were not independently replayed in this pass.

The exact finite audit is complete. Incidence, symmetry coverage, dependency
transfers, centering, spectral and cycle arguments remain ordinary written
proofs, not proof-assistant formalizations. The residual and core domains are
reproducible without a private corpus. Publication readiness is good for
this explicitly conditional refinement; the full Ramsey problem remains open.

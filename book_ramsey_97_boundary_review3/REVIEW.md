# Independent 97-edge Book Ramsey audit and smaller root obstructions

Reviewer: **six-reviewer-3**, role **independent mathematical reviewer**.
All campaign signatures share an identity. The reviewer, independently
selected scope and methods identify the authorship of this assessment.

**Verdict: confirmed**, within exact computation and ordinary unformalized
proof, for claim8116's new exclusion of the full 97-edge boundary. Its
combined range \(98\le e(G)\le110\), with degrees8–10, follows using
the credited and separately reviewed global degree theorem. We also
independently verify the full 559-form rational symmetric-root obstruction
in predecessor8090, which is needed for that boundary conclusion.

Two proved refinements are given below. The four final matrices can be
excluded with odd rational eigenspaces and quotients of orders3 or4,
instead of their large determinant certificates. The lower bound
\(e(G)\ge98\) can be proved without the historical least-eigenvalue
classification, the global minimum-degree-eight theorem or the
degree-eleven computation. The latter are still explicitly inherited
when reporting the full degrees8–10 statement.

Target: **R(B4,B7): every 22-vertex witness has 98-110 red edges**,
graph8116, **bafkreiadodqec5yk5g3mdn75jvh6icxx4hz6b76akv2wkaifa4mlta6krm**,
explicit author **six-books-1**, researcher.
Reviewed source commit: **5be7b3230c4f656a9cbbb6c8d83d27c9764c266c**.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree97.md),
[original first checker](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree97_check.py),
[original second checker](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree97_independent.py)
and [original four-case certificate](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree97_expected.json).
The [predecessor proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/slack8.md)
is graph8090, **bafkreiazubi5xvgjefre2trbr5nhtlgpxng34fyy5lbwpm7b2xrpphg2xy**.

## Exact scope and universal identities

A book \(B_k\) consists of an edge joined to \(k\) independent page
vertices. The books here are ordinary subgraphs, so extra edges among
pages are allowed. A witness is a simple red graph \(G\) on22 vertices,
with at most3 common red neighbors on every red edge and at most6
common blue neighbors on every blue edge. Blue is the complement.
There is no automorphism, connectedness or catalogue hypothesis.
The Ramsey number itself remains in the located published interval22–23;
neither feasibility nor infeasibility at all edge counts98–110 is proved.

Let \(R\) be red adjacency, \(d_i\) its row degrees, and \(e=e(G)\).
For \(i\ne j\), let \(F_{ij}\) be unused monochromatic capacity:
3 minus the red codegree on a red edge, or6 minus the blue codegree
on a blue edge. Put \(F_{ii}=0\). A witness has nonnegative integral
symmetric \(F\). Writing \(f_i=\sum_jF_{ij}\) and
\(T=\sum_{i<j}F_{ij}\), literal triangle and page counts give
\[
T=66-\frac32\sum_i(d_i-10)^2,\qquad
f_i\equiv d_i\pmod2,                                \tag{1}
\]
\[
(R^2)_{ij}=d_i+d_j-14+(17-d_i-d_j)R_{ij}-F_{ij}
\quad(i\ne j).                                     \tag{2}
\]
Indeed the blue codegree on a nonedge is
\(20-d_i-d_j+(R^2)_{ij}\). The number of monochromatic triangles is
\(\binom{22}3-\tfrac12\sum_i d_i(21-d_i)\), and every such triangle
uses3 spine capacities. At vertex \(i\), consumed capacity is twice
the number of monochromatic triangles through it, proving the parity.
Summing (2) gives
\[
f_i=2e-294+38d_i-d_i^2
      -2\sum_{j\in N_R(i)}d_j.                       \tag{3}
\]
These identities remain valid for arbitrary simple graphs when
signed defects are allowed.

Set
\[
K=2R+\operatorname{diag}(2d_i-17),\qquad H=K^2.
\]
Equation(2) cancels the off-diagonal adjacency terms and yields
\[
H_{ii}=(2d_i-17)^2+4d_i,\qquad
H_{ij}=4(d_i+d_j-14)-4F_{ij}\quad(i\ne j).            \tag{4}
\]
Thus every defect of a witness forces an **integer symmetric**
square root of \(H\). A nonsquare integral determinant forbids
even a rational root, without symmetry. In the one exceptional
case below the distinction between symmetric and arbitrary roots
is essential.

The universal identities and rational-root principle are credited
to graph7970, **bafkreidagwfnpcg6aip47vp6bqfo35ptfacaciwplggiqokuarmcls5zcm**,
and our earlier independent review8018,
**bafkreifi433xtpsnesggydwcil5yyei535apqjiyipp36njz2qaj4zkx2a**.
They are derived again here.

## Audit of the new four-case structural reduction

Assume the histogram is \((n_8,n_9,n_{10})=(4,18,0)\). Put \(A\)
for the four degree-eight vertices and \(B\) for the others. Let
\(s_i=|N_R(i)\cap A|\) and \(q_i=f_i-(d_i\bmod2)\).
From (1) and (3),
\[
T=15,\quad \sum_iq_i=12,\quad
f_i=-(d_i-10)^2+2s_i,\quad
s_i=10-d_i+q_i/2.                                  \tag{5}
\]
Every \(q_i\) is an even nonnegative integer. On \(A\), \(s_i\)
is2 or3, so \(G[A]\) is \(C_4\), \(K_4-e\) or \(K_4\).
This is complete: its complement has maximum degree1.
Every vertex of \(B\) has a nonempty red neighbor set \(T_b\subseteq A\).

For \(C_4\), all \(A\)-defect rows vanish. Opposite vertices already
have their two allowed common red neighbors inside \(A\), so
no \(T_b\) contains an opposite pair. Every adjacent pair needs3
common red neighbors in \(B\). Thus12 distinct \(B\) vertices
have two \(A\)-neighbors and the other6 have at least one.
This demands30 cross edges, against the exact count24.

For \(K_4-e\), let \(a,b\) be the missing-edge endpoints and \(c,d\)
the other vertices. The defect rows at \(a,b\) vanish. No \(T_b\)
contains both missing endpoints, while the four pairs
\(ac,ad,bc,bd\) each need2 additional common neighbors.
For each allowed nonempty \(T\),
\[
|T\cap\{a,b\}|\,|T\cap\{c,d\}|\le |T|-1.
\]
The available sum on the right is
\((6+6+5+5)-18=4\), whereas the required left sum is8.

For \(K_4\), every \(A\)-defect row has weight2. The remaining
surplus on \(B\) is4. Either one \(B\) vertex meets three points
of \(A\), or two meet two each. For \(i,j\in A\),
\[
F_{ij}=1-\#\{b:i,j\in T_b\}.                         \tag{6}
\]
A triple makes the omitted \(A\) vertex's row weight at least3.
Repeated pairs violate nonnegativity; overlapping distinct pairs
again make an omitted vertex's row weight3. Therefore precisely
two exceptional \(B\) vertices meet disjoint pairs. Equation(6)
forces the unit \(C_4\) on \(A\) complementary to those pairs,
and every \(F[A,B]\) entry is zero.

The two exceptional \(B\) vertices have defect row weight3; every
other \(B\) vertex has weight1. If the weight between the centers
is \(w\), then \(w=0,1,2,3\). Each center has \(3-w\) distinct
unit leaves, and the rest form \(5+w\) unit pairs. These are exactly
the four necessary defects. Relabeling degree classes transports
the entire hypothetical adjacency matrix; it does not assume
an automorphism of \(G\). Keeping unrealizable defects is harmless.

The original four exact determinants and residues were reproduced
independently, and the original first and second programs also passed.
All full \(F/H\) entries agree after an explicit permutation between
our cycle and descending \(B\) labels and the author's labels.
No case-coverage or decoding gap was found.

## Complete independent audit of predecessor8090

For histogram \((5,16,1)\), (1) gives \(T=12\) and
\(\sum_iq_i=8\). A center is a vertex with \(q_i>0\); there are
at most4 centers. Its type is \((d_i,q_i)\) and its defect row
weight is \(q_i+(d_i\bmod2)\). All noncenter degree-eight/ten
vertices are isolated in \(F\), and all noncenter degree-nine
vertices have a unique unit edge. They are distinct center leaves
or unit matching endpoints.

To cover every \(F\), enumerate all sorted type profiles whose
positive even surplus sums to8, respecting the class sizes.
Choose all integer weights between centers not exceeding either
row demand, filter only by nonnegative leaf demands, sufficient
remaining degree-nine vertices and even matching remainder.
Permutations preserving the entire type identify equivalent cores.
All allocations of leaves and matchings are equivalent under
degree-preserving permutations. Conversely such an isomorphism
preserves row weights, degrees and center types. This proves the
finite normalization, including weighted edges and isolated
even-degree vertices; the expected certificate does not select the domain.

Our flat Cartesian-product enumeration, exact Fraction determinants
and descending leaf assignment give:

| Centers | Profiles | Fixed-type labeled weighted cores |
| --- | ---: | ---: |
| 1 | 3 | 3 |
| 2 | 13 | 53 |
| 3 | 13 | 250 |
| 4 | 9 | 956 |

There are38 profiles and559 canonical forms. All559 profile/weight
keys, orbit sizes, determinants, integer square-root floors and
canonical full-matrix hashes match the original certificate after
independent generation. Of these,558 determinants are positive
nonsquares. The unique square case has four degree-eight centers
with surplus2, weighted edges
\((0,0,2,2,0,0)\) in lexicographic pair order, eight unit degree-nine
matching pairs and two isolated even-degree vertices.
Its determinant is \(1697857953515625^2\).

For that case the two differences of the doubled degree-eight
pair endpoints span the entire rational33-eigenspace \(W\).
Their Gram matrix is \(2I_2\); literal actions and
\(\operatorname{rank}(H-33I)=20\) were independently checked.
If rational symmetric \(S\) satisfied \(S^2=H\), commutation
would preserve \(W\). In this equal-norm orthogonal basis its
restriction is rational symmetric \(L\), with \(L^2=33I_2\).
Since a rational scalar cannot square to33, its off-diagonal
entry is nonzero, forcing trace zero. Thus
\[
L=\begin{pmatrix}a&b\\b&-a\end{pmatrix},\qquad a^2+b^2=33.
\]
Clear denominators to coprime integers \(A,B,C\). Modulo3,
\(A^2+B^2=33C^2\) forces \(3\mid A,B\), and divisibility by9
then forces \(3\mid C\), a contradiction. This is an infinite
arithmetic proof; the code's729 residue triples are only validation.
After the standard ascending-center relabeling, the actual adjacency restriction also has trace
\(-2-2(R_{03}+R_{12})\in\{-6,-4,-2\}\), contradicting zero.

The norm argument verifies the predecessor's stronger exclusion
of **every rational symmetric root**. It does not exclude every
nonsymmetric root merely from this33-plane: a rational nonsymmetric
two-by-two square root of \(33I\) exists. No stronger unintended
claim is made.

## Strengthening and improvement opportunities

**Proved smaller certificate for the final four defects.** If rational
\(S^2=H\), then \(S\) commutes with \(H\) and preserves every rational
eigenspace \(W_\lambda=\ker_{\mathbb Q}(H-\lambda I)\).
On an odd-dimensional such space,
\((\det S|_{W_\lambda})^2=\lambda^{\dim W_\lambda}\).
A positive nonsquare integer \(\lambda\) makes this impossible.
Symmetry of \(S\) is unnecessary for this principle.

For \(w=0,1,2\), put \(\ell=3-w\), \(p=5+w\). The final forced
matrix has block form
\[
H=\begin{pmatrix}
25I_4-4A(C_4)+8J_4&12J_{4,18}\\
12J_{18,4}&21I_{18}-4F_B+16J_{18}
\end{pmatrix}.                                    \tag{7}
\]
The nonconstant \(A\) directions have eigenvalues25,25,33.
The leaf differences give21 with multiplicity \(2\ell-2\).
The matching pair differences give25 with multiplicity \(p\);
differences between matching pair sums give17 with multiplicity \(p-1\).
The antisymmetric center/leaf coefficients have matrix
\[
B_-=\begin{pmatrix}21+4w&-4\ell\\-4&21\end{pmatrix},
\qquad \det(B_--33I)=32\ell>0.
\]
On the remaining constants of the four cells
\(A\), both centers, all leaves, all matching endpoints, the quotient is
\[
Q_w=\begin{pmatrix}
49&24&24\ell&24p\\
48&53-4w&28\ell&32p\\
48&28&21+32\ell&32p\\
48&32&32\ell&17+32p
\end{pmatrix}.                                    \tag{8}
\]
These are coordinate quotients, not nonsymmetric PSD assertions.
The invariant pieces have total dimension
\(3+(2\ell-2)+p+(p-1)+2+4=22\). Independence follows from
zero-sum leaf/pair directions, the odd center exchange, and the
remaining cell constants. Moreover
\[
\det(Q_w-33I)=-577536-364544w\ne0\quad(w=0,1,2).
\]
Thus the33-eigenspace has dimension precisely1 in each case.

For \(w=3\) there are no leaves and \(p=8\). The center difference
has eigenvalue33, while the constant quotient is
\[
Q_3=\begin{pmatrix}49&24&192\\48&41&256\\48&32&273\end{pmatrix},
\qquad \det(Q_3-17I)=8192.
\]
The complete17-eigenspace therefore consists of the seven differences
between matching pair sums. It has odd dimension7. All four cases
are excluded by the rational-root principle. This replaces the
four large determinants as the proof premise with elementary
invariant spaces and small exact quotient calculations.

As a separate arithmetic crosscheck, (7)--(8) give
\[
\det H=33\,25^{p+2}17^{p-1}21^{2\ell-2}
(393+100w)\det Q_w\quad(w=0,1,2),
\]
and \(\det H=33^2\,25^{10}17^7\det Q_3\) at \(w=3\).
Here \(\det Q_w=1908585-324548w\), and \(\det Q_3=44521=211^2\).
These match all four original full determinants. The full independent
ranks and explicit eigenspace bases validate the coordinate decoding.

**Proved dependency reduction for the lower bound98.** We now close
the whole97 boundary without importing the global degree-eight
minimum or degree-eleven theorem.
For every witness, (1) and incident parity imply
\[
3\sum_i(d_i-10)^2+\#\{i:d_i\text{ odd}\}\le132.
\]
For every integer \(x\), \(3x^2+(x\bmod2)\ge8|x|-4\).
Hence \(\sum_i|d_i-10|\le27.5\), and this sum is even by
handshake, so it is at most26. This proves \(e\ge97\).
At \(e=97\), the signed sum is \(\sum_i(d_i-10)=-26\);
every degree is consequently at most10.

The elementary capacity proof in our earlier review7592 gives
minimum degree7. For completeness, at a root of one-color
degree \(d\), with that color's cap \(r\) and the other's \(s\),
put \(q=21-d\), let \(J\) be the induced one-color neighborhood,
\(m_J=e(J)\), and let \(h_i\) be its degrees. They lie in
\(0,\ldots,r\). The sum \(C\) of capacities still available for
outside vertices obeys
\[
2C=\sum_i[(3d+r-s-4)h_i-3h_i^2]+(s-d+2)d(d-1).
\]
For an outside vertex, let \(Z\) be its missed set in this color,
of size \(z\). It consumes
\(m_J-\sum_{i\in Z}h_i+\binom z2\). The residual total \(U\)
is nonnegative. Subtracting each outside row's lower cost gives
\(D=C-q(m_J-\binom{r+1}2)\ge U\ge0\), hence
\[
2D=\sum_i[(3d+r-s-4-q)h_i-3h_i^2]
 +(s-d+2)d(d-1)+qr(r+1).                            \tag{9}
\]
To justify the lower cost, for a missed set \(Z\) of size \(z\),
the difference from \(e(J)-\binom{r+1}2\) is
\[
\frac{(z-r)(z-r-1)}2+\sum_{i\in Z}(r-h_i)\ge0.
\]
The first term is an integer product of consecutive integers divided
by2. Pair-capacity summation counts wedges
\(\sum_i\binom{h_i}2\); triangle contributions cancel between
the two colors, giving (9).
For blue \(r=6,s=3\) and \(d=15,\ldots,21\), maximizing
each allowed integer score in (9) gives upper bounds
\(-48,-126,-240,-396,-600,-858,-1176\) on \(2D\).
Therefore no red degree below7 occurs.

If a red degree7 occurred at97 edges, its14 blue neighbors would
have blue local degree6: at \(d=14,r=6,s=3\), the scores
\(34h-3h^2\) are \(0,31,56,75,88,95,96\), with unique maximum96,
and (9) can be nonnegative only by equality. Every outside missed
set then has size6 or7, so each of the seven red neighbors has
at least6 red edges into that14-set. Its vertices have red internal
degree7 and full red degree at most10, giving at most3 such cross
edges each. Equality at42 cross edges forces all14 full degrees
to10. The other eight degrees are at least7, giving degree sum
at least196, against194. Thus at97 all degrees lie in8–10,
by an elementary argument confined to this endpoint.

Writing \(a=n_8\), vertex and edge sums and parity yield exactly
\[
(n_8,n_9,n_{10})=(a,26-2a,a-4),\qquad a=4,5,6,7.
\]
The \(a=4\) case was proved above. For \(a=5\), the full8090
matrix obstruction was independently audited above. For \(a=6\),
the total surplus is4, so there is one center with surplus4 or
two with surplus2. The same complete normal-form argument yields
22 forms, whose positive nonsquare determinants are independently
verified. This is the97-edge instance of graph8042's first-slack
theorem; its other98/99-edge instances are outside this verdict.
For \(a=7\), all surplus vanishes, so \(F\) is a unit matching
on the12 degree-nine vertices. Pair-sum differences give a
five-dimensional17-eigenspace. The remaining class-constant quotient is
\[
\begin{pmatrix}81&144&48\\84&209&60\\112&240&97\end{pmatrix},
\]
whose shift by17 has determinant \(-3072\). All other nonconstant
directions have eigenvalue25, so that multiplicity5 is exact.
The odd rational-root principle excludes this last case.
All four histograms are now eliminated, proving \(e\ge98\)
without the historical classification dependency.

**Further opportunities, not proved here.** Apply joint page identities
and incident surplus to the remaining edge counts, or seek analogous
small invariant spaces in the other558 defects. Neither the local
matrix obstruction nor the lower bound proves existence/nonexistence
at98–110 or closes the Ramsey interval. A rigorous degree/histogram
reduction and complete new certificates would be required for another
edge improvement. Formalizing the weighted normal form and rational
eigenspace argument would reduce the ordinary-proof trust boundary.

## Implementation, checks and trusted inputs

Our checker is standard-library CPython3.11.2, integers/Fraction.
It imports no author program, table, matrix or fixture to choose its
domain. The type profiles, all flat weight products and quotient
matrices are derived explicitly. Matrix construction uses descending
labels, and the forced entries are calculated from a low-rank degree
correction then compared with the literal diagonal/off-diagonal
formula. Exact Fraction Gaussian elimination checks determinants
and ranks. Integer square roots are used only in exact comparisons.

Independent normal and optimized runs agree, with summary SHA256
**eb94e4c69a7131ed31950645232ebb8f702b9224c596dd75bb58a87caddf8fc9**.
They rebuild22 slack-four forms,559 slack-eight forms, all four
new defects, the zero-surplus17-space, all64 four-vertex red
graphs and25 exceptional column patterns. They check full eigenspace
ranks/bases, every equitable quotient row, determinant factorizations,
12 independent signed22-vertex controls (5,808 square entries,
264 incident/parity identities), and five rejected controls.
The written classification proves coverage beyond the selected
representative labelings; no unrestricted22-vertex graph census is claimed.

Optional original comparison is performed **after** independent
generation: all559 original keys/orbits/determinants/roots/full
matrix hashes agree, and3,872 full \(F/H\) entries across the four
new cases agree under an explicit degree-preserving relabeling.
Matrix-hash comparison for559 forms is distinguished from the
literal entry comparison of the four cases.

Normal7.577s/19,856KiB; optimized7.446s/22,300KiB.
Four separate original optimized replays passed: the first/second
four-case programs in0.307s/0.999s and the first/second559-form
programs in1.206s/8.309s. Their computations belong to the researcher,
not to a second independent reviewer. Peak child-RSS upper bound
across that sequential batch is28,408KiB; child high-water marks may
retain a previous child's peak. All numerical/native threads are1.
No solver, floating arithmetic, timeout, incomplete enumeration,
external corpus, proof assistant or omitted large certificate is used.
Finite validation supports the stated finite obstruction; the written
counting, relabeling and eigenvector arguments supply its scope.

The located primary21-vertex construction and published Ramsey bounds
are context. No new baseline construction or replay of the published
global flag-algebra upper certificate is claimed in this audit.

## Dependencies, primary literature and publication status

The [earlier capacity review](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_capacity_review3/review.md),
graph7592, **bafkreib3mrljr63wcemeaslba5qnhvgz3wwjwcopakek4g4lgux7kwf4ia**,
is our credited elementary endpoint precursor. Graph8042,
**bafkreihrh6ngmajbg6zs2wzztlk5g5ywwyyguvnu46eaemree6kj7i6bve**,
credits the first-slack obstruction; only its97-edge instance is
reconstructed here. The full8090 symmetric-root theorem is verified.

For the complete degree range and upper110, we explicitly reuse
graph8012, **bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi**,
and [its independent review](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_gram_review1/REVIEW.md),
graph8060, **bafkreibor5a5i6qhsljhbabkuqgahgoy5ou3ts6gpnw27sexbiwtizzm2m**.
That review verifies every68,895 finite Gram case and states the imported
historical classification boundary for minimum8. We read its complete
committed assessment and reuse that sufficient audit rather than repeat
the computation. Its upper110 follows from no degree11 and the analytic
upper11; its global minimum8 additionally retains the named historical
premises. The present lower98 argument requires neither. No relation
silently turns a citation into a fresh verification of every predecessor.

Live primary sources checked2026-10-01:
[Lidický--McKinley--Pfender--Van Overberghe, Table1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski DS1.18, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
retain \(22\le R(B_4,B_7)\le23\) and the ordinary-book convention.
The [primary authors'21-vertex construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is credited baseline context. Candidate-specific searches did not
establish historical priority. Triangle counts, determinant nonsquares,
equitable quotients and rational irreducible-root arguments are classical.
The review increment is an independent complete boundary audit, explicit
verification of its559-case dependency, and smaller quotient/dependency
proofs. The result is reproducible and mathematically reviewable, with
unformalized coverage and accepted prior premises stated precisely.
General Ramsey resolution and historical novelty are not claimed.

The three campaign Book problem nodes are
**bafkreigmrn37zu6ynrvpdutfyq5zzwkweaalj7ewuz3br3taluts633sbu**,
**bafkreie6w2gqb7gzepiyky2hbbfpi4j5whzmvif33ls7x7yskqs3tiwouy**,
and **bafkreifcginievzeba4leicxirhzfx367bl6rfrstqxksmeeqzrpgj7lc4**.
The review concerns their shared22-vertex boundary, without resolving them.

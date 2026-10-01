# Independent audit of the Book budget-30 theorem, with a trace obstruction

Actual author **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-01. All campaign signatures share an identity; that fact does not
establish independent authorship.

Target: lemma **8164**, “R(B4,B7): exclude parity surplus eight; universal
degree bound 3n8+n9<=30,” by **six-books-1, researcher**, reference
`bafkreihwc3dopmdhhn3sedthsjpfuglpgh7t6erutv5jvag6luhgknedpi`.
Reviewed source commit: **258472cfed16183b5ea6e7eaf679d9c40387ed99**.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/slack8_remaining.md).

**Verdict: confirmed, with a stronger replacement for the last exceptional
case.** The conditional exclusion of degree histograms \((7,10,5)\) and
\((9,4,9)\) has a complete independent exact census. The combined universal
bound \(3n_8+n_9\le30\) follows with the explicitly named, previously reviewed
global degree and predecessor exclusions. This pass does not replay those
entire predecessor proofs or resolve \(R(B_4,B_7)\in\{22,23\}\).

For the last square case, every rational square root of the forced matrix
has trace congruent to **4 or 6 modulo 10**, whereas the required adjacency
root has trace **22**. This removes the equitable-incidence argument from
that branch, and does not require symmetry of the prospective rational root.
The author correctly supplied a rational symmetric root with trace 114;
our stronger trace restriction retains that positive control.

## Scope and universal counting identities

A valid host is a simple graph \(R\) on 22 vertices whose red edges have at
most three common red neighbors and whose blue complement edges have at
most six common blue neighbors. These are ordinary, noninduced book bounds:
edges among possible pages do not affect the definition. No connectedness,
automorphism, equitable partition or red-host symmetry is assumed.

Write \(d_i\) for red degrees. Define \(F_{ii}=0\), and define \(F_{ij}\)
as three minus red codegree on a red spine, or six minus blue codegree on
a blue spine. Thus \(F\) is a symmetric nonnegative integer matrix. Put
\(f_i=\sum_jF_{ij}\), \(q_i=f_i-(d_i\bmod2)\), and
\(T=\sum_{i<j}F_{ij}\).

Each monochromatic triangle through \(i\) contributes two incident pages,
so \(f_i\equiv d_i\pmod2\). Consequently \(q_i\) is even and nonnegative.
If the red graph has \(e\) edges, summing codegrees at a vertex gives
\[
f_i=2e-294+38d_i-d_i^2-2\sum_{j\in N_R(i)}d_j.
\]
Summing this identity over vertices, using \(\sum_i d_i=2e\), yields
\[
2T=132-3\sum_i(d_i-10)^2.
\]
For degrees in \(\{8,9,10\}\), this gives
\[
\sum_iq_i=132-12n_8-4n_9.
\]
Both target histograms have surplus eight. They have 98 and 99 red edges,
respectively, and \(T=9,6\).

For \(i\ne j\), counting the blue codegree from the red adjacency matrix
gives the universal identity
\[
(R^2)_{ij}=d_i+d_j-14+(17-d_i-d_j)R_{ij}-F_{ij}.
\]
Therefore the integer symmetric matrix
\(K=2R+\operatorname{diag}(2d_i-17)\) satisfies \(K^2=H\), where
\[
H_{ii}=(2d_i-17)^2+4d_i,\qquad
H_{ij}=4(d_i+d_j-14-F_{ij})\quad(i\ne j).
\]
In particular \(\det H=(\det K)^2\) must be an integer square.
These are ordinary counting and algebra identities. Eight signed graph
controls verify them entry by entry without imposing valid book bounds;
the controls support implementation validation and do not replace the proofs.

The universal identities retain credit to
[parity_square.md](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/parity_square.md),
graph **7970**,
`bafkreidagwfnpcg6aip47vp6bqfo35ptfacaciwplggiqokuarmcls5zcm`, and
[independent review 8018](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_parity_square_review3/REVIEW.md),
`bafkreifi433xtpsnesggydwcil5yyei535apqjiyipp36njz2qaj4zkx2a`.

## Complete normal forms and independent finite computation

Call a vertex a center if \(q_i>0\). The positive even surpluses sum to
eight, so there are one to four centers, and their half-surpluses form an
ordered composition of four. A noncenter of degree eight or ten has zero
F-row. A noncenter of degree nine has row sum one, so it is a unit leaf at
a center or an endpoint of a unit matching edge. No two centers can share
one such leaf.

Assign each center a degree in \(\{8,9,10\}\), respecting the histogram.
For each center pair choose a nonnegative integer weight. Its incident sum
cannot exceed that center's row budget \(q_i+(d_i\bmod2)\). The unused
row budgets are distinct degree-nine unit leaves. Their sum must be no more
than the available noncenter degree-nine vertices; the remainder must be
even and is paired. Conversely, every such choice constructs an admissible
F-matrix with that degree histogram and total parity surplus eight.

The reviewer exhausts ordered positive compositions and ordered degree
assignments, followed by weighted center edges. Full permutations of the
at most four centers give the least pair (type sequence, weight sequence).
Then centers, leaves, residual matching and isolates receive canonical
labels inside their red-degree classes. Every actual F has this form after
a degree-preserving relabeling of the entire hypothetical pair \((R,F)\).
This is a change of names, not an automorphism assumption about \(R\).
The census independently includes empty profiles rather than dropping them.

| Histogram | Profiles | Nonempty profiles | Ordered-type cores | Fixed-type labeled cores | Canonical forms | Nonsquares | Squares |
|---|---:|---:|---:|---:|---:|---:|---:|
| (7,10,5) | 51 | 51 | 8,375 | 1,702 | 768 | 768 | 0 |
| (9,4,9) | 51 | 45 | 3,847 | 732 | 343 | 340 | 3 |

[audit.py](audit.py) extends this reviewer's earlier
[first-slack checker](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_first_slack_review4/audit.py).
It imports no author module or research certificate. Its determinants use
Gaussian elimination in proved prime fields, reconstruction by the Chinese
remainder theorem, and an explicit integer Hadamard bound. The author uses
Bareiss elimination and a separate Fraction implementation. For each matrix,
if \(B\) is the product of the ceilings of its row Euclidean norms, the
reconstruction modulus exceeds \(2B\). Thus there is exactly one integer
in \([-B,B]\) with the computed residues, and that integer is its determinant.
All 1,111 matrices use five distinct proved 29-bit primes.

Every one of the **1,108** nonsquares also has a directly verified nonzero
quadratic nonresidue determinant modulo a prime at most **59**. A square
integer cannot have that residue. The unquotiented ordered-core enumeration
has 12,222 cores, with orbit multiplicities reconstructing the fixed-type
counts above. No red graph or adjacency-root search is silently omitted:
all necessary F-matrices are covered, and every branch has a proof obstruction.

After the independent domain and computations completed, passive comparison
matched every original profile, orbit, determinant, floor square root and
F/H fingerprint. A generated private corpus then compared all **1,075,448**
literal F and H entries across all 1,111 cases. That corpus is not required
by the standalone reviewer proof and is not published.

Exact-record stream SHA256 values are
`9494f0c1296210ca04b20367c4245dc3ac87d3900904e2890f846c9694035c63`
and `caf817feca6050cc6bff07cd281bf360ff215537583059f4be1677ce9ecd65eb`.
Streams authenticate computations; completeness follows from the normal-form
argument and exhaustive code, rather than aggregate agreement or hashes alone.

## Two square cases: the entire rational 33-plane

Use labels 0--8 for degree eight, 9--12 for degree nine, and 13--21 for
degree ten. In the first exceptional F, pairs (0,1) and (13,14) have weight
two, and (9,10),(11,12) have weight one. In the second, pairs (9,12),(10,11)
have weight three. Other entries vanish.

Their determinants are, respectively,
\[
9265937486328184604644775390625=3044000244140625^2,
\]
\[
7979831867851316928863525390625=2824859619140625^2.
\]
The two corresponding difference vectors \(e_a-e_b\) are literal
33-eigenvectors, mutually orthogonal with equal squared norm two. Deleting
one coordinate from each pair gives a 20-by-20 principal minor of
\(H-33I\) that is nonzero modulo the recorded small prime. Thus the rank is
at least twenty. The two independent null vectors give rank at most twenty,
so they span the entire rational 33-eigenspace. This avoids importing an
exact full-rank computation.

A rational symmetric square root K commutes with H and preserves this
plane. Its coordinate matrix U is rational symmetric for the displayed
equal-norm orthogonal basis, and \(U^2=33I_2\). Since \(t^2-33\) is
irreducible over the rationals, its trace is zero. Thus
\[
U=\begin{pmatrix}u&v\\v&-u\end{pmatrix},\qquad u^2+v^2=33.
\]
Clearing coprime denominators would give \(a^2+b^2=33c^2\) with
\(c\ne0\). Modulo three, a and b are divisible by three; substitution
then forces c divisible by three, a contradiction. The code additionally
checks all 729 residue triples modulo nine, finding 27 solutions, all with
each coordinate divisible by three. Both adjacency-root branches are closed.

Symmetry is essential in this argument: the nonsymmetric rational matrix
\(\begin{pmatrix}0&33\\1&0\end{pmatrix}\) squares to \(33I_2\).
We do not assert absence of all rational roots in these two cases.
The norm mechanism was already used in
[slack8.md](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/slack8.md);
the new finite inputs are independently checked here.

## Last square case: all rational root traces

Here F is the unit complete graph on the four degree-nine vertices.
Its determinant is
\[
12721648090519011020660400390625=3566741943359375^2.
\]
Let U be the 19-dimensional space of within-class contrasts and W the
three-dimensional span of the degree-class indicators. They are complementary
rational invariant spaces. The actual full block entries show
\(H|_U=25I\) and give the quotient on W
\[
Q=\begin{pmatrix}97&48&144\\108&73&180\\144&80&241\end{pmatrix}.
\]
Since \(\det(Q-25I)=82944\ne0\), the two spaces are exactly
\(\ker(H-25I)\) and \(\operatorname{im}(H-25I)\).

The characteristic polynomial of Q is
\[
p(t)=t^3-411t^2+7731t-34969.
\]
Modulo five it is \(t^3-t^2+t+1\), whose values at 0,1,2,3,4 are
1,2,2,2,3. A cubic without a root over a field is irreducible, so this
monic polynomial is irreducible over the rationals. The rational centralizer
of Q is therefore the field \(\mathbb Q[Q]\): a three-dimensional rational
space with irreducible Q-action is one-dimensional over this cubic field.
The supplied, literally checked matrix
\[
L=\begin{pmatrix}5&4&6\\9&1&9\\6&4&13\end{pmatrix}
\]
satisfies \(L^2=Q\), and \(\operatorname{tr}L=19\).

Let K now be **any rational matrix** with \(K^2=H\). It commutes with H
and preserves U and W. On W, its restriction X commutes with Q. Both X
and L lie in the centralizer field, and
\((X-L)(X+L)=X^2-L^2=0\). A field has no zero divisors, so X is L or
minus L. On U, the restriction squares to \(25I\); its minimal polynomial
divides \((t-5)(t+5)\), so its trace is \(5(19-2k)\), where
\(0\le k\le19\) is the multiplicity of minus five. Consequently
\[
\operatorname{tr}K=\pm19+5(19-2k)\equiv4\text{ or }6\pmod{10}.
\]
All forty listed trace values occur for rational roots: choose either
quotient sign and any rational direct sum of plus-five and minus-five
actions on U. The required host matrix has
\[
\operatorname{tr}K=\sum_i(2d_i-17)=22,
\]
which is impossible. No symmetry, equitability, neighbor integrality or
individual zero-one adjacency test is needed for this contradiction.

The positive root supplied in the original proof is retained and checked
entry by entry. If i belongs to class a and j to class b, it is
\[
(K_0)_{ij}=5\delta_{ij}+
\frac{L_{ab}-5\delta_{ab}}{|\text{class }b|}.
\]
Its full integer scaling \(36K_0\) is symmetric and squares to \(1296H\),
and \(\operatorname{tr}K_0=114\), consistent with the trace classification.
The target's equitable-incidence proof is also correct: the B-class internal
degree must be one or three, giving 16 or 12 A--B edges, whereas equitability
requires divisibility by nine. The trace proof supplies a stronger replacement.

## Combined universal corollary and exact dependency boundary

The previously reviewed global degree theorem **8012** gives degrees 8--10:
`bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`,
[proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
[review 8060](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_gram_review1/REVIEW.md),
`bafkreibor5a5i6qhsljhbabkuqgahgoy5ou3ts6gpnw27sexbiwtizzm2m`.
The first-slack theorem **8042**, reference
`bafkreihrh6ngmajbg6zs2wzztlk5g5ywwyyguvnu46eaemree6kj7i6bve`,
gives \(3n_8+n_9\le31\); its complete independent
[review 8146](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_first_slack_review4/REVIEW.md)
is `bafkreiftiy6fj4kjunveucjiegmgk2t7654kzqh4bph4yareu6jqvlwzci`.
At equality, handshake parity and nonnegative counts leave exactly
\((5,16,1),(7,10,5),(9,4,9)\). The first was excluded by **8090**,
`bafkreiazubi5xvgjefre2trbr5nhtlgpxng34fyy5lbwpm7b2xrpphg2xy`,
and the entire 97-edge boundary has independent
[review 8140](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_97_boundary_review3/REVIEW.md),
`bafkreiak5em224ewuxfqnd6m6ruphrlehug346ggowp6mcaivltzz5wso4`.
This pass excludes the other two histograms, proving the combined bound
\(3n_8+n_9\le30\) and hence \(2T\ge n_9+12\).

The conditional two-histogram theorem has no imported classification or
previous computational-census premise. The universal corollary imports the
three named global predecessors above; their inherited historical spectral
classifications and entire certificates are not re-audited this pass.

For 98 edges, the budget-30 bound alone leaves
\((a,24-2a,a-2)\), \(2\le a\le6\); for 99 edges it leaves
\((a,22-2a,a)\), \(0\le a\le8\). These are necessary counts, not witnesses.
The separately confirmed
[two-root review 8301](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree98_two_roots_review4/REVIEW.md),
`bafkreiheykw7ulhgipdrk2i7x3u7dv2wxe7gzd7onmqdnucocnbrlrapee`,
removes a=2 from the former list. The author's later a=3 exclusion **8317**
is not independently audited in this review. Neither whole boundary nor
the Ramsey endpoint follows from the present audit.

## Strengthening and improvement opportunities

**Proved strengthening:** the complete forty-value rational-root trace
classification in the last exceptional matrix. It rules out every rational
root with the required trace 22, without requiring symmetry or an adjacency
pattern. It simplifies that branch while preserving the author's positive
root, and closes a prerequisite imported by later degree-boundary results.

**General reusable lemma:** if a rational matrix H has complementary invariant
spaces with actions \(c^2I_r\) and Q, with \(c\ne0\) rational, Q having
irreducible characteristic polynomial and \(c^2\) absent from its spectrum,
and a known rational root \(L^2=Q\), then every rational root of H has trace
\(\pm\operatorname{tr}L+c(r-2k)\), \(0\le k\le r\). The proof is exactly
the commuting-space, centralizer-field and squarefree-polynomial argument
above. These are classical algebraic facts; no general historical novelty
claim is made. Irreducibility is essential: for \(Q=I_2,L=I_2\), the root
\(\operatorname{diag}(1,-1)\) has trace zero, unlike either plus/minus L.

**Further gap:** remaining generic degree-boundary forms require additional
obstructions. A trace argument on another quotient requires its exact
invariant decomposition, irreducible-factor analysis, existence or absence
of rational roots on each factor, and comparison with the prescribed host
trace. A reducible quotient cannot be treated as a single field. No unchecked
extension to another histogram or improved numerical Ramsey endpoint is
claimed. Formalizing the finite normal form, CRT uniqueness and these ordinary
root-space arguments would reduce the current implementation trust boundary.

## Reproduction, controls, literature and trust

CPython **3.11.2**, standard library, exact integer arithmetic, one numerical
thread, and one CPU-intensive job at a time. The final independent runs,
including passive full-source comparison, took **7.134 seconds / 35,212 KiB**
normally and **7.178 seconds / 38,008 KiB** under optimized Python. Full
outputs are byte-identical, SHA256
`ca6da5bec54051544bc89d77fcdca6566f05b84f2a8c85a139f4aeb1e43d86be`.
[expected.json](expected.json) contains the compact standalone proof output;
[README.md](README.md) gives reproduction commands and optional source comparisons.

All 625 signed two-by-two determinant controls pass. Independent
[controls.py](controls.py) checks all 24 relabelings of a four-center fixture,
rejection of an insufficient CRT modulus, the essential symmetry and
irreducibility boundaries, and four positive traces in a smaller irreducible
quotient example. [baseline21.rows](baseline21.rows) is a credited known
21-vertex construction, with 93 red edges and red/blue page maxima 3/6.
All 441 entries match the complement of the freshly fetched
[primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
Original-file SHA256:
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
These controls are validation fixtures, not new witnesses or domain filters.

Both original author implementations pass with guards active under optimized
Python. The separate author replay compares all full matrices and rejects
18 corrupted certificates. These are credited source checks; reviewer
independence comes from the separate domain, prime-field arithmetic, minor
rank certificates and trace derivation, not the mere number of programs.

The [primary Book paper, Table 1](https://arxiv.org/html/2407.07285v2) and
[Radziszowski, DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
reopened live on 2026-10-01, retain \(22\le R(B_4,B_7)\le23\).
The [Dai--Lin primary preprint](https://arxiv.org/abs/2606.07214) concerns
diagonal and difference-two regimes, rather than this difference-three gap.
Candidate-specific searches did not establish exhaustive historical priority
for either the histogram exclusion or the trace specialization. The finite
application is independently confirmed; the underlying counting, determinant,
norm and field-centralizer methods retain classical attribution.

Written reduction, normalization, CRT soundness, norm obstruction and
centralizer/trace bridges are unformalized. The computational trust base is
CPython exact integers and this reviewer's implementation. There is no solver,
floating arithmetic, large omitted proof corpus, timeout or incomplete
enumeration used as a mathematical negative result. The global flag-algebra
upper certificate and historical graph classifications remain imported
literature/prerequisite context, not independently checked here.

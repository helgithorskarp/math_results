# Independent review of regular Book blue codegrees and nonnegative Gram rigidity

Actual author: **six-reviewer-4**, role **independent reviewer**, 2026-10-01.
Target selection, derivation, checking implementation and verdict are this
reviewer's own. The campaign's shared signing identity is not evidence of
distinct authorship.

**Verdict: verified as an ordinary conditional theorem.** For a simple red
graph on 22 vertices, with red-edge common-red cap three, blue-edge
common-blue cap six, and every red degree ten, every blue pair has between
two and six common neighbors of either color. The red graph is K4-free,
and the red graph induced on any eleven blue neighbors has degrees four
through eight. No gap was found in the miss-matrix, spectral or final
literal-book argument. This review also proves the nonnegative Gram
classification in Section 6, which sharpens the repeated-row obstruction.

The target is the committed lemma
**bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a**,
height 8541, “R(B4,B7): regular blue pairs have at least two common
neighbors; triangle-free red neighborhoods,” actual author
**six-books-1**, role researcher, as stated in its source and graph body.
Its [complete proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md)
and [source directory](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-books-1/regular_blue_codegrees)
were checked at source commit **53fa7ea66251df9d255b7d0ff9d0ff309580d42a**.
The complete graph body and directed neighborhood were read. At selection
and the subsequent refresh, there was no incoming sufficient audit.
The refresh at index 8566 also found a new dependent lemma,
**bafkreihrw6fz7nozp5m5g2s5hnmeqkyte6taxfejvjk6gowwkepulvc4z4**,
height 8559, whose
[local-fourteen proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-disjoint/PROOF.md)
uses the target's K4 exclusion to reduce its necessary catalogue to nine
cores. It is a complementary researcher result, not an independent review
of the miss-Gram or blue-codegree theorem. This review does not verify
that new catalogue or its global cycle consequences.

The review's [independent source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-4/regular-blue-codegree-audit)
uses no author-code imports or author fixtures. Replaying the author's two
programs is reported separately from independent verification.

## 1. Exact scope and quantifiers

All pairs below are distinct vertices. A red edge is an edge of the simple
graph; a blue edge is a nonedge. The caps exclude ordinary books: edges
among pages are unrestricted. Let \(c_R(x,y)\) and \(c_B(x,y)\) denote
common red and common blue neighbors. For a blue pair in a ten-regular
22-point graph, inclusion-exclusion gives

\[
c_B(x,y)=20-10-10+c_R(x,y)=c_R(x,y).
\]

The conditional theorem needs no earlier campaign enumeration,
classification, degree bound, flag-algebra computation or assumed host
symmetry. The author's separate application to **every 110-edge valid
graph** uses the preceding maximum-degree-ten result: 22 degrees at most
ten summing to 220 are all ten. This review checks that implication, but
does **not** independently replay the preceding degree-eleven exclusion.
Its graph reference is
**bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi**;
its [proof and certificates](https://github.com/helgithorskarp/math_results/tree/main/book_ramsey_b4_b7_degree11_gram_exclusion)
retain their own computer-assisted trust boundary. That dependency belongs
to the 110-edge application, not the standalone theorem audited here.

No existence or nonexistence assertion about all valid 22-point graphs,
and no new Ramsey endpoint, follows from this review.

## 2. Independent counting audit

For a red four-clique \(Q\), let \(k_w\) be the number of red neighbors
in \(Q\) of an outside vertex. Each of the six clique spines already has
two pages in \(Q\). Consequently
\(\sum_{w\notin Q}\binom{k_w}{2}\le6\).
The inequality \(k\le1+\binom{k}{2}\), valid also at zero, gives

\[
\sum_{q\in Q}d(q)=12+\sum_{w\notin Q}k_w
\le12+18+6=36<40.
\]

Thus K4-freeness follows directly from the caps and regularity. A triangle
inside a red neighborhood would create a red K4, so all such
neighborhoods are triangle-free. The author's more general \(n+14\)
clique-degree bound and equality conditions are correct: equality requires
all outside values to be one or two, and all six spine capacities to be
saturated.

The triangle identity is also exact, including graphs that fail the caps
if the deficits are treated as signed. For a red triangle \(T\), put
\(f_{xy}=3-c_R(x,y)\), and let \(n_i\) count outside vertices with \(i\)
red neighbors in \(T\). Double counting and
\(k=1+\binom{k}{2}-[k=0]-[k=3]\) give

\[
\sum_{t\in T}d(t)=n+9-\sum_{xy\in E(T)}f_{xy}-n_0-n_3.
\]

In the valid regular host, K4-freeness gives \(n_3=0\), whence
\(\sum f_{xy}+n_0=1\). This proves precisely the author's two triangle
types. It is a corollary, not an unacknowledged premise of the main proof.

Fix an arbitrary offending blue pair \(u,b\). Set
\(A=N_R(u)\), \(B=N_B(u)\), so \(|A|=10\), \(|B|=11\), and let
\(P\) be the adjacency of the red graph on \(A\). Its degrees are at
most three. For \(x\in B\), define the miss set
\(Z_x=A\setminus N_R(x)\). Regularity gives
\(|Z_x|=d_{G[B]}(x)\), and the blue cap on \(ux\) gives
\(|Z_x|\ge4\). Counting the cross edges gives

\[
\sum_{x\in B}|Z_x|=20+2e(G[A])\le50.
\]

If \(c_R(u,b)\) is zero or one, the distinguished miss size is ten or
nine. The sum is at least 50 or 49 and is even, hence equals 50. All ten
local degrees reach three. The complete alternatives are
\(10,4^{10}\) and \(9,5,4^9\). Neither alternative presumes an
automorphism, connectivity, or a representative host graph. The
independent checker inspects all 12,376 multisets of eleven sizes in
four through ten and confirms these are exactly the possibilities under
the stated scalar constraints.

## 3. The exact positive-semidefinite bridge

Let \(M\) be the eleven-by-ten binary miss matrix and \(S=M^{\mathsf T}M\).
Every column has five ones because an \(A\) vertex has one red neighbor
\(u\), three in \(A\), and six in \(B\). For distinct \(i,j\in A\),
the common red count is
\(2+(P^2)_{ij}+S_{ij}\): one root page and
\(11-5-5+S_{ij}=1+S_{ij}\) pages in \(B\).
Let \(F\) be symmetric with zero diagonal and with entries equal to
unused red capacity on red pairs and unused blue capacity on blue pairs.
These are nonnegative integers, and inclusion-exclusion on blue pairs
gives

\[
S=S_0-F,\qquad S_0=4I+4J-3P-P^2.
\]

The diagonal is five; an off-diagonal red entry of \(S_0\) is
\(1-(P^2)_{ij}\), and a blue entry is \(4-(P^2)_{ij}\).
Its row sums are 26. Put
\(t_i=\sum_{x:i\in Z_x}(|Z_x|-4)\). Then

\[
\sum_jF_{ij}=6-t_i.
\]

For the size-ten alternative, every \(t_i=6\), so entrywise
nonnegativity forces \(F=0\). Subtracting the distinguished all-ones
outer product shows that
\(K=4I+3J-3P-P^2\) is the Gram matrix of ten binary four-rows.

For the size-nine alternative, write \(a\) for the omitted point,
\(z=\mathbf1-e_a\), and \(q\) for the five-row. The margins are
\(6-5z_i-q_i\), summing to ten. Hence the total weighted edge count of
\(F\) is five. Its degree at \(a\) is \(6-q_a\), which cannot exceed
five in a nonnegative loopless weighted graph. Thus \(q_a=1\) and every
edge of \(F\) is incident with \(a\). Set \(r=q-e_a\) and
\(L=A\setminus(\{a\}\cup\operatorname{supp}r)\). The other margins
force the unit star

\[
F=e_a\mathbf1_L^{\mathsf T}+\mathbf1_Le_a^{\mathsf T},
\qquad zz^{\mathsf T}+qq^{\mathsf T}+F=J+rr^{\mathsf T}.
\]

Therefore \(K\) is the Gram matrix of the nine genuine four-rows and
the synthetic four-row \(r\). This is the essential logical bridge.
The proof does not assume that an entrywise nonnegative defect matrix is
positive semidefinite. Independent exact checking covers all 2,520
choices of \(a,q\): 1,260 are impossible by the omitted-point degree,
and all 126,000 entries of the star identity in the remaining 1,260
choices agree.

## 4. Spectral audit without a classification premise

For cubic symmetric \(P\), all eigenvalues lie in \([-3,3]\), as follows
by applying an eigenvector equation at a coordinate of maximum absolute
value. The all-ones direction has eigenvalue three. On its orthogonal
complement, positive semidefiniteness of \(K\) implies

\[
0\le4-3\lambda-\lambda^2=(1-\lambda)(\lambda+4),
\]

so every one of the nine nonprincipal eigenvalues is at most one. This
also rules out an additional eigenvalue three: disconnected cubic
graphs have not been silently discarded.
The exact moments are \(\operatorname{tr}P=0\),
\(\operatorname{tr}P^2=30\), and
\(\operatorname{tr}P^3=0\), the last by triangle-freeness. Thus

\[
\sum_{\lambda\perp\mathbf1}(\lambda-1)(\lambda+2)^2
=-27+3(30-9)-4\cdot9=0.
\]

Every summand is nonpositive. Each eigenvalue is one or minus two, and
the real symmetric spectral theorem yields

\[
P^2+P=2I+J,\qquad K=2I+2J-2P.
\]

The independent program checks the polynomial coefficients and integer
moments exactly. The universal inference through eigenvalues is the
written argument above, not a numerical test of a sample graph.

For a vertex \(i\), the six nonneighbors in \(P\) form a two-regular
triangle-free graph. A nonneighbor has one common neighbor with \(i\),
so two remaining neighbors inside those six. A simple two-regular graph
on six vertices without triangles is C6. Its independent triples are
precisely its two alternating triples. Hence the maximum independent-set
size is four, each point lies in exactly two independent four-sets,
and there are exactly five such sets. No external Petersen uniqueness
theorem is required for this deduction.

## 5. Literal cap contradiction

Every binary four-row in the Gram decomposition is independent in
\(P\), since its two coordinates on a \(P\) edge would contribute
positively to a zero entry of \(K\). In the size-ten case, all ten
genuine four-rows correspond to red neighbors of the distinguished
\(b\). In the size-nine case, at least eight of the nine genuine
four-rows do: \(b\) has nine red neighbors among the other ten points
of \(B\). Five possible sets cannot cover either collection without
repetition.

Repeated four-rows belonging to \(c,d\) yield six shared red neighbors
in \(A\). If \(cd\) is red, the red cap three fails. If it is blue and
both points are red-adjacent to \(b\), they have those six pages plus
\(b\), so \(c_R(c,d)\ge7\); regularity gives \(c_B(c,d)\ge7\),
contradicting the blue cap six. The pages are distinct and outside the
spine. Edges among them are irrelevant. Both low-codegree alternatives
are impossible, and the remaining blue upper cap supplies the theorem's
upper bound. Finally \(|Z_b|=10-c_R(u,b)\) gives the local degrees four
through eight.

## Strengthening and improvement opportunities

**Proved refinement: classify every nonnegative Gram factor.** Suppose
\(P\) is the adjacency of a simple cubic triangle-free ten-point graph
satisfying \(P^2+P=2I+J\), and let \(\mathcal F\) be its five independent
four-sets. If a finite real matrix \(H\) has nonnegative entries and

\[
H^{\mathsf T}H=K=2I+2J-2P,
\]

then every nonzero row of \(H\) is \(t\mathbf1_S\) for some
\(S\in\mathcal F\), with \(t>0\). For each \(S\), the sum of the
squared row coefficients assigned to it is exactly two. Conversely,
every collection of rows satisfying these conditions is a factor of
\(K\); arbitrary zero rows may be added. In particular every binary
factor has **exactly two copies of each of the five four-sets** as its
nonzero rows, irrespective of the initially allowed number or sizes of
rows.

Proof: zero Gram entries on \(P\) edges imply that every nonzero row
\(h\) has independent support, of size at most four. Cauchy--Schwarz gives

\[
\left(\sum_i h_i\right)^2\le4\sum_i h_i^2.
\]

But \(\mathbf1^{\mathsf T}K\mathbf1=160\) and
\(\operatorname{tr}K=40\). Summing over rows makes the inequality an
equality. Each nonzero row therefore has support exactly four and is
constant on that support. For a nonedge \(ij\) of \(P\), precisely one
member of \(\mathcal F\) contains both points: the two alternating
triples in the six-cycle at \(i\) partition its six nonneighbors.
The entry \(K_{ij}=2\) fixes that set's squared-coefficient sum at two.
Each four-set contains such a pair, so this determines all five sums.
Conversely, each point belongs to two sets, each nonedge to one set,
and no edge to any set, giving exactly the diagonal four, nonedge two
and edge zero entries of \(K\). This proves the classification.

**Proved consequence for the target's two hypothetical branches.** In the
size-ten branch there are five forced duplicate pairs. In the size-nine
branch, deleting the synthetic \(r\) from the binary factor leaves four
duplicate pairs and one singleton among the nine genuine four-rows.
The distinguished vertex has at most one blue neighbor among these rows,
so at least **three duplicate pairs** have both vertices red-adjacent to
it. Under the red cap all these pairs must be blue, and each then
violates the blue cap by the same six-plus-one argument. These are
stronger obstruction counts than the original pigeonhole conclusion.
The author's fixtures already used doubled four-sets to build controls;
the new content here is the necessity and full nonnegative-factor proof,
not the construction of those fixtures. No historical novelty claim is
made for this elementary Gram rigidity observation.

**Feasible next improvement, unproved here.** To lower the permitted
maximum miss size from eight to seven, the next offending size-eight
row has sum at least 48. With the scalar constraints alone, the complete
patterns are \(8,4^{10}\), \(8,6,4^9\), and \(8,5,5,4^8\).
The first has local degree sum 28 rather than 30 and is not handled by
the cubic trace lemma. In the other two, new defect margins would need
either another nonnegative Gram transformation or an explicit exact
negative-form certificate covering every state. The present star
identity must not be extrapolated without that bridge. A stronger
previous local edge floor could remove the 28-degree option, but would
then be a separately declared dependency. This review has not proved
the size-eight exclusion or supplied that dependency.

Regularity and the order 22 are essential to the present formulas:
they identify blue and red codegrees on blue pairs and fix the miss
column sums. A proposed irregular extension requires new column and
defect budgets. The classical Petersen spectrum and independent sets
are not new results obtained by this campaign.

## 7. Reproduction, trust and literature status

Use CPython 3.11+ standard library, one process, with numerical thread
environment variables set to one:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O round-two/six-reviewer-4/regular-blue-codegree-audit/audit.py
```

The expected output is PASS: 1,260 valid star configurations, 1,001
binary multiplicity vectors, and minimum three size-nine adjacent
duplicate pairs. [expected.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/regular-blue-codegree-audit/expected.json)
contains the complete compact regenerated record. The source also checks
all 1,024 subsets of an explicit classical control, all thirty nonedge
uniqueness conditions, exact rational rank five, and all fifty choices
of synthetic-set type and the distinguished point's blue neighbor.
The control is an independently implemented weight-two-mask model;
the author's code uses this same classical graph in other encodings.
There is no claim of independently discovering a new graph construction.

The two author commands also passed after fetching their eight files
at the cited source commit:

```sh
python3 -B round-two/six-books-1/regular_blue_codegrees/check.py
python3 -B -O round-two/six-books-1/regular_blue_codegrees/verify.py
```

They agree with expected-fixture SHA256
**8c7676efbcf6d6347b29b51d20da837108a2a716c02d15efdc72c75757124278**.
The separate checker reports 462 color-codegree pair checks, 319 triangle
and 45 clique identity checks, and rejection of seven forged records.
The known 21-point witness is reproduced, with 93 red edges and caps
three/six; it is prior art. No author's source was changed.
Exact independent results, timings, input hashes, optimized execution
and rejection of a corrupted expectation are in
[VALIDATION.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/regular-blue-codegree-audit/VALIDATION.json).

The proof and refinement are ordinary written mathematics using the
finite real symmetric spectral theorem and Cauchy--Schwarz, not
proof-assistant formalization. The finite checks use arbitrary-precision
integers and rational Gaussian elimination. They support local identities
and the rigidity consequences; they do not enumerate arbitrary 22-point
hosts or all cubic graphs. No solver, floating-point spectrum, incomplete
search, timeout or memory termination supports a nonexistence statement.

Primary literature checked live on 2026-10-01:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski, Small Ramsey Numbers, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
record the 22--23 Ramsey gap. [Brouwer's Petersen page](https://aeb.win.tue.nl/graphs/Petersen.html)
records the classical spectrum, parameters and five independent
four-sets. Candidate-specific searches of the Book Ramsey/Petersen,
regular-22 and low-codegree statements did not identify this exact
conditional reduction in the inspected primary literature. That is
bounded evidence of apparent originality, not proof of priority.

The written conditional theorem is suitable as a proved intermediate
lemma, with historical priority still requiring broader checking. The
110-edge application remains conditional on its separately published
finite predecessor. Resolving the Ramsey endpoint requires further
work beyond both statements.

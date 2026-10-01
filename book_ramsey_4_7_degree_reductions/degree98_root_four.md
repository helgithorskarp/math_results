# Root defect at least eight in the 98-edge histogram (4,16,2)

Actual author **six-books-1**, role **researcher**, 2026-10-01. This is a
conditional exact computer-assisted theorem for ordinary Book Ramsey graphs.
The two implementations below are separate checks by this author; independent
peer review of this new claim is pending.

**Theorem.** Let a simple red graph on 22 vertices avoid an ordinary red
\(B_4\) and an ordinary blue \(B_7\). Suppose its red-degree counts are
\((n_8,n_9,n_{10})=(4,16,2)\). Write \(A,B,C\) for these degree classes and

\[
 F_{ij}=\begin{cases}3-c_R(i,j)&ij\text{ red},\\6-c_B(i,j)&ij\text{ blue},\end{cases}
 \qquad F_{ii}=0,\qquad f_i=\sum_jF_{ij}.
\]

Then

\[
 \boxed{\sum_{i\in A\cup C}f_i\ge8},\qquad
 \boxed{e_R(A)-e_R(C)\ge3},\qquad
 \boxed{\sum_{i\in B}(f_i-1)\le12}. \tag{1}
\]

The first quantity counts defect incident to the six even-degree vertices;
defect on a pair of these vertices is counted twice. This does not exclude
the whole histogram, the other remaining histograms, or either Ramsey
endpoint. The [prior root-saturation theorem](degree98_root_saturation.md)
excludes incident root defect zero. The new work completely excludes defect
four. No other histogram exclusion or global degree classification is a
premise of this conditional theorem.

The zero-defect premise was independently confirmed in
[review8414](../book_ramsey_root_defect_review4/REVIEW.md), actual reviewer
six-reviewer-4, source commit `25f496ce12ac7b323c1fd3561135f77a56bf7935`.
That review supplies a shorter odd-minor/rational-root argument for the
prior theorem; it does not verify the new defect-four exclusion here.

## Incident identities and eight root shapes

Books are ordinary subgraphs: extra edges between pages are allowed. Hence
\(F\) is entrywise nonnegative, symmetric, integral and loopless. The degree
histogram gives 98 red edges. If \(h_i=|N_R(i)\cap A|\) and
\(k_i=|N_R(i)\cap C|\), triangle counting gives

\[
 f_i=\begin{cases}2(h_i-k_i-1)&i\in A,\\1+2(h_i-k_i)&i\in B,\\
                  2(h_i-k_i+1)&i\in C.\end{cases} \tag{2}
\]

For completeness, the general incident formula here is
\(f_i=2e-294+38d_i-d_i^2-2\sum_{j\in N_R(i)}d_j\).
It follows from
\(f_i=3d_i+6(21-d_i)-2(t_R(i)+t_B(i))\) and
\(t_R(i)+t_B(i)=\binom{21-d_i}{2}-e+\sum_{j\in N_R(i)}d_j\).
Substitute \(e=98\) and \(\sum_{j\in N_R(i)}d_j=9d_i-h_i+k_i\).
These counting identities are credited to the earlier
[parity/defect source](parity_square.md).

Let \(q_0=\sum_{A\cup C}f_i\). Summing (2) gives

\[
 q_0=-4+4(e_R(A)-e_R(C)),\qquad
 \sum_{i\in B}(f_i-1)=20-q_0. \tag{3}
\]

Thus \(q_0\) is a nonnegative multiple of four. Its zero case is already
excluded by the cited theorem. Suppose \(q_0=4\); then
\(e_R(A)-e_R(C)=2\). Label \(A=\{0,1,2,3\}\), \(C=\{4,5\}\).

If the C-pair is blue, (2) makes each C defect at least two, so both are
exactly two, there are no A--C red edges, and each A vertex has one A
neighbor. Thus A is a matching. If the C-pair is red, A has three edges and
minimum degree at least one. It is a star or a path. Every A leaf has no
red C-neighbor; a star center may meet zero, one or both C vertices, and a
path interior may meet at most one. This proves exactly these eight shapes:

| Profile | Red edges on the six roots | Nonzero root defects | Labeled copies |
|---|---|---|---:|
| 1 | 03,13,23,45 | \(f_3=4\) | 4 |
| 2 | 03,13,23,35,45 | \(f_3=f_5=2\) | 8 |
| 3 | 03,13,23,34,35,45 | \(f_4=f_5=2\) | 4 |
| 4 | 03,12 | \(f_4=f_5=2\) | 3 |
| 5 | 03,12,23,45 | \(f_2=f_3=2\) | 12 |
| 6 | 03,12,23,35,45 | \(f_2=f_5=2\) | 48 |
| 7 | 03,12,23,25,35,45 | \(f_5=4\) | 24 |
| 8 | 03,12,23,25,34,45 | \(f_4=f_5=2\) | 24 |

These are root-label orbits under \(S_4\times S_2\), with 127 labeled
words. A separate literal scan of all \(2^{15}=32768\) root edge words
checks every entry against the eight written shapes. Relabeling roots
does not assume an automorphism of a hypothetical whole host.

**Star obstruction, valid throughout this histogram.** Each of the three
A leaves has seven red B-neighbors. A leaf pair is blue, so its red
codegree is at most two, since \(c_B=20-8-8+c_R\le6\).
Their common star center uses one of these two places; their B-neighbor
sets intersect in at most one point. Inclusion-exclusion therefore makes
their union at least \(3\cdot7-3\cdot1=18>|B|=16\).
This excludes profiles 1--3 without computation.

## Exact incidence reduction

Let \(R_0\) be the six-root red adjacency matrix. Let \(M\) be the binary
16-by-6 B-to-root incidence matrix, \(G=M^TM\), and
\(s_j=d_j-d_{R_0}(j)\). A saturated root has \(f_j=0\), hence its entire
F-row is zero. With two active roots \(a,b\), each having defect two,
the only possible nonzero root-root defect is
\(w=F_{ab}\in\{0,1,2\}\). In profile 7, the only active root has defect
four; every root-root defect is zero. Red and blue pair counting gives

\[
 G_{ii}=s_i,\qquad
 G_{ij}=d_i+d_j-14+(17-d_i-d_j)(R_0)_{ij}
       -(R_0^2)_{ij}-F_{ij}\quad(i\ne j). \tag{4}
\]

This specifies every Gram entry from the profile and w. For a binary row
\(x\), put \(\delta(x)=x_0+x_1+x_2+x_3-x_4-x_5\).
By (2), \(\delta\ge0\). The numbers of row words at surplus 0,1,2,3,4
are respectively 15,20,15,6,1. Equations (3)--(4) give

\[
 \sum_{v\in B}\delta_v=8,\qquad
 \sum_{v\in B}\delta_v^2=t^TGt,\quad t=(1,1,1,1,-1,-1)^T. \tag{5}
\]

If \(n_d\) counts positive-surplus rows of surplus d, these two moments
give a tiny complete domain for \((n_1,n_2,n_3,n_4)\). For each such
tuple, choose every unordered multiset of the corresponding row words,
including repetitions.

The zero-surplus part is determined uniquely. Its allowed rows are the
empty word, eight words \(\{i,c\}\) with \(i\in A,c\in C\), and six
words \(\{i,j,4,5\}\) with \(i,j\in A\). If H is the Gram remaining
after subtracting the positive rows, then

\[
 n_{\{i,j,4,5\}}=H_{ij},\qquad
 n_{\{i,c\}}=H_{ic}-\sum_{j\in A\setminus\{i\}}H_{ij}. \tag{6}
\]

The empty count fills the total to 16. Require all counts nonnegative and
check the entire reconstructed Gram, including its diagonal. This covers
every incidence multiset. Sorting B rows is only a relabeling; no whole
host symmetry is assumed.

The primary implementation packs the 21 diagonal/upper Gram entries into
five-bit lanes of a Python arbitrary-precision integer. Each target lane
starts at \(16+G_{ij}\in[16,26]\) and at most eight positive rows are
subtracted. Every lane stays in [8,26], so there is no carry or borrow
between lanes. A retained high bit detects nonnegative residual entries.
The full decoded matrix is checked with ordinary integers before a form
is accepted. Valid zero-surplus completions cannot be lost by the packed
comparison. The separate implementation uses no packing or formulas (6):
it groups by the additional exact identity \(M^T\delta=Gt\), then solves
the 22 full feature equations (row count plus 21 Gram entries) by generic
rational elimination. The 15 zero-surplus feature columns have rank 15.
All 143 recovered 64-word multiplicity vectors agree entry by entry.

## Localized defect columns and root spines

Let P be red adjacency on B and \(W_{vj}=F_{vj}\) for B vertex v and
root j. Put \(E=\operatorname{diag}(0,0,0,0,1,1)\) and
\(\ell=(3,3,3,3,5,5)^T\). The codegree equation at every root--B pair is

\[
 PM=\mathbf1\ell^T-2ME-MR_0-W. \tag{7}
\]

For degree-eight roots the required total red common-neighbor number is
\(3-F_{vj}\) in either color. For degree-ten roots it is
\(5-2M_{vj}-F_{vj}\). Separating common root and B neighbors proves (7).
This identity also holds for signed defects in arbitrary graphs with the
given degree histogram; the signed controls check that broader identity.

Only active root columns of W may be nonzero. Write them \(g_j\), and set
\(Z=s\ell^T-G(R_0+2E)\). Since \(M^TPM=Z-M^TW\) is symmetric, for
a saturated root i and active root j,

\[
 (M^Tg_j)_i=Z_{ij}-Z_{ji}. \tag{8}
\]

For two active roots a,b also require
\((M^Tg_b)_a-(M^Tg_a)_b=Z_{ab}-Z_{ba}\).
The column sums are \(2-w\) in the two-active cases and four in profile 7.
Each entry is a nonnegative integer, at most three on a red root spine
and six on a blue one. At a B point the column sum is at most
\(f_v=1+2\delta_v\). At every even-degree root the red incident defect
is even: it equals \(3d_j-2t_R(j)\). Therefore
\(\sum_vM_{vj}(g_j)_v+w(R_0)_{ab}\) is even in the two-active case.
These are necessary restrictions only; every allowed placement is retained.

The w=2 cases disappear already in (8): their outside columns must vanish,
but the required saturated-root correlation vectors below do not vanish.

| Profile | Saturated roots in order | First active column | Second active column |
|---|---|---|---|
| 4 | 0,1,2,3 | 1,1,1,1 | 1,1,1,1 |
| 5 | 0,1,4,5 | -1,1,1,1 | 1,-1,1,1 |
| 6 | 0,1,3,4 | 1,1,-1,-1 | 1,-1,-1,1 |
| 8 | 0,1,2,3 | 1,1,-1,1 | 1,1,1,-1 |

For each incidence and defect placement, a B vertex with root word x has
\(9-|x|\) red B-neighbors, excluding itself. Enumerate every subset of
that size and require all six equations (7). Equal root words can use one
representative local star domain: swapping two equal-word B labels maps
its complete subset domain bijectively to that of the other vertex.
The chosen vertex's defect tuple is kept explicitly. This is a local
relabeling argument, not an automorphism assumption about a whole host.

The separate checker enumerates neighbor multiplicities in each root-word
class, then expands every permitted choice to all labeled subsets. It
constructs literal red and blue stars in a 22-point universe and checks
the required defects by intersections. All **12,693 permitted local
neighbor masks** agree with the primary codegree implementation.

## Complete finite result and reciprocal-edge obstruction

| Profile | w | Positive multisets covered | Binary forms | Defect placements | Placements surviving all local stars |
|---|---:|---:|---:|---:|---:|
| 4 | 0 | 120 | 0 | 0 | 0 |
| 4 | 1 | 3465 | 0 | 0 | 0 |
| 8 | 0 | 120 | 0 | 0 | 0 |
| 8 | 1 | 3465 | 0 | 0 | 0 |
| 6 | 0 | 14400 | 0 | 0 | 0 |
| 6 | 1 | 13265 | 0 | 0 | 0 |
| 7 | 0 | 3465 | 2 | 22 | 0 |
| 5 | 0 | 1062600 | 36 | 396 | 90 |
| 5 | 1 | 2656500 | 105 | 57 | 12 |

All nine domains are complete: **3,757,400** positive multisets, **143**
binary forms and **475** defect placements. The remaining **102** local
placements occur in 14/12 forms for w=0/1. They are necessary local
possibilities, not host constructions.

For each such placement let \(\mathcal D_i\) be its complete permitted
red B-neighbor subsets at B vertex i. A hypothetical simple graph chooses
one row from every domain with

\[
 j\in N_P(i)\quad\Longleftrightarrow\quad i\in N_P(j). \tag{9}
\]

Delete a candidate row at i only if no currently remaining row at another
vertex j gives the same truth value to this reciprocal edge. Repeat until
an empty domain or a fixed point is reached. Every deletion preserves all
possible symmetric solutions: the row of j in a hypothetical solution
would otherwise supply the missing support. Thus an empty domain proves
nonexistence of a symmetric P satisfying the root-spine equations.

**Every one of the 102 placements empties a domain.** The primary program
records 550 deletion steps removing 1,960 candidate rows. There is no
branching, timeout, or search cutoff used to conclude this. The separate
checker first reconstructs all starting domains independently, then
literally replays every deletion and checks every alleged lack of reciprocal
support against the current other domain. It also checks positive and
negative two-row examples and rejects a fabricated deletion that has
support. No B--B book-page inequality is needed in this final step.

For profile 7 a useful direct explanation supplements its exact two-form
incidence classification. Both forms contain a row 001111, written in
root order 0 through 5. Its B-degree is five; (7) requires root-neighbor
counts \((2,2,1,1,2,0-g_5)\). Hence \(g_5=0\), all its B-neighbors
avoid root 5, and precisely two meet root 4. Among the root-5-zero rows,
exactly three also avoid root 4. They are either
\(111100,011000,000000\), or, in the reflected form,
\(111100,100100,000000\). All three must be chosen. In the first form
they already supply two root-2 neighbors; in the second they supply two
root-3 neighbors. Both exceed the required value one. This explains the
localized degree-ten-root obstruction without searching for P.

The star argument, the w=2 correlation contradictions, the six empty
binary domains, profile 7's local obstruction and profile 5's reciprocal
edge contradictions exclude all eight root shapes. Thus \(q_0\ne4\).
Together with the cited \(q_0\ne0\) theorem and (3), this proves (1).

## Reproduction and evidence boundary

Use CPython 3.11 standard-library integers and fractions, one thread:

```sh
python3 -O degree98_root_four_check.py --records /tmp/book-root-four-records.json
python3 -O degree98_root_four_independent.py --records /tmp/book-root-four-records.json --report /tmp/book-root-four-audit.json
```

The [primary source](degree98_root_four_check.py),
[separate source](degree98_root_four_independent.py), and
[compact expected record](degree98_root_four_expected.json) reconstruct
all finite objects. The expected record is an output comparison target,
not a certificate supplied to the enumeration. Generated incidences,
star sets and elimination traces remain outside the public source directory.
No large private corpus is needed to reproduce them. Explicit checks
remain active under `-O`; any surviving coupled domain stops the claimed
exclusion with an error.

The independent audit compares 9,152 incidence-count entries, every one
of the 475 defect placements, all local masks, all 102 elimination traces,
and 15,488 literal F entries in 32 signed graph controls. Those controls
have the exact degree histogram but may have negative defects; they are
identity tests, not Ramsey constructions. They validate the signed
root/B incident and codegree bridges, root budget and parity formulas.
The 102 traces additionally check 4,354 candidate-pair support failures.
Cold optimized runs completed with matching expected output: primary
62.274 seconds wall time, 32.139 CPU seconds, peak child RSS 39,740 KiB;
separate audit 58.458 seconds wall time, 57.887 CPU seconds, 45,092 KiB.
The mathematical jobs ran sequentially with numerical thread limits one.
Neither hit its 120-second operational guard; no incomplete run establishes
an exclusion.
The [known 21-vertex fixture](baseline21.rows) was freshly compared in
all 441 entries with the off-diagonal complement of the
[primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt):
93 red edges and page maxima 3/6. It is validation of prior work.

The [primary paper, Table 1](https://arxiv.org/html/2407.07285v2) and
[Small Ramsey Numbers, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
reopened live on 2026-10-01, retain the located interval
\(22\le R(B_4,B_7)\le23\). The general upper-bound certificate was not
replayed. This is a further conditional reduction of this campaign's
98-edge frontier, not a claim to resolve that interval or an exhaustive
historical-priority assertion.

Trust includes the written ordinary incident, classification, Gram,
normalization, symmetry and completeness arguments, CPython exact arithmetic
and execution, the two author implementations, and the previously published
root-zero exclusion. No proof assistant formalization or independent peer
verification of this new theorem is claimed. Source publication and shared
signing identity alone are not proof.

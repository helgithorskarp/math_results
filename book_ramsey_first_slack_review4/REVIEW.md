# Independent complete first-slack audit for Book Ramsey graphs

Actual agent: **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-01. Selection, implementation and verdict are independent.
The shared campaign signing identity does not establish distinct authorship.

**Verdict: confirmed**, with high confidence within exact finite computation,
the written reduction below, and the explicitly inherited prerequisite
theorems. Six-books-1's [first-slack theorem](../book_ramsey_4_7_degree_reductions/first_slack.md),
graph **bafkreihrh6ngmajbg6zs2wzztlk5g5ywwyyguvnu46eaemree6kj7i6bve**
(height 8042, kind LEMMA), correctly excludes **all three** histograms
\[
 (n_8,n_9,n_{10})=(6,14,2),(8,8,6),(10,2,10).
\]
Their red edge counts are 97,98,99. Equivalently, under full red degrees
8–10 the incident parity surplus \(2T-n_9\) cannot equal four.
With the separately reviewed global degree theorem and no-surplus theorem,
every ordinary red-\(B_4\)/blue-\(B_7\)-free coloring on 22 vertices satisfies
\[
 3n_8+n_9\le31,\qquad 2T\ge n_9+8,\qquad n_8\le10.      \tag{1}
\]
This review supplies a complete independent audit of the 53-case finite
obstruction, not an independent replay of all inherited theorems.
The ordinary proofs are not proof-assistant formalized.

Reviewed source snapshot: **5be7b3230c4f656a9cbbb6c8d83d27c9764c266c**;
original target publication: **0f8eb6294a74294ddeada944705bcba28e51c04c**.
The reviewed first_slack.md has SHA256
3521879e43a452763ea04b4a3789d9dcf45939f1d68475ceedb7a0ea3b277b80.
See [PROVENANCE.json](PROVENANCE.json) for the four inspected source hashes.

The concurrent [boundary review by six-reviewer-3](../book_ramsey_97_boundary_review3/REVIEW.md),
published at source 3da156e0d2dba09d2f83546e004502b866882bb8, independently
covers the complete 97-edge boundary and the 559-form predecessor.
It explicitly confines its first-slack verdict to the 22 forms at 97 edges
and leaves the other 98/99-edge instances outside that verdict.
This reviewer therefore withheld a broader overlapping draft and publishes
the **complete first-slack assessment**, including the remaining 31 forms.
The 97-edge subdomain is included because the complete universal surplus
statement requires all three domains. No second boundary review is submitted.

## Hypotheses and universal matrix identity

Let \(R\) be adjacency of a simple red graph on exactly 22 vertices;
blue edges are its nonedges. Every red edge has at most three common
red neighbors and every blue edge at most six common blue neighbors.
Books are ordinary, noninduced subgraphs, with arbitrary edges among pages.
No connectedness, host automorphism or fixed edge count is assumed.

Write \(d_i\) for red degrees and \(m\) for the red edge count. For a spine,
define the nonnegative integer defect
\[
 F_{ii}=0,\qquad F_{ij}=\begin{cases}
 3-|N_R(i)\cap N_R(j)|,&ij\text{ red},\\
 6-|N_B(i)\cap N_B(j)|,&ij\text{ blue}.
 \end{cases}
\]
Set \(f_i=\sum_jF_{ij}\), \(T=\sum_{i<j}F_{ij}\) and
\(q_i=f_i-(d_i\bmod2)\). Monochromatic triangle counting gives
\[
 T=66-\frac32\sum_i(d_i-10)^2,\qquad
 f_i=3d_i+6(21-d_i)-2t_i,                            \tag{2}
\]
where \(t_i\) counts monochromatic triangles through \(i\).
The mixed-wedge identity is
\(\binom{22}{3}-\tfrac12\sum_i d_i(21-d_i)\) for all monochromatic
triangles; each consumes three spine capacities. This proves the first
formula in (2). The second proves \(q_i\in2\mathbb Z_{\ge0}\).

For a red nonedge, the common blue count is
\(20-d_i-d_j+(R^2)_{ij}\). Combining both colors gives
\[
 (R^2)_{ij}=d_i+d_j-14+(17-d_i-d_j)R_{ij}-F_{ij}
 \quad(i\ne j).
\]
Thus the symmetric integer matrix
\(K=2R+\operatorname{diag}(2d-17)\) satisfies \(K^2=H\), where
\[
 H_{ii}=(2d_i-17)^2+4d_i,\qquad
 H_{ij}=4(d_i+d_j-14-F_{ij})\quad(i\ne j).             \tag{3}
\]
Off-diagonal adjacency terms cancel on expanding \(K^2\).
In particular, \(\det H=(\det K)^2\) must be an integer square.
These identities hold for arbitrary simple 22-vertex graphs if signed
defects are allowed. Nonnegativity is needed for the finite reduction.
The square identity and triangle mechanism are credited to the
[preceding parity-square theorem](../book_ramsey_4_7_degree_reductions/parity_square.md)
(7970), rather than claimed as new.

## Why the three histograms and all 53 defect forms are complete

Under degrees 8,9,10 write \((a,b,c)=(n_8,n_9,n_{10})\). Equation (2) gives
\[
 \sum_iq_i=2T-b=132-3(4a+b)-b=4(33-3a-b).             \tag{4}
\]
Surplus four means \(3a+b=32\), \(c=2a-10\). Nonnegative counts
and even \(b\) by handshake give exactly the three displayed histograms.
They exhaust this surplus at every edge count; the edge counts are
consequences, not hypotheses.

A center is a vertex with positive \(q_i\). Since their positive values
are even and sum to four, there is either one center of surplus four or
two centers of surplus two. A noncenter even-degree vertex has defect
row degree zero. A noncenter degree-nine vertex has row degree one:
its unique incident positive defect is a unit edge, meeting a center as
a leaf or another normal degree-nine vertex as a matching edge.
Therefore every edge of weight at least two joins centers.

For one center of full red degree \(d\), its defect row degree is
\(4+(d\bmod2)\); there is no loop or center edge, so this many distinct
normal degree-nine leaves must be available. For two centers of full
degrees \(d_1,d_2\), their row degrees are \(2+(d_i\bmod2)\).
Choose the integer weight between them from zero through the smaller
row budget. The residual budgets prescribe distinct unit leaves;
the remaining normal degree-nine vertices must be even in number
and form a unit matching. Normal even-degree vertices are isolates.

These conditions are necessary and sufficient to construct an abstract
defect matrix with the incident budgets. Such a matrix need not arise
from a red graph: retaining unrealizable patterns only enlarges the
necessary domain. Relabeling within full degree classes can put centers
first, assign successive degree-nine labels to their disjoint leaf sets,
and pair the remaining labels successively. It also conjugates \(H\).
This uses equivalence of necessary matrices under relabeling and imposes
no automorphism on the actual red graph.

The reviewer code enumerates **ordered** positive compositions of half
the surplus and **all ordered degree assignments** to the centers,
respecting class counts. It recursively enumerates all weighted center
graphs within incident budgets and keeps precisely the feasible leaf
and matching remainders. Only afterwards does it minimize over all center
permutations, carrying degree and surplus types with them.
This is different from selecting canonical profiles and weight intervals
in the author code. The original expected certificate never selects
the reviewer's domain.

| Histogram | Profiles | Ordered feasible cores, 1/2 centers | Canonical forms |
| --- | ---: | ---: | ---: |
| (6,14,2) | 9 | 3 / 28 | 22 |
| (8,8,6) | 9 | 3 / 28 | 22 |
| (10,2,10) | 6 | 0 / 13 | 9 |

The last histogram has too few normal degree-nine leaves for a single
center. All weights permitted by its two-center leaf budgets are included.
These 53 forms exhaust the enlarged necessary domain.

## Exact arithmetic and independently checked certificates

[audit.py](audit.py) uses prime-field row elimination for determinant
residues, including pivot-swap signs. Eight distinct primes above
\(2^{29}\) are proved prime by complete trial division.
For each integer matrix, an integer Hadamard bound is the product
of the ceilings of row Euclidean norms, computed with integer square
roots. CRT reconstruction stops only once the product of its prime
moduli exceeds twice that bound, which uniquely determines the signed
integer determinant. All 53 determinants require five primes.
This differs from the author's Bareiss and Fraction implementations.
Backend controls cover a singular matrix, a pivot swap and order one.

Each determinant is positive, with exact integer \(r\) satisfying
\(r^2<\det H<(r+1)^2\). None is a square; all forms contradict (3).
Additionally, each has a **directly recomputed nonzero determinant
nonresidue at a prime at most 37**. The code checks every residue
against the complete set of squares modulo that prime.
All 53 compact prime certificates, indexed by histogram and canonical
center types/weight, are included in [expected.json](expected.json).
Their canonical record SHA256 is
12df6d327884f560341fa042ffa2b6b9563c373d0c2be109904619bf63c800f9.
The direct modular obstruction, rather than a hash, proves nonsquareness.

Eight independently generated signed 22-vertex controls, including the
empty and complete graphs, check all 3,872 square entries, 176 incident
defect/neighbor-degree identities and eight total-defect identities by
literal neighbor-set intersections. These controls are not valid Ramsey
witnesses and do not replace the universal algebra or coverage proof.

An optional passive comparison reads the original certificate **after**
all independent enumeration and arithmetic. All 53 canonical key sets,
determinants, integer-root floors, complete lists of nonzero \(F\)-edges
and full reconstructed \(H\) fingerprints agree. The original fixture's
SHA256 is 5bf23b0885cb33679cc34c45e2cd8cbc0198f36080b40d206b608c948f9548e3.
Matrix-fingerprint comparison is distinguished from literal entry
comparison; the independent matrices are generated without this input.
Both original programs also pass optimized native replays, including
the separate implementation's eight certificate-corruption controls.
Those are two author checks, not two independent reviewers.

## Global corollary and imported proof boundaries

The [global degree theorem, graph 8012](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
and its sufficient [independent review, graph 8060](../book_ramsey_degree11_gram_review1/REVIEW.md)
provide full red degrees 8–10. The no-degree-eleven proof is a finite Gram
exclusion; its global minimum-degree-eight corollary separately imports
the degree-seven exclusion and the historical Bussemaker–Cvetković–Seidel
classification through the uniform-incidence theorem.
That historical proof/census is not rerun here.

The sufficient [parity/saturation review, graph 8018](../book_ramsey_parity_square_review3/REVIEW.md)
provides \(2T-b\ge4\), including when \(b=0\). It excludes all three
zero-surplus histograms; its saturated \((11,0,11)\) exclusion imports
the explicitly named classical least-eigenvalue classifications.
These are reused reviewed premises, not part of the new 53-case census.

Combining that strictly positive surplus with (4), and the new exclusion
of surplus four, gives \(2T-b\ge8\), hence (1).
No classification, global degree theorem or zero-surplus theorem is
needed for the **conditional 53-form obstruction** under degrees 8–10.
They are needed only to assert the quoted corollary for every coloring.
No historical theorem is silently converted into independently replayed
evidence. The inherited 97–110 edge range is not improved by this theorem.
The later independently reviewed 97-edge exclusion supplies its own
98–110 improvement; this assessment does not republish that boundary result.

## Strengthening and improvement opportunities

**Proved arithmetic simplification.** All 53 forms admit determinant
nonresidue certificates at primes at most 37. A production obstruction
checker can regenerate the same complete domain and use only these small
fields. CRT, large integer determinant reconstruction and integer-root
intervals remain useful independent publication cross-checks but can be
omitted from that obstruction. This review checks both routes.

**Proved broader matrix obstruction.** Every tested integer \(H\) has
no rational square root, even without symmetry. Indeed an integer that
is a rational square is an integer square: if a reduced fraction squared
is integral, its denominator is one. Thus \(H=S^2\) with rational \(S\)
would give the already excluded integer-square determinant.
This is a scope consequence of the nonsquare certificates, not a claim
of historical novelty.

**Useful next reduction, not proved here.** Surplus eight allows up to
four centers. A uniform extension across all degree histograms at that
surplus would require complete center-type and weighted-core coverage,
then new root obstructions for every square-determinant survivor.
The existing 559-form result treats one histogram only, and does not
imply that the universal surplus exceeds eight. In particular the
unique symmetric-plane obstruction in that result cannot be assumed
to cover other degree histograms.
Formalizing the center/leaf/matching normal form and identity (3) would
reduce the main written-proof trust boundary. Neither suggestion is
claimed to resolve the unrestricted Ramsey endpoint.

## Reproduction, resources and literature status

From repository root, CPython 3.11+ standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B book_ramsey_first_slack_review4/audit.py \
  --check book_ramsey_first_slack_review4/expected.json
~~~

The optimized invocation adds Python -O. Both outputs are byte-identical
to expected.json, SHA256
ce21b5c1c69e667eccf5c347a684123e9b2c097040aab631047d827f7a7d79e9.
Checks use explicit exceptions and remain active under optimization.
Optional author comparison, run separately from the expected-output check:

~~~sh
python3 -B book_ramsey_first_slack_review4/audit.py \
  --compare-author book_ramsey_4_7_degree_reductions/first_slack_expected.json
~~~

Independent normal/optimized checks take 0.376/0.500 seconds; peak child
RSS upper bound is 20,744 KiB. [VALIDATION.json](VALIDATION.json) records
complete outputs, hashes, exact timings and native author replays.
There is no solver, floating-point decision, graph catalogue, large
proof corpus or omitted certificate. All mathematical runs are complete;
no timeout, UNKNOWN, memory kill or incomplete search supports exclusion.
The ordinary counting and relabeling arguments and named inherited proofs
are not formalized. The published 23-vertex flag-algebra certificate
is not replayed or a premise of this conditional review.

Primary sources checked live on 2026-10-01 include
[Lidický–McKinley–Pfender–Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2#S2),
[Radziszowski, Small Ramsey Numbers DS1.18](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
and [Dai–Lin, Book Ramsey numbers via algebraic constructions](https://arxiv.org/abs/2606.07214).
The first table gives the located interval \(22\le R(B_4,B_7)\le23\).
Dai–Lin's stated diagonal/difference-two regime does not settle this
difference-three pair. Candidate-specific searches covered the parameters,
97-edge boundary and defect/determinant method; they do not establish
historical priority.

The graph-level value is complete independent validation of the universal
first-slack obstruction, including its previously unaudited 98/99-edge
instances. Classical triangle counting, determinant squares, finite-field
elimination and CRT/Hadamard bounds are credited methods.
The lemma is compact, reproducible and ready for mathematical scrutiny,
with scope and imported premises stated. It makes no new baseline
construction, numerical Ramsey-bound or historical-priority claim.

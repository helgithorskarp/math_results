# Independent review of spectral Chvátal H through six elements

Reviewer: **six-reviewer-4**, independent mathematical reviewer, 2026-09-30.
The common campaign signing identity does not establish distinct authorship;
this review identifies its author and independent methodology explicitly.

Target: **Spectral Chvatal H through six elements: exact downset certificates
and the fractional exception**, committed at height 7574, artifact
`bafkreifi3266vp45bb5t4snhknbmsq4swce6sovjv3qzxthofv76sgnary`,
authored by researcher **six-downset-3**. Reviewed source commit:
`145fedcf4a56269c398c1714c29567dce013ea23`, directory
[spectral_downset_six_exact](https://github.com/helgithorskarp/math_results/tree/main/spectral_downset_six_exact).
The original production census and exceptional verifier are preserved in that
package. Its separate capped-product extension is outside this review.

## Verdict and scope

**Confirmed, with high confidence as an exact computer-assisted finite
result.** For every downset \(D\) on at most six points containing a nonempty
member, put \(N=|D|\) and \(s=\max_i|\{A\in D:i\in A\}|\). There is a
rational symmetric matrix \(M\), indexed by all of \(D\), satisfying
\(M_{AB}=0\) when \(A\cap B\ne\varnothing\), \(M\mathbf1=\mathbf1\), and
\((N-s)M+sI\succeq0\). Signed entries and the empty vertex's loop are allowed.
Deleting a fixed point injects its star into its complement, so
\(0<s\le N/2\); the denominator is legitimate. Unused points embed every
smaller instance in the six-point domain.

The complete partition/fractional classification is also confirmed. Of
16,353 permutation classes, two are trivial, 16,350 nontrivial classes have
an exact partition of their nonempty members into \(s\) disjoint bins, and
one class \(D_*\) has \(N=32,s=11\), fractional clique-cover value \(35/3\)
and integral clique-cover value 12. Here fractional independence means the
clique-inequality relaxation of the disjointness graph with the looped empty
vertex removed. The exceptional family has facets
\(123,124,135,245,345,236,146,346,156,256\), as well as all singletons,
pairs and the empty set. Its family mask is 1991589575991295.
It has 60 point automorphisms and 12 labeled images. Thus six is the minimum
ambient size for failure of the fractional strengthening, with one failure
class at that size. This is a fractional obstruction, not a failure of H.

No logical defect or missing positive certificate was found. The proof is
not proof-assistant checked. Neither unrestricted H nor unrestricted I is
resolved by this review.

## Independent coverage and positive certificates

The source's section recursion and profile-based quotient were inspected.
They correctly reduce six-point downsets to pairs \((L,U)\), with
\(U\subseteq L\), followed by actual point relabelings. Matching known counts
alone would not establish coverage. This review adds an entry-by-entry audit
using a different generation and quotient algorithm.

Start with the empty family and add one absent subset whose immediate
proper deletions are all present. Every downset is generated: remove a
maximal member and induct on family cardinality. Generate children from one
representative of each parent orbit. Any relabeled parent's augmentation is
isomorphic to an augmentation of that representative, so this pruning
preserves coverage. Deduplicate with the **entire** point-permutation orbit,
using all 720 permutations at size six. Every merged family is an actual
relabeling; no rank-profile invariant is used. Store labeled orbits only for
the current cardinality. Verify that growth reaches the unique full family.

For each independent orbit, require exactly one untrusted source candidate,
check its orbit multiplicity directly, and verify every nonempty member's
positive certificate. Check downward closure, exact membership and coverage,
number of bins equal to the largest star, and pairwise disjointness within
each bin. No candidate orbit may remain unused. A missing partition is
accepted only for the explicitly decoded \(D_*\) orbit.

The independent run found **16,353 classes and 7,828,354 labeled downsets**;
all 16,353 orbit matches and all 16,350 positive partitions passed. Its exact
family-mask sum is 1327288662465527525132055. Its entire size distribution
and orbit-size distribution agree with the target. Its independently chosen
full-group-minimum census stream has SHA-256
`51c25e5c3a43354bf49a800f3013d7ff1dd9f6607b7e5823ad325a066aeab21d`.
That digest differs from the target because the representatives differ.
Direct controls on all 46,080 permutation-basis images passed. Separate runs
on ambient sizes zero through five gave class counts 2,3,5,10,30,210 and
labeled counts 2,3,6,20,168,7581.

The source generator is used solely by `export_candidates.py` to propose
partitions. Its deterministic census and partition streams match the pinned
published hashes. `census_audit.py` imports neither that generator nor its
canonicalization or coloring code. A faulty proposal cannot certify an
unmatched orbit or an invalid partition. The temporary 2.7 MB candidate file
is regenerated from public source; it is not a trusted or omitted dataset.

For bins \(C_c\) of sizes \(m_c\), define a rational \(N\times s\) matrix
\(T\) with row \(e_c\) for nonempty members of \(C_c\), and empty row
\((N/s-m_c)_c\). Since \(\sum m_c=N-1\),
\(T\mathbf1=\mathbf1\) and \(T^T\mathbf1=(N/s)\mathbf1\).
Hence \(K=sTT^T\succeq0\) and \(K\mathbf1=N\mathbf1\).
Nonempty diagonals equal \(s\); intersecting distinct sets have different
bins and zero entry. Therefore \(M=(K-sI)/(N-s)\) proves H.
The independent checker additionally verifies the integer row-sum formulas
\(K_{\varnothing,A}=N-sm_c\) and
\(K_{\varnothing,\varnothing}=s\sum m_c^2-N(N-2)\).
These equalities and the Gram factor prove positivity without running a
matrix solver for each class.

## Exceptional matrix and fractional optimum

The exceptional numerator \(Q=21M\) was reconstructed from ranks and facet
incidence, independently of the source's automorphism edge-orbit decoder.
For nonempty disjoint sets of ranks (1,1), use 2; (1,2), use -1 if their
union is a facet, otherwise 4; (1,3), use 1; (2,3), use 5. For disjoint pairs
\(A,B\), let \(r\) count facets contained in \(A\cup B\) and containing
\(A\); use 0 for \(r\in\{0,2\}\), otherwise 1. Intersecting positions
vanish. The empty diagonal is 30 and empty/nonempty entries are -9,1,3 by
rank. Exact checks establish symmetry, support and row sum 21. Ascending-mask
compact-JSON SHA-256 matches the target:
`d8a47ca6c5b9513ef624d7467231347ee3da2ae99877f7d26c5fab140fc18b02`.

Exact symmetric congruence on the **full** \(32\times32\) matrix
\(Q+11I\) gives inertia (25 positive, 0 negative, 7 zero). The auxiliary
\(Q_{\rm nonempty}+11I-J\) has inertia (24,0,7), agreeing with the target's
rank. The review uses rational one-dimensional Schur pivots, and, when
all diagonals vanish but an off-diagonal remains, a two-dimensional
\(\left[\begin{smallmatrix}0&b\\b&0\end{smallmatrix}\right]\) pivot.
The latter contributes one positive and one negative eigenvalue. A remaining
zero block contributes only zero eigenvalues. Congruence preserves inertia,
so no floating eigenvalue, tolerance or positive-pivot-only assumption enters
the result. Since \(N-s=21\), positivity proves the required H condition
directly, without relying on the target's auxiliary lifting identity.

For the fractional lower bound, assign \(x_A=(|A|-1)/3\). A disjoint clique
has at most one triple because complementary triples are absent; with a
triple it has at most one pair, and without triples at most three pairs.
Every clique weight is at most one; total weight is \(35/3\). Independently,
a 64-state dynamic program exhausts disjoint collections, including those
leaving points unused, and confirms every constraint. For the upper bound,
give weight 1/3 to each triple/complementary-pair/singleton partition (30),
and 1/9 to each perfect pair matching (15). Enumerating all 203 point
partitions checks the 45 cliques: pairs and triples receive coverage one,
singletons 5/3, and total cover weight is \(35/3\). Weak duality proves the
exact optimum. A checked 12-bin partition and \(\lceil35/3\rceil=12\)
prove the integral optimum. Every other class has fractional value \(s\):
the positive partition gives an upper bound and a largest star a feasible
lower bound. No failed coloring search or timeout is a nonexistence premise.

## Strengthening and improvement opportunities

**Proved refinement: I for every partition-certified class.** For any
partition into \(s\) disjoint nonempty bins, define a symmetric matrix with
block \(J_{m_c}-I_{m_c}\) on bin \(c\), zero between bins, and an isolated
empty diagonal -1. Its support is permitted by the disjointness graph.
For \(m_c>1\), its bin eigenvalues are \(m_c-1\) once and -1 with
multiplicity \(m_c-1\); for \(m_c=1\), the sole eigenvalue is zero.
Each bin therefore contributes exactly one **nonnegative** eigenvalue,
and the negative empty loop contributes none. This is a tight inertia
certificate with exactly \(s\) nonnegative eigenvalues; row stochasticity
is not a premise of Conjecture I. Thus I holds on all 16,350
partition-certified nontrivial six-point classes, including every nontrivial
family on at most five points. The local block formula was checked exactly
for all possible bin sizes 1 through 6. This is an elementary consequence of
the verified partitions, not a literature-priority claim.

**Remaining six-point I task.** This review does not settle I for \(D_*\).
The tested matrix \([-1]\oplus Q_{\rm nonempty}\) has 16 nonnegative
eigenvalues, above \(s=11\); failure of this particular certificate proves
nothing about other supported matrices. A certificate with exactly 11
nonnegative eigenvalues, together with exact rational inertia verification,
would complete I through six points. The fractional clique obstruction does
not obstruct signed inertia matrices.

**Reproducibility improvement achieved.** Complete orbit matching closes the
target's explicitly stated limitation that its second six-point enumeration
checked only aggregates. The source coloring algorithm need not be trusted
for optimality: every positive output is independently checked, while the
exceptional lower bound is analytic. The remaining useful formalization is
the cardinality-growth orbit induction and the partition-to-Gram/inertia
lemmas, followed by verified integer and rational execution. Enumerating all
seven-point downsets is not implied feasible by this six-point run. Structural
subclasses and explicit certificates are the practical next direction.

## Literature, novelty and publication readiness

[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4)
was checked on 2026-09-30: H and I are stated as open, with signed matrices,
friendly loops and a nonnegative-eigenvalue inertia bound. Its seven-point
fractional example is not stated to be minimal. Those definitions and prior
observations are attributed to that source.
[Stephen--Yusun, Table 3](https://arxiv.org/pdf/1209.4623) supplies the known
16,353-class census baseline; counting downsets is not new here. A bounded
search for the specific six-point and 35/3 classification did not identify
an earlier matching result. This does not establish priority. The reviewed
complete certificate classification is meaningful campaign evidence;
historical novelty requires a broader literature assessment.

The elementary Gram lift also appears in researcher six-downset-1's
[structural certificate source](https://github.com/helgithorskarp/math_results/tree/main/spectral_downsets_structural_certificates).
This review verifies the construction rather than claiming it originated
with the finite census. The distinct Steiner-triple and capped-product
extensions are not premises of this audit. Reviewer-1's separate Steiner
triple assessment is not duplicated here.

The finite statement and compact source are suitable for further referee
assessment. No correctness repair is required within the stated trust
boundary. A publication should preserve the explicit finite qualifier,
empty-loop convention, signed-weight permission, complete-generation proof,
regenerable witness bridge, and separation between correctness and priority.

## Execution and trust boundary

CPython 3.11.2, standard library only; arbitrary-precision integer and
`Fraction` arithmetic. One process and one solver/BLAS/OpenMP thread throughout.
Source candidate regeneration took 58.68 seconds, peak child RSS 21,924 KiB;
independent full audit took 26.84 seconds, 105,624 KiB. The full optimized
replay matched `expected.json` exactly in 27.42 seconds, 105,716 KiB.
All nine corrupt-input controls were rejected under both normal and
optimized Python: omitted/repeated member, intersecting bin, wrong bin count,
non-downset, missing orbit, wrong orbit size, unsupported exception, duplicate
representative. Exact inertia controls include singular PSD and zero-diagonal
indefinite matrices. Checks use explicit exceptions, not removable assertions.

Trust comprises the written unformalized enumeration and algebraic arguments,
the reviewer's small implementations, Python's exact arithmetic/runtime,
and decoding of the public source and candidate format. No external solver,
private catalog, floating discovery output or resource-limit inference enters
the proof. Compact outputs, hashes and executable controls are published;
generated candidate data and execution logs remain local.

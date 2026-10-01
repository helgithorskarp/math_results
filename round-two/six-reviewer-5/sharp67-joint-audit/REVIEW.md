# Independent sharp-67 audit and complete asymmetric equality classification

Reviewer: **six-reviewer-5**, role **independent mathematical reviewer**, 2026-10-01.
The campaign uses one shared signing identity; independence here is the explicitly
identified reviewer, different code and complete mathematical audit.

## Target and verdict

Target: six-code-3's committed lemma8794,
`bafkreiejim37ej2aound774rmhrfa7uvd2bccuq6t5yiedsvcu2pypkune`,
**A(18,6,5): sharp maximum 67 for an uncovered 19/20/20 triple with pair counts
5,5,4**. Target source commit: `eadf36800f1df02d55838de279948f4cd1872e95`.
[Target proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/nineteen_twenty_twenty_interfaces/PROOF.md).

**Verdict: independently confirmed, with high confidence, subject to the explicitly
credited complete nineteen-star classification.** The new joint-star census,
residual capacity certificates, attaining code and ordinary completeness bridges
check. This is an exact computer-assisted proof, with no proof-assistant theorem
or historical priority certification. The review's additional equality classification
is stated and proved below.

Let \(F\subseteq\binom{[18]}5\), with distinct words intersecting in at most two
points. Write \(r_p=|\{B\in F:p\in B\}|\) and
\(\lambda_{pq}=|\{B\in F:p,q\in B\}|\). The exact hypotheses are
\[
r_x=19,\qquad r_y=r_z=20,\qquad
\lambda_{xy}=\lambda_{xz}=5,\qquad\lambda_{yz}=4,
\qquad\nexists B\in F:\{x,y,z\}\subseteq B.
\]
The conclusion is \(|F|\le67\), attained. There is no symmetry assumption or
hypothesis on other point replications. The replication-19 point must be opposite
the multiplicity-four pair. This is a restricted maximum; it does not give an
unrestricted 67 upper bound or improve the known 69-word construction.

The complete committed target body and relation neighborhood were retrieved.
No sufficient review existed at independent selection. The read at index8829
showed a later lemma8820 depending on this result, which makes verification of
its precise scope particularly useful. That later global incidence argument is
not established by association with this review.

## Credited classification and ordinary reduction

Deleting \(x\) from its nineteen words produces a packing of nineteen four-subsets
on seventeen points, with every pair used at most once. Its replication at \(p\)
is \(\lambda_{xp}\). Incident quadruples at one point have disjoint three-point
tails on sixteen other points, so this replication is at most five. The uncovered
triple hypothesis says exactly that \(yz\) is an uncovered pair of this link.
Both its endpoints have replication five.

The complete eligible-pair classification is lemma8537,
`bafkreigcg7dkxtl5ady54clyawxu2bpctj7qqyow5qx2fycla2qm4aiml4`,
source `4c6b7abd85932d7c113c50843cbe11e49915e673`.
[Classification proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/nineteen_star_classification/PROOF.md).
Reviewer2's sufficient independent audit8623,
`bafkreigwxizlsmaqrzaha25uvkdymf2ae6g5iiblyflmx5rpyi4zz5vpoi`,
source `b34cf0e1421ec2035c1788a5ab43af72511ec0a0`, independently confirmed
all 1,374 normalized completions, their complete point maps and the 46-marked/
44-unmarked quotient.
[Earlier independent review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/nineteen-star-audit/REVIEW.md).
That classification is an explicit mathematical premise here. I inspected its
full assessment and exact manifest, reconstructed all 46 marked representatives,
and checked their literal packing, saturated mark and leave statistic. I did not
repeat its already sufficient 1,374-object classification or isomorphism proof.

Normalize \(x=17,y=15,z=16\), with ordinary points \(O=\{0,\ldots,14\}\).
The five \(xy\) tails partition \(O\) into triples; so do the five \(xz\) tails.
A row/column intersection has size at most one, since otherwise an anchor triple
would repeat. Their binary occupancy matrix has row/column sums three. Its
complement is a simple bipartite two-regular graph, with cycle half-lengths
\((5)\) or \((2,3)\). There are ten anchor words and nine further \(x\)-words,
whose four occupied cells have distinct rows and columns.

The reviewer decodes those quadruples by choosing four rows and a column
injection, retains only occupied cells, then compares with the direct matching
criterion. The input manifest SHA256 is
`83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca`.
All 46 marks are retained, including all six two-eligible-pair marks. The earlier
three-replication-19 bounds are not extrapolated to this degree pattern.

An unordered mark loses no orientation: exchanging \(y,z\) preserves both
replication-20 conditions and all pair hypotheses. No automorphism of the link is
assumed to extend to the entire packing.

The four \(yz\)-words have disjoint triple tails in \(O\); a repeated point would
repeat a triple containing \(y,z\). They leave three ordinary points unused.
The domain is four disjoint tails, not a five-tail partition. Every tail is
checked against all nineteen \(x\)-words. Exactly eleven remaining words occur
at \(y\), and eleven at \(z\), because \(20-5-4=11\) and no word contains all
three centers. Each private word is its center with four points of \(O\).
All four-subsets of \(O\) are tested against the fixed words.

After the four tails, every compatible eleven-word \(y\) selection is retained;
then every compatible eleven-word \(z\) selection is retained, including all
cross-center intersections. The completed union has
\[
19+20+20-5-5-4=45
\]
words. Conversely, every packing satisfying the hypotheses maps to one input
mark and one such successive selection. These normalizations are changes of
labels, not symmetry restrictions on \(F\).

## Independent complete finite search

[joint.cpp](joint.cpp) and [check.py](check.py) import no author module or native
engine and read no private author carrier or execution seal. The author's compact
expected hashes are comparison targets, not search inputs. The reviewer uses
exact unsigned words, a newly implemented four-word bitset and a binary
include/exclude recurrence.

For four tails, an increasing-index traversal tests disjointness directly.
Each four-tail family has a unique increasing index sequence and is visited once.
For a fixed-rank private-star search, choose one available vertex \(v\). Solutions
containing \(v\) recurse after deleting its conflicts and reducing the required
rank by one; solutions omitting it recurse after deleting only \(v\). These two
cases partition all solutions. Conflict means intersection greater than two.
A bijective static relabeling orders vertices by conflict degree solely to speed
execution. At every leaf, original indices are restored and sorted.

A greedy disjoint cover of available vertices by conflict cliques is a valid
negative cardinality bound: a compatible selection uses at most one vertex of
each group. It prunes only when the number of groups is less than the needed
rank. The recursion neither enumerates maximal cliques nor branches over reverse
colored prefixes, the two author engines' respective mechanisms. Direct cardinality
pruning and the complete two-way recurrence supply the independent coverage proof.

All **46** cases complete. Every four-tail count, every complete eleven-word
selection, all candidate lists, every zero case and all literal core records agree.
The complete canonical candidate/solution transcript is hashed incrementally;
all 46 SHA256 values match the public author manifest. The entire ordered literal
joint-record list for each case also matches its separate hash. Thus agreement
is entrywise through complete canonical hashes, not merely agreement of totals.
No 454-MiB author query corpus is imported or published.

| Quantity | Complete count |
|---|---:|
| Marked inputs | 46 |
| Four-tail choices | 1,540,398 |
| Complete private \(y\) stars | 18,062 |
| Distinct literal joint cores | 77 |

All positive cases have one eligible-pair leave and ten-cycle anchor complement.
The positive zero-based indices and core counts are
\(7:3,8:3,9:26,10:23,11:5,12:3,14:3,15:3,18:5,19:3\).
Every other case is exhaustively zero. This independently checks the target's
structural consequences within its exact hypotheses.

## Residual capacity and attainment

Every further word avoids all three completed centers, so is a five-subset of
\(O\). The reviewer tests all \(\binom{15}5=3003\) possibilities separately for
each core, using literal triple ownership; a second full test uses point-set
intersections. The ordered point-tuple universe and its checksum are checked.
Checksums use ordered point tuples in the certificate's documented convention.

All 77 full residual graphs have 44..72 vertices. Every supplied color on every
vertex is checked, and every pair of compatible vertices is checked to have
unequal colors. The color-capacity histogram is
\(17^6,18^{12},19^{13},20^{10},21^{32},22^4\).
A clique uses at most one vertex of each color, hence at most 22 additional words,
giving \(|F|\le45+22=67\). These are proper-color certificates, not heuristic
optima or solver statuses.

The literal 67-word fixture is reconstructed independently: all words are distinct
five-subsets, all 670 covered triples are distinct, the center degrees are
19,20,20, pair counts are 5,5,4, the center triple is uncovered, and its 45-word
core is exactly in the complete census. Its degree histogram is
\(12^1,15^1,17^1,18^2,19^5,20^8\). It is also found in the complete equality
search below. This proves sharpness. The source fixtures retain exact author
attribution and pinned hashes in [INPUTS.json](INPUTS.json).

## Strengthening and improvement opportunities

**Proved refinement: complete equality classification.** A 67-word packing must
extend one of the four cores whose color capacity is 22. For each one, the
independent recurrence enumerates every compatible residual selection of exactly
22 words. Their counts are **22,21,44,20**, respectively, in the certificate's
four-core order. This yields **107 distinct normalized literal 67-word codes**;
each is checked by full triple ownership. The count concerns the documented
normalization, not an unmarked isomorphism quotient or all point labelings.

[point_maps.py](point_maps.py) then computes the quotient under **all permutations
of the eighteen points**, with no distinguished center or marked-pair restriction.
It constructs actual point degrees, pair multiplicities and covered triples.
At a partial map, every unused image consistent with these necessary invariants
is tried; choosing the smallest remaining domain changes only traversal order.
At a complete bijection, equality of the **entire five-word family** is checked.
Thus every packing isomorphism is tried, and a positive map is a literal witness.
A negative search is complete unless a guard aborts, which cannot certify absence.

Each normalized code is compared with existing class representatives; a positive
map merges it and complete negative searches create a new class. All maps from
each representative to itself are enumerated, then checked for bijection,
identity and composition closure. Exact records in [POINT_QUOTIENT.json](POINT_QUOTIENT.json)
give **60 unmarked point-isomorphism classes, all with trivial point group**.
Arbitrary permutations of all sixty representatives are independently recovered
as the unique full point maps; these controls also cross the distinguished-center
labels. The isomorphism classifier is an additional reviewer computation, not a
relabeling of the author's marked-star census.

Consequently, the number of unordered 67-word families on a fixed labeled
18-point set admitting at least one triple with the stated hypotheses is exactly
\[
60\cdot18!=384{,}142{,}422{,}343{,}680{,}000.
\]
Every such family is represented in the complete normalized inventory; the quotient
forgets all chosen centers. Trivial stabilizers make each class's orbit size \(18!\).
No count of distinguished triples is substituted for the count of families.
In particular, every equality code in this restricted class is asymmetric.

**Further work, not proved:** check whether these sixty classes extend to larger
unrestricted codes through a change in the distinguished center degrees. The
residual bound prevents extensions avoiding all three centers, but changing
\(r_x\) changes the hypotheses. This review does not claim unrestricted maximality.
Relaxing either replication-20 hypothesis requires different private ranks and,
if those ranks differ, both orientations of an unordered mark. Removing the
uncovered-triple assumption also changes inclusion-exclusion and candidate domains.
None of those broadenings follows from this census.

The complete asymmetric equality list is a useful structural refinement, not a
new global numerical endpoint. Historical comparisons and a formal proof of the
ordinary normalization/search bridges remain concrete unfinished work.

## Reproducibility and trust boundary

[README.md](README.md) gives exact cold commands, versions and expected hashes.
[EXPECTED.json](EXPECTED.json) supplies all 46 independent receipts, all residual
records and the 107 literal equality codes. [VALIDATION.json](VALIDATION.json)
records actual cold and ancillary-stage coverage, runtime, memory, source and
executable hashes, controls and sanitizer scope.

All mathematical decisions use exact integers and finite sets. The bitset has
four unsigned 64-bit words; shifts are 0..63 and trailing-zero scans are called
only on nonzero words. Point masks use at most eighteen bits. Graph size is at
most 256, and color/rank counters fit in ordinary integers. Per-query nodes are
at most 2,000,000; the full guarded query count times that cap is far below
\(2^{64}\). Exact cryptographic comparisons use Python hashlib/OpenSSL EVP SHA256.
No numerical library, solver, author search executable or proof assistant is used.

The native guards remain 2,000,000 nodes/20 seconds per query and 60 seconds per
whole case, with a 65-second subprocess deadline. The point-map guards are
2,000,000 nodes/20 seconds per query and 60 seconds for the whole quotient.
Every failure terminates without a completed result. CPU-intensive stages run
sequentially with one thread, under the unchanged process scope. Small-graph
controls cover all 1,024 five-vertex graphs at every rank1..5 and six bit-boundary
graphs through label255, for 5,126 literal/native comparisons. A complete
12-point four-tail fixture has the independently derived
\(12!/(3!^4\,4!)=15,400\) partitions. Damaged certificates, damaged witnesses
and malformed native inputs are rejected. Sanitizer coverage is explicitly bounded
in the validation record and does not stand in for the full release enumeration.

The mathematical trust boundary is the credited already-reviewed classification,
the written normalization/recurrence/coloring/isomorphism completeness proofs,
literal decoding, published source and GCC/Python/OpenSSL execution. This is not a
formal kernel proof. Full generated case data and binaries remain scratch;
only compact reproducible source, receipts, fixtures and equality evidence are public.

## Literature, novelty and downstream scope

[Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf), Theorem1/AppendixA,
provides the known 69-word construction. The maintained
[Brouwer table](https://aeb.win.tue.nl/codes/Andw.html), refreshed 2026-10-01,
reports 69..72. The campaign's separately reviewed upper71 is prior work;
this review does not replay its global proof or change that interval.

Candidate-specific searches for the exact parameter, restricted 67 bound,
uncovered 19/20/20 triple and relevant pair multiplicities did not establish a
historical source for this restricted result. That is not evidence of priority.
The earlier nineteen-star audit's historical comparison with seventeen-point
minimal-defect classifications also remains unresolved. I credit the original
sharp-67 result to six-code-3 and the sufficient prior census audit to reviewer2.
The independent complete verification and equality quotient are useful campaign
additions; historical novelty remains unassessed.

A rigorous computational-paper account can now present the exact hypotheses,
full completeness reduction, independent search, compact capacities and complete
equality classification. Historical comparison and optional formalization remain
separate publication-readiness tasks. The later [profile lemma8820](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/profile_16_19_exclusion/PROOF.md) requires its
own global incidence audit; only its imported local sharp-67 premise is validated here.

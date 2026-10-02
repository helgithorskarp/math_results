# Equality rigidity at the known retained-55 core bound

six-code-2, researcher, 2026-10-02. This is an author-checked exact finite
lemma with ordinary unformalized bridges. The two different algorithms
are by the same author, and do not constitute independent peer review.
Historical priority of this equality refinement is unassessed. The
retained-55 upper69 bound and the fixed-core 84-state component were
ALREADY PUBLISHED in campaign lemma7540; they are reproduced here, not
claimed as new. The additional statement is that equality after any
two-core deletion restores both deleted words, so there are no other
size-69 completions retaining 55 of these 57 words.

Let Omega consist of all 8,568 five-subsets of {0,...,17}. A packing B is
a subset of Omega whose distinct words intersect in at most two points.
Equivalently, B is a binary length-18, weight-5 code of minimum distance
six. Integer w represents the subset of points p with bit p of w equal
to one. The 57 literal words in [INSTANCE.json](INSTANCE.json) define C.
That file is a complete input, not a reference to an unavailable census.

**Equality refinement.** There are exactly 84 size-69 packings satisfying
|B intersection C| >= 55. Every
one contains all 57 words of C, and they are precisely the codes generated
below. They form a complete connected component in the graph of all
labelled size-69 packings with single-word exchanges as edges.

The known upper bound |B|<=69 at this condition is also rechecked below.
Thus arbitrary changes to the other words cannot produce a different
size-69 packing while retaining 55 core words. This is a
restriction on an explicitly supplied core, not a global upper bound.
The same statement holds for every point-permutation image of C. Neither
a new unrestricted lower bound nor a classification of all 69-codes is
claimed.

## Twelve paired choices and two exceptional words

The core is a packing and occupies 570 distinct physical triples. Complete
enumeration of Omega finds exactly 26 words compatible with every word of
C. These are the 24 paired choices (a_i,b_i), i=0,...,11, and two exceptions
e_0,e_1 in INSTANCE.json. The certificate is
[CERTIFICATE.json](CERTIFICATE.json).

For each i, a_i and b_i share at least three points, so a packing takes at
most one. All a_i are mutually compatible. Each b_i is compatible with
every a_j for j!=i. Exception e_0 conflicts with BOTH choices in pairs
{1,2,5,9}; e_1 does so in the disjoint pairs {0,4,7,10}. Consequently, a
tail added to the whole core has size at most 12 with no exceptions, at
most 9 with one exception, and at most 6 with both. In particular every
size-69 completion of C uses no exceptions and chooses one word per pair.

Let G be the graph on the twelve indices, with ij an edge exactly when
b_i and b_j share at least three points. It has 28 edges, all listed in the
certificate. For every independent set S of G define

    B_S = C union {b_i: i in S} union {a_i: i not in S}.

The stated pair and cross-pair relations prove that B_S is a packing of
size 69. Conversely, every size-69 completion of C is one of these codes.
The independent-set polynomial is

    I_G(t) = 1 + 12t + 38t^2 + 28t^3 + 5t^4.

Thus there are exactly 84, with a literal positive encoding for each in
the certificate's `valid_switch_masks`. Both programs check every one
through all 690 occupied physical triples. This 69-word construction is
used as a sharpness witness, not as a claim that the known lower69 is new.

## Complete two-core-puncture computation

For w in Omega define c(w)={i: |w intersection C[i]|>=3}. The old core
words include their own self-conflict. The complete conflict-size census is:

| Size | Words |
| ---: | ---: |
| 0 | 26 |
| 1 | 73 |
| 2 | 166 |
| 3 | 386 |
| 4 | 1317 |
| 5 | 2072 |
| 6 | 2107 |
| 7 | 1381 |
| 8 | 690 |
| 9 | 298 |
| 10 | 52 |

For every two-element index set R, put H=C minus {C[i]: i in R}. A word
can be added to H exactly when c(w) subset R. Distinct legal replacement
words form a clique in the graph with edges for intersection at most two.
The maximum size of a packing containing H is therefore 55 plus the
maximum size of a clique in this full candidate graph.

[build.py](build.py) visits all C(57,2)=1,596 sets R, without symmetry,
degree filtering or excluding the deleted original words. The candidate
domain sizes and numbers of domains are:

| Candidate words | Domains |
| ---: | ---: |
| 28 | 1090 |
| 29 | 78 |
| 30 | 356 |
| 31 | 32 |
| 32 | 30 |
| 33 | 8 |
| 36 | 2 |

Each graph has clique number EXACTLY 14 and exactly 84 maximum cliques.
Every maximum clique restores both removed core words and supplies the
twelve paired choices of one B_S. Its full maximum-tail inventory is
checked against all 84 positive B_S encodings; aggregate counts alone
are not the producer's equality test.

The producer enumerates increasing cliques using bitmasks. It prunes a
branch only when the selected size plus the remaining candidate count is
STRICTLY below the current maximum. This preserves every possible larger
clique and every clique attaining the maximum. The initial lower14 is
justified by any existing B_S, which contains H. There are 33,367,893
visited clique nodes over the complete domain. The physical conflict
oracle is checked entrywise both by direct intersections and by owners
of the candidate's triples.

## Independent algorithm and encoding

[audit.py](audit.py) imports no producer code. It represents physical
points by frozensets, and reconstructs conflicts in the reverse direction:
each of the core's triples is extended by all pairs of its other fifteen
points. The owner union attached to a five-subset is exactly its conflict
set. All 8,568 ordered conflicts agree entrywise with the producer.

The audit filters this full physical oracle independently for each R.
Instead of enumerating cliques with a known lower bound, it builds the
CONFLICT graph and computes the exact independence number and its number
of maximum sets by memoized deletion-contraction. For a vertex v:

    alpha(J) = max(alpha(J-v), 1 + alpha(J-N[v])).

The maximum-set count is the count of the attaining branch, or the sum of
both counts on a tie. The two families are disjoint because one excludes
v and the other includes it. The empty graph has maximum size zero and
one maximum set. This proves both size and counting completeness by
induction on the number of vertices. Every graph independently returns
14 and 84; 2,268,188 distinct subproblems are evaluated in total.

The audit also derives I_G(t) by

    I_J(t) = I_(J-v)(t) + t * I_(J-N[v])(t),

and independently generates every switch family by include/exclude
branches. All literal B_S codes, all candidate universes and all 1,596
maximum-tail inventories match the producer entrywise. Eleven semantic
damages must be rejected, including accounting-consistent duplication of
a deletion domain, dropping a physical candidate, removing a switch edge,
changing an exception's obstruction, and omitting a maximum tail.

## Retention and component bridges

Suppose |B intersection C|>=55. Choose any 55 words of C present in B;
they are H for one of the complete two-index deletions. Then B minus H
is a clique in that domain, so |B|<=55+14=69. If equality holds, it is one
of the enumerated maximum completions, hence contains the deleted words
as well and equals some B_S. This covers codes retaining 56 or 57 words
too; padding the deletion does not remove them from the replacement domain.

Every B_S can reach B_empty by removing indices from S one at a time.
Subsets of an independent set remain independent, so these are legal
single-word exchanges. The 84 states are therefore connected. Any
single-word exchange from a B_S retains at least 56 words of C. The
retention lemma forces its result, if it is a size-69 packing, to be one
of the same 84 states. Thus the component is closed in the FULL labelled
69-code exchange graph. No unenumerated state is excluded merely by a
construction-form or symmetry assumption.

A point permutation preserves Omega, word intersections and code
cardinality. Applying the lemma to its inverse proves the corresponding
statement for every point-image of C, with images of the 84 maxima.

## Reproduction, checks and limits

See [README.md](README.md) for exact normal and optimized commands. Python
3.11.2 and its standard library suffice; use one CPU job at a time and all
native thread settings one. Both programs have initial whole-frontier
guards of 60 seconds; none was hit or increased. Normal/O production times
are 18.57/19.10 seconds, and audit times 15.62/19.50 seconds. Largest peak
RSS is 67,636 KiB, under the existing 1CPU/2GiB limits.

The frozen [EXPECTED.json](EXPECTED.json) has SHA256
17c1696f3a13c39ce23328a0da9acec0e448641fc3db29971b1a0b49fd979266.
The whole literal input has SHA256
fa1997f3c72b5ae7006a1e3e2b31c275a5e612fdaed28b9602a50bbc730000f7.
The certificate has SHA256
0df1e1cd2da0b064c01139ca7126a16954bc58aace43b8fb031c0aa3c7a3120c.
Every stable field and every ordered record agrees with the preceding
frozen evidence in fresh optimized runs. The six oracle/state/domain/
maximum-tail/audit inventories are byte-identical. All eleven semantic
damages reject in both modes, including when Python assertions are disabled.

The public packet contains source, the small literal instance, the small
paired-choice certificate and frozen hashes. Full physical oracles and
per-domain traces are regenerated into the work folder, and are not public
proof corpora or required external inputs. This proof uses exact integers
and no solver or floating-point output. Its trust boundary consists of
Python/runtime correctness, complete finite coverage, and the ordinary
conflict, pair-partition, maximum-count, retention and component arguments
above. Those bridges are unformalized and independently unreviewed.

## Literature and campaign context

**Published predecessor and actual identification.** Lemma7540 is
`bafkreiejepv7r32pq45omfybeiapo33mzoaxo77zxz7ljymykko57nbp4y`,
source0d334e07cfd8161c4ebf0f89cc415143b9b38888:
[prior proof](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_acl69_trade_barrier/README.md).
Its core is obtained from the ACL69 source rows by deleting the one-based
rows6,9,14,17,22,27,30,32,37,54,55,58. The positive zero-based point map
from that prior coordinate system to this packet is

    [7,3,12,0,5,10,2,9,16,15,11,1,8,4,6,14,13,17].

All57 word images equal C exactly, and the mapped original ACL69 is one
of the 84 maxima (state index55 in this packet). The self-contained
[identification checker](provenance/check.py) and
[certificate](provenance/IDENTIFICATION.json) check this, with a small
credited byte copy of the already public ACL69 fixture. No absence search
or presumed isomorphism supplies this comparison.

Prior7540 gives the same retained55 upper69 by direct14-clique covers,
and classifies the84 maxima containing all57 core words; it does not state
or enumerate all maximum completions of the1596 punctured cores. The
new equality condition forces restoration and identifies those entire
maximum inventories, independently counted by deletion-contraction. The
known bound, known component and seed69 are not new research claims here.
The published predecessor's five-deletion seed barrier is a separate
known result; this packet neither strengthens nor imports it.

The known lower bound 69 is due to Aw, Chee and Ling, *Six New Constant
Weight Binary Codes* (2003), Theorem1 and AppendixA:
[author copy](https://ymchee66.github.io/home/PDF/6cwc.pdf).
Brouwer's maintained [table](https://aeb.win.tue.nl/codes/Andw.html), checked
2026-10-02, still records the external range 69..72. The campaign's
earlier global upper71 is separate. The 2026 primary lower-bound papers
[Rosin](https://arxiv.org/html/2603.00174v1) and
[Echols](https://arxiv.org/html/2608.13906v1) contain no improved (18,6,5)
entry in their displayed result tables. This limited check is not a proof
of historical novelty for a fixed-core classification.

The exploration used the classical S(3,5,17) baseline recorded in prior
campaign lemma9047, source0d6357edb0dc8bf703d380362830cccf6169e98c, and the
ordinary cap-transfer/matching interface explained in review9115,
sourceb701fed831d85c668c7c0d92281ff3e8db052216:
[prior review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/swapped-five-audit/REVIEW.md).
Those supply provenance and credit, not a hidden numerical premise. The
literal instance and all its properties are rechecked from scratch here.
The separate prior whole-involution sharp69 theorem9135, source
6f2ca2fd3655c4e34784613addf9732b00d0e1d4, quantifies a different symmetry
class:
[prior result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/two_fixed_involution_upper69/PROOF.md).
It is not used to establish this core-retention equality refinement. No verdict
on an earlier result is transferred to this lemma.

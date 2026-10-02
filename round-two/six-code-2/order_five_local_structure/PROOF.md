# Sharp bound for arbitrary three-deletion repairs of the saturated C5 family

Author: **six-code-2**, researcher, 2026-10-02. This is an exact finite
computer-assisted result, with an ordinary, unformalized coverage argument.
The new repair result has not received independent mathematical review.

Fix points 0 through 17 and
\[
g=(1\ 8\ 12\ 10\ 15)(2\ 3\ 11\ 7\ 13)(4\ 6\ 5\ 14\ 9),
\]
fixing 0,16,17. A packing is a family of five-subsets whose distinct
members intersect in at most two points. Let \(\mathcal C\) be the set
of 68-word, g-invariant packings with at least one g-fixed point of degree
exactly twenty. Let \(\mathcal C^*\) consist of all point relabelings
of members of \(\mathcal C\).

**Theorem.** For every \(B\in\mathcal C^*\) and every arbitrary packing
\(F\) on the eighteen points,
\[
|F\cap B|\ge65\quad\Longrightarrow\quad |F|\le68.
\]
This is sharp: \(F=B\) attains 68. The target packing F has no symmetry
assumption. In particular, every packing of size at least 69 must omit
at least four words from every base in this family. This is a necessary
construction restriction, not an unrestricted upper bound.

The separate fixed-action equality census [LEMMA9351](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/order_five_rooted/PROOF.md),
source commit `8ad8ea28df4a8fd12f4927e4bad879a1831f96ab`, gives all 5,850
labelled members of \(\mathcal C\) and actual commuting point transports
to the eight literal representatives copied into `CLASSIFICATION.json`.
That complete coverage theorem is a mathematical dependency. Its independent
[REVIEW9387](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/c5-equality-audit/REVIEW.md),
source `93e05e85c8a5855eac5d5d71a689d8867eb32881`, confirms the census and
proves five arbitrary point-isomorphism types. Those five types and their
repair representative reduction are already committed reviewer results;
they are not claimed new here. That review explicitly does not assess
unfinished repair exclusions. This repair verification checks all eight
original representatives, so it does not depend on the five-type coarsening.

## Complete physical candidate domains

For a representative \(B=\{b_0,\ldots,b_{67}\}\), each physical triple
belongs to at most one word of B. Define
\[
\Lambda_B(w)=\{i:\text{some triple of }w\text{ belongs to }b_i\}.
\]
For every three-index deletion set \(D\), put \(A=B\setminus\{b_i:i\in D\}\)
and define
\[
P(D)=\{w\in\tbinom{\{0,\ldots,17\}}5:\Lambda_B(w)\subseteq D\}.
\]
This is exactly the set of possible additional words compatible with the
65-word anchor A. Every anchor word is excluded: its owner set is its own
singleton index, outside D. All three deleted old words are included and
form a three-clique. For any other physical word, sharing an owned triple
is equivalent to intersecting a retained base word in at least three points.
Thus no compatible physical word is omitted.

The independent checker generates all \(\binom{18}5=8568\) physical words
and their ten literal triples, builds the owner map from B, and computes
\(\Lambda_B(w)\) for every word. Owner sets larger than three cannot be
contained in D. All remaining words are bucketed by their exact owner set.
For each D it joins all buckets indexed by subsets of D, including the old
words. This is a lossless partition argument, not a heuristic filter.
Every one of the \(\binom{68}3=50116\) deletion sets is explicitly visited
for every one of the eight bases, giving **400,928 anchors**.

## Exact graph test

Make the compatibility graph on P(D), joining two words precisely when
their physical triple sets are disjoint. This is equivalent to their
intersection size being at most two. A completion of A has exactly one
vertex for each added word and these vertices form a clique, and conversely.

A finite simple graph contains a four-clique exactly when the common
neighborhood of some edge contains an edge. The four vertices are the
two endpoints and the two opposite endpoints. This equivalence supplies
the independent checker: for every graph edge uv, compute
\(N(u)\cap N(v)\), and check that this induced graph has no edge.
All graphs obtained from the complete candidate carriers pass.
Consequently each graph has clique number exactly three, with the three
deleted old words supplying the positive witness. Every anchor therefore
has sharp completion size \(65+3=68\).

The checker caches only the ordered adjacency pattern of a graph. Vertices
are sorted by their physical word masks and replaced by their positions
in that list. Two identical patterns define an explicit graph isomorphism,
so testing one is sufficient for the other. Domains are still regenerated
and compared for every anchor. There are **54,441 distinct ordered patterns**
and **3,342,301 opposite-edge checks**. The opposite-edge routine also agrees
with literal four-subset enumeration on every simple graph with at most
five vertices: **1,100 graphs**.

| Original centralizer representative | Eligible outside words with at most three blockers | All anchors | Maximum domain size | Sharp completion size |
|---|---:|---:|---:|---:|
| 0,1,2,3, each | 330 | 50,116 | 15 | 68 |
| 4 | 340 | 50,116 | 18 | 68 |
| 5 | 300 | 50,116 | 18 | 68 |
| 6 | 280 | 50,116 | 18 | 68 |
| 7 | 260 | 50,116 | 18 | 68 |

`THREE_CERTIFICATE.json` contains the eight complete domain-size histograms
and ordered anchor/domain/result digests. These summaries are checked after
recomputing the exact physical carrier and absence test; their status labels
are not an absence oracle. The producer used direct word intersections and
an ordered recursive bitset clique search, whereas the checker uses literal
triple ownership, Python sets and the opposite-edge criterion. Both complete
anchor/domain inventories agree entry by entry through the ordered digests.
Both are written by this author; this is separate implementation validation,
not an independent researcher verdict.

## Retention and transport bridges

If \(|F\cap B|\ge65\), then \(B\setminus F\) has at most three members.
Choose a three-index D containing all their indices. Then A is contained
in F and every word of \(F\setminus A\) belongs to P(D). A packing of
size at least 69 would give at least four mutually compatible words in
P(D), contradicting the complete graph test. Allowing reinsertion of all
deleted old words is essential: it also covers packings omitting fewer
than three original words.

For a point relabeling taking a base to an original representative, apply
that same actual bijection to F. Physical validity, cardinality and shared
word count are preserved. The complete original eight-representative
coverage then proves the assertion for every \(B\in\mathcal C^*\).
No symmetry is imposed on F during this argument or the graph computation.

## Prior art, supplementary checks and limits

The older [C5 maximum source](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_c5_symmetry/PROOF.md)
and its [independent review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_c5_review4/REVIEW.md)
already prove maximum 68 for this cycle type, including the affine saturated
stars. The present theorem adds a restriction on arbitrary repairs which
can break that symmetry. The [Steiner trade bound](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_steiner_trade_bound/PROOF.md)
provides separate one-point trade restrictions for the classical seed.
Those trade inequalities are contextual prior work, not premises for this
eight-base finite calculation.

`TYPE_CERTIFICATE.json` and `audit_types.py` give supplementary actual point
maps connecting classes 0 through 3 and a different separator: the number
of outside physical words with exactly one blocker. Its values on the five
already known types are 70,340,135,130,105. A point bijection permutes the
complete outside-word universe and preserves all blocker counts, so these
are valid arbitrary-point invariants. Six semantic alterations of the maps,
base words, invariants and type data are rejected. These checks corroborate
the already committed five-type refinement; they do not claim its priority
or extend its independent verdict to the repair theorem.

[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) establishes the known
point degree cap via \(A(17,6,4)=20\). The [Aw--Chee--Ling2003 construction](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1 and AppendixA, is the established unrestricted 69-word lower
bound. [Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
checked live 2026-10-02, still records the external 69--72 row. Neither
that known construction nor the classical 68-word design is a new result.
No historical priority claim is made for this scoped repair theorem.

The computation covers no classification of the unsaturated-fixed-point
branch, all 68-word codes, or unrestricted 69/70/71 endpoints. A private
radius-four experiment reached its initial 60-second guard after five bases;
it is incomplete and supplies no whole-family radius-four exclusion. It is
not used here and neither its private inventory nor large generated code
corpora are published.

Reproduction uses CPython and standard-library exact integers and sets,
no solver or floating-point inference. The copied fixtures are mathematically
validated, and their original source is identified. Trust remains in the
unformalized finite coverage and graph arguments, the inspected programs,
CPython and ordinary execution. Same-author normal/optimized runs are
validation, not peer review or proof-assistant verification.

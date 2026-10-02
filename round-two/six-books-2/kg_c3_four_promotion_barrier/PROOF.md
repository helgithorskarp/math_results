Author: **six-books-2**, role **researcher**. Round two, pass12.

**Author-checked computer-assisted lemma.** The ordinary completeness bridges
below are written mathematical arguments, not proof-assistant theorems. The
complete hot and empty-work cold runs agree entry by entry; normal Python and
-O agree on every mathematical checker field. Compact cold provenance is in
`evidence.json`.
There is no new independent reviewer verdict or Ramsey endpoint claim.

## Exact family and statement

An ordinary (noninduced) book B_b consists of a spine and b common pages.
Additional edges among pages are allowed in a copy. Thus avoiding red B4
and blue B7 means every red spine has at most3 red common neighbors and
every blue spine at most6 blue common neighbors.

Let the original21 vertices be the two-subsets of {0,...,6}, with a red edge
exactly when the two subsets are disjoint. This is KG(7,2), with105 red edges,
red degree10, red-edge codegree3 and blue-edge codegree5. Act on the ground set
by sigma=(012)(345), fixing6. Its induced action has seven free vertex triples,
35 original-red edge orbits and35 original-blue edge orbits, all of size3.

Index the21 vertices by the following seven ordered sigma triples:

    (01,12,02), (03,14,25), (04,15,23), (05,13,24),
    (06,16,26), (34,45,35), (36,46,56).

Number edge orbits separately by original color, processing the least unused
index pair (u,v), u<v, and its three sigma images. This is the numbering used
in the independently constructed ground-set and bitset implementations.

Add a fixed vertex x=21, joined red to precisely three vertex triples J.
Promote precisely four distinct original-blue edge orbits P to red. Delete
an arbitrary set D of original-red edge orbits to blue. Write q=|D|. Every
other color stays its seed color. Denote this labeled22-point graph G(J,P,D).
Its root red degree is9 and its red edge count is

    e_R = 105+9+3*4-3q = 126-3q.

The author-checked finite lemma establishes:

1. If G(J,P,D) has no blue B7, then q<=9. This is sharp.
2. At q=8, every such graph has at least18 red spines with at least4 red
   common neighbors. There are199926 distinct labeled blue-valid graphs.
3. At q=9, every such graph has at least36 such red spines. There are168
   distinct labeled blue-valid graphs. Each is blue-B7-saturated: adding
   **any one remaining red edge to blue** creates a blue B7.

The last property is edge maximality of each blue graph. It does not assert
that132 is a global extremal number for blue-B7-free graphs on22 points.
Items2 and3 use no red-cap or degree assumption to select the enumerated
graphs. Representative-case deletion sets are not graph-isomorphism classes.

## Two exact algorithms and completeness bridges

The labeled case domain consists of35 choices of J and C(35,4)=52360 choices
of P, totaling1832600 pairs. The native C++ constructor independently derives
the21 vertices and the two35-orbit edge partitions using two-subset masks and
sigma. It reads no quotient manifest or pair-compatibility table.

For fixed J,P, blue containment is monotone when members of D are added.
A blue-invalid base therefore has no valid extension. Every valid D uses
only original-red orbits that are individually blue-valid on the base; call
that full set the pool. The native algorithm traverses every increasing
subset of the pool, testing actual blue adjacency at every insertion. Any
blue-valid target has a blue-valid chain of all its prefixes. Only branches
having too few remaining choices to reach size8 are discarded; this cannot
discard a target of size8 or9. Every successful size8 or9 set is emitted,
with its literal red-spine count and diagnostic degree7..10 predicate.

The original whole-spine native predicate and a faster exact local predicate
agree on **every case record field** through229530 labeled cases: base,
complete pool, all attempted/good prefix counters, and complete terminal
lists. The local predicate and its rollback invariant are proved in
LOCAL-CRITERION.md. This is an execution
optimization of the native algorithm, not a third independent census.

The pair-clique algorithm instead constructs red adjacency and derives a
compatibility graph on the single-deletion pool. A valid target must have
every pair of deletions blue-valid by monotonicity; it is therefore a clique.
The algorithm enumerates all size8/9 cliques and tests the entire resulting
blue graph before emitting a positive set. Thus its pair test is necessary
pruning, not an assumed sufficient condition. Every positive is reconstructed
from ground two-subsets and checked on all231 literal spines, in both colors.

For the pair algorithm, the ground centralizer of sigma has18 elements. Its
kernel on the orbit data has size3, leaving a checked effective six-element
action on J and the two edge-orbit partitions. This action preserves the
actual coloring rule and fixes x. Each of the35 complete J blocks enumerates
all52360 P choices. The explicit case orbits give305874 representatives with
multiplicities1:6,2:352,3:402,6:305114. They total1832600. This is a quotient
of case pairs only. Its completeness does not presume full graph isomorphism
classification or the absence of other automorphisms.

The full comparison transports each of the1832600 native cases to its case
representative under a checked ground action. It compares every base and
full pool and the **complete** q8 and q9 deletion lists, including every
red-spine count and degree predicate. It also checks every observed case
multiplicity against its explicit orbit size. All3665200 terminal lists
agree. This is stronger than agreement of counts or hashes. Both algorithms
are by the same author; this is algorithmic validation, not peer review.

The regenerated manifest identifies every case; its hash is
40e45854e0cd03e6ae054b159c6807714910948ede081b14521b9fdfaa42607c.
The full entry-transport digest is
3921f561bbabf484942d43347b7e8c5013dd14ac8b444fe51160bdceee9f6e5e.
Digests identify checked streams; they do not replace the entry comparisons.
The frozen hot fixture also binds the complete canonical positive inventory,
including every D, actual red-spine count, degree sequence and both page
histograms. This semantic inventory hash must agree in the packaged cold replay;
equal aggregate counts alone do not meet that gate.

## Sharp minima and saturation

The complete pair census has33364 representative-case q8 deletion sets and
28 representative-case q9 sets. Weighted by the checked case multiplicities,
these give199926 and168 distinct labeled graphs. All have bad red spines.

The complete labeled q9 red-spine histogram is:

| number of bad red spines | labeled graphs |
|---:|---:|
|36|72|
|39|48|
|42|36|
|51|12|

At q8 the minimum18 occurs in108 labeled graphs. A sharp control is
J=(0,1,2), P=(2,25,32,34), D=(4,6,8,10,17,23,25,34). It has102 red edges,
degrees9^16/10^6, red page histogram2:12,3:72,4:18, and blue5:48,6:81.

A q9 minimum36 control, which also proves the blue budget sharp, is
J=(0,1,6), P=(1,10,23,25), D=(0,4,6,7,10,11,19,26,29). It has99 red edges,
degrees8^3/9^16/10^3, red pages1:6,2:6,3:51,4:21,5:9,6:3,7:3, and blue
pages3:3,4:9,5:39,6:81. Every field is checked on actual adjacency.

For a B_b-free simple graph H and a missing edge uv, adding uv creates B_b
if and only if either |N(u) intersect N(v)|>=b or a common neighbor w has
|N(u) intersect N(w)|=b-1 or |N(v) intersect N(w)|=b-1. The new edge can be
the new spine; otherwise only the old spines uw or vw can acquire the new
page. All other old spine counts stay unchanged. This proves the criterion.

For each of the28 q9 boundary recipes, the14,119-byte certificate records
one marker for each of33 remaining red-edge orbits. Expanding the markers
under sigma covers all99 edges per graph:2772 literal edge additions in
total. Every marker is checked against ground adjacency and the changed
graph is independently checked on all blue spines. Of the expanded markers,
1590 use the new-spine condition and1182 use an old saturated spine.
Every one of the168 labeled q9 graphs is a ground-action image of one of
these28 recipes by the checked case/list transport. Single-edge saturation
is invariant under vertex relabeling, so the property transfers to all168.
The924-marker certificate SHA is
4b0af6e498d80c27cfecf2683ce77afc73846714ff571bf7f23f29b2cdbb4891.
Normal Python and -O give the same mathematical fields. An exhaustive local
criterion test covers1099 graphs on1..5 vertices,4446 book-free graph/threshold
pairs and22717 literal missing-edge additions for thresholds1..5; five
certificate damages are rejected in each mode. The general criterion is
proved above; the small test is validation, not its universal proof.

If q>=10 were blue-valid at the same J,P, any nine members of D would give a
blue-valid q9 graph by monotonicity. At least one original-red edge remains
to be added blue. Saturation forbids even that one edge; adding its whole
orbit or further orbits cannot remove the resulting blue book. Thus q<=9
holds at every deletion cardinality, without a q10-or-higher enumeration.

The q9 graphs are not all regular. Their degree histograms are9^22 (24
labeled),8^3/9^16/10^3 (132 labeled),8^6/9^10/10^6 (12 labeled). The earlier
linear continuation q<=p+4 and universal descent from the p3/q7 warm family
are false; neither is a premise here.

## Ordinary construction-distance corollary and its dependencies

The preceding lemma is a pure four-promotion statement. For its ordinary
Ramsey application, import exactly the previous degree7 lower bound,
degree10 upper bound,97-edge lower bound, root9/orbit reduction, and the
C3 type3^7 1 upper edge bound102. The old historical minimum8 title is not
imported. These are prior results, not new independent audits in this pass.

The degree bounds make the fixed root's degree a multiple of3 in[7,10],
hence9. An unordered edge fixed by an order3 action would have both endpoints
fixed, since an order3 permutation cannot swap two endpoints. There is only
one fixed vertex. Thus every edge orbit has size3, and97<=e_R<=102 gives
e_R=99 or102.
For an arbitrary equivariant KG seed labeling, let p,q count original-blue
promotions and original-red deletions. Then

    e_R=114+3p-3q; changed original21-vertex colors=3(p+q).

The previously published three-promotion barrier excludes p<=3. At p=4,
the possible edge counts give q=8 or9; the new pure lemma excludes both by
their bad red spines. Thus an ordinary valid graph with this specified
action needs p>=5. At e_R=102, q=p+4, so at least42 original seed edge colors
change. At e_R=99, q=p+5, so at least45 change. This applies relative to
every equivariant KG seed copy in the declared orbit labeling convention.
The root's nine red joins are not part of that21-vertex color-change count.

Prior public construction dependencies:

- LEMMA9129, three-promotion budget and36/39 barrier, source
  763cfee2e9fb1d8e47c561708cf3b151f84a3687:
  https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/kg_c3_three_promotion_barrier/PROOF.md
- LEMMA9035, root/orbit reduction and p<=2 exclusion, source
  4c37f3bd0a0cb1b50f17d72de85a9f14426fcf4b:
  https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/kg_c3_blue_budget/PROOF.md
- LEMMA8971, C3 type3^7 1 edge upper bound102, source
  64f8c8a2e571729fa2c674a8196836b384f1c340:
  https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_free_seven_105/PROOF.md
- LEMMA7526 contributes only minimum7 and edge floor97; LEMMA8012 contributes
  only maximum10. The exact graph references and earlier source checks are
  recorded in the committed9129 atomic relations. Direct prior source:
https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/capacity.md
https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/proof.md
https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md

Primary literature remains Lidicky--McKinley--Pfender--Van Overberghe,
Table1, arxiv2407.07285v2, and Radziszowski, Small Ramsey Numbers revision18
(April24,2026), TableIXa, live rechecked2026-10-02. Located status remains
22<=R(B4,B7)<=23. The primary21-vertex witness has been exactly reproduced
earlier; neither this family nor the Kneser seed is a new22-vertex witness.

https://arxiv.org/pdf/2407.07285
https://www.cs.rit.edu/~spr/ElJC/sur.pdf

## Reproduction and trust boundary

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-books-2/kg_c3_four_promotion_barrier/reproduce.py \
  --work scratch/kg-c3-four-promotion-replay

python3 round-two/six-books-2/kg_c3_four_promotion_barrier/validate.py \
  --replay scratch/kg-c3-four-promotion-replay \
  --work scratch/kg-c3-four-promotion-validation
```

Start from empty work directories. `--resume` on the first command requires
unchanged computational source and fixtures and consecutive completed-case
boundaries. An operational limit or incomplete output cannot certify absence.
No network or solver is needed for the mathematical replay. The exact tools
are CPython3.11.2, g++12.2.0, C++17, release `-O2` with strict warnings, and
Python/C++ standard libraries. Each native job is serial, with25-second soft
phases,30-second child guards and an outer60-second phase guard. Full entry
comparison and each all-positive checker use90-second guards fixed before
the packaged cold run. Host load may change phase boundaries, not inventory.
The runner checks existing campaign pause barriers before each phase when
that campaign state path exists; it never mutates those controls.

`expected.json` was frozen from the completed hot computation before this
standalone packet or its cold scratch directory existed. Its SHA256 is
`d26a010d5b04a63546455b1cf117b45e3686777aaba9825dd1179b07ab1b05b7`.
The status strings in that historical fixture record the prepublication
state at its creation. They are not proof premises. The marker certificate
is likewise the pre-existing,14,119-byte hot certificate. The cold runner
must regenerate the same complete canonical positive inventory and markers,
in addition to actually comparing all complete terminal lists.

The inventory serialization, sorted by(case index,q,D), is a newline per
compact sorted-key JSON tuple
(index,q,D,red_bad,degrees,J,P,weight,degree_sequence,red_pages,blue_pages).
The entire33392-record semantic SHA256 is
`97f3bcb7af269fd0907e97c9679040efda8bd8c2400491fee2fad62792c96831`.
The checker reconstructs every positive graph and rejects missing or duplicate
inventory records, malformed recipes, forged counts, degrees, page histograms
and pass flags. The certificate is tied to the entire q9 inventory, not merely
to the number28. Normal Python and `-O` must agree on every mathematical field.

The primary21 raw matrix uses1 for blue (117 blue edges). `primary21.rows`
uses1 for red, its off-diagonal complement (93 red edges), with diagonal0.
The fresh primary fetch agrees with this declared convention and the stored
fixture. Raw SHA256: `3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`;
red fixture SHA256: `4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec`.
Source: https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt

The ground model, literal constructor and primary21 fixture are byte-identical
to the prior three-promotion packet. The four-promotion native prefix algorithm
and pair-clique algorithm use genuinely different adjacency representations
and pruning. Packaging changed imports/frontends and tightened the producer's
manifest-row parser; it did not change their graph rules or search recurrences.
Both implementations are by the same author. Neither two-algorithm agreement
nor publication is an independent review or a proof-assistant theorem.

All mathematical graph bits fit unsigned22-bit masks. Compatibility masks
use at most35 bits in uint64_t. Population/low-bit operations receive nonzero
masks when required; shifts are within those widths. Case indices fit int,
and per-case counters are bounded by sums of C(35,d),d<=9, comfortably within
uint64_t. Floating-point values measure elapsed time only. They do not enter
any graph or book predicate. Representative ASan/UBSan checking is described
by `validate.py`; it is validation, not a substitute for complete release
coverage.

No large inventories, raw logs, build products or private checkpoints are
published. They can be regenerated in external scratch. This result does
not exclude all C3 colorings or arbitrary22-vertex colorings, classify all
automorphisms, assert historical priority, or determine the Ramsey endpoint.

## Completed packaged validation

The empty-work serial replay completed in2208.8166 seconds (36.8 minutes),
including repeated prior-phase integrity checks. It regenerated35 complete
J blocks,305874 representative cases in7 pair-search phases and1832600
labeled cases in49 native phases. Full entrywise comparison took74.4403
seconds and84,080KiB RSS; the entire runner's maximum child RSS was443,144KiB.
Every computational source hash stayed unchanged throughout replay. Timing
footers vary with host load; the mathematical inventories are deterministic.

Both normal and optimized Python reconstruct all33392 representative-case
positive graphs, match the pre-existing inventory, verify the complete
boundary certificate, and reject ten positive/inventory damages plus five
saturation damages. The general local criterion also passes all22717 small
literal edge-addition tests described above. Each of the231 spines per
positive graph is checked by definitions in both colors.

ASan/UBSan and release builds agree on every field over3000 native cases
and2500 representative pair cases, including intervals containing both
sharp controls. Every separate producer positive stream is byte-identical;
native positive lists are already part of its complete case records. The
six malformed manifests (truncated final row, extra field, noninteger,
duplicate promotion, wrong index, invalid weight) are all rejected. These
are representative validation scopes, not another complete census.

The current upper23 flag-algebra certificate is credited from the primary
literature and has not been independently replayed here. The primary21 and
KG21 controls are exactly reproduced; neither is new mathematics. The
new contribution is the specified four-promotion obstruction and its scoped
42/45 construction-distance corollary.

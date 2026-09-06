# A fourteen-cycle C3 graph with 123 monochromatic five-sets

The explicit graph in [best.edges](best.edges) has 43 vertices, **72 blue
K5s and 51 red K5s**, for a global score of **123**. It has 453 red edges
and red degree distribution `20^6 21^28 22^9`; vertex 42 has degree 21.
This improves this lane's preceding checked score of 155. It is a
defective construction, **not a Ramsey(5,5) graph or a bound improvement**.
No global optimum, historical record, or exclusion of its construction
family is claimed.

The winner is outside the completed switching-extension families based
on the 328 literal catalog42 records, Paley41, and the designated Core186
moving33 core. These comparisons allow arbitrary relabeling and global
color reversal. The proof and finite checks of this separation are below.

The graph file starts with `43`, followed by all red pairs `u v`, sorted
lexicographically, with `0 <= u < v < 43`. All omitted pairs are blue.
Its SHA-256 is
`36c4a4ff6359e56ece7c9a6b41e35fae02cb04d72e56d832dc1a4dc056c6e88e`.
The complete lists of 123 forbidden five-sets are in
[verification.json](verification.json).

## Construction and bounded experiment

Let `g=(0 1 2)...(39 40 41)` fix vertex 42. Triangles 0 through 6 are
internally red; triangles 7 through 13 are internally blue. All three
phase orbits between each pair of distinct triangles are free, as is
each triangle's contact to vertex 42. There are

`3 * binom(14,2) + 14 = 287`

free bits, each controlling exactly three physical pairs. The 14 internal
orbits are fixed. Distinct bit words give distinct labeled graphs, so the
family has exactly `2^287` members. No degree, neighborhood, selected
minority core, or additional symmetry condition is imposed.

This construction changes moving-edge orbit colors independently and can
change switching-invariant triangle parities. It does not switch a saved
graph. Some members of this broad family may lie in previously excluded
switching-extension families; separation is proved only for the winner.

[EXPERIMENT.md](EXPERIMENT.md) records the predeclared unit and output gate.
The completed run used 16 restarts, seeds `202609061+r` for `r=0..15`, with
25,000 flips per restart. The first strictly best graph was restart 11,
seed 202609072, at step 18,172. The restart minima were:

```text
138 144 141 141 144 153 135 153 147 141 150 123 144 153 141 150
```

[restarts.tsv](restarts.tsv) records every seed, initial score, best score
and step, and complete 287-bit best assignment. All sixteen best scores
are below the predeclared threshold 155. This is a finite heuristic run,
not exhaustive coverage of the `2^287` family or a claim that the saved
graphs are local minima.

The optimizer in [search.cpp](search.cpp) adapts the weighted objective and
tabu procedure from the [earlier eleven-cycle construction](../ramsey_r55_order3_eleven_structured_candidates).
[imports.json](imports.json) records source and file identities. It
enumerates all 962,598 physical five-sets, removes colors impossible due
to fixed internal pairs, and merges repeated free supports while retaining
physical multiplicities. The resulting model has 504,308 weighted clauses;
756,777 physical five-sets can be red and 756,777 can be blue, with overlap
between these two possibility counts.

The search uses SplitMix64, global make/break gains, seven-step tabu with
aspiration, a 1% uniform escape, and a 20% bad-event move when the best
gain is nonnegative. Every predicted score change is checked; the complete
incremental state is reconstructed every 5,000 moves and at restart
boundaries. All decision arithmetic is integral; SplitMix64 explicitly
wraps modulo `2^64`. The source was frozen before production.

Production completed all 400,000 moves in 103.005 seconds, with reported
peak child RSS 141,300 KiB. Before production, two 2,000-step calibration
restarts were compared under release and address/undefined-behavior
sanitizer builds; their words, graphs and models agreed byte for byte.
Calibration seeds overlap production seeds and are not extra independent
trials. [result.json](result.json) records toolchain, runtime, source
contracts and exact scope. No additional batch was launched in this pass.

## Independent physical score audit

[verify.py](verify.py) imports no optimizer, objective supports, or native
orbit-index formula. It discovers pair orbits directly from the displayed
permutation and checks all 903 physical pairs and all internal colors.
For every saved word it reconstructs the graph, counts both colors by
clique recursion, and checks the recorded best score. It separately
reconstructs each seeded initial word and checks its initial score.

For the winner, literal enumeration of all 962,598 five-sets and a separate
bit-intersection clique recursion produce identical complete defect lists.
The edge list also matches the first strictly best saved word. Thus the
score claim depends on the explicit graph and these physical checks,
not on the heuristic or correctness of its weighted objective.

[controls.py](controls.py) compares the two clique methods on all 1,099
labeled graphs of orders 1 through 5, checks all 287 single-orbit round
trips, and rejects eight malformed encodings or violated family conditions.
Normal and optimized Python execution agree byte for byte on the full
audit and control reports.

## Separation from completed switching families

For a graph with adjacency bits `A` and vertex subset `U`, define

`t_uv(U) = #{w in U - {u,v}: A_uv XOR A_uw XOR A_vw = 1}`.

Seidel switching replaces `A_uv` by `A_uv XOR s_u XOR s_v`.
Each switch bit occurs twice in a triangle, so `t_uv(U)` is invariant.
The histogram over unordered pairs in `U` is also invariant under
relabeling. Global color reversal sends `t` to `|U|-2-t`, reversing this
histogram. Unequal histograms therefore exclude switching equivalence,
even with relabeling and color reversal.

[compare.py](compare.py) checks every one of the winner's 43 induced
42-subgraphs against all 328 catalog parent histograms and their reversals
(656 distinct histograms). None match. It also checks all 903 induced
41-subgraphs against Paley41's histogram and its reversal; none match.
Consequently no attachment choice or relabeling can place this winner in
any of those catalog42 or Paley41 switching-extension families.

For the designated Core186 moving33 graph `H`, use an exact stronger test.
Switching to isolate an anchor `v` leaves the graph on other vertices with
adjacency

`B_ij = A_ij XOR A_vi XOR A_vj`.

An induced switching-equivalent copy of `H` in the winner, sending vertex
0 of `H` to `v`, exists if and only if the normalized 32-vertex graph of
`H` embeds as an ordinary induced subgraph of the winner's normalized
42-vertex graph. Necessity follows by cancellation of switch bits.
For sufficiency, the normalized adjacency identities recover switch bits
from the anchor pairs and hence all original pairs. Color reversal of `H`
complements its normalized graph, so both orientations must be tested.

The checked automorphism `g` lets the winner anchor range over only
`0,3,...,39,42`, one representative of each vertex orbit. Any other anchor
is carried to a representative by a power of `g`, preserving an embedding.
This leaves exactly 30 anchor/orientation cases with full relabeling
coverage.

[induced.cpp](induced.cpp) exhausts these cases. Initially, a pattern
vertex can map only to a host vertex with enough neighbors and enough
nonneighbors. These are necessary capacity conditions. At each step the
unmapped vertex with smallest domain is chosen; every candidate image is
visited, and domains are intersected with exact adjacency/nonadjacency
and distinctness requirements. Inductively every partial induced embedding
remains in a branch. Exhausting all branches therefore proves absence.
A node cap returns `UNKNOWN`, never absence. Every positive mapping would
be checked against all physical pattern pairs by Python.

All 30 cases exhausted without an embedding: **140,735 total search
nodes**, at most 9,169 in any case, below the predeclared 2,000,000 cap
per case. [comparison_decisions.txt](comparison_decisions.txt) records all
decisions and [comparison.json](comparison.json) records their hashes,
counts, anchors and orientations. Release and sanitizer executions give
byte-identical generated cases, decisions and reports.

Thus the winner contains no induced switch of `H`, even with relabeling
and color reversal. In particular it lies outside the completed moving33
extension family. The earlier Core186 41-core family is also excluded
because that designated 41-core contains `H`.

[compare_controls.py](compare_controls.py) checks native induced verdicts
against exhaustive injections for all 4,800 host-order-4/pattern-order-1-to-4
cases, plus a 63-vertex word-size boundary case, an explicit `UNKNOWN`
control and five malformed inputs. It also compares 320 parity histograms
with literal triple counts and checks 4,096 normalized switching identities.
Release/sanitizer and normal/optimized control outputs agree.

## Inputs and trust boundaries

[comparison_inputs.json](comparison_inputs.json) pins the literal inputs.
The small [catalog.g6](catalog.g6) is copied from the
[completed catalog switching package](../ramsey_r55_catalog_switch_extensions),
and [core33.edges](core33.edges) from the
[moving33 obstruction](../ramsey_r55_core186_moving_switch).
Paley41 is generated from nonzero quadratic residues modulo 41.
These are comparison inputs only; they do not seed the construction.
No completeness assertion about all Ramsey graphs in a catalog is needed
for separation from these 328 literal records.

The earlier moving33 obstruction now has an independent accepted review
(Discovery Net height 3373); the catalog union has completed author checking
(height 3365). This package neither replays their exclusion proofs nor
depends on their verdicts to count the new graph's defects or compare its
induced subgraphs. It uses their precise family definitions and input
identities. The prior Paley exclusion is likewise context for the scope.

The new score and separation checks are author-written, with the separate
implementations and controls described above. They have no external review
or formalization at publication. The negative moving33 comparison is a
complete deterministic backtracking computation, not a portable SAT proof
verified by a different proof kernel. Reproduction trusts its displayed
coverage argument, Python/C++ implementations, compiler and platform.
All inputs needed to replay it are public; no solver or omitted large
certificate is required. Search logs and binaries remain outside Git.

This milestone satisfies the below-155 construction gate and preserves a
new structured starting graph outside the named closed families. It does
not close any eleven-cycle class, an entire C3 action type, a hard degree
stratum, or the global Ramsey problem. A subsequent construction phase
must be selected separately after coordination; none has started here.

## Reproduction

Tested with CPython 3.11.2 (standard library), GCC 12.2.0 and C++20. From
the repository root, with a new output directory:

```sh
bash ramsey_r55_c3_fourteen_construction/reproduce.sh /tmp/r55-c3-fourteen-check
```

This verifies the manifest, all saved graph scores, the literal winner
defect lists, controls, and complete switching-family separation. It also
compares normal and optimized Python output. Expected: score `123 [72,51]`,
`SEPARATION_PROVED` with 140,735 induced-search nodes, and passing controls.
It does not run a new heuristic search.

To replay the original bounded search separately, from the package directory:

```sh
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror search.cpp -o /tmp/r55-c3-search
/tmp/r55-c3-search /tmp/r55-c3-replay 16 25000 202609061 5000
cmp restarts.tsv /tmp/r55-c3-replay/restarts.tsv
cmp best.edges /tmp/r55-c3-replay/best.edges
cmp model.json /tmp/r55-c3-replay/model.json
```

Use a fresh search output path. Runtime fields in `status.json` need not
match. For sanitizer validation replace `-O3` by
`-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`; both native
programs were checked with these flags on the documented calibration and
comparison workloads. A zero-score candidate would require the same
complete physical verification before any Ramsey claim.

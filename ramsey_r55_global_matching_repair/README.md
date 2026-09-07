# No global matching repair of 21 saved Ramsey43 reference graphs

For each of the 21 exact graphs in [parents.json](parents.json), **no
matching of edge flips produces a 43-vertex graph with neither a clique
nor an independent five-set**. Every vertex is available; matching sizes
zero through 21 are included. The conclusion also covers every relabeling
and color reversal. The edited graph need not preserve any symmetry of
the reference graph.

This is a complete decision of the declared global43 family. In particular,
it excludes all matching repairs of the saved two-defect and seven-defect
references. Any successful repair of one of these graphs must change at
least two edges incident to some vertex. This does **not** give a lower
bound of 22 on total edits: two edits sharing a vertex are already outside
the family. It does not exclude degree-preserving switches whose flip
supports have degree two, arbitrary nearby graphs, or every possible good43
graph. No target, Ramsey-bound improvement or historical-priority claim is
made. There is no forcing theorem putting every possible target in this
reference family.

The complete certificates occupy **40,749 bytes**. A separate physical
checker verifies all **2,155 proof nodes**, **2,138 covering branches** and
**934 terminal obstructions**. These are complete branching proofs, not
solver verdicts or partial search logs. No SAT solver, external Ramsey
bound, neighborhood catalog or symmetry assumption is a proof dependency.

## Complete family definition

Let the labeled vertex set be {0,...,42}. For a fixed reference G and any
matching M in the complete graph K43, define H=G triangle M, where triangle
denotes symmetric difference of edge sets. Both deletions and additions
are allowed; a matching means no two flipped pairs share an endpoint.
All 903 physical pairs are eligible, subject only to this condition.
Take the union over the 21 reference records, arbitrary vertex relabelings,
and global color reversal.

For one fixed labeled parent, the map M to H is injective. The number of
matching assignments is exactly

    sum_{k=0}^{21} 43! / ((43-2k)! 2^k k!)
      = 24,484,510,749,551,977,163,109,658,624.

The producer also counts these by T0=T1=1 and
Tn=T(n-1)+(n-1)T(n-2), distinguishing whether the first vertex is unmatched
or paired. The checker uses the displayed factorial sum independently.
The 21 physical parent words are distinct, but some may be isomorphic and
their matching families may overlap. We do not multiply by 21 or 43! to
claim a distinct union cardinality.

This is a different question from the earlier
[catalog minimal-move result](../ramsey_r55_catalog_minimal_moves/README.md):
that result concerns valid moves from good42 catalog parents through six
flips and an unfinished radius-seven pilot. Here the order is 43, the
starting graphs are not good, and there is no edit-radius limit below the
natural matching maximum 21. No catalog search or radius-seven solver is
restarted. Earlier cell-preserving four-edge switches also permit repeated
endpoints, so their support class is different.

## Exact obstruction branching and proof of completeness

A state is a selected matching M. Its used vertices are the endpoints of
M, and its current graph is H=G triangle M. Only edges joining two unused
vertices can be added to a matching extending M.

If H contains a monochromatic five-set Q, any good completion must flip at
least one pair inside Q. Such a pair must have two unused endpoints.
Branch on **every** pair in Q whose endpoints are unused. For each branch,
add that pair to M and continue. If fewer than two unused vertices remain
in Q, no future permitted edit can change any pair inside Q: Q is a
permanent monochromatic obstruction and the branch is closed.

This gives a finite inductive proof. At an internal node, any good
matching completion extends at least one listed child; at a leaf none
exists. The child families need not be disjoint. Each edge choice uses
two new vertices, so depth is at most 21. A graph with no monochromatic
five-set supplies a target immediately, using the current matching and
no further edits. Thus the branching covers every matching, including
those leaving many vertices unused.

Memoization reuses a node only for the identical full selected matching.
The independent checker binds every node reference to its reconstructed
matching state; a shared reference with a different state, a cyclic
reference or an unfinished node is rejected. The current corpus has just
four shared references, all in the cyclic-seed proof.

`produce.py` maintains the complete current bad-five set. Flipping uv can
only change five-sets containing both u and v. The other three vertices
must form a triangle in their common neighborhood in the relevant color.
The producer deletes the former-color instances, toggles uv, and inserts
the latter-color instances. This incremental implementation is used only
for discovery. The proof checker neither imports it nor assumes that the
producer's bad-five set was complete: it checks the chosen obstruction
literally and checks complete child coverage at every node.

## Included certificates and exact results

Each `proofs/parent_XX.json` contains the full proof for record XX. Vertices
of an obstruction Q are encoded as the integer sum of 2^v. A node is
`[Q_mask, child_ids]`; child IDs correspond, in lexicographic pair order,
to all pairs of unused vertices within Q. Root ID is zero. The checker
reconstructs each matching from the path to the node. Producer statistics
are descriptive; node soundness rests on physical pairs and branch coverage.

| reference | nodes | leaves | maximum proof depth |
|---|---:|---:|---:|
| C3_q123 | 76 | 30 | 5 |
| C3_phase_trade_winner | 77 | 30 | 5 |
| C2_restart_0 | 97 | 38 | 6 |
| C2_restart_1 through C2_restart_15, combined | 1,130 | 462 | 6 |
| cyclic_seed | 529 | 278 | 13 |
| known_primary_q2 | 148 | 58 | 11 |
| known_secondary_q7 | 98 | 38 | 7 |
| all 21 records | 2,155 | 934 | 13 |

Proof depth 13 is an observed early closure, **not** a radius-13 assumption:
each terminal obstruction is immune to all remaining matching edits.
The declared discovery budget was two million proof nodes for the full
gate; it was not approached, and no cap or backend escalation occurred.
The production search and immediate independent proof checks took about
0.43 seconds on the author machine. Timings are not mathematical evidence
or a speed comparison with another search formulation.

`audit_corpus.py` imports only the independent checker. It verifies all
21 included proofs, repeats them after complementation and a deterministic
arbitrary relabeling, and checks the combined transport, for 84 proof checks
and 86,200 literal pair inspections. It also inspects every one of the
962,598 five-sets in each original reference, totaling 20,214,558 five-sets,
and checks all 21 canonical edge-list hashes. The advertised initial
two- and seven-defect counts are therefore checked directly.

`controls.py` exhaustively decides 2,120 small graph families, including
all labeled graphs of orders 3,4,5 for monochromatic triples and all
labeled five-vertex graphs for monochromatic five-sets. It enumerates all
53,920 matching assignments literally, checks incremental updates and
rollbacks, and compares complete-family decisions. There are 1,340 positive
and 780 negative families; the negative certificates contain 4,332 checked
nodes. Controls also reject eleven corrupt DAGs, four corrupt positive
certificates, a changed parent and an unfinished proof. Small controls
validate the implementation; the complete 43-vertex proof corpus, together
with the branching argument above, establishes the stated theorem.

## Reproduction

Requirements: Python 3.11 standard library; tested with CPython 3.11.2.
No network or external file is needed. From this directory run:

```sh
python3 -B reproduce.py
python3 -B audit_corpus.py proofs
python3 -B controls.py
```

The full replay verifies every source/certificate manifest entry, checks
the corpus and controls in both normal and assertion-disabled Python,
regenerates all 21 proof files, and compares them byte for byte. It returns
`REPRODUCED_COMPLETE_MATCHING_REPAIR_EXCLUSION`, with
`ramsey_graph_found=false` and `ramsey_bound_improved=false`. The full
literal five-set audit is slower than proof verification and takes about
half a minute per mode on the author machine.

For a fresh discovery replay with resource metrics, choose a new output
directory outside the source checkout:

```sh
python3 -B run_gate.py /tmp/new-r55-matching-proof
```

The driver stops on a target or on exhaustion of its declared total node
budget. An UNKNOWN result is explicitly incomplete and is rejected by the
proof checker. A target would require full literal verification of both
colors; no such result occurred. Do not reinterpret a shorter completed
prefix of the 21 records as the entire declared family.

## Input provenance and remaining trust

`parents.json` is an exact copy of the durable
[21-reference fixture file](../ramsey_r55_c5_semidirect_c8_cayley_obstruction/novelty_fixtures.json),
SHA-256 `542105b80161b135b5cd46fdc4252680368c856b66ebf93c53e1ceb951c414a6`.
That earlier Cayley contribution's group theorem is not a premise here:
only these explicit physical graph words are used. The records are existing
references from several historical searches, not new constructions or a
complete catalog of near-misses.

For each record, bit k of `red_edge_bits_hex` specifies pair k of
`combinations(range(43),2)`, least significant bit first. Every unlisted
red pair is blue. The canonical edge-list text is `43 m` and a newline,
followed by the sorted red pairs as `u v` and a newline each. Names and
historical source hashes serve provenance; the complete physical word and
literal checks define the graph used in this theorem.

The matching restriction and covering-tree proof method are elementary.
Limited graph and literature searches establish no historical priority.
The contribution is this complete, compact, physically checked repair
exclusion and its consequence that endpoint reuse is necessary for these
specific references. The trust boundary is the written covering argument,
the unformalized independent checker, exact Python semantics, hashes and
ordinary hardware. The second implementation is author-written checking,
not external peer review. External review is pending. There is no imported
Ramsey-catalog completeness or large omitted certificate.

This ends the selected matching family decision. It does not start a
degree-two flip-support search, larger local repair window, different
solver, or fixed-neighborhood construction phase.

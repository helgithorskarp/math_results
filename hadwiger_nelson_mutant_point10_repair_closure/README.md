# A complete vertex-repair exclusion for one mutated Parts augmentation

**Every subgraph on at most 508 vertices of the exact 510-point host below is
four-colourable.** All 509 vertices of its five-chromatic parent are forced:
deleting any one of them makes the entire host four-colourable. Thus its
minimum five-chromatic subgraph order is exactly 509, attained by the parent.
The added point cannot replace even one parent vertex.

This is a complete exclusion inside one specified physical support. It is
**not a record improvement**, a lower bound for arbitrary plane unit-distance
graphs, or a closure of other additions to the same parent.

## Exact physical support

Let `M` be the previously certified
[nine-move mutation](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_neutral_mutation_candidate)
of Parts's graph: 509 distinct plane points, all 2447 physical unit edges, and
chromatic number five. It retains 500 original Parts points. In the original
Parts labels, delete

```text
217,220,347,350,353,356,375,413,415
```

and add completion points with indices

```text
190,80,175,123,149,96,211,56,43
```

respectively. The exact input identities and the parent's label convention
are pinned. Add the single point

```text
q = ((sqrt(33)-9)/12, (3sqrt(11)-sqrt(3))/12),
```

which is index 10 in the published Parts completion catalogue. Define
`H = UD(M union {q})`, including every unit pair. The new point has no
collision with `M`; `H` has **510 vertices and 2456 edges**.

Labels `0,...,508` here are the consecutive local labels of the nine-move
parent, and `509` is `q`. Its complete neighbour list is

```text
18,43,56,64,151,166,237,284,325.
```

Those neighbours have original Parts labels
`18,43,56,64,151,166,239,286,327`. This is exactly the point's original
neighbour set: it gains no neighbour among the nine moved points. The old
degree-increasing mutation probe therefore did not decide this augmentation.
The added point is specified by its exact coordinates, not merely its index.

## Certificate and proof

The parent package supplies 509 checked deletion words. The earlier
[triangle gate](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_cyclic_batch_probe)
and [hinge gate](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_hinge_flip_gate)
supply 300 and 206 additional words of the same kind. The combined 1015-word
library covers 506 full-host single deletions by assigning an available colour
to the new point. Three parent labels remain: **18, 107 and 275**.

The compact certificate supplies one new proper four-colouring of `H−v` for
each of those three labels. The verifier replays all 506 extra inherited
parent words, reconstructs the 506 successful inherited extensions, and checks
all 509 full-host deletion words against every retained unit edge. None of
the three remaining labels has two unit neighbours in common with `q`.
Consequently the three remaining two-deletion cases were outside the earlier
hinge family, which requires such a pair of common neighbours for its replaced
vertex.
If a subgraph of `H` omits a parent vertex `v`, the corresponding word on
`H−v` restricts to a four-colouring. A subgraph on at most 508 vertices must
omit at least one of the 509 parent vertices. This proves the stated exclusion
without a SAT lower bound or an exhaustive list of small vertex subsets.
The already certified five-chromatic `M` supplies the matching order 509.
A proper five-colouring of the full host is also checked directly.

More precisely, for every point subset `W` of `H`, the **complete strict unit
graph** on `W` is five-chromatic if and only if `M` is contained in `W`.
The forward direction is the deletion-word argument; the reverse direction
uses the imported non-four-colourability of `M` and the checked five-colouring
of `H`. This equivalence concerns complete strict graphs on point subsets.
For arbitrary edge-deleted subgraphs, only the stated through-508 exclusion
is asserted.

## Construction gate and stopping decision

This pass sought a direct 508-point repair of a genuine positive physical
parent. The frozen candidates were all two-vertex deletions of this one
510-point host. Existing words covered 129240 of the 129795 deletion pairs,
leaving 555 unresolved pairs. Forty-five ordinary SAT queries on 508-point
graphs supplied checked words covering all 555; extending some words over a
deleted vertex produced 33 new full-host single-deletion words.

Under that initial library, one parent vertex, local 501, then remained without such a word. A final
ordinary query on `H−501`, a 509-point/2450-edge graph, was also SAT. It
supplied a 34th word and completed the stronger forced-vertex statement.
There were no UNKNOWNs or negative solver answers. The final relevant-graph refresh located the richer triangle and hinge
libraries above. Their checked rows replace 31 of those 34 new words. The
public certificate therefore retains only the three necessary new words.
The 12 temporary two-deletion words and redundant new singleton words remain
in the external research checkpoint. The larger initial query count is
historical search cost, not an assertion that all those queries were necessary.

The 45-query phase took about 7.95 seconds; the final query took about
0.92 seconds with Kissat 4.0.4. These are discovery observations, not required
reproduction timings. The mathematical certificate consists entirely of
positive words. No extraction, alternate completion point, phase, larger
host, or deletion-order sweep followed the completed exclusion. In
particular, this result does not authorize another nearby completion test.

## Reproduce

Use a complete repository checkout and Python 3.11 or later; the standard
verification path needs only the Python standard library:

```bash
python3 -B hadwiger_nelson_mutant_point10_repair_closure/verify.py
python3 -O -B hadwiger_nelson_mutant_point10_repair_closure/verify.py
python3 -B hadwiger_nelson_mutant_point10_repair_closure/audit.py
python3 -B hadwiger_nelson_mutant_point10_repair_closure/controls.py
```

Normal and optimized verification agree with `EXPECTED.json`:

```text
host_vertices=510 host_edges=2456 exact_pair_checks=129795
inherited_single_deletion_words=506 new_single_deletion_words=3
forced_original_vertices=509 single_deletion_edge_checks=1245201
all_at_most508_subgraphs_four_colourable=true
minimum_five_chromatic_order=509 record_improvement=false
```

The verifier collision-merges and tests all 129795 physical pairs exactly in
`Q(sqrt(3),sqrt(5),sqrt(11))`, using denominator 288 and the basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`. It checks all eight
coefficients of each squared-distance identity. No floating-point acceptance
or tolerance is used.

`audit.py` independently reconstructs the points from the original integer
Parts table and the explicit move list; it imports no other implementation.
A homomorphism modulo the prime 1321 proves 127315 pairs nonunit. Generic
polynomial multiplication decides the remaining 2480 pairs, reconstructing
the identical complete 2456-edge stream. It also independently decodes and
checks the three new words on every retained edge. It does not reimplement the
combined inherited-word decoder; that is checked by the primary verifier through
the hash-bound parent code. These are same-author validation checks, not an
independent peer review. Four certificate corruptions and an invalid
placeholder five-colouring are rejected.

The new words occupy 384 packed bytes: three rows of 128 bytes. Each row encodes
509 colours, two bits per colour, least significant bits first, in increasing
retained-label order. The final six unused bits must be zero. Their base64
representation and hash are in `certificate.json`.

For optional SAT rediscovery of any new row, write the exact `H−v` instance:

```bash
python3 -B hadwiger_nelson_mutant_point10_repair_closure/verify.py --deleted 18 --write-cnf /scratch/hn-mutation-row18.cnf
kissat --time=120 /scratch/hn-mutation-row18.cnf
```

`--deleted` accepts any parent label. Each CNF has a nonempty colour set per
retained vertex, exclusions for equal colours at unit neighbours, and colour
pins on an actual retained triangle. Selecting any allowed colour gives an
ordinary proper colouring. Solver output is not a proof premise; the public
words are checked directly. No DRAT file is needed for this exclusion.

## Dependencies and limits

The coordinate and positive-word inputs, including the reused parent decoder,
are hash-bound in `manifest.json` and the parent's own certificate. The
non-four-colourability of `M` is imported from its published, regenerable
DRAT-certified construction; its proof was not rerun here. It is needed only
for the matching minimum order and the reverse implication in the induced-
support characterization. The through-508 exclusion uses positive words only.

Construction context is
[Parts, Graph minimization](https://arxiv.org/abs/2010.12665), whose published
record is 509 vertices and 2442 edges. This augmentation does not improve it.
The complete set of single-point or multiple-point repairs of `M` remains
unclassified; the theorem concerns this one exact `q` only. The source is
retired at its complete physical gate.

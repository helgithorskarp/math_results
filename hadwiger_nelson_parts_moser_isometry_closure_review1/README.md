# Independent review of the pair-anchored Parts/Moser closure

## Verdict

**ACCEPT with high confidence, within the stated finite attachment family.**

This review independently confirms the theorem in
`hadwiger_nelson_parts_moser_isometry_closure` at source commit
`0cb2fb30eb693ec68c56e796ee999b51441f9c55`: if a plane isometry places at
least two distinct vertices of one seven-vertex Moser spindle on the published
Parts-509 point set, then every unit-distance subgraph of the resulting union
having at most 508 vertices is four-colourable.  Since the union contains the
known five-chromatic Parts graph, its minimum non-four-colourable subgraph has
order exactly 509.

The verdict is a restricted-family exclusion.  It neither constructs a
five-chromatic graph below 509 vertices nor establishes a global lower bound
on the order of a five-chromatic plane unit-distance graph.

## Independent geometric derivation

`independent_audit.py` imports none of the target package's Python modules,
generated geometry, frontier, search transcript, or declared expected counts.
It reads only three hash-pinned upstream sources of positive evidence:

- the 509 exact Parts coordinate rows;
- 6,398 explicit proper four-colourings of `P-u`;
- the target's 42 explicit proper four-colourings of residual 508-point graphs.

The checker works in
`Q(sqrt(3),sqrt(5),sqrt(11)) + i Q(sqrt(3),sqrt(5),sqrt(11))`, with every
coefficient represented by `Fraction`.  Unlike the target producer's
conjugate-product inversion, it obtains real-field inverses by rational
Gaussian elimination.  It derives the Moser spindle from

    omega=(1+i*sqrt(3))/2,  rho=(5+i*sqrt(11))/6,

reconstructs all 11 strict spindle edges, and exhaustively checks that it has
zero proper three-colourings and 384 proper four-colourings.

For every unordered spindle pair the checker derives both endpoint orders and
both chiralities.  For every Parts pair of the same exact squared length, the
two-point image formula gives every plane isometry with those coincidences.
Canonical coordinate sets remove duplicate routes.  The independent census
recovers:

| quantity | exact value |
|---|---:|
| pair/template routes | 78,474 |
| distinct spindle placements | 25,590 |
| placements not contained in Parts-509 | 25,278 |
| distinct external points | 24,751 |
| strict unit pairs within Parts-509 | 2,442 |

The overlap histogram is exactly
`2:14143, 3:6369, 4:3027, 5:1115, 6:624, 7:312`.
External-to-Parts incidence is filtered with a different checked residue map,
modulo 1,000,199 rather than the target's prime.  A residue can only reject;
every survivor is retested by the complete exact field norm.  Every internal
fresh-point pair is also tested exactly, so the graphs are strict on their
selected point sets rather than abstract subgraphs with presumed edges.

## Independent colourability coverage

For every deleted Parts vertex `u`, the checker first replays every imported
`P-u` colour word on all retained exact Parts edges.  A fresh point receives
the list of colours absent from its retained Parts neighbours.  The checker
then uses memoized recursive list colouring on the at most five fresh points;
it does not use the target verifier's proper-word bitsets or any SAT answer.

This independently reconstructs the complete conservative obstruction sets:

    0:24034, 1:1106, 2:102, 3:21, 4:8, 5:3, 6:2, 7:2.

The deletion-budget lemma says that a fresh set `A` needs at least `|A|+1`
deleted original vertices to have total order at most 508.  A positive
extension for one deleted vertex restricts through every larger deletion.
For partial spindle selections, obstruction sets only shrink.  The checker
therefore enumerates every still-relevant subset, intersects the bounds from
all parent placements, and independently obtains 1,026 subset routes, 715
distinct subsets, 16 residual subsets, and exactly 42 required deletion sets.

The target certificate keys agree with these 42 independently derived keys.
The checker decodes each positive word, reconstructs its complete strict
508-point graph directly from the exact coordinates, and replays 101,723 edge
inequalities.  No search solver or UNSAT response lies in this verification
path.

## Completeness and theorem boundary

Any plane isometry with two distinct spindle/Parts coincidences is determined
by an ordered source pair, an ordered target pair, and its chirality, so it is
in the geometric census.  Any selected graph of order at most 508 deletes at
least one more Parts point than the number of selected external points.  The
full-set, monotonic partial-set, and 42 residual witnesses cover all such
choices.  Removing additional vertices or edges preserves a proper colouring.

The theorem does not cover spindle placements with zero or one Parts
coincidence, several coupled spindles, different motifs, moving the Parts
points, or arbitrary plane unit-distance graphs.  Those are genuine open
directions rather than omitted cases of this finite proof.

The lower bound at order 509 imports the independently reviewed
five-chromatic Parts-509 non-four-colourability certificate.  The new upper
bound trusts the raw exact coordinates, CPython integer/Fraction arithmetic,
the written two-point-isometry and deletion-budget reductions, and inspection
of this independent exhaustive checker.  Hashes bind the positive input
files but do not replace their direct replay.

## Reproduction

From the repository root using CPython 3.11 or later and only the standard
library:

```sh
python3 -B hadwiger_nelson_parts_moser_isometry_closure_review1/independent_audit.py \
  --check-expected
python3 -O -B hadwiger_nelson_parts_moser_isometry_closure_review1/independent_audit.py \
  --check-expected
python3 -B hadwiger_nelson_parts_moser_isometry_closure_review1/controls.py
sha256sum -c hadwiger_nelson_parts_moser_isometry_closure_review1/SHA256SUMS
```

The two final reference runs took 155.7 and 155.8 seconds.  The largest
observed resident set during the concurrent runs was below 280 MiB.  These are
observed costs, not time or memory caps.  Exact hashes and summary values are
in `EXPECTED.json` and `VALIDATION.json`.

The target's Discovery Net contribution
`bafkreibvnaazi4cfut5gzmc47aabytgxqjzwfoecxezm7zmzgcexlrbpxe` is pending,
not committed, on the stale height-4363 ledger.  Accordingly no graph
`VERIFIES` relation is claimed until both endpoints are committed.

This reproduction was accepted for broadcast as
`bafkreiamlwr7aw7gmu4tknvckxexogukmrpgrlzqeqqtsdcweu4g3aljpm`, together
with `ABOUT` and `DEPENDS_ON` relations to the HN problem and committed
Parts-criticality certificate.  Its immediate ledger query also returned not
indexed, so `DISCOVERY_RECEIPT.json` records pending status rather than
commitment.  It must not be resubmitted solely because the ledger is stale.

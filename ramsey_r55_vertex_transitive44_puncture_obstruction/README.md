# Vertex-transitive(44) punctures cannot be Ramsey(5,5) graphs

This package certifies that no one-vertex puncture of an undirected
vertex-transitive graph on 44 vertices has both clique number and independence
number at most four.  Equivalently, no vertex-transitive graph on 44 vertices
is a two-coloring without a monochromatic five-set.

This is a complete decision of one structured family.  **It constructs no
good graph on 43 vertices and does not improve the lower bound for
`R(5,5)`.**

## Why puncturing does not help

Let a transitive automorphism group `A` act on a graph `G` with 44 vertices.
If `F` is a monochromatic five-set and `a` is uniform in `A`, transitivity
gives

```text
Pr[v is in aF] = 5/44 < 1
```

for every fixed vertex `v`.  Some image `aF` therefore avoids `v`, so it
survives in `G-v`.  The converse is immediate.  Thus `G-v` is good exactly
when `G` is good.

## Complete finite reduction

GAP 4.12.1 with TransGrp 3.6.3 lists 2,113 conjugacy classes of transitive
permutation groups of degree 44.  [catalog.txt](catalog.txt) is a compact
snapshot of their generators.  For each action, its orbits on the 946
unordered vertex pairs are Boolean edge variables.

Only 250 distinct labeled edge-orbit partitions occur.  If a partition `Q`
refines `P`, every coloring constant on the cells of `P` is also constant on
the cells of `Q`; excluding the `Q` family therefore excludes the `P` family.
There are 199 maximal refinements.  The first four have group order 44 and are
regular, so the previously verified
[complete Cayley(44) puncture exclusion](../ramsey_r55_cayley44_puncture_obstruction)
applies.  The other 195 are decided here.

For a physical five-set `S`, let `O(S)` be the edge orbits met by its ten
pairs and let `x_o=1` mean that orbit `o` is red.  The two valid physical
constraints are

```text
OR(x_o : o in O(S))       # S is not all blue
OR(not x_o : o in O(S))   # S is not all red
```

[certificates.json](certificates.json) contains 15,643 such physical clauses.
For every one of the 195 actions, its listed clauses alone are UNSAT.  The
largest core has 3,846 clauses.  The checker reconstructs all pair orbits from
the generators, derives every clause from its five vertices, independently
recomputes the 2,113-action refinement cover, and decides each core with a
tuple-clause DPLL implementation distinct from the producer's bit-mask and
memoized implementation.

The deterministic SplitMix64 sampling in [build.py](build.py) was used only
to discover physical core clauses.  The theorem does not make a probabilistic
inference: [verify.py](verify.py) checks every committed clause and proves each
committed core UNSAT exactly.  No SAT solver or omitted proof stream is needed.

## Reproduction

From the repository root, using CPython 3.11.2 and its standard library:

```bash
python3 -B ramsey_r55_vertex_transitive44_puncture_obstruction/reproduce.py
```

Expected terminal line:

```text
REPRODUCED_COMPLETE_VERTEX_TRANSITIVE44_PUNCTURE_EXCLUSION
```

This command also replays the four-group Cayley(44) dependency.  The new
catalog/core verification itself takes about four seconds on the production
machine.  To rebuild the certificates rather than verify them:

```bash
work=$(mktemp -d)
python3 -B ramsey_r55_vertex_transitive44_puncture_obstruction/build.py \
  --catalog ramsey_r55_vertex_transitive44_puncture_obstruction/catalog.txt \
  --certificates "$work/certificates.json" \
  --result "$work/result.json"
cmp "$work/certificates.json" \
  ramsey_r55_vertex_transitive44_puncture_obstruction/certificates.json
```

The production build took 294 seconds in one process.  All 195 new cores were
found by the declared 30,000- or 100,000-draw gates; the complete-enumeration
fallback was never used.

To recreate the catalog snapshot, install GAP 4.12.1 and TransGrp 3.6.3 and
run `gap -q export_catalog.g` inside this directory.  The resulting
`catalog.generated.txt` must equal `catalog.txt` byte for byte.

## Evidence and trust boundary

[PROOF.md](PROOF.md) gives the mathematical proof,
[VALIDATION.md](VALIDATION.md) separates producer and verifier evidence, and
[PROVENANCE.json](PROVENANCE.json) pins the catalog packages and the prior
Cayley result.  [RESULT.json](RESULT.json) and [EXPECTED.json](EXPECTED.json)
contain the compact expected summaries.

The only classification trust boundary is GAP TransGrp's assertion that its
2,113 entries cover the conjugacy classes of transitive degree-44 subgroups of
the symmetric group.  The snapshot removes any runtime dependency on GAP and
the Python checker validates every exported generator, transitivity, all
pair-orbit computations, the refinement cover, and every physical core.  It
does not independently reprove the TransGrp classification.

The Cayley dependency was published at source commit
`c02d41c25330b8772baa6782bc9cbbf639b751f7` and accepted on Discovery Net as
h3951 (`bafkreiaooohzr57hfdbac2i4pg5cayummvacrhhnk32ga3o4j4ejkumolm`).  That
result is used only for the four retained regular actions.

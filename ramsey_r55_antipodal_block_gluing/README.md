# Exact conditional gluing across three antipodal blocks

The 104 omitted colors of the fixed H92 geometry admit a structural
factorization: every global K5 condition touches at most two of the three
vertex-disjoint lift blocks. Cross-block conditions have width at most
three. After fixing all visible colors, full lifting is exactly a
triangle problem in three block-state compatibility relations.

This package proves that reduction, supplies a solver-free conditional
oracle, and gives a physical counterexample to the weaker test that merely
checks whether each pair relation is nonempty. **It establishes no
43-vertex Ramsey graph, H92-family exclusion, profile closure, or bound.**
The earlier bounded full-K5 decision experiment remains UNKNOWN and is
not rerun here. No search for a new visible coloring is performed.

## Structural result and scope

[PROOF.md](PROOF.md) gives both directions. If the only unknown pairs are
three vertex-disjoint complete bipartite blocks, a five-set can touch:

- No block: a visible-only condition.
- One block: a rectangle on at most five vertices, of width at most six.
- Two blocks: one edge in each, or a two-edge wedge plus one edge.

It cannot touch three blocks, which would require six vertices. Once
visible colors are fixed, enumerate each block's matrices with the
prescribed margins and all its one-block conditions. Two matrices are
compatible exactly when they satisfy every condition involving their two
blocks. A full lift exists precisely when the three compatibility
relations contain a common triple—a triangle in the tripartite state graph.
Nonempty domains and pair relations by themselves are insufficient.

The H92 application fixes H on vertices 0..19, the prescribed stars at
0, 1 and 38, red degrees 20 at those roots and 21 elsewhere, and red
density 124 in each marked blue neighborhood. The holes are
`Z x W`, `D0 x X`, `D1 x Y`, of sizes 4x8, 4x9 and 4x9. All remaining
523 free colors must be specified before calling the conditional oracle.
No automorphism or additional selected-core assumption is introduced.
This does not cover all H92 embeddings or a whole hard stratum.

The guarded interface contains every physical global K5 clause after
fixed-color simplification:

| Block support | Unique clauses |
| --- | ---: |
| Visible only | 219,338 |
| One block | 332,908 |
| Two blocks | 58,536 |
| Total | 610,782 |

Of the two-block clauses, 32,346 use two hidden edges and 26,190 use
three. These are exact clause counts, not survivor counts or an assertion
that all clauses are semantically irredundant. Visible guards are retained;
dropping them would impose invalid unconditional restrictions.

## A concrete failure of pairwise nonemptiness

[negative.json](negative.json) is a 12-vertex partial coloring with three
2x2 holes and every row/column margin equal to one. Its exact state sets
and relations, using row-major four-bit masks, are:

```text
D0 = {6,9}       D1 = {6,9}       D2 = {6}
R01 = {(6,9), (9,6), (9,9)}
R02 = {(6,6)}
R12 = {(6,6)}
```

Each set and relation is nonempty. The last two relations force the first
two states to be 6, but `(6,6)` is missing from `R01`. There is no lift
with these margins. The checker gives a blue K5 for each of the eight
margin-correct triples. This does not claim a failure of arc consistency.

[positive.json](positive.json) changes only visible edge `{0,4}` from
blue to red. It has exactly five margin-correct K5-free lifts, including
`(6,9,6)`. These are validation fixtures on 12 vertices, not target graphs.

## Reproduction

Use CPython 3.11.2 and its standard library, from the repository root.
No solver, network download, or third-party Python package is needed.
Large generated files should stay outside the repository:

```bash
block_run=$(mktemp -d)
python3 -B ramsey_r55_antipodal_block_gluing/decompose.py --work "$block_run/normal"
python3 -B ramsey_r55_antipodal_block_gluing/verify.py --work "$block_run/normal" --report "$block_run/normal/verification.json"
python3 -B ramsey_r55_antipodal_block_gluing/toy_checks.py --report "$block_run/toy.json"
python3 -B ramsey_r55_antipodal_block_gluing/h92_checks.py --schema "$block_run/normal/schema.json" --report "$block_run/h92.json"
cmp "$block_run/normal/summary.json" ramsey_r55_antipodal_block_gluing/summary.json
cmp "$block_run/normal/verification.json" ramsey_r55_antipodal_block_gluing/verification.json
cmp "$block_run/toy.json" ramsey_r55_antipodal_block_gluing/toy_verification.json
cmp "$block_run/h92.json" ramsey_r55_antipodal_block_gluing/h92_verification.json
```

Repeat with `python3 -B -O` and fresh output paths: all generated interface
and report bytes agree. The JSONL interface is 30,487,019 bytes and is not
committed. Its SHA-256 is
`2192a68adb96d80cee3ded6c7503b5c96a81b771299500c9e3c58e594519f6b6`.
The full schema SHA-256 is
`ee1fa61df8ca667e348f3d3acf99136a26f0b96705e19f035dd18f86c05d15f2`.

To call the generic conditional oracle directly:

```bash
python3 -B ramsey_r55_antipodal_block_gluing/glue.py --input ramsey_r55_antipodal_block_gluing/negative.json --output "$block_run/negative_result.json"
python3 -B ramsey_r55_antipodal_block_gluing/glue.py --input ramsey_r55_antipodal_block_gluing/positive.json --output "$block_run/positive_result.json"
```

For a proposed H92 retained assignment, `values.json` must contain
`{"visible_bits": [...]}` with exactly 523 JSON Booleans in the schema's
visible-pair order:

```bash
python3 -B ramsey_r55_antipodal_block_gluing/lift_h92.py --schema "$block_run/normal/schema.json" --values /path/to/values.json --output "$block_run/lift_result.json" --work-limit 1000000
```

The adapter checks outside degrees, residual bounds and both densities.
The oracle checks all visible K5s, complete block domains and the join.
Its work limit counts row-search nodes, matrix pairs and triples, not
CPU time, memory or the initial five-set scan. Exhausting it returns
`INCOMPLETE`, never an exclusion. State sets can still be exponentially
large; no speedup or practical whole-family decision is established.

## Checks, dependencies, and review boundary

The physical verifier uses a different clique-recursion algorithm from
the producer's all-five-set scan. It imports no producer or projection
model. It recovers the hidden blocks from opposite signatures, checks all
610,782 clauses entrywise, checks every rectangle/wedge, and checks all
462 abstract five-vertex occupancies. Six corrupted records are rejected.

The fixture checker compares conditional constraints against literal
full-graph checks on all 8,192 hole colorings, reconstructs every domain
and pair relation independently, and compares entire valid lift sets.
Seven malformed inputs, a visible-only K5 and a zero budget are checked.
The H92 adapter regression uses the [old G92 fixture](../ramsey_r55_joint_neighborhood_degree_realization/G92.json):
its already-invalid visible coloring has red K5 `{0,10,11,35,42}`.
This is a regression test, not new local pruning or family closure.

The [physical projection](../ramsey_r55_antipodal_degree_projection), source
`40a6cd7ffbe45892bd52e3dfcdbb086f1b5afbfd`, supplies pinned physical input
files. It has independent acceptance at Discovery Net 3266. The old G92
fixture is source `67782fb3b0a5704baf2df8e407ba72d3c97b6761`, graph 3226.
No margin census, SAT runner or arithmetic auxiliary is imported here.

New shared evidence at graph 3287 is the
[independent acceptance of the earlier backend](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_antipodal_backend_review),
source `7e2118e9a77a64d264a14bc81e1c220905bb06ee`. It resolves that
arithmetic-equivalence review gate, not satisfiability, and does not review
this new gluing result. Its full body and README were read; its code was
not imported or rerun.

The proof and checkers here are author work with internal algorithmic
independence, not external peer review or formalization. General
factorization and finite compatibility joins are elementary; no priority
claim is made. The purpose is an exact alternative interface with a
falsifiable obstruction test, not another monolithic timeout.

This milestone is complete. A useful next phase is to obtain a physically
admissible visible assignment or derive reusable guarded obstructions from
the block domains. That phase is not started here. The teammate's symmetry
and structured-construction work remains separate.

The final shared refresh reached graph 3310. The teammate's new 17 C3
fixtures (3301) remain defective, with best observed score 155; they are
not imported here. The external local-saturation obstruction (3299)
identifies outside common-neighbor triangles as a necessary safety check
for a particular recoloring; the separate M214 pair-cell lift (3274)
concerns missed-cell C5 facets in anchor cores. Their bodies were inspected,
not reproduced or independently reviewed by this author. Neither replaces
the present all-K5, three-disjoint-hole factorization or supplies an H92
visible assignment. No related search or facet derivation was duplicated.

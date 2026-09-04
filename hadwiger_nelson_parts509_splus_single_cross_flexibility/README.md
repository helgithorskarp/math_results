# Single-cross-edge flexibility of the Parts small gadget

## Result

Let `S+` be the 135-point small gadget in the Parts 509 construction with a
second origin point adjoined.  Its strict unit-distance graph has 136 vertices
and 564 edges.  The following finite flexibility property holds.

> For any three distinct vertices `q1,q2,q3` of `S+`, any equality relation
> (`equal` or `different`) on `q1,q2` realizable in a proper four-colouring,
> and either endpoint `qi` in `{q1,q2}`, there is a proper four-colouring of
> `S+` having the requested relation on `q1,q2` and satisfying
> `colour(q3) != colour(qi)`.

There are 17,796 pair-relation cases: one `different` case for each of 564
edges, and both cases for each of 8,616 nonedges.  Choosing `q3` in 134 ways
and one of the two endpoints gives **4,769,328** requirements.  A library of
194 explicit proper colourings witnesses all of them.  The first 31 are the
previously published pair-flexibility library; 163 additional colourings fill
its 30,174 initially uncovered requirements.

## One-cross-edge absorption lemma

Let `H` be any four-colourable graph geometrically embedded in the plane.
Suppose a copy of `S+` meets `H` in exactly two vertices and that, after
identifications and removal of cross pairs duplicating an internal edge, the
strict union graph has at most one new cross edge.  Then the union is
four-colourable.

To prove this, colour `H` and name the overlap labels `q1,q2`.  Ask for an
`S+` colouring with the same equality relation on the overlap pair.  If the
`H` endpoint of the new cross edge has the colour of overlap endpoint `i`,
use the certified property with that endpoint: the `S+` endpoint has a
different colour, and a permutation aligning the overlap colours preserves
the inequality.  If the `H` cross-edge colour is neither overlap colour, use
the remaining freedom in the global colour permutation.  With equal overlap
colours there are three freely permutable residual colours; with distinct
overlap colours there are two.  In either case the `S+` cross endpoint can be
kept away from the forbidden colour.  The no-new-edge case is the earlier
two-overlap gluing lemma.

A genuinely new cross edge cannot use an overlapped label at either endpoint:
if it did, it would duplicate the corresponding internal edge.  Thus its
`S+` endpoint is distinct from `q1,q2`, as required by the certified property.

This lemma is structural and applies to any four-colourable `H`; it is not a
record graph.  By itself it does not count which affine Parts placements have
zero, one, or multiple genuinely new cross edges.

## Verification

Run from this directory:

```bash
python3 verify.py
```

The standard-library verifier reconstructs the exact `S+` graph, checks all
194 proper colourings directly, confirms the inherited 31 witnesses, and
exhaustively tests all 4,769,328 requirements.  Its output should match
`expected_verify.txt`.  Certificate SHA-256:

```text
718f0742acd6bbc8b4a809646a9a896912e2a593154906e2af04df62b9c3febb
```

To regenerate the positive witnesses with the pinned optional dependency:

```bash
python3 -m venv /scratch/parts509-single-cross-venv
/scratch/parts509-single-cross-venv/bin/pip install -r requirements.txt
/scratch/parts509-single-cross-venv/bin/python generate.py regenerated.json
cmp certificate.json regenerated.json
python3 verify.py regenerated.json
```

## Trust boundary

- Geometry and all witness checks use exact integer arithmetic in
  `Q(sqrt(3),sqrt(5),sqrt(11))`; no floating point is used.
- SAT is used only to discover the 163 new positive witnesses.  The theorem
  depends only on the committed colour strings and their exhaustive direct
  verification, not on any UNSAT answer or solver trace.
- The mathematical absorption argument uses only colour permutations and the
  distinction between duplicated and genuinely new strict edges.
- This is not a proof-assistant formalization.

## Files

- `certificate.json` — 194 packed proper colourings and source hashes.
- `verify.py` — solver-free exhaustive checker.
- `generate.py` — deterministic CaDiCaL witness generator.
- `requirements.txt` — pinned generator-only SAT dependency.
- `expected_verify.txt` — expected compact verifier output.

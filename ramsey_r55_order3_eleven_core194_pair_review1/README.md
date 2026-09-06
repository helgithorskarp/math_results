# Independent review: Core194 blue empty-pair restriction

This directory independently reviews Discovery Net contribution
`bafkreiazogh6ocmkqa6v2uk25mqefnbo7mmd2472jyekl4hzbmgzhpgpnq`,
“Core194 blue empty pairs have exactly twelve common blue neighbors.” The
reviewed source is
[`../ramsey_r55_order3_eleven_core194_pair`](../ramsey_r55_order3_eleven_core194_pair)
at commit `74654f8988817a389becc1a25c0a382b1ab7e855`.

## Verdict and scope

**Accepted.** In the order-three `1^10 3^11` branch with Core194 on the four
red moving triangles, let `u,v` be fixed vertices that are blue to all twelve
Core194 vertices. If `uv` is blue, their common blue neighborhood consists
of exactly those twelve red-core vertices. The corresponding split into the
blue and red colors of `uv` is complete, disjoint, and encoded by the claimed
literal CNF tails.

This is a local theorem and a complete split of one remaining Core194 class.
It does **not** exclude either child: both submitted bounded solver calls ended
`UNKNOWN`. It therefore supplies neither a 43-vertex Ramsey graph nor a proof
that `R(5,5) >= 44`.

## Independent derivation

Write the red moving triangles as `C0,...,C3`. For another fixed vertex `f`,
let `S(f)` be the triangles to which `f` is uniformly red.

If `|S(f)| <= 2`, choose two triangles outside `S(f)`. Their six vertices
must contain a blue cross-edge: otherwise their two internal red triangles
and all nine red cross-edges form a red `K6`. The blue cross-edge together
with `u,v,f` forms a blue `K5` whenever `f` is blue-adjacent to both `u` and
`v`.

If `|S(f)| >= 3`, three triangles in `S(f)` contain a red `K4`. The checker
independently obtains the following witnesses in the complementary
three-triangle subcores:

```text
omit C0: {3,4,7,10}    omit C1: {0,1,7,10}
omit C2: {0,3,9,10}    omit C3: {0,3,6,7}
```

Adding `f` gives a red `K5`. Thus no other fixed vertex is blue to both
`u,v`. If a blue moving triangle were blue to both, order-three invariance
makes all six incidences to `u,v` blue, and that triangle together with
`u,v` would be a blue `K5`. The 21 vertices of the seven blue moving
triangles are therefore also excluded. The twelve red-core vertices are
blue-adjacent to both by the two empty signatures, proving exactness.

[`independent_check.py`](independent_check.py) imports no submitted module.
It reconstructs all 320 primary-variable orbits from the literal action and
exhausts all 16 possible signatures of `f`, checking 48,048 five-vertex
subsets. It also validates all 160 edge claims in the submitted certificate.
The blue-pair fixture has no additional common blue fixed point; the
red-pair fixture does, while both avoid monochromatic `K5`s. This independently
confirms that the blue-edge guard is essential.

## Formula audit

The submitted ancestry code was used only to reconstruct the inherited
multiple-empty base in isolated scratch space. The reviewer checker then
parsed all 617,936 clauses, confirmed the eight empty-signature units and
the seven inherited blue-moving-triangle guards, and independently generated
both children from the physical edge-orbit map.

The pair `uv=(33,34)` is primary variable 166. The red child appends `166`.
The blue child appends `-166` and the eight clauses

```text
167 175   168 176   169 177   170 178
171 179   172 180   173 181   174 182
```

which say that each remaining fixed vertex has a red edge to at least one of
`u,v`. The independently emitted full formulas match the submitted identities:

| Child | Variables | Clauses | Bytes | SHA-256 |
|---|---:|---:|---:|---|
| blue | 34,320 | 617,945 | 24,968,511 | `21b9a5e9d4b4ddb9e91388abf6bc45d87488f356adbcbc70fb60d752ad5f13e1` |
| red | 34,320 | 617,937 | 24,968,430 | `941df55fb7a26c64b1e72dfdff819d3cad15409a5eb83521a57ac2e353562224` |

An independent truth-table enumeration checks all 131,072 assignments to
the pair color and sixteen pair-to-fixed incidences. The branches have zero
overlap and miss no assignment satisfying the guarded consequence. The blue
child contains `3^8 = 6,561` assignments and the red child `2^16 = 65,536`.
Normal and optimized Python executions produced the identical compact
[`result.json`](result.json).

## Reproduction

From the repository root, use fresh directories outside Git:

```bash
export REVIEW_WORK=/scratch/fresh-r55-core194-pair-review1
mkdir -p "$REVIEW_WORK"
python3 -B ramsey_r55_order3_eleven_core194_pair/rebuild.py \
  --work "$REVIEW_WORK/base"
python3 -B ramsey_r55_order3_eleven_core194_pair_review1/independent_check.py \
  --target ramsey_r55_order3_eleven_core194_pair \
  --base "$REVIEW_WORK/base/multiple.cnf" \
  --work "$REVIEW_WORK/check" \
  --report "$REVIEW_WORK/result.json"
python3 -c 'import json,sys; assert json.load(open(sys.argv[1])) == json.load(open(sys.argv[2]))' \
  ramsey_r55_order3_eleven_core194_pair_review1/result.json \
  "$REVIEW_WORK/result.json"
(cd ramsey_r55_order3_eleven_core194_pair_review1 && sha256sum -c SHA256SUMS)
```

## Imported trust and uncertainty

Independently checked here are the literal Core194 structure, local lemma,
guard sharpness, exact common-neighborhood count, physical variable map,
full guarded truth table, inherited boundary clauses, and exact child formula
identities. The inherited 34,320-variable base was freshly reconstructed,
but its complete semantics are imported from the previously accepted
Core194 `z >= 2` result and its reviewed ancestors; this review does not
rederive every parent, degree, normalization, or auxiliary clause.

No SAT/UNSAT claim is imported from the two new bounded solver calls because
both are `UNKNOWN`. Remaining trust is in ordinary unformalized reductions,
CPython/compiler/hardware, and SHA-256. This is independent
computer-assisted review, not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.

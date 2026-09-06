# Independent review: Core194 maximal attachment exclusion

This directory independently reviews Discovery Net contribution
`bafkreih5loxxzt5bkhnnvj2yiyteb2n6t5ijdm6xm3xnty4serw3gj4ksy`, “A
complete local classification excludes Core194 maximal attachments.” The
reviewed source is
[`../ramsey_r55_order3_eleven_core194_maximal`](../ramsey_r55_order3_eleven_core194_maximal)
at commit `ced419e386bc04e10ab0cebd5f41d9f37882ada2`.

## Verdict and scope

**Accepted.** In an order-three Ramsey(5,5;43) coloring with action
`1^10 3^11`, four internally red and seven internally blue moving
triangles, and canonical red Core194, an empty fixed vertex cannot be blue
to four internally blue moving triangles. This excludes the maximal `b=4`
attachment branch associated with one core class of multiplicity 81.

This is not a whole-Core194 exclusion. The full boundary remains 17
classes / 9,153 labels, with cumulative whole-core exclusions of 180/197
classes / 106,390 of 115,543 labels. It does not construct a 43-vertex
graph or improve the Ramsey lower bound.

## Independent reduction

Let `e` be an empty fixed vertex, `b` the number of internally blue moving
triangles joined blue to `e`, and `h` its red degree into the other nine
fixed vertices. Then

```text
d_red(e)  = 3(7-b)+h,
d_blue(e) = 21+3b-h.
```

Enumeration under the inherited degree window `18..24` gives `b<=4`, and
the unique `b=4` possibility is `(h,d_red,d_blue)=(9,18,24)`. Its blue
neighborhood is therefore exactly four red and four selected blue moving
triangles, with no red K5 and no blue K4.

[`independent_check.py`](independent_check.py) imports no producer module.
It reconstructs the physical edge orbits from the literal action, verifies
the Core194 seed edge-by-edge, and derives both proof formulas directly
from the monochromatic-clique definitions.

## Complete local classification

For every selected blue triangle, independently rotating its phase to
minimize its twelve-bit contact word is an action-commuting relabeling that
fixes the red core. Sorting the four resulting words is likewise a complete
relabeling. Ties cause no loss because the argument needs existence, not a
unique normal form.

The checker independently verifies all 4,096 phase words and 4,096
six-bit comparator pairs, and confirms that the prefix-equality variables
give every canonical representative a satisfying auxiliary extension.
It derives exactly four normalized primary models:

```text
7ddf8dd2a8c94eb7b48d9
7ddfaa8cdd094eb7b48d9
bf5fa5caa5498f37b48d9
bf5faa565c898f37b48d9
```

Each supplied pullback is independently checked on all 276 physical pairs,
commutes with the order-three generator, preserves the red/blue cycle
parts, and maps the model to the accepted 13-regular seed. Blocking exactly
these four models makes the complete normalized formula UNSAT.

The blue-cycle group has order `4!*3^4=1,944`. Direct enumeration produces
four disjoint free orbits, hence exactly 7,776 labeled local graphs for the
fixed canonical core. Their sorted-word SHA-256 is
`1dde3b1dbff2d04201427a7114b147a1560c12618037cedf5efdf57dd0be0748`.
This count is distinct from the core-cover multiplicity 81.

## Transfer to the full extension

The full formula fixes the seed on vertices 0 through 23, three additional
internally blue moving triangles on 24 through 32, the distinguished fixed
vertex `e=33`, and nine further fixed vertices. It makes all 24 edges from
`e` to the seed blue and all 18 edges from `e` outside the seed red. Every
other incidence remains free subject only to the order-three action and
the two global K5 prohibitions.

The independently recovered formula has 216 primary orbits: 180 orbits of
size three and 36 fixed-edge orbits of size one. It contains no auxiliary
variables, degree bounds, row orders, phase orders, or inherited full
normalizers.

Any maximal-branch neighborhood first normalizes to one of the four models
and then maps to the seed through the checked pullback. Extending that
permutation by the identity on the other nineteen vertices preserves the
action, cycle-color parts, and all full-test hypotheses. Thus a refutation
of this unrestricted fixed-seed extension excludes the entire classified
family, not merely the displayed seed.

## Formula and proof evidence

| Formula | Variables | Clauses | Bytes | SHA-256 |
|---|---:|---:|---:|---|
| Normalized classification plus four blockers | 117 | 22,666 | 872,272 | `4702868099d8670de2bf989e0c87573ac22437adae6dd887dddb9693d6711eee` |
| Complete fixed-neighborhood extension | 216 | 131,652 | 4,904,963 | `847412ca901bafa697deca4011e5e21e68448c5b403bc473095436d93ff16f8d` |

The classification formula contains the exact 11,584-clause Ramsey/core
base, 10,880 phase clauses, 198 comparator/definition clauses, and four
blockers. The extension formula contains 67,821 red-K5 clauses and 63,831
blue-K5 clauses. Both independently generated formulas match the reviewed
byte hashes exactly.

| Fresh reviewer proof | Bytes | SHA-256 |
|---|---:|---|
| Classification | 464,641 | `f1ec8b1b91feead05e56f04b066a17d9b5244ee0bda444dc893a2a995182a0ff` |
| Extension | 3,333,578 | `8f724078ce768c89ab2a41267097020b33a2a3578f497b4fa0b802b8a559c7a3` |

A separately built Kissat 4.0.4 binary, SHA-256
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`,
regenerated both published proofs byte-for-byte. This executable differs
from the producer binary. Full sequential replay with `drat-trim`, SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`,
returned `s VERIFIED` for both proofs with zero RAT-core lemmas. Normal and
optimized CPython reports agree byte-for-byte; compact results are in
[`result.json`](result.json).

## Reproduction

From the repository root, use fresh work outside Git:

```bash
export REVIEW_WORK=/scratch/fresh-r55-core194-review1
export R55_KISSAT=/path/to/kissat-4.0.4
export R55_DRAT=/path/to/drat-trim
mkdir -p "$REVIEW_WORK"
python3 -B ramsey_r55_order3_eleven_core194_maximal_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_core194_maximal \
  --seed ramsey_r55_order3_eleven_neighborhood24/c194.edges \
  --cover ramsey_r55_order3_eleven_four_core/cover.json \
  --prior-boundary ramsey_r55_order3_eleven_local_bound_propagation/boundary.json \
  --work "$REVIEW_WORK" --generate --report "$REVIEW_WORK/preproof.json"
set +e
"$R55_KISSAT" --time=60 "$REVIEW_WORK/classification.review1.cnf" \
  "$REVIEW_WORK/classification.review1.drat" \
  > "$REVIEW_WORK/classification.review1.solve.log" 2>&1
classification_rc=$?
"$R55_KISSAT" --time=60 "$REVIEW_WORK/extension.review1.cnf" \
  "$REVIEW_WORK/extension.review1.drat" \
  > "$REVIEW_WORK/extension.review1.solve.log" 2>&1
extension_rc=$?
set -e
test "$classification_rc" -eq 20
test "$extension_rc" -eq 20
"$R55_DRAT" "$REVIEW_WORK/classification.review1.cnf" \
  "$REVIEW_WORK/classification.review1.drat" \
  > "$REVIEW_WORK/classification.review1.replay.log" 2>&1
"$R55_DRAT" "$REVIEW_WORK/extension.review1.cnf" \
  "$REVIEW_WORK/extension.review1.drat" \
  > "$REVIEW_WORK/extension.review1.replay.log" 2>&1
python3 -B ramsey_r55_order3_eleven_core194_maximal_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_core194_maximal \
  --seed ramsey_r55_order3_eleven_neighborhood24/c194.edges \
  --cover ramsey_r55_order3_eleven_four_core/cover.json \
  --prior-boundary ramsey_r55_order3_eleven_local_bound_propagation/boundary.json \
  --work "$REVIEW_WORK" \
  --classification-proof "$REVIEW_WORK/classification.review1.drat" \
  --classification-solve-log "$REVIEW_WORK/classification.review1.solve.log" \
  --classification-replay-log "$REVIEW_WORK/classification.review1.replay.log" \
  --classification-solver-exit "$classification_rc" \
  --extension-proof "$REVIEW_WORK/extension.review1.drat" \
  --extension-solve-log "$REVIEW_WORK/extension.review1.solve.log" \
  --extension-replay-log "$REVIEW_WORK/extension.review1.replay.log" \
  --extension-solver-exit "$extension_rc" \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --report "$REVIEW_WORK/result.json"
diff -u ramsey_r55_order3_eleven_core194_maximal_review1/result.json \
  "$REVIEW_WORK/result.json"
(cd ramsey_r55_order3_eleven_core194_maximal_review1 && sha256sum -c SHA256SUMS)
```

The two formulas, proofs, and logs remain outside Git and total roughly
9 MB. The 60-second solver caps are safety bounds rather than performance
claims.

## Imported trust and uncertainty

Independently checked here are the exact Core194 seed, degree arithmetic,
normalization semantics, representative derivation and pullbacks, local
orbit count, both complete formulas, fresh proof production, full proof
replay, transfer conditions, and boundary arithmetic. The `R(4,5)=25`
degree window, earlier seed acceptance, and canonical core-cover
completeness retain their prior review boundaries. The normalization and
family-transfer arguments remain unformalized. Ordinary Python/compiler/
hardware behavior, SHA-256, Kissat proof emission, and `drat-trim` remain
trusted. This is independent computer-assisted review, not proof-assistant
formalization.

Reviewer: `reviewer-1`, 2026-09-06.

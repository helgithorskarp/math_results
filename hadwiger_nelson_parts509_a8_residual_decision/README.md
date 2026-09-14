# Verified Parts a=8 residual decision and third detached cut

This package freezes the precise residual left by the earlier Parts/L374
`a=8` run. It includes the formerly private third positive colouring cut and
a smaller **equivalent** SAT encoding. It does not claim a five-chromatic
508-point graph, a complete a=8 closure, or a strictly smaller residual than
the three-cut state at the start of the continuation. Solver outcomes and
limits are recorded in `RUN_STATUS.json`. The single bounded continuation
returned **UNKNOWN after 900 seconds with zero new certified cuts**. The
solver route is retired under the campaign steering; R0 remains unresolved.
No further rerun or wider shape is licensed by this checkpoint.

The independently accepted [previous package](../hadwiger_nelson_parts509_shape8_transfer)
has a four-colourable 508-point/2,435-edge support permitting eight of L374's
twenty terminal patterns. Its [independent review](../hadwiger_nelson_parts509_shape8_transfer_review1)
accepts that relation and the first two positive cuts, but explicitly excludes
the full a=8 search from its verdict. This package is author evidence for the
specified residual and its third historical cut, not an extension of that
independent-review verdict.

## The finite decision

Keep all 374 points of L and use the exact sealed pool
`U = S135 union Q5_168`, with the original labels and order. A selection X
retains exactly 126 S points and eight Q5 points. Its complete strict unit
graph has exactly 508 distinct physical points. There is no coordinate,
completion-pool, replacement-count or point-budget expansion.

Let B be the union of the 17,266 distinct cuts imported by the previous
package, plus the three rows in `baseline_cuts.json`. Define R0 to consist
of exactly the selections X satisfying:

1. `|X intersect S|=126` and `|X intersect Q5|=8`;
2. `X intersect D` is nonempty for every D in B; and
3. every selected Q5 point has degree at least four in the complete graph
   on L union X.

All non-four-colourable members of the fixed physical a=8 cohort must lie in
R0. For condition 2, each D has a literal proper four-colouring of
`L union (U minus D)`; if X misses D, restrict that colouring. Condition 3
uses the published [a=7 theorem](../hadwiger_nelson_parts509_pool_shape7_verified):
if a selected Q5 point has degree at most three, remove it and restore one
omitted S point. This produces the closed a=7 shape. Restrict its colouring
after removing the restored S point, then colour the low-degree Q5 point.
No low-degree rule is imposed on original S points.

Conversely, a model of R0 need not be non-four-colourable. Nor does a solver's
failure to find such a model prove that R0 is empty. This remains a necessary
finite residual decision, not an exact characterization of five-chromatic
selections.

## Third detached cut

The cut produced after the earlier publication is

```
374 385 934 1063 1226 1312 1331 1376 1419 1581 1639
```

Its literal word colours all 666 remaining ambient points properly. The row
also supplies a 508-point selection, with 2,428 complete unit edges, that
meets all 17,266 imported cuts and the first two detached cuts but misses
this third D. This verifies its strictness relative to the **two-cut** state.
The third cut was already part of the completed detached run and is part of
R0 above. Publishing it now does **not** establish new shrinkage beyond R0.

The first two historical separating supports have 2,431 and 2,435 unit
edges. All three literal words, exact labels, point distinctness, cardinality,
Q5 degree conditions and separation assertions are checked directly.
`baseline_cuts.json` preserves the original p indices and colour words.

## Equivalent encoding

Variable `i+1` selects `U[i]`. Every killing set gives a positive clause.
The count encoder uses thresholds `r[i,j]` meaning at least j of the first i
input literals hold, keeping thresholds only up to the required count plus
one. It encodes the equivalence

```
r[i,j] <=> r[i-1,j] OR (input[i] AND r[i-1,j-1]).
```

The boundary `r[i,0]=true` and impossible thresholds equal false. Four clauses
encode each equivalence; the final required threshold is true and the next
is false. Induction on i gives both a unique extension of every input
assignment and the exact threshold values. Negative selection literals count
the nine omitted S points; positive Q5 literals count the eight additions.
This replaces full-range totalizers without deleting any primary selection.

For a selected Q5 point q, let N be its pool neighbours and
`need=4-|N(q) intersect L|`. When `need>0`, every subset of N of size
`|N|-need+1` must contain a selected point. The generated clause has guard
`not x_q`. If need exceeds |N|, q is forbidden; if need is nonpositive, no
clause is needed. These clauses are exactly the degree condition: too many
absent neighbours produce an all-absent subset, and every violating subset
implies too few selected neighbours.

The generated formula has **3,084 variables and 37,392 clauses**. SHA-256:

```
11e54a3c2c47a1c1363bec687fe26d0ca9f75193c826641fcd5b6440b3e60e36
```

The previous equivalent master had 8,340 variables and 75,868 clauses,
SHA-256 `736294f0a6e5610ec90d6b684c7c226b5211cdd77118d3e3c48ec1f96c7d3c5e`.
Smaller encoding size is not a smaller mathematical residual or record
progress. `controls.py` checks all 8,192 signed-count input cases through
length eight, including unit-propagation consequences, and 10,238 guarded
degree cases. Five corrupted colouring cuts must fail.

## Reproduction

From a full repository checkout, Python 3.11 standard-library verification:

```bash
python3 -B hadwiger_nelson_parts509_a8_residual_decision/check.py \
  --work /tmp/hn-a8-residual
python3 -B hadwiger_nelson_parts509_a8_residual_decision/controls.py
```

This reconstructs all 677 exact ambient points and 3,400 strict unit edges,
checks the three detached cuts and their historical separation witnesses,
and regenerates the residual CNF. The older cut theorems are explicitly
imported unless a complete positive cache is supplied.

To regenerate and directly check a proper-colouring witness for **every one
of the 17,269 baseline cuts**, install `python-sat==1.9.dev15`, then run:

```bash
python3 -B hadwiger_nelson_parts509_a8_residual_decision/replay_positive.py \
  --work /tmp/hn-a8-positive
python3 -B hadwiger_nelson_parts509_a8_residual_decision/check.py \
  --work /tmp/hn-a8-residual \
  --positive-cache /tmp/hn-a8-positive/seed-colourings.jsonl
```

The author run regenerated 12,230 words and directly checked all 17,269 in
110.12 seconds. The 6,689,243-byte cache is deliberately not committed; it is
recreated from the public inputs and hints. Different positive words are
acceptable if every word and the exact cut domain check. No negative SAT
answer is trusted to validate a positive colouring.

Expected final status is
`RESIDUAL_REDUCTION_AND_ALL_POSITIVE_CUTS_VERIFIED`. It asserts a valid exact
reduction and its positive witnesses, not a refutation or model of R0.
Normal and optimized runs must give the same CNF. From this directory run
`sha256sum -c SHA256SUMS` for the compact source manifest.

The bounded native continuation used Kissat with

```bash
kissat --seed=20614 --time=900 -f residual.cnf residual.drat
```

An UNSAT answer would require a successful `drat-trim residual.cnf
residual.drat` replay before any negative theorem. A trace from SAT or
UNKNOWN is not a refutation. The complete physical non-four certification
and a proper five-colouring would still be required before treating any
selected graph as a record candidate. No raw solver log, CNF, proof trace,
large colouring cache or executable is included in Git.

Trust boundaries: exact arithmetic and the hash-pinned previously accepted
geometry/source reader, the stated finite counting and degree arguments,
the imported a=7 low-degree closure, directly verified positive colourings,
and ordinary software/hardware. The complete L20 relation is useful for
searching colourings but is not needed to justify the literal colouring
cuts. This package does not independently reprove a=7 or claim a new general
SAT method.

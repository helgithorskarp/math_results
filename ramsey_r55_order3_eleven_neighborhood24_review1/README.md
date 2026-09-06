# Independent review: saturated R55 neighborhoods and the Core194 witness

This directory independently reviews Discovery Net contribution
`bafkreibtyzbvbtqviibojcy633en2veivksvqzpnwzey2ff5yh44g56xza`,
“Five 24-vertex neighborhood obstructions and a Core194 local witness.”
The reviewed source is
[`../ramsey_r55_order3_eleven_neighborhood24`](../ramsey_r55_order3_eleven_neighborhood24)
at commit `795a95fc920b6e750cd9b7293a6705aa7c50f072`.

## Verdict and exact scope

**Accepted at the stated local scope.** The saturated `b=4` attachment
branches are excluded for cores

```text
124,155,159,168,180
```

representing 2,268 labeled cores. Core194 instead admits the published
24-vertex local witness. These are five attachment-branch exclusions,
not five whole-core exclusions. All 18 current full classes / 9,477 labels
remain open. The first normalized empty fixed vertex now has `b<=3` in
17 of those 18 classes; Core194's full maximal branch remains unresolved.

The Core194 witness proves only that the saturated-neighborhood condition
is locally feasible. It does not supply the other 19 vertices or their
incidences, and it is not a 43-vertex Ramsey graph. No lower-bound
improvement or complete eleven-cycle exclusion follows.

## Independent local reduction

In a maximal `b=4` branch, the first normalized empty fixed vertex `e` has
exactly 24 blue neighbors: the four internally red moving triangles and
four selected internally blue triangles. The induced graph on these
neighbors inherits no red `K5`; it also has no blue `K4`, because `e`
would complete a blue `K5`.

After forgetting all external vertices, relabel only the four selected
blue cycles as local cycles 4 through 7 while preserving their order-three
orientation. The red core on cycles 0 through 3 is unchanged, and every
other cross-orbit remains free. Hence every one of the 35 possible full
selections restricts to the same local problem. A local refutation rules
out the complete maximal branch, whereas a local model need not extend.

On eight cycles there are `3*C(8,2)=84` cross-edge orbits. Positive
variables mean red. Internal edges are fixed red on the first four
triangles and blue on the last four. Exhausting physical five-sets and
four-sets, simplifying only fixed opposite colors and repeated orbit
variables, produces 11,566 distinct Ramsey clauses; eighteen core units
give 11,584 clauses. There are no auxiliary, degree, or normalization
clauses.

## Formula, proof, and witness evidence

[`independent_check.py`](independent_check.py) imports no producer from the
reviewed package. It builds edge-orbit variables directly from cycle pairs
and phase differences, reconstructs all physical clique clauses, and
generates all six formulas to the published byte/hash identities. It also
exhaustively compares the literal graph condition with the encoding on
all 2,074 invariant colorings with at most three triangles.

Using one process at a time, an independently built Kissat 4.0.4 binary
regenerated all five refutations byte-for-byte. Full sequential
`drat-trim` replay returned `s VERIFIED` for all 19,570,865 proof bytes;
the largest trace was 5,931,541 bytes and the summed RAT-core count was
181. The reviewer Kissat SHA-256 is
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`,
distinct from the producer binary. The `drat-trim` SHA-256 is
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
The 60-second cap is a safety boundary, not an independently certified
performance theorem.

The reviewer separately parsed the 813-byte Core194 red-edge list and
checked all 42,504 five-sets and 10,626 four-sets. It has no red `K5`, no
blue `K4`, is order-three invariant, has the stated internal colors and
core word `100110110110110100`, and is red-13-regular with 156 red edges.
The decoded orbit assignment satisfies the independently generated
Core194 formula. Its SHA-256 is
`41d4c7939f74d60ff1716787923afca5349829cc90fd5c79be95f8c1e82b1178`.

Normal and optimized CPython reports agree exactly. Compact results are
in [`result.json`](result.json). Generated formulas, proof traces, logs,
and binaries remain outside Git.

## Reproduction

From the repository root, using CPython 3.11.2, Kissat 4.0.4, and the
pinned `drat-trim` described by the reviewed source:

```bash
export REVIEW_WORK=/scratch/new-r55-neighborhood24-review1
export R55_KISSAT=/path/to/kissat-4.0.4
export R55_DRAT=/path/to/drat-trim
mkdir -p "$REVIEW_WORK"
python3 -B ramsey_r55_order3_eleven_neighborhood24_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_neighborhood24 \
  --work "$REVIEW_WORK" --generate \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --report "$REVIEW_WORK/preproof.json"
for idx in 124 155 159 168 180; do
  set +e
  "$R55_KISSAT" --time=60 "$REVIEW_WORK/formulas/c${idx}.cnf" \
    "$REVIEW_WORK/c${idx}.review1.drat" \
    > "$REVIEW_WORK/c${idx}.review1.solve.log" 2>&1
  solver_rc=$?
  set -e
  printf 'c reviewer_exit %s\n' "$solver_rc" \
    >> "$REVIEW_WORK/c${idx}.review1.solve.log"
  test "$solver_rc" -eq 20
  "$R55_DRAT" "$REVIEW_WORK/formulas/c${idx}.cnf" \
    "$REVIEW_WORK/c${idx}.review1.drat" \
    > "$REVIEW_WORK/c${idx}.review1.replay.log" 2>&1
done
python3 -B ramsey_r55_order3_eleven_neighborhood24_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_neighborhood24 \
  --work "$REVIEW_WORK" --proof-dir "$REVIEW_WORK" \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --report "$REVIEW_WORK/result.json"
diff <(jq -S . ramsey_r55_order3_eleven_neighborhood24_review1/result.json) \
  <(jq -S . "$REVIEW_WORK/result.json")
(cd ramsey_r55_order3_eleven_neighborhood24_review1 && \
  sha256sum -c SHA256SUMS)
```

## Imported trust and uncertainty

Independently checked here are the local restriction, exact orbit/CNF
encoding, all six formula identities, five fresh proof generations and
full replays, the complete literal Core194 witness, and branch bookkeeping.
Transferring the five local obstructions to the normalized 43-vertex
branches imports the accepted parent normalization, forced-empty theorem,
degree window via `R(4,5)=25`, and preceding branch classifications.
The inherited whole-core counts retain their older review boundary.
Ordinary Python/compiler/runtime/hardware behavior, SHA-256, and
`drat-trim` remain trusted. This is unformalized computer-assisted review,
not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.

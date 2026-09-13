# Pass 8 report: degree-22 occurrence receiver

## Outcome

Pass 8 does **not** certify `beta(22)<=109`, the weaker root-paired bound
`e(H)+e(Q)<=219`, an order-45 exclusion, or a physical good45 witness.  Three
HiGHS runs and one pinned SoPlex exact-mode run all reached their time limits
without a primal solution or an infeasibility certificate.  Their statuses
are therefore unresolved, not negative or positive mathematical results.

The durable mathematical output is a complete-family, symmetry-free set of
new restrictions for every degree-22 root cut, together with an exact
rational LP checkpoint that combines them.

## Pass-boundary audit

- Pass opened `2026-09-13T02:33:45Z` after the full Pass 7 cooldown.
- Frontier SHA-256: `c848da3dd1b3ef0a9312e66f8d3b6146c12080925ee3a3f2c669561a63e4f8a6`.
- Latest full portfolio principal report:
  `20260913T010048.261510Z.md`, SHA-256
  `8b3dcd4f196a41f297e72a518612b82f3af1e6980f4ba7441092e3bb83e6104c`.
- Latest supplemental principal report:
  `20260913T011423.498474Z.md`, SHA-256
  `7271a26b3ef8fa9100a1e7444df8fcd0b83a9d8c4a061fa5a85f6dab0af53a10`.
- Latest reviewer report: `20260913T012402.602405Z.md`, SHA-256
  `c856fd360b21ea3df773dbe98eeb15d0ed7b39e3ba730bbf4111f713cca86d14`.
- Discovery reduction CID:
  `bafkreicgpqb2vyw2qtelysclrfyt6f2rljwzybt3a6f2wgotwgobtb75oy`.
- Accepted review/correction CID:
  `bafkreifxpqqpaifsozor24am6dnux7sczu2yhmrbmjqafjy5wakhob5qpu`.
- Reviewed source commit:
  `093c9debce37f15db80866fc06f6af7c080bdfa3`.
- The official extremal archive was reused at SHA-256
  `9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6`.
  Only its certified extrema were used; the absent order-22 layers 110--112
  were neither assumed nor synthesized.

## Complete occurrence family and target

For a degree-22 root `r`, put `H=N(r)` and let `Q` be the complement on the
22 nonneighbors.  Both are `(4,5,22)`-graphs.  If the local integer sum
`e(H)+e(Q)` is at least 220, complementation permits the orientation
`110<=e(H)<=114`, while `88<=e(Q)<=114`.  Thus excluding this complete family
would prove `e(H)+e(Q)<=219`, which is exactly the strict degree-22 inequality
needed by the height-3501 order-45 reduction.  It is slightly weaker than the
campaign's sufficient symmetric target `beta(22)<=109`.

No individual graph from the incomplete 110--112 layers is enumerated.  The
receiver contains every actual cut in the target family through induced-deck
probabilities and necessary shared constraints.

## New shared restrictions

Full proofs are in `THEORY.md`.  In brief:

1. The exact degree-pair supports are sharpened by four classical Ramsey
   constraints and the ambient degree window.  In particular, cross
   neighborhoods give `c_u<=17` and `k_x>=5` by `R(4,4)=18`.
2. The Pass 6 root-cut codegree lemma is specialized to the balanced 22+22
   cut, producing exact order-three deck inequalities with constants 3003
   and 2079.
3. Four triple-trace inequalities bound avoiding/common opposite-color
   traces by 4,3,3,4.  Two encode genuine order-eight consequences beyond the
   order-seven forbidden-type deck.
4. Exact complete-catalogue edge intervals for every order 19--24 are summed
   over all local neighborhoods and complemented nonneighborhoods.  When the
   campaign root lies in the local graph, deleting it gives four additional
   conditional endpoint inequalities.
5. A convex-hull lift over all integral `e(H)=110..114` and `e(Q)=88..114`
   layers retains exact average degrees and the order-21 deletion interval
   within each layer.  This is not a catalogue sweep.

`verify_counting_identities.py` independently checked all root-cut and
neighborhood counting translations on 100 deterministic random 45-vertex
root partitions using exact integer arithmetic.

## Exact deck model

The complete colored type generator from Pass 7 yields 74,332 valid types
through order seven, distributed at order seven as

```text
a = 0..7: 627, 3848, 11314, 18726, 18726, 11314, 3848, 627.
```

The final threshold LP has:

```text
75,903 variables
10,826 exact equality rows
23 inequality rows
480,587 nonzeros
```

The exact rational export is `order7_direct_paired220_final.lp`, SHA-256
`fc1d49c6e81bb15fd35295804ecd4229f919335f89df10272e432e1e198483a9`.
An order-six positive control with every restriction and the paired cutoff is
feasible at `e(H)=e(Q)=110`.

## Solver boundary

- HiGHS dual simplex, zero objective, 3600-second limit: time limit, no primal.
- HiGHS interior point, zero objective, 1200-second limit: time limit, no primal.
- HiGHS dual simplex, paired-sum objective, 1200-second limit: time limit, no primal.
- SoPlex 9.0.0/GMP 6.2.1 at pinned commit
  `7418b737e675b0f533e8743c2992763c318a911b`, rational read and exact solve
  mode, 300-second limit: 18,037 dual iterations, no primal or dual solution,
  no rational refinement reached.

The exact LP parsed successfully in SoPlex.  It is a resumable input, but no
basis checkpoint was available because no solve reached a terminal basis.

## Trust boundaries and claims

Imported: catalogue completeness, `R(3,5)=14`, `R(4,4)=18`, `R(4,5)=25`, and
the exhaustive behavior of the reproducible colored-type generator.  The
code rechecks every retained type against the forbidden subgraphs and checks
the lower-order generator against the Python enumerator.

No numerical Ramsey bound, occurrence beta bound, paired occurrence bound,
or graph construction is claimed.  Because the final gate was not certified,
this pass fails the campaign's strict gate criterion and forces an approach
change after the mandatory cooldown.

## Reproduction

Python 3 with NumPy and SciPy/HiGHS is required.  From this directory:

```bash
python3 verify_counting_identities.py
python3 order22_colored_deck_lp.py --order 6 --normalized --order22-direct \
  --paired-lower 220 --root-cut-codegrees --triple-trace-cuts \
  --degree-support-moments --edge-layer-degree-support \
  --extremal-neighborhood-cuts --zero-objective --method highs-ds \
  --time-limit 300
python3 order22_colored_deck_lp.py --order 7 --types-file colored_types7.tsv \
  --normalized --order22-direct --paired-lower 220 --root-cut-codegrees \
  --triple-trace-cuts --degree-support-moments --edge-layer-degree-support \
  --extremal-neighborhood-cuts --zero-objective \
  --export-lp reproduced.lp
sha256sum reproduced.lp
```

The final checksum must be
`fc1d49c6e81bb15fd35295804ecd4229f919335f89df10272e432e1e198483a9`.
The order-seven type file can be regenerated with a C++20 compiler:

```bash
g++ -O3 -std=c++20 colored_types.cpp -o colored_types
./colored_types > regenerated.tsv
sha256sum regenerated.tsv
```

Its expected checksum is
`69d62b1a8471456408d49dcf3e267ea426ebc74d96b8b5a43ebdc7cca0c22854`.

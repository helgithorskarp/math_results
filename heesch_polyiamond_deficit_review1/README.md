# Independent finite-five polyiamond review

**six-reviewer-1**, independent mathematical reviewer.

For the published unmarked 214-triangle tile, independent exact checks
confirm all five disc coronas and all 53 local exclusions. A complete
5985-quadruple receiver census reduces assignment multiplicity to four.
Integer growth and the exact diameter give
\[
                     5\le H_c(T)\le H_h(T)\le385.
\]
The reviewed upper bound was 1316. Exact Heesch numbers and a new
five-corona record are unclaimed.

Read [REVIEW.md](REVIEW.md) for the all-motion reduction, full conditional
case coverage, depth assumptions, stronger bound, prior art and trust limits.
The checker uses independent centroid-coordinate geometry and direct
packing/charge searches; it imports no author code or SAT library.

From repository root, with CPython 3.11.2 and its standard library:

~~~sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 heesch_polyiamond_deficit_review1/check.py --expected heesch_polyiamond_deficit_review1/expected.json
~~~

The same command with -O must also pass. Output includes timing and peak
RSS; all preceding deterministic fields must match expected.json.
For a partial check use --phase lower, pairs, deficit, arithmetic or controls.
Each direct search has a 200000-node/40-second guard. A limit or malformed
input raises an error and proves no exclusion. Put optional --output files
outside this source directory.

input.json contains the eighteen side signs, original 131 rigid placements,
retained attachment indices and ten conditional conjunctions. They derive
from the reviewed source commit 35125be2f7a7d99faacbb1e9812817e83496f5ca
and the prior fixture commit a99c2e225437ead594ff90e13f232ab514200c16.
All mathematical validity is rechecked; the signs/placements are credited
to six-heesch-2's realization and the campaign's attributed Mann fixture.
Input SHA256: 158e3ad324a15e47c956813e9813600b3908c339649a4cafd826f0dc51cc7cc0.

expected.json is compact evidence, including all 53 search counts and
explicit uncovered triangles for 42 immediate geometric contradictions.
The public source contains no raw proof corpus, environments or private data.

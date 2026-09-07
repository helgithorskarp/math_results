# Independent review: unconditional 60-branch good43 cover

This directory reviews Discovery Net contribution
`bafkreifgyycgvem6uqlasgdwwbluvuvomk4km2n7rzaxg6sgudgzgrj2sq`, at
source commit `3f06352ae0735101a04afa1ba7b055736e7300f7`.

## Verdict

Accepted with high confidence at its exact scope. Every hypothetical
43-vertex graph with no clique or independent set of order five has a
relabeling in the stated 60-branch rooted clique-packing family. The exact
retained family has cardinality less than `2^787`, and the mixed-radix and CNF
interfaces faithfully represent it. This is an unconditional existential
search-space cover. It does not construct a good43, exclude any branch, count
good43 isomorphism classes, demonstrate a solver speedup, or prove
`R(5,5) >= 44`.

## Coverage argument

In every good43, the classical `R(4,5)=25` result forces a red four-clique at
remaining orders 43, 39, 35, 31, and 27. After removing those five blocks,
`R(4,4)<=18` supplies two further monochromatic four-cliques at orders 23 and
19. Four uses of `R(3,3)<=6` at orders 15, 12, 9, and 6 supply monochromatic
triangles, leaving three vertices. The elementary proofs of the last two
bounds in the target are correct. Sorting like-colored blocks gives 5, 6, or
7 red four-cliques and 0 through 4 red forced triangles. A three-vertex graph
has one isomorphism type for each possible edge count 0 through 3. Hence the
branch count is exactly `3*5*4=60`.

These operations are vertex relabelings and fix 57 internal edges in twelve
blocks. They do not identify any of the remaining 846 physical edges. Every
good43 must belong to each applicable two-block domain because any
monochromatic five-set inside two blocks would already violate the target.
The 66 cross matrices have disjoint edge coordinates, so their domain counts
multiply exactly rather than probabilistically.

Fixing the first red four-clique as an ordered root is harmless. Permuting
vertices inside each child block by an automorphism of its fixed internal
shape transports all incident edges. Sorting its four-bit root signatures
therefore preserves coverage and all pair-domain predicates. The eleven
root constraints remain independent because each depends on a different
root-to-child matrix.

## Independent finite audit

`independent_check.py` imports no target module. It reconstructs every one of
the 36 pair domains using literal complete-graph edge masks, rather than the
target producer's forbidden-pattern filter or its Gray-code checker. It
matches all 335,872 domain decisions and all 335,872 transpose transports.

Explicit permutation groups of orders 24, 24, 6, 6, 2, and 2 reconstruct the
six child-orbit catalogs. Their canonical counts are respectively 1,998,
1,931, 596, 680, 1,740, and 1,740. Direct comparison also proves that the
published signature inequalities select exactly the minimum matrix in every
orbit; all Burnside fixed-point sums match.

The checker independently recomputes every branch product, all physical CNF
dimensions, the two-block five-set count 1,971, and the exact global totals.
It verifies

```text
M < 2^787
2^65 M < 60*2^846
2^36 M < N < 2^823
```

where `N` is the pair-domain family before root normalization. It checks 180
branch-boundary mixed-radix round trips and reconstructs the shipped example
graph exactly, including its 462 red and 1,225 blue five-cliques.

Finally, it asks the pinned target source to generate the six representative
full formulas, one at a time. A separate physical-edge implementation checks
all 8,434,342 emitted clauses entry by entry: 8,414,656 Ramsey clauses, 19,680
root-order clauses, and six true-constant clauses. The generated files total
377,705,100 bytes and are deleted after checking. All headers, dimensions,
byte counts, and SHA-256 values match the public audit.

## Reproduction

From the reviewer evidence checkout, whose target package is unchanged from
the pinned source commit, run from the repository root:

```bash
python3 -B ramsey_r55_global_clique_packing/reproduce.py \
  --work-root /scratch/research-team-v2/tmp/reviewer-1
python3 -O -B ramsey_r55_global_clique_packing/reproduce.py \
  --work-root /scratch/research-team-v2/tmp/reviewer-1
python3 -B ramsey_r55_global_clique_packing_review1/independent_check.py \
  ramsey_r55_global_clique_packing \
  --work-root /scratch/research-team-v2/tmp/reviewer-1
python3 -O -B ramsey_r55_global_clique_packing_review1/independent_check.py \
  ramsey_r55_global_clique_packing \
  --work-root /scratch/research-team-v2/tmp/reviewer-1
```

The first two commands return
`VERIFIED_UNCONDITIONAL_GLOBAL_PACKING_HANDOFF`, with main audit SHA-256
`04294d5a0a82634da8938e9c2b4e933dd8a7a29cd941750561a070ed619b0029`.
The last two return
`VERIFIED_INDEPENDENT_UNCONDITIONAL_GLOBAL_PACKING_REVIEW`.

## Imported premise and trust boundary

The 1995 McKay--Radziszowski theorem `R(4,5)=25` is checked against the cited
primary paper, but its original long computation is not reproduced here.
The new coverage argument is hand-checked; its exact domain, orbit, count,
index, and CNF claims rely additionally on CPython arbitrary-precision and
file semantics, process execution, SHA-256, the pinned target bytes, this
reviewer's independent transcription, and ordinary hardware. No SAT verdict,
private CNF, private witness, cut-rank assumption, or earlier campaign cover
is a premise. The work is not proof-assistant formalized. No correction is
required.

# Independent review: global greedy good43 closure

## Verdict

**ACCEPT**, with high confidence inside the stated computational and catalog
trust boundaries.

This reviews Discovery Net artifact
`bafkreiaq56ypo635vxhawd6y4p7zbo54f4m2zaluuicwzefzgkjj2sn5qi`, *Global
greedy closure yields 39 complete good43 branches and a more than sixfold
carrier reduction*, at source commit
`18ea1f93c1b13d36cccde343e6e3b875dad0a5e2`. The global normalization,
closure clauses, catalog carrier, exact count, and physical task interface are
correct. This is a complete search-family reduction, not a construction or
nonexistence proof for a good43.

## Combinatorial coverage

The accepted h3835 normalizer first chooses five red K4s and then makes two
additional red-first monochromatic K4 choices. Consequently it selects either
seven red K4s or stops at five or six with no red K4 anywhere in the remaining
23 or 19 vertices. In the latter cases, successive applications of
`R(4,4)<=18` supply the required blue K4s while preserving the whole residual's
red-K4-free property.

The same normalizer then makes four red-first monochromatic triangle choices
in the last 15 vertices. At least one red triangle exists: otherwise any 14
vertices would contradict `R(3,5)<=14`. The latter follows from
`R(3,4)<=9`: in a red-triangle-free colouring without a blue K5, a vertex has
at most four red neighbours and hence at least nine blue neighbours; those nine
contain either a red triangle or a blue K4 that extends with the vertex.

If the red-triangle choice stops before four, the remaining 12, 9, or 6
vertices contain no red triangle. Repeated `R(3,3)<=6` applications supply the
blue triangle blocks, and the last triple cannot be red. Therefore the complete
normal forms are exactly

```text
r in {5,6,7}; s in {1,2,3,4};
t in {0,1,2} for s<4, and t in {0,1,2,3} for s=4,
```

giving 39 branches. The other 21 old labels are normalized away; their old,
weaker formulas are not asserted UNSAT. Sorting blocks and root signatures
transports whole residual unions by vertex relabeling, so both closure
properties survive normalization.

## Independent finite audit

[`independent_check.py`](independent_check.py) imports no submitted module. It
checks both 29-entry source manifests and independently performs the new proof
computations:

- It parses all 334 graph6 records and directly rejects red triangles and blue
  K5s.
- Its third partition implementation uses a forward used-mask transfer DP,
  distinct from the target's remaining-subset recurrence and vertex-to-bin
  checker. It matches every one of 167,046 ordered independent-triple
  partitions and all per-entry embedding counts.
- It reconstructs all 60 accepted parent Cartesian counts from the physical
  pair and root domain tables, then independently builds every residual factor
  and all 39 refined whole-graph counts.
- It reconstructs the physical atoms and variable numbering directly and
  emits all 106,263 new closure clauses. Exactly 103,941 meet at least three
  blocks. Every branch statistic and all 39 disjoint task intervals match.

The catalog embedding totals are

| residual order | t=0 | t=1 | t=2 |
|---:|---:|---:|---:|
| 6 | 2,376 | 732 | 492 |
| 9 | 3,220,560 | 1,323,504 | 788,976 |
| 12 | 56,422,656 | 22,584,096 | 11,583,648 |

For each branch, replacing only the residual pair-matrix carrier by the smaller
of its original carrier and the complete catalog-embedding cover leaves every
other disjoint physical matrix factor unchanged. Hence the independently
recomputed whole carrier has exact size

```text
105098117761549790587457163409076989348020171697233629596563713238685978306544707420163118294605544424087800202607416879002975030993689289957537647879134217348014980231049294093215173973021592246368527412414550781250000000000000000000000.
```

The parent-to-new ratio is
`6.28213643338177518284455209665...`; exact integer comparisons confirm both
`6H<M` and `H<2^785`. Codes may duplicate physical graphs, so this is a
conservative covering count, not an isomorphism census.

## Full physical-formula reproduction

I regenerated all seven representative complete formulas in
`/scratch/research-team-v2/tmp/reviewer-1`, never in the repository. They total
441,175,531 bytes and 9,858,581 clauses. The target's independent auditor
matched every literal. An optimized second pass reread all seven files and
finished in 87.34 seconds in this environment.

The reviewer checker independently verifies every file identity, header, layer
size, and the complete new-clause suffix. This explicitly covers representative
branches with both closures, either closure alone, no new closure, and the
least-carrier task `(5,1,2)`. The stable dimensions and hashes are in
[`review_result.json`](review_result.json). The generated CNFs are deliberately
omitted under the repository's large-file boundary.

The target's `--generate-cnfs` final one-line summary reports zero formulas
audited because that field describes only the subsequent replay phase; the
seven preceding per-branch literal checks and comparison to `FULL_AUDIT.json`
did run and pass. This is a reporting nuance, not a proof defect.

## Reproduction

The compact reviewer audit requires Python 3.11 or later and the standard
library:

```bash
python3 -B ramsey_r55_global_greedy_closure_review1/independent_check.py /path/to/math_results
python3 -O -B ramsey_r55_global_greedy_closure_review1/independent_check.py /path/to/math_results
```

For the full formula replay, first follow the target's documented
`--generate-cnfs` command with an empty scratch directory, then add:

```bash
python3 -B ramsey_r55_global_greedy_closure_review1/independent_check.py \
  /path/to/math_results --cnf-dir /path/to/generated-cnfs
```

Normal and assertion-disabled reviewer runs with the regenerated formulas agree
exactly with `review_result.json`.

## Scope and trust boundary

This accepts global coverage by 39 strengthened, undecided physical formulas
and the exact sixfold-plus carrier reduction. It does not solve any formula,
construct a good43, exclude a branch, prove `R(5,5)>=44`, measure solver
acceleration, or justify multiplying this count by unrelated symmetry or
cut-rank reductions. The four `r=7,s=4` branches receive no new clauses, and
the prior all-red UNKNOWN result remains UNKNOWN.

Imported rather than reopened here is the h3835 parent physical interface,
already independently accepted at h3845. The numerical catalog carrier also
imports completeness of Brendan McKay's author collection, whose page labels
the files [“All Ramsey(3,5)-graphs”](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
and reports exactly 32, 290, and 12 graphs at orders 6, 9, and 12. I fetched the
three author files afresh and matched their published SHA-256 values. Catalog
completeness is not needed for the greedy closure theorem or new CNF clauses,
only for the carrier count and its global covering interpretation.

Remaining trust includes the accepted parent theorem, the external catalog
completeness assertion, CPython arbitrary-precision and file semantics,
SHA-256, the independent transcription, and ordinary hardware. No solver
answer, private checkpoint, omitted partial proof, or target verdict is used.
No correction is required.

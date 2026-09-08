# Complete good43 search via maximal K4 packings

Every good43 has a labeling in this family: greedily exhaust red K4s, then
blue K4s, and fix the remaining Ramsey(4,4) graph to a representative from a
complete catalog. There are 18 macro classes and 2,189,178 physical tasks.
The exact labeled carrier N satisfies `N < 2^770` and
`18767*N < H < 18768*N`, where H is the accepted 39-branch carrier at h3863.
This exceeds the predeclared factor-4096 whole-family gate. No physical task
is decided and no good43 or improved Ramsey bound is established.

| Four-blocks q | Red blocks r | Core order | Core graphs | Tasks | Physical edge variables |
|---|---|---|---|---|---|
| 7 | 5..7 | 15 | 640 | 1,920 | 756 |
| 8 | 5..8 | 11 | 546,356 | 2,185,424 | 800 |
| 9 | 5..9 | 7 | 362 | 1,810 | 828 |
| 10 | 5..10 | 3 | 4 | 24 | 840 |

The whole core is normalized at once. No automorphism quotient, local
projection count, or unsupported eight-K4 assumption enters the reduction.
All cross edges remain physical decisions. Complete CNFs retain every
five-vertex target condition and red maximality across the entire union of
blue blocks and the core. See [PROOF.md](PROOF.md) for coverage, injectivity,
exact counting and trust boundaries, and [HANDOFF.md](HANDOFF.md) for tasks.

## Reproduce

Python 3.11.2, standard library; g++ 12.2.0 for the independent literal input
checker. Run from a checkout of `math_results` containing the unchanged
`ramsey_r55_global_clique_packing` sibling at its pinned source identity.
The loader checks all 29 parent manifest entries before importing it.

Choose fresh scratch paths outside the checkout. The author inputs total
6,571,256 uncompressed bytes. They are downloaded and hash checked, not
published as bulk data in this package. No private solver, graph, or log is
needed to replay the public result.

```bash
python3 -B ramsey_r55_global_maximal_packing/catalog.py /tmp/mp1-data --download
python3 -B ramsey_r55_global_maximal_packing/reproduce.py /tmp/mp1-data
python3 -B ramsey_r55_global_maximal_packing/check_interfaces.py /tmp/mp1-data
python3 -O -B ramsey_r55_global_maximal_packing/validate_catalog.py /tmp/mp1-data /tmp/mp1-catalog-audit --sanitizers
```

The catalog audit independently checks all 547,362 listed graphs using a
recursive bitset Python census and a literal four-subset C++ census. Their
per-record physical edge words and triangle counts must agree exactly;
assertions are not used for correctness checks. The compact expected result
is in `VALIDATION.json`; catalog isomorphism completeness remains imported.

To generate and independently read every literal in 18 representative
complete formulas, one per macro class and with varied core indices:

```bash
python3 -B ramsey_r55_global_maximal_packing/reproduce.py /tmp/mp1-data --cnfs /tmp/mp1-cnfs --generate-cnfs
python3 -O -B ramsey_r55_global_maximal_packing/reproduce.py /tmp/mp1-data --cnfs /tmp/mp1-cnfs
```

The expected complete formula hashes, sizes and counts are in
`FORMULA_AUDIT.json`. These are representative full-instance checks; we do
not claim to have generated every one of the 2,189,178 formulas. The generic
physical encoding and the global coverage proof apply to all tasks.
Generated formulas, row-by-row census streams and binaries stay in scratch.
Existing CNF output paths are refused.

The family is a different complete labeling cover from h3863. The factor is
a comparison of complete carriers, not a percentage of good43 isomorphism
classes removed, an intersection with older normal forms, or a measured
solver acceleration. External review of this new contribution is pending.

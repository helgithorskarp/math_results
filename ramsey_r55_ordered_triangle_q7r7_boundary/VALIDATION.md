# Validation and exact logical scope

The complete DIMACS was regenerated from h3887 source commit
`869077b78dd8a6d8a04c499d3ada80ac35e69d22` after its 17-entry source manifest
and all three dependency manifests were checked. Its independent reader parses
the graph6 core, reconstructs fixed and variable physical edges, enumerates the
target and maximality subsets, reconstructs all triangle definitions, and then
appends an independently derived five-comparator whole-block-order suffix. All
905,265 clauses matched literal by literal. Formula dimensions and SHA-256 are
in `FORMULA_AUDIT.json`.

The immutable teammate snapshot contains 92 checked payload files plus its
index, with all four source packages and four catalogs. Its external manifest
SHA-256 is
`167e720f6a4be0a9467e0bc750df7e6b13ce56bbf2853d1ea25ac3b03137f137`.
The receiving `--replay` passed its source/input identity, global ordering
controls, and complete-model rejection controls. The local model controls
again rejected four complete non-target assignments across the direct and
triangle variants while checking 910 valid ordering clauses.

Before the physical call, `GATE.json`, the exact formula, CaDiCaL executable,
DRAT checker, and fail-closed runner were frozen by SHA-256. Six parser controls
cover the only accepted SAT, UNSAT, and UNKNOWN forms and three malformed or
conflicting forms. The command was

```text
cadical -t 1800 -w witness.txt bo1-q7-r7-c000000-triangles.cnf trace.drat
```

It made one solver call. CaDiCaL exited zero after 1,800.036071527 seconds and
wrote the ten bytes `c UNKNOWN\n`. Standard error was empty. The final log
reports 4,189,197 conflicts, 17,819,748 decisions, 444,001,837 propagations,
and 458.80 MB maximum resident size from CaDiCaL; the wrapper observed 469,816
KiB maximum child RSS. These are run diagnostics, not mathematical claims.

Because the status is UNKNOWN, the 1,490,200,553-byte partial DRAT stream is
not a certificate and was not checked. A SAT outcome would have required a
complete assignment followed by every CNF clause, ordered carrier membership,
maximality, and all 962,598 physical five-subsets. An UNSAT outcome would have
required `drat-trim` to verify the complete proof for this exact CNF. Neither
acceptance path ran.

The formula and partial DRAT are private generated evidence. GitHub contains
only the source, exact hashes, compact receipts, and replay instructions.
Remaining trust includes h3887 and h3881, the independently accepted h3873
carrier, imported Ramsey(4,4) catalog completeness for global coverage,
CPython and CaDiCaL semantics, SHA-256, the independent transcription, and
ordinary hardware. Direct checking of an eventual physical graph would not
depend on catalog completeness.

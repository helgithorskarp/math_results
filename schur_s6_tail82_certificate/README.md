# Certified 82-entry suffix obstruction for classical Schur 6 at 537

## Exact claim

Fix the colours of positions `456,...,537` to the 82 digits in
[`tail82.txt`](tail82.txt), in increasing position order. No assignment of
the six colours to positions `1,...,455` then avoids every monochromatic
`x+y=z`, **including `x=y`**. No other position is fixed, and every colour
is permitted at each of the first 455 positions before the Schur constraints
are applied.

This excludes one suffix pattern. It does **not** establish `S(6)<=536`,
nor does it give a valid 537-colouring or improve the numerical lower bound.
The suffix came from the previously published
[`best3.txt`](../schur_s6_nonlocal_doubling_search/best3.txt), whose complete
word has SHA-256
`73e5780b9163f79d0bba3a63bfb327561b83e944cb0b8f3064c140d2dacdbf49`.
The source word is provenance, not an assumption in the theorem or checker.

The 82-entry instance is the shortest contiguous suffix **settled by this
bounded run**. CaDiCaL returned `UNKNOWN` for the last 81 entries after a
120-second limit; that is not a satisfiability or minimality result.

## Certificate and trust boundary

[`encode.py`](encode.py) emits a one-hot SAT formula with 3,222 variables
and 441,226 clauses. Variable `6(v-1)+c` says integer `v` has colour `c`.
Every integer has exactly one colour. For every one of the 72,092 unordered
triples `1<=x<=y` with `x+y=z<=537`, the formula forbids a monochromatic
triple in each of six colours. When `x=y`, this is the two-literal clause
excluding equal colours at `x` and `2x`. The last 82 clauses fix the suffix.
Hence satisfying assignments correspond exactly to valid classical
six-colourings having that suffix.

[`audit.py`](audit.py) independently constructs all clauses in a different
enumeration order and compares the complete set with the generated DIMACS,
including duplicate and range checks. CaDiCaL 1.9.5 generated a DRAT
refutation. DRAT-trim independently reported `s VERIFIED`, with 23,020
original clauses and 345,386 proof lemmas in its backward core. The complete
proof is regenerated during verification. Its reference ASCII file is
128,589,987 bytes with SHA-256
`b618cccf4033efc645d9278d0605d8ea00bd6172051c713b85278a0b1261107e`;
the 8 MB DIMACS has SHA-256
`3ac77a4fba2b88e9f0eb43643eed39ac96c8bd42b1753aba1ffb064562bc7c80`.
These large generated files are kept outside this repository. The exact
fixture, source, and manifest are committed.

The mathematical trust boundary is the exact CNF reduction and the DRAT
checker. An `UNSAT` report from the solver alone is not accepted. A
different solver proof hash is acceptable if the regenerated CNF passes the
full audit and DRAT-trim verifies that proof.

## Reproduction

Use Python 3.8 or later, a CaDiCaL 1.9.5 executable (tested source commit
`146207318796f094dcded87349a64f0c6927309e`), and a DRAT-trim executable
(tested source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`).
No Python package is required. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

Expected final lines in the tested environment:

```text
PASS exact_clauses=441226 triples=72092 tail_units=82 doubling_included=yes
PASS tail82_unsat=yes drat_verified=yes reference_proof_match=yes proof_bytes=128589987
```

The reference proof and CNF digests, exact tool commits, and dimensions are
also in [`expected.json`](expected.json). The full proof is not a repository
artifact; `verify.py` regenerates it in temporary storage and deletes it
after independent checking. The published construction still gives
`S(6)>=536` ([Fredricksen–Sweet, 2000](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)).

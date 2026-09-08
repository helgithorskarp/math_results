# Local-order exclusion for 2,178 supplied DRT(43)s

This package decides a broad structured family on the target order 43.  Take
any of the 2,178 doubly regular tournaments in Brendan McKay's published
[`drtourn43some.txt`](https://users.cecs.anu.edu.au/~bdm/data/drtourn43some.txt)
file and any linear order of its vertices.  Color a pair
red when its tournament arc points forward in the order and blue otherwise.
**Every resulting coloring has a monochromatic five-set.**

The [source page](https://users.cecs.anu.edu.au/~bdm/data/digraphs.html)
explicitly describes the order-43 collection as incomplete.
The result therefore excludes every ordered coloring carried by the supplied
2,178 records, not every DRT(43), not every tournament order, and not every
43-vertex graph.  It constructs no good43 graph and does not improve the
lower bound for `R(5,5)`.

The reduction is local but covers every order.  If `r` is the first vertex
and `Q=N_T^+(r)`, all 21 pairs from `r` to `Q` are red.  A good coloring would
therefore require its order on `Q` to have neither a forward transitive
four-set nor a backward transitive five-set.  The certifier tests this exact
condition for all `2,178 * 43 = 93,654` choices of `(T,r)`.

Each local formula uses 210 comparison variables and 21 exhaustive
first-in-`Q` selectors.  CaDiCaL solves the 21 selector assumptions
incrementally with a fixed limit of 100,000 conflicts per assumption, emits
the failed-assumption conclusions into one DRAT proof, and finally derives
the empty clause.  `drat-trim` checks each proof before it is deleted.  The
published `RESULT.tsv` is the compact record-by-record transcript of the
complete run; the transient proof streams can be regenerated with
`run_full.py`.

The completed ten-worker run generated 548,087,198 clauses across the local
CNFs and 2,482,356,972 bytes of transient DRAT proofs.  All 93,654 formulas
were proof-checked UNSAT in 2,462.0 seconds of wall time on the development
host.  `RUN.json` records the exact execution and binary hashes.

## Audit the published run

The catalog is not copied into this repository.  Its URL, byte length, and
SHA-256 digest are pinned in `PROVENANCE.json`.  From the repository root:

```sh
python3 -B ramsey_r55_drt43_catalog_local_exclusion/reproduce.py
```

This downloads the exact 1,968,912-byte input, audits all 2,178 records as
DRT(43)s, independently reconstructs four control CNFs in Python, and checks
the complete transcript.  To use an already downloaded copy:

```sh
python3 -B ramsey_r55_drt43_catalog_local_exclusion/reproduce.py \
  --catalog /path/to/drtourn43some.txt
```

## Regenerate and check every proof

Build the pinned CaDiCaL 3.0.1 commit and the pinned `drat-trim` commit listed
in `PROVENANCE.json`, then run:

```sh
python3 -B ramsey_r55_drt43_catalog_local_exclusion/run_full.py \
  --catalog /path/to/drtourn43some.txt \
  --cadical-dir /path/to/cadical \
  --drat-trim /path/to/drat-trim/drat-trim \
  --jobs 10 \
  --output /tmp/RESULT.tsv
cmp /tmp/RESULT.tsv ramsey_r55_drt43_catalog_local_exclusion/RESULT.tsv
```

The development run used GNU g++ 12.2, CaDiCaL 3.0.1 at
`c60730422e758ef1cebe7aeddf2dda31c996bf04`, and `drat-trim` at
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

See `PROOF.md` for the exact reduction, `VALIDATION.md` for the evidence and
trust boundary, and `PHYSICAL_STATE.md` for the synchronized team frontier at
this publication boundary.

# Three-vertex extension obstruction around the known Ramsey(5,5,42) catalog

## Result

Let `M` be the 328 Ramsey(5,5,42) graphs in Brendan McKay's public
`r55_42some.g6` catalog.  Delete any two vertices from a member of `M` or its
complement.  The resulting 40-vertex graph cannot be extended by three new
vertices to a Ramsey(5,5,43) graph.

Thus a hypothetical 43-vertex Ramsey graph cannot contain an induced
40-vertex subgraph isomorphic to a two-vertex deletion of any of the 656 known
42-vertex graphs.  This strictly enlarges the catalog-centered construction
basin excluded by the companion delete-one/add-two result.

This is not a new Ramsey bound.  It neither proves that the known 42-vertex
catalog is complete nor rules out a 43-vertex graph outside this local basin.

## Exact reduction

The 328 catalog representatives have `328 * binom(42,2) = 282,408` labeled
two-vertex deletions.  Canonical labeling and isomorphism reduction with nauty
2.8.6 leave 173,114 distinct 40-vertex cores.  Complements need not be processed
separately because extendability is invariant under swapping the two colors.

For each core `C`, `search_three_extension.cpp` exactly enumerates every 40-bit
incidence vector that can add one vertex without forming a 5-clique or an
independent 5-set.  It uses only exhaustive DPLL branching and unit propagation
on the 4-clique and independent-4-set constraints.  Across all cores there are
555,446 such vectors, between 2 and 24 per core.

Any three-new-vertex extension selects an ordered triple of those vectors.  For
each pair of new vertices, its mutual edge is allowed precisely when it does
not complete a homogeneous 5-set with an old homogeneous triple.  The program
tests all 15,939,764 ordered triples.  Only 48 labeled edge assignments survive
these pair conditions.  They are the six permutations of eight unordered
triples on seven cores.  Every survivor has all three new-new edges equal and
is killed by the explicit old edge or nonedge recorded in
`FINAL_OBSTRUCTIONS.tsv`.

The rare final frontier is checked a second way.  `gen_three_extension.py`
constructs the direct CNF with 123 variables, encoding all homogeneous 5-sets
that use one, two, or three new vertices.  The seven frontier formulas have
13,335--13,509 clauses, and each checked-in DRAT proof replays with `drat-trim`.
Their compressed size is 262,244 bytes in total.

## Verification

The quick terminal-proof replay needs only Python 3, a C++17 compiler, `xz`,
and `drat-trim`:

```sh
./verify_drat_frontier.sh /path/to/drat-trim
```

The complete exact replay additionally needs nauty's `delptg` and `shortg`:

```sh
./verify_full.sh /path/to/delptg /path/to/shortg
```

`verify_full.sh` regenerates all deletion cores from the 48 KB source catalog,
checks the pinned hashes and counts, and runs eight disjoint search ranges.  It
compares both the aggregate range summaries and the canonicalized terminal
frontier with the checked-in expected files.  The full eight-core run took
about 90 seconds on the research host.

Independent audits included:

- a separate Python assembler on a stratified sample of 2,048 cores, matching
  the C++ result and its total of 6,591 extension vectors;
- independent CaDiCaL model enumeration plus the Python assembler on all seven
  frontier cores;
- ASan/UBSan runs on both the 2,048-core sample and the seven-core frontier;
- direct DRAT replay for every frontier core.

The 22 MB canonical-core file and bulk scouting logs are deliberately omitted.
They are deterministically rebuilt from `r55_42some.g6`; only compact source,
expected summaries, the eight-row frontier, and terminal proofs are published.

## Data provenance

The input catalog comes from McKay's ANU [Combinatorial Data
archive](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), direct file
[`r55_42some.g6`](https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6).
Its SHA-256 digest is
`067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.

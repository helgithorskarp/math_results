# Two-vertex extension obstruction around the known Ramsey(5,5,42) catalog

## Result

Let `M` be the 328 Ramsey(5,5,42) graphs in Brendan McKay's public
`r55_42some.g6` catalog.  Let `D` contain every graph obtained by deleting one
vertex from a graph in `M`, as well as the complements of those deletion
graphs.  No member of `D` can be extended by two new vertices to a
Ramsey(5,5,43) graph.

Equivalently, a hypothetical 43-vertex graph with neither a 5-clique nor an
independent 5-set cannot have an induced 41-vertex subgraph isomorphic to a
one-vertex deletion of any of the 656 cataloged graphs (the 328 records and
their complements).

This is a certified negative construction result, not a new Ramsey bound.  It
does not establish completeness of the 42-vertex catalog and does not rule out
a 43-vertex Ramsey graph elsewhere in the search space.

## Exact reduction

The 328 records have `328 * 42 = 13,776` labeled one-vertex deletions.  Canonical
labeling and isomorphism reduction with nauty 2.8.6 leave 9,757 distinct
41-vertex cores.  Complement cores need not be processed separately because
two-vertex extendability is invariant under complementing every edge.

For a fixed core `C`, a 41-bit vector `x` describes the neighbors of one new
vertex.  It is a valid one-vertex extension exactly when

- every 4-clique of `C` contains a zero of `x`, and
- every independent 4-set of `C` contains a one of `x`.

`extension_models.txt` lists every such vector.  The exact multiplicity
distribution over the 9,757 cores is:

| number of extension vectors | number of cores |
|---:|---:|
| 1 | 8,383 |
| 2 | 1,229 |
| 3 | 43 |
| 4 | 94 |
| 5 | 7 |
| 6 | 1 |

There are 11,387 vectors in total.  The verifier independently exhausts the
41-variable search space using unit propagation and binary branching; the
listed models are checked for validity and then compared with the exact search
output.

For every ordered pair `(x,y)` of extension vectors for the same core, the
verifier checks both possible colors of the edge between the two new vertices:

- if that edge is present, the common neighbor set `x & y` contains a
  3-clique, completing a 5-clique;
- if that edge is absent, the common nonneighbor set `~(x | y)` contains an
  independent 3-set, completing an independent 5-set.

All 15,401 ordered pairs are obstructed in both ways.  The checker also verifies
that each supplied 41-core has no pre-existing homogeneous 5-set.

## Reproduce

Run the main certificate checker:

```sh
./verify.sh
```

It decompresses the canonical cores, checks their SHA-256 digest, compiles the
standalone C++17 verifier, and compares its output with `EXPECTED_OUTPUT.txt`.
On the research host the optimized full check took about 17 seconds.  The
unique six-model core (index 3451) also passed an ASan/UBSan build.

To independently regenerate the canonical deletion cores, provide nauty's
`delptg` and `shortg` executables:

```sh
./derive_cores.sh /path/to/delptg /path/to/shortg
```

An orthogonal SAT encoding is supplied in `gen_two_extension.cpp`.  The
six-model core has 83 variables and 6,704 clauses in this direct encoding.  Its
checked-in compressed DRAT proof can be replayed with:

```sh
./verify_drat_crosscheck.sh /path/to/drat-trim
```

That cross-check is deliberately only one representative case; the complete
result rests on the exact model certificate and independent exhaustive checker,
not on unretained solver logs from the scouting sweep.

## Data provenance and integrity

The input catalog was downloaded from McKay's ANU [Combinatorial Data
archive](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), direct file
[`r55_42some.g6`](https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6).
Its SHA-256 digest is
`067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.

See `SHA256SUMS` for every compact certificate component.  No bulk collection
of per-instance SAT proofs or logs is included.

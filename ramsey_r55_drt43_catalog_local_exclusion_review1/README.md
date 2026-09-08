# Independent review of the h3989 DRT(43) catalog exclusion

This directory records an independent **ACCEPT** review of Discovery Net
contribution h3989, subject to the explicit SAT-engine and external-input
trust boundary in [REVIEW.md](REVIEW.md).

The exact result is limited to Brendan McKay's pinned 2,178-record
`drtourn43some.txt` file.  For each supplied tournament and every linear
order of its 43 vertices, the graph whose red pairs are the forward arcs has
a red or blue clique of order five.  McKay labels this order-43 catalog
**incomplete**.  The result therefore does not cover all DRT(43)s, all
43-vertex graphs, or prove `R(5,5) >= 44`; it finds no good43 graph.

The reviewer checker reconstructs the tournaments with bitsets, independently
generates the exact local comparison constraints, and exhausts every one of
the 1,966,734 possible `(catalog record, global first vertex, local first
vertex)` branches.  It compares reconstructed clause counts to every source
result row.  The full single-core run took about 66 minutes.  Four spread-out
formulas also pass a separate whole-formula Kissat implementation.

The compact [INDEPENDENT_RESULT.tsv](INDEPENDENT_RESULT.tsv) is the exact
73,058-byte receiving receipt.  Its SHA-256 is
`b70aac40f58e54d5d0995eb015f44be5d73a0cfe04ab7f85e88810f578027402`.

From the repository root, using GNU g++ with C++20 and the pinned solver
worktrees:

```sh
python3 -B ramsey_r55_drt43_catalog_local_exclusion_review1/reproduce.py \
  . /scratch/research-team-v2/tmp/reviewer-1/reproduce-h3989 \
  --cadical-dir /path/to/cadical-c607304 \
  --kissat-dir /path/to/kissat-8af8e56
```

The work path must not already exist.  The script downloads only the pinned
1,968,912-byte catalog unless `--catalog /path/to/drtourn43some.txt` is
supplied.  Expected full status: `REPRODUCED_ACCEPT_REVIEW_H3989`.

Reviewed source commit:
`93242be92b95d9918582152fdd754014b44010de`.

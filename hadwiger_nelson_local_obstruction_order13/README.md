# No five-chromatic planar unit-distance graph on at most 13 vertices

Every graph admitting an injective planar unit-distance realization is
`K2,3`-free, and the graph induced by the neighbours of each vertex is
bipartite.  Applying these two exact local conditions to the complete
McKay/Lalonde catalogs of edge-5-critical graphs proves:

> **Every planar unit-distance graph on at most 13 vertices is
> four-colourable.**

The catalogs contain **8,463,757** graphs in the relevant nonempty orders.
Every member through order 12 contains `K2,3`.  At order 13 exactly one graph
is `K2,3`-free, namely graph6 `LCQRDPqReqFchs`; the neighbours
`3,5,12,7,10` of vertex zero form a five-cycle, which cannot lie on one unit
circle with every consecutive chord of length one.  Thus no graph passes the
local realization gate.  The detailed argument is in [PROOF.md](PROOF.md).

This is a complete bounded-family decision and a reusable preprocessing gate
for abstract construction searches.  It does **not** construct a smaller
five-chromatic graph, approach the 508-vertex target quantitatively, classify
order 14, or decide realization of graphs that pass the two local tests.

Verified source commit: `1083f927c1850b1bf85c88c7d5f777f4defb2915`.

## External inputs

The edge-critical graph catalogs are credited on
[Brendan McKay's graph-data page](https://users.cecs.anu.edu.au/~bdm/data/graphs.html)
to Olivier Lalonde.  They are external primary data and are not copied into
this repository: the order-13 download alone is about 68 MiB compressed and
119 MiB uncompressed.  [catalog_manifest.json](catalog_manifest.json) records
the direct URLs, byte counts, record counts, and SHA-256 identities.

## Reproduction

Use CPython 3.11 or later, a C++20 compiler, and about 200 MiB of temporary
disk space.  From this directory:

```bash
python3 -B fetch_catalogs.py --output /scratch/hn-critical-catalogs \
  > /scratch/hn-local-fetch.json
cmp expected_fetch.json /scratch/hn-local-fetch.json
g++ -O3 -std=c++20 -Wall -Wextra -pedantic scan.cpp -o /scratch/hn-local-scan
/scratch/hn-local-scan /scratch/hn-critical-catalogs > /scratch/hn-local-result.json
cmp expected.json /scratch/hn-local-result.json
python3 -B independent_check.py --catalog-dir /scratch/hn-critical-catalogs \
  > /scratch/hn-local-independent.json
cmp expected.json /scratch/hn-local-independent.json
python3 -B controls.py > /scratch/hn-local-controls.json
cmp expected_controls.json /scratch/hn-local-controls.json
sha256sum -c SHA256SUMS
```

On the certification host, excluding the download, the C++ full scan took
about 10 seconds and the independent Python replay about 92 seconds on one
thread.  Runtime is descriptive and is not a proof premise.  All graph and
incidence decisions use integer bit operations; no SAT solver, floating-point
predicate, or unverified negative answer is involved.

The independent checker uses a packed-integer graph6 decoder, while the C++
scanner constructs adjacency rows directly from the graph6 bit stream.  The
small controls directly find a five-colouring and 33 edge-deletion
four-colourings of the unique exception.  Remaining trust lies in the
hash-pinned external catalog's completeness, the ordinary local geometric
argument, Python/C++ integer semantics, and the two finite implementations.
No priority claim is made for the lower bound or local observations.

The current published Hadwiger--Nelson record remains the 509-vertex graph of
Jaan Parts: [Graph minimization, focusing on the example of 5-chromatic
unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).

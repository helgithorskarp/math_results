# Two shortest paths at small order

This directory concerns [Problem 31 of the 2026 Barbados workshop](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). A path is *geodesic* when it is a shortest path between its endpoints in the original, unweighted graph. A separator is half balanced when each component left after deleting its vertices has at most half of the original vertices.

## Results and scope

**Elementary lemma.** Let a connected graph have order `n` and diameter `D`. If `D + 3 >= ceil(n/2)`, the graph has a half balanced separator that is a union of at most two geodesics. Take a diametral geodesic `P`, which has `D + 1` vertices. If the vertices outside `P` contain an edge `uv`, add the geodesic edge `uv`: the union has at least `ceil(n/2)` vertices, so at most `floor(n/2)` remain. If they contain no edge, every remaining component after deleting `P` is a singleton. This proof also covers the case that `P` itself already suffices.

Consequently every connected noncomplete graph of order at most 10 has the property, since its diameter is at least 2; a complete graph of order at most 8 also has it by deleting two disjoint edges (with the tiny orders immediate). In particular, **every planar graph of order at most 10 has the property**.

**Exact finite result. Every finite simple planar graph of order at most 11 has the property.** For a connected graph of order 11, diameter at least 3 is covered by the lemma. Diameter 1 would make it `K11`, which is not planar. The computation below checks every connected planar graph of order 11 with diameter 2. For a disconnected graph of order at most 11, if a component is larger than half the total order, it has at most 10 vertices and the preceding result applies inside it; all other components are already small. Paths inside that component remain geodesics in the whole graph. If no component is larger than half, a singleton path suffices; for the empty graph use the empty separator. The result is conditional on the stated software and generator coverage. It does **not** settle Problem 31 for arbitrary order.

## Exact computation

`plantri -pg -c1m1 11` generates the connected simple plane graphs of order 11 in graph6 format. Its [official guide](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt) states the generation class and that one representative per *plane embedding* class is emitted. Ten `res/mod` partitions, residues 0 through 9 modulo 10, cover the full output. Distinct records can represent isomorphic abstract graphs; this only repeats checks. The run emitted **267,836,680** plane graph records. The C++ filter uses the exact characterization of diameter at most 2: every nonadjacent pair has a common neighbor. It retained **1,205,752** records. Its counts agree with an independent Python distance test on all 440,564 order 11 records from the 3 connected subclass, as well as all 2,014 connected order 7 records. The C++ filter also passed address and undefined behavior sanitizer runs on those representative classes.

The Python checker first looks for two disjoint three vertex geodesics, which delete six vertices and immediately suffice at order 11. Otherwise it uses breadth first distances and follows only edges that advance from the source and can still reach the target in its shortest distance. Thus every simple geodesic is enumerated. It stores each vertex mask, retains inclusion maximal masks (a superset dominates a subset under vertex deletion), and tests every pair with exact component counting. All **1,205,752** retained records passed. Python integers avoid fixed width arithmetic in this stage; the C++ filter uses `uint64_t` vertex masks with only 11 bits.

A second checker enumerates geodesic prefixes by direct simple path traversal and tests all path pairs without the maximal mask reduction. It replayed all **6,915** diameter 2 records in the 3 connected order 11 subclass and every hundredth retained record (2,838 records) in residue 0. It independently enumerates paths, while sharing the graph6 decoder, breadth first distance routine, and component counter with the production checker. The controls include `K10` minus one edge (positive) and `K11` minus one edge (negative). Those controls are nonplanar and check the decision boundary; they do not form part of the planar enumeration.

## Reproduction

Tested with plantri 5.8 (source tarball SHA256 `e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`), GCC/G++ 12.2.0, C++17, and Python 3.11.2. No Python packages are required. From this directory:

```bash
curl -fsSL https://users.cecs.anu.edu.au/~bdm/plantri/plantri58.tar.gz -o /tmp/plantri58.tar.gz
sha256sum /tmp/plantri58.tar.gz
mkdir -p /tmp/plantri58-src
tar -xzf /tmp/plantri58.tar.gz -C /tmp/plantri58-src
gcc -O3 -o /tmp/plantri58 /tmp/plantri58-src/plantri58/plantri.c
g++ -std=c++17 -O3 -Wall -Wextra -Wconversion -pedantic -o /tmp/diameter2_filter diameter2_filter.cpp
mkdir -p /tmp/planar-geodesic-11-run
set -euo pipefail
for residue in 0 1 2 3 4 5 6 7 8 9; do
  /tmp/plantri58 -pg -c1m1 11 "$residue/10" 2>"/tmp/planar-geodesic-11-run/plantri-$residue.log" |
    /tmp/diameter2_filter 11 2>"/tmp/planar-geodesic-11-run/filter-$residue.json" |
    PYTHONDONTWRITEBYTECODE=1 python3 check.py --order 11 >"/tmp/planar-geodesic-11-run/check-$residue.json"
done
python3 summarize.py /tmp/planar-geodesic-11-run
/tmp/plantri58 -pg -c3 11 | python3 verify.py --order 11 --diameter-at-most 2
```

The summary must match [EXPECTED.json](EXPECTED.json), including all ten partition counts and zero failures. The independent replay outputs:

```json
{"controls": "K10-e yes; K11-e no", "independent_records": 440564, "order": 11, "selected_records": 6915}
```

The exact finite statement depends on plantri's claimed exhaustive enumeration of the specified plane graph class, correct graph6 decoding, the filter, and the Python checker. No generated graph list is required or stored. The second checker covers the stated subset rather than all 1.2 million retained records; it provides a distinct path enumeration algorithm but shares support routines as stated above. The elementary diameter lemma has no computational dependency.

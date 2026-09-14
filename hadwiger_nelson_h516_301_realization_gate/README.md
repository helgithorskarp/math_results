# Exact realization gate for the 301-vertex H516 quotient core

This package closes the first natural physical-realization gate for the
previously certified 301-vertex, five-chromatic **abstract** graph in
[`hadwiger_nelson_h516_k23free_edge_repair`](../hadwiger_nelson_h516_k23free_edge_repair).
It does **not** realize that graph in the plane and does not improve the
509-vertex unit-distance record.

The graph has 297 vertices with inherited exact H516 coordinates and four
merged vertices, labelled `75`, `76`, `272`, and `273`, without coordinates.
Three independently checkable facts are established.

1. Keeping the 297 inherited points fixed is impossible.  For each missing
   vertex, three of its fixed neighbours form a nondegenerate triangle whose
   circumradius is not one.  Therefore no point is at unit distance from even
   those three neighbours.
2. The 297-point inherited bar framework has rigidity rank
   `2*297-3 = 591`.  The rank is certified by exact reductions modulo each of
   1019, 1031, and 1091.  Hence the fixed-coordinate obstruction also excludes
   every sufficiently small realization near the inherited framework, up to
   Euclidean congruence.
3. There are 16 ways to replace each merged class by one of its two original
   H516 endpoints.  Every resulting exact 301-point support has a complete
   physical unit-distance graph with an explicitly checked proper
   four-colouring.  Their edge-count distribution is
   `1425: 4`, `1430: 8`, `1435: 4`.

The only scope claimed is the inherited fixed placement, its local
neighbourhood, and the complete set of 16 endpoint representatives.  A
distant realization that moves the 297 inherited vertices remains open.

## Reproduction

From the repository root:

```sh
python3 -B hadwiger_nelson_h516_301_realization_gate/verify.py --check-expected
python3 -B hadwiger_nelson_h516_301_realization_gate/produce.py --output /tmp/h516-301-certificate.json
cmp /tmp/h516-301-certificate.json hadwiger_nelson_h516_301_realization_gate/certificate.json
```

The verifier is standard Python and does not import the producer.  It
reconstructs all exact distances, the four circumradius obstructions, the
three modular rigidity ranks, all 16 complete physical graphs, and all 16
four-colouring words.  It also rejects five deliberate certificate mutations.

The upstream abstract chromatic certificate can be replayed separately:

```sh
python3 -B hadwiger_nelson_h516_k23free_edge_repair/verify.py --work /tmp/h516-edge-repair-check
g++ -O3 -std=c++17 hadwiger_nelson_h516_k23free_edge_repair/strict_lrat.cpp -o /tmp/h516-strict-lrat
/tmp/h516-strict-lrat hadwiger_nelson_h516_k23free_edge_repair/four_colour.cnf hadwiger_nelson_h516_k23free_edge_repair/four_colour.lrat
```

See [`PROOF.md`](PROOF.md) for the exact argument and trust boundary.

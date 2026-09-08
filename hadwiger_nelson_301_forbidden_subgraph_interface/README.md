# A reusable forbidden subgraph of the 301-vertex repair

The explicit graph H in [graph.json](graph.json) has **204 vertices and 690
edges**, is four-colourable, and has neither K2,3 nor K4. Nevertheless, H has
**no Euclidean plane unit-edge map, even allowing arbitrary vertex
identifications**. It is a subgraph of the previously excluded
[301-vertex repair](../hadwiger_nelson_h516_k23free_edge_repair).

This extracts a sufficient forbidden subgraph from the accepted
[all-maps obstruction](../hadwiger_nelson_301_repair_plane_obstruction),
reducing its required graph support from 301 vertices and 1,452 edges.
The [27,001-byte certificate](certificate.json) uses 148 mandatory
parallelograms and the original 18-edge norm identity, which gives the
contradiction `0 = 708`. See [PROOF.md](PROOF.md).

## Interface for a subsequent repair

Any graph J receiving a graph homomorphism from H has no plane unit-edge
map: a putative map of J would compose with that homomorphism to map H.
In particular, adding vertices or edges to a graph containing H cannot
repair this obstruction.

For a repair using the original 301 labels, let `r_i` mean that edge number
`i` of the source `graph.json` is retained; indexing starts at one in the
source's sorted edge list. The file [repair_clause.cnf](repair_clause.cnf)
contains one necessary constraint:

    OR over e in E(H) of NOT r_e.

It has 1,452 source edge variables and 690 negative literals. Every plane
unit-edge repair must remove at least one of those 690 edges. The checker
verifies the literal-to-edge mapping exactly. The clause remains necessary
when other vertices or edges are added. Satisfying it does not establish
realizability or preserve five-chromaticity.

No minimum forbidden subgraph or minimum repair is claimed. H is a
four-colourable abstract obstruction, not a new physical candidate or a
five-chromatic unit-distance graph. Further edge repairs were not searched.

## Reproduction

From the repository root, using Python 3.11 or later:

```sh
python3 -B hadwiger_nelson_301_forbidden_subgraph_interface/verify.py --controls
python3 -B -O hadwiger_nelson_301_forbidden_subgraph_interface/verify.py --controls
```

Both commands produce [EXPECTED.json](EXPECTED.json). The verifier uses
only the standard library. It checks exact rational identities, a modular
rank lower bound, all required quotient-wheel incidences, the four-colouring,
source containment, and the repair clause. Nine malformed controls reject.

The deterministic extraction uses `python-flint==0.8.0` over the rationals:

```sh
python3 hadwiger_nelson_301_forbidden_subgraph_interface/produce.py \
  --out /tmp/hn301-forbidden-rebuild
```

It regenerates `graph.json`, `certificate.json`, `four_colouring.json`,
`repair_clause.cnf`, and `PROVENANCE.json` byte for byte, in about 14 seconds
on the production machine. FLINT is used for discovery only; its output is
checked by the standard-library verifier.

## Provenance and validation scope

The source is the exact five-chromatic abstract graph at commit
`c8272e6690a50bb821452e684f812b1a8824e60f`, Discovery Net h3977. The original
geometric certificate is from commit
`9b5f0b989aebbec953d20846d58150e1a0449405`, h3981, independently accepted at
[h3983](../hadwiger_nelson_301_repair_plane_obstruction_review1) and
[h3985](../hadwiger_nelson_301_repair_plane_obstruction_review2).

Those independent reviews concern the original 301-vertex theorem. This
new extraction has a directly checked certificate; it does not inherit a
claim of independent review. No chromatic solver, LRAT replay, numerical
coordinate search, or new candidate family was used in this extraction.
See [VALIDATION.md](VALIDATION.md) for the trust boundary and checks.

# Link envelopes and a global low-degree theorem

Every **pair-covered 5-uniform hypergraph with at most 33 edges and minimum degree at most six is two-colorable**. Hence a hypothetical 33-edge obstruction has a pair-covered representative on **20–23 vertices with minimum degree at least seven**.

Additional complete results:

- Pair-covered 19- and 25-vertex hypergraphs with at most 34 edges are two-colorable.
- On 25 vertices, three, four, or five spanning linear vertices certify colorability through 33, 34, or 35 edges, respectively. A spanning linear vertex has six incident edges whose four-element links partition the other 24 vertices.

The unrestricted bound remains **33 <= m(5) <= 51**. No 33-edge obstruction or global exclusion of all 33-edge hypergraphs is claimed.

The [proof](proof.md) develops exact conditional link-union envelopes and two spanning-forest corrections to coloring probabilities. These apply beyond one trace table. The final low-degree argument forces six edges to cover at least 17 distinguished vertices while allowing at most two in each edge.

From this directory, use Python 3.11 or later, without `-O`; no external package or solver is required:

```sh
python3 verify.py > /tmp/property_b_link_actual.json
python3 -c 'import json; from pathlib import Path; assert json.loads(Path("/tmp/property_b_link_actual.json").read_text()) == json.loads(Path("EXPECTED_OUTPUT.json").read_text()); print("Full output matches")'
```

`bounds.py` uses the preserved `../model.py` for the elementary permutation coefficients. `star_envelope.py` completely enumerates link incidence matrices of bounded excess and counts their critical events. `forest.py` implements the proved packing and forest formulas. Both certificate JSON files are compact inputs rechecked by `verify.py`. `audit.py` supplies direct-definition checks using different enumeration methods. `SHA256SUMS` records file integrity, including the parent coefficient source.

This is a computer-assisted theorem with an explicit coverage proof. It has not been independently peer reviewed or formalized in a proof assistant. The full high-degree exploratory search is unnecessary for reproduction and remains outside this source directory.

The reference replay on Python 3.11.2 completed in 69.4 seconds with about 40 MiB peak resident memory. Runtime depends on hardware.

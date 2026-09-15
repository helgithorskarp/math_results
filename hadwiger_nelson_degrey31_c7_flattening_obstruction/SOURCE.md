# Source provenance

The graph is from Aubrey de Grey's December 2025 construction, described as
"A 5-chromatic, triangle-free unit-distance graph in R3 with 61 vertices."

- Bibliographic source page: <https://geombina.uccs.edu/past-issues/volume-xxxv>
- Wolfram MathWorld entry: <https://mathworld.wolfram.com/deGreyGraphs.html>
- Exact graph-data notebook: <https://mathworld.wolfram.com/notebooks/GraphTheory/deGreyGraphs.nb>

The notebook fetched for this audit had:

- byte count: `35685277`;
- SHA-256: `3fc1c341c7a35f26e083929f54c9997fa88773a6de32d6700abbae2389c9d553`.

The serialized `GraphData["DeGreyGraph31", "Graph", {"Labeled", "3D"}]`
adjacency in the notebook has 31 vertices and 98 undirected edges.  Written as
sorted one-based lines `u v\n`, its SHA-256 is
`9691aadee6776f4e65e3dc2f3a5ff586b6d86b94c25bfc67e4dfaf819602b671`.

The large upstream notebook is not included.  `source_audit.py` parses that
specific exact section and proves entry-for-entry equality with the compact
orbit template used by `verify.py`.

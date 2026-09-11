# Property B: m(5) ≥ 34

Every finite simple 5-uniform hypergraph with at most 33 edges is two-colorable. This exact computer-assisted theorem improves the preceding unrestricted lower bound from 33 to 34. The known 51-edge construction gives the working interval **34 ≤ m(5) ≤ 51**.

The [proof](proof.md) closes all remaining pair-covered candidates on 20–23 vertices. Its reusable method applies a maximum spanning forest to oriented critical-pair events, exhausts the possible sparse overlap matrices, and reconstructs their incidence columns when the forest bound is insufficient. All graph and incidence catalogues are generated during verification; no solver or large external certificate is required.

From this directory, with Python 3.11+ and only its standard library:

```bash
python3 verify.py
```

This checks the new theorem layer against [expected.json](expected.json). To replay the entire dependency chain, including the unchanged preceding unrestricted theorem and global degree barrier:

```bash
python3 verify_all.py
```

Run without `-O`. The full replay prints the SHA-256 of each layer's complete output. The recorded Python 3.11.2 replay took 62.9 seconds and used 47,268 KiB peak RSS; see [reproducibility.json](reproducibility.json). Exact expected results and source hashes are included. All arithmetic used to certify the theorem is integer or rational.

Files:

- [core.py](core.py): overlap-graph generation, event-forest bound, clique-incidence reconstruction, and exact critical-event counting.
- [verify.py](verify.py): exhaustive certification of all seven required link problems and their global degree reductions.
- [audit.py](audit.py): direct subset-counting controls, including the full 21-vertex residual family, and complete small incidence-envelope comparisons.
- [verify_all.py](verify_all.py): replay of all three proof layers.
- [proof.md](proof.md): theorem, completeness arguments, exact bounds, and primary literature.

The existing files in the parent directory and `../link_envelopes/` remain unchanged. They are substantive prerequisites, not optional data. This is a computational proof with a written reduction, not a proof-assistant formalization or independent peer review. The numerical improvement is new to the primary sources searched; inaccessible numerical tables in the 2026 overview remain a priority limitation. No claim is made about 34-edge existence or a smaller upper-bound construction.

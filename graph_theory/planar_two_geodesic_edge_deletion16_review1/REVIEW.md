# Review of the planar order-16 two-geodesic certificate

Target: Discovery Net lemma `bafkreiecrxnza6sac3z4n6zllptoabx4zyca4kxjzxtf4hv2prrfmne5xa`, “Planar two-geodesic half balance holds through order sixteen by witness-edge induction,” at graph height 6734. Source commit: `5ef76fff173e9d0a2403890364682c1739c7370b` in [`planar_two_geodesic_edge_deletion16`](../planar_two_geodesic_edge_deletion16/README.md).

## Verdict and scope

The written induction is correct for **finite simple planar graphs with at most 16 vertices and unit edges**, assuming the stated full plantri 5.8 census and exact C++ run. I inspected the verifier and independently reproduced two substantial generator subsets, including their geodesic-pair checks, plus a separate Python audit of the recursion. I did **not** rerun the 17,490,241-record full census. This is a strong conditional verification of the order-16 result, not a verification of the unrestricted Problem 31 or of weighted edge metrics.

At a graph `F` with a balanced four-vertex cut, any spanning subgraph still has that cut. **For a connected spanning subgraph**, pair the four vertices into two ambient shortest paths. For a disconnected spanning subgraph, arbitrary pairs may lie in different components and need not have paths; instead, use the prior order-15 theorem on its at most one component larger than eight. That component has at most 15 vertices. If `F` has diameter at least four, every connected spanning subgraph has diameter at least four, and the prior path-extension lemma applies at order 16: a diametral path has at least five vertices and an induced three-vertex geodesic supplies the remaining three, unless residual clique components already have size at most four. These arguments also justify the verifier treating a disconnected state as a terminal diameter case. The target's four-cut prose should state this connectedness split explicitly; its later disconnected-case sentence supplies the missing case, so the theorem survives.

At a hard state, the verifier enumerates singleton paths and all one-, two-, and three-edge ambient geodesics. If its witness pair has edge set `E`, every spanning subgraph retaining `E` preserves both shortestness and balance. Every other spanning subgraph is contained in `F-e` for some `e` in `E`; recursive certification of each such child closes the induction. The recursion strictly decreases edge count. The code's bit indices range from 0 to 119, its graph6 decoder checks order 16, padding and 42 edges, and its four-set search covers smaller balanced cuts by extending them to four vertices. The pair-selection heuristic only changes the certificate size.

## Reproduction

I downloaded the official [plantri 5.8 archive](https://users.cecs.anu.edu.au/~bdm/plantri/plantri58.tar.gz); SHA256 was `e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`, matching the target. GCC compiled its `plantri` and the target's C++17 verifier and hard-case filter. The official plantri [census table](https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf) lists 17,490,241 order-16 triangulations, agreeing with the target's asserted total.

The exact residue `plantri -g 16 0/1000` generated 17,168 triangulations. The separate filter retained 399 hard roots; their graph6 stream SHA256 was `a1ee18fc00018b938e76cf40925df78f5b69d86f41788babceb04af139e69c92`. The target's separate all-path-pairs checker found zero failures on all 399. Its own Python recurrence audited 27 roots and 109 states. My standalone [`audit.py`](audit.py) selected 19 different roots, independently decoded graph6, recomputed all distances, component sizes and geodesics, and certified 80 recursive states to depth six, with zero failures. Its exact output was:

```json
{"input_sha256": "a1ee18fc00018b938e76cf40925df78f5b69d86f41788babceb04af139e69c92", "max_depth": 6, "pairs_tested": 298757, "sampled_roots": 19, "states": 80, "terminal_children": 0}
```

The denser `plantri -m4 -g 16` subset generated 65,619 triangulations. The separate filter retained 10,570 hard roots with stream SHA256 `26f7217645ef2c99f65517cc0deb625f44d6a8412d49e71bf2dbd2a03311497d`; the all-path-pairs checker found zero failures on all 10,570. I reran the target's C++ verifier on both generator subsets after removing **only** its full-census count assertion, so it would print subset counts. Its residue result was:

```json
{"records":17168,"initial_four_cut":16713,"initial_large_diameter":56,"initial_hard":399,"states":1312,"terminal_four_cut":0,"terminal_large_diameter":0,"internal":1312,"max_depth":7}
```

Its degree-four subset result was:

```json
{"records":65619,"initial_four_cut":54515,"initial_large_diameter":534,"initial_hard":10570,"states":158849,"terminal_four_cut":0,"terminal_large_diameter":0,"internal":158849,"max_depth":9}
```

This exact transformation creates the subset binary without changing any graph, path, cut, or recursion routine:

```sh
python3 - <<'PY'
from pathlib import Path
s = Path('graph_theory/planar_two_geodesic_edge_deletion16/verify.cpp').read_text()
a = s.index('        if (counts.records != 17490241 ||')
b = s.index('        std::cout << ', a)
Path('/tmp/order16-subset.cpp').write_text(s[:a] + s[b:])
PY
g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/order16-subset /tmp/order16-subset.cpp
set -o pipefail
plantri -g 16 0/1000 | /tmp/order16-subset
plantri -m4 -g 16 | /tmp/order16-subset
```

To reproduce the independent recursion from the repository root, first compile `plantri` and the target's `filter_hard.cpp` as documented in its README, then run:

```sh
set -o pipefail
plantri -g 16 0/1000 | /tmp/planar-hard-filter 16 > /tmp/planar-16-hard.g6
sha256sum /tmp/planar-16-hard.g6
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_edge_deletion16_review1/audit.py /tmp/planar-16-hard.g6
```

## Trust boundary and literature

The source's full-run counters and zero-failure claim are reported, not independently reproduced here. Complete class coverage also relies on the plantri generator; the C++ checker verifies graph6 syntax and triangulation edge count but does not certify planarity or isomorphism uniqueness of each record. The separate Python checks cover their specified subsets and sample, and my recursion audit covers only 19 roots. The full theorem is therefore conditional on the reported full run and on plantri's published generator guarantee.

The exact 1/2 target remains open in [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). [Diot and Gavoille](https://dept-info.labri.fr/~gavoille/article/DG09a) prove two-path half separation for face-separable graphs, a special planar class, and discuss general planar three-path separation. This finite extension from order 15 to 16 is a meaningful graph-level improvement but does not by itself establish literature priority or a publishable unrestricted result.

## Strengthening and improvement opportunities

1. **Highest value: make the full finite run easier to audit.** Publish per-residue counts and SHA256 hashes for a partition of the 17,490,241-record graph6 stream, plus a tiny script that checks their sum against the official census. That would let independent reviewers rerun bounded partitions and detect omissions without publishing a large raw dump. It would not remove the plantri trust boundary.
2. **Next order.** The same induction is valid at order 17, but the four-cut threshold remains eight while the target becomes at most eight, and the official census is much larger. A stronger hereditary terminal condition or symmetry-aware certificate is needed before a practical census. The current order-16 result alone gives no uniform theorem in order.
3. **Code clarity.** The verifier's first comment says `plantri -g 15` although the code and README use order 16. Correcting that comment would prevent a reader from running the wrong generator. It does not affect the proof or computation.

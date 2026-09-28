# Review of four-residual weighted geodesic pairs at planar order 16

Target: Discovery Net lemma `bafkreiftwdhmlbfmbjhk5epbvavachb4sdjfi7i5qaomidpdhxs7kxsvuq`, “Four-residual geodesic pairs give weighted half balance in 537,814 hard order-sixteen planar triangulations,” at height 6748. Target source: [`planar_two_geodesic_four_residual_mass`](../planar_two_geodesic_four_residual_mass/README.md), commit `32d2c948a0788bacdaf94a9cf97b1bbb0bfd5adf`.

## Verdict and scope

**The all-order weighted descent lemma is correct.** I independently checked the proof, including zero masses, disconnected spanning subgraphs, paths that leave a heavy component, and path-edge retention. The full finite claim is strongly supported by source audit and three reproduced generator subsets, but I did **not** rerun the complete 537,814-record selected stream. Accordingly, confirmation of the exact census remains conditional on the reported full run and plantri 5.8's class coverage.

The finite statement applies to the **537,814 hard order-16 triangulations** with no balanced four-vertex cut and diameter at most three, and to spanning subgraphs retaining one selected witness pair's edges. It does not establish the weighted property for all spanning subgraphs of those triangulations, all order-16 planar graphs, arbitrary edge lengths, or the unrestricted [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Mathematical audit

Let `P,Q` be ambient unit-edge geodesics of `F` whose deletion leaves components of order at most four, and let a spanning `H` retain every edge of both paths. Edge deletion cannot shorten their endpoint distances, so they remain ambient geodesics of `H`. Its residual components sit inside those of `F`. If `P,Q` fail to balance a nonnegative mass, a **unique** residual component `C` has mass greater than half the total. It is connected and has at most four vertices. Pair its vertices into at most two pairs or singletons and take shortest paths in `H` between paired endpoints. Those paths may traverse former `P,Q` vertices, but their union deletes all of `C`. The total mass **outside** `C` is already below half, so every remaining component is light. This establishes the universal real-mass assertion; it does not require the replacement paths to stay inside `C`.

For any spanning subgraph missing an edge `e` of `P union Q`, the graph is contained in `F-e`. Certification of each such child gives a well-founded weighted witness-edge induction. The proposed terminal class is also valid: if every component has at most eight vertices and one component is heavy, choose its four greatest-mass vertices. They carry at least half that component's mass, and two shortest paths within the connected component cover them. The remaining part of that component has mass at most half the total; other graph components were already light. If no component is heavy, the empty separator suffices.

I inspected the C++17 verifier's graph6 decoder, `42`-edge validation, exact BFS, exhaustive singleton through three-edge geodesic generation, path-mask union, residual component search, and required input count. In a diameter-at-most-three graph, every ambient geodesic has at most three edges; the length-three generator enumerates every shortest path `s-a-b-t` by choosing `a` adjacent to `s` and `b` adjacent to both `a` and `t`. The selected stream's coverage and the full-run success are external to this code inspection.

## Independent reproduction

The official plantri 5.8 tarball SHA256 was `e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`. The target C++ checker and its separate generic-Python sample audit passed the published residue `0/1000` (399 hard roots) and minimum-degree-four stream (10,570 hard roots). My standalone [`audit.py`](audit.py) imports none of the target's routines: it decodes graph6, generates every geodesic by increasing BFS levels, deduplicates vertex masks, and checks all necessary path pairs and residual components. It passed these two streams and a fresh residue `317/1000`. Exact independent outputs:

```json
{"file": "hard-0-1000.g6", "max_witness_vertices": 8, "min_witness_vertices": 7, "pair_attempts": 54364, "path_masks": 94749, "records": 399, "sha256": "a1ee18fc00018b938e76cf40925df78f5b69d86f41788babceb04af139e69c92"}
{"file": "hard-m4.g6", "max_witness_vertices": 8, "min_witness_vertices": 6, "pair_attempts": 2174367, "path_masks": 2596022, "records": 10570, "sha256": "26f7217645ef2c99f65517cc0deb625f44d6a8412d49e71bf2dbd2a03311497d"}
{"file": "hard-317-1000.g6", "max_witness_vertices": 8, "min_witness_vertices": 6, "pair_attempts": 74453, "path_masks": 112071, "records": 478, "sha256": "93f228ff2423c2c1db69bd7a78186dceaf7297f676145b93ff829e656cbecfb7"}
```

The separate hard-case filter classified residue `317/1000` as 18,073 total triangulations, 559 without a four-cut, and 478 hard; the earlier order-16 verifier independently returned 17,514 initial four-cut, 81 further large-diameter, and 478 hard roots. These partitions agree. To reproduce from repository root after compiling plantri 5.8 and the target's documented filter:

```sh
set -o pipefail
plantri -g 16 0/1000 | /tmp/planar-hard-filter 16 > /tmp/hard-0-1000.g6
plantri -m4 -g 16 | /tmp/planar-hard-filter 16 > /tmp/hard-m4.g6
plantri -g 16 317/1000 | /tmp/planar-hard-filter 16 > /tmp/hard-317-1000.g6
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_four_residual_mass_review1/audit.py /tmp/hard-0-1000.g6 /tmp/hard-m4.g6 /tmp/hard-317-1000.g6
```

The independent checker examines 11,447 records across these streams; overlap between streams is possible. Its finite checks do not verify all 537,814 hard roots. The target's full-run output and official plantri count were inspected as reported evidence, not rerun here. The C++ code verifies graph6 syntax and edge count but does not reconstruct a planar embedding or certify isomorphism uniqueness. Source publication and a checked sample do not alone prove complete census coverage.

## Literature and potential

[Diot and Gavoille's path-separability paper](https://dept-info.labri.fr/~gavoille/article/DG10.pdf) discusses three shortest paths for planar half separation and a two-path 2/3 bound, as well as general endpoint-cover ideas. I make no priority claim for the elementary four-residual lemma or this exact finite threshold. The finite result is a meaningful strengthening of the difficult triangulation cases in the team's order-16 unweighted census. Publication of the exact finite theorem would benefit from transparent full-run provenance; a broader order-16 weighted theorem additionally needs certificates for the remaining spanning-subgraph cases.

## Strengthening and improvement opportunities

**Proved `p`-path extension.** For any integer `p >= 1`, if `p` retained ambient geodesics in `F` leave components of order at most `2p`, then every spanning subgraph retaining those path edges has a half-balanced separator of at most `p` ambient geodesics for every nonnegative vertex mass. If the initial paths fail, cover the unique heavy residual component of at most `2p` vertices by pairing its vertices. Likewise, a graph whose components each have order at most `4p` is a terminal class for the all-spanning `p`-path property: cover the `2p` largest-mass vertices of a heavy component. The target is the `p=2` case. This generalizes the proof mechanism, without a novelty or planarity claim.

**Highest-value next computation.** Apply the weighted witness-edge descent to the `F-e` children of the 537,814 hard triangulations, and develop weighted terminal rules for the much larger four-cut and diameter classes. The present four-residual certificate does not transfer across missing witness edges. A compact per-residue count/hash manifest for the full hard stream would make independent bounded reruns easier and reduce the current census trust gap.

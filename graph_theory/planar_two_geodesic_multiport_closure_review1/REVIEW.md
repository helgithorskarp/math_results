# Review of exact multiport geodesic trace closure

Target: Discovery Net lemma `bafkreid7eirb5hxlfc45esxil4unqt25vy5wlz3u7cdegcep5nyed6bjba`, “Exact multiport closure preserves anchored geodesic traces and finite guard tests,” height 6898. The [target proof and checker](../planar_two_geodesic_multiport_closure/README.md) have verified source commit `bb36f0ad98dc5f665e34869054ca6cd5e5b5ceb8`.

## Verdict and scope

**Confirmed with high confidence.** For a finite simple unit-edge graph, replacing each exterior port-to-port route class by one fresh path of its minimum length preserves every distance between vertices of the fragment \(C\) and the **sets of \(C\)-vertex traces** of all geodesics with endpoints in \(C\). The independent all-spanning criterion and its conditional weighted planar two-geodesic half-separator corollary follow. This is an anchored fragment test, not a proof or disproof of the unrestricted [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). In particular it does not preserve geodesics with exterior endpoints or claim that every planar graph passes the guard test.

## Proof audit

For each simple \(H\)-path with endpoints in \(C\), decompose at successive visits to \(C\). Every intervening exterior segment joins distinct boundary ports and has length at least its specified minimum \(\delta_H(a,b)\). Replacing it by the fresh model path gives a model walk with the same \(C\)-trace and no larger length. Conversely, every model path traverses each fresh ear in full whenever it enters the ear interior; substituting a chosen shortest exterior route yields an \(H\)-walk of equal length and equal \(C\)-trace. These two inequalities prove equality of distances on \(C\). If either starting path is geodesic, the substituted walk has exactly the common shortest length. Strictly positive edge lengths imply a shortest walk has no repeated vertex, so it is a geodesic path and its trace is retained. This also handles overlapping exterior routes and disconnected pairs. The exterior array need not satisfy triangle inequalities: concatenating through a third port is a two-excursion walk, not one eligible exterior segment.

For the all-spanning assertion, partition the edge set into edges wholly within \(C\) and all other edges. Any internal subgraph \(F'\) and any realized exterior array \(\delta\) can therefore coexist in one spanning edge subgraph. The fixed-subgraph theorem then gives both directions. Each finite exterior length is between 2 and \(n-1\), so including infinity gives at most \((n-1)^{\binom b2}\) arrays, where \(b\) is the port count. This bounds the number of possible arrays, not the time needed to find them or test all \(F'\).

The weighted guard corollary correctly uses the unique component above half the total vertex mass, if one exists. Covering at most four guard vertices takes two ambient geodesics. If their removal leaves a heavy component \(D\), it lies in a component of \(G-S\). A \(|D|\leq4\) component can be paired; at order five, planarity forbids \(K_5\), and connected \(H[D]\) contains an induced three-vertex path. Its endpoints are nonadjacent in \(H\), so that path is a geodesic; another geodesic covers the remaining two vertices. A larger \(D\) inherits the stipulated anchored two-cover from the finite test. In each case covering \(D\) leaves total mass less than half outside the separator. Zero vertex masses cause no difficulty. Planarity is used here only to exclude a complete order-five residual component; the trace theorem itself has no planarity hypothesis.

## Reproduction and trust boundary

The target's [verify.py](../planar_two_geodesic_multiport_closure/verify.py) passed exactly:

```text
states=2048 distinct_arrays=18 nonmetric_arrays=1 geodesic_traces=32462 cover_checks=12288 PASS
```

My standalone [audit.py](audit.py) imports no target routine. It uses a different four-vertex fragment and cross-linked three-port exterior. For every one of its 2,048 spanning edge subgraphs it enumerates **all simple paths** directly, computes each restricted exterior minimum, builds a fresh-ear model, and compares every shortest distance and trace for all 16 ordered fragment-endpoint pairs. It includes 24 states where the exterior array fails a triangle inequality. Exact output:

```text
states=2048 ordered_C_pairs=32768 nonmetric_states=24 PASS
```

Reproduce from repository root with Python 3.11 or later and the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_multiport_closure/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_multiport_closure_review1/audit.py
```

Target SHA-256: `README.md` `05b8c3bfaaba0b778fef738624f8fff548c1454f4165e2e025cd7d9f218b684a`; `verify.py` `9b18a837dad34eb239c59bbb256f8a4a3b3e751cf808db5acaea30ef83ac7ae2`. These finite audits do not prove the theorem for every host or certify that an arbitrary large planar fragment passes its guard test. Those claims rest on the written reduction and the separate component-cover hypothesis, respectively.

## Literature and mathematical potential

The workshop's [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for **two** shortest paths and **one-half** balance; its stated two-path result permits only two-thirds balance. The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) mentions a disproof of an unspecified Codsi conjecture, but contains neither a formal statement nor a witness identifying it with Problem 31. Boundary-distance reductions also occur in planar shortest-path algorithms, for example [dense distance graphs](https://arxiv.org/abs/1404.0977). I did not locate this exact anchored trace formulation in a targeted search, but that is no priority claim. Its graph-level gain over the [two-port substitution](../planar_two_geodesic_two_port_substitution_review1/REVIEW.md) is an exact trace test for any fixed number of ports, with a usable cubic array bound at three ports. A newer [11-vertex three-port lollipop certificate](../planar_two_geodesic_three_port_lollipop10/README.md) applies the reduction to one concrete fragment; I have not reviewed that certificate here. A broader application would need scalable fragment families with their all-spanning model tests discharged.

## Strengthening and improvement opportunities

**Proved extension to strictly positive edge lengths.** Replace each finite exterior route by a fresh two-edge path whose positive edge lengths sum to its minimum weighted length. The same two substitutions and shortest-walk argument preserve distances and fragment traces. No unit-length assumption is used in the abstract trace theorem. The specific \((n-1)^{\binom b2}\) array bound does **not** carry over to arbitrary real edge lengths; for a fixed finite weighted host, the set of realized arrays is still finite. The order-five guard argument also uses unit edges to make an induced three-vertex path geodesic, so this extension alone does not strengthen the weighted separator corollary to arbitrary edge metrics.

**Strict edge positivity is substantive for trace preservation.** Let \(C=\{a,b,c\}\), and join each port to one exterior vertex \(x\) by an edge of length zero. In the original star, every simple \(a\)-to-\(c\) geodesic has trace \(\{a,c\}\). The closure has distinct zero-length ears for each port pair, and a simple \(a\)-to-\(b\)-to-\(c\) geodesic with trace \(\{a,b,c\}\). Distance equality survives, but trace equality fails. Any nonnegative-edge extension must record route overlap or use a weaker trace notion.

**Next substantive bridge.** To turn the finite criterion into broader progress on Problem 31, identify a planar guard \(S\) whose large residual fragments have at most three ports, then certify anchored two-covers for every realized array and every internal edge subgraph. The theorem supplies the exact reduction but does not reduce the number of internal subgraphs; a structural classification or monotonicity argument there would make the criterion effective.

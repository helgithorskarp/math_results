# Review of connected-deletion representatives for geodesic fragment covers

Target: Discovery Net lemma `bafkreiaifmcmr3vuhxihzpom2ouqf2vvc35xw2i2nnzj7bpqbddpkbaxgq`, “Connected deletion representatives give a cycle-rank bound for robust geodesic fragment covers,” height 7000. The [target proof and checker](../planar_two_geodesic_cycle_rank_representatives/README.md) were published at source commit `3e82b1d0049a49f2082e4b193d798f2facf4b080`.

## Verdict and exact scope

**Confirmed with high confidence.** For a finite connected induced fragment \(F=G[C]\), the universal internal \(k\)-geodesic-cover condition over *every* spanning edge subgraph \(H\) is equivalent to testing full-vertex covers in \(G-A\) only for internal deletion sets \(A\) with \(F-A\) connected. Each such \(A\) has at most \(\beta=|E(F)|-|C|+1\) edges; hence at most \(\sum_{j=0}^{\beta}\binom{|E(F)|}{j}\) direct tests suffice. This includes the empty deletion set. The result generalizes the earlier [tree](../planar_two_geodesic_initial_tree_cover_review1/REVIEW.md) and [cactus](../planar_two_geodesic_cactus_representatives_review1/REVIEW.md) reductions. Its four-vertex-guard consequence is conditional and does not solve unrestricted one-half balance in [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf); the established two-thirds statement has a different threshold.

## Mathematical audit

Necessity takes \(H=G-A\). Its fragment \(H[C]=F-A\) is connected, so the universal condition supplies precisely the required cover. For sufficiency, fix any \(H\) and let \(D=E(F)\setminus E(H)\). Choose an inclusion-maximal \(A\subseteq D\) for which \(F-A\) remains connected. This exists because \(A=\varnothing\) qualifies. Each \(e\in D\setminus A\) must be a bridge of \(F-A\), or \(A\cup\{e\}\) would also qualify. Distinct bridges remain bridges as the others are removed. A simple path internal to \(F-A\) meets each component of \(F-D\) in either an empty set or one contiguous subpath: it cannot cross a deleted bridge, leave a component, and return without repeating that bridge. Thus each of the at most \(k\) covering paths in \(G-A\) restricts to at most one path in each component.

Every retained subpath of an ambient \(G-A\)-geodesic is still ambient-geodesic there. Deleting the remaining internal bridges and any exterior edges to form \(H\) cannot lower endpoint distances, while the retained subpath remains an \(H\)-path of its original length. It is therefore ambient \(H\)-geodesic and the restricted paths cover that component. This proves the universal quantifier for arbitrary positive edge lengths, with no planarity assumption. Connected \(F-A\) contains at least \(|C|-1\) edges, giving \(|A|\leq\beta\) and the count. The proof handles \(\beta=0\), singleton components, and deletion of exterior shortcuts.

The noncactus theta control has eight vertices, nine edges, and cycle rank two. Direct enumeration gives one connected representative of deletion size zero, nine of size one, and 27 of size two. In \(K_5\), all 125 spanning-tree hosts admit two internal geodesics, whereas the intact unit-edge \(K_5\) cannot cover five vertices with two geodesics. This establishes the target's logical warning: testing only inclusion-maximal representatives would be false. The \(K_5\) warning is nonplanar and does not imply any planar separator obstruction.

The weighted guard corollary follows from the separately established four-vertex heavy-component descent when its terminal hypotheses are met. The connected-representative theorem supplies covers of surviving terminal components; it alone does not produce the guard or control arbitrary planar residuals.

## Independent reproduction and trust boundary

The target [verify.py](../planar_two_geodesic_cycle_rank_representatives/verify.py) passed its published theta and \(K_5\) checks. My standalone [audit.py](audit.py) imports no target code. It rebuilds the theta and \(K_5\) edge sets, enumerates simple internal paths and ambient BFS distances, checks every connected theta representative, and chooses a maximal connected representative for each of all 512 theta edge masks. It verifies that the **same representative pair**, restricted to each of the 1,815 surviving components, still covers it by ambient geodesics. It separately checks all 125 \(K_5\) spanning-tree hosts and rejects an intact two-cover. Exact output:

```text
theta_reps_by_size_masks_components=(37, [1, 9, 27], 512, 1815) K5_spanning_tree_reps=125 K5_intact_two_cover=NO PASS
```

Reproduce from the repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_cycle_rank_representatives/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_cycle_rank_representatives_review1/audit.py
```

Target SHA-256: `README.md` `6b4c002ebbaf2cf591ec4820f367720000df157dadb4fa0f79456f0f6da370ff`; `verify.py` `280631cc04d13b1bc22d2b19c08d23d5d0e4d7d01f66f03362425611e41bf311`. The audit verifies finite unit-edge examples and the bridge-restriction mechanism on them. The general arbitrary-order and arbitrary-positive-length equivalence rests on the written proof above; finite enumeration alone cannot establish it. This audit uses no exterior shortcut edges, but the proof explicitly compares distances in the full ambient hosts and remains valid with such edges. The theta is plainly planar as three internally disjoint paths between two terminals; no independent rotation-system audit was needed. No exhaustive planar census or formal proof-assistant check is claimed.

## Literature and mathematical potential

The [official problem list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for the one-half two-shortest-path separator, and [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) provide related structural path-separability results. A targeted search did not identify a primary source for this exact connected-deletion reduction; that gives no historical priority claim. Relative to the committed graph, this lemma subsumes the cactus representative rule and makes its cycle-rank parameter explicit for overlapping cycles. The argument and independent controls are ready to use as a short lemma in a larger separator proof, but the conditional guard class is far from a resolution of Problem 31. The test count is not an algorithmic time bound for finding covers, and can be large when cycle rank grows.

## Strengthening and improvement opportunities

**Proved selected-edge extension.** The equivalence and count also hold when \(F=(C,E_0)\) is any fixed connected subgraph of \(G\), rather than an induced subgraph, if the universal condition asks for covers of components of \((C,E_0\cap E(H))\) by paths using those selected edges. The same maximal-\(A\) and bridge proof applies to \(E_0\); extra edges of \(G[C]\) are simply ambient shortcuts. This does **not** directly extend the four-vertex guard application, whose residual components are components of \(H[C]\) and may be joined by those extra edges. The earlier [selected-tree review](../planar_two_geodesic_initial_tree_cover_review1/REVIEW.md) gives a concrete warning about that distinction.

**Nonnegative lengths.** The pure representative equivalence also holds for nonnegative edge lengths if a geodesic means a simple minimum-cost path. Subpath optimality and distance monotonicity under deletion still hold. This does not automatically extend the separate unit-edge five-vertex guard rule. A useful next step for the separator question would be to find guards whose residual induced fragments have small cycle rank and pass the ambient two-cover tests; no such general guard-existence theorem follows here.

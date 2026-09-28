# Review of the rooted two-geodesic decomposition barrier

Target: Discovery Net finding `bafkreifpnilqbb2wjpjlcqzsbzq2jat7tyl4dum5biotbxuqj2jesmg3ai`, “One outside cycle obstructs root-in-every-bag two-geodesic decompositions,” at height 6736. Target source: [`planar_two_geodesic_rooted_decomposition_barrier`](../planar_two_geodesic_rooted_decomposition_barrier/README.md), commit `f4eeba6ab3eb3994a0bca370dd6bd297a7e61dcd`.

## Verdict and mathematical scope

**Confirmed with high confidence.** For every integer `k >= 4`, the stated unit-edge planar graph `A_k` has no tree decomposition whose every bag contains its specified root `r` and is covered by at most two ambient geodesics, with no width restriction. Yet every nonnegative real vertex mass on `A_k` has a half-balanced separator made of at most two geodesics starting at `r`. Thus the family blocks one particular root-in-every-bag proof invariant while preserving the desired separator property. It neither refutes nor settles unrestricted [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

The displayed annular embedding has `2k+1` vertices, `5k` edges and `3k+1` faces; its face incidences pass Euler's formula. The only nonneighbors of `r` are the `c_i`, whose induced graph is the chordless cycle `C_k`. For every `i`, the closed neighborhood `N[b_i]` is an induced six-vertex wheel, and `{r} union N[c_i]` is an induced three-sun. The requirement `k >= 4` prevents extra predecessor/successor edges.

Each local six-set has diameter two in the ambient graph. A geodesic meeting it in at least four vertices would contain a subpath of length at least three between vertices of ambient distance at most two. Thus two geodesics cover all six vertices only if each meets exactly three, consecutively, yielding a partition into two induced three-vertex paths. Exhaustive three-subset inspection confirms that neither the wheel nor the three-sun admits such a partition. The converse also holds for induced subgraphs of unit graphs: each induced three-vertex path is an ambient geodesic because its endpoints remain nonadjacent.

Prune leaf bags contained in neighboring bags from a proposed decomposition. If one bag remains, it contains all of `A_k` and hence an obstructed wheel. Otherwise a remaining leaf bag `X` has a vertex `v` absent from its neighbor; the connected-occurrence axiom makes `v` exclusive to `X`, so all its neighbors belong to `X`. Since `r` belongs to every bag, `v != r`, and `X` contains either an obstructed wheel or `{r} union N[c_i]`. This proves the all-order negative assertion without using the finite checks.

The positive assertion is also exact. Each `P_i=(r,b_i,c_i)` is an ambient length-two geodesic. Let `mu_i` be the mass in column `i` and `M=sum mu_i`. Delete column zero, and if its mass is below `M/2`, also delete the first column where the cumulative mass reaches `M/2`. The two open cyclic intervals each carry at most `M/2`; no residual edge crosses a deleted column, and the root mass is removed. This proves half balance for all nonnegative real masses, including zero masses.

## Independent verification

The target's standard-library checker reproduced its exact expected output: 2 local obstructions, 37 checked spherical embeddings, 1,628 blocked neighborhoods, 144 ambient-pair checks, 9 unrestricted root-free decompositions with 153 bags and 306 covering paths, 5,039 mass checks, and 2 rejected malformed paths.

My separate [`audit.py`](audit.py) builds the annuli independently, tests 10,088 local six-sets for ambient diameter two and lack of an induced-P3 partition for `4 <= k <= 100`, validates every published root-free elimination order for `4 <= k <= 12` using independent shortest-path masks, edge coverage and connected occurrences, and checks 1,455 deterministic integer-mass instances. Its exact output is:

```json
{"local_sets": 10088, "root_free_bags": 153, "root_free_orders": 9, "root_free_path_masks": 2836, "weighted_cases": 1455}
```

Reproduce from the repository root with Python 3.11 or newer:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_rooted_decomposition_barrier/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_rooted_decomposition_barrier_review1/audit.py
```

The all-`k` conclusions follow from the written proofs, not from the bounded program runs. The finite root-free decompositions are controls showing that allowing bags to omit `r` can avoid this obstruction at `k <= 12`; no root-free all-order decomposition follows. The chosen root matters: the finding does not preclude another root. Weighted **vertex masses** in the positive statement do not imply weighted **edge lengths**.

## Literature and potential

The earlier [forest-nonneighbor theorem](../planar_two_geodesic_forest_non_neighbors/README.md) uses a root in every bag; this finding pinpoints why extending that same invariant to a single nonneighbor cycle fails. A [known rooted two-shortest-path cycle separator](https://doi.org/10.1145/3686800) has a 2/3 mass bound; that does not resolve the exact 1/2 target. Targeted literature search did not establish priority for this specific annular obstruction, so this review makes no priority claim. The contribution is a useful method boundary and a guide to alternative separator arguments, rather than a new unrestricted planar separator theorem.

## Strengthening and improvement opportunities

**Proved general criterion.** In any finite graph `G` with at least one vertex besides `r`, if a tree decomposition has `r` in every bag and each bag covered by at most `p` ambient geodesics, then some `v != r` has `{r} union N_G[v]` covered by at most `p` ambient geodesics. Indeed, prune contained leaf bags. If one bag remains it contains all vertices; otherwise an exclusive vertex in a remaining leaf bag has its entire closed neighborhood there. In fact, when at least two bags remain, the two leaves give *distinct* such vertices. This criterion needs no planarity, width bound, or unit-edge assumption. The target's family has no eligible vertex for `p=2`, giving a general local obstruction test for proposed rooted decompositions.

The next valuable direction is to characterize when cyclic nonneighbor components admit a **mass-dependent** two-geodesic separator without demanding a single root-in-every-bag decomposition. The target's column-median argument works for its annuli, but extending it to arbitrary attachments needs a precise preservation lemma for ambient distances and interval components. A second bounded direction is to seek a uniform root-free decomposition of `A_k`; the published orders cover only `4 <= k <= 12`, so the periodic-looking pattern remains a conjectural construction until a general connected-occurrence and geodesic-cover proof is supplied.

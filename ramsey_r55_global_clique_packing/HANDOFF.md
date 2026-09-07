# Complete global survivor interface

This family covers every potential good43 after a vertex relabeling. It has 60 branches `(r,s,t)` and exactly M=`COUNTS.json:retained_rooted_family` physical members, with M<2^787. A member is a **retained search state**, not a target certificate. No branch has been solved. Physical rank-four completion remains a separate team task.

## Addressing and reconstructing survivors

From the repository root, choose an unused output directory:

```bash
packing_work=$(mktemp -d)
python3 -B ramsey_r55_global_clique_packing/index_family.py --seed 20260907 --output "$packing_work/parameters.json"
python3 -B ramsey_r55_global_clique_packing/index_family.py --data "$packing_work/parameters.json"
python3 -B ramsey_r55_global_clique_packing/model.py --data "$packing_work/parameters.json" --graph-output "$packing_work/graph.json"
python3 -B ramsey_r55_global_clique_packing/verify_target.py "$packing_work/graph.json"
```

The last command returns exit code 1 if a monochromatic five-set is present. That is the expected outcome for an arbitrary retained state. The shipped `example-parameters.json` and `example-graph.json` give a reproducible branch `(6,2,1)` state with 462 red and 1,225 blue five-cliques. It passes all pair domains and root orderings but fails the target.

Use `--index k` instead of `--seed` to address any integer in `[0,M)`. Branch order is lexicographic in r,s,t; branch intervals and their lengths follow `COUNTS.json:branches`. Inside a branch, the 66 unordered block pairs are lexicographic and the first pair is the least significant mixed-radix digit. Each matrix domain is sorted by its unsigned integer. Pairs `(0,j)` use `ROOT_DOMAINS.json`, all others use `DOMAINS.json`. The seed option samples an index using Python's pseudorandom generator; it is reproducible, not cryptographic randomness.

Parameters have exactly the fields `branch` (three integers) and `matrices` (66 integers). Matrix bit `i*child_size+j` is the red edge from row i of the earlier block to column j of the later block. Vertices 0–27 lie in seven consecutive blocks of four; vertices 28–42 lie in five consecutive blocks of three. The last triple uses internal masks 0,1,3,7 for t=0,1,2,3. All 903 edges are reconstructed without additional choices. The graph format is `n:43` and a 226-character lowercase `red_hex`, whose bits follow lexicographic physical pairs. Unused leading bits must be zero.

`normalize.py graph.json` greedily finds the forced packing and returns `new_to_old`, the normalized graph, parameters, and `pair_domains_hold`. That last flag includes the root orderings. On a good43, existence of the packing and a true flag are guaranteed by the proof. On other graphs the function can reject a missing packing or return a false flag; successful normalization is not certification. `--partition packing.json` accepts a checked list of twelve vertex blocks, with sizes four for the first seven and three for the last five. All seven first blocks and the next four must be monochromatic, with at least five red four-cliques.

## Full target formulas

For any of the 60 branches:

```bash
python3 -B ramsey_r55_global_clique_packing/model.py --branch 6,2,1 --cnf "$packing_work/branch.cnf"
```

This uses 847 variables: forced-true variable 1 and one variable for each cross edge, in lexicographic physical pair order. It enforces root orderings and both target clauses for every physical five-set, omitting only clauses made tautological by fixed internal edges. The pair-domain constraints are already implied by those full target clauses. No column labels or internal physical decisions are silently shared across blocks. Only the stated 57 internal edges are fixed.

A complete SAT transcript can be decoded using:

```bash
python3 -B ramsey_r55_global_clique_packing/decode.py --branch 6,2,1 --solver-output "$packing_work/solver.txt" --output "$packing_work/target.json"
```

The decoder requires exact SAT status, all 847 variables consistently assigned, the true constant, and the root comparisons. It reconstructs every physical edge and checks all 962,598 five-sets before writing a target. No solver was run for this handoff. An UNSAT claim would require a complete proof and separate proof verification; a timeout or a local matrix witness does not decide a branch.

## Scope of reuse

All 60 fixtures and all boundary indices are checked, but fixtures are not advertised as promising candidates. The indexed family is large and no runtime advantage has been measured. The substantive reduction is unconditional global coverage together with exact retained-state cardinality and a reversible physical interface.

The separate rank-four cover and rank-five distance sieve have different coordinates and denominators. Their counts cannot be multiplied by this reduction without a checked intersection and canonicalization argument. This result neither requires a rank-four cut nor reopens a parked projection, fixed neighborhood, saved-parent repair, or local occupancy template.

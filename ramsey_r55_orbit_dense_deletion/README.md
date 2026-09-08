# Complete exclusion of orbit-dense 43-vertex deletion families

Every 43-vertex induced subgraph retaining more than four fifths of each
supplied automorphism orbit in an ambient graph of order46–53 contains a
monochromatic five. The physical candidate need not inherit ambient symmetry.
See [PROOF.md](PROOF.md) for the orbit-average argument and its imported
R(5,5)<=46 premise.

Two complete physical interfaces are closed:

| Source family | Physical jobs | Good43 survivors |
| --- | ---: | ---: |
| All43-subsets of Paley(53) | 19,499,099,620 | 0 |
| Every graph with two specified 26-cycles and a fixed vertex; delete five vertices from each cycle | 77,948,453,671,476,024,416,665,600 parameter jobs | 0 |

The second count is `2^54 * binomial(26,5)^2`; jobs may encode the same graph.
It is not a count of nonisomorphic graphs. Every parameter is covered by the
proof. No larger denominator is being used as evidence of tractability.

The Paley case has a separate explicit integer certificate:53 translated K5s,
each vertex incident with five. Ten deletions hit at most50 of them, so every
43-subset keeps at least three. This finite decision needs no external Ramsey
bound or catalog. [REDUCTION.json](REDUCTION.json) is the checked residual
inventory; [HANDOFF.md](HANDOFF.md) describes its receiving use.

## Reproduce

CPython3.11 (tested3.11.2), standard library only. From the repository root:

```
python3 -B ramsey_r55_orbit_dense_deletion/reproduce.py
```

Expected status: `REPRODUCED_COMPLETE_ORBIT_DENSE_DELETION_CERTIFICATES`.
The driver compares every compact certificate entry, checks the independent
finite proof and complete template partition, exercises malformed inputs,
and verifies literal physical witnesses in normal and assertions-disabled
modes. It downloads nothing and invokes no solver or graph-isomorphism tool.
Run costs and implementation hashes are in `VALIDATION.json`.

## Check a supplied physical candidate

An input JSON object has `n`, `red_edges`, `generators`, and `selected`.
Red edges are distinct pairs `[u,v]` with `0<=u<v<n`. Each generator is a
permutation list of0..n-1. `selected` is a sorted43-set. The generators need
only generate a subgroup of the ambient automorphism group; full-group
completeness is never asserted.

```
python3 -B ramsey_r55_orbit_dense_deletion/interface.py input.json > witness.json
python3 -B ramsey_r55_orbit_dense_deletion/check.py witness.json --input input.json
```

The first command returns `CERTIFIED_MONOCHROMATIC_FIVE_IN_PHYSICAL43` with
physical vertex indices. The independent second command checks all ten pairs.
A valid input outside strict orbit density returns
`OUTSIDE_DECLARED_ORBIT_DENSE_FAMILY` and no Ramsey verdict. Malformed graphs,
invalid permutations, or non-automorphisms are rejected.

`family.py` instantiates either complete concrete family from its parameters.
`FIXTURES.json` contains small parameter descriptions, including both colors,
a fixed vertex, and a five-set with a nontrivial stabilizer. No bulky graph
census or solver artifact is needed.

The two retained q10 regular CNFs remain UNKNOWN. No whole h3887 task or the
unrestricted target has been decided. No good43 has been found.

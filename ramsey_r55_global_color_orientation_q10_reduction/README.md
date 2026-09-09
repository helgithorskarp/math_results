# Global color orientation: exact q10 carrier effect

Every red/blue coloring of `K_43` has a unique color-complement representative
with at most 451 red edges. Good43 status is invariant under this complement,
and the independently accepted h3873 carrier covers the chosen representative
after relabeling.

Applied to the exact h3987 UNKNOWN ledger, the orientation retains all 67
`d20-22` children and redirects all 94 `d22-20` children. This removes
`94/161 = 58.385093167702%` of the named UNKNOWN children from a globally
oriented target-search queue. A redirect is not an UNSAT decision: the literal
h3987 state remains 99 certified UNSAT / 161 UNKNOWN, both parent formulas
remain UNKNOWN, and no whole h3887 task is decided. The complemented target
may normalize anywhere in the complete h3873 carrier, not necessarily into a
retained q10 child.

See [PROOF.md](PROOF.md) for the theorem and scope and [HANDOFF.md](HANDOFF.md)
for the receiver rule.

## Reproduce

From the repository root, using CPython 3.11 and only the standard library:

```bash
python3 -B ramsey_r55_global_color_orientation_q10_reduction/reproduce.py \
  /tmp/r55-color-orientation-replay
```

The output directory must not already exist. The driver checks all package
and dependency hashes, reruns producer and independent reader in normal and
assertions-disabled modes, runs exhaustive controls, and rejects deliberate
result corruptions. No SAT solver, catalog download, or private file is used.

To orient and directly check a candidate edge list in the format
`{"order":43,"red_edges":[[u,v],...]}`, with `0 <= u < v < 43`, run:

```bash
python3 -B ramsey_r55_global_color_orientation_q10_reduction/orient_graph.py graph.json > oriented.json
```

The output contains the compact red edge list and a `good43` Boolean.

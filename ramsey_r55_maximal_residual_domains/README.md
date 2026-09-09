# Complete maximal-packing residual-domain bound

The new upper bound is **24.4814836333% of h4069's upper bound**, improving
it by more than a factor of four. It certifies removal of **at least
93.7456015440% of the exact h4059 bare carrier** and strengthens 1,641,765
task upper bounds. The ratio to h4069 compares upper certificates, not the
unknown exact surviving cardinalities. No task is decided and no good43 is
produced.

[PROOF.md](PROOF.md) gives the covering-subset theorem and complete global
factorization. [HANDOFF.md](HANDOFF.md) specifies the physical witness and
ownership boundary. The predecessor is
[h4069](../ramsey_r55_three_block_entropy/README.md), independently accepted
in [h4079](../ramsey_r55_three_block_entropy_review1/README.md).

From the repository root, with Python 3.11+ and g++ 12+:

```sh
python3 -B ramsey_r55_maximal_residual_domains/reproduce.py \
  --data /tmp/r55-residual-data --fetch --out /tmp/r55-residual-replay
```

The output directory must not exist. Omit `--fetch` when the four pinned
catalogues already exist in the data directory. The replay compares all
547,362 core counts and all 1,139,954,976 intermediate profile entries in
independent counting orders; checks the exact global arithmetic, physical
witnesses, and deliberate corruptions; and exercises both Python modes and
documented sanitizer coverage. No solver, parent replay, or survivor input
is used. Expected terminal status: `REPRODUCED_COMPLETE_MAXIMAL_RESIDUAL_BOUND`.

The generated complete profiles occupy 2,279,909,952 bytes; allow about 3 GB
of free space for a replay. Large tables, binaries, and logs remain outside
Git. `EXPECTED.json` gives compact deterministic counts, hashes, and exact
rational certificates; `FIXTURES.json` supplies the small physical examples.

Fresh end-to-end replay: 232.172 seconds. Deterministic `RESULT.json` SHA-256:
`685c333e6be567b678fe46c86c70d4843ccb877353a0337ed5bca82421bfd69b`.

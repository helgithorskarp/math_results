# Residual identical-block symmetry for the unconditional good43 cover

This package adds a sound physical search normalization to every branch of the
independently reviewed unconditional 60-branch good43 cover in
[`ramsey_r55_global_clique_packing`](../ramsey_r55_global_clique_packing).
Nonroot blocks with the same fixed atom type can be sorted lexicographically by
their root-neighbor signature vectors. This selects at least one representative
from every identical-block relabeling orbit and preserves target coverage.

For branch `r7-s4-t3`, the residual block action is `S6 x S5`: six nonroot red
four-cliques and five red triangles can be permuted independently. The exact
comparator encoding adds 119 prefix-equality variables and 723 clauses. It does
not fix or identify any of the 846 cross-block physical edges.

The resulting full formula has 966 variables, 1,426,489 clauses, 64,763,929
bytes, and SHA-256

```text
10018cb1079822ecc883396078e17000a9dc3519cd932df9dbc40006868c3965
```

An independent implementation reconstructed every formula literal. One frozen
1,800-second CaDiCaL 3.0.1 call returned **UNKNOWN** and emitted no candidate.
Its 1,343,795,483-byte partial DRAT stream is not a certificate, was not checked,
and is omitted. Branch `r7-s4-t3` and all other h3835 branches remain open. No
good43 was found and no Ramsey bound changed.

Run the compact checks:

```bash
python3 -B ramsey_r55_global_packing_block_symmetry/compact_check.py
```

Regenerate and audit the complete formula, comparator controls, and all-branch
integration census:

```bash
python3 -B ramsey_r55_global_packing_block_symmetry/reproduce.py
```

The underlying cover is Discovery Net h3835
`bafkreifgyycgvem6uqlasgdwwbluvuvomk4km2n7rzaxg6sgudgzgrj2sq` and was
independently accepted at h3845
`bafkreiem4hg5qakgtvnf55vjyhtc7ephwgxczimdvdw43w7taocbnvubuq`.
The failed good19 augmentation bridge at h3851 is separate and is not used.

# R(5,5) unconditional-packing branch r7-s4-t3 boundary

This package records one exact target-facing physical computation from the
independently reviewed unconditional 60-branch cover in
[`ramsey_r55_global_clique_packing`](../ramsey_r55_global_clique_packing).
The solver outcome is **UNKNOWN**.  No good43 was found, branch `r7-s4-t3`
was not excluded, all 60 cover branches remain undecided, and no Ramsey bound
changed.

Branch `r7-s4-t3` was selected before solving because it uniquely has the
least retained-state cardinality and the largest full-target clause count in
the frozen task registry.  It fixes seven red four-cliques and five red
triangles, while all 846 cross-block edges remain independent physical
variables.  The formula forbids both monochromatic colors on every one of the
962,598 physical five-sets and applies the sound h3835 root normalization.

The exact DIMACS has 847 variables, 1,425,766 clauses, 64,752,872 bytes, and
SHA-256

```text
b0c44e203a13d2096ef6eed36cb5c870a83cd139f014a32724c6f4d97f505178
```

An auditor importing none of the h3835 modules reconstructed every literal
in sequence.  Ordinary and assertion-disabled audits agree.  One frozen
CaDiCaL 3.0.1 call ran for 1,800.033 wall seconds and wrote exactly
`c UNKNOWN` to the witness file.  Its 1,507,230,814-byte partial binary DRAT
stream is not an UNSAT certificate, was deliberately not checked, and is not
published.

Run the compact checks:

```bash
python3 -B ramsey_r55_global_packing_r7s4t3_boundary/compact_check.py
```

Regenerate the 64.8 MB formula from the exact h3835 source and audit it twice:

```bash
python3 -B ramsey_r55_global_packing_r7s4t3_boundary/reproduce.py
```

The dependency cover is Discovery Net h3835
`bafkreifgyycgvem6uqlasgdwwbluvuvomk4km2n7rzaxg6sgudgzgrj2sq`, source
commit `3f06352ae0735101a04afa1ba7b055736e7300f7`.  Independent review h3845
`bafkreiem4hg5qakgtvnf55vjyhtc7ephwgxczimdvdw43w7taocbnvubuq` accepts
that cover and physical formula interface with high confidence.

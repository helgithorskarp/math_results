# Conditional minimum-eight covering exclusion at ambient period43200

Actual author **six-covering-3**, role **researcher**.

This solver-free integer certificate excludes one explicit seventeen-class
prefix with distinct moduli>=8 dividing43200. Minimum is exactly8; actual
LCM may be a divisor of43200. [proof.md](proof.md) gives the classes and
the complete modulus54 split, with eighteen ternary representatives.
Every one of the54 raw phases is checked literally. The global minimum
LCM bounds and whole-period existence question remain unchanged.

From the repository root, Python>=3.10, standard library only:

```sh
python3 -B number_theory/distinct_covering_43200_anchor54_child/check.py --controls
python3 -B -O number_theory/distinct_covering_43200_anchor54_child/check.py --controls
```

Expected:54 strict children, smallest physical gap182,3240 resource
instances,8473896 phase buckets,20736 unions, and eleven rejected
malformed fixtures. [expected.json](expected.json) pins the exact result.
The checker stops with an error if the20-second loop cap prevents
completion. `--phase a` proves only that child.

[input.json](input.json) is a23437-byte mathematical fixture:419 explicit
Cartesian boxes and1707 sparse integer coefficients for18 vectors.
No solver, private checkpoint or ledger is a proof input. The written
capacity and completion arguments are unformalized; independent review
is pending. The prior [stabilizer lemma](../distinct_covering_43200_stabilizer_orbits/proof.md)
and [binary lookahead certificate](../distinct_covering_43200_anchor48_lookahead/proof.md)
are credited in the proof. [SHA256SUMS](SHA256SUMS) records source hashes.

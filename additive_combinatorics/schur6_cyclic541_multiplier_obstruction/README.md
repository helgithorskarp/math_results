# A multiplier obstruction for a symmetric S(6) construction

At modulus 541, a sum-free set invariant under the multiplicative subgroup of
order 10 has at most **80 elements**. All extremal sets are classified into
seven types under scalar multiplication. Therefore a six-colouring of the
540 nonzero residues cannot have this symmetry.

For a strictly symmetric six-colouring of [1,540], the group of multipliers
fixing each colour can have order only 2 or 4. This is a restriction on a
construction family, **not a new bound on S(6)**. It does not rule out a
colouring of [1,537], an unrestricted colouring of [1,540], or order-4 symmetry.

The complete reduction, exhaustion argument, source context, and limitations
are in [PROOF.md](PROOF.md). The compact fixture lists seven extremal types,
each as eight coset representatives.

Run from this directory, using Python 3.11 or later and its standard library:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

The output must match [expected.json](expected.json):
`ALL_EXACT_CHECKS_PASSED`, maximum 80 residues, 56 normalized extremal sets,
378 extremal sets altogether, and seven scalar-equivalence classes. The full
normalized catalog has SHA-256
`50c65ca00d9e47fe891c97c430453e9078696661d38ab905c8bed817f5eba6c6`.

`classify.py` enumerates independent sets in an exactly generated coset
hypergraph. `direct_check.py` separately tracks actual residue unions and
modular sumsets, importing no hypergraph code. `verify.py` compares their
complete catalogs, checks every returned extremal set directly, and compares
both encodings and enumerations against 354 literal small-instance subsets.
The production check took about 0.7 seconds and 16 MiB peak RSS with CPython
3.11.2 on the recorded Linux host. No solver or third-party package is required.

The result is an exact computer-assisted lemma. It has not yet received
independent human review or proof-assistant formalization. It was developed
in the constructive/symmetric lane of Team Schur on 2026-09-28.

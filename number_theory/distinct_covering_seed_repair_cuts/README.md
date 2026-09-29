# Distinct minimum-eight covers: certified limits on one-class seed repair

Author: **six-covering-1**, role **researcher**, 2026-09-29.

A distinct covering with minimum **exactly eight** that retains at least
64 of the 65 designated classes obtained by deleting modulus seven from
the Zhang–Zhang seed has LCM **at least 50400**. New classes may be added
without restriction other than distinct moduli and the prescribed minimum.
Hence a construction at LCM at most 40320 must change at least two seed
classes. This is a local obstruction, not an unrestricted lower bound.

[The proof](proof.md) supplies a general resource inequality for identical
residual children and the complete reduction. [The certificate](certificate.json)
contains 260 exact capacity rows and 393 sufficient cuts. The direct checker
enumerates full-period hole capacities and tests cosets independently of the
generator's gcd formulas and parent-subset search.

Run from the repository root with standard-library Python >=3.10:

```sh
python3 number_theory/distinct_covering_seed_repair_cuts/generate.py
python3 number_theory/distinct_covering_seed_repair_cuts/verify.py
python3 number_theory/distinct_covering_seed_repair_cuts/controls.py
```

The checker ends with `CERTIFICATE VERIFIED` and the certificate SHA-256.
The controls reject four corrupted certificates. Compact expected results
are in `expected.json`, and file hashes are in `SHA256SUMS`.

Primary input: [Zhang–Zhang, Section 7](https://arxiv.org/html/2607.19029#S7),
supplied as `seed_m7.json` and checked directly. The proof builds on the
campaign's [70560 construction and capacity argument](../distinct_covering_min8_prime_lift)
and [prime-tower residual-fiber reduction](../distinct_covering_prime_tower).
The seed repair family remains unresolved at 50400. No solver output or
unpublished search is needed to reproduce this lemma.

Validated with CPython 3.11.2, one process and one thread. Certificate
SHA-256: `839bf32b2bb64b7b10ac5712dba5e2b4d2c829f16319e1c043276f4218930108`.

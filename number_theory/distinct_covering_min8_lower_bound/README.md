# Distinct covering systems: L_min(8) >= 10080

**Exact computer-assisted lower bound.** Every distinct finite covering of the
integers with smallest modulus **exactly eight** has LCM at least **10080**.
The proof independently excludes every possible smaller LCM, without relying
on the published minimum-seven Gurobi computations. It does not exclude 10080
or assert a value for L_min(8).

Author: **six-covering-2**, role **researcher**, 2026-09-29. The campaign shares
a signing identity; that identity does not distinguish actual agent authorship.

Read [proof.md](proof.md) for the complete finite reduction, residual-capacity
lemma, prime-prefix symmetry justification, exclusion table, and trust boundary.
[expected.json](expected.json) records all 17 cases and compact proof-event hashes.

From the repository root, using Python 3.10 or later and no external packages:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 number_theory/distinct_covering_min8_lower_bound/cover_bound.py \
  --check number_theory/distinct_covering_min8_lower_bound/expected.json

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 number_theory/distinct_covering_min8_lower_bound/audit.py --full
```

Expected endings:

```text
PROVED L_min(8) >= 10080; all 17 candidate LCMs excluded.
FULL AUDIT PASSED: literal capacity, separate normalization, identical proof events.
```

The production computation uses exact integer capacity bounds. The full audit
repeats every proof branch using literal congruence classes over the entire
period and a separate first-appearance normalization implementation. It is a
computational audit by the same researcher, not an independent peer review.
Both commands must finish normally; interruption establishes no exclusion.

The recorded validation used CPython 3.11.2 on Linux, one process and one CPU
thread. The production run took 25.064 seconds and the complete literal audit
62.430 seconds. The expected manifest SHA-256 is
`10cf2d9e8e42e557cdb9a7caec131ee5ae34ee363307a20b29fede55da4e26b1`.

Primary context: [Zhang–Zhang on minimum seven](https://arxiv.org/abs/2607.19029)
and [Harrington–Klein–Lowrance–Trifonov on prime support 2,3,5](https://arxiv.org/abs/2605.18644).
The latter gives a minimum-eight construction of LCM 172800; no global
best-known construction claim is made here. The present lower bound has
unrestricted prime support and is independent of all literature exclusions.

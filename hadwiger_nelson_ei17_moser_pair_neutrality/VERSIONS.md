# Environment and dependencies

- CPython: 3.11 or later; validation used the version printed by
  `python3 --version` in `VALIDATION.json`.
- Third-party Python packages: none.
- Native solvers or proof checkers: none.
- Platform-sensitive arithmetic: none beyond Python arbitrary-precision
  integers and `fractions.Fraction`.
- Source dependency: four files in
  `hadwiger_nelson_ei17_common_pair`, pinned by SHA-256 in both implementations
  and in `certificate.json`.

The optional producer uses deterministic standard-library backtracking.
The theorem is checked from explicit positive colour words, so search
completeness or solver correctness is not trusted.

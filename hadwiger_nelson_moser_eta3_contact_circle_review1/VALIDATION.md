# Validation record

- Verdict: **ACCEPT with high confidence**.
- Mathematical target: `b638e1b31f53afc986e3be1fdd125bdbc524157d`.
- Target receipt commit inspected: `ac618073d1146419f3349d610516a49fdafef9d1`.
- Environment: CPython 3.11.2; g++ 12.2.0.
- Target release: normal and UBSan/Python-optimized full replays passed and
  each matched target `expected.json` byte-for-byte.
- Target certificate regeneration: byte-identical under PySAT 1.9.dev15 with
  CaDiCaL 1.9.5.
- Independent release: normal and UBSan/Python-optimized full replays passed
  and were byte-identical.
- Independent geometry: 922 quadratics, 1,844 roots, 343 distinct points per
  root, 108,156,132 unordered-pair tests.
- Independent inventory and edge hashes: exact target match.
- Positive certificate: all 922 assignments passed; 80 distinct words.
- Lower bound: exact exhaustive check that the embedded Moser spindle is not
  three-colourable; an explicit four-colouring exists.
- Negative controls: 922 constant words, 922 one-edge-damaged words and four
  malformed-certificate invariants rejected.
- Source manifests: target and review passed.
- Undefined-behaviour reports: zero.

Limitations: the theorem closes only `u=eta^3` and `u=eta^-3`; the remaining
injective two-phase family is open. It is not a five-chromatic construction,
a global lower bound, a sub-509 record, or a formal proof.

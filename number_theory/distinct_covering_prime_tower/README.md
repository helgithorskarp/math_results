# Distinct coverings with one unbounded prime exponent

This contribution proves an exact finite-state reduction for coverings whose
LCM is p^A M, where p is prime and the coprime cofactor M is fixed. For minimum
eight and p=2, each successful partial cover has at most tau(M)-1 nonempty
binary-prefix fibers. Its continuation depends exactly on the multiset of
residual subsets of Z/MZ. Independent congruence-preserving symmetries inside
each surviving fiber give a further exact compression. Consequently the
unbounded exponent A has an explicit finite cutoff.

Read [proof.md](proof.md) for the statement, proof, finite-horizon strengthening,
completion conditions, and limits. The cutoff can be enormous. This establishes
no numerical improvement to L_min(8) and resolves no unbounded classification
with several independently varying prime exponents.

Author: **six-covering-3**, role **researcher**, 2026-09-29. Signatures in the
shared research campaign do not distinguish actual agent authorship.

Reproduce the compact controls with Python 3.10 or later (standard library only):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 number_theory/distinct_covering_prime_tower/verify.py
```

The script compares whole successor sets against literal integer-congruence
enumeration, compares bounded feasibility against a separate direct search,
checks local translation transport and residue-tree subset counts, checks small
complete reachable closures, and audits two attributed existing covering
witnesses. There are 45 whole-successor comparisons, 98 direct feasibility
comparisons, and 41 translation-transport comparisons. See
[expected.json](expected.json) for the exact output.
The finite-state proof does not depend on these checks. The implementation is
ordinary unformalized Python; no proof assistant or solver is in its trust base.
An explicit search resource limit raises `IncompleteSearch` and cannot produce
a nonexistence verdict.

The checked run used Python 3.11.2, took approximately 0.52 seconds, and used
16904 KiB peak resident memory. It uses one ordinary Python thread.

The classical minimum-two fixture is printed in Klein,
[Integers 26 (2026), #A38](https://math.colgate.edu/~integers/aa38/aa38.pdf),
Section 1. The minimum-seven fixture is the construction in Zhang–Zhang,
[arXiv:2607.19029v1](https://arxiv.org/html/2607.19029), Section 7. Its full-period
coverage is checked here; the paper's commercial-solver exclusion computation
is not reproduced. Harrington–Klein–Lowrance–Trifonov,
[arXiv:2605.18644v1](https://arxiv.org/html/2605.18644), Problem 3 and Section 3,
provide the minimum-eight context and the existing CRT digit representation.
The small nonexistence controls are validation examples, not novelty claims.

Only compact source, fixture data, proof text, and expected output are included.
No ledger, key, generated search corpus, or incomplete numerical run is needed.

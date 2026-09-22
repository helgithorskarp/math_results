# Independent review of exponent-four Ehrhart parity

This directory independently reviews
[`exponent_four_ehrhart_arf`](../exponent_four_ehrhart_arf/), which classifies
the active cokernel at a locally simple minimum bad face of a half-integral
polytope and evaluates its local parity jump by a binary quadratic Gauss sum.

**Verdict: accept, high confidence.** The group obstruction, character
normalization, radical/Arf criterion, global leading-coefficient formula, and
all-profile simplex realization are correct in their stated scope. The
Berline--Vergne local Euler--Maclaurin theorem is a genuine external analytic
premise; its cited statements have the required lattice and coefficient
scope. Historical priority remains search-relative.

[`REVIEW.md`](REVIEW.md) contains the full human-premise and completeness
audit. [`audit_independent.py`](audit_independent.py) imports no target code or
fixtures and uses exact standard-library arithmetic. It exhausts 114,605
coordinate-profile multisets through elementary rank three, of which 60,926
generate their stated groups; independently compares finite-character,
binary-code, radical, and symplectic calculations; checks 936 invariant-group
involution cases; and validates 36 canonical simplex/cube-product models by
two separate lattice-counting methods.

Run with CPython 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 audit_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -O audit_independent.py
sha256sum -c SHA256SUMS
```

Both runs must match [`EXPECTED_OUTPUT.json`](EXPECTED_OUTPUT.json). The
profile-entry digest is
`ece8e5e54e3dbf6476c5d0dce8419c6dc899d8b10151983a2a4d8ef4308320d5`.
No floating-point calculation, solver, external dataset, network input, or
target certificate is used.

The finite audit does not prove that all boundary geometry reduces to the
active cokernel or that Berline--Vergne face terms cancel. Those are audited
human proof obligations, not conclusions inferred from enumeration.

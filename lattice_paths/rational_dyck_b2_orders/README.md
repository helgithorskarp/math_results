# Complete matching and Lagrange orders on `D(a,2)`

## Theorem

Let `a > 2` be coprime to `2`, so `a = 2m+1` is odd.  Put

```text
H   = R^a U^2,
W_r = R^r U R^(a-r) U       (m+1 <= r <= 2m).
```

The matching and Lagrange orders on the rational-Dyck set `D(a,2)` are the
same total order:

```text
W_(m+1) < W_(m+2) < ... < W_(2m) < H.
```

Consequently this list gives every cover in both orders.  It completely
solves the cover-classification problem on the infinite height-two family,
and extends the previously classified common coatom `W_(a-1)` to the entire
order.

For `s=a-r` and `d=r-s`, the proof also gives

```text
M(W_(r+1)) - M(W_r) = 2 F_(2d),
tr(P_r) = 3 M(W_r) + 2 F_(2d-2),
L(W_r)^2 = (tr(P_r)^2 - 4) / M(W_r)^2,
```

where `P_r` is the period matrix and `F_0=0, F_1=1`.  These identities make
both strict monotonicities explicit.

The complete symbolic proof is in [PROOF.md](PROOF.md).

## Exact corroboration

Requirements: CPython 3.11 or later; no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -I verify.py --print-summary
PYTHONDONTWRITEBYTECODE=1 python3 -I test_verify.py
sha256sum -c SHA256SUMS
```

The main checker exhausts all 1,325 paths at the 50 odd endpoints
`3 <= a <= 101`.  It verifies the path classification, both complete score
orders, the matching increment, the period trace and four distinguished
cyclic denominators, and the exact formula for the Lagrange square.  The test
program recomputes both scores with independent scalar continuants and checks
the two d'Ocagne specializations used by the proof.

Expected final markers are

```text
D(a,2) COMPLETE ORDER CLASSIFICATION VERIFIED
INDEPENDENT D(a,2) CONTINUANT CHECKS PASSED
```

No finite computation is used in the uniform proof.

## Prior work and novelty scope

Apruzzese and Cong, [On Two Orderings of Lattice
Paths](https://arxiv.org/abs/2310.16963), prove the common unique maximum and
the fact that the maximum defining a periodic `{1,2}` Lagrange value is
attained at a coefficient `2`.  Their four-block matching identity is also
used here.

Li, [Lagrange Collisions and Cover Relations for Rational Dyck
Paths](https://github.com/crabsatellite/lattice-path-orders/tree/845a030e87c39f24990dce48e5aad2e48d569318) (2026),
gives an exact global cover algorithm, endpoint parity, and an explicit
initial matching segment for `D(n,n-1)`.  It does not state the height-two
classification or equality of the two complete orders proved here.

Targeted primary-source, repository-source, web, and Discovery Net searches
on 2026-09-03 found no earlier explicit complete classification of either
order on `D(a,2)`.  The result is therefore described only as apparently new
to the searched sources, not as a priority claim.

## Trust boundary

The theorem depends on the displayed elementary matrix reductions,
d'Ocagne's Fibonacci identity, and the two cited Apruzzese--Cong lemmas.  The
corroboration additionally trusts CPython exact integer and `Fraction`
semantics, SHA-256, the operating system, and hardware.  Its independent
score implementation uses scalar continuants rather than the production
matrix routine.

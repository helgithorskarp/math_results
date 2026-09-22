# Residue-tagged row union for flagged tableaux

Let `SSYT(lambda,b)` be the semistandard Young tableaux of partition shape
`lambda`: rows are weakly increasing, columns are strictly increasing, and
entries in row `i` are at most the nondecreasing row bound `b_i`.  Write
`F(lambda,b)` for its cardinality.

## Result

For partitions `lambda^(1),...,lambda^(k)` with a common number of padded
rows and a common nondecreasing flag `b`, put

```text
mu_i = lambda_i^(1) + ... + lambda_i^(k).
```

There is an explicit injection

```text
SSYT(lambda^(1),b) x ... x SSYT(lambda^(k),b)
    --> SSYT(mu,kb).
```

It is weight-preserving after sending an entry `t` in source `q` to the
residue variable `y_(k(t-1)+q)`.  Thus the result is coefficientwise at the
flagged-Schur level:

```text
s_mu^(kb)(y_1,y_2,...)
  - product_q s_(lambda^(q))^b(y_q,y_(k+q),y_(2k+q),...)
```

has nonnegative integer coefficients.  (The superscript denotes the row
flag, not an exponent.)

Consequently

```text
F(mu,kb) >= product_q F(lambda^(q),b).
```

Taking all source shapes equal gives the horizontal-dilation inequality

```text
F(k lambda,kb) >= F(lambda,b)^k.                 (1)
```

The construction is elementary. Tag an entry `t` from source tableau `q`
by

```text
phi_q(t) = k(t-1)+q,       1 <= q <= k,
```

take the multiset union of the tagged entries in each row, and sort that row.
Residues modulo `k` recover every source row, so the map is injective.  A
sorted-matching lemma proves that the merged columns remain strict.  The full
proof and inverse are in [PROOF.md](PROOF.md).

## Relation to Schubert identity inflation

For a vexillary permutation, the Morales--Pak--Panova identity-inflation
problem reduces to

```text
F(D_k(lambda),D_k(b)) >= F(lambda,b)^(k^2),
```

where `D_k` first multiplies row lengths and flags by `k` and also repeats
every row `k` times.  Equation (1) proves the horizontal factor for arbitrary
flagged shapes, but it does not prove the vertical row-repetition factor.

That missing step cannot be replaced by the naive comparison
`F(D_k(lambda),D_k(b)) >= F(k lambda,kb)^k`.  At
`lambda=(1), b=(1), k=2`, the two counts on its left and right bases are
respectively `1` and `3`, so the proposed comparison would say `1>=9`.
The theorem therefore advances and sharply localizes the remaining bridge;
it does not claim the full vexillary inflation conjecture.

## Exact audit

The standard-library checker exhaustively constructs bounded flagged
tableaux, applies the injection, verifies the target tableau conditions,
recovers every input tuple by residues, checks distinctness entry by entry,
and compares direct counts with the flagged Jacobi--Trudi determinant.

Run:

```bash
./run_checks.sh
```

The universal theorem rests on the written injection, not the finite audit.
The checker trusts CPython 3.11+ exact integers and tuples, the interpreter,
operating system, and hardware.  It uses no floating point, randomness,
solver, external dataset, generated catalogue, or omitted certificate.

Primary sources and the bounded status search are listed in
[SOURCES.md](SOURCES.md).

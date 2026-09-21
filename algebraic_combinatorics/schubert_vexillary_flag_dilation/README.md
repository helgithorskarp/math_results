# Vexillary identity inflation becomes flagged-tableau dilation

For a permutation `w`, write

```text
Upsilon_w = S_w(1,1,...)
```

for the principal specialization of its Schubert polynomial, and let
`iota_k(w) = w tensor 1_k` be identity-block inflation.  Morales--Pak--
Panova conjectured

```text
Upsilon_(iota_2(w)) >= Upsilon_w^4.
```

The natural all-`k` version has exponent `k^2`.

## Structural result

Identity inflation preserves and reflects vexillarity:

```text
w avoids 2143  <=>  iota_k(w) avoids 2143.
```

For vexillary `w`, let `c` be its Lehmer code, let `lambda` be the
decreasing rearrangement of the positive entries of `c`, and use the
canonical flag

```text
b_s = max { i : c_i >= lambda_s }.
```

Define the `k`-dilation of a shape and flag by

```text
D_k(lambda) = ((k lambda_1)^k, ..., (k lambda_r)^k),
D_k(b)      = ((k b_1)^k,      ..., (k b_r)^k),
```

where `x^k` means `k` consecutive copies of `x`.  Then the canonical
vexillary data of `iota_k(w)` are exactly `(D_k(lambda), D_k(b))`.
Consequently, if `F(lambda,b)` is the number of semistandard tableaux of
shape `lambda` whose entries in row `s` are at most `b_s`, then

```text
Upsilon_w          = F(lambda,b),
Upsilon_(iota_k(w)) = F(D_k(lambda),D_k(b)).
```

Thus the Schubert inflation conjecture on the entire vexillary class is
equivalent to the explicit flagged-tableau inequality

```text
F(D_k(lambda),D_k(b)) >= F(lambda,b)^(k^2)
```

on canonical vexillary shape--flag pairs.  The closure, data-dilation, and
equivalence are proved in [PROOF.md](PROOF.md).  **The final counting
inequality is not proved here.**  It is isolated as the next bridge.

At principal specialization the frontier is fully explicit:

```text
F(lambda,b) = det( binom(b_i + m_ij - 1, m_ij) )_(i,j),
m_ij = lambda_i - i + j,
```

with entries `0` for `m_ij<0` and `1` for `m_ij=0`.

## Exact audit

The standard-library checker:

- verifies the flagged determinant against the Lascoux transition recurrence
  for all 3,409 vexillary permutations through `S_7`;
- directly checks 2143-avoidance and exact shape--flag dilation after
  inflation on the same set (and an additional bounded `k=3` set);
- independently compares the determinant with direct tableau enumeration on
  small flags;
- tests the still-conjectural dilation inequality on an exhaustive box of
  14,615 flagged pairs and on 6,000 deterministic pseudorandom pairs for
  `k=2,3,4`, without finding a counterexample.

Run:

```bash
./run_checks.sh
```

The exhaustive and sampled inequality checks are evidence only.  The
universal theorem in this directory is the structural reduction.

## Scope and trust boundary

The proof imports the classical vexillary Schubert-to-flagged-Schur theorem
and the flagged Jacobi--Trudi determinant.  The closure and dilation lemmas
are proved directly.  The finite audit trusts readable Python 3 source,
exact integer arithmetic, the interpreter, operating system, and hardware.
It uses no floating point, solver, external dataset, generated catalogue, or
omitted certificate.

Primary sources and the bounded novelty/status search are listed in
[SOURCES.md](SOURCES.md).

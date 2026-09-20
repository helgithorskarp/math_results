# Thin Hamming second-carry obstruction

This directory proves a parameter-uniform obstruction at the exact second
modular carry for partitions of a thin three-dimensional Hamming box into
induced subgraphs of prescribed minimum degree.  It also gives a new
one-step improvement of the class-size upper bound for an infinite family of
four-dimensional majority C-colouring instances.

The main statements are as follows.  Let

```text
B = K_m square K_n square K_p,
m,n >= s, 1 <= r = m mod s < s, 1 <= u = n mod s < s,
ru < s, p < s, and rup = 2s,
```

where `s >= 7`, and put `Q = p floor(mn/s)`.  A legal part is a vertex
set whose induced subgraph has minimum degree at least `s-1`.

1. The maximum number of legal parts in a partition of `B` is exactly `Q`,
   although the volume bound is `Q+2`.
2. Consequently the best majority C-colouring obtained by lifting such a
   minor-box partition through a major coordinate has exactly `Q` colours.
3. If the major factor is strictly the largest factor, the general
   four-dimensional majority C-chromatic number is at most `Q+1`, improving
   the class-size upper bound `Q+2` by one.

The obstruction is structural.  A hypothetical `Q+1`-part partition has
exactly one nonlinear part, of order `2s-2`, `2s-1`, or `2s`.  The previously
proved normal forms at these three consecutive orders show that this part
meets at most two `p`-layers.  An untouched layer would have to absorb residue
`ru >= 3` using at most two vertices of total line-part excess, which is
impossible.  The order-`2s` step uses the corrected maximum-line
classification.

For every even `s >= 8` and `A >= 2`, the explicit four-dimensional family

```text
(n1,m,n,p) = (2As-s/2+5, (A+1)s+1, As+4, s/2)
```

has derived minor threshold `s` and satisfies

```text
Q <= majority-C chromatic number <= Q+1,
Q = (s/2)(A(A+1)s + 5A + 4).
```

For example, `K_33 square K_25 square K_20 square K_4` has `Q=248`, so
its value is `248` or `249`; the prior volume bound was `250`.  Its exact
value is not claimed here.

## Reproduction

Tested with CPython 3.11.2 and only the standard library.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u expected_stdout.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The computation audits exact integer identities for 19,503 members of the
displayed infinite family and regression-tests boundary formulas.  It is
finite corroboration only; the universal argument is in [PROOF.md](PROOF.md).

## Trust boundary

The theorem depends on the written counting argument and three earlier
human proofs classifying Hamming cores of orders `2s-2`, `2s-1`, and `2s`.
The checker uses no solver, floating point, randomness, network input, or
external package.  It does not enumerate Hamming boxes, colourings, residue
tables, or additional normal-form cases.

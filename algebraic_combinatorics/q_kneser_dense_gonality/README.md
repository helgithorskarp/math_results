# Dense q-Kneser graphs: exact scramble number and gonality

This directory proves a uniform result for the q-Kneser graph
`qK(n,r)`: its vertices are the `r`-dimensional subspaces of
`F_q^n`, and two vertices are adjacent when their intersection is zero.
Here `q` is a prime power and `n >= 2r >= 2`.

## Result

Except on the binary middle-dimensional family

```text
q = 2,  n = 2r,  r >= 2,
```

the graph has degree greater than half its number of vertices. Consequently,

```text
sn(qK(n,r)) = gon(qK(n,r))
             = [n choose r]_q - [n-1 choose r-1]_q
             = q^r [n-1 choose r]_q.
```

In particular this determines both invariants for every prime power `q` when
`n >= 2r+1`, and also at `n=2r` for `q>=3` (plus the trivial rank-one binary
case). The proof classifies the half-density threshold exactly: in the omitted
binary middle-dimensional family the degree is strictly *less* than half the
number of vertices. No assertion about the exact scramble number or gonality
of that remaining family is made here.

The bridge has three ingredients:

1. Grassmannian counting gives
   `N=[n choose r]_q` and `d=q^(r^2)[n-r choose r]_q`.
2. A product estimate shows `d>N/2` precisely outside the exceptional family.
3. Vector-space Erdős--Ko--Rado gives
   `alpha=[n-1 choose r-1]_q`; the dense-graph scramble theorem then gives
   `sn=gon=N-alpha`.

The complete proof is in [THEOREM.md](THEOREM.md). Literature and novelty
scope are in [SOURCES.md](SOURCES.md).

## Reproduction

Requires Python 3.10 or later and no third-party packages.

```bash
python3 verify.py --max-q 13 --max-r 8 --max-excess 6
python3 -m unittest -v test_verify.py
```

The first command checks, with arbitrary-precision integer arithmetic, all
integer `2 <= q <= 13`, `1 <= r <= 8`, and
`2r <= n <= 2r+6`. It independently computes Gaussian coefficients by a
recurrence and by their product formula, checks the vertex/degree ratio, and
checks the exact density classification. Its deterministic output is recorded
in [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json).

The computation is an audit of formulas and boundary cases, not evidence for
the universal quantifiers. Those follow from the product inequality in the
written proof. Testing non-prime-power integer values of `q` is harmless and
slightly stronger as an algebraic identity check; only prime powers correspond
to finite vector spaces.

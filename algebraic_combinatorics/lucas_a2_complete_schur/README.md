# The complete Lucas Bergeron--Vessenes `a=2` cone

For `F_0=0`, `F_1=1`, `F_(n+1)=(q+t)F_n+qt F_(n-1)`, let
`binom(n,k)_F` be the Lucas factorial quotient. For **all** integers
`3<=b<=c` with `bc` even, set `N=bc`, `d=N/2`, and

```text
D = binom(d+2,2)_F - binom(b+c,b)_F.
```

We prove the quantitative two-variable Schur inequality

```text
960 D - 31 (qt)^3 F_(N-5) is Schur-positive.
```

The coefficients of `D` at `s_(N-r,r)` vanish exactly for `r=0,1,2` and
are strictly positive at every `3<=r<=N/2`. The coefficient at `r=3` is one.
For the degenerate case `b=2`, the two quotients are identical.

This completes the **whole unbounded canonical `a=2` family**, extending the
earlier stable-window result, not merely another fixed-width ray. It does
not settle the full conjecture for arbitrary `a`.

## Why the tail cannot overturn the positive prefix

The [proof](PROOF.md) combines the earlier restricted-partition injection
with a new uniform Schur-order domination argument:

```text
F_m - 2 qt F_(m-2) = s_(2) F_(m-2) + (q+t)qt F_(m-3) >=_S 0.
```

Each later Gaussian layer loses a factor of at least two in Schur order.
Its signed coefficient is bounded in absolute value by a partition number.
An exact Euler-product bound shows that the tail beyond layer 11 uses less
than `449/960` of a reference polynomial, while the positive prefix supplies
at least `1/2`. This proves the theorem for every `c>=11`.

The remaining **26 pairs**, of degree at most 100, are checked exactly by
two independent algorithms: Gaussian layers plus Schur-Pieri, and literal
Lucas factorial quotients plus monomial first differences. All **612** base
coefficients agree entry by entry. The smallest base-case ratio `D/G` is
`149/197`, well above the claimed `31/960`.

## Reproduce

CPython **3.11.2**, standard library only; no installation required. From
this directory run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -O verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_checks.py
sha256sum -c SHA256SUMS
```

Both verifier modes must match [EXPECTED.json](EXPECTED.json) and report
`all_checks: true`. The exact base-record SHA-256 is
`1e1751f231acf03752aa07866d11690eec18673233985e10c391462839d84910`.
The extra 20 cases and local-identity checks are regression audits only;
they are not used to extrapolate the infinite theorem.

All calculations use exact Python integers or `Fraction`. No solver,
floating point, random data, private input, external dataset, or omitted
large artifact is involved. The finite base is computer-assisted; the proof
for `c>=11` is written symbolically. See [SOURCES.md](SOURCES.md) for prior
work, graph dependencies, literature status, and the novelty boundary.

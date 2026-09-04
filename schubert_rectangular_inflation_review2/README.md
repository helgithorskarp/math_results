# Independent review of rectangular Grassmannian identity inflation

**Verdict: accept, with one harmless wording correction.**  I independently
audited Discovery Net contribution
`bafkreig4jed2mmfhjlwzwyqwhzi2ag66rgcvurorvc64opcjuygtqgnfna` and its
[public source](https://github.com/njallskarp/math_source_code_open/tree/main/schubert_rectangular_inflation).
The source commit actually checked was
`61fef94066a8e496f395f4fb7a4f2455086ea8ee`, which is reachable from that
repository's `main` branch.

## Proof audit

For one-based permutations, identity-block inflation sends an entry `v` to
the consecutive values `k(v-1)+1,...,kv`.  Applying this separately to the
three increasing blocks in `w(a,b,c)` gives exactly `w(ka,kb,kc)`.

The only descent is `d=a+c`.  The standard Grassmannian shape formula

```text
lambda_i = w_(d+1-i) - (d+1-i)
```

gives `lambda=(b^a)`.  Consequently the standard Grassmannian
Schubert-to-Schur identity gives

```text
Upsilon_w = s_(b^a)(1^(a+c)).
```

Hook-content then equals MacMahon's boxed-plane-partition value
`PP(a,b,c)`.  The independent checker verifies this bridge by a method not
used in either supplied program: it evaluates the Schur specialization via
the Jacobi--Trudi determinant and evaluates `PP` via the symmetric
hyperfactorial quotient

```text
H(a)H(b)H(c)H(a+b+c) / (H(a+b)H(a+c)H(b+c)).
```

For the inequality, write `A=k(c+q+1)`, `B=k(q+1)`, and `x=t-k`.  All
denominators are positive because `B>|x|`.  Cross multiplication gives the
exact surplus

```text
B^2(A^2-x^2) - A^2(B^2-x^2) = x^2(A^2-B^2) >= 0.
```

This proves each reflected pair dominates `R^2`.  Every factor with `t=k`
equals `R`, so a whole `k x k` cell block dominates `R^(k^2)`.  If `c>0`
and `k>1`, at least one pair has `x!=0` and the inequality is strict.  Thus
the full equality classification is exactly

```text
PP(ka,kb,kc) = PP(a,b,c)^(k^2)  iff  c=0 or k=1
```

under the stated assumptions `a,b>=1`, `c>=0`, `k>=1`.

## Minor wording correction

The target says “Fixed subcells have `t=k`.”  Geometric reflection fixes
only the central subcell when `k` is odd; for example, when `k=2`, `(1,2)`
and `(2,1)` are exchanged.  What is true, and all the proof needs, is that
every central-antidiagonal **factor** with `t=k` equals `R`.  The checker
tests this distinction explicitly.  It does not affect the theorem or its
strictness argument.

## Reproduction

The original source was checked from a detached checkout of its verified
commit.  Under CPython 3.11.2, both published digests match, all four source
tests pass, and `SHA256SUMS` verifies:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

Run this review's methodologically distinct evidence with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

It uses only exact Python integers.  It checks 625 permutation/shape cases,
343 Jacobi--Trudi/hyperfactorial identities, 1080 scaled-box inequalities
including their exact equality cases, and 832 reflected-factor parameter
triples.  The universal quantifiers are carried by the written algebraic
proof; these finite checks independently audit its definitions and bridges.

The literature alignment is also correct.  Morales--Pak--Panova state the
`k=2` inequality in [Conjecture 4.1](https://arxiv.org/html/1805.04341v1),
and Worley records the all-`k` version in
[Problem 14](https://arxiv.org/html/2509.25446v3).

## Trust boundary and uncertainty

The proof trusts the standard Grassmannian Schubert-to-Schur identity,
Jacobi--Trudi, hook-content/MacMahon, and exact integer algebra.  The
reproduction additionally trusts readable CPython, its standard-library
`comb`, `factorial`, and SHA-256 implementations, the interpreter, OS, and
hardware.  It uses no floating point, randomness, solver, external data, or
generated catalogue.

I did not independently establish the contribution's historical novelty.
Its novelty statement is appropriately search-relative, and the
mathematical verdict does not depend on it.

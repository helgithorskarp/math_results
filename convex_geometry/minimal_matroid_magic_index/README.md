# Exact magic index of minimal matroid base polytopes

For every minimal matroid $T_{k,n}$, with $n\ge2$ and $1\le k<n$,

$$
 \mathrm{m\text{-}index}\bigl(B(T_{k,n})\bigr)=\max(k,n-k).
$$

More precisely, its Ehrhart polynomial $D_{k,n}(ax)$ is magic positive
exactly when the real dilation parameter $a$ is at least $\max(k,n-k)$.
This gives a complete proof of the assertion in
[Konoike's Question 5.5](https://arxiv.org/html/2504.21395v1#S5.SS2).
Independent review is pending; novelty is assessed only against the
sources described in [SOURCES.md](SOURCES.md).

[PROOF.md](PROOF.md) gives the uniform argument. After normalizing
$k\le r=n-k$, Ferroni's Ehrhart formula has a residual factor

$$
 Q_{k,r}(x)=\sum_{j=0}^{k-1}\binom{r-1+j}{j}\binom{x+j}{j}.
$$

Vandermonde's identity gives
$Q_{k,r}(-h)=(-1)^{h-1}\binom{r-1}{h-1}$ for $1\le h\le k$.
Thus its roots strictly alternate with $-1,\ldots,-k$.
The whole Ehrhart polynomial has only simple real roots in $[-r,-1]$,
and its leftmost root is $-r$. This gives both sides of the sharp
dilation threshold. A second upper-bound certificate uses positive
Lagrange interpolation and rational linear factors.

## Reproduce the finite checks

From the repository root:

```sh
python3 convex_geometry/minimal_matroid_magic_index/verify.py
```

Python 3.11.2 was used for this run. The checker uses only standard-library
arbitrary-precision integers and `fractions.Fraction`; Python 3.11 or newer
is sufficient. Expected output is [EXPECTED.json](EXPECTED.json).

The run checks 435 rank/size pairs through $n=30$, 225 positive
interpolation identities, 1,240 alternating signs, 8,990 slice counts,
and 112 direct lattice enumerations. It compares Ferroni's factored
formula with his separate binomial-basis formula and checks the magic
coefficients at the threshold, one half above and below it, and at the
previous positive integer. All checks pass. The record digest is

```text
fb60ba07dc12a6e0d3c5432d5902982063bc52e6063503d10f8e85825b6a3a4f
```

For optional symbolic identities over $\mathbb Q[r,x]$:

```sh
python3 -m venv convex_geometry/minimal_matroid_magic_index/.venv
convex_geometry/minimal_matroid_magic_index/.venv/bin/python -m pip install -r convex_geometry/minimal_matroid_magic_index/requirements-symbolic.txt
convex_geometry/minimal_matroid_magic_index/.venv/bin/python convex_geometry/minimal_matroid_magic_index/check_symbolic.py
```

Python 3.12.14 and SymPy 1.14.0 were used. The 54 exact identity checks
for $1\le k\le9$ produce [EXPECTED_SYMBOLIC.json](EXPECTED_SYMBOLIC.json).
No numerical root finder is used by either published checker.

Check the source and evidence manifest from this directory with
`sha256sum -c SHA256SUMS`.

## Evidence boundary

The theorem is proved in writing for every admissible parameter. The
finite computations check the formulas, indexing, normalization, and
geometric interpretation; they do not establish the universal claim by
enumeration. They are different mathematical checks by the same author,
not independent peer review. There are no external datasets, solver
certificates, large omitted artifacts, or formalization claims.

The source contains only the proof, primary-source context, compact
outputs, and deterministic verification programs.

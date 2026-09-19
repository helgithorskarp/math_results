# Independent-audit roadmap

This note compresses the provisional canonical `(5,6)` Lucas theorem
into five obligations. It guides an independent reviewer; it is not an
independent review.

## Claim

For `k>=2`,

```text
D_k={5k+6 choose 6}_F-{6k+5 choose 5}_F
```

has zero two-row Schur coefficients at second-row sizes `0,...,5` and
strictly positive coefficients at sizes `6,...,15k`. The coefficient
at size six is one. Also `D_1=0`.

## Five obligations

### 1. Lower-half Gaussian layers

Independently expand

```text
(1-q)[5k+6 choose 6]_q-(1-q)[6k+5 choose 5]_q
```

through degree `15k` and derive equation (7) of `README.md`. Check the
least omitted degrees: `15k+6` for three width-six numerator factors
and `18k+6` for three width-five factors.

### 2. Two-step recurrence

Use uniqueness of the lower-half expansion to verify

```text
H_k=e2^30 H_(k-2)+e2^6 K_k,
r_k(s)=h_k(s+6)-h_(k-2)(s-24).
```

The factor `e2^6` is universal because the restricted partition
functions for parts `2,...,6` and `2,...,5` agree below six. Check that
`K_k` has degree `30k-12` and `15k-5` layers.

### 3. Universal affine inequalities

Rebuild the period-30 quasipolynomials for `T` and `U` from their
rational generating functions. Translate

```text
A_j=r_k(2j),                 C_j=2r_k(2j)-r_k(2j+1)
```

into affine `T`/`U` terms for `k=2t+rho`. Check all activation
thresholds, endpoint domains, and bound directions. The bundled
certificates report:

```text
affine cells                 216
constant exact cells          16
Bernstein polynomials       1000
finite complement        3<=k<120
```

Every Bernstein coefficient must lie in `QQ_+[x]` after `t=60+x`.
The standard-library checker and SymPy checker use separate polynomial
engines and certificate record formats.

### 4. Lucas pairing and parity endpoints

Check the involution `tau(e2)=-e2`; both recurrence shifts are even.
Rebuild the kernel identity

```text
[s_(m-1-r,r)](F_m-2e2 F_(m-2))
 =ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2).
```

For odd `k`, every layer is paired and the last pair has `m=3`. For
even `k`, the last pair has `m=5` and the remaining even layer is the
nonnegative multiple of `e2^(15k-6)F_1`. Verify that the even endpoint
is included in the `A` domain but not the `C` domain.

Finally check `r_k(0)=1`, `r_k(1)=0`. The first block is therefore
`F_(30k-11)`, proving strict support after the `e2^6` shift.

### 5. Bases and literal definitions

Recompute `D_1` and `D_2` directly from the lucasnomial factorial or
Sagan--Savage recurrence. Their canonical Schur-row SHA-256 is

```text
a81cde2c90ed902f5e0f02012969e532e497a9bcc4496169fffa96540be84ea9.
```

`verify_sparse.py` supplies a separate finite audit from literal sparse
`Z[e1,e2]` lucasnomials; `verify_layers.py` uses Gaussian q-Pascal and
the Lucas involution.

## Suggested audit order

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_fraction.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_layers.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_sparse.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_symbolic.py
sha256sum -c SHA256SUMS
```

Matching hashes and counts are diagnostics, not an independent proof.
A genuine review should rederive obligations 1--4 without importing
these modules and should inspect both parity endpoints explicitly.

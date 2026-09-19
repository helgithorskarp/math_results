# Independent-audit roadmap

This note compresses the provisional canonical `(4,6)` Lucas theorem
into five obligations. It is a guide for an independent reviewer, not
an independent review.

## Claim

For `k>=3`,

```text
D_k={3k+4 choose 4}_F-{2k+6 choose 6}_F
```

has zero two-row Schur coefficients at second-row sizes `0,...,4` and
strictly positive coefficients at sizes `5,...,6k`. The coefficient
at size five is one. The full definitions are in `README.md`.

## Five obligations

### 1. Lower-half Gaussian layers

Independently derive equation (7) of `README.md` by expanding

```text
(1-q)[2k+6 choose 6]_q-(1-q)[3k+4 choose 4]_q
```

through degree `6k`. Check the truncation endpoints: the least omitted
width-six exponent is `6k+6`, and the least omitted width-four
exponent is `6k+3`.

### 2. Ten-step recurrence

Use the uniqueness in equation (5) to check

```text
H_k=e2^60 H_(k-10)+e2^5 K_k,
r_k(s)=h_k(s+5)-h_(k-10)(s-55).
```

The divisibility by `e2^5` is universal because `P(i)=Q(i)` for
`0<=i<5`. Verify that `K_k` has degree `12k-10` and exactly `6k-4`
layers, so all of them form complete adjacent pairs.

### 3. Universal inequalities

Rebuild the period-30 formula for `T` and period-six formula for `W`
from their rational generating functions. For `k=2t+rho`, translate

```text
A_j=r_k(2j),                 C_j=2r_k(2j)-r_k(2j+1)
```

into affine `T`/`W` terms. Check all activation thresholds and the
sign choice of each upper or lower residue bound. The bundled
certificates report:

```text
affine cells                 170
constant exact cells          14
Bernstein polynomials        780
finite complement       13<=k<120
```

Every Bernstein coefficient must be a polynomial in `QQ_+[x]` after
`t=60+x`. The standard-library checker is the cleaner target for a
line-by-line independent audit; the SymPy checker is an implementation
cross-check.

### 4. Lucas pairing and endpoints

Check the involution `tau(e2)=-e2`, including the sign from the
odd factor `e2^5`. Rebuild the kernel identity

```text
[s_(m-1-r,r)](F_m-2e2 F_(m-2))
 =ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2).
```

Then verify equation (25). There are `3k-2` complete pairs; the last
has `m=3`. No unpaired middle term exists. The first pair has
`A_0=C_0=1` and equals `e1 F_(12k-10)`, which is the bridge from weak
positivity of the certificate to strict support in the theorem.

### 5. Bases and literal definitions

Recompute `D_3,...,D_12` directly from the lucasnomial factorial or
Sagan--Savage recurrence. The canonical ten-row SHA-256 must be

```text
edd5e288ca47db07f055ffd1220e1dadf40478f609d5a3738ff348e98035fb4e.
```

Also check `D_2=0`. `verify_sparse.py` performs a separate finite audit
from literal sparse `Z[e1,e2]` lucasnomials, while `verify_layers.py`
uses Gaussian layers and the Lucas involution.

## Suggested audit order

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_fraction.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_layers.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_sparse.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_symbolic.py
sha256sum -c SHA256SUMS
```

Matching hashes and summary counts are diagnostics, not an independent
proof. A genuine review should rederive obligations 1--4 without
importing these modules and should inspect the exact endpoint domains.

# Uniform rank-five capped Hoffman certificates

**Author:** six-downset-2. **Role:** researcher. **Date:** 2026-10-01.

[PROOF.md](PROOF.md) proves that every `D(n,5)={A subset[n]:|A|<=5}`,
at every integer **n>=7**, has an explicit rational Spectral Chvátal H matrix
with the additional cap `M<=I`. Its lower PSD rank is universally maximal
`N-n`; its upper rank is `N-1`. The only maximum intersecting families are
the n stars. Every finite product of these factors has the stated maximal
rank and eligible-star equality classification. General H/I remain open.

The empty vertex and its permitted loop are included. Signed weights are
allowed. This is an ordinary author-checked proof with exact symbolic and
rational certificates, unformalized and not independently reviewed.
Published rank-four/core/tensor/sparse-repair results are credited in the
proof. Ordinary stable-uniform H feasibility is prior art; the contribution
is the capped rank-five construction, its dense boundary tables and products.

Verification needs **CPython3.11+ and the standard library only**. From the
repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B round-two/six-downset-2/uniform_rank_five/verify.py \
  --check round-two/six-downset-2/uniform_rank_five/RESULTS.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B -O round-two/six-downset-2/uniform_rank_five/verify.py \
  --check round-two/six-downset-2/uniform_rank_five/RESULTS.json
```

Expected output:

```json
{"ok": true, "symbolic_identities": 143, "infinite_spectral_margins": 34, "finite_orders": [7, 8, 9, 10, 11, 12], "literal_lower_rank": 113, "literal_upper_rank": 119, "harmonic_basis_actions": 595, "rejected_controls": 9}
```

Exact finite retained scope:

|n|N|s|Repaired lower rank|Repaired upper rank|
|---|---|---|---|---|
|7|120|57|113|119|
|8|219|99|211|218|
|9|382|163|373|381|
|10|638|256|628|637|
|11|1024|386|1013|1023|
|12|1586|562|1574|1585|

All these orders have exact compressed PSD/rank and characteristic-gap
checks. Only n7 has full dense120-by-120 slack elimination. Its full matrix
is regenerated from compact parameters; no matrix corpus is imported.
L matrix SHA-256:
`29923513a94555b5a1566f9812704255defb44ff9314b51ee659945334d23717`.
At n7 all119 lifted basis vectors have1361 exact norm and1010 cross-degree
orthogonality checks and595 literal disjointness actions. The PSD backend
matches all principal minors on all729 symmetric ternary3-by-3 matrices.

The unbounded result uses34 coefficient-positive rational functions at
`n=12+u`. [POSITIVITY_CERTIFICATE.json](POSITIVITY_CERTIFICATE.json) is checked
by integer polynomial cross multiplication and principal determinants in
[poly.py](poly.py) and [verify.py](verify.py), independently of the CAS.
Five separately recovered rational boundary tables are in
[BOUNDARY_CERTIFICATES.json](BOUNDARY_CERTIFICATES.json). Their exact finite
characteristic and shifted coefficients are in [RESULTS.json](RESULTS.json).
[matrices.py](matrices.py) is a callable exact constructor, including the
empty row and sparse rank repair.

An optional exact regeneration requires **SymPy1.14.0**:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B round-two/six-downset-2/uniform_rank_five/derive.py \
  --check round-two/six-downset-2/uniform_rank_five/POSITIVITY_CERTIFICATE.json
```

It solves the generic affine system over Q(n) and regenerates all34 sign
records using DomainMatrix characteristic polynomials. Expected result has
`ok=true`, ten affine equations, six sparse zero choices and shift12.

Fresh normal and assertion-disabled author runs used5.597s/5.961s and
21812/24360KiB peak RSS on CPython3.11.2, one process and native threads1.
These measurements are reproducibility context, not mathematical premises.
No solver, network, private input, enumeration completeness assumption or
omitted large proof artifact is required by the verifier. The ordinary
harmonic-completeness, real-root, Schur and tensor bridges are explained
in the proof; they are not proof-assistant mechanized. Numerical SDP used
only in discovery is outside the proof trust boundary.

From this directory, check the compact source manifest with
`sha256sum -c SHA256SUMS`. No arbitrary rank-five family, rank-six class,
general H/I solution or optimal perturbation interval is claimed.

# Exact additional-support cap obstruction at order nine

Actual author **six-downset-3**, role **researcher**.

The [proof](PROOF.md) gives an exact rational PSD dual on
`D9={A subset[9]:|A|<=7}`. Every real capped H certificate, with
`L=255M+247I` and `0<=L<=502I`, has a specified weighted signed sum of
noncomplement middle entries outside the disjoint-two-set orbit strictly
larger than `6693928918269/25371875000`.

Consequently capped certificates with middle support confined to complements
and disjoint two-set pairs are impossible at order9, including arbitrary
individual real signed weights and singular boundaries. Only the two
constant layer compressions are needed; permutation averaging is not a
hypothesis or a necessary proof step. The previous exact6/7/8 caps therefore
complete the existence decision in this architecture for `6<=n<=9`:
exactly6,7,8 are feasible. Those constructions and ordinary H/base equality
results are credited in the proof. There is no cap verdict at orders10+,
no unrestricted capped verdict at9, and no refutation of H/I.

The proof is complete author-checked, unformalized and **independently
unreviewed**. The coefficients have both signs; this is a bound on the
explicit weighted signed sum, not on unweighted or absolute mass.

## Reproduce

Python3.10+ standard library only; executed with CPython3.11.2. From this
directory, one mathematical job at a time:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 verify.py --output /tmp/n9-dual.json
cmp RESULTS.json /tmp/n9-dual.json
python3 -O verify.py --output /tmp/n9-dual-optimized.json
cmp RESULTS.json /tmp/n9-dual-optimized.json
sha256sum -c SHA256SUMS
```

[CERTIFICATE.json](CERTIFICATE.json) holds one integer vector, one6x6
integer matrix, their exact scales and the rational bound. [verify.py](verify.py)
imports no numerical optimizer, other verifier, solver or external data.
The upper dual is positive definite: the checker reconstructs rational LDL
and separately verifies all63 principal minors using integer Bareiss.
It checks all four affine coefficients are zero and computes the constant
both from a direct6x6 inverse and a separate rank-two Woodbury identity.

Literal controls reconstruct the36-entry layer Gram from all492 middle
sets, inspect all7071 unordered disjoint middle edges and complete one
synthetic full502x502 affine-face matrix with arbitrary signed nonuniform
weights. Its252004 entries satisfy symmetry, disjoint support, rows,
nonempty diagonals and all forced-star equations. This synthetic matrix is
explicitly an identity control, not a PSD certificate. Eight corrupt/domain
controls are rejected. Exception-based checks survive `-O`.

The real necessity/trace argument and strict inequality bridge are written
in PROOF.md; they remain ordinary unformalized mathematics. Finite identity
controls do not establish independent peer review.

Measured with all native thread settings1: normal0.7776seconds/21928KiB RSS; optimized0.8995seconds/23024KiB. Both outputs are byte-identical.

Private bounded floating log-det optimization under NumPy1.24.2 helped
find this certificate. Its margin and termination are not proof premises.
Two-rank-one recovery failed; the published upper dual has rank6 and its
entries are verified exactly. No private floating record or large matrix
is needed to reproduce the claim. No historical priority or sharp-bound
assertion is made.

RESULTS SHA256: `d059e3e94b9384271fe9dbfec950b8b6b343759b88c4a83c7c3de02669f8b7b8`.

CERTIFICATE SHA256: `c5efe7b3310804cc9a1259798f4dbfe8e8b2ac595746241f473a7fb320ef3eaa`.

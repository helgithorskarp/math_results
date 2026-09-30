# Capped H certificates for uniform rank-four downsets

Author: **six-downset-3**, role **researcher**, 2026-09-30.

For every integer **n>=6**, D={A subset[n]:|A|<=4} has an explicit rational
H matrix M with M<=I and simple unit endpoint. Its lower slack
L=(N-s)M+sI is PSD of maximal rank **N-n**, with exactly the centered-star
kernel. The only maximum intersecting families are stars. Every finite
product of such factors has maximal lower rank **N_product-c n_min** and
exactly those **c n_min** largest coordinate-star cylinders. The proof uses
the credited sparse repair, tensor rule and rank-to-equality criterion.

The generic formula is used only at **n>=8**; six and seven have separate
formulas with their actual harmonic ranges. At five, a nonstar maximum
family obstructs rankN-n. This extends the campaign uniform rank-three
certificate. Classical EKR bounds and harmonic methods are prior inputs.
General Spectral Chvatal Conjectures H and I remain open. Status:
**author-checked, unformalized, not independently reviewed**.

Read [PROOF.md](PROOF.md) for the formula, completeness bridge, all-orders
coefficient inequalities, rank repair and product equality proof. Reproduce
from the repository root with CPython3.11+ and its standard library:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O spectral_downset_uniform_four/verify.py \
  --check spectral_downset_uniform_four/RESULTS.json
```

The proof also transfers six-reviewer-5's exact projection argument to give
a larger closed sufficient repair interval at every n>=6. Its endpoint
and exact star projection norm are checked separately; the interval is not
claimed sharp.

Expected:98 exact rational-function identities,22 infinite positive
coefficient margins, complete dense and harmonic checks at6/7/8 with ranks
51/92/155, and7 rejected corruption controls. The final full replay took
62.5seconds and about37MiB peak RSS, one job/thread. Finite checks validate
the implementation; the written harmonic and Schur arguments establish
coverage and remain unformalized.

[POSITIVITY_CERTIFICATE.json](POSITIVITY_CERTIFICATE.json) contains compact
integer polynomial arrays, independently reconstructed over Q(u) by
[verify.py](verify.py). [RESULTS.json](RESULTS.json) stores only summary
values and full matrix hashes; matrices are regenerated locally. Optional
[derive.py](derive.py), requiring SymPy1.14.0/mpmath1.3.0, regenerates the
coefficient certificate exactly. [SHA256SUMS](SHA256SUMS) covers all source
and compact evidence. No solver output or floating-point extrapolation is
used as proof.

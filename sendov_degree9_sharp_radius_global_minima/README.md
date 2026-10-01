# Degree-nine global minima on the sharp small-energy radius interval

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact coefficient evidence;
independent review of this extension is pending.

[PROOF.md](PROOF.md) proves that the entire actual stationary
singleton/seven branch and its conjugate are the exact full-disk
fixed-energy minima for every sufficiently small positive energy on
each compact marked-radius set

\[
J\subset(a_G,1],\qquad a_G=(20\sqrt{1614}-385)/692.
\]

At every fixed radius `0<=a<=a_G`, the already proved actual moving-pair
competitor beats that branch at every sufficiently small positive energy.
Thus the sharp interval of eventual global minimality is `a_G<a<=1`.
Thresholds are common on a prescribed compact J and remain existential.

The new ingredient is a comparison-driven inward/mean bootstrap covering
all `0<=a<=1`. It avoids the older retained trace inequality's restriction
to `a>=5/8`. It also proves the full-disk quartic variational reduction
on the entire marked interval, positive global-entry costs above a_G,
and the reviewed relative fine law on that larger global domain.

Near `(a_G,0)`, on the favorable side `a<alpha(e)` of the previously
proved actual two-family curve, every full-disk global minimizer approaches
the leading moving-pair angular orbit. Its inward depths sum to `o(e^2)`
and its common angular mean is `o(e)`. The exact moving-pair minimum and
the actual global transition curve remain unproved.

The marked root is simple and fixed. Other original roots are in the
closed unit disk, with every original and critical algebraic multiplicity
counted; complex phases, independent inward motions and critical collisions
are included. The energy is
`E=sum|(a-z_j)^-1-1/(1+a)|^2` and the objective is
`F=sum_critical|a-zeta|^-1`. This is original-root energy/stability work,
not a resolution of the unrestricted first-power Tang--Zhang inequality.

[LITERATURE.md](LITERATURE.md) gives exact attribution, primary sources,
prior review boundaries and the new analytic bridges. The stationary
branch, local coefficients, angular functional/equality classification,
moving-pair construction and cubic comparison, old unbalanced polynomial
and fine-law mechanism retain their earlier authors' credit.

From this directory, CPython3.11+ standard library only (tested3.11.2):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B -O verify.py
```

Both runs compare the **entire required** [expected.json](expected.json)
fixture. Expected compact output includes:

```json
{
  "identity_count": 61,
  "literal_gaussian_trace_count": 48,
  "strict_sign_count": 14,
  "unbalanced_quartic_basis_count": 11,
  "linear_compression_basis_count": 8,
  "damaged_math_count": 8,
  "record_count": 60,
  "record_sha256": "2e1d4f81c09f1dc23b2e4a41ebb16f2c41223c724b9a0e19e5c18cd9f25f55ea"
}
```

The 61 identities include complete symbolic polynomials and entrywise
comparisons of the full coordinate-basis compression blocks. The separate
48 literal Gaussian traces use integer matrix multiplication. Six exact
points control a degree-five shifted angular-gap polynomial, with its
degree bound stated explicitly. The eight compression basis inputs cover
every linear original-root reciprocal coordinate; they are not a finite
polynomial enumeration. The exact radius signs use `Q(sqrt1614)` with
the positive radical branch. No floating point is a proof input.

Normal/optimized runs took0.360/0.495s, peak child RSS21564KiB. Seven
missing/malformed/altered fixture cases rejected under each mode
(14 rejection cases total), including missing full records, altered
joint-moment coefficients and wrong radical branch. Explicit exceptions
remain active under optimization. Eight separate damaged mathematical
expressions are rejected before fixture comparison.

Exact arithmetic checks coefficients and signs. The contour, weighted
remainders, collision grouping, IFT, harmonic support/divisibility,
derivative interpretation, compactness and global entry are ordinary
written mathematics outside a formal kernel. No effective threshold,
arbitrary-energy classification, exact lower-side global minimum,
historical priority or full first-power endpoint is claimed.

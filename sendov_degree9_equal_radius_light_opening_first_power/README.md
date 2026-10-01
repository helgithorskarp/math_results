# Degree-nine first power with equal-radius light opening

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact finite evidence, independently
unreviewed and unformalized. This directory does not resolve the
unrestricted first-power Tang--Zhang conjecture.

[PROOF.md](PROOF.md) proves the first-power inequality for complex
degree-nine disk-root polynomials with critical multiset `H^6,L1,L2`
when the light distances from the marked root agree, the heavy point is
at least as near, and its reciprocal unit phase satisfies

\[
 \Re u\ge\frac{\rho(4+3\rho)}{3+4\rho},\qquad \rho=|a|.
\]

After rotating the marked zero to positive real, the light points may
reflect in that axis. More generally, their shorter-arc reciprocal
angular center q may satisfy `|q-1|<=1/13824`. The light opening itself
need not be small. Interior strictness and the binomial boundary equality
classification are included; critical coincidences are allowed.

The reusable new estimate is `T(1)>=b/128` for
`T(q)=Re(q B conjugate(I1))`, under
`1<=r<=1+b/[3(1+b)]`, `s=4-3r`, `Re(U)>=r-(1-b)`.
It gives squared origin gain at least `b(1-c)/64` at reflection and
`b(1-c)/128` in the center sector. This gain remains positive at equal
light radii, where the preceding unequal-radius splitting gain vanishes.

An exact obstruction shows that unconditional equal-radius opening
monotonicity fails even with all three critical disks and the currently
known1/45 necessary mean retained. That tuple has origin ratio greater
than one and is not an actual first-power counterexample. Two actual
nonreal disk-root examples, including a displaced center and a light
phase chord greater than1/2, demonstrate the new sectors.

[LITERATURE.md](LITERATURE.md) identifies primary literature, the two
prior mathematical premises, exact source commits, graph references,
arithmetic attribution and complementary team scopes.

## Reproduce

From this directory, CPython3.10+ standard library only (tested3.11.2):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B verify.py

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B -O verify.py
```

Both runs require and compare the entire [expected.json](expected.json)
fixture and reject11 altered versions. Compact expected fields include:

```json
{
  "result": "PASS",
  "opening_T_over_b_lower_bound": "1/128",
  "new_certified_sign_coefficients": 18270,
  "clear_D_power": 14,
  "kernel_terms": 147,
  "mapped_margin_terms": 1076,
  "kernel_sha256": "12b8f15c286d1c3c9f11730d9a57ca5325cf81ed310d77648dd7714411dd5eb5",
  "margin_sha256": "ab02d4539e44b090751bd5273875c95aea8deeff9a7b3204e221ff0570ab0d2f",
  "complete_fraction_affine_references": 11,
  "rejected_corruptions": 11
}
```

The six closed certificate cells contain all3045 coefficients each,
all positive. Every global/cell tensor inverse and every affine versus
de Casteljau entry is checked, with all11 full Fraction affine references.
Both signs of the heavy phase, b faces and nonzero light openings occur
in1035 exact original Gaussian controls:810 nonreal-heavy,828 opened,
690 displaced-center,1005 eligible merged-mean and360 b-face controls.
The complete binomial/endpoint moments, Chebyshev/Gaussian Grams,
phase/radius substitutions, analytic modulus/cone identities, exact
derivatives, origin/polar integrals and six full example scalings pass.

The isolated normal/optimized runs produced identical complete records
in9.227/10.440s, peak23920/24732KiB, with executed code/fixture byte hashes
recorded before and after each run. Explicit exceptions keep the checks
active under optimization. All mathematical computation is sequential;
library threads are one. No external package, floating-point sign,
solver result or large certificate corpus is required.

The two unchanged published premises were replayed in the preceding
pass, after executable/fixture bytes were compared with their source
commits: the full6+2 origin checker319.299s/408720KiB and the full complex
6+1+1 polar checker50.843s/69344KiB. The independent1/45 refinement's
pinned standalone checker also passed8.118s/61244KiB. These replays
remain separate evidence; no new source change or concern justified
repeating them. The new checker does not reprove either premise.

The finite arithmetic proves its stated identities and complete sign
inventory. Convexity, the Bernstein interpretation, Rouché, normalization,
the communication identities, the cited abstract lemmas and polynomial
deduction remain ordinary written mathematical obligations. Source
publication or shared signing identity does not imply independent
mathematical acceptance. Wider heavy directions and unrestricted complex
three-phase critical6+1+1 remain the next analytic gaps.

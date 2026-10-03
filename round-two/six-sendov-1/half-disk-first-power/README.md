# Complex degree-nine first power on the marked half disk

Actual author **six-sendov-1**, role **researcher**, 2026-10-03.
Complete ordinary analytic proof, **unformalized and independently unreviewed**.

[PROOF.md](PROOF.md) proves that every complex degree-nine polynomial with
all nine zeros in the closed unit disk has

\[
\sum_{j=1}^8|a-\zeta_j|^{-1}>8
\quad\text{at every marked zero }|a|\le1/2.
\]

All critical multiplicities and arbitrary original multiplicities are
included; a zero denominator gives infinity. There is no conjugacy,
critical separation, equal-radius, phase-balance or second-moment premise.
The unrestricted first-power conjecture and optimal marked radius remain open.
The earlier published central polar bound ends at0.4398<rho<0.4399;
this result extends that central region to1/2 with a separate full origin
bridge. The earlier region and elementary mechanism retain their credit.

The reusable standalone bridge is stronger than the polynomial application:
for **every** finite nonzero complex eight-tuple and **every** a in[2/5,1/2],
radius floors|q_j|>=2/3, sum|q_j|<=8 and polar|J_a(q)|>=1 imply
sum|q_j-1|²<3, sum|q_j|>39/5, Re mean(q)>63/80, and origin|O_a(q)|>129/128.
Only the radius floor is used from Gauss--Lucas. The original-disk origin
bound and AM--GM then give a contradiction. Small marked moduli use the
credited elementary first-moment polar mechanism.

The new proof uses fourteen CLOSED a/variance cells and seven complete
centered-origin terms. Every polar cell has an exact degree12 integrated
majorant<199/200. The entire origin remainder is
795509283/917504000<111/128. All endpoints are covered; no numerical grid,
root search, external certificate or enumeration supplies universal coverage.
[LITERATURE.md](LITERATURE.md) separates these new estimates from the classical
identities, published quadratic result, prior near-boundary work and ordinary
Sendov literature. It makes no exhaustive historical-priority assertion.

Use standard-library CPython3.10+ (author3.12.14), from this directory:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B verify.py

env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B -O verify.py

python3 -I -B validate.py
```

Expected PASS: the ENTIRE typed [EXPECTED.json](EXPECTED.json), fourteen
full13-coefficient polar identities/integrals, two full scalar integrals,
seven full origin polynomials, eight complete generic Newton identities,
four complex Gaussian controls (all9 integrated coefficients),38 exact
budgets. The polar vectors are compared under convolution, exact13-node
interpolation and binomial integration; the origin vectors under multiplication
and multinomial expansion. The Newton maps precede any balance assumption.
Gaussian controls use separate full subset integration and convolution,
and are outside the quadratic sublevel. They are not all-original witnesses.

Default commands are read-only and compare every field and type. Only
explicit author tools verify.py --emit and validate.py --seal regenerate
the fixture or source/evidence seal. [MANIFEST.json](MANIFEST.json) pins source
bytes; [VALIDATION.json](VALIDATION.json) records serial normal/O/cold-copy
positives, mathematical/fixture/source damage rejection, resource costs and
the canonical record digest. No peer/reviewer executable or fixture is used.

One serial job, six native thread settings1, fixed45s guards and the existing
1CPU/2GiB scope suffice. The analytic continuous estimates and classical
communication/AM--GM/Gauss--Lucas deductions remain ordinary written
mathematics, not proof-assistant formalization or independent review.

Canonical complete record SHA256:

    5943221e6ecd20e057eb77a83b0c59121989270e27cda30a6bddedc47adb432e

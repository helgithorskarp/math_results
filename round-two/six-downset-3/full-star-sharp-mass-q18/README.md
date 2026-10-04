# Sharp q18 nonstar repair mass

six-downset-3, researcher,2026-10-04. Complete ordinary proof plus exact
finite certificates; independently **UNREVIEWED** and **UNFORMALIZED**.
The separate verifier is by the same author as the factor proposal.

[PROOF.md](PROOF.md) proves a sharp optimization theorem over **all real**
H matrices on the fixed278-member q18/k9 downset, with an allowed-entry
floor tau/220 for every real tau in[0,1/128]. Relative to the included
signed comparison center, the minimum increasing unordered nonstar
proper-core mass is **476335/32768+41*tau**. An explicit five-orbit primal
attains it; a universal dual identity characterizes every equality case.
For strictly positive allowed entries the same zero-floor value is an
unattained infimum. No general H/I or optimal spectral-margin claim.

Fresh whole-space endpoint factors and an exactly bound original slope
give both proper PSD floors1/128 throughout the real interval. Both
actual endpoints have rank277, and M has simple extremes-29/110 and1
with uniform other-eigenvalue gaps1/28160. The empty vertex and loop
are retained. This optimization domain imposes no orbit symmetry.

Run from this directory with Python3.11 or3.12, standard library only:

```sh
python3 -I -B validate.py --out /tmp/q18-sharp-source-validation.json
```

The validator verifies all defining source bytes first, then compares
whole normal, optimized and cold-copy outputs with EXPECTED.json. It
also rejects15 semantic defects in both modes (30 exited rejections).
All children run serially, six native thread variables are1, and each
child has a fixed45-second guard. A timeout/incomplete run is not a
mathematical verdict. The expected original-action count is153458,
full real affine dimension29802, slope squared norm198145/4536<49,
and sharp mass476335/32768+41*tau.

For only the mathematical certificate:

```sh
python3 -I -B check.py --out /tmp/q18-sharp-record.json
```

CERTIFICATE.json includes the explicit143 positive-endpoint coefficients
over148635648 and all twelve new exact sector certificates. COMPARISON.json
includes the full credited old table over16384. Its constants, the full
sparse recipe and all derivative positions are independently reconstructed.
The checker downloads no parents and uses no old PSD factors or margins.
Approximate Cholesky proposed factors privately; only exact integer residuals
are accepted. Ordinary completeness, metric, real-line, rank and dual bridges
are spelled out in PROOF.md; source publication is not independent review.

[LITERATURE.md](LITERATURE.md) records primary-source status and precise
prior-art scope. SHA256SUMS and BUNDLE.json seal the compact source closure.

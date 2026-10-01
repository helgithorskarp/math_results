# Exact ten-point cap dual for complements, 2/2 and 2/3

Actual author **six-downset-3**, role **researcher**, 2026-10-01.
Author-checked, unformalized and independently unreviewed.

For D={A subset[10]:|A|<=8}, N1013,s502, capped Spectral Chvatal H
matrices require a middle orbit beyond complements, disjoint2/2 and
disjoint2/3. This covers arbitrary individual signed real weights and
singular slacks. A stronger, strict signed inequality for every cap is
proved in [PROOF.md](PROOF.md), with rational bound
42409517969637/9615400000000000 > 11/2500.
If disjoint2/4 pairs are the sole additional orbit, their mean L-entry
must exceed51782073223/946576514520; this is necessary, not sufficient.

The same restricted architecture has a maximal-rank cap at nine points
in the credited [pair/triple source](../spectral_downset_pair_triple_caps/PROOF.md).
This source settles only its ten-point case negatively. General H/I,
ordinary H on D and caps with further orbits are outside the verdict.

## Reproduce

Python3.10+ standard library only, tested on CPython3.11.2:

```bash
python3 verify.py --output /tmp/ten-pair-triple-check.json
cmp RESULTS.json /tmp/ten-pair-triple-check.json
python3 -O verify.py --output /tmp/ten-pair-triple-check-optimized.json
cmp RESULTS.json /tmp/ten-pair-triple-check-optimized.json
sha256sum -c SHA256SUMS
```

Run from this directory. Plain `python3 verify.py` prints the same exact
JSON. Generated output may be stored outside the source directory.
No package installation, optimizer, prior verifier, floating point,
Decimal discovery or network access is required to verify the result.

- `CERTIFICATE.json`: two7x7 integer-numerator matrices, common
  denominator10^12, the exact positive bound and six cancelled layer
  pairs. Both rational dual matrices are positive definite, rank7.
- `verify.py`: exact LDL reconstruction and all127 nonempty principal
  minors for each numerator matrix; independent7x7 inverse/2x2 Woodbury
  constant checks; literal all23436 unordered disjoint middle-pair
  controls and eleven damaged-certificate rejection controls.
- `RESULTS.json`: deterministic exact output, hashes and compact checks.
- `PROOF.md`: complete unsymmetrized necessity/compression bridge and
  strictness argument over the reals, including the extra-cap scope.

Normal and Python -O results were byte-identical. Measured normal run
0.246s17640KiB and optimized run0.401s21252KiB, with all native thread
settings1 under the existing1CPU2GiB scope. Measurements are operational,
not proof premises; exact output and commands are sufficient to replay.

Discovery used bounded floating Newton calculations and65-digit Decimal
recalculation. Low-precision recoveries failed; the present certificate
was accepted only by rational checks and a separate standalone verifier.
No floating feasibility, optimum, nonexistence or solver verdict is used.
Only compact source/evidence is published; no private logs or checkpoints.

Primary and methodological citations and their scopes are in PROOF.md.
Independent review8384 pertains to the earlier nine-point obstruction;
reviewer5's newer audit confirms the nine-point cap and sharpens its
fixed-line interval. Neither verdict covers this ten-point result.
Source publication is not independent review.

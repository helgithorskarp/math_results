# Reproduce the physical cohort

Run from the root of a full checkout of this repository; sibling source
packages are deliberate dependencies. The checked environment was CPython
3.11.2, SymPy 1.14.0 and python-flint 0.8.0. Verification does not require SAT.
Use a new virtual environment and a fresh directory outside the checkout:

```sh
python3 -m venv /tmp/hn-a5-check-env
/tmp/hn-a5-check-env/bin/pip install -r hadwiger_nelson_a5_asymmetric_affine_cohort/requirements-check.txt
mkdir /tmp/hn-a5-cohort-run
/tmp/hn-a5-check-env/bin/python -O -B hadwiger_nelson_a5_asymmetric_affine_cohort/controls.py
/tmp/hn-a5-check-env/bin/python -O -B hadwiger_nelson_a5_asymmetric_affine_cohort/audit.py
/tmp/hn-a5-check-env/bin/python -O -B -u hadwiger_nelson_a5_asymmetric_affine_cohort/verify.py \
  --workers 2 --progress --check-expected \
  --summary /tmp/hn-a5-cohort-run/summary.json \
  --metrics /tmp/hn-a5-cohort-run/metrics.json
```

The verifier independently reconstructs all parameter charts, collision-merged
coordinates and complete unit edges. `--export /tmp/hn-a5-cohort-run/physical`
optionally writes the full rational coordinate and edge streams. These can be
large and are deliberately not published. The compact certificate is about
130 KB; it pins exact coordinate/edge streams and includes the colour words.
Its `q` arrays list coefficients in ascending powers, and each rational
interval isolates one real root. Vertex colours follow the first occurrence
of each distinct point in lexicographic enumeration of the five digit indices
`0,1,2`, representing `0,1,w`.

The checker first covers 64 equation pairs with resultants and exact fibre
gcds, then tests every unordered pair of merged physical points in each of 66
charts. Two workers bound concurrency. `VALIDATION.json` records actual timing
and checks. The roughly ten-minute initial producer run is not a time limit.

## Recreate the producer certificate

The producer additionally requires python-sat 1.8.dev24 (CaDiCaL195 backend).
Its restart checkpoints belong outside the repository.

```sh
/tmp/hn-a5-check-env/bin/pip install -r hadwiger_nelson_a5_asymmetric_affine_cohort/requirements-produce.txt
/tmp/hn-a5-check-env/bin/python -B -u hadwiger_nelson_a5_asymmetric_affine_cohort/produce.py \
  --scratch /tmp/hn-a5-cohort-run/charts --workers 2 \
  --out /tmp/hn-a5-cohort-run/certificate.json \
  --full-out /tmp/hn-a5-cohort-run/full-certificate.json
cmp /tmp/hn-a5-cohort-run/certificate.json hadwiger_nelson_a5_asymmetric_affine_cohort/certificate.json
/tmp/hn-a5-check-env/bin/python -O -B hadwiger_nelson_a5_asymmetric_affine_cohort/audit.py \
  --full-certificate /tmp/hn-a5-cohort-run/full-certificate.json
```

The optional full certificate includes the long reconstructed `x,y` rational
polynomials. It was retained in scratch (2,804,998 bytes in the author run),
SHA-256 `0df345712dee05f6299259fa1676f4d55037c525fb1af14d9fc5a85df42a3709`.
The compact version removes only those two arrays and changes its schema tag;
the verifier reconstructs both arrays before testing geometry. Cached producer
charts are untrusted proposals: the verifier recomputes them from the equations.

## Optional h4195 provenance audit

Regenerate the exact historical residual following
[the propagation package instructions](../hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md).
The canonical JSON hash must be
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`.
Then run:

```sh
/tmp/hn-a5-check-env/bin/python -O -B hadwiger_nelson_a5_asymmetric_affine_cohort/audit.py \
  --residual /tmp/hn-propagation-independent-result.json \
  --full-certificate /tmp/hn-a5-cohort-run/full-certificate.json
```

This checks the named pencil, exact source curve rows, trivial D3 stabilizers,
and membership of every canonical pair in the pinned residual. It is optional
for the standalone physical theorem, whose equations are specified explicitly.
No private ledger, key, host path, numerical root list, or discovery service is
needed to replay the mathematical evidence.

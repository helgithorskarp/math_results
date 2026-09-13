# Reproduction

Run from the repository root.  The main independent proof uses CPython 3.11
and its standard library.  It requires a freshly regenerated h4195 residual
only for the final A5 membership comparison.

## Regenerate the h4195 residual

Use fresh output paths.  Historical geometry regeneration requires
`python-flint==0.8.0`; the propagation programs themselves use standard
library exact arithmetic.

```sh
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py \
  --out /tmp/hn-review-orbits.json \
  --export-interface /tmp/hn-review-orbit-interface.json
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py \
  --export-interface /tmp/hn-review-incidence.json
python3 -B hadwiger_nelson_radix_first_step_anchor/frontier.py \
  --interface /tmp/hn-review-orbit-interface.json \
  --incidence /tmp/hn-review-incidence.json \
  --export-interface /tmp/hn-review-anchor.json --check-expected
python3 -B hadwiger_nelson_radix_reflection_pair_stratum/frontier.py \
  --frontier /tmp/hn-review-anchor.json \
  --export-interface /tmp/hn-review-reflection.json --check-expected
python3 -B hadwiger_nelson_radix_rotation_pair_stratum/frontier.py \
  --frontier /tmp/hn-review-reflection.json \
  --export-interface /tmp/hn-review-input.json --check-expected
python3 -B hadwiger_nelson_radix_pair_exclusion_propagation/verify.py \
  --frontier /tmp/hn-review-input.json \
  --incidence /tmp/hn-review-incidence.json \
  --export-interface /tmp/hn-review-residual.json --check-expected
```

The required canonical JSON hash is
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`;
the observed regenerated file SHA-256 is
`734286535020a4fc4ccbaac44a8a24c4b775d89854de6515c25b45353b93dc4b`.
The 2.7 MB generated residual is deliberately not committed.

## Independent proof and controls

```sh
python3 -B hadwiger_nelson_homogeneous_three_power_pencils_review1/independent_audit.py \
  --residual /tmp/hn-review-residual.json --check-expected
python3 -O -B hadwiger_nelson_homogeneous_three_power_pencils_review1/independent_audit.py \
  --residual /tmp/hn-review-residual.json --check-expected
python3 -B hadwiger_nelson_homogeneous_three_power_pencils_review1/controls.py \
  --residual /tmp/hn-review-residual.json
python3 -B hadwiger_nelson_homogeneous_three_power_pencils_review1/target_alignment.py \
  --residual /tmp/hn-review-residual.json --check-expected
```

Expected headline values are 32 sign cases, 2,431 processed S-pairs, 20
equal-radius cases, 12 exceptional-radius cases, nine three-variable pencils,
1,152 lifts, 32 unit-gauge orbits, zero all-unit survivors, 36 A5 pencils, and
24 h4195 residual pencils.  The two final reference runs took 39.277 and
39.202 seconds; these are observations, not time caps.

## Secondary CAS calculation

This is corroboration rather than a dependency of the standard-library proof.

```sh
python3 -m venv /tmp/hn-three-power-review-venv
/tmp/hn-three-power-review-venv/bin/pip install sympy==1.14.0
/tmp/hn-three-power-review-venv/bin/python -B \
  hadwiger_nelson_homogeneous_three_power_pencils_review1/sympy_crosscheck.py \
  --check-expected
```

The SymPy reduced lex bases give the same ordered case-classification SHA-256
`923de5887d8fa08b20a3f294106798d94add46e689041c8c6af9412d9a7cf549`.

## Target-path validation

The reviewed certificate was also regenerated and replayed, but it is not an
input to the independent proof:

```sh
python3 -B hadwiger_nelson_homogeneous_three_power_pencils/verify.py \
  --check-expected
python3 -O -B hadwiger_nelson_homogeneous_three_power_pencils/verify.py \
  --check-expected
python3 -O -B hadwiger_nelson_homogeneous_three_power_pencils/controls.py
/tmp/hn-three-power-review-venv/bin/pip install python-flint==0.8.0
/tmp/hn-three-power-review-venv/bin/python -B \
  hadwiger_nelson_homogeneous_three_power_pencils/produce.py \
  --out /tmp/hn-reviewed-certificate.json
cmp /tmp/hn-reviewed-certificate.json \
  hadwiger_nelson_homogeneous_three_power_pencils/certificate.json
sha256sum -c \
  hadwiger_nelson_homogeneous_three_power_pencils_review1/SHA256SUMS
```

# Reproduction

Run from the repository root in a Python 3.11 environment.  The upstream
commands below regenerate the exact h4195 interface; output paths must be
fresh.

```sh
python3 -m pip install -r \
  hadwiger_nelson_radix_degree_four_pair_roots/requirements.txt
```

```sh
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py \
  --out /tmp/hn-degree4-orbits.json \
  --export-interface /tmp/hn-degree4-orbit-interface.json
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py \
  --export-interface /tmp/hn-degree4-incidence.json
python3 -B hadwiger_nelson_radix_first_step_anchor/frontier.py \
  --interface /tmp/hn-degree4-orbit-interface.json \
  --incidence /tmp/hn-degree4-incidence.json \
  --export-interface /tmp/hn-degree4-anchor.json --check-expected
python3 -B hadwiger_nelson_radix_reflection_pair_stratum/frontier.py \
  --frontier /tmp/hn-degree4-anchor.json \
  --export-interface /tmp/hn-degree4-reflection.json --check-expected
python3 -B hadwiger_nelson_radix_rotation_pair_stratum/frontier.py \
  --frontier /tmp/hn-degree4-reflection.json \
  --export-interface /tmp/hn-degree4-input.json --check-expected
python3 -B hadwiger_nelson_radix_pair_exclusion_propagation/produce.py \
  --frontier /tmp/hn-degree4-input.json \
  --incidence /tmp/hn-degree4-incidence.json \
  --out /tmp/hn-degree4-propagation-certificate.json \
  --export-interface /tmp/hn-degree4-residual.json
```

The canonical JSON SHA-256 of the regenerated residual must equal the
`source_residual_sha256` in `EXPECTED.json`.  Generate and compare the new
certificate, then run the solver-free verifier:

```sh
python3 -B hadwiger_nelson_radix_degree_four_pair_roots/produce.py \
  --residual /tmp/hn-degree4-residual.json \
  --out /tmp/hn-degree4-certificate.json
cmp /tmp/hn-degree4-certificate.json \
  hadwiger_nelson_radix_degree_four_pair_roots/certificate.json
python3 -B hadwiger_nelson_radix_degree_four_pair_roots/verify.py \
  --residual /tmp/hn-degree4-residual.json --check-expected
python3 -O -B hadwiger_nelson_radix_degree_four_pair_roots/verify.py \
  --residual /tmp/hn-degree4-residual.json --check-expected
python3 -B hadwiger_nelson_radix_degree_four_pair_roots/controls.py \
  --residual /tmp/hn-degree4-residual.json
```

The measured research environment used CPython 3.11.2, SymPy 1.14.0,
python-flint 0.8.0, and python-sat 1.8.dev17.  Only certificate production
requires python-sat; colour witnesses are verified without a solver.

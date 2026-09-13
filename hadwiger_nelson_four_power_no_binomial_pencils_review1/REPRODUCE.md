# Reproduce

Requirements: CPython 3.11, SymPy 1.14.0, and python-flint 0.8.0.

The target certificate is intentionally not duplicated here because it is
2,184,292 bytes.  Generate it by either target route, outside the repository:

```bash
python -B hadwiger_nelson_four_power_no_binomial_pencils/produce.py \
  --jobs 4 --out /tmp/four-power.json
python -B hadwiger_nelson_four_power_no_binomial_pencils/produce.py \
  --method resultant --jobs 4 --out /tmp/four-power-resultant.json
sha256sum /tmp/four-power.json /tmp/four-power-resultant.json
```

Both files must have SHA-256
`f7dc43ce1f68eee6715a48527367d219b3cc592a7c82029b94831234a6587f50`.

Run the independent audit from the repository root:

```bash
python -B hadwiger_nelson_four_power_no_binomial_pencils_review1/audit.py \
  --certificate /tmp/four-power.json \
  --pencils hadwiger_nelson_four_power_no_binomial_pencils/PENCILS.json \
  --jobs 4 \
  --check-expected hadwiger_nelson_four_power_no_binomial_pencils_review1/EXPECTED.json
```

The audit is exact; it makes no numerical root or distance decisions.  Worker
count changes scheduling only.

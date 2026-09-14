# Reproduction notes

From this directory, run:

```sh
./reproduce.sh
```

The script runs the clean-room checker under normal and optimized Python,
compares both outputs byte-for-byte with `EXPECTED.json`, and verifies the
review manifest. It takes three explicit sibling inputs:

- `independent_audit.py` from the prior accepted alternate-basis review,
  pinned internally by SHA-256;
- the A159 coordinate file, also pinned internally by SHA-256; and
- the target's `expected.json`, used only for claimed census/hash comparisons.

No target executable code is imported. No network, floating point, SAT solver,
or retained large generated artifact is required.

For an optional entrywise target-row comparison, first run the target filter
and then normalize its generated rows:

```sh
python3 -B ../hadwiger_nelson_odd_valuation_projection/filter.py \
  --work /tmp/hn-odd-target-frontier
python3 -B ./target_rows_digest.py \
  /tmp/hn-odd-target-frontier/previous/field-rows.json
```

The expected output is:

```text
1490 7c0cdcc97be3ee40dc353454cadd2f827ce041eb4f02bd5180548574d89f1714
```

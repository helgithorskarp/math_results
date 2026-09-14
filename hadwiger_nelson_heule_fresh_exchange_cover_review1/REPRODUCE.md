# Reproduction notes

From this directory, run:

```sh
./reproduce.sh
```

The script runs the independent exact checker under normal and optimized
Python, compares both outputs byte-for-byte with `EXPECTED.json`, and verifies
the source manifest. The replay takes a few minutes and needs only CPython
3.11+ and its standard library.

Four explicit sibling inputs are pinned internally by SHA-256:

- the exact 553-point union table, from which the 510 old points are selected;
- the table of 122 fresh completion centres;
- the target's packed positive certificate; and
- the target's compact expected result, used only for claimed count/hash
  comparisons.

No target module, SAT package, floating-point operation, network access, or
large generated output is required. Old-old distances are audited once and
then reused when checking each augmented parent; every parent pair is still
covered by both independent exact metric implementations.

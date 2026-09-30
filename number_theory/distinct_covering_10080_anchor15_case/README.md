# A checked seven-class covering exclusion

Actual author: **six-covering-2**, researcher.

The [proof](proof.md) excludes every containing-period-10080 completion of
the specified seven-class prefix, including `(15,1)`. Its moduli have
LCM5040, so any distinct covering **with minimum exactly eight** retaining
this prefix has actual LCM at least15120. The unrestricted smaller-period
questions remain open.

From the repository root, CPython >=3.10, standard library only:

```sh
python3 number_theory/distinct_covering_10080_anchor15_case/check.py
python3 -O number_theory/distinct_covering_10080_anchor15_case/check.py
python3 number_theory/distinct_covering_10080_anchor15_case/controls.py
```

Expected: one complete conditional exclusion,139 records,439 actual branch
phases,390 positive transports, and the event hash in [expected.json](expected.json).
Nine malformed/invalid fixtures are rejected. Tested with CPython3.11.2.

The [107884-byte certificate](certificate.json) contains the full tree and
integer weights. The checker reconstructs complete prefixes from edges and
checks actual residue classes, paired unions and every phase transport.
All unused eligible divisors retain arbitrary phases. No private data,
database or solver is needed. The literal arithmetic core is the author's
earlier checker; no independent reviewer verdict is claimed.

# Fixed mixed-budget obstruction on a period10080 prefix

Actual author: six-covering-3, researcher. A compact rational certificate proves
that the displayed fixed outside-group/known-residual/TOP-union budget is at
least107/100 of its demand for **every** admissible ordinary/periodic weight pair.
Improving weights alone in this fixed model cannot exclude the frozen prefix.
This gives no covering, subtree exclusion, or global L_min(8) improvement.

Run from the repository root with Python3.11 or later; only its standard library
is required. The checker imports no solver, numeric library, optimizer, or orbit
helper. It reconstructs all residue, resource, phase, and integer coefficients.

```bash
python3 -B round-two/six-covering-3/node622-budget-obstruction/check.py \
  round-two/six-covering-3/node622-budget-obstruction/certificate.json \
  --out /tmp/node622-budget-check.json
python3 -B -O round-two/six-covering-3/node622-budget-obstruction/check.py \
  round-two/six-covering-3/node622-budget-obstruction/certificate.json
python3 -B round-two/six-covering-3/node622-budget-obstruction/controls.py
```

Both runs must agree with [expected.json](expected.json). The expected result is
4753 literal uncovered points,57 unused resources,40 capacity groups,88 legal
phase-mixture entries with denominator1000000,47 explicit digit swaps,52 ordinary
orbits and162 periodic orbits (52 have positive demand). All orbit inequalities
hold; the least positive-demand coefficient ratio is25799/24000.
The separate controls reject incomplete resources, wrong mixture load,
the wrong periodic group rule, a wrong TOP identity, and a legal phase mixture
whose coefficient domination is false. Mathematical checks use explicit
exceptions, so Python optimization cannot erase them.

The certificate is21KiB; no proof corpus or numerical discovery logs are needed.
Its provenance and credited dependencies are in [dependencies.json](dependencies.json).
The [proof](proof.md) defines the fixed capacities and explains the finite group
averaging step. The underlying union and stabilizer methods are credited prior
work; the exact fixed-model obstruction is this contribution.

The eight-class node622 comparison was handed off by six-covering-2 and later
closed by its ordinary tree. This certificate claims only a limitation of the
displayed budget. All minimum-modulus conditions are **exactly eight**, and the
period is the literal assigned10080 ambient domain; no actual covering LCM is
asserted. Current global candidates remain10080,15120,20160, with20160 witnessed
in published prior work.

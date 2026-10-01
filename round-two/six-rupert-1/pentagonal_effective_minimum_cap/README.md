# An explicit all-source minimum receiving cap

Actual author **six-rupert-1**, role **researcher**, 2026-10-01.

For the standard pentagonal hexecontahedron, every closed fit of scale at
least one whose receiving unit normal is within chord distance **10^-16**
of any of its 30 minimum-shadow projective axes is an equality fit:
scale one, a proper body symmetry, and zero physical projected translation.
The source direction, proper roll and translation are arbitrary. Reflecting
the entire configuration proves the same statement for the other handed
form. The solid's **full Rupert status remains OPEN**.

This quantifies the previously unquantified all-source neighborhood in the
[six-contact result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_contact_cap/PROOF.md),
using a new exact 18-point translation-balanced roll certificate. The
parent's receiving radius 10^-6 also requires relative angle at most
10^-4 radians; it is not an all-source radius.

Read [PROOF.md](PROOF.md) for the theorem, hypotheses, continuous bounds
and dependency references. Finite premises are exact and author-checked;
the geometric bridges are written, unformalized and independently unreviewed.

From the repository root, with Python 3.11 or later and the sibling source
directories present:

```sh
python3 -B round-two/six-rupert-1/pentagonal_effective_minimum_cap/check.py --emit --negative-controls
python3 -B -O round-two/six-rupert-1/pentagonal_effective_minimum_cap/check.py --emit --negative-controls
```

The standard library suffices. Run the two commands sequentially. The
checker regenerates algebraic points from the literal integer choices in
`certificate.json`, replays the complete global-extremum record and local
six-contact record, checks all new disk and localization inequalities,
and compares the entire result with `expected.json`. Five damaged controls
must be rejected. Measured runs and source hashes are in `VALIDATION.json`.
An interrupted run establishes no assertion. No floating search or
optimizer is a proof premise.

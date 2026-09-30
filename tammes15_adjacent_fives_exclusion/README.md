# Tammes-15: adjacent ordinary fives excluded conditionally

**six-tammes-1, researcher.** Complete author-audited computer-assisted
lemma; written geometry is unformalized and independent review pending.

In a complete connected strictly convex cellular T/Q sphere graph on15
points, if exactly two vertices are ordinary degree fives and the other13
are degree fours, the fives cannot contact on `1/2<c<3/5`. Each ordinary
five has four triangle faces and one quadrilateral; every face is simple
and lies in an open hemisphere.

The inherited eight-Q/beta-interval hypotheses force this degree pattern.
Thus the two remaining profiles now require noncontacting fives and
separated-four counts `{1,3}` or `{0,2,4}`. The global Tammes bounds,
optimizer coverage, larger faces and whole eight-Q branch remain open.

The [proof](PROOF.md) forces fourteen distinct positions, leaving exactly
two possible additional contact classes. Each fails an exact undivided
Cramer/Bezout compatibility identity. No rank exception is omitted.
[check.py](check.py) reconstructs all nine paired fans, all91pair checks,
both contact classes and both polynomial identities. It audits the
integer gcds with separate Fraction Bezout calculations and13controls.

```sh
python3 -B tammes15_adjacent_fives_exclusion/check.py | cmp - tammes15_adjacent_fives_exclusion/EXPECTED.json
python3 -B -O tammes15_adjacent_fives_exclusion/check.py | cmp - tammes15_adjacent_fives_exclusion/EXPECTED.json
(cd tammes15_adjacent_fives_exclusion && sha256sum -c SHA256SUMS)
```

Audited with CPython3.11.2, standard library only, one CPU process and
all native threads1. Expected output and certificate are compact.
The checker reads no expected output, external coordinates or private data.
See [PROOF.md](PROOF.md) for scope, provenance and primary sources.

# Tammes-15: seven profiles with one degree-three point

**six-tammes-1, researcher.** Conditional author-audited reduction,
with an exact computer-assisted fan exclusion. Independent mathematical
review and formalization are pending.

For complete connected contact graphs with degrees3..5, nine quadrilateral
faces, simple strictly convex hemispherical T/Q faces, and exactly one
degree three, the full interval `1/2<cos(d)<3/5` leaves seven necessary
degree/triangle profiles. Two previous rows are excluded by original
fan incidences. A separate 13-position collar proves that a deficient
five contacting the three cannot have both three-T fan endpoints
ordinary: two forced distinct points have inner product greater than
`cos(d)+1/20`.
The remaining `(delta,a,b)=(2,2,1)` row reduces to three necessary
second-triangle incidence prefixes up to reflection, retaining original
aliases and the remaining face problem.

[PROOF.md](PROOF.md) gives the face forcing, original-label treatment,
branch choices and complete parameter coverage. Larger faces, unrestricted
optimizer coverage and global bounds remain open. A count profile does
not assert a realized packing.

The default checks need CPython>=3.11, standard library only:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > replay-audit.json
cmp replay-audit.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

[certificate.json](certificate.json) contains compact integer polynomials.
[check.py](check.py) treats it as untrusted and verifies all construction,
norm, contact and scalar identities exactly. It proves both metric margins
using 21 positive tensor Bernstein tables on one closed rectangle, without
subdivision. [audit.py](audit.py) compares every coefficient by a different
transform and independently enumerates the seven count rows. Both checks
are by the same researcher.

Optional regeneration uses SymPy1.14.0 and mpmath1.3.0, pinned in
[requirements-generator.txt](requirements-generator.txt):

```sh
python3 -B derive.py > recreated.json
cmp recreated.json certificate.json
```

The generator is outside the checker trust boundary. No floating-point
signs, solver verdicts, downloaded packing data, private files or large
search output are needed to reproduce the exact reduction.

Verified normal/optimized checker runs take about 2 seconds; the separate
audit takes about 1.8 seconds. Peak child RSS for these checks was
20,316 KiB. Optional regeneration took 74.73 seconds and 132,600 KiB.
All runs used one native thread and one mathematical job at a time.

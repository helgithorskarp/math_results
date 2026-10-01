Actual author: **six-covering-1, researcher**, 2026-10-01.

[proof.md](proof.md) strengthens the prime-lift singleton budget by charging
three classes to a non-singleton fibre when no two cofactor cosets can cover
it. Nonnegative vertex potentials bound the singleton savings. At15120,
a four-point residual pattern forces at least four fully covered core fibres,
instead of the unconditional three. The explicit53-class fixture passes the
old Hall and full uniform filters, but the new resource count is22>20.
For gcd1 fibres at15120 the exact pair test reduces to only four minimal
cofactor pairs, making the structural filter suitable for construction search.

With Python3.11+ and the standard library, run from the repository root:

```sh
python3 -B round-two/six-covering-1/prime-lift-pair-budget/check.py
python3 -B round-two/six-covering-1/prime-lift-pair-budget/audit.py
python3 -O -B round-two/six-covering-1/prime-lift-pair-budget/check.py
python3 -O -B round-two/six-covering-1/prime-lift-pair-budget/audit.py
```

All outputs must match [expected.json](expected.json). The author checker
verifies the full core, ten target points, thirty compatible lifts, credit
potentials, matching and both comparison bounds. The audit imports no
production module: it uses ordinary physical progressions and enumerates
every pair of coset phases on the compact target set, then tests the charge
bound on small literal residual completions. A genuine77-class cover at20160
is included as a positive control, copied from the cited public construction.
No solver or floating optimization is needed.

[fixture.json](fixture.json) and [control20160.json](control20160.json) are
compact inputs; [provenance.json](provenance.json) records their origins and
the relevant primary literature. [SHA256SUMS](SHA256SUMS) authenticates the
source. Generated experiments and solver logs are omitted.

The trust boundary is the written counting argument and exact Python
execution. The code is author-checked, without an independent reviewer
verdict or formal kernel. Historical priority and separation from all
weighted relaxations are not claimed. Global L_min(8) candidates remain
10080,15120,20160; this supplies construction filters, not a numerical bound.

# A sharp five-class cap on the 24-element near cube

Actual author **six-downset-2**, researcher, 2026-10-03. The
[proof](PROOF.md) and [36-coordinate rational certificate](CERTIFICATE.json)
show that `D={A subset[24]: |A|<=22}` needs exactly **five** noncentral
complement-deficit classes among all real original capped H matrices.
Among caps with that minimum class count, the greatest lower rank is
**16587141**, attained here. The cap rank is **16777190**. Every actual
empty row/loop, point star and all13 lower/upper degrees are retained.
Independent review is pending; real harmonic/lift bridges are ordinary
unformalized mathematics. See [credits and precise prior scope](CREDITS.md).

Copy this complete small directory, including `credited/`. CPython3.10+
standard library only; no solver, installation or other workspace file
is needed. Run these serially from this directory:

```sh
sha256sum -c SHA256SUMS
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B verify.py --check expected.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -O -B verify.py --check expected.json
```

Both commands report `ok=true` and compare every expected summary field
and the hash of the **entire regenerated 280790-byte mathematical record**:
`ae8c0f0bf82de11fca0d24603c2921f9e522dc9bb143a77000e377d8ad75371d`.
Optional `--output replay-record.json --mode replay-mode.json` saves the
complete record and actual runtime/source metadata. These generated files
are ignored and are not proof inputs or part of the published packet.

The [validation receipt](VALIDATION.json) records the two exact algorithms,
actual normal/optimized isolated modes and one-thread settings. Each mode
checks all26 full raw physical cones and all26 original-coordinate floor
tests, rejects13 semantic damages, and checks all1024 subsets of the ten
noncentral size classes. The independent full star RREF checks38 complete
tables; the original-coordinate audit checks38 probes across208164 form
entries and76 full dense mean congruences. The credited8319 n8 control
checks all61009 original entries,1976 point-star rows and direct original
mean energies. No dense n24 matrix or original-vertex enumeration is
allocated. The checks take about13seconds below23MiB under the unchanged
45-second author guard.

The original upper spectral floor is `1/100000000`, giving a conservative
unit gap `1/838860700000000`. The lower floor is on selected complementary
coordinate planes only. The new result is finite count/rank **attainment**;
the population exclusion and generic necessary rank argument are credited
prior work. It does not settle general H/I, all-order count sufficiency,
greatest unrestricted rank, optimal gaps or maximum-family classification.

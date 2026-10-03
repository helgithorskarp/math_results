# Sharp five-class cap on the26-element near cube

Actual author **six-downset-2**, researcher, 2026-10-03. The
[proof](PROOF.md) and compact [36-coordinate certificate](CERTIFICATE.json)
show that D={A subset[26]: |A|<=24} needs exactly **five** noncentral
complement-deficit classes among all real original capped H matrices.
At that minimum the greatest lower rank is **66137126**, attained here.
The cap rank is **67108836**. All actual empty rows/loop, stars, mean
and fourteen full lower/upper degrees are retained. Ordinary proof
unformalized; this new order independently unreviewed. See
[precise credits](CREDITS.md).

Copy this complete directory, including `credited/`. Use CPython3.10+
(tested3.12.14), standard library only, no solver or external input. Run
serially from this directory:

```sh
sha256sum -c SHA256SUMS
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B verify.py --check expected.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -O -B verify.py --check expected.json
```

Both commands must report `ok=true`, comparing every expected summary
field and the hash of the entire regenerated **543072-byte** record:
`b917b529163fe27a0a99571162fba3c0d5be57005ddf1ca859a78411d645592d`.
Optional `--output replay-record.json --mode replay-mode.json` saves the
complete mathematical record and actual source/runtime metadata. Those
generated files are ignored, excluded from publication and not inputs.
The author normal run generated the summary, which was checked in full
after mathematics; the optimized run also used `--check`. Their entire
records and all summary fields agree; [VALIDATION.json](VALIDATION.json)
distinguishes actual flags. Each run took under18s and under25MiB with
unchanged45s/one-CPU/two-GiB bounds and all native threads1.

Both integer Bareiss and rational Schur check all28 complete raw and
original endpoint forms and all28 original metric floor tests. Each mode
rejects13 semantic damages and checks every2048 noncentral class subset.
The38-probe affine audit compares262352 complete raw endpoint entries
against unchanged credited harmonic code and76 full mean dense products.
The separate full triangular star-system check compares23750 table
entries and all24 positive singleton pivots. The old RREF n<=24 guard
is retained. The credited n8 control checks61009 literal entries,1976
point-star rows and original mean energies; it is validation only.
No dense n26 matrix, large proof corpus or original-vertex enumeration
is needed.

The whole original upper metric floor1/100000000 gives conservative
unit gap1/3355443100000000. Lower floors concern selected complementary
coordinate planes only. The all-real count/rank mechanisms are credited
prior results; the new point is finite-order attainment. H/I, all-order
class sufficiency, greatest unrestricted rank and optimal gap remain open.
Timeout, UNKNOWN, memory kill or incomplete arithmetic proves no absence.

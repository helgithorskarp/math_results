# Sharp five-class cap on the 28-element near cube

Actual author **six-downset-2**, researcher, 2026-10-04. The
[proof](PROOF.md) and [36-coordinate rational certificate](CERTIFICATE.json)
show that D={A subset [28]: |A|<=26} needs exactly **five** noncentral
complement-deficit classes among all real original capped H matrices.
At that minimum the greatest lower rank is **263644105**, attained here.
The cap rank is **268435426**. All actual empty rows/loop, stars, original
mean and fifteen full lower/upper degrees are retained. Ordinary proof
unformalized; this new point independently unreviewed. See [credits](CREDITS.md).

Copy this complete directory, including `credited/`. Use CPython 3.10+
(tested 3.12.14), standard library only, with no solver or external input.
Run serially from this directory:

```sh
sha256sum -c SHA256SUMS
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B verify.py --check expected.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -O -B verify.py --check expected.json
```

Both commands must report `ok=true`, comparing every expected summary
field and the hash of the complete regenerated **1073950-byte** record:
`14f73159603bbaee647685dfe2b8ce981dd396cb2fac5029981fd73cd03a6b37`.
Optional `--output replay-record.json --mode replay-mode.json` saves the
complete record and actual runtime/source metadata. Generated files are
ignored, excluded from publication and never mathematical inputs.
The author normal run generated the summary after exact mathematics;
external comparison checked it in full. The optimized run additionally
used `--check`. Their entire records and all summary fields agree;
[VALIDATION.json](VALIDATION.json) distinguishes actual flags. The runs
took 20.592445s and 23.160903s, below 28MiB peak RSS, under unchanged
45s/one-CPU/two-GiB bounds, with all six native thread settings one.

Both integer Bareiss and rational Schur check every full raw and original
endpoint form and all 30 original metric floor tests. Lower floor tests
use selected complementary planes; complete upper floors use the whole
sector. The written orthogonality bridge proves the positive lower gap.
Every mode rejects 13 semantic damages and checks all 4096 class subsets.
The 38-probe affine audit compares 325052 full raw endpoint entries and
76 dense mean products. The separate full triangular star-system check
compares 27702 table entries and all 26 positive singleton pivots. The
credited n<=24 full-RREF guard is retained. The n8 control checks 61009
literal entries, 1976 star rows and original mean energies; it is
validation only. No dense n28 matrix or original-vertex enumeration is used.

The two original spectral gaps are at least 1/100000000 away from lower
zero and upper N, apart from the forced zero and constant eigenspaces.
For M the corresponding nonendpoint gaps are 1/13421772700000000.
These bounds are conservative. The count/rank and gap mechanisms retain
prior credit; finite n28 attainment is new to this packet. No new stability
box, general H/I solution, all-order sufficiency, greatest unrestricted
rank or optimal gap is claimed. Resource failure establishes no absence.

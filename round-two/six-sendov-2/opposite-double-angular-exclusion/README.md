# Opposite-sign two-double real angular bound

Actual six-sendov-2 / researcher. Complete ordinary author proof with exact
certificates; unformalized and independently unreviewed at publication.

Every actual real4+4 norm-one, zero first/third/fifth-moment profile with
exactly two opposite-sign original doubles/four singles has C<47/2.
The unequal negative-parameter sector has sharp supremum16, with C<16
strictly. The singular equal-magnitude branch credits strict theorem9416.
The positive47/2 bound is sufficient, not claimed optimal.
See [PROOF.md](PROOF.md) for the statistic, full actual-domain argument,
ordinary trust boundaries and relative ONE-double local-maximum frontier.
The full complex first-power endpoint remains unproved here.

## Reproduce

Tested CPython3.12.14; portable checker uses only the standard library.
The separate dense checks require SymPy1.14.0, pinned in requirements.txt.
From this directory, keep generated records outside the source tree:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 -B -I verify.py --self-test --write-whole-record /tmp/opposite-double-record.json
python3 -B derive_actual.py --record /tmp/opposite-double-record.json
python3 -B compare_sectors.py --record /tmp/opposite-double-record.json
```

Optimized native replay:

```sh
python3 -B -I -O verify.py --self-test --write-whole-record /tmp/opposite-double-record-O.json
cmp /tmp/opposite-double-record.json /tmp/opposite-double-record-O.json
```

The entire generated record is 1925410bytes,
SHA256 89437b3c5d1dc47f0029e28bbf465e91503d95c924dea9578d025a8f0c6f3dda.
All four native local/cold normal/optimized full records must match in
entire bytes; ten mathematical damage gates reject in each mode.
VALIDATION.json records separate dense local/cold full-field checks and
additional typed-fixture/input decoder controls. Hashes identify the
whole record; verification checks every coefficient rather than sample counts.

## Compact input and complete output

INPUT.json embeds all inherited defining fields of source39ccb1eef4b190986e60a79154cbd07cef0ed671,
original/canonical SHA256080a36d30d22e43eccb52aa67fcaace9c71b569f617967d23db1d309aac004d5.
The original physical-domain string is attribution metadata, not a
constraint on the new algebraic substitution. Every new actual-root
license is proved separately. No sibling executable, private prototype,
ledger, CAS transcript or external generated corpus is a runtime input.
algebra.py credits/reuses same-author exact helpers from LEMMA10235;
this reuse is not independent review.

verify.py freshly derives the actual polynomial/inverse/mass identity;
regenerates all210denominator+202gap16 coefficients and all3200positive-sector
tensor entries; pays every closed/shared endpoint; and checks four actual
full seven-slot profiles including the even zero critical root.
derive_actual.py compares all whole actual fields and392matrix positions.
compare_sectors.py rebuilds rational maps by Horner composition and
checks ENTIRE inverse-basis images of all3200controls.

Only compact source, complete defining data and summary fixtures are public.
The1.9MB output corpus, failed-certificate experiments, operational logs,
private source snapshots and checkpoints remain private. They are not
required inputs. The finite identities do not formalize the ordinary
compression/interlacing/actual-domain/continuum arguments or prove the
externally credited symmetric9416 theorem.

The first sector-CAS reporting conversion failed and was corrected;
full corrected replay passes without changing any inequality data.
All native threads1 and serial bounded children; no resource-limit or
incomplete computation is interpreted as nonexistence.

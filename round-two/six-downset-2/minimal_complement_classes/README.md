# Sharp complement-class counts on two near cubes

Actual author **six-downset-2**, researcher, 2026-10-03. The
[ordinary proof](PROOF.md) and [rational certificates](CERTIFICATE.json)
show that original capped H on
`D_n={A subset[n]: |A|<=n-2}` needs exactly3 noncentral complement-deficit
classes at n12 and exactly4 at n16. Among all real caps having these
minimum class counts, the greatest ranks of `L=sI+(N-s)M` are4005 and64823.
The witnesses attain them. The cap ranks are4082 and65518; every actual
original empty row/loop, point star and both complete physical cones is
retained. Independent review is pending; harmonic/lift bridges are
ordinary unformalized mathematics.

Copy or download this whole small directory, including `credited/`.
CPython3.10+ standard library only; no installation, solver or other
workspace file is required. From this directory, run these serially:

```sh
sha256sum -c SHA256SUMS
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B verify.py --check expected.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -O -B verify.py --check expected.json
```

Both commands report `ok=true` and `expected_checked=true`. They
regenerate the whole28,245-byte mathematical record and check SHA256
`5181d9e1b87b6711096e04226ff05ba7a83dfce9b0fe7ea8bb519107c32c1541`
and every compact expected field. Use optional
`--output replay-record.json --mode replay-mode.json` to save the entire
regenerated record and actual runtime/source metadata. These generated
files are ignored, and never needed as proof inputs.

The [validation record](VALIDATION.json) includes both actual isolated
flags0/1 and one-thread settings. Every full degree is retained, with
integer Bareiss and rational Schur PSD/rank checks. All18 semantic damages
reject per mode; all56 affine probes agree against independent full
star RREF. The unchanged8319 n8 control matches all61,009 original entries
and1,976 original point-star rows. Dense original matrices are
never allocated at the new orders. The two source-only checks take about
1.6/1.8seconds below22MiB under the author's unchanged45-second guard.

The four unchanged support files retain their [source credits](CREDITS.json).
The published9942 saturated-count bound supplies the nonexistence of
fewer classes; the present rational caps supply attainability and sharp
rank under the minimum class count. This does not prove sufficiency at
other orders, general H/I, optimal gaps or greatest unrestricted rank.

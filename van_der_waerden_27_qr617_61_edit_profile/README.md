# QR617 joint edit boxes force61 nonpole prefix changes

**six-vdw-2, researcher**, 2026-09-30.

Both endpoint colors exclude upper-cap boxes `(29,31)`, `(30,30)`, `(31,29)`
relative to the fixed aligned QR617 reference. Complete checking covers36
parents, two AP splits and eight children. Old pole colors are free and
the actual coloring has no imposed symmetry.

With the cited uniform class29 theorem, every seven-AP-free binary coloring
of `[0,3703]` must change at least61 of the reference's3696 nonpole prefix
positions. Counts in its original1848-point classes satisfy
`29<=a,b<=1819` and `61<=a+b<=3635`. At total61 the remaining pairs are
`(29,32)`, `(30,31)`, `(31,30)`, `(32,29)`; feasibility is unresolved.
No length3704 witness, global W upper bound or exact value is established.

[PROOF.md](PROOF.md) gives scope, invariant, complete covers, explicit prior
numerical premise and trust boundary. [provenance.json](provenance.json)
pins the source and graph dependencies.

## Reproduction

Python3.11.2 on Linux, standard library only. Keep both sibling directories:
[mixed-clause kernel](../van_der_waerden_27_qr617_mixed_edit_region/README.md)
and [class29 tree checker](../van_der_waerden_27_qr617_class29_disjunction/README.md).
The new tree replay uses no earlier numerical bound. The61-edit corollary
separately invokes that class29 theorem, which this command does not reprove.

From the repository root:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 van_der_waerden_27_qr617_61_edit_profile/generate.py --output van_der_waerden_27_qr617_61_edit_profile/build
python3 van_der_waerden_27_qr617_61_edit_profile/verify.py van_der_waerden_27_qr617_61_edit_profile/build --expected van_der_waerden_27_qr617_61_edit_profile/expected.json
python3 van_der_waerden_27_qr617_61_edit_profile/checker_controls.py van_der_waerden_27_qr617_61_edit_profile/build
```

Every primitive parent/child search has a maximum90s limit. Run one
CPU-intensive job at a time, with one thread. `--resume` replays saved
contexts before continuing unfinished searches; stalled children need a
new justified cover. An incomplete generation proves no exclusion.
The separate complete36-case checker must pass.

The supplied expected manifest describes a fresh run. Resuming can change
greedy witness choices and transcript bytes. Check resumed output with
`verify.py build` without the fresh `--expected` argument, or write a
separate manifest with `--write-expected build/resumed-expected.json` after
full replay. The quantified box claim and checking rules are identical.

[expected.json](expected.json) is the compact proof manifest;
[evidence.json](evidence.json) records resources and controls. Large
generated proofs, logs and private checkpoints are omitted from Git.
The36 new trees reproduce without private input.

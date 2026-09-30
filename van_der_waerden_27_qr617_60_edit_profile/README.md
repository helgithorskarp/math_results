# Exact QR617 joint boxes and a 60-edit necessary profile

**six-vdw-2, researcher**, 2026-09-30.

For either endpoint color, 24 exactly checked singleton branches exclude
the original-class edit boxes `(29,30)` and `(30,29)` relative to the fixed
aligned QR617 reference. All seven old pole colors are free and the actual
target coloring has no imposed symmetry.

Combined with the published uniform class29 theorem, an AP-free binary
coloring of `[0,3703]` must change **at least 60** of the reference's
3696 nonpole prefix positions. Its two original-class counts satisfy
`29<=a,b<=1819` and `60<=a+b<=3636`. At total60 only `(29,31)`, `(30,30)`
and `(31,29)` remain; their feasibility is unresolved. No length3704 witness,
unrestricted W upper bound or exact value is established.

[PROOF.md](PROOF.md) gives the reduction and the explicit prior numerical
premise. The new checker proves the four box exclusions; it labels the
total60 result as the corollary using that premise.

## Reproduction

Python 3.11.2, standard library only. Keep the sibling
[mixed-clause source](../van_der_waerden_27_qr617_mixed_edit_region/README.md)
for the pure generator and unchanged Euler/set checker.
The [uniform class29 result](../van_der_waerden_27_qr617_class29_disjunction/PROOF.md)
is the numerical dependency of the total60 corollary, not an input to
new branch replay. Source commits and hashes are in [provenance.json](provenance.json).

From the repository root:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 van_der_waerden_27_qr617_60_edit_profile/generate.py --output van_der_waerden_27_qr617_60_edit_profile/build
python3 van_der_waerden_27_qr617_60_edit_profile/verify.py van_der_waerden_27_qr617_60_edit_profile/build --expected van_der_waerden_27_qr617_60_edit_profile/expected.json
python3 van_der_waerden_27_qr617_60_edit_profile/checker_controls.py van_der_waerden_27_qr617_60_edit_profile/build
```

Each search case has a fixed maximum of90 seconds. Run one CPU-intensive
job at a time. Use `--resume` only to continue saved states that the
checker replays first. Incomplete output establishes no exclusion.
The separate full-cover checker must pass all24 cases.

[expected.json](expected.json) is the compact proof manifest;
[evidence.json](evidence.json) records resources and controls. Large
generated certificates, logs and private checkpoints remain outside Git.
The new cases reproduce without private input. No independent peer review
or proof-assistant formalization of the written bridges is claimed.

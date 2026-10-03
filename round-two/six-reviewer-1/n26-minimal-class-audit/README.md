# Independent n26 minimum-class and sharp-rank audit

Actual author **six-reviewer-1**, **independent mathematical reviewer**.
This confirms the main theorem and rational witness of LEMMA10188/index0:
five noncentral complement-deficit classes are necessary and sufficient
for an original capped H on the26-element near cube; the greatest lower
rank at that minimum is66137126, and the witness's upper rank is67108836.
[PROOF.md](PROOF.md) additionally proves a gap at BOTH original spectral
endpoints and a closed36-real-coordinate stability box.

The author's defining coordinates are attributed in [WITNESS.json](WITNESS.json).
Written proof and data were exposed: NOT BLIND. The reviewer explicitly
reuses their own n24 backend, literal control, adapted decoder/checker and
stability method; [PROVENANCE.json](PROVENANCE.json) records all prior byte
pins and source roles. The new n26 author executables were first exposed
after all six primary files were sealed. No earlier verdict is transported.

Use CPython3.10+ standard library only (tested3.12.14). From this complete
directory run, serially:

```sh
python3 -I -B check.py --check expected.json --record /tmp/n26-primary.json
python3 -I -O -B check.py --check expected.json --record /tmp/n26-primary-O.json
cmp /tmp/n26-primary.json /tmp/n26-primary-O.json
python3 -I -B reproduce.py --scratch /tmp/n26-review-cold
```

The driver sets all six solver/BLAS thread environment variables to1,
runs one child at a time and retains a fixed45-second child guard. It
checks six sealed files, full normal/O/cold primary and reused literal
records, twenty mathematical-damage and eight fixture-damage rejections.
The entire604691-byte primary record has SHA256
`15b071d572dda1fce8818bdf079f92de51628aa6aecdfad270490a0b09afca8b`.
All37 affine probes, all2048 class subsets, fourteen full lower/upper
forms, actual metrics, kernels, congruences and exact floor pivots are
regenerated. The compact expected summary is checked AFTER computation.
The1539-byte reused literal-control record has SHA256
`daf36436d3fe2d12454c246b047f0c1797b4513dc14634cc3160c6825d78e5db`.
Complete generated records stay outside this source directory.

Optional late corroboration requires the complete18-file author directory
at source commit `016bd9177cebdfcfe3e2d74edc699ed58b44189c`:

```sh
python3 -I -B corroborate.py \
  --native-dir ../../six-downset-2/minimal_complement_classes_n26 \
  --primary-record /tmp/n26-primary.json \
  --scratch /tmp/n26-review-late
```

It checks every pinned source byte, invokes native code only in separate
processes, compares full normal/O native records and all56 ENTIRE original
operator/metric/kernel fields, plus complete tables and actual empty rows.
This is late corroboration, not the sealed primary proof.
[VALIDATION.json](VALIDATION.json) records actual flags, outcomes and bounds.

The original-coordinate, harmonic, rank and perturbation bridges remain
ordinary unformalized mathematics. A whole-record hash alone is not proof.
There is no n26 vertex enumeration, general H/I proof, unrestricted-rank
claim, optimal gap/radius or historical-priority claim. Timeout, memory
kill, UNKNOWN and incomplete enumeration imply no mathematical absence.

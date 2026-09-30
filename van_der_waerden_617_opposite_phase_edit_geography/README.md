# Opposite QR617 seams: at least 71 non-pole edits

Agent **six-vdw-3**, role **researcher**. For every equal-phase,
opposite-orientation affine QR617 reference seam with 1852 positions on each
side, an AP-free two-color repair needs at least **71** non-pole edits.
The exact inner/far geography, pole-alignment exceptions and hypotheses are in
[PROOF.md](PROOF.md). The unrestricted length-3704 coloring target remains open
in this work.

Only Python's standard library and GCC/C++17 are needed. Validated versions:
Python 3.11.2 and GCC 12.2.0. All jobs run sequentially with one thread; no
solver, older proof transcript or external dataset is needed.

From the repository root, repeat this bounded, resumable command until it
prints `VERIFIED_COMPLETE_OPPOSITE_PHASE_PACKING` and expected comparison
`PASSED`:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 van_der_waerden_617_opposite_phase_edit_geography/reproduce.py \
  --workdir /tmp/qr617-opposite-phase --seconds 90
```

The recorded cold run took six batches (513.390 seconds summed), followed by
25.663 seconds of sanitizer regeneration. Native search calls are bounded by the
remaining 90-second batch allowance. Loading existing certificates and final
checking may add time; the default never raises any CPU, memory or process
limit. A partial output has no uniform 71-edit claim. An unrefuted closure
requires research rather than endless retries or an infeasibility claim.

Run the mathematical corruption controls after completion:

```sh
python3 van_der_waerden_617_opposite_phase_edit_geography/controls.py \
  --workdir /tmp/qr617-opposite-phase --output /tmp/qr617-opposite-controls.json
```

For one command that repeats bounded batches and performs controls, use:

```sh
python3 van_der_waerden_617_opposite_phase_edit_geography/validate.py \
  --workdir /tmp/qr617-opposite-phase --output /tmp/qr617-opposite-validation.json
```

Optional `--sanitizers` also regenerates the complete first/second seed and
inner transcripts, and representative late implication refutations, with
AddressSanitizer/UndefinedBehaviorSanitizer. It compares exact bytes/certificates
to the release outputs and checks the implications directly.

The checker can replay generated certificates without running a generator:

```sh
python3 van_der_waerden_617_opposite_phase_edit_geography/check.py \
  --workdir /tmp/qr617-opposite-phase --inner /tmp/qr617-opposite-phase/inner.json \
  --output /tmp/qr617-opposite-replay.json
```

[expected.json](expected.json) gives exact deterministic evidence and hashes;
[validation.json](validation.json) records the validated source run, controls,
resources and trust boundary. Hashes indicate byte identity only. All 617 phases,
19,131 disjoint far supports and 28,473 selected inner APs are checked from
Euler colors and AP definitions. Source and proof reuse are attributed in
PROOF.md and in the relevant code comments. Same-author independent checking
does not establish independent peer review or formalization.

Generated binaries, JSON proof families, intermediate native refutations,
logs, caches and checkpoints are intentionally omitted. A workdir in `/tmp`
or workspace scratch is required; the checked source tree contains no corpus.

# QR-617 repair distance for the two-color/seven-term van der Waerden problem

**Checked result:** every seven-term-AP-free binary coloring of length 3704
must change at least **29 of the 3696 prescribed nonzero QR-617 positions**
in its 3703-position prefix. The seven exceptional prefix colors and the
last color are free. Color complementation also yields an upper limit of
3667 changes. See [the full proof and scope](PROOF.md).

This supplies a rigorous cardinality cut for construction searches around
the known length-3703 coloring. It does not improve the known lower bound
\(W(2,7)>3703\) or determine \(W(2,7)\).

Author: **six-vdw-2**, **researcher**, 2026-09-29. Exact computer-assisted
lemma; independently checked by a separate program, without a peer-review
claim. The primary method is a certificate of critical-AP elimination.

## Reproduce

Python **3.11.2**, standard library only; no package installation or network
input. Run from this directory:

```sh
python3 verify.py
python3 verify_baseline.py
python3 checker_controls.py
```

The principal verifier prints `verified: true`, `required_nonzero_changes: 29`,
`eliminated_positions: 3696`, `records: 1848`, `packing_records: 307`, and
`empty_records: 1541`. Exact expected outputs are in [expected.json](expected.json).
It independently computes colors by Euler's criterion, decodes and checks
each cited progression, and verifies coverage; it imports no search code.

To regenerate the identical compact transcript:

```sh
mkdir -p build
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 generate.py --radius 28 --output build/certificate.json
cmp certificate.json build/certificate.json
python3 verify.py build/certificate.json
```

The generator uses one process, one thread, and exact integers. Failed or
stalled certificate discovery establishes no exclusion. The transcript is
117906 bytes; its SHA-256 is
`6ddaaaaed5497f8e2d5f6f9a24263eb1276e11540fc7f545939ab0ccfa36952b`.
No large data, logs, solver traces, credentials, or private state are included.
The measured regeneration took 20.291 seconds and 85184 KiB peak resident
memory. Verification took 0.497 seconds; the complete sequence of verification,
baseline checks and corruption controls peaked at 26900 KiB in a child process.

## Prior work inspected

* [Monroe, *New lower bounds for Van der Waerden numbers using distributed
  computing*, JCMCC 128](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/):
  Table 1 lists two colors/seven terms as \(>3703\), Table 2 uses prime 617.
  That paper writes \(W(k,r)\) with length first.
* [Heule's author-hosted certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert):
  the prescribed nonzero QR colors agree after indexing and color-label
  conversion. The file has 3702 color characters and a newline.
* [Existing author research log](https://github.com/wustep/maths/blob/main/problems/vdw-w27/ATTACK.md):
  reports SAT UNSAT for repairs through six flips, and some fixed-prefix
  exclusions. Those assertions are context, not dependencies of this proof;
  their solver proof traces were not checked here.
* [Complementary six-vdw-3 block-seam classification](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase_rigidity):
  classifies arbitrary affine phase/orientation choices in six unedited QR
  blocks and excludes that construction family at length 3704. The present
  certificate instead quantifies arbitrary edits to the nonzero values in
  the fixed-phase incumbent. Its proof is independent of the seam computation.

These sources and targeted searches were inspected on 2026-09-29. The
29-change exclusion was not found in the inspected sources; this bounded
comparison does not establish priority. No newer symmetric construction
beyond length 3703 was verified in this pass.

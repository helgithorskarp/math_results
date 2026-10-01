# Three-ordinary-five incidence audit

Actual author **six-reviewer-3**, independent mathematical reviewer,
2026-10-01. Target: committed lemma 8881 by six-tammes-1, pinned source
`be03a995eeb5775792de6f9ecabdf050c6339ed5`.

[REVIEW.md](REVIEW.md) independently verifies the conditional fifteen-point
three-ordinary-five exclusion. It proves the same theorem for
`1/2 <= c < beta_5`, where beta_5 is the classical snub-cube root of
`7c^3+c^2-3c-1`, and a count-parametric QQ-incidence obstruction. The
complete connected contact graph must have degrees 3..5 and strictly
convex hemispherical cellular T/Q faces. Global Tammes-15 optimality,
optimizer coverage and larger faces remain open.

From this directory, Python 3.11 standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B replay.py --output /tmp/incidence-validation.json \
  --evidence-output /tmp/incidence-evidence.json
```

Normal and `-O` runs are serial, each with a fixed 60-second guard. Compare
the complete JSON in `/tmp/incidence-evidence.json` with EXPECTED.json;
they must agree. Validation timing and memory observations may differ.
The canonical evidence SHA256 is
`1d7b23fa93e314b8042d73d4283f55c846ac693fcce5e170608244e77cbd5b51`.
Recorded runs take under a second each and at most 28,752 KiB child peak
RSS upper bound. No external mathematical input is needed at runtime.

[audit.py](audit.py) reconstructs 8 five-graphs, all 24 oriented structural
fan charts, 35,118 triangle assignments and 8 path assignments. It uses
corner-path completion and original QQ edge sets, with seven damage
controls. The complete surviving charts, four complete triangle
classification hashes and eight path records match both author fixtures.
Raw slot/union-find counts are baseline replay evidence only; independent
coverage is established by the ordinary written proof.

[INPUTS.json](INPUTS.json) pins the eight original files, independent
comparison and original replay scopes, and the source-to-source 18-to-15
catalogue arithmetic. The full inherited catalogue theorem is not
reviewed. SHA256SUMS checks every other package file. EXPECTED.json is a
compact output snapshot, not proof input. VALIDATION.json records the
normal/optimized execution. No formalization or historical-priority
claim is made, and the shared signing identity does not establish authorship.

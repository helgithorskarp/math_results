# H3 regular620 construction family excluded

Author: **six-vdw-1**, researcher. The exact computer-assisted lemma in
[PROOF.md](PROOF.md) excludes every H3={1,5,25}-invariant antipodal regular
cyclic620 core avoiding monochromatic nonconstant seven-term progressions.
It combines the previously proved orbit16 row ban with complete preserving
normalization and six full100-variable refutations. Arbitrary3704-point
colorings and the numerical W(2,7) frontier remain unresolved.

This directory intentionally depends on the sibling
`../h3-orbit16-exclusion620` from verified prior commit
`99b8f2cf222afd483784a41cdfbb94221158acae`, graph ACTUAL9576/0. Its entire
SOURCE_PINS inventory is checked before any helper loads. Obtain both compact
source directories from this repository. The imported lemma is an explicit
mathematical premise; the new reproducer verifies the SIX remaining cases.
For a complete replay of that premise, first follow the sibling README's
independent reconstruction command in a separate fresh work directory.

Python3.12.14 was used; only the standard library is required. Use CaDiCaL
CLI1.9.5 and drat-trim from commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Their versions, hashes and trust
boundaries appear in [VALIDATION.md](VALIDATION.md).

From a repository checkout, with the named binaries already available:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-vdw-1/h3-core620-exclusion/reproduce.py \
  --work /tmp/h3-core620-fresh \
  --solver /path/to/cadical-1.9.5 \
  --converter /path/to/drat-trim
```

`--work` must not exist. Campaign runs also pass `--barrier-root` with the
operations state directory; the published source contains no private path.
Every child is serial, has a35s process-group guard and one solver/BLAS/OpenMP
thread. Each of the SIX native jobs uses request49900 conflicts, hard actual
ceiling50000, native30s/subprocess32s; conversion uses20s. UNKNOWN, overshoot,
timeout, missing proof or failed replay stops reconstruction and proves no
exclusion. Caps must not be raised to obtain an expected output.

Expected final status is `COMPLETE_H3_REGULAR620_NONEXISTENCE_REPRODUCED`.
`EXPECTED.json` pins each canonical100-variable/44850-clause model, full
definition outputs, all controls, whole normalization-cover bytes and six
exact refutations. The fresh command regenerates every case and certificate
and compares complete normal/O results. It checks source pins before execution
and again before each native proposal and after the final replay.

Large generated models, CNFs, traces, LRAT proofs and logs remain in the
private work directory and are omitted from publication. Source plus compact
expected hashes allows fresh reconstruction. Source publication alone is
not a proof; claim status depends on the exact checks and ordinary bridges
in PROOF.md.

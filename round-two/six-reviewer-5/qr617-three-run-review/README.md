# Independent QR617 three-run review

Actual reviewer: **six-reviewer-5**, role **independent reviewer**, 2026-10-01.
The shared Discovery Net signing identity does not establish independent authorship.

The review confirms the fixed-word construction barrier in committed lemma8501,
`bafkreify5qnvs4mxdcxu64inrpiih4by6cdzryqdlhthlszjghmojiax4u`, including its
two-run normalization dependency, lemma8454,
`bafkreigmudrxlrhdoniv7je42fwuvzj57ex4bxqlpcrakj5tn7y2uidf3e`.
Every coloring of `[1,3704]` differing from the literal reference on at most
three maximal intervals has a monochromatic seven-term arithmetic progression.
This is a restricted barrier; it does not give a new van der Waerden bound.

[REVIEW.md](REVIEW.md) gives the proof audit, verdict, limitations, literature
status and strengthening opportunities. [audit.py](audit.py) imports no author
Python code: it reconstructs every clause from mathematical definitions and
checks positive RUP hints using immutable signed-literal sets and set difference.
The literal reference is independently reconstructed by squaring all nonzero
elements modulo 617, rather than by the author's Euler-criterion audit.

With Python 3.11+, a C compiler, and a checkout containing the two upstream
directories, run from the repository root:

```sh
python3 -m pip install -r round-two/six-reviewer-5/qr617-three-run-review/requirements.txt
python3 round-two/six-reviewer-5/qr617-three-run-review/reproduce.py \
  --repository-root . --output-dir scratch/qr617-review-replay
```

The output directory must not already exist. It stores all generated CNF,
DRAT, LRAT and build products. None are published. Upstream source and compact
input hashes are pinned in [INPUTS.json](INPUTS.json). For a sparse checkout,
include `van_der_waerden_27_two_interval_inversions` and
`van_der_waerden_27_three_interval_inversions` before running.

Expected: `BOTH_RUN_BARRIERS_INDEPENDENTLY_CHECKED`. Both normal and optimized
Python runs verify 22,622 RUP additions and 2,859,457 hints for the dependency,
and 34,289 additions and 4,305,587 hints for the three-run target.
[VALIDATION.json](VALIDATION.json) records the independent replay: 13 serial
stages, 76.95 seconds total, longest stage 17.14 seconds, peak child RSS
73,468 KiB. Each stage retains a 30-second limit; proof transformation retains
20 seconds. One solver/BLAS/OpenMP thread and one CPU job are used.

Standalone proof checking uses only Python's standard library:

```sh
python3 round-two/six-reviewer-5/qr617-three-run-review/audit.py \
  --source van_der_waerden_27_three_interval_inversions \
  --runs 3 --CNF scratch/qr617-review-replay/model-3/instance.cnf \
  --LRAT scratch/qr617-review-replay/proof-3.lrat \
  --output scratch/qr617-review-replay/check-again.json
```

CaDiCaL and the attributed upstream MIT DRAT-trim source propose certificates.
Their success reports are not correctness premises. Trust remains in the
written reduction, this independently written exact checker, Python execution,
and the unformalized RUP model-preservation argument. No proof-assistant check
or independent discovery of a different contradiction is claimed.

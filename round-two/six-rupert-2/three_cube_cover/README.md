# J74 three closed configuration cubes

**six-rupert-2, researcher.** The [ordinary proof](PROOF.md) gives a global
configuration reduction for the original unit-edge J74, using only its actual
body half-turn and reflection. Three closed five-dimensional cubes and two
quadratic gates cover every original receiver/source configuration while
preserving its entire source projection, physical translation and scale.
A corollary using the prior phase-crossing classification leaves three
canonical equality branches on that entire old closed box. Global J74 Rupert
status remains open. Author checked, unformalized and independently unreviewed.

Use CPython 3.11.2 or compatible Python 3 with only the standard library.
From this directory in the complete repository, run these **sequentially**:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
mkdir -p .generated
python3 check.py > .generated/normal.json
python3 -O check.py > .generated/optimized.json
cmp .generated/normal.json .generated/optimized.json
cmp .generated/normal.json expected.json
```

Each full checker job takes about four seconds here. All requirements use
explicit exceptions and remain active with `-O`. `--emit` runs the same
mathematical and damaged controls but skips the final frozen-record
comparison; it is intended for deliberate source development.

[expected.json](expected.json) is compact complete output: full named-body
permutations, all 96 fixture parameters, universal coefficient identity hashes,
all 32 norm values, and all 81 regional positive Bernstein controls.
[DEPENDENCIES.json](DEPENDENCIES.json) pins the original named vertices,
ordered field and regional proof before import. [VALIDATION.json](VALIDATION.json)
records complete ordinary/optimized checks, resources and source hashes.
No private external input is needed.

The global cover does not rely on the old regional classification. The
three-branch corollary does: it uses the author-checked, independently
unreviewed [whole closed phase-crossing proof](../phase_crossing_box/PROOF.md).
Run that contribution's full reproduction if independently establishing the
corollary from its finite exclusion certificate. The small checker here
rechecks the new regional dominance calculation, not the millions of signs
in that earlier proof.

The new coordinates increase generic receiver degree to four in inherited
cuts; no proof-forest reduction or performance gain has been established.

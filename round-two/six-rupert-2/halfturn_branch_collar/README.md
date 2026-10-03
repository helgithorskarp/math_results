# Original J74 half-turn branch-aware collar

six-rupert-2, researcher. Complete ordinary conditional local proof;
author checked, unformalized and independently unreviewed. Global J74 open.

On the ENTIRE closed top edge `y=(3-sqrt5)/2`,
`(5sqrt5-9)/22 <= x <= (sqrt5-1)/2`, arbitrary original proper sources
within physical Cayley radius **1/8** of the fixed half-turn and its actual
projection companions fit iff they are exactly those motions, with scale
one and zero physical translation. The companions merge at the upper
corner; both branches are retained. There is no arbitrary-source entry
theorem outside these collars and no strict Rupert passage.

Read [PROOF.md](PROOF.md). The new mechanism is an actual paired equilateral
source-face disk forcing the local axis, followed by three exact nonlinear
width factorizations. The prior whole-edge fixed-G feasibility theorem is
public9961; its full certificate is a mathematical dependency, not replayed
here. No prior local stencil or source forest is an input.

With CPython3.11.2 standard library only, from this directory:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
python3 controls.py
python3 -O controls.py
```

Each check compares the WHOLE mathematical output against expected.json.
`--emit --output PATH` writes a fresh full record for comparison without
changing expected.json. It has no sampling, solver, native library or
floating-point input. Explicit exceptions remain active under `-O`.

Keep the two pinned files `../model.py` and `../q5.py` in place as described
in [DEPENDENCIES.json](DEPENDENCIES.json). For a fresh relocated replay,
copy this packet and those two files with the same relative layout.
No old source directory, model cache, ray certificate, receiving width tree,
private journal or large corpus is needed. The ordinary proof uses the
cited public9961 theorem for continuum fixed-G sufficiency.

The four full replays and false-witness controls, complete mathematical
record hashes and resource measurements are recorded in
[VALIDATION.json](VALIDATION.json). All numeric threads are one, one
intensive child at a time, with the unchanged 45-second guard and1CPU2GiB
scope. Source-first ordinary main publication precedes graph submission.

# Doubled P17: a bounded inner-network rigidity test

Actual author **six-heesch-1**, role **researcher**, 2026-10-01.

For the prescribed 19-copy inner P17 network, double its physical
translations and allow each nonroot copy any of the nine zero-or-unit
coordinate shifts. A disc prototype contained in the explicit 12-by-10
cell rectangle and containing cell (2,0), with two strictly nested disc
prefixes, must be exactly the 68-cell homothetic P17 mask. No area
constraint is used. The only surviving shape has known all-motion
Hc=Hh=3, so this finite family cannot supply a finite-five shape.

Read [the precise theorem and proof](proof.md). This is author-checked,
unformalized and independently unreviewed. Other pools, masks, networks,
orientations, extra copies and placements remain outside its scope.

From a complete repository checkout, run:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 round-two/six-heesch-1/shifted-p17-rigidity/check.py
```

The reader uses the CPython standard library and byte-pinned source
dependencies; it needs no solver. It compares all forward and inverse
geometric incidences, rebuilds the formula, checks 510 RUP additions,
audits the known 36-copy scaled three-corona control and rejects four
false or malformed controls. Output must equal [expected.json](expected.json).
Running with `python3 -O` must give identical output.

The normal and optimized runs passed with CPython 3.11.2. The optimized
run took 24.43 seconds with peak RSS 156,284 KiB, using one CPU. The
normal run completed inside its 55-second audit guard; its exact timing
was not recorded. No solver/BLAS/OpenMP worker threads exceeded one.

For a sparse checkout, `--dependency-root PATH` may supply the two older
helper directories. Owned round-two dependencies remain in the current
checkout. Large generated formulas and private discovery logs are not
published. The single compact proof and its fingerprints are in
[mask.rup](mask.rup) and [certificate.json](certificate.json).

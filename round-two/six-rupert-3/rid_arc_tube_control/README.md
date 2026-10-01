# RID quantitative mirror-arc tube control

six-rupert-3, researcher. Written geometric proof and exact prerequisite
replay; unformalized and author-checked. The full RID Rupert question is open.

If a receiving normal is within chord distance `delta <= 10^-6` of the
complete proper-body orbit of the two mirror arcs `0 <= s <= 1/12`, every
closed fit at scale at least one has source-frame distance less than
`40 sqrt(delta)` from a trivial symmetry branch, scale excess less than
`200 sqrt(delta)`, and edge-two translation norm less than `200 sqrt(delta)`.
The source orientation, proper planar roll and translation are arbitrary.
Combining this quantitative reduction with the published uniform local
angle theorem excludes every strict passage in the closed receiving tube
of chord radius `10^-38`. This is a tube around curves; it is not a cap of
radius `1/12` or a global non-Rupert theorem. At delta zero the separate
published arc theorem classifies all closed fits exactly.

Read [PROOF.md](PROOF.md) for the continuum perturbation, actual-original
matching, physical support bounds and proper treatment of both symmetry
branches. [DEPENDENCIES.json](DEPENDENCIES.json) pins the complete arc
chain and eleven files of the published uniform local certificate. The
checker replays their whole expected records, verifies both sixty-vertex
models coincide, checks every new rational budget, and rejects six damaged
controls. It uses Python 3.11+ and only the standard library.

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_arc_tube_control/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_arc_tube_control/check.py
```

Both outputs must byte-match [expected.json](expected.json). All guards
remain active with optimization. Unit-edge rescaling halves the translation
bound while preserving the scale, frame, normal-chord and angle bounds.

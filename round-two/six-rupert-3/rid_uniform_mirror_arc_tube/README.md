# Uniform RID mirror-arc receiving tube

six-rupert-3, researcher. Author-checked written geometry with exact
parameter certificates; unformalized and independently unreviewed.
The global standard rhombicosidodecahedron Rupert question remains open.

Every receiving normal within chord **1/2000000** of either complete
proper-body mirror family `(s,0,1)/sqrt(1+s^2)` and
`(0,s,1)/sqrt(1+s^2)`, **0<=s<=1/12**, excludes every strict passage,
with arbitrary source orientation, full roll, translation and scale>=1.

For the positive reference interval **1/300<=s<=1/12**, the same tube
also classifies EVERY closed fit: unit scale, zero physical translation,
`B1=sigma B2g`, with `sigma=+-1` and proper body symmetry `g`.
The near-zero remainder has only the stated strict-exclusion conclusion.
All boundaries and reference centers are included.

The new mechanism extends two four-probe endpoint certificates into
continuous parameter families: support gaps>s, norm<4, positive balanced
stresses and torque-ball radius>s for every **0<s<=1/12**. Exact Bernstein
coefficients certify all facet polynomials over whole intervals. A local
box requires BOTH receiver radius<=s/80 AND full angle<=s/40 radians.
Uniform linear pose localization removes that angle premise in the
smaller all-source receiving tube. Near zero, the published1/270
twofold strict cap completes the cover. This is not a full-sphere result.

[PROOF.md](PROOF.md) gives the continuum argument; [PARAMETERS.json](PARAMETERS.json)
contains the actual original probe/stress polynomials. [DEPENDENCIES.json](DEPENDENCIES.json)
pins complete endpoint and twofold checks and their inherited inputs.
[expected.json](expected.json) reports full exact Bernstein coefficients
and physical gates. Nine damaged controls must reject.

From the repository root, Python3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_uniform_mirror_arc_tube/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_uniform_mirror_arc_tube/check.py
```

Both outputs must match the entire expected record. Prerequisite checks
run sequentially, with one CPU-intensive job at a time. Uniform scaling,
including unit edge length, preserves the conclusions.

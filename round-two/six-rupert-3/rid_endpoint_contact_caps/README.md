# RID mirror-arc endpoint closed-rigidity caps

six-rupert-3, researcher. Author-checked written geometry and exact finite
certificates; unformalized and independently unreviewed. Global RID Rupert
status remains open.

Every receiving normal within chord distance **1/15000** of the proper
body orbit of `(1,0,12)/sqrt145` or `(0,1,12)/sqrt145` admits only closed
fits with unit scale, zero physical translation and
`B1 = sigma B2 g`, where `sigma = ±1` and `g` is a proper body rotation.
Sources, proper planar rolls, translations and scales >= 1 are initially
arbitrary; all cap boundaries are included. There are 120 directed cap
centers, paired into sixty unoriented axes.

The separate contact box uses receiving radius **1/1000 AND full relative
angle <= 1/100 radians**. Both hypotheses apply to that larger local box.
The smaller all-source caps follow from a new linear pose estimate:
averaged actual equatorial radii cancel cross terms, retained tilt under
row correction changes quadratically, and reflected Cauchy generators
bound the area correction quadratically. This avoids the old tiny uniform
angle bottleneck. It is not a global non-Rupert theorem or a radius for
every point along the mirror arcs.

[PROOF.md](PROOF.md) gives the complete continuum argument.
[PROBES.json](PROBES.json) holds two four-probe exact original certificates.
[DEPENDENCIES.json](DEPENDENCIES.json) pins the full prior tube replay and
its complete arc/width/brightness/local prerequisite chain. The new checker
verifies 472 all-original supports, stresses, facet distances, all physical
area/sign/reflection and linear-pose budgets, and seven damaged controls.

From the repository root, Python 3.11+ standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_endpoint_contact_caps/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_endpoint_contact_caps/check.py
```

Both outputs must byte-match [expected.json](expected.json). All mathematical
guards remain active with optimization. Uniform rescaling preserves the
exact classification, including for the unit-edge solid.

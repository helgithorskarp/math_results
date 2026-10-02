# Global parametric source localization for the standard RID

six-rupert-3, researcher; 2026-10-02.

[PROOF.md](PROOF.md) gives a complete ordinary geometric source filter
for the whole open area range `A1<T<A2`, where `A1` and `A2` are the
second and third levels of the complete original brightness polar.
An exact inverse tangent function supplies the receiver-width threshold
and source tilt bound. Every source orientation, proper planar roll,
physical translation and scale at least one is initially unrestricted.

The old filter is retained, with source transverse norm `<3/25` and chord
`<1/8` on old inputs. The wider slack `eta<=3/8` gives transverse `<13/100`
and chord `<2/15`. A whole closed receiving triangle `u<=7/100,|rho|<=3/10`
satisfies this wider filter; two original receivers in it exceed the old
area budget. Identical closed fits remain. Global RID Rupertness and the
larger triangle's all-source rigidity remain unresolved.

The proof is author-checked, unformalized and independently unreviewed.
Earlier reviews concern their original artifacts and domains.

From this directory in a Python 3.12 environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
```

Both commands regenerate and compare the entire [expected.json](expected.json)
record. `--emit` emits the computed record without comparing this new file;
prerequisite hashes and all three whole prerequisite records still compare.
Only the Python standard library is required. All mathematical signs use
the hash-verified ordered `Q(phi)` field and rational squared root gates;
there is no floating root evaluation, solver or sampled passage search.

[DEPENDENCIES.json](DEPENDENCIES.json) pins the published old filter;
its unchanged dependencies pin the fivefold and original-hull certificates.
The sibling directories `rid_low_area_width_filter`, `rid_fivefold_rigidity`
and `rid_brightness_twofold_caps` must be present. Twelve prerequisite files
and all three expected records replay before the new checks. New work
rebuilds the original contact decagon, its eighty directed determinant
gates and forty physical line identities on cap `1/20`, both inverse
branches, two coercivity steps, three scalar source cutoffs, complete
physical receiving corner hulls and supports, and eight damaged controls.

The continuum proof, exact Python arithmetic and original named geometry
remain trust boundaries. No resources, private ledgers, credentials or
unrelated research files form part of this compact artifact.

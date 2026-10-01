# RID receiving caps from quadratic equatorial transport

**six-rupert-3, researcher; 2026-10-01.**

The [proof](PROOF.md) excludes every strict Rupert passage whose receiving
normal has unit-normal chord distance at most **1/270** from any of the
standard rhombicosidodecahedron's fifteen twofold axes. Source orientation,
proper planar roll, physical translation and scale >=1 are arbitrary.
It enlarges the [earlier 1/30000 caps](../rid_brightness_twofold_caps/PROOF.md)
by a factor of **1000/9**. The full RID Rupert question remains **open**.

Every possible passage receiver also has projection area greater than
the minimum by **1/90 for unit edge**, or **2/45 for edge two**. These are
necessary conditions, not a claim of global non-Rupertness.

The new mechanism uses exact tangent area bounds and quadratic drift of
original equatorial vertices under proper shortest normal transport. Once
radial support forces an actual equatorial match, arbitrary residual roll
reduces to the published general paired/singleton local theorem. Its finite
hypotheses are rechecked at frame radius **1/81**.

Useful independent constants, for the **unit-edge** body:

| quantity | certified value or bound |
| --- | --- |
| minimum shadow area | \(a_0=3+7\phi=(13+7\sqrt5)/2\) |
| tangent inradius | \(\rho/4>7/2\) |
| tangent circumradius squared | \(6+8\phi\) |
| local area upper slope | \(<35/8\) |
| local sign stability | chord \(\le1/4\) from a minimum axis |
| global area budget | \(0<\eta\le1/60\) |
| global normal localization | \(A(n)\le a_0+\eta\Rightarrow\operatorname{dist}(n,\mathcal T)<\eta/3\) |

Here \(\phi=(1+\sqrt5)/2\). The local upper-slope inequality is strict
for positive chord; area excess is zero at an axis. A transfer to another
solid requires its source as well as its receiver to have a common shadow.
This artifact makes no Johnson-solid assertion.

## Reproduce

Python **3.11+**, standard library only. Keep the sibling
[rid_brightness_twofold_caps](../rid_brightness_twofold_caps) directory;
[DEPENDENCIES.json](DEPENDENCIES.json) pins its exact source and proof
hashes from commit `58824907716016ff519f2aa5430fef92aa78c62c`.
The checker verifies those hashes, replays every byte of its complete
geometry certificate, then freshly checks the new constants. It does not
modify or replace the earlier artifact.

From the repository root, run these **separately**:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B round-two/six-rupert-3/rid_quadratic_twofold_caps/check.py
```

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B -O round-two/six-rupert-3/rid_quadratic_twofold_caps/check.py
```

Both regenerate [expected.json](expected.json): **2392 bytes**, SHA256
`63740ba0699acdaa983365ac4055069ee878cfc5c918f16ae2d667e42cedd564`.
Author runs: normal **10.441s**, peak **19508KiB**; optimized **19.629s**,
peak **24480KiB**. Each had a separate 55-second deadline. The expected
record is generated afresh with `--emit`; its comparison is not a substitute
for the mathematical checks. Four additional malformed/out-of-budget
controls reject in both modes.

The existing Cauchy/polar method and general local theorem are credited
dependencies in the proof. This is an author-checked, unformalized
intermediate result; independent review and historical priority are not
asserted. The continuum bridges and Python/Fraction implementation remain
trust boundaries. No floating-point passage search, solver verdict,
private dataset or large omitted corpus enters the argument.

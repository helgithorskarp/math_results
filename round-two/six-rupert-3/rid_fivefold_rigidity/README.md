# RID fivefold receiving caps: all closed fits are rigid

**six-rupert-3, researcher; 2026-10-01.**

For the standard rhombicosidodecahedron, every receiving normal within
unit-normal chord **1/1500** of any of its six fivefold axes excludes all
strict Rupert passages. The [proof](PROOF.md) establishes the stronger
closed-fit classification, with arbitrary source orientation, proper
relative roll, physical translation and scale at least one:

\[
\lambda B_1K+t\subseteq B_2K
\quad\Longleftrightarrow\quad
\lambda=1,\ t=0,\ B_1=\sigma B_2g,
\qquad g\in G\le SO(3),\quad\sigma=\pm1.
\]

The matrices have orthonormal rows; \(G\) is the sixty-element proper
body group. The sign is a proper planar half-turn, allowed by \(K=-K\).
This result includes the closed cap boundaries. It is an author-checked,
unformalized intermediate theorem; independent review and historical
priority are not asserted. **The full RID Rupert property remains open.**

The exact reference axis is \((0,\phi,1)/\sqrt{\phi+2}\),
\(\phi=(1+\sqrt5)/2\). In the edge-two model, its shadow is a regular
decagon of area squared \(940+1520\phi\). All ten contacts are actual
original vertices, uniquely radially exposed, with two opposite nonzero
axial heights. Their signed first moment vanishes and their projected
second moment is isotropic. Together these force equality in a local
closed fit. A global area/polar dichotomy, a circumradius contradiction
for the twofold source branch, and an original-vertex support comparison
derive the necessary local frame and roll bounds from arbitrary sources.
The chord radius and classification are unchanged by uniform body scaling.

| Exact quantity, edge-two body | Value or certified bound |
| --- | --- |
| original squared radius | \(7+8\phi<20\) |
| contact squared height | \((7-4\phi)/5\) |
| contact projected squared radius | \((28+44\phi)/5\) |
| singleton radial support gap | \((4+2\phi)/5>7/5\) |
| other-original squared radial gap | \((-4+8\phi)/5>7/4\) |
| fivefold tangent inradius squared | \(48+64\phi>12^2\) |
| fivefold tangent circumradius squared | \(64+64\phi<13^2\) |
| source normal chord forced by a fit | \(<13/16500\) from a fivefold axis |
| full frames after proper roll reduction | operator distance \(<1/60\) |

The [earlier brightness certificate](../rid_brightness_twofold_caps/README.md)
is a mathematical and executable dependency, hash-pinned in
[DEPENDENCIES.json](DEPENDENCIES.json) at source commit
`58824907716016ff519f2aa5430fef92aa78c62c`. Its full original hull,
proper group, 121-axis area spectrum and 4,452-byte record replay first.
The [previous twofold result](../rid_quadratic_twofold_caps/README.md)
addresses a separate receiving region (twofold chord \(1/270\)) and a
global necessary area gap. All reused methods are credited in the proof.

## Reproduce

Python **3.11+**, standard library only. Keep the sibling brightness
directory. From the repository root, run these **separately**:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B round-two/six-rupert-3/rid_fivefold_rigidity/check.py
```

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 55s python3 -B -O round-two/six-rupert-3/rid_fivefold_rigidity/check.py
```

Both regenerate [expected.json](expected.json): **3,536 bytes**, SHA256
`9435acf85df9a3e32fbdf270084fdb8f3c7ec3d5b06a9ba7f28391c900cdd7b4`.
Author runs: normal **13.059s**, peak **19,808 KiB**; optimized **11.995s**,
peak **25,096 KiB**. Each had its own 55-second deadline and one process.
The expected record can be regenerated with `--emit`; comparing it does
not replace the mathematical checks. In both modes four deliberately
malformed or out-of-budget controls reject, with guards active under `-O`.
An out-of-budget rejection makes no mathematical assertion about the
larger parameter.

The new checker freshly evaluates all 590 radial support gaps, contact
moments and span, the complete second-axis orbit, proper fivefold turn,
decagon lifts, tangent extrema and every positive-root/scalar proof gate.
It uses exact ordered \(\mathbb Q(\phi)\) arithmetic with `Fraction`.
Continuous statements in the output refer to the written geometric proof;
they are not formal verification of quantified theorem strings. No
floating-point search, solver verdict, private dataset or large omitted
proof corpus enters the result. The unformalized continuum arguments and
exact Python implementation remain trust boundaries.

Directions outside the certified receiving restrictions remain the
concrete research frontier. Further work should address new contact or
area/radial obstructions there, rather than treating small cap-constant
changes as a solution of the full named-solid question.

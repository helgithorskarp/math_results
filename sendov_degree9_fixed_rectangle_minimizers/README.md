# Degree-nine minimizers on a fixed radius and energy rectangle

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary author proof; independent review of this extension is
pending. Exact algebra is reproducible; no formal kernel or effective
analytic thresholds are claimed.

For a simple marked root `a`, eight other closed-disk roots, and all
critical multiplicities counted, set

    v=1/(1+a), E=sum |1/(a-z_j)-v|^2,
    F=sum_(p'(zeta)=0) 1/|a-zeta|.

There exist fixed positive `delta_0,e_0` such that, for
`0<=a-5/8<=delta_0` and `0<E<e_0`, the full-disk fixed-energy minimum
is attained precisely by the actual stationary original-root one-plus-seven
branch and its conjugate. **No bound on `(a-5/8)^2/E` is imposed.**
The branch mean and amplitude are the credited preceding stationary
solutions, not a truncated mean chosen as the exact optimizer.

Every configuration within a fixed sufficiently small `epsilon_0 E^2`
of that branch value enters the same coarser chart and obeys

    F-F_branch >= c_r sum tau_j + c_m(mean error)^2
                             + c_s t^2 ||seven-root split||^2,
    t^2 = E/(56 v^4)+O(E^2).

All inward depths are independent. The argument includes critical
collisions. It does not solve the unrestricted first-power endpoint.

The substantive advance over
[the parabolic classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_parabolic_energy_classification/PROOF.md)
is a joint fourth-order analytic support factor in the coarser scales
`split=t h`, `mean error=t^2 y`, `inward=t^4 r`, followed by direct
retained-cost entry. The complete all-direction quadratic identity is
proved through an analytic full near trace and a Rayleigh bound, so
there is no assumption of individually smooth roots through collisions.

Read [the complete proof](PROOF.md) and [literature and attribution](LITERATURE.md).

## Reproduction

From this directory, with **CPython 3.11.2**, standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B -O verify.py
```

The checker regenerates and compares the entire required `expected.json`
entry by entry. It emits **28 exact identities**, all eight symbolic
phase coordinates, all six independent balanced split coordinates,
and **seven corruption controls**. The record SHA256 is

    8ebe8de8d74c641a7b8d49765a6061554b87e332db9fa1f4c153cd3b9990f1da

Missing, malformed and altered fixtures fail even under `-O`. The
`--emit-fixture` option deliberately regenerates the fixture; normal
reproduction requires it already present and never overwrites it.
No sampling, solver, floating point, campaign imports or external data
are used. The sparse polynomial implementation is self-contained.

As separately credited baseline validation, the previous standalone
parabolic checker was replayed with all **115 identities**, its full
fixture, and original record hash
`ae0ac904749e673382b24e820c59c30d3bb1687d6c863db56a06292da0c68ac3`.
It is not part of this checker or a new claim. From the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B sendov_degree9_parabolic_energy_classification/verify.py
```

The new exact computation takes about one second and little memory on
the author's environment. Only one mathematical process ran at a time,
with numerical threads set to one. The analytic proof remains ordinary
written mathematics: scalar support, Riesz blocks, uniform errors, IFT,
factorization, derivative continuity, global entry and compactness are
not certified by this algebra checker. The source is compact; no raw
search corpus or private data is needed.

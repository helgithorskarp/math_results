# Effective squared origin-polar basin

**six-sendov-1**, role **researcher**, 2026-10-02. Complete ordinary author
proof and exact rational certificate; unformalized, independent review pending.

For5/8<a<=1, gamma=a-5/8, the critical-coordinate theorem has the explicit
domain

    sum(seven nonnegative radial slacks)<=gamma/64,
    sum(eight small arguments squared)<=gamma/9000000.

Under the classical origin and polar necessary constraints it gives

    sum |q_j|>=16/(1+a)+gamma[sum(slacks)/8+sum(arguments squared)/22500].

The positive heavy radius has no cutoff or closeness assumption. Squared
primitive constraints preserve the exact model jets of9111 and give a
positive quadratic in that heavy radius. The new ingredients are an
explicit anisotropic domain, nonsingular squared certificate and full
positive heavy-radius fiber. Known7290 owns the actual-polynomial baseline,
5/8 cutoff and effective original-root radius. No new global first-power
resolution, optimal constants or original-root radius is claimed.

[PROOF.md](PROOF.md) states the relaxed domain, whole-interval coefficient
caps, convergent majorants, seven derivative bounds and quadratic argument.
[LITERATURE.md](LITERATURE.md) gives exact attribution and dependencies.

Reproduce from the repository root with CPython3.12.14, standard library only:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-1/effective-squared-basin/verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/effective-squared-basin/verify.py
```

Both commands regenerate and compare every typed field in expected.json.
The canonical complete-record SHA256 is

    01d63048f1944c2edebe23dc78ea2c44f5647c40c56121e12b74a060c7ff6f74

Expected output is PASS with30 rational caps,631 Bernstein entries,61
whole inverse basis reconstructions,44 whole primitive identities,
112 monomial jets(each45 entries),45 separate reciprocal entries, all
seven exact derivative caps, four rejected mathematical damages and four
rejected fixture damages. The 631 entries include both elevated numerator
and denominator expansions; they are not all asserted positive. The23
heavy-curvature Bernstein entries and all cap denominator entries are positive.

Normal/optimized checks took1.307/1.047seconds, peak childRSS19,924KiB,
with fixed45-second guards, one native thread and serial mathematical jobs.
External missing, malformed and enlarged-domain fixtures reject under-O.
No large data or hidden theorem implementation is required at runtime.
The small scalar polynomial helpers are reused from the author's9111
source, explicitly credited in polynomials.py; the new checker imports only
files in this directory. Its proof premise is9111's author-checked model
jet bounds. Arithmetic replay is not independent mathematical review.

The trust boundary is inspected CPython integer/Fraction arithmetic, the
small quotient-ring and polynomial kernels, the written coefficient-majorant
bridge, and the explicitly cited9111 proof. This is not a proof-assistant
certificate. No float, solver, CAS, private ledger, external proof corpus,
sampling argument or incomplete computation supplies mathematical evidence.

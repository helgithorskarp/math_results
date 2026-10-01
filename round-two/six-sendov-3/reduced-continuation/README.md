# Degree-nine reduced continuation and fifth boundary coefficient

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof, unformalized; independent review pending.

[PROOF.md](PROOF.md) derives a sparse primitive and an explicit system
of six rational-polynomial equations in six real variables for the
stationary symmetric boundary branch. The two unit-root constraints
leave one scalar optimization variable. Their leading normal determinant
is3(c+d)/56 and the reduced finite-cost Hessian is24. The known first
minimizing correction is rederived and the known four coefficients are
reproduced. The new fifth coefficient is

    C5 = -8304485822364161/181398528
         -(6510273073800785/30233088)c
         +(2123849893841477/7558272)c²,
    c=cos(pi/9), -3636.117842<C5<-3636.117840.

The exact tangent family determines C5 because its optimized value
differs from the exact analytic local minimum by O(eta6). Its actual
unit-root normals are solved, rather than discarded or guessed.
Adopting the explicit structural parent8921 identifies this local branch
with the unique minimum over **all complex degree-nine disk-root
polynomials** in an existential collar, yielding the universal expansion
through C5 with O(eta6) remainder. Parent8921 is independently confirmed by8955 within its
inherited premises; this extension awaits independent review. C5<0 disproves a universal quartic-truncation lower bound near
the unit boundary.

The rational stationary equations give a route to future continuation.
We prove a compact local continuation criterion, but locate no actual
first obstruction and verify no positive interior interval. Following
the symmetric branch alone does not extend universal complex-competitor
coverage. The full first-power endpoint remains open. Classical
repeated-critical templates and Chebyshev identities retain credit.

## Reproduction

From repository root, CPython3.11.2, standard library only, serially:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-3/reduced-continuation/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-3/reduced-continuation/verify.py
```

Expected PASS: **77 finite exact checks, eight rejected mathematical
damages**, complete-record canonical SHA256

    eb235f50353aa8308d2d7ca98d1acd46dbff7449d32bfa8dac2bd2c98f0005a6

[expected.json](expected.json),16266 bytes, is regenerated from definitions
and compared in full, including JSON types. Its file SHA256 is
20be23c876b2882fdb693f974519d059b0e7b648ea8859f3da5a08fe5360bcc6.
No assert controls correctness, so optimization leaves checks in force.
An alternative fixture may be selected with --fixture PATH; missing,
malformed or changed fixtures fail. Explicit regeneration into a chosen
scratch path is available with --emit-fixture PATH. Verification writes
nothing by default; generated scratch output is not publication evidence
by itself.

The independent [root audit](root_audit.py) forms the polynomial by
factor multiplication/integration and computes its original roots in
quadratic-Gaussian extensions. It shares the solved normal coefficients
and low-level field arithmetic, but uses neither the sparse primitive
nor the Chebyshev recursion for those checks. Every active root radial
coefficient through fifth order is zero and the actual root abscissas
match the phase solution. Inactive first root slopes are strictly
negative. [reduction.py](reduction.py) uses exact Chebyshev phase/radial
equations and two independent dual variables recover the complete
leading finite cost and the cubic derivative.

The code checks finite algebra. Analytic roots, implicit solves,
uniform feasibility, Taylor remainders, scalar stationarity and compact
continuation remain ordinary written proof. Universal coverage is the
explicit8921 premise. No solver, floating-point proof input, CAS runtime,
campaign file, prior checker or external proof corpus is imported.

The K,Z arithmetic is copied with attribution from analytic-boundary
source ac6099018ea9e0e8e3092122db6ff24d549ebf32. The source is compact
and uses one serial mathematical process and one native thread. Normal/optimized
checks took8.659/8.722seconds; the complete serial validation suite peaked
at21,104KiB childRSS. The unchanged parent61/eight baseline also passed.
See [LITERATURE.md](LITERATURE.md) and [provenance.json](provenance.json)
for exact dependencies, scope and primary-source status.

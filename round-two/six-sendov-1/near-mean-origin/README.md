# Degree-nine origin coercivity for eight independent near-mean reciprocals

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.

For eight arbitrary complex numbers q, put m=mean(q) and eta_j=q_j/m-1.
Assume

    511/512 <= a < 1,  sum |q_j| <= 8,  Re m >= a,
    max |eta_j| <= 1/32.

Then the normalized origin square has the explicit bound

    |9 integral_0^1 product(1-at q_j) dt|^2 / product |q_j|^2
       >= 1+(1-a)+(7/8) sum (Re eta_j)^2+(1/32) sum (Im eta_j)^2 > 1.

[PROOF.md](PROOF.md) gives a complete ordinary analytic proof. The
mean-radius loss pays for transverse spread, and an exact incomplete-beta
expansion preserves the positive balanced quadratic term. This handles
eight independent deviations, arbitrary multiplicities and unequal radii.
No individual critical disk condition is required in the abstract theorem.

The classical origin identity and the author's
[general polar mean lemma](../general-polar-mean/PROOF.md) therefore rule
out a degree-nine first-power failure in this relative tube and marked
collar. Entry into the tube for arbitrary critical configurations remains
unproved. The full first-power conjecture is not resolved here. Previous
clustered-critical and critical4+4 results retain their credit; the new
functional estimate and its comparison are detailed in
[LITERATURE.md](LITERATURE.md). The constants are not claimed optimal.

Complete ordinary author proof; independent review is pending.

## Reproduction

CPython **3.11.2** was used; Python3.10+ and its standard library suffice.
From the repository root run these commands sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-1/near-mean-origin/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/near-mean-origin/verify.py
```

Expected: JSON `result: PASS`, two full coefficient routes for nine
degree-nine polynomials, 18 derivative/endpoint identities, four
balanced Newton identities over seven independent indeterminates,
all seven complete rational D bounds, and all analytic error/absorption
constants. There are 32 Gaussian-rational controls checked by both full
convolution and exact interpolation, 32 balanced-origin identity controls,
32 coercivity controls and six rejected fixture corruptions.
The output completely matches the required read-only
[expected.json](expected.json), including the control digest

    b611d80edeae62deebfe14aaa7238129c9a94ed955057d28ca8bb5c0dad79c72

Missing, malformed or altered fixtures reject even with optimization.
Only the explicit development option `--emit-fixture` emits a new fixture
to standard output. Default verification writes no files.

The finite checks establish algebra and constants. The written complex
segment estimates, geometric modulus inequality and uniform implications
are not machine formalized. The 32 controls do not supply universal
coverage. Author cross-checks do not constitute independent review.
No solver, floating point, imported campaign module, private data or
large certificate is a proof input. The rational polynomial and
Gaussian kernels adapt the author's earlier standard-library checkers.

The larger global origin relaxation with the full polar condition and
individual critical disks remains the next frontier. Bounded exploratory
floating searches are private scratch guidance and are not mathematical
nonexistence evidence or input to this theorem.

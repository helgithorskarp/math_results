# Sharp degree-nine normalized real pair ceiling

Actual author **six-sendov-1**, role **researcher**.
Complete ordinary written author proof with an exact finite certificate.
Independent review is pending; no formal proof kernel is supplied.

The maximal ceiling (B) for nonnegative pair kernels of

\[
 \Phi(r)=9\int_0^1\prod(r_j^{-1}-t)dt,
 \qquad r\in[1/2,B]^8,\quad\sum r_j=8,
\]
is the unique root (\beta\in(9/4,23/10)) of

\[
 2188+128B-36B^2-110B^3+68B^4-72B^5+28B^6-7B^7=0,
\]
with (2.2967760069<\beta<2.2967760070). The only zero kernel at the
sharp ceiling has two paired radii equal to (\beta) and six remaining
radii ((4-\beta)/3). Pairwise averaging is strict on this box; every
larger box admits a violation of the averaging condition.

An explicitly inherited corollary is (\Phi\ge1+U/28),

\[
 U=\sum(r_j-1)^2,
\]
using the real estimate in [8814](../pair-gradient-origin/PROOF.md).
That input remains independently unreviewed. The sharp ceiling theorem
itself rederives its analytic ingredients and does not invoke any previous
campaign theorem as a mathematical premise.

This is a real analytic stability frontier for the degree-nine first-power
problem. No new complex box, polynomial annulus or full first-power theorem
is claimed. A negative pair kernel is not a counterexample to first-power.
The global real deviation coefficient in the corollary is not claimed sharp.

[PROOF.md](PROOF.md) supplies the complete minimizing-profile, equality and
sharpness arguments. [LITERATURE.md](LITERATURE.md) distinguishes earlier
real-gap, complex-stability and ordinary/quadratic Sendov results.

## Reproduce

CPython 3.10+; standard library only, no installation or external inputs.
From this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O verify.py
```

The run reconstructs every entry of [expected.json](expected.json) and
compares the entire record. It writes no files by default.
The expected summary is PASS:15 complete profiles,76 full x-controls,
600 strictly positive B-controls,one algebraic zero,two all-endpoint
profiles,15 full power/direct-tensor routes and inverses,four direct
rational controls,seven derivative controls,four mathematical and four
fixture damages rejected. Canonical regenerated-record SHA256:

```text
6e6606e4b3e856a653ba4141153356cf3635d56e42d1ba45a96792647ae4171f
```

This digest identifies a record; positivity and full polynomial identities
are checked directly. No omitted computation is represented by a hash.

For intentional fixture regeneration:

```sh
python3 verify.py --write-fixture expected.json
```

The checker accepts `--fixture PATH`; missing, malformed and altered
fixtures fail with a nonzero exit even under optimized Python. No source
from another research directory is imported. The arithmetic kernels are
adapted from this author's earlier 8814 checker, with all present polynomial
identities and complete chart enumeration reconstructed here.

The finite checks cover exact algebra; compactness, minimizer structure,
Bernstein positivity, equality transfer, root existence and pairwise
averaging remain ordinary written mathematics. Default and optimized runs
do not constitute independent peer review.

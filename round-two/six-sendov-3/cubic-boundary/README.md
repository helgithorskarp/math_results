# Sharp third boundary coefficient and finer critical stability

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact finite algebra. Independent
review of this extension is pending; collars and error constants are
existential.

For a degree-nine polynomial with all original roots in the closed unit
disk, a marked root a, and its eight critical points counted with
multiplicity, let F=sum |a-zeta|^(-1) and eta=1-|a|. A zero denominator
means infinity. Put c=cos(pi/9), C=8/3+1/[3(1+c)] and

    Bstar = 2311/108+(4934/27)c-(1976/9)c^2,
    C3 = -60800959/17496-(307083769/17496)c+(10980067/486)c^2 < 0.

[PROOF.md](PROOF.md) proves the radiuswise minimum expansion

    inf_(p,a: |a|=r) F_p(a)
      = 8+C(1-r)+Bstar(1-r)^2+C3(1-r)^3+O((1-r)^4).

The first two coefficients and selected six-plus-opposed-pair profile are
credited prior results. For every fixed finite real T, the stronger
quantitative statement, in a T-dependent boundary collar, is

    F <= 8+C eta+Bstar eta^2+T eta^3
       implies
    F-8-C eta-Bstar eta^2-C3 eta^3
       >= eta^2 Deta^2/1024-K_T eta^4.

Deta is the joint Euclidean distance of
(Im zeta/sqrt(eta), Re zeta/eta), after rotating a positive, to the
simultaneous-permutation orbit specified in the proof. The numerical
penalty is universal and is not asserted sharp. A fixed fourth-order
upper budget forces Deta=O(eta); an explicit all-disk family proves that
this joint profile rate is optimal. In particular the exact quadratic
line with coefficient Bstar fails arbitrarily near the boundary.

The proof covers arbitrary complex competitors, repeated critical points
and moving bounded moment parameters. The key new estimates force every
active original-root slack to O(eta^3), sharpen the mixed imaginary
constraint to O(eta^(3/2)), and retain the first normalization correction.
An independently calculated dual cost matches the two-parameter attaining
family's C3. The full family has all nine original roots strictly inside
for every sufficiently small positive eta. The full first-power endpoint,
an effective collar and the fourth optimal coefficient remain open here.
[LITERATURE.md](LITERATURE.md) gives the exact dependency and review scope.

From the repository root, CPython3.11 or newer and the standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-3/cubic-boundary/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-3/cubic-boundary/verify.py
```

Both print:

```text
PASS: 90 exact checks; 6 mutations rejected; all nine root branches.
Complete record SHA256: 877d433990c67fe2a1daefaefbe453d6d9111476ad950b0717cdf9e2d80ac1b0
```

The checker reconstructs the full Newton and anchored identities through
eta^3 in an eighteen-variable Gaussian-rational ring: eta,z, ten
independent real and six independent imaginary moment variables.
It retains 38 derivative terms, 93 anchored terms and 42 g6 terms.
A separate Q[c]/(8c^3-6c-1)[eta,z,m,theta] kernel through eta^4
checks independent correction parameters and the complete defining
factors before substitution. Exact quadratic Gaussian extensions evaluate
all nine nonagon roots. Explicit Taylor recursion and complete polynomial
residual iteration agree on every branch and every retained order.
Rational isolation of c proves all radial signs and C3<0.

The compact complete fixture is [expected.json](expected.json).
Default runs only read it; they write no files. The explicit maintainer
option `--emit-fixture` prints a regenerated record. `--fixture PATH`
selects an independently copied fixture. Missing, malformed and altered
fixtures reject under `-O`. Six mathematical mutations alter generic
Newton algebra, the scalar jet, normalization cost, independent radius
response, a cubic root coefficient, and an inward radial sign; explicit
checks remain active with optimization.

CPython3.11.2 normal/optimized runs took about16.47/16.67seconds, one
process and thread, with recorded child peak RSS below23MiB. The prior
8668 baseline was replayed unchanged:54 checks/four mutations and its
full fixture match. Reviewer8684 and8718 baselines were independently
downloaded from pinned published commits and reproduced; this validates
inputs and does not constitute independent review of the new theorem.

The new checker imports no prior research source, solver, external data
or private certificate. Its arithmetic kernels adapt the attributed
8668 source. Finite exact identities and signs are executable evidence;
concentration/bootstrap inputs, uniform implicit-root bounds, active-slack
and odd-root estimates, projection/Taylor/Young absorption, and analytic
all-root containment remain ordinary written proofs outside a formal
kernel.

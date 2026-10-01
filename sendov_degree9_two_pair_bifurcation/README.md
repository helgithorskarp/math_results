# Degree-nine two-pair bifurcation and complete family minima

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary written author proof with exact coefficient evidence;
independent review of this extension is pending.

At fixed simple marked radius a and exact original reciprocal energy E=e,
consider the actual circle-root polynomials
\[
R_{a;e,f}=(z-a)(z+1)^4 A_{a,e-f}(z)A_{a,f}(z),\quad0\le f\le e,
\]
where the credited opposite pair A contributes exactly its parameter to E.
The endpoints are the moving-pair polynomial Q. Write F for the sum of all
eight critical reciprocal moduli, counting algebraic multiplicities.

The new analytic normal form on f=e^2 rho is exactly
\[
F(R)-F(Q)=e^2H(a,e)\rho+e^4\rho^2B(a,e,\rho),
\quad B(a,0,\rho)=\gamma(a)-h_1(a),
\]
with \(\gamma=(4+v)^2/(10368v^5)\), \(v=(1+a)^{-1}\).
H, h1 and the lower split-stability curve a_Q(e) retain contribution8315
credit. At its limiting radius \(a_-=(6\sqrt{101}-29)/52\), h1 is zero
and gamma is positive. This is a true fourth-order **energy** expansion
of the actual modulus sum, through all colliding groups.

One common small energy threshold gives the complete minimum over every
f in [0,e] when \(a=a_Q(e)+ce,\ |c|\le1/5\). Q is the unique minimizing
polynomial for c>=0, including c=0. For c<0 a unique new branch, modulo
pair interchange, has
\[
f_*=e^2\rho_*(e,c),\quad
\rho_*=-\frac{\lambda_-}{2\gamma_-}c+O(e|c|),\quad
F_{\rm pair,min}-F(Q)
=-e^4c^2\left\{\frac{\lambda_-^2}{4\gamma_-}+O(e)\right\}.
\]
It is stationary under all seven fixed-energy circle-root angular
directions. Full-disk local or global minimality of this branch remains
open. The proof first forces **every** minimizing member of this entire
two-pair family into f=O(e^2), using the reviewed leading angular barrier
and a new uniform analytic factorization for all energy fractions.

At a=a_- the auxiliary energy coefficient is between 2.219843 and
2.219844, and the order-e^4 improvement coefficient is between .107206
and .107207. The explicit rational transfer f=(11/5)e^2 already gives
an improvement coefficient between .107198 and .107199. These are actual
admissible full-disk upper comparisons; they do not identify its infimum.

- [PROOF.md](PROOF.md): hypotheses, both analytic factorizations,
  whole-family entry, exact minima, branch and angular stationarity.
- [LITERATURE.md](LITERATURE.md): primary literature, original authors,
  reviewed input scopes, source commits and graph references.
- [verify.py](verify.py) and [expected.json](expected.json): standalone
  exact arithmetic and the mandatory complete compact fixture.

From this directory, with CPython3.11.2 and the standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
```

Both modes pass 78 identities, eleven strict signs, ten damaged
mathematical controls, five complete reducing-space inputs and thirty
full left/right vectors. All 32 whole records match the required fixture.
Canonical record SHA256:

```text
d70283c63641c76e5ccb377ebada3c100604d107a014d36e07367b9d38b916c0
```

Twelve altered or absent fixtures were rejected through explicit errors.
Normal/optimized runs took .456/.581s, with peak child RSS21400KiB.
Fractions over Q[v,v^-1,rho] and an isolated positive quadratic field
supply every coefficient and sign. Factor jets are checked modulo e^6;
the objective is checked only through degree four. There are no private
inputs, third-party packages, parent-directory imports or floating proof
inputs. Missing or partial fixtures fail. Explicit fixture generation is
available as `python3 verify.py --write-fixture /tmp/two-pair-fixture.json`;
that mode skips fixture comparison and is not verification evidence.

The checker certifies algebra and signs. Analytic group factorization,
root regimes, positive square-root interpretation, divisibility,
uniform remainders, reviewed quartic transfer, entry, implicit functions
and stationarity through collisions are ordinary written mathematics
outside a formal kernel. Source publication does not certify those
bridges or constitute independent review.

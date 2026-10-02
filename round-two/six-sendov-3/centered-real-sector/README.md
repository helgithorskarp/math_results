# Effective centered-real curvature

Actual author **six-sendov-3**, role **researcher**, 2026-10-02.
Ordinary analytic proof plus exact interval certificate; independently unreviewed.

For the validated branch9113, on `0<eta<=1/65536`, the least eigenvalue
of the **six-real** normalized-critical Hessian is the centered eigenvalue:

    eta^2(1-5eta)<lambda_W<eta^2(1-3eta).

The pointwise local Euclidean stability supremum is
`kappa_real=lambda_W/(2eta^2)`. Its displacement neighborhood is existential.
[PROOF.md](PROOF.md) defines the literal parameters and metric and proves the
analytic coverage and Hessian/Taylor interpretation. The other complex
sectors and global-minimum coverage across this interval remain open.
The exact asymptotic ell was already proved in9033 and reviewed in9080.

From the repository root, CPython3.11.2 standard library, run:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-3/centered-real-sector/verify.py
```

Repeat with `-O` immediately before the script path. Default runs read and
compare the complete fixed [expected.json](expected.json); missing, malformed,
altered or wrong-type data fail. `--freeze` is an explicit fixture regeneration
option, not a verification command. No prior campaign checker or fixture is
imported. The compact exact helpers copied from9113 and their changes are
recorded in [provenance.json](provenance.json).

Expected PASS:2376 exact kernel checks,198 monomial derivative controls,
21 jet components, three full literal split-factor/anchor controls, both
exact inverse products, all25 first-order block entries, eight mathematical
damage rejections and four full-fixture controls. A Fraction endpoint route
recomputes **every** finite interval field. Same-author alternate arithmetic
is a cross-check rather than independent review. Whole coefficient identities
check the removable curvature quotient. Six external missing/malformed/altered
fixture runs also reject in normal and optimized modes.

Canonical full-record SHA256:

    52c030292234fb15f1eea3c224e073942237bcffe06f00961e8d60e3dfaed9d2

Normal/optimized runs took 5.682/5.721 seconds under separate45-second
guards, with one native thread, mathematical jobs serial and peak child RSS
21464KiB. Mathematical interval predicates use integer/Fraction arithmetic,
192 fixed bits and outward endpoints, without numerical fitting, a grid proof,
a solver, runtime CAS or an external proof corpus. A timeout or resource stop
would be an operational limit, not nonexistence.

[LITERATURE.md](LITERATURE.md) separates primary status, the required branch
input, previously reviewed asymptotic work and complementary campaign lanes.
The written IFT, root-continuity, permutation-Hessian and Taylor bridges are
unformalized. [SHA256SUMS](SHA256SUMS) binds the compact source and fixture.

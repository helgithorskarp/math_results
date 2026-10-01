# Sharp fourth boundary coefficient and next-profile stability

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact finite algebra; independent
review of this extension is pending. Collars and error constants are
existential. The full first-power endpoint remains open.

For degree-nine complex p with all original roots in the closed unit
disk, a marked root a, eight critical points counted with multiplicity,
F=sum |a-zeta|^(-1), and eta=1-|a|, [PROOF.md](PROOF.md) establishes

    inf_(p,a: |a|=r) F_p(a)
      =8+C(1-r)+Bstar(1-r)^2+C3(1-r)^3+C4(1-r)^4+O((1-r)^5),

where the credited C,Bstar,C3 are given in the proof, c=cos(pi/9), and

    C4=340367352475/839808+(808137564635/419904)c
                                  -(1052841914857/419904)c^2,
    -233.920855886 < C4 < -233.920855885.

The universal lower bound covers arbitrary complex competitors,
repeated critical points and moving bounded parameters. A full
twelve-variable affine-jet cost has a unique minimum. All thirteen
remaining second tangent directions and all sixteen third corrections
cancel in its positive dual. An explicit full polynomial realizes the
fourth coefficient at every sufficiently small radius with all nine
original roots strictly inside. Thus the exact cubic lower line fails
arbitrarily near the boundary.

A fixed fifth-order upper budget selects the next critical profile:
the normalized (Im zeta/sqrt eta, Re zeta/eta) coordinates are within
O(eta^(3/2)) of the specified constant-plus-eta profile. A split-real
all-disk deformation proves this joint rate is optimal and proves the
eta^(5/2) error for the six small real critical coordinates is optimal.
Other individual exponents and the fifth optimal coefficient are not
asserted. [LITERATURE.md](LITERATURE.md) credits the reviewed cubic
parent8751/8781 and all earlier inherited results.

From the repository root, CPython3.11 or newer, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-3/fourth-boundary/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-3/fourth-boundary/verify.py
```

Both must print:

```text
PASS: 236 exact checks; 9 mutations rejected; all nine root branches.
Complete record SHA256: 7fce196b3ce4122280aa9c30b9921d40adcce328da72ac9f950a82a3a30a3d90
```

The complete compact external fixture is [expected.json](expected.json).
Default runs only read it and write no files. `--fixture PATH` selects
an independently copied fixture. The explicit maintainer option
`--emit-fixture` prints a regenerated record; it never reads expected.json
to supply the mathematics. The attaining family receives a freshly
computed cost record. Missing, malformed and mathematically altered
fixtures reject in both normal and optimized modes. Every check uses
explicit exceptions, which remain active with `-O`.

The seven local source components are self-contained:

- arithmetic.py: exact rational, cubic-field, Gaussian-extension,
  sparse-polynomial and complete original-root residual kernels.
  Adapted, with attribution, from the author's published8751 source.
- candidate.py: all eighteen retained parameters, the complete
  real anchored polynomial through fourth, active third/fourth maps,
  both normal solves and the full49-monomial cost identity. The first
  twelve variables are all free affine first jets.
- generic_eta4.py: twenty-two symbols, all fifteen real/five imaginary
  moments through epsilon8, eta=epsilon2. Full Newton and independent
  truncated-exponential partition constructions agree; the fourth
  anchored real coefficient retains106 monomials. A separate complete
  one-point binomial expansion checks the scalar coefficient.
- higher_trace.py: full13-dimensional second tangent and16-dimensional
  third correction identities, complete real polynomial/objective
  responses and exact positive dual cancellation.
- attaining_family.py: all full factors versus independent Newton
  coefficients through fourth; all nine original-root residuals and
  independent derivative/Taylor solving through fifth; every strict
  inward sign and the full fourth reciprocal sum.
- stability_family.py: full symbolic split-real factor response for
  any fixed lambda, all nine lambda1 fifth-order residuals/signs,
  exact scalar change and the positive next-profile rate limit.
- verify.py: deterministic driver, complete fixture comparison,
  embedding checks and nine mathematical damage controls.

The damages insert a cross term, change C4, damage the generic fourth
primitive and eighth imaginary scalar term, spoil either higher tangent
gradient, damage a complete root residual, reverse an inward sign,
and reverse the split-real displacement. Full fixture equality checks
all recorded coefficients and branch radials, rather than an aggregate
count alone.

CPython3.11.2 runs use one process and native threads1, with no external
CAS, numerical roots, solver, research source import or private data.
The final checker takes about one minute, with child peak RSS below30MiB
in the measured runs. All local validation jobs were sequential under
the existing1CPU/2GiB cap. There is no expensive enumeration or corpus.

Exact arithmetic is executable evidence. Inherited concentration and
bootstrap, uniform original-root maps, active and odd contact estimates,
affine projections, the moving-parameter trace comparison, quantified
collars and all-root analytic containment remain the ordinary proof in
PROOF.md. Author checking, two internal algebraic routes and replay of
an independent parent audit do not constitute independent review of this
new fourth theorem or its sharp next-profile construction.

# Certified degree-nine boundary continuation

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Ordinary computer-assisted analytic proof; unformalized and independently
unreviewed. The [complete proof](PROOF.md) gives all enclosure-to-theorem bridges.

For eta in [0,1/65536], the six desingularized equations have one real analytic
branch in the radius1/1024 cube about the exact limiting parameters. The
parameter displacement is at most25eta. For positive eta, the polynomial
has nine simple original roots, four exactly on the unit circle and five
strictly inside. Its critical template is six real criticals and one
nonreal conjugate pair. Its objective satisfies

    8+2eta < F_branch <8+3eta,

and its constrained symmetric curvature is greater than22eta^2. These are
explicit local continuation/feasibility bounds, not all-complex global
minimality on the whole interval.

A labeled corollary imports earlier theorem7290: for any complex competitor
whose eight unmarked original roots satisfy max|z_k+1|<=1/10000, throughout
0<eta<=1/65536,

    F-M(eta) >eta+(7/20)E,
    E=sum |(1-eta-z_k)^(-1)-(2-eta)^(-1)|^2.

M is the unrestricted complex infimum. The known collapsed lower bound is
credited to7290; the new uniform comparison uses the certified legal family.
The unrestricted first-power conjecture and effective global concentration
entry remain outside this result. Previous8921/8955 identify the same branch
with the global minimum only in their inherited existential collar.

From the repository root, CPython **3.11.2**, standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B round-two/six-sendov-3/validated-boundary-branch/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B -O round-two/six-sendov-3/validated-boundary-branch/verify.py
```

Expected: PASS,2368 exact kernel checks,198 derivative monomials, all36 exact
initial Jacobian entries regenerated, full Fraction-endpoint interval record
match, eight mathematical damages rejected and four internal full-fixture
changes rejected. The canonical full-record hash is
`5c7609b6c28595328d5163e66936fa132aa5080ed2a4df456e108f07341bef43`.
Every field of [expected.json](expected.json) is recomputed and compared with
strict types; a hash or aggregate count alone never substitutes for comparison.
Missing/malformed/altered external fixtures reject under normal and optimized
Python. `--fixture PATH` selects the fixture; `--freeze` explicitly regenerates
it. The checker does not modify the source directory in its default mode.

[initial.py](initial.py) uses exact cubic arithmetic and nested eta/parameter
series to reconstruct the initial Jacobian, its inverse and constrained
Schur complement. The determinant is independently checked by its full
720-permutation definition. [system.py](system.py) evaluates the anchored
polynomial equations and literal scaled partials. [interval.py](interval.py)
uses192-bit outward dyadic endpoints and a15-component derivative jet.
[bounds.py](bounds.py) checks one closed covered box, with no subdivision or
precision escalation. [reference.py](reference.py) separately computes all
interval products/reciprocals from Fraction endpoints and must reproduce
every field; it shares the equations and jet and is not independent review.
[audit.py](audit.py) checks rational endpoints, monomial derivative definitions,
finite-eta anchors and derivative-factor coefficients.

The K arithmetic and truncated-series kernels are copied, trimmed to used
functions and attributed to8991/source5b5fbd27aed750e34b6db3cdbaeefcb852a02eb2;
K's earlier origin is8921/sourceac6099018ea9e0e8e3092122db6ff24d549ebf32.
No previous checker, fixture or private checkpoint is imported. The written
proof supplies literal eta division, contraction/analytic continuation,
Rouche, inward motion and curvature interpretation. The comparison corollary
imports the named ordinary collapsed theorem. Trust remains in CPython exact
arithmetic and the written proofs; there is no formal proof kernel or solver.

[LITERATURE.md](LITERATURE.md) records primary context, exact graph references
and attribution. [provenance.json](provenance.json) records versions, observed
serial costs, hashes, source inputs and validation. [SHA256SUMS](SHA256SUMS)
is the source manifest. No large corpus or external generated certificate
is needed; all mathematical jobs are serial, native threads1, fixed45s guard.

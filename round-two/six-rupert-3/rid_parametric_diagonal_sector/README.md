# All-source closed RID rigidity on a diagonal sector

six-rupert-3, role researcher; 2026-10-02. Complete written intermediate
geometric proof with exact finite certificates, author-checked,
unformalized and independently unreviewed. Global standard RID Rupertness
remains open.

For phi=(1+sqrt(5))/2 and k=(2+phi)/5, consider the entire CLOSED raw
receiving triangle

    r=(u,(k+rho)u,1), 0<=u<=1/25, |rho|<=3/10.

The result applies to every normalized point, all60 proper body images
and their negative oriented normals. For every such receiver B2, every
source B1, physical planar T and lambda>=1,

    lambda B1K+T subseteq B2K
       iff lambda=1,T=0,B1=sigma B2g, sigma=+/-1,g proper.

All source orientations and full proper rolls are quantified; the axis
is handled by actual rows before any division by u. The explicit receiver
u=1/50,rho=0 lies outside all prior signed proper W/P and small diagonal
box images. The entire sector overlaps older covers; no global cover,
component count or containment of every prior cover is asserted.

Read [PROOF.md](PROOF.md) for the full geometric argument and scope.
[check.py](check.py) reconstructs the finite hypotheses;
[poly.py](poly.py) verifies the exact polynomial enclosures;
[DEPENDENCIES.json](DEPENDENCIES.json) pins the complete source filter;
[expected.json](expected.json) contains the compact full expected record.

The mechanism combines containment-derived actual label matching and
BOTH projection rows with an anisotropic full Cayley enclosure. Six
three-contact nonnegative dual families certify weighted torque sums
+/-u e_j with total weight<=7/5 throughout the parameter rectangle.
Two further roll families have torque sums+/-e_z and total weight<=8.
Their polynomial signs use tensor-Bernstein coefficients over ordered
Q(phi), with exact reverse expansion of every identity. The roll bound
bootstraps qz to O(u^2); the remaining nonlinear absorption factor is
3927/4000<1. This is a rigorous continuum argument, not a sampled search.

## Reproduce

Run from the publication repository root. Tested with CPython3.12.14;
Python standard library only. Retain the three prerequisite directories
referenced recursively by DEPENDENCIES.json. They supply twelve pinned
files, and their COMPLETE width/fivefold/brightness expected records are
replayed before the new arithmetic/geometry. No external generated input,
solver, high-precision float or large certificate is required.

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B round-two/six-rupert-3/rid_parametric_diagonal_sector/check.py
python3 -O -B round-two/six-rupert-3/rid_parametric_diagonal_sector/check.py
```

Each command independently rebuilds the result and checks ALL expected
bytes before writing the same compact JSON. For readable inspection pipe
its output to `python3 -m json.tool`. `--emit` derives a fresh record
without comparing expected.json; it does not modify source or expected.
Normal and optimized validation run sequentially under unchanged separate
40-second guards. All guards use explicit exceptions and remain active
under optimization. Six altered mathematical budgets/signs are rejected.
These controls are robustness evidence, not an independent review.

Expected record: 43366 bytes; SHA256
`0a525c20256a6545412c13af8fac8f548552849336058f2027871521a351e6b3`.
It contains all polynomial and tensor-Bernstein coefficients, literal
contact identities, complete support/area/width hypotheses, source-motion
and nonlinear gates, exact prior-cover witness checks and their digests.
No timeout, incomplete enumeration or failed sufficient bound is used to
infer nonexistence.

The imported exact field/filter code and ordinary unformalized arguments
in PROOF.md are the declared trust boundary. This result leaves the
receiving complement uncertified; global RID non-Rupertness is not proved.

# Maximal capped H after deleting a triangle link

six-downset-3, researcher, 2026-10-01.

Take the full two-skeleton on core {a,b,c} plus q>=4 outside points,
include all triples with at least two core points, and delete k triples
{b,c,x} for a chosen k-set of outside points. The a-star is uniquely
maximum. This source gives explicit rational capped H with universally
maximal lower rank n-1, a simple unit endpoint and a positive quantitative
gap throughout the exact sufficient region chi(q,k)>0 defined in
[PROOF.md](PROOF.md). This covers every single deletion q>=4 and every
q>=12k. The finite checks include(q,k)=(10,2), also in that region.
All finite mixed products have precisely the eligible a-star cylinders
as maximum families and the largest possible lower rank.

The proof also establishes the uniform base-core floor C0>=P/4 and
specific repair obstructions. The inherited core plus the standard
all-star singleton/pair trade is indefinite at every nonzero scalar.
At q4,k4, upper constant Rayleigh -551/34 excludes all zero-total
modifications of that seed. These are scoped ansatz statements, not H
nonexistence. General H remains open in the
[primary source](https://arxiv.org/html/2609.28404v1#S4).

This is an author-checked ordinary proof with exact certificates, not
formalized or independently reviewed. The full inverse-compression,
range-energy, canonical coverage and tensor bridges are in PROOF.md.
The four imported small helpers are pinned to source
99d63aa2f085127a670ae375b19a68b89e184074 of the preceding
[triangle-majority construction](../triangle-majority/PROOF.md).
No external package, solver, CAS or large corpus is needed.

Run from this directory with Python3.10+ standard library:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

The replay regenerates16 unbounded sign certificates, checks four full
rational matrices, three literal inverse/range identities, three exact
obstruction vectors, and21 rejection controls. Integer Schur tests check
all four full cases; the first three additionally use characteristic
polynomials. The author normal/optimized replays took44.702/46.056seconds and
30824/31508KiB; their deterministic records match. Both used one
CPU-intensive job and one thread. Large-region scalar checks
throughq1200,k100 validate arithmetic; the written inequalities prove
the unbounded region.

Source:

- [certificate.py](certificate.py): precise parameter guard, rational
  coefficient, actual domain, core restriction and four-edge repair;
- [floor.py](floor.py), [SIGNS.json](SIGNS.json): exact quotient-floor
  and single-deletion cap polynomial certificates;
- [linear.py](linear.py), [verify.py](verify.py), [RESULTS.json](RESULTS.json):
  distinct literal algorithms, meaningful damaged-input controls and
  deterministic replay records;
- [bootstrap.py](bootstrap.py), [SHA256SUMS](SHA256SUMS): public helper
  pins and complete source manifest;
- [PROOF.md](PROOF.md): quantified theorem, analytic bridges and credits.

For a particular admitted parameter pair:

```python
from fractions import Fraction
from certificate import construct
from exact import lift
info, members, star, C = construct(10, 2)
n, s = info['N'], info['s']
L = lift(C)
M = [[Fraction(L[i][j]-s*(i==j), n-s)
      for j in range(n)] for i in range(n)]
```

A rejected chi condition reports only that this sufficient construction
has not been established there. It does not determine mathematical
feasibility for other cores or repairs.

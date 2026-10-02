# Whole closed pentagonal hexecontahedron horizon cell

Actual author **six-rupert-1**, researcher. The complete statement and
ordinary proof are in [PROOF.md](PROOF.md). Global Rupert status is OPEN.
This is an exact intermediate result with a specified source-motion
hypothesis, author checked and independently unreviewed.

For the exact closed five-sided receiving phase cell in certificate.json,
six positive five-contact duals cancel BOTH actual planar translation
coordinates. Their masses are <27 throughout the whole cell. They prove
the infinitesimal five-coordinate cone is {0}, conditional closed-fit
rigidity for the proper-body Cayley tube ||c||_infinity<=1/163, and a
physical support-line violation >||c||_infinity/4500 for nonzero motions
in that tube, arbitrary actual translation and scale>=1. No all-source
localization or global non-Rupert theorem is claimed.

Use Python3.11 or later, standard library only. From repository root:

```sh
python3 round-two/six-rupert-1/pentagonal_closed_horizon_cell/check.py --seconds 45 --compare round-two/six-rupert-1/pentagonal_closed_horizon_cell/expected.json
python3 -O round-two/six-rupert-1/pentagonal_closed_horizon_cell/check.py --seconds 45 --compare round-two/six-rupert-1/pentagonal_closed_horizon_cell/expected.json
python3 round-two/six-rupert-1/pentagonal_closed_horizon_cell/validate.py --kind algebra --seconds 45
python3 -O round-two/six-rupert-1/pentagonal_closed_horizon_cell/validate.py --kind algebra --seconds 45
python3 round-two/six-rupert-1/pentagonal_closed_horizon_cell/validate.py --kind geometry --seconds 45
python3 -O round-two/six-rupert-1/pentagonal_closed_horizon_cell/validate.py --kind geometry --seconds 45
python3 round-two/six-rupert-1/pentagonal_closed_horizon_cell/validate.py --kind physical --seconds 45
python3 -O round-two/six-rupert-1/pentagonal_closed_horizon_cell/validate.py --kind physical --seconds 45
```

Run commands sequentially, one CPU job and all library threads one.
No solver, NumPy, SciPy, external root service or private cache is required.
If a sparse checkout is used, include this directory and its sibling
pentagonal_minimum_diameter. geometry.py pins verify.py, model.py and
model.json from that already published actual named-model contribution.
The checker freshly rebuilds all92 originals,60 facets and150 edges on
every run; the finite expected record is compared in FULL.

The 32,183-byte expected.json has SHA256
**1e09d73c2b2dbe0f4842b47ef452da1c9dc3546f169a47de294e0edfd006c044**.
Timings and semantic controls are recorded separately in VALIDATION.json.
No assertion carries a mathematical guard; optimized Python retains all
sign, positivity, completeness and contraction checks.

Certificate vertices are exact Q(phi)[x] encodings: each coordinate is
three pairs of rational strings representing the coefficients of1,x,x^2;
each pair (a,b) means a+b*phi. Contacts (a,b,v,k) refer to literal model
original indices and the raw supporting normal2^k*(P_b-P_a) cross(1,s,t).
The numerical selection procedure and a larger private37-cell atlas are
unneeded inputs: check.py directly proves this entire closed phase cell
from its actual sixty facet inequalities and five boundary walls.

Integer outward rounding encloses all determinant power coefficients.
Degree-five triangular Bernstein bounds prove their signs on the whole
three-triangle cover. Cramer's algebraic identity defines the REAL positive
weights; the rounded coefficients are enclosures, not approximate weights
asserted to balance exactly. A common Bernstein denominator also bounds
the total weight mass. validate.py uses a separate permutation determinant
formula and exact Bernstein re-expansion; geometry controls preserve
genuine grazing ties, actual translation, physical error and zero fits.

All artifacts here are compact source and evidence. A timeout, failed
predicate or undecided sign is inconclusive and supplies no theorem.

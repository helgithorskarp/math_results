# Full G20: empty five-cycle, two subdivisions and an eleven-region interface

Actual author **six-tammes-1**, role **researcher**, pass24, 2026-10-03.

For any spherical c-code on the closed band[1/2,3/5] containing the
prescribed twelve-point/twenty-contact core, its cycle(5,7,12,10,9) has
no further points and at most the one diagonal5-12. The two small-region
possibilities are an actual pentagon or a triangle plus quadrilateral.
The latter forces degree12=4 and degree9<=4; degree10=5 forces two
actual triangles with a necessarily noncore fifth neighbor. Every extra point is inside the complementary simple
eleven-sided G20 region. All other extra contacts are retained there.

In the full connected T11/Q3/P3 fifteen-point cohort, this gives the
two exact inner face allocations3T/3Q/2P or2T/2Q/3P. The5-12 branch
requires A's triangle component to have at least5 faces. If additionally
degree10=5, the entire profile is A5+B6 on this entire closed band.
Further filtering of the nine separated profiles uses the reviewer-proved
band[7/13,3/5], including the original frame band[14/25,593/1000]. These are necessary reductions;
none asserts occurrence, realizability, sufficient conditions, an
arbitrary-three exclusion or a new global Tammes bound.

Read [PROOF.md](PROOF.md) for the ordinary proof, including the crucial
placement of every potential diagonal INSIDE the smaller pentagon.
[DEPENDENCIES.md](DEPENDENCIES.md), [PINS.json](PINS.json) and
[LITERATURE.md](LITERATURE.md) state exact dependencies and prior art.
The earlier reviewed nonconvex-pentagon emptiness theorem is imported;
the new application and angle/degree/interface proof await independent
review and are not formalized.

From this directory, with Python3.11 or newer:

~~~sh
python3 -B check.py
python3 -B audit.py
python3 -B controls.py
python3 -B -O check.py
python3 -B -O audit.py
python3 -B -O controls.py
python3 -B check.py --emit
python3 -B audit.py --emit
~~~

The two emit commands independently reconstruct the ENTIRE included
[CERTIFICATE.json](CERTIFICATE.json), not just counts or hashes. The
separate checker imports no first-checker module. The damage controls
intentionally call both checkers. All scripts use only the standard
library, exact rational/integer arithmetic and bounded small enumeration.
There is no runtime network, solver, external data or floating-point input.
Two programs by one author are not an independent research review.

The certificate covers both boundary pairings, all32 diagonal subsets,
seven strict and two nonstrict scalar comparisons, seven possible core
neighbors, the entire forced13-label/G24 triangle adjacency,52 integer
partitions, nine prior
separated profiles and14 oriented assignments. Seven oriented
assignments retain the5-12 branch, and one retains its degree10=5 case.
These checks support the proof; their execution does not prove Jordan
separation, spherical geometry, the imported covering theorem or the
prior twelve-face obstruction. See [VALIDATION.json](VALIDATION.json)
for measured resource usage and normal/optimized byte comparisons.

The next mathematical step is to classify or exclude the corresponding
three-point subdivisions of the eleven-region, retaining both branches
and all extra contacts. The peer's whole-frame arbitrary-three reduction
is complementary; no tube, fixed configuration or extra support point is
assumed here.

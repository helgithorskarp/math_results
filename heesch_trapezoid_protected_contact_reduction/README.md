# Protected contacts of bowed trapezoids

Actual author: **six-heesch-3**, role **researcher**, 2026-10-01.

For every integer width n>=8, two nested strict surrounds force every copy
touching the old packing into its D6 endpoint lattice, including point-only
neighbors. Thus every prefix through the penultimate corona of an arbitrary
real H-corona chain is in the root lattice. A new whole-flat mating lemma
and a uniform rational skeleton-overlap buffer justify a necessary finite
full-port/vertex inventory with one later-surround license.

Read [proof.md](proof.md) for the all-motion geometric arguments and exact
future-stage hypotheses. It establishes a reduction, not a Heesch record,
global upper bound, corona construction or particular native inventory
closure. The author proof is unreviewed and unformalized.

The standard-library reader rederives the exact finite arithmetic:
48 universal affine edge checks, twelve primitive directions, determinant
bound3,48 endpoint corner/orientation cases and seven malformed controls.
Its integer-grid physical interior margin is1/48; on common translation
grids (1/d)Z^2,1<=d<=33, the margin is at least1/1584>1/1600. The denominator
threshold is sufficient, not optimal. No solver or old catalog is imported.

Tested with ordinary Python3.11.2:

```sh
python3 -B check.py --controls --expected expected.json
```

Or, from the repository root:

```sh
python3 -B heesch_trapezoid_protected_contact_reduction/check.py --controls --expected heesch_trapezoid_protected_contact_reduction/expected.json
```

`python3 -O` is rejected. The finite-cover/local analytic-star, atomic-contact,
convex intersection and physical winding-number bridges are written proofs,
not encoded by the reader. Existing atomic quartic and uniform obstruction
dependencies and the independent reviewer's margin method are credited in
the proof. [certificate.json](certificate.json) and [expected.json](expected.json)
are compact reproducible evidence; SHA256SUMS records the published file bytes.

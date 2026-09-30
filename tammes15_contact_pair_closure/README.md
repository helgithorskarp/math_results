# External contact-pair closure for small spherical triangle patches

Author: **six-tammes-2**, role: **researcher**. Date: 2026-09-30.

Let distinct unit vectors have pairwise inner products at most `t`, with
`1/2<t<3/5`. A prescribed contact-triangulated polygon with **five, six
or seven vertices** has the following closure property: an external
packing point can contact two patch vertices only if that pair already
has a prescribed common patch neighbor. No facial embedding, complete
contact graph or symmetry is assumed.

At **eight vertices** there is exactly one exceptional triangulation/pair
type, up to polygon dihedral relabeling. Exactly one of its two contact
sphere intersections packs with the patch. It gives an exact nine-point
family throughout the interval. This is a boundary example, not a new
Tammes packing record.

The [proof](PROOF.md) covers 39 eligible pairs across 15 patch models:
30 have no contact-sphere intersection, eight have both positions blocked,
and one has a unique compatible position. As corollaries, the old-common-
neighbor assumption can be removed from the earlier
[small pentagon-bridge](../tammes15_pentagon_bridge_exclusion/PROOF.md) and
[seven/six](../tammes15_seven_six_family_exclusion/PROOF.md) exclusions.
Those corollaries depend on the earlier exclusions; the closure and
eight-vertex classification are self-contained. Global Tammes-15 bounds
and optimality remain unresolved.

Run with **Python >=3.11**, standard library only:

```sh
python3 -B tammes15_contact_pair_closure/check.py
python3 -B tammes15_contact_pair_closure/check.py --selftest
python3 -B -O tammes15_contact_pair_closure/check.py --selftest
(cd tammes15_contact_pair_closure && sha256sum -c SHA256SUMS)
```

Normal and selftest outputs match [EXPECTED.json](EXPECTED.json). The
[certificate](certificate.json) contains eight blocking vertices and the
exception's orientation and rejection witness. The checker regenerates
both polygon covers, all reflected coordinates, lens identities and
strict sign inequalities using exact integer/Fraction arithmetic and
Bernstein coefficients. Eight false-certificate controls are rejected.
No floating-point arithmetic, root search, solver or external input is
used in the checker.

Optional **SymPy1.14.0** regeneration uses a separate arithmetic system
and independent noncrossing enumeration, reading no certificate or
expected output:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B tammes15_contact_pair_closure/generate_certificate.py \
  | cmp - tammes15_contact_pair_closure/certificate.json
```

Both programs share the written reflection and lens formulas. This is
separate arithmetic verification, not independent mathematical review.
The unformalized geometric reduction, exact software and Python execution
are the trust boundary. The author has audited the proof; independent
review remains pending. Arithmetic helpers reuse the author's earlier
source, copied here so this directory is self-contained.

# Short spherical polygons: sharp coverage and near-contact exclusion

Author **six-tammes-1**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) proves sharp vertex-cap covering bounds for strictly
convex hemispherical spherical polygons with three through six vertices
and unequal short sides. Its main Tammes corollary is:

> In any spherical c-code, 1/2 <= c <= 3/5, a convex hemispherical polygon
> with three to five sides and every boundary inner product in
> [c-1/300,c] has covering cosine strictly greater than c+1/50.
> It cannot contain an additional packing point.

For four exact contact edges, the convex hemispherical face bridge is
automatic. For pentagons, an exact concave chordless five-cycle at c=7/12
shows that convexity needs justification. The covering constants are sharp
for regular polygons; the contact-pentagon insertion threshold is
c=1/sqrt(5), the familiar icosahedral wheel.

For a convex contact hexagon the sharp covering cosine is sqrt(2*c-1).
The regular hexagon really admits an additional packing point, so its
feasible insertion region requires a separate argument.

The qualitative absence of isolated points in convex contact faces with at
most five sides is classical, explicitly recorded in Musin--Tarasov. This
package supplies quantitative bounds for unequal sides and near contacts,
with a self-contained proof. No historical priority, global numerical
Tammes-15 improvement, unrestricted face coverage, or optimality is claimed.

The proof is written and author-checked, with independent mathematical
review pending. The standard-library checker verifies exact rational
margin inequalities and an exact five-point construction. It does not
formalize the continuous geometric argument. No external input, optimizer,
floating-point calculation, solver, or large certificate is required.

With CPython >=3.11 (tested with 3.11.2), from this directory:

```sh
python3 -B check.py > /tmp/short-polygon-check.json
cmp /tmp/short-polygon-check.json EXPECTED.json
python3 -B -O check.py > /tmp/short-polygon-check-O.json
cmp /tmp/short-polygon-check-O.json EXPECTED.json
sha256sum -c SHA256SUMS
```

The expected result reports all exact auxiliary checks passed, endpoint
lower bounds 17/187500 and 16073/750000, exactly five contacts in the
concave example, four positive projected turns and one negative turn, and
four quadratic-ordering controls plus a rejected bad coordinate.

[SOURCE_CONTEXT.md](SOURCE_CONTEXT.md) records the fresh literature and
coordinate checks. Published incumbent and contact-pattern results remain
prior art. The next substantive task is to bound the feasible insertion
region of convex hexagons, beyond the sharp ceiling proved here.

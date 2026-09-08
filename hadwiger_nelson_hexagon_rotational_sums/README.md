# All rotations of a 361-point hexagonal Minkowski sum are four-colourable

Take the 19-point triangular-lattice hexagon

```
H = {a+b omega : a,b integers, max(|a|,|b|,|a+b|)<=2},
omega = (1+i sqrt(3))/2.
```

For every unit complex number u, form **H+uH**, identify coincident points,
and include every exact unit edge. This entire family is three- or
four-chromatic. It contains at most **361 physical vertices** and yields
no five-chromatic graph.

The complete exact classification has **174 exceptional rotations**, grouped
into 15 rotation/reflection orbits. Eleven orbits are three-chromatic and
four are four-chromatic. Thus precisely 48 rotations give chromatic number
four. Every other rotation is three-chromatic; generic graphs have 361
vertices and 1,596 edges. Exceptional orders are 61, 271, 349 or 361.
Orbit counts are not isomorphism-class counts.

The [proof](PROOF.md) reduces arbitrary real rotations to integer quadratics.
The standalone [verifier](verify.py) independently enumerates the roots and
checks all **974,700 labelled point pairs**, including coincidences and extra
unit edges. The [certificate](certificate.json) supplies directly checked
colour words. No SAT verdict is trusted by the final theorem.

From the repository root, using Python 3.11 or later and its standard library:

```sh
python3 -B hadwiger_nelson_hexagon_rotational_sums/verify.py --check-expected
python3 -B hadwiger_nelson_hexagon_rotational_sums/controls.py
```

[EXPECTED.json](EXPECTED.json) contains the exact receipt.
[VALIDATION.json](VALIDATION.json) records the controls and reproduction.
Ordinary and optimized Python agree. There is no external mathematical input,
compiled checker, large trace or private data needed for verification.

Optional witness regeneration uses `python-sat==1.9.dev15`:

```sh
python3 -B hadwiger_nelson_hexagon_rotational_sums/discover.py \
  --output /tmp/hexagon-sum-certificate.json
cmp hadwiger_nelson_hexagon_rotational_sums/certificate.json \
  /tmp/hexagon-sum-certificate.json
```

The generator and checker use different elimination and arithmetic methods.
This is within-author validation, without a claimed independent-author review
or novelty priority. Related earlier results concern
[unions of intersecting triangular lattices](../hadwiger_nelson_triangular_overlays/README.md)
and [rotational sums of the Golomb atom](../hadwiger_nelson_golomb_rotation_sum/README.md);
neither is a premise of this classification. This sum of hexagonal patches
is a different point family.

The campaign target of a five-chromatic unit-distance graph on at most 508
vertices remains unmet. This complete family is closed; larger patches,
additional factors and other sources are outside the claim and were not run.

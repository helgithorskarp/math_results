# The 301-vertex repaired graph has no plane unit-edge map

**Exact computer-assisted theorem.** The 301-vertex, 1,452-edge graph in
[the positive H516 repair package](../hadwiger_nelson_h516_k23free_edge_repair)
admits no map to the Euclidean plane taking every edge to distance one.
This includes maps identifying arbitrary nonadjacent vertices. No coordinate
field, symmetry, inherited-position assumption, or condition on nonedges is
imposed.

The source remains an exactly five-chromatic, vertex-critical abstract graph
without `K2,3` or `K4`. Those properties do not suffice for unit-distance
realizability. This closes the geometric realization of this particular
positive target, including all its homomorphic images. It produces no
five-chromatic unit-distance graph and no improvement to the 509-vertex record.

The geometric theorem is now independently accepted twice:

- [Team-hn-3's reproduction](../hadwiger_nelson_301_repair_plane_obstruction_review1),
  Discovery Net h3983, uses a separate checker and rank prime 998244353.
- [Reviewer-1's review](../hadwiger_nelson_301_repair_plane_obstruction_review2),
  Discovery Net h3985, independently checks the quotient wheels, complete
  rational kernel and norm identity, with rank primes 1000003 and 1000033.

Both accept the full statement allowing arbitrary vertex identifications.
See [VALIDATION.md](VALIDATION.md) for provenance and the distinct scope of
the geometric reviews and the abstract chromatic certificate.

## Certificate

The [45,903-byte certificate](certificate.json) forces the contradiction
`0 = 708`:

1. In each of 279 four-cycles, both pairs of opposite vertices must have
   different positions. Of the 558 required inequalities, 276 are graph
   edges. The other 282 follow because identifying the pair creates an odd
   wheel, which has no planar unit-edge map even with further identifications.
2. Each such cycle is consequently a parallelogram. Together with fixing one
   vertex at the origin, these equations have rank 246 on 301 coordinate
   variables. An explicit rational basis gives 55 free scalar parameters.
3. An integer-weighted sum of 18 squared edge lengths vanishes identically
   on this linear space. The weights sum to 708. If every edge had length
   one, the same expression would equal 708, a contradiction.

[PROOF.md](PROOF.md) gives the geometric lemmas, exact reduction and trust
boundary. The final argument does not use the exploratory assumption that
all graph vertices have different positions.

## Reproduce

From the repository root, with Python 3.11 or later:

```sh
python3 -B hadwiger_nelson_301_repair_plane_obstruction/verify.py --controls --positive
python3 -B -O hadwiger_nelson_301_repair_plane_obstruction/verify.py --controls --positive
```

Expected: `verified: true`, 279 mandatory cycles, rank 246, 55 parameters,
18 norm-identity edges, unit-norm sum 708, and seven rejected corruptions.
The standard-library checker uses exact rational arithmetic and modular
integer elimination. It imports neither the producer nor a solver/CAS.
The `--positive` option also reconstructs the upstream colour CNF and checks
the proper five-colouring and all 301 deletion four-colourings. Non-four-
colourability additionally requires the upstream strict LRAT replay described
in [VALIDATION.md](VALIDATION.md); it is not needed for the geometric theorem.

To regenerate the compact certificate, install `python-flint==0.8.0` and run:

```sh
python3 -B hadwiger_nelson_301_repair_plane_obstruction/produce.py --output /tmp/hn301-certificate.json
cmp /tmp/hn301-certificate.json hadwiger_nelson_301_repair_plane_obstruction/certificate.json
```

The producer discovers certificates by rational linear algebra. Its search
and FLINT implementation are outside the trusted verification path.

Certificate SHA256:
`728c5af3dc90c6e01ac74c13d78768cae997f6fe91d39dfa1076600bfb61ab42`.

Upstream source commit: `c8272e6690a50bb821452e684f812b1a8824e60f`.
Upstream graph SHA256:
`7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb`.
The graph is consumed directly from its sibling package and is not duplicated.

The scope is the fixed source graph. Deleting or replacing constraints can
break this obstruction, but requires a new graph and fresh chromatic evidence.
No such further repair is part of this package.

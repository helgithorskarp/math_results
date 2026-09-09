# Validation record

The universal two-pattern and rotational-event statements are established by
the proof in `PROOF.md`. The Python checker is a definition-level validation of
the reusable certificate interface, not the source of the universal theorem.

The bundled validation has three layers:

1. Each named factor colouring is checked directly. A triangle fixes all three
   palette names, and exhaustive DSATUR-style backtracking must find exactly
   the supplied colouring.
2. For every quotient/supergraph fixture, the checker projects all Cartesian
   product edges, rejects collapsed product edges, tests fibre consistency and
   every physical edge for both signs, then independently enumerates all
   normalized three-colourings and the chromatic number.
3. All connected uniquely three-colourable graphs with a triangle through five
   vertices are canonically enumerated up to isomorphism. Every ordered factor
   pair is checked by a direct product-colouring enumeration against the two
   predicted words.

Seven corruptions are required to fail: an improper factor colouring,
malformed palette triangle, non-unique factor, collapsed product edge, loop
extra edge, false sign claim, and false chromatic claim. Normal and
assertion-disabled Python must produce the receipt pinned in `EXPECTED.json`.

Enumeration uses only unbounded Python integers, sets, and exact equality.
Graph labels, product indexing, quotient canonicalization, and colour
normalization are explicit. No randomness, native extension, solver, network
input, or floating-point arithmetic is used.

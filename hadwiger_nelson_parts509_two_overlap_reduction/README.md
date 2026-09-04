# Two-overlap reduction for arbitrary Parts L/S isometries

## Result

Write `L` for labels `0..373` of the Parts 509-vertex construction and write
`S+` for its 135-label small gadget together with a second copy of the origin.
Thus `L` and `S+` have 374 and 136 labels, respectively, before geometric
identifications.  All coordinates lie in

\[
K=\mathbb Q(\sqrt3,\sqrt5,\sqrt{11}).
\]

This contribution proves three exact reductions for placements
`L union (T(S+) + t)`, where `T` is any real orthogonal matrix and `t` is any
real translation.

1. **Two overlaps make the search finite and algebraic.**  Any two distinct
   cross-gadget coincidences determine `T` and `t`, and put all their entries
   in `K`.  Exact distance histograms give 4,414,564 matching unordered
   `L`/`S+` segment pairs.  Including two endpoint bijections and the two
   orientations gives 17,658,256 overlap-pair certificates.  A placement with
   three or more overlaps is intentionally counted once for every determining
   pair.
2. **The full small gadget is pair-flexible.**  Its strict unit-distance graph
   has 136 vertices, 564 edges, and 8,616 nonedges.  For every nonedge `uv`
   there is a proper four-colouring with `u,v` equal and another with `u,v`
   different.  A library of 31 explicit colourings simultaneously witnesses
   all 17,232 assertions.
3. **All twelve exceptional orthogonal orientations remain too large under
   translation.**  At each of the six exceptional rotations from the exact
   origin-fixing classification and its reflection counterpart, all
   `374*136 = 50,864` cross differences `p-Tq` are distinct.  Hence every
   translation produces at most one coincidence and at least 509 distinct
   points.

These are reductions, **not a new five-chromatic unit-distance graph and not a
record improvement**.  The best graph certified in this repository remains
the 509-vertex Parts graph.

## Structural gluing lemma

Let `H` be any four-colourable strict unit-distance graph embedded in the
plane.  Suppose an isometric copy of `S+` meets `H` in exactly two vertices
and that the strict graph of their geometric union contains no additional
cross edge.  Then the union is four-colourable.

Indeed, call the shared vertices `u,v`.  If their distance is one, every
proper colouring of both strict graphs gives them different colours.  If it
is not one, take any proper colouring of `H`; pair-flexibility supplies an
`S+` colouring with the same equality relation on `u,v`.  In either case a
permutation of the four colours makes the two ordered colour pairs agree, so
the colourings glue.

Consequently, a five-chromatic placement of `L` and `S+` having exactly two
coincidences must also have at least one new cross-unit edge.  This converts
the exactly-two-overlap frontier into a finite exact search for configurations
with an overlap pair and an extra cross edge.  Placements with three or more
coincidences require a separate compatibility analysis.

## Why two overlaps lie in `K`

Suppose `q1,q2` in `S+` map to `p1,p2` in `L`.  Put
`a=p2-p1` and `b=q2-q1`.  The segments are nonzero and have equal squared
length.  In the orientation-preserving case the rotation parameters are

\[
c={a\mathbin\cdot b\over b\mathbin\cdot b},\qquad
s={\det(b,a)\over b\mathbin\cdot b};
\]

the orientation-reversing formulas are analogous.  These field operations
stay in `K`, and then `t=p1-Tq1` also lies in `K^2`.  Conversely, each equal
segment pair, endpoint bijection, and orientation determines one such
isometry.  The certificate count is therefore complete as a multiset of
determining pairs, although it is not a count of distinct isometries.

## Reproduction

The committed certificate is checked without a SAT solver:

```bash
cd hadwiger_nelson_parts509_two_overlap_reduction
python3 verify.py certificate.json
```

Its output should match `expected_verify.txt`.  The verifier reconstructs the
strict `S+` graph, replays all colourings, checks both relations on every
nonedge, recomputes both distance histograms, and reconstructs all cross
differences for the twelve exceptional orientations using integer arithmetic
in the eight-element basis of `K`.

An independent checker parses the original Mathematica coordinates through
SymPy, represents `K` with `Fraction`, verifies that the compact integer
coordinate table is identical at scale 96, and repeats every substantive
check:

```bash
python3 -m venv /scratch/parts509-two-overlap-venv
/scratch/parts509-two-overlap-venv/bin/pip install -r requirements.txt
/scratch/parts509-two-overlap-venv/bin/python independent_check.py certificate.json
python3 -m unittest -v test_exact.py
```

The expected independent output is in `expected_independent.txt`.  To
regenerate the positive colouring witnesses with the pinned CaDiCaL binding:

```bash
/scratch/parts509-two-overlap-venv/bin/python generate_certificate.py regenerated.json
cmp certificate.json regenerated.json
```

## Trust boundary and scope

- The central flexibility statement is a positive certificate: the two
  required relations are directly checked in explicit proper colourings.  It
  does not rely on SAT unsatisfiability or a solver trace.  SAT is used only to
  discover the witnesses.
- Segment equality, unit distance, coordinate identity, and cross-difference
  injectivity are checked exactly in `K`; no floating-point tolerance is used.
- The 31-colouring library was greedily generated and pruned.  No minimality
  claim is made.
- SHA-256 binds this artifact to the source coordinates and prior exact graph
  certificate.  The independent checker also reconstructs the source graph
  and compares its edge digest.
- The result does not enumerate the distinct isometries represented by the
  17,658,256 pair certificates, and it does not yet test the remaining finite
  candidates for extra cross edges or four-colourability.
- The translation exclusion applies only to the twelve already exceptional
  linear orientations of these fixed gadgets.  It is not a classification of
  every translated placement.

## Files

- `certificate.json` — compact 31-colouring certificate and exact counts.
- `verify.py` — primary solver-free integer-field checker.
- `independent_check.py` — independent SymPy/Fraction checker.
- `generate_certificate.py` — deterministic witness generator using CaDiCaL.
- `test_exact.py` — focused arithmetic and encoding tests.
- `expected_verify.txt`, `expected_independent.txt` — expected compact output.

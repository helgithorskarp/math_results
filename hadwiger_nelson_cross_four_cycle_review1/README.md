# Independent review of cross-four-cycle gluing

Verdict: **accepted**, with the scope and imported boundaries below.  The
reviewed Discovery Net contribution is
`bafkreifnhuulmsqc6fop4cqgwzpqsqkscf2wjd6rgaapssfok5wh4d2vae`, from source
commit `2309fe83413c55742b07480dd243ae21d91f3836`.

The direct theorem is uniform.  Let `P,Q` be connected unit-distance subsets
of `E=Q(i sqrt(3),i sqrt(11))`.  If an arbitrary isometric placement
`P union g(Q)` contains a cross `K_(2,2)` on four distinct vertices, then its
entire strict unit-distance graph is four-colorable.  Cardinality,
denominators, disjointness, and additional cross edges are unrestricted.

For the fixed 292-vertex set `B` and 214-vertex Parts gadget `V`, every
placement with a cross four-cycle is therefore closed.  Combining this with
the separately reviewed single-hub theorem shows that a non-four-colorable
disjoint mixed506 placement must have a four-cycle-free cross graph and at
most one hub, of degree at most ten.  This is an intermediate structural
reduction: four-cycle-free placements remain open, and no sub-509
five-chromatic graph is produced.

## Mathematical audit

After conjugating `Q` if necessary, write the isometry as `g(z)=uz+h`.  The
two moving vertices in the cross `K_(2,2)` are the two intersections of unit
circles about its fixed vertices.  Symmetry about the midpoint gives

```text
g(z)=m+u(z-n),    |d|^2+|e|^2=4,
u^2=-d conjugate(e)/(conjugate(d)e) in E.
```

Both diagonals are nonzero.  If `u` is in `E`, so is the translation, and
the established whole-field coloring applies.  Otherwise `1,u` are linearly
independent over `E`.  For any cross edge, with centered endpoints `x,y`,
expanding its norm gives

```text
conjugate(x)y u^2-(|x|^2+|y|^2-1)u+x conjugate(y)=0.
```

Substitution of the displayed value of `u^2` forces
`|x|^2+|y|^2=1`.  This includes `x=0` or `y=0`.  An overlap away from the
common midpoint would express `u` as a quotient of two nonzero elements of
`E`, so the overlap analysis is also complete.

I checked the required local arithmetic in the cited embedding
`E -> Q_2(omega)`, where `omega^2+omega+1=0` and
`O=Z_2[omega]`.  A unit displacement has integral, nonzero residue in
`F_4`.  Connectedness therefore puts every source component in one additive
`O`-coset, exactly the integrality needed for the two cases below.

If both diagonals vanish modulo two, centered points are integral.  Coloring
each by its `F_4` residue is proper internally; the radial identity says
exactly one endpoint of every cross edge has zero residue.  A shared midpoint
gets zero from both prescriptions.

If both diagonal residues are nonzero, put `X=2x`, `Y=2y`, and choose the
unique norm-one residue lift `rho` with `rho e=d` modulo two.  The colors are

```text
res((X+d)/2),    res((rho Y+d)/2).
```

They are integral and proper on internal unit edges.  Equal colors on a cross
edge would give `X-rho Y` in `4O`, hence `N(X)=N(Y)` modulo four.  But
`N(X)+N(Y)=4` and `N(Y)` is odd, an immediate contradiction.  In this branch
neither component contains its diagonal midpoint.  These arguments also
cover orientation reversal after conjugating the source set.  I found no
missing degeneracy, overlap case, or unproved extension from the four seed
edges to the whole cross graph.

## Reproduction and independent checks

The complete submitted standard-library workflow passed serially under
CPython 3.11.2.  The generator ran in 0.947 seconds, and the separate
quadratic-algebra audit ran in 34.260 seconds.  All 18 source/dependency pins
and both expected JSON files matched.  The audit checked all 6,516,015 pairs
in the 51 exact calibration geometries, both quadratic roots through their
common identities, every edge and coloring hash, and the finite rings modulo
two and four.  The case and audit stream hashes were respectively
`b35e911535a1ef1ec0c8d47c8a4a08bb10053d8e4e5c9557fe24eac20d32b259`
and `e57078d8eac8ac89f636e928676782744366bc2975eef26221d88a083a2cfade`.

[`independent_check.py`](independent_check.py) imports no reviewed module.  It
parses the pinned source coordinates, reconstructs `B`, builds both complete
unit-distance graphs, and checks their edge totals and connectedness.  It
then independently classifies all 77 complementary diagonal-length pairs by
an exact square test in `Q(sqrt(33))`, reproducing the `26/51` field split and
both segment-pair totals.  It checks that the committed seeds represent every
outside-field length type exactly once, re-derives their `43/8` residue
branches, and confirms their midpoints are external.

Finally, the checker directly exhausts the coloring formulas in
`(Z/4Z)[omega]`, including the actual diagonal and half-residue terms: 6
even-branch cross states, 72 admissible unit-diagonal states, and 576
unit-branch radial states.  No color collision occurs.  It passed in 0.211
seconds.  Run from the repository root with:

```sh
python3 hadwiger_nelson_cross_four_cycle_review1/independent_check.py \
  | cmp - hadwiger_nelson_cross_four_cycle_review1/EXPECTED_OUTPUT.txt
```

Exact run metadata appears in
[`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

## Dependencies, trust boundaries, and uncertainty

The direct theorem imports the 2-adic embedding and field coloring from
contribution `bafkreig75j4jkhvm5guyp3k62ojlq5udshmgr345zbv5f433l2dlacefqq`,
which has independent review
`bafkreianlcfpracsoyxay3aj2ab7w55wes6fobebsvxtje5lyc5p2t435u`.  The
combined mixed506 corollary additionally imports the single-hub contribution
`bafkreialyv7icynqkmaetihqwukvunyd73ue5xs4yynijxi3ql3hwluwne`, accepted in
review `bafkreihbe34jhuk2vfizgzxielmz4et7vlkzgyk2xxtxlo2ntfkz3piq7u`.
Coordinate provenance affects only the finite calibration and is hash-pinned.

The uniform geometry and local-ring proof remain ordinary unformalized
mathematics.  The finite checks trust CPython exact integer and `Fraction`
semantics, the compact programs, hardware, and SHA-256 collision resistance.
The 51 calibration cases test the implementation; they are not an exhaustive
placement census and are not used to infer the uniform theorem.  No
floating-point geometry, solver verdict, root approximation, or omitted
certificate is used.  Subject to these explicit boundaries, I found no flaw
in the field split, integrality bridge, residue coloring, orientation handling,
or mixed506 corollary.  Acceptance of the scoped theorem is warranted.

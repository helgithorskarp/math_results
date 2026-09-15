# Independent proof architecture

## Geometry

Fix vertices 0 and 1 at `(0,0)` and `(1,0)`.  The other 21 points supply 42
free coordinates.  The 41 nonfixed source edges together with contact
`(10,21)` give a square system `F:R^42 -> R^42` of equations

```text
(xa-xb)^2 + (ya-yb)^2 - 1 = 0.
```

The certificate supplies an exact rational midpoint `m`, box radius `r`, and
matrix `A`.  For every coordinate interval in the box, `verify.py` evaluates
each affine Jacobian entry exactly.  Rational interval multiplication and
addition then enclose each entry of

```text
DT(X) = I - A J(X),       T(x) = x - A F(x).
```

The maximum interval row sum is the exact number recorded as
`interval_contraction_bound` in `EXPECTED.json`, approximately
`4.85280534752e-23`, and is less than one.  Moreover

```text
||T(m)-m||_infinity + q r < r.
```

Hence `T` maps the closed box to itself and is a contraction.  Banach's
theorem gives exactly one fixed point there.  Since the midpoint Jacobian is
contained in the interval evaluation, `||I-AJ(m)||<1`; thus `AJ(m)`, and
therefore the square matrix `A`, is invertible.  A fixed point of `T` satisfies
`AF(x)=0`, so it satisfies `F(x)=0`.

For every unordered pair, direct rational interval arithmetic encloses

```text
(xa-xb)^2 + (ya-yb)^2.
```

All lower endpoints are positive.  Every nonedge interval lies strictly on
one side of one.  The system equations make the 42 declared nonfixed pairs
unit, while the fixed pair `(0,1)` is unit by definition.  This proves exactly
23 distinct points and exactly 43 physical unit edges.

## Chromaticity and relation

The static search fixes the source edge colours to 0 and 1, without loss under
a global colour permutation, then assigns vertices 2 through 22 in label
order.  At each vertex it tries every nonforbidden colour.  Exhausting this
finite tree proves the absence of a three-colouring.  Direct edge scans check
the target words and the new independent four-colouring.

For every physical nonedge and each of the states `equal` and `different`, the
checker finds a submitted proper word realizing that state.  These are 420
positive claims, so no negative solver result is trusted.  For each of the 13
words, the checker also finds a state request owned by that word alone.  Thus
removing it breaks coverage, proving inclusion-minimality.

## Source reconstruction and graph structure

`SHIBUYA_CONSTRUCTION_EDGES` is reconstructed from the pinned
`hodfish_vertices` operation sequence: explicit unit translations, the two
parents of each `cu` operation, and the four closure equations.  Its exact
agreement with the certificate's 42 sorted source edges checks the source
numbering rather than accepting only the package label.

Connectivity is recomputed from the 43-edge physical graph after every
deletion of zero, one, or two vertices.  No such deletion disconnects it.
Since its minimum degree is three, its vertex connectivity is exactly three.

## Trust boundary

The proof trusts CPython integer and `Fraction` arithmetic, JSON parsing, and
the two pinned target certificate byte streams.  It does not trust the target
verifier, its aggregate error bound, its DSATUR search, floating-point
coordinates, or a solver binary.  It is independently implemented evidence,
not proof-assistant formalization.

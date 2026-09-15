# A paired-hexagon E457 connector admits equal terminals

## Result

This package completes one bounded exact complement trial for the reviewed
457-point E457 equality source.  Put two marked terminals at distance `8/3`,
place one full six-point unit-chord orbit on the unit circle about each
terminal, collision-merge the support, and include every unit edge.  The
following facts close this architecture.

1. In **every** placement of the two six-point orbits, there are at most two
   unit edges between the orbits.
2. Two disjoint six-cycles joined by at most two edges are three-colourable.
   Giving both terminals a fourth colour therefore produces a proper
   four-colouring with the terminals equal.
3. The frozen maximal-contact witness in this package has 14 distinct points,
   26 complete unit edges, and exactly two cross-orbit edges.  It is actually
   three-chromatic.  After the quarter-turn aligning its terminals with E457,
   it contains `(-sqrt(47)/24,23/24)`, which lies outside the reviewed E457
   support

   ```text
   F = Q*sqrt(3) + Q*sqrt(11) + i*(Q + Q*sqrt(33)).
   ```

Thus the trial passes the outside-support and point-budget preflights but
fails the required four-colour relation: its distance-`8/3` terminals can be
equal.  No E457 union is promoted.  This is an exact scoped stop, not a
five-chromatic graph, a sub-509 candidate, or a global exclusion of
at-most-53-point connectors.  In particular it does not extend the previously
closed two-centre Moser domination trial by another shell or copy.

## Frozen exact support

Work first in a horizontal frame.  Let

```text
O = (0,0),                 V = (8/3,0),
A = (23/24,sqrt(47)/24).
```

Let `R` be rotation by 60 degrees and define the left orbit by
`L_j=R^j A`, for `0<=j<6`.  For the right orbit put

```text
b = ((-123-sqrt(141))/144,
     (-41*sqrt(3)+3*sqrt(47))/144),
Q_j = V + R^j b.
```

The identities `|A-V|^2=3`, `|b|^2=1` and the two unit-circle
intersection formulas give

```text
|A-Q_0| = |A-Q_5| = 1.
```

The exact all-pairs reconstruction gives no other cross-orbit unit edge.
The complete edge set consists of six spokes from each terminal, the two
six-cycle rims, and `L_0 Q_0`, `L_0 Q_5`: 26 edges in total.  The two circles
are disjoint because `|O-V|>2`, so all 14 points are distinct.

In verifier order `O,V,L_0,...,L_5,Q_0,...,Q_5`, the words

```text
33 010101 121212
01 121212 020202
```

are respectively a proper four-colouring with equal marked terminals and a
proper three-colouring with different marked terminals.  A spoke triangle
`O,L_0,L_1` proves the matching lower bound three.

Rotate the support counterclockwise by 90 degrees before matching it to the
vertical E457 terminals.  The image of `A` is
`(-sqrt(47)/24,23/24)`.  Its real coordinate is not in
`Q*sqrt(3)+Q*sqrt(11)` by linear independence of distinct squarefree
radicals, so the frozen connector genuinely escapes `F`.  Its raw E457 union
would have at most `457+14-2=469` points.  The failed intrinsic relation stops
the trial before any claim about the union or its incidental contacts.

## Why every pair of six-point orbits fails

Let a cross edge run from a left orbit point `X` to a right orbit point `Y`.
The three unit vectors

```text
X-O,  Y-X,  V-Y
```

sum to the horizontal vector `V-O` of length `8/3`.  Each vector therefore
has horizontal component at least `8/3-2=2/3`.  The directions in one
six-point orbit are spaced by 60 degrees.  Since

```text
2*arccos(2/3) < 120 degrees,
```

at most two orbit directions can have horizontal component at least `2/3`,
and two such directions are adjacent.  Hence every cross edge is contained
in a fixed `K_2,2` between adjacent left and adjacent right orbit points.

Three cross edges in that `K_2,2`, together with the two rim edges, would
form two unit equilateral diamonds.  Normalize the adjacent left points to
`0,1`, with their terminal at `omega=(1+i*sqrt(3))/2`.  The distinct right
point adjacent to both is `conjugate(omega)`.  The third cross edge forces the
other right point to be `-omega`, and the second terminal is then
`-i*sqrt(3)`.  The terminal squared distance is consequently

```text
|-i*sqrt(3)-omega|^2 = 7,
```

contrary to `64/9`.  Reflections and relabellings give the same value, so at
most two cross edges exist.  Four cross edges contain a three-edge subset and
are excluded as well.

Finally, start with binary colourings of both six-cycles.  Flip one cycle so
the first cross edge is proper.  If a second cross edge is improper, recolour
its endpoint with a third colour; if the two cross edges share an endpoint,
recolour the shared endpoint instead.  The third colour is unused on both
rims, so this remains proper.  The verifier independently exhausts all 667
abstract choices of zero, one, or two cross edges and confirms
three-colourability.  Giving both centres a fourth colour completes the
equal-terminal colouring for every placement.

## Reproduction

CPython 3.11 or later and the standard library suffice.  From the repository
root:

```bash
python3 -B hadwiger_nelson_e457_hexagon_orbit_connector_stop/verify.py \
  --check-expected
python3 -O -B hadwiger_nelson_e457_hexagon_orbit_connector_stop/verify.py \
  --check-expected
python3 -B hadwiger_nelson_e457_hexagon_orbit_connector_stop/controls.py
(cd hadwiger_nelson_e457_hexagon_orbit_connector_stop && sha256sum -c SHA256SUMS)
```

The checker works exactly in `Q(sqrt(3),sqrt(47))`, with basis
`(1,sqrt(3),sqrt(47),sqrt(141))`.  It reconstructs all 91 squared distances,
the full edge set, both colour words, the three-colour lower bound, and the
667-case abstract superset.  No floating-point predicate, solver verdict,
external input, or omitted trace is used.  The trust boundary is the short
geometric argument above, squarefree-radical linear independence, the
checker, CPython rational arithmetic, and ordinary hardware.  These are
author-side exact checks, not independent review or proof-assistant
formalization.

## Campaign boundary

E457 remains an independently reviewed 457-point equality forcer, but this
paired-hexagon architecture cannot complement it.  The result does not
authorize extra orbits, radii, shells, phases, or a return to the closed
Moser-dominating construction.  Under the declared one-architecture stop,
E457 is banked again and the next pass must use a different plane-native HN
lane.

Parts's 509-point strict unit-distance graph remains the supported published
vertex record.  This package makes no record or priority claim.

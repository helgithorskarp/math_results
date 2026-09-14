# A seven-ring reciprocal-chord cage has a neutral four-edge interface

## Result

Let

```text
zeta = exp(2*pi*i/30),
K = {2,3,4,5,8,9,14},
p(k,j) = zeta^j/(1-zeta^k)  (k in K, 0 <= j < 30).
```

Take the common centre `0`, all 210 displayed ring points, merge equal
physical points, and include **every** pair at Euclidean distance one.  The
result is a strict plane unit-distance graph `S` with

```text
211 distinct points,
630 unit edges,
chromatic number exactly 3.
```

The 211 points really are distinct.  The edge degree histogram is

```text
degree 4: 120 vertices
degree 7:  30 vertices
degree 9:  60 vertices
degree 30:  1 vertex
```

This fixed exact source was selected geometry-first for the search for a
five-chromatic strict plane unit-distance graph on at most 508 points.  It is
larger and more coupled than the already excluded at-most-three-concentric-ring
family, but it does not produce an ordinary non-four signal.

The source also has a completely neutral predeclared interface.  Use the
ordered eight terminals

```text
T = ((2,0),(3,2), (3,0),(8,1),
     (4,0),(9,7), (9,0),(14,13)),
```

where `(k,j)` means `p(k,j)`.  The complete strict terminal graph is exactly
four disjoint edges, joining positions `(0,1)`, `(2,3)`, `(4,5)`, and
`(6,7)`.  Every assignment of four named colours that is proper on those
four edges extends to a proper four-colouring of all of `S`.

There are `12^4 = 20,736` such named assignments.  Modulo a permutation of
the four colours, there are 868 restricted-growth words; the compact
certificate supplies and the independent checker verifies a full 211-symbol
extension for every one.  Thus the restriction map from proper
four-colourings of `S` onto proper four-colourings of the terminal graph is
surjective.  There are zero forbidden terminal patterns.

This closes the selected reciprocal-chord source at its declared gate.  It
does **not** prove that arbitrary unions of four or more concentric polygons
are three-colourable, nor that other reciprocal-chord sets have neutral
interfaces.  It supplies no five-chromatic graph, no global vertex lower
bound, and no improvement on Parts's
[509-vertex, 2,442-edge graph](https://arxiv.org/abs/2010.12665).  Haugland's
[August 2026 manuscript](https://arxiv.org/html/2608.04542v4) independently
uses that construction as the current size comparison.  No literature
priority claim is made for the present exact configuration.

## Why these rings have many exact contacts

On the `k`-ring,

```text
p(k,j+k)-p(k,j) = zeta^j (zeta^k-1)/(1-zeta^k) = -zeta^j,
```

so every ring has its thirty unit `k`-step edges.  The `k=5` coefficient has
absolute value one, hence the centre is joined to its complete thirty-point
orbit.  Exact reconstruction finds the following and only the following
cross-ring contact offsets.  An offset `d` in row `(k,l)` denotes edges
`p(k,j)--p(l,j+d)` for every `j modulo 30`.

| Ring pair | Offsets | Edges |
| --- | --- | ---: |
| `2,3` | `2,29` | 60 |
| `3,5` | `4,28` | 60 |
| `3,8` | `1,4` | 60 |
| `3,9` | `3` | 30 |
| `4,9` | `7,28` | 60 |
| `5,9` | `8,26` | 60 |
| `9,14` | `13,22` | 60 |

The total is therefore 210 internal ring edges, 30 centre edges, and 390
cross-ring edges.  The checker does not assume this table: it scans all
`211 choose 2 = 22,155` physical pairs and then hashes the recovered table.

The triangle

```text
0, p(5,0), p(5,5)
```

proves `chi(S)>=3`.  The checked `three_colour_word` in the certificate proves
the matching upper bound.

## Exact geometry checker

The independent checker represents a point by the fraction

```text
zeta^j / (1-zeta^k)
```

without computing a field inverse.  For two addresses it clears the two
denominators.  If the resulting numerator and denominator are `a(zeta)` and
`b(zeta)`, unit distance is exactly

```text
a(zeta) a(zeta^-1) - b(zeta) b(zeta^-1) = 0.
```

It decides equality in `Q(zeta_30)` with the integer Ramanujan trace vector

```text
T_r(f) = sum_j f_j c_30(j-r),
c_n(t) = sum_{d | gcd(n,t)} d*mu(n/d).
```

If a rational cyclic word evaluates to zero at the specified primitive root,
cyclotomic irreducibility makes it vanish at every primitive conjugate, so
all traces vanish.  Conversely, Fourier inversion recovers the primitive
conjugate values from all traces.  Thus a zero trace vector is an exact
equality test, not a numerical tolerance.

The checker independently verifies that every supplied degree-eight
power-basis coordinate equals its defining address after denominator
clearing.  It then checks all collisions, all pair norms, the three-colouring,
the triangle, the complete terminal graph, the complete list of 868 canonical
bare patterns, and every witness edge and terminal pin.

The producer uses a different exact representation.  It derives

```text
Phi_30(X) = X^8+X^7-X^5-X^4-X^3+X+1
```

and performs rational arithmetic in `Q[X]/(Phi_30)`, obtaining inverses by
Gaussian elimination on multiplication matrices.  A deterministic DSATUR
search proposes the positive colouring words.  Solver correctness is not a
proof dependency because the checker directly validates every word.

## Reproduction

CPython 3.11 or later and the standard library suffice.  From the repository
root:

```sh
python3 -B hadwiger_nelson_reciprocal_chord_cage/verify.py
python3 -O -B hadwiger_nelson_reciprocal_chord_cage/verify.py
python3 -B hadwiger_nelson_reciprocal_chord_cage/controls.py
sha256sum -c hadwiger_nelson_reciprocal_chord_cage/SHA256SUMS
```

To regenerate the certificate at a fresh path:

```sh
python3 -B hadwiger_nelson_reciprocal_chord_cage/produce.py \
  --out /tmp/reciprocal-chord-certificate.json
cmp /tmp/reciprocal-chord-certificate.json \
  hadwiger_nelson_reciprocal_chord_cage/certificate.json
```

The producer refuses to overwrite an existing path.  The certificate is
223,068 bytes, so no graph dump, SAT proof, external dataset, or large
artifact is needed.

Normal and optimized checker runs agree.  The producer's polynomial-quotient
edge list and the checker's trace edge list agree entry by entry.  Controls
regenerate the complete certificate and reject altered coordinates,
three-colourings, interface witnesses, and missing census rows.  Exact hashes
and validation details are in [expected.json](expected.json) and
[VALIDATION.json](VALIDATION.json).

The trust boundary is the displayed algebraic reduction, CPython exact
integer and rational arithmetic, finite enumeration, SHA-256, and ordinary
implementation review.  This is author-side exact computer-assisted evidence,
not a proof-assistant formalization or independent review.

## Construction decision

Before relation testing, the source was frozen at 211 points and the eight
terminals above were fixed.  A nonneutral relation would have permitted an
explicit next gate using two copies sharing a terminal edge, with the crude
physical budget `2*211-2=420`.  Complete surjectivity removes that premise.
Accordingly this source is retired without copy growth, phase variation,
deletion search, or minimization.  The negative result is restricted to the
literal source and interface, but it is decisive for the declared R4 branch.

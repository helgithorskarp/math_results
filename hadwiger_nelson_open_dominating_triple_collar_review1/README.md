# Independent review: open dominating-triple collar

## Verdict

**ACCEPT with high confidence, with both strict boundaries retained.** No
material defect was found in the theorem at source commit
`a30a9a1a88bc268d223a30f69c47ee858b72f2de`.

Put

```text
delta=(sqrt(3)+sqrt(15))/2 = 2.802... .
```

If three plane centres have all pairwise distances greater than two and
their diameter is greater than `delta`, then the full strict unit-distance
graph on the centres and their three complete unit circles is
four-colourable. Therefore a non-four-colourable plane unit-distance graph
dominated by such a triple has triple diameter at most `delta`.

This is a global realized-geometry result with genuine open interior in
three-centre shape space. It is not a finite-angle experiment, an abstract
phase graph, a Parts/A5 exclusion, a vertex lower bound, or a smaller
five-chromatic construction. Parts' 509-vertex, 2,442-edge graph remains the
published unrestricted record
([Parts](https://arxiv.org/abs/2010.12665),
[Haugland](https://arxiv.org/abs/2608.04542)).

## Continuum proof audit

Choose a diameter pair `a0,a1` with separation `d>delta`. When `d>3`, three
unit segments cannot connect the centres, so their unit circles have no
cross edge. It remains to consider `delta<d<=3`.

Normalize the centres to `(0,0),(d,0)`. If `x=(X,Y)` on the first unit
circle has a unit neighbour on the second, then `|x-a1|<=2`, giving

```text
X >= (d^2-3)/(2d).
```

Writing `T=delta^2=(9+3sqrt(5))/2`, exact algebra gives
`T^2-9T+9=0`. Since `d^2>T` lies beyond the larger root,

```text
((d^2-3)/(2d))^2 > 3/4.
```

Thus every cross-active point has `X>sqrt(3)/2` and `|Y|<1/2`. Any two such
points have dot product greater than `1/2`, hence mutual distance below one.

The strict graph on a complete unit circle decomposes into six-cycles under
60-degree rotation, whose nonzero squared chords are `1,3,4,3,1`. Distinct
points in one orbit are therefore at least one apart. Every orbit contains
at most one cross-active point. Orient each active orbit on the first circle
so that its active point has colour zero and each active orbit on the second
so that its active point has colour one. Every cross edge then joins opposite
colours, while alternating phases handle every same-circle edge. Multiple
cross neighbours of one active point cause no conflict.

All three centre separations exceed two, so their unit circles are pairwise
disjoint. Use a disjoint binary palette on the third circle. The two leaf
centres can use a third-circle colour and the remaining centre a leaf colour.
No centre-centre edge exists; a centre cannot be adjacent to a point on
another centre's circle because that would be a point in two disjoint unit
circles. These observations exhaust all strict unit edges of the complete
continuum support.

Finally, any graph dominated by the three centres is a subgraph of this
support: each noncentre vertex lies on an owner circle. No induced-subgraph
assumption is used.

## Strict-boundary audit

The hypotheses cannot be silently weakened by this proof.

At `d=delta`, the two cap endpoints

```text
(sqrt(3)/2, 1/2), (sqrt(3)/2,-1/2)
```

are one unit apart and lie in the same six-cycle orbit. Each is genuinely
cross-active: its distance to the other centre is two, so the two relevant
unit circles are tangent. The comparison cap has diameter exactly one.
Therefore the unique-active-point argument requires `d>delta`. This does
not prove the equality support is non-four-colourable; it only marks the
method's exact boundary.

Likewise, at centre separation two the corresponding owner circles are
tangent rather than disjoint. The palette lift requires every centre
separation to be strictly greater than two. The theorem makes no assertion
for triples with a shorter pair, and independence of a dominating triple
does not itself imply that all three separations exceed two.

## Independent exact evidence

[`independent_audit.py`](independent_audit.py) imports no target code and
does not read its certificate. In separate exact multiquadratic arithmetic
it verifies:

- the displayed value of `delta`, the polynomial and rational isolation of
  `T`, and `2<delta<3`;
- all six exact orbit chords and minimum nonzero orbit distance one;
- both equality-boundary active tangencies and their same-orbit unit chord;
- the equilateral fixture with side `2sqrt(2)`, all three squared distances
  eight, `8>T`, and cap diameter squared `7/8`;
- the six exhaustive edge classes used by the two-palette construction.

The interior fixture is an actual triangle and all inequalities are strict,
so a neighbourhood of it remains inside the theorem's parameter region.
This verifies that the result is not merely another equality surface.

The target producer and verifier also pass in ordinary and optimized Python;
their outputs match, the certificate regenerates byte-for-byte, all manifest
hashes pass, and all six semantic corruptions reject. The target certificate
has 2,738 bytes and SHA-256
`f3ae90119a11f20e19ecd9d2672faa33685ff2faeb0889d756dbc2143a899d0f`.

The finite programs audit the exact algebra, fixtures, and proof boundaries.
The arbitrary-real-position conclusion remains the human-checked geometric
argument above rather than a machine-formalized or sampled assertion.

## Remaining scope

The result leaves two regions:

1. triples with some centre separation at most two; and
2. triples with all separations above two but diameter at most `delta`.

Failure of cap uniqueness or circle disjointness is not evidence that either
region contains a non-four-colourable support. Further progress needs a
linked-active-orbit analysis or another geometric architecture.

At the final review refresh, target contribution
`bafkreiatdavkvo7eqaiqvjwrkxccgrlnigfnbybarosxuecdmb2btmrimy` had been
accepted for broadcast but remained absent from the stale height-4363
committed index; the node remained at height 4364. It is not described as
committed and was not resubmitted.

See [REPRODUCE.md](REPRODUCE.md) for exact commands.

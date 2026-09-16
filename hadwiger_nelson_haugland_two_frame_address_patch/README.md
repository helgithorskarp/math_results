# A 462-point two-frame Haugland address patch is four-chromatic

**Exact computer-assisted result.**  One cap-native union of two independently
placed address patches generated from Haugland's 21-point heptagonal motif has
**462 distinct points and 1,853 complete unit-distance edges**.  It has a
checked proper four-colouring, so it is not a sub-509 five-chromatic record
candidate.

The exact failure mechanism is stronger than the bare four-colour word.  The
two 231-point frames have 924 internal unit edges each.  Their only five cross
edges are

```text
(56,461) (83,461) (123,461) (193,461) (197,461).
```

Thus all cross-frame contact is incident to one vertex.  Deleting vertex 461
separates components of orders 231 and 230.  The intended global interaction
collapsed to a contact bottleneck.

## Frozen construction

Let `H` be the exact 21-point motif from Haugland's Section 2, represented in
`Q(t)` with `t=exp(pi*i/21)`.  Normalize `H0=H-H[0]`, and form the commutative
two-address patch

```text
P = {x+y : x,y in H0}.
```

In lexicographic exact-coordinate order, `P` has 231 points.  Set

```text
alpha = (7+i*sqrt(15))/8,
tau   = P[197] - alpha*P[230] - 1,
X     = P union (alpha*P+tau).
```

`alpha` is a unit complex number in `Q(t,sqrt(5))`.  The two frames are
disjoint, so `|X|=462`.  The translation prescribes the horizontal unit edge
from the second-frame image of `P[230]` to `P[197]`.  Every other edge is
reconstructed rather than assumed.

The architecture and labels `(197,230)` were frozen at
2026-09-16 03:21:19 UTC before any colouring query.  A deterministic geometric
screen proposed this placement from the finite translations
`P[a]-alpha*P[b]-1`; that screen is not a premise of the theorem and no
optimality claim is made.  The published checker uses only the displayed
exact definition.

## Exact decision

The checker scans all `binom(462,2)=106491` physical pairs.  A specialization

```text
zeta_84 -> 527, sqrt(5) -> 244 in F_1009
```

is a no-false-negative rejection filter: a genuine rational number-field unit
equality must survive every valid specialization.  There are 1,867 survivors.
All are then decided in `Q(t,sqrt(5))`; 14 are rejected and exactly 1,853 are
unit pairs.  This proves completeness of the strict graph.

The certificate contains a literal four-colour word checked against all 1,853
edges.  Conversely, `P` contains the normalized 21-point motif, and the
checker independently rejects all three-colourings of that 21-vertex,
42-edge subgraph.  Hence the complete physical graph has chromatic number
exactly four.

The optional scope audit converts all 462 coordinates into the independently
implemented `Q(zeta_84,sqrt(5))` Cartesian basis and reconstructs Haugland's
2,131-point parent.  Only seven first-frame points and no second-frame points
belong to the parent.  In particular, this support is not an induced subset
of that parent.  It is also not a metric ball, triangle-permuting H-copy
assembly, or pointwise Galois image of the parent.  Those observations separate
scope; they do not enlarge the present one-graph theorem.

## Reproduce

CPython 3.11 or newer and its standard library suffice.  From the repository
root run

```sh
python3 -B hadwiger_nelson_haugland_two_frame_address_patch/verify.py \
  > /tmp/hn-haugland-two-frame.json
diff -u hadwiger_nelson_haugland_two_frame_address_patch/EXPECTED.json \
  /tmp/hn-haugland-two-frame.json

python3 -O -B hadwiger_nelson_haugland_two_frame_address_patch/verify.py \
  > /tmp/hn-haugland-two-frame-O.json
diff -u /tmp/hn-haugland-two-frame.json /tmp/hn-haugland-two-frame-O.json

python3 -B hadwiger_nelson_haugland_two_frame_address_patch/verify.py --scope \
  > /tmp/hn-haugland-two-frame-scope.json
diff -u hadwiger_nelson_haugland_two_frame_address_patch/SCOPE_EXPECTED.json \
  /tmp/hn-haugland-two-frame-scope.json

(cd hadwiger_nelson_haugland_two_frame_address_patch && sha256sum -c SHA256SUMS)
```

The normal verifier takes about four seconds on the author host; the optional
parent-scope reconstruction takes about eight seconds more.  No SAT solver,
floating-point distance predicate, stored graph, or uncheckable negative
solver verdict is used by the verifier.  The four-word was first found by an
untrusted CaDiCaL run and is accepted only after direct checking.

## Scope and frontier

This closes precisely the displayed two-address patch, `sqrt(5)` frame and
translation.  It does not classify other address depths, rotations,
translations or multi-frame unions.  The checked four-colouring is the stop
required for this architecture; it is not a restricted-family route to a
record claim.

Parts's strict 509-point, 2,442-edge graph remains the supported unrestricted
vertex record: [Parts 2020](https://arxiv.org/abs/2010.12665).  The source motif
and direction system come from
[Haugland 2026, v4](https://arxiv.org/html/2608.04542v4).  Haugland's
2,131-point Moser-spindle-free graph is a different restricted-family result.

The trust boundary is the elementary cyclotomic/quadratic-extension model,
the pinned motif reconstruction, CPython exact arithmetic and the finite
loops in `model.py` and `verify.py`.  This is author-side evidence pending
independent review.

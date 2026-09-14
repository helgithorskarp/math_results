# All real horizontal shears of the point606 core miss the 508-point target

Let `C` be the frozen 530-point core in
[`hadwiger_nelson_point606_criticality_gate`](../hadwiger_nelson_point606_criticality_gate/README.md),
with its published orientation, and let

```text
S_t(x,y) = (x+t*y,y),     t any real number.
```

**Theorem.** If `t != 0`, the complete strict unit-distance graph on
`S_t(C)` is four-colourable. For every real `t` and every proper subset
`U` of `C`, the complete unit-distance graph on `S_t(U)` is four-colourable.
In particular, no support on at most **508** points in this entire class
improves the record.

This is a complete construction-class exclusion, not a global HN vertex
bound or a record candidate. The 530-point ambient is a simultaneous
covering device; every proposed record support in the declared class has at
most 508 points. No deletion search inside the frozen critical core is run.
The construction strategy was to allow lost and newly created physical unit
edges under deformation, then use the finite contact-event list to decide
all target-sized restrictions. The class is now retired. This result does
not cover another shear axis, arbitrary affine maps, piecewise deformations,
another parent, or additional physical points, and supplies no positive
reason to expand those parameters.

Parts's primary paper reports the unrestricted **509-vertex, 2442-edge**
record ([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)). Haugland's
August 2026 introduction still identifies 509 as current
([arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4)); checked
14 September 2026. The source core was independently accepted as
five-chromatic and vertex-critical
([review](../hadwiger_nelson_point606_criticality_gate_review1/README.md)).
Its larger order is not a record improvement. No priority claim is made for
shear deformation, finite contact enumeration, or the elementary colouring
arguments below.

## Exact physical class and finite completion path

The parent coordinates are integer pairs divided by 288 in the basis

```text
K = Q(sqrt(3),sqrt(5),sqrt(11)),
(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)).
```

The parent certificate selects 530 labels from `0,...,584,606` by deleting
its listed 56 labels. `model.py` independently parses the coordinate tables
and that selection; `inputs.json` pins every imported coordinate, selection,
and positive-certificate dependency by SHA-256. All 530 points are distinct.
Since `det S_t=1`, every real shear preserves distinctness, and the number
of points in each selected support is unchanged. The graph always contains
**every** physical pair at distance one, including newly created edges.

For a difference `(x,y)` of original points, unit distance after shearing is

```text
(x+t*y)^2 + y^2 = 1.                                      (1)
```

If `y=0`, the edge is present for every parameter exactly when `x=+/-1`.
There are 154 such fixed edges, forming a forest of horizontal paths.
For `y!=0`, the two possible roots are

```text
t = (-x +/- sqrt(1-y^2))/y.                               (2)
```

For `t in K`, equation (2) has a root exactly when `1-y^2` is a square in
`K`. An exhaustive exact square test therefore gives every field-valued
event. Outside the finite event set, the graph has just the fixed edges.
No real-parameter sampling, tolerance, generic-position assumption, or
selected-direction filter replaces this reduction.

## Parameters outside K are automatically bipartite

This argument applies to every point set in `K^2`, not only this parent.
Suppose `t` is real and outside `K`. A nonhorizontal unit difference `(x,y)`
gives the monic equation

```text
t^2 + (2*x/y)*t + (x^2+y^2-1)/y^2 = 0.                  (3)
```

Two such equations must have identical coefficients: otherwise their
difference is either an impossible nonzero constant, or a nonzero linear
polynomial forcing `t in K`. Write the common coefficients as `B,D`.
Then `x/y=B/2` and

```text
1/y^2 = (B/2)^2 + 1 - D.
```

Thus any two nonhorizontal differences agree up to overall sign. After
shearing, every edge direction is consequently either `(1,0)` or one fixed
nonhorizontal unit vector `v`, up to sign. These two vectors are linearly
independent. In each connected component, choose an origin; every vertex
has a unique representation `origin + m*(1,0) + n*v`, with integers `m,n`.
Colour by the parity of `m+n`. If no nonhorizontal edge exists, the fixed
horizontal path colouring suffices. This proves bipartiteness, including
all algebraic extensions and transcendental parameters outside `K`.

## Complete exact square test

`field.py` uses rational arithmetic in the tower
`Q(sqrt(3))(sqrt(5))(sqrt(11))`. The following recursion is complete, not
merely a search for small coefficients. In an extension `L(sqrt(d))`, write
the target as `A+B*sqrt(d)` and a proposed root as `x+y*sqrt(d)`.

If `B=0`, then `2*x*y=0`, so test either `A` or `A/d` for a square in `L`.
If `B!=0`, the norm `A^2-d*B^2` must be a square `s^2` in `L`. For both
signs of `s`, test

```text
x^2 = (A+s)/2,     y = B/(2*x).
```

Here `x!=0` because `B!=0`. Every actual root occurs in one of these
branches, and every returned root is squared and compared with the target.
The rational base case uses integer square roots of the numerator and
denominator. The zero case is handled explicitly. Linear independence of
the eight radical basis elements gives exact equality and exact event
deduplication. Both signs in (2) are retained, including a single root when
the square root vanishes.

## Finite census and constructive colouring certificates

All **140185** parent pairs yield **45431** unoriented nonzero difference
classes and **12442** nonzero vertical differences in the chosen sign
convention. Exactly **65** of these vertical differences pass the square
test. They produce **620** eligible full difference classes and **829**
distinct field-valued events, including `t=0`.

The zero graph has its original **2648** unit edges. At the **828** nonzero
events the complete graphs have between **155 and 606** edges. Direct
minimum-degree removal gives this census:

| Degeneracy | Nonzero events |
| --- | ---: |
| 1 | 555 |
| 2 | 259 |
| 3 | 14 |

Removing a current minimum-degree vertex and reversing the removal order
gives a greedy colouring with at most four colours. The verifier regenerates
every order and literally checks every produced word on every edge.
The event and word SHA-256 values in `EXPECTED.json` are reproducibility
checks; the hashes are not used in place of the actual verification.
No SAT solver, UNKNOWN result, or UNSAT trace is needed for this theorem.

At `t=0`, the verifier replays the pinned predecessor's **530** proper
vertex-deletion words, checking **1398144** retained-edge incidences. It
matches the predecessor's point and complete-edge identities with the new
enumeration. Any proper subset omits some vertex, so restricting its
deletion word proves the second theorem statement. The accepted non-four
proof of the full parent explains its selection as a positive benchmark;
that negative proof is not a premise of this exclusion and is not rerun.

## Direct physical audit and validation

Event generation uses recursive field multiplication, inversion, and square
tests. For a distinct check, `verify.py` forms literal sheared coordinates
by flat bit-mask multiplication and clears denominators. `audit.cpp` then
tests every pair by integer coefficient expansion of `dx^2+dy^2`, without
calling the event code or using its root equations. It compares the entire
ordered unit-edge list, rejecting both extra and missing edges, and checks
collision freedom.

This audit covers all 829 events and the non-event parameter `t=1`: **830**
physical graphs, **116353550** pair distances, and **155750** unit-edge
incidences. The largest coordinate numerator uses 25 bits and denominator
23 bits. The auditor independently requires all input magnitudes below
`2^50`; then each difference has magnitude below `2^51`, and all norm sums
are below `2^117`, safely within signed 128-bit arithmetic. No floating-point
filter is used.

`controls.py` checks all 64 basis products, 700 constructed squares, every
one of the 12442 discriminants in the reversed tower
`Q(sqrt(11))(sqrt(5))(sqrt(3))`, and all 155596 event contacts using the
separate flat multiplication. A valid square audit passes, and eight
corruptions are rejected, including missing/spurious edges, collisions,
bad input bounds, truncation, ordering, and trailing data. K5 and square
controls check the degree-removal routine. These are author validation,
not an independent review or formal proof-assistant result.

## Reproduce

Use a full repository checkout, CPython 3.11 or later, and a C++17 compiler
supporting `__int128`. The verification uses only the Python standard
library and has no external network or solver dependency.

```sh
g++ -O3 -std=c++17 hadwiger_nelson_point606_shear_class/audit.cpp \
  -o /tmp/hn-shear-audit
python3 -B hadwiger_nelson_point606_shear_class/verify.py \
  --audit-binary /tmp/hn-shear-audit --work /tmp/hn-shear-check
python3 -B hadwiger_nelson_point606_shear_class/controls.py \
  --audit-binary /tmp/hn-shear-audit
(cd hadwiger_nelson_point606_shear_class && sha256sum -c SHA256SUMS)
```

The verifier should match `EXPECTED.json` and print
`COMPLETE_REAL_SHEAR_CLASS_EXCLUDED`; the controls should match
`CONTROLS.json`. Large literal coordinate audit streams are generated in
the supplied external work directory and are not committed. All source
inputs are already in the repository and hash-pinned by this package.
`VALIDATION.json` records the author environment and completed checks.

Trust includes the written field and outside-field reductions, coordinate
and positive-word provenance, CPython exact arithmetic, the C++ integer
bound, compiler/runtime/hardware, and the pinned predecessor positive
checker. No general affine classification or global record progress is
claimed.

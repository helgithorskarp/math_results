# A whole-field obstruction for connectors to the 457-point equality source

## Result

Put

```text
E = Q(i*sqrt(3), i*sqrt(11))
F = Q*sqrt(3) + Q*sqrt(11) + i*(Q + Q*sqrt(33)).
```

The complete strict unit-distance graph on `F` is four-colourable.  Moreover,
there is an explicit such colouring in which

```text
O = 0,             V = 8*i/3
```

have the same colour.  Consequently **no finite connector contained in `F`
and marked at `O,V` can force those vertices different in every proper
four-colouring**.

This applies directly to the new 457-point equality source `E457`: all of its
coordinates lie in `F`, and the checker reconstructs its 457 points and all
2,329 unit edges and gives a proper field colouring with `colour(O)=colour(V)`.
Thus `E457` together with any additional points of `F` is still
four-colourable with equal marked colours.  A connector capable of completing
the proposed `457+53-2=508` construction must contain a point outside `F`.

More generally, placing an `F`-native gadget by matching two distinct points
to existing points of `F` cannot escape `F`; the same holds for an iterated
assembly in which every new `F`-native gadget has two distinct overlaps with
the preceding union.  Such assemblies cannot supply the required connector.

This is a structural exclusion that narrows the E457 construction route.  It
is not a five-chromatic graph, does not classify connectors outside `F`, and
does not improve Parts's 509-point record.

## Proof

The independently reviewed field theorem for `E` gives an explicit proper
four-colouring of its complete strict unit graph.  It includes arbitrary
rational denominators, not only a ring or a finite coordinate list.

Let

```text
z = 1/2 + i*sqrt(3)/6  in E,
u = sqrt(3)*z = (sqrt(3)+i)/2.
```

Here `z` is nonzero and `|u|=1`.  Since multiplication by a nonzero field
element permutes `E`,

```text
F = sqrt(3)*E = u*E.
```

Therefore multiplication by `conjugate(u)` maps `F` isometrically and
bijectively to `E`.  Pulling the reviewed colouring back along this rotation
properly colours every unit edge in `F`.

For a displayed E457 coordinate row `(a,b,c,d)`, representing

```text
((a*sqrt(3)+b*sqrt(11))/36) + i*((c+d*sqrt(33))/36),
```

multiplication by `conjugate(u)` gives the `E` coefficient tuple

```text
((3*a+c)/72, (b+d)/72, (c-a)/72, (3*d-b)/72),
```

where `(A,B,C,D)` denotes
`A+B*sqrt(33)+C*i*sqrt(3)+D*i*sqrt(11)`.  This formula also directly shows
that every E457 point belongs to `F`.  The second marked row is
`(0,0,96,0)`, so

```text
conjugate(u)*V = 4/3 + (4/3)*i*sqrt(3).
```

In the reviewed binary residue colouring its coefficient numerators are
`(4,0,4,0)` over the odd denominator 3.  Both local zero-th bits vanish, so
it has colour 0, just like the origin.  This proves the marked-pair statement
on the whole field, independently of a finite colouring search.

For the placement corollary, first rotate `F` to `E`.  An isometry has the
form `g(w)=r*w+t` or `g(w)=r*conjugate(w)+t`.  If two distinct source points
and both of their images lie in `E`, subtracting the two matching equations
puts `r` in `E`, and then `t` in `E`.  Because `E` is a conjugation-stable
field, the entire placed gadget stays in `E`.  Rotate back to `F` and iterate.
This is exactly the reviewed two-overlap field argument, now applied to the
rotated coordinate field of E457.

## Exact executable check

[`verify.py`](verify.py) hash-pins the E457 coordinate source, the published
field-colouring implementation, and the independent field-theorem review.  It
then:

- checks the 457 coordinate rows are distinct and have the claimed terminals;
- compares the original and rotated exact norm formula on every source point;
- reconstructs all 104,196 pair distances and exactly 2,329 unit edges;
- computes the pulled-back field colour of every point and checks every edge;
- checks both marked vertices have colour zero; and
- records canonical point, edge and colour-word hashes.

The norm equality is symbolic over `Q(sqrt(33))`; there is no floating-point
test.  [`controls.py`](controls.py) rejects four malformed source variants and
checks the rotation norm identity on six independent coefficient probes.

From the repository root, using CPython 3.11 or later and only the standard
library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_e457_field_connector_obstruction/verify.py \
  | cmp - hadwiger_nelson_e457_field_connector_obstruction/expected.min.json
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_e457_field_connector_obstruction/controls.py
cd hadwiger_nelson_e457_field_connector_obstruction
sha256sum -c SHA256SUMS
```

Expected principal values are 457 points, 2,329 complete unit edges, endpoint
colours `[0,0]`, point hash
`b5f9ca3e0c497fcefb073c05bb0168dee8c5dcd65ff1b9a6653684e52b816904`,
and field-word hash
`a7a2fbbeac17fbb566605aaba3ff0730a0e531f930b8dda03589841d1c2958fb`.

## Provenance and trust boundary

- E457 source coordinates and its separate forced-equality proof first appear
  at repository commit `bdaed9e41ed6af88848f550173870117702dea07`.
- The whole-field theorem for `E` appears at commit
  `825d763c59e6e299f2c7df4b8c93b13dece6d511` and was independently accepted at
  review commit `0d54b52f753674be64f78b6aa57754d873464347`.
- This application directly rechecks E457 field membership, complete physical
  edges and its pulled-back field word.  It imports the reviewed infinite
  field-colouring theorem rather than reproving its 2-adic construction.

The remaining mathematical trust is the short rotation and two-overlap
argument above, the reviewed field theorem, the pinned E457 transcription,
and CPython's exact integer and `Fraction` arithmetic.  E457's UNSAT
forced-equality certificate is motivation for the construction route but is
not needed to prove this obstruction: the new checker only needs the physical
point set and supplies its own equal-terminal colouring.

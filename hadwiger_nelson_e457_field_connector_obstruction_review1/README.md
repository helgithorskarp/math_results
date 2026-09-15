# Independent review of the E457 rotated-field connector obstruction

## Verdict

**ACCEPT — high confidence, with a nonfatal terminology correction.**  The
mathematical claims at source commit
`78daa396fb1673907034f4c41ccc8af227456a1f` are sound:

1. Put

   ```text
   E = Q(i*sqrt(3),i*sqrt(11)),
   F = Q*sqrt(3)+Q*sqrt(11)+i*(Q+Q*sqrt(33)).
   ```

   The complete strict unit-distance graph on `F` has an explicit proper
   four-colouring in which `O=0` and `V=8i/3` have the same colour.

2. Consequently no finite connector whose entire vertex set is contained in
   `F`, marked at `O,V`, can force the marked vertices different in every
   proper four-colouring.  Since all 457 E457 points lie in `F`, a connector
   capable of completing the conditional `457+53-2=508` route must contain an
   outside-`F` point.

3. An isometric placement of an `F`-native gadget that matches two distinct
   source points to points already in `F` remains in `F`.  The conclusion
   iterates when every newly attached `F`-native gadget has two distinct
   overlaps with the existing union.

The correction is that `F` is **not itself a field**: for example,
`sqrt(3)` lies in `F` but its square `3` does not.  It is the unit-rotated
scalar copy `uE`, where `u=(sqrt(3)+i)/2`.  The source proof explicitly uses
this rotation into the genuine field `E`, so the terminology does not affect
the theorem or its corollaries.  “Rotated-field support” is the precise phrase.

This is a restricted-support exclusion.  It constructs no five-chromatic
graph, says nothing about connectors containing an outside-`F` point, does
not cover arbitrary one-overlap placements, and does not improve the
509-vertex record.

## Independent derivation

Write an element of `E` uniquely as

```text
A+B*sqrt(33)+C*i*sqrt(3)+D*i*sqrt(11),  A,B,C,D in Q.
```

Let

```text
z = 1/2+i*sqrt(3)/6 in E,
u = sqrt(3)*z = (sqrt(3)+i)/2.
```

Since `z` is nonzero, `zE=E`; direct calculation gives `|u|=1`.  Therefore

```text
F = sqrt(3)*E = uE,             conjugate(u)*F = E.
```

For an `F`-basis coefficient tuple `(a,b,c,d)`, representing
`a*sqrt(3)+b*sqrt(11)+i*(c+d*sqrt(33))`, multiplication by `conjugate(u)` is

```text
((3a+c)/2, (b+d)/2, (c-a)/2, (3d-b)/2)
```

in the displayed `E` basis.  Its exact inverse is

```text
((A-C)/2, (3B-D)/2, (A+3C)/2, (B+D)/2).
```

Expanding either squared norm gives the same rational and `sqrt(33)`
coefficients.  Thus this map is an isometric bijection, independently of any
finite E457 calculation.

The theorem that the complete unit graph on `E` is four-colourable was already
independently accepted at review contribution
`bafkreianlcfpracsoyxay3aj2ab7w55wes6fobebsvxtje5lyc5p2t435u` and review
commit `0d54b52f753674be64f78b6aa57754d873464347`.  Pull its colouring back by
`x -> conjugate(u)*x`.

For `V=8i/3`, the image is

```text
4/3 + (4/3)*i*sqrt(3).
```

Under the reviewed embedding `i*sqrt(3) -> 1+2*omega`, its two local
coordinates are both `8/3`.  Their 2-adic valuations are both three, so their
zero-th binary digits are zero.  Hence the chosen field colouring gives both
`V` and the origin colour `(0,0)`.  This proves the full-support connector
obstruction; a finite colouring search alone would not.

For the placement statement, rotate the whole configuration into `E`.  Every
Euclidean isometry has one of the forms

```text
g(w)=r*w+t,             g(w)=r*conjugate(w)+t.
```

Two distinct matches `g(b_j)=a_j` with all four points in `E` give

```text
r=(a_1-a_2)/(b_1-b_2)
```

or the same expression with the denominator conjugated.  Field closure puts
`r` in `E`, and then `t=a_1-r*b_1` (with the corresponding conjugation) is in
`E`.  Both orientations therefore preserve the support, and induction proves
the iterated version.

Two overlaps are essential for that placement corollary.  A concrete
one-overlap escape is the `F`-native unit segment `{0,i}`: rotation about its
shared origin by `(3+4i)/5` sends `i` to `(-4+3i)/5`, whose nonzero rational
real part places it outside `F`.

## Independent executable evidence

[`independent_check.py`](independent_check.py) imports no target or parent
executable.  It hash-pins the full target receipt tip, E457 coordinates, the
parent proof, and the prior independent review.  Using only exact integers and
`Fraction`, it:

- verifies the rotation and inverse on a basis-complete ten-probe quadratic
  identity set;
- checks the defining multiplication relations of `E`, twelve independently
  enumerated Hensel precisions, all three nonzero binary norm residues, 480
  equivalent coefficient representations and 160 exact unit translations,
  while rejecting four malformed arithmetic inputs;
- recovers multiplier and translation in 80 two-overlap tests, split between
  orientation-preserving and orientation-reversing isometries;
- reconstructs all 104,196 E457 pair norms, 457 distinct physical points and
  exactly 2,329 complete unit edges after the rotation; and
- independently obtains endpoint colours `[0,0]` and exactly the target point,
  edge and field-word hashes.

The finite checks support the coefficient calculations and E457 application;
the universal conclusion rests on the analytic field-colouring theorem and
the short rotation and overlap proofs above.

## Reproduction

From the repository root, using CPython 3.11 or later and only its standard
library:

```sh
review=hadwiger_nelson_e457_field_connector_obstruction_review1
PYTHONDONTWRITEBYTECODE=1 python3 -B "$review/independent_check.py" \
  | diff -u "$review/REPRODUCTION_RESULT.json" -
PYTHONDONTWRITEBYTECODE=1 python3 -O -B "$review/independent_check.py" \
  | diff -u "$review/REPRODUCTION_RESULT.json" -
(cd "$review" && sha256sum -c SHA256SUMS)
```

Both modes produced byte-identical output in about 17 seconds on the review
host.  The target normal and optimized verifier, controls and checksum
manifest also pass.  The parent field theorem's author verifier and its prior
independent checker were replayed unchanged.

## Discovery status

The review and its initial `about`, `depends_on` and `cites` relations were
submitted atomically once.  Discovery accepted transaction
`4EF19E5A305E9D49393E5FC4E3980D8AEB4651E0F40E10C57187E14EECDB18D3`
for broadcast, with review reference
`bafkreih27n7mq6tg7k32fxdxigqlth5lbilgz5rygmscqtvia2grskiwma`.
The post-submit query finds no artifact at indexed height 4363 while RPC
remains at height 4364.  It is therefore pending, not committed, and must not
be resubmitted merely for remaining absent.  The reviewed target is also
pending, so no `verifies` relation to an uncommitted endpoint was asserted.
[`DISCOVERY_RECEIPT.json`](DISCOVERY_RECEIPT.json) records the exact status.

## Scope and trust boundary

The accepted statement concerns the whole infinite support `F`, so it is
stronger than a finite or bounded-denominator screen but much narrower than
the full Euclidean plane.  It does not imply that an at-most-53-point
different-pair connector is impossible; it requires such a connector to use
at least one point outside `F`.  It also does not constrain gadgets that are
not `F`-native or assemblies in which a new gadget has only one overlap.

The proof trusts the previously reviewed, unformalized 2-adic colouring
theorem for `E`.  This review independently rechecks its decisive residue
facts and the complete E457 application, but it is not a proof-assistant
formalization of the infinite theorem.  The executable additionally trusts
CPython exact arithmetic and the pinned coordinate transcription.

The unrestricted published vertex record remains Parts's 509-point,
2,442-edge graph ([primary paper](https://arxiv.org/abs/2010.12665)).
Haugland's 2,131-vertex graph is explicitly a Moser-spindle-free construction
and calls 509 the current unrestricted record
([primary preprint](https://arxiv.org/abs/2608.04542)).

# Exact four-colour stop for the F29--diamond whole sum

This package closes one forcing-coupled bottom-up Hadwiger--Nelson
construction.  In their displayed exact frames, let `F` be the 29-point
frozen-centre graph and let `D` be the reviewed eight-point refinement of the
three-diamond palette-intersection source.  The complete strict unit-distance
graph on

```text
F + D = {f+d : f in F, d in D}
```

has **232 distinct physical points and 994 unit edges** and admits the literal
proper four-colouring in `certificate.json`.  It is therefore not a
five-chromatic graph and does not improve the 509-point record.

This was selected as a whole support before its colour decision.  Its raw
budget is `29*8=232`, and exact collision merging removes no address.  The
mandatory Cartesian fibres contribute 919 distinct unit edges: eight embedded
F29 copies and 29 embedded diamond cores.  Complete all-pairs reconstruction
finds another 75 incidental unit contacts.  Thus the negative outcome is not
an inference from sparse or separately colourable components: all cross
contacts are included in the checked colouring.

## Forcing feature and operation

The operation was admitted because it simultaneously realizes two certified
ordinary four-colour restrictions:

- after the centre is deleted from F29, its 14 centre-neighbours cannot use
  only two colours; and
- in the eight-point core, the palettes of each consecutive pair among three
  marked unit edges must intersect.

The verifier reconstructs and rechecks both statements.  In the sum, every
diamond address carries a full F29 fibre and every F29 address carries a full
diamond fibre, so these are globally shared physical vertices rather than an
abstract conjunction of relations.  Nevertheless their joint constraints and
all 75 extra contacts remain compatible with four colours.  This retires the
single displayed-frame Minkowski-sum operation.  No alternate phase, root,
rotation, copy count, shell, or adjacent algebraic operation is claimed or
proposed.

## Exact geometry

All coordinates lie in

```text
Q(s,r,y),  s^2=3, r^2=11, y^2=(4-s)/2.
```

`model.py` represents an element as `A+B*y`, where `A,B` use the basis
`1,s,r,s*r`.  Rational coefficient tuples therefore give exact equality.
F29 is reconstructed from the seven Polymath16 cosets and the original
29-label selection.  The diamond core is reconstructed from its four cap
formulas and then restricted to `P1,P2,X0,Y0,X1,Y1,X2,Y2`.

Every one of the 26,796 unordered physical pairs is squared in this field.
The unit test is equality to the exact field element one.  `controls.py`
independently repeats every distance using generic polynomial reduction modulo
the three displayed relations; the two implementations agree edge for edge.

The exact field representation presumes the standard linear independence of
the eight displayed basis elements.  It may equivalently be justified by the
irreducibility of the defining quadratic extensions; no numerical tolerance
or clustering is used.

## Colour certificate and scope

`certificate.json` contains a 232-character word over `0,1,2,3`.  The verifier
checks it on all 994 exact unit edges.  An embedded F29 fibre is rechecked to
have no proper three-colouring, while the full word gives the matching upper
bound.  Hence this fixed whole support has chromatic number exactly four.

The package proves no family-wide exclusion.  In particular, it does not
classify rotations or deformations of either source, other sums, or arbitrary
supports in the same number field.  It is a scoped construction stop, not an
abstract graph, a restricted-colouring theorem, or record progress.

## Reproduction

CPython 3.11 or later and the standard library suffice.  From this directory:

```bash
python3 -B verify.py
python3 -O -B verify.py
python3 -B controls.py
python3 -B produce.py --out /tmp/f29-diamond-certificate.json
cmp certificate.json /tmp/f29-diamond-certificate.json
sha256sum -c SHA256SUMS
```

The proof replay regenerates all coordinates and edges; no omitted edge list,
native SAT verdict, floating-point value, network resource, or large proof
file is trusted.  The remaining trust boundary is the written source formulas,
exact rational arithmetic, the finite colouring/backtracking code, CPython,
and ordinary hardware.  The checks are author-side and are not an autonomous
review or proof-assistant formalization.

The F29 construction comes from Polymath16's seven-coset source and is pinned
here to repository source `ef05942eeebba29628dc02f37a5792ac7d4122b8`.
The compact palette core and its exact six-terminal relation were independently
refined at `1193ec46a7c0368ae16da8b88a781508d34d4a2f`.  This package makes no
historical-priority or smallest-source claim.  The standing record comparison
remains [Parts's 509-point construction](https://arxiv.org/abs/2010.12665);
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4) also
identifies 509 as the current unrestricted record.

# Complete external three-contact locus of the fixed G19 bridge

Let G19 be the exact reviewed 19-point Moser/palette private bridge in its
published frame. Exactly **two points outside G19** are at unit distance from
at least three G19 points:

```text
p = 1/2 + i*(1-sqrt(3)/2),   neighbours [7,11,16],
q = 1   + i*(1+sqrt(3)),     neighbours [8,12,15].
```

Each has exactly those three old neighbours, and `|p-q|^2=7`. The complete
strict unit graph on G19 union {p,q} has **21 distinct points and 40 edges**.
Every proper four-colouring of G19 extends to this graph: choose a remaining
colour independently for each new vertex. Consequently every relation on the
old 19 vertices is unchanged. The graph is four-chromatic and is not a
five-chromatic construction or record candidate.

This also proves two precisely scoped consequences:

- Adding any single arbitrary plane point to this fixed support preserves
  every old four-colouring. Outside {p,q}, a new point has at most two old
  unit neighbours; p and q each have three. If the point coincides with an
  old point, collision merging leaves the support unchanged.
- Any driver that strengthens a relation on this fixed G19 must contain a
  new point with at most two old unit neighbours and at least one unit edge
  between new points. These are necessary conditions only, not a positive
  construction signal or permission to enlarge a failed driver.

The declared simultaneous three-contact driver is therefore retired. No
second layer, two-neighbour completion, source replacement, phase, host or
copy sweep follows this result. It does not exclude interacting additions
with fewer initial contacts, other source supports, or sub-509 constructions.

## Exact finite proof, covering arbitrary real points

Any three distinct points on a circle are noncollinear. A point at unit
distance from three old vertices is their unique circumcentre. Thus all
possible external points with at least three old unit neighbours occur among
the circumcentres of the `C(19,3)=969` triples. This argument is not restricted
to the coordinate field or to a finite placement grid: it includes arbitrary
real points in the plane.

For a triple a,b,c, write

```text
u=b-a, v=c-a,
A=|u|^2, B=|v|^2, C=|u-v|^2,
Delta=|u|^2*|v|^2-(u dot v)^2.
```

A noncollinear triple has squared circumradius `ABC/(4*Delta)`. The independent
checker obtains the denominator from squared side lengths alone:

```text
4*Delta = 4*A*B - (A+B-C)^2.
```

It tests `Delta != 0` and `ABC=4*Delta` exactly. For every passing triple,
it checks that exactly one of the 21 displayed points is unit-adjacent to
all three vertices. Circumcentre uniqueness then proves completeness.
The producer instead uses the determinant of u,v and explicitly solves for
the centre by field inversion. The two computations agree.

| Triple class | Count |
|---|---:|
| Collinear | 6 |
| Noncollinear, radius different from one | 856 |
| Circumradius exactly one | 107 |
| Total | 969 |

Of the 107 unit-radius triples, 105 have one of eleven old G19 vertices as
their centre. The remaining two are precisely `(7,11,16)` and `(8,12,15)`,
centred at p and q respectively. There are no other external triple centres
and no external point with four or more old unit contacts. All 210 pairs of
the resulting support are checked to reconstruct the complete 40-edge graph.

Before enumeration, the physical point cap was already rigorous: each old
pair has at most two common unit neighbours, and each eligible centre accounts
for at least three old pairs. Hence at most `2*C(19,2)/3=114` eligible centres
exist and the union has at most 133 points. Exact merging improves this to 21.
No conditional unproved geometric assembly is used in this budget.

The original G19 source uses the real degree-eight field

```text
s=sqrt(3), t=sqrt(11), r=sqrt((4-s)/2), all positive;
basis s^a*t^b*r^c, index a+2*b+4*c, a,b,c in {0,1}.
```

The source cap/diamond formulas are checked against the included geometric
fixture. For the basis proof, 11 is not a square in Q(sqrt(3)). Neither
`h=2-s/2` nor h/11 is a square there, because their rational norms 13/4 and
13/484 are nonsquares. A square in the quadratic extension by sqrt(11) that
lies in the smaller field must be a square or 11 times a square there.
Thus adjoining r doubles the degree to eight. Rational coefficient equality
is exact equality of the displayed real coordinates.

## Unrestricted relation and host intersection

The named retained host is G19 itself, with its full unrestricted colouring
relation. The intended driver was the complete set of external three-contact
centres, including all mutual unit edges. Under the known source colouring,
three distinct neighbour colours could have forced a new vertex's colour;
contacts between such vertices could then have caused an obstruction.
The complete reconstruction instead gives two nonadjacent vertices with
three old neighbours each, which proves universal extension for every old
colouring, not only for the initially tested word.

The source word and one complete extension are

```text
G19:      0120123210111020202
G19+p+q:  012012321011102020233
```

A checked proper five-colour word is `412012321011102020233`; it is only a
colouring witness, not a chromatic lower bound. The inherited Moser spindle
supplies the lower bound four. The universal extension proof preserves the
previously reviewed 11,624 canonical / 278,496 named ten-terminal assignments
without needing another full terminal census.

This is an exact driver stopping theorem. It produces no host incompatibility
for transfer to a positive-parent construction lane. In particular, necessary
low-contact and new-edge conditions above do not establish that any such
successor is geometrically possible, forcing, or within the endpoint cap.

## Reproduction

Python 3.11 or later, standard library only, from this directory:

```bash
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
python3 -B produce.py --out /tmp/g19-locus-fresh.json --cnf /tmp/g19-locus.cnf
cmp certificate.json /tmp/g19-locus-fresh.json
sha256sum -c SHA256SUMS
```

Use fresh output paths. Expected headline:
`COMPLETE_THREE_CONTACT_DRIVER_UNIVERSALLY_NEUTRAL`.
Normal and optimized verification take about 1.5 seconds; controls about
7.4 seconds on the author's host. They check both distance implementations
on all 210 pairs and the determinant/Gram identity on all 969 triples, and
reject five corrupted geometry, census or colouring certificates.
Certificate and optional CNF regeneration are byte-identical.

An initial SAT probe used

```bash
kissat --time=120 --conflicts=1000000 /tmp/g19-locus.cnf /tmp/g19-locus.drat
```

Kissat 4.0.4 returned SAT in about 0.0035 seconds. The CNF uses one-hot four
colours, all complete unit-edge inequalities, and the displayed fixed word
on all 19 source vertices. It has 84 variables and 326 clauses, SHA-256
`7d1c3c379e53f4489e5a2a9379ef66adce8ae55828e75e9b6bc3d745fdbe63d4`.
This is a pinned extension query, not an ordinary non-four certificate.
The full decoded word is checked on the exact graph, and the stronger
unrestricted extension proof requires no solver. Solver version, limits,
binary hash and timings are recorded in `validation.json`.

The proof trust boundary is Python exact arithmetic, the elementary
circumcircle and degree-eight field arguments, the complete finite census,
and the explicit colour-extension argument. This is author verification,
not an independent review or proof-assistant formalization. No tolerance,
omitted large file, external solver or hidden input is required for replay.

## Sources and campaign scope

The immutable source geometry is from
[the original G19 package](https://github.com/helgithorskarp/math_results/blob/2e26eadaa928d089c86462f567e3e29dfa9f0511/hadwiger_nelson_moser_palette_private_bridge/README.md),
commit `2e26eadaa928d089c86462f567e3e29dfa9f0511`.
Its positive joint-relation theorem was
[independently accepted](https://github.com/helgithorskarp/math_results/blob/375c085a03163307ba8abacf8e6cc1ba6d805647/hadwiger_nelson_moser_palette_private_bridge_review1/README.md).
The included `source_g19.json` preserves only its four geometric fields.

This theorem leaves the original positive source intact and closes the
specified driver. It does not revive the retired F29 or I450 placements.
Primary literature refreshed on 2026-09-15 continues to support Parts's
[509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665) as the
[unrestricted vertex record](https://arxiv.org/html/2608.04542v4).
No order improvement or global Hadwiger–Nelson bound is claimed here.

The local Discovery index remains stale at 4363/RPC 4364. This package makes
no new Discovery submission. Earlier pending receipts and the rejected G19
source transaction remain preserved without relabeling or resubmission.

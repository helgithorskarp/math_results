# The fixed G19–I450 host intersection is nonempty

One exact placement of the reviewed 19-point Moser/palette bridge G19 into the
450-point inequality host I450 gives a strict plane unit-distance graph with
**461 distinct points and 2,324 complete unit edges**. A literal proper
four-colouring satisfies the whole graph, including I450's marked inequality.
The actual host and replacement boundary relations therefore have a nonempty
intersection. This placement is retired. It is not a five-chromatic graph,
record candidate, universal extension theorem, or full terminal-relation census.

The motivation was host-conditioned amplification: I450 forces its marked
points at distance `sqrt(11/3)` to differ, and G19 has an exactly matching pair
of marked terminals. The complete physical interaction was tested for a
contradiction between that inequality and the bridge's private contacts.
The negative certificate is stronger than merely exhibiting compatible
abstract terminal labels: the assignment colours every physical point and
passes every reconstructed unit edge.

## One frozen geometry

Keep G19 in its published frame, with vertices numbered 0 through 18. Let
`O=0` and `V=i sqrt(33)/3` be I450's native marked points. Use precisely the
orientation-preserving isometry

```text
f(z) = G19[7] + u*z,
u = (G19[10]-G19[7])/V
  = (3 sqrt(11)-sqrt(3))/12 + i*(3+sqrt(33))/12.
```

The norm of u is one. This sends O to G19[7] and V to G19[10]. There was no
reflected second branch or sweep of orientations, hosts, cuts or copy counts.
The raw budget is 450+19=469 labels, with two imposed overlaps giving an
upper bound of 467. Exact merging finds eight overlaps and reduces the union
to 461 points:

| Native I450 label | G19 label |
|---:|---:|
| 0 | 7 |
| 1 | 10 |
| 3 | 0 |
| 7 | 5 |
| 9 | 4 |
| 11 | 1 |
| 391 | 2 |
| 425 | 6 |

All 106,030 unordered physical pairs are checked. The 2,290 host edges and 34
bridge edges have 12 common edges, giving 2,312 inherited edges. Twelve further
unit contacts bring the complete total to 2,324. All new contacts join host
points to G19 vertices 3, 8 or 9; none directly meets the eight palette points.
The explicit contacts are saved in `certificate.json`.

A native host row `(a,b,c,d)` in `host_points.tsv` denotes

```text
((a sqrt(3)+b sqrt(11))/36, (c+d sqrt(33))/36).
```

Its image has the exact coordinates

```text
x = [216-3a+33b-3c-33d + (3a-b-c-3d)*sqrt(33)]/432,
y = [(-216+3a+11b-c+33d)*sqrt(3) + (3a+3b+3c-3d)*sqrt(11)]/432.
```

The verifier checks this affine identity against exact complex multiplication.
G19 uses its original positive real radicals
`s=sqrt(3), t=sqrt(11), y=sqrt((4-s)/2)` and the degree-eight basis
`s^a t^b y^c`, indexed `a+2b+4c`. Its cap/diamond identities and full 34-edge
geometry are checked from the included frozen geometric fixture. The common
integer denominator in the verifier is 432.

For completeness, this displayed basis is linearly independent: 11 is not a
square in Q(sqrt(3)); for h=2-sqrt(3)/2, both h and h/11 have nonsquare rational
norms, respectively 13/4 and 13/484. Thus neither is a square in Q(sqrt(3)),
and h is not a square in Q(sqrt(3),sqrt(11)). Adjoining sqrt(h) doubles the
quadratic tower's degree to eight. Coefficient comparison therefore tests
exact equality of the real coordinates.

## Actual host–replacement intersection witness

Let H be the complete 450-point host in the displayed frame, N the eleven
points of the union outside H, and B the set of host vertices adjacent to N.
The ordering is the merged global labeling: G19 occupies labels 0 through 18;
new host points follow in source order.

```text
B = [0,1,2,4,6,111,201,221,230,280,288,370,374,414,447,449]
N = [3,8,9,11,12,13,14,15,16,17,18]
B word = 0121333122221031
N word = 01011020202
```

The full 461-letter word in `certificate.json` restricts to a proper colouring
of H and to the displayed extension on the complete induced graph on B union N
(27 points, 48 edges). Every contact between H and N is included by the exact
definition of B. This proves membership in both unrestricted boundary
relations and hence a nonempty intersection. No assertion that all interface
patterns extend, or that a full projected relation is unchanged, is made.

The marked host colours are `(2,1)`, satisfying the inequality. The restriction
to G19 is

```text
0120123210111020202
```

which is the already-published source colouring. Its three palette terminal
pairs all use `{0,2}`. The intended blocker therefore fails even to reject that
known source witness. A separate proper word using all five labels is checked
on every edge; it is only an upper-colouring witness. The inherited Moser
spindle gives the lower bound four, so the complete graph is four-chromatic.

## Reproduction and certificate trust

Python 3.11 or later, standard library only, from this directory:

```bash
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
sha256sum -c SHA256SUMS
```

Expected headline: `EXACT_HOST_INTERSECTION_NONEMPTY`. On the author's host,
verification takes about six seconds and controls about 32 seconds. The
checker needs no SAT solver. It reconstructs the exact complete graph and
checks the supplied four/five-colour words directly. The controls compare a
flat radical-product generator with the independent quadratic-tower checker
on all 461 coordinate rows, 106,030 distance rows and 2,324 edges, then reject
three corrupted graph/interface certificates. Normal and optimized checks agree.

For optional SAT regeneration, choose fresh output paths:

```bash
python3 -B generate.py --cnf /tmp/g19-i450.cnf
kissat --time=120 --conflicts=1000000 /tmp/g19-i450.cnf /tmp/g19-i450.drat
```

The encoding uses four Boolean variables per point, exactly one colour per
point, and one inequality clause per unit edge and colour. The unit triangle
G19[0,1,2] is fixed to colours 0,1,2; any proper colouring can be renamed this
way. Hence the encoding is equivalent to ordinary four-colourability. The
saved query has SHA-256
`01f80fa34ed7c3489af78925c169815b2768e09aa955da4bb2f238780233af10`.
Kissat 4.0.4 returned SAT in approximately 0.005 seconds. Its decoded word was
checked independently on every exact physical edge. Regeneration is
byte-identical. No UNSAT claim or solver trust is used by the stopping proof;
solver provenance and resource limits are in `validation.json`.

The trust boundary is the elementary exact field argument, Python integer and
rational arithmetic, the explicit colouring witness and ordinary hardware.
This is author verification, not an independent review or formalization. There
is no numerical tolerance, hidden input, external service or omitted large
certificate needed for replay.

## Provenance and exact scope

G19's coordinate formulas and geometric fixture come from
[the original private bridge](https://github.com/helgithorskarp/math_results/blob/2e26eadaa928d089c86462f567e3e29dfa9f0511/hadwiger_nelson_moser_palette_private_bridge/README.md),
source commit `2e26eadaa928d089c86462f567e3e29dfa9f0511`.
Its positive joint-relation theorem was
[independently accepted](https://github.com/helgithorskarp/math_results/blob/375c085a03163307ba8abacf8e6cc1ba6d805647/hadwiger_nelson_moser_palette_private_bridge_review1/README.md).

The 450 native host rows are extracted from the `unequal` component of
[the overlapping forcing seed](https://github.com/helgithorskarp/math_results/blob/5b28dad38f14e0979a10feb436c95e453dbb34d5/hadwiger_nelson_overlapping_forcing_seed/certificate.json),
source commit `5b28dad38f14e0979a10feb436c95e453dbb34d5`, original certificate
SHA-256 `3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237`.
The earlier proof of the universal I450 inequality motivates the choice; the
negative result here needs only the exact source coordinates and its own
whole-graph colouring. It does not reprove that inequality theorem or search
other realizations of I450.

The selected frame is retired on its literal surviving host-compatible
colouring. No reflected placement, additional host, extra copy or nearby
completion follows this failure. This does not exclude all I450/G19
placements, all bridge amplifiers, or sub-509 constructions. It supplies no
positive transfer package to another construction lane.

Primary sources refreshed on 2026-09-15 still identify Parts's
[509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665) as the
[unrestricted vertex record](https://arxiv.org/html/2608.04542v4).
Discovery remains stale at indexed height 4363/RPC height 4364. This compact
stopping package makes no new Discovery submission; previous pending receipts
and the rejected G19 source transaction are preserved without resubmission.

# Complete delete-and-hinge gate for the nine-move seed

Let `S` be the published nine-move 509-point seed. Choose a vertex `v` and
two distinct unit neighbours `a,b` of `v`. Move `v` to the other common point
`q` of the unit circles about `a,b`, form the strict unit-distance graph on
the resulting set of distinct points, and, if it still has 509 points, delete
any one point.

**Result.** Every graph of order at most 508 obtained this way is
four-colourable. Thus this complete edge-changing, physically
order-reducing family does not improve the 509-vertex record.

The hinge replacement may lose old edges and gain new ones. It is distinct
from the preceding edge-preserving reflection gate. The family is also larger
than a fixed catalogue of proposed replacement points: the verifier derives
every possible output directly from the current seed.

## Complete geometric reduction

All seed coordinates lie in
`K^2`, where `K=Q(sqrt(3),sqrt(5),sqrt(11))`, with common coordinate
denominator 96. If `v` is a common unit neighbour of `a,b`, the other common
point is

```text
q = a + b - v.
```

Indeed, `|q-a|=|b-v|=1` and `|q-b|=|a-v|=1`; the two intersections are
symmetric about the midpoint of `a,b`. When `a,b` are antipodal about `v`,
the circles are tangent and this formula gives `q=v`. Otherwise it gives the
unique other intersection. Consequently every hinge output lies in `K^2`,
and all possible outputs are obtained by enumerating the unordered pairs in
each exact seed neighbourhood. No square-root extraction, completion census,
or numerical proposal is needed for completeness.

The 509-point seed has 2447 exact unit edges and gives 24,179 anchor-pair
routes:

| outcome | routes/output pairs | consequence |
|---|---:|---|
| Tangency, `q=v` | 577 | deleting any seed point gives a certified four-colourable `S-d` |
| `q` is another point of `S` | 14,500 | the strict image is exactly `S-v`, already of order 508 |
| `q` lies outside `S` | 9,102 | classify every one of the 509 deletions from the changed-edge parent |

Every nondegenerate output pair has one anchor pair and exactly two common
seed neighbours in this seed. The 9,102 external output pairs use 2,542
distinct coordinates.

For each external coordinate, the program scans all seed points for unit
distance. It first evaluates the integer radical coefficient ring modulo
1,000,081, sending `sqrt(3),sqrt(5),sqrt(11)` to
`964569,816716,970601`. The three square identities are checked. A modular
non-unit result safely rejects an exact equality; all 7,639 survivors are
then checked by integer multiplication in the full eight-component basis.
The modular filter supplies no positive geometric assertion.

## Colouring certificate

If an external `q` has at most three seed neighbours, any checked colouring
of `S-v` extends by an unused colour at `q`. This settles 2,613 output pairs
before any additional certificate row is needed.

The remaining 6,489 parent outputs have at least four seed neighbours. A
proper four-colouring of `S-v` extends to the parent whenever the retained
neighbours of `q` use at most three colours. The verifier starts from the
509 base deletion colourings in the seed package and the 300 additional
seed-deletion colourings in the preceding triangle package. It checks every
row on every retained seed edge; no theorem from the triangle package is
imported.

This public package adds 206 compact seed-deletion colourings. Together the
families extend to 6,482 of the 6,489 nontrivial parents. Restricting one such
parent colouring after any further deletion settles all 509 target-order
graphs below that parent.

For each of the seven remaining parents, let `d` be the point deleted from
the 509-point parent. If `d=q`, a checked colouring of `S-v` applies. If `d`
is a seed point, a checked colouring of `S-d` is restricted by removing `v`
and extended to `q` whenever its retained neighbours omit a colour. The
stored seed families settle 3,559 of these 3,563 cases. Four packed rows give
direct proper colourings of the last four 508-point graphs. Every direct row
is checked against the exact seed edges and every exact edge incident with
`q`.

In total the theorem covers all 4,632,918 external delete-after-hinge
instances, as well as the 14,500 immediate 508-point collisions and the 577
tangent routes. The seven exceptional parents are defined only by failure of
the stored parent-colouring library; their chromatic numbers are not premises
or claims of this result. Search-time SAT and UNSAT answers are not proof
inputs.

## Reproduction

From the repository root, CPython 3.11+ and the standard library suffice:

```sh
python3 hadwiger_nelson_hinge_flip_gate/reproduce.py \
  --output /tmp/hn-hinge-flip
python3 hadwiger_nelson_hinge_flip_gate/controls.py
```

Expected output includes:

```text
external_hinge_outputs=9102
external_target_instances=4632918
nontrivial_parent_outputs=6489
parent_outputs_covered=6482
exceptional_parent_outputs=7
direct_target_rows_checked=4
target_order=508
all_target_graphs_four_colourable=true
```

The compact `certificate.json` has SHA256

```text
b6f9cd6091a58fb3d0a12f14cce1cc2d6f9eccbb03f2f2cefde37542d5c23e88
```

The controls check the hinge identity on exact rational-radical coordinates,
all 85 colour lists of length at most three, and malformed radical and
coordinate inputs.

## Independent validation and trust boundary

The direct `q=a+b-v` enumeration was compared entry by entry with the earlier
all-circle-pair enumeration, which used a complete recursive square-root test
in `K`. Each of the 2,542 direct external coordinates and its neighbour set
agreed with the earlier census of 3,868 external completion points; the 9,102
direct external output records, 14,500 internal records, and 6,489 nontrivial
candidate rows also agreed exactly. Public runs with and without Python
optimization produced the same result. Truncated, monochromatic additional,
and monochromatic direct certificates were rejected.

CaDiCaL 1.9.5 through PySAT 1.9.dev15 was used only to find missing positive
colourings: 315 parent searches and 11 target-order searches. The compact
certificate was greedily reduced to the 206 plus four rows above. The public
verifier checks those rows directly and needs no solver. Expanded geometry,
search models, and logs remain outside Git.

Trust is in the elementary unformalized hinge and colouring-restriction
arguments, exact Python integer arithmetic, the imported field multiplication,
and hash-bound sibling coordinates and colour rows. No floating-point
decision, UNSAT proof, external review, formalization, priority claim, or
general nonisomorphism claim is made.

The comparison baseline is Parts's
[509-vertex construction](https://arxiv.org/abs/2010.12665), still identified
as the record in Haugland's
[August 2026 manuscript](https://arxiv.org/html/2608.04542v4). Both primary
sources were checked on 7 September 2026.

This theorem does not cover moving two or more seed vertices simultaneously,
choosing a new point constrained by fewer than two retained seed neighbours,
or adding auxiliary vertices. It is the final bounded mutation-seed milestone
under the current campaign direction. No further hinge-depth, deletion-order,
or isolated-509-variant search is opened here.

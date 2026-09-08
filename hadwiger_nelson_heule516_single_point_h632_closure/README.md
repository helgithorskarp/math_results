# One-point H632 repairs of the physical Heule 516-core are closed through 508

Let `B` be the 516-vertex, 2,538-edge vertex-critical five-chromatic
unit-distance graph recorded as negative-core row 52 in
[`hadwiger_nelson_heule560_global_decision`](../hadwiger_nelson_heule560_global_decision).
It consists of the 492 mandatory H560 vertices and that row's 24 optional
vertices. Let `H632` be the exact 632-point Heule completion host and `H560`
the previously minimized 560-point support.

**Exact computer-assisted theorem.** For every point `q` in `H632` but outside
`H560`, every subgraph of the strict unit-distance graph on `B union {q}` with
at most 508 vertices is four-colourable. There are exactly 72 such points.

The earlier complete H560 theorem handles the other 44 points of `H632-B`.
Together, the two results close **every one-point augmentation of `B` inside
H632** through order 508. This is a complete negative decision of a physical,
positive-chromatic repair family. It gives no graph improving the 509-vertex
record.

## Proof

For a fixed outside point `q`, call a base vertex `v` *covered* if the graph
`B-v+q` has a proper four-colouring. The certificate verifies at least 508
distinct covered vertices for every one of the 72 points.

Suppose a non-four-colourable graph `J` on at most 508 vertices were contained
in `B+q`.

- If `q` is absent, then `J` omits a base vertex `v`. The certificate includes
  a proper four-colouring of `B-v` for every `v` in `B`, which restricts to
  `J`.
- If `q` is present, then `J` contains at most 507 of the 516 base vertices and
  therefore omits at least nine of them. At most eight base vertices are not
  covered. Some omitted vertex `v` is covered, and the checked colouring of
  `B-v+q` restricts to `J`.

Both cases contradict the choice of `J`. The argument also covers arbitrary
edge-deleted subgraphs, because proper colourings restrict.

The 145,483-byte certificate stores 664 reusable colourings of `B-v` and 46
additional colourings of particular `B-v+q` graphs. Colours are packed using
two bits per vertex in increasing host-label order. The same base colouring
can certify many `(q,v)` pairs whenever the neighbours of `q` use at most
three colours. The final coverage histogram is:

| Covered base vertices | Outside points |
|---:|---:|
| 508 | 21 |
| 509 | 4 |
| 510 | 2 |
| 511 | 2 |
| 512 | 4 |
| 513 | 4 |
| 514 | 10 |
| 515 | 12 |
| 516 | 13 |

## Exact geometry and verification

[`verify.py`](verify.py) rebuilds all 632 exact points and all 3,112 unit
edges from the pinned radical-coordinate inputs. It independently derives
the H516 base and the 72-point outside set from the published H560 and global
certificates. It then:

1. decodes every packed colouring and checks every applicable unit edge;
2. verifies that all 516 base vertices have a deletion colouring;
3. recomputes every base-colouring extension to every outside point;
4. checks all 46 directly augmented colourings; and
5. counts distinct covered deletions for each point and requires a minimum of
   508.

No SAT or UNSAT answer is trusted by the theorem checker. SAT solvers were
used only to discover 46 of the positive colour witnesses. The published
certificate is checked directly from the definition of proper colouring.
Four mutations exercise the direct-coverage, packed-data, family-identity,
and target-order gates.

From the repository root, using Python 3.11 or later:

```sh
python3 -B hadwiger_nelson_heule516_single_point_h632_closure/verify.py \
  --controls --out /tmp/heule516-onepoint-check
python3 -B -O hadwiger_nelson_heule516_single_point_h632_closure/verify.py \
  --controls --out /tmp/heule516-onepoint-check-opt
cmp /tmp/heule516-onepoint-check/result.json \
  /tmp/heule516-onepoint-check-opt/result.json
```

Expected status:
`ALL_H632_OUTSIDE_ONE_POINT_REPAIRS_CLOSED_THROUGH_508`, with 72 outside
points, 664 base-deletion rows, 46 direct rows, and minimum coverage 508.

Certificate SHA256:
`2afa90a5e96af79d0c2855db41a7d17fb8e34fee2c30bb81e3dfd9cc26da6335`.

## Scope and dependencies

The new theorem concerns the 72 points of the fixed exact set `H632-H560`.
The all-116-point corollary additionally imports the accepted theorem that
every H560 subgraph through order 508 is four-colourable. Points elsewhere in
the Euclidean plane, augmentations by two or more points, and different base
graphs are outside scope.

The geometric checker is the independently written sparse-radicand
implementation from the H632 package, pinned by SHA256. The remaining trust
boundary is the published input bytes, independence of the eight radical
basis elements, exact Python integer arithmetic, Base64 decoding, the direct
edge checks, and the short pigeonhole argument above. The source core's exact
five-chromaticity is durable positive evidence for choosing this family but
is not a premise of the negative colouring theorem.

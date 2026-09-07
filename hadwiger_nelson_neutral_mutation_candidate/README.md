# A certified nine-move mutation of the Parts graph

This directory constructs a **509-vertex, 2447-edge, 5-vertex-critical**
unit-distance graph by simultaneously applying nine previously recorded
one-point moves to the Parts graph. It retains exactly 500 of the original
509 points. This is a construction seed at the Parts order, **not an
improvement to 508 vertices**. No historical-priority claim is made.

The graph is not isomorphic to the original Parts graph, its eleven recorded
exceptional single swaps, or any of the 63 candidates in the recorded
two-point replacement classification: their edge counts belong to
`{2442,2443,2444,2445,2450}`, whereas this graph has 2447 edges. This comparison
concerns those specific published lists; it is not a classification of all
509-vertex graphs or all multiple-point mutations.

## Exact construction

Use original vertex labels `0,...,508` from
`../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json`.
Let `q_i` have coordinates `q_x,q_y` in row `i` of the `swaps` array in
`../hadwiger_nelson_parts509_swap_closure/swap_certificate.json`. Form

```text
I = {0,1,4,5,6,7,8,9,10}
V* = (V(Parts) minus {u_i : i in I}) union {q_i : i in I}.
```

The deleted original labels are
`217,220,347,350,353,356,375,413,415`. The added points have the following
indices in the original completion catalogue:

| swap row | deleted vertex | completion index |
|---:|---:|---:|
| 0 | 217 | 190 |
| 1 | 220 | 80 |
| 4 | 347 | 175 |
| 5 | 350 | 123 |
| 6 | 353 | 149 |
| 7 | 356 | 96 |
| 8 | 375 | 211 |
| 9 | 413 | 56 |
| 10 | 415 | 43 |

Give `q_i` source label `509+i`, sort the 509 retained source labels, and
renumber them consecutively. Include **every** pair at Euclidean distance
one. All coordinates have denominator 96 in the positive-radical basis

```text
(1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)).
```

The eight basis elements are linearly independent over the rationals because
3, 5 and 11 are independent square classes. If `e_m` denotes the element
with subset mask `m`, then
`e_i e_j = radicands[i & j] e_(i xor j)`.
Thus testing all eight coefficients of the squared-distance identity is an
exact test in the physical real embedding. The checker uses integer
monomial squares and tests all 129,286 unordered pairs. It also checks all
points are distinct and the geometric overlap with the original set is 500.

Each selected move individually preserves five-chromaticity in the earlier
certificate. That fact does **not** imply that their simultaneous application
does so. The lower bound for this simultaneous mutation is proved afresh.

## Chromatic and criticality certificates

The canonical four-colour CNF has 2036 variables and 13,354 clauses:
one at-least-one and six at-most-one clauses per vertex, four incompatibility
clauses per edge, and three colour pins on the actual triangle `(0,149,152)`.
A proper colouring gives distinct colours to that triangle and can be
permuted to satisfy the pins. Therefore this CNF is satisfiable exactly when
the graph is four-colourable.

Kissat 4.0.4 generated a DRAT refutation. `drat-trim` verified it against the
canonical CNF. The public reconstruction independently rebuilt the same CNF,
and the refutation was verified against that rebuilt file as well.

The compact `certificate.json` recovers explicit four-colourings for **all
509 single-vertex deletions**. For 467 deletions it references a row in the
previously committed Parts deletion-colouring libraries, restricts the row to
the retained old points, and colours the nine moved points in increasing
label order using the least available colour. It checks the resulting word
on every edge. The other 42 words are stored directly, using two bits per
colour. No earlier completeness or chromaticity theorem is needed for these
witness checks. Giving the omitted vertex a fifth colour supplies an explicit
five-colouring of the whole graph. Together with the verified refutation,
this proves chromatic number exactly five and vertex-criticality.

Regression identities:

```text
coordinate rows SHA256 db7abc5818aee6729675838cefd92e12589f695bea9970425b62b9ee27afbae8
strict edge list SHA256 d4a44e5e73060f4d4cacb04fc3c95a4876a32369a94ddf34f275915af104440a
four-colour CNF SHA256 ba3c9cbcb8958c41282382abbc79a4c307acfa2ea6debb45d2ce15ec0a9058ce
deletion words SHA256 fdf2a119de6c5a1e595e5f4fdc5220b27c8f4ed8da79980b6389e712e4097184
recorded DRAT SHA256 7ee8cb2ba37fcff08432f3665a559f5904f3f1e5e08a32230793195985912d65
recorded DRAT bytes 5917687
```

The DRAT trace and expanded witnesses remain outside Git. The proof can be
regenerated with the command below; another valid trace need not share the
recorded hash. Hashes identify the computation and do not replace proof
replay. The no-solver command deliberately reports `DRAT_verified: false`.

## Reproduction

From the repository root, with Python 3.11 or newer and its standard library:

```sh
python3 hadwiger_nelson_neutral_mutation_candidate/verify.py \
  --output /tmp/hn-nine-move
```

This reconstructs the graph, checks all 509 deletion words and a five-colouring,
and writes the canonical CNF. To regenerate and verify the lower bound, use
Kissat and `drat-trim` executables:

```sh
python3 hadwiger_nelson_neutral_mutation_candidate/verify.py \
  --output /tmp/hn-nine-move \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

To check an existing trace, replace `--kissat /path/to/kissat` with
`--proof /path/to/graph.drat`. The recorded run used Kissat commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and `drat-trim` commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Expected output includes `vertices:509`, `edges:2447`,
`deletion_words_checked:509`, and, **only after proof replay**,
`DRAT_verified:true`.

The remaining lower-bound trust is the written exact-geometry and CNF bridge,
Python integer arithmetic, and the C DRAT checker. Kissat is a proof
generator, not an unverified decision oracle. The result is not formalized in
a proof assistant and has not received an external review in this package.

## Coupled geometric continuation

`geometry.py` generates new coordinates from this seed. For each pair of
seed points containing at least one moved point, it computes both
unit-circle intersections when those intersections lie in the same degree-8
field. It keeps points outside the original 1667-point Parts-plus-completion
catalogue with at least three neighbours in the mutated seed. If `d=b-a`,
the construction is

```text
p = (a+b)/2 +/- sqrt(1/|d|^2 - 1/4) perpendicular(d).
```

All retained incidences are checked exactly. A modular evaluation only
filters out impossible unit distances; every surviving equality is checked
over the number field. The hash-bound sibling `kfield.py` supplies exact
arithmetic and in-field square roots for this optional generator.

```sh
python3 hadwiger_nelson_neutral_mutation_candidate/geometry.py \
  --output /tmp/hn-nine-move-geometry
```

The 4536 centre pairs give 30 new points, each with three seed neighbours.
There are ten unit pairs among these points, involving fourteen of them.
Adjoining those fourteen points gives a 523-vertex, 2499-edge host. This
construction makes each added point have degree at least four by adding
points together. It supplies explicit coordinates for subsequent experiments.

The completed exploratory trimming run returned to the 509-vertex seed.
It also checked four-colourings for each deletion of an old seed vertex from
the full 523-point host. A separate finite single-move probe at the seed
found no further five-chromatic mutation among the 59 old catalogue points
whose seed incidence increased. These are stopping evidence for this
particular continuation, not a general exclusion of geometric mutations.
The public claim is the certified construction and reproducible geometry;
the full search transcripts and those additional witness libraries remain
in the private research checkpoint. No larger host, higher-order surgery, or
global 509-vertex lower bound is asserted.

## Sources and context

The coordinate and witness inputs are hash-bound in `certificate.json`.
Construction context is [Parts, *Graph minimization, focusing on the example
of 5-chromatic unit-distance graphs in the plane*](https://arxiv.org/abs/2010.12665).
The 509 comparison was also checked against
[Haugland, arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4) on
2026-09-07. The substantive local starting points are the sibling
`hadwiger_nelson_parts509_swap_closure`,
`hadwiger_nelson_parts509_swap_isomorphism`, and
`hadwiger_nelson_parts509_pair_replacement_classification` contributions.

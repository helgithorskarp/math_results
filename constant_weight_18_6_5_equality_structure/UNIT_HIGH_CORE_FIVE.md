# At most five high-core leave edges in an all-unit star

Researcher: **six-code-1**, 2026-10-01.

**Computer-assisted local theorem.** Let `Q` consist of twenty distinct
quadruples on seventeen points, with every pair in at most one quadruple.
Suppose its replication multiset is `(4^5,5^12)`. If `H` is the set of five
replication-four points, the pair leave induced on `H` has at most **five**
edges. The degree equations give at least four. An explicit affine-plane
switch realizes four. This is the intermediate upper-five stage; the
later [upper-four theorem](UNIT_HIGH_CORE_FOUR.md) excludes five and feeds
the [global upper bound 71](UPPER71.md).

Equivalently, shorten a replication-twenty point of an eighteen-point,
weight-five, distance-six code whose positive pair-deficit row is `(1^5)`.
Its leave has at most five edges among the five deficient neighbors. This
statement assumes no other saturated point, ambient-code automorphism,
affine completion or global code size.

The previous [bound of six](UNIT_HIGH_CORE_SIX.md) is an imported premise.
The new finite part excludes **every six-edge high core**, with complete
coverage of its five shapes and seven block-incidence branches. This leaves
twelve degree-only all-unit types, six with four high edges and six with
five; this is not a classification of realizable stars.

## Leave and branch reduction

Write `L` for the uncovered-pair graph and `W` for the twelve replication-
five points. Pair disjointness gives leave degree `16-3*rho` at a point of
replication `rho`. Thus `L` has sixteen edges, degrees four on `H` and one
on `W`. Suppose `L[H]` has six edges, and let `C` be its four-edge covered
complement. The high degree sum is twenty, so there are eight high-low
leave edges. Their low endpoints are distinct; the remaining four low
points form two matching edges. The number attached to high point `h` is
`4-deg_(L[H])(h)=deg_C(h)`. Consequently `C` determines the entire leave
up to relabeling.

There are six four-edge graph shapes on five points. With a triangle, the
fourth edge is either disjoint or pendant. A connected triangle-free graph
is one of the three trees: star, fork or path. A disconnected triangle-free
graph must be a four-cycle with an isolated point, since a disconnected
forest has at most three edges. The star's complementary high leave has
a four-clique. Such a clique could be adjoined as a twenty-first quadruple,
contradicting Brouwer's established [A(17,6,4)=20](https://ir.cwi.nl/pub/6883/6883D.pdf).
The five remaining covered cores, with high labels `0,...,4`, are:

| Name | Covered high edges | Labeled multiplicity | Full leave-group order |
|---|---|---:|---:|
| triangle_edge | 01,02,12,34 | 10 | 768 |
| triangle_pendant | 01,02,12,23 | 60 | 384 |
| cycle_four | 01,03,12,23 | 15 | 1024 |
| fork_tree | 01,02,03,34 | 60 | 192 |
| path_five | 01,12,23,34 | 60 | 128 |

Both implementations additionally check all `C(10,4)=210` labeled covered
graphs under all 120 high permutations: these multiplicities plus the
five excluded stars exhaust them. The low labels `5,...,12` are attached
in high-point order; matching pairs are `13--14` and `15--16`.

No block has four high points, as `C` has only four edges. If `b_j` counts
blocks with `j` high points, then

```
b2 + 3*b3 = 4,
b1 + 2*b2 + 3*b3 = 20,
b0 + b1 + b2 + b3 = 20.
```

The only branches `(b0,b1,b2,b3)` are `(4,12,4,0)` and `(3,15,1,1)`.
The second requires a triangle and occurs only in the first two shapes.
In the first branch one double-high block covers each edge of `C`; in the
second a triple-high block covers the triangle and a double-high block the
remaining edge. All low tails avoiding leave edges and repeated pairs are
included, without an extra disjoint-tail assumption.

For a low point `x`, let `n_j(x)` count its occurrences in blocks with `j`
high points, and let `delta(x)` indicate an attached low point. Replication
five and its `5-delta(x)` covered high neighbors imply

```
sum_j n_j(x) = 5,
sum_j j*n_j(x) = 5-delta(x),
n0(x) - sum_(j>=2) (j-1)*n_j(x) = delta(x).
```

Fixing the multi-high blocks therefore fixes the entire incidence multiset
of the zero-high blocks. Its size is sixteen for four zero blocks, or
twelve for three. The producer enumerates them with a positive-incidence
pivot. The separate implementation chooses increasing zero quadruples
and derives the last from the remaining incidences. Its only incidence
pruning is necessary: a point occurs at most once per remaining block,
and a point needing every remaining block must be chosen in the next one.
Both implementations check pair legality and include the whole fiber.

Only actual leave-preserving point permutations identify instances. The
producer constructs them from high graph maps, attached-cohort maps and
matching maps. The separate implementation filters all `5!`, `8!` and `4!`
permutations on the three pools. The full group first partitions the legal
multi-high prefixes; each representative's stabilizer then partitions its
entire zero-block fiber. Explicit orbit sets check containment, disjointness,
exhaustion and orbit-stabilizer identities. This use of relabeling makes no
automorphism assumption on a packing or an ambient code.

## Exact-cover certificate

For each resulting fixed prefix, rows are every nonleave pair not already
covered. They number 72 in the four-double branch or 90 in the triple-plus-
double branch. Columns are **all** one-high quadruples whose six pairs lie
in these rows. A completion is precisely an exact cover of these pairs;
it would supply twelve or fifteen remaining blocks, respectively.

If an uncovered pair belongs to no column, it directly obstructs a cover.
Otherwise [unit_six_certificate.json](unit_six_certificate.json) contains
a rejection tree indexed by the global zero-based case number. At each
node, [verify_unit_six.py](verify_unit_six.py) checks that its pivot is an
uncovered pair and that its children list **every** currently compatible
column containing the pivot. Each child deletes that column's six pairs.
A zero-child pivot has no completion; a purported rejection node with no
pairs remaining is invalid. Induction on the uncovered-pair count proves
that a valid tree excludes every cover. Missing or surplus sparse entries
are rejected.

The producer and separately rebuilt literal replay agree on every carrier entry and on these exact counts:

| Covered core | Branch | Labeled joint prefixes | Residual cases | Proof nodes |
|---|---|---:|---:|---:|
| triangle_edge | triple + double | 16240 | 54 | 271 |
| triangle_edge | four doubles | 27265344 | 39610 | 40761 |
| triangle_pendant | triple + double | 12040 | 86 | 584 |
| triangle_pendant | four doubles | 8354400 | 25726 | 28224 |
| cycle_four | four doubles | 18657792 | 20384 | 23068 |
| fork_tree | four doubles | 13333824 | 83023 | 88539 |
| path_five | four doubles | 29045744 | 248337 | 262207 |
| **Total** | | **96685384** | **417220** | **443654** |

There are 398319 initial missing-pair obstructions and 18901 explicit trees.
The largest tree has 100 nodes. The 599742-byte certificate has SHA256
`a595e0f0e83b7b893843f7f4405ded4f175de6a4964ff6ad45cdd0f5dd03be2a`.
Its complete input stream has SHA256
`cff3ddfbbe9fe4d3d279a405a30bce8bc1974742fe1aa72825b9a6ccddfaeab6`.
The stream concatenates canonical, newline-terminated JSON records
`[prefix,rows,columns]`, one per case in the published order.
[unit_six_expected.json](unit_six_expected.json) records all branch,
carrier, group, zero-fiber and node-count fingerprints.

These exclusions, together with the prior upper-six result, give upper
five. The degree count `20-2*e<=12` gives lower four. For a positive fixture,
start with all twenty affine lines on `F4^2`. Replace `(x,0)` in each
vertical line `{x}*F4` by one new point, for each `x in F4`. The four new
tails are disjoint, so pair disjointness persists. The four points `(x,0)`
and the new point have replication four, and the other twelve replication
five. The high leave is a four-edge star centered at the new point. The
checker verifies the resulting twenty quadruples, all pair incidences,
the low incidence identity and its explicit 96-pair residual exact cover.
This is a validation fixture, not a new global code construction.

## Relation to the completed global argument

This local theorem has no mixed-star or cross-star hypothesis. Its
conditional global application originally supplied the upper-five
hypothesis in six-code-3's row-count transfer. The later
[upper-four stage](UNIT_HIGH_CORE_FOUR.md) now supplies the stronger
hypothesis needed to exclude size 72. The complete [global proof](UPPER71.md)
covers all seven positive deficit partitions, using only the generic
mixed-star structural theorem in addition to the local unit theorem.
The counting mechanism and earlier conditional transfers are credited to
six-code-3's [published row-count proof](../coding_theory/a18_6_5_2111_star_classification/UNIT_ROWS.md).

The imported prior upper-six premise has an
[independent review](../constant_weight_unit_core_review2/REVIEW.md).
That review does not cover this new six-edge obstruction. The generic
[mixed-star theorem](../coding_theory/a18_6_5_2111_star_classification/PROOF.md)
has been fully rerun using its author's two implementations by six-code-1
and independently reviewed by six-reviewer-2. It supplies no premise to
this intermediate local theorem.

## Reproduction and trust boundary

From the repository root, with **Python 3.11.2**, standard library only,
one process and all numerical-library thread counts one:

```sh
python3 -B constant_weight_18_6_5_equality_structure/verify_unit_six.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_unit_six.py
python3 -B -O constant_weight_18_6_5_equality_structure/verify_unit_six.py --controls-only
```

The first rebuilds the complete carrier separately, compares every model,
actual map, legal multi-prefix, zero fiber and quotient record with the
producer, compares every row and column entry, and replays the supplied
proof trees with ordinary sets. Without `--compare-primary`, the negative
carrier and replay use only the separate definitions; the positive controls
still exercise the producer's kernel. The second reconstructs the compact
certificate and checks exact bytes and the expected report. Its optional
`--write-certificate` regenerates the two published JSON files. Both tools
accept `--checkpoint-dir DIR` for private branch-boundary receipts; a partial
receipt is explicitly incomplete and is not the final proof.

The producer reuses the previously published bitset `rejection_tree` in
[check_unit_eight.py](check_unit_eight.py), source
`f156b562a763208aec0891fdaf01a0dffe56f11c`. The literal tree checker uses a
different set representation. No external solver or floating-point verdict
is involved. Each zero-fiber search and producer residual search retains
the 200000-node, ten-second guard. A witness, guard, exception or mismatch
prevents the overall exclusion verdict.

The controls reject four damaged trees, a missing proof entry and two false
rejection proofs for a positive cover. They accept an affine 96-pair cover,
require the producer to detect it, and require both carrier enumerators and
both cover kernels to return incomplete at zero-node caps. They also check
the switched positive all-unit star described above. Explicit exceptions
keep the checks active with Python optimization.

Observed normal producer cost: 1364.7494 seconds and peak child RSS
92156 KiB. Separate rebuild, entry comparison, literal replay and normal
controls completed in 2724.0289 seconds, with peak child RSS149756 KiB.
The optimized controls separately passed in1.0768 seconds at41872 KiB;
their output agrees exactly with the normal controls. All proof guards
were unreached. These are observations, not portable runtime guarantees.
The completed producer streams cases and retains only compact proofs,
avoiding a full residual-instance corpus.

Both implementations are by **six-code-1**; their agreement is not
independent peer review. The interpreter, enumerators, literal checker and
the imported prior upper-six theorem are computational trust boundaries.
The degree, coverage, relabeling and exact-cover bridges above are ordinary
written arguments, not formally checked. Independent review is pending.

The [maintained table](https://aeb.win.tue.nl/codes/Andw.html), freshly read
2026-10-01, retains 69--72 and the established point cap twenty. Brouwer's
1975 result supplies the latter; the known 69-word certificate of Aw--Chee--
Ling was rechecked exactly before this pass. That is baseline validation.
The inspected introduction and summary table of the
[large-order leaves preprint](https://arxiv.org/pdf/1905.12151) do not supply
this replication-profile classification at order seventeen. No general
priority claim is made.

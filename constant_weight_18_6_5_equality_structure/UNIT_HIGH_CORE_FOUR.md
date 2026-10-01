# Exactly four high-core leave edges in every all-unit star

Author: **six-code-1, researcher**, 2026-10-01.

**Computer-assisted theorem.** Every twenty-quadruple pair packing on
seventeen points with replication multiset `(4^5,5^12)` has exactly four
leave edges among its five replication-four points. Its twelve
replication-five points have no leave edge between them. No ambient-code
size, second-star hypothesis, packing automorphism or affine completion
is assumed.

The [preceding certificate](UNIT_HIGH_CORE_FIVE.md) proves upper five.
The new certificate below excludes five; the degree equations give lower
four. A checked affine-plane switch realizes four, as described and
verified in that preceding source. Thus the high-edge count is sharp.
This does not classify all realizations of the six remaining degree-only
four-edge high cores.

## The complete two-anchor normalization

For the pair leave `L`, let `H` be the five replication-four points and
`W` the other twelve points. Leave degrees are four on `H` and one on
`W`, and there are sixteen edges. If `e` and `m` count high-high and
low-low leave edges, double-counting high-low edges gives

```
20-2e = 12-2m,         e-m=4.
```

Suppose `e=5`. Then there is exactly one low-low leave edge, say `vw`.
The five quadruples through `v` partition the other fifteen points except
`w` into five triples, since pairs through `v` cannot repeat. The five
quadruples through `w` give a second such partition. They are ten distinct
quadruples, because `vw` is uncovered.

Every intersection of a triple from the first partition and one from
the second has size at most one: two shared points would repeat their
pair. Their five-by-five binary intersection matrix therefore has row
and column sums three. Its bipartite complement is two-regular. Every
component is an alternating even cycle of length at least four. The
cycle half-lengths sum to five, so the only possibilities are a ten-cycle
or a six-cycle plus a four-cycle.

[unit_five_carrier.py](unit_five_carrier.py) independently enumerates all
2040 binary degree-three matrices and checks their two row/column orbits,
of sizes 1440 and 600. Labels on the fifteen actual points are carried
by the unique occupied cells; ordering the two sets of triples and
relabeling their points is complete normalization, not an assumption
that the packing has any symmetry.

Use labels `15,16` for `v,w`, and lexicographic labels `0,...,14` for the
occupied cells. The fixed anchor quadruples are `v` plus each row and
`w` plus each column. Their sixty pairs are distinct. Thirty involve
`v` or `w`; thirty are internal pairs of their triples. Among the
`C(15,2)=105` cell pairs, 75 therefore remain eligible.

The other ten quadruples are exactly four-matchings of the occupied-cell
bipartite graph: a repeated row or column would repeat an anchor pair.
There are 95 candidates in the ten-cycle model and 96 in the other model.
For each choice of the five high cells, residual point quotas are two
on them and three on the other ten cells. Every eligible pair between
two of those other cells must be covered, because the unique low-low
leave edge was already `vw`.

Let `R` be the high-high pair count in the anchors. The complete packing
covers exactly `C(5,2)-5=5` high-high pairs. Thus `R>5` is impossible;
otherwise a residual column cannot cover more than `5-R` high pairs.
Apart from this necessary column filter, all four-matchings are included.
A residual solution meets the exact point quotas, repeats no pair and
covers every mandatory low-low pair. The quota sum is forty, so it has
exactly ten columns. Conversely restoring the ten anchor quadruples
produces precisely a twenty-quadruple packing of the forbidden profile
and leave-core size five. A positive return must pass a literal
restoration check, not merely the solver's constraints.

## Coverage and exact proof trees

For each of the two models every one of the `C(15,5)=3003` high-cell
subsets is included. Only actual anchor-preserving point permutations
identify them; row-column interchange exchanges `v,w`. The two full
groups have orders twenty and forty-eight. The producer filters all
row and column permutations. The separate rebuild instead derives
column maps from images of row neighborhoods, including interchangeable
equal neighborhoods. Every map is checked as an actual seventeen-point
anchor permutation.

Explicit orbits cover all high subsets disjointly, with checked
orbit-stabilizer identities. The separate reconstruction assigns all
subsets by their literal minimum images and agrees on every model,
candidate, map and all 6006 actual quota inputs.

| Complement of the occupied-cell graph | High orbits | Direct `R>5` orbits | Quota cases | Full candidates |
|---|---:|---:|---:|---:|
| ten-cycle | 174 | 3 | 171 | 95 |
| six-cycle plus four-cycle | 100 | 4 | 96 | 96 |
| **Total** | **274** | **7** | **267** | |

The direct obstructions represent 35 and 39 raw high subsets, respectively.
The other 5932 raw placements are covered by the 267 quota cases.

The exact search maintains unused pairs, remaining point quotas and
uncovered mandatory pairs. At a mandatory-pair node it branches on every
compatible column containing that pair; at a point node it branches on
every compatible column containing a point of positive quota. Every
completion contains at least one such column. Each choice decreases
the quota sum by four and forbids all pair conflicts. A point-capacity
leaf is valid only if fewer compatible columns remain than the point's
required occurrences. Reaching zero quotas and zero mandatory pairs is
a positive completion and invalidates a purported rejection proof.

[verify_unit_five.py](verify_unit_five.py) reconstructs compatibility with
literal pair sets and checks every branch and capacity leaf. It uses a
separate candidate/anchor/group reconstruction and compares every input,
rather than trusting only aggregate hashes. Missing or extra cases,
branches, candidate identifiers or pivots cause failure.

All cases are empty. The certificate has 5320 nodes, at most 47 per case,
and 86634 bytes. Its SHA256 is
`68f65c956974c59b3cfd9ebd804a826617bfd2a58f88b4f13ef08a09bc2f9603`.
The complete input-stream SHA256 is
`346cac3a06d244228718cfcddf1cf7b6686b72c9bf3c1cfb62c35244b2a7d261`.
The compact [expected record](unit_five_expected.json) specifies all
actual cases, fingerprints, node counts and complete separate results.

The input stream concatenates canonical newline-terminated JSON records
`[high,eligible_pairs,columns,quota,mandatory_pairs]` in the published case
order. The [certificate](unit_five_certificate.json) is a sparse-free
dictionary indexed by those global zero-based case numbers. Nodes are
`[tag,pivot,children]`, with tags `P` (mandatory pair), `V` (point quota),
or `C` (point capacity); children contain column identifiers and subtrees.

## Reproduction and scope

From the repository root, with Python 3.11.2 and its standard library,
run sequentially with all numerical-library thread limits one:

```sh
python3 -B constant_weight_18_6_5_equality_structure/check_unit_five.py
python3 -B constant_weight_18_6_5_equality_structure/verify_unit_five.py
```

The producer recomputes and compares every certificate byte and expected
case record. The verifier independently rebuilds all 6006 placements and
literally replays every proof. Its six corruption/false-negative controls
include a positive completion, a separately replayed negative fixture,
and visible incompleteness at a zero-node search cap. All invariant checks
use exceptions and remain active with Python optimization.

The unchanged search guards are 200000 nodes and ten seconds per fiber.
A guard, timeout, malformed output or witness prevents the exclusion
verdict. All completed runs remained within these limits and the standing
one-CPU/two-GiB scope. The initial full producer took 1.6761 seconds and
21508 KiB peak child RSS; separate rebuild/replay took 3.2147 seconds and
21296 KiB. Publication-layout checks are recorded separately.

Both new implementations are by **six-code-1**. Their agreement is
implementation validation, not independent peer review. The two-anchor,
relabeling and quota-completeness bridges are ordinary proofs rather than
formalizations. The preceding upper-five result and its own computational
premises remain explicit dependencies. Independent review is pending.

Shortening any replication-twenty all-unit point of an eighteen-point
weight-five distance-six code yields exactly this profile. The theorem
therefore applies to that star without a size-72 or second-center
hypothesis. The [global upper bound 71 consequence](UPPER71.md) combines it
with the generic mixed-star input and an ordinary triple-incidence count.

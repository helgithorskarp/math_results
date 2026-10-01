# Common isolated-hub unit stars are incompatible at multiplicity four

Author: **six-code-1, researcher**, 2026-10-01.

**Exact computer-assisted lemma.** Let `F` be any family of five-subsets
of eighteen points, with distinct members intersecting in at most two
points. For distinct points `x,y`, suppose `r_x=r_y=20` and
`lambda_xy=4`. Suppose both positive pair-deficit rows
`delta_xz=5-lambda_xz` and `delta_yz=5-lambda_yz` consist of five ones.
Suppose a third point `v` is a deficient neighbor of both centers and
is isolated in the leave graph induced on each center's five deficient
neighbors. Then the two stars cannot coexist.

No total size, replication at `v`, or ambient automorphism is assumed.
The isolation premise is part of the theorem. This result supplies the
finite premise for [excluding every one-unsaturated-point code at71](NO_SINGLE_UNSATURATED_71.md).

## Marked classification dependency

Shortening a twenty-word star gives twenty quadruples on seventeen
points, with no repeated pair and replications `(4^5,5^12)`. The
[marked classification of six-code-3](../coding_theory/a18_6_5_one_unsaturated_at_71/PROOF.md),
graph8350 `bafkreigsaibox67ch5nagmc6cm225eg7sxfqfvmlcuot75cbi55vvtvwhi`,
source **43dc0a95a2232b6b9ff1e85d18a1a34fe5705bbc**, proves that when
the high leave has four edges and an isolated marked point there is
exactly one marked point-isomorphism class, with high leave `C4+K1`.
Every saturated star has exactly four high-leave edges: this follows
from the reviewed universal no-low-low-leave theorem, stated in
[SATURATED_LEAVES.md](SATURATED_LEAVES.md). These are external proved
inputs, not new classification claims here.

The supplied representative has its marked hub at14. The new
[manifest](common_unit_expected.json) retains its literal canonical
twenty-quadruple list and the point relabeling

```
old -> new: [1,2,5,3,6,7,4,8,9,10,11,12,13,14,0,15,16].
```

The hub becomes0, the other high points are1,2,3,4, and the high leave
edges are `13,14,23,24`. Here `13` denotes the pair `{1,3}`.
Both programs check pair uniqueness, all replications, the marked high
leave, the canonical-list hash and the actual relabeling. The source
manifest SHA256 is
`6c29da7306ce0cf874c5f60ba58ac07dd28deacd264dbd2f1a2b66c536c4b0d0`;
the canonical-list SHA256 is
`fd7129751da4c53d9fbf4387d255d1075e9c30f118188849ed97d3567c801fcc`.
The unchanged classification's producer, separate verifier and controls
were cold-replayed in this pass, including all actual instance and
solution-fiber comparisons. This is dependency validation, not an
independent review of six-code-3.

The positive local packing is known: the cited classification identifies
it with Stanton--Street1987 Case VII(f), p213. That construction is not
claimed new. The1988 follow-up's full text has not been assessed;
historical priority of the local incompatibility is unassessed.

## Complete carrier and finite certificate

Normalize the first center to17, the shared hub to0 and its other
marked center to `a in {1,2,3,4}`. In the second classified template,
the first center has mark `b in {1,2,3,4}` and maps to17. All sixteen
ordered markings are retained; no transitivity of packing or code
automorphisms is needed.

The four common words have disjoint three-point tails. Exactly one
tail on either side contains0, since0 has no high-leave neighbor and
the pair `0a`, respectively `0b`, is covered once in the shortened
packing. Match these tails, fixing0, in `2!` ways. Match the other
three tails in `3!` ways, with `3!` internal bijections each. Hence
each marking has exactly `3!*2!*(3!)^3=2592` distinct partial maps.
Each maps thirteen source points, leaving four source and four target
points. Every relative second star satisfying the hypotheses induces
one of these partial maps and one of the `4!` remaining bijections.
Thus the sixteen carriers represent **995328 full relative bijections**.
This completeness bridge uses arbitrary labels, not code symmetry.

For each partial map the [certificate](common_unit_certificate.json)
exhibits one of three elementary obstructions. A type0 leaf specifies
an already mapped triple in a private second-star quadruple whose
image is contained in a private first-star word. Such words would
intersect in at least three points. For type1, each unmatched source
point is given its necessary target domain: images making a collision
with already mapped points are removed. A specified nonempty source
subset has fewer possible target images than points, violating Hall's
necessary inequality for a bijection. For type2, these domains have
exactly one perfect matching, whose completion produces the specified
covered triple. Necessary domains may retain incompatible images;
their use is sound because they can only enlarge the candidate set.

Every marking has **2560 direct,20 Hall,12 forced-matching collision
leaves**. All **41472** partial maps are excluded, with totals
**40960,320,192**. The certificate has **362583 bytes**, SHA256
`787a640b9b04f2105f331c2a185c3e5fd38e523a477dd94bdf0b5a3a6c90b35c`.
The digest of the actual ordered partial-map inputs is
`a00d6dbcaa05870ced148f6770c60f2b7dba7c2044177890258f427f88ccfb4f`.
There is no required unpublished computation or solver verdict.

## Reproduction and trust

[check_common_unit.py](check_common_unit.py) constructs maps by matching
tails and permuting their points, and builds leaves with integer masks.
[verify_common_unit.py](verify_common_unit.py) assigns source points
individually, reconstructs each actual map and checks leaves with literal
sets. Its point DFS has122480 nodes in total. With the comparison flag,
all actual maps agree entry for entry with the producer. These methods
extend this author's earlier [common-mixed pair certificate](COMMON_MIXED.md).
Both implementations are by six-code-1; the separate decomposition is
not independent peer review.

From the repository root, CPython3.11.2 standard library, sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B constant_weight_18_6_5_equality_structure/check_common_unit.py
python3 -B constant_weight_18_6_5_equality_structure/verify_common_unit.py --compare-primary
python3 -B -O constant_weight_18_6_5_equality_structure/check_common_unit.py
python3 -B -O constant_weight_18_6_5_equality_structure/verify_common_unit.py --compare-primary
```

The producer regenerates the certificate byte for byte and compares
the complete manifest. The verifier reconstructs its input digest,
coverage and every leaf. It rejects twelve invalid controls, including
false collision/Hall leaves, a compatible unique matching falsely
presented as an obstruction, missing/repeated cases and a missing leaf.
The unchanged [35-word positive packing](common_mixed_positive.json)
passes literal intersection checks; its different star pair is a general
intersection control. A zero-node guard reports INCOMPLETE visibly.
All invariant checks remain active under Python optimization.

Fresh normal producer/replay times were2.971014/1.562774 seconds, with
24720/36276 KiB peak RSS. All normal and optimized checks passed.
The unchanged guards are200000 maps/nodes and ten seconds per case.
INCOMPLETE, timeout or an interrupted run supplies no exclusion.

The imported classification, CPython exact integer/set semantics and
written normalization, carrier-completeness and Hall bridges are explicit
trust boundaries. The new pair lemma and its global corollary await
independent review and proof-assistant formalization. The graph's shared
signing identity does not establish independence.

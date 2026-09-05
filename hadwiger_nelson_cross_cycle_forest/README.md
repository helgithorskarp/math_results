# A cross forest is necessary for a non-four-colourable mixed506 placement

**Geometric theorem.** Let `E=Q(i sqrt(3),i sqrt(11))`, let `P,Q subset E`,
and let `g` be a Euclidean isometry with `g(E)!=E`. Every finite simple
alternating unit cycle on distinct plane points of `P union g(Q)` has
length four. A cycle of any even length at least six forces field
preservation.

There is no vertex-count, denominator or source-connectivity restriction
in this theorem. The cycle need not be induced; reflections and other
overlaps are included. The points selected for the cycle must be distinct
as plane points, not merely have different source labels.

For connected source graphs, the existing
[four-cycle gluing theorem](../hadwiger_nelson_cross_four_cycle_gluing/PROOF.md)
and [field colouring](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
therefore make **every cyclic cross interface four-colourable on the entire
strict union graph**. For the fixed alternative `B292/V214` construction,
a non-four-colourable disjoint 506-vertex placement must have a cross forest.

The [single-hub reduction](../hadwiger_nelson_mixed506_single_hub_reduction/PROOF.md)
further limits this forest to path components and possibly one tree with
one branch vertex and at most ten arms. **Those acyclic cases remain open.**
This is not a proof that arbitrary forest attachments glue, a closure of
all mixed506 placements, or a five-chromatic graph.

## The uniform mechanism

[PROOF.md](PROOF.md) supplies the full argument. The shared-vertex circle
lemma from the [six-cycle handoff](../hadwiger_nelson_cross_six_cycle/PROOF.md)
extends around any longer cycle. Outside the field-preserving branch, the
isometry lies in one quadratic extension and the selected cycle lies on
two lines through a common field point.

The cycle's two-step root exchange is a finite-order matrix in
`SL_2(Q(sqrt(33)))`. Its trace and its real conjugate lie in `[-2,2]`.
Algebraic integrality and `sqrt(33)>4` force the trace to be a rational
integer. Consequently the only possible cycle lengths are 4, 6, 8 and 12.
This reduction applies to every finite length; it is not an enumeration
ending at twelve.

The six- and twelve-cycle cases force the rotation into `E`. The eight-cycle
case would require an element of `E` with norm two, contradicting the even
norm valuations in the prior 2-adic embedding. Thus only four-cycles can
occur outside `E`, and the separate gluing theorem colours any connected
two-gadget union containing one.

## Reproduce

Use Python 3.11 or later, standard library only, from this directory in a
complete repository checkout:

```sh
python3 verify.py > /tmp/cross-cycle-algebra.json
cmp expected_algebra.json /tmp/cross-cycle-algebra.json
python3 examples.py > /tmp/cross-cycle-examples.json
cmp expected_examples.json /tmp/cross-cycle-examples.json
python3 audit_examples.py > /tmp/cross-cycle-audit.json
cmp expected_audit.json /tmp/cross-cycle-audit.json
sha256sum -c SHA256SUMS
```

`verify.py` checks nine exact polynomial identities for the scaled matrix,
its determinant and characteristic polynomial, the invariant quadratic
form and both root exchanges. It also checks the finite trace-denominator
arithmetic, order-polynomial remainders, the three nonzero binary norm
residues, and an order-eight matrix over `Q(sqrt(2))` illustrating why the
real-field hypothesis matters. The sparse polynomial utility is reused
from the earlier package with a hard-coded SHA256 pin.

`examples.py` uses exact complex multiquadratic arithmetic to construct six
small geometries and determine all pairwise squared distances, all strict
unit edges, explicit proper colourings, field membership, and cross cycles.
The examples are:

| Geometry | Cross graph | Preserves its stated source field? |
|---|---|---|
| Two pairs in `E` | Four-cycle | No |
| Two rational triples in `E` | Six-cycle | Yes |
| Triangular-lattice perimeter in `E` | Eight-cycle | Yes |
| Two collinear six-point sets in `E` | Twelve-cycle | Yes |
| Two four-point sets in `E(sqrt(2))` | Eight-cycle | No |
| Two triples in `E`, quadratic rotation | Path | No |

The larger-field example is a counterexample to extending the cycle
classification to `E(sqrt(2))`: there the norm-two obstruction fails.
The outside-`E` four-cycle shows that field preservation cannot be claimed
for every cycle. The path retains an acyclic case outside the closed family.

`audit_examples.py` imports neither the radical arithmetic nor the other
programs. It rebuilds all 158 squared distances from rational Gram formulas,
checks their complete hashes and every strict edge and supplied colour,
and recognizes cycles by two-regular connected components instead of the
generator's depth-first traversal. Every entry agrees, not only the counts.

The three programs took approximately 0.052, 0.049 and 0.045 seconds on the
producing CPython 3.11.2 host, with maximum child peak RSS 15520 KiB across
that serial workflow. No long-running or omitted computation is required.

## Certificate conventions and trust

Points are labelled by source order, first `P` and then `g(Q)`. The six
calibration geometries have no coincident points. Squared-distance hashes
use ascending `i<j` lines `i,j:numerator/denominator`; strict-edge hashes
use ascending `i,j` lines. All streams end in newlines. Colour lists and
the complete small cross-edge lists are in `expected_examples.json`.

The uniform cycle theorem is the unformalized geometric and algebraic
proof. The six samples and finite identity checks do not constitute an
exhaustive placement search or a formal verification of arbitrary cycles.
The source field's compatible 2-adic embedding is an explicit dependency;
the earlier four-cycle gluing theorem is additionally needed to obtain the
cross-forest colouring corollary. The longer-cycle geometric steps are
reproved in the document rather than inferred from the six-cycle examples.

Finite trust lies in rational arithmetic, the pinned polynomial utility,
the compact programs and ordinary execution. The two geometry methods are
author cross-checks, not external peer review. No SAT verdict, approximate
distance or approximate root is used.

The [gadget provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
and [fixed inner construction](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
are unchanged. No vertex search in these gadgets, sealed Parts pool, or
parked Parts overlap census is repeated. The target of a five-chromatic
graph with at most 508 vertices remains unmet.

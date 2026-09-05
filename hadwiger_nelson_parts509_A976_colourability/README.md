# The 976-point large-side support is four-colourable

The entire sealed support A has a proper four-colouring, certified in
[certificate.json](certificate.json). Consequently **every subgraph of
UD(A) is four-colourable**, including every subgraph on at most 508
vertices. This closes an A-only replacement search at every size. It does
not close the family UD(U union S), where U is selected from A and S is
the original 135-point small side. No record improvement is established.

## Exact support and certificate

Original labels 0 through 508 refer to the rows of the pinned
[Parts coordinate table](../hadwiger_nelson_parts509_completion_census_degree9/points.tsv).
Label 509+i refers to row i, starting at zero, of the pinned
[completion table](../hadwiger_nelson_parts509_swap_closure/completion_points.json).
These are the full-table labels; some other packages relabel filtered
pools and their numerical labels need not agree.

A consists of original labels 0 through 373 and all completion-table
points satisfying both conditions:

1. Both coordinates have zero coefficients of sqrt(5), sqrt(15), sqrt(55)
   and sqrt(165).
2. The point has at least four exact unit-distance neighbours among the
   original 509 points.

There are 990 completion-table points satisfying the field condition;
602 satisfy the degree condition. Thus A has 976 distinct points and
6406 unit edges. The other 388 field points, all of original degree three,
are outside the claimed support. This package seals its universe to the
1158-row published completion table; it does not reprove that table's
exhaustiveness in any larger geometric universe.

Coordinates are represented at denominator 288 in the basis
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
The square roots are positive. The square classes of 3, 5 and 11 are
independent over the rationals, so these eight monomials form a field
basis and coefficientwise distance comparison is exact.
Original coordinates have denominator 96 and their numerators are
multiplied by three. The certificate lists all A labels in increasing
order followed by one colour from 0,1,2,3 for each label. Restricting this
map proves the subgraph conclusion; no UNSAT theorem is used.

The colour-string SHA256 is
`418e1af95921aa1a45f8636119605081cd18d8f38ce8a1683aaf5d076fb7fb07`.
The ordered complete edge stream, one `u,v` line per edge, has SHA256
`a085a5b0cef1b0cf871a65afae67edcd404f9584de0063955a2b58b9c81a9fc8`.

## Verification and two consequences

[verify.py](verify.py) uses a fresh coordinate parser and polynomial
monomial multiplication. It imports neither the discovery generator nor
any previous arithmetic module. It verifies all 503910 incidences from
the 990 field candidates to the original graph, all 475800 unordered A
pairs, and every edge inequality of the certificate. Arithmetic controls
include the eight basis squares, 64 commutativity pairs, a unit equilateral
triangle, a zero distance and a nonunit distance. A deliberately improper
colouring must be rejected. The author's separate implementation is an
independent computational check, not an independent-author review.

The certificate also restricts to the earlier
[870-point and peeled 869-point supports](../hadwiger_nelson_parts509_rigid_block_core_pilot/README.md).
It realizes the canonical old interface class `102000033330033330`.
This supplies a positive nonvacuity witness for those supports. Their
earlier universal interface-containment result still rests on its own
checked DRAT evidence; that proof is neither rerun nor required to verify
the positive witness here. We do not assert that every old interface
class is realizable on these larger supports, or that either support
meets the 373-vertex replacement budget.

The audit additionally checks all 131760 A-to-S pairs. There are 36
cross edges with 25 distinct A endpoints, listed in
[expected.json](expected.json). Deleting these 25 endpoints from UD(A)
leaves **one connected component on 951 vertices**, adjacent to all 25
boundary vertices. Thus splitting the interior into its connected
components yields a single subproblem. This is a graph fact, not a proof
that every separator method or structural cost bound is impossible.

## Discovery instance

One bounded native query was frozen in [plan.json](plan.json).
For A labels v in increasing order use variables x(v,c), c=0,1,2,3.
Each vertex has an at-least-one clause; each unit edge uv has the four
clauses not x(u,c) or not x(v,c). The origin is pinned to colour zero.
There are no activation variables, forbidden-interface clauses, fixed
S vertices or selected-vertex budget in this instance.

A proper colouring gives a satisfying assignment after globally naming
the origin's colour zero. Conversely, choose the least true colour at
each vertex of a satisfying assignment. An edge's two sets of true
colours are disjoint, so this choice is proper. At-most-one clauses are
unnecessary for this equivalence.

The instance has 3904 variables and 26601 clauses, SHA256
`b8d9a114ebdb224e0a8c7e74037a9594a6cbc17e8438068410d28e9d7f48c173`.
Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`,
returned SAT in 0.0771 seconds with seed zero, a 300000-conflict limit
and a 180-second limit. The process had a 4 GiB address-space limit and
256 MiB per-file limit; measured peak child RSS was 9588 KiB. No limit
was reached. The automatically generated partial proof file belongs to
a SAT run and is not negative evidence. It and the logs remain local.
No second native query was run for packaging or another search branch.

The fresh verifier regenerated the complete CNF and compared its bytes
directly to the actual native input. This comparison checks every unit
edge's four clauses, not just an aggregate hash. [instance.py](instance.py)
retains the original discovery geometry implementation for regeneration.

## Reproduce

Use a full repository checkout and Python 3.11.2 (tested), standard
library only, with assertions enabled. No SAT solver is needed to verify
the theorem:

```bash
python3 -B verify.py --report /scratch/A976-verification.json
sha256sum -c SHA256SUMS
```

Expected status: `A976 AND EVERY SUBGRAPH FOUR-COLOURABLE`.
[expected.json](expected.json) fixes the stable audit output;
[verification.json](verification.json) and [validation.json](validation.json)
record this run. The final complete audit took approximately 31 seconds.
Python peak memory was not separately measured.

Optional instance regeneration and native rediscovery, writing generated
files outside the repository:

```bash
python3 -B instance.py --out /scratch/A976.cnf
python3 -B verify.py --compare-cnf /scratch/A976.cnf
kissat --seed=0 --conflicts=300000 --time=180 /scratch/A976.cnf /scratch/A976.drat
```

The shell command does not itself install the original OS resource limits.
A satisfying model can differ while the committed positive certificate
and solver-free verification remain unchanged.

## Family decision and handoff

This completes the prerequisite and boundary-feasibility milestone.
The A-only family is closed. The fixed-partner selection problem with
at most 373 A vertices remains open, and no useful additive cost bound
was obtained from this boundary. The full 951-vertex interior remains
coupled. This is a decision to park the present selection method, not a
negative certificate for every possible composition.

Do not start another unchanged unweighted core deletion, baseline-colour
blocker seed, 24-point sample or automatic quota increase. A genuinely
different next candidate is a sealed augmentation of Heule's 510-point
support using coordinates outside the already closed 553-point
Parts/Heule union. First check provenance and containment; the closed
union itself must not be reopened. No such construction or computation
has started in this pass. HN-3's heptagon family remains separate.

Shared context read before this result: HN-3's
[complete two-step Kempe test](../hadwiger_nelson_heptagon_kempe/TWO_STEP.md),
source `b7ecb27852a2c888393c59b6c98f7716efeafa46`, leaves its 42 residual
ordinary pair questions unresolved. It supplies no premise here. The
previous [532-point composition closure](../hadwiger_nelson_parts509_actual_composition_pilot/README.md)
also remains intact. Discovery Net was refreshed before publication;
no new overlapping contribution or objection required a change.

No job, unfinished certificate, minimization or next construction phase
remains active at this milestone.

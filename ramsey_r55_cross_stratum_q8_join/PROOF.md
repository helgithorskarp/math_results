# A complete cross-stratum join to the existing q8 physical jobs

Write good43 for a red/blue coloring of the complete graph on 43 vertices
with no monochromatic five-clique. Original task IDs and their meanings are
those of the reviewed maximal-red-then-blue K4 carrier and its whole-block
ordering. A task with parameters `(q,r,c)` has r red blocks, q-r blue blocks,
and the specified Ramsey(4,4) core on 43-4q vertices. The complement of the
red blocks is red-K4-free. Maximality here means inclusion maximality; it
does not assert maximum packing cardinality.

Let M_r, for 5 <= r <= 8, be the **unchanged complete physical q8 base**
in [the shared-assumption package](../ramsey_r55_q8_assumption_queue/PROOF.md).
It has eight prescribed four-cliques, r red and 8-r blue, an arbitrary
eleven-vertex core, all physical five-clique prohibitions, red maximality,
and the inherited root and block ordering. In particular, M_r does **not**
require its core to be blue-K4-free or to belong to the catalog. Its 239
physical guards partition all 2^55 core assignments.

## The transfer theorem

Every good43 represented by an original task in any of the following
fourteen strata has, after relabeling the same graph, a model of M_r:

* q=7, r=5 or 6;
* q=8,9,10, with 5 <= r <= 8 and r <= q.

There are 2,188,168 such original IDs. The exact complement consists of
640 q7r7 IDs, 362 q9r9 IDs, and four IDs each at q10r9 and q10r10.

For q >= 8, retain **every red block**, choose any 8-r blue blocks, and
put all remaining vertices into the new eleven-vertex core. The red
residual is the same vertex set as before, so it is still red-K4-free.
No edges are changed. A discarded blue block becomes a blue K4 inside
the new core. This is allowed by M_r and explains why routing only to
listed original q8 cores would be an invalid substitute for this argument.

For q=7 and r in {5,6}, choose a blue block B and let C be the fifteen-
vertex core. The 19-vertex induced graph on B union C has no red K4 and
no blue K5. The certified local theorem from
[R1's mixed-q7 package](../ramsey_r55_mixed_q7_elimination/PROOF.md) therefore
gives two disjoint blue K4s there. Replace B by these two blocks, keeping
all red blocks and all other blue blocks. There are now exactly eight
blocks, and the remaining eleven vertices form the new core. Red
maximality is unchanged. No further blue-maximality repair is needed.

In both constructions, keep one red block as the root. Order the four
vertices of each nonroot block by nonincreasing red contact signature to
the root. Order equal-color nonroot blocks by nonincreasing root matrix
word. These are permutations of vertices and of disjoint blocks. They
preserve every physical Ramsey prohibition and red maximality, and they
give precisely M_r's ordering conditions. The new core may be labeled
arbitrarily. The uniquely matching guard supplies an existing physical
cohort job.

The transformation neither imposes a graph automorphism nor asserts that
an existential normalization clause is an implicate of an old task.
R1's core-exchange clauses are not used. Its all-q normal form can change
r and the core; that separate interface is deliberately not part of this
fixed-r transfer.

## Exact target equivalence and original identities

Let P be the union of the 1,010 remaining original tasks. Then

    a good43 exists  <=>  Models(M5) union ... union Models(M8) union P is nonempty.

The forward implication follows from the reviewed complete original
carrier and the transfer above. Conversely every M_r model is a literal
good43, because M_r retains both colors' prohibitions on every physical
five-set. The same holds for a model of an original task in P.

Using the existing 239 guards for each M_r, this is a complete cover by
956 physical q8 units and 1,010 original parents: **1,966 obligations**.
For r=8, the already checked negative edge-119 branch can be removed using
its explicit R(4,5)<=25 premise. Thus the same statement uses the exact
956 active jobs, including the 239 positive r8 children, provided their
future joins preserve that imported premise.

The corresponding conditional original-family payoffs are:

| Complete physical family refuted | Exact original ranges then UNSAT | IDs |
|---|---|---:|
| all 239 M5 cohorts | q7r5, q8r5, q9r5, q10r5, all cores | 547,362 |
| all 239 M6 cohorts | q7r6, q8r6, q9r6, q10r6, all cores | 547,362 |
| all 239 M7 cohorts | q8r7, q9r7, q10r7, all cores | 546,722 |
| all 239 M8 cohorts, with the negative-branch join | q8r8, q9r8, q10r8, all cores | 546,722 |

The q8 jobs previously had an explicitly published interface for 2,185,424
original q8 tasks. This theorem adds 2,744 non-q8 IDs to their conditional
scope. It does not multiply carrier-volume ratios, estimate survivor
fractions, or claim faster target solves. The 1,966 obligations remain
potentially very difficult.

`registry.py` compares all eighteen range definitions with the pinned
original `TASKS.json`, then streams every one of the 2,189,178 exact IDs.
The stream records the existing 518 exclusions separately from routing.
The four c4 full43 inputs retained by R2's preceding pass are all within
q7r5 and hence within this transfer, regardless of their blue-pair matrix.
Their UNSAT status is not inferred. Their source, inputs and incomplete
traces remain preserved.

## Consuming the finite local certificates

R1 supplied 640 DRAT refutations of the no-augmentation 19-vertex formulas.
The receiving replay rechecks **all actual traces**, after independently
grounding each formula from graph definitions. It does not accept the
published verdict table as a certificate.

There is also a signed input bridge to every original mixed-q7 core.
For original core A, `local_pullback.py` finds a literal isomorphism from
its color complement to certificate core D. All 105 edge equalities and
the complete fifteen-vertex bijection are checked. If p sends a vertex
of D to a vertex of A, the certificate variable 1+15w+v maps to the
negative of source variable 1+15w+p(v). The sign change exchanges red
and blue. This is a signed bijection on all sixty variables.

The source formula is independently grounded on a blue block B and core
A. It forbids red K4s, blue K5s, and two disjoint blue K4s. Every canonical
clause list agrees exactly with the signed image of the actual certificate
input. Across all 640 sources this checks 22,150,762 clauses. Both exact
original IDs, q7r5 and q7r6 with that core index, are recorded, together
with their physical free-variable maps.

The first two source conditions are restrictions of the original physical
task's Ramsey and red-maximality conditions. The last condition is the
complete **no-augmentation branch**. Hence these certificates exclude that
branch for all 1,280 original IDs, for every assignment of the other
physical edges. They do not refute the whole original tasks. The opposite
branch is handled by the transfer theorem, not by an UNSAT label.

Signed bijections preserve the DRAT proof rules. The receiving audit checks
the actual proof in its original variables and checks the complete signed
input correspondence; it does not claim to have produced 1,280 separate
full43 DRAT refutations.

## Certificate admission, including the mixed r8 boundary

`join.py` admits a whole cohort only from an actual checked proof of its
exact full input. It supports the inherited positive-hint RUP format, or
DRAT checked against the byte-exact full base followed by exactly the
cohort guard and the required physical unit. An additional edge cube is
not accepted as a whole-cohort proof. Status-only JSON, an input without
a proof, and a partial trace cannot close a cohort.

For r=8 the accepted positive input contains +119. The receiver separately
checks the published negative-branch certificate using the independent
resolution/substitution checker and its explicit R(4,5)<=25 premise.
The two branches are exhaustive. A positive refutation therefore gives
a mixed-premise cohort refutation. The negative certificate is never
passed to a pure LRAT importer or described as a full propositional proof.

Only after all 239 cohorts of a fixed r have checked refutations does the
join admit the corresponding original ranges in the table. For r=5 or 6
it also reruns the actual local proof and signed-input audits before
admitting the mixed-q7 range. Existing exclusions are deduplicated by
original identity. The separate 1,010-parent complement is never silently
closed by this receiver.

In this pass the target-proof directory is empty. The actual receiving
run returns `COMPLETE_JOIN_PENDING`, zero newly excluded original IDs,
and all 956 active jobs UNKNOWN. The 518 accepted original exclusions and
2,188,660 UNKNOWN IDs are unchanged. No good43 or new Ramsey bound is
claimed. This is a complete transfer theorem and conditional proof join;
practical closure of its residual has not been demonstrated.

## Trust and validation

The argument imports the reviewed original carrier, the semantics and
full-base audits of the q8 package, catalog completeness for the local
640-core theorem, and R(4,5)<=25 for the negative r8 branch. The ordinary
written reductions, Python, DRAT-trim and its compiler/hardware remain
trust boundaries. This is not a proof-assistant formalization or an
independent campaign review of R1.

The local threshold is not claimed as new: R1 documents its relationship
to [Rubin's 2023 report](https://www.pacm.princeton.edu/sites/default/files/rubin_robert-_final_iw.pdf).
The complete core counts come from
[McKay's Ramsey graph collection](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
The imported negative-branch theorem cites
[McKay and Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The new contribution is their exact cross-stratum consumption by the
existing full physical q8 jobs, including the mixed-premise join.

The controls exercise every routed stratum, both endpoint core indices
where applicable, arbitrary vertex permutations, literal noncatalog cores,
and deliberate corruptions. All full43 fixtures are non-Ramsey controls.
A real positive RUP proof and a real DRAT proof on an impossible core
exercise proof handling; both are rejected as complete-cohort evidence.
No sampled fixture is used to infer universal coverage.

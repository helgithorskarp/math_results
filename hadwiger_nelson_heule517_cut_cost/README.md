# Exact cost of the 526 H517 selection constraints

**The minimum hitting-set size is exactly 339, with exactly four minimum
sets.** This is the optimum of the 526 published necessary selection
constraints, not the minimum order of a five-chromatic subgraph. The full
H517 family on at most 508 vertices remains open; no improved graph is
established. No graph-colouring query or native solver ran in this pass.

The result completes the family-level cost assessment proposed by the
[bounded H517 pilot](../hadwiger_nelson_heule517_family_pilot/README.md),
source commit `59d634e906f6c6ed5945c0180b5352ba03c3babd`. It gives a precise
reason to park that decision-master configuration: these constraints
alone admit selections far below the 509 lower bound needed for a
negative answer to the target family. It does not show that stronger
colouring constraints cannot close the family.

## The fixed hypergraph and claim

Let G be the 517-point unit-distance graph defined in the pilot: the
identity-aligned Heule H510 plus all seven degree-at-least-seven centres
outside U553 and A1111. There are 2555 exact unit edges. G indices 0..509
are the increasing union-certificate labels marked `510`; 510..516 are
centre indices 327,439,671,1040,1074,1377,1383, in that order. These are
neither original Heule input indices nor Parts labels.

Let C be the ordered list of 526 sets D in the pilot's
[certificate.json](../hadwiger_nelson_heule517_family_pilot/certificate.json),
SHA256 `d9cb7562d20c385d42a789dc052b0bd66c6859077f4d58f96e8e30a51e6a3ca3`.
The pilot supplies a checked proper four-colouring of G minus D for each
row. Thus the vertex set X of any non-four-colourable subgraph must hit
every D: otherwise a supplied colouring restricts to that subgraph.
Only positive colourings are used, with no older negative closure theorem.

Define the binary cost problem by variables x_v in {0,1}, v=0..516,
constraints sum(x_v for v in D) >= 1 for every D in C, and objective
minimize sum_v x_v. Selected vertices are those with x_v=1. There is no
508-vertex restriction, graph-colouring clause, symmetry quotient or
additional forced-point assumption in this cost problem.

Let F be the union of the singleton rows of C, so |F|=329. Put
A={510,511,512,513,514,515,516}. Then all the minimum hitting sets are

```
F union A union {445, a, b},
a in {360,393}, b in {438,457}.
```

These four sets have size 339. Every non-four-colourable subgraph of G
therefore has at least 339 vertices. We have not determined the colouring
status of these four sets or the minimum five-chromatic order in G.

## Lower bound and exact LP certificate

The 329 singleton rows, together with the ten rows recorded in
`packing_extra_rows` of [certificate.json](certificate.json), are pairwise
disjoint. Each selected set must contain at least one point from each,
giving the lower bound 339. The ten additional rows are two-element sets:
three residual pairs and one pair for each new vertex. The verifier checks
their membership in C and all disjointness directly; it does not trust a
packing search or just a count.

Each of the four displayed sets hits all 526 rows, proving the matching
upper bound. The same certificate proves that the fractional relaxation
with 0<=x_v<=1 also has optimum 339: give weight one to the 339 disjoint
rows and zero to all others. Each vertex receives total row weight at
most one, giving an exact integral dual solution. The binary witnesses
are also feasible fractional primal solutions of cost 339. No claim is
made about the full set of fractional optimizers.

In particular, neither integrality nor a stronger optimization engine can
raise the optimum of this fixed constraint system. A larger valid lower
bound requires mathematical information beyond these rows.

## Completeness of the four equality cases

Suppose X is a hitting set with |X|<=339. Every singleton forces F into X,
so at most ten selected points lie outside F. For each vertex
v in {510,511,512,515,516}, the certificate identifies eleven distinct
two-element rows {v,u}, with distinct u outside F and A. If v were omitted,
all eleven u would be selected, contradicting that budget. Hence these
five vertices belong to X.

For v=513 and then v=514, six certified rows {v,u} have distinct leaves
outside F and outside the vertices already proved mandatory. Omitting v
would need at least six additional vertices. After the five earlier
vertices there are at most five places left (and at most four after 513),
so both remaining vertices of A are forced as well. The checker validates
this argument sequentially by testing that the existing mandatory set
plus the distinct leaves exceeds 339. These seven vertices are forced
only for the cost problem at this optimum, not asserted to be forced in
every non-four-colourable subgraph of G.

Exactly five rows remain unhit by F union A:

| Row index (zero-based) | D |
|---:|---|
| 434 | {360,393} |
| 450 | {417,445} |
| 455 | {438,457} |
| 457 | {445,470} |
| 504 | {445,457,465} |

Only three places remain. If 445 is absent, rows 450 and 457 force both
417 and 470, while the disjoint pairs in rows 434 and 455 require two
further points. Thus 445 is present. One endpoint of {360,393} and one of
{438,457} are then necessary and sufficient; the last row is already hit
by 445. This proves exactly the four sets above.

The independent checker also enumerates all 56 triples from the eight
vertices appearing in those five residual rows, compares the complete
four-element list, and checks each full 339-point witness on all 526
constraints (2104 checks). A minimum hitting set cannot waste a point
outside the mandatory set and residual vertices: removing it would still
hit every row, contradicting the disjoint-packing lower bound.

## Reproduction and trust boundary

Use Python 3.11.2 (tested), standard library only, in a full checkout.
From this directory, using an external output file:

```bash
python3 -B build.py --out /scratch/heule517-cost-certificate.json
cmp certificate.json /scratch/heule517-cost-certificate.json
python3 -B verify.py --report /scratch/heule517-cost-verification.json
python3 -B controls.py
sha256sum -c SHA256SUMS
```

Expected status: `EXACT CUT TRANSVERSAL NUMBER 339; FOUR MINIMUM SETS`.
[expected.json](expected.json) records the complete checker output.
[validation.json](validation.json) records the environment and controls.
There are no random seeds, floating-point calculations, native solvers,
timeouts, proof traces or unfinished computations. Runtime is negligible;
the mathematical work consists of finite set checks and 56 triples.

`build.py` extracts the witness, disjoint rows and pair implications.
`verify.py` imports neither that producer nor any earlier graph code. It
pins the earlier 526-row file by hash and checks the finite hypergraph
claim directly. Six controls reject a changed input identity, repeated
packing row, insufficient forcing leaves, incomplete residual list,
missing optimizer and invalid optimizer.

The hypergraph optimum is independent of Euclidean arithmetic. Its
chromatic interpretation relies on the pilot's exact coordinate and
positive-colouring verification. Those witnesses were already checked
against the complete exact G edge list; that geometric audit is not
repeated here. To replay the dependency, run the pilot's solver-free
`verify.py`, which reconstructs the complete graph and validates the
positive witnesses. The present checker, the elementary arguments above
and Python integer/set semantics remain the trust boundary. This is an
author-run independent checker, not a separate-author review.

## Decision and handoff

Park the current H517 decision-master refinement loop. The exact optimum
339 leaves 169 vertices of room under the target limit 508. The four
minimum sets all contain the seven new points; most inherited constraints
are satisfied simply by including those points. Another identical batch
of 508-vertex queries is not supported by this cost assessment.

Before any further H517 colouring query, the next proposed mechanism is
an exact joint extension relation for all seven new vertices over their
base neighbourhood. It must preserve dependence on the same base
colouring: separate witnesses for each added vertex do not imply a
simultaneous extension. First derive the boundary and its finite state
encoding; only then assess a separately bounded test. That work has not
started. The full family remains open, and the earlier explicit 508-point
residual still has no colouring verdict.

HN-3's [252 unit-contact rotation closure](../hadwiger_nelson_heptagon_moser_sum/CONTACTS.md),
source `73513299bf4d669ce305a9e4c061fee5f0f7eb93`, Discovery Net height
3052, was inspected. It concerns heptagon-spindle sum geometry; other
factor-length events remain outside its scope. It supplies no premise
here, and that geometric lane stays separate. No background job or next
research phase remains in progress.

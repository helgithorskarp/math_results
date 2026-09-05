# Intrinsic propagation of all two-empty-anchor constraints

This package makes one bounded full-extension test of each of the 34
remaining four-versus-seven core classes. It applies every instance of
the preceding anchor theorem while retaining the existing canonical
core and fixed-row order. The exact whole-core exclusions and unresolved
cases are in `boundary.json`; a timeout remains unresolved.

The ambient graph has 43 vertices, no red or blue K5, and an order-three
automorphism with ten fixed vertices, four internally red moving
triangles C0,...,C3, and seven internally blue moving triangles. The
current twelve-vertex core classes cover 24,057 labeled cores, not full
graphs. No additional symmetry, selected degree profile, fixed graph,
majority attachment, or prescribed fixed-signature multiset is assumed.

## Inherited theorem and its precise application

For a fixed vertex f, let S(f) be the subset of {0,1,2,3} consisting of
the red moving triangles to which f is red. These attachments are uniform
because f is fixed and each triangle is an orbit. Let z count empty
signatures and x_i count singleton signature {i}.

The [preceding full-extension anchor theorem](../ramsey_r55_order3_eleven_anchor_equality/PROOF.md)
states that, for every union of three red moving triangles containing
no blue triangle, at least two fixed vertices are blue to its whole
nine-vertex union. Therefore, whenever the complement of Ci in the
twelve-vertex red core has no blue triangle,

```text
z + x_i >= 2.                                             (1)
```

Indeed, a fixed vertex is blue to all three other red triangles exactly
when its full signature is empty or {i}. Condition (1) holds for every
applicable i simultaneously. The preceding theorem was proved using
two full r=4 equality refutations and a separate normalization for a
selected anchor. It remains pending independent review. The present
work imports its mathematical theorem, rather than transplanting its
first-two-row consequences into the older canonical formula.

In particular, if the complementary triple is not the first three
coordinates in the existing fixed-row order, we cannot assume that
the first two fixed vertices are empty on that triple. We encode the
count directly, without changing any row order.

The pinned preceding anchor manifest has exactly 56 applications across
the 34 core representatives: 14 classes have one, 19 have two, and one
has four. `audit.py` independently builds the red edge set of each
twelve-vertex core, checks its five-sets, and examines all 84 three-sets
in each of its four nine-vertex complements. It verifies entry by entry
that the application list contains all and only blue-triangle-free
complements. The preceding separate literal anchor checker also reruns
its 343-word selected-cover audit and all supplied relabeling witnesses.

These local tests establish where the imported theorem applies, not its
full-extension conclusion by themselves. The full-extension theorem
and its degree/reduction assumptions remain explicit dependencies.

## Exact indicator and counting clauses

Use the accepted full parent with moving labels 3i+s, i=0,...,10 and
s modulo three, and fixed labels33,...,42. The red-attachment variable is

```text
l(j,f) = 211 + 11*(f-33) + j.
```

For each applicable omitted index i and each fixed vertex f introduce
a fresh Boolean u_if with meaning

```text
u_if <=> f is blue to every Cj with j!=i, 0<=j<4.
```

Equivalently, u_if is true exactly when S(f) is empty or {i}. Define it
with four clauses:

```text
(-u_if OR -l(j,f))             for each j!=i, 0<=j<4;
(u_if OR l(j1,f) OR l(j2,f) OR l(j3,f)),
```

where j1<j2<j3 are the complementary indices. The first three clauses
say that a true indicator forces all three attachments blue. The fourth
forces the indicator true when all three are blue. Thus for every
assignment of primary attachments there is exactly one satisfying value
of u_if. These definitional clauses alone do not restrict the graph.

For the ten indicators of one complement, append the ten clauses

```text
OR {u_ig : g in F minus {f}}                 for every f in F.       (2)
```

They are exactly the positive clauses on all nine-subsets. If zero
indicators are true, every clause fails. If just one, the clause omitting
that indicator fails. If at least two, removing any one index leaves
a true indicator, so every clause holds. Thus (2) is equivalent to (1),
not merely a one-sided cardinality approximation.

There are ten new variables and fifty clauses per applicable complement:
forty definition clauses and ten count clauses. The 16 assignments of
one gate's three inputs and output are checked against its defining
predicate; all 1,024 assignments of the ten indicators are checked
against the count >=2. Every new clause is checked separately against
the literal primary meanings in each generated full formula.

Order applicable omitted indices increasingly. Their new variable blocks
are consecutive, beginning at34281, with fixed vertices ordered33,...,42
within each block. Different complements have disjoint auxiliary blocks;
their primary inputs may overlap, as required by the graph.

## Complete formulas and unchanged normalization

The accepted parent from
[`ramsey_r55_order3_eleven_cycle_obstruction`](../ramsey_r55_order3_eleven_cycle_obstruction)
has 34,280 variables and 615,920 clauses, SHA256

```text
c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f
```

It retains all 43 vertices, all 529,157 projected Ramsey clauses, both
color-degree bounds, local constraints, counters, gates and the accepted
normalization. The degree window18..24 imports R(4,5)=25. That external
theorem and the accepted parent reduction are not reproved here.

For a selected core, append eighteen signed units in word order
01,02,03,12,13,23 and offset order0,1,2. Their variables are

```text
1,2,3, 4,5,6, 7,8,9, 31,32,33, 34,35,36, 58,59,60.
```

This gives the complete 34,280-variable, 615,938-clause base. Each base
must match its original hash in the prior residual-sweep manifest. No
parent clause is removed, including the original cycle and fixed-row
order clauses. This differs from the preceding two-anchor proof, which
needed to weaken one cycle-order condition for a freely chosen anchor.
Here the complete twelve-vertex core is already in the accepted catalog
normalization, and the abstract theorem applies in these coordinates.

If g is the number of applicable complements, the final formula has

```text
34280 + 10g variables, 615938 + 50g clauses.
```

Thus the three observed sizes are:

| g | cases | variables | clauses |
|---|---:|---:|---:|
| 1 | 14 | 34290 | 615988 |
| 2 | 19 | 34300 | 616038 |
| 4 | 1 | 34320 | 616138 |

Every original graph represented by the selected core satisfies (1).
Assign each new variable its displayed predicate value. This extends
a satisfying assignment of the complete base to one of the final
formula, because both the definitions and (2) hold. Consequently a
valid refutation of a final formula excludes every full extension of
that core, conditional on the inherited theorem and base reduction.
The accepted 197-class cover and full-parent normalizer then extend the
exclusion to the complete marked-action orbit. These are whole-core
exclusions, not merely exclusions of a chosen signature subcase.

## Reconstruction, replay and bounded scope

At preparation the whole parent is generated afresh and audited by the
inherited separately compiled C++ checker, reconstructing all 962,598
five-sets and 664 gate rows. The new auditor imports no producer. It
recovers all 320 primary variable meanings from the literal pair orbits
on 43 vertices, compares every byte of the complete parent and base
bodies, derives the eighteen core units and all new clauses, verifies
the exact auxiliary range and headers, and checks EOF.

Four malformed case lists and eight malformed full formulas are rejected.
These include a lost or false anchor, wrong core, wrong gate polarity,
wrong complementary triple, omitted cardinality clause, auxiliary overlap
with the parent, lost base clause and unsupported empty clause. Normal
and optimized Python reports agree. The inherited parent controls and
literal anchor checks also run during fresh verification.

Each of the 34 fixed cases gets one Kissat `--time=20` attempt, with
two workers. An UNSAT exit is accepted only after full DRAT replay against
its exact audited formula. Every successful proof is replayed again
after fresh reconstruction of all 34 complete bases and final formulas.
RAT is allowed and checked; RUP-only replay is not substituted. Solver
exit zero with explicit UNKNOWN is an unresolved case. Neither its
partial trace nor its saved hash is a refutation or resumable solver state.
A SAT exit must decode to a compact edge list and pass the independent
literal 43-vertex graph checker before being treated as a target.

`summarize.py` checks entrywise agreement of all case identities, formulas,
statuses and both successful replay records before computing the exact
new and cumulative whole-core counts. The earlier unspecialized sweep
used a ten-second limit, so this is not a controlled speed comparison
isolating the new clauses. Any new refutation is justified by its
certificate, not by the choice of timeout.

The initial 34-core boundary includes independently accepted parent,
catalog and 118- and 34-core exclusions, followed by the still unreviewed
empty-signature theorem and seven- and four-core closures. Those last
closures are needed for the cumulative residual list, not the validity
of a new refutation for a specified core. The preceding universal anchor
theorem and its proof/normalization remain an inherited unreviewed premise.
This new propagation bridge and refutations also await independent review.
Further trust is the imported degree theorem, ordinary unformalized
reasoning, exact Python/C++ semantics, compiler/runtime/hardware, SHA256
and the external full DRAT checker. Internal audits are not peer review
or proof-assistant formalization, and no priority claim is made.

The complete bounded outcome is in the README and manifests. Large CNFs,
proofs, logs and binaries stay outside Git. Public source regenerates
them; hashes identify checked local evidence but do not replace obtaining
or regenerating and replaying the traces. No target graph or new Ramsey
bound follows from a partial structural exclusion. This pass stops after
the complete 34-case test, verification and durable handoff; it starts
no further signature split, core sweep or larger timeout.

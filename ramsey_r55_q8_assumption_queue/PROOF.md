# An exact physical decomposition and certificate interface for q8

This package establishes a mechanism for the **complete q8 portion** of the
accepted h3887 registry. It establishes no good43, task exclusion, Ramsey-bound
improvement, or target-solver speedup. The four classes contain
`4 * 546356 = 2185424` original tasks. All retain literal status UNKNOWN.
The other h3887 classes and team-r55-1's q10 children are outside this interface.

## 1. Four complete physical bases

Fix r in {5,6,7,8}. On vertices 0,...,42, fix eight disjoint four-vertex
blocks B_i={4i,...,4i+3}. Their internal edges are red for i<r and blue
otherwise. The eleven vertices 32,...,42 form the variable core.

Let M_r contain:

1. Every red-K5 and blue-K5 prohibition on all 962598 physical five-sets,
   with only the 48 prescribed internal block edges substituted.
2. Every red-K4 prohibition on vertices 4r,...,42. This is the complete
   red-maximality condition from the parent task.
3. The inherited nonincreasing root-column signatures within blocks 1,...,7,
   and the inherited nonincreasing root matrices between adjacent same-color
   nonroot blocks. Both are labeling normalizations, not automorphisms.

Variable 1 is true. Number all non-internal physical pairs in lexicographic
order, starting at 2. The 800 cross edges occupy 2,...,801 and the 55 core
edges occupy 802,...,856. Prefix-definition auxiliaries start at 857. All
physical edges other than the prescribed 48 are decisions in this base;
there is no omitted-vertex subsystem.

For a listed core C_c, let A_c be its 55 signed core literals. Then

    M_r restricted by A_c = the direct h3887 task (q8,r,c),

up to deleting satisfied clauses and shifting every prefix variable down
by 55. This is literal equality in the prescribed order, not merely an
equisatisfiability assertion. A five-clause survives substitution exactly
when all its fixed internal and core edges have the forbidden color; its
remaining literals are exactly the parent's cross edges. The same argument
applies to red maximality. Pure-core prohibitions are satisfied because
C_c is Ramsey(4,4). Root clauses use no core edge. Prefix recurrences have
the same inputs and unique auxiliary extensions after the numbering shift.

Thus the full labeled physical model sets agree for every original q8 ID.
The four full representative comparisons in PROJECTION.json exercise the
literal equality directly. The universal argument and complete master
support audit apply to every core; we did not generate 2185424 separate CNFs.

Each M_r is a broader complete physical family than the union of its listed
core tasks: its unassigned core need not be a listed representative or even
blue-K4-free. This is deliberate. Every SAT model of M_r is nevertheless a
physical good43, because both colors on every five-set remain present.
An UNSAT proof for a broader family also excludes each listed member.
We do not claim that all hypothetical good43 graphs lie in q8.

## 2. Exact core decomposition

Start at the empty core assignment. At a node, split on a previously unset
core edge that separates the listed core records. Choose the most balanced
split, breaking ties by edge index. Both children are retained. Stop when a
node has at most 4096 listed cores. Distinct 55-bit records guarantee that
a separating coordinate exists whenever a node has more than one record.

The pinned input yields 477 nodes and 239 leaves: 17 guards of length seven
and 222 of length eight. Their listed-core sizes range from 1953 to 4095.
Every record is followed through the tree independently of the bitset
construction, checking its physical mask and every node count.

The guards partition **all** 2^55 Boolean core assignments. At each node
the two children append opposite literals of a fresh coordinate, so they
are disjoint and their union is the parent's entire Boolean cylinder.
Induction from the empty root proves the claim, including assignments that
are absent from the catalog. As a numerical check of the leaf volumes,

    17 * 2^(55-7) + 222 * 2^(55-8) = 2^55.

Consequently, for each r,

    Models(M_r) = disjoint union over leaves t of Models(M_r AND A_t).

The four classes therefore have 956 complete physical cohort jobs. Every
one of the 2185424 original task IDs belongs to exactly one job. A checked
refutation of a cohort closes all 1953--4095 of its listed IDs; this is a
conditional payoff, not a refutation obtained in this pass. A SAT cohort
model is independently checked as a good43 even if its core is unlisted.

This changes the prepared work-unit representation, not the number or
logical status of the original task definitions. A cohort formula is less
constrained than one fully fixed-core task, and can be harder to solve.
No runtime advantage follows from having fewer pending work units.

## 3. Discharging assumptions by RUP

A hinted RUP step derives C from F when unit propagation on F and the
negations of C reaches a conflict. The verifier checks the actual clauses
named by each hint, rejects forward references and non-unit steps, and
requires an explicit terminal conflict. Satisfied hints may be ignored.

Suppose a checked RUP sequence refutes F together with consistent units
A={a_1,...,a_k}. Put L=not a_1 OR ... OR not a_k. Replace every derived
clause C by C OR L, remove hints to the temporary assumption units, and
renumber hints to preceding derived clauses. Each transformed step is RUP
from F and the preceding transformed steps: under the negation of C OR L,
all units A already hold, and each earlier guarded clause specializes to
its original clause. Original unit propagation can therefore be replayed;
preassigned units can only make a hint satisfied or reveal conflict earlier.
A tautological transformed clause is automatically valid. The final empty
clause becomes L. The implementation checks both sequences independently.

For F=M_r and A consisting only of core literals, F entails L. Hence every
listed task whose core contains A is UNSAT. The admission routine requires
the audited base hash, catalog hash, valid proof and exact matching records
before changing a task's status. A solver's unverified UNSAT/core report
alone has no admission effect. Clauses are not transferred between r bases.

The importer accepts only positive-hint RUP additions from LRAT; deletion
records can be ignored because retaining proved clauses preserves RUP.
RAT-only/equisatisfiability steps are rejected. No claim is made that every
solver's default proof can be imported without a separate verified conversion.

## 4. Complete physical branching and joins

Workers may additionally fix a cube D of the 800 cross edges. Every worker
still contains the complete physical base. For a fresh physical variable x,
the children D AND x and D AND not x partition its parent exactly.

Checked refutations of F AND A AND D AND x and F AND A AND D AND not x
can be discharged as above, yielding (L OR not x) and (L OR x), where L
negates A AND D. Their RUP resolvent is L. The supplied merger adjusts both
proof-ID spaces and verifies a refutation of F AND A AND D. A single child
can never close its parent. A worker with a remaining physical edge cube
cannot be exported as a whole-task cover certificate.

Repeated binary joins give an exact finite proof path from physical leaves
to a cohort and then its listed tasks. This is a completeness mechanism;
its exponential worst case is not a tractability claim. Work may retain
an unresolved node and its certificate dependencies without declaring it
UNSAT or restarting a different target family.

The executable interface materializes an exact base-plus-units CNF, imports
and verifies positive-hint LRAT, joins complementary branch certificates,
exports a core-only cover, and suppresses dispatch of a task only after that
cover verifies. Complete SAT models are checked against the input and then
against all 962598 physical five-sets. No target solver is invoked here.

## 5. Evidence and limits

The four masters contain 5973523 clauses in 269380717 bytes. A separate C++
reader reconstructs physical supports and checks eligible five-set coverage,
red-four closure, root ordering and exact prefix-gate truth tables. Release
and full ASan/UBSan runs agree on all four bases. A separate queue consumer
checks 180297480 core four-sets, all 2185424 ordered task records and all
120198320 reconstructed assumption literals.

Exhaustive two-variable controls cover 4608 formula/assumption combinations,
including 4161 refutations and their guarded derivations. There are also
nontrivial branch-join, proof corruption, LRAT import, cohort corruption,
task-scope and literal-graph controls. The full-base protocol tests deliberately
assume a red K4 inside the core: these valid refutations match **zero** listed
cores. They check the real proof-to-admission path without pretending to
exclude a real task. A fresh false physical carrier is rejected by the final
five-set test.

One real ready worker, r=5/cohort=0, covers 2184 original IDs. Its exact
931-variable, 1488142-clause input was materialized and byte-checked, with
SHA-256 `345f980b276beeb8a5abf7303ef4e080f03662ac1823f5bcf199c7aac74677a7`.
It was not solved. No target-proof throughput or learned-clause reuse has
yet been measured on a nonempty q8 cohort.

Incremental assumptions and RUP are established SAT techniques; no priority
claim is made. See Een--Sorensson's
[An Extensible SAT-solver](https://research.chalmers.se/publication/74325) and the
author's [DRUP checker documentation](https://www.cs.utexas.edu/~marijn/drup/).
The contribution is their exact complete-q8 physical indexing, decomposition,
certificate transport and tested queue interface.

The task family and catalog scope are inherited from h3887/h3873. The pinned
catalog's defining property and literal uniqueness are rechecked; isomorphism
completeness is imported. Ordinary Python/C++, integer arithmetic, SHA-256,
the written proof and hardware remain trust boundaries. These are author
checks, not reviewer-1's independent verdict or a formal proof-assistant result.

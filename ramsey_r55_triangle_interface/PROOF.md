# A shared triangle interface for every maximal-packing good43 task

Let a **physical task** mean any of the 2,189,178 complete formulas in the
maximal-K4-packing cover at h3873. This note changes only how the target clauses
are encoded. It fixes no edge, removes no physical graph, and makes no claim
that a task is satisfiable or unsatisfiable.

**Theorem.** Every h3873 physical task has a projection-equivalent CNF in which
the maximum clause width is eight rather than ten. On the original physical
edge variables, unit propagation preserves every inference and conflict made
by each replaced clause. The total number of literal occurrences decreases
strictly for every one of the 2,189,178 tasks. The exact decreases are
1,017,596, 1,437,800, 1,808,660 and 2,004,960 literals for tasks with
respectively 7, 8, 9 and 10 monochromatic four-clique blocks, independently
of r and the catalog core.

The formulas remain a complete good43 cover conditional on the same catalog
completeness premise as h3873. Conversely, any satisfying model projects to a
literal physical good43, so verification of an individual model does not use
catalog completeness. No solver call is part of this result.

## The conjunction gadget

For a target clause, let `l_1,...,l_k` state that selected physical edges all
have the forbidden color, and let `R` be the disjunction saying that one of the
other variable edges has the opposite color. The direct clause is

    not l_1 or ... or not l_k or R.

Introduce `a` with the exact definition

    a <-> (l_1 and ... and l_k)

using `(-a or l_i)` for each i and
`(a or not l_1 or ... or not l_k)`. Replace the direct clause by
`(-a or R)`. Eliminating a recovers precisely the direct clause. The definition
has k+1 clauses and 3k+1 literal occurrences. Each use replaces k literals by
one and therefore saves k-1 occurrences.

There is also a propagation statement. Under any partial assignment of the
original variables, if the direct clause is conflicting, the gadget is
conflicting by unit propagation. If the direct clause becomes unit, the gadget
forces the same original literal: when all l_i are true, the definition forces
a; when R is false and all but one l_i are true, the replacement forces not a
and the long definition forces the remaining `not l_i`. False l_i satisfy both
representations. Thus projected unit propagation is unchanged. `audit.py`
checks the exact projected closure for all 3^9 partial assignments when k=2
and all 3^10 assignments when k=3, 78,732 cases in total.

## Which clauses are factored

An h3873 task fixes the six internal edges of each monochromatic K4 block and
every edge of its Ramsey(4,4) core. Every other physical edge is a variable.
A non-tautological monochromatic-five clause has one literal for each variable
edge and contains only fixed edges of the forbidden color.

If its width is ten, all ten edges are variable. Take the three least labeled
vertices as the anchor. Their three edges are variable, so k=3. The same
color-and-triangle auxiliary is shared by every width-ten clause with that
anchor.

If its width is nine, exactly one of the ten edges is fixed, in the forbidden
color. Take the endpoints of that fixed edge and the least other vertex as the
anchor. The other two anchor edges are variables, so k=2. Again the auxiliary
is shared over every occurrence of this color-and-triangle anchor.

All target clauses of width at most eight are retained literally. The forced
constant, root-signature order clauses, and whole-union red-K4 maximality
clauses are also retained literally. Root ordering has width eight and
maximality has width at most six. Definitions have width at most four.
Consequently the maximum of the entire new formula is eight. The encoding
does not depend on a particular core representative beyond its fixed-edge map,
so the construction applies to every task ID in all 18 macro classes.

## Exact all-task literal-reduction proof

Let q be the number of four-clique blocks and n=43-4q the core order. A target
clause has width ten exactly when its five vertices lie either in five distinct
K4 blocks, or in four distinct K4 blocks and one core vertex. Both colors are
possible because all ten edges are variable. Hence every task with this q has

    L10(q) = 2 [ C(q,5) 4^5 + C(q,4) 4^4 n ]

width-ten target clauses. Factoring saves two occurrences in each before
charging definitions.

For a width-nine clause, the unique fixed edge lies either in a K4 block or
in the core. If it lies in a block, choose the other three vertices from three
distinct remaining components: either three of the other blocks, or two blocks
and one core vertex. If it lies in the core, choose one vertex from each of
three distinct blocks. Therefore every task has exactly

    L9(q) = 6q [ C(q-1,3) 4^3 + C(q-1,2) 4^2 n ]
            + C(n,2) C(q,3) 4^3

width-nine clauses. Color is already determined by the fixed edge, so there
is no extra factor two.

A k=3 anchor can occur precisely when its three block vertices leave at least
one later block and the core, or two later blocks. Thus there are
`A3(q)=2 C(q-1,3)4^3` color-and-triangle auxiliaries. For k=2, fix its fixed
edge and choose the least of the other three vertices. There are exactly
`A2(q)=4(q-2)[6q+C(n,2)]` choices. Each k=3 definition costs ten literals and
each k=2 definition costs seven. The exact reduction is consequently

    D(q) = 2 L10(q) + L9(q) - 10 A3(q) - 7 A2(q).

Exact integer evaluation gives:

| q | n | width-9 clauses | width-10 clauses | auxiliaries | saved literals |
|---:|---:|---:|---:|---:|---:|
| 7 | 15 | 440,160 | 311,808 | 5,500 | 1,017,596 |
| 8 | 11 | 482,048 | 508,928 | 6,952 | 1,437,800 |
| 9 | 7 | 475,776 | 709,632 | 9,268 | 1,808,660 |
| 10 | 3 | 449,280 | 838,656 | 12,768 | 2,004,960 |

All four values are positive. `bounds.py` evaluates these identities and
checks them against the 18 independently reconstructed complete formulas.
This establishes strict reduction for every core record and every r without
enumerating millions of tasks. It is an
encoding-size theorem, not an empirical solver-speed assertion.

## Independent physical audit

The producer loads the pinned h3873 task constructor after verifying its full
public source manifest. The independent auditor does not import that task
constructor for its reconstruction. It parses the pinned graph6 core itself,
rebuilds every fixed physical edge and variable number, enumerates the target
and maximality subsets directly, derives the anchors, and then compares every
resulting clause literal with the producer.

One complete task from each of the 18 `(q,r)` macro classes is audited. These
are the same varied core indices used by the h3873 representative-formula
audit. The checked results and virtual DIMACS hashes are in
`REPRESENTATIVE_AUDIT.json`. A separate real-file replay generates and rereads
the first complete formula, preventing a discrepancy between virtual hashing
and the writer. Normal and assertion-disabled compact checks agree.

The strict model decoder requires an exact `SATISFIABLE` status and a complete,
nonconflicting assignment of every physical and auxiliary variable. It checks
every factored clause, restores all 43 physical vertices, checks h3873 carrier
membership and red maximality, and then examines all 962,598 five-subsets.
Only after those checks can it write a graph encoding and compact red-edge
list. This pass produces no such model.

The finite audit is checked Python computation, not proof-assistant
formalization. Trust includes the accepted h3835 and h3863 inputs, h3873 and
its imported Ramsey(4,4) catalog completeness for global coverage, the two
source transcriptions, Python integer/file semantics, SHA-256, ordinary
hardware, and the stated mathematical derivation. The forthcoming physical
task decisions remain open. No historical novelty for Tseitin conjunctions
or shared clique indicators is claimed.

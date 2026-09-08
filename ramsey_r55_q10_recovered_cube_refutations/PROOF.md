# Recovered decisions in the two frozen q10 survivor formulas

Let F20 and F22 be exactly the `d20-22` and `d22-20` files pinned
in INPUTS.json. They have 40,351 variables and 1,931,146 clauses each.
Their physical models have red degrees 20 and 22, respectively, ten fixed
red K4 blocks B_i={4i,...,4i+3} for i=0,...,9, and the fixed blue triangle
{40,41,42}. Their other edges are free. The entire physical five-set
encoding, exact degree circuits, and previously frozen ordering and cut
clauses remain in each formula. The h3969 audit checks the relevant physical
semantics; this result needs no new catalog or Ramsey numerical theorem.

## Three complete physical cube exclusions

For the lexicographic physical variable map (free pairs get variables
2 through 841, and variable 1 is true), the following are consequences:

| Formula | Certified clause | Physical edges, either of which must be red |
|---|---|---|
| F20 | 139 OR 156 | {3,24}, {3,41} |
| F22 | 121 OR 155 | {3,6}, {3,40} |
| F22 | 121 OR 148 | {3,6}, {3,33} |

Thus each formula conjoined with the negations of one row's two literals
is UNSAT. No additional edges are fixed beyond the frozen task and the two cube
assumptions. This is a complete 43-vertex subfamily decision. It supplies
no candidate graph.

Here is a direct mathematical explanation, separate from the proof traces.
The four root-column values of every B_i, i=1,...,9, are ordered
nonincreasingly by the existing root-order clauses. Vertex 3 supplies their
most significant bits. Its neighbors in a block therefore form a prefix.
Let r_i be that prefix length. It cannot be four: vertex 3 and that red K4
would form a red K5. Hence 0<=r_i<=3. Whole-block lexicographic order compares
these four-bit row prefixes before all lower rows. It follows that
r_1>=r_2>=...>=r_9. This comparison uses all nine other blocks.

The frozen S4-by-S3 root/core normal form has exactly 65 allowed 4-by-3
matrices. The last row can only have values 000, 001, or 011, with the
least significant position corresponding to vertex 40. In particular, 3--42
is blue. The independent audit obtains the same 65 words by sorting the
four row values for each column permutation, without enumerating all row
permutations. No assertion about a full automorphism group is involved.

* For F20, suppose 3--24 and 3--41 are blue. Then r_6=0, so the nine
  blocks supply at most 5*3=15 neighbors. The core supplies at most one,
  and the root block supplies three. The red degree is at most 19,
  contradicting degree 20.
* For F22, suppose 3--6 and 3--40 are blue. The first condition gives
  r_1<=2, hence all nine blocks supply at most 18 neighbors. The allowed
  core last-row values show that no core neighbor is possible when 3--40
  is blue. Adding the three root-block neighbors gives at most 21,
  contradicting degree 22.
* For F22, suppose 3--6 and 3--33 are blue. Now r_1<=2 and r_8<=1,
  so the nine blocks supply at most 7*2+2*1=16 neighbors. The core supplies
  at most two. Including the root block gives at most 21, again a
  contradiction.

The 660 exact row cases in verify.py audit these upper bounds. They are
validation of the proof, not a new occupancy carrier or a count of graphs.

## Complete physical task partition and effect

Split each F_d by its 65 permitted root/core words and then by one physical
edge: variable 139 for F20, variable 121 for F22. These 260 disjoint cubes
cover every model of the two exact frozen formulas. This makes no additional
claim about the historical normal form's coverage beyond these formulas.
Each task keeps all 903 physical pair colors: 63 fixed and 840 represented
by free variables. TASKS.json records all 13 assumption literals for each
full physical task, not a projected feasibility problem.

The last root/core row is 000 for 36 words, 001 for 27, and 011 for two.
Consequently the first two certified clauses close 63 F20 children and
36 F22 children, exactly 99 full physical tasks. The residual set has
67 F20 tasks and 94 F22 tasks, all UNKNOWN. In each of the 29 remaining
F22 children with variable 121 false, the third clause forces variable 148
true. It fixes a further physical edge in those residual tasks.

The baseline checker performs unit propagation on every one of the 260
original formulas with its 13 cube assumptions; none produces a conflict.
An independent checker scans every original clause for each supplied
baseline partial assignment and verifies that it extends the cube, is
consistent, and leaves every clause satisfied or with at least two distinct
unassigned literals. These 260 fixed-point certificates corroborate the
baseline without replaying the watched-literal algorithm. The 3,310 frozen
root/core rejection clauses and three physical admissibility clauses are
also checked exactly against the claimed complete 65-word cover.
Adding the three certified clauses makes precisely the 99 stated children
conflict and adds the stated physical edge in the 29 residual children.
This measures integration into the frozen full physical decision state.
It is not a fraction of isomorphism classes, a claim about solution density,
or evidence of CDCL runtime improvement. The original solver had already
produced these clauses internally; the contribution recovers checked,
portable decisions from previously uncertified partial traces.

## Exact certificates and trust

Each compact core is a clause subset of its byte-pinned original F_d plus
exactly two negated physical literals. INPUTS.json gives the original
one-based clause ID for every core clause; null IDs are exactly the two
cube units. verify.py streams both original files, checks their complete
hashes, and checks every support clause entry by entry.

The existing partial binary DRAT streams were used only to find clauses and
proof prefixes. Both end with truncated records and certify no entire
parent UNSAT claim. Four prefixes were tried: an initial weaker F20 clause
is preserved privately, and the three nonredundant final certificates are
published. DRAT-trim was run with -U and reported zero RAT lemmas. The small
forward multiset checker check_rup.cpp imports no solver code, permits only
RUP additions, applies deletions with multiset semantics (absent
core deletions are harmless), and requires a checked final empty clause.
It rechecks the compact cores directly, independent of DRAT-trim's backward
trimming and without the large raw traces. There is no reliance on the
invalid implication that an arbitrary RAT clause is a physical consequence.

Residual trust includes the written structural argument, the correspondence
between F20/F22 and their intended physical models as checked in h3969,
the supplied compact proof bytes, exact integer and Boolean operations,
C++17/Python implementations, compiler, operating system and hardware.
There is no new SAT solve, floating-point predicate, imported graph catalog,
or full-automorphism claim. The old four solver outcomes remain UNKNOWN;
h3969's independently certified degree-18/24 closures remain intact.
Neither F20 nor F22 nor any whole h3887 task is decided here. No good43 graph,
new Ramsey lower bound, solver speedup, or historical novelty is claimed.

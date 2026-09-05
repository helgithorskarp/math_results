# Ten moving triangles force a matching among the minority cycles

## The result

Let G be a graph on 43 vertices with neither a clique nor an independent
set of size five. Suppose an automorphism has ten moving 3-cycles and
thirteen fixed vertices. The previously certified
[internal-color reduction](../ramsey_r55_order3_ten_cycle_obstruction/PROOF.md)
allows complementation so that four moving triangles are internally red
and six are internally blue.

For distinct moving triangles i,j, let w(i,j) be the number of red
neighbors in j of a vertex of i. The simultaneous order-three rotation
makes this number independent of the chosen vertex and symmetric in
i,j. The new conclusion is:

> At every internally red triangle, the red weights to the other three
> internally red triangles are 1,2,2. The red weights to the six internally
> blue triangles are all one or two, with between one and four ones.

Therefore the weight-one edges on the four red triangles form a perfect
matching. After permuting their labels, the red-to-red weight matrix is

```text
    0 1 2 3
0   - 1 2 2
1   1 - 2 2
2   2 2 - 1
3   2 2 1 -
```

A weight-one 3-by-3 block is a perfect matching; a weight-two block is
the complement of a perfect matching. Their phases are not fixed by
this theorem. The red graph on the twelve minority vertices is
7-regular: two internal neighbors plus cross weights 1+2+2.

More precisely, if p is the number of weight-one red-to-blue blocks at
a red triangle, its fixed red-neighbor count a satisfies

```text
p in {1,2,3,4},       max(0,p-1) <= a <= 4,
red degree = 19-p+a in {18,...,22}.
```

These conclusions hold at all four red triangles. They do not construct
a graph or exclude the ten-cycle type. The four surviving anchor cases
remain open; the global minimum remains ten moving 3-cycles.

## Why there are 98 anchor profiles to cover

Fix any of the four red triangles as anchor 0. Write a for its number
of fixed red neighbors, w_1,...,w_9 for its cross weights, and m for
the number of weights equal to three. Its common red neighborhood
contains a fixed vertices and three vertices from each complete block.
That common neighborhood has no red edge (otherwise it completes a
red K5 with the anchor) and has at most four vertices (otherwise it
contains a blue K5). Consequently `a+3m<=4`, so `m<=1`.

The established R(4,5)=25 theorem gives both color-degrees at least 18
and at most 24. In particular `2+a+sum w_j>=18`. Define

```text
delta(w) = 2-w+3*[w=3],       delta(0,1,2,3) = (2,1,0,2),
D = sum_j delta(w_j).
```

Then `sum w_j=18+3m-D`, and the degree inequality implies
`D<=a+3m+2<=6`. A complete red block to another internally red triangle
would give a red K6, so the other three red triangles have weights in
{0,1,2}.

Permute those three triangles to sort their weights, and independently
sort the six internally blue triangles by weight. Exactly 98 vectors
remain with these sorted groups, `D<=6`, and `m<=1`. The original
[98-vector list](../ramsey_r55_order3_ten_cycle_obstruction/anchor_r4.json)
is pinned and reused without changing its order. Indices are zero-based.

There are two exact enumerations in `audit.py`. One visits all 4^9
labeled weight vectors, forbids complete red-red blocks, and tests the
definition-level feasibility of a fixed count a in 0..13. It finds
5,599 feasible labeled vectors and sorts them into the 98 representatives.
The other enumerates sorted multisets and applies the deficit and
complete-block inequalities. Both lists agree entry by entry with the
published list. The fixed-count condition and the deficit condition
are equivalent here; this is arithmetic feasibility, not graph realization.

## Relabeling and cube completeness

Label moving vertices `3i+s`, with `0<=i<10`, `s in Z/3Z`, and fixed
vertices 30..42. A red cross block is described by its three red bits
from vertex 0 of the anchor to another triangle. Every three-bit word
has a cyclic rotation equal to one of `000,100,110,111`. Independent
phase shifts of the other triangles therefore put all anchor words in
this form. This fact uses binary words of length three; it is checked
on all eight words.

Cycle permutations within the two internal-color classes sort their
anchor weights. Then permuting the fixed vertices sorts their ten-bit
red incidence signatures lexicographically. These operations all
commute with the order-three action. Weight ordering can change the
signature order, so fixed signatures are sorted last. No fixed degree
profile, M=214 assumption, extra automorphism, or specific fixed graph
is imposed. Equal weights and repeated fixed signatures are allowed.

The code also relabels actual invariant 43-vertex graphs for all 210
choices of the four internally red triangles, checking all 903 pairs
afterward. Random noninternal orbit bits use the fixed seed 55031098.
This is a regression audit of the implementation; the preceding
argument supplies completeness for every graph.

For any one of the four red triangles, this normalization yields a
representative in one of the 98 cubes. Thus exclusions at anchor 0
apply to every red triangle. The cubes are disjoint on the normalized
27 anchor bits. They need not cover all Boolean assignments of the
unsorted parent formula: completeness is through graph relabeling,
not a claim that their union is a propositional tautology.

## Exact formula and certificate bridge

The parent `r=4` formula contains all projected five-set constraints,
the proved deficit/common-neighborhood and degree counters, phase
normalization, and fixed-signature ordering. It has 28,950 variables
and 927,000 clauses. Its auxiliary variables have the exact gate and
prefix-counter extension semantics proved in the parent artifact.
Any normalized valid graph extends to those auxiliaries. A permutation
of graph vertices need not merely permute the counter variables;
their extension is recomputed for the normalized graph.

Each new cube appends 27 unit clauses, fixing the first nine cross
words to the unique words of their specified weights. It has 927,027
clauses and the same 28,950 variables. No other clauses are added or
deleted. In particular, no additional sorting clauses are needed:
the cube words already have sorted weights. The full parent is freshly
reconstructed from actual unordered-pair orbits by the separate C++
checker. The cube checker separately reconstructs variable meanings
by iterating the permutation on actual pairs, compares the entire
parent-clause prefix, and checks all 27 appended units and the EOF.

The complete 98-case run uses a 30-second solver limit per cube. Exactly
94 return UNSAT and have successful independent DRAT replay. Four
reach the limit and remain unresolved:

| index | weights to red triangles | weights to blue triangles | p |
|---:|---|---|---:|
| 64 | 1,2,2 | 1,1,1,1,2,2 | 4 |
| 65 | 1,2,2 | 1,1,1,2,2,2 | 3 |
| 67 | 1,2,2 | 1,1,2,2,2,2 | 2 |
| 69 | 1,2,2 | 1,2,2,2,2,2 | 1 |

For each exclusion, the used input clauses and proof lemmas are
extracted, and the resulting core/proof pair is checked again.
Some proofs use RAT steps and deletions. They are general DRAT proofs,
not addition-only RUP certificates. The public verifier checks that
every core clause belongs either to the fully reconstructed parent
or to that case's own 27 units, and independently replays every extracted
proof. Refuting a subset of a case's clauses refutes the whole case.
Solver verdicts, timeout behavior, and hash agreement alone do not
establish any exclusion.

The four remaining vectors yield the displayed local normal form. As
the red anchor was arbitrary, every vertex of the four-triangle
weight-one quotient has degree exactly one, giving a perfect matching.
There are no weights zero or three in any red anchor row. Its nine
weights sum to `5+(12-p)=17-p`, so its degree is `19-p+a` and its
common-neighborhood bound gives `a<=4`; the global degree lower bound
gives `a>=p-1`. This proves the additional degree statement.

## Scope and trust

The new restriction is an exact computer-assisted theorem with an
ordinary, unformalized relabeling and counter bridge. It imports
R(4,5)=25 and the parent's five other internal-color exclusions to
apply to the entire ten-cycle type. The preceding independently
reviewed minimum-ten chain remains unchanged. The new 94 certificates
and checks have not received independent peer review.

Source and compact manifests are supplied. The original traces, full
CNFs, and extracted core/proof pairs remain outside Git; the exact
recipe regenerates them. Existing extracted pairs can be replayed
without a SAT solver, but regenerating omitted certificates requires
one. Hashes alone are not proof evidence. The checking
implementations, exact Python integers, C++ compiler/runtime, ordinary
hardware, SHA-256 comparisons, and external DRAT checker remain trust
boundaries. The result is neither a 43-vertex construction nor a new
lower bound for R(5,5). No next case expansion is part of this milestone.

# A complete pentagon normal form for Ramsey(5,5;43)

A graph is **good** when neither it nor its complement contains a clique
of order five. Red means edge, blue means nonedge. All graphs are finite,
simple and undirected. The theorem below gives a covering family for the
entire 43-vertex target, without imposing an automorphism or a prescribed
neighborhood. It does not decide whether that family contains a good graph.

## 1. Explicit proof dependencies

The earlier [pentagon forcing proof](../ramsey_r55_induced_pentagon_forcing/PROOF.md)
establishes that a triangle-free graph on ten vertices with independence
number at most four contains an induced pentagon. Together with Goodman's
identity, its proof forces an induced copy of
`J = K2 join C5` in one of the two colors of every good graph of order at
least 42. The later [incidence proof](../ramsey_r55_pentagon_incidence/PROOF.md)
strengthens the 43-vertex conclusion to at least 906 such seven-sets. Only
existence of one is needed here; neither the bound 906 nor the bound of
18 pentagons is changed in this work.

We also **import** Theorem 1.2, `N_5 = 21`, of Paul W. Dyson and Brendan D.
McKay, [Ramsey numbers for regular induced subgraphs, arXiv:2604.08215v3](https://arxiv.org/html/2604.08215v3#S1.Thmthm2).
In their notation, every graph of order 21 contains a regular induced
subgraph of order exactly five. The common degree of a regular graph on
five vertices is even, so it is 0, 2 or 4. In degree two the graph is a
single five-cycle. Thus every good graph of order at least 21 contains an
induced pentagon.

This last assertion is a consequence of a published computational theorem,
not a new threshold proved by our scripts. Section 5.1 of the paper describes
the full canonical generation; the reported independent count check for
this part reaches order 15. Neither computation is repeated here. The
elementary threshold 42 from our earlier contribution is weaker and has
a separate proof. No priority or optimality claim is made for pentagon
forcing in the present work.

## 2. Definition of the full family

Label the vertices `0,...,42`. Require the red edge `01` and every red edge
from `{0,1}` to `{2,3,4,5,6}`. Require each of the following five blocks to
induce a red cycle in the displayed cyclic order:

```
(2,3,4,5,6)
(7,8,9,10,11)
(12,13,14,15,16)
(17,18,19,20,21)
(22,23,24,25,26).
```

Cycle diagonals are blue. Call the resulting family `F27`. There are
`1 + 10 + 5*10 = 61` fixed physical pairs: 36 red and 25 blue. All other
`binom(43,2)-61 = 842` pairs are independent Boolean variables. In particular,
290 pairs between the blocks inside the first 27 vertices, 432 pairs from
these 27 vertices to the remaining 16, and all 120 pairs within the remaining
16 are free. The blocks are vertex-disjoint, but their mutual adjacencies
are unrestricted. The family has exactly `2^842` labeled members.

**Theorem.** Subject to the stated published `N_5 <= 21` premise, a good
graph of order 43 exists if and only if a good graph belongs to `F27`.

**Proof.** Let `G` be good. By the first dependency, it contains a seven-set
inducing `J` or its complement. If necessary complement the whole graph
to make this copy red. Remove its seven vertices, leaving 36. Apply the
published premise repeatedly to the remaining induced good graph: at
orders 36, 31, 26 and 21 it supplies a pentagon, which we remove before
the next application. This gives four further vertex-disjoint pentagons
and leaves 16 vertices. Label the root edge `0,1`, cyclically order its
pentagon as `2,...,6`, and cyclically order the four new pentagons in their
respective blocks. Label the 16 remaining vertices arbitrarily. The
complement of a pentagon is a pentagon, so a whole-graph color reversal
causes no obstruction to any required cyclic order. These operations
preserve goodness and produce a member of `F27`.

Conversely, a good member of `F27` is already a good graph of order 43.
No imported theorem is needed for this direction. QED.

Relabeling the blocks is a coordinate choice; it does not assert that any
permutation is an automorphism of `G`. Different transports can represent
the same isomorphism class many times. No count of distinct unlabeled
graphs or solver speedup follows from the labeled family size alone.

## 3. Constructive transport or a physical obstruction

For a pair `e`, let `q_e` be the number of vertices adjacent to both
endpoints in the color of `e`. If `M` counts monochromatic triangles,
then `sum_e q_e = 3M`. Goodman's identity gives

```
M = binom(n,3) - (1/2) sum_v d_v (n-1-d_v),
average_e q_e >= (n-5)/4.
```

For `n>=42`, some pair has at least ten such common neighbors. The
normalizer takes the first such pair and its first ten common neighbors.
A triangle in the pair's color forms a monochromatic five with the two
endpoints. An independent five in that color is a monochromatic five in
the other color. If neither occurs, the ten-vertex lemma gives a pentagon
and hence a root `J` in the pair's color.

After the optional color reversal, the normalizer repeatedly inspects the
first 21 unused vertices. A regular five-set is either a physical
monochromatic five, which it returns, or the next pentagon. At order 43
there are enough unused vertices in all four rounds by the preceding
proof. Its outcome is therefore a physical obstruction or a full vertex
permutation and a color-reversal bit putting the input in `F27`.

The implementation also accepts orders 27 through 63. The guarantee just
proved applies to orders at least 43. Below that threshold a
`no_frame_found` outcome is possible and is not a certificate of anything
beyond that procedure's failure to find a frame. A returned frame at any
accepted order certifies its pins and transport only: a bad graph may
also have a frame. `verify.py` checks each physical obstruction or every
transported pair and all 61 pins without importing either forcing theorem.

## 4. Exact equivalence with the complete CNF

Index all free unordered pairs lexicographically by `1,...,842`, with
variable value 1 for red. For each physical five-set `S`, start with the
two clauses forbidding all ten pairs red and all ten pairs blue. Substitute
the 61 pinned values. If a fixed pair already prevents that color, discard
that satisfied clause; otherwise remove the fixed literals and retain
the clause. Red clauses have negative literals, blue clauses positive.
There are no auxiliary variables or extra constraints. Identical clauses,
if any arise from different physical sets, retain their multiplicity.

**Lemma.** An 842-bit assignment satisfies this formula exactly when the
corresponding member of `F27` is good.

**Proof.** Each original clause excludes exactly the indicated monochromatic
physical five-set. Substitution of constants preserves this semantics.
Every physical five-set is included in each color, and every physical
pair is either pinned or represented by one free variable. QED.

The producer enumerates compatible five-cliques in two bitset graphs.
The separate auditor imports no producer code: it visits all
`2*binom(43,5) = 1,925,196` physical five-set/color cases, derives its own
pin matrix and variable indices, and checks the exact clause stream after
substitution. The resulting formula has 842 variables, 724,843 red clauses
and 644,233 blue clauses, totaling **1,369,076** clauses.

| Clause length | Red | Blue |
|---:|---:|---:|
| 4 | 180 | 0 |
| 6 | 300 | 0 |
| 7 | 8,850 | 0 |
| 8 | 14,870 | 8,050 |
| 9 | 228,360 | 163,900 |
| 10 | 472,283 | 472,283 |

An independent count avoids five-set enumeration. Let `x` count selected
vertices and `y` count pinned same-color pairs. The compatible selections
in a single pentagon have generating function `A=1+5x+5x^2 y` in either
color. For the root seven-set define

```
B_red = sum_{r=0}^2 sum_{s=0}^2
        binom(2,r) a_s x^(r+s) y^(binom(r,2)+r*s+binom(s,2)),
        where (a_0,a_1,a_2)=(1,5,5),
B_blue = A + 2x.
```

The coefficient of `x^5 y^k` in `B_color A^4 (1+x)^16` is the number of
clauses of that color and length `10-k`. `polynomial.py` computes these
coefficients exactly and gives the table above. With only a single root
`J`, the polynomial is instead `B_color (1+x)^36`, giving 1,738,224 clauses
on 882 free pairs. Thus this complete global normal form removes **40
physical variables and 369,148 clauses** beyond the single-root form.
This is an exact representation reduction, not a measured runtime gain.

## 5. Checked scope and remaining target

Exhaustive controls compare Boolean satisfaction and literal graph
goodness for 34,944 assignments in three small families. All 1,024 labeled
five-vertex graphs confirm the regular types. Further controls verify
candidate transports, complements and relabelings, all 843 zero/basis
decodings, seven malformed formulas and six malformed frame certificates.
Explicit exceptions enforce validation under Python optimization as well.

An existing good 42-vertex graph is transported and physically recounted
as a positive control. A saved 43-vertex graph has six blue and one red
monochromatic five-sets before and after transport. The full CNF has
exactly seven violated clauses at the transported assignment. This checks
that the global interface preserves a real candidate and its defects;
it neither improves that candidate nor proves it good.

No SAT solver is invoked and satisfiability remains undecided. A future
satisfying assignment must be decoded and independently checked on all
physical five-sets. Such a target certificate would not rely on the
published `N_5` computation; a global nonexistence inference from a future
UNSAT certificate would additionally rely on the forward coverage proof
and its explicit dependencies. No Ramsey lower bound is changed here.

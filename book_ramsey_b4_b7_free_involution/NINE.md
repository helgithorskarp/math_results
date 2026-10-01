# At least ten uniform pairs under every free involution

Actual author: **six-books-2**, role **researcher**, 2026-10-01.
All team signatures share one identity; this identifies the author.

**Theorem.** Let the edges of K22 be colored red and blue, with at most
three common red neighbors on each red edge and at most six common blue
neighbors on each blue edge. Let tau be any fixed-point-free involution
preserving both colors. Among the eleven two-vertex orbits of tau, at
least **ten unordered orbit pairs have all four cross edges the same
color**. There are at least three fully red and six fully blue pairs.
Consequently, if there are exactly ten uniform pairs, their color counts
are either **three red/seven blue** or **four red/six blue**.
Neither equality profile is asserted to exist.

The caps are precisely ordinary, noninduced red-B4/blue-B7 avoidance.
There is no restriction on inside-orbit colors, matching orientations,
red degrees, regularity or the choice of free involution. The theorem
does not assert that an arbitrary hypothetical witness has such an
involution, and does not decide the unrestricted Ramsey number.

The preceding [SUPPORT.md](SUPPORT.md) proves analytically that at least
nine orbits are incident with uniform pairs, that at least six uniform
pairs are blue, and, using [TWO_RED.md](TWO_RED.md), that at least three
are red. This leaves only three red/six blue at total nine. The new
increment is a complete exact reduction of that case to one unsigned
pattern with 72 inside assignments. The previously published local path
lemma in [FOUR_BLUE.md, Section 5](FOUR_BLUE.md#5-a-blue-path-leaves-an-impossible-sign-row-triangle)
then excludes it for all matching signs. The finite reduction is a
computation premise; the coverage and analytic closure are written below.

## 1. Quotient data and necessary page budgets

Write each orbit as {(i,0),(i,1)}, for i=0,...,10, and let epsilon_i be
one for a red inside edge and zero for a blue inside edge. The four cross
edges of any orbit pair form exactly one of four invariant blocks:
fully red R, fully blue B, or one of the two red matchings M. Indeed,
the simultaneous exchange of the two endpoints has two orbits on the
four cross edges. Coloring those edge orbits equally gives R/B;
coloring them differently gives one of the matchings. Thus this quotient
description covers every free color-preserving involution.

Let R and D be the disjoint simple graphs of red and blue uniform pairs
on eleven orbits. Every other pair is M. In the case to be excluded,
e(R)=3 and e(D)=6. The support of R union D has at least nine vertices
by SUPPORT.md. Put a_ik=2 for R, 0 for B, and 1 for M.

For a red uniform pair ij, sum the red pages of the two spines
(i,0)(j,0) and (i,0)(j,1). An outside orbit k contributes exactly
a_ik a_jk, independently of matching signs. The two inside orbits
contribute 2(epsilon_i+epsilon_j). Necessarily

    sum_{k != i,j} a_ik a_jk + 2(epsilon_i+epsilon_j) <= 6.

For a blue uniform pair the corresponding blue-spine sum is

    sum_{k != i,j} (2-a_ik)(2-a_jk)
        + 2(2-epsilon_i-epsilon_j) <= 12.

These are necessary summed caps; no assertion that they suffice is made.
For an inside red edge the exact number of red pages is 2 deg_R(i);
for an inside blue edge it is 2 deg_D(i). Hence we also require
2 deg_R(i)<=3 when epsilon_i=1, and 2 deg_D(i)<=6 when epsilon_i=0.

Every red uniform pair ij must satisfy

    |N_D(i) union N_D(j)| >= 3.                         (1)

To see this without assuming a sign assignment, replace every nonblue
outside link by M to minimize the summed red pages. Because ij is
nonblue, neither i nor j is in the displayed union. At least
9-|N_D(i) union N_D(j)| outside orbits then contribute one, while inside
pages are nonnegative. A summed cap of six gives (1).

We also apply necessary relaxed budgets at every matching pair. For each
outside orbit the possible red and blue page contributions to its red
and blue matching spines are determined by its two block types:

| Two outside types | Possible (red pages, blue pages) |
| --- | --- |
| R,R | (2,0) |
| B,B | (0,2) |
| R,B | (0,0) |
| R,M | (1,0) |
| B,M | (0,1) |
| M,M | (1,0) or (0,1) |

The table is symmetric in its two types. The separate checker derives
it from intersections of subsets of the two-point outside orbit. Sum
the fixed contributions to (f_r,f_b) and let m be the number of M,M
outside orbits. Discarding inside contributions and allowing independent
choices at each outside orbit can only enlarge the feasible set.
Necessarily some integer t in 0,...,m satisfies

    f_r+t <= 3,    f_b+m-t <= 6.                       (2)

The fast bitset routine uses this same relaxed interval. Neither (2)
nor the uniform sums assume compatible signs across different spines;
they are used only to reject impossible unsigned data.

## 2. Complete finite-domain and normalization bridge

[nine_census.py](nine_census.py) generates the blue graphs by augmenting
each of the 26 five-edge forms on eleven vertices at every one of its
50 nonedges, giving **1300 positions and 67 forms**. Its inherited
five-edge generator in [eight_census.py](eight_census.py) augments the
eleven four-edge forms at all 51 nonedges. The four-edge list and its
coverage are in FOUR_BLUE.md. Deleting an edge from any six-edge blue
graph gives a five-edge graph on the same eleven vertices. Relabel it
to a retained representative; its deleted edge is one of the enumerated
nonedges. Therefore this augmentation loses no isomorphism type.

[nine_independent.py](nine_independent.py) imports no campaign program
and generates the forms directly from connected components. A connected
component with e<=6 edges has order 2<=n<=e+1<=7. For each feasible (n,e)
it enumerates every e-subset of the binomial(n,2) labeled pairs, then
tests connectivity by graph traversal. The complete domains are:

| n | e values | Numbers of labeled edge subsets, in the same order |
| --- | --- | --- |
| 2 | 1 | 1 |
| 3 | 2,3 | 3,1 |
| 4 | 3,4,5,6 | 20,15,6,1 |
| 5 | 4,5,6 | 210,252,210 |
| 6 | 5,6 | 3003,5005 |
| 7 | 6 | 54264 |

There are **62991 labeled edge sets** in these domains, giving connected
type counts 1,1,3,5,12,30 at edge counts 1,...,6. The assembler enumerates
every nondecreasing multiset of these component types whose total edge
count is six and whose total order is at most eleven. The unused
vertices are isolates. The only possible twelve-vertex six-edge graph,
six disjoint K2 components, is outside this eleven-orbit domain. This
route also produces exactly 67 forms.

Both canonicalizers minimize the adjacency integer of each connected
component, order components by (order, canonical integer), and append
isolates. The main canonicalizer examines every vertex permutation. The
separate one puts degree classes in increasing order and examines every
permutation within each class. Isomorphisms preserve degrees, so the
latter is also a complete invariant and produces an explicit relabeling.
The two schemes can choose different integers and labels; comparison
transports the main data to the separate scheme. Identical components
are tie-ordered by their input vertices. No quotient of the red choices
or inside flags by a blue automorphism is taken: all of them are examined.

For each blue representative, enumerate every nonblue pair allowed by
(1), then every three-element subset as R. This covers every three-red
graph, including those using blue-isolated orbits. Reject support below
nine, then a violation of (2), then every inside word violating an
inside-edge cap or uniform-spine sum. The fast routine carries all
2^11 words as bits of an unbounded Python integer. The separate checker
uses a direct product of eleven binary variables, literal two-point
page tables, and a minimum-page derivation of the red-candidate cut.

Orbit permutations transport R, D and epsilon. Exchanging the two
vertices in an orbit changes only matching signs, which are universally
unassigned during the reduction. The cuts and support are invariant.
Thus any valid coloring in the three-red/six-blue case appears among
the necessary survivors after one explicit transport. Rejecting an
unsigned pattern is legitimate because every cut is necessary; retaining
one does not imply that any matching signing lifts it to a valid graph.

## 3. Exact reduction result

The two author implementations agree on every blue form, every red
candidate position, every per-form diagnostic, the surviving red triple,
and all 72 inside words. [nine_expected.json](nine_expected.json) includes
all 67 forms, full red-candidate lists, all case counts and the survivor.

| Stage | Exact count |
| --- | --- |
| Blue forms | 67 |
| All permitted red triples | 26081 |
| Triples with uniform support at least nine | 6982 |
| Triples passing relaxed matching budgets | 329 |
| Unsigned patterns with any passing inside word | 1 |
| All passing inside words | 72 |

In the main labeling the single pattern is

    B: 01,23,46,48,56,57
    R: 45,47,58.

All other blocks are M. Its support is {0,...,8}; orbits 9,10 are entirely
matching. Precisely the following inside conditions survive:

    epsilon_4=epsilon_5=epsilon_7=epsilon_8=0,
    epsilon_0+epsilon_1 >= 1,
    epsilon_2+epsilon_3 >= 1;
    epsilon_6,epsilon_9,epsilon_10 are unrestricted.

There are 3*3*2^3=72 such words. The entire word set is compared, rather
than just its cardinality. The separate checker also verifies an exact
local-path embedding and the entire flag description in its own labels.
An altered inside flag and a missing survivor are deliberately rejected
against its freshly computed full record set.

## 4. Analytic closure of the surviving pattern

Map the local core 0,1,2,3,4, in that order, to main-label orbits

    7,5,6,4,8.

Its blue pairs are exactly 01,12,23,34, and its red pairs exactly
03,13,14; its other three blocks are M. Every link to the six outside
orbits {0,1,2,3,9,10} in the main labeling is M. The extra two blue K2
blocks lie wholly in this outside set. The arbitrary-complement local
path lemma of FOUR_BLUE.md Section 5 applies, excluding the pattern
for all matching signs and inside colors. No restriction on those
outside blue blocks is a premise of the lemma.

For clarity, the known local argument is as follows. The three red
core sums force core inside colors 0,1,3,4 blue and saturate their
six-page summed caps. At blue01 the core orbit 2 contributes two
summed blue pages, the six outside orbits six, and inside colors four,
saturating twelve. For a saturated uniform pair, the difference between
its two same-color spine page counts is the corresponding entry of
S^2, up to an irrelevant sign, where S has 0 on uniform pairs and
the matching orientation +/-1 on M pairs. Both spines attain the same
cap, so (S^2)_01=(S^2)_03=(S^2)_13=0. All contributions from the other
core orbits vanish, since one factor is zero. Hence the three sign
rows from core orbits 0,1,3 to the six outside orbits are pairwise
orthogonal. Switch outside labels to make the first row all ones.
The other two each have three positive entries, so their mutual
Hamming distance is even and their dot product is 2 modulo 4. It
cannot be zero. This uses no block between two outside orbits.

Thus total nine is impossible. The inherited red and blue minima
give total at least nine, so total is at least ten. At total ten,
subtracting the individual minima leaves one extra pair; the two
color profiles in the theorem are the only possibilities. QED.

## 5. Reproduction, dependencies and trust boundary

Python 3.11+ standard library only. From the repository root:

```sh
python3 book_ramsey_b4_b7_free_involution/check_nine.py --scratch /tmp/book-nine-check
```

The runner executes one child at a time, with all numeric thread
counts one, Python `-O`, and a 120-second child timeout. Explicit guards
survive `-O`. Generated records and logs go outside the source directory.
Failure, timeout or mismatch aborts validation; none is evidence of
mathematical nonexistence. No solver or floating-point calculation is
used. All integers are exact and unbounded. The full CPython 3.11.2
replay took 12.785 seconds with 26300 KiB peak child RSS on Linux: 2.746
seconds for the fast child and 10.037 for the separate child.

The computational premise is the complete unsigned/inside reduction.
The finite-domain, normalization, necessity and local-closure bridges
above are unformalized mathematical reasoning. Two algorithmically
separate implementations by this author are reproducibility evidence,
not an independent peer-review verdict. No full matching-sign search,
unrestricted graph classification or degree theorem is a premise.
No external data or omitted large corpus is needed for this reduction.

The mathematical premises are the analytic support/red/blue bounds in
SUPPORT.md and the arbitrary-complement local path obstruction in
FOUR_BLUE.md. The earlier finite nine-total theorem of EIGHT.md is
refined but not needed as a proof premise; its component-generation
method and fast page routines are reused with explicit attribution.
[six-reviewer-1](../book_ramsey_free_involution_review1/REVIEW.md) and
[six-reviewer-4](../book_ramsey_free_involution_review4/REVIEW.md) supplied
reviews/refinements of earlier analytic bounds, credited in the linked
sources. Neither reviewed this extension.

Primary literature reopened live on 2026-10-01 includes
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1 and Section 3.3](https://arxiv.org/html/2407.07285v2)
and [Radziszowski, DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
with the located interval 22<=R(B4,B7)<=23. The known 21-vertex graph
was exactly reproduced earlier in this campaign; that was baseline
validation, not a new construction. The literature's general upper
flag-algebra certificate was not replayed. The quotient representation
is known block-circulant structure, as in [Wesley, Section 3](https://arxiv.org/html/2410.03625v2);
no historical-priority claim is made for the representation or a
comprehensive literature exclusion. The unrestricted 22-versus-23
endpoint and both ten-pair equality profiles remain unresolved here.

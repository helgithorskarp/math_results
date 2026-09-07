# A complete rank-four cut family decision and search reduction

A good graph has no red or blue complete graph on five vertices. All graphs
below are simple, all ranks are over F2, and both colors are treated separately.

**Theorem.** In a good graph on 43 vertices, no cut has both an all-zero row
and an all-zero column in its cross-adjacency matrix in either color.
Consequently the complete class admitting a rank-four 20+23 cut with all
16 row types and all 16 column types present is empty.

On a fixed labeled 20+23 cut, the theorem removes exactly

    166472869961950839672373904116655134899335779200 * 2^443

physical graphs from the family whose red cross matrix has rank exactly four.
This is approximately 56.0636965570% of that entire family. The factor 2^443
covers every assignment of the internal edges. Every removed cross matrix
has blue rank five, so all these cases survived the earlier necessary lower
bound of four in both colors across this cut.

The remaining rank-four family is not decided. A hypothetical good43 need
not have a rank-four cut at all. This result does not increase the rank-width
lower bound, produce a good43, or improve a Ramsey number.

## Global obstruction

The only nonelementary imported theorem is R(4,5)<=25, from McKay and
Radziszowski, [R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf),
J. Graph Theory 19 (1995), 309--322. We do not rerun its computation.
In a good43 every vertex has degree at most 24 in either color: 25 neighbors
contain a four-clique of that color or an opposite five-clique. Thus each
degree is at least 42-24=18.

For completeness, R(3,3)<=6 follows by taking three same-color contacts of
one vertex. To prove R(3,4)<=9, suppose a triangle-free graph on nine vertices
has independence number at most three. Every neighborhood is independent,
so degrees are at most three. A vertex's nonneighbors form a (3,3) graph,
so there are at most five of them and degrees are at least three. Degree
sum 27 is odd, a contradiction. By complementation R(4,3)<=9 as well.
At a vertex of an 18-vertex coloring, at least nine contacts have the same
color. R(3,4)<=9 on these contacts gives a same-color triangle or an
opposite four-clique. Hence R(4,4)<=18. Only upper bounds are used.

Now suppose a cut A|B has a zero red row u in A and a zero red column v
in B. All red neighbors of u lie in A. Every vertex of A is blue to v.
The set N_red(u) has at least 18 vertices. A red K4 there extends with u;
a blue K4 there extends with v. R(4,4)<=18 gives a contradiction, regardless
of every remaining edge. This proves the theorem for every nontrivial cut,
with no rank, balance, internal degree, symmetry or support assumption.

Equivalently, a good43 cannot have two nonadjacent vertices with disjoint
neighborhoods in either color. This elementary diameter-two observation
is used here as a concrete cut-family consumer, with no novelty claim for
the observation itself.

For arbitrary input graphs, the extractor splits on d_red(u)>=18. In that
case it finds a monochromatic K4 among 18 red contacts and extends it as
above. Otherwise u has at least 25 blue contacts; R(4,5)<=25 supplies a red
K5 or a blue K4 extending with u. Thus even inputs violating the necessary
degree bounds receive a physical monochromatic five, rather than an assumed
Ramsey verdict. The independent verifier checks the ten actual pairs.

## From rank four to the declared complete family

Every rank-four 20-by-23 matrix M factors as U V^T, where U has 20 rows,
V has 23 rows, both have four columns, and both have column rank four.
Conversely every such pair of factors gives rank exactly four: U is
injective as a linear map and V^T is surjective. Cross adjacency is the
dot product of the corresponding row labels in F2^4.

Since V spans F2^4, a row of M is zero exactly when its U label is zero.
Since U spans F2^4, the corresponding statement holds for columns and V.
Thus the entire branch with zero occurring in both label lists is excluded.
In particular this excludes all graphs where every one of the 16 labels
occurs on each side, with arbitrary multiplicities and arbitrary internal
edges. Choice of factor basis, vertex labels and global color does not
affect this statement. No graph automorphism is imposed.

The surviving generator condition is simply

    zero absent from U OR zero absent from V.

This is a necessary filter, not a sufficient Ramsey condition. `family.py`
implements the complete rank-four factor map and this filter, including all
443 internal physical bits. A cut of any input graph can be relabeled to
the fixed 20+23 partition; the count below is for that one fixed labeled cut,
not for isomorphism classes or the union over all cuts and both colors.

If M has a zero row and column, move them to the first row and column.
In M+J, add the first row to each other row. The result has the all-one
first row, a first column zero below it, and M's remaining submatrix below
and to the right. Therefore rank(M+J)=rank(M)+1=5. The removal is disjoint
from the old cut-rank-at-most-three exclusion in both colors on this cut.
It is not claimed disjoint from every other known necessary condition.

## Exact number of distinct physical matrices

Let T_m(r) count ordered m-tuples spanning F2^r, and N_m(r) count those
spanning tuples with every entry nonzero. Put Z_m(r)=T_m(r)-N_m(r), and
g_r=|GL(r,2)|. Then

    T_m(r) = product_(i=0..r-1) (2^m-2^i),
    g_r = product_(i=0..r-1) (2^r-2^i).

The recurrence below independently computes N and T. After m entries, let
D[m,k] count sequences with span dimension k in an ambient F2^r. From
dimension k there are 2^k choices staying in the span, or 2^k-1 if zero is
forbidden, and 2^r-2^k choices increasing its dimension. Start D[0,0]=1.
As a separate exact check, subspace-lattice inclusion-exclusion gives

    N_m(r) = sum_(k=0..r) [r choose k]_2
               * (-1)^(r-k) * 2^((r-k)(r-k-1)/2) * (2^k-1)^m.

Every rank-r matrix has exactly g_r full-rank factorizations U V^T.
Indeed their U columns are precisely the ordered bases of its column
space, and each such U uniquely determines V. Replacing U by U S and V
by V S^(-T) preserves zero labels and full support. This action is free.
There is no division by a basis-group order for degenerate factors here.
It follows that the exact matrix counts at m=20,n=23,r=4 are

    total = T_20(4) T_23(4) / 20160
          = 296935236499420514245609548376980635622730104000,

    removed = Z_20(4) Z_23(4) / 20160
            = 166472869961950839672373904116655134899335779200,

    remaining = 130462366537469674573235644260325500723394324800.

Their exact removed fraction is

    11082739332310042690903561559441706322
    / 19768120928371528230187646401013892765.

For the initial all-16-types branch, let S_m be the number of surjections
from m labeled positions onto 16 labels. Inclusion-exclusion gives
S_m=sum_(j=0..16) (-1)^j binom(16,j)(16-j)^m. The complete initial family
has exactly

    S_20 S_23 / 20160
    = 370003189750044329182215197142967910400000

distinct cross matrices. All are excluded. An independent onto-label
recurrence checks S_m. The full graph count in each displayed class is
its cross count times 2^(binom(20,2)+binom(23,2))=2^443.

## Why the global bridge matters

The compulsory induced 32-vertex full-support core is itself feasible:
`core32.json` has neither monochromatic five and its cross matrix is the
16-by-16 dot-product table. Its two zero representatives both have red
degree 14. It also satisfies the weak necessary core conditions that these
degrees be at least 14 and 11, obtained by allowing four and seven further
internal neighbors. Both a direct complete-core CNF and that CNF with these
conditions returned SAT during discovery. Neither result decided the
43-vertex class. The durable witness is independently checked directly;
no solver verdict, omitted DRAT trace or SAT model parser is a proof premise.

The full-order degree and mixed-neighborhood argument supplies the missing
bridge and excludes every 43-vertex extension in the declared class at once.
No larger global SAT solve was performed or is needed to reproduce the result.

## Scope, dependencies and trust

The prior [rank-width-four theorem](../ramsey_r55_rank_width_four/PROOF.md)
(source `931cd80b76854a3d42f605839508d4a72848fc7c`, Discovery Net h3735,
`bafkreiedakh5pu7x2az265jg65bzpyaa5wfvmmdzcrlonjdqhlkggwnynq`)
motivates the first surviving cut-rank level. Its proof is not a premise
of this exclusion. The earlier accepted
[cut-rank theorem](../ramsey_r55_cut_rank_obstruction/PROOF.md) and
[module-resilience bounds](../ramsey_r55_module_resilience/README.md)
are context; the degree bound is rederived here from R(4,5)<=25.

The claim rests on the short unformalized argument above, elementary
linear algebra and exact counting. The only imported classification is
R(4,5)<=25. The code uses Python integers and the standard library, hashes
for byte identity, and ordinary hardware. Exact recurrences, inclusion-
exclusion, exhaustive small matrices, factor fibers, literal graph checks,
and a separate physical certificate verifier test the implementation.
They do not enumerate the 43-vertex family. No priority or solver-speedup
claim is made. In particular the percentage is a count of physical
assignments in one specified branch, not a fraction of all good candidates
or of the full unrestricted 43-vertex search.

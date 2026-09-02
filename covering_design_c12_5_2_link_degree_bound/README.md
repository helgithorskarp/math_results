# Sharp point-degree bound for optimal `(12,5,2)` coverings

## Result

A `(12,5,2)` covering is a family of 5-subsets of a 12-point set in which
every pair lies in a block.  The known exact value is `C(12,5,2)=9`.

**Theorem.** In every nine-block `(12,5,2)` covering, every point has degree
at most five.  The bound is sharp: `degree_five_witness.json` is a directly
checked nine-block cover with point-degree sequence `(5,4^7,3^4)`.

The proof is symbolic except for 35 small SAT instances at the last boundary.
The instances use 330 mathematical variables, one for each 4-subset of an
11-point set.  CaDiCaL 3.0.1 proved every instance UNSAT, and `drat-trim`
independently verified every binary DRAT proof.  The generated CNFs, proof
traces, and logs stay under `/scratch`; they are not committed.

## Reduction

Fix a point `x` of degree `r`.  Removing `x` from the blocks through it gives
`r` four-subsets of the other 11 points; call these the `A`-blocks.  The
remaining `9-r` five-subsets are the `B`-blocks.  The `A`-blocks must cover
each of the 11 pairs `{x,p}`, and the `A`- and `B`-blocks together must cover
all 55 pairs not involving `x`.  All nine original blocks are distinct,
because a repeated block could be discarded to produce a forbidden
eight-block cover.

The total pair capacity away from `x` is

\[
6r+10(9-r)=90-4r.
\]

This is less than 55 for `r >= 9`, so `r <= 8`.  If `r=8`, there is one
`B`-block.  Each of its six outside points must occur in at least four
`A`-blocks, and each of its five inside points must occur in at least two,
requiring at least `6*4+5*2=34` incidences in eight four-subsets, which supply
only 32.  Thus `r <= 7`.

### Symbolic exclusion of degree seven

For `r=7`, let the two distinct `B`-blocks have intersection size `h`, where
`0 <= h <= 4`, and let `U` be the graph of pairs not covered by either
`B`-block.

For `h >= 3`, classify the 11 vertices as outside both blocks, in their
symmetric difference, or in their intersection.  There are respectively
`1+h`, `10-2h`, and `h` such vertices.  Their `U`-degrees are `10`, `6`, and
`1+h`; since one occurrence in an `A`-block covers at most three incident
pairs, the seven `A`-blocks would need at least

\[
4(1+h)+2(10-2h)+h\left\lceil\frac{h+1}{3}\right\rceil
\]

point incidences.  This is 30 for `h=3` and 32 for `h=4`, exceeding the 28
available.

For `h=0`, the two blocks are disjoint and one vertex `z` is outside both.
The 35 edges of `U` form `K_{5,5}` plus the ten edges incident with `z`.
A four-subset contains at most five `U`-edges, with equality only when it
contains `z`.  Seven `A`-blocks must therefore all attain equality and cover
every `U`-edge exactly once.  But then all seven contain `z`, producing 21
incidences with the ten `U`-edges at `z`, a contradiction.

For `h=1`, write the Venn classes as `I,X,Y,Z`, of sizes `1,4,4,2`.  Assign
weights `1/4` to each `X-Y` edge, `1/6` to each edge from `Z` to `X union Y`,
`7/24` to each `I-Z` edge, and `1/12` to the edge inside `Z`.  The total edge
weight is

\[
16/4+16/6+2(7/24)+1/12=22/3.
\]

Every four-subset has weight at most one.  Indeed, if it contains
`i,x,y,z` vertices in the four classes, its weight is

\[
xy/4+z(x+y)/6+7iz/24+\binom z2/12,
\]

and direct checking of `i in {0,1}`, `z in {0,1,2}`, and
`i+x+y+z=4` gives a maximum of one.  Seven `A`-blocks have total weight at
most seven and cannot cover `U`, whose weight is `22/3`.

For `h=2`, the Venn classes have sizes `|I|=2`, `|X|=|Y|=|Z|=3`.  Here `U`
consists of the nine `X-Y` edges and all 27 edges having at least one endpoint
in `Z`.  If `z_j` is the number of `Z`-vertices in the `j`-th `A`-block, pair
coverage forces

\[
\sum_j z_j\ge12,
\qquad
\sum_j \binom{z_j}{2}\ge3,
\qquad
\sum_j z_j(4-z_j)\ge24,
\qquad
\sum_j \left\lfloor(4-z_j)^2/4\right\rfloor\ge9.
\]

Among seven integers `0 <= z_j <= 3`, these inequalities leave only the
sorted multisets

\[
(0,2,2,2,2,2,2),\quad
(1,1,1,2,2,2,3),\quad
(1,1,2,2,2,2,2).
\]

In the first, the `Z`-to-non-`Z` capacity inequality is equality, so each non-`Z` vertex must
meet a total of exactly three `Z`-vertices across its blocks; every nonzero
contribution is two, impossible.  In the other two, the last inequality is
equality.  For `(1,1,2,2,2,2,2)`, equality in every per-block bound uses all
non-`Z` slots on `X` or `Y`, leaving no occurrence of `I`.  For
`(1,1,1,2,2,2,3)`, the blocks with one or two `Z`-vertices again use all such
slots on `X` or `Y`; the block with three `Z`-vertices has only one remaining
slot, so at most one of the two `I`-vertices occurs anywhere.  In either case
some pair from `I` to `Z` is uncovered.  This excludes degree seven.

### Exact exclusion of degree six

For `r=6`, there are three distinct `B`-blocks.  Encode each of the 11 points
by its three-bit membership mask.  The eight Venn-cell counts sum to 11,
each row sum is five, and the rows are pairwise distinct.  Point relabeling
within Venn cells changes nothing, while permuting the three blocks acts as
`S_3` on mask coordinates.

There are 110 labeled count vectors.  The fixed counts for an identity, a
transposition, and a three-cycle are 110, 28, and 8, so Burnside gives

\[
(110+3\cdot28+2\cdot8)/6=35
\]

orbits.  `audit.py` independently regenerates these counts and exhaustively
tests the sequential cardinality encoding on small inputs.

For each orbit, a Boolean variable selects each of the 330 possible
four-subsets.  Positive clauses require coverage of every pair `{x,p}` and
every pair of other points not already covered by a `B`-block.  A transparent
sequential counter permits at most six selected four-subsets.  Every actual
degree-six point would satisfy one of these instances.  All 35 instances are
UNSAT; the expected hashes and verification summary are in
`expected_summary.json`.

## Consequence for the `C(13,6,3)` frontier

In a hypothetical 20-block `(13,6,3)` cover, a point of degree nine has an
optimal nine-block `(12,5,2)` link.  For any other point `y`, its degree in
that link is the pair multiplicity `lambda(x,y)`.  The theorem and the basic
pair-capacity lower bound give

\[
3\le \lambda(x,y)\le5.
\]

Thus every degree-nine point has `n_3+n_4+n_5=12` and
`n_4+2n_5=9` among its pair multiplicities.  In the exceptional candidate
degree profile `(12,9^12)`, all twelve pairs incident with the degree-12 point
are forced to have multiplicity five.  Equivalently, the low-low pair-excess
multigraph has edge weights in `{0,1,2}` and weighted degree seven at every
low point.  This is a new necessary structural layer; it does not by itself
decide whether a 20-block cover exists.

## Reproduction

Python 3.11 or later is sufficient for generation and the independent audit.
Supply external CaDiCaL and `drat-trim` executables; all generated material is
written below the first argument.

```bash
./run_and_check.sh /scratch/c12_5_2_link_bound /path/to/cadical /path/to/drat-trim
```

The verified production run used CaDiCaL 3.0.1 at source commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04` and `drat-trim` at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  Binary DRAT files total about
400 MB and are deliberately omitted from Git.

## Scope and trust boundary

The symbolic reductions and orbit completeness argument are inspectable in
this directory.  The degree-six exclusion trusts the Python generator,
CaDiCaL, `drat-trim`, their compilers/runtimes, and hardware.  The independent
orbit/Burnside audit, exhaustive small cardinality tests, per-instance CNF
hashes, and separately checked DRAT traces narrow that boundary.  No floating
point, randomized search, timeout, or unverified solver status is used in the
theorem.

The exact value `C(12,5,2)=9` and the maintained gap
`20 <= C(13,6,3) <= 21` are imported from the La Jolla Coverings Repository
version 1.2: <https://zenodo.org/records/19735294>.  Targeted searches found no
prior source for this point-degree-five classification; that supports only a
search-relative novelty statement, not a priority claim.

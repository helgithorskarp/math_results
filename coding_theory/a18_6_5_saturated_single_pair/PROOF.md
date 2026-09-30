# Proof and computational completeness

Agent: **six-code-3**. Role: **researcher**.

Let `F` be a family of five-subsets of an eighteen-point set such that distinct
words intersect in at most two points. Suppose `x!=y`, `d_x=d_y=20`, and
`lambda_xy=1`. We prove `|F|<=56`, with an attaining fixture. The refinement
distinguishing the further deficient neighbors gives exact maxima 56 and 53.

## 1. The forced `(1,4)` split

The words through any fixed pair have mutually disjoint complementary
triples on sixteen points. Hence each pair degree is at most five.
For a degree-20 point `x`,

```text
sum_{z!=x} lambda_xz = 4 d_x = 80,
sum_{z!=x} (5-lambda_xz) = 5.
```

Since `lambda_xy=1`, there is exactly one further deficient neighbor `a`,
with `lambda_xa=4`; all other pair degrees at `x` equal five. Similarly
there is a unique `b` distinct from `x,y` with `lambda_yb=4`.
Let the unique word through `x,y` be `{x,y} union T`, with `|T|=3`.

Delete `x` from its twenty incident words. The resulting quadruples on
seventeen points intersect in at most one point. Their replication numbers
are one at `y`, four at `a`, and five at each of fifteen remaining points.
In the leave graph of uncovered pairs, degrees are therefore thirteen at
`y`, four at `a`, and one at each remaining point, because a point of
replication `r` covers `3r` of its sixteen incident pairs.

Let `t` be the indicator of the uncovered pair `ya`, `m` the number of
uncovered pairs between two of the fifteen degree-one points, and `s` the
number of uncovered pairs from those points to `{y,a}`. The degree sums give

```text
17 = 2t+s,       15 = s+2m,       t-m = 1.
```

Thus `t=1` and `m=0`. Each other point's unique leave neighbor is one of
`y,a`; exactly one of its pairs to those two points is covered. No quadruple
contains both `y,a`. Identifying them therefore gives twenty distinct
quadruples on sixteen points, covering every pair exactly once. This is a
`2-(16,4,1)` design `P`. The five lines through the merged point have one
line assigned to `y` and four to `a`; no duplicate quadruple can be created
by merging, since two preimages would share three old points.

In particular `a notin T`. Applying the same argument to the `y`-star
identifies `x,b`, gives a second `2-(16,4,1)` design `Q`, and shows
`b notin T`. Both designs are on the same old coordinate set
`V=Omega minus {x,y}`, of size sixteen.

## 2. Every such design is an order-four affine plane

A `2-(16,4,1)` design has five lines through every point. For a point `p`
outside a line `L`, four distinct lines through `p` meet the four points of
`L`, and the fifth is the unique line through `p` disjoint from `L`. These
disjoint lines partition the twelve points outside `L` into three lines.
They are mutually disjoint because a point outside `L` lies on only one
line disjoint from `L`. Thus the lines decompose into five parallel classes
of four lines; distinct parallel classes are orthogonal, meaning each line
of one meets each line of the other once.

Choose any two parallel classes and order their lines. Their intersections
give a four-by-four coordinate grid. Each of the other three classes is a
Latin square; orthogonality of classes is orthogonality of squares. Relabel
each square's symbols so its first row is `0,1,2,3`. Complete enumeration
has 24 such Latin squares and precisely two unordered mutually orthogonal
triples. `geometry.normalization()` constructs the two resulting grid
planes and explicit row/column permutations mapping both to the field
plane `P=AG(2,4)`. `verify.check_normalization()` separately enumerates the
squares cell by cell and checks the actual triples, actual planes and maps.

Therefore the first plane can be normalized to the standard field plane.
The checked group of 5,760 valid plane permutations is transitive on all
80 incident point-line flags. Normalize the merged point to `a=0` and
the line assigned to `y` to `L0={0,1,2,3}`. Thus `T={1,2,3}`. Label the
two new points `x=17,y=16`. The `x`-star is

```text
{ {x} union A : A in P, A!=L0 } union { {x,y} union T }.
```

In the second plane the distinguished line is `Lb=T union {b}`; all other
nineteen lines receive `y`. The two stars share exactly their common word,
so their union has 39 words.

## 3. The unique exceptional cross-line pair

Every `Q`-line other than `Lb` meets `T` in at most one point, by `Q`'s
pair uniqueness. Cross-star compatibility makes it meet every `P`-line
other than `L0` in at most two points. It also meets `L0=T union {a}` in
at most two points, so it is a four-arc of `P`. The line `Lb` meets every
`P`-line other than `L0` in at most two points: such a line contains at
most one point of `T`, and possibly `b`. Meanwhile

```text
|L0 intersect Lb| = 4 if a=b, and 3 otherwise.
```

Hence exactly one pair of lines, one from each plane, has intersection
larger than two. All lines of `Q` other than its specified exceptional line
belong to the 840 four-arcs of `P`.

The stabilizer of the flag `(0,L0)` has 72 checked permutations and has
two orbits on the thirteen permissible values `b notin T`: `{0}` and
the twelve points outside `L0`. Normalize `b` to `0` or `4`. The remaining
stabilizers have orders 72 and 6. This uses relabelings, without assuming
that the original code has any nontrivial automorphism. The verifier
generates the permutation group as a closure from nine basic field maps,
checks each map preserves the plane, and checks these flag and point orbits.

## 4. Exhaustive second-plane coverage

The parallel class of `Q` containing `Lb` consists of that line and three
disjoint four-arcs covering its twelve-point complement. Complete exact
cover enumeration gives 600 such classes for `b=0` and 537 for `b=4`.
The corresponding stabilizers cover them by 14 and 92 orbits. The manifest
stores each representative and its orbit size. The verifier independently
enumerates all first classes using sets, explicitly checks each orbit's
members are valid, checks disjoint orbit coverage, and compares the union
with the complete class set. No orbit-size divisibility inference substitutes
for actual coverage.

For each of these 106 first classes `A`, enumerate every parallel class
`C` of four-arcs transverse to `A`. `C` cannot contain `Lb`, since every
one of its lines meets each `A`-line once. Across the representatives there
are 79,643 such classes. Ordering the lines of `A,C` supplies a grid;
mapping both normalized grid planes into it gives every possible affine
completion. Retain exactly those twenty-line planes containing `Lb` whose
other lines are four-arcs. Each accepted plane is encountered four times,
once for each of its other parallel classes. The generator checks this
actual multiplicity for every accepted plane.

For independent coverage, the checker labels each transverse parallel
class by its four line memberships and declares two classes orthogonal
exactly when their sixteen pairs of labels are all distinct. It enumerates
all four-cliques of this orthogonality graph. Together with `A`, a clique
is exactly a five-class affine plane; every possible plane containing `A`
arises this way. It validates every resulting design directly and compares
the actual plane sets with the generator's manifest, carrier by carrier.

After retaining the anchor labels there are three selected `Q`-planes for
`b=0` and 26 for `b=4`. These 29 labelled planes cover arbitrary qualifying
codes after the preceding relabelings; no inequivalent-pair census is claimed.

## 5. Complete residual bounds and attainment

Every other word avoids `x,y`. It must meet `T` in at most two points,
each `P`-line other than `L0` in at most two, and each `Q`-line other than
`Lb` in at most two. The first two conditions leave 378 five-subsets of
`V`; filtering by the third condition gives precisely the residual universe
for each selected plane. The generator directly checks every 39-word star
union and all residual-to-star intersections. The independent checker scans
all 4,368 five-subsets of `V` against the actual 39 star words, using sets,
and compares the resulting word lists entry by entry.

Make a graph whose vertices are the residual words and whose edges join
words intersecting in at most two points. Compatible residual codes are
exactly graph cliques. The generator computes maxima by complete ordered
inclusion/deletion recursion, with the exact upper bound consisting of the
chosen size plus the number of remaining vertices. The checker computes
maxima independently by Bron--Kerbosch enumeration of all maximal cliques.
Every clique extends to a maximal clique, so the largest maximal clique
gives the exact optimum. Both algorithms validate the attaining word sets.

The three `b=0` cases each have 52 residual candidates and optimum 17.
For `b=4`, the exact residual maximum histogram is

```text
optimum       10   11   12   13   14
plane count    2    3    7    9    5
```

Therefore `|F|<=39+17=56`, with `|F|<=39+14=53` if `a!=b`.
The fixture `witness56.json` is a directly checked fifty-six-word code
with degrees twenty at points 16 and 17 and their pair occurring once.
The manifest also has attaining residual sets for all five `b=4` cases
of optimum 14, proving the refined maximum 53 is attained.

## 6. An absent pair with one degree-19 endpoint

Suppose instead `d_x=20`, `d_y=19` and `lambda_xy=0`. The first star is
an affine plane `P` on the sixteen old points, as in the earlier absent-pair
proof. The second shortened star consists of nineteen quadruples on those
points, covering 114 of their 120 pairs. At a point of replication `r`,
its leave degree is `15-3r`, a nonnegative multiple of three. There are
six leave edges and twelve total leave degrees, so at most four nonisolated
vertices. Every positive degree is at least three and at most three, forcing
exactly four vertices of degree three: the leave is a complete graph `K4`.
Its four-set `L` is the unique line that completes the second star to
an affine plane `Q`. This is the completion observation in
six-reviewer-1's
[independent absent-pair review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_absent_pair_review1/REVIEW.md).

All nineteen existing `Q`-lines are four-arcs of `P`. We handle the missing
line without assuming it is also an arc.

If `L` is a four-arc of `P`, then `P,Q` are orthogoval. Remove every residual
word meeting `L` in at least three points, and add `{y} union L`. There
are at most four removed words: each contains a triple of `L`, distinct
words cannot contain the same triple, and `L` has only four triples.
If a word contains all four points it uses all four triples, strengthening
the same bound. All other retained words meet the added word in at most
two points: residual words by construction, `x`-star words because `L`
is a `P`-arc, and existing `y`-star words by `Q`'s pair uniqueness.
The new packing has both point degrees twenty and an absent pair, hence
size at most 56. Writing `k<=4` for the removed words gives

```text
|F|-k+1 <= 56,      |F| <= 55+k <= 59.
```

If `L` is not a four-arc, it contains a triple `T` of a `P`-line `M`.
Replace the existing word `{x} union M` by `{x,y} union T`. This replacement
is compatible with every retained word. Other `x`-star lines meet `M`
in at most one point; existing `y`-star lines, being different from `L`
in `Q`, meet `T` in at most one point; and old residual words meet `M`
in at most two points, hence meet `T` in at most two. Cardinality is
unchanged, both degrees become twenty, and the pair `xy` now occurs once.
The new theorem gives the stronger bound `|F|<=56` in this branch.
In either branch, `|F|<=59`. The number 59 is an upper bound;
no attaining example or exact maximum for the degree-20/19 case is claimed.

## 7. Consequences and trust boundaries

The
[earlier absent-pair calculation](https://github.com/helgithorskarp/math_results/tree/main/coding_theory/a18_6_5_saturated_absent_pair)
gives the same upper bound 56 when both point degrees are twenty and their
pair never occurs. Thus any code of at least 57 words has pair degree at
least two between any two degree-20 points.

Brouwer's established
[A(17,6,4)=20 theorem](https://ir.cwi.nl/pub/6883/6883D.pdf),
applied to shortening, gives `d_z<=20` for every point. If `|F|=M`, the
total point-degree deficit is `sum_z (20-d_z)=360-5M`; consequently at
least `18-(360-5M)=5M-342` points have degree twenty. For `M=70,71,72`
this gives at least 8, 13, 18 such points. In particular every pair in
a 72-word code occurs between two and five times. Brouwer's proof is
imported for these corollaries and is not recomputed here. The restricted
maxima 56 and 53 use no external degree bound.

The finite computations use Python arbitrary-precision integers and sets.
Searches have explicit node caps, and a cap raises an `INCOMPLETE` exception.
All quoted searches finished below their caps; incomplete runs establish
no nonexistence statement. The compact manifest is replayed at entry level;
agreement of aggregate counts alone is not used as evidence of coverage.
The independent algorithms are same-researcher checks, not independent peer
review. The analytical bridges in this document and the finite algorithms
are not formalized in a proof assistant. Neither the restricted theorem
nor its corollaries improve the current global interval 69--72.

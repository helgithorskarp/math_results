# Complete classification of optimal nine-block pair coverings

Let `D` consist of nine distinct five-subsets of a twelve-point set, with
every pair contained in at least one block. Isomorphism means a permutation
of the twelve points taking the unordered block family to another one.

The known value `C(12,5,2)=9` makes these coverings optimal. For completeness
of the classification we import only the previously proved assertion that
every point of such a covering has degree at most five. The mathematical
reduction below and the new enumeration are otherwise self-contained.

## 1. Arithmetic and the degree-three structure

Each point has degree at least three: a block through it contains only four
of its eleven partners. Let `n_i` count the points of degree `i`. Then

```
n_3+n_4+n_5 = 12,
3*n_3+4*n_4+5*n_5 = 45.
```

Consequently, for `a=n_5`,

```
(n_3,n_4,n_5) = (3+a, 9-2*a, a),     0 <= a <= 4.
```

We include all five arithmetic cases. In particular, we do not import the
earlier SAT exclusion of the fifth case.

Label the nine blocks `0,...,8`. Represent a point `x` by its signature
`S_x`, the subset of block labels containing it. The incidence conditions
are exactly:

1. There are twelve signatures of sizes 3, 4, or 5.
2. Each block label occurs in exactly five signatures.
3. Any two signatures intersect.
4. The nine resulting five-subsets are distinct.

Signatures of different points may be identical; the search allows these
multiplicities. For instance, the degree-five profiles include twin points.

For a degree-three point `x`, double counting pairs `(block,y)` gives

```
sum_{y != x} |S_x intersect S_y| = 3*(5-1) = 12.
```

There are eleven positive terms. Exactly one is two and the other ten are
one. Thus the signatures of the `r=3+a` degree-three points are distinct
intersecting triples on nine positions; their pairwise intersections have
size one or two, and the pairs with intersection two form a matching.

More generally, if some of these triples are fixed, each has a remaining
intersection excess budget of one minus its already-used excess. This
budget constrains subsequent signatures, not just subsequent triples.

## 2. Complete enumeration of the degree-three families

After `k` triples have been chosen, each of the nine block positions has
a `k`-bit membership mask. Write `c_m` for the number of positions with mask
`m`, including `m=0`. This histogram loses only the irrelevant names of block
positions. The action of `S_k` on the triple coordinates gives the remaining
isomorphisms; the least histogram under all `k!` actions is canonical.

To adjoin a triple, choose integers `0 <= s_m <= c_m` with `sum s_m=3`.
The new histogram has cells `c_m-s_m` and `s_m`. These are all possible
extensions, because positions in a common cell are interchangeable.
Discard an extension precisely when a new pairwise intersection is zero,
has size at least three, or uses more than one excess at any triple.

Inductively, every admissible family of `k+1` triples arises by deleting one
triple, choosing the represented orbit of the remainder, and adjoining the
corresponding triple. Canonicalization merges precisely isomorphic families.
The counts for `k=1,...,7` are

```
1, 2, 4, 8, 7, 6, 2.
```

The cases needed for covering completion have `r=3,...,7`, hence 27 types.
The histograms are regenerated, rather than trusted as an input list.

## 3. Complete enumeration of the remaining signatures

Fix one degree-three family. A block position `j` must occur in another
`5-d_j` signatures, where `d_j` is its current incidence count. Adjoin
`9-2a` signatures of size four and `a` of size five.

`enumeration.py` lists every four- or five-subset of the nine positions.
It retains as initial candidates those meeting every low signature within
that signature's remaining excess budget. It chooses the four-subsets in
the fixed lexicographic order of their underlying position lists, followed
by the five-subsets in their fixed lexicographic order. Equality is allowed.
Every high-signature multiset therefore has
exactly one such ordered representation.

The recursive checks are only necessary conditions:

- Every new signature meets all previously chosen high signatures.
- No block-column margin or low-signature excess budget becomes negative.
- A column requiring `m` more occurrences has at least `m` remaining slots.
- For each degree class, the available signatures give upper and lower
  bounds on how many remaining slots can or must contain a column.

The only terminal condition is that all column margins vanish. At this
point every pair is covered. Every final representative is also decoded
and checked directly for nine distinct blocks, each of size five. Thus the
positive witnesses do not rely on interpreting a search status.

For the quotient, every permutation of the low signatures is tried. Such
a permutation determines a permutation of their column cells. It extends
to a block-position permutation exactly when corresponding cell sizes
agree; all within-cell bijections are enumerated. This is the full group
preserving the unordered low family. Minimizing the high-signature multiset
under that group gives precisely the full covering isomorphism classes:
an isomorphism must preserve the intrinsic degree-three point set.

The result is:

| `a=n_5` | Low types | Labelled high-signature completions | Covering classes |
|---:|---:|---:|---:|
| 0 | 4 | 2331 | 53 |
| 1 | 8 | 3668 | 46 |
| 2 | 7 | 21 | 6 |
| 3 | 6 | 4 | 2 |
| 4 | 2 | 0 | 0 |
| Total | 27 | 6024 | 107 |

Here “labelled” refers to the nine fixed block positions within each
normalized low type, with high signatures an unordered multiset. These
6,024 objects are intermediate completions, not coverings on a fixed
twelve-point label set. There are 206,814 primary recursive states.

## 4. Independent completeness and isomorphism checks

`audit.py` imports no primary enumeration function.

For the low families it adjoins actual three-subsets of nine named block
positions. It retains one representative per coloured incidence-graph
isomorphism class using NetworkX. This representation does not use column
cell splitting or `S_k` histogram minimization. At all seven levels it
recovers the same types, and it matches every one of the 27 final types
individually to the primary representatives.

For each fixed low type it performs a different completion search. It
starts with every four- and five-subset meeting each low signature; it
does not impose the primary low-excess pruning. It chooses a block column
with nonzero margin and enumerates the complete multiset of remaining
signatures containing that column. The size of this bundle is exactly its
margin. After selecting the bundle, every unused candidate containing that
column is removed, and the search continues on the other columns.

This procedure is exhaustive: every completion determines one and only one
bundle at the chosen column. Signatures in a bundle are taken in a fixed
order with repetition allowed. Intersections with previously selected
signatures, the exact counts of four- and five-subsets, and column margins
are checked throughout. No result is inferred from a timeout.

The independent search visits 815,226 column states and 2,198,275 bundle
states. For all 27 cases the full sorted labelled answer sets have identical
SHA-256 digests to those of the primary enumeration, including the empty
cases. Comparing these digests checks the full answer sets, beyond merely
matching totals; as usual a digest comparison has the negligible theoretical
hash-collision boundary.

Finally, the audit checks every primal representative directly, tests
nonisomorphism of all pairs not separated by simple invariants (343 graph
isomorphism tests), and enumerates all 768 coloured incidence-graph
automorphisms across the 107 representatives. Every automorphism order and
every point orbit agrees with the primary calculation.

## 5. Automorphisms, labelled counts, and marked points

Let `G` be the group of block-position permutations preserving a complete
multiset of point signatures. If a signature `S` occurs `m_S` times, the
order of the point automorphism group is

```
|Aut(D)| = |G| * product_S m_S!.
```

Indeed, each element of `G` has exactly that many lifts to permutations of
the twelve points. Conversely every point automorphism induces a block
permutation, since the blocks are distinct. The kernel consists precisely
of permutations of points with equal signatures.

The automorphism orders and numbers of classes are:

```
order:    1  2  3  4  6  8 12 16 24 32 48
classes:  3 20  1 46  1 19  1  9  2  4  1
```

Orbit-stabilizer therefore gives

```
sum_D 12! / |Aut(D)| = 13,531,795,200
```

coverings on a fixed labelled twelve-point set, with blocks unordered.
The point orbits give 306, 592, and 56 pointed isomorphism classes when the
marked point has degree three, four, and five respectively.

## 6. A different decomposition checks all 56 marked degree-five classes

`marked_five.py` marks a point `h` of degree five and splits the cover into
five through-blocks and four away-blocks. Removing `h` from the former
gives five distinct four-subsets covering eleven points. It enumerates
these directly by column-cell splitting, with no cap on intersections of
column supports. The intermediate type counts are `1,4,24,235,1129`.

For each through-system, let `F` be the graph of pairs not covered by it.
Assign to each of the eleven points a four-bit signature describing its
membership in the away-blocks. Endpoints of an `F` edge must have
intersecting signatures. Each away-block must have weight five; through
and away point degrees together must lie between three and five. Equal
row histories are ordered during the search to remove only permutations
of the four away-blocks. At a terminal state all four blocks must be
distinct. These are exactly the necessary and sufficient completion rules.

Exactly 36 through-types are feasible, with 148 labelled completions.
The point-signature search visits 5,821,442 states. Every completion maps
to exactly one of the 56 marked classes obtained from the full catalogue,
and all 56 occur. This checks the entire degree-five portion using a
different mathematical decomposition.

## 7. Consequence for the (13,6,3) frontier

If a point `p` of a twenty-block `(13,6,3)` covering has degree nine,
deleting `p` from its nine incident blocks gives a nine-block `(12,5,2)`
covering. Thus its link must be one of the 107 classes.

Suppose the global degree profile is `(11,10,9^11)`. Write `h,q` for the
points of degrees eleven and ten and `c=lambda(h,q)`. For every other
point `p`, the imported optimal-link theorem gives `lambda(h,p)<=5`.
Moreover,

```
sum_{p low} lambda(h,p) = 5*11-c = 55-c.
```

Since `c<=degree(q)=10`, this sum is at least 45. If all eleven terms were
at most four, it would be at most 44. Therefore some degree-nine point
`p` satisfies `lambda(h,p)=5`, and its link with `h` marked belongs to the
56 marked degree-five classes.

This is a finite starting list for global compatibility searches. The
present classification alone excludes neither `(11,10,9^11)` nor
`(10^3,9^10)`. No upper bound of five is assumed for the pair `{h,q}`.

## 8. Trust boundary

The new finite result for maximum-degree-five covers trusts the transparent
integer programs, the completeness arguments above, Python, and hardware.
NetworkX 3.7 supplies the independent graph-isomorphism checks; it is not
used in the primary proof. No floating-point calculation, solver verdict,
external enumeration list, or uncompleted search enters the new proof.

The unconditional classification imports the earlier maximum-degree-five
theorem and its reviewed computer-assisted proof. Its upstream SAT/DRAT
instances are not regenerated here. The known minimum of nine is imported
only to describe these coverings as optimal. The earlier degree-profile
classification, the exceptional global profile exclusion, and other
`C(13,6,3)` computational exclusions are not proof prerequisites.

All independent checks here were performed within this research run. They
are not an external review. The theorem is not formally verified in a proof
assistant, and the literature search supports no absolute priority claim.

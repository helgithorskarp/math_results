# Rigidity when all four-bit signatures are nonempty

Consider a hypothetical Ramsey `(5,5;43)` graph with an automorphism of
cycle type `1^10 3^11`, in the four-versus-seven internal-color split.
Write `C0,C1,C2,C3` for the four red moving triangles, and F for the ten
fixed vertices. Each vertex of F is uniform to each Ci. Its signature
S is the subset of indices to which it is red. All counts below refer
to these **four** coordinates, with no condition on the other seven
moving triangles or on the graph induced by F.

This argument starts at the inherited boundary of 26 full cores. It
closes a signature branch, without excluding any additional whole core.
The previous 171 whole-core exclusions and their trust boundaries are
retained. No 43-vertex graph or Ramsey lower-bound improvement is claimed.

## Forced singleton counts

Assume temporarily that no signature is empty. Let x_i be the number
of signatures {i}, y_ij the number of signatures {i,j}, t_ijk the number
of signatures {i,j,k}, and q the number of full signatures. Let U consist
of indices i for which the union of the other three red triangles has
no blue triangle, and let g=|U|.

The accepted [three-triangle uniform-neighbor lemma and its equality
case](../ramsey_r55_order3_eleven_signature_bound/PROOF.md) say that at
most nine uniform vertices have nonempty signature on three red
triangles. Projecting onto the complement of i, an empty projected
signature is now exactly a singleton {i}. Thus x_i>=1.

Any two fixed vertices red to Ci must be blue to one another, since a
red edge would complete a red K5 with Ci. Consequently their total
number a_i is at most four. Also x_i<=2: three singleton-{i} vertices
would be pairwise blue and blue to any blue cross-edge between two
other red triangles. Such a cross-edge exists, since two red triangles
with all cross-edges red would form a red K6. Those five vertices would
be a blue K5.

If i is outside U, a blue triangle on its complement together with two
singleton-{i} vertices gives a blue K5. Hence x_i=1. If i belongs to U,
the inherited [universal two-empty-anchor theorem](../ramsey_r55_order3_eleven_anchor_equality/PROOF.md)
forces at least two fixed vertices blue to the complementary nine
vertices. Under the no-empty assumption these are singleton-{i}
vertices. Hence, precisely,

```text
x_i = 1 + 1[i in U].                                    (1)
```

That universal theorem is specific to the complete four-versus-seven
extension; its two full refutations and formula reduction are an inherited dependency.
They now have an [accepted independent review](../ramsey_r55_order3_eleven_anchor_equality_review1),
commit `3fdfbd7063001dbae84491027bd03882c1e4f2c5`, confirmed during this pass.

For an index i outside U there is exactly one empty projected signature.
The other nine attain equality in the three-triangle lemma: each
singleton occurs twice, each pair once, and the triple never occurs.
Thus, whenever j,k are distinct and both different from i,

```text
x_j + y_ij = 2,
y_jk + t_ijk = 1,
t_(complement of i) + q = 0.                            (2)
```

For each i in U, the particular nine-vertex complementary core contains
a red K4. This is checked directly in every inherited core, with a
literal four-vertex witness in `classification.json`. Equivalently the
two normalized anchor types have words 100,110,110 and 110,110,101 on
pairs 01,02,12; explicit red K4s are {0,3,6,7} and {0,1,4,7}, respectively.
A fixed vertex red to the entire complement would complete a red K5.
Therefore

```text
t_(complement of i) = q = 0       for i in U.             (3)
```

No external value of R(3,4) is used in this step. The literal witnesses
suffice. Finally, for any distinct i,j, vertices with signatures {i}
or {i,j} are pairwise blue and blue to any triangle Ck outside {i,j}.
Four such vertices and one vertex of Ck would form a blue K5. Thus

```text
x_i + y_ij <= 3.                                        (4)
```

## Two hand contradictions and one fifteen-case cover

The 26 inherited cores have g=1 in seven cases, g=2 in eighteen cases,
and g=4 only in core194. This is checked by exhaustive inspection of
all triples in each complementary nine-vertex graph, without a solver.

If U={a}, write b,c,d for the other indices. Equation (1) gives x_a=2,
and (2) gives y_ab=y_ac=y_ad=0. Applying the projected pair equations
for omitted b,c,d gives t_abc=t_abd=t_acd=1. Thus at least five fixed
vertices are red to Ca: the two singleton-{a} vertices and one from
each of these three triple signatures. This contradicts a_a<=4.

If U={a,b}, let c,d be the other indices. The equality for omitted c
gives y_ac=0. The equality for omitted d then gives t_acd=1. But acd
is the complement of good index b, and (3) gives t_acd=0. This is a
contradiction.

These arguments close the no-empty branches for 25 cores. They do not
assert a general classification for g=0 or g=3.

For core194, U consists of all four indices. Equation (1) gives two
copies of each singleton, consuming eight fixed vertices. Equation (3)
forbids every signature of size at least three. The remaining two
signatures are therefore pairs. Equation (4) forces every pair
multiplicity to be at most one. Hence precisely the following fifteen
multisets form a necessary cover of the no-empty branch:

```text
{1,1,2,2,4,4,8,8,p,q},
where {p,q} ranges over all two-subsets of {3,5,6,9,10,12}.
```

These are numeric masks with bit i representing red incidence to Ci.
This is a cover of necessary signatures, not a claim that all fifteen
are realizable. We use all labeled choices; no quotient by a stabilizer
or new normalization is assumed.

In fact the four-triangle setting strengthens (4):

```text
x_i + y_ij <= 2.                                        (5)
```

Three vertices counted on the left are pairwise blue. They are blue to
both remaining red triangles, which have a blue cross-edge, since otherwise
they form a red K6. The three fixed vertices and that cross-edge would be
a blue K5. With x_i=2 for every i, (5) forbids every pair signature. This
contradicts the two pair signatures just proved necessary. Thus core194's
no-empty branch is also excluded by hand.

Therefore **every one of the 26 residual full cores requires at least
one fixed vertex blue to all twelve red-core vertices**. Combining this
with the inherited 171 full exclusions gives the same consequence for
the entire four-versus-seven branch. No further whole core is excluded.

`local_obstructions.json` makes (5) literal in all fifteen profiles on
only 22 vertices. Each certificate specifies three fixed edges forced
blue, and a resulting blue K5. A fixed edge is forced blue by an explicit
core red triangle to which both endpoints are red: if that edge were red,
those five vertices would instead form a red K5. `check_local.py` imports
no producer module and checks every indicated edge, all fifteen profile
identities, and five deliberately corrupted certificates. It needs neither
the full CNF nor a SAT/DRAT executable. The certificates prove the local
profile contradictions; their application still uses the reviewed anchor
theorem to obtain the forced singleton counts.

## Independent arithmetic and complete formula bridge

`classify.py` enumerates weak compositions of the remaining multiplicity
among the eleven masks of size at least two, after imposing (1).
There are 3003 raw completions for each g=1 core, 1001 for each g=2
core, and 66 for core194: 39,105 in total. It applies a_i<=4 and (2)--(4).
`audit.py`, without importing that producer, instead enumerates sorted
lists of remaining masks and reconstructs literal adjacency by rotations.
It checks every core's local Ramsey property, all good and bad indices,
each displayed red K4, all 39,105 arithmetic completions, and the exact
fifteen multisets. Both implementations agree entry by entry. The hand
arguments above explain the finite result.

For each of the fifteen profiles we retain the entire inherited
strengthened core194 formula: 34,320 variables and 616,138 clauses.
This includes the complete accepted r=4 parent, all eighteen core units,
and all four intrinsic two-empty-anchor constraints. Its SHA-256 is

```text
f3a99ee8b211cfcf134f26670ada6fcdce9dc765b92dce3812a5bfdb16f971eb
```

We append exactly forty primary units, assigning the four signature
bits for each of the ten fixed vertices. Each final formula has
34,320 variables and 616,178 clauses. No parent clause or normalizer
is removed. No fixed-to-fixed edge, attachment to a blue moving
triangle, or selected degree profile is imposed.

The existing accepted parent orders fixed vertices lexicographically
by their eleven attachment bits, with these four red coordinates first.
The complete four-bit prefixes must therefore appear in lexicographic
order. Sorting the profile prefixes loses no graph: equal-prefix
vertices still have unconstrained seven-bit suffixes, which can be
ordered by the inherited normalizer. Numeric mask order is deliberately
not used as fixed-vertex order. In the parent convention the bit joining
fixed vertex f to red triangle i has variable 211+11(f-33)+i.

The new formula auditor independently recovers all 320 primary meanings
from the literal unordered-edge orbits on 43 vertices. It compares the
entire strengthened base byte by byte, checks the forty units using the
profile masks, and checks the header and EOF. The inherited base is
regenerated from the complete parent, whose separate C++ checker
reconstructs every clause, and through the previous anchor-propagation
checker. No old UNKNOWN trace is reused as a proof. Six malformed
classification records and six malformed formulas must be rejected;
normal and optimized-Python control reports agree.

The bounded decision, fresh second reconstruction, and final scope are
recorded in `README.md`, `result.json`, `verification.json`, and
`boundary.json`. The fifteen additional full-formula refutations were accepted only after
full DRAT replay against their complete formulas. All fifteen are already
contradictory by unit propagation; none needs a RAT step. These corroborate
the local hand proof rather than being necessary for its final step. Large formulas, proof traces,
and logs remain outside Git and are regenerated by the published code.
Hashes and compact reports alone are not refutations. Internal duplicate
implementations and second replays are not independent peer review;
the hand reduction, the inherited theorem chain, the exact source,
compiler/runtime, and external DRAT checker remain trust boundaries.

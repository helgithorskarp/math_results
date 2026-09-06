# Guarded full propagation of the Core194 attachment theorem

Fix a hypothetical Ramsey(5,5;43) graph in the action `1^10 3^11`, with
four internally red and seven internally blue moving cycles. Its red core
is the canonical Core194 word `100110110110110100`. Use the inherited
complete full normalization and unrestricted full base F.

For each fixed vertex f and moving cycle i, let L(f,i) mean that the three
edges joining f to that cycle are red. In the full primary numbering,

```
L(f,i) = 211 + 11*(f-33) + i,   f=33,...,42; i=0,...,10.
```

## The imported bound is universal over empty fixed vertices

The preceding [Core194 maximal-branch theorem](../ramsey_r55_order3_eleven_core194_maximal)
applies to **any** fixed vertex e blue to all four red moving cycles. Its
proof does not require e to occupy the first fixed row: the local contact
normalization only relabels moving cycles, and the full 216-variable
extension test has no fixed-row order or other full normalizer.

Specifically, if b blue moving cycles are blue to e and h other fixed
neighbors are red, then

```
d_red(e)=3(7-b)+h,  d_blue(e)=21+3b-h.
```

The inherited degree window 18..24 gives b<=4. At b=4, h=9; the blue
neighborhood is a local 24-vertex graph on four red/four blue triangles,
with no red K5 or blue K4. The preceding complete classification proves
that every such Core194 neighborhood transforms to the explicit seed.
Its full 43-vertex extension refutation, without full normalizers,
then excludes this branch for every choice of the distinguished fixed e.
Thus b<=3 whenever the red-core signature of e is empty.

The distinction matters. A bound proved only for the first normalized row
could not simply be imposed at all ten fixed vertices. The universal
quantifier here follows from the preceding theorem and its unrestricted
choice of distinguished vertex, not from symmetry of an already ordered
full formula.

## Exact guarded clauses

For every fixed f, append all 35 clauses

```
L(f,0) OR L(f,1) OR L(f,2) OR L(f,3) OR OR_(j in S) L(f,j),
                  S subset {4,...,10}, |S|=4.
```

If any red-core link is red, every new clause for f is automatically
satisfied. If all four links are blue, the clauses prohibit four
simultaneously blue links to the seven blue cycles. They are equivalent
to at least four red blue-cycle links, or b<=3.

No fixed vertex is assumed to have an empty signature. At the first row,
the already inherited empty-prefix units make the four guard literals
false, so these clauses reduce to the previous positive four-subset form.
At every other row the guard remains. This prevents an unjustified
unconditional bound on vertices with nonempty signatures.

There are 350 positive eight-literal clauses and 11,900 appended bytes.
All literals are existing fixed-to-moving primaries 211..320. No auxiliary,
fixed-edge unit, row order, phase order or other normalization is added.
Every byte of F after its DIMACS header is retained. Its 34,320 variables
and 617,582 clauses become 34,320 variables and 617,932 clauses.

Every complete graph represented by F satisfies the new tail by the
imported universal theorem. Therefore a complete UNSAT certificate for
F plus this tail excludes the **whole Core194 extension class**. An UNKNOWN
solver outcome excludes nothing. Any target SAT result must instead be
decoded into a compact edge list and checked literally on all five-sets.

## Unrestricted-base identity and auditing

F is the Core194 case from
[empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation).
It contains the whole parent, eighteen core units, all four intrinsic
anchor constraints, the first empty prefix and the sharp pair cuts.
Its exact identity is 24,956,496 bytes, SHA256
`2df3017147bd8cb5ceb6f561b8014a5b808e77db14fc6d9f3d6978b53d8c6490`.

Three other formulas are unsuitable substitutes:

1. The old maximal b=4 child already assumes the excluded attachment;
   adding the new bound to it would create an irrelevant contradiction.
2. The preceding 117-variable classifier is local and has different IDs.
3. The preceding 216-variable full extension formula freezes a particular
   neighborhood and the maximal e attachment; it is not the unrestricted
   red-core extension base.

The source pipeline reconstructs the complete inherited parent/preparation
and the one selected Core194 base in an isolated namespace, matching all
previous preparation fields and the exact complete base. It does not
rerun any other full-core solver case. The independent auditor imports no
producer, reconstructs all 320 primary meanings from literal pair orbits,
derives the guards and four-subsets, and compares the entire base and tail.

Truth tables check all 2,048 incidence patterns at each of ten fixed rows:
1,920 nonempty-signature patterns and 64 empty-signature patterns remain
at every row. The 64 rejected patterns are precisely the empty signatures
with at least four blue blue-cycle links. The degree bridge additionally
checks 65,536 empty moving/fixed incidence patterns and retains all 17,728
degree-valid complementary assignments. Sixteen malformed case/formula
inputs are rejected under normal and optimized Python. Fresh verification
rebuilds the complete formula and replays any refutation a second time.

## Scope and trust

The preceding maximal-branch classification, contact normalization and
full transfer have strong author checking and await independent review.
The parent, canonical core cover, intrinsic-anchor and forced-empty
results have accepted reviews at their stated scopes. Core159's separate
full exclusion now has accepted independent review. Older
empty-signature-specific whole-core closures retain the cumulative-count
review boundary. The new guarded clause bridge and solver outcome are
reported at their actual status, independently of those historical counts.

The degree window imports R(4,5)=25 through the parent. Ordinary
unformalized reductions, exact code/interpreter/compiler/hardware, SHA256
and full DRAT replay remain trust boundaries. Internal independent
reconstruction is not peer review or proof-assistant formalization.

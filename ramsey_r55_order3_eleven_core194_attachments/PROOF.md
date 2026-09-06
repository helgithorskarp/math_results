# A complete attachment cover for a Core194 blue empty pair

Let G be a hypothetical Ramsey(5,5;43) coloring with action
`(0 1 2)...(30 31 32)`, fixing33,...,42. Its first four moving
triangles are internally red and induce Core194, word
`100110110110110100`; its other seven moving triangles are blue.
Choose an empty fixed pair u,v, meaning both are blue to the entire
twelve-vertex red core, and assume uv is blue.

The accepted Core194 pair lemma says their common blue neighborhood
is exactly the twelve core vertices. Every other fixed vertex and
every blue moving triangle therefore has one of three contacts to
the ordered pair: RR, RB or BR. BB is impossible. For moving triangles
these are uniform contacts, by the action. The proof below applies
to any distinguished blue empty pair; it does not assert one exists
in every Core194 graph, whose empty pairs might all be red.

## Degree window and forced common-red triangle

The imported theorem [R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
implies that every red and blue degree in G is between18 and24.
A red neighborhood cannot contain a red K4 or blue K5, so has at
most24 vertices; the complementary color gives the same bound on
blue degree. Since the two degrees sum to42, both lower bounds are18.
This imports the theorem, not a new verification of its proof.

Write (a,b,c) for the numbers of blue moving triangles of types
RR,RB,BR, respectively, and (x,y,z) for the numbers of the other
eight fixed vertices of those types. Then

```
a+b+c = 7,                 x+y+z = 8,
d_R(u) = 3(a+b)+x+y,       d_R(v) = 3(a+c)+x+z,
d_B(u) = 13+3c+z,          d_B(v) = 13+3b+y.
```

The thirteen common contributions to each blue degree are the twelve
core vertices and the other endpoint. Hence the exact degree conditions
on these counts are

```
5 <= 3b+y <= 11,           5 <= 3c+z <= 11.
```

In particular b,c<=3, and a=7-b-c>=1. Thus **every blue empty pair
has at least one internally blue moving triangle red to both endpoints**.
If b=c=0, then y,z>=5, contradicting x+y+z=8. Consequently a<=6:
there is also at least one moving triangle red to exactly one endpoint.

Swap the two endpoints if necessary to make b<=c. The possible moving
counts are exactly the following nine for this degree relaxation:

```
(1,3,3), (2,2,3), (3,1,3), (3,2,2), (4,0,3),
(4,1,2), (5,0,2), (5,1,1), (6,0,1).
```

Every listed moving count has a nonnegative fixed count (x,y,z)
satisfying the two inequalities. This means it survives the specified
degree relaxation, not that it extends to a Ramsey graph.

## Exact joint count classification

If b=c, a remaining endpoint swap interchanges y,z, so choose y<=z.
If b<c, no additional comparison on y,z is imposed. Enumerating
nonnegative x,y,z with sum8 and the two displayed inequalities gives
119 canonical joint profiles. Their counts by the moving rows above are

```
6, 18, 18, 19, 9, 27, 10, 9, 3.
```

This is an exact classification of the two stars under the following
explicit relaxation: RR/RB/BR contacts only, seven labeled moving
triangles, eight labeled other fixed vertices, and root degrees18..24.
It is not a classification of complete Ramsey graphs or of their
isomorphism classes.

Independent permutations of the seven blue triangles and eight other
fixed vertices, together with endpoint swapping, act on these contacts.
The counts determine an orbit under these operations. The multiplicity
of a canonical count profile is

```
7!/(a!b!c!) * 8!/(x!y!z!) * e,
```

where e=1 if b=c and y=z, and e=2 otherwise. These multiplicities sum
to4,806,900 labeled assignments out of3^15=14,348,907 assignments with
no BB contact. The independent checker exhausts the3^7 moving words
and3^8 fixed words separately, combines their exact histograms, and
tests physical red degrees. Because constraints depend only on these
counts, this factors the full labeled domain without omitting an
assignment. Its weights match every certificate profile individually.

## Normalization of full extensions

The accepted direct Core194 formula has no row order or other auxiliary
normalizer. Permuting the seven blue moving triangles, keeping their
within-cycle phase labels, commutes with the C3 action and fixes the
red core pointwise. Permuting the eight other fixed vertices and swapping
u,v also preserve the action, core, empty blue pair and every literal
Ramsey constraint. The eight blue-pair consequences are symmetric under
these operations. Thus every operation preserves full graph feasibility.
It need not be an automorphism of an individual graph: it is an allowed
relabeling of the entire graph.

After an endpoint swap, order the blue moving triangles as RR, then RB,
then BR. For the nine moving profiles this fixes fourteen primary units
on the links of33,34 to cycles4,...,10. Append exactly these units to
the entire accepted direct BLUE formula. All other fixed incidences
and all unmentioned edges remain free. No further degree constraint
or selected fixed-neighborhood graph is imposed.

The union of these nine full formulas covers every full Core194 graph
with a distinguished blue empty pair up to the proved relabeling.
Each formula model is a full valid extension by the accepted base
equivalence. The canonical contact words distinguish the nine normalized
moving-count cases; unlabeled graphs with several distinguished pairs
can occur in several cases. Refuting all nine would forbid every blue
empty pair, but would leave the RED empty-pair case open.

The119 joint profiles also record thirty normalized star units, obtained
by sorting the eight other fixed vertices into RR,RB,BR after the stated
endpoint convention. These units have been checked physically, but the
present artifact materializes only the nine moving-profile formulas.
It does not run either nine or119 new SAT searches.

## A tempting stronger local cap is false

The19-vertex edge list `five_fixed19.edges` disproves the proposed local
claim that an endpoint of a Core194 blue empty pair can be blue to at
most four other fixed vertices. Core194 occupies0,...,11; v=12 and u=18
are empty and joined blue. Vertices13,...,17 are all blue to u and red
to v, with core signatures (0,0,1,6,10). All are uniform to the four
red triangles. The graph has69 red edges and no monochromatic K5.
Its local action rotates the four red triangles and fixes the rest.
The common blue neighborhood of u,v is exactly the twelve core vertices.

In fact u is blue to the entire18-vertex graph obtained by deleting it;
that graph has no red K5 or blue K4. Thus the fixture also passes the
corresponding local blue-neighborhood test. The checker inspects all
11,628 five-sets and all3,060 four-sets in that neighborhood, as well as
the core, contacts, action and common-neighbor set. It does not certify
a full43-vertex extension, a global degree completion, or feasibility
of any of the119 full count profiles. Accordingly no b=0 moving case
is removed using this failed cap.

## Evidence and trust boundary

The generator uses the two blue-degree inequalities and multinomial
weights. The independent auditor uses labeled words, physical red-degree
counts, action orbits, and literal vertex permutations. It checks all
profile weights and all unit meanings, not just totals. Normal and
optimized Python agree. Malformed count certificates and local fixtures
are rejected; full-child controls reject altered retained bases or tails.

The complete BLUE base has320 variables,366,069 clauses,14,883,777 bytes,
SHA256 `f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c`.
It is freshly regenerated and independently checked by the reviewed
direct package. Each new child retains every byte of its body and adds
fourteen unit clauses, giving366,083 clauses and no new variable.
Fresh verification reconstructs and checks the same nine full files.
No SAT/UNSAT verdict or proof trace is part of this milestone.

Imported mathematical trust consists of R(4,5)=25, the accepted local
pair lemma, and the accepted direct graph/formula equivalence. Only an
application covering every Core194 graph also needs the accepted z>=2
theorem and a separate resolution of the red-pair case. Cumulative
catalog counts retain their earlier review boundaries. Ordinary
unformalized arguments, exact Python/hardware and hashes for file
identity remain trusted. The new normalization/count proof has internal
independent checking, not independent peer review or formalization.

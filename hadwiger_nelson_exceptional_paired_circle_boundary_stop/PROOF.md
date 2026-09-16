# Exact construction and complete certificate verification

## Placement and cap

Use the exact `omega,r,t,D,P,Q` of README.md. Both `omega` and `r` have
unit modulus. In coordinates relative to `z=omega`, the four centres are

```
-omega, -omega^2, -r*omega, -r*omega^2.
```

Thus they all have distance one from z; the two pairs have unit separation.
Every cross pair has roots z and `ai+bj-z`, reflected in its midpoint. The
strict cross squared distances given in the README show that these are two
distinct roots. The A-relative directions of the roots lie in `U` or `rU`,
and likewise the B-relative directions. Together with the intrinsic paired
segment directions they give exactly `U union rU`. This proves the kernel
formula from the general definition. It contains all four centres.

The two sets of segment midpoints differ: their doubled displacement is
`2t+r-1=(1-r)(2omega-1)`, which is nonzero. All four cross squared distances
are regular and less than four, with neither one nor three. The root z proves
that four pairwise-distinct centre colours are impossible, regardless of the
rest of the support. No ordinary non-four consequence follows.

The slot incidence `x=y=z`, `00 -> 11`, `k=1` has odd parity. Put `d=t`,
`e=t+r-1`, `v=omega^-1 e`. Direct substitution gives `v=d`, hence `q=w=H`
in the reviewed factor

```
F = q*w*(q+w-2H-4) + 4H^2,
q=|d|^2, w=|e|^2, H=d dot v.
```

Consequently F=0 with a singular determinant. This verifies both polynomial
membership and actual physical realization, without elimination assumptions.

There are at most 48 kernel points and four distinct centre points in it.
For each of its other points x and each centre d, the two distinct unit circles
have at most two common points. Thus the complete first boundary has at most
`48+8*(48-4)=400` points. This bound is fixed before the ordinary graph query.
The producer finds 39 kernel points and 111 points after the union; the checker
proves those exact counts by the following separate procedure.

## Producer: pairwise quadratic arithmetic

The base real field is `K=Q(sqrt(3))`, represented by rational pairs `(a,b)`.
Its sign is decided by sign checks and the comparison `a^2` with `3b^2`.
If `a+b sqrt(3)` is a square `(u+v sqrt(3))^2`, then

```
(a^2-3b^2) = (u^2-3v^2)^2,
u^2 = (a +/- sqrt(a^2-3b^2))/2.
```

These identities give a complete rational-square extraction test, with the
`b=0` and `u=0` cases handled separately. The extracted root is chosen positive.

For kernel point x and centre d, put `s=|d-x|^2`. If `0<s<4`, the roots are

```
(x+d)/2 +/- i*(d-x)/2 * sqrt((4-s)/s).
```

At s=4 there is one midpoint; at s>4 there are no roots. All real and imaginary
coordinates have the form `A+B sqrt(q)` with A,B in K and q>0 in K. The producer
reduces square radicals to K and identifies two nonsquare radicals when their
ratio is a square in K. Each point therefore needs at most one of five stored
positive radical representatives.

For two different representatives q,t, the set
`{1,sqrt(q),sqrt(t),sqrt(q*t)}` is linearly independent over K: q and t are
nonsquares and q/t is not a square. A pair's squared distance can therefore be
tested by its four K coefficients, without constructing the entire compositum.
Equal radical classes reduce to one quadratic extension. This supplies exact
merging and all-pairs edge production. The checker does not rely on the
producer's square-class independence argument or its intersection formula.

## Standalone checker: explicit embeddings and enclosure coverage

The geometry certificate has keys `roots` and `points`. A base coefficient
is `[[a_num,a_den],[b_num,b_den]]`, meaning `a+b sqrt(3)`; a complex base
coefficient has two such entries. A point `[A,B,j]` means the actual complex
number `A+B sqrt(roots[j])`, using the **positive real** square root. The index
-1 represents A alone and requires B=0. All fractions must be reduced with
positive denominators. Root positivity is checked exactly in K.

All numbers are real algebraic expressions in explicitly chosen positive
roots, so real feasibility is immediate once positivity is proved. For a
nonnegative rational interval `[l,h]`, at scale `N=2^192` the checker uses

```
L = floor(sqrt(floor(l*N^2)))/N,
H = (floor(sqrt(floor(h*N^2)))+1)/N.
```

The floors are exact integer square roots, giving `L<=sqrt(l)` and
`H>sqrt(h)`. Apply this first to 3 and then to each positive K radical.
Addition, multiplication, subtraction and interval squaring use exact rational
endpoint bounds. Dependency only enlarges enclosures. There is no floating
rounding, subdivision, adaptive precision or numerical tolerance.

Every pair of point boxes is separated along at least one coordinate, proving
all 111 listed points physically distinct. Every squared-distance interval
that avoids 1 proves a nonedge. For every remaining pair the checker expands
its squared distance into formal radical monomials. It reduces each repeated
radical by its supplied equation, and uses `sqrt(3)^2=3` in the rational base.
The expansion must equal the constant 1 identically. This is a sufficient
algebraic identity even if several radicals have hidden algebraic relations.
Thus radical-independence assumptions are unnecessary for the checker.
All 6,105 pairs are decided; ambiguity is an error, not a nonedge.

The exact minimum enclosure margins are recorded in EXPECTED.json. They imply
coordinate separation greater than 1/1000 along at least one coordinate for
every pair, and nonedge squared-distance gap greater than 1/3000 from 1.
These are fixed-instance margins, not bounds for nearby placements.

## Independent support-completeness argument

The checker constructs the 48 formal kernel addresses directly from D and
the two direction orbits, identifies their supplied base-field coordinates,
and finds 39 distinct kernel points. For every one of the 35 noncentre kernel
points and every one of the four centres, it computes their exact squared
separation in K. Elementary circle geometry requires zero, one or two roots
according as this separation is greater than, equal to, or less than four.

Using the independently checked complete graph, it counts points adjacent
to both circle centres and requires precisely that number for every pair.
There are 8 empty pairs, 4 tangencies and 128 secant pairs. Since two distinct
unit circles have at most two intersections, these tests prove that **all**
required roots are listed, not merely that supplied roots are valid. Finally
every listed point must be a kernel point or one of these intersection roots.
Both inclusions are proved, so the supplied points are exactly Q.

## Ordinary colour certificate and limits

The coordinate hash serializes the full `roots,points` object as sorted-key,
compact JSON plus newline. The edge hash uses lexicographically ordered pairs
in the same format. The checker reconstructs both hashes. It validates the
111-symbol four-word and five-word directly on all 302 complete unit edges.
The five-word merely assigns a new colour to one vertex of the four-word.

The discovery CNF has exactly one of four colours per vertex and forbids equal
colours on every reconstructed unit edge. Fixing vertex zero to colour zero
uses only a global colour permutation. There is a single SAT query. The
positive theorem trusts the checked word, not the solver's verdict.

The result is an exact four-colourability certificate for one finite graph.
It neither colours the infinite support nor proves an exact chromatic number.
All proofs and programs are author-side, not formally mechanized or
independently peer-reviewed. Python integer/Fraction arithmetic, the explicit
real-root embedding and the elementary Euclidean arguments are trust
boundaries. No extra layer, altered placement or replacement stratum is tested.

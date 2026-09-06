# One complete fixed-star test on Core186

Input is `input.edges`, copied exactly from the prior structured-candidate
package at source `c4e697c219deb07c08dd638baf609c323a9928ee`. SHA-256:
`f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441`.
It labels vertices 0..42; listed pairs are red and omitted pairs blue.

The action cycles each of the triples 0..2, 3..5, ..., 30..32 and fixes
33..42. For each fixed vertex f, independently from the same input graph,
vary its eleven uniform contacts to these triples. Bit i of mask A says
that all three contacts from f to triple i are red. Every other physical
pair keeps its input color, including all pairs between fixed vertices.
These moves preserve the action and the prescribed Core186 word
`100110110011011101`. No degree restriction or necessary condition that
holds only for Ramsey graphs is imposed on these defective colorings.

The bounded computation is ten exhaustive blocks of 2^11 assignments.
Minimize the number of physical monochromatic five-sets, counting red and
blue separately. Retain exact coefficients, the full score table's hash,
every block's complete set of minimizing masks, score histograms, the best
changed assignment value, and improving/neutral assignment counts.
Ties for the overall representative are resolved by (score, f, A).
Do not update the base between blocks. Do not launch another sweep, random
restart batch, or move family during this milestone.

## Exact objective

For a physical five-set Q, examine its pairs outside the variable star.
There are at least six such pairs. If they contain both colors, Q never
contributes. Otherwise their color c is uniquely determined. Let S be the
set of triple indices whose variable contacts appear in Q, with repeats
collapsed. Q contributes precisely when all variables in S have color c.
Its physical multiplicity is one, regardless of how many repeated indices
occur. Aggregate these contributions into nonnegative integers B_f[S]
and R_f[S]. Mask zero includes *all* unconditional contributions, both
five-sets avoiding f and five-sets through f with no variable contact.

The exact blue and red counts are respectively

    sum(B_f[S] : S & A == 0),
    sum(R_f[S] : S & A == S).

Thus the total is their sum, with each mask-zero term counted once in its
own color. Subset zeta transforms compute all scores using integer
arithmetic. Each support has at most four bits. There is no probabilistic
or solver assumption.

## Independent reconstruction and finite scope

The verifier imports no producer. It counts monochromatic K5s avoiding f
by bit-intersection clique recursion. Every remaining possible K5 equals
f plus a monochromatic K4 in G-f. Discard a K4 if one of its nonvariable
contacts to f has the opposite color; its variable contact indices yield
S. This gives an independent reconstruction of every coefficient. The
verifier evaluates all 20,480 assignments by direct support predicates,
with no zeta transform, and compares every separate blue/red count. It
checks both the original and chosen graphs by complete literal five-set
enumeration as well as clique recursion, and verifies every physical pair
under the action and the winner's exact change support.

The ten assignment families share exactly the original graph: their
variable edge sets are disjoint and no changed member of one family can
equal a member of another. Therefore their union has
1 + 10*(2048-1) = 20,471 distinct labeled colorings, of which 20,470 differ
from the input. This finite union is the entire claim scope. It does not
allow simultaneous changes at two fixed vertices, changes between moving
triples, changes between fixed vertices, or changes of the prescribed
core. A negative result is not a family exclusion or a Ramsey bound.

Checks additionally exhaust all visible colorings on the specified five-
and six-vertex grouped-star fixtures and all four assignments for each,
then compare literal physical counts. A seven-vertex control checks the
often-missed unconditional K5 through f. Corrupted coefficient weights,
supports, minima, argmins, block identity and tables must be rejected.
Checks use explicit exceptions and must also pass Python's optimized mode.
These are author checks with algorithmic independence, not external peer
review or formalization. Python, ordinary exact arithmetic and hardware,
the unformalized reduction and parsing remain trust boundaries.

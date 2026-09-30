# Degree-two links are split affine planes

Author: six-code-1, researcher. Date: 2026-09-30.

**Lemma.** Let \(\mathcal P\) be twenty four-element subsets of a
17-element set, any two meeting in at most one point. Suppose exactly
two points \(a,b\) have replication less than five. Merging \(a,b\)
produces an affine plane of order four. Conversely, split the five
lines through any point of an affine plane of order four into two
nonempty parts, replacing that point by \(a\) on one part and \(b\)
on the other. This constructs precisely a packing of the stated kind.

In particular, at a replication-twenty point of an \((18,6,5)\)
code whose pair-deficit support has degree two, its twenty shortened
quadruples are obtained by splitting a point of an affine plane.
This application does not require the whole code to have 72 words.

## Proof

Every point replication \(q_y\) is at most five, since the other
three points of its incident quadruples are disjoint. Exactly
120 of the \(\binom{17}{2}=136\) pairs are covered. The leave
graph has sixteen edges and degree \(16-3q_y\) at \(y\).
The sum of deficits \(5-q_y\) is \(85-80=5\). Thus the fifteen
points other than \(a,b\) have leave degree one, and the two
high leave degrees sum to seventeen.

Let \(e\) indicate whether \(ab\) is a leave edge, and let \(p\)
count leave edges between two other points. Subtracting the two
degree sums gives \(2e-2p=17-15=2\). Hence \(e=1\) and \(p=0\).
The leave is a double star: every other point has exactly one
uncovered pair to \(a\) or \(b\), and all pairs among those
fifteen points are covered.

No quadruple contains both \(a,b\). Merge them into a single
point \(c\). A pair between two other points remains covered
exactly once. For every other point \(y\), exactly one of
\(ay,by\) was covered, so \(cy\) is covered exactly once.
All resulting quadruples are distinct: a repeated quadruple
would repeat a pair of their other points. We obtain twenty
four-subsets covering every pair of a 16-set exactly once,
a \(2\!-(16,4,1)\) design.

This is an affine plane of order four directly from its parameters.
Every point is on five lines. Given a line and a point outside it,
four of that point's lines intersect the given line, one at each
of its four points. The fifth is its unique disjoint line. Two
points have a unique line, and noncollinear points exist.
These are the affine-plane axioms.

Conversely, a split of the five lines through \(c\) preserves
coverage of every pair between other points. Each other point
lies on exactly one line with \(c\), so it acquires a covered
pair to exactly one of \(a,b\); their mutual pair is uncovered.
The result is a twenty-quadruple pair packing with exactly the
two under-replicated points. Their replications are \(1,4\)
or \(2,3\), up to exchange; the deficit partitions are
\(4+1\) or \(3+2\). This proves both directions.

## Scope and exact examples

This is a structural reduction, not an assertion that every abstract
leave graph extends to a global code. No classification or uniqueness
theorem for order-four affine planes is used or claimed. The proof
assumes twenty quadruples; only the application forcing that number
from 72 words imports Brouwer's established bound.

`check_support15.py` constructs the twenty lines of the standard
affine plane over \(\mathbb F_4\), directly checks all 120 pairs,
and checks all thirty nonempty proper splits of the five lines
at its origin. It verifies every resulting 17-point packing,
its double-star leave, and the exact inverse merge. The unsplit
plane plus an unused seventeenth point reproduces twenty words
of weight four and minimum distance six, the familiar lower
certificate in \(A(17,6,4)=20\). These examples and the theorem
are separate from a 72-word global construction.

It also directly checks the inverse merges at all three saturated
degree-two points of the published 69-word incumbent. Each produces
twenty lines covering every pair of its sixteen active points once.

The proof is an ordinary combinatorial argument, not a formalization
or independent review. No priority claim is made.

# A 72-point line-free set has at most one eight-point plane

**Computer-assisted theorem.** Let (S\subseteq\mathbb F_5^3) have
72 points and contain no complete five-point affine line. At most one
affine plane meets (S) in eight points.

**Corollary.** In the preceding [global four-case cover](../low_planes72/README.md),
the cases AAA and AAB are impossible. The remaining cases are ABB and BBB,
where (A=(8,16,16,16,16)) and (B=(9,15,16,16,16)).
In particular, the previously proved inequality (a_8+a_9\ge5) now implies

\[
a_8\le1,\qquad a_9\ge4.
\]

This does not exclude 72-point sets altogether, decide 71, or improve the
numerical interval (70\le r_5(\mathbb F_5^3)\le72).

## 1. Projection from two eight-point planes

Every affine plane section has at most 16 points. For a finite verification,
the existing [planar enumeration](../plane_caps.cpp) checks all 1,081,575
17-subsets of the 25-point plane and finds none without a complete line.
A larger line-free section would contain a line-free 17-subset.

Suppose two eight-point planes exist. They are not parallel: otherwise the
five parallel planes contain at most (8+8+3\cdot16=64) points.
Choose affine coordinates so that they are (x=0) and (y=0), with their
intersection parallel to the (z)-axis. Define the fiber weights

\[
w_{xy}=|\{z:(x,y,z)\in S\}|\in\{0,1,2,3,4\}.
\]

Their total is 72. The five row sums and the five column sums are both

\[
(8,16,16,16,16). \tag{1}
\]

Indeed the four companions of an eight-point plane have total 64 and each
has size at most 16. Every affine line in the quotient plane corresponds
to an affine plane in three dimensions, so its weight is at most 16.

For any affine line containing (k) points of (S), its six containing
planes have total section size (72+5k): the line points are counted six
times, and all other points once. Applying this identity to the intersection
of the two small planes gives

\[
72+5w_{00}\le8+8+4\cdot16=80,
\]

so (w_{00}\le1). Applying it to a fiber contained in either small plane gives

\[
72+5w_{0y}\le8+5\cdot16=88,
\]

and similarly for (w_{x0}). Thus all weights in row zero or column zero
are at most three.

## 2. Complete finite enumeration

Put (d_{xy}=4-w_{xy}). Its row and column sums are

\[
(12,4,4,4,4),
\]

and its total is 28. The interior (4\times4) block determines every other
entry. If its sum is (T), then

\[
d_{00}=T-4\in\{3,4\},\qquad T\in\{7,8\}.
\]

Every interior row and column has sum at most three, because the omitted
axis entry is at least one. Conversely, given a nonnegative integral
interior block with these conditions, set

\[
d_{x0}=4-\sum_{y=1}^4d_{xy},\quad
d_{0y}=4-\sum_{x=1}^4d_{xy},\quad d_{00}=T-4.
\]

These entries all lie in ([0,4]), and the required margins follow.
The remaining necessary condition is that every quotient line has deficit
at least four, equivalently weight at most 16.

[deficit_enumeration.cpp](deficit_enumeration.cpp) visits every interior
block in this exact range, then tests all nonvertical quotient lines.
The vertical lines already satisfy (1). It retains **4,442** different
weight matrices. No solver or heuristic pruning enters this enumeration.

[row_enumeration.cpp](row_enumeration.cpp) independently constructs the
same list: it enumerates the 35 possible weight rows of size 16 whose
first entry is at most three, chooses four such rows, infers the zero row
from the column margins, and checks the quotient line bounds. The sorted
outputs agree entry by entry. All arithmetic consists of small integers;
indices are at most 25 and partial sums at most 80.

## 3. Affine equivalence and the 164 representatives

For each retained weight matrix, select an ordered pair of nonparallel
quotient lines of weight eight. Write them as

\[
u\cdot p=b,\qquad v\cdot p=c.
\]

For every (s,t\in\mathbb F_5^\times), apply

\[
p\longmapsto(s(u\cdot p-b),\ t(v\cdot p-c)). \tag{2}
\]

All these maps are invertible and put the selected lines on the coordinate
axes. Every affine equivalence between normalized matrices occurs this
way: the preimages of the two zero coordinate lines must be an ordered
pair of weight-eight lines, and their defining affine forms are determined
up to nonzero scalars. Thus (2) gives the full intersection of each affine
orbit with the normalized catalogue, not merely a subgroup of symmetries.

[quotients.py](quotients.py) checks that these orbits are disjoint and cover
all 4,442 entries. There are **164** orbits. Their lexicographically least
representatives and their multiplicities are in [orbits.json](orbits.json).
As an additional control, the verifier uses all 12,000 elements of
\(\operatorname{AGL}(2,5)\) on samples with each occurring number of
weight-eight lines, and obtains exactly the same normalized orbit.

An affine change in quotient coordinates lifts to an affine transformation
of the three-dimensional space. Consequently it suffices to exclude lifts
of these 164 representatives.

## 4. The lifting formulas are complete

Use a Boolean variable (X_{xyz}) for each of the 125 points, with variable
number (1+25x+5y+z). The formula for a quotient matrix (w) imposes:

1. No one of the 775 affine lines is completely selected.
2. Each of the 155 affine planes contains at most 16 selected points.
3. For every (x,y), exactly (w_{xy}) points in its five-point fiber are selected.

These conditions are necessary for a lift. They are also sufficient for
the question in hand: any model decodes directly to a 72-point line-free
set with the required quotient and its two eight-point planes.

We add a proved normalization. The interior deficit sum is at most eight,
so at least eight of its 16 entries have deficit zero. Their fibers each
have four selected points and a unique hole. Eight quotient points cannot
lie on one five-point affine line. Choose the first noncollinear triple
of four-point fibers in the fixed lexicographic order. If their hole heights
are (h_1,h_2,h_3), there is a unique affine function \(\ell(x,y)\) taking
these three values. The invertible affine map

\[
(x,y,z)\longmapsto(x,y,z-\ell(x,y))
\]

preserves all quotient weights and sends the three holes to height zero.
We may therefore require those three height-zero points to be absent.
There is no unproved permutation of coordinate values or assumed
transitivity of planar sections.

[model.py](model.py) generates these exact formulas. The cardinality
constraints use the sequential-counter encoding from the pinned Python-SAT
version. The auxiliary variables are existential; the geometric clauses
refer to the primary point variables only. The generator also accepts a
70-point quotient as a positive control; the verifier solves it and checks
the reconstructed set directly.

## 5. Checked exclusions and conclusion

CaDiCaL 1.9.5, through Python-SAT 1.9.dev15, returns UNSAT for every one of
the 164 formulas. A separate DRAT-trim process checks each proof against its
exact generated CNF. All 164 checks report `s VERIFIED`. The per-case CNF
hashes, proof hashes, formats, sizes, and verification results are recorded
in [certificates.json](certificates.json).

The fresh-source verifier regenerates all 164 CNFs and compares them
byte for byte by SHA256 with the proof inputs. [replay.py](replay.py)
regenerates solver proofs and invokes DRAT-trim again; UNKNOWN, a SAT model,
a changed CNF, or a failed checker stops the run with an error.

Therefore no representative lifts. Sections 1–3 show that any hypothetical
72-point set with two eight-point planes would give one of these lifts,
which proves the theorem. Combining it with the earlier global cover gives
the stated corollary.

The trust boundary includes the written finite reduction, the two ordinary
C++ enumerations, the affine canonicalizer, the Python-SAT cardinality
encoder, and DRAT-trim. Solver answers alone are not evidence for the
exclusions; every answer has a checked proof. This is not a proof-assistant
formalization and has not received independent peer review.

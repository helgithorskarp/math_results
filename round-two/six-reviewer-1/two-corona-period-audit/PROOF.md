# Independent physical and logical reduction

Actual author six-reviewer-1, role independent mathematical reviewer.
The target is lemma9992, authored by six-heesch-1. Its written statement and
literal input/tiling data were visible during this derivation; this is not
a blind review. The independent executable below was written before reading
the target executable, RUP trace, counterexample or expected output.

Let Q, U, the nineteen isometries and eight periodic representatives be
exactly the finite data in input.json and tiling.json. The theorem concerns
every nonempty subset S of U. It fixes physical maps from Q before changing
S; normalizing a changed shape would change the question.

For a signed permutation matrix M and translation t, transform the doubled
cell center \(2p+(1,1)\). Its image cell coordinate is
\[
 \frac{M(2p+(1,1))+2t-(1,1)}2.
\]
Both coordinates are integers, and transforming the four square vertices
gives the same square. This proof includes reflections and negative
coordinates. Normalize the eight transformed Q coordinate lists, sort those
lists lexicographically, and recover the prescribed orientation indices.
The root is exactly the identity. The normalization offset is recovered
from Q, never from the candidate S.

Two integer grid unit squares have overlapping interiors exactly when
their lower-left coordinates coincide. Thus every collision of a site p in
copy i and site q in copy j gives precisely the clause
\(\neg x_p\vee\neg x_q\). When p=q it is a unit. All unordered copy pairs,
including first/second and second/second, are retained. This is not an
assumption that other possible rigid motions are registered.

For every possible occupied prefix cell contributed by site p, and every
one of its nine Moore neighbors w, collect all sites q whose image under
ANY next-prefix map covers w. The clause
\(\neg x_p\vee\bigvee_q x_q\) is exactly the required coverage implication.
A missing supplier gives a unit, a repeated supplier is one Boolean
literal, and a tautology can be deleted. Taking all contributors at levels
zero and one gives both whole-prefix halo inclusions, with no connectivity
or topology premise.

For these grid patches, placing the whole boundary of P in the interior
of a larger union R, with P contained in R, implies that every Moore
neighbor of an occupied P cell is in R. Each omitted neighbor would leave
points arbitrarily close to their common edge or vertex uncovered. Conversely,
the full Moore inclusion places P inside the interior of R: all four
quadrants around every P vertex and both sides of every P edge are covered.
Therefore complete admissible grid-motion coronas imply the clauses.
The extra contact and disc requirements of Heesch coronas are not required
for the logical theorem itself.

The lattice has generators \(u=(22,6)\), \(v=(-6,22)\). Its determinant
is520, and
\[
 h_1=11u-3v=(260,0),\qquad h_2=4u-v=(94,2);
 \quad u=-h_1+3h_2,\ v=-4h_1+11h_2.
\]
Every grid cell has exactly one quotient label
\[
 s=y\bmod2,\qquad r=(x-47(y-s))\bmod260.
\]
Thus all520 labels are represented by (r,s), with 0<=r<260 and s=0,1.
The independent checker groups the eight representative images by these
labels. It also derives the adjugate naming
\((22x+6y,-6x+22y)\bmod520\) as a bijective alternative label,
and verifies the entire formula under the corresponding auxiliary-variable
renaming. This second naming is for literal trace compatibility, not a
different physical condition.

Write \(C_r=\sum_p m_{rp}x_p\), with positive integer multiplicities
retained. A proposed bad-row variable z_r is permitted exactly when
\(C_r\ne1\): for each term of coefficient one impose
\[
 \neg z_r\vee\neg x_p\vee\bigvee_{q\ne p,\ m_{rq}>0}x_q.
\]
If z_r is true, a solitary coefficient-one active term is forbidden.
Zero active terms, two distinct active terms, or a solitary term with
coefficient at least two all satisfy these clauses. Conversely those are
all ways a nonnegative integer count can differ from one. Requiring some
z_r gives a lossless existential encoding of failure of the fixed period.
The nonempty clause is essential: the empty source satisfies all packing
and halo implications and fails the period.

A RUP addition c is sound if unit propagation from the preceding database
and the negation of every literal of c reaches a contradiction. The fresh
checker implements repeated complete clause scanning, not hints or solver
calls. Each propagation step is a consequence of a clause whose other
literals are false. An empty derived clause therefore refutes the original
formula. No solver success, finite mask sampling or incomplete enumeration
is a premise. Exact replay of the supplied trace remains to be recorded
after the independent source has been sealed.

When every quotient count is one, translating all eight representatives
by the lattice covers every grid cell exactly once. It gives a plane
tiling with disjoint interiors and no uncovered point: shared square
boundaries are included. Summing the520 rows counts each selected site
eight times, so \(8|S|=520\), hence |S|=65.

This is a finite fixed-envelope/fixed-motion statement, not a global
classification of shapes or coronas. Common Euclidean conjugation transports
all sets, maps and the translation lattice, so the statement holds in any
common coordinate frame. It does not permit changing motions individually.

## Strengthening and improvement opportunities

The independent propagator records the complete transitive original-clause
support of every addition. If the final support is a strict subset, it
supplies a rigorously weaker sufficient Boolean premise set: retain only
that support and the ordered additions whose supports are contained in it.
An independent second replay checks this extraction. This is a support
certificate, not a minimum support or a whole-copy/whole-stage minimality
theorem; its numerical size and any geometric consequence await the trace.

The useful next broadening is to alter the early physical motions or enlarge
U and certify the new lossless implication. The target's larger guarded
UNKNOWN run supplies no such theorem. One stage alone needs a counterexample
or independent failed-period witness before it can be called insufficient.
The literal counterexample has not yet been opened here.

All physical, quotient, Boolean and RUP arguments are ordinary and
unformalized. Python and the independent implementation are trust
boundaries. Source/input/certificate identities and full replay checks
must accompany the final verdict.

# A conditional minimum in a fixed-corona family

Agent: **six-heesch-2**. Role: **researcher**. Status: computer-assisted
conditional minimum, with an independently checked UNSAT certificate. The
geometric implication into the formula is a written proof; it is not
formalized or independently peer reviewed.

Let T0 be the 215-cell unmarked polyiamond in the sibling
[hexapillar reproduction](../heesch_polyiamond_hexapillar/README.md). All cells
are closed unit equilateral triangles, with vertices in the axial basis
(1,0), (1/2,sqrt(3)/2). Let star(v) be the six unit triangles incident to v.
Define

\[
D=T_0\cup\bigcup_{v\in V(T_0)}\operatorname{star}(v).
\]

D has **354 triangles**. Let Pi be the **131 exact isometries**, with corona
levels 0 through 5, in the reproduction's `coronas.json`. Neither D nor Pi is
varied in this result.

**Theorem.** Suppose P is a nonempty topological-disc polyiamond contained
in D. Suppose the copies Pi(P), with exactly those prescribed levels, have
disjoint interiors and form five complete coronas. If the number of 300-degree
vertices of P strictly exceeds its number of 60-degree vertices, then

\[
|P|\geq215.
\]

T0 attains this minimum: it has 215 triangles, nine 300-degree vertices,
eight 60-degree vertices, and the independent mesh certificate verifies five
complete disc coronas. Thus **215 is the minimum in this specified family**.
Prefix topology need not be used in the lower-bound calculation: its formula
only requires strict surrounding and disjoint interiors. The claim therefore
also holds if the admissible corona prefixes are relaxed to allow holes.

This is not a minimum among all finite-five polyiamonds. It does not exclude
smaller tiles with different placements, cells outside D, a different finite
upper obstruction, or no positive 300/60 surplus.

## Necessary formula

For every t in D introduce a Boolean variable x_t, meaning t belongs to P.
No symmetry identification is made. Every triangle and every prescribed
motion participates in the constraints.

**Nonoverlap.** If two different prescribed copies send t and u to the same
unit triangle, add `not x_t or not x_u`. Isometries in Pi preserve the unit
triangular grid. Two such elementary triangles have overlapping interiors
exactly when they are the same triangle. Consequently every disjoint family
of full copies satisfies these clauses. If t=u, this is simply a negative
unit clause.

**Complete stars.** For a motion p at level k<5, a selected triangle t, and
every triangle s sharing a vertex with t, the triangle p(s) must be covered
by the prefix through level k+1. Add

\[
\neg x_t\ \lor\!
\bigvee_{q(u)=p(s),\ \operatorname{level}(q)\leq k+1}x_u.
\]

The case s=t is automatic from p(t) itself and is omitted. To justify the
other cases, take a vertex v of p(t). Strict surrounding places v in the
interior of the next cumulative prefix. A finite union of unit triangles
can have a neighborhood of v only if all six incident unit triangles are
present. Hence p(s) is covered by one of the enumerated full copies. All
possible cells u in D and all allowed prefix copies q are included. There
is no additional pool or grid-locking assumption about hypothetical
unrestricted coronas; this theorem deliberately fixes Pi.

**Single-tile links and angles.** At each vertex of D, enumerate every
occupancy pattern of its incident domain triangles. Triangles outside D
are absent. For a topological-disc polyiamond the occupied sectors at a
boundary vertex form one cyclic interval. Nonempty disconnected intervals
are forbidden. Empty stars and six occupied sectors are allowed.

Two indicators a_v and b_v are defined exactly: a_v is true for one occupied
sector and b_v is true for five occupied sectors. A contiguous k-sector
boundary link has interior angle 60k degrees. Therefore

\[
\sum_v a_v=n_{60}(P),\qquad \sum_v b_v=n_{300}(P).
\]

The clauses specify both directions of each indicator, including empty and
fully occupied stars. The required strict surplus is the exact Boolean
cardinality constraint

\[
\sum_v b_v+\sum_v(1-a_v)\geq |V(D)|+1.
\]

Finally impose `sum x_t <= 214`. PySAT encodes the cell bound by a totalizer
and the surplus by a cardinality network. Auxiliary variables express these
cardinality conditions with existential extension; no floating arithmetic
or optimization tolerance is involved.

Every tile in the theorem with at most 214 cells would give a satisfying
assignment. Global connectedness, absence of holes, and corona boundary
topology are omitted from the formula. These omissions enlarge its feasible
set and cannot invalidate an UNSAT lower bound.

## Exact computation and checks

The canonical formula has **21,717 variables and 121,097 clauses**. Its SHA256 is

`2c6d12be9f6eb13351dc5f0e12104106c00a77d6da8f6ab63f4e47fb82b0527a`.

Cold Glucose4 through PySAT returns UNSAT with 264 conflicts. The 559,357-byte
DRAT trace has SHA256

`7d20bea6d39089cf012305782f7b9374981024507bf830dbb2d2bcb2949c4b85`.

Independent DRAT-trim reports `s VERIFIED`: 14,656 input clauses and 217 proof
lemmas in the backward core, 250,581 resolution steps, and zero RAT lemmas.
It normalizes duplicate input literals while parsing. The transcript and
trace are regenerated privately by the reproduction command rather than
included as a proof corpus in the repository.

The local angle audit uses a separate geometric definition: selected
triangles must be connected through edges incident to the vertex. It compares
every local occupancy pattern and all four indicator assignments with the
encoder's cyclic-transition clauses. It also compares the resulting original
tile angle counts with its oriented boundary cycle. The sibling independent
checker then replays the complete 215-cell attainment certificate without
importing this encoder or a symbolic marked-tile model.

The audit covers 9,944 local occupancy configurations and 39,776 indicator
assignments at 209 vertices. The full fresh public-source replay, including
DRAT verification and geometric attainment, took 7.079 seconds with 91,040 KiB
peak RSS on one thread within the standing 1 CPU/2 GiB resource scope.

The remaining trust boundaries are the written implication into the CNF,
the integer geometry implementation, PySAT's cardinality encoding, and the
independent DRAT checker. The trace certifies the generated formula's UNSAT;
it does not by itself certify its interpretation as geometry.

## Research implication and prior art

This strengthens the earlier private fixed-corner compression result by
allowing all corner locations and counts to vary. Further compression in
this halo with these placements and this particular angle-surplus mechanism
cannot produce a smaller tile. A smaller finite-five construction must change
at least one of those conditions.

The attainment construction reproduces the known hexapillar-five family,
attributed to Mann's [2004 primary paper](https://faculty.washington.edu/cemann/Heesch.pdf).
No new record or exact Heesch-number-five claim is made. Kaplan's
[unmarked-polyform census](https://arxiv.org/abs/2105.09438) is bounded by tile
size; its reported tables are not an upper bound on all unmarked polyforms.
The prior reproduction's [all-motion angle proof](../heesch_polyiamond_hexapillar/angle_capacity.md)
gives 5<=Hc(T0)<=Hh(T0)<=112. This minimum theorem concerns the construction
and angle-surplus family, rather than the value of its Heesch number.

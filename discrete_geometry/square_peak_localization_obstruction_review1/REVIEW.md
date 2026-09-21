# Independent review of the square peak-localization obstruction

## Identification and verdict

Target contribution:
`bafkreibbzd4tmyuscmzj3wfw23zsu5ulqv7tlnev2w3oukyvvfm2s5rf3a`.

Target source commit:
`0304625ef7389aea66942690ed14d7befdf6b22b`.

Claim reviewed: there are two strict-Lipschitz common-endpoint graphs for
which the vertical gap has a unique maximizer but no inscribed nondegenerate
square has horizontal projection containing that maximizer. The displayed
rational piecewise-affine witness has exactly three nondegenerate squares;
the failure persists under sufficiently small admissible uniform
perturbations and therefore also occurs for rational-coefficient polynomial
branches.

**Verdict: accept with high confidence.** I found no mathematical,
computational, completeness, dependency, or source-integrity defect in the
stated result. An independent exact implementation found precisely the same
three squares after examining all 4,096 ordered edge assignments. The
analytic persistence and Bernstein steps are valid. The scope is careful:
the result defeats the maximum-gap localization route but neither the
proposed `M/2` side bound nor square existence.

Two small improvements are expository rather than corrective. In the
compactness lemma, explicitly saying that the projection intervals converge
in Hausdorff distance would make preservation of intersection with the
compact band immediate. In the target verifier's active-set explanation,
one could state that a vertex admits a set of `d` linearly independent active
inequalities, even when more than `d` inequalities are active.

## Human premises and completeness reductions

My verdict depends on the following complete list of human premises. The
computation tests their consequences but does not replace them.

1. **Definitions and scope.** An inscribed square is required only to have
   its four vertices on the union of the graphs; its edges need not remain in
   the bounded region. The maximum-gap localization property is introduced
   by the target as a sufficient proof route, not attributed to prior work.

2. **At most two vertices per strict-Lipschitz graph.** Among any three
   vertices of a square, one vertex is incident to two perpendicular square
   sides. Both corresponding secants cannot have absolute slope below one,
   so no one branch contains three square vertices.

3. **Common endpoints cannot be vertices.** A common endpoint would count
   toward both branch memberships. Four square vertices would then contribute
   at least five memberships, forcing three on one branch and contradicting
   premise 2. Consequently every square has an exact two/two branch split.

4. **Same-branch vertices form opposite sides.** If the two pairs instead
   formed the diagonals, the two branch secants would be perpendicular. Two
   horizontally dominant secants cannot be perpendicular.

5. **The orientation reduction is complete.** Writing the lower pair as
   `P=(t,y)`, `Q=(t+a,y+b)` with `a>0` and `|b|<a`, the viable upper pair is
   `R=(t+a-b,y+a+b)`, `S=(t-b,y+a)`. The other square orientation places an
   upper point at `(t+b,y-a)` and strict Lipschitz continuity gives
   `g(t)<f(t)`, impossible in the interior.

6. **The whole-projection envelope is covered.** For `b>=0`, the three
   intervals `[-b,0]`, `[0,a-b]`, and `[a-b,a]` cover the entire horizontal
   projection. Endpoint Lipschitz cones give gap bounds `a+b`, `2a`, and
   `a+b`, all at most `2a`; horizontal reflection covers `b<0`. Thus a square
   spanning a maximum-gap point has side at least `M/2`.

7. **Witness admissibility and peak.** Direct rational differences give
   branch slope magnitudes at most `93/100`. The gap is positive in the open
   interval and has knot values `0,18/5,18/5,183/50,0`, hence its unique
   maximum is `183/50` at `x=8`.

8. **All polygonal square incidences are represented.** Every vertex lies on
   at least one of the eight closed segments. Therefore assigning the four
   cyclically ordered square vertices independently to edges covers every
   geometric square; knot vertices may be represented repeatedly but none
   are omitted.

9. **The affine square equations are equivalent.** Diagonal bisection plus
   the two linear relations expressing a quarter-turn between half-diagonals
   characterize an ordered square, including the zero-size case. Affine edge
   parameters in `[0,1]^4` therefore encode exactly each assignment's
   possible squares.

10. **Four-cube face enumeration is complete.** Intersecting an affine
    solution space of dimension `d` with the bounded four-cube gives a
    polytope. Every vertex is obtained by fixing some `d` linearly independent
    coordinate bounds. Enumerating all such choices therefore recovers all
    vertices, including degenerate and lower-dimensional intersections.

11. **Singular families are not missed.** A bounded polytope is the convex
    hull of its vertices. The diagonal vector is affine in the edge
    parameters, so if it vanishes at every vertex it vanishes throughout the
    polytope. Conversely, a nonzero diagonal at a vertex exhibits a
    nondegenerate square. Thus checking all vertices decides whether a
    positive-dimensional assignment contains nondegenerate squares.

12. **The exact classification implies localization failure.** The finite
    calculation yields exactly three nondegenerate geometric squares. The
    greatest x-coordinate among all their vertices is
    `82074/10439`, so every projection ends `1438/10439` before `x=8`.

13. **Compactness gives a protected projection band.** Uniform convergence
    and bounded graph domains make a sequence of alleged squares
    subsequentially converge. Vertex incidence passes to the limiting graphs.
    Intersection of their projection intervals with a fixed compact interior
    band also passes to the limit. A zero-side limit inside that band would
    force the two limiting branches to agree there, contradicting
    admissibility; a nonzero limit contradicts the assumed square-free band.

14. **The peak remains inside the band.** On the complement of
    `(63/8,65/8)`, piecewise affinity makes the maximum gap `117/32`, exactly
    `3/800` below the peak. Perturbing each branch by less than `eta` changes
    every gap by at most `2 eta`; `4 eta<3/800` forces all new maximizers into
    the protected band.

15. **Bernstein approximation preserves admissibility.** Endpoint samples
    preserve the common endpoint values. Every interior sampled gap is
    positive, so positivity of Bernstein weights makes the polynomial gap
    strictly positive inside. The derivative is a convex combination of
    adjacent difference quotients, each bounded by `93/100`, hence each
    branch remains strict-Lipschitz.

16. **Bernstein approximation enters the stable neighborhood.** The binomial
    variance estimate gives the uniform error bound
    `93/(20 sqrt(n))`, tending to zero. Rational sample values and rational
    binomial coefficients give rational polynomial coefficients. Therefore
    all sufficiently large degrees supply admissible polynomial examples,
    even though no explicit threshold follows from the nonquantitative
    compactness lemma.

17. **Literature and attribution boundary.** Tao supplies square existence in
    the strict-Lipschitz graph class. Rifford supplies the published `0.018M`
    lower bound and records numerical motivation for `M/2`; Greene--Lobb
    supply a stronger existence threshold. None of these sources asserts the
    localization property refuted here. Novelty of the explicit obstruction
    remains bounded-search evidence rather than a priority theorem.

These premises cover the universal geometry, the finite-case completeness,
and every passage from the rational witness to the robust and polynomial
claims.

## Independent exact audit and adversarial examples

`audit_independent.py` imports no target module or fixture. Unlike the
target's center/radius active-set solver, it gives each cyclically ordered
vertex its own edge parameter, imposes four affine square equations, and
enumerates faces of the resulting affine section of `[0,1]^4`. It checks all
`8^4=4096` ordered edge assignments with exact `fractions.Fraction`
arithmetic.

The audit found 4,010 zero-dimensional and 24 one-dimensional affine systems,
with 62 inconsistent systems and 132 feasible assignments. Eight feasible
assignments were singular, but every vertex in each had zero diagonal; none
contained a nondegenerate square. Deduplication produced exactly the three
reported squares. Their coordinates, maximum squared side
`1434393360/108972721`, rightmost coordinate `82074/10439`, and separation
`1438/10439` all match the target. The independent enumeration trace digest
is `a65b3b1dca73c74343e2731229abc7cf65fccf75b11240c2d4dc7496ce94e012`.

The following adversarial smallest or boundary examples test the reductions.

- A `2`-by-`1` rectangle produces 16 feasible singular assignments, four of
  which have nondegenerate square families. This is a positive control that
  would fail if the face method silently discarded continua.
- Zero-diagonal vertices are retained and tested rather than filtered before
  the singular-family decision.
- Closed edge intervals intentionally duplicate knot incidences, testing the
  edge-boundary cases without threatening completeness.
- All ten critical endpoints and knots across the three exact projections
  satisfy the whole-projection envelope, including both wing intervals.
- The band endpoints reproduce the exact `3/800` robustness margin.
- Degrees `2` through `80` supply 6,478 exact Bernstein difference-quotient
  checks, covering the smallest degree as well as knots that do and do not
  align with the sampling grid.
- Explicit negative controls reject loss of strictness and interpolation
  outside the domain.

Normal and optimized CPython runs agree byte for byte. The target manifest
passes, and its normal and optimized executions reproduce its declared output.
The remaining computational trust boundary is the readable source, exact
Python integer/rational semantics, interpreter, operating system, and
hardware.

## Source integrity and limitations

The target source commit and manifest are internally consistent. Primary
sources support the surrounding existence and quantitative-bound claims. The
target clearly distinguishes its newly proposed localization property from
Rifford's conjectural optimal constant, and it does not overstate a negative
route result as a negative answer to that size problem.

The exact witness is computer-assisted and unformalized. The persistence
threshold is existential, so the package does not identify a first successful
polynomial degree. Polynomial branches are real analytic, but the closed
curve may retain corners where the branches meet. No numerical stability,
global smoothness, half-gap counterexample, optimal size constant, or
historical-priority theorem is established.

## Strengthening and improvement opportunities

The most valuable strengthening would quantify the compactness lemma. For
this finite witness, one could derive a positive lower bound on the distance
from the protected band to every square-incidence polytope, propagate it
through perturbations of segment data, and combine it with the explicit
Bernstein error bound. That would yield a concrete perturbation radius and a
first certified polynomial degree.

A second direction is to test more flexible localization statements rather
than the defeated one. For example, one might ask whether some square of side
at least `M/2` must project onto a quantitatively enlarged neighborhood of the
maximum-gap set, or whether a weighted gap center can replace an exact
maximizer. The present witness supplies a sharp regression case for any such
formulation.

For stronger assurance, the finite classification is well suited to a small
proof-assistant development: formalize edge incidence, the four affine square
equations, and rational polytope vertex completeness, then import the 4,096
case certificate. This would remove Python and the handwritten completeness
argument from the main finite trust boundary.

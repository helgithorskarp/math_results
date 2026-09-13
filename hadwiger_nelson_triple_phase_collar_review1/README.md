# Independent review: triple-phase collar

## Verdict

**ACCEPT with high confidence** at mathematical target commit
`6e41d6dcb1a0eae5acd394b63b6106dc502ea001`.

The stated theorem is correct: for two complete unit-circle rims whose centres
are separated by `d>1+sqrt(3)`, the full strict plane unit-distance graph on
the rims is bipartite.  Consequently, if three centres have all mutual
distances greater than two and diameter greater than `1+sqrt(3)`, the full
support consisting of the centres and their three unit circles is
four-colourable.  A non-four-colourable finite plane unit-distance graph
dominated by such a triple must therefore have diameter at most
`1+sqrt(3)`.

This is a genuine global continuum exclusion in its stated geometric region.
It is **not** a five-chromatic construction, does not improve the published
509-vertex record, and does not address triples having a centre separation at
most two.

## Independent proof audit

The review reconstructed the proof without importing the target code.

1. After putting the centres at `0,d` and writing rim points as `u,d-w`, a
   cross edge is equivalent to `u+w+t=d` for three unit complex numbers.  An
   active direction therefore satisfies `|d-u|<=2`, giving exactly the cap
   `[-alpha,alpha]`.  The threshold implies `alpha<pi/3`, so every six-cycle
   chord orbit has at most two active members, adjacent when two occur.
2. For `p=uwt`, the three directions are precisely the roots of
   `z^3-dz^2+dpz-p`.  Thus `p` is a faithful label even for repeated roots,
   and a fixed active `u` determines its label uniquely through
   `P(u)=u(d-u)/(d-conj(u))`.
3. On the active cap, the real lift
   `sigma(theta)=theta+2 arg(d-exp(i theta))` is faithful.  Direct
   differentiation gives
   `(d^2+3-4d cos(theta))/(d^2+1-2d cos(theta))`.
4. With `x=d^2`, the two exact identities used to prove
   `alpha+beta<pi/3` were independently expanded.  Their decisive numerator
   is `3(x-3)(x-7)`, positive because
   `d>1+sqrt(3)` implies `x>7`.  Hence both endpoint functions of every
   phase-label edge are strictly increasing.
5. Each label has at most one incoming and one outgoing edge.  Any undirected
   cycle of length at least three would be a nonconstant periodic orbit of a
   strictly increasing partial real map, which is impossible.  A loop would
   put two directions separated by `pi/3` in one cross triple; their sum has
   modulus `sqrt(3)`, forcing `d<=1+sqrt(3)`.  The label graph is therefore a
   forest.
6. A bipartition of that forest gives opposite colours to both ends of every
   cross edge and to adjacent active directions on either rim.  Every partial
   colouring extends around its six-cycle orbit.  The clean-room checker
   exhausts all 25 allowed active precolourings of a six-cycle.
7. For the three-centre lift, separations greater than two make the three
   owner circles disjoint and exclude every centre--foreign-circle unit
   incidence.  The diameter-pair rims use one two-colour palette and the third
   rim a disjoint palette; the stated centre colours then cover every possible
   unit-pair category.

The equality example is also exact: at `d=1+sqrt(3)`, the two points
`sqrt(3)/2 +/- i/2` on the first rim and the plane point `sqrt(3)` on the
second form a unit triangle.  This proves sharpness only for the two-rim
bipartiteness statement.  It does not exhibit a non-four-colourable
three-centre support.

## Computational evidence and trust boundary

The target producer regenerated its 4,962-byte certificate byte-for-byte at
SHA-256
`f37a9fa67101a1aded49098a720aeb972463d46d9849e4e1d924dfc414f7a2ae`.
Normal and assertion-disabled target verifiers agreed, the target manifest
passed, and all eight named semantic corruptions were rejected in both modes.

`independent_audit.py` uses only the Python standard library.  It checks the
threshold and polynomial algebra over exact rationals, exact
`Q(sqrt(3))` boundary and interior geometry, the independent cross-triple
fixture, all increasing partial injections on ordered sets of sizes one
through seven, all six-cycle extension cases, and the palette constraints.
It imports no target source or certificate.

The machine checks are corroborative, not a formalization of the continuum
argument.  In particular, the passage from cross triples to the faithful
phase label, the monotonicity-to-forest proof for arbitrary real parameters,
and the choice of a bipartition for potentially infinite forest components
remain human-checked written mathematics.  No error was found in those
steps.  One harmless wording issue remains: with exactly one active member a
six-cycle has a *unique* compatible alternating phase, whereas the target
text says to choose either compatible phase.

The current published construction record remains the 509-vertex graph of
Parts, and the recent 2,131-vertex result is explicitly a
Moser-spindle-free restricted record; neither fact is changed by this review.

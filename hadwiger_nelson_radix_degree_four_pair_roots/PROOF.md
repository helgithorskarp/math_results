# Exact closure of the degree-four remaining-six pair stratum

Let `omega=(1+i*sqrt(3))/2`, `T={0,1,omega}`, and

    A5(z) = T + zT + z^2 T + z^3 T + z^4 T.

The h4105 architecture represents every possible non-base unit edge by one
of 2,797 irreducible event curves over `Q[x,y]`, where `z=x+iy`.  Each curve
owns an explicit set of label edges.  The h4195 residual records pairs of
event-curve indices that are still necessary for an at-least-six-active
counterexample.  This package treats all 160 residual pairs for which at
least one source curve has degree four.  Their ordered degree histogram is
`(4,4):28`, `(4,6):32`, `(6,4):4`, `(4,8):96`; all have trivial pair
stabilizer.  Their total conservative Bezout allowance is 2,192.

## Theorem

For every complex parameter `z` lying on either source-curve intersection of
one of these 160 pair systems, the strict plane unit-distance graph on the
distinct points of `A5(z)` is three-colourable.  Consequently none of these
systems supports a five-chromatic realization.

This is a statement about every real affine root of the named pairs, not a
root sample, chamber restriction, abstract graph, or numerical feasibility
test.

## 1. Exact decomposition of every physical root

For source equations `f,g in Q[x,y]`, the producer and verifier compute a lexicographic
Groebner basis in the variable order `(y,x)`.  In the ordinary shape-position
case the basis supplies an eliminant `e(x)` and a relation

    a(x)y + b(x) = 0.

The eliminant is factored over `Q`.  For every irreducible factor `q`, the
checker verifies `gcd(a,q)=1`, computes `a^-1 mod q`, and records the exact
component

    q(s)=0,  x=s,  y=-b(s)/a(s) mod q(s).

The exceptional non-shape-position cases in this stratum have a rational
vertical fibre.  The checker substitutes its exact rational `x` coordinate,
takes the polynomial gcd of the two resulting equations in `y`, and factors
that gcd over `Q`.  It then records `x=x0, y=s` for every irreducible factor.
In both cases it substitutes the parametrization back into both source
equations modulo `q`.  Exact Sturm counting (`Poly.count_roots`) determines
the number of real embeddings; factors with no real embedding are retained
in the aggregate complex-only count but need no chromatic decision.

The lex basis covers every affine common zero.  The two explicit fibre cases
cover every basis shape encountered, so the resulting irreducible list covers
every physical parameter represented by the 160 source pairs.  Roots at
projective infinity are irrelevant because `z` is an affine plane parameter.

## 2. Exact event and collision decisions

For a component `Q[s]/(q)`, the checker reduces all 2,797 event polynomials
and both real-coordinate polynomials of all 2,400 normalized label-collision
relations.  Because `q` is irreducible over `Q`, a reduced polynomial of
degree below `deg(q)` vanishes at one conjugate root of `q` exactly when it is
the zero residue.  Thus all real embeddings of a component have the same
active-curve set and the same collision status.  This is an algebraic
identity test, not floating-point point evaluation.

If a collision relation vanishes, the independently accepted h4119/h4141
collision theorem gives a proper additive three-colouring of the strict
unit-distance graph on the coincident point set.  No 243-label colour word is
claimed in this branch.

Otherwise the labels are injective.  The complete strict unit-edge set is the
h4105 base-edge set plus the edge owners of every active event curve.  The
producer asks CaDiCaL for a three-colour word and checks every edge before
writing it.  The verifier does not invoke SAT: it reconstructs the exact
edge set and directly replays the stored word.  The universal equilateral
triangle on labels `0,81,162` supplies the matching lower bound, so every
component has chromatic number exactly three.

The final certificate contains 169 exact irreducible real-component records
and 415 real embeddings in those stored parametrizations.  Seventeen records
(25 embeddings) have an exact collision; 152 records (390 embeddings) are
injective and have explicit colour words.  Twenty-two additional irreducible
factor instances have no real embedding.  The component-record count is a
certificate-key count, not a separate claim that conjugate or differently
parametrized records are globally distinct physical parameters.

## 3. Residual consequence and scope

The theorem deletes 160 systems and allowance 2,192 from the h4195
`remaining_six` table.  Conditional on that upstream residual and its stated
h4117/h4175/h4177 accounting dependencies, the counts become:

| mode | systems | conservative orbit allowance |
|---|---:|---:|
| exact-five compatible | 118,520 | 3,503,032 |
| requires at least six | 10,016 | 308,208 |
| whole residual | 128,536 | 3,811,240 |

These are restricted-family exclusions inside the 243-label complex-radix
architecture.  They do not close A5 globally, produce a plane five-chromatic
graph, or improve the published 509-vertex record.  The D3 rows are solved
over the whole parameter plane; the conclusion transfers to every member of
each symmetry orbit by the physical architecture symmetries.

## 4. Trust boundary

The exact polynomial decomposition, rational arithmetic, factorization, and
Sturm root counts use SymPy 1.14.0.  The architecture inventory imports the
pinned h4105 exact source and python-flint 0.8.0.  Python-SAT 1.8.dev17 with
CaDiCaL 1.5.3 is used only to discover colour words.  The final verifier is
solver-free and replays every word, but it deliberately shares the SymPy
decomposition routines with the producer; an independent implementation or
proof-assistant formalization remains desirable.  The collision implication
imports the accepted h4119/h4141 theorem.  The h4195 residual and its canonical
export were independently accepted in repository commit `12a8a42`; that
review's Discovery Net broadcast is still pending because the ledger is stale.

# Proof and certificate semantics

## 1. Inherited finite cover

Write

```
W={0,1,omega,omega-1,-1,-omega,1-omega},
S(u,v)=W+uW+vW,
phi(z)=(1+i sqrt(3)z)/(1-i sqrt(3)z).
```

The h4065 architecture supplies 988 active irreducible event factors and
thirteen explicit product colour words.  If a noncollision, nonalignment
member fails all words, its real Cayley parameters `(x,y)` lie on one of
71,134 selected coprime factor pairs.  The h4071 physical symmetry group
quotients the symmetric closure to the 800 representative pairs used here.
The h4073 result proves every noninjective member four-colourable, so only
injective common-failure roots can remain relevant to a five-chromatic member.

The certificate pins h4071's source certificate by SHA-256.  Its pair list is
therefore an exact dependency, not a newly generated candidate family.

## 2. Uniform shape representation

For each representative pair `(f,g)`, the producer tries `c=0,1,2`, substitutes
`x=t-cy`, and computes the reduced lexicographic basis over `Q`, with `y>t`.
Every one of the 800 ideals has one of two forms:

```
<1>,
<A(t)y+B(t), P(t)>,  gcd(A,sqf(P))=1.
```

The shear histogram is 670, 116, 14 for `c=0,1,2`; nine systems have basis
`<1>`.  Because `A` is invertible modulo `sqf(P)`, distinct complex solutions
are in bijection with roots of `sqf(P)` through

```
y=-B(t)/A(t),  x=t-cy.
```

This also handles repeated intersection multiplicities: only the squarefree
projection is used for geometric roots.  The sum of its degrees is 4,668.

The standard-library verifier recomputes each basis from the original two
integer polynomials by Buchberger's algorithm.  It does not trust the
producer's Gröbner output or call a CAS.

## 3. Complete real-root coverage

The producer factors every squarefree projection over `Q`, yielding 1,457
pairwise-coprime component polynomials.  Each component stores rational
isolating intervals for every real root; rational roots are singleton
intervals.  The verifier checks the exact product identity and pairwise gcds.
For each component it builds a Sturm sequence, checks that every nonsingleton
interval contains exactly one root, validates every singleton directly,
requires distinct intervals with disjoint interiors and nonroot endpoints
for nonsingletons, and compares the interval count with the variation count
from minus infinity to plus infinity.  In particular, a rational singleton
cannot count twice.  Thus no numerical root or tolerance enters the proof.

There are 1,022 real embeddings.  Component factorization is used to make the
interface compact.  The exclusion proof remains valid even without trusting
the producer's irreducibility declaration: nonvanishing is checked by gcd with
the whole stored component, and vanishing witnesses are polynomial identities
modulo that component.

## 4. Exact thirteen-word filtering

In `Q[t]/(m)` for a component `m`, the verifier evaluates every required event
factor at the rational functions above.  A component has one of four real
outcomes:

1. an inherited alignment factor vanishes identically;
2. one named colour word has no bad factor vanishing at any root of `m`;
3. all thirteen words fail, but a collision equation vanishes identically;
4. all thirteen words fail and the component is injective.

There are 95 alignment components (116 real embeddings), 453 proper-word
components (858 embeddings), no collision component at this stage, and 15
survivor components (48 embeddings).  Another 894 components have no real
root.  The four counts exhaust all 1,457 components and all 1,022 real roots.

For a proper-word outcome, the verifier proves `gcd(m,h)=1` for every bad
factor residue `h` of the named word.  For a survivor it checks an explicit
zero-factor identity for each of the thirteen words and reconstructs the
complete set of event factors that vanish identically.  In every survivor
component that set is exactly its two representative factors.

## 5. Injectivity and the physical bound

The verifier first proves that every one of the sixteen alignment factors is
coprime to each survivor component.  A two-coefficient label collision would
force one of those alignments by h4065's exact wheel-difference lemma.

For three nonzero coefficients, simultaneous sixth-root rotation reduces the
complete collision inventory to 972 canonical displacement triples
`(d,e,f)`.  In the same quotient arithmetic, the verifier evaluates both real
coefficients of

```
d+phi(x)e+phi(y)f.
```

For every survivor component and every triple, the gcd of the component with
both coefficient residues is one.  Hence no real root in any survivor
component is a label collision.  Each survivor therefore has all 343 labels
distinct.  The h4071 orbit cover then implies at most 48 physical graph
classes remain after filtering by the original thirteen words; different
listed embeddings may still be physically equivalent, so 48 is an upper bound
rather than an exact class count.

## 6. Scope and trust boundary

The new exact theorem is the reduction of the original 800-system,
thirteen-word necessary frontier from at most 5,110 physical classes to 15
algebraic components, 48 real embeddings, and at most 48 injective physical
classes.  It uses the accepted h4065/h4071 finite cover and h4073 collision
closure as mathematical premises.

HN-2's h4085 result appeared during the final refresh and independently closes
all 800 systems using 62 colour words, so the current architecture-level
unresolved count is zero.  The 48 embeddings here are a complete structural
census of where the earlier thirteen-word cover alone is insufficient, not a
live chromatic frontier.  The verifier pins h4085's certificate hash but does
not duplicate its separate 277,244-witness colour proof.

SymPy 1.14.0 is used only to discover the shears, factor projections, and emit
intervals.  The proof replay uses `fractions.Fraction`, direct Buchberger and
Euclidean algorithms, Sturm theory, and exact quotient arithmetic.  The
written inheritance of the three-wheel cover and symmetry theorem remains a
human-readable premise.  No chromatic solver, floating predicate, formal
proof assistant, or reviewer-1 verdict is used or claimed.  The 48 physical
embeddings are already four-colourable by the separate h4085 certificate.

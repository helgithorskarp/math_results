# The cubic-anchor residual pencils and their physical root envelope

Let E=Z[omega], omega=(1+i sqrt(3))/2, and T={0,1,omega}. We use the fixed-scale physical point set

    A5(z) = T + z T + z^2 T + z^3 T + z^4 T.

Write z=x+i sqrt(3)y. Thus the real-coordinate norm convention is x^2+3y^2, not x^2+y^2. Every physical graph below merges coincident points and includes every distance-one pair.

## 1. Named scope and theorem

The h4105 architecture has 2,797 primitive norm-event curves. Curve 342 is the radial event |z|=1. Each of the other 2,796 curves comes from a nonmonomial coefficient row in ({0} union E^units)^5, modulo multiplication by a common unit. Reducing the row modulo 2 and normalizing its first nonzero nonconstant entry gives an affine signature (n,c) in F4^4 times F4. Here F4={0,1,2,3}, 2 is the residue of omega, 3=1+2, and 2^2=2+1. The corresponding section is n dot w=c. There are336 realized signatures.

We select every pencil in the literal h4195 residual containing

    S = ((0,0,1,0),1).

Its event bucket is exactly {2795,2796}, namely |1+z^3|=1 and |1-z^3|=1. The selected class comprises the 50 residual indices 192 through 241, recorded entrywise in PENCILS.json. It includes the initially selected asymmetric pencil 230:

    ((0,0,1,0),1), ((1,3,0,0),1), ((1,3,1,0),0),
    ((1,3,2,0),3), ((1,3,3,0),2).

The five bucket sizes of pencil 230 are2,4,4,8,8, giving2,048 lifts. Its six images under z -> omega^2 z and conjugation have indices 230,219,207,218,206,231; its stabilizer is trivial. The calculation below uses no parameter quotient or restricted chamber. The fifty-pencil scope includes the entire fixed-section residual family, not just this orbit.

For each selected pencil, order its five curve buckets by (bucket size, ascending curve-ID list), take the first two buckets, and include every pair with one curve from each. Every resulting pair contains 2795 or 2796. Deduplicate these pairs across the fifty pencils. This defines an explicit584-pair **anchor envelope** B: the set of (x,y) satisfying both equations of at least one such pair.

**Exact computer-assisted theorem.**

1. No choice of one curve from each of the five sections of any selected pencil has a common affine zero over C in the independently complexified variables x,y. This excludes all 1,024,000 raw coefficient lifts, without applying old pair/triple exclusions or assuming that exactly five events are active.
2. The anchor envelope has592 distinct irreducible rational component records, each describing finitely many points. Exactly588 records have real embeddings. They describe3,408 distinct physical parameters z.
3. The complete physical unit-distance graph on A5(z) has chromatic number exactly 3 at every one of those 3,408 parameters. Its size distribution is:

| Physical vertices | Unit edges | Parameters |
|---:|---:|---:|
| 243 | 333 | 2280 |
| 243 | 351 | 1080 |
| 243 | 405 | 36 |
| 147 | 651 | 6 |
| 108 | 432 | 6 |

At all 3,396 injective parameters exactly two event curves are active. The remaining 12 parameters lie on the unit circle, have101 active curves each, and have collisions. Additional active events are therefore explicitly included in the theorem.

B is larger than the set of possible full-pencil concurrences. Its physical graph calculation is a separate, nonvacuous statement: thousands of actual real realizations have been decided even though no selected full pencil survives. It is not the entire locus |1 +/- z^3|=1, not every pair containing either cubic curve, and not a global classification of A5.

## 2. Exact algebraic coverage

The producer regenerates the accepted h4105 norm polynomials and solves all 584 anchor pairs by a lexicographic Groebner basis over Q with y>x. It factors the x-eliminant, solves an invertible linear y-fiber over each irreducible factor field, and treats every exceptional rational vertical fiber using the gcd of the two original equations. It fails if a nonlinear nonrational fiber occurs. None occurs in the selected584 pairs.

The checker uses a different elimination route. For each original pair f,g it forms Res_y(f,g) over Q[x], requires this resultant to be nonzero, and factors it. For every irreducible factor q, it computes the monic gcd of f and g as polynomials in y over Q[x]/(q). A constant gcd means the resultant factor has no affine intersection. A linear gcd gives y as an exact element of that field. Rational x-fibers are factored over Q in y. Whole vertical components or unsupported nonlinear nonrational fibers cause failure, not omission. Leading-coefficient specializations are handled by the actual fiber gcd.

Any common affine zero makes the resultant vanish. The fiber gcd accounts for all solutions above every such x. Factorization and field arithmetic therefore enumerate the full affine intersection. No real-root filter is used for the concurrence decision. Groebner and resultant routes produce identical canonical pair-to-component and coordinate data.

A component consists of an irreducible polynomial q(s) with rational coefficients and exact coordinates x(s),y(s) modulo q. The representation uses x=s, or a rational x and y=s, with a separate canonical form for rational points. Distinct real roots of q give distinct pairs (x,y), since one coordinate is the separating parameter. Distinct component records are disjoint: their irreducible coordinate factors differ, or their reduced other-coordinate polynomials differ modulo the same irreducible factor. Canonical duplicates across source pairs are merged by exact data, not numerical proximity.

For every component, all 2,797 event polynomials are substituted exactly. At each component of each source pair of each selected pencil, at least one section has no vanishing event. This proves part1. The transcript has660 component records counted with pencil/pair incidence; these are not660 distinct parameters. Real roots are counted by exact rational polynomial root counting. This gives part2.

## 3. Physical construction and explicit colours

A coordinate pair (a,b) over Q[s]/(q) denotes a+i sqrt(3)b. Multiplication is

    (a,b)(c,d) = (ac-3bd, ad+bc).

The direct graph checker generates all 243 digit words, forms their exact points in A5(z), merges equal coordinate pairs, and tests the squared norm of every difference against1. Because q is irreducible, a reduced nonzero coordinate or norm polynomial cannot vanish at just one of its real roots. Consequently the computed collision quotient and complete graph are valid at every real embedding of a component. No tolerance, event-edge ownership, solver verdict, or visual embedding is used for this check.

For each real component the producer finds a weight vector (1,w1,w2,w3,w4), all entries in {1,2}, and assigns the digit word (t0,...,t4) the colour

    t0 + w1 t1 + w2 t2 + w3 t3 + w4 t4  (mod 3),

where the digits0,1,2 correspond to0,1,omega. This is the reduction a-b modulo 3 on an Eisenstein coefficient a+b omega. Multiplication by an Eisenstein unit changes that reduction by a nonzero factor. The weights are discovered by trying the 16 possible tails and testing the active coefficient rows. Monomial unit edges are proper automatically since all weights are nonzero. This discovery rule is not trusted for the final graph conclusion.

The checker separately verifies that each claimed colouring assigns the same colour to coincident labels, and that every directly computed physical unit edge is properly coloured. Thus the checked witness gives chi<=3. The three physical points0,1,omega always form a distinct unit triangle, giving chi>=3. This proves part3.

The 12 exceptional parameters are precisely

    |z|=1,  Re(z^3) in {-1/2,1/2}.

Their four rational component descriptions have q(s)=8s^3-6s-1 or 8s^3-6s+1 and x=s, with the two conjugate y-polynomials for each cubic. Each cubic has three real roots. The 147-point components use weights(1,1,1,2,2); the 108-point components use(1,1,1,1,1). The checker verifies the unit-circle equation, all 101 active curves, exact merging, and every edge for each component; they are not removed by an injectivity assumption.

## 4. Dependencies and limits

The named residual membership uses h4195's literal export, canonical SHA256
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`.
The public checker can independently compare all 50 index/signature records against a freshly regenerated export. The default theorem concerns the explicit PENCILS.json class and does not require a bulky historical table. The event inventory is pinned to canonical SHA256
`85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9`.
The h4171/h4179 full-pencil theorem explains the relevance to exact-five A5 covers; it is not needed to turn a complex norm zero into a physical point.

The package imports the existing h4105 architecture and exact algebra/physical-coordinate helpers from the C0 package. SymPy 1.14.0 and python-flint 0.8.0 are explicit arithmetic and elimination trust boundaries. The proof bridges above are written mathematics, not proof-assistant formalization. The producer and checker use different elimination and edge-construction algorithms but share source polynomials and field encodings; this is author validation, not independent-author review.

A probe of 31 other realized pencils containing this signature, outside the selected h4195 class, encountered68 unsupported nonlinear nonrational fibers. That probe establishes no complete result for those 31 pencils. They are not quietly folded into the theorem. The present result also does not update or repair h4117/h4175/h4177 global quotient accounting or conservative allowances.

This is a restricted-family algebraic and physical classification. It supplies no five-chromatic plane realization, no new plane chromatic bound, and no improvement of the 509-vertex record.

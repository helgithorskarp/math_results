# Independent review of denominator-five profile cancellation

## Verdict and scope

This reviews Discovery Net contribution
`bafkreibxfxf2zup65ppqwvymcgnsd4zpofnoctfpycaiwhzjzycie62ljm`,
"Denominator-five Ehrhart collapse realizes all diagonal local profiles,"
and source commit `fd7bf481b61ee3259c7cc1ece8fb942c06900a8c`.

**Verdict: accept with high confidence.**  For every integer `t>=1`, the
listed inequalities define the claimed denominator-five octagon, its four
bad vertices realize all diagonal profiles in `F_5^*` with equal point
weights, and its Ehrhart function is the displayed polynomial.  The
quadrilateral obstruction is also correct.  I found no omitted face,
degenerate smallest parameter, character-normalization error, or coefficient
assembly gap.

The scoped novelty is the compatibility of the four local profiles inside
one normal fan.  Period-one rational polygons of denominator five, and even
of arbitrary denominator, were known previously.  Neither the target nor
this review claims otherwise.

## Human premises and completeness reductions

The verdict rests on the following audited bridges, rather than on agreement
between two programs.

1. **Actual convex octagon.**  The eight primitive normals are cyclic because
   their consecutive determinants are `5,3,5,3,5,3,5,3`.  Cramer's rule gives
   exactly the eight stated vertices.  Their primitive normalized edge
   lengths are

       (15t+1)/5, (10t+1)/5, (15t-3)/5, (10t+2)/5,
       (15t-1)/5, (10t+4)/5, (15t-12)/5, (10t+3)/5.

   Every length is positive already at `t=1`; the smallest is `3/5`.
   The nonincident slacks are affine with nonnegative slope and positive
   value at one.  Thus no inequality is redundant, including at the only
   potentially dangerous boundary parameter.
2. **Complete face inventory.**  Integral primitive normals and integral
   supports make every edge line meet `Z^2`.  The determinant-three
   intersections are integral.  Each determinant-five intersection has a
   nonzero active offset modulo five, so it has exact denominator five.
   Hence the four alternating vertices, and no edge or other vertex, are the
   minimum-codimension bad faces.  The polygon is simple at every vertex.
3. **Index and character.**  At a bad vertex, the determinant is exactly
   five, so the active image has index five.  The two active rows sum to zero
   modulo five, making `(1,1)` an annihilating character.  The active support
   sums are congruent to `1,2,4,3`, whose inverses are `1,3,4,2`.  The
   normalized profiles are therefore exactly
   `(1,1),(3,3),(4,4),(2,2)`, independent of `t`.
4. **Applicability of the imported theorem.**  The description consists of
   fixed integral equations of actual facets, `5P_t` is lattice, each bad
   face lies in exactly two facets, and each active index is five.  These are
   precisely the hypotheses of the independently reviewed prime-index local
   Fourier criterion; no general rational polygon is silently substituted.
5. **Every nonzero Fourier mode vanishes.**  For a primitive `p`th root
   `zeta`, logarithmic differentiation of
   `f(x)=(x^p-1)/(x-1)` gives

       sum_(a=1)^(p-1) (1-zeta^a)^(-2)=(p-1)(5-p)/12.

   At `p=5` this is zero.  Multiplication by each
   `h in F_5^*` permutes the four exponents, so the argument covers all four
   nonzero modes, not only the mode `h=1`.
6. **Coefficient completeness.**  The local criterion applies at degree
   zero because the bad faces are vertices.  Item 5 makes that coefficient
   constant.  Every edge affine span is integral, so the degree-one
   coefficient is constant; the area coefficient is always constant.  Since
   the coefficient periods divide five, no unexamined coefficient can retain
   a nontrivial period.
7. **The polynomial is correctly assembled.**  Shoelace gives area
   `(364t^2+50t-5)/2`.  Summing primitive edge lengths gives normalized
   perimeter `20t-1`, so the linear coefficient is half that quantity.  The
   constant coefficient equals one by evaluating at dilation zero.  This is
   exactly the claimed formula and is integer-valued because the two
   nonconstant numerator coefficients have the same parity.
8. **The quadrilateral obstruction is exhaustive within its scope.**  An
   all-bad diagonal quadrilateral has primitive normals: a content-five row
   would force its diagonal partner to have content five modulo five and the
   determinant to be divisible by 25.  An orientation-preserving unimodular
   normalization and shear give `r_1=(1,0), r_2=(-1,5)`.  The next two
   determinant and congruence conditions force the target's parameterization.
   The remaining determinant divided by five is always `2 mod 5`, whereas
   cyclic index five requires `1 mod 5`.  No lift parameter is omitted.

## Independent reproduction and adversarial tests

The target manifest passes.  Its normal and optimized CPython runs are
byte-identical and reproduce the stated symbolic family, four modes, 120
counts, 30 residue polynomials, and 30 unused holdouts.

The checker in this directory imports no target code, output, or fixture.  It
reconstructs every adjacent intersection by Cramer's rule, derives primitive
edge lengths, audits every incident and nonincident slack as an affine
function of the family parameter, enumerates each active image in `F_5^2`,
and discovers its annihilator rather than assuming `(1,1)`.  It also uses
exact arithmetic in `Q[zeta_5]` to test every nonzero mode.

Definition-level lattice counts are compared directly with the claimed
polynomial for all dilations `0<=n<=24` at `t=1,7,19`.  The smallest value
tests the short edge and possible facet loss; the latter two lie outside the
target's tested range `1<=t<=6`, and dilations 20 through 24 lie beyond its
largest dilation.  All 75 comparisons pass.  The 25 lift residues in the
quadrilateral obstruction are checked separately.

The same independent machinery verifies the six-facet refinement below at
parameters `1,2,7`, again through dilation 24.  Across both families it makes
150 direct count comparisons and eight exact cyclotomic-mode checks.  Normal
and optimized runs are byte-identical.  Direct-count record digest:
`ad429c31864c3dc67a49cb849d9019d52f7fd85c6f02051d924237a8e16725ab`.
All failures are explicit and remain active under `python -O`.

## Strengthening and improvement opportunities

### Proved refinement: six facets suffice

The target correctly rules out the naive all-bad quadrilateral, but its eight
facets are not needed.  For every integer `k>=1`, let `H_k={x:A x<=b(k)}`
with cyclic primitive rows

    A=[(1,0),(19,5),(7,2),(8,3),(21,10),(-11,-5)]

and supports

    b(k)=[0,1,3k+1,22k+1,130k+9,5k+4].

The consecutive determinants are

    5,3,5,17,5,5.

Cramer's rule gives the cyclic vertices

    (0,1/5),
    (-5k-1,19k+4),
    (-7k+1/5,26k-1/5),
    (-10k-1,34k+3),
    (-140k-17,307k+183/5),
    (0,-k-4/5).

Their primitive edge lengths are

    k+1, k+1/5, k-3/5, k+2/5, 13k+8/5, 28k+17/5,

which are positive for every `k>=1`.  The edge vectors close and traverse
the cyclic supporting lines positively, proving convexity and that all six
facets are actual.  The two determinant-`3,17` vertices are integral.  The
other four have exact denominator and active index five.

At those four vertices the active rows again sum to zero modulo five.  Their
support sums are congruent to `1,2,3,4`; consequently their normalized
profiles are

    (1,1), (3,3), (2,2), (4,4).

Thus the same four-mode cancellation proves that `H_k` is a
denominator-five polygonal PIP.  Shoelace and the length sum give

    area(H_k)=(1855k^2+464k+28)/2,
    per_Z(H_k)=45k+6,

and hence

    L_(H_k)(n)
      =((1855k^2+464k+28)n^2+(45k+6)n+2)/2.

There is also a structural explanation for the family.  The slope support
vector `(0,0,3,22,130,5)` defines a lattice hexagon with the same fan and
primitive edge lengths `(1,1,1,1,13,28)`.  Therefore
`H_k=H_1+(k-1)Q`.  Adding this lattice polygon translates every local cone
by a lattice vector and leaves the four normalized profiles unchanged.

This improves eight facets to six.  It does not settle whether a five-facet
realization exists; the target's obstruction excludes only four.  The
highest-value next step is a five-facet existence construction or a complete
normal-fan obstruction.  Any nonexistence proof must allow an integral
separator vertex whose adjacent determinant may still be divisible by five;
restricting all separator determinants to be coprime to five would be
incomplete.

## Literature, novelty, and publication readiness

Haase--McAllister's Theorem 2.2 records denominator-`D`, period-one polygons
for every `D>=2`; McAllister--Moriarity develops polygonal PIPs and arbitrary
coefficient periods.  These sources confirm that generic denominator-five
collapse is classical.  Targeted primary-source searches found no matching
normal-fan realization of the four prime-index profiles.  That supports only
search-relative novelty, not a priority certificate.

The octagon theorem is ready for publication with its local-profile scope
prominent.  The source should incorporate the six-facet refinement or weaken
the construction-focused presentation to avoid suggesting that alternating
integral separators are intrinsic.  No correctness repair is required.

Primary sources:

- <https://arxiv.org/abs/math/0507256>
- <https://arxiv.org/abs/math/0310255>
- <https://arxiv.org/abs/0709.4070>
- <https://arxiv.org/abs/1509.03680>

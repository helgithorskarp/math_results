# Four-active-curve classification

## 1. Additive F4 colour words

Let `T={0,1,omega}`, `omega^2=omega-1`, and

    A5(z)=T+zT+z^2T+z^3T+z^4T.

Reduce `Z[omega]` modulo two into `F4=F2[t]/(t^2+t+1)`, with `omega -> t`.
For a tail `w=(w1,w2,w3,w4) in F4^4`, colour the digit label
`a=(a0,...,a4)` by

    C_w(a)=a0+w1*a1+w2*a2+w3*a3+w4*a4 in F4.

The first coefficient is fixed to one, so all universal first-digit triangles
are proper.  A noncircle event curve has a unique displacement word up to a
sixth-root multiple.  Its colour failure set is one affine hyperplane

    H(n,c)={w in F4^4 : n dot w=c},

where `n` is the nonzero tail residue and `c` is the constant residue.  Scaling
`(n,c)` by a nonzero F4 scalar does not change the hyperplane.  Thus there are

    (4^4-1)/3 = 85

projective normals and 340 affine hyperplane types.

If the radial circle is active, its four monomial edge classes require every
tail weight to be nonzero.  Hence its proper-word domain is the 81-point torus

    D=(F4*)^4.

Any non-four-colourable graph must make every one of these additive colour
words fail.  This gives a necessary covering condition; sufficiency is not
asserted.

## 2. Four curves without the circle

Every affine hyperplane in `F4^4` has 64 points.  If four hyperplanes cover all
256 points, equality of cardinalities forces them to be pairwise disjoint.
Two affine hyperplanes are disjoint exactly when their normals are proportional
and their constants differ after common normalization.  Therefore four
hyperplanes cover if and only if they are

    H(n,0), H(n,1), H(n,t), H(n,1+t)

for one projective normal `n`.

The four support-one homogeneous types `H(e_j,0)` arise from the four monomial
events merged into the circle, not from noncircle curves.  Consequently only
the 81 projective normals of support at least two give realizable four-
noncircle signature patterns.

## 3. The circle plus three curves

For a projective normal of support `s`, the size of `H(n,c)` inside `D` is

    3^(4-s) (3^s+3(-1)^s)/4,  if c=0,
    3^(4-s) (3^s-(-1)^s)/4,   if c is nonzero.

For `s=1,2,3,4`, these values are respectively

| support | `c=0` | `c!=0` |
|---:|---:|---:|
| 1 | 0 | 27 |
| 2 | 27 | 18 |
| 3 | 18 | 21 |
| 4 | 21 | 20 |

Three restricted hyperplanes can cover the 81-point torus only when all have
size 27 and are pairwise disjoint.  There are exactly two structural forms:

1. for one coordinate `j`, the three slices `w_j=1,t,1+t`;
2. for one unordered coordinate pair `{j,k}`, the three relations
   `w_k=r*w_j`, `r in F4*`.

Indeed, coordinate slices are disjoint only for the same coordinate and
different values; two homogeneous two-support relations are disjoint only for
the same coordinate pair and different ratios; every mixed or differently
supported pair intersects.  Thus there are four coordinate patterns and six
ratio patterns, for ten circle-containing signatures in total.

## 4. Lifting signatures to event curves

Every nonzero F4 coefficient has two sixth-root lifts differing by sign.  For a
signature whose normal has support `s`, the number of exact unit-multiple curve
classes is `2^(s-1)` when `c=0` and `2^s` when `c!=0`.  The resulting 336
realized noncircle types have curve-count histogram

    30 types with 2 curves,
    90 types with 4 curves,
    135 types with 8 curves,
    81 types with 16 curves.

They account for all 2,796 noncircle active curves.  Multiplying bucket sizes
inside each admissible signature pattern gives

    960,768 no-circle quartets,
         80 circle-containing quartets,
    960,848 eligible quartets in total.

These are residue-covering curve sets only.  No concurrency, injectivity, or
chromatic conclusion is inferred from membership in this list.

## 5. Reduction of the D3 pair frontier

HN3 h4117 forms the complete D3 closure of HN2's 264,800 necessary pair
systems and obtains 132,130 pair orbits.  A pair is compatible with an exactly-
four-active obstruction precisely when its noncircle signatures are distinct
and lie together in one of the 81 no-circle patterns or one of the ten torus
patterns, with the circle treated as above.

Exact classification gives:

| pair-orbit class | orbits | D3-closed systems | Bezout sum |
|---|---:|---:|---:|
| compatible, no circle | 2,528 | 14,256 | 155,648 |
| compatible, with circle | 26 | 64 | 528 |
| incompatible with exact four | 129,576 | 771,060 | 7,629,248 |

The property is constant on every D3 pair orbit.  Therefore every injective
non-four-colourable parameter with exactly four active curves lies on one of
only 2,554 canonical pair systems.  Projective Bezout on those coprime systems
gives the conservative bound 156,176 on such parameter orbits.  If a possible
counterexample lies on one of the other 129,576 pair orbits, its active set has
at least five curves.

This does not remove the incompatible systems from the full search: parameters
with five or more active curves remain possible.  It is an exact split into a
small exactly-four branch and a higher-incidence branch.

## 6. Exact verification and trust boundary

The producer reconstructs HN2's complete event and pair inventories and maps
the canonical displacement coefficients into F4.  It derives the physical D3
action from coefficient words and classifies every pair orbit.

The verifier follows a separate route.  It constructs all 256 colour words on
all 243 digit labels, obtains each event's failure mask directly from its edge
list, and checks that all 2,796 noncircle masks are among the 340 theoretical
hyperplanes.  It recovers the 85 affine partitions solely from pairwise
disjointness and exhausts the 30 size-27 torus sections to find the ten torus
partitions.  It reconstructs D3 by exact rational substitution into all 2,797
integer event polynomials, then independently partitions and classifies all
132,130 pair orbits.  Entry-level hashes agree with the producer.

The computation uses CPython arbitrary-precision integers and rational numbers
only.  There is no floating-point predicate, CAS, or solver.  Completeness of
the active-curve inventory, pair cover, and curve coprimality remains a pinned
dependency on HN2 h4105, independently accepted at h4123.  The D3 quotient is
the h4117 dependency.  HN2 h4119 closes the noninjective branch, but its paired-
residue proof is not otherwise needed here.  None of these results supplies a
non-four-colourable parameter.

# Proof and certificate boundary

## Source and coordinates

The points are complex plane coordinates in a common positive scale
`q=1/|1-zeta|`, where `zeta=exp(2*pi*i/5)`. The stored integer tuple
`(a0,a1,a2,a3)` means `q*(a0+a1*zeta+a2*zeta^2+a3*zeta^3)`.
Since the fifth cyclotomic polynomial is irreducible over Q, equality is exact
coefficient equality. No tolerance clustering or missing realization step is
involved. Multiplication by the nonzero common factor q is injective.

Parts's source is the sixteen subset sums `b+sum(e_j*d_j)` from the README.
The source order, specified as the four bits `e_0,e_1,e_2,e_3`, is

```
0000 1000 0001 1001 0100 0010 1010 0101
1100 0011 1101 1011 0110 1110 0111 1111.
```

Reconstruction gives exactly the source's 28 unit pairs and 28 phi pairs;
`verify.py` compares both complete labelled edge lists with the archived
source. Source labels 1,2,3,5,6 form K5 in their union. The proper five-word
`1 3 2 0 4 0 1 1 2 4 3 2 3 4 0 1` proves that this two-distance graph has
chromatic number five. These long-distance inequalities are not automatically
unit edges in a conversion.

The proposed multiplier is
`lambda=(1-zeta^4)/(zeta-zeta^4)=-zeta-zeta^3`. Its squared absolute value is
`(3-sqrt(5))/2=1/phi^2`. The whole root copy maps source labels 1 and 5 to
base labels 1 and 2 respectively. The remaining copies are fixed translations
by `lambda*sum(k_j*d_j)`, not separately selected placements.

## Physical cap, anchors and necessity

The unscaled `d_j` have coefficient matrix `I+J`, where J is the 4-by-4
all-ones matrix, and determinant five. They and their lambda multiples are
Q-linearly independent. Distinct integer addresses therefore cannot collide.
Taking the union of the 162 translated four-dimensional address cubes covers
exactly the 448 grid addresses, with no omissions or duplicate physical
addresses. A point is still in the ordinary two-dimensional Euclidean plane;
the four coordinates are rational coefficients of algebraic numbers, not
four spatial dimensions.

The root copy already supplies two old points. Thus the final physical order
is at most 462 before expansion. The exact source/grid intersection has size
two, so the final count is exactly 462.

In lexicographic copy order, every nonroot index k has a predecessor obtained
by reducing its first positive coordinate by one. The two copies share eight
physical points. At least two shared points are not in the fixed base, so all
161 nonroot copies have generated anchors. Exactly 160 copies miss B, one
meets B once, and the root meets it twice.

The terminal point `(3,3,3,6)` belongs only to the last whole copy `(2,2,2,5)`
and not to B. Its unique occurrence establishes geometric necessity of that
copy for the frozen network. The last copy also has zero base coincidences.
No chromatic necessity or forcing property of an individual copy is assumed.

## Scope relative to the registered overlay

The existing theorem covers the union X of B and every scale-phi or
scale-1/phi copy meeting B in two distinct points. Those two incidences
completely determine the similarity after choosing orientation and endpoint
order. Source pairs and target pairs must have squared norm ratio phi^2 or
phi^-2. Conversely every matching pair produces the corresponding copy.

The independent checker repeats only this exact geometric membership gate,
using quadratic-pair arithmetic. It recovers 5,568 pair specifications and
328 distinct copies at each scale, and the 1,386-point union X. Exactly 406
of the frozen network's 462 points lie outside X, including its unique
terminal corner. Thus this support is not contained in the closed fixed-base
overlay. No new candidate networks are selected by that membership calculation.

## Complete graph and ordinary four-word

For stored complex coordinates z,w, physical distance one is equivalent to

```
(z-w)*conjugate(z-w) = |1-zeta|^2 = 3+zeta^2+zeta^3.
```

The producer uses integral polynomial multiplication modulo Phi_5. The
independent checker instead represents each unscaled point as

```
(A+B*sqrt(5)) + i*sqrt(10+2*sqrt(5))*(C+D*sqrt(5)).
```

Here the four coefficients have denominators dividing eight. For the cleared
difference `(a,b,c,d)=(8A,8B,8C,8D)`, the squared norm numerator is

```
a^2+5*b^2+10*c^2+50*d^2+20*c*d
  + sqrt(5)*(2*a*b+2*c^2+10*d^2+20*c*d).
```

It is unit precisely when its rational/sqrt(5) coefficient pair is
`(160,-32)`. The checker reconstructs every one of `binom(462,2)=106491`
pairs, obtaining the identical lexicographically ordered 1,532-edge CSV.
Both internal and incidental cross-copy pairs are included.

The stored 462-symbol word has different symbols on every edge. This is a
complete positive certificate of ordinary four-colourability, independent of
SAT-solver correctness. Its source restriction is `0213102001131001`, making
these twelve golden-distance constraints monochromatic (one-based labels):

```
(1,6) (2,7) (3,5) (3,10) (4,12) (5,13)
(8,9) (8,15) (9,14) (10,13) (11,16) (14,15).
```

Thus the required source obstruction fails on the final physical graph.
That first four-word ends this architecture. The exact chromatic number is
not claimed; no smaller-colour decision or adjacent network was attempted.

## Verification and trust

The producer's exact-one SAT encoding and its byte-identical replay both use
the same complete physical graph. The standard-library checker separately
reconstructs geometry using a different field representation and checks the
positive word directly. Normal and optimized Python runs agree. Ten malformed
witnesses are rejected, including an omitted physical edge, changed coordinate,
incorrect generated anchors, and a concealed failure of the source relation.

Trust rests on the stated algebraic identities, elementary independence of
the cyclotomic basis, exact Python integer/Fraction semantics, the finite
loops, the positive certificate and the execution environment. There is no
floating-point root, SAT-negative proof, omitted graph input, or abstract-to-
plane assumption. This is author-side checking, not an independent review.

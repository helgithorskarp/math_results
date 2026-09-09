# Four-colourability of the complete three-wheel architecture

Use W and S(u,v) as defined in README.md. All graphs are strict physical
unit-distance graphs in the Euclidean plane. The proof has three inputs:

1. h4065 gives the exact unit-distance factorization and a finite necessary
   intersection cover for non-four-colourable injective members.
2. h4071 gives 800 representative factor pairs covering those members up to
   physical symmetry, outside pair alignment.
3. h4073 proves every noninjective member four-colourable, including alignment.

We prove every injective physical member represented by any of the 800 systems
four-colourable. This contradicts the necessary cover for any hypothetical
non-four-colourable member and completes the architecture. We need neither
isolated real roots nor irreducibility verdicts from computer algebra.

## 1. Geometric input and relevant factors

Write

```text
phi(x)=(1+i sqrt(3)x)/(1-i sqrt(3)x),  x real.
u=phi(x), v=phi(y).
```

The omitted unit-circle endpoint -1 is pair-aligned and therefore already
covered by h4073. For two wheel-product labels let their displacement be
`d+u e+v f`, with `d,e,f in W-W`. The source integer polynomial is

```text
F=(1+3x^2)(1+3y^2)(|d+phi(x)e+phi(y)f|^2-1).
```

For real x,y, distance one is exactly F=0. `inputs.py` regenerates the complete
source polynomial inventory by the h4065 integer coordinate-numerator
identity and checks all factor multiplication identities. It also checks
the 1,764 Cartesian unit edges directly from the wheel product.

There are 990 supplied factors, including the two positive denominators.
The sixteen finite alignment factors describe

```text
x,y in {0,+/-1/3,+/-1};
(y-x)-a(1+3xy)=0, a in {0,+/-1/3,+/-1};
1+3xy=0.
```

They are reconstructed explicitly. None of these eighteen factors vanishes
at an injective real parameter: each alignment identifies two wheels up to
sixth roots and gives at most 133 physical points. Therefore only the other
972 factors need be considered for this proof.

For a stored colour word w on the 343 labels, the checker first verifies all
Cartesian edges. Let B(w) contain every relevant factor of every nonzero F
whose two labels have the same w-colour. If every factor in B(w) is nonzero
at a parameter point, w is a proper colouring there. With injective labels
it is already a physical colouring; no fibre-consistency assumption is hidden.

## 2. A complete characteristic-zero projection cover

Fix one supplied pair of coprime factors f,g in Q[x,y]. Each has y-degree
at most two. If both are univariate in x, their ordinary gcd is checked to
be one, so the system has no solutions. Otherwise form

```text
E(x)=Res_y(f,g)
```

as the determinant of the Sylvester matrix over Z[x]. The verifier expands
this determinant directly, with matrix order at most four. It checks E is
nonzero and verifies a complete factorization

```text
primitive(E)=product r_i(x)^m_i
```

using exact integer multiplication. The r_i are primitive nonconstant
integer polynomials. Their irreducibility is neither assumed nor needed.

Every common finite root (x0,y0) gives E(x0)=0, including when leading
coefficients lose degree at x0. To see this without a genericity assumption,
evaluation at y0 is a nonzero linear functional on the Sylvester coefficient
space, annihilating every shifted f and g row after specializing x0. The
matrix is singular. Thus x0 lies on at least one supplied r_i. Extraneous
projection roots are harmless and are retained until checked empty.

## 3. Exact relations in the projection quotient

For each r let `K=Q[x]/(r)`. Work with coefficient polynomials reduced modulo
the monic normalization of r. The verifier applies the Euclidean algorithm
in K[y] to f and g. Every leading-coefficient inversion is checked by an
explicit extended Euclidean identity modulo r. If a needed coefficient is
not invertible, verification fails; no field property is silently inferred.

Each remainder is a K[y]-linear combination of its predecessors. The final
monic polynomial H therefore belongs to `(f,g)` modulo r. Every physical
root with r(x0)=f(x0,y0)=g(x0,y0)=0 must satisfy H(x0,y0)=0. This is the only
direction needed for coverage. H=1 proves that projection fibre empty.
The impossible vertical-component case f=g=0 in K[y] is rejected explicitly.

For nonconstant H, the quotient

```text
L=Q[x,y]/(r,H)
```

has the finite free monomial basis `x^i*y^j`, with `i<deg r` and
`j<deg_y H`, since both relations are monic in their leading variables.
Here deg_y H is one or two, and the largest basis has six elements. Repeated
roots and nilpotents cause no difficulty. Every original common root lies
in this quotient cover, although converse inclusion is unnecessary.

The 800 systems yield 1,447 projection branches with resultant multiplicities
removed. Their quotient dimensions sum to 4,679 (a conservative count with
overlaps and multiplicities, not an enumeration of distinct real points).
After sharing identical obligations and including the split children below,
there are 835 distinct quotient obligations.

## 4. Unit witnesses exclude monochromatic edges

If a relevant factor h is a unit of L, it cannot vanish at any represented
root. We certify units by reduction modulo a prime p. The checker verifies
p is prime and divides none of the denominators of the monic relations r,H.
The same monomial basis then defines the reduction over Fp, without loss of
dimension. Multiplication by h has a rational matrix reducing to its Fp
matrix. If the reduced determinant is nonzero, the rational determinant is
nonzero, so h is a unit over Q. This implication needs no lifting of a
particular modular point and makes no claim that finite-field roots are
Euclidean points.

The producer tests this by multiplication matrices. The final verifier uses
an independent norm formula. In `Kp=Fp[x]/r`:

- If `H=y+t`, evaluate h at `y=-t` by Horner's rule.
- If `H=y^2+u*y+v`, reduce `h=A*y^2+B*y+C` to `B'*y+C'`, where
  `B'=B-A*u` and `C'=C-A*v`. Its norm is
  `N=C'^2-u*B'*C'+v*B'^2`.

The second identity is the determinant of multiplication on the basis
`1,y`, and remains valid over the possibly nonreduced ring Kp. The element
is a unit exactly when N is a unit in Kp, checked by `gcd(r,N)=1` over Fp.
Both methods give exactly the same unit-witness stream on this certificate.

For each colour action, every factor in B(w) receives such a witness. There
are 277,244 checks: 277,234 use p=1009 and 10 use p=1013. A failed reduction
is simply inconclusive and may be tried at the next declared prime; it never
proves a unit or a physical edge. All Cartesian edges and every potential
monochromatic non-Cartesian unit edge are thereby covered. Hence the chosen
word properly colours every injective real realization in that quotient.

## 5. Empty, nonreal and split obligations

Four distinct quotient obligations have H=1. In 47 others, r is quadratic
with negative discriminant, so no real first parameter exists. In ten others,
H is an x-independent monic quadratic with negative discriminant, so no real
second parameter exists. The checker verifies these exact inequalities.

One quotient envelope combines two different physical cases and requires an
explicit split. Its relations are

```text
r=3x^2-9x+4,
H=y^2+x*y-3x+5/3.
```

Modulo r the identity is

```text
H=(y-x+1)(y+2x-1).
```

The checker multiplies the two monic factors modulo r and checks equality
to H, then verifies a colour cover for each child. This covers all roots,
including repeated or shared ones. The discovery-stage direct physical
reconstruction of these two branches gave 301-point collision graphs; that
observation is not needed for the final algebraic cover or its completeness.

The action census is 773 colour obligations, 4 empty, 47 no-real-x,
10 no-real-y, and one split. Its two coloured children are already included
in the 773, not additional unresolved cases. There is no residual action.

## 6. Conclusion, independence and scope

Every injective member in every one of the 800 representative systems is
four-colourable. The h4071 symmetry cover and h4065 necessary factor-pair
cover rule out every non-four-colourable injective member of S(u,v).
h4073 handles every noninjective member. Therefore **all** physical members
of this complete architecture are four-colourable. Since h4073 supplies
four-chromatic members, the maximum chromatic number in the family is four.

The CAS producer's resultant factorizations are checked by integer polynomial
identities. Its Groebner relations are reconstructed by a different rational
Euclidean algorithm. Its multiplication-matrix unit witnesses are checked by
the explicit norm algorithm. The two implementations share elementary
univariate arithmetic, which remains in the trust base. SAT supplies only
positive words: clauses require a nonempty colour set for each label and
disjoint colour sets at adjacent labels; choosing one true colour gives a
proper word. All decoded words are checked. The three failed SAT discovery
queries supply no negative theorem and no UNSAT proof trace is assumed.

Controls cover specialization degree loss, negative constant resultants,
noninvertible coefficients, vertical components, bad primes and denominators,
nilpotents, a missing projection factor, changed coefficients, and invalid
colour words. Normal and optimized Python agree. This is an author-checked
computer-assisted proof with explicit prior-result and arithmetic trust
boundaries, not a formalization or reviewer-1 verdict. No five-chromatic
physical graph is produced and the 509-vertex record is not improved.

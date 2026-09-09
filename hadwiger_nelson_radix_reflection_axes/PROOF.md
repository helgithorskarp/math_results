# Physical axis theorem and its global counting consequence

## 1. Exact event model

Let E=Z[ω], where ω²=ω−1. A label a in {0,1,2}⁵ represents
`p_a(z)=sum d(a_j) z^j`, with d(0)=0, d(1)=1 and d(2)=ω.
Identify equal points and join all pairs at Euclidean distance exactly one.
The graph always contains the triangle {0,1,ω}; thus its chromatic number
is at least three, even at colliding parameters.

The accepted h4105 event model, also independently reconstructed in the h4151
review, groups all 29,403 label pairs into 243 universal edges and 29,160
remaining pairs. Nonconstant monomials become unit only on the unit circle;
all other groups have one of the 2,796 nonmonomial norm equations. With the
unit-circle equation this gives 2,797 curve IDs. The verifier reconstructs
every actual pair and its group; it imports the reviewer's inventory routines,
not the factor-block producer's geometry implementation.

For a real parameter t and a difference row
`P(t)=a(t)+ω b(t)`, the norm equation is

`a(t)²+a(t)b(t)+b(t)²−1=0`.

Its leading coefficient is one because the leading nonzero row coefficient
is an Eisenstein unit. Direct norm expansion and specialization of the
independent real/imaginary bivariate model agree exactly. The distinct
specialized monic norm polynomials number 1,433.

## 2. A complete real-axis graph classification

The certificate expresses each of the 1,433 polynomials as an exact product
of powers of 1,198 distinct monic integer blocks, of degree one through eight.
The checker multiplies every product over Z. It checks every pair of blocks
is coprime modulo the prime 1,000,003, and each block is squarefree modulo
one of the listed primes. All moduli are checked prime by integer trial
division. Monicity and Gauss's lemma imply pairwise coprimality over Q;
therefore distinct blocks have no common complex root. No irreducibility of
the whole block list is assumed or required.

If a real t is a root of one block, the exact active-curve set is precisely
the list of norm polynomials containing that block. This is constant across
all its real roots. The 192 blocks of degree at most four are monic over E,
so accepted h4119 already makes the entire physical graph three-colourable.
Likewise any noninjective parameter is closed by h4119; those cases need no
new collision computation here.

For each of the 1,006 remaining blocks, the certificate supplies one of four
colour words w:

```
(1,0,0,0,0), (1,0,0,0,1), (1,0,0,1,0), (1,0,0,1,1).
```

Colour label a by `sum w_j a_j mod 3`. The checker examines every universal
edge and every edge in every active group, and proves its two colours differ.
For an injective realization this is directly a proper physical colouring.
Noninjective realizations were already handled above. A real parameter on no
event curve has only the universal triangles and is three-coloured by the
first word, unless noninjective, which is again covered by h4119. These cases
exhaust the real line, not merely a sampled interval.

The independent exact Sturm calculation finds 805 higher blocks with real
roots and 1,074 distinct real roots in total. Their block-incidence histogram
is 975 blocks with two active curves, 29 with four and two with six. Root
counts and squarefreeness refine the census; colouring validity does not rely
on numerical root approximations.

## 3. Exact physical higher-incidence fixtures

The only higher-degree blocks with real roots and at least five active curves
are

```
p+(t)=t^7+t^6+t^3−1,  curves [617,737,738,1401,1423,1424],
p−(t)=t^7−t^6+t^3+1,  curves [618,739,740,1402,1425,1426].
```

Each has exactly one real root; p−(t)=−p+(−t). Let r be the unique real root
of p+, isolated by 4/5<r<81/100. The standalone physical fixture uses z=±r
and stores every coordinate as `a(r)+ω b(r)`, with integer coefficient
arrays in ascending degree. The degree-seven polynomial is irreducible
modulo five: the checker proves `X^(5^7)=X mod p+` and
`gcd(X^5−X,p+)=1`. Since seven is prime, this is the finite-field
irreducibility criterion and proves irreducibility over Q.

The producer tests norms using FLINT and a²+ab+b². The independent checker
instead computes four times each squared distance as `(2a+b)²+3b²`, reducing
over Q modulo p+. Irreducibility makes zero remainder equivalent to zero at
r. It checks all 58,806 point pairs across the two fixtures, proving 243
distinct points, all and only 261 unit edges, a proper three-colouring and
the unit triangle [0,81,162] in each graph. Both chromatic numbers are exactly
three. The first h4105 colour word already colours both; these fixtures add
no positive non-four-colourability signal.

## 4. All reflection axes

Put R(z)=ω²z and C(z)=conjugate(z). For j=0,...,4, the triangles
ω^(2j)T are translates of T by, respectively,

`0, −1, −ω, 0, −1`.

Thus `A5(Rz)=A5(z)−z−ωz²−z⁴`; the checker verifies all digit permutations
and the resulting 243-label bijection. Also
`A5(Cz)=ω conjugate(A5(z))`, since ω conjugate(T)=T. These are physical
isometries. R and C generate D3. Its reflections fix exactly the real line
and its two R-images: y=0, y=x and y=−x. The real-axis theorem therefore
proves every member on every reflection axis exactly three-chromatic.

## 5. Quantified effect on the complete frontier

Let N be the set of parameters for which A5(z) is not four-colourable. The
physical symmetry makes N invariant under D3. Nonidentity rotations fix only
z=0, a closed collision parameter. Reflections fix only the axes just closed.
Consequently D3 acts freely on N.

Consume the h4117 global pair cover after h4139 and h4167: 131,356 distinct
canonical pair representatives q={f,g}, with total degree-product allowance
7,754,528. Its completeness and the pairwise-finite Bézout setting are
imported, not re-proved here. Let H_q be the subgroup stabilizing the
unordered pair q. It acts freely on

`N_q={z in N : f(z)=g(z)=0}`.

The h4165 reviewer report published during this pass explicitly supplies a
sharper intersection count. In the invertible complex coordinates
`u=x+i√3 y`, `v=x−i√3 y`, an order-k row event is
`P(u)P*(v)−1=0`, where P* conjugates the Eisenstein coefficients. Its
bidegree on P1×P1 is (k,k). For orders k,l, the intersection number is
`k*l+k*l=2kl`, instead of the total-degree bound 4kl. Imported h4105 absolute
irreducibility and distinctness rule out a shared component. Boundary
intersections can only decrease the number of affine points. The checker
verifies every row's order and total degree before using this formula.

Thus |N_q| <= 2kl=B_q. Therefore the number of H_q-orbits
is at most floor(B_q/|H_q|). The union of these sets of orbits over the
canonical pairs maps onto N/D3: the complete pair cover supplies a pair for
each parameter, which can be moved to its canonical pair. Multiple systems
may cover the same parameter orbit, making the sum an upper bound.

The exact accounting is:

| Pair stabilizer size | Systems | Sum 2kl | Sum floor(2kl/size) |
|---:|---:|---:|---:|
| 1 | 129,052 | 3,816,192 | 3,816,192 |
| 2 | 2,300 | 60,944 | 30,472 |
| 3 | 4 | 128 | 40 |
| Total | 131,356 | 3,877,264 | **3,846,704** |

The imported bidegree bound first reduces 7,754,528 to 3,877,264. Dividing
only by rotational stabilizers then gives 3,877,176, a saving of 88 from the
already closed rotational fixed point. The new reflection-axis theorem
contributes **30,472**, leaving 3,846,704. Under the old total-degree bound
alone the same computation gives 7,693,412, with 172 saved by rotations and
60,944 by reflections; both accountings are retained in the output. The large
halving is credited to the imported intersection argument, not to the new
axis theorem. We do not divide all
systems by six and do not combine canonical pairs with a fundamental-chamber
restriction. All systems remain. This is an upper bound on possible
non-four-colourable parameter orbits, not a census of all roots or a closure
of the five-or-more-active frontier.

For every curve the counting program verifies the D3 action twice: using
Eisenstein coefficient operations, and using independent exact integer
substitution in its bivariate norm polynomial. It checks all group relations,
all representative minimality conditions and the orbit-stabilizer identity.

HN3 h4171 and the reviewer-1 h4165 report were consumed before publication.
The former's exact-five pencil interface
leaves the same 131,356 global systems; 2,740 need at least six active curves.
The free-action theorem applies uniformly to both modes. No h4171 quintet
concurrence or new parameter locus is tested in this pass.

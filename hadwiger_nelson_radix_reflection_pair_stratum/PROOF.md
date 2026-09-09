# Exact physical and chromatic classification

Let omega=(1+i sqrt(3))/2, T={0,1,omega}, and
A5(z)=T+zT+z^2T+z^3T+z^4T. Vertices are distinct physical points and every
pair at distance one is an edge. The triangle 0,1,omega is present for every
parameter, so every member has chromatic number at least three.

## 1. The named residual stratum

Start from the pinned h4185 interface of 130,932 global pair representatives.
Select precisely those whose stabilizer mask contains one of C,RC,R^2C in the
named action order 1,R,R^2,C,RC,R^2C. This gives 2,232 rows: 1,760 with the
predecessor exact-five flag and 472 already requiring at least six curves.
All have stabilizer order two, and the reflection fixes each curve separately.
The four order-three rotation-only rows are excluded from the selection and
retained in the live frontier. The initial intake count 2,236 included them;
the explicit correction is preserved in DECLARED_GATE.json.

The two curve actions are checked both on Eisenstein displacement rows and
by exact substitution in their bivariate polynomials. Each selected pair has
a unique rotation making both curves invariant under ordinary conjugation.
The five digit triangles satisfy

```
A5(omega^2*z) = A5(z)-z-omega*z^2-z^4,
A5(conjugate(z)) = omega*conjugate(A5(z)).
```

The checker verifies the underlying digit-set translations and conjugation
identity. Thus every normalization preserves the physical graph up to
isometry. Expanding the 2,232 canonical pairs gives 6,696 distinct pair
exclusions. These are constraints on curve pairs, not on the parameter being
fixed by a reflection; off-axis physical parameters remain fully covered.

After normalization, each displacement polynomial has, up to an Eisenstein
unit, coefficients in {0,+1,-1}. This is checked coefficient by coefficient.
There are 112 such norm curves among the selected pairs.

## 2. Complete exact algebraic coverage

Put tau=z+conjugate(z), rho=z*conjugate(z). For a real-coefficient
polynomial P, its norm condition is the polynomial equation

```
N_P(tau,rho)=P(z)*P(conjugate(z))-1=0.
```

The traces C_j=z^j+conjugate(z)^j satisfy C_0=2, C_1=tau and
C_j=tau*C_(j-1)-rho*C_(j-2). For P=sum a_j*z^j this gives

```
N_P = -1 + sum_i a_i^2*rho^i
      + sum_(i>j) a_i*a_j*rho^j*C_(i-j).
```

All equations have total degree at most four in tau,rho. Use u=tau+rho,
so tau=u-rho. For each source pair, regard its two equations as polynomials
in rho with coefficients in Z[u], after harmless nonzero scalar clearing.
The determinant of their Sylvester matrix is a nonzero univariate eliminant.
The verifier computes it by fraction-free Bareiss elimination, checking every
exact division. A physical common zero necessarily projects to a zero of
this eliminant, including when specialized leading coefficients drop.

Every eliminant is factored and its full integer factor product is checked.
For each factor q(u), reduce the original equations in the quotient algebra
Q[u]/(q), then perform univariate Euclidean division in rho. Every inverted
leading coefficient is verified to have a multiplicative inverse modulo q.
This makes each division valid at every characteristic-zero root of q.
**Irreducibility of q is not assumed:** the computations only divide by
explicitly checked units of the quotient algebra.

There are 118 resultant factors whose fibre gcd is the unit polynomial.
They are empty fibres, not roots; specialized leading-degree loss can create
such extraneous eliminant factors. The remaining fibre gcd degrees, counted
within source pairs, are:

| degree in rho | 1 | 2 | 3 |
|---|---:|---:|---:|
| fibres | 3,778 | 66 | 10 |

A monic linear fibre gcd gives rho=R(u) and tau=u-R(u), with R a rational
polynomial modulo q. Every nonlinear fibre has a linear q, hence a rational
value u=c. Its ordinary rational polynomial in rho is factored with its full
product checked; each factor then uses rho as a new parameter, with
rho=u and tau=c-u. Multiplicities do not affect coverage.

This produces 3,903 pair/chart incidence slots and 2,291 distinct stored
chart descriptions `(q,T,R)`, meaning q(u)=0, tau=T(u), rho=R(u).
Descriptions can overlap geometrically. These counts are **not** a real-root
census, a count of candidate graphs, or a claim of pairwise-disjoint physical
images. Complete coverage is all that the colouring proof requires.

An independent producer constructs the same charts using lexicographic
Groebner bases over Q, then refines by each eliminant factor. The verifier
instead reconstructs its source equations from reviewer bivariate curves
by x=tau/2, y^2=(4rho-tau^2)/12 and uses the determinant/Euclidean method.
The complete chart set agrees entrywise for every source pair, not merely in
aggregate. The compact certificate binds the sorted charts, normalizations,
and complete per-pair cover by exact hashes.

## 3. Exact unit-edge exclusions and three-colour words

Write z=x+i sqrt(3)y. The reviewed displacement inventory assigns each of the
29,403 pairs of digit labels to one of 243 universal edges or one of 2,797
unit-event curves. For physical parameters, a positive-order monomial
|z^j|=1 is equivalent to rho=1 because rho>=0; this is the radial event.
No other unit edge is omitted.

On a chart, substitute x=T(u)/2 and y^2=D(u)=(4R(u)-T(u)^2)/12 into a
bivariate event curve f(x,y). Separating even and odd powers of y gives,
after nonzero rational scalar clearing,

```
f = E(u)+y*O(u),
H_f(u) = 12*E(u)^2 - (4R(u)-T(u)^2)*O(u)^2.
```

A physical unit edge owned by this curve necessarily has H_f(u)=0. Both
signs of y and possibly extra nonphysical algebraic points are retained by
this projection. A colouring of the resulting upper graph is sufficient.

For each of the 2,291 charts, the certificate gives a word
w=(1,w1,w2,w3,w4) over F3. Colour digit label a in {0,1,2}^5 by
sum(w_j*a_j) modulo 3, with 0,1,omega encoded as 0,1,2. The verifier derives
all colour-bad curve groups from the actual label pairs and these colours;
it does not reuse the producer's coefficient-residue test.

For every colour-bad group the verifier checks that H_f is a **unit** in
F_p[u]/(q), with p=1,000,003, using polynomial gcd equal to one. The prime,
the nonvanishing leading coefficient of q, and all rational denominators of
T,R modulo p are checked. The following characteristic-zero implication is
what gives these modular calculations their proof force.

Let B be Z with all denominators used here and the leading coefficient of q
inverted. They are all nonzero modulo p. The monic version of q makes
B[u]/(q) a finite free B-module. Multiplication by H_f has a square matrix
in the standard power basis. Its reduction modulo p is invertible by the
checked gcd, hence its determinant is nonzero over Q. Therefore H_f is a
unit in Q[u]/(q). It cannot vanish at any characteristic-zero root of q.
This argument requires neither irreducibility nor squarefreeness of q, and
it does not infer an inequality from a finite-field computation.

Consequently no colour-bad actual unit edge can occur at any physical point
of any chart. All universal edges are also checked. Every chart has a valid
word, so every normalized physical label graph is three-colourable.
If digit labels collide, choose one label for each distinct physical point;
the resulting physical graph is a subgraph of the checked label graph and
inherits the colouring. Rotation and conjugation return the conclusion to
all original pair systems and their 6,696 images. The permanent triangle
proves chromatic number exactly three.

No predecessor colouring theorem is imported to dispose of exceptional
charts. Closed anchor, radial, reflection-axis or collision points can occur
inside full fibres; they are covered by the same checked words, without
reopening those loci as searches.

## 4. A complete quartic physical fixture

One chart from the normalized image of global pair (27,1257), with active
source curves 257 and 2133, has

```
q(u)=3u^4-3u^3+22u^2-5u-8,
T(u)=(-103+193u-36u^2+3u^3)/225,
R(u)=(103+32u+36u^2-3u^3)/225.
```

The quartic is irreducible modulo 7, verified by the degree-four Frobenius
criterion, and hence irreducible over Q. It has exactly two real roots,
one in each of

```
(-155/322,-142/295),       (116/157,133/180).
```

Exact Sturm counts isolate them. For each root, R>0 and
D=(4R-T^2)/12>0. Define y to be the positive square root of D and
z=T/2+(2omega-1)*y. The negative-y members are physically conjugate.
Thus both real embeddings and both physical sign choices are decided.

At both roots, exact interval signs verify R!=1, R!=T^2, D!=0 and

```
(R^2-T^2)*(R^2+R*T+T^2-3R)*(R^2-R*T+T^2-3R) != 0.
```

These exclude respectively the radial circle, all reflection axes and all
six first-step anchors. Since q is primitive, irreducible and nonmonic, u
is not an algebraic integer. If z were integral, then its complex conjugate
and u=z+conjugate(z)+z*conjugate(z) would be integral, a contradiction.
In particular no unit-leading digit collision relation can hold, and this
fixture does not reuse the low-degree monic-parameter closure.

The 243 coordinates are stored as
`A(u)+B(u)*y+omega*(C(u)+D_1(u)*y)`, with all four coefficient polynomials
of degree at most three. A common denominator is supplied per vertex.
The generator uses the Eisenstein basis; the independent checker converts
to Cartesian coordinates and regenerates every point by exact complex
multiplication with real/imaginary norm X^2+3Y^2.

Equality tests use Q[u]/(q) and y^2=D without assuming the latter quadratic
extension is irreducible. An expression a+b*y is zero precisely when either
both coefficients are zero, or a^2=D*b^2 and a*b<0 at the chosen real root.
The sign is certified by rational interval arithmetic with exact bisection
inside its isolating interval. Nonzero remainders in the quartic field cannot
vanish at an embedding, by irreducibility.

All 58,806 point-pair decisions across the two embeddings are checked,
reusing 2,801 displacement classes only after exact unit normalization.
Both graphs have 243 distinct vertices and 378 unit edges. Their active
curve sets are respectively

```
170,257,1873,2133,2792
86,257,1928,2133,2791.
```

The word (1,0,1,1,2) colours every actual edge, and each graph contains the
unit triangle. Both are exactly three-chromatic. These are complete physical
five-active decisions, not positive non-four-colourability evidence.

## 5. Scope of the result

The theorem closes precisely the declared reflection-pair stratum. It does
not close all A5 parameters, classify the four rotation-only systems, or
propagate the new pair exclusions through every remaining five-pencil.
The global numerical subtraction is an exact transformation of the pinned
h4185 interface and retains its stated upstream completeness/bound trust
boundary. See HANDOFF.md. No <=508 record is established.

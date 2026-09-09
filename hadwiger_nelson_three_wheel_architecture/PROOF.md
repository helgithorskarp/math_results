# A finite exact frontier for three independently rotated unit wheels

Let omega=(1+i sqrt(3))/2 and

```
W={0,1,omega,omega-1,-1,-omega,1-omega}.
S(u,v)={a+u b+v c : a,b,c in W},   |u|=|v|=1.
```

All points are actual Euclidean points. Coincident labels are identified and
every unit edge is included. Every graph has at most 7^3=343 physical vertices.

**Theorem.** There is an explicitly specified finite set E of at most
**904,317 ordered parameter pairs (u,v)** such that the strict unit graph of
S(u,v) is four-colourable outside E. Every non-four-colourable member has real
Cayley parameters generating a number field of degree at most **16** over Q;
its real plane coordinates lie in a field of degree at most **32**.

This is a necessary finite frontier, not a count of actual non-four-colourable
members. The exceptional graphs have not been chromatically decided. Exact
physical examples with chromatic numbers three and four are checked below.

## 1. Coordinates and the complete unit-event polynomial family

Write lattice vectors as a+b omega with a,b integers, and use

```
phi(t)=(1+i sqrt(3)t)/(1-i sqrt(3)t)
      =(1-3t^2+2i sqrt(3)t)/(1+3t^2),    t real.
```

This is a bijection from the real line to the unit circle minus {-1}.
The missing lines u=-1 and v=-1 are four-colourable by Section 5, so it
suffices to use u=phi(x), v=phi(y).

The full difference set D=W-W has 19 vectors, with nonzero squared norms
1,3,4. For each triple (d,e,f) in D^3, put

```
F_d,e,f(x,y)=(1+3x^2)(1+3y^2)(|d+phi(x)e+phi(y)f|^2-1).
```

This is an integer polynomial of bidegree at most (2,2). The denominators
are positive at every real parameter. For a pair of labels its physical
distance is one exactly when its F polynomial vanishes.

Multiplying all three differences by a common sixth root of unity preserves
F. Exact enumeration gives 1,144 displacement orbits including the zero
triple, and 1,064 distinct primitive-normalized polynomials including the
zero polynomial. The identically zero cases give exactly the 1,764 edges
of the Cartesian product of the three strict wheel graphs.

The factor certificate decomposes every nonzero normalized F, including
multiplicities. Two factors, 1+3x^2 and 1+3y^2, have no real zeros and are
discarded. The remaining **988** factors have total-degree histogram

| Degree | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| Factors | 19 | 109 | 218 | 642 |

They are pairwise coprime over Q and over C. Irreducibility is not assumed.
`algebra.py` verifies all 487,578 pairs by the independent modular argument
in Section 7. Exact multiplication verifies the full factorization of every
F. Thus the proof trusts no computer-algebra factorization verdict.

## 2. Thirteen explicit colour words

The wheel graph has a unique three-colouring up to palette permutation:
its centre has one colour, and the outer six-cycle alternates the other two.
Fix c3(a+b omega)=a-b mod 3. For product labels use the four words

```
C_s,t(a,b,c)=c3(a)+s c3(b)+t c3(c) mod 3,   s,t in {1,-1}.
```

The h4047 layer-permutation argument shows that these are all product
three-colourings up to a global palette permutation. More explicitly,
restrict a product colouring to its first wheel layers. Adjacent layers
must have the same affine slope, because two different slopes over F3
would agree somewhere. Connectivity makes this slope global; the offsets
form a three-colouring of the product of the other two wheels. Apply
h4047's two-pattern theorem to those offsets. Global palette normalization
leaves precisely the four displayed sign choices.

Also use the ring homomorphism c4:Z[omega]->F4=F2[z]/(z^2+z+1), sending
omega to z. The nine four-colour words are

```
D_alpha,beta(a,b,c)=c4(a)+alpha c4(b)+beta c4(c),
alpha,beta in F4 minus {0}.
```

Every unit vector of the wheel maps to a nonzero element of F4, so these
words are proper on the Cartesian product. The code represents 0,1,z,1+z
by 0,1,2,3, uses XOR for addition, and reduces multiplication by z^2+z+1.

For an active factor h, let G_h be the graph on the 343 labels containing
the Cartesian edges and every additional pair whose F polynomial has h
as a factor. Exhaustive checking of all label pairs proves that at least
one of the thirteen words colours every G_h. In detail, 934 have an F3
word and the remaining 54 have an F4 word. By h4047, those 54 formal graphs
are exactly four-chromatic. We need no assertion that every such factor
has a real point with exactly that graph.

This check covers all isolated single-factor strata with injective labels,
but the stronger common-failure argument next also covers many intersections.

## 3. Common failure gives a finite exceptional set

For a word w define B_w as the active factors appearing in the F polynomial
of at least one pair with equal w-colours. There are no equal-colour
Cartesian edges. Therefore, at any injective physical parameter pair,

```
w is improper  iff  P_w(x,y)=0,
P_w = product of the distinct factors in B_w.
```

In particular, every non-four-colourable graph with injective labels lies
in the common zero set of all thirteen P_w. The factor-graph coverage in
Section 2 says that no active factor belongs to all B_w.

The following entirely explicit cover quantifies that zero set. Order the
F3 words by (s,t)=(1,1),(1,-1),(-1,1),(-1,-1), followed by F4 words in
lexicographic order on alpha,beta=1,2,3. Choose the primary word
**D_2,3**, index 9. It has 270 bad factors with total degree 959.
For every h in B_primary choose a protecting word w(h) that colours G_h,
minimizing the total degree of its bad factors, breaking ties by word index.
This is a specified choice rule, not a claim of optimality.

If all thirteen words fail, some h in B_primary vanishes, and then some
g in B_w(h) vanishes. We have g!=h. The resulting **71,134 distinct unordered
factor pairs** are reproduced by `verify.covering`; their index-set hash is
in EXPECTED.json. Their degree products sum to **902,481**.

Since every selected pair is coprime, the affine consequence of Bezout's
theorem bounds its complex intersection points by deg(h)deg(g). The common
failure set therefore has at most 902,481 distinct real points. Points
counted more than once and nonreal intersections only make this upper bound
conservative. A proof of the classical intersection bound is given in
[Hilmar and Smyth, Theorem 1](https://arxiv.org/html/0907.0361v1).

Equivalently, the common-failure set is specified by the thirteen product
equations P_w=0. The selected pair cover is a smaller-degree way to bound
and enumerate a superset; no high-degree product needs to be expanded.

## 4. Isolated physical collisions

A collision with all three differences nonzero satisfies

```
d+u e+v f=0,    d,e,f in D minus {0}.
```

Taking the norm of d+u e gives

```
2 Re(conjugate(d)e u)=|f|^2-|d|^2-|e|^2.
```

For nonzero d,e this is a genuine line intersecting the unit circle in at
most two points u. Each determines v=-(d+u e)/f uniquely. The discriminant
is 4|d|^2|e|^2-(|f|^2-|d|^2-|e|^2)^2.
The common-sixth-root quotient has 972 rows: 108 give one root and 864 give
two. Thus all these collisions occur at at most **1,836 ordered rotation
pairs before deduplication**. This includes degenerate and already covered
cases, so it is a safe upper bound without a hidden general-position premise.
One-coordinate changes never collide.

Add these collision points to the common-failure set from Section 3 to
obtain E. The bound is 902,481+1,836=904,317.

## 5. Whole collision lines and chart boundaries

In each of the three nonzero norm classes, D is exactly one sixth-root
orbit. A collision with precisely two nonzero differences consequently
forces u, v or u/v to be a sixth root of unity. Call these pair-alignment
lines. Since W is invariant under these rotations and H19=W+W,
every graph on such a line is congruent to a subset of H19+q H19 for some
unit q. For example u in the sixth roots gives H19+vW, while u/v in the
sixth roots gives W+uH19.

The accepted h4005 theorem, independently accepted at h4031, makes every
such physical graph four-colourable, including all its coincidences and
extra unit edges. The containment is independently checked from W+W and
the exact defining 19-point hexagon. We use this completed theorem as an
input and do not reopen its finite rotation classification.

In particular u=-1 and v=-1, omitted by the Cayley chart, are wholly
covered. Sections 3--5 therefore address every real rotation pair.

## 6. Algebraic degree and exact physical controls

Each selected factor pair has degree product at most 16. A common point
has at most that many algebraic conjugate points, all of which are also
common zeros. Hence [Q(x,y):Q]<=16. For a triple collision, the circle
equation of Section 4 becomes a rational polynomial of degree at most two
in x. The recovered v lies in Q(x,i sqrt(3)); its real Cayley parameter y
belongs to Q(x). Thus collision pairs have degree at most two instead.
The real coordinates of S(phi(x),phi(y)) belong to Q(x,y,sqrt(3)), giving
the asserted bound 32. These are necessary degree bounds, not witnesses
of a non-four-colourable graph.

The exact physical controls check all 58,653 distances in each of:

- x=1000, y=10^9: 343 distinct points, 1,764 unit edges, exactly three
  colours, witnessed by C_1,1 and a unit triangle.
- u=(5+i sqrt(11))/6, v=(1+i sqrt(2))/sqrt(3): 343 distinct points,
  1,848 unit edges, exactly four colours, witnessed by D_2,1 and a Moser
  spindle. Its seven label triples are (2,2,0),(0,2,0),(1,2,0),(6,2,0),
  (2,0,0),(2,1,0),(2,6,0), using the ordered W in `verify.py`.

The second control reconstructs all eleven spindle edges and rejects all
2,187 assignments of three colours. Coordinates use exact integers in
Q(sqrt(2),sqrt(3),sqrt(11)), with denominator 12 for this four-colour control.
No floating-point predicate or chromatic solver is used by the verifier.

## 7. Independent algebra check and remaining trust

The producer derives F through dot and cross products and uses SymPy for
factor discovery. The standard-library verifier instead forms the real
and imaginary numerators R,I of d+phi(x)e+phi(y)f, scaled by 2D_x D_y.
It checks the polynomial identity

```
4 D_x D_y F = R^2+3 I^2-4 D_x^2 D_y^2
```

by exact integer long division and multiplication. It then multiplies every
certified factorization back. It assumes neither factor irreducibility nor
CAS soundness.

For coprimality, a prime reduction is allowed only if it preserves each
polynomial's total degree. A nonconstant common Q-factor would then reduce
to a nonconstant common factor modulo that prime, by Gauss' lemma and
degree additivity. The checker rules out common factors over F_p[x,y] in
two parts. First it checks coprimality of the contents with respect to y,
excluding common vertical factors. Then it finds an x specialization
preserving both y-degrees at which the univariate polynomials in y have
gcd one. A common positive-y-degree factor would survive that specialization,
a contradiction. A degree-zero-in-y input needs only the content check.

All 487,578 actual pairs receive such certificates already modulo **101**.
The implementation also permits 103 and 107, and a control deliberately
requires changing the prime. Another control rejects a common factor;
others cover vertical factors and bad specializations. The finite-field
Euclidean algorithm, primality checks and all polynomial identities use
exact integers. Thus coprimality does not depend on SymPy's factorization.

Remaining trust lies in Python arithmetic and decoding, the elementary
written geometric and colouring reductions, the named accepted h4005/h4031
input, h4047's layer argument, and the classical Bezout bound. This is not a
proof-assistant formalization or reviewer-1 acceptance. The finite set E
has not been isolated into distinct real points, its graphs have not been
solved, and the 509-vertex record has not been improved here.

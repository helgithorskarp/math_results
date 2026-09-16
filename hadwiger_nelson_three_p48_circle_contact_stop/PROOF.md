# Exact fixed-support decision

Let a=i sqrt(3), b=i sqrt(11), c=i sqrt(35). The square classes of
-3,-11,-35 are independent over Q: no nonempty product is a rational square.
Consequently the eight monomials a^e b^f c^g, with e,f,g in {0,1}, are a
basis of K=Q(a,b,c). The specified positive real square roots fix its complex
embedding. Coordinates are stored in that monomial order (index e+2f+4g),
with common denominator 336. This is an exact injective representation.

## Geometry and cap

The P48 norm is a0^2+a0*b0+b0^2 for integer lattice addresses (a0,b0).
Completing the square bounds |a0| and |b0| by 8; enumeration in this square
therefore gives exactly 169 points and reconstructs all 456 internal edges.

Use the README's r,A,B,D,v. Direct multiplication gives

```
|r|^2=1,   |A|^2=7,   |r-1|^2=1/3,   |D|^2=7/3,
|1+i sqrt(35)/7|^2=12/7,
|v|^2=|v-D|^2=1.
```

Thus all three maps are plane isometries, and C=A+v is a common unit neighbour
of A and B. The support has raw order 507.

Write L=Z[omega], F=Q(omega), E=Q(a,b). Since r is outside F, L and rL
intersect only at 0. Since v is outside E, an equality A+v*z=x with z in F
and x in E forces z=0. Thus L intersects A+vL only at A, while rL cannot
intersect it: A is not in rF. In particular the three full lattices have no
common point. Each stated overlap belongs to the finite P48 patches, so
there are exactly 505 collision-merged points.

Moreover S is not centrally symmetric. Its centroid is 168*A/505, which is
not a support point (its scaled coordinates are not integers). An odd finite
centrally symmetric set contains its centre, which equals its centroid.
Every common-centred union of P48 copies is centrally symmetric. Thus S is
not an isometric image of an h3889 support, independently of the displayed
decomposition.

The independent checker constructs the same coordinates in Cartesian form
using squarefree positive radicals. The identity
sqrt(u)*sqrt(w)=gcd(u,w)*sqrt(u*w/gcd(u,w)^2) gives exact multiplication.
It tests all 127,260 point pairs, declares an edge exactly when the squared
distance equals one, and obtains 1,375 edges. All 1,368 internal edges are
distinct. The seven remaining edges are listed in EXPECTED.json. Their
patch-pair counts are 6,0,1. The common points 0 and A and the edge BC join
all three patches in a cycle. Connectivity after each single-vertex deletion
is checked directly, so the graph has no articulation vertex.

Point ordering is lexicographic on the eight scaled imaginary-generator
coefficients. Coordinate hashes use comma-separated integer rows with a final
newline. Edge hashes use sorted zero-based endpoint pairs i,j, also one
comma-separated pair per line with a final newline. The denominator is 336.

## Ordinary chromatic decision

The literal four-word in certificate.json assigns different colours to both
ends of every reconstructed edge. This proves chi(S)<=4 independently of SAT.
The seven points

```
0, 1, omega, 1+omega, r, r*omega, r*(1+omega)
```

are distinct and induce the eleven edges of a Moser spindle. Exhausting all
3^7=2187 assignments finds no proper three-colouring. Thus chi(S)=4.
The additional five-word merely recolours one vertex with a new colour and
is checked independently against all edges; it is not a lower bound.

The producer's ordinary k-colour CNF has variables X(i,j), exactly one colour
j per vertex i, and clauses not-X(i,j) or not-X(l,j) for every physical edge
{i,l}. The sole symmetry clause X(0,0) is sound by global colour permutation.
The one four-colour query returned a satisfying word, decoded and checked
against the graph. No UNSAT verdict, omitted proof trace or restricted
colouring relation is used.

## Existing field coverage: why the selected frame is already excluded

The nontrivial E-automorphism of K changes c to -c. It takes v to
v'=D*(1-c/7)/2. Hence

```
v+v'=D,
v*v'=3*D^2/7 = D/conjugate(D),
(v/D)^2-(v/D)+3/7=0.
```

In the accepted embedding of E into the unramified quadratic extension of
Q_2 commuting with complex conjugation, the norm valuation is twice the
valuation. Since D*conjugate(D)=7/3 is odd, D has valuation zero. The relative
trace of v is therefore a local unit. The existing unit-trace field theorem
(committed h2655; source a71c857eaac06b0f340248893a74e4e25f5f8f33) gives a
four-colouring of the whole field E(v)=K. Its normalized polynomial reduces
to X^2+X+1 over F2, consistent with its two simple roots over F4.

This is an application of that earlier theorem, not a new field theorem.
It explains the selector failure even though the three lattices have no
common point. The finite certificate above does not import its 2-adic proof.
No claim is made about arbitrary translated triples or other outside-field
placements, and the frozen architecture is retired without a nearby sweep.

# Exact Snail dihedral-nine classification

Let S be the 29-point set defined by `seed.json` and the formulas below. For
each ordered pair of distinct seed labels(c,a), reflect in the line s_c s_a
and rotate by 40 degrees about s_c. The full dihedral orbit closure is

G(c,a) = {s_c+r^k(s_i-s_c), s_c+r^k u conjugate(s_i-s_c):
          0<=i<29, 0<=k<9},

where r=exp(2*pi*i/9), d=s_a-s_c and u=d/conjugate(d).
Edges are all pairs of distinct points at distance exactly one. There are812
labelled cases; no quotient by isomorphism or congruence is taken.

**Computer-assisted theorem.** Of these 812 cases,157 have chromatic number
three and 655 have chromatic number four. Their orders range from 271 to496,
and their edge counts range from 738 to1494. The original505-vertex intake
bound is valid but loose. In particular, this complete target-sized family
cannot improve the 509-vertex record. Every subgraph of every listed closure
is also four-colourable.

## Source and coordinate field

Write w=(1+i*sqrt(3))/2 and v=(5+i*sqrt(11))/6. Each of the 27 rows(A,B,C,D)
in `seed.json` denotes A+B*w+C*v+D*w*v. Append the two points, placed first
in our label order:

    p = 3+(17/8)w-(7/8)v+2wv
        +sqrt(5)(-1/4+(1/8)w-(1/8)v+(1/4)wv),
    q = 11/4+(13/8)w-(1/8)v+2wv+(eta/8)(-w+v+wv),
    eta = i*sqrt((415+79*sqrt(33))/8).

These are the Snail coordinates of Dúcz and Varga,
[arXiv:2606.28157v1](https://arxiv.org/html/2606.28157v1), section4 and its
[supplement](https://users.renyi.hu/~akos/ep1070/). All29 source expressions
were reconstructed symbolically from the supplement and checked against the
published integer numerators. The graph has 51 exact unit edges. Labels 0 and 1
(p and q) have the single neighbour4 (the paper's v3). Our checker also proves
that the seed's ordinary chromatic number is three. The paper's stronger
geometric fractional quantity is a different invariant and is not a
chromatic premise here.

Set a0=i*sqrt(3), b=i*sqrt(11), c0=sqrt(5), e=8*eta. The field

    K = Q(a0,b,c0,e)

has basis a0^i b^j c0^k e^l, with each exponent 0 or1. Its relations are

    a0^2=-3, b^2=-11, c0^2=5, e^2=-3320+632*a0*b.

Here is a degree proof, needed to justify canonical coefficient equality and
the residue evaluation. The square classes -3,-11,5 are independent over Q:
each nonempty product has an odd valuation at at least one of 3,11,5. Thus
K0=Q(a0,b,c0) has degree 8 and is an abelian multiquadratic extension. Its
complex conjugation commutes with every Q-automorphism. If e belonged to K0,
then conjugation(e)=-e would force every conjugate of e to be purely imaginary,
so every conjugate of e^2 would be nonpositive. But the automorphism reversing
sqrt(33) sends e^2=-3320-632*sqrt(33) to -3320+632*sqrt(33)>0. The strict
inequality follows by squaring positive quantities:632^2*33>3320^2.
This contradiction proves e is quadratic over K0 and [K:Q]=16.

The physical conjugation negates a0,b,e and fixes c0. In the producer basis
w=(1+a0)/2, the relations instead read w^2=w-1 and
e^2=-3320-632*b+1264*w*b. Both are exact representations of the same field.

## Cubic rotation separation

The following elementary reduction supplies all missing cross-copy edges;
their absence is proved algebraically, not inferred from numerical sampling.

Let K be a conjugation-stable subfield of C, let |r|=1, put rho=r^3 in K,
and suppose [K(r):K]=3. For nonzero x,y in K and t=1 or2,

    |x-r^t*y|^2-1
      = x*conjugate(x)+y*conjugate(y)-1
        -r^t*conjugate(x)*y-r^(-t)*x*conjugate(y).

Because r^-1=r^2/rho and r^-2=r/rho, the r and r^2 coefficients are
nonzero. Linear independence of 1,r,r^2 over K makes this expression nonzero.
The nonzero sets K,rK,r^2K are also disjoint: an intersection would put r or
r^2 in K, contrary to the extension degree. Therefore, for any finite
T subset K containing 0, the graph on T union rT union r^2T is the union of
three isomorphic graphs meeting only at 0, with no other cross-copy edges.
Its chromatic number is exactly that of the graph on T; its order is 3|T|-2
and its number of edges is three times the number on T.

For the present field take rho=w-1=exp(2*pi*i/3). The polynomial X^3-rho
has roots r,r*rho,r*rho^2, all primitive ninth roots of unity and hence all
of degree 6 over Q. None can lie in the degree 16 field K. A reducible cubic
over a field has a root, so X^3-rho is irreducible over K and the separation
lemma applies. This argument does not assume K is normal over Q.

Let T(c,a) consist of the relative seed and its reflected copy, each rotated
by rho^k for k=0,1,2. Since d,u and all relative seed points lie in K, so does
T(c,a). Splitting each exponent modulo 3 gives

    G(c,a)-s_c = T(c,a) union r*T(c,a) union r^2*T(c,a).

Thus it suffices to classify the 812 dihedral-three clouds. The centre has
orbit size1, the distinct axis seed point has orbit size3, and each of the
other27 seed points has orbit size at most6. Hence |T|<=1+3+27*6=166 and
|G|<=496. This count remains valid when additional coincidences occur.

## Independent upper-colouring certificate

`certificate.json` supplies a colour for each of 174 formal addresses(k,f,i)
in each T(c,a), with k=0,1,2, reflection flag f=0,1, and seed label i=0..28.
Words use two bits per colour in increasing address order. They need not
identify coincident addresses: choose the first address for each actual point
and restrict the colouring. Every exact unit pair of representatives is still
among the checked formal pairs. Rotating this colouring into the three copies
gives the same colour at their common centre.

`verify.py` evaluates the paper's rational formulas directly modulo
P=1000001539, using the roots

    (a0,b,c0,e) -> (512562457,103889680,157886017,2545130).

It checks all four defining equations before use. The degree argument above
shows that the integer algebra generated by a0,b,c0,e is precisely the
monic quotient with those relations. Hence evaluation is a ring homomorphism.
The inverses of 2,6,8,64 and of both axis differences are checked to exist
modulo P, extending the homomorphism to every denominator used here. In
particular, equality of a squared distance with 1 in C implies equality
of its evaluated norm with 1. Primality of the modulus is not needed for
this implication; the code explicitly computes all required inverses.

For every same-colour pair the checker evaluates the difference and its
conjugate separately and proves their product is not1 modulo P. No modular
survivor is silently treated as a nonedge. The final certificate checks
3,548,735 such pairs for the family, and 132 for the seed. This proof uses
neither the producer edge list nor its arithmetic implementation nor a
solver verdict. Certificate version, source hash, ordering, padding, exact
case coverage and declared number of colours are checked explicitly.

## Lower bounds and exact classification

A triangle in the seed, verified by exact arithmetic in the a0 basis, proves
the common lower bound three. For each case labelled four, the certificate
lists formal addresses of a smaller subgraph. The checker reconstructs their
exact coordinates, rejects coincidences, and derives every unit edge by
exact norm equality. It then enumerates all possible three-colourings with
an elementary backtracking procedure. A present triangle is assigned colours
0,1,2 without loss of generality; all remaining available colours are tried.
Vertex selection is only a search-order heuristic. Exhaustion is the proof
of non-three-colourability. The subgraphs are witnesses, not a claim of
vertex-criticality or minimum size. Solver UNSAT answers are not premises.

## Complete geometry audit and scope

`geometry.py` generates canonical integer vectors in the w basis, clearing
the reflection denominator with N=d*conjugate(d). Its unit equality is
(X-Y)*conjugate(X-Y)=384^2*N^2. A first residue map rejects most nonedges;
every survivor receives a full integer norm calculation.

`audit_geometry.py` independently constructs all coordinates in the a0 basis,
with denominator768 for the seed and a separate multiplication algorithm
using a quadratic extension of an eight-dimensional multiquadratic algebra.
It compares all 141288 formal positions, every coincidence class, and every
edge with the producer. Its8,738,622 distinct-point pair checks use a second
residue map and 295485 full norm calculations. The exact census yields the
orders and edge counts in the theorem. The cubic separation proof then
reconstructs the full D9 incidence, including all cross-copy nonedges.

The result concerns exactly these 812 seed-centred, seed-axis closures at
unit scale. It does not classify arbitrary centres or axes, other rotation
orders, unions of different closures, or the paper's much larger blow-up
construction. It gives no general four-colouring of K and no record graph.
The trust boundary is the unformalized elementary field and gluing arguments,
the explicit source-coordinate table, and CPython arbitrary-precision integer
arithmetic and exhaustive search. No floating-point decision, SAT soundness
assumption, imported chromatic theorem, external peer review or formal proof
assistant is used in the proof checker.

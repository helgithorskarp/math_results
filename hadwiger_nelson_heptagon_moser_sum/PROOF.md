# An aligned heptagon–spindle sum and the exceptional-rotation reduction

**Exact result.** The point set G=H+M defined below has 143 vertices and
512 strict unit edges. It is four-chromatic. Every unit edge is an image
of an edge of the Cartesian product UD(H) square UD(M), and the only
nontrivial sum fibres are three explicitly listed collision classes.
An XOR colouring descends through those collisions. Consequently every
subgraph of this fixed support is four-colourable.

For arbitrary relative rotations r, all but at most 42840 values on the
unit circle also give a four-chromatic graph UD(H+rM). This is an explicit
finite-exception reduction, not an enumeration or closure of the
exceptional orientations. No five-chromatic graph is established.

## Coordinates and the exact field

Put t=exp(pi*i/21) and K=Q(t). The primitive 42nd-root polynomial is

```
Phi42(T)=T^12+T^11-T^9-T^8+T^6-T^4-T^3+T+1.
```

For j=0,...,6, set

```
P_j = t^(6j)/(t^24-t^(-24)),
Q_j = -t^(6j-7)/(t^6-t^(-6)),
R_j = -t^(6j+7)/(t^12-t^(-12)).
```

Let H be these 21 points, labelled P_0,...,P_6,Q_0,...,Q_6,R_0,...,R_6.
This is the heptagon motif from
[Haugland, Section 2](https://arxiv.org/html/2608.04542v4), in the exact
coordinates of the [parent package](../hadwiger_nelson_heptagon_difference_lifts/PROOF.md).
Only the coordinate definition is imported from that paper. No source
SAT assertion, approximate distance calculation or larger graph is used.

Define u=h_7-h_0, v=h_14-h_0, s=i*sqrt(11), and rho=(5+s)/6. The points
h_0,h_7,h_14 form a unit triangle, so |u|=|v|=|u-v|=1 and |u+v|=sqrt(3).
Also |rho|=1. The spindle, with labels 0 through 6, is

```
M=(0, u, v, u+v, rho*u, rho*v, rho*(u+v)).
```

Its unit edges are

```
01,02,04,05,12,13,23,36,45,46,56.
```

The two diamonds share vertex 0. The closing edge 36 has squared length
|u+v|^2*|1-rho|^2=3*(1/3)=1. The full exact pair scan finds precisely
these 11 edges and seven distinct vertices. This defines the Moser spindle
without relying on an external coordinate file.

The field L=K(s) has degree 24 over Q. Here is the algebraic justification
for coefficientwise equality. The standard cyclotomic Galois description
gives Gal(K/Q) isomorphic to C6 times C2, hence exactly three quadratic
subfields. The elements 2*t^7-1 and

```
(t^6+t^12+t^24)-(t^18+t^30+t^36)
```

square to -3 and -7 respectively, as is also checked exactly. Thus the
three quadratic subfields are Q(sqrt(-3)), Q(sqrt(-7)), Q(sqrt(21)).
Q(sqrt(-11)) is different from all three, by rational square classes.
It is not contained in K; adjoining s therefore has degree two.

The producer represents elements as a(t)+b(t)*s with each polynomial
of degree below 12. It reduces by Phi42 and s^2=-11, and conjugates by
t->t^(-1), s->-s. All point coordinates have a common denominator 42.
Unit distances are tested by the exact equation z*conjugate(z)=1.

The independent audit uses the tensor basis z^a*omega^b*w^c, with
0<=a<6 and b,c in {0,1}, where

```
z=exp(2*pi*i/7), omega=exp(pi*i/3), w=(1+s)/2,
1+z+...+z^6=0, omega^2=omega-1, w^2=w-3.
```

The basis map is t=z^6*omega and s=2*w-1. Conjugation sends z to z^(-1),
omega to 1-omega, and w to 1-w. The audit constructs H using the
denominator-seven inverse identity

```
(z^k-z^(-k))^(-1) = (1/7)*sum_{j=0}^6 j*z^(k+2*k*j),
```

and directly verifies that identity. It constructs rho as (2+w)/3.
Thus neither the primary inverse algorithm nor its multiplication or
conjugation implementation is imported into the independent audit.

## Complete geometry and the quotient colouring

There are 147 formal sums (h_a,m_b). Exact duplicate removal gives 143
points. In the sorted 24-coefficient numerator table, the non-singleton
fibres are precisely

| Sum vertex | Formal representations (a,b) |
|---:|---|
| 21 | (0,3), (7,2), (14,1) |
| 38 | (0,2), (14,0) |
| 60 | (0,1), (7,0) |

The other 140 fibres are singletons. The Cartesian product has
7*42+21*11=525 edge occurrences. Their images give 512 distinct edges
of the sum graph. Scanning all 10153 unordered pairs of distinct sum
points finds exactly these 512 unit edges, with **no additional unit
edge**. These are complete scans, not candidate-edge tests.

More generally, let A,B be finite point sets with proper four-colourings
p,q, with colours identified with F2^2. If p(a) XOR q(b) is constant on
every fibre of the sum map (a,b)->a+b, it defines a colour on A+B.
Every image of a factor edge is proper: its colour difference equals
the nonzero colour difference in that one factor. If all unit edges of
A+B are such images, the descended colouring is proper. This is the
ordinary Cartesian-product colouring argument, with the necessary
collision condition made explicit; no priority claim is made for it.

For this G take any proper H-colouring normalized to
p_0=0,p_7=1,p_14=2, and take

```
q=(0,1,2,3,1,2,0)
```

on M. This q is proper. The three listed fibres have common XOR values
3,2,1 respectively, so the sum colouring is well-defined. The displayed
incidence equality proves it proper. One explicit p and the resulting
143-colour row are in [certificate.json](certificate.json).

The code additionally takes the 42 supplied H-colour rows from the
parent's potential certificate and all ten proper spindle rows with
q_0,q_1,q_2,q_3 fixed to 0,1,2,3. Every one of the 420 combinations
descends and is proper, checked on 215040 unit-edge inequalities.
These ten rows are exhaustive only under those four fixed values;
the value q_3=3 is imposed for collision compatibility, not a
without-loss-of-generality claim about all spindle colourings. The 42
H rows are an explicit supplied class, not all ordinary H colourings.

The 420 resulting colourings are distinct: restricting to H+0 recovers
p, and restricting to h_0+M recovers q. No exhaustive classification
of ordinary G-colourings is claimed or needed.

For the lower bound, a three-colouring of each spindle diamond must
give its two nonadjacent ends the same colour, since their two common
neighbours are adjacent. The two diamonds would force both vertices 3
and 6 to have the colour of vertex 0, contradicting edge 36. The audit
also rejects all 81 three-colour assignments normalized on triangle 012.
G contains the translate h_0+M, so chi(G)>=4. Together with the explicit
upper bound this gives chi(G)=4. Restricting the colouring proves that
every subgraph of this fixed support is four-colourable.

## Finite exceptional orientations

For arbitrary finite four-colourable point sets A,B, put
DeltaA=(A-A) minus{0} and DeltaB=(B-B) minus{0}. For |r|=1 consider A+rB.
If there are neither sum collisions nor unit edges between formal sums
whose two factor indices both differ, the sum map identifies its unit
graph with the Cartesian product. The XOR colouring is then proper.

Any collision with both factors different satisfies a+r*b=0 for some
a in DeltaA,b in DeltaB, giving at most one unit-modulus r per pair.
Any mixed unit-distance event satisfies

```
|a+r*b|^2=1,
2*Re(r*b*conjugate(a)) = 1-|a|^2-|b|^2.
```

Since a and b are nonzero, the latter is a line intersecting a circle,
so it has at most two solutions on |r|=1. Thus an explicitly described
exceptional set E has cardinality at most 3*|DeltaA|*|DeltaB|. Outside E,
A+rB is four-colourable. This deliberately includes events whose unit
edge images may already be factor edges after collisions; membership
in E is only a necessary place to search, not evidence of five-chromaticity.

Here |DeltaH|=420 and |DeltaM|=34 by exact duplicate checks. Hence
|E|<=42840. Every rotation contains a translate of rM, so outside E
the graph is exactly four-chromatic. The aligned r=1 is exceptional
because it has collisions, and is separately settled above. No member
list of E, distinct-angle count, or other exceptional placement was
enumerated in this pass. There is no all-rotation closure.

## Verification and limits

The audit reconstructs all coordinates in its different tensor basis,
compares every coordinate and sum fibre entrywise, and rescans all 210
H pairs, 21 M pairs and 10153 sum pairs. It independently reconstructs
all product edge images, enumerates the ten spindle rows by recursive
edge propagation, and checks all 420 colourings and their sorted byte
stream. It verifies the selected certificate and the spindle embedding.

Controls compare all 576 basis products and all 24 conjugates under the
basis map, check the three quadratic square identities and |rho|=1,
and reject two invalid sum colourings. Small exact sum examples cover
an injective product, a compatible collision, and an extra unit edge
that defeats the XOR colouring. That last control remains colourable;
it illustrates why a critical angle alone does not prove the target.

The trust boundary is the coordinate transcription, the stated
cyclotomic/Galois and graph arguments, exact Python integer/rational
arithmetic, complete finite scans, and ordinary runtime/code correctness.
The new audits were run by the author, not an external reviewer. No
SAT solver, floating-point tolerance or omitted negative proof is used.
This settles the single aligned construction and the generic-rotation
reduction. It leaves the exceptional-orientation search unstarted.

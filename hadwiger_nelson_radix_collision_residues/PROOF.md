# Collision closure by three-colour residue maps

Let ω=(1+i√3)/2, let E=Z[ω], and let U(X) be the strict Euclidean
unit-distance graph on a subset X of C. Coincident labels represent one vertex.

**Theorem.** If z satisfies a monic polynomial P in E[X] of degree d≤4,
then U(E[z]) has an additive proper colouring by F3. In particular its chromatic
number is exactly three.

**Architecture corollary.** Put T={0,1,ω} and A5(z)=Σ(j=0..4) z^j T.
If its 243 digit labels are not injective as complex points, then U(A5(z))
has chromatic number exactly three. The conclusion includes z=0 and every
possible multiple collision, extra unit edge, and singular event intersection.
It also holds for injective A5(z) whenever z satisfies the theorem's monic
polynomial hypothesis.

This is a computer-assisted upper-bound theorem. The two finite colour maps
below are checked exactly. No finite residue graph is asserted to be a physical
plane graph, and no non-four-colourable physical candidate is obtained.

## 1. A finite residue field without a conjugation assumption

The ring R=E[z,conjugate(z)] is a finitely generated Z-module: reduce powers of
ω using ω²−ω+1=0, and powers of z and conjugate(z) using P and its coefficient
conjugate. The at most 2d² monomials ω^e z^j conjugate(z)^k, with e<2 and j,k<d,
span it. All its elements are algebraic integers. In particular 1/3 is not in R,
so R/3R is a nonzero finite commutative ring. Choose a maximal ideal in this
finite ring. Its residue field F has characteristic three. Write ρ:R→F for the
resulting unital ring map.

Since ω²−ω+1=(ω+1)² in characteristic three and F is a field, ρ(ω)=−1.
For any coefficient c=a+bω in E we have ρ(c)=a−b=ρ(conjugate(c)).
Consequently α=ρ(z) and β=ρ(conjugate(z)) are roots of the **same monic**
reduced polynomial p in F3[X], of degree d≤4. No squarefreeness is required.
We do not assume that the chosen maximal ideal is conjugation invariant.

For v=f(z) in E[z], the pair

    Φ(v)=(ρ(v),ρ(conjugate(v)))=(f0(α),f0(β))

uses the same coefficient reduction f0 in F3[X]. This is well defined on actual
complex points, independently of the polynomial representation. Its image is
B={(f(α),f(β)): f in F3[X]} inside F×F. Every unit difference δ satisfies
δ conjugate(δ)=1 in R, hence Φ(δ)=(a,b) has ab=1. Thus Φ is a graph
homomorphism into the additive Cayley graph on B whose connection set is
{(a,b) in B: ab=1}. A unit edge cannot map to a loop. This is the step that
makes the colouring descend through arbitrary physical collisions.

## 2. Complete classification of B and its connection set

Let mα,mβ be the monic minimal polynomials of α,β over F3. Both divide p.
We work inside a common algebraic closure of F3; finite subfields and their
intersections are unique. There are two cases.

**Same irreducible factor, degree r≤4.** We have β=α^(3^k), 0≤k<r.
Evaluation identifies B with F_(3^r), by a↦(a,a^(3^k)). The connection set
is the multiplicative subgroup

    S={a: a^(1+3^k)=1},   |S|=gcd(3^r−1,3^k+1).

All possibilities are as follows.

| r | k | connection size | three-colouring mechanism |
|---|---|---|---|
| 1 | 0 | 2 | ±1 |
| 2 | 0 | 2 | ±1 |
| 2 | 1 | 4 | F9 grid |
| 3 | 0,1,2 | 2 | ±1 |
| 4 | 0 | 2 | ±1 |
| 4 | 1,3 | 4 | F9 grid in additive cosets |
| 4 | 2 | 10 | certified norm81 graph |

For S={±1}, any F3-linear functional taking 1 to 1 is proper.
A size-four subgroup is {±1,±i}, i²=−1, inside the unique F9 subfield.
The functional a+bi↦a+b is nonzero on every connection. Extend it linearly
from F9 to the ambient field to colour all additive cosets. These arguments
use only cyclicity of the multiplicative group of a finite field.

**Different irreducible factors, degrees r,s with r+s≤4.** The polynomial
Chinese remainder theorem identifies B with F_(3^r)×F_(3^s). If ab=1,
then a and b belong to the intersection F_(3^g), g=gcd(r,s), and b=a^−1.
If g=1 the only connections are ±(1,1), so a linear functional taking
(1,1) to 1 gives three colours. The only g>1 possibility is r=s=2.
It is precisely the certified hyperbola81 graph on F9×F9. Different choices
of field presentations or Frobenius identifications give isomorphic graphs.

These cases also cover zero residues, repeated factors of p, and α=β.
Repeated factors add no minimal-factor type. As a finite completeness audit,
verify.py factors **all 120 monic polynomials** of degrees one through four
over F3 into the 32 monic irreducibles (3,3,8,18 by degree), and checks all
ordered distinct-factor cases and all same-factor Frobenius positions.
There are exactly 16 types, recorded in EXPECTED.json. The written minimal
polynomial argument establishes why this finite audit covers every α,β.

## 3. Two explicit linear colour maps

Elements of F3[X]/m are encoded as Σ a_j 3^j, where their field value is
Σ a_j X^j and each a_j is in {0,1,2}. Arithmetic is polynomial arithmetic,
not integer arithmetic modulo 3^r.

For **norm81**, take m=X^4+X+2. The checker proves this polynomial irreducible
by trial division by all irreducibles of degree at most two. The graph on F81
joins u,v exactly when (u−v)^10=1. It has 405 edges. Its ten connections,
in the specified encoding, are

    1, 2, 10, 13, 20, 26, 34, 47, 59, 64.

All have nonzero constant coefficient. Thus c(Σ a_j X^j)=a_0 is a proper
three-colouring. This is the unique size-ten subgroup required for r=4,k=2,
so any F81 presentation is covered by a field isomorphism.

For **hyperbola81**, take F9=F3[i], i²=−1. Encode a pair (a,b) as
encode(a)+9 encode(b). Join (a,b),(c,d) exactly when (a−c)(b−d)=1.
The graph has 324 edges. Writing a=a0+a1 i and b=b0+b1 i, a proper colouring is

    c(a,b)=a1+b0+2b1  (mod 3).

The eight connections (encoded componentwise) are

    (1,1), (2,2), (3,6), (4,5), (5,4), (6,3), (7,8), (8,7).

The displayed functional is nonzero on each. The certificate stores these
connection sets, the four coefficients of each functional, and the full
81-character words. verify.py reconstructs adjacency from the defining field
identities for every unordered pair and checks the words on every edge.

Composing the appropriate F3-linear map with Φ proves the theorem. Since
{0,1,ω} is a unit equilateral triangle inside E[z], exactly three colours are
necessary. Translates and subsets inherit the upper bound.

## 4. Application to the complete collision branch

A collision of different digit words gives a nonzero polynomial
Q(z)=Σ(j=0..4) d_j z^j=0. Each d_j belongs to T−T, which is zero together
with the six units of E. The leading nonzero coefficient is therefore a unit;
dividing by it makes Q monic, still of degree at most four. A nonzero constant
cannot vanish. The theorem applies, and T⊂A5(z) gives the lower bound three.
For z=0 the graph is T directly.

The previous h4105 inventory has 2,400 normalized nonzero-constant collision
polynomials and degree sum 9,204. This theorem removes their **entire root
union**, not just a sample, without relying on numerical roots or on a
collision enumeration. The numerical inventory is needed only to quantify the
change to that previous frontier. All noninjective members are now closed;
the injective pair frontier from h4105 remains (264,800 systems, at most
15,513,472 parameter points before further reductions). Its additional
requirements of four active curves and 1/2<|z|≤2 remain unchanged. Any parameter
in that remaining branch satisfying a monic E-polynomial of degree≤4 is also
excluded by the present theorem, but no count for this further filter is claimed.

The prepublication refresh consumed HN3's h4117 D3 quotient. On that shared
frontier the present theorem removes all 442 collision-polynomial orbits and
their 1,682 root-orbit allowance. The remaining necessary frontier has 132,130
pair-orbit representatives, of total Bezout allowance 7,785,424. Representatives
must be solved over the whole parameter plane; a chamber-restricted solve
requires all 785,380 systems in the D3 closure. The present theorem does not
change that completeness rule or claim a count of realized candidate graphs.

## 5. Trust boundary and provenance

The proof uses elementary integral-ring reduction, finite-field classification,
cyclicity of finite-field multiplicative groups, and polynomial CRT as written
mathematics. It is not proof-assistant formalized. The exact finite certificate
is checked by CPython integer arithmetic; no floating-point equality is used.
The producer searches at most 81 possible linear functionals per graph and
builds edges by Cayley translations. The checker separately constructs every
pair and multiplies with a companion linear map, rather than importing the
producer's convolution arithmetic or edges. It also checks the complete
120-polynomial factor audit. Solver output is not a proof premise.

An exploratory CaDiCaL four-colour query first supplied positive colour words;
subsequent exact linear search gave the stronger three-colour formulas above.
The final producer and checker use only Python's standard library. The earlier
finite-abelian-lifts package supplied a known q=9 colourability signal; its
physical-realization obstruction is not used. This application is a residue
homomorphism upper bound for the existing complex-radix architecture, not a
reopening of that retired physical Cayley construction family. The three-wheel
architecture remains retired by h4085 and reviewer-1 acceptance h4097.

Reduction to finite quotient colourings is an established method (for example
the Polymath discussion “Algebraic formulation of Hadwiger–Nelson problem”).
No priority is claimed for that method or for these small finite graphs. The
specific result here is the paired-residue degree-four theorem and its complete
collision-branch application. At publication this result is author checked;
team-internal checks do not constitute reviewer-1 acceptance.

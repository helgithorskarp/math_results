# Finite abelian Cayley graphs admitting unit-distance drawings

A drawing here is an **injective** map into the Euclidean plane that gives
every edge length one. Crossings and extra unit-distance nonedges are allowed.
No equivariance or additivity of the drawing is assumed.

## The classification

Let A be a finite abelian group, let S=-S be a subset of A excluding zero,
and choose representatives s_1,...,s_r of S modulo sign (an involution gives
one singleton class). Put B=<S> and H_i=<s_j:j!=i>.

**Theorem.** Cay(A,S) admits such a drawing if and only if

    <s_i> intersect H_i = {0}  for every i.

Equivalently, B is the internal direct sum of the cyclic groups <s_i>.
Equivalently, each connected component is a Cartesian product of cycles
C_m (m>=3) and factors K_2. Empty products give isolated vertices. Every
admissible graph has chromatic number at most three. The assertion concerns
the given Cayley presentation; the equivalent graph-product statement is
intrinsic.

### Necessity: rhombi force finite translation identities

Four distinct points p_0,p_1,p_2,p_3 whose successive distances are one
satisfy p_0+p_2=p_1+p_3. Indeed, p_1 and p_3 are the two distinct
intersections of the unit circles centred at p_0 and p_2, and their midpoint
is the midpoint of the centres. This uses injectivity and dimension two.
It is the standard rhombus constraint used, for example, by Alexeev,
Mixon and Parshall in Section 4 of [their paper](https://arxiv.org/html/2412.11914v2).

Suppose F is a drawing. Fix i and write s=s_i. For t in S with t!=s,-s,
the four distinct group elements x,x+s,x+s+t,x+t form a four-cycle.
Consequently, for D(x)=F(x+s)-F(x),

    D(x+t)=D(x).

Thus D is invariant under all translations in H_i. Take h in
<s> intersect H_i, and write h=ks with k>=0. Then

    E(x)=F(x+h)-F(x)=sum_{j=0}^{k-1} D(x+js)

is invariant under every translation in H_i, in particular under h.
If h has finite order m, telescoping gives

    0 = F(x+mh)-F(x) = m E(x).

Over the real numbers this implies E(x)=0. Injectivity forces h=0.
This proves the intersection condition. A relation sum h_i=0 with
h_i in <s_i> puts every h_i in <s_i> intersect H_i, so all h_i vanish;
the generated sum is therefore internal and direct.

### Sufficiency and chromatic number

Draw each cyclic factor as a regular polygon with side length one; draw an
order-two factor as a unit segment. Rotate these drawings independently and
map a product vertex to the sum of its factor positions. Every product edge
has length one.

Generic rotations make this drawing injective and give no extra unit edges.
For a pair differing in exactly one factor, its difference is a polygon
chord (or the segment): it is nonzero, and it has length one exactly for a
factor edge. For a pair differing in at least two factors, write its
difference as sum exp(i theta_j) d_j with at least two nonzero d_j.
Its squared norm is a nonconstant trigonometric polynomial: the Fourier
coefficient at theta_j-theta_k is d_j conjugate(d_k), which is nonzero.
Thus the equations for a coincidence or an unwanted unit distance have
empty interior in the rotation torus. There are finitely many pairs, so
rotations avoiding all these equations exist. They can be chosen with
rational cosine and sine, since such rotations are dense; the resulting
coordinates are algebraic. Draw different connected components far apart.
This also supplies a strict unit-distance realization.

Colour each even cycle and each segment with colours 0,1, and each odd
cycle with 0,1,2. The sum of factor colours modulo three properly colours
the product. More precisely, a nontrivial product is two-chromatic when
all factors are bipartite, and three-chromatic otherwise. Isolated vertices
have chromatic number one. The product-realization argument is included
for completeness; no priority is claimed for that construction or rhombus
logic.

## Norm-one finite-field graphs: exactly one realizable parameter

For any prime power q=p^f>=2 define

    G_q = Cay((F_(q^2),+), {s : s^(q+1)=1}).

The multiplicative group of the field is cyclic, so the generating set has
q+1 members. The additive group is an F_p-vector space of dimension 2f.
For odd p there are (q+1)/2 sign classes; for p=2 there are q+1 singleton
classes. If the number of classes exceeds 2f, their representatives are
linearly dependent. Solving a nonzero dependence for one representative
puts it in the span of the other classes, contradicting the theorem.

For p=2, 2^f+1>2f for all f>=1. For odd p, p^f+1>4f except p=3,f=1:
it holds for f=1,p>=5 and for f=2,p=3, and persists on increasing f.
These elementary inequalities can also be proved immediately by induction.

When q=3 use F_9=F_3[i], i^2=-1. The generators are {1,-1,i,-i}.
They give G_3=C_3 square C_3, with nine vertices, eighteen edges and
chromatic number three. An explicit strict drawing is

    F(a+bi) = T_a + ((3+4i)/5) T_b,
    (T_0,T_1,T_2) = (0, 1, (1+i sqrt(3))/2),   a,b in {0,1,2}.

The independent checker verifies injectivity and all 36 squared distances
in Q(sqrt(3)), as well as the colouring (a+b) mod 3 and a triangle.

**Corollary.** Among all prime powers q>=2, G_q admits an injective
unit-distance drawing in the plane exactly when q=3. In particular, the
complete target-sized family q^2<=508 consists of

    q = 2,3,4,5,7,8,9,11,13,16,17,19,

and cannot produce the target graph. Finite-field unit-distance terminology
does not make these graphs Euclidean unit-distance graphs.

## Compact integer certificates for the eleven finite exclusions

`certificate.json` specifies exact quotient-field moduli and addresses, with
one relation s=sum c_j t_j for each q!=3. Each t_j is a norm-one generator
different from s and -s. The checker independently proves each quotient is
a field by checking a^(q^2-1)=1 for every nonzero element, reconstructs the
entire norm-one set and graph, and checks the relation.

It then expands the relation into a path from 0 to s. At each x=ks,
0<=k<=p-2, this path gives a sum of actual four-cycle rows equal to
D(x+s)-D(x). Weighted summation gives the formal identity

    sum_{k=0}^{p-2} (p-1-k) [D((k+1)s)-D(ks)] = -p D(0).

Here sum_{k=0}^{p-1}D(ks)=0 by telescoping. The checker constructs the
integer row sum literally and verifies that it equals p(e_0-e_s).
Every constituent row uses four distinct vertices and four checked edges.
Thus every putative injective unit drawing would identify 0 and s. There
are 933 checked rows across the eleven exclusions. This finite certificate
does not need the general rank argument as a premise.

## The family really contains an abstract five-chromatic candidate

For q=11 the field is F_11[i], i^2=-1. G_11 has 121 vertices and 726
edges. `q11_five_colouring.json` is checked on all those edges. For the
lower bound the checker independently constructs the exactly-one Boolean
four-colouring formula. Pinning the endpoints of its first edge to distinct
colours loses no solutions, since colour names can be permuted.

`q11_four_unsat.drat` has 539 additions and 101 deletions. The checker
establishes **every addition by reverse unit propagation**: negating that
clause and propagating previous clauses reaches a contradiction. Deletions
can safely be ignored because every retained clause was proved a logical
consequence of the original formula. The final empty clause establishes
unsatisfiability. No RAT step or solver verdict is trusted. Hence

    chi(G_11) = 5,

while the explicit rhombus certificate proves G_11 is not realizable as a
unit-distance graph in the plane. This is not a record improvement.

## Scope

The classification allows arbitrary injective drawings, not only
group-equivariant lifts. It excludes neither noninjective homomorphisms
(which can collapse opposite vertices of a four-cycle), nor selected
subgraphs or edge-deleted graphs. It says nothing comparable about the
infinite torsion-free additive groups generated by Euclidean unit vectors;
these are the groups in the plane-direction work of
[Eng et al.](https://arxiv.org/html/2511.10813v1). No statement closes the
general Hadwiger–Nelson problem or the <=508 search.

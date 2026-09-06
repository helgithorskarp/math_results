# The complete two-orbit exterior support is four-chromatic

The full infinite unit-distance graph on the three unit circles around a unit equilateral triangle, together with **all 108 exterior points** of the fixed two-orbit construction below, has chromatic number **exactly four**. Every subgraph of that support is therefore four-colourable. This closes the entire fixed support, including every subset of its exterior points, without the previous bound of two source normals per rotation class.

The new step is an exact finite graph homomorphism that handles components whose contact normals are all parallel. It includes directions outside the coordinate field and does not require enumerating their circle-intersection roots. A 5,849-byte extension certificate colours all 36 contact patterns over the previously published finite colouring.

This is a negative construction-family result for the Hadwiger–Nelson record search. No five-chromatic graph is produced.

## The fixed geometric support

Work in the complex plane, with all pairs at Euclidean distance exactly one taken as edges. Put

$$
\omega=\frac{1+i\sqrt3}{2},\quad U=\{\omega^j:0\le j<6\},\quad
D=\{d_0,d_1,d_2\}=\{0,1,\omega\},
$$

$$
P=D+U,\quad B=P\setminus D,\quad
X=D\cup C(0,1)\cup C(1,1)\cup C(\omega,1).
$$

The symbol $C(d,1)$ denotes the **whole** circle. The set $P$ has 12 points; $B$ is a nine-cycle. Define the exact unit vectors

$$
\rho=\frac{5+i\sqrt{11}}6,\qquad
\sigma=\frac{-3-\sqrt{33}+i(-\sqrt3+3\sqrt{11})}{12}
$$

and the full exterior set

$$
F=\bigcup_{j=0}^5\big((B+\rho\omega^j)\cup(B+\sigma\omega^j)\big).
$$

These are 108 distinct points outside $X$. The prior [coupled-orientation result](../hadwiger_nelson_triangle_coupled_orbits/README.md) coloured the 36 choices of one translated cycle from each orbit and some other restricted subsets of $F$. It explicitly left $X\cup F$ open. The present result settles that remaining simultaneous support.

**Theorem.** The strict Euclidean unit-distance graph induced by $X\cup F$ has chromatic number four.

The support remains fixed throughout this work. There is no statement about arbitrary translation vectors, another rotation angle, arbitrary three-centre supports, or all finite exterior sets.

## A finite homomorphism for identical contact normals

The [dominating-triangle theorem](../hadwiger_nelson_dominating_triangle/README.md), now [independently accepted](../hadwiger_nelson_dominating_triangle_review1/README.md), decomposes $X\setminus D$ into the exceptional cycle $B$ and generic components

$$
Q(u)=\{d_i+\omega^j u:0\le i<3,\ 0\le j<6\},
$$

one for each nonexceptional unit direction modulo $U$. Each $Q(u)$ is exactly $K_3\square C_6$. Its vertex $(i,j)$ has centre neighbour $d_i$, and different generic components have no edges between them or to $B$. The centre spokes are retained.

The following sufficient finite certificate applies more generally.

**Homomorphism lemma.** Let $W$ be any nonempty finite subset of the plane outside $X$. For each source pair $(w,i)$, form the nonzero normal $A=w-d_i$. Partition these normals under multiplication by $U$, and choose representatives $N_1,\ldots,N_m$.

Let $R$ be the set of generic direction orbits whose components have two nonparallel contact normals from $W$. Set

$$
M_W=P\cup W\cup\bigcup_{u\in R}Q(u)
$$

with its complete geometric unit edges. For each normal representative $N_h$, add a fresh abstract copy $T_h$ of $K_3\square C_6$, labelled $(h,i,j)$. Give this copy its owner spokes to $d_i$, and add the edges

$$
w\ \text{--}\ (h,i,j)
\quad\text{exactly when}\quad
w-d_i=\omega^jN_h.
$$

There is a graph homomorphism from the full unit-distance graph on $X\cup W$ into this finite abstract graph $H_W$, fixing $M_W$ pointwise. Thus

$$
\chi(X\cup W)\le\chi(H_W).
$$

This is a sufficient colouring certificate. We do **not** assert the converse: abstract blocks can impose constraints even when their corresponding unit-circle equations have no realization or only a realization already retained in $M_W$. The abstract graph need not admit a unit-distance embedding.

### Proof of the lemma

A contact from $w$ to $d_i+\omega^j u$, where $|u|=1$, is equivalent to

$$
2\langle u,\omega^{-j}(w-d_i)\rangle=|w-d_i|^2.
$$

Call $\omega^{-j}(w-d_i)$ its contact normal in this parametrization. Two compatible parallel nonzero contact normals must be **identical**. Indeed, if they are $A$ and $tA$, their two equations require $t|A|^2=t^2|A|^2$, giving $t=1$ since both are nonzero.

A generic component outside $M_W$ has no pair of nonparallel contact normals. If it has a contact at all, all its contact normals must therefore be one identical vector $A=\omega^kN_h$. Replace its direction representative $u$ by $z=\omega^{-k}u$. This only rotates its six column labels. In the resulting parametrization every contact normal equals $N_h$.

For this $z$, map $d_i+\omega^jz$ to $(h,i,j)$. Every actual exterior contact then maps to one of the stipulated source-pattern edges. In fact the pattern is exact: whenever $w-d_i=\omega^jN_h$,

$$
|w-(d_i+\omega^jz)|^2-1
=(|z|^2-1)+|N_h|^2-2\langle z,N_h\rangle=0.
$$

All internal component edges and owner spokes are preserved. If a generic component has no exterior contact, map it by its owner and column labels to any one block, for example $T_1$; extra target edges cause no problem for a homomorphism.

Keep the vertices of $M_W$ fixed. The triangle-circle decomposition shows there are no additional cross-component edges to check. Distinct components may map to the same block, which is allowed because they have no edges between them. Thus the map preserves every edge on the entire uncountable support.

Finally, $R$ is finite. A pair of nonparallel contact equations has at most one solution for its unit direction, and there are only finitely many source-normal pairs and six relative rotations. The statement for empty $W$ follows separately from the three-colouring of $X$.

Both roots of an identical-normal circle equation, when they exist in different direction orbits, use the same labelled block. Tangencies and missing roots require no additional case in this sufficient construction. No assumption about a field containing those roots is made.

## Exact nonparallel census for this support

For $W=F$, the complete source multiset has $3\cdot108=324$ normals. Its 36 rotation classes have sizes

| Class size | Number of classes |
|---|---:|
| 6 | 12 |
| 9 | 12 |
| 12 | 12 |

The prior [compact contact certificate](../hadwiger_nelson_triangle_coupled_orbits/certificate.json) gives all 36 canonical representatives. It includes the full nonparallel census across those representatives and is rechecked here.

All representative pairs, including equal representatives, and all six relative rotations give

$$
\binom{36+1}{2}\cdot6=3996
$$

cases. Their exact outcomes are:

| Outcome | Number |
|---|---:|
| Identical normals | 36 |
| Parallel incompatible normals | 78 |
| Nonparallel, nonunit circumcentre | 3,742 |
| Nonparallel, unit circumcentre | 140 |

For nonparallel normals $A,A'$, the independent checker uses

$$
|A|^2|A'|^2|A-A'|^2=4\det(A,A')^2
$$

as the unit-circumradius criterion and checks each positive solution against the original two linear equations. The determinant is separately nonzero. All 140 unit witnesses reduce to the three direction orbits represented by $-1,-\rho,\sigma$.

The first orbit is already the exceptional patch. Therefore the only generic components having any nonparallel contact pair are

$$
Q(-\rho),\quad Q(\sigma).
$$

This conclusion holds for the full $F$, even though the prior colouring argument applied only to certain subsets. Every source normal from $F$ is represented in the rechecked census. Its coefficients lie in $\mathbb Q(\sqrt3,\sqrt{11})$ on each Cartesian axis; a nonparallel pair uniquely determines its solution in that field. Components involving contact directions outside the field have only identical contact normals and are covered by the new abstract blocks.

The resulting actual finite base is

$$
M=P\cup F\cup Q(-\rho)\cup Q(\sigma),
$$

with 156 distinct vertices and all 690 unit edges. These points and edges are reconstructed and all 12,090 pair distances are tested exactly.

## The positive extension certificate

For each of the 36 classes, the new certificate supplies the full list of source triples $(w,i,j)$ and a proper four-colouring of its 18-vertex block. The old 156-vertex colouring is used **unchanged**, with centre colours $0,1,2$.

The abstract graph has

$$
156+36\cdot18=804\text{ vertices}
$$

and

$$
690+36(36+18)+324=2958\text{ edges}.
$$

The terms are the actual base edges, 36 internal edges and 18 owner spokes per block, and one attachment for each source event. The verifier checks all 2,958 colour inequalities directly.

The **804 vertices belong to an abstract colouring certificate**, not to a new Euclidean unit-distance construction. The actual support being coloured is infinite. Applying the homomorphism proves its four-colour upper bound.

The producer finds each block colouring by a finite cycle dynamic program. A column is a triple of distinct colours from $\{0,1,2,3\}$ avoiding each owner colour. There are 11 such states, with 44 compatible ordered pairs, where neighbouring columns differ in each coordinate. Exterior colours filter the allowed states; a compatible six-cycle gives a complete block colouring. The verifier does not trust this search and does not use its dynamic program: it checks the resulting complete abstract graph directly.

## Exact lower bound

The actual finite base already contains a Moser spindle. Using the coordinate order of the linked parent certificate, its shared root is vertex 0, its two tips are 22 and 35, and the respective middle pairs are $(1,8)$ and $(4,14)$.

The checker verifies seven distinct exact points and all 21 pair distances. They induce exactly the eleven edges of two diamonds sharing the root, together with the edge between the tips. In any three-colouring, the two nonadjacent tips of a diamond must have the same colour. The common root therefore forces both outer tips to its colour, contradicting their unit edge.

As a separate definition-level check, the verifier exhausts all $3^7=2187$ assignments and finds no proper three-colouring. The inherited four-colouring is proper on all eleven edges. This proves the lower bound four without importing the earlier 57-vertex three-colour obstruction. Combining with the upper bound gives the stated exact chromatic number.

This use of a small classical lower-bound witness is not a new Moser-spindle construction or a return to the retired Moser/Parts assembly family.

## Reproduction and trust

From the repository root with Python 3.11.2 or compatible Python 3, using only the standard library and a new output directory:

~~~sh
python3 -B hadwiger_nelson_triangle_simultaneous_exterior/build.py --out /tmp/hn-full-exterior
python3 -B hadwiger_nelson_triangle_simultaneous_exterior/verify.py --work /tmp/hn-full-exterior
~~~

[build.py](build.py) regenerates the 5,849-byte [certificate.json](certificate.json) and requires a byte match. Its SHA-256 is

~~~text
8be9e1a93df1ff717432b20f26b4e331ff89703dbc55493be924a64396a9c27a
~~~

The only external data file needed is the linked 19,427-byte parent certificate, already in this repository. Its SHA-256 is pinned in both programs and the new certificate:

~~~text
8680dc794ddb0543fd89f93fa61e6119521ebba51c422a74c4eae0dcf7f5a23a
~~~

[verify.py](verify.py) imports neither producer nor any parent executable. It reuses the prior author-written sparse-radical audit as local source, rechecks the entire 3,996-case census and the complete actual base geometry, and reconstructs every source event by direct matching against the 216 explicit representative/rotation slots. The new producer instead assigns events through canonical orbit representatives and finds colourings by the 11-state cycle program. The positive checker checks every edge directly.

Five malformed extension certificates are rejected: a missing block, a missing source event, a wrong column label, an owner-colour conflict, and a wrong lower-bound witness. Normal and optimized Python executions agree byte for byte. [expected.json](expected.json) supplies exact results and [validation.json](validation.json) supplies timings and provenance. [SHA256SUMS](SHA256SUMS) pins this package's source and compact evidence.

The universal step depends on the triangle-circle decomposition and the homomorphism proof above, not on finite sampling. Operational trust remains in exact Python integer/Fraction arithmetic, the squarefree-radical basis, faithful decoding, exhaustive execution, and SHA-256. No floating-point geometry, native solver, large omitted proof trace, proof-assistant formalization, or independent-author review of this new result is claimed. The parent continuum decomposition has a separate independent acceptance.

## Research decision

Every subgraph of $X\cup F$, with any subset of the fixed 108 exterior points, is now four-colourable. This removes the multiplicity restriction from the previous fixed-family exclusion. No further search inside this support can yield a five-chromatic graph.

The target remains a five-chromatic Euclidean unit-distance graph on at most 508 vertices. [Parts's primary paper](https://arxiv.org/abs/2010.12665) gives 509 vertices, and [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4) still names that record; both were checked live on 2026-09-06. No record or priority claim is made.

The teammate's [630-vertex five-chromatic seed](../hadwiger_nelson_heule632_pair_pilot/README.md) is a separate exact-support direction, not a premise here. This pass ends with the full fixed two-orbit construction closed. A subsequent geometric phase should change the support mechanism, for example by using a three-centre set that is not a clique, rather than continuing subset searches inside this now excluded support. No next support or parameter phase has started.

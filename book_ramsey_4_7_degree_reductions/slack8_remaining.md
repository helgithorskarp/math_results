# Every 22-vertex Book Ramsey witness has 3n8+n9 at most30

Actual author: **six-books-1**, role **researcher**, 2026-10-01.
The team shares one signing identity; this identifies the actual author.

**Conditional theorem.** A simple red graph on22 vertices, with every
red edge having at mostthree common red neighbors and every blue
complement-edge having at mostsix common blue neighbors, cannot have
either degree histogram **(n8,n9,n10)=(7,10,5) or(9,4,9)**.
Books are ordinary noninduced subgraphs. No connectedness or automorphism
is assumed.

**Combined corollary.** Every red-B4/blue-B7-free coloring on22 vertices
satisfies **3n8+n9<=30**, equivalently its even incident parity surplus
is at least12. Its total unused spine capacity T satisfies **2T>=n9+12**.
Using the credited earlier degree and97-edge theorems, the degree range
remains8..10 and edge range98..110. At98 edges only
**(a,24-2a,a-2),2<=a<=6** remain; at99 only
**(a,22-2a,a),0<=a<=8** remain. These are necessary counts, with no
realizability assertion. Neither entire boundary nor the Ramsey22..23
gap is resolved.

The increment excludes the two remaining surplus-eight histograms.
Of1,111 necessary weighted-defect forms,1,108 have nonsquare forced
determinants. Two square cases have a rational33-plane norm obstruction.
The last square case forces an equitable red degree partition with an
impossible incidence count. Its forced matrix actually has a rational
symmetric square root, explicitly checked below; the adjacency condition
is needed in that branch. The new conditional proof is free of historical
spectral graph classifications; the combined corollary inherits the
named dependencies of the earlier global theorems.

## 1. Defects, parity and the forced integer square

Let R be red adjacency, d_i its degrees. Define the symmetric matrix F
with diagonalzero, whose off-diagonal entry is three minus the red
codegree at a red spine, or six minus the blue codegree at a blue spine.
F has nonnegative integer entries. Put f_i=sum_j Fij and
q_i=f_i-(d_i mod2). Every monochromatic triangle through i contributes
twice to incident pages, so

```
f_i=3d_i+6(21-d_i)-2*(monochromatic triangles through i).
```

Thus f_i has degree parity and q_i is even and nonnegative.
The universal identities in [parity_square.md](parity_square.md) give

```
T=sum_{i<j}Fij=66-(3/2)*sum_i(d_i-10)^2,
sum_i q_i=2T-n9=132-12n8-4n9.                         (1)
```

For both target histograms the surplus total is8. T is9 at(7,10,5)
and6 at(9,4,9). The page identity is

```
(R^2)ij=d_i+d_j-14+(17-d_i-d_j)Rij-Fij  (i!=j).
```

For K=2R+diag(2d_i-17), the off-diagonal R terms in K^2 cancel:

```
H=K^2,
Hii=(2d_i-17)^2+4d_i,
Hij=4(d_i+d_j-14)-4Fij                 (i!=j).          (2)
```

For degrees8,9,10, putting y_i=10-d_i gives the equivalent formula

```
H=25I-4diag(1_{d_i=9})+24J-4(y1^t+1y^t)-4F.          (3)
```

In particular detH must be an integer square. Equations(1)--(3) are
written counting/algebra identities, not empirical claims from the controls.

## 2. Complete weighted-defect normal forms

Call a vertex a center when q_i>0. There are at mostfour centers;
each has type(d,q), d in8,9,10 and q in2,4,6,8. Other degree-eight and
degree-ten vertices have F-rowzero. Every other degree-nine vertex
has F-rowone, hence is either a unit leaf at a center or an endpoint
of a unit matching edge. Nonnegativity makes these leaves distinct.

Choose a sorted center-type profile of totalq8. For every unordered
center pair, assign an integer weight fromzero to the smaller remaining
row budget. The row budget at type(d,q) is q+(d mod2). At the end the
unused row budgets are unit leaf counts. Their sum cannot exceed the
noncenter degree-nine count; the remainder must be even and is paired.
These conditions are sufficient to construct F, and necessary for every
F with the required nonnegative parity surplus.

Only center permutations preserving the identical(d,q) types are
quotiented, using the least lexicographic center-weight tuple. Assign
center labels first within each red-degree class, then increasing
degree-nine leaf labels and matching pairs. Any actual F can be brought
to this form by permuting its centers, leaves, matching endpoints and
isolates within red-degree classes. This relabels the entire hypothetical
R together with F; it makes no red-host automorphism assumption.
All possible leaf choices and residual matching choices are therefore
covered, even though the host's remaining red edges are not enumerated.

The complete exact census is:

| Histogram | Candidate profiles | Nonempty profiles | Fixed-type labeled cores | All ordered-type cores | Normal forms | Nonsquares | Squares |
|---|---:|---:|---:|---:|---:|---:|---:|
| (7,10,5) | 51 | 51 | 1702 | 8375 | 768 | 768 | 0 |
| (9,4,9) | 51 | 45 | 732 | 3847 | 343 | 340 | 3 |

The six empty profiles are recorded withzero counts, rather than silently
omitted. The two labeled-core counts count weighted center graphs and
center type orders; they are not counts of unrestricted red graphs.
Every canonical record, exact determinant, floor square root and full
F/H fingerprint appears in
[slack8_remaining_expected.json](slack8_remaining_expected.json).

For the1,108 nonsquare cases the determinant is strictly between the
square of its recorded integer and the square of its successor. This
contradicts detH=(detK)^2. At(7,10,5) this finishes the conditional
theorem, even excluding arbitrary rational square roots of every retained
H. An integer that is a rational square is an integer square, by clearing
coprime numerator and denominator. The three squares at(9,4,9) require
the following additional arguments.

## 3. Two square cases: a rational33-plane

Use canonical labels A=degree8 on0..8, B=degree9 on9..12, and C=degree10
on13..21. The first square F has weighttwo on01 and13,14, weightone
on9,10 and11,12, andzero elsewhere. The second has weightthree on9,12
and10,11, andzero elsewhere.

| Case | detH | Square root | Basis of the33 eigenspace |
|---|---:|---:|---|
| Two weight-two pairs | 9265937486328184604644775390625 | 3044000244140625 | e0-e1, e13-e14 |
| Two weight-three pairs | 7979831867851316928863525390625 | 2824859619140625 | e9-e12, e10-e11 |

Each displayed basis has Gram2I. Both exact rank computations give
rank(H-33I)=20, so these two vectors span the entire33 eigenspace.
Any rational symmetric K with K^2=H commutes with H and preserves that
rational plane. Its coordinate matrix U is rational and symmetric,
because its basis vectors have equal norms and are orthogonal.
It satisfies U^2=33I. The irreducible polynomial x^2-33 has degree2,
so U has characteristic polynomial x^2-33 and tracezero. Consequently

```
U=[[u,v],[v,-u]],       u^2+v^2=33.
```

Clear common denominators, obtaining coprime integers a,b,c with
a^2+b^2=33c^2 and c!=0. Mod3 forces a,b divisible by3. Substituting
a=3a', b=3b' gives3(a'^2+b'^2)=11c^2, which forces c divisible by3.
This contradicts coprimality. Both cases have no rational symmetric
square root and hence no adjacency root. The same norm mechanism was
used for the earlier [97-edge surplus-eight exclusion](slack8.md);
the two new matrices and their entire eigenspaces are checked here.

## 4. Last square case: an equitable red partition

The last F is the unit K4 on B andzero elsewhere. Its determinant is
12721648090519011020660400390625, the square of3566741943359375.
Let W be the rational span of the three degree-class indicator vectors.
H acts by25 on the contrasts within each degree class. On W it acts by

```
Q=[[97,48,144],[108,73,180],[144,80,241]],
Gram(class indicators)=diag(9,4,9),
det(Q-25I)=82944.                                     (4)
```

Every block is constant away from its diagonal and its diagonal exceeds
the within-block constant by25. Thus the19-dimensional contrast space
is killed by H-25I. Its restriction to W is invertible by(4), so
**image(H-25I)=W**, dimensionthree. The programs separately verify the
full block formula, rankthree, quotient and determinant.

An adjacency root K commutes with H and therefore preserves W. The
diagonal matrix diag(2d_i-17) also preserves W, so
R=(K-diag(2d_i-17))/2 preserves W. This means the red degree classes
form an equitable partition: within each class every vertex has the
same integer neighbor count into any other class. It is a consequence
of the forced matrix, rather than a symmetry hypothesis on G.

For completeness, summing the universal page identity gives

```
f_i=2e-294+38d_i-d_i^2-2*sum_{j in N_R(i)}d_j.
```

Writing s8_i,s10_i for the red-neighbor counts in A,C, the neighbor
degree sum is9d_i-s8_i+s10_i. At e=99 this gives

```
s8_i-s10_i=8-d_i+q_i/2.                              (5)
```

At each B vertex, d_i=9, f_i=3, q_i=2, so s8_i=s10_i. Let k be the
common red degree inside the four-element B, supplied by equitability.
Then9-k is even and0<=k<=3, forcing k=1 or3. Each B vertex has
(9-k)/2=4 or3 red neighbors in A. There are therefore16 or12 red
A-B edges. Equitability on the nine-element A makes this count nine
times an integer. Neither16 nor12 is divisible bynine. Contradiction.

This last H has an explicit rational symmetric square root. Its quotient
has the root L=[[5,4,6],[9,1,9],[6,4,13]], with L^2=Q. For i in classa,
j in classb, define

```
K0_ij=5*delta_ij+(L_ab-5*delta_ab)/|classb|.
```

K0 is symmetric and K0^2=H; its trace is114. The certificate includes
the complete integer matrix36K0. Both programs verify all its entries
and the square1296H. This control exhibits the distinction needed for
the theorem: the equitable-incidence argument excludes actual red
adjacency roots, while general rational symmetric roots exist here.

## 5. Exact reproduction, separate algorithms and trust boundary

[slack8_remaining_check.py](slack8_remaining_check.py) imports no older
research program. It recursively fills center edge weights with row
budgets, quotients identical center types, constructs full22 matrices,
uses checked integer Bareiss determinants, integer square roots and
integer row operations with gcd reduction for the ranks.

[slack8_remaining_independent.py](slack8_remaining_independent.py) also
imports no author or predecessor program. It uses ordered positive
surplus compositions, every degree-color order, and multisets of unit
center edges. It normalizes the resulting literal weighted adjacency
from reverse labels under all center permutations. Exact Fraction
Gaussian elimination supplies full determinants and ranks; binary search
supplies floor roots. For the last case it independently checks the
complete contrast/indicator decomposition and derives L through rational
matrix inversion. All51+51 profiles,1,111 canonical cases,12,222 ordered
type cores, and every full F/H entry agree: **537,724 entries per family**.

The separate program rejects18 corrupted certificates, including altered
coverage, weights, determinants, roots, ranks, norm residues, quotient,
incidence counts and full matrix entries. Guards remain active under-O.
These are two author implementations; no independent peer-review verdict
or proof-assistant formalization of this extension is asserted.

Both programs reproduce the known21-vertex matrix:93 red edges,
degree counts4/16/1 and red/blue page maxima3/6. Its original primary
file was freshly fetched this pass; all441 complemented entries matched
[baseline21.rows](baseline21.rows). Original-file SHA256:

```
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55
```

There are24 degree-preserving signed controls per target histogram.
They can violate books. Literal pages,1,056 incident row identities
and23,232 K^2 entries are checked; the separate program also counts all
monochromatic triangles through each vertex. The48 recorded masks are
validation fixtures only, not inputs selecting the theorem's domain.
Their arithmetic controls do not replace the displayed universal proofs.

From the repository root, using CPython3.11.2 and the standard library:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_4_7_degree_reductions/slack8_remaining_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_4_7_degree_reductions/slack8_remaining_independent.py
```

For optional full-entry comparison, give the first command
`--matrices /tmp/book-slack8-matrices.json`, and the second the same
argument. It is generated data and is not published. The main final
replay used2.925s/43,768KiB; the separate full-entry audit used
16.068s/56,636KiB. Jobs were sequential and all numerical threadsone.
No timeout, memory failure, incomplete domain, native solver, or floating
arithmetic supplied any mathematical inference.

Compact expected certificate SHA256:

```
c1cf104dfe3f8b71c07b8b85678669e7dbd274a949131798bc0f9390064e9679
```

The exact finite determinant/rank computations are premises of the
computer-assisted proof. The counting, normal-form completeness,
rational norm and image-to-equitability bridges are written mathematics,
unformalized. No large omitted proof corpus or external graph catalogue
is needed by the conditional theorem.

## 6. Combined corollary, dependencies and primary literature

The prior [global degree theorem](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
graph `bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`,
gives degrees8..10. The prior [first-slack theorem](first_slack.md), graph
`bafkreihrh6ngmajbg6zs2wzztlk5g5ywwyyguvnu46eaemree6kj7i6bve`,
gives3n8+n9<=31. At equality, a+b+c=22 and3a+b=31 give
b=31-3a,c=2a-9. Handshake parity makes b even and a odd; nonnegativity
then leaves exactly(5,16,1),(7,10,5),(9,4,9). The first was excluded by
[slack8.md](slack8.md), graph
`bafkreiazubi5xvgjefre2trbr5nhtlgpxng34fyy5lbwpm7b2xrpphg2xy`.
The conditional theorem here excludes the other two. Thus3n8+n9<=30,
and(1) gives2T>=n9+12. The shortened98/99 lists follow from handshake.

The current98..110 edge range is credited to [degree97.md](degree97.md),
graph `bafkreiadodqec5yk5g3mdn75jvh6icxx4hz6b76akv2wkaifa4mlta6krm`;
its lower bound is not a new increment here. The universal matrix and
incident identities are credited to [parity_square.md](parity_square.md),
graph `bafkreidagwfnpcg6aip47vp6bqfo35ptfacaciwplggiqokuarmcls5zcm`.
The earlier [parity/saturation independent review](../book_ramsey_parity_square_review3/REVIEW.md)
and [degree-eleven independent review](../book_ramsey_degree11_gram_review1/REVIEW.md)
concern earlier premises, not this extension. The new
[independent97-edge audit](../book_ramsey_97_boundary_review3/REVIEW.md),
graph `bafkreiak5em224ewuxfqnd6m6ruphrlehug346ggowp6mcaivltzz5wso4`,
confirms the whole97 boundary and the full559-form predecessor. It also
gives smaller spectral certificates and an elementary lower98 argument
without the historical classification dependency. The separate
[complete first-slack review](../book_ramsey_first_slack_review4/REVIEW.md)
graph `bafkreiftiy6fj4kjunveucjiegmgk2t7654kzqh4bph4yareu6jqvlwzci`,
confirms all53 earlier forms, including the98/99 instances.
These assessments cover the credited premises, not the new1,111-form
extension. The independent lower98 refinement leaves the following
global degree/count dependency boundary intact.
The combined minimum-degree and first-slack premises retain their named
Bussemaker--Cvetkovic--Seidel1976 and Doob--Cvetkovic1979 classification
dependencies. Those historical proofs and earlier computational
certificates are not replayed here.

Primary tables were reopened live2026-10-01:
[Lidicky--McKinley--Pfender--VanOverberghe, Table1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski, DS1.18, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
retaining22<=R(B4,B7)<=23. The [Dai--Lin primary paper](https://arxiv.org/abs/2606.07214)
concerns diagonal/difference-two regimes. The
[primary21-vertex construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is the known baseline above. Targeted literature and committed graph
checks found no overlapping two-histogram exclusion; they are bounded
evidence and do not establish historical priority. No novelty is claimed
for Goodman counting, determinant squares, rational norm obstructions,
or equitable partitions themselves. The increment is their fully
quantified application to these two remaining histograms and the
combined degree-count restriction. The global flag-algebra upper-bound
certificate is literature context and was not rerun.

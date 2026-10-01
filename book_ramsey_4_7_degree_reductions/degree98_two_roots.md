# A 98-edge Book Ramsey witness cannot have degree counts (2,20,0)

Actual author: **six-books-1**, role **researcher**, 2026-10-01.
The campaign shares one signing identity; this names the actual author.

**Conditional theorem.** There is no simple red graph on 22 vertices
with two vertices of degree eight, twenty of degree nine, at most three
common red neighbors at every red edge, and at most six common blue
neighbors at every edge of its complement. Books are ordinary,
noninduced subgraphs. There is no connectedness or automorphism hypothesis.

**Combined corollary.** Every 98-red-edge coloring avoiding red B4 and
blue B7 has degree counts

```
(n8,n9,n10)=(a,24-2a,a-2),       3<=a<=6.
```

These are necessary counts, without a realizability assertion. The
credited global degree range remains 8..10, edge range 98..110, and
degree budget 3n8+n9<=30. No entire 98-edge boundary is excluded; the
unrestricted Ramsey interval remains 22..23.

The mechanism is a structural defect decomposition followed by a small
exact computation. A saturated pair forces a defect triangle with three
leaves at each center, two internal matchings, and a 4-by-4 cross matrix
with row and column sums two. Of the complete 282 forms, 264 have
nonsquare forced determinants. All 18 square forms have the same
six-dimensional integral eigenspace. An even-trace condition for its
integral Gram matrix contradicts the forced adjacency trace -3.

## 1. The saturated pair and its attachment classes

Let R be red adjacency and d its degrees. Use the nonnegative symmetric
spine-defect matrix F, with zero diagonal and

```
Fij=3-(common red neighbors of i,j)       when ij is red,
Fij=6-(common blue neighbors of i,j)      when ij is blue.
```

Put f_i=sum_j Fij and q_i=f_i-(d_i mod2). The universal counting and
matrix identities are credited to [parity_square.md](parity_square.md),
graph `bafkreidagwfnpcg6aip47vp6bqfo35ptfacaciwplggiqokuarmcls5zcm`.
In particular,

```
f_i=2e-294+38d_i-d_i^2-2*sum_{j in N_R(i)}d_j,
K=2R+diag(2d-17),       H=K^2,
Hii=(2d_i-17)^2+4d_i,
Hij=4(d_i+d_j-14)-4Fij                    (i!=j).     (1)
```

There are two degree-eight vertices a,b and twenty degree-nine vertices
B; their degree sum gives e=98. If sA_i counts red neighbors in
A={a,b}, the incident identity becomes

```
f_i=2-(d_i-10)^2+2*sA_i.                              (2)
```

At a and b, nonnegativity and sA<=1 force ab red and f_a=f_b=0.
Every F entry touching either root vanishes. The red edge ab therefore
has exactly three common red neighbors in B. Each root has seven red
neighbors in B. Partition B into

| Class | Red adjacency to the roots | Size | F-row sum |
|---|---|---:|---:|
| C | both a and b | 3 | 5 |
| X | a only | 4 | 3 |
| Y | b only | 4 | 3 |
| Z | neither | 9 | 1 |

Every root-B pair has red codegree exactly three, regardless of its
spine color. Indeed the universal identity

```
(R^2)ij=d_i+d_j-14+(17-d_i-d_j)Rij-Fij
```

has d_i+d_j=17 and Fij=0 for such a pair.

## 2. A positive vector forces the entire defect decomposition

Write 1 for the all-one vector, u=e_a+e_b, v=e_a-e_b,
h=R*u, and w=1_X-1_Y. Coordinates of h are one on A, two on C,
one on X and Y, and zero on Z. Degrees and the saturated codegrees give

```
R*1=9*1-u,       R*u=h,       R*h=6*1+5*u.             (3)
```

The last identity counts R^2*u: its coordinates are eleven on A and
six on B. Let D=diag(2d-17). Then

```
D*1=1-2u,       D*u=-u,       D*h=h-2u.
K*1=19*1-4u,    K*u=2h-u,    K*h=12*1+8u+h.
```

Consequently K^2*h=240*1-48u+17h. With u the indicator of A, the
forced matrix in (1) also has the full block formula

```
H=21I+16J-4(u1^t+1u^t)+4diag(u)-4F.                  (4)
```

Here 1^t*h=16 and u^t*h=2. Thus (4) gives
H*h=248*1-60u+21h-4F*h. Comparing the two expressions proves

```
F*h=2*1-3u+h.
```

From the row sums and zero root rows, F*1=1-3u+2h and F*u=0.
The vector

```
p=1+h-2u=3*1_C+2*(1_X+1_Y)+1_Z
```

is positive on B and satisfies **F*p=3p**.

For the contrast identity, (1) gives H*v=25v, while R*v=-v+w,
hence K*v=-3v+2w. K commutes with H, so H*w=25w. Formula (4)
on w reduces to H*w=21w-4F*w, proving **F*w=-w**.

Now each Z vertex has F-row sum one, so has exactly one unit F edge.
Its p-weighted row sum is three; its neighbor must lie in C, where
p has value three. Hence there are no F edges from Z to X,Y,Z.
At a vertex of X or Y the ordinary F-row sum is three and its
p-weighted sum is six. Available neighbors have p-values two or three,
so every F edge from X or Y to C must vanish.

At a C vertex let x be its F-weight into C and z its number of Z
leaves. The row and weighted-row equations are x+z=5 and 3x+z=9.
Therefore x=2 and z=3. The three loopless C row degrees all equal two,
forcing **F[C] to be a unit triangle**, with exactly **three distinct
unit Z leaves at each C vertex**.

For X, F*w=-w and the total row sum three give F-weight one within X
and two into Y. The analogous statement holds for Y. Nonnegative
integer row degree one makes F[X] and F[Y] unit perfect matchings.
Their cross block **M=F[X,Y] is a nonnegative integer 4-by-4 matrix
with every row and column sum two**. Its entries belong to 0,1,2.
There are no other positive F entries.

## 3. Complete finite domain and exact determinants

Normalize labels as follows: A=0,1; C=2,3,4; X=5..8; Y=9..12;
Z=13..21. Put the three leaves at C vertex 2 at 13,14,15, and
likewise successive triples at 3 and 4. Put the internal X matching
at 5,6 and 7,8, and the Y matching at 9,10 and 11,12.

Every actual F can be so labeled: permute its leaves within Z and its
matching endpoints within X and Y. Relabel the whole hypothetical R
together with F. No automorphism of the red host is being assumed.
The finite domain retains **all** M after this matching normalization.

The primary generator chooses one of the ten compositions of two into
four nonnegative parts for each row, with remaining column budgets two.
This generates precisely **282** matrices. A separate generator uses
unordered pairs of the 24 perfect matchings between X and Y: **300**
pairs produce the same 282 matrices. Completeness of that second route
follows by alternating colors around every component of a degree-two
bipartite multigraph, including a pair of parallel edges. Each color
then gives a perfect matching. Different decompositions can give the
same M, which the separate program explicitly deduplicates.

For each M construct the full F and the integer H in (1). Its exact
determinant must equal (detK)^2. All 282 determinants are positive;
**264 lie strictly between consecutive integer squares**. The compact
[expected certificate](degree98_two_roots_expected.json) records every
M, determinant, floor root and full F/H fingerprint. These 264 forms
cannot come from red adjacency.

The eight matching-preserving permutations of X and independently Y
give 16 orbits on the 282 forms, without using X/Y transposition.
There are three square-determinant orbits:

| Orbit | Representative M, with rows separated by semicolons | Labeled forms | detH |
|---|---|---:|---:|
| 1 | 0002;0020;0200;2000 | 8 | 1364618767559333941760197640625 |
| 2 | 0011;0011;1100;1100 | 2 | 1693735740792209039117431640625 |
| 3 | 0101;1010;0110;1001 | 8 | 1958440261171195679159399000625 |

Every one of the 18 square matrices is checked directly, not inferred
solely from the orbit count. **rank(H-21I)=16** in every case.

## 4. One integral trace obstruction for every square case

For each of the three Z leaf triples take two vectors

```
e_first-e_last,       e_second-e_last.
```

They are supported in Z and give six independent vectors. Each is a
21 eigenvector of H: its F-image is zero and its coordinate sum is
zero in (4). The exact rank 16 computation proves that they span the
**entire** eigenspace E=ker(H-21I).

The lattice L=E intersect Z^22 is exactly the integer vectors supported
on Z with coordinate sum zero in each leaf triple. The displayed
vectors form a basis of this full lattice: its coordinates are simply
the first two integer entries in each triple. Its Gram matrix is

```
G=diag([[2,1],[1,2]], [[2,1],[1,2]], [[2,1],[1,2]]),
detG=27.
```

Since K commutes with H, it preserves E. D is the identity on E,
because E is supported on degree-nine vertices. Thus R=(K-D)/2
preserves E. R has integer entries, so it preserves the full lattice
L. Its matrix S in this lattice basis is integral. Symmetry of R gives
**S^t G=G S**. The square equation on E gives

```
(2S+I)^2=21I,       S^2+S-5I=0.                     (5)
```

The polynomial x^2+x-5 is irreducible over Q, with nonsquare
discriminant 21. On the six-dimensional rational space E, (5) therefore
forces characteristic polynomial (x^2+x-5)^3 and **traceS=-3**.
For example, this follows by regarding E as a dimension-three vector
space over Q[x]/(x^2+x-5); each multiplication block has trace -1.

On the other hand, reduce S^tG=GS modulo two. G becomes three
off-diagonal blocks [[0,1],[1,0]]. Symmetry of GS, at coordinates
(2k,2k+1), gives

```
S_(2k,2k) = S_(2k+1,2k+1) mod2     for k=0,1,2.
```

Summing these three pairs makes **traceS even**, contradicting -3.
All 18 square cases are excluded, finishing the conditional theorem.

This obstruction uses the integral lattice, its complete eigenspace,
and an adjacency root. Rational self-adjoint quadratic roots are
compatible with the Gram form: on one Gram block,

```
S0=[[0,5/2],[2,-1]],       S0^t G2=G2 S0,
S0^2+S0=5I,              traceS0=-1.
```

Both programs check this control. It is not integral, exactly as the
trace obstruction requires. No assertion that every square-case H
lacks a rational symmetric root is needed or made.

## 5. Reproduction, separate algorithms and trust boundary

[degree98_two_roots_check.py](degree98_two_roots_check.py) is standalone.
It fills row compositions against column budgets, uses checked integer
Bareiss determinants and integer row reduction with gcd normalization,
and verifies the displayed F identities and full cyclic square on every
form. Every square case receives its own full shifted-matrix rank check.
The complete eigenspace basis, Gram matrix, integral coordinate selectors
and rational odd-trace control are in the compact expected certificate.

[degree98_two_roots_independent.py](degree98_two_roots_independent.py)
imports no author or predecessor program. It enumerates the 300 unordered
perfect-matching pairs, builds F as an edge multiset, reconstructs H by
the separate block formula (4), and uses Fraction Gaussian elimination
and binary-search floor roots. It enumerates all three internal matchings
on each side, hence **2,538 labeled placements**, and checks every full
F and H entry against the primary regenerated matrices:
**1,228,392 entries in each matrix family**. It computes determinants
for all 282 normalized matrices and ranks for all 18 square matrices.

For the same eigenspace the separate program uses the alternative basis
e_first-e_second, e_second-e_last in each triple. Its Gram blocks are
[[2,-1],[-1,2]]. The integral change of basis has determinant one, and
the separate rational rank and determinant checks give dimension six
and Gram determinant 27. This supplies a separate basis and coordinate
audit for the integral-lattice bridge, in addition to the full ranks.

The full-entry audit rejects 18 altered certificates, including missing
forms, matrix weights, determinants, floor roots, full matrix entries,
kernel ranks, nonprimitive basis vectors, Gram entries, odd trace,
quadratic coefficients and rational-root controls. Guards stay active
under Python -O. These are two implementations by the author, without
an asserted independent peer-review verdict for this new theorem.

From repository root, CPython 3.11.2 and the standard library:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_4_7_degree_reductions/degree98_two_roots_check.py \
  --matrices /tmp/book-degree98-two-roots.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_4_7_degree_reductions/degree98_two_roots_independent.py \
  --matrices /tmp/book-degree98-two-roots.json
```

Both programs also run without --matrices, regenerating the proof domain
and checking the compact certificate. The optional full matrices are
generated data, with no omitted proof corpus required by the theorem.
The primary final replay and separate full-entry audit run sequentially
with all numerical threads one; exact times and memory are recorded in
the source provenance of the graph claim. No solver, floating-point
decision, timeout or incomplete domain supplies an exclusion premise.

The final primary replay took 1.159 seconds / 28,388 KiB; the separate
full-entry audit took 6.159 seconds / 27,072 KiB. Compact expected
certificate SHA256:

```
0e59d047dc33e78a75faaf92cb93b2175c38e670a78e71f13a7d83bf174852d5
```

Both programs exactly reproduce the known [21-vertex fixture](baseline21.rows):
93 red edges, degree counts 4/16/1 and page maxima 3/6. This pass freshly
retrieved the primary construction and checked all 441 complemented
entries. The original primary-file SHA256 is

```
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55
```

Twenty-four deterministic degree-preserving signed controls at the
target histogram verify 528 incident identities and 11,616 entries of
K^2. Their defects may be negative. The separate program counts all
monochromatic triangles through each vertex directly. These fixtures
validate arithmetic; they do not select the theorem domain or replace
the written universal identities.

The exact finite determinant and rank computations are premises of
this computer-assisted proof. Saturation, positive-vector decomposition,
normalization, lattice completeness and trace parity are written
mathematics, unformalized. No external graph classification is used
by the conditional (2,20,0) theorem.

## 6. Combined corollary, attribution and primary literature

For an arbitrary valid coloring, the earlier
[global degree theorem](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
graph `bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`,
gives degrees 8..10. The earlier [budget theorem](slack8_remaining.md),
graph `bafkreihwc3dopmdhhn3sedthsjpfuglpgh7t6erutv5jvag6luhgknedpi`,
gives 3n8+n9<=30. At e=98, handshake and total count give
b=24-2a and c=a-2. Nonnegative c forces a>=2; the budget forces a<=6.
The conditional theorem removes a=2 and proves the stated 3..6 list.
The [97-edge theorem](degree97.md), graph
`bafkreiadodqec5yk5g3mdn75jvh6icxx4hz6b76akv2wkaifa4mlta6krm`,
supplies the credited lower edge bound 98. The global degree/count
consequences inherit the named Bussemaker--Cvetkovic--Seidel 1976 and
Doob--Cvetkovic 1979 prerequisites of the minimum-degree/saturation
theorems. Those historical classifications are not replayed here.

The [parity-square review](../book_ramsey_parity_square_review3/REVIEW.md)
and [degree-eleven review](../book_ramsey_degree11_gram_review1/REVIEW.md)
confirm earlier premises. The
[independent 97-boundary review](../book_ramsey_97_boundary_review3/REVIEW.md)
also gives smaller spectral certificates and a classification-free
proof of the lower edge bound. The
[complete first-slack review](../book_ramsey_first_slack_review4/REVIEW.md)
confirms all 53 predecessor forms used by the budget lineage. These
reviews concern earlier results, not this new 282-form theorem.

Primary sources checked live on 2026-10-01:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski, DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
still listing 22<=R(B4,B7)<=23. The
[primary 21-vertex construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is the reproduced baseline, not a new construction. The literature's
general flag-algebra upper certificate was not rerun. Bounded targeted
literature and committed graph checks found no overlapping histogram
exclusion; this does not establish historical priority. Classical
counting, bipartite cycle decomposition, determinant squares and
integral trace parity are credited mechanisms. The quantified increment
is their application to this specific remaining 98-edge histogram.

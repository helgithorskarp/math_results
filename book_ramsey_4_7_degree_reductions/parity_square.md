# Parity defect equality forces a saturated 99-edge degree pattern

Author: **six-books-1**, role **researcher**, 2026-09-30.

**Later refinement:** [saturation.md](saturation.md) excludes the remaining
99-edge equality histogram and proves the universal strict bound
3n8+n9+n11<=32. The next [first-slack exclusion](first_slack.md) removes
three further histograms and gives 3n8+n9<=31 with the current global
degree range8..10. The original argument and its scope follow below.

**Theorem.** Let G be a simple graph on 22 vertices with red-edge
codegrees at most three, blue-edge codegrees at most six, and all
red degrees in **8..10**. Write n9 for the number of degree-nine
vertices and T for the total unused monochromatic spine capacity.
If **2T=n9**, its degree counts are **8:11, 9:0, 10:11**, it has
**99 red edges**, and every spine attains its codegree cap. Moreover
every vertex has exactly **four red neighbors of degree eight**.

**Corollary using the committed global degree theorem.** Every
22-vertex graph under the two book restrictions with **97 red edges**
has degree counts `(n8,n9,n10)` in

    (4,18,0), (5,16,1), (6,14,2),


At **98 red edges**, its degree counts are
`(a,24-2a,a-2)` with **2<=a<=8**. No vertices of other degrees occur
at either edge count. These are necessary possibilities, with no
realizability claim. Both boundaries and the Ramsey gap remain unresolved.

The theorem is a self-contained analytic proof. Its only finite
arithmetic is two displayed three-by-three determinants. It excludes
the whole histograms **8:7,9:12,10:3** at 97 edges and
**8:9,9:6,10:7** at 98 edges. The corollary
additionally uses six-books-3's fresh
[degree 8--11 theorem and degree-eleven edge lower bound](../book_ramsey_b4_b7_degree11_global_cut/PROOF.md).
Books here are ordinary, not induced, subgraphs.

## 1. Parity equality forces a defect matching and three histograms

For a spine ij let F_ij be its unused monochromatic capacity: three
minus its common red count when ij is red, or six minus its common
blue count when ij is blue. Put F_ii=0. Thus F is symmetric,
nonnegative and integral. Write T=sum_{i<j} F_ij and d_i for red degree.

Classical monochromatic-triangle counting gives

    number of monochromatic triangles
      = binomial(22,3) - (1/2) sum_i d_i(21-d_i).

Each nonmonochromatic triangle is counted twice in the sum of mixed
wedges, explaining the factor one half. Summing the spine capacities
and subtracting three times the monochromatic triangle count gives

    T=66-(3/2) sum_i (d_i-10)^2.                    (1)

At a vertex i the incident defect sum is

    (F1)_i=3d_i+6(21-d_i)-2t_i,                    (2)

where t_i counts monochromatic triangles containing i. Hence it has
the parity of d_i. An odd-degree vertex has incident defect at least
one, and an even-degree vertex has nonnegative incident defect.

Write the degree counts as a=n8,b=n9,c=n10. Equations (1),(2) give
`2T=132-3(4a+b)>=b`. Parity equality is equivalent to

    3a+b=33,  a+b+c=22,
    b=33-3a,  c=2a-11.

The handshake lemma makes b even. Nonnegative counts therefore
give exactly three equality candidates:

    (a,b,c)=(7,12,3), (9,6,7), (11,0,11),
    e(G)=97,98,99 respectively.

The incident lower bounds in (2) consume all 2T=b units.
Every degree-nine vertex has defect degree exactly
one, and all other vertices have defect degree zero. Consequently F
is the adjacency matrix of **m=b/2 disjoint pairs on the b
degree-nine vertices**, with all other vertices isolated. This
asserts no color for a defect pair; its capacity can be missed in
either color.

## 2. A universal integer matrix square

Let A be the red adjacency matrix, d=A1, y=10*1-d, Y=diag(y), and
J the all-ones matrix. Common-page counting at a nonedge gives
`c_blue=20-d_i-d_j+(A^2)_ij`. At an edge the red codegree is
`(A^2)_ij`. Including the diagonal yields the exact identity

    A^2=d1^T+1d^T-14J+diag(14-d)
                       +17A-diag(d)A-A diag(d)-F.

Define the symmetric integer matrix

    K=2(A-Y)+3I.

Completing the square in the preceding identity gives, for any
22-vertex graph with F defined as above,

    K^2=25I+24J-4(y1^T+1y^T)+4(Y^2-2Y)-4F.        (3)

The identity is valid even when a graph violates the book caps and
some F entries are negative. Nonnegativity was used only in Section 1.

Here y equals 2 on the degree-eight vertices, 1 on the
degree-nine vertices, and 0 on the degree-ten vertices. Thus
`Y^2-2Y=-E9`, where E9 is the diagonal indicator of degree-nine
vertices. Let H denote the right side of (3). The forced matching F
makes H completely determined up to degree-preserving permutation.
The matrix E9+F consists of m two-by-two all-one blocks.

## 3. The determinant cannot be a square

For either candidate with b>0, decompose the real coordinate space
into the following invariant
subspaces of H:

- Zero-sum vectors on the degree-eight class (dimension a-1), zero-sum
  vectors on the degree-ten class (dimension c-1), and the antisymmetric
  direction within each defect pair (dimension m).
  The rank-two term in (3) vanishes and E9+F kills each vector, so
  **H acts as 25I on their (a+c+m-2)-dimensional direct sum**.
- Vectors constant within each defect pair, supported on the
  degree-nine class, with their m pair coefficients summing to
  zero (dimension m-1). The rank-two term again vanishes; E9+F acts
  as 2I, so **H acts as 17I**.
- Vectors constant on each of the three full degree classes
  (dimension 3). This space is orthogonal to the preceding spaces
  and completes the direct sum.

In the last space, use the three class-indicator vectors. Row sums
into the respective classes give the exact action matrix

    C = [25+8a     12b       16c   ]
        [ 12a    17+16b      20c   ]
        [ 16a      20b     25+24c  ].

It need not be symmetric in this unnormalized basis. The two cases give the matrices

    C97 = [ 81  144   48 ]       C98 = [ 97   72  112 ]
          [ 84  209   60 ]             [108  113  140 ]
          [112  240   97 ]             [144  120  193 ].

    det C97=114177,  det C97 mod17=5,
    det C98=65681,   256^2 <65681<257^2.

The invariant direct sum therefore gives

    det H = 25^(a+c+m-2) * 17^(m-1) * det C.       (4)

For (7,12,3), this is `25^14*17^5*114177`, of 17-adic valuation five,
which is odd. For (9,6,7), it is `25^17*17^2*65681`, a nonzero
integer square factor times a nonsquare integer. Both are nonsquares.
But (3) says H=K^2 for an integer matrix K, so `det H=(det K)^2`
must be an integer square. This excludes both positive-b candidates.

All perfect matchings on the degree-nine vertices are equivalent
under relabeling within that degree class, which preserves y and
conjugates H by a permutation. No enumeration of possible red
graphs, no host symmetry, and no spectral classification is required.

## 4. The remaining equality case is a rigid 99-edge partition

Only (11,0,11) remains. It has n9=0 and T=0, so every spine is
saturated. Here `sum y=22` and `y_i^2=2y_i`. The definition of K gives
`K1=23*1-4y`. Summing (3) over columns, and also evaluating
`K(23*1-4y)`, gives

    8Ay=64*1-8y+4(y squared)=64*1.

Thus `Ay=8*1`. Since y is twice the indicator of the degree-eight
class, every vertex has exactly four red neighbors in that class.
Its induced red graph is four-regular on 11 vertices; the degree-ten
class induces a six-regular red graph on 11 vertices; the cross red
incidence is four-regular on both sides. This is necessary structure,
not a construction or exclusion of the remaining equality case.

Equivalently, for any witness with degrees 8..10 and n9>0,
the usual count inequality `3n8+n9<=33` is strict: **3n8+n9<=32**.

## 5. Consequences at 97 and 98 red edges

The fresh global theorem gives full degrees 8..11, and its Section 6
says a degree-eleven vertex forces at least 106 red edges. Thus a
97-edge witness has only degrees 8,9,10. Write their counts as a,b,c.
At97 edges the vertex and edge counts give

    a+b+c=22,  8a+9b+10c=194,
    b=26-2a,  c=a-4.

The usual parity inequality gives a<=7 and nonnegative c gives a>=4.
Our equality exclusion gives a<=6. At98 edges one instead has
`b=24-2a,c=a-2`; the usual bound gives 2<=a<=9 and our exclusion
improves the upper bound to 8. These corollaries use the committed
global theorem; the parity-equality classification itself does not.

## Exact checks, dependencies and current scope

Run from the repository root with Python **3.11.2**, standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/parity_square_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/parity_square_independent.py
```

The main verifies a full 22-vector invariant basis for each excluded
histogram, its exact rank, every block action, both three-by-three
determinants and the complete equality-histogram arithmetic. Its
[compact expected output](parity_square_expected.json)
includes both matchings, quotients, full forced H matrices, determinants and
valuation. The separate author implementation imports no main code:
it constructs each H through diagonal squared lengths and off-diagonal
page identities, compares all 968 entries, computes both entire
22-by-22 determinants by fraction-free integer elimination with every
division checked, and verifies both the factorization and nonsquareness.
It reconstructs every entry of both C matrices and every histogram. Hashes are
diagnostics, rather than a replacement for the entry comparisons.

The final one-process runs took approximately **0.29 seconds / 16,824 KiB**
for the main and **0.33 seconds / 11,712 KiB** for the separate checker.
All solver/BLAS/OpenMP thread settings were one.

The two implementations also check 96 deterministic 22-vertex controls:
46,464 square-matrix entries, 22,176 literal spine counts and 2,112
incident parity equations. The separate checker counts triangles
literally, independently of the mixed-wedge formula. Controls can
violate book caps and are only algebra checks. No saved corpus,
solver, floating-point decision, timeout or incomplete enumeration
supports the exclusion. The proof uses written, unformalized counting
and invariant-subspace bridges; the two programs are author checks,
not independent peer review or proof-assistant formalization.

The corollary's additional premise is
`bafkreiecuupqvqi52tjsmavr7enyg4fczuvgoy66odpscxyisp4ruwgog4`,
committed at height 7924, source commit
`91c5d953cc5d8a1474f4995b0ac0d4655bb15ce1`. Its degree-eight theorem
uses our earlier uniform-incidence exclusion and its named regular
least-eigenvalue-minus-two classification. That inherited trust
boundary belongs to the corollary alone.

The defect-matching observation at 97 edges was already proved in
six-reviewer-3's [capacity review](../book_ramsey_4_7_capacity_review3/review.md),
committed as `bafkreib3mrljr63wcemeaslba5qnhvgz3wwjwcopakek4g4lgux7kwf4ia`
at height 7592, source `0c809c1604e2c572a43216899ea2a63387014ebc`.
Section 1 rederives it and extends the equality bookkeeping; no novelty
is claimed for that matching observation or classical triangle counting.
The new obstruction is the forced integer matrix square and its
nonsquare determinants, followed by the equality classification.

The current global necessary range is **degrees 8..11, edges 97..112**.
The other boundary histograms, the saturated 99-edge equality case,
and higher-edge witnesses remain unresolved. There is no Ramsey
endpoint decision or historical priority claim.

Primary literature was reopened live 2026-09-30:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
retain the located 22--23 interval. The primary
[21-vertex construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly fetched and exactly reproduced this pass: 93 red edges,
degrees 8:4/9:16/10:1, spine caps 3/6, matrix SHA256
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
This is known baseline validation, not new research. The global upper
certificate is not independently replayed.

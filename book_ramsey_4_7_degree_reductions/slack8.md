# Excluding the 97-edge histogram (5,16,1)

Author: **six-books-1**, role **researcher**, 2026-09-30. The team shares
one signing identity; this identifies the actual author.

## Statements and scope

Let G be a simple graph on 22 vertices with no ordinary B4 subgraph and
with no ordinary B7 subgraph in its complement. Thus a red edge has at
most three common red neighbors and a blue edge at most six common blue
neighbors. The books are not required to be induced.

**Histogram exclusion.** G cannot have five vertices of red degree eight,
sixteen of red degree nine, and one of red degree ten. This is a
97-edge histogram.

Here is the stronger finite matrix statement used to prove the exclusion.
Set

```
d = (8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,10).
```

Let F be any symmetric 22 by 22 matrix of nonnegative integers such that

```
Fii = 0,    sum_{i<j} Fij = 12,    sum_j Fij = di (mod 2).
```

Define the symmetric integer matrix H by

```
Hii = (2di-17)^2 + 4di,
Hij = 4(di+dj-14) - 4Fij          (i != j).
```

**Matrix obstruction.** For every such F, H has no rational symmetric
square root. Up to permutations preserving the degree classes there
are exactly 559 such F. Of these, 558 give positive nonsquare
determinants. The remaining determinant is a square, but a rational
two-dimensional eigenspace gives a sum-of-two-squares obstruction.

Combining the histogram exclusion with the previously established
[first-slack bound](first_slack.md) and the current
[degree-eleven exclusion](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
a hypothetical valid graph with 97 edges must have **(n8,n9,n10)=(4,18,0)**.
This is only a necessary remaining histogram. Neither the whole 97-edge
boundary nor either value of R(B4,B7) is decided here. The conditions
at 98 and 99 edges in first_slack.md remain as previously stated.

The finite matrix theorem and the conditional histogram exclusion use
no external graph classification. The combined statement about all
97-edge graphs inherits the earlier global degree and parity results,
including their explicitly named historical classification dependencies.

## 1. Literal defect and integer square

Write R for red adjacency and di for its row sums. For i != j let Fij
be three minus the number of common red neighbors when ij is red,
or six minus the number of common blue neighbors when ij is blue.
Let Fii=0. Validity gives Fij >= 0.

There are 1,540 triples of vertices. The number M of monochromatic
triangles is

```
M = 1540 - (1/2) sum_i di(21-di),
```

because summing mixed pairs in the neighborhoods counts each
nonmonochromatic triangle twice. Every monochromatic triangle is a
page for three spines. With e red edges, the total unused capacity T is

```
T = sum_{i<j} Fij = 3e + 6(231-e) - 3M
  = 66 - (3/2) sum_i (di-10)^2.
```

The proposed histogram has e=97 and sum(di-10)^2=36, hence T=12.
At vertex i, each monochromatic triangle through i contributes twice
to the incident page count. Therefore

```
sum_j Fij = 3di + 6(21-di) - 2*(monochromatic triangles through i)
         = di (mod 2).
```

For a blue pair, the blue codegree is 20-di-dj+(R^2)ij. Unifying the
two colors gives, for i != j,

```
(R^2)ij = di+dj-14 + (17-di-dj)Rij - Fij.
```

Set K=2R+diag(2di-17). Multiplication now gives K^2=H exactly, with
H as in the statement. In particular K is a symmetric integer square
root. This derivation is also the universal identity in
[parity_square.md](parity_square.md), graph contribution
`bafkreidagwfnpcg6aip47vp6bqfo35ptfacaciwplggiqokuarmcls5zcm`.

It therefore suffices to establish the stronger matrix obstruction.

## 2. Complete normal form, including weighted center edges

Define the incident parity surplus

```
qi = sum_j Fij - (di mod 2).
```

Every qi is a nonnegative even integer, since a nonnegative odd row
sum is at least one. Its total is

```
sum_i qi = 2T - n9 = 24-16 = 8.
```

Call a vertex a center when qi > 0. The positive surplus partition is
one of

```
8;   6+2;   4+4;   4+2+2;   2+2+2+2.
```

Thus there are at most four centers. A center has type (di,qi) and
F-row sum qi+(di mod 2). A noncenter of degree eight or ten has F-row
sum zero and is isolated in F. A noncenter of degree nine has F-row
sum one, so it lies on exactly one unit-weight F edge. Such a vertex
is either a leaf at a center or part of a unit matching with another
noncenter of degree nine. A leaf cannot be shared by two centers.

For a sorted center profile ((d1,q1),...,(dk,qk)), choose all loopless
nonnegative integer weights wij between the centers, with

```
sum_{j!=i} wij <= qi+(di mod 2).
li = qi+(di mod 2) - sum_{j!=i} wij.
```

Exactly li distinct degree-nine leaves must then be attached to
center i. There are 16 minus the number of degree-nine centers
available leaves. We require that sum li not exceed this number and
that the remaining number be even; these remaining vertices are
paired. These conditions are necessary and sufficient for F.

Within each fixed type, center relabelings identify isomorphic weighted
center graphs. No permutation exchanges different (degree,surplus)
types. All choices of the degree-nine leaf labels and the remaining
matching are equivalent under degree-preserving permutations: map
each center's leaf set bijectively and each matching pair bijectively,
then map isolated vertices within each degree class. Conversely an
isomorphism of full F preserves row sums, degrees, and hence center
types, and restricts to an isomorphism of its weighted center graph.
This proves both coverage and uniqueness of the normal forms used
below. It imposes no symmetry on red adjacency R.

The census is:

| Centers | Profiles | Canonical forms | Fixed-type labeled cores | All ordered-type cores |
|---:|---:|---:|---:|---:|
| 1 | 3 | 3 | 3 | 3 |
| 2 | 13 | 53 | 53 | 95 |
| 3 | 13 | 210 | 250 | 1125 |
| 4 | 9 | 293 | 956 | 4590 |
| Total | 38 | 559 | 1262 | 5813 |

The last two columns count weighted graphs on the small center sets,
not all labelings of 22-vertex defect matrices or red graphs. The
fixed-type count is the sum of orbit sizes under permutations of
equal types. Its product with k! divided by the type multiplicity
factorials gives the all ordered-type count.

## 3. Exact determinant certificate

[slack8_check.py](slack8_check.py) enumerates sorted profiles and all
center-edge weight vectors by incident row-budget recursion, taking
one lexicographic minimum under the type-preserving permutations. It
constructs the full 22 by 22 F and H for every normal form. Checked
integer Bareiss elimination computes det H.

[slack8_expected.json](slack8_expected.json) records every one of the
559 cases, including its center profile index, complete center-edge
weight vector, orbit size, determinant, integer square-root floor,
and SHA-256 of the full F/H pair. For each of 558 cases the certificate
checks

```
0 < r^2 < det H < (r+1)^2.
```

These determinants cannot equal the square of a rational determinant:
an integer that is a rational square is an integer square, by clearing
coprime numerator and denominator. Thus these H have no rational
square root, with or without symmetry. No floating-point eigenvalue
or determinant is used.

Exactly one case has square determinant. Its sorted profile is four
centers of type (8,2). In lexicographic pair order
(01,02,03,12,13,23) its weights are

```
(0,0,2,2,0,0).
```

With canonical full vertex labels, its nonzero F edges are weight two
on (0,3) and (1,2), and weight one on

```
(5,6),(7,8),(9,10),(11,12),(13,14),(15,16),(17,18),(19,20).
```

The remaining degree-eight vertex 4 and degree-ten vertex 21 are
F-isolated. The square determinant is

```
det H = 2882721630316266223297119140625
      = 1697857953515625^2.
```

## 4. The exceptional 33-plane forbids a symmetric rational root

Let ei be the standard basis. Direct multiplication by H verifies the
following invariant rational subspaces:

* The two degree-eight pair differences e0-e3 and e1-e2 have eigenvalue 33.
* The eight degree-nine pair differences have eigenvalue 25.
* The seven differences between degree-nine pair sums, together with
  the difference of the two degree-eight pair sums, have eigenvalue 17.
* The four indicators of {0,1,2,3}, {4}, {5,...,20}, {21} have quotient

```
Q = [[49,  8,192,16],
     [32, 33,192,16],
     [48, 12,273,20],
     [64, 16,320,49]].
```

Take the degree-nine pair-sum differences relative to its last pair
(19,20), and order the basis as these displayed spaces. The full
22-vector basis has determinant 16384. Thus the invariant spaces
give a direct sum of dimensions 2+8+8+4=22. Moreover

```
det Q = 2486929 = 1577^2,
det(Q-33I) = -524288 != 0.
```

Consequently the full 33-eigenspace is precisely

```
W = span_Q{e0-e3, e1-e2}.
```

The separate checker additionally verifies rank(H-33I)=20 by exact
rational elimination; it determines dimensions eight for each of the
25- and 17-eigenspaces in the same way.

Suppose S is a rational symmetric matrix with S^2=H. It commutes
with H, so it preserves W. The displayed basis of W has Gram matrix
2I; hence the matrix L of S restricted to W is rational and symmetric,
and L^2=33I. The polynomial x^2-33 is irreducible over Q. The minimal
polynomial of L divides it, and cannot have degree one, so in dimension
two the characteristic polynomial is x^2-33. Thus tr L=0 and

```
L = [[a,b],[b,-a]],     a,b rational,
a^2+b^2 = 33.
```

This equation has no rational solution. Clear denominators to get
coprime integers A,B,C, C != 0, with

```
A^2+B^2 = 33 C^2.
```

Modulo three, the only solution is A=B=0 mod 3. The left side is then
divisible by nine; since 33 is divisible by three exactly once,
C is also divisible by three. This contradicts coprimality. Equivalently,
the checkers list all 27 solutions modulo nine and verify that each
has A,B,C divisible by three. The infinite rational argument is the
coprime-denominator proof just given, not an inference from a bounded
search for rationals.

This rules out the last rational symmetric root and proves the matrix
obstruction and histogram exclusion.

There is also an adjacency-specific trace proof. For an actual
K=2R+diag(2di-17), the restriction trace on W equals

```
(K00-K03) + (K11-K12)
  = -2 - 2(R03+R12) in {-6,-4,-2},
```

contradicting the necessary rational trace zero. Neither proof assigns
a color to either positive F pair. The norm argument is stronger:
it excludes every rational symmetric root. Symmetry matters:
the rational nonsymmetric 2 by 2 matrix [[0,33],[1,0]] squares to 33I,
so the 33-plane alone would not obstruct an unrestricted rational root.

The rational irreducible-eigenspace principle is classical. The prior
[parity-square independent review](../book_ramsey_parity_square_review3/REVIEW.md)
uses it at eigenvalue 17; the new local ingredient here is the exceptional
two-dimensional 33-plane and its rational symmetric norm obstruction.
No novelty claim is made for the sum-of-two-squares criterion itself.

## 5. Independent computation, commands, and trust boundary

[slack8_independent.py](slack8_independent.py) imports no author or
predecessor code. It derives its domain from every ordered positive
composition of four surplus units and every degree-color assignment
to those centers, constrained only by available class counts. It
enumerates center graphs as multisets of unit edges, rather than by
row-budget weight recursion. After checking row demands and the
leaf/matching remainder, it minimizes over all center permutations.
It counts all 5,813 ordered-type cores independently.

The second implementation uses reverse full-vertex labels, then
recovers the normal form from weighted adjacency and incident surplus.
It builds H from the separate literal diagonal/off-diagonal formula
and computes all 559 full determinants with Fraction Gaussian
elimination, and square-root floors by integer binary search. It
compares every certificate field and optionally every F/H entry;
the latter comparison was performed for this publication. There are
559*484=270,556 entries checked in each of F and H. The expected file
does not determine the second implementation's domain.

Both programs are deterministic Python 3 standard-library source,
tested with Python 3.11.2 and one CPU thread. From the repository root:

```bash
python3 -O book_ramsey_4_7_degree_reductions/slack8_check.py
python3 -O book_ramsey_4_7_degree_reductions/slack8_independent.py
```

To reproduce the full entrywise matrix comparison, use a temporary
file outside the source directory:

```bash
python3 -O book_ramsey_4_7_degree_reductions/slack8_check.py --matrices /tmp/books-slack8-matrices.json
python3 -O book_ramsey_4_7_degree_reductions/slack8_independent.py --matrices /tmp/books-slack8-matrices.json
```

The checker reports 38 profiles, 559 forms, 558 positive nonsquare
determinants, one square determinant, no rational symmetric root
survivors, and rank(H-33I)=20 for the exceptional pattern. Its 13
corruption controls reject missing and duplicate cases, altered
weights, orbit sizes, determinants, square-root intervals, matrix
digests, histogram, square-survivor list, eigenspace dimension, primitive
norm residue, adjacency trace and a loop in the full F matrix. Checks
remain active under `-O`.

The generators reproduce the known 21-vertex construction with 93 red
edges, degrees (4,16,1), and red/blue page maxima 3/6. For this pass the
[authors' original matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly fetched; all 441 complemented entries equal baseline21.rows.
This baseline reproduction is validation, not new research.

The exact complete runs used about 1.2 seconds / 29 MiB for generation
and 7.6 seconds / 37 MiB for the separate audit. There was no solver,
timeout, incomplete enumeration, or resource-limit rejection. The
temporary full matrices are generated on demand and are not published.

The compact expected-file SHA-256 is

```
7a1a9bc483f9328c74e29e116b9aaa53f5feb77cbf697eec8a5271cd400eaf22
```

This is an exact computer-assisted exclusion with a written coverage
proof and a written rational square-root obstruction. The coverage
bridge, universal identities, and algebraic reasoning are not formalized
in a proof assistant. Two distinct author implementations agree entry
by entry; that is not an independent peer review of this new claim.

The incoming independent
[degree-eleven review](../book_ramsey_degree11_gram_review1/REVIEW.md)
confirms the inherited global degree exclusion and strengthens its
finite Gram audit, but does not review this 559-form theorem.

## 6. Literature and inherited global context

The primary table in
[Lidicky, McKinley, Pfender and Van Overberghe, arXiv:2407.07285v2](https://arxiv.org/html/2407.07285v2),
Table 1, and
[Radziszowski, Small Ramsey Numbers, DS1.18, April 24, 2026](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
Table IXa, retain 22 <= R(B4,B7) <= 23. The current paper of
[Dai and Lin, arXiv:2606.07214](https://arxiv.org/abs/2606.07214)
concerns diagonal and difference-two regimes; it does not settle this
difference-three parameter. These sources were checked on 2026-09-30.
The upper-bound flag-algebra certificate is not replayed here. This is
context, not a premise of the histogram exclusion or a priority guarantee.

The dependency for the remaining 97-edge histogram is the previously
published first-slack theorem, graph
`bafkreihrh6ngmajbg6zs2wzztlk5g5ywwyyguvnu46eaemree6kj7i6bve`,
which gives 3n8+n9<=31. Together with degree range 8..10 and
2n8+n9=26 at 97 edges, it leaves n8=4 or 5. The latter is excluded here.
The degree range comes from six-books-3's graph
`bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`.
Its lower-degree part inherits the earlier minimum-degree-eight spectral
classification; its new degree-eleven Gram exclusion is exact finite
arithmetic. No prior peer result is silently promoted into a proof of
the new finite matrix statement.

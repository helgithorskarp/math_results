# No 97-edge graph for R(B4,B7)

Actual author: **six-books-1**, role **researcher**, 2026-10-01.
All team members share one signing identity; this identifies the author.

**Conditional histogram theorem.** There is no simple graph G on 22
vertices with four red degrees eight, eighteen red degrees nine, at most
three common red neighbors on every red edge, and at most six common blue
neighbors on every blue edge. Books are ordinary, noninduced subgraphs.

**Combined boundary theorem.** Every ordinary red-B4/blue-B7-free
coloring on 22 vertices has **98 <= e(G) <= 110** red edges and red
degrees **8..10**. The new increment is the exclusion of 97 edges.
The preceding global theorem supplied degrees 8..10 and edges 97..110;
the preceding parity and histogram theorems left only (4,18,0) at 97
edges. These prerequisites are credited in Section 7.

The conditional theorem has a structural proof reducing to four exact
integer matrices. Two cases of a four-vertex graph are contradicted
analytically. The remaining case has four possible weighted defects,
whose forced-square determinants are all nonsquares. The conditional
theorem uses no historical spectral graph classification. Applying it
to the whole boundary inherits the named dependencies of the earlier
global results. No red graph automorphism or connectedness is assumed.

This excludes one edge boundary, not every graph on 22 vertices. The
unrestricted Ramsey endpoint and feasibility at edges 98..110 remain
unresolved. The 98- and 99-edge histogram lists from
[first_slack.md](first_slack.md) are unchanged by this theorem.

## 1. The incident defect counts neighbors in the degree-eight class

Let A be the four degree-eight vertices and B the eighteen degree-nine
vertices. Let R be red adjacency, di its degrees, and s_i the number of
red neighbors of i in A. For i != j put Fij equal to three minus the
red codegree if ij is red, or six minus the blue codegree if ij is blue;
set Fii=0. Validity gives symmetric nonnegative integer F. Write
f_i=sum_j Fij and q_i=f_i-(di mod 2).

Each monochromatic triangle through i contributes twice to incident
pages, so

```
f_i = 3di + 6(21-di) - 2*(monochromatic triangles through i)
    = di (mod 2).
```

Thus q_i is even and nonnegative; an odd nonnegative f_i is at least one.
The universal page identity, proved in
[parity_square.md](parity_square.md), is

```
(R^2)ij = di+dj-14 + (17-di-dj)Rij - Fij       (i != j).
```

Summing this row, using (R^2)ii=di and sum_j dj=2e, gives

```
f_i = 2e-294+38di-di^2-2 sum_{j in N_R(i)} dj.                (1)
```

At this histogram e=(4*8+18*9)/2=97 and the neighbor sum is 9di-s_i.
Consequently

```
f_i = -(di-10)^2 + 2s_i,
s_i = 10-di + q_i/2.                                        (2)
```

The monochromatic triangle identity also gives

```
T = sum_{i<j} Fij = 66 - (3/2) sum_i (di-10)^2 = 15,
sum_i q_i = 2T-n9 = 30-18 = 12.                             (3)
```

For i in A, (2) gives s_i=2 or 3 and q_i=0 or 2. The red graph
G[A] has minimum degree two. Its complement on four vertices has
maximum degree one, so is a matching of size zero, one or two.
Therefore **G[A] is K4, K4-e, or C4**, a complete analytic classification.
For i in B, (2) gives s_i=1+q_i/2>=1. Every vertex of B has a
nonempty red neighbor set T_i in A.

## 2. C4 demands too many cross edges

Suppose G[A]=C4. All four A vertices have q_i=f_i=0. Nonnegative F
therefore vanishes on every spine incident with A, including all pairs
inside A: those spines attain their capacity.

Opposite A vertices have two common red neighbors inside A. For any
blue pair of red degrees eight, the blue codegree is

```
20-8-8+(red codegree) = 4+(red codegree).
```

Saturation at six therefore forces the full red codegree to be two,
leaving no common red neighbor in B. No T_i can contain opposite
vertices of the cycle. Each T_i is thus a singleton or an adjacent pair.

An adjacent A pair has no common red neighbor inside A, and its saturated
red spine needs three in B. Summing over the four cycle edges requires
12 distinct B vertices with two A neighbors: each two-element T_i is
one cycle edge and cannot count for another. All other B vertices have
at least one A neighbor. This demands at least 18+12=30 red cross edges.
The actual count is 4*(8-2)=24. Contradiction.

## 3. K4-e demands too many mixed pairs

Suppose G[A]=K4-e. Let a,b be the missing-edge endpoints and c,d
the other vertices. The local red degrees are 2,2,3,3. Vertices a,b
have f=q=0, so every spine incident with either is saturated.

The blue pair ab has two common red neighbors in A; the same blue
codegree calculation as above leaves none in B. Thus each T_i contains
at most one of a,b.

Each of ac,ad,bc,bd has one common red neighbor in A, and its saturated
red spine needs two in B. Summed, these four pairs require eight mixed
low/high pairs in the T_i. For every nonempty T_i with at most one of
a,b,

```
|T_i intersect {a,b}| * |T_i intersect {c,d}| <= |T_i|-1.       (4)
```

Indeed, if it contains one low vertex this is equality, and if it
contains none its left side is zero. The total right side is the
cross edge count minus |B|, namely

```
(6+6+5+5)-18 = 4.
```

This contradicts the eight mixed pairs required by saturation.

## 4. K4 forces a cycle defect and two exceptional degree-nine vertices

Suppose G[A]=K4. Equation (2) gives f_i=q_i=2 at each A vertex, so
their total surplus is eight. The remaining surplus on B is four.
Since s_i=1+q_i/2 there, exactly one of the following occurs:

* One B vertex has three A neighbors (q=4), with all others having one.
* Two B vertices have two A neighbors each (q=2 each), with all others
  having one.

For each pair i,j in A, its two common red neighbors inside K4 give

```
Fij = 1 - #{b in B : i,j belong to T_b}.                      (5)
```

In the first alternative, the A vertex outside the unique triple T_b
has three unit F edges to the triple. Its F-row sum would be at least
three, contradicting f_i=2.

In the second alternative, repeated pair subsets would give a negative
F entry by (5). If the two pairs are distinct but intersect, the A
vertex in neither again has three unit F edges and row sum at least
three. Thus the two pairs are disjoint. Equation (5) now forces F[A]
to be the unit C4 complementary to that matching. Each A row already
has weight two inside A, so nonnegativity and f_i=2 give **F[A,B]=0**.

The two exceptional B vertices have F-row sum three; all other sixteen
B vertices have row sum one. Every normal B vertex is therefore a
unit leaf at a center or a unit matching endpoint. Leaves are distinct
because their full F-row sums are one. If w is the weight between the
two centers, w is one of 0,1,2,3. Each center has 3-w unit leaves,
and the remaining 10+2w normal vertices are paired.

This leaves exactly four necessary full F normal forms. Any unit C4
on A is equivalent by an A permutation. Map the two centers, their
leaf sets and the remaining matching pairs by B permutations. These
operations preserve red degree classes. No red host symmetry is
assumed: they relabel the whole hypothetical graph, including its R.
Additional red-edge constraints can only remove forms; this proof does
not assert that any of the four defects has a red host.

## 5. Four nonsquare forced determinants

As in the universal integer-square identity, set

```
K = 2R+diag(2di-17).
```

The page identity in Section 1 cancels all off-diagonal R terms in
K^2, yielding

```
H=K^2,
Hii=(2di-17)^2+4di,
Hij=4(di+dj-14)-4Fij                  (i != j).               (6)
```

We use canonical A labels 0..3 and B labels 4..21. Put unit F edges
on 02,03,12,13, weight w on 45, attach 3-w leaves to each center in
increasing normal B order, then pair the remainder. All four complete
F and H matrices are in [degree97_expected.json](degree97_expected.json).

| w | det H | Floor square root | Prime p | det H modulo p |
|---:|---:|---:|---:|---:|
| 0 | 2453979450761782305084228515625 | 1566518257398164 | 13 | 5 |
| 1 | 2462234694611000055084228515625 | 1569150947044611 | 23 | 14 |
| 2 | 2269429095100456729888916015625 | 1506462443972785 | 23 | 7 |
| 3 | 1897297029307302188873291015625 | 1377424055731314 | 23 | 15 |

For each row, the checker verifies the determinant is strictly between
the square of the displayed integer and that of its successor. There
is also a smaller nonsquare certificate: the quadratic residues are

```
mod 13: {0,1,3,4,9,10,12},
mod 23: {0,1,2,3,4,6,8,9,12,13,16,18}.
```

None contains the corresponding determinant residue. Thus det H is
not an integer square, contradicting det H=(det K)^2. In fact none
of these four H has any rational square root: an integer that is a
rational square is an integer square, by clearing coprime numerator
and denominator. This completes the conditional histogram theorem.

## 6. Exact checks and reproducibility

The computation premise is the exact nonsquare determinant of these
four matrices. Sections 1--4 are written algebra and counting proofs;
their finite checks are validation of those arguments, not substitutes
for the coverage proof.

[degree97_check.py](degree97_check.py) imports no predecessor program.
It checks all 64 four-vertex adjacency masks, leaving ten minimum-degree
two graphs (3 C4, 6 K4-e, 1 K4). It checks the eight allowed C4 subsets,
eleven K4-e subsets and all 25 K4 exceptional patterns (four triples
plus 21 unordered pair multisets). It constructs the four full F/H
matrices and uses integer Bareiss with checked exact divisions.

[degree97_independent.py](degree97_independent.py) imports no author
or predecessor program. It constructs the local graphs by complement
matchings and the allowed neighbor subsets by separate constructions.
It enumerates 40 ordered K4 patterns (four triples and 36 ordered pair
choices), comparing every normalized pattern and local F entry. For
the final matrices it uses all three A cycles, every one of 153 labeled
B center pairs, and all four center weights: **1,836 placements**.
Reverse leaf/matching labels are normalized from weighted adjacency;
every full F/H entry is compared across all placements and to the four
expected matrices. The expected certificate does not choose this domain.
There are **888,624 full entries per matrix family** across the placements.

The separate program computes full determinants with exact Fraction
Gaussian elimination, roots by integer binary search, and determinant
residues independently by finite-field Gaussian elimination. All four
records and all local records agree. It rejects 12 corrupted certificates,
including missing/duplicate cases, altered full F/H entries, determinant,
root, residue, modulus, local graph, column survivor, incidence budget
and signed control mask. Checks remain active under Python `-O`.

Both programs check 24 deterministic degree-preserving controls with
the literal (4,18,0) histogram. They may violate books and have signed
defects. Their 528 incident row identities and 11,616 full square entries
are checked against literal pages. The main uses neighbor intersections;
the separate checker uses row products, explicit blue pages and all
monochromatic triangles through each vertex. The recorded red masks
are validation fixtures, not inputs to the four-case theorem domain.

Both reproduce the known 21-vertex construction: 93 red edges,
degrees (4,16,1), and red/blue page maxima 3/6. The original primary
matrix was freshly fetched for this pass and all 441 complemented
entries matched [baseline21.rows](baseline21.rows). Its original-file
SHA-256 remains

```
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55
```

This is known baseline validation, not a new construction.

Python 3.11 or later, standard library only, tested with CPython 3.11.2.
From the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_4_7_degree_reductions/degree97_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_4_7_degree_reductions/degree97_independent.py
```

The main complete replay used 0.581 seconds / 20,512 KiB;
the separate replay used 1.015 seconds / 21,744 KiB. Jobs were sequential,
all numerical thread counts one, with no solver, timeout, incomplete
domain, floating arithmetic or resource-limit rejection.

The compact certificate has SHA-256

```
cee8ae2ba1bdcdbd6fd1eb0ffe33edcf43b0f4acbc13b7875ea5bb3e808381e0
```

This is an exact computer-assisted theorem with written coverage and
decoding proofs. These bridges are not proof-assistant formalized.
The two implementations belong to the same researcher and are not an
independent peer-review verdict on this new boundary theorem.
No large corpus or external solver input is required or published.

## 7. Combined boundary, dependencies and primary literature

The prior [degree theorem](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
graph `bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`,
gives degrees 8..10 and edges 97..110. Its new degree-eleven proof is
exact finite Gram arithmetic; the inherited minimum-degree-eight part
uses the earlier degree-seven exclusion and its named spectral
classification dependency. Its
[independent review](../book_ramsey_degree11_gram_review1/REVIEW.md),
graph `bafkreibor5a5i6qhsljhbabkuqgahgoy5ou3ts6gpnw27sexbiwtizzm2m`,
confirms and strengthens the degree-eleven finite obstruction. Neither
the historical classification nor that peer computation is replayed here.

At 97 edges, write (a,b,c)=(n8,n9,n10). Then

```
a+b+c=22,       2a+b=26.
```

The [first-slack theorem](first_slack.md), graph
`bafkreihrh6ngmajbg6zs2wzztlk5g5ywwyyguvnu46eaemree6kj7i6bve`,
gives 3a+b<=31, so 4<=a<=5. Thus only (4,18,0) or (5,16,1) remained.
The [last histogram exclusion](slack8.md), graph
`bafkreiazubi5xvgjefre2trbr5nhtlgpxng34fyy5lbwpm7b2xrpphg2xy`,
excludes (5,16,1). The conditional theorem here excludes (4,18,0),
therefore excludes the entire 97-edge boundary. The upper edge bound110
and degree range are credited premises, not claimed new increments.
The necessary four-histogram classification at 97 edges was also
proved in the [independent capacity review](../book_ramsey_4_7_capacity_review3/review.md),
graph `bafkreib3mrljr63wcemeaslba5qnhvgz3wwjwcopakek4g4lgux7kwf4ia`;
its exact-endpoint degree argument is elementary. The histogram exclusions
credited above and proved here supply the further boundary obstruction.
The universal square and row identities are credited to
[parity_square.md](parity_square.md), graph
`bafkreidagwfnpcg6aip47vp6bqfo35ptfacaciwplggiqokuarmcls5zcm`.
The first-slack theorem also inherits the earlier saturation result;
all transitive historical classification dependencies remain explicit
for the combined statement, while absent from the new conditional proof.

Primary tables were checked live on 2026-09-30 and again on 2026-10-01:
[Lidicky, McKinley, Pfender and Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski, DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
retain 22 <= R(B4,B7) <= 23. The later
[Dai--Lin paper](https://arxiv.org/abs/2606.07214) concerns diagonal and
difference-two regimes. The
[primary authors' construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is the verified baseline above. Candidate-specific searches are not
a guarantee of historical priority. No novelty is claimed for the
triangle identity, determinant obstruction or modular nonsquare test.
The increment is this conditional structural proof and its application
to exclude the entire lower edge boundary. The general flag-algebra
upper-bound certificate is literature context and was not rerun.

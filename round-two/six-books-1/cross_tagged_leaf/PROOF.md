# Closing the cross-repeated specified leaf with known-edge red books

Actual author **six-books-1**, role **researcher**, 2026-10-02.
Campaign signatures share one identity; they do not identify independent authors.

A valid graph is a simple red graph on22 vertices with at most three common
red neighbors on each red edge and at most six common blue neighbors on each
blue pair. Blue is the complement on distinct vertices. Books are ordinary
subgraphs; page-to-page edges are unrestricted. All degrees below are red.

**Main theorem.** Suppose a valid graph has degree multiset9^4,10^18.
Let u have degree ten and this induced labeled red neighborhood. Its mark0=a
has global degree nine and its other nine points have global degree ten:

```text
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

Put v=1, X=N(u) minus {v,a}, Y=N(v) minus {u,a}, and let T be the
remaining three points. Put S_X=N(a) intersect X and S_Y=N(a) intersect Y.
The repeated omission among the four special-to-T rows cannot consist
of one S_X point and one S_Y point.

**Secondary corollary.** Under the same global degree model, this specified
one-nine leaf cannot occur at any degree-ten vertex. This additionally imports
the Y-repeated exclusion
[9327](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/caseI_tagged_leaf/PROOF.md)
and X-repeated exclusion
[9381](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/caseII_tagged_leaf/PROOF.md).
The pair theorem9131 partitions its36 labeled omission cores into six
Y-repeated, six X-repeated and24 cross-repeated cores. These three exclusions
therefore exhaust the cores for this specified leaf.

The new theorem is an exact computer-assisted structural exclusion. Distinct
implementations by the same author regenerate the entire same mathematical
record. The ordinary reductions, normalization, finite completeness and
code-to-statement bridges below are unformalized. Independent review of the
new cross theorem is pending. Other neighborhoods, other global multisets,
arbitrary108-edge hosts and the Ramsey endpoint remain outside its scope.

## 1. Ordinary structure and cross normalization

Use coordinates u,v,a,X0..X5,SX0,SX1,SY0,SY1,T0,T1,T2,Y0..Y5, numbered0..21
in that order. Ordinary X and ordinary Y mean the six Xi and six Yi points.
Old neighborhood labels2..7 become X0..X5; labels8,9 become SX0,SX1.
The specified neighborhood gives

```text
ordinary X cycle: X0--X4--X3--X1--X2--X5--X0;
SX0 own pair: {X3,X5};  SX1 own pair: {X2,X4}.
```

The sole common red page of uv is a. The ordinary pair theorem
[9131](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/single_page_pairs/PROOF.md),
`bafkreiesfsfe44lvytykz4oczwidosjpdxf4g3imjfnw7pxdllkmqsfqwu`, gives
|X|=|Y|=8, |T|=3, |S_X|=|S_Y|=2, all three a--T edges, independence
of S_X union S_Y and of T, and exactly two own-block and two T neighbors
for each special. The omission multiplicities are2,1,1. These statements
do not prescribe or classify the neighborhood at v.

Let r be the repeated SX index, retained as either0 or1. Label the repeated
SY point SY0 and the common omitted T point T0. Label the other SX omission
T1 and the other SY omission T2. With bit t meaning red to Tt, the masks are

```text
r=0: SX0=6, SX1=5;   r=1: SX0=5, SX1=6;
both: SY0=6, SY1=3.
```

This only relabels unnamed SY and T points; both actual SX choices remain.
No host or displayed-leaf symmetry is assumed. There are2*2*3*2=24
original labeled cross cores. The two normalized r choices cover them all
by these relabelings, which also transport every individual degree tag.

## 2. Four-regularity and the T cover

The multiset gives108 edges. The ten degrees in N(u) sum to99, its local
graph has13 edges, and its cut into B_u=N_B(u) has99-10-26=63 red edges.
Thus e(G[B_u])=108-10-13-63=22. For each blue ub pair its common blue
count is10-d_(G[B_u])(b). All eleven B_u local degrees are at least four;
their degree sum44 forces four-regularity. This ordinary bridge is rederived
and credited to
[review9105](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md).

B_u consists of SY,T and ordinary Y. Each T has four neighbors in whole Y;
its SY incidence ranks are1,2,1, so its ordinary-Y ranks are **3,2,3**.
Each SY has two own ordinary-Y neighbors. Each SX has four ordinary-Y
neighbors from its specified global degree ten. Whole Y has10 internal
edges, four incident to SY; ordinary Y has six internal edges. The last
six-edge fact is not needed to enumerate any internal-Y graph here.

For y in ordinary Y let t_y count its T neighbors. The red vy spine has
exactly4-t_y common red pages: v meets every SY and ordinary Y and no T.
Its cap gives t_y>=1. Thus the three T ordinary-Y rows must cover all six
ordinary Y points.

## 3. All actual degree tags and row budgets

Only a is low in {u} union N(u). The other three degree-nine points lie
in the eleven points of B_u. Preserve flags

```text
l=(l_T0,l_T1,l_T2,l_SY0,l_SY1),  m=sum(l)<=3.
```

There are26 flag words. For each choose3-m of the six ordinary Y points
to be low, giving sum_l binomial(6,3-m)=binomial(11,3)=165 placements
per normalized r core. Initially forgetting these six-point low locations
is a necessary overapproximation; the final join recovers their actual tags.
It does not identify arbitrary tag locations as equivalent host colorings.

Let c_i be Xi's T mask and write g_i=popcount(c_i),
M=(2,2,1,1,1,1), and k_i=g_i-M_i>=0. Inside whole X, X0,X1 have
degree2 and the other four have degree3. The exact blue vXi count is
10-d_(G[X])(Xi)-g_i, giving these minimum T ranks.

Subtract the mark edge, SX incidence rank and four whole-Y edges from
each actual T degree. The ordinary-X ranks and excess sum are

```text
(4-l_T0,4-l_T1,3-l_T2),   sum(k)=3-l_T0-l_T1-l_T2.
```

Each SY ordinary-X cross row has rank4-l_SY after subtracting its root,
mark, two T and two own-Y neighbors.

The degrees in N(a) sum to90-m; its local graph has13 edges. Its cut is
55-m and e(G[B_a])=31+m, where B_a is ordinary X union ordinary Y.
Both ordinary blocks have six edges, leaving a mutual red cut of19+m.
For blue aXi the common blue count11-d_(G[B_a])(Xi) forces local degree
at least5. Put beta_i=d_(G[B_a])(Xi)-5. Xi's ordinary-Y row has rank
3+beta_i, since its ordinary-X degree is two. If s_i counts its SY
incidences, its exact global degree equation gives

```text
s_i+k_i+beta_i=2;  0<=beta_i<=2;  sum(beta)=1+m.
```

No fixed T row or degree tag from the closed same-side cases is imposed.
The earlier
[9281 isolated-mark reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/isolated_leaf_mark/PROOF.md)
is credited context, not an input to the finite domain.

## 4. Complete X projection

Let K be the16 points outside Q=ordinary Y. Its edges are fixed by the
leaf, core, T masks and SY cross rows. Its Q row ranks are

```text
u:0, v:6, a:0, Xi:3+beta_i, SX:4, SY:2, T:3,2,3.
```

For a K pair ij let c_K be its common red count inside K. The necessary
lower bound c_K+max(0,q_i+q_j-6) is at most3 for red pairs and at most
d(i)+d(j)-14 for blue pairs. Only for blue pairs we use
c_B=20-d(i)-d(j)+c_R. All actual flagged endpoint degrees are retained.

[derive.py](derive.py) enumerates both r choices, all26 flags, all T subsets
of the stated ranks and both SY cross subsets of their actual ranks. It
uses these early necessary red tests before checking all120 K pairs:

```text
popcount(c_i intersect c_j)<=min(2,k_i+k_j) on each X cycle edge;
popcount(c_SX intersect c_i)<=min(2,1+k_i) on each SX--own-X edge.
```

For the first, whole-Y rows of Xi,Xj have ranks5-k_i,5-k_j on eight
points and u is a further common red page. For the second, the SX whole-Y
rank is4 and Xi's is5-k_i, again with page u. Ignoring other pages weakens
these tests; the actual SX mask6 or5 is used.

[verify.py](verify.py) independently starts from all38416 minimum-rank
T-column words per r, infers actual T flags, and starts from all4096 SY
column words,1225 of which have both ranks3 or4. It checks literal colored
intersections on14 known points with eight omitted points, then16 points
with six omitted. Its blue bound uses common blue points inside the known
set plus max(0,6-q_i-q_j), rather than the producer's red/degree identity.
It separately verifies the exact rank and cut bridges.

Both retain exactly **836** X interfaces,418 per r, matching every interface
and every actual tag record. The sorted full X-domain SHA256 is
`fa7d77736174b810552241296e9b70a94c42d3579336fed24402b80ad598d5be`.
These necessary interfaces are not full graph witnesses.

## 5. Lossless SX frames and all Y endpoints

The two SX Q four-sets A,B have a blue spine with three known common red
points u,a,T2. Both endpoints have degree ten, giving |A intersect B|<=3;
six-point cardinality gives |A intersect B|>=2. The two ordered prototypes are

```text
A=15={0,1,2,3}, B=51={0,1,4,5}: intersection2;
A=15={0,1,2,3}, B=23={0,1,2,4}: intersection3.
```

Every ordered pair of the same intersection size is transported to the
prototype by matching the four membership cells A intersect B, A minus B,
B minus A and the remaining points. All other Q incidences, tags and
unknown edges travel with this permutation. No Q labels or tags were fixed
beforehand. Independent controls enumerate all720 permutations of each
prototype and recover all90 and120 distinct ordered pairs, respectively.
Equal four-sets violate the blue SX spine; no other type is possible.

For every X interface and prototype enumerate all T Q rows of sizes3,2,3
retaining their Q cover and all SX--T and T--T caps. Enumerate both SY Q
two-sets and check all SX--SY, SY--T and SY--SY caps. All21 pairs of the
seven SX/SY/T endpoints are checked. The producer uses c_K plus outside
intersections. The checker completes the entire22-point colored neighborhoods
of these endpoints and counts literal red and blue pages. Its T triples
are transposed from all7^6 nonzero column words and their exact3,2,3 ranks.
Exactly **52,664** normalized endpoint frames remain. No internal-Y graph
enumeration or graphical-degree filter is required.

## 6. Complete row joins and actual Y tags

For each endpoint frame enumerate every Q subset of rank3+beta_i for Xi,
retaining all seven Xi--endpoint caps. Exactly **4,500** frames have nonempty
candidate sets for all six Xi. The producer checks exact intersection
budgets; the checker uses each candidate's complete colored neighborhoods.
Caching these fixed neighborhoods changes no candidate domain.

Enumerate every joint row choice and check all15 Xi--Xj caps. The producer
recurses in increasing candidate-count order and prunes impossible column
upper/lower bounds. The checker instead traverses the entire Cartesian
products, **2,018,064** row tuples, using literal colored compatibility tables.

For y in Q let b_y be its SX incidence count and z_y its ordinary-X column
rank. Four-regularity of B_u gives the exact global equation d(y)=5+b_y+z_y:
one neighbor is v and four are in B_u. Columns therefore have rank5-b_y
for high points or4-b_y for low points, with exactly3-m low columns. This
recovers all previously forgotten tag locations. The checker independently
adds the point's known outside degree and required B_u internal degree.

Exactly **192** joint interfaces remain. Every one has

```text
(l_T0,l_T1,l_T2,l_SY0,l_SY1)=(0,0,1,1,1),
and all ordinary Y points have global degree ten.
```

This is a complete-census output, never an assumed endpoint condition.

## 7. Known-edge red books finish every join

All K and K--Q edges are now assigned; Q internal edges remain entirely
unspecified. Each of the192 partial red graphs already contains a red spine
with four distinct common red pages. [EXPECTED.json](EXPECTED.json) gives
one lexicographically first spine and four lowest pages for each sorted join.
Both engines reconstruct every partial graph and check all nine required
book edges. No internal-Q edge is assigned or used in a witness.

For example, the first sorted join has Xi Q rows(21,22,45,57,46,58),
SX rows(15,51), SY rows(24,48), and T rows(13,3,52). Its red spine
X3--Y3 has common red pages X4,SX0,SY0,T0, at coordinates7,9,11,13.
The entire192-witness inventory, not this example alone, closes the domain.
Page-to-page colors and unknown Q edges cannot destroy an ordinary B4.
Every hypothetical valid cross graph maps through the necessary projections
to such a join, contradicting its red cap and proving the main theorem.

## 8. Reproduction, literature and trust

[reproduce.py](reproduce.py), explained in [README.md](README.md), regenerates
both engines in normal and optimized modes and compares the **entire**
1,556,203-byte mathematical record byte-for-byte. Its whole SHA256 is
`8b39a65ce59cb832f1bd4f07b615fa2f2c3d43e625681a98ba5be041e180d4a4`.
Intermediate inventories are regenerated into scratch, not supplied as an
opaque corpus. The11888-byte compact fixture predates the standalone cold
replays; its SHA256 is
`754ad4ac9083582191554e5b8fa0db5add48be7314aab86844448240c77cd34c`.
Checksums alone do not establish completeness.

Fresh self-tests first match the frozen fixture, then reject16 whole-record,
schema, scope, domain, tag and witness damages with counts/hashes repaired.
They also check4096 subset minima and1440 SX transports. Actual measurements
are in [provenance.json](provenance.json). One intensive child runs at a time,
all numerical threads are one, and the scope remains1CPU/2GiB. Program
guards are30 seconds per complete X flag in the producer, per r in the
checker's X stage, and per subsequent stage; wrapper child guards are90 seconds.
The first uncached checker hit its row-stage guard and supplied no completed
verification. Precomputing unchanged neighborhoods removed duplicate work
under the same limits. No guard failure is treated as an exclusion.

The main dependency is9131. The full-leaf corollary additionally imports
9327 and9381 in their shared explicit degree model. Independent
[review9414](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/x-repeated-leaf-audit/REVIEW.md),
`bafkreibfuwpcdg7ifqkupycjbywe3lq7kwmqmm3knxummn2kxjpimwfzzu`, confirms9381
and strengthens that CaseII theorem to E<=108 with arbitrary outside degrees.
Its verdict and edge-only extension do not transfer to cross or CaseI.
Earlier [9197](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/degree9_cycle_saturation/PROOF.md)
and [review9247](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/degree-nine-audit/REVIEW.md)
retain credit for the cycle/leaf frontier. Rootless incidence theorem
[9371](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/three-root-incidence108/PROOF.md)
is complementary context; rootlessness and an exact one-nine-root count
are not premises of the new result.

The live2025 [journal Table1](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v32i4p64/pdf/)
and [arXiv version](https://arxiv.org/pdf/2407.07285) were reopened2026-10-02
and retain22<=R(B4,B7)<=23. The published
[21-point matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is exactly reproduced with93 red edges,117 blue pairs and page maxima3/6.
Off-diagonal0 is red and1 is blue; search metadata follows its leading JSON
matrix. This is prior-art validation, not a new construction. The upper23
flag certificate is not independently replayed. No exclusive historical
priority or complete-literature claim is made.

Finite completeness, ordinary normalization/degree reductions, exact CPython
arithmetic and code-to-statement correspondence remain trust inputs and
unformalized. Separate same-author algorithms are not independent peer review.
The secondary corollary closes only this specified leaf in9^4,10^18; other
leaves, weaker global hypotheses and the Ramsey endpoint remain open.

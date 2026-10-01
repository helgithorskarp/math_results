# Three low roots at the 98-edge Book Ramsey boundary

Actual author **six-books-1**, role **researcher**, 2026-10-01.

A red graph on22 vertices is valid when every red edge has at most
three common red neighbors and every blue complement-edge has at most
six common blue neighbors. These are the ordinary, non-induced
red-B4 and blue-B7 restrictions.

**Conditional theorem.** Suppose a valid graph has exactly three
red-degree-eight vertices A, eighteen degree-nine vertices B, and one
degree-ten vertex z. Then **A induces a red triangle and all three A-z
edges are blue**. The histogram(3,18,1), with98 red edges, remains open.

The new finite lemma excludes the case in which A is a triangle and
z has exactly one red A-neighbor. Written incidence arguments exclude
both path cases and the triangle cases with two or three red z edges.
The sole remaining local root shape is the triangle with zero red
z edges. No host automorphism, equitable partition, construction,
full98-edge exclusion or Ramsey endpoint resolution is claimed.

## Incident identity and the six root classes

For distinct vertices define the nonnegative, symmetric, zero-diagonal
integer defect matrix F by

```
F_ij=3-|N_R(i) intersect N_R(j)|       on red pairs,
F_ij=6-|N_B(i) intersect N_B(j)|       on blue pairs.
```

Write f_i=sum_j F_ij, d_i=d_R(i), sA_i=|N_R(i) intersect A|, and
epsilon_i=1 if iz is red, zero otherwise (epsilon_z=0).
The universal [incident identity](parity_square.md), here also derived
directly, specializes to

```
f_i=2e-294+38d_i-d_i^2-2 sum_(j in N_R(i))d_j
   =2-(d_i-10)^2+2(sA_i-epsilon_i),       e=98.
```

Indeed, let t_R,t_B count the red and blue triangles through i.
Then f_i=3d_i+6(21-d_i)-2(t_R+t_B). Counting edges between its red
and blue neighborhoods gives
t_R+t_B=binom(21-d_i,2)-e+sum_(j in N_R(i))d_j.
The displayed identity follows. Since that neighbor-degree sum is
9d_i-sA_i+epsilon_i, its specialization requires no external degree
classification.

Parity gives f_i=d_i modulo2. Put q_i=f_i-(d_i mod2), a nonnegative
even integer. The degree-square sum is1750, so summing the incident
identity gives sum f_i=42 and sum q_i=24. At A,
f_i=-2+2(sA_i-epsilon_i)>=0. Thus each A point has at least one
A-neighbor; G[A] is P3 or K3. A path endpoint cannot meet z.
At B,

```
q_i=2(sA_i-epsilon_i)>=0.
```

Consequently every red z-neighbor in B has an A-neighbor. The64
simple graphs on A union{z} leave14 labeled masks, in six classes
under the six A permutations. If k=e_R(z,A), the totals are:

| A shape | k | sum q_A | q_z | sum q_B | conclusion |
|---|---:|---:|---:|---:|---|
| P3 | 0 | 2 | 2 | 20 | impossible |
| P3 | 1 | 0 | 4 | 20 | impossible |
| K3 | 0 | 6 | 2 | 16 | remaining necessary shape |
| K3 | 1 | 4 | 4 | 16 | impossible by the finite lemma below |
| K3 | 2 | 2 | 6 | 16 | impossible |
| K3 | 3 | 0 | 8 | 16 | impossible |

## The path and the two larger triangle attachments

For P3 write a,b,c for the path, middle b, and epsilon=R_bz.
The endpoint F rows vanish. The blue pair ac has red codegree2;
b supplies one common neighbor. Their seven-point B-neighbor sets
therefore intersect in a single point C. The only-a and only-c
classes X,Y have size6 each; the neither class Z has size5.

The saturated red ab,bc pairs each have three common neighbors, all
in B. If gamma records whether b meets C, then its B-neighbor count
6-epsilon and its union count6-gamma give

```
|N_R(b) intersect Z|=gamma-epsilon<=1-epsilon.
```

The blue endpoint-z pairs have zero defect and red codegree4, since
their degree sum is18. The middle root b supplies epsilon of those
common neighbors, so each B-intersection has size4-epsilon. If rho
records whether z meets C, then z has10-epsilon B-neighbors and
8-2epsilon-rho in the union. Thus

```
|N_R(z) intersect Z|=2+epsilon+rho>=2+epsilon.
```

At a B vertex in Z, its only possible A-neighbor is b. Nonnegative
q forces its adjacency to z to imply adjacency to b, so the second
set is contained in the first. Their sizes contradict this containment.
This excludes both path classes.

For a triangle with k=2, let a,b be attached to z and c not attached.
The a,b F rows vanish. Each has five B-neighbors. The saturated
ab pair has common neighbors c,z and exactly one B point C. The
only-a/only-b classes have size4 each and the neither class Z size9.
The saturated ac,bc pairs each have two common B-neighbors: their
other common neighbor is the other attached A root. If gamma is
adjacency of c to C, its six B-neighbors give

```
|N_R(c) intersect Z|=2+gamma<=3.
```

The saturated az,bz pairs also have two common B-neighbors, the
other attached root supplying the third. If rho is adjacency of z
to C, its eight B-neighbors give

```
|N_R(z) intersect Z|=4+rho>=4.
```

Nonnegative q in Z requires the latter set to lie in the former.
Hence k=2 is impossible.

For k=3 all three A F rows vanish. Each saturated A-z spine has
the other two A vertices as common neighbors and exactly one common
B-neighbor. Summing over the three spines gives
sum_(i in N_R(z) intersect B)sA_i=3. There are seven red B-neighbors
of z, each with sA_i>=1, contradicting that sum. This excludes k=3.
The two programs separately check the64-mask census and all six path
and four k=2 parameter states, as well as the k=3 bound3<7.

## The one-edge triangle: a cubic neighborhood and one outside defect

Now let A={a,b,c} be a triangle, with az red and bz,cz blue.
Then F_a=0, f_b=f_c=2, f_z=4. Put

```
N=N_R(a)={b,c,z} union U,       |U|=5,
V=N_B(a),                     |V|=13,
J=G[N], W=G[V],
M_(v,x)=R_vx,                 v in V, x in N.
```

Every red a-x spine is saturated, so J is cubic. Every blue a-v
spine is saturated; since d_a+d_v=17, its red codegree is3.
Thus every M row has weight3. Its column sums, in b,c,z,U order, are

```
r=(4,4,6,5,5,5,5,5),          r_x=d_x-4.
```

All V points have degree9 and no red edge to a, so W is six-regular.
For v in V put delta_v=M_vb+M_vc-M_vz. Nonnegative q gives delta_v>=0
and f_v=1+2delta_v. We next use the cross codegrees to get a stronger
constraint than that pointwise inequality.

For x in N, v in V, their full red codegree is
(JM^T+M^T W)_(x,v). On a red pair it equals3-F_xv; on a blue pair
it equals d_x-5-F_xv. Equivalently,

```
(JM^T+M^T W)_(x,v)
    =(d_x-5)+(8-d_x)M_vx-F_xv.
```

Sum over x. Cubicity gives9 from JM^T, and the row-weight-three
and six-regular conditions give18 from M^T W. On the right,
sum_x(d_x-5)=31 and sum_x(8-d_x)M_vx=-3+delta_v. Therefore

```
sum_(x in N) F_vx=1+delta_v,
sum_(w in V) F_vw=delta_v.
```

The latter row sums total r_b+r_c-r_z=4+4-6=2. A loopless symmetric
nonnegative integer matrix with degree sum2 is precisely one unit
edge. Hence F[V] is one unit edge, and **every delta_v is0 or1,
with exactly two delta_v=1 points**.

The possible b,c,z incidence patterns are000,100,010,101,011,111.
In particular110 and001 are excluded. Let t count111 rows and p,q
count100,010 rows. The column sums force

```
t in{0,1,2},  p+q=2-t,
(n000,n100,n010,n101,n011,n111)
       =(5+t,p,q,4-p-t,4-q-t,t).
```

There are six labeled root-count profiles. Across all eight columns,
the eligible binary rows are the **41 three-subsets** with
0<=1_b+1_c-1_z<=1. These are necessary rows only; no exterior graph
is assumed to exist.

## Exact pair capacities and complete finite coverage

Let E=F[N] and S=M^T M. Let a_xy denote the number of common J-neighbors.
The root a supplies one common red neighbor of every pair x,y in N.
Thus

```
S_xx=d_x-4,
S_xy=(2 on red J pairs, d_x+d_y-15 on blue J pairs)-a_xy-E_xy.
```

Let S0 be the expression before subtracting E. All its off-diagonal
entries are capacities for nonnegative E and binary Gram entries.
The M row weights imply S*1=3*diag(S). Hence the degrees of E are

```
sum_y E_xy=sum_y(S0)_xy-3(d_x-4)
          =d_x+19-sum_(y in N_J(x))d_y.
```

In b,c,z,U order these are

```
(1,1,2, 1+J_ub+J_uc-J_uz for u in U),
```

and their sum is10: **five weighted defect edges**, with multiplicity.
Only nonnegativity, these degrees, and E_xy<=(S0)_xy are used.

The [primary program](degree98_three_roots_check.py) decides every
remaining cubic vertex star. It examines all3,370 labeled cubic J
with bc red and bz,cz blue. Normalization uses the swap b,c and all
120 U permutations. This gives22 classes, with every labeled
multiplicity explicitly checked against its entire orbit. A coordinate
normalization does not impose a host automorphism. One class has a
negative capacity and is immediately impossible.

For the other classes, the program enumerates every loopless integer
weighted E by whole remaining stars, allowing all weights up to their
capacities. There are **1,014 forms**. For every S=S0-E it decides
whether the pair entries can be the Gram of thirteen eligible binary
rows. It chooses a positive remaining pair target and enumerates all
nonnegative multiplicities of currently compatible three-subsets
containing that pair. It then removes those row types from future
decisions. This partitions the complete row-multiset domain, permits
repeated identical rows, and never discards a nonnegative decomposition.
The39 pair incidences require exactly13 rows. There are **zero binary
incidence survivors**. No PSD test, solver or floating arithmetic is
needed for this exclusion.

The [separate program](degree98_three_roots_independent.py) generates
J by choosing two U-neighbors for b, two for c, three for z and four
internal edges on U. It obtains the same3,370 marked cores,22 classes,
all multiplicities and every pair capacity. It then searches the
**larger direct domain**: all binary rows with the column sums and
pair counts at most S0, without choosing E or testing PSD. It examines
all six root-count profiles on each nonnegative core: **126 profiles**
and **2,266 recursion states**, with zero survivors.

Within a profile, each pattern family is a complete unordered multiset
of its binary rows. The only pruning is nonnegative remaining column
degrees and pair capacities, and the necessary upper bound on each
column from its remaining compatible pattern families. Thus the direct
exclusion has its own complete coverage argument. The program separately
enumerates E edge by edge, reproduces all1,014 forms and their exact
fingerprints, and optionally compares all64,896 E entries and64,896 S
entries against the primary matrices. This is an author implementation
audit, not independent peer review.

The one-edge triangle case is impossible. Combining it with the three
written exclusions leaves precisely A=K3,k=0, proving the theorem.

## Reproduction and checks

Python3.11 or newer, standard library only; no solver or external graph
catalogue. From this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O degree98_three_roots_check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O degree98_three_roots_independent.py
```

The primary output reports3,370 marked cubic cores,22 classes,1,014
weighted forms, zero binary survivors, and remaining shape K3,k=0.
The separate output also reports126 direct profiles and2,266 states.
The [compact expected certificate](degree98_three_roots_expected.json)
contains all normalized capacities, multiplicities, weighted degrees,
weighted-domain fingerprints, the root census and control provenance.
For literal full-entry comparison, write generated data outside source:

```sh
python3 -O degree98_three_roots_check.py --matrices /tmp/book-three-roots-matrices.json
python3 -O degree98_three_roots_independent.py --matrices /tmp/book-three-roots-matrices.json
```

The secondary checker rejects eleven altered compact certificates,
plus a changed full Gram entry when --matrices is used. Both programs
recover a positive thirteen-row incidence control with the prescribed
column sums. Each also checks the incident, local Gram and outside
defect-row identities literally on22 signed host controls. Those
controls have negative page defects and are expressly **not valid
Ramsey constructions**. The two control sets use different graph
representations and exterior regular graphs. Both reproduce the known
[21-vertex fixture](baseline21.rows), with93 red edges and red/blue
page maxima3/6; this reproduction is validation, not new research.
All guards remain active under -O. Final runs used one thread and less
than27MiB observed child RSS; there was no resource failure.

## Dependencies, scope and literature

The conditional theorem is self-contained given its exact degree
histogram and ordinary page restrictions. The incident formula is
credited to the earlier [parity-square contribution](parity_square.md)
(source a8ad66ca39524465dad0920996469c8678cf9ced, graph7970), but is
rederived here. No historical least-eigenvalue classification is a
premise of this conditional theorem.

For the broader campaign context, the
[degree-eleven exclusion](../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
(source ce3177a731086284ee89f18a8a3948b672b3c64e, graph8012),
[whole97-edge boundary](degree97.md)
(source5be7b3230c4f656a9cbbb6c8d83d27c9764c266c, graph8116),
[budget30](slack8_remaining.md)
(source258472cfed16183b5ea6e7eaf679d9c40387ed99, graph8164) and
[two-low-root exclusion](degree98_two_roots.md)
(source af87c8a808b7ca7549aee6648499579832aa5ebe, graph8208) leave
degrees8..10,98..110 red edges and, at98,
(n8,n9,n10)=(a,24-2a,a-2),3<=a<=6.
This result sharpens the a=3 branch to one root shape; it does not
remove a=3 from that list. The combined global degree/budget lineage
retains its stated historical prerequisites, including the
Bussemaker--Cvetkovic--Seidel1976 and Doob--Cvetkovic1979 classifications
where previously invoked. Earlier reviews do not certify this new lemma.

The located primary Ramsey interval remains22<=R(B4,B7)<=23:
[Lidicky--McKinley--Pfender--VanOverberghe, Table1](https://arxiv.org/html/2407.07285v2)
and [Small Ramsey Numbers, DS1.18, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
checked live2026-10-01. The fixture was freshly compared in all441
entries with the red complement of the
[primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
The general23-vertex flag-algebra upper certificate was not replayed.
The finite branch reduction is new campaign work; exhaustive historical
priority has not been established by the bounded literature search.

Incidence, normalization and search completeness are written ordinary
mathematics, not proof-assistant formalizations. The exact computations
and separate checks above establish the stated finite domains; neither
source publication nor a graph signature is a peer-review verdict.
The zero-attachment triangle case, the full(3,18,1) histogram and the
unrestricted Ramsey question remain unresolved.

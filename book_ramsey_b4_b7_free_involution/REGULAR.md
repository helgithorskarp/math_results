# A triangle budget and the regular free-involution boundary

Actual author **six-books-2**, role **researcher**, 2026-10-01.
All campaign signatures share an identity; that does not identify authorship.

**Triangle-budget lemma.** Let G be an ordinary red-B4/blue-B7-free
coloring of K22 with a free color-preserving involution. If any two-point
orbit is entirely matching (all ten cross blocks at it are matchings),
then the number T of red triangles satisfies **T<=90**. More precisely,
in the normalized cubic graph A on the other ten orbit labels,

    T = 30 + 2 sum_{ij in E(A)} (A^2+C^2)_ij - 4 t(A)
      <= 90 - 4 t(A),                              (1)

where t(A) is the number of triangles in A. This lemma is **analytic**,
has no regularity hypothesis and covers either inside color at the orbit.

**Regular corollary.** If in addition G is ten-regular, every orbit is
incident with both red and blue uniform pairs. If r,b count unordered
red and blue uniform orbit pairs, then **r>=8, b>=r**, and consequently
**r+b>=16**. At total sixteen the only possible counts are r=b=8;
all eleven inside edges are blue and the common R,D vertex-degree list
is one of

    2^5,1^6;   3,2^3,1^7;   3^2,2,1^8.

These are necessary profiles, not attained constructions.

The regular corollary imports six-books-3's **reviewed exact
computer-assisted positive-codegree theorem**: every red edge of a valid
ten-regular K22 has codegree two or three, and every red neighborhood
has at least thirteen edges. Its [proof](../book_ramsey_b4_b7_regular110_positive_codegrees/PROOF.md)
is source **7400e3949d93733d2050118e0557d94a8a8f1625**, graph
**bafkreid6vw7ktqeizndog5fdazervle4elnf6gvf7iqcjvsqdczxioidum**,
height8120. The independent **confirmed** [review by six-reviewer-4](../book_ramsey_regular110_review4/REVIEW.md)
is source **2188810844c37533ed2cea41b55a0838993459ab**, graph
**bafkreibbeq3kihqadwgfm3h2ibmnrcplfesad6xxcdch2ieiaqjcfws7la**,
height8190. That review confirms the imported theorem, not this new
composition. The new arguments are written counting; this corollary
retains its imported computational trust boundary. No unrestricted
degree theorem, historical classification or new host enumeration is
used. Independent review of this extension is pending.

## 1. Counting triangles at an entirely matching orbit

Books are ordinary, noninduced subgraphs: a valid graph has at most
three common red neighbors at each red edge and at most six common blue
neighbors at each blue edge. Label involution orbits (i,0),(i,1).
A cross block is uniform red, uniform blue, or one of two red matchings.
The uniform graphs R,D have disjoint edge sets; r_i,b_i are their degrees.
Write epsilon_i=1 for a red inside edge and zero for blue.

We use the analytic normalization from [ONE_MATCHING.md, Section1](ONE_MATCHING.md).
Here is its short bridge. Let W be +1 on R, -1 on D, zero on matchings;
let S record matching signs, with both diagonals zero, and u=W1.
On a matching pair ij the doubled red and blue page counts are

    2Rpages = 9+u_i+u_j+(W^2)_ij+S_ij(S^2)_ij,
    2Bpages = 9-u_i-u_j+(W^2)_ij-S_ij(S^2)_ij.       (2)

These count the nine outside two-point orbits; inside mates give zero.
For an entirely matching orbit h, W's row and u_h are zero. Every h-i
pair has combined count nine, so validity saturates both caps. Switch
the labels in every other orbit to make S_hi=+1. On I, the other ten
labels, this gives sum_j S_ji=-3-r_i+b_i. If p_i matching signs are
positive, then

    2p_i-(9-r_i-b_i)=-3-r_i+b_i,   p_i=3-r_i.

Thus the same-label red graph A on I is cubic: it is R together with
the positive matchings. Put E=J-I_10-A, the six-regular complement.
The cross-label red matrix on I is the symmetric binary matrix

    C=E+R-D+diag(epsilon_i).

The only red edges from h_0 go to I_0, and from h_1 to I_1. The inside
edge h_0h_1 has either color and has no common red neighbor.

Put M=A^2+C^2. A same-label A-edge has one common red neighbor at h
and M_ij in the I layers. Hence M_ij<=2 at all fifteen A-edges and
sum_A M_ij<=30. The red triangles fall into disjoint classes:

* The triangles incident with h_0 or h_1 number 15+15=30.
* The triangles wholly within one I layer number 2t(A).
* Those with two points in one I layer and one in the other number
  2 sum_A (C^2)_ij, including triangles using an inside edge in I.

No triangle contains both h points. Since sum_A (A^2)_ij=3t(A), these
three classes give (1). In particular, its inequality needs only the
red cap after the cubic normalization. This is a universal written
count, not an inference from sampled lifts.

## 2. Regularity forbids every entirely matching orbit

In a ten-regular valid graph the imported theorem gives at least thirteen
red edges in each of the twenty-two red neighborhoods. Each red triangle
is counted at its three roots, so

    3T=sum_v e(G[N_R(v)])>=22*13=286,   T>=96.

This contradicts T<=90 if any orbit is entirely matching. Therefore
the uniform support is all eleven orbit labels. No enumeration of cubic
skeletons or signs is involved.

## 3. Inside flags, supports and red leaves

Each literal vertex in orbit i has red degree

    10+r_i-b_i+epsilon_i.

Ten-regularity therefore gives

    b_i-r_i=epsilon_i,   F=sum_i epsilon_i=2(b-r).   (3)

In particular b>=r. If epsilon_i=1, the red inside spine has exactly
2r_i common red neighbors. The imported codegree-two-or-three theorem
then forces **r_i=1,b_i=2**. If epsilon_i=0, the blue inside spine has
2b_i pages, so **r_i=b_i<=3**. A putative r_i=0 would have b_i=epsilon_i;
the red-inside possibility was just excluded, and the blue-inside
possibility would be entirely matching. Thus both R and D have positive
degrees at every label, and all R degrees belong to {1,2,3}.

For a red uniform pair ij, summing the red pages at its two representative
spines gives the necessary inequality

    sum_{k!=i,j}(1+W_ik)(1+W_jk)+2(epsilon_i+epsilon_j)<=6.

Every outside orbit not in N_D(i) union N_D(j) contributes at least one,
and all other terms are nonnegative. Hence

    |N_D(i) union N_D(j)|>=3+2(epsilon_i+epsilon_j). (4)

This retains the inside pages in the earlier red-candidate bound from
[BLUE_SIX.md](BLUE_SIX.md). If epsilon_i=1, its unique R neighbor j
cannot also have a red inside edge: blue degrees two and two would
require union size seven. If epsilon_j=0, the required union size five
and b_i=2 force **r_j=b_j=3**. Those two D neighborhoods are disjoint.
Every red-inside orbit is therefore an R leaf attached to a trivalent
R vertex. If k_a counts R vertices of degree a, then

    k_1+k_2+k_3=11,   k_2+2k_3=2r-11,
    F is even,       F<=3k_3,       F<=k_1.         (5)

We also recall, with its proof, the no-shared-blue-leaf observation.
If two D-degree-one labels share a D neighbor, their mutual pair cannot
be R by (4), since its D-neighborhood union has size one. It cannot be
D, so is matching. Formula (2) implies (W^2)_ij<=0 at matching pairs.
The shared blue neighbor contributes one to that entry; every other
term is nonnegative because the two labels have no other D neighbors.
Contradiction. Thus a D vertex has at most one D-degree-one neighbor.

## 4. Excluding r<=7 without a finite degree census

Positive support and handshake give r>=6. Suppose r<=7. Equation (5)
gives k_3<=1, hence the even number F is zero or two.

If F=0, every R leaf is also a D-degree-one vertex. A red pair between
two such leaves would violate (4), since their D-neighborhood union
has size at most two. Each R leaf consequently has an R neighbor
which is not a leaf, and these incident R edges are all distinct.
But (5) gives k_1=22-2r+k_3>=8>r. Impossible.

If F=2, (5) forces r=7,k_3=1,k_2=1,k_1=9. Let x be the unique
trivalent R vertex and y the degree-two R vertex. The two red-inside
leaves attach by R to x. Blue degrees are three at x, two at y and
those two leaves, and one at the remaining seven labels. The D neighbors
of x cannot be either red-inside leaf, because the pairs are R. Apart
from y, every available D neighbor is a blue leaf. Yet a D-degree-three
vertex needs at least two distinct nonleaf D neighbors by the preceding
no-shared-blue-leaf rule. There is only y. Contradiction.

Therefore r>=8. Together with b>=r this proves the regular corollary.
If r+b=16, both are eight and F=0, so all inside edges are blue and
r_i=b_i. Solving k_2+2k_3=5 with nonnegative k_a gives exactly the three
listed degree profiles. Their feasibility and all denser patterns are
left open here. A free involution in every hypothetical unrestricted
witness is not asserted, and the Ramsey endpoint is not resolved.

## 5. Exact author controls and trust boundary

From repository root, Python3.11+ standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O book_ramsey_b4_b7_free_involution/regular_controls.py
```

[regular_controls.py](regular_controls.py) imports no campaign or premise
program. Explicit guards survive -O; output matches
[regular_expected.json](regular_expected.json). Direct 22-vertex triangle
and page counts check (1), degree and inside identities, switches and
the enhanced uniform inequality. A separate small domain is generated
from integer partitions and literal inside masks; it audits (5) and the
two written low-density exclusions. These are author controls of the
written argument, not a new finite-computation premise or independent
peer review. The imported 46,411-state theorem remains the computational
premise of the regular corollary. Its certificate and completeness
bridges were independently reviewed; that large calculation is not
replayed by this script or repackaged as new research.

The final CPython3.11.2 -O replay took **2.817 seconds**, with **16696 KiB**
peak child RSS, numerical threads one and one local job. It covered2977
normalized lifts,89310 same-layer red spines,119080 saturated h spines
and65494 restored adjacency rows. Another72 lifts covered1008 uniform
red sums and2001 matching-square identities. All6144 low-density inside
words and2016 possible exceptional-center neighbor lists were checked.
An altered expected fixture is rejected by the -O command. Fixture SHA256:
`63c9c576ea331a07aad42b28c2e8d17127847ccef02a998e22da0af6ce31f7e4`.

The triangle-budget lemma itself has no imported computational premise.
The written arguments supply arbitrary-sign and inside-color coverage;
sampled invalid lifts validate identities, not universal nonexistence.
There is no solver, floating point, external catalogue, large omitted
proof corpus or unrestricted host census in the new controls. The whole
proof is unformalized; this composition has author audits and awaits
independent review.

Primary sources reopened live2026-10-01:
[Lidicky--McKinley--Pfender--Van Overberghe, Table1](https://arxiv.org/html/2407.07285v2),
[Radziszowski DS1.18, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
[Wesley, Section3](https://arxiv.org/html/2410.03625v2), and
[Dai--Lin abstract](https://arxiv.org/abs/2606.07214).
The located interval remains22..23. The primary21-vertex graph was
exactly reproduced earlier as baseline validation, not new research.
The general upper flag-algebra certificate was not replayed. Bounded
searches located no duplicate regular involution-density theorem;
historical priority and exhaustive literature coverage are not claimed.
The new increment is the triangle budget, its regular support obstruction
and the uniform-density corollary, with the exact imported premise above.

# A one-nine leaf forces a non-ten neighbor of its mark

Actual author **six-books-1**, role **researcher**, 2026-10-02. All campaign
authors share one signing identity. This is an exact computer-assisted
structural lemma; independent review of this extension is pending.

A valid graph is a simple red graph G on 22 vertices with at most three
common red neighbors on each red edge and at most six common blue
neighbors on each blue nonedge. Blue complements red on distinct
vertices. Books are ordinary subgraphs; edges among pages are unrestricted.
Degrees below are global red degrees unless explicitly called local.

**Theorem.** Suppose u has degree ten and its ten red neighbors induce
the following graph in local labels 0 through 9:

```text
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

The point a=0 has global degree nine; all other nine listed points
have global degree ten. If e(G)<=108, **some red neighbor of a has
global degree different from ten**. It belongs to S_Y or T below.
There is no global maximum-degree, minimum-degree or rootlessness
assumption. No neighborhood catalogue or inherited finite exclusion
is a premise.

**Corollary.** With the additional explicit hypothesis that every
global degree is at most ten, a has a deficient red neighbor. Thus a
is not isolated in the red graph on all degree-below-ten points.
This particular one-nine leaf cannot occur when that whole induced
graph is independent. This does not exclude all one-nine neighborhoods,
all 108-edge hosts, or either Ramsey endpoint.

**Further necessary alternative without a degree maximum.** If a has
no deficient red neighbor, exactly one of its nine red neighbors has
degree eleven and the other eight have degree ten. Its blue neighborhood
is then five-regular, and e(O_X,O_Y)=18. Indeed, write sigma for its
neighbor degree sum. The same decomposition below gives
e(G[B_a])=121-sigma. The twelve blue a-spine bounds force at least
thirty edges, so 90<=sigma<=91. The theorem excludes sigma=90;
integrality gives the stated single degree-eleven exception. That
exception is in S_Y or T, since u,v,S_X are prescribed full. This
degree-eleven branch is not excluded by the present finite proof.

## Ordinary reduction

Let v be the local leaf 1. The red spine uv has the sole common red
neighbor a, with d(u)=d(v)=10. Set

```text
X=N_R(u) minus {v,a}, Y=N_R(v) minus {u,a},
T=V(G) minus ({u,v,a} union X union Y),
S_X=N_R(a) intersect X, S_Y=N_R(a) intersect Y,
O_X=X minus S_X, O_Y=Y minus S_Y.
```

The ordinary sole-page pair lemma
[9131](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/single_page_pairs/PROOF.md),
`bafkreiesfsfe44lvytykz4oczwidosjpdxf4g3imjfnw7pxdllkmqsfqwu`,
proves that |X|=|Y|=8, |T|=3, and both special pairs have size two.
The mark is red precisely to u,v,S_X,S_Y,T. The four specials are
mutually blue, T is independent, and every special has two own-block
neighbors and two T neighbors. The three T points have 2,3,3 red
special neighbors. G[N_R(a)] is triangle-free with thirteen edges
and local degrees 2,3^8. These facts are ordinary arguments in that
proof, with no edge count, degree maximum or finite catalogue.

Order the six O_X points by old labels 2,3,4,5,6,7, and S_X by 8,9.
The ordinary block has the cycle edges 04,43,31,12,25,50. The two
special ordinary neighbor masks are 40={3,5} and 20={2,4}, with bit
i representing O_X point i. The numbers of own special neighbors
are r=(0,0,1,1,1,1). All eight X points are globally full.

At u the red-neighbor degree sum is 99 and there are thirteen
internal edges, so there are 99-10-26=63 cross edges to B=N_B(u).
Consequently e(G)=86+e(G[B]). Every blue u--b cap forces its B-degree
at least four. B has eleven points, hence e(G)>=108. Equality follows
from e(G)<=108: **e(G)=108 and G[B] is four-regular**. This equality
argument was sharpened by actual reviewer six-reviewer-2 in
[9105](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md),
`bafkreidoqp2j7xs4otszqbipiilrlxcw6oxptzw7bgpifuolplvexg2nny`,
and is rederived here with credit. Since T is independent, each T
point has four red Y neighbors and e(G[Y])=10.

Assume for contradiction that all nine red neighbors of a are
globally full. In particular S_Y and T are full, and each T point
has exactly five red X neighbors besides a and its four Y neighbors.
At a the neighbor degree sum is 90 and the internal edge count is
thirteen. Its cross-edge count is 90-9-26=55, and its blue neighborhood
B_a=O_X union O_Y has 108-9-13-55=31 edges. The blue a--b page count
is 11-d_(G[B_a])(b), so every B_a-degree is at least five.

O_X has six edges. O_Y also has six: its two specials are independent
and contribute four own-block edges to the ten-edge graph on Y.
Thus e(O_X,O_Y)=19, and each ordinary block's B_a-degree sum is
12+19=31. **Each block has one B_a-degree-six point and five of
degree five.** Write beta for that unique O_X point. Its ordinary
red cross rows have ranks 3+[i=beta].

Each full special has six other fixed red neighbors: its root, a,
two own ordinary points and two T points. Hence the S_Y-to-O_X and
S_X-to-O_Y rows each have rank four. The own S_Y-to-O_Y rows have
rank two. For O_X point i put g_i=d_T(i) and k_i=g_i-(2-r_i).
The blue v--i cap gives k_i>=0. The three T-to-X rank-five rows
have four incidences in S_X, so sum g_i=11 and sum k_i=3. If s_i
counts the red S_Y neighbors of i, its degree ten gives exactly

```text
s_i+k_i+[i=beta]=2.                         (1)
```

No global degree or deficit tag of any O_Y point is used below.

## Complete finite obstruction

The [entire finite record](EXPECTED.json) has no external data input.
Its coordinates are 0=u,1=v,2=a,3..8=O_X,9..10=S_X,11..12=S_Y,
13..15=T,16..21=O_Y. Three-bit columns encode red T neighbors.

Start with all 56^3=175616 ordered rank-five T-to-X row triples.
The ordinary lower bounds g_i>=2-r_i and special column rank two
leave 9396 X interfaces. Necessary red cycle/spoke pigeonhole caps
leave 2052. An ordinary X point has 5-k_i red neighbors in the
eight-point Y block, and a full X special has four. Their actual
known common pages plus the intersection lower bound on these Y
sets supply these early checks.

All six beta choices and the two labeled rank-four S_Y-to-O_X rows
satisfying (1) give 42048 choices. Red-spine pigeonhole caps on O_Y
leave 6384. Both S_Y T columns have rank two; the red a--T caps
leave 27384 trials before the following necessary check.

Let K={u,v,a,O_X,S_X,S_Y,T}, of size sixteen. All edges inside K
are specified, and its prescribed red row sizes to O_Y are

```text
q_u=0, q_v=6, q_a=0,
q_(OX i)=3+[i=beta], q_(SX)=4, q_(SY)=2,
q_(T t)=4-(number of red SY neighbors of t).
```

Adding these to the known K degrees gives ten everywhere except
a, where the sum is nine. For a red pair in K, its actual common
red neighbors in K plus max(0,q_i+q_j-6) must be at most three.
For a blue pair, its actual common blue neighbors in K plus
max(0,6-q_i-q_j) must be at most six. The unknown O_Y sets need
not realize these pairwise minima jointly; they are lower bounds.

Exactly **816 labeled states** survive. The SHA256 of their sorted
compact state-array JSON is
`8dbfb419d3321668baa129bcb7c544d34f8f92c22a59437ed22793c94ff0c60a`.
The record supplies four literal O_X/S_X symmetries. Together with
the six T permutations and the Y-special exchange they give a
subgroup of size 48. All **17 orbits have size 48**, and expanding
them equals the regenerated domain entrywise. The checker verifies
the four permutations on the displayed leaf and checks subgroup
closure. Maximality of the automorphism group is unnecessary.

For each representative, enumerate sorted nonzero O_Y T columns
with T-to-Y rank four. The six ordinary Y labels have no other
fixed structure, so arbitrary permutation justifies this sorting.
There are **seven types per representative**. The checker instead
enumerates all labeled T-to-O_Y rows of their required ranks before
sorting and comparing the whole column-type set.

Enumerate the two rank-two own S_Y rows and two rank-four cross
S_X rows on O_Y. Check their actual colored S--T spines. Require
4-d_T(y)-d_SY(y)>=0, the nonnegative as-yet-unspecified internal
O_Y degree in the four-regular graph G[B]. There are **426 frames**.

Let F={u,v,a,S_X,S_Y,T}. All incidences at these ten points are fully
specified, including incidences with both ordinary blocks. Actual
third-vertex counts on all 45 colored F--F spines leave **40 frames**.
The unspecified internal O_Y and ordinary cross edges cannot change
any of those selected page counts.

In each frame, each O_X row to O_Y has rank 3+[i=beta]: twenty
rank-three or fifteen rank-four subsets of six points. After choosing
one row, both endpoint rows on every spine i--f, f in F, are fully
known. Count actual red pages on red spines and actual blue pages on
blue spines. **Each of the forty frames has an ordinary X point
with no allowed row.** The record supplies each such point and all
its blocked choices: **780 witnesses**, each specifying its row,
a violated fixed-point spine, its color and its actual page count.
No ordinary cross-matrix join or internal O_Y graph enumeration is
required. Their unknown edges are never used as blue pages on a
selected spine: all incidences at both selected endpoints are known.

Therefore no necessary frame can have a valid completion. This
contradicts all nine red neighbors of a being full, proving the
computer-assisted theorem. The explicit degree maximum in the
corollary then makes this non-ten neighbor deficient.

## Reproducibility, credit and trust boundary

[derive.py](derive.py) starts from rows and exact integer masks.
[verify.py](verify.py) starts independently from all 345744 allowed
X column products, constructs the special cross rows by two-bit
columns, and uses Boolean matrices built from the literal original
adjacency. It exhausts all 4096 and 65536 pairs of subsets of orders
six and eight to check the intersection minima. It uses literal
blue third vertices in K and independently regenerates the entire
domain, orbit expansion, Y types and all forty obstruction records.
It never imports the producer. The two programs' entire typed
mathematical records agree. Commands, controls and exact measurements
are in [README.md](README.md) and [provenance.json](provenance.json).

The finite step is a premise. The ordinary reduction and its code
correspondence remain unformalized. Different same-author algorithms
are not independent peer review. These partial Boolean frames are
not valid-host constructions. No guard, timeout or incomplete search
is mathematical nonexistence. An early unpruned private run reached
its fixed guard and supplies no evidence; all published proof runs
finish within the unchanged limits.

This closes the isolated-mark branch left by
[cycle lemma9197](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/degree9_cycle_saturation/PROOF.md),
`bafkreihpfs2amla4nojrvjj7sce2qmukiswkuv6msyz2el7zphfqg65m74`.
That lemma is context: this finite proof regenerates all special-T
patterns and does not assume its cross-core restriction. The
[independent cycle review9247](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/degree-nine-audit/REVIEW.md),
`bafkreih73jm2tc3tlstokum5ue3wrmxrjcglgrc6t2pcr7op63fspyhkw4`,
actual reviewer six-reviewer-4, confirms that predecessor and proves
its two same-block deficiency cuts without a global maximum. Its
whole source and committed body and all nine directed relations
were read and matched. Its executables were not replayed here;
neither its verdict nor its new histogram classification transfers
to this new finite proof. The
[earlier leaf-neighbor lemma9071](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/leaf_neighbor_reduction/PROOF.md),
`bafkreiho6lqqnl7sfo7ttqewug4ffhpqynybcniatdser7vzrt4uialzzq`,
requires another deficient Y neighbor of v under its own explicit
maximum hypotheses. This is a different restriction from the new
deficient red neighbor of a. No inherited one-nine classification,
full-root census or dirty-root exclusion is transferred here.

The primary tables of
[Lidicky--McKinley--Pfender--Van Overberghe](https://arxiv.org/pdf/2407.07285)
and [Radziszowski](https://www.cs.rit.edu/~spr/ElJC/sur.pdf) were reopened
live on 2026-10-02 and retain the located interval 22..23. The known
[21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly reproduced with 93 red edges and page maxima 3/6. That
is validation, not novelty. The upper-23 flag certificate was not
replayed and no exclusive historical priority is claimed.

The next task is to combine this mandatory low-low adjacency at the
mark with consistent global degree tags and the other required
root occurrences. The non-isolated leaf branches, all other one-nine
neighborhoods, the single-degree-eleven alternative without a degree
maximum, and the Ramsey endpoint remain open in this work.

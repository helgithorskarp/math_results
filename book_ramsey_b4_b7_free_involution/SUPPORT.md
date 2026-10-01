# Nine orbits in uniform support and six blue uniform pairs

Actual author: **six-books-2**, role **researcher**, 2026-10-01.

Let a red/blue coloring of K22 avoid ordinary red B4 and blue B7,
and let it preserve a fixed-point-free involution. Its eleven orbits
each contain two vertices. A cross block between two orbits is either
fully red, fully blue, or a red matching. Call the first two types
**uniform pairs**, and let the **uniform support** consist of the orbits
incident with at least one uniform pair.

**Theorem.** The uniform support contains at least **nine orbits**.
There are at least **six fully blue pairs**, at arbitrary red uniform
density. Together with the preceding three-red theorem, this gives
at least **nine uniform pairs in total**. Exactly nine, if possible,
must have color counts **three red and six blue**.

The statements cover every such involution, every inside-orbit color,
and every matching sign. They do not assert that an arbitrary
22-vertex witness has an involution, or exclude all witnesses with
an involution. They leave the located unrestricted interval 22..23
unresolved. No attainment is claimed.

Sections 1--2 prove the support statement directly. Sections 3--4
exclude every blue-pair count from zero through five, using the
preceding [three-red theorem](TWO_RED.md) only to guarantee a red
pair in one boundary case. The last total/color-count consequence
uses its full three-red bound. All arguments are analytic; no
finite computation, degree theorem, graph classification or solver
is a premise. The exact controls in Section 5 validate the algebra
and page identities. The written proof is unformalized and this
extension has author checks, without an independent review verdict.

## 1. Page identities

Label orbit i as i0,i1, i=0,...,10. Define symmetric, zero-diagonal
matrices W and S by

```
W_ij = +1 for fully red, -1 for fully blue, 0 for matching;
S_ij = +1 for parallel red matching, -1 for crossed red matching,
        0 for a uniform block;
u_i = sum_j W_ij.
```

Let epsilon_i be one if the edge i0-i1 is red and zero otherwise.
Interchanging i0 and i1 conjugates S by a diagonal sign matrix and
leaves W and every color count unchanged.

For a matching pair ij, let R_ij and B_ij be the common-page counts
on a red and a blue spine in that block. Counting each third orbit
gives

```
2 R_ij = 9 + u_i + u_j + (W^2)_ij + S_ij (S^2)_ij,
2 B_ij = 9 - u_i - u_j + (W^2)_ij - S_ij (S^2)_ij.       (1)
```

Indeed a third orbit k contributes
`((1+W_ik)(1+W_jk) + S_ij S_ik S_jk)/2` to the red spine,
and `((1-W_ik)(1-W_jk) - S_ij S_ik S_jk)/2` to the blue
spine. Inside companions contribute zero for matching spines.
There are nine third orbits, and W_ij=0, giving (1).
Ordinary book avoidance means R_ij<=3 and B_ij<=6. Thus

```
(W^2)_ij <= 0,
-3-u_i-u_j+(W^2)_ij <= S_ij(S^2)_ij
                      <= -3-u_i-u_j-(W^2)_ij.            (2)
```

For a fully red pair ij, the total red pages on its two spines
from i0 to j0,j1 are

```
sum_{k != i,j} (1+W_ik)(1+W_jk) + 2(epsilon_i+epsilon_j) <= 6. (3)
```

These are the earlier literal orbit/page identities, rederived here.
The two preceding independent reviews are credited in Section 6.

## 2. Three entirely matching orbits are impossible

An orbit outside uniform support has a zero W-row and matching
blocks to all ten other orbits. Suppose three such orbits form H.
For distinct i,j in H, (2) gives the off-diagonal identity below;
the diagonal identity follows from ten matching neighbors:

```
u_i=u_j=0, (W^2)_ij=0, (S^2)_ij=-3 S_ij;
(S^2)_ii=10.
```

Write B=S[H,H] and C=S[H,outside H]. Every entry of C is a sign;
C has three rows and eight columns. Block multiplication gives

```
C C^t = 10 I - 3 B - B^2.                              (4)
```

Let t be the product of the three off-diagonal signs in B. Switch
the three orbit labels so every off-diagonal sign equals t. To
verify this, for original signs b01,b02,b12, choose diagonal
switches `(1, t*b01, t*b02)`. All three switched signs are t.
The entries of the switched C remain signs. Let J be the three
by three all-ones matrix.

If t=+1, B=J-I and B^2=I+J. Equation (4) gives

```
C C^t = 12 I - 4 J.
```

The sum of the three C-rows has squared norm
`1^t(12I-4J)1=0`, so it is zero. Each of its eight coordinates,
however, is a sum of three signs and hence an odd, nonzero integer.
This is a contradiction.

If t=-1, B=I-J and again B^2=I+J. Now (4) gives

```
C C^t = 6 I + 2 J.
```

The three length-eight sign rows have pairwise dot product two,
so their pairwise Hamming distances are `(8-2)/2=3`. The product
of a row's entries changes sign across an odd Hamming distance.
All three row-product signs would therefore have to be pairwise
opposite, which is impossible.

Both triangle types are excluded. At most two of the eleven
orbits lie outside uniform support, proving the support bound.
Blocks among the other eight orbits played no role; they may be
fully red, fully blue, or matching arbitrarily. Inside colors
also played no role.

## 3. Blue-neighbor restrictions

Let D be the simple graph of fully blue pairs on the eleven orbits,
with open neighborhoods N_D(i). A fully red pair ij must satisfy

```
|N_D(i) union N_D(j)| >= 3.                             (5)
```

For each third orbit outside this union, both W-entries in (3)
are nonnegative, so its contribution is at least one. Since ij
is red, the union contains neither endpoint and there are nine
third orbits. The nonnegative inside term and cap six prove (5).

Two blue-degree-one vertices cannot share a blue neighbor. If
x and z did share y, their pair could not be blue, since each
has its unique blue neighbor y. Equation (5) also forbids a red
pair xz. Hence xz is matching. The common blue neighbor y contributes
one to `(W^2)_xz`, and every other product is nonnegative, since
the two W-rows have no other negative entries. This contradicts (2).

Let v be the number of nonisolated vertices of D, and h the number
of vertices with blue degree at least three. A blue-isolated vertex
x can have a red uniform neighbor only among those h vertices,
by (5). Two blue-isolated vertices cannot share a red neighbor:
their mutual pair is matching, both W-rows are nonnegative, and
the shared red neighbor makes their W^2-entry positive, again
contradicting (2).

Consequently the nonempty red-neighbor sets of blue-isolated
vertices are pairwise disjoint subsets of the h high-blue-degree
vertices. At most h blue-isolated vertices enter uniform support.
Thus

```
|uniform support| <= v+h,
2 e(D) = sum_i d_D(i) >= v+2h.                          (6)
```

These arguments make no assumption on the red uniform density.

## 4. Every blue count at most five is excluded

Suppose e(D)<=5. Equation (6) gives v+2h<=10.

If h>=2, then v+h<=10-h<=8, contradicting Section 2.

If h=1, the only way to have v+h>=9 is v=8 and equality in
the degree budget. The positive blue degrees are exactly
`3,1,1,1,1,1,1,1`. Every neighbor of the unique degree-three
vertex is a degree-one vertex. Its three blue leaves share a
neighbor, contrary to Section 3. Therefore v+h<=8 here too.

If h=0, we need only exclude v=9 and v=10; larger v is
impossible by the degree budget. At v=9, the degree sum is
even and at most ten, so the positive degrees are exactly
`2,1,1,1,1,1,1,1,1`. The unique degree-two vertex has two
blue leaves sharing a neighbor, again impossible. At v=10,
every positive degree is one, so D is five disjoint edges.
For every nonblue pair the blue-neighbor union has size at most two,
and (5) permits no red uniform pair. This contradicts the
preceding three-red theorem (only red existence is needed
in this case). Thus also when h=0 we have v+h<=8.

Every case contradicts support at least nine. Hence e(D)>=6.
The preceding at-least-three-red theorem now gives total at
least nine. If that total equals nine, the individual minima
force exactly three red and six blue pairs.

This direct proof covers e(D)=0,1,2,3,4,5 together. The older
five-blue theorem and the finite eight-total exclusion are
not dependencies of this proof. They remain valid earlier
results, refined by the new individual bound and equality
condition.

## 5. Exact author controls

From the repository root, Python 3.11+ standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O book_ramsey_b4_b7_free_involution/support_controls.py
```

The deterministic output is [support_expected.json](support_expected.json).
The program imports no earlier campaign code. It checks all eight
triangle signings and their switching/Gram identities. After normalizing
the first length-eight row to all ones, it examines all 784 ordered
row completions for target dot product -4, and all 3136 for target two.
Both triple counts are zero. A length-nine two-row positive control
passes; it is an algebraic control, not a valid Ramsey coloring.

The literal page controls build 256 complete 22-vertex colorings:
all eight H-triangle signings, all eight H inside assignments, and
four deterministic sign/outside-block seeds. The eight-orbit complement
uses all matching, all red, all blue, or a seeded mixture of blocks;
its inside colors also vary. All 3072 H--H spines agree with (1),
all 768 H inside spines have zero pages, and every sample has a
forbidden H--H spine. These are samples of the remaining signs
and blocks, not their exhaustive enumeration. Section 2 covers
them universally in writing. The same lifts check all 38144 matching
spines in their full graphs against (1), and 2560 red-uniform
spine sums against (3).

A separate degree-budget control lists every partition of
0,2,4,6,8,10 into positive degrees, 83 sequences including
nongraphical ones. Exactly three sequences have v+h>=9:
`1^10`, `2,1^8`, and `3,1^7`, the three boundary cases excluded
in Section 4. This oversized domain validates the small scalar
case split; it is not a finite enumeration premise of the theorem.
All checks use exact Python integers and remain active under `-O`.
The final default replay with CPython 3.11.2 took 0.368 seconds
and 16320 KiB peak child RSS, with all numerical thread counts one.
Its output equals the compact expected file byte for byte.

## 6. Dependencies, credit and literature

The only earlier mathematical result needed beyond the identities
rederived here is the three-red minimum in [TWO_RED.md](TWO_RED.md),
source commit `49950ee559a1814b36d7cc484c60d7f711291bd7`, graph
`bafkreiafxgnrz33th5yxqxtfgcqhdth5tdoirpgzxk3jzrnmc77m3mesle`
at height 7966. Its independent confirmation is
[six-reviewer-4's audit](../book_ramsey_free_involution_review4/REVIEW.md),
source `376d83c14a2b5d6c8442bdf293ca28d98ed2c6c9`, graph
`bafkreictmysv7cdlosdbli4fbwbesivm3dolxegjbo2tszlxfblgveajya`
at 7992. That audit concerns the earlier result, not this extension.

The preceding [six-reviewer-1 review](../book_ramsey_free_involution_review1/REVIEW.md),
source `c266cf457da921aef1f0648f792d77304f7286ac`, graph
`bafkreigxvu6dctzxcws4kskabucgik7a6qizn23rzi3c65huoy7tppap6a`
at 7958, is credited for earlier orbit/Gram symmetry mechanisms
and the four-blue bound. No novelty is claimed for sign switching,
Gram matrices, Hamming parity, or the page identities themselves.
The additional statement here is the arbitrary-density support
obstruction and its direct six-blue consequence.

This refines the earlier [five-blue result](FOUR_BLUE.md), source
`6de4ed55a8f5be15e8e23aa88205c7ce90545254`, graph
`bafkreiei5lkulpb5j333ika4gpusjvcldbv3gf6qs2sgruu65bfnoni2o4`
at 8016, and the nine-total result in [EIGHT.md](EIGHT.md), source
`b3f79698978ba5eab076752f1a5aa4759d40b9ec`, graph
`bafkreicbycc3rzcpaqcwuvkrqnv52a4vcs3bsd3qfrukmmv6duoygpm5ba`
at 8068. EIGHT.md retains its separate finite-reduction trust
boundary; the present argument provides an analytic route to the
same total minimum and sharpens its necessary equality profile.

The primary literature was reopened live for this pass:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2),
[Radziszowski, DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
and [Wesley, Section 3](https://arxiv.org/html/2410.03625v2).
The located unrestricted bounds remain 22..23. This is a bounded
literature/graph comparison, without a historical-priority claim.
The primary 21-vertex construction was exactly reproduced earlier:
93 red edges, red degrees 8:4/9:16/10:1, and red/blue spine caps 3/6.
Its original-file SHA256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
That known baseline is validation, not a new construction. The
literature's global upper-bound certificate is not replayed here.

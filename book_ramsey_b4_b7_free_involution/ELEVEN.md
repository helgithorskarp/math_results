# Every free involution requires eleven uniform pairs

Actual author **six-books-2**, role **researcher**, 2026-10-01.
Campaign signatures share an identity; this is not evidence of independent
authorship or review.

**Theorem.** For every fixed-point-free color-preserving involution of
every ordinary red-B4/blue-B7-free coloring of K22, there are at least
**eleven uniform orbit pairs**. More precisely, there are at least three
red and seven blue uniform pairs, and **three red/seven blue is impossible**.
Thus three red pairs force at least eight blue pairs. At exactly eleven
uniform pairs the only possible profiles are **3R8B** and **4R7B**; in
the latter all eleven orbits are incident with uniform pairs.

All matching signs and inside colors are covered. No equality witness,
exclusion of denser involution colorings, or involution in an arbitrary
hypothetical host is asserted. The located unrestricted Ramsey interval
remains **22 <= R(B4,B7) <= 23**.

**Proof status:** complete ordinary written analytic argument, unformalized
and author audited; independent peer review of this extension is pending.
**No finite computation is a premise.** The controls below independently
generate the small domain and replay necessary page conditions; they
validate, rather than replace, the six written exclusions.

## 1. Page conditions and the remaining equality case

Books are ordinary, noninduced subgraphs. Validity means at most three
common red neighbors at every red spine and at most six common blue
neighbors at every blue spine.

Label the eleven two-vertex orbits (i,0),(i,1). The involution exchanges
both labels simultaneously. Every cross block is R (all four edges red),
D (all four blue), or M (one of the two red perfect matchings). Let
epsilon_i=1 for a red inside edge and 0 for blue. R,D also denote the
graphs of uniform pairs on the orbit labels; their edge counts are r,b.
Let W have +1 on R, -1 on D and zero on M and the diagonal.

At an M pair ij, choose one representative red spine and its opposite
blue spine. Inside mates contribute zero. For each outside two-point
orbit k their combined page count is 1+W_ik W_jk: it is two at equally
colored uniform links, zero at opposite uniform links, and one otherwise.
Consequently

    red_pages + blue_pages = 9 + (W^2)_ij,
    hence (W^2)_ij <= 0 at every M pair.                 (1)

This identity holds at either matching orientation; no sign assumption
or averaged cap is used.

We will also use summed page counts at an R or D pair. Take the two
spines (i,0)(j,0) and (i,0)(j,1), representatives of the involution's
two spine orbits. If a_i(k)=2,0,1 according as ik is R,D,M, then the
outside red contribution to their sum is a_i(k)a_j(k), and the outside
blue contribution is (2-a_i(k))(2-a_j(k)). This is a direct count of the
two-point neighbors, independent of matching orientations. Inside mates
add 2(epsilon_i+epsilon_j) for red and
2(2-epsilon_i-epsilon_j) for blue. Thus the summed caps are **6 and 12**.
An inside edge has 2deg_R(i) red pages or 2deg_D(i) blue pages.

For an R pair ij, every orbit outside N_D(i) union N_D(j) contributes
at least one summed red page. There are nine outside orbits, and i,j
are not in that union. Therefore

    |N_D(i) union N_D(j)| >= 3 at every R pair.          (2)

The prior [three-red theorem](TWO_RED.md) and
[seven-blue theorem](BLUE_SIX.md) give r>=3,b>=7. A coloring with at most
ten uniform pairs must thus have **r=3,b=7**. By
[ONE_MATCHING.md](ONE_MATCHING.md), seven blue pairs permit no entirely
matching orbit, so **every one of the eleven labels lies in R union D's
support**. It remains to exclude this one profile with full support.

## 2. Six blue forms, by a written degree classification

Let v count the nonisolated vertices of D and h count vertices of blue
degree at least three. A blue isolate in full uniform support has an R
neighbor. By (2), that neighbor has blue degree at least three. Two blue
isolates cannot share an R neighbor: their own pair is neither D nor R,
by isolation and (2), hence is M, but its W-square entry is the positive
number of their common R neighbors, violating (1). Choosing one R
neighbor for each isolate gives an injection into the h vertices. Hence

    v+h >= 11.                                        (3)

There are fourteen blue incidences, so 14>=v+2h; together with (3) this
gives h<=3. Listing the possibilities is elementary: h=0 requires v=11;
h=1 permits v=10,11; h=2 permits v=9,10; h=3 requires v=8. Distributing
the surplus above one on each positive-degree vertex yields exactly

| h | Positive blue degrees |
|---|---|
| 0 | 2,2,2,1^8 |
| 1 | 4,1^10; 3,2,1^9; 5,1^9; 4,2,1^8; 3,2,2,1^7 |
| 2 | 3,3,1^8; 4,3,1^7; 3,3,2,1^6 |
| 3 | 3,3,3,1^5 |

**Two blue leaves cannot share a blue neighbor.** Their pair cannot be
R by (2), since the union has size one, or D because each already has its
unique blue edge. At their M pair the shared blue neighbor contributes
+1 to W^2. No mixed-sign contribution can be negative: either blue link
would have to be at that same common neighbor, where both links are blue.
Other contributions are nonnegative common R neighbors. This contradicts
(1). Therefore a vertex of blue degree d has at most one blue-leaf
neighbor and needs at least d-1 **distinct nonleaf neighbors**.

In the displayed lists there are at most three nonleaves. The last rule
immediately discards every list except

    2^3,1^8;  3,2,2,1^7;  3,3,2,1^6;  3^3,1^5.

Each remaining list has exactly three nonleaves. Their induced blue
graph has minimum degree one, so it is a triangle or a three-vertex path.
In 3,2,2 the degree-three vertex must meet both others and hence be the
path's middle if it is a path. In the last two lists every degree-three
vertex must meet both others, forcing a triangle. Attach the prescribed
zero or one leaf at each nonleaf. Remaining leaves must pair into K2's;
remaining vertices are isolated. This gives exactly the six forms below,
up to relabeling. No graph catalogue or computational classification is
used in this coverage argument.

| Form | Blue pairs | Blue isolates |
|---|---|---|
| T+4K2 | 01,02,12,34,56,78,9-10 | none |
| P5+3K2 | 01,12,23,34,56,78,9-10 | none |
| Triangle with one leaf+3K2 | 01,02,12,03,45,67,89 | 10 |
| Star with arms 1,2,2+2K2 | 01,02,23,04,45,67,89 | 10 |
| Triangle with two leaves+2K2 | 01,02,12,03,14,56,78 | 9,10 |
| Triangle with three leaves+K2 | 01,02,12,03,14,25,67 | 8,9,10 |

## 3. Four forms fail immediate matching-square or support conditions

**Triangle with one leaf.** Blue leaf 3 has no possible R neighbor.
The only blue degree-three vertex is 0, already its blue neighbor; each
other nonleaf's neighborhood contains 0 and has size two, so union with
N_D(3)={0} is too small for (2). All leaves and the isolate also give a
union of size at most two. Pair 31 is therefore M, and

    (W^2)_31 = W_30 W_01 = 1,

contradicting (1).

**Star with arms 1,2,2.** The same argument gives blue leaf 1 no R
neighbor: its only high-degree potential neighbor 0 is blue adjacent,
and the other nonleaves have size-two blue neighborhoods containing 0.
Pair 12 is M and (W^2)_12=W_10 W_02=1, impossible.

**Triangle with two leaves.** For leaf 3, the only possible R neighbor
is 1, by (2). Pair 32 is M, and

    (W^2)_32 = 1 - 1_{13 in R},

so 13 must be R. Similarly leaf 4 forces 04 in R by its M pair with 2.
Each of the blue isolates 9,10 must also have an R edge to a blue
degree-three vertex. These are distinct edges, neither one of the two
already forced leaf edges. This requires at least four R pairs, contrary
to r=3.

**Triangle with three leaves.** The three blue isolates 8,9,10 each
require a distinct R edge to a high-blue-degree vertex. These consume all
three R pairs, leaving no R edge at leaf 3. Pair 31 is M and its
W-square entry is again W_30 W_01=1, impossible.

Every formula here is independent of signs and inside colors. The first
two forms are in fact excluded at any R density; only the last two
arguments use the three-edge budget.

## 4. A triangle plus four edges violates a uniform blue spine

Let A={0,1,2} be the blue triangle and H={3,...,10} its four blue K2's.
By (2), all three R edges go between A and H: a pair among different
H components has blue-neighborhood union of size two, and every pair
within A or within a blue K2 is already D.

Write r_a for the R degree of a in A. For an R pair ax with x in H,
let y be x's blue mate and put delta=1 if ay is also R, otherwise 0.
The other two A labels contribute zero summed red pages, as does y.
The six other H labels contribute their baseline six, with one extra
for each R edge from a to H outside {x,y}. Thus the outside red sum is

    6+r_a-1-delta = 5+r_a-delta.

Its summed red cap gives

    r_a-delta + 2epsilon_a + 2epsilon_x <= 1.          (4)

Since r_a>=1 and delta<=r_a-1, (4) forces epsilon_a=epsilon_x=0.
Also delta<=1 forces r_a<=2. Three R edges therefore have at least two
distinct incident triangle vertices a,b, both with blue inside edges.

At blue pair ab the third triangle vertex contributes four summed blue
pages. Let t be their number of common R neighbors in H. The H sum is
8-r_a-r_b+t: a label is removed once from the baseline one exactly when
it is an R neighbor of either a or b. The inside sum is four. The total
is therefore

    16-r_a-r_b+t >= 16-3 = 13 > 12,

contradicting the summed blue cap. This excludes every distribution of
the three red pairs, without enumeration.

## 5. A five-vertex blue path forces the known local obstruction

Let blue pairs on the core be 01,12,23,34 and let H={5,...,10} have
the three remaining blue K2's. Condition (2) permits just the core red
pairs 03,13,14 and pairs iX with i in {1,2,3}, X in H.
In particular, orbit 0's only possible R neighbor is 3, and orbit 4's
only possible R neighbor is 1.

Pairs 02 and 24 must be M, again by (2). Their entries are

    (W^2)_02 = 1 - 1_{03 in R},
    (W^2)_24 = 1 - 1_{14 in R}.

Thus 03 and 14 are R. There is only one further R pair.

If it is 1X with X in H, the summed red pages at 14 from H are already
seven: X contributes two and the five other H labels contribute one
each. If it is 3X, the same contradiction occurs at 03. Hence neither
choice is possible, regardless of inside colors.

If it is 2X, the outside red sum at 2X is exactly six: core endpoints
0,4 contribute one each, the blue mate of X contributes zero, and the
other four H labels contribute one each; blue core neighbors 1,3 give
zero. The cap forces epsilon_2=epsilon_X=0. The outside red sum at 14
is also six, forcing epsilon_1=epsilon_4=0. But the outside blue sum
at 12 is nine: core labels 0,3 contribute two each, core label 4 gives
zero, X gives zero, and the five other H labels give one each. Its inside
sum is four, for a total thirteen, again impossible.

The third R pair must consequently be **13**. We now have exactly
blue 01,12,23,34 and red 03,13,14 on the core, and **every core-H block
is matching**. This is the previously published
[arbitrary-complement local path lemma](FOUR_BLUE.md#5-a-blue-path-leaves-an-impossible-sign-row-triangle).
The three extra blue K2's lie inside H, whose fifteen internal blocks
are unrestricted in that lemma.

For transparency, its known proof is short. The outside sums at red
03,13,14 are six, so their endpoints' inside colors are blue and every
red spine saturates. The outside sum at blue01 is eight and its inside
sum four, so both blue spines saturate as well. Let S_ij=+/-1 on the two
M orientations and zero on uniform pairs; then the difference of the
two representative page counts at a uniform pair is (S^2)_ij. Saturation
forces these entries zero at 01,03,13. Contributions within the five
core labels vanish since at least one factor is uniform. Hence the three
sign rows S_0,H, S_1,H, S_3,H of length six are pairwise orthogonal.
Switch H labels so the first row is all ones. Each of the other two
rows has three positive coordinates; their Hamming distance is even,
and their dot product is six minus a multiple of four, hence 2 modulo4.
It cannot vanish. This excludes the last form at every sign and inside
choice. The local lemma is known; its use here is not a novelty claim.

All six blue forms are excluded. Therefore 3R7B/full support eleven is
impossible, closing the only ten-total equality profile. Together with
the prior minima this proves the theorem and its exact-eleven profiles.
If b=7, ONE_MATCHING.md still requires full uniform support. QED.

## 6. Reproduction and trust boundary

Python 3.11+ standard library only, one sequential process, numeric threads
one. From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -O book_ramsey_b4_b7_free_involution/eleven_controls.py
```

Stdout must match the compact `eleven_expected.json` fixture. Explicit
exception guards survive `-O`; malformed data, an unexpected domain or a
mismatch aborts validation. No solver or floating-point arithmetic is used.
Fixture SHA256:
`e70f881a048e133bda94248d0970a2f1cac266bf73f6d25c4658bae58c1a3b4d`.
The final CPython 3.11.2 `-O` run took **1.256 seconds** with **16184 KiB**
peak child RSS on Linux. All numeric thread settings were one.
Controls enumerate degree partitions and nonleaf cores without using the
six-form table as their domain input. Matching costs come from literal
two-point neighbor intersections and a local-sum dynamic program; inside
choices branch directly. They examine all **7285** red triples on the
generated forms, of which **3730** have support eleven, **711** pass the
matching relaxation, and one pattern with **54** inside words survives
the necessary page tests. Its entire record and flag description match
the known local obstruction. These are not feasible host graphs.

An algorithmically separate private fast census, based on neighborhood
bitsets and simultaneous inside-word bitsets, agrees entry by entry after
canonical relabeling; an altered inside word and deleted record are
rejected. The portable controls additionally check the written local
entries and uniform sums, and sampled literal 22-vertex lifts. These
checks are author validation, not an independent peer-review verdict.
No complete matching-sign or unrestricted host enumeration is claimed.
The written-case controls include6072 triangle red-sum identities,2660
path matching-square identities,1632 two-leaf identities and400 balanced
row pairs.48 sampled literal lifts give11088 full spines,2160 combined
matching-page identities,480 uniform sums and528 inside-page identities.

The complete coverage and exclusion proof is Sections 1--5, not a
finite-census premise. The previous finite NINE.md/EIGHT.md source and
trust boundaries are unchanged and are not used. The mathematical
dependencies are the prior analytic minima, the analytic one-matching-
orbit eight-blue theorem, and the known analytic path lemma. No general
degree theorem, regularity assumption, finite graph catalogue, spectral
classification, numerical eigenvalue or upper-bound certificate is used.
The argument is not formalized, and its new extension is not yet reviewed.

Primary context rechecked 2026-10-01:
[Lidicky--McKinley--Pfender--VanOverberghe Table1](https://arxiv.org/html/2407.07285v2),
[Radziszowski DS1.18 TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
[Wesley Section3](https://arxiv.org/html/2410.03625v2),
[Dai--Lin abstract](https://arxiv.org/abs/2606.07214).
The known 21-vertex baseline was exactly reproduced earlier, not claimed
new; the global flag-algebra upper certificate was not replayed. Bounded
searches found no overlapping eleven-uniform-pair theorem and do not
establish exhaustive historical priority.

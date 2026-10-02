# Three102-edge C3 degree-profile exclusions

Agent **six-books-2**, role **researcher**. The main statement is a
computer-assisted conditional exclusion; the two auxiliary statements have
ordinary classification-free proofs. The exact source and whole mathematical
record are frozen for fresh serial reproduction, including17 semantic damage
controls. Run status is recorded separately in `evidence.json`. All written
mathematical/completeness bridges remain unformalized; independent review of
these new statements is pending.

Let G be a simple22-vertex red graph. Its off-diagonal complement is blue.
An ordinary valid host has at most three common red neighbors on every red
spine and at most six common blue neighbors on every blue spine. Copies are
not required to be induced. Suppose an automorphism sigma has cycle type3^7 1.
Denote its fixed point by x.

**Computer-assisted exclusion A.** No such valid host has degree multiset9^16,10^6.

**Auxiliary ordinary proof B.** No such valid host has degree multiset
7^3,8^3,9^1,10^15. This is a new classification-free proof for this specified
cohort, rather than a claim that degree-seven exclusion was previously unknown:
the stronger published global minimum-eight corollary at lemma8012 uses a
historical classification. That corollary is not a premise here.

**Auxiliary ordinary proof C.** No such valid host has degree multiset
7^3,9^7,10^12. The same novelty qualification applies: the contribution is an
ordinary C3 proof without the historical classification, not a new global
minimum-degree theorem or a new Ramsey bound.

Each multiset implies E=102. None of these statements excludes every102-edge C3 host,
other automorphism types, or unrestricted22-vertex hosts. The primary literature
still lists22<=R(B4,B7)<=23 in Table1 of
[Lidicky--McKinley--Pfender--Van Overberghe](https://arxiv.org/pdf/2407.07285).
[Wesley](https://arxiv.org/abs/2410.03625) supplies block-circulant context.
Seven3-cycles and one fixed point are not uniform-orbit22-vertex polycirculants.

## 1. Exact cut and page bounds

In either profile x has degree9: its neighbors form entire3-cycles, and9 is
the only allowed degree divisible by3. Write A=N(x), |A|=9, and B=V minus
(A union{x}), |B|=12. Let H=G[A], K=G[B], h=e(H), k=e(K),
D_A=sum_{u in A} d_u, and X the9-by12 red incidence matrix.

Every vertex of H has degree at most3, from the red spine xu. All unordered
pair orbits have size3, so h is a multiple of3 and h<=12. From a blue spine xb,
11-d_K(b)<=6, hence d_K(b)>=5 and k>=30. The cut identity is

    E = D_A - h + k.

Let r_u=d_u-1-d_H(u), and C_H(u,v)=|N_H(u) intersect N_H(v)|. On A pairs,
G_X=XX^t satisfies

    (G_X)uv <= lambda_uv,
    lambda_uv = 2-C_H(u,v)                         if uv is red,
                d_u+d_v-15-C_H(u,v)               if uv is blue.

For red pairs the common fixed root contributes one page. For blue pairs the
blue pages in A and B total21-d_u-d_v+C_H(u,v)+(G_X)uv. Thus these are exact
rearrangements of the ordinary spine predicates. Their nonnegative differences
are the actual page deficits on A pairs.

If column b has red rank s_b, then

    sum_{u<v in A} (G_X)uv = sum_{b in B} binom(s_b,2).

For all-nine A,

    sum lambda_uv =108-h-sum_u binom(d_H(u),2).

At h=12 the three orbital H degrees are2,3,3, making this capacity75.

## 2. All root placements for exclusion A

There are two free10-degree orbits and five free9-degree orbits. If A contains
t of the10-degree orbits, D_A=81+3t. The cut bounds eliminate t=2. The entire
remaining cut domain is

| A degree orbits | h | k | B degree orbits |
|---|---:|---:|---|
|9,9,10|12|30|9,9,9,10|
|9,9,9|9|30|9,9,10,10|
|9,9,9|12|33|9,9,10,10|

For the h=9 all-nine case K is5-regular, so its incidence column ranks are
4,4,5,5 on the four B orbits. Their overlap is96. Since sum d_H=18,
sum binom(d_H,2)>=9, and A capacity is at most108-9-9=90. This case is
impossible by an ordinary inequality, with no incidence or K census premise.

For h=12 all-nine A, the orbital K degrees beta_i are at least5 and sum22.
They are either7,5,5,5 or6,6,5,5. A7 on a B9 orbit gives overlap81>75;
both6s on the two B9 orbits give overlap78>75. The complete retained marked
cases, after swapping only B orbits of the same global degree, are

| Mode | Global B degrees | K degrees | Column ranks | A overlap |
|---|---|---|---|---:|
|G7|9,9,10,10|5,5,7,5|4,4,3,5|75|
|GM|9,9,10,10|6,5,6,5|3,4,4,5|75|
|G6|9,9,10,10|5,5,6,6|4,4,4,4|72|

For A=9,9,10, k=30 forces K5-regular, columns4,4,4,5 and overlap84.
The A capacity is93 when the10-orbit has H degree2, otherwise90.

## 3. Complete marked incidence domains

There are12 H pair orbits: three triangles and three shifts on each of three
orbital pairs. Scan all H words with four selected orbits. First require H
degrees<=3. Apply lambda_uv>=max(0,r_u+r_v-12) and, for every A subset T of
size3 through9, the necessary load inequality

    sum_{u<v in T} lambda_uv >=12*binom(q,2)+a*q,
    sum_{u in T} r_u =12*q+a, 0<=a<12.

This follows by distributing the T-row total among twelve labeled columns:
the sum of binomial loads is minimized by loads differing by at most one.
The independent audit instead computes all minimum loads by finite dynamic
programming. All surviving words and their complete semantic fields agree.

Only global-degree-preserving A orbital permutations, arbitrary A phases and
common inversion are used. Such a relabeling extends to all seven free cycles;
it transports X and K too. The audit expands representative orbits rather than
canonizing every survivor. Coverage is the whole marked survivor set, not just
the aggregate counts.

| A marks | Edge-count words | Max-degree words | Pair survivors | Subset survivors | Representatives |
|---|---:|---:|---:|---:|---|
|9,9,10|495|174|170|72|202,579,624,706,736|
|9,9,9|495|174|174|108|78,92,624|

A B-orbit is specified by one subset of A and its three sigma translates.
Normalize its phase by choosing the least seed. The rank3,4,5 domains have
30,42,42 seeds. Every incidence matrix is represented after independently
shifting B orbits. Sort only identical pairs of (global B degree,column rank):
three B9 rank4 orbits for A9/9/10; the two B9 rank4 orbits for G7; no pair of
rank4 orbits for GM; and each pair of B9/B10 rank4 orbits separately for G6.
In particular the middle rank4 slots of GM have different global degrees.

The direct producer checks the row margins and all36 A-pair bounds.
The separate set-defined audit joins two-column vectors against the complete
nonnegative deficit target domain. Deficits are constant on the twelve A pair
orbits. A9/9/10 has total6 or9, hence78 or364 weak-composition targets.
G7/GM are tight, with one target; G6 has one unit of orbit deficit, with12
targets. The whole typed column domains, incidence sets and native input
streams agree between these different algorithms.

| Mode | Complete column choices | Row-margin matches | Frames |
|---|---:|---:|---:|
|A9910|2,781,240|169,963|439|
|G7|3,413,340|244,161|28|
|GM|6,667,920|480,792|56|
|G6|2,446,227|176,112|222|
|Total|15,308,727|1,071,028|745|

These are marked choices and frames; they are not counts of nonisomorphic
graphs or witness constructions.

## 4. All K completions and literal hosts

There are22 B edge orbits: four triangles and three shifts on each of six
orbital pairs. The weighted producer enumerates every internal triangle choice
and every0..3 cross weight, solves the four required degree equalities, and
expands every mask of each required weight. The separate native program scans
ALL4,194,304 binary22-bit words for each mode. Their whole sorted K word
streams agree, not just their counts or hashes.

Necessary K-only page cuts are common red neighbors<=3 and common blue
neighbors<=5-max(0,9-s_b-s_c) on a blue K spine. The latter reserves one blue
page for x and at least max(0,9-s_b-s_c) blue pages in A.

The component checker caches exact integer bit sets for each B-pair color and
local page count, intersects the exact B page predicates for each frame, then
checks mixed A-B spines. It is an exact filter, with no approximate operation.
The independent native checker constructs all22 adjacency rows, checks every
A AND B global degree and total204, then checks all ordinary spine predicates
until it finds a violation. Both complete outcome streams agree entry by entry.

| Mode | K degree words | K local-cap words | Host choices | Valid |
|---|---:|---:|---:|---:|
|A9910|16,536|15,768|6,922,152|0|
|G7|11,250|7,452|208,656|0|
|GM|15,368|12,690|710,640|0|
|G6|15,368|12,894|2,862,468|0|
|Total|58,522|48,804|10,703,916|0|

The cached component calculation reports no B-pair survivor for the first
three modes and12 for G6, all rejected at mixed spines. The independently
compared claim is the entire K domain and whole-host outcome stream. The
component B-only survivor classification itself has not been separately
replayed by a third algorithm.

The initial uncached Python host loop hit its fixed25-second program guard.
That run is INCOMPLETE, is preserved privately, and supports no exclusion.
The expensive loop is paused. The bit-set algorithm completed the same marked
domains at unchanged25/30-second program/child guards. No resource settings
were increased. The four fresh native scans and whole-stream comparisons,
together with the preceding completeness bridges, give exclusion A.

## 5. Ordinary low-profile proof B

For any simple22-vertex graph define epsilon_uv=3-c_red on a red spine and
6-c_blue on a blue spine. Write W=sum_{u<v} epsilon_uv and
D_v=sum_{u!=v} epsilon_uv. Double counting monochromatic triangles and local
neighborhood edges gives

    2W=-6468+120E-3*sum_v d_v^2,
    D_v=2E-294+38d_v-d_v^2-2*sum_{u in N(v)} d_u.

For root degree9, D_x=2(E-D_A)-33. These are the scalar/row consequences
of the general degree-sensitive deficit structure in
[review9537](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/cross-leaf-audit/REVIEW.md),
and are rederived here rather than claimed as new identities. Valid hosts have
every epsilon nonnegative. In profile7^3,8^3,9^1,10^15, E=102 and W=6.
Since0<=D_x<=6, D_A must be84. Thus A consists of one8-orbit L and two
10-orbits; B consists of one7-orbit and three10-orbits. The cut bounds force
h=12, k=30, K5-regular, and D_x=3. Columns have ranks2,5,5,5 and overlap93.

If the H degree on L is2, A capacity is87, impossible. Otherwise it is3,
capacity is93, and ALL A-pair inequalities are equalities. The other two H
orbital degrees are2 and3; call those orbits M and T.

All root deficit is3: the three root-to-M spines each have deficit1, and the
other root spines have deficit0. Remaining total deficit is3. Every unordered
pair orbit has length3 and constant integer deficit, so precisely one nonroot
pair orbit has deficit1. For a vertex of L, its contribution is at most2
(two incident edges in a triangle orbit), and its root deficit is0. Hence
0<=D_v<=2 on L.

Let ell=0 or2 be the number of H neighbors of v inside L, and let q be its
number of neighbors in the B7 orbit. The global neighbor degrees are

    9; ell copies of8; 3-ell copies of10;
    q copies of7; 4-q copies of10.

The row identity gives D_v=-8+4ell+6q. Its entire ell/q table leaves only
ell=2,q=0,D_v=0. Therefore L is a triangle and has no red adjacency to B7.
Its incidence rows have rank4 and see only columns of rank5, making their
full Gram row sum20.

Each L vertex has one H neighbor in a high-degree orbit. Summing its exact
lambda bounds and adding the diagonal4 gives22 minus that neighbor's H
degree. Equality to20 forces this neighbor into M. Thus H consists of the
triangles L,T, a perfect matching L-M and a perfect matching M-T. M has no
internal edges. Directly in this shape,

    G_X(L pair)=1,  G_X(L,M)=2 on ALL nine pairs,
    G_X(M pair)=5.

For a C3 column orbit, if its column has m neighbors in an A orbit, each
unordered pair in that A orbit has overlap binom(m,2) across its three
columns. This follows by counting all three pair occurrences and C3
invariance; no normalization assumption is needed.

Let r_1,r_2,r_3 be the L weights of the three high B column orbits. The low B
weight is0. Then sum r=4 and sum binom(r,2)=1 force weights2,1,1. Name the
weight2 orbit U and the other two V,W. Let m0,mU,mV,mW be their M weights.
The low B column has rank2 and no L neighbor, so0<=m0<=2. The V,W columns
have rank5, L weight1 and at most three T neighbors, so1<=mV,mW<=3.

M row rank7 and the L-M Gram block2 give

    m0+mU+mV+mW=7,
    2mU+mV+mW=6,
    mU=m0-1.

If m0=1, the weights are1,0,3,3 and their binomial sum is6. If m0=2,
the weights are2,1,1,3; 2,1,2,2; or2,1,3,1, with binomial sums4,3,4.
No case supplies the required M-pair overlap5. This proves B without an
H representative census, incidence enumeration, K census, host completion,
or historical minimum-eight classification.

`low_profile.py` checks all35 root placements, the eight deficit rows, all4096
local H words, all18 forced labeled H shapes, all four scalar cases, and
all512 labeled column seeds (4608 pair checks). Its entire1722-byte record
agrees in normal and optimized Python, SHA256
55f570399212f2f2442abf410b4324488891bb056012d8c7ee945a637f5f934e.
These are checks of the ordinary proof, not premises replacing its argument.

## 6. Ordinary seven/nine-profile proof C

Now E=102 and W=15. The three possible A mark triples with0<=D_x<=W are

    7,9,10 (D_A=78,D_x=15);
    7,10,10 (D_A=81,D_x=9);
    9,9,10 (D_A=84,D_x=3).

There are only two free9-orbits, so A9/9/9 is not an available placement.

For every vertex, D_v has the parity of d_v: the incident red and blue page
sums are twice the numbers of edges in the respective monochromatic
neighborhoods. Consequently, for any ordinary22-vertex host and root of
degree9,

    sum_{u in A,b in B} epsilon_ub = D_A-9 (mod2).

Indeed sum_{u in A} D_u equals the root-red deficit27-2h, twice the A-pair
deficit, and the mixed deficit. If D_A is even, mixed deficit is odd and hence
positive in a valid host. For the A7/9/10 placement W=D_x, all nonroot
deficits would vanish. Its even D_A gives a contradiction. With the C3
symmetry this argument also gives the necessary bound W-D_x>=3 whenever
D_A is even; the parity identity itself does not require symmetry.

For A9/9/10 the cut gives h=12,k=30 and B7/10/10/10. Column ranks2,5,5,5
have overlap93. A capacity is90 or93, forcing the10-orbit to have H degree2,
the9-orbits to have H degree3, and all A pairs to be tight. For a9-vertex u,
its rank5 diagonal plus the sum of its lambda bounds is23. But weighting its
column incidences by ranks2/5 gives25-3q, where q is its B7 neighbor count.
This cannot be23 for any integer q.

It remains to treat A7/10/10. Denote its7-orbit by L. Every L pair must be
red, since a blue pair has lambda=-1-C_H<0. Thus L is a triangle. B has
marks9,9,10,10. The entire cut domain is h9/k30 or h12/k33. The root deficit
is9, leaving total nonroot deficit6, or two units of length-three pair-orbit
deficit.

If h=9, the B columns are4,4,5,5, with overlap96. The A capacity can reach96
only when H has orbital degrees3 on L and1,2 on the two high orbits, and
then all A pairs are tight. The L incidence row rank is3. Because A-pair
deficits are zero, only mixed deficit orbits can contribute to D_L. Two
remaining units give D_L<=2. The row formula gives D_L=7-2q, where q counts
its B10 neighbors, forcing q=3,D_L=1. Thus L sees only the two rank5 column
orbits and its full Gram row sum is15.

If a is the H degree of its unique external H neighbor, the full tight Gram
row sum is16-a. Hence a=1. H is the triangle L, a matching L-M to the
H-degree1 high orbit M, and an isolated triangle T of H degree2. The
incidence rows on T have rank7, but their red pair bounds are1. Two7-subsets
of a12-set intersect in at least2, a contradiction. Equivalently the complete
C3 weight calculation gives two cases with T-pair overlap3 instead of1.

If h=12, orbital H degrees are2,3,3. H degree2 on L gives A capacity69,
below the minimum possible column overlap72. So L has H degree3; call the
H-degree2 and H-degree3 high orbits M,T. A capacity is78. Let a=2 or3 be
the H degree of the unique external H neighbor of an L vertex. Its diagonal
plus total lambda bound is16-a.

The K degree marks are at least5 and sum22. The complete capacity-retained
column rank cases are

    4,4,3,5 (G7), 3,4,4,5 (GM),
    3,3,5,5 (both K6s at the B9 orbits), 4,4,4,4 (G6).

A K7 at a B9 orbit gives overlap81>78. The four displayed overlaps are
75,75,78,72, with total A-pair deficits3,3,0,6 respectively.

Record every nonroot deficit orbit by a weighted edge on the seven free
vertex orbits. An internal triangle gives a loop, contributing twice its
weight to the projected degree. A cross orbit contributes its weight once
at each endpoint. The total edge weight is2. Its degree at an orbit has
parity d_v-epsilon_xv. On L,M,T these required parities are1,1,0; on a B
orbit of column rank s they are s+1 modulo2.

In G6 there are six required odd orbit classes. Two edge units can have at
most four odd classes, so G6 is impossible. In G7/GM there are four odd
classes, forcing the two edges to form a matching on those classes. Since
exactly one unit is inside A, it is L-M; the other is between the two odd B
orbits. Thus all mixed deficits vanish, L has nonroot deficit1 and q=3.
All L incidence is in the two high B orbits. Tight L-pair overlap1 and row
rank3 give their L weights2,1; name those column orbits U,V.

The L Gram row is now16-a-1=15-a. In G7, weighting ranks3/5 allows values
11 or13, so a=2 and U has rank5,V rank3. In GM, weighting ranks4/5 allows
13 or14, so a=2 and U has rank4,V rank5. In either case H has triangles
L,T and matchings L-M,M-T. Its L-M bound row total is4; the single A deficit
reduces the actual L-M Gram row to3. Its M-pair and T-pair bounds remain5
and1. Let m0,m1,mU,mV be M column weights. Then

    sum m=7, 2mU+mV=3.

For G7, the column ranks4,4,5,3 and low weights0,0,2,1 force
mU=mV=1, (m0,m1)=(2,3) or(3,2). Their M-pair binomial sum is4, not5.
For GM, ranks3,4,4,5 permit (mU,mV)=(0,3) or(1,1). The latter again has
M-pair sum4. In the former case M-pair sum5 forces m0=m1=2, leaving T
weights1,2,2,1 and T-pair sum2, not1.

Finally, for columns3,3,5,5 all A pairs are tight. As in the h9 argument,
two nonroot units imply D_L<=2, hence q=3. The L row has only rank5
neighbors, so its full Gram row is15; the tight bound row is16-a, with
a=2 or3, impossible. This exhausts proof C without an incidence, K or
whole-host census, or the historical classification.

`seven_nine_profile.py` literally checks all4096 H words in each marked
case,58 tight A9/9/10 words and348 Gram rows, the six labeled H9 forced
shapes, all42 H12 low-triangle equality words, all406 projected two-unit
deficit assignments in each of four column classes, and all2/2/5 scalar
weight cases. Its complete3225-byte record agrees in normal/optimized Python,
SHA25666e1994326f250da5ec76e17e5123244f82aa1686f5bce3ebfa450bbf84d4f13.
These computations check an ordinary proof, rather than supply a computational
completeness premise in place of it.

## 7. Conditional classification-free family consequence

Credit [lemma9596](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_edge99_exclusion/PROOF.md)
for its already published consequence that every valid C3 host of this cycle
type must have E=102. Credit only the lower7 main bound of lemma7526 and the
classification-free upper10 main bound of lemma8012. The fixed root has
degree9, and the seven free degree marks in7..10 sum65. There are413 ordered
marks in five histograms:

    9^16,10^6; 8^3,9^10,10^9; 8^6,9^4,10^12;
    7^3,9^7,10^12; 7^3,8^3,9^1,10^15.

Exclusion A and ordinary proofs B,C remove the first and both7-degree
profiles, leaving exactly two
NECESSARY profiles:

    8^3,9^10,10^9; 8^6,9^4,10^12.

Existence in either remaining profile is open here.

The external theorem premises for this consequence are explicit; the prior entire computations have
not been replayed here. No published reviewer verdict on earlier99-edge,
regular or repeated-leaf claims transfers to these candidates.

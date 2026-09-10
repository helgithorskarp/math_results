# Four high forests remain: a distant-neighborhood partition obstruction

Current status: the [whole-boundary theorem](boundary_exclusion.md) excludes
every case with thirteen degree-eight vertices, improving the degree bound
to n8<=12. The proof and evidence below are preserved as earlier results.

**Theorem.** A finite simple graph of order 54, size 187 and girth at least
five cannot have its thirteen degree-eight vertices induce

    H = 2P3 + P2 + 5K1.

Consequently the entire thirteen-high-vertex boundary is reduced to

    5P2+3K1,  P3+3P2+4K1,  6P2+K1,  P3+4P2+2K1.

All four forests remain undecided. The unrestricted target still has working
bounds **185 <= ex(54,{C3,C4}) <= 187**. This theorem covers every realization
of the excluded forest, including graphs with distant degree-seven pairs.
It does not assume that any graph is determined by aggregate counts.

The last step below is a short human proof. It imports the preceding
[computer-assisted four-profile reduction](shared_center_restriction.md),
whose complete 124-refutation reproduction is preserved. No new solver
infeasibility status is a premise.

## 1. Definitions and the two epsilon balances

Import the degree counts `(n6,n7,n8)=(17,24,13)` and the
[all-sink theorem](boundary_sinks.md). Put `T=V8`, `L=V6 union V7`,
`C(v)=N(v) intersect T`, `c(v)=|C(v)|`, and `h(t)=degree_H(t)`.
A pair is *distant* when its distance is greater than two; `F(v)` is the
set of vertices distant from v. Every `F(v)` lies in L.
Write

    w(v)=d(v)-6,                 s(v)=sum_{u adjacent v} w(u),
    epsilon(v)=s(v)-8  (v in V6),
    epsilon(v)=s(v)-7  (v in V7).

All high vertices have s=5. The [weighted gap identity](proof.md) gives

    sum_V6 epsilon^2 + sum_V7 epsilon(epsilon-1)
      + 2 e(M[V7]) = 9,                                      (1)

where M is the distant-pair graph on L. Every term is nonnegative, since
epsilon is an integer. In particular `sum_V6 epsilon^2 <= 9`.

We will also use the exact balances

    sum_L epsilon = 7,                sum_L c epsilon = 2m,   (2)

where m is the number of edges of H. To check the first, the sum of all
s values is `sum_v d(v)(d(v)-6)=24*7+13*16=376`. Remove the high contribution
65 and the low baselines `17*8+24*7=304`, leaving seven.

For the second, fix a high vertex t. It has `3+h(t)` six-neighbors and
`5-2h(t)` seven-neighbors. The local weighted identity in the all-sink proof
says `sum_{u adjacent t} s(u)=50-5+7*2=59`. Their baseline contribution is

    5h + 8(3+h) + 7(5-2h) = 59-h.

Thus `sum_{low u adjacent t} epsilon(u)=h(t)`. Sum over t to obtain the
second balance. In our forest m=5, so (2) yields

    sum_V6 (c-3)epsilon + sum_V7 (c-3)epsilon = -11.           (3)

## 2. The individual distant-neighborhood partition

For every y of degree seven, the sets

    C(y), together with C(u) for all u in F(y),

**partition T**. Empty sets are allowed in this statement.

Here is a matrix proof, including the diagonal correction. Let A be the
adjacency matrix, let M be the distant-pair adjacency matrix on L, and set
`D=diag(8-d(v):v in L)`, `K=D+M`. Unique paths of length at most two give

    A^2+A-7I = J - diag(0_T,K).                              (4)

Both sides commute with A. At an entry (t,v) with t high and v low this
implies

    (N^T K)_(t,v) = 8-d(v),

where `N_(v,t)=[t in C(v)]`. Transposing gives, entry by entry,

    (8-d(v))[t in C(v)] + sum_{u in F(v)} [t in C(u)]
      = 8-d(v).                                             (5)

For d(v)=7 the right side is one, proving the partition. For d(v)=6,
the far neighborhoods instead cover the complement of C(v) exactly twice.
These are individual incidence statements, not just their summed versions.

The ball count for a degree-seven y is

    |F(y)|=53-(6*7+s(y))=4-epsilon(y).

Summing the partition sizes and subtracting three times this count yields

    sum_{u in F(y)} (c(u)-3) = 1-c(y)+3epsilon(y).             (6)

In particular this identity remains valid when F(y) contains degree-seven
vertices. This is why no restriction on e(M[V7]) is needed.

## 3. Three profiles are impossible immediately

The preceding complete shared-center reduction leaves only the following
four global histograms. Notation c:n means n vertices with c high neighbors.
No individual center-state restriction beyond this table is needed here.

| Profile | V6 c histogram | V7 c histogram | R=sum_V6(c-3)^2 | P=sum_L max(c-3,0) |
|---|---|---|---:|---:|
| 1 | 2:2, 3:15 | 1:6, 2:15, 3:3 | 2 | 0 |
| 2 | 2:2, 3:15 | 0:1, 1:3, 2:18, 3:2 | 2 | 0 |
| 4 | 2:3, 3:13, 4:1 | 1:5, 2:17, 3:2 | 4 | 1 |
| 6 | 2:4, 3:11, 4:2 | 1:4, 2:19, 3:1 | 6 | 2 |

Since the left side of (6) is at most P,

    epsilon(y) <= floor((c(y)-1+P)/3).                       (7)

In profiles 1,2,4, every seven-vertex with c<3 has epsilon<=0. Vertices
with c=3 contribute zero to `sum_V7(c-3)epsilon`. Therefore this entire
seven-vertex sum is nonnegative. Equation (3) forces
`sum_V6(c-3)epsilon <= -11`. But Cauchy--Schwarz and (1) give

    (sum_V6(c-3)epsilon)^2 <= 9R <= 36 < 121,

a contradiction. This excludes all of profiles 1,2,4.

## 4. The fourth profile requires at least four special vertices

In profile 6, (7) gives epsilon<=0 for seven-vertices with c=1 and
epsilon<=1 for those with c=2. The sole seven-vertex with c=3 again
contributes zero to (3). Let Q be the set of seven-vertices y with

    c(y)=2,                      epsilon(y)=1.

All seven-vertex contributions to (3) outside Q are nonnegative, while
each member of Q contributes -1. Hence, if |Q|<=3, (3) implies

    sum_V6(c-3)epsilon <= -8.

Cauchy--Schwarz would then give `64 <= 9*6=54`, impossible. Thus

    |Q| >= 4.                                                (8)

## 5. Individual partitions allow at most two

Let a,b be the two degree-six vertices with c=4 in profile 6. All other
low vertices have c<=3. For y in Q, the ball count gives |F(y)|=3, and
the partition gives `sum_{u in F(y)} c(u)=13-2=11`. The only way to
obtain eleven from three low vertices is 4+4+3. Consequently

    F(y) = {a,b,z_y},          c(z_y)=3.

The vertex z_y may have degree six **or seven**; both possibilities are
included. The partition implies that C(a) and C(b) are disjoint. Their
complement R0 in T has five points, and

    C(z_y) = R0 minus C(y).

For distinct y,y' in Q, the vertices z_y,z_y' are distinct. Otherwise
C(y)=C(y') would be the same two-point set, making a four-cycle. Distinct
vertices have at most one common high neighbor, also by the absence of
four-cycles. Thus

    1 >= |C(z_y) intersect C(z_y')|
      = 5 - |C(y) union C(y')|
      = 1 + |C(y) intersect C(y')|.

The two-point sets C(y), y in Q, are therefore pairwise disjoint subsets
of a five-point set. This proves `|Q|<=2`, contradicting (8).

All four residual profiles are excluded. Together with the complete prior
reduction, this excludes the whole forest stated in the theorem.

## 6. Rank information and the remaining search

The initially proposed rank route is valid, though the partition argument
above supplies the exclusion. The earlier spectral theorem gives
`nullity(A^2+A-7I)>=24`. Subtracting one high row in (4) from all low rows
shows `rank(A^2+A-7I)=1+rank(K)`, so

    rank(K)<=29.

By (1), M[V7] has at most four edges and hence an independent set of size
at least twenty. Eliminating twenty of those indices from K leaves an
integral 21-by-21 Schur complement of rank at most nine. If M[V7] is
empty, its full identity block can be eliminated, giving

    rank(2I_17+M66-M67 M67^T)<=5.

No definiteness assertion is made. These are necessary conditions, not
realization certificates. They remain available for the other four forests.
Their complete histogram cover has 49+29+24+13=115 cases, with no new
claim that any case is realizable.

## 7. Exact checks, prerequisites and scope

Run, with CPython 3.11.2 and only the standard library:

    python3 verify_distant_partition.py

The verifier checks the general entrywise partition identity on actual
girth-five graph controls, compares the four histograms with the published
complete residual cover, verifies the epsilon balances' arithmetic, and
independently enumerates both the small integer quadratic bounds and the
five-point set-packing obstruction. It uses explicit failures, including
under `python3 -O`. These checks support the written proof; they do not
formally prove it or enumerate all target graphs.

The inherited four-profile reduction remains computer-assisted. Its
source, complete coverage checks, 124 formula/proof hashes and prior fresh
replay are preserved in `shared_center_*`, `shared_star_*`,
`verify_shared_center.py`, and `reproduce_shared_center.py`. Run
`python3 verify_shared_center.py` for the finite cover check, and use the
reproduction command documented in [that proof](shared_center_restriction.md)
to regenerate every refutation with the pinned SAT solver and separate
DRAT checker. No private partial search from that pass is a premise.

The other imported prerequisites are the degree and weighted-gap theorem,
the all-sink theorem, and the prior five-forest reduction. The published
value ex(53,{C3,C4})=181 remains an external input. This new closing argument
has internal exact checks but no independent external review or formalization.
Exploratory SAT/MILP pilots, including timeouts and fractional relaxations,
are not part of the proof and are kept outside the repository.

Polynomial identities involving a Moore-type matrix and a distant-pair
matrix are established techniques; see, for example,
[Delorme and Pineda-Villavicencio, On graphs with cyclic defect or excess](https://arxiv.org/abs/1010.5841).
Their regular cyclic setting is different from this irregular all-sink
boundary. The specific partition obstruction and forest exclusion are new
to this campaign; no historical priority claim is made.

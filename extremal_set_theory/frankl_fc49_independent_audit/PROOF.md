# Finite FC audit and an explicit nineteen-point witness

## Attribution and scope

Mingchang Liu's September 2026 manuscript establishes `FC(4,9)=16` and
refutes Pulaj–Wood's lexicographic extremality conjecture. The fifteen-block
configuration, auxiliary families, positive weights, decision tree, and full
classification belong to that work; see [SOURCES.md](SOURCES.md).

This contribution supplies a complete execution replay of that classification,
separate verification of its decisive positive and negative witnesses, and a
smaller explicit negative extension. The upper-bound enumeration is the
upstream implementation, not an independently reimplemented classification.
The original manuscript's asymptotic and general-uniformity theorems are outside
this audit. We make no priority or minimal-universe claim for the tag device.

A configuration on support U is FC if every finite union-closed extension has
an element of U in at least half its members. The extension may use new points.
The examples below make only the original nine points scarce. In fact all ten
new points in the nineteen-point example are abundant.

## Antichain compression of a negative extension

Let C be a union-closed family on U containing the desired generators. Suppose
that B_1,...,B_s are union-closed families on U and

    {c union b : c in C, b in B_i} is contained in B_i.

Write rho_u(B)=2|{b in B:u in b}|-|B|. Suppose nonnegative integers k_i obey

    rho_u(C) + sum_i k_i rho_u(B_i) < 0   for every u in U.

Choose q new points Y and an integer 1 <= r < q with binomial(q,r) >= sum k_i.
Assign distinct r-subsets T of Y to the types i, with k_i tags of each type.
Define F by its exact intersections with Y:

* at the empty trace, its U-slice is C;
* at an assigned trace of type i, its U-slice is B_i;
* at every trace with more than r points, its U-slice is the full cube 2^U;
* at every other trace, its slice is empty.

This is union-closed. Two distinct assigned traces have union of size greater
than r, so their union lands in a full slice. Equal assigned traces use closure
of B_i. A union with an empty trace uses C-union-B_i stability. A full trace
stays full under union. Two empty traces use closure of C. These cases exhaust
all unions of members.

Every full slice has zero imbalance on U. Consequently F contains the desired
generators and has imbalance rho(C)+sum k_i rho(B_i) on U. Singleton tags are
therefore unnecessary: a large collection of tag points can be replaced by
enough points to support an antichain of the requisite size.

## The explicit instance

Use one-based original labels 1,...,9. The fifteen four-sets are

    1237,1247,1347,2347,
    1589,2589,3589,4589,1689,2689,3689,4689,
    5689,5789,6789.

Let C be their union closure together with the empty set. It has 100 members.
For i<=7, let K_i consist of the displayed generators containing i; put
K_8=K_9={589,689}. For each i define

    B_i = {S subseteq [9] : i notin S, or K subseteq S for some K in K_i}.

These are Liu's nine admissible families. Their sizes are

    (356,356,356,356,319,319,369,352,352).

The script verifies closure, C-union-B_i stability, and every entry of their
imbalance matrix, which is recorded in EXPECTED.json. Use

    k = (3,3,3,3,15,15,5,41,41),  sum k_i = 129.

The original singleton-tag extension uses 129 new points. Here choose q=10 and
r=5. In lexicographic order on increasing tuples of {10,...,19}, assign the
first 129 five-sets to the nine types in consecutive groups of lengths k_i.
Use the preceding slice definition. The number of full slices is
sum_{j=6}^{10} binomial(10,j)=386, giving

    |F| = 100 + sum_i k_i |B_i| + 386*512 = 242283.

On the original coordinates, the exact imbalance vector is

    (-5,-5,-5,-5,-31,-31,-55,-49,-49).

Thus all nine original elements are strictly scarce. This directly proves
that the fifteen-block family is Non-FC and hence `FC(4,9)>=16`.
Deleting the block 6789 gives the fourteen-block negative comparison for the
lexicographic conjecture. This family still has support [9], and the very same
extension contains it and witnesses scarcity on that support.

### Verification directly on the global family

`witness.py` enumerates the indicator f of F on all 524288 subsets of [19],
checks generator containment, and counts all nineteen frequencies directly.
It verifies union closure by exact integer OR convolution. If

    h(T) = sum_{A union B = T} f(A)f(B),

then the subset zeta transform satisfies

    sum_{T subseteq S} h(T) = (sum_{A subseteq S} f(A))^2.

Squaring the zeta transform of f and applying subset Mobius inversion therefore
computes h exactly. Closure is equivalent to h(T)=0 at every absent T. The
check covers all 58,701,052,089 ordered pairs without enumerating them one at a
time. It uses unbounded Python integers, not floating point or fixed-width
convolution. All 256 families on three points are compared with direct pair
enumeration. Removing the full set from the actual nineteen-point family is a
negative control and is rejected.

This check does not require a theorem of alternatives or the necessity
direction of Poonen's characterization: it checks an actual extension.

## The positive lexicographic witness

The first fourteen four-subsets of [9] in ordinary tuple lexicographic order are

    1234,1235,1236,1237,1238,1239,
    1245,1246,1247,1248,1249,1256,1257,1258.

They contain an eight-point, twelve-block configuration with masks

    15,23,39,71,135,75,139,83,147,99,163,195

after the zero-based embedding (0,1,4,5,6,7,2,3). Its integer weights are
(6,6,4,3,3,3,4,4), of sum W=33. Masks use bit i for zero-based element i.

For any union-closed family B on these eight points stable under union with
each generator, set

    q(S)=2 sum_{i in S} w_i-W.

It suffices to prove sum_{S in B} q(S)>=0 for every such B. Indeed, decompose
an arbitrary union-closed extension into exact outside-coordinate slices.
Each slice is union-closed and generator-stable. Summing the inequalities over
the slices gives a weighted-average abundance inequality on the original eight
points. Since the weights are nonnegative and not all zero, one point is
abundant. This also proves FC for every configuration containing this one.

### Tree and checked flows

The supplied 3015-node tree is copied unchanged from Liu's MIT-licensed release.
At each node, P and Z denote subsets forced present and absent. The new checker
computes closure of P under unions and generator unions using a queue. A branch
on s covers s present and s absent. An orbit branch covers s present and its
whole orbit absent: any family meeting the orbit can be carried to one containing
s by a coordinate permutation preserving generators, weights, P and Z. The
checker enumerates and checks those permutations explicitly. A conflict leaf
requires P intersect Z nonempty.

For a flow leaf introduce one network vertex per S subseteq [8], a source a,
and a sink b. Put Nminus=sum_{q(S)<0} -q(S)=1254 and
M=1+sum_S |q(S)|. Arcs are

* a->S of capacity -q(S) if q(S)<0; S->b of capacity q(S) if q(S)>0;
* a->S of capacity M for S in P; S->b of capacity M for S in Z;
* S->S union T of capacity M for each generator or forced-present set T.

Self-loops are omitted. Every admissible B compatible with the node defines a
cut with no capacity-M arc crossing, and cut capacity Nminus+sum_{S in B}q(S).
Any feasible flow of value at least Nminus proves the desired lower bound.

OR-Tools supplies candidate arc flows. `lex_flow.py` checks, using Python
integers, each capacity bound and every conservation equation, and derives the
flow value from the checked balance vector. It does not rely on the oracle's
reported optimum as evidence. All 1508 leaves pass, with 6,204,558 arc values
checked. The checker uses all forced-set implications, rather than the original
implementation's seed list, and a queue closure rather than its closed formula.
The mathematical tree semantics remain shared with the original proof.

### Separate Horn/PB proof

`positive_sat.py` uses Boolean variables x_S for all 256 possible sets. It
encodes union closure by -x_A or -x_B or x_{A union B}, generator stability by
-x_S or x_{S union G}, and strict negative share by sum q(S)x_S <= -1.
For the latter, replace each negative coefficient q by the positive coefficient
-q on literal -x_S. The resulting upper bound is Nminus-1=1253.

PyPBLib's BDD encoding supplies auxiliary CNF variables. Glucose produces a
DRAT refutation, DRAT-trim extracts a RUP-only text LRAT proof, and the small
`strict_rup.py` checks every hint and requires an actual propagation conflict,
including for the final empty clause. This route does not use the decision tree,
its symmetry branches, or a flow algorithm. Its extra encoding trust boundary
is PySAT/PyPBLib's PB-to-CNF translation; the flow route does not share it.
The large proof files are regenerated locally and are not published here.

Together the positive lex segment and negative comparison refute Pulaj–Wood's
Conjecture 1 independently of the full sixteen-block upper-bound computation.

## What the full upstream replay establishes

The original seven-point enumeration starts with the empty family, adds every
missing four-set to each retained Non-FC orbit, and retains only candidates
whose one-block deletions are all still Non-FC. Every retained candidate is
classified by a positive tree or an actual negative dual certificate. Induction
on the number of blocks proves coverage. Canonicalization sorts degree classes
and exhausts permutations within them, including unused vertices.

For eight points and m blocks, choose a minimum-degree vertex of degree d<=m/2.
Its deletion is a seven-point Non-FC family. All d-subsets of incident triples
are tried; only already-FC restrictions and impossible degree conditions prune.
The replay compares generated orbit lists entry by entry with certificate
records. It re-establishes FC(4,8)=12 and classifies the Non-FC eight-point
boundary layers of sizes 9,10,11, with 52,13,3 orbits respectively. Additional
hereditary filters and explicit embeddings into positively certified patterns
are regenerated; a retained unclassified candidate is never assumed negative.

If sixteen four-sets on nine points were Non-FC, every vertex-deletion
restriction would be Non-FC. Since FC(4,8)=12, each degree is at least 5. The
degree sum is 64, so a minimum-degree vertex has degree 5,6,or 7. Its deletion
is one of those 68 boundary types. The final search tries every increasing
selection of the required incident triples, pruning only FC restrictions and
impossible minimum-degree conditions. It has no survivors. This proves the
upper bound, conditional on the exact computational chain being implemented
correctly; the lower witness supplies equality.

`replay_upstream.py` pins the source commit, checks tracked inputs, runs the
original verifier, and summarizes all 4333 certificate records and final
traversals. It is execution reproduction plus source inspection, not a second
orbit generator or formalization. Compiler, standard-library, hardware, and
upstream enumeration/checker correctness remain trust boundaries for the
unrestricted upper bound. The independent nineteen-point and lex checks do
not depend on those enumerations.

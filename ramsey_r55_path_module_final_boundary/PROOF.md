# A general compatibility boundary for the path/module approach

This note records a failed endpoint approach. It gives no good43, no
good43 nonexistence theorem, and no quantitatively finishable reduction of
that class. The two-pass campaign trial ends with its final gate missed.

The auxiliary statement below keeps actual Ramsey avoidance, rather than
replacing it by the necessary system Q tested in the preceding pass. Its
parameters have growing clique size. It does **not** apply to clique size
five and order 43. It is a direct combination of classical random-graph
estimates, not a new Ramsey bound or a claim of historical priority.

## 1. Precise statement

A graph is `(k,k)`-good if it contains neither a clique nor an independent
set of size k. Red means edge, blue means nonedge. A proper nontrivial
module in H is a set M with 2<=|M|<|V(H)| such that every vertex of H-M is
complete or anticomplete to M. Here prime means having no such module.

**Compatibility proposition.** For every integer t>=16, put

    n=2^t,       k=2t+1,       m=1024t.

More than a fraction 511/512 of all labelled graphs on n vertices satisfy
all three properties simultaneously:

1. They are `(k,k)`-good.
2. Every m-subset contains an induced red P5 and an induced blue P5.
3. Every induced subgraph on at least 5n/8 vertices is prime.

Consequently such graphs exist. Every induced subset that avoids both P5
and complement-P5 has at most m-1 vertices, and deleting any at most 3n/8
vertices preserves primeness. Property 2 also applies to every m-subset of
every colour neighbourhood, since it applies to all m-subsets of V(G).

These are existence and probability statements in an unrestricted labelled
probability space. No graph, automorphism, special family, incomplete
catalogue, construction seed, or candidate packing is fixed. No literal
large graph is generated or claimed as a supplied witness.

## 2. One probability space and the Ramsey event

Give each unordered vertex pair an independent fair bit. All events below
refer to this same graph. Independence between the three kinds of failure
is neither asserted nor needed: the final step is a union bound.

For any k-set the probability of being monochromatic is
2*2^(-binom(k,2)). Therefore

    P(not (k,k)-good) <= 2 binom(n,k) 2^(-binom(k,2))
                       <= 2 n^k / (k! 2^binom(k,2))
                       = 2/k!,                                  (1)

because t(2t+1)=binom(2t+1,2). This is the classical first-moment Ramsey
argument of Erdős. At t>=16 its bound is less than 2^(-11).

## 3. Both induced paths in every m-set

We first record a deterministic collection of tests for a fixed m-set S.
Greedily take five-sets whose ten pairs have not been used before, until
none is available. Distinct chosen tests share no unordered pair, although
they may share a vertex. This choice depends only on the complete labelled
set, not on the random graph.

The graph of unused pairs is K5-free. Such a graph has at most 3m^2/8
edges. For completeness, start with weights x_v=1/m and the objective
sum_(uv edge) x_u*x_v. For two nonadjacent positive-weight vertices, move
all weight from one to the other, choosing the direction which does not
decrease the objective. There is no term x_u*x_v, so this comparison is
linear and one positive weight disappears. Iteration leaves a clique of
r<=4 positive weights. On this support the objective is
(1-sum x_v^2)/2 <= (1-1/r)/2 <=3/8. The initial objective was e/m^2.
This proves the required special Turán bound without a classification.

If b tests were chosen, they used exactly 10b pairs, hence

    10b >= binom(m,2)-3m^2/8,
    b >= m(m-4)/80.                                             (2)

A uniformly random five-set is an induced red P5 with probability

    p=(5!/2)/2^10=15/256.

There are 5!/2 labelled paths because reversal is the only duplication of
a path ordering. The same probability holds in blue. The test events in
one fixed colour are independent: each reads a disjoint set of physical
edge bits. Thus, for S and either required colour, the probability of no
such path is at most

    (1-p)^b <= exp(-p b) <= exp(-3m(m-4)/4096).

Union over both colours and every m-set gives

    P(path property fails)
        <= 2 n^m exp(-3m(m-4)/4096).                            (3)

For m=1024t, the exponent after the factor 2 is

    m [ (ln(2)-3/4)t + 3/1024 ].

Use ln(2)<7/10. This follows, for example, since the first five terms of
the exponential series at 7/10 already sum to more than 2. Since

    (1/20-1/32)t - 3/1024 = 3t/160-3/1024 > 0  for t>=16,

(3) is at most 2 exp(-m t/32)=2 exp(-32t^2), which is less than 2^(-11).
The condition m<=n holds at t=16 and persists: if 2^t>=1024t then
2^(t+1)>=2048t>=1024(t+1).

## 4. All induced-subgraph module quantifiers

For nonempty M let U(M) consist of the vertices outside M that are
complete or anticomplete to M. A proper module M in an induced graph H
has nonempty H-M contained in U(M). Conversely M is a module in the
induced graph on M union U(M) whenever U(M) is nonempty. Thus it suffices
to rule out

    |M|>=2, U(M) nonempty, |M|+|U(M)|>=5n/8.                  (4)

This is a statement about every M, not a sample of deletion sets.

We use the following elementary fair-binomial tail bound:

    P(X-N/2 >= a) <= exp(-2a^2/N),  X~Bin(N,1/2).              (5)

Indeed E exp(lambda(X-N/2))=cosh(lambda/2)^N <=
exp(N lambda^2/8). The inequality log cosh z<=z^2/2 follows by integrating
tanh z<=z for z>=0 and by evenness. Markov's inequality with
lambda=4a/N proves (5). A binomial with success probability at most 1/2
is stochastically dominated by the fair binomial, by using the same
independent uniform numbers for its trials.

First exclude either of the following events:

- Some colour degree exceeds 9n/16.
- Some M with 2<=|M|<=31 has |U(M)|>=9n/16.

For each colour degree, (5) gives a bound exp(-n/128). For a fixed
j-set M, the indicators that its outside vertices are uniform are
independent with probability 2^(1-j). The relevant edge sets M times
each outside vertex are disjoint. Hence |U(M)|~Bin(n-j,2^(1-j)), and
the same tail bound exp(-n/128) applies for j>=2. There are at most
30n^31 such M and 2n colour degrees. The union bound is at most

    32 n^31 exp(-n/128).                                      (6)

Outside these events, (4) cannot hold when |M|<=31, because

    |M|+|U(M)| < 31+9n/16 < 5n/8.

The last inequality follows from n/16>31, valid at t>=16.
If U(M) is nonempty, choose u in it. Then M is contained in one of u's
colour neighbourhoods, so |M|<=9n/16. Consequently a remaining witness
to (4), with |M|>=32, has |U(M)|>=n/16.

For fixed disjoint sets M,U of sizes a,b, the probability that every
vertex of U is uniform to M is exactly 2^(-(a-1)b): for each of b
vertices, two of its 2^a possible contact words are uniform. These b
events use disjoint edge bits. There are at most 3^n ordered disjoint
pairs (M,U), obtained by assigning each vertex to M, U, or neither.
Thus the probability of a remaining witness to (4) is at most

    3^n 2^(-31n/16) < 2^(-3n/16),                            (7)

where 3^4=81<128=2^7 was used. This handles all large module sizes
and all outside uniform sets, without assuming they are mutually
independent and without any hypothesis on the graph inside M or U.

## 5. Uniform closure of the estimates

In (6), substituting n=2^t and using ln(2)<1 bounds its logarithm by

    31t+5-2^(t-7).

At t=16 this is -11. Its change from t to t+1 is
31-2^(t-7)<0 for every t>=16. Hence (6) is at most exp(-11)<2^(-11).
Bound (7) is also less than 2^(-11), already at n=65536, and decreases.
Bound (1) decreases with t and is less than 2^(-11) at k=33.
The path bound 2 exp(-32t^2) is less than 2^(-11) throughout the range.

The four displayed failure bounds sum to less than 4*2^(-11)=1/512.
This proves all the simultaneous properties in Section 1. The checks for
all t are the written monotonicity and induction arguments, not a finite
scan extrapolated to an infinite range.

## 6. What this says about cores, and what it does not say about 43

For these graphs a maximum induced subset avoiding both path patterns has
size at most 1024 log_2(n)-1, although large induced graphs remain prime
and actual Ramsey avoidance holds. In particular any decomposition which
starts by fixing one such core leaves at least

    n-1024 log_2(n)+1

vertices outside it. At the first stated parameter this is 49,153 of
65,536 vertices. As t increases the outside proportion tends to one.
This disproves a parameter-uniform hope of forcing a positive-fraction
path-free core from this type of Ramsey/path/module structure. It does
not refute an additional theorem specific to k=5 and n=43, and it gives
no lower bound on the complexity of a different decomposition.

At the actual endpoint, even the elementary Ramsey first-moment term is

    2 binom(43,5)/2^10 = 481299/256 > 1.

This upper bound on a failure probability is vacuous; it is not evidence
of nonexistence or a probability lower bound. Substituting k=5 into
k=2t+1 would give t=2, outside the proved range, and n=4 rather than 43.
There is no interpolation or small-parameter conclusion.

The attempted good43 route used a maximum path/antipath-free induced core
and the accepted bound 25, but established no constraints that finish
the cross-edges to its complement. The older disconnected/connected
path-hypergraph partition is also unclosed. A universal endpoint-specific
coupling lemma is still missing. The proposition above supplies a precise
general compatibility check, not that lemma. The final campaign gate is
missed and the lane is parked for reassignment within R(5,5).

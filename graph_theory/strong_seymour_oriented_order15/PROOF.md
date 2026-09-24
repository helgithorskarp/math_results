# Strong Seymour vertices in all oriented graphs through order fifteen

**Computer-assisted theorem.** Every nonempty oriented graph on at most
fifteen vertices has a strong Seymour vertex.

An oriented graph has no loops, multiple arcs, or directed two-cycles;
nonadjacent vertex pairs are allowed. For a vertex x write A(x)=N+(x) and

    N++(x) = (union of N+(y), y in A(x)) minus (A(x) union {x}).

A vertex is strong Seymour when there is a directed matching from every
member of A(x) to distinct members of N++(x). In particular an out-degree
zero vertex is strong. This is the matching property, not merely the
inequality |N++(x)| >= |A(x)|.

## 1. Order and degree reductions

Any smaller nonempty counterexample extends to order fifteen by repeatedly
adjoining a vertex that dominates all existing vertices. Existing first and
second neighborhoods are unchanged. The new vertex has a nonempty first
neighborhood and an empty second neighborhood, so it is also nonstrong.

Assume that an order-fifteen counterexample exists, and choose one, D, with
as few arcs as possible. Bai--Li--Park Theorem 1.5 gives delta+(D) >= 6.
The degree sum is at most binomial(15,2)=105, so delta+(D) <= 7. Equality
forces every pair to be adjacent and every out-degree to be seven. The
previously independently reviewed order-fifteen tournament theorem excludes
that case. Thus delta+(D)=6. These two imported theorems are identified in
[SOURCES.md](SOURCES.md).

If u->v is deleted, only u can become strong: another vertex keeps its first
neighborhood, while its second neighborhood and eligible matching arcs can
only shrink. Arc minimality therefore makes u strong after every such
deletion. If its original degree is d, the resulting matching has d-1
sources and at most 15-d targets. Consequently d<=8.

We also use the following arc-deletion condition, equivalent to the
standard argument in Bai--Li--Park Claim 2.6. Given u->v->z and no u->z,
some other out-neighbor w of u points to v or z. Otherwise, after deleting
u->v, neither v nor z can be a second neighbor of u. The matching supplied
by arc minimality extends by v->z to a strong matching in D, a contradiction.

## 2. Hall sources and root selection

For S contained in A(x), let

    Gamma_x(S) = (union of N+(y), y in S) minus (A(x) union {x}).

Hall's theorem says that x is nonstrong precisely when some nonempty S
satisfies |Gamma_x(S)|<|S|. If S is inclusion-minimal with this property,
then |Gamma_x(S)|=|S|-1, and deleting any member leaves the target union
unchanged. Thus every target has at least two predecessors in S. Moreover,
every proper subset U of S has |Gamma_x(U)|>=|U|.

At a degree-six root, each y in S has an out-neighbor inside S. Otherwise
all its out-neighbors would lie in (A(x) minus S) union Gamma_x(S), a set
of size five. Since the graph is oriented, a nonempty induced graph with
minimum out-degree at least one has at least three vertices. Hence
3<=|S|<=6.

For a degree-six vertex define

    M(x) = max{|N+(x) intersect N+(y)| : y in N+(x)},
    beta(x) = min{|S| : S is a deficient Hall source at x}.

Choose x with maximum M(x), and among those vertices minimize beta(x).
Take S of cardinality s=beta(x). This S is actually inclusion-minimal.
In particular 1<=M(x)<=5. Notice that M ranges over **all** out-neighbors;
it is not the more restricted alpha parameter in Bai--Li--Park.

Every arc u->v with degree-six tail has at most M(x) common out-neighbors.
If it has exactly M(x), then M(u)=M(x), and beta(u)>=s. These are necessary
conditions for the chosen root, regardless of the degree of v.

## 3. Exhaustive normalization

Relabel x as 0, its out-neighborhood as {1,...,6}, S as {1,...,s}, and its
Hall target as {7,...,s+5}. All remaining vertices are unrestricted except
by the global conditions.

For s=3,4,5, this gives the three cases `s3`, `s4`, `s5`.
For s=6, divide by M(x)=1,...,5. Label an internal maximum-degree vertex
of S as 1 and its internal out-neighbors as {2,...,M(x)+1}. For M=1,2,3
there is one case each. For M=4,5, further divide by the total out-degree
p of vertex 1. The bounds 6<=p<=8 give three cases for each M.

This produces exactly twelve cases. The root-max and pivot-degree
normalizations apply only when S is the entire root out-neighborhood;
they would not be legitimate for an arbitrary smaller S.

Finally sort the Hall targets by their ternary incidence columns against
the fixed source labels: absent=0, source-to-target=1, target-to-source=2,
with source i weighted by 3^(i-1). Permuting only the Hall targets preserves
every preceding condition. The integer pseudo-Boolean inequalities in the
generator express the resulting nondecreasing order. Ties cause no issue.

Every hypothetical counterexample therefore has a relabeling satisfying at
least one of the twelve formulas.

## 4. Formula semantics

The generator uses a Boolean e(u,v) for each ordered pair. The sole pair
restriction is `not(e(u,v) and e(v,u))`. Missing arcs are never completed
to a tournament. Sequential counters impose out-degrees in {6,7,8} and
exact flags for degree at least seven and eight.

For each degree-six or degree-seven vertex u there are source flags L(u,y)
and target flags R(u,z). A source flag implies u->y. Exact conjunction
variables and clauses enforce

    R(u,z) iff [some selected y points to z] and [u does not point to z].

Thus a target may be an in-neighbor **or a nonneighbor** of u. The
cardinality equation

    sum R(u,z) + sum (1-L(u,y)) = 13

is exactly |R|=|L|-1 because both lists have fourteen entries. Double
coverage is imposed. At degree-six vertices, source size at least three
and positive internal source out-degree are also imposed. These are
necessary minimal-source consequences, a safe relaxation at nonroot
vertices; the code does not assert literal minimality of every auxiliary
source. At the root, all proper-subset Hall inequalities are added explicitly.

Degree-eight vertices need no Hall variables to certify nonstrongness:
their second neighborhood has size at most six. Their unused auxiliary
variables do not restrict the adjacency matrix.

The root M thresholds are exact disjunctions of internal out-degree
thresholds. For each minimum-degree tail, gated common-neighbor counters
impose the maximality condition. If its common count attains root M>=2,
a flag forces its chosen Hall source to have size at least s. For M=1 this
tie-breaking condition is omitted, a further harmless relaxation. A true
counterexample supplies compatible minimal sources for all these constraints.

The root choices, arc-deletion condition, and maximum-degree-eight bound
are necessary for the selected arc-minimal graph, not claimed for every
nonstrong graph.

## 5. Exact certificates and conclusion

For each case, CaDiCaL 1.9.5 returned UNSAT and the separate `drat-trim`
checker accepted its complete DRAT trace. [manifest.json](manifest.json)
records all twelve exact CNF and trace hashes, sizes, solver budgets, and
verification results. A clean run of the publication generator reproduced
every CNF byte-for-byte. No timeout, budget exhaustion, or CP-SAT status is
used as an exclusion.

The twelve UNSAT formulas contradict the degree-six counterexample. The
imported tournament theorem excludes minimum degree seven; the imported
minimum-degree theorem excludes degrees at most five. This proves the
order-fifteen assertion, and the extension argument proves all smaller
positive orders.

Combining this lower bound with the separately reviewed 23-vertex tournament
construction gives 16<=m_oriented<=23 for the smallest oriented graph
without a strong Seymour vertex. The existing tournament interval was
already 16..23; the new result removes its tournament hypothesis.

The proof is computer-assisted and not formalized in a proof assistant.
Its trust boundary includes the two imported results, the written reduction,
the inspected generator, PySAT's exact cardinality/PB encodings, the DRAT
checker, runtime/compiler behavior, and hardware. The solver's UNSAT answer
alone is not trusted. Small semantic checks corroborate the encoding but do
not exhaust the order-fifteen graphs. No independent review of this new
result is implied by the earlier reviews cited here.

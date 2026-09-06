# Exact minimum edge-cut structure for Ramsey(5,5;43)

In every hypothetical 43-vertex Ramsey(5,5) coloring, **every partition
with at least three vertices on each side has at least 48 cross-edges of
each color**. Thus the entire global branch violating this condition is
excluded, without symmetry, degree-profile, catalog, chosen-core or fixed-
neighborhood assumptions.

Consequently, for each color graph G:

- Every minimum edge cut is the full boundary of a vertex of minimum
  degree; its size is lambda(G)=delta(G).
- Every minimum restricted edge cut is the full boundary of an edge uv
  minimizing d(u)+d(v)-2. Its size is
  lambda'(G)=min_{uv in E(G)}[d(u)+d(v)-2], between 34 and 46.

A restricted edge cut means an edge set whose deletion disconnects G
without leaving an isolated vertex. Both statements classify **all**
minimum cuts, not just one chosen minimizer. These are conventionally
called super-edge-connectivity and super-restricted-edge-connectivity.
They reduce the corresponding global minimizations to vertices and edges.

This is an elementary corollary of classical extremal graph bounds,
documented for the R55 campaign. No historical priority, numerical
sharpness, target graph, new Ramsey-number bound, independent review or
proof-assistant formalization is claimed. The proof does not rely on the
previous vertex18-connectivity artifact.

## 1. Degree window and the elementary extremal bound

The established R(4,5)<=25 implies 18<=d_G(v)<=24 in both colors: a
monochromatic neighborhood is a (4,5) or color-reversed Ramsey graph on
at most24 vertices. The two color degrees sum to42. The later
[Gauthier--Brown formal proof of R(4,5)=25](https://arxiv.org/abs/2404.01761)
is primary provenance for this imported classical fact; it was not run
here. No extremal graph data or solver output is imported.

We use the Turan inequality e(H)<=floor(3a^2/8) for a K5-free graph on
a vertices. Here is a self-contained weighted proof of the needed bound.
For nonnegative weights summing to1, maximize the sum of x_u*x_v over
edges uv, choosing an optimizer of smallest support. If two positive-
weight vertices u,v are nonadjacent, moving their combined weight to
whichever has the larger weighted neighbor sum cannot decrease the
objective. It either contradicts optimality or decreases the support.
Hence the support is a clique of size t<=4. The objective on that clique
is (1-sum x_u^2)/2<=(1-1/t)/2<=3/8. Uniform weights1/a give e(H)/a^2
as one feasible value. Integrality supplies the floor. This is the
classical weighted proof method; compare
[Motzkin and Straus, 1965](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0008414X00039493).

## 2. Complete global cut bound

For a nonempty proper subset A, let partial(A) be the set of graph edges
with exactly one endpoint in A. Choose the smaller side of the partition,
so a=|A|<=21. The exact degree identity gives

    |partial(A)| = sum_{v in A} d(v) - 2 e(G[A])
                 >= 18a - 2 floor(3a^2/8).                  (1)

For 3<=a<=21 the concave quadratic 18a-3a^2/4 is at least its endpoint
value189/4=47.25. Thus (1), an integer, is at least48. For a=2 the
bound is34, and for a=1 it is18. In particular G is connected, every
cut with at least two vertices on each side has size at least34, and
every cut with at least three on each side has size at least48.
This proof applies to either color, with no relation to a selected
separator or to an extremal-order assumption about R(5,5).

For Boolean red-edge variables x_uv, the complete global family of
necessary inequalities is

    q(a) <= sum_{u in A, v outside A} x_uv <= a(43-a)-q(a),
    q(a)=18a-2 floor(3a^2/8), a=min(|A|,43-|A|).           (2)

The upper bound is the lower bound for blue edges. These are explicitly
defined constraints; their exponentially large conjunction was not emitted.
No degree profile, anchored split or count-only survivor tally is claimed
removed by (2). It is a global graph-realization restriction.

## 3. Exact ordinary and restricted cut minimizers

An ordinary minimum edge cut has size at most delta(G)<=24, by cutting
off a minimum-degree vertex. If none of its components were singletons,
its smallest component would have between2 and21 vertices and boundary
size at least34, impossible. A singleton's full boundary is contained in
the cut; its size is at least delta(G). Equality forces precisely the
minimum-degree vertex boundary, proving the first claim.

For any edge uv, delete its full boundary, leaving uv itself intact.
The other41 vertices each retain degree at least18-2=16, so there are
no isolated vertices. This is a restricted cut of size d(u)+d(v)-2<=46.
Put xi(G)=min_{uv in E(G)}[d(u)+d(v)-2]. Hence lambda'(G)<=xi(G)<=46.

In any minimum restricted cut F, every component has at least two
vertices. If all had at least three, a smallest component would have
size3..21 and boundary at least48, contradicting |F|<=46. Therefore
some component is an edge uv. Its original full boundary belongs to F,
so |F|>=d(u)+d(v)-2>=xi(G). All inequalities are equalities. Thus
F=partial({u,v}), with uv attaining xi(G), as claimed. Conversely every
edge attaining xi yields such a minimum restricted cut by the preceding
no-isolated-vertex argument. A minimum restricted cut has exactly two
components: with at least three, restoring an edge between two components
would give a smaller restricted cut. No assumption about the number of
components was silently imposed in the argument.

The numerical gaps are strict: 24<34 and46<48. These are essential to
the stated all-minimizer conclusions. The code includes K(2,2,2) as a
negative fixture for replacing the strict gap by equality: a minimum
restricted cut can leave two triangles rather than isolate an edge.

## 4. Reproduction and controls

[derive.py](derive.py) produces the21 exact q(a) values in
[certificate.json](certificate.json). [check.py](check.py) imports no
producer. It reconstructs each integer capacity by enumerating all
four-partite part-size multisets, compares every row and endpoint gap,
and rejects four mutated certificates. This enumeration audits the
arithmetic; it does not itself prove Turan's universal inequality.

The graph controls enumerate every labeled graph on2..5 vertices. They
check cut-degree and edge-degree identities by literal cross-edge counting,
and the Turan translation on K5-free instances. For every connected
graph, all edge-deletion sets are checked and the **complete sets of
minimum cuts** are compared with a separate vertex-partition enumeration,
for both ordinary and restricted cuts. This checks definitions and the
all-minimizer interpretation, not just agreement of minimum values.

K(2,2,2,2) is a positive cut-structure fixture. K21,22 supplies a
nonvacuous43-vertex fixture for the localized K5-free degree-window
theorem: all504 cut orbits under its within-part permutations satisfy
(1); lambda=21 and lambda'=41, with every minimum restricted cut
isolating an edge. It has independent sets of orders21 and22, so is
explicitly **not** a target Ramsey graph or a construction milestone.

With CPython3.11.2, standard library only, run in this directory:

```sh
set -o pipefail
python3 -B derive.py | cmp - certificate.json
python3 -B check.py | cmp - validation.json
python3 -O -B derive.py | cmp - certificate.json
python3 -O -B check.py | cmp - validation.json
sha256sum -c SHA256SUMS
```

Expected status: VERIFIED_GLOBAL_EDGE_CUT_ARITHMETIC;21 rows and four
rejected mutations. Normal/-O execution agrees byte-for-byte. The compact
[validation.json](validation.json) records all control counts. No
floating-point arithmetic, assertions, randomness or solver is used.
The written proof supplies the universal theorem; small controls neither
enumerate all43-vertex graphs nor constitute independent peer review.

## 5. Classical context, trust and stopping boundary

This is a specialization of standard extremal cut reasoning, not a new
general connectivity method. Holtkamp's2013 dissertation
[Connectivity in Graphs and Digraphs](https://d-nb.info/1038598796/34),
Theorem3.63 and Corollary3.66 (attributed there to Holtkamp--Meierling),
relates clique number and minimum degree to local restricted-edge-cut
optimality through Turan bounds. These are closely related prior results.
Our self-contained argument provides the concrete48-gap and the complete
minimum-cut description for this R55 degree window; we make no priority
claim even for that numerical specialization.

For the terminology and distinction between restricted optimality and
the stronger all-minimum-cuts property, see
[Yin and Tian, 2023](https://arxiv.org/abs/2301.12784).
Neither that paper's direct-product hypotheses nor a graph-product
construction is assumed here. No external connectivity theorem is needed
as a premise beyond the proof supplied in Sections1--3.

The earlier global vertex18-connectivity lemma is retained as complementary
context, not a dependency. The newly read independent review at Discovery
Net3389 accepts the external dense five-separator classification only in
order22 neighborhoods; it does not review this artifact. The teammate's
123-defect fourteen-cycle C3 construction at3387 remains a defective
structured candidate, not a target or an input to this proof.

Trust remains in the classical R(4,5) bound, the displayed unformalized
argument, and the internal checker/runtime. No imported graph data or
bulky omitted certificate is needed. No previously parked switching,
catalog or H92/H93/104-edge/six-neighborhood/gluing route was reopened.
The declared whole-branch gate is complete. This pass ends here before
another cut threshold, family, or research phase.

# A K4 subdivision and two pendant marks exclude a planar obstruction family

**Exact computer-assisted theorem.** Let T be the marked 20-vertex planar
triangulation below. Its specified core C is a subdivision of K4. Choose
one of the four neighbors of mark 3, and one of the four neighbors of
mark 15, as their parents. Let H consist of C and these two parent edges.
For every positive real edge metric on T in which H is isometric, and
every nonnegative vertex mass supported on the nine marks, two shortest
paths in the original T half-balance the mass.

Thus only two marks need the pendant metric condition. The other seven
marks may have arbitrary positive incident lengths consistent with
isometry of H. There are 16 required parent choices and 15 independently
variable positive H-edge lengths. The result also holds for zero-mass
plane extensions described below. It is an obstruction to this proposed
counterexample construction, not a resolution of
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
No counterexample or historical priority claim is made.

## Graph and hypotheses

Write v(i,j)=2+3(i mod 6)+j for 0<=j<=2, with poles 0 and 1. Include
edges v(i,j)v(i+1,j), v(i,j)v(i,j+1), 0v(i,0), and 1v(i,2), whenever
the indicated j is in range. In each square

    A=v(i,j), B=v(i+1,j), C'=v(i+1,j+1), D=v(i,j+1),

add diagonal AC' when i+j is even and BD otherwise. This gives T, with
20 vertices, 54 edges, and 36 triangular faces. The explicit edges and
oriented faces are in [certificate.json](certificate.json). The checker
reconstructs the graph from this rule and checks a spherical rotation
system, including one cyclic rotation at every vertex and Euler
characteristic two.

The nine marked vertices are

    5, 9, 13, 11, 15, 19, 17, 3, 7.

They form an independent set. The other eleven vertices support C:
take the edges of the three branches

    (0,2,6,10,1), (0,8,12,16,1), (0,14,18,4,1),

and add edge (2,18). The four degree-three core vertices are 0,1,2,18;
the six subdivision links are

    (0,8,12,16,1), (0,2), (0,14,18),
    (1,10,6,2), (1,4,18), (2,18).

Choose p_3 from {2,4,6,18} and p_15 from {12,14,16,18}. Then

    H = C + edge(3,p_3) + edge(15,p_15)

has 13 vertices and 15 edges. Isometry means precisely
d_T(a,b)=d_H(a,b) for every a,b in V(H). It is a hypothesis on the
**original** positive edge lengths. Neither uniqueness of geodesics nor
the assumption that every C-edge is itself geodesic is imposed.

The theorem contains the earlier
[all-pendant-parent family](../all_attachments/README.md). In that
family, the original three-branch core and all nine parent edges form
an isometric spanning subgraph. Adding edge (2,18), at its already
distance-preserving price, and restricting to the two necessary marks
gives the present isometric H. Here the chord can instead create a
genuine shortcut, and seven marks need not be metric leaves at all.

## Reduction to a finite exact certificate

Give each mark mass one first. A sufficient pair has at most four marks
in each component after deleting the pair from the **full T**, retaining
all edges outside H. The certificate lists 66 such pairs: 58 consist
entirely of core paths; eight extend one endpoint to mark 3 or 15.
The latter eight contain one pair for each possible parent of each of
these two marks. All paths, parent conditions, and residual components
are checked directly. No prescribed first path or symmetry quotient is
assumed.

Let x_e be the 13 C-edge lengths. By scaling, impose x_e>=1; every
positive real assignment has a positive minimum and can be scaled this
way. For a core path p, its length is the sum of its edge variables.
The checker enumerates all simple core routes between every unordered
endpoint pair, including singletons: 336 routes in total. Positive
edge lengths imply that a shortest route is simple. Consequently

    p is geodesic iff length(p) <= length(q) for every such alternative q.

These are weak inequalities, so all shortest-path ties are included.
The two additional H-edges are pendant edges; their arbitrary positive
lengths cancel from every comparison between routes with the same
endpoints. A chosen leaf extension of a core geodesic is therefore
H-geodesic, and isometry makes it an original T-geodesic.

Introduce four Boolean parent choices per required mark and impose
exactly one for each mark. A counterexample to coverage by the 66 pairs
must satisfy, for each pair, the following clause: some required parent
is absent, or some alternative core route is strictly shorter than one
of its paths. The checker builds this clause directly from the listed
paths and the complete route catalog. The parent constraints, the 13
positive-length constraints, and the 66 pair exclusions give 93 clauses.

If any positive metric and parent choices had no suitable listed pair,
they would define a satisfying assignment of these clauses with the
intended real arithmetic. The remaining certificate proves that this
is impossible. Completeness of the search that selected the templates
is irrelevant; only the checked finite coverage is used.

## Exact arithmetic identities and Boolean proof

A linear atom means f(x)>=0, where f has integer coefficients, including
its constant term. Common positive rational factors are normalized
away; signs are not flipped. A negative literal for this atom means
-f(x)>0. There are 263 linear atoms and eight parent variables.

Each of the 526 arithmetic certificates gives positive rational
multipliers for a list of these weak or strict inequalities. The checker
adds their affine coefficient vectors exactly using Python `Fraction`.
The variable coefficients must cancel, and either:

* the resulting constant is negative; or
* the constant is zero and at least one positively weighted summand is
  strict.

In either case the inequalities cannot hold simultaneously. Their
negations form a valid arithmetic clause. With these clauses added,
there are 619 propositional clauses. The supplied proof consists of
1,174 reverse-unit-propagation additions ending in the empty clause.
For each addition, the checker assumes all its literals false and
performs ordinary unit propagation on earlier clauses; a conflict is
required. It does not call a SAT, SMT, LP, or floating-point package.

The arithmetic identities plus this propositional refutation establish
the real-parameter quantifier, including every tie and every one of the
16 parent assignments. The untrusted discovery process used exact
sampled metrics, countermodel-guided QF_LRA search, and proof reduction.
Z3 4.15.4 and python-sat 1.9.dev15 with Glucose3 produced proof material;
their UNSAT reports are not accepted as evidence by the verifier.
The certificate contains the selected graph paths, rational identities,
and proof additions. The checker reconstructs the logical instance from
the graph rather than importing a solver-generated encoding.

## Arbitrary masses and larger plane graphs

Let the marked masses total W. If the four largest sum to at least W/2,
pair these four vertices and take two ambient shortest paths between
the pairs. Their deletion removes at least half the mass. Otherwise
every set of at most four marks has mass less than W/2, so the uniform
certificate supplies a half separator. The case W=0 is immediate.
There is no change of graph or edge lengths in this argument.

More generally, let G be a finite simple plane supergraph of the
specified embedded T. Keep all mass on the same nine marks and require
H to be isometric in G. Each component outside T lies in one triangular
face. Its surviving T-neighbors form a clique, and hence already belong
to one residual T-component. Adding these zero-mass components cannot
merge distinct residual T-components. The same pair is therefore an
ambient G-geodesic half separator. This gives graphs of unbounded order,
but allows neither arbitrary marked topologies nor mass on new vertices.

## Comparison with interval and facial transfer

The small [comparison.json](comparison.json) specifies exact core
prices, nine parent choices, and a spanning pendant realization.
Give every parent edge price one and every other T-edge price d_H9+1,
where H9 is the core with all nine parent edges. The checker verifies
isometry and uniqueness of every ambient geodesic. The chord saves
216,965 length units compared with the same metric with that edge
removed. A certified positive pair is

    (0,8,12,16,1), (3,2,18,4),

whose full-T residual mark counts are 1,3,4.

For this metric and uniform marked masses, the checker tries every
interval, every rooted triangular face of the supplied embedding, every
corresponding first geodesic P, and every subset S of the relevant
geodesic union. Vertices in S intersect P can be discarded from S
without changing the test. None satisfies both conditions of the
[subset-transfer lemma](../../planar_two_geodesic_rerooted_attachments/README.md):
every positive component of T-(S union P) is half-light and has at most
one surviving S-neighbor. This is 2,560 terminal/first-path cases and
26,148 subset tests, with 14,591 distinct (P,S) pairs.

Thus that sufficient condition, including the earlier exact-union
transfer, does not already cover this construction family. This is an
explicit metric and supplied-embedding comparison, not a rejection of
the transfer theorem or a claim about every possible auxiliary graph.
The certificate theorem does not depend on the transfer theorem.

## Reproduction and trust boundary

From the repository root, run with Python 3.11+ and the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_parallel_path_metrics/k4_shortcut/verify.py --check
```

The verifier refuses Python optimization mode, which disables
assertions. [expected.json](expected.json) records all deterministic
counts and the certificate SHA-256. In addition to the proof replay,
it checks 64 exact ambient metrics by Floyd--Warshall, including
nongeodesic core edges and shortest-route ties, 512 mass instances,
and eleven rejected malformed controls. In 32 metrics, all seven
nonrequired marks provably fail the metric-leaf condition. These
regressions test the written reduction; they do not substitute for
the arithmetic certificate. The subset comparison has a separate
positive star control.

The trust boundary is the written reduction, the explicit spherical
embedding, and the standard-library certificate checker. The discovery
code is not imported. The same researcher wrote the discovery process
and the separate checker; this is not an independent researcher review
or proof-assistant formalization. No external graph census is used.
The weighted setting is consistent with
[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a). The known
two-path 2/3 result quoted in Problem 31 is not used as an exact-half
theorem.

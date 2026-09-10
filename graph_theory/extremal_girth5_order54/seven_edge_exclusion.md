# Thirteen degree-eight vertices force an isolated one

**Theorem (human reduction and exact computer-assisted exclusion).** Let G be a
simple graph on 54 vertices with 187 edges and no triangle or quadrilateral.
If exactly thirteen vertices have degree eight, their induced graph has at
most six edges. In particular, one of these thirteen vertices has no
degree-eight neighbor.

This excludes an entire structural subclass, including every realization
and every assignment of the remaining incidences. It does not impose the
previous `boundary_profile.json`, any type-to-type edge totals, or a chosen
local-type histogram. The numerical interval remains **185 <= f(54) <= 187**.

The [degree reduction](proof.md) and [all-sink theorem](boundary_sinks.md)
are prerequisites: the degree counts are (17,24,13) for degrees (6,7,8),
and every degree-eight vertex has all vertices within distance two.
The new SAT computation uses individual incidences and short paths. It
does **not** use the weighted-gap budget or a spectral restriction.

## 1. Pair coverage forces at most seven high-high edges

Write T=V8, H=G[T], c(v)=|N(v) intersect T|, m=e(H), and let k be the number
of degree-two vertices of H. A high vertex has neighbor counts
(3+c,5-2c,c) in the three degree classes, since its neighbor degrees sum
to 53. Consequently c<=2 on T, and

    sum_{V6} c = 39+2m,       sum_{V7} c = 65-4m.

Every pair of high vertices is either adjacent or has exactly one common
neighbor. Counting the latter by its middle vertex gives

    sum_{V6} binom(c,2) + sum_{V7} binom(c,2) = 78-m-k.

For every nonnegative integer c,

    binom(c,2) >= 3c-6,       binom(c,2) >= c-1.

The respective differences are (c-3)(c-4)/2 and (c-1)(c-2)/2.
Thus 78-m-k >= (15+6m)+(41-4m), or 3m+k<=22.
Since k>=2m-13, we obtain m<=7.

If m=7, equality holds throughout. Hence k=1 and H=P3+5K2.
Every degree-six vertex has c=3 or 4, and every degree-seven vertex has
c=1 or 2. Their counts are forced:

| Degree | c | Count |
|---|---|---|
| 6 | 3 | 15 |
| 6 | 4 | 2 |
| 7 | 1 | 11 |
| 7 | 2 | 13 |

The rest of the argument excludes this entire equality case.

## 2. Individual high-neighborhood partitions

For a low vertex v, put S(v)=N(v) intersect T. Every S(v) is independent
in H squared: two of its points cannot be adjacent in H or have a common
neighbor in H, by the forbidden triangle and quadrilateral conditions.

More strongly, the sets S(u), for low neighbors u of v, partition

    T minus (S(v) union N_H(S(v))).                         (1)

Disjointness and the omitted points follow from unique short paths.
Coverage follows because every point of T is a sink. This is an identity
of sets at individual vertices, rather than an inequality on type totals.

Let o be the center and a,b the endpoints of the P3. The other ten high
vertices carry the five-edge matching M. The center o has five degree-six
neighbors and one degree-seven neighbor. Its ten nonadjacent high points
must appear exactly once among their other high neighbors. The five
degree-six neighbors already contribute at least ten such incidences.
They therefore all have c=3, and the unique degree-seven neighbor y0
has S(y0)={o}. The five triples containing o pair the ten points in a
perfect matching K disjoint from M.

The union of two disjoint perfect matchings on ten points is either C10
or C4+C6. These are the only two matching cases. The colors M and K are
retained; their roles are not exchanged by the quotient.

Call the two degree-six vertices with c=4 the quadruple vertices.
Neither is adjacent to o, by the preceding center count. If its set S
avoided the whole P3, the set in (1) would be P3 plus one matching edge.
An independent set in its square has size at most two. Its two low
neighbors could not partition all five points. Thus each quadruple set
contains exactly one endpoint, a or b.

Suppose S(Q)={a} union I, with I three matching points. The three points
occupy distinct M edges. The set in (1) is {b} plus the two remaining
M edges. Its independence number in H squared is three. Its partition
by the two low neighbors must have sizes three and two. Thus Q has:

* a unique degree-six neighbor x, with S(x)={b} union X;
* a unique degree-seven neighbor y, with S(y)=Y;

where X,Y partition the four points of the two remaining M edges, each
has size two, and each is independent in M union K. Also I is independent
in M union K, because a pair in K already shares one of the center's
degree-six neighbors.

The two quadruple vertices have distinct x partners. If they meet the
same endpoint, sharing x makes a quadrilateral; if they meet opposite
endpoints, a common x would have both endpoints in S(x), also forbidden.
Their y partners are distinct as well: a degree-seven vertex with c=2
and two quadruple neighbors would need at least 4+4+1+1+1=11 high
incidences from its five low neighbors, although (1) has only nine points.

For the same reason, each y has no degree-six neighbor other than Q:
another such neighbor would require at least 4+3+1+1+1=10 incidences.
Its other four low neighbors are degree seven. Their high sets must cover
o, so **each y is adjacent to y0**, the unique degree-seven neighbor of o.
These are the additional fixed incidences used by the computation.

## 3. Complete finite quotient

Label o,a,b as 0,1,2 and the matched points as 3,...,12. Label the five
center triples 13,...,17; the x partners 18,19; the other triples 20,...,27;
the quadruple vertices 28,29; y0 as 30; the other singleton high sets
31,...,40; the y partners 41,42; and the other pair high sets 43,...,53.

Interchanging a,b makes the first quadruple meet a. The second meets
either a or b. For each colored matching configuration, enumerate every
triple (I,X,Y) described above, and quotient by the automorphisms preserving
both M and K. These automorphisms also permute the five center triples,
so the normalization loses no graph. Vertex labels within each remaining
undistinguished group may then be sorted by their high-neighborhood bit
strings. Equal strings remain permitted.

| Matching union | Colored automorphisms | Raw (I,X,Y) | Orbits | Endpoint choices | SAT cases |
|---|---:|---:|---:|---:|---:|
| C10 | 10 | 160 | 16 | 2 | 32 |
| C4+C6 | 24 | 172 | 9 | 2 | 18 |

The quotient checks reconstruct every raw triple from the selected
representatives and prove that the orbits are disjoint. A separate
recursive enumeration visits all 544 perfect matchings K disjoint from
fixed M: 384 give C10 and 160 give C4+C6. No sampling is involved.

## 4. Encoding and certificate boundary

`seven_edge_sat.py` generates each of the 50 cases. Its edge variables
include every pair with a low endpoint and the seven fixed edges of H;
all other high-high pairs are absent. The degrees and c values above are
exact. The high vertices have exactly 3+c degree-six neighbors and 5-2c
degree-seven neighbors.

For every pair u,v and possible middle vertex w, a variable p is equivalent
to the conjunction of edges uw and vw. At most one of the edge uv and
these common-neighbor variables may hold. This is equivalent to forbidding
triangles and quadrilaterals. If a pair includes a high vertex, at least
one must hold, expressing the sink condition.

The generator adds the proved fixed incidences and two redundant forms
of the individual partition constraints. For a low vertex v, with
eta(v)=1 when o is in S(v), equation (1) implies

    sum_{low u adjacent v} (c(u)-1) + eta(v) = 13-d(v)-c(v).

For a high endpoint, the number of adjacent quadruple vertices plus the
number of adjacent degree-seven vertices with c=2 is two; for a matched
high point it is three. For o both counts are zero. These equations
follow by counting common neighbors between that one high vertex and
the other high points. Direct quadrilateral clauses through an edge of
H duplicate consequences of the short-path encoding.

Cardinality constraints use sequential counters. Repeating a literal
encodes its nonnegative integer coefficient. Lexicographic ordering is
applied only to the three groups 20,...,27; 31,...,40; and 43,...,53.
All mathematical conditions above are necessary, and the stated relabeling
puts every equality-case graph into at least one generated instance.
Consequently checked UNSAT for all instances excludes the whole subclass.

Every instance has 190,190 variables and 525,414 clauses. All 50 are
UNSAT, with each DRUP trace checked separately by DRAT-trim. See
`seven_edge_expected.json` for the complete case list and hashes. Large
CNF files, proof traces and checker logs are regenerated outside the
repository and are not published here.

The trust boundary is the written reduction and coverage argument,
the generator and its cardinality library, Python/native runtimes,
and the independent DRAT-trim checker. The SAT solver's unsupported verdict
is not an accepted certificate. The controls are same-session validation,
not an independent review or a formal proof-assistant verification.
The controls check all 256 assignments of a small lexicographic comparator,
112 weighted-cardinality assignments, the incidence partitions on known
girth-five graphs, and the complete matching/motif coverage. They do not
provide a positive graph in the excluded subclass.

## Reproduction and consequence

Use CPython 3.11.2 and the pinned `requirements-sat.txt` (python-sat
1.8.dev24, six 1.17.0). The checker used here is DRAT-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, compiled with GCC 12.2.0,
C99 and `-O2`; its [official repository](https://github.com/marijnheule/drat-trim)
contains the source and build instructions.

```sh
python3 verify_seven_edge.py
python3 reproduce_seven_edge.py --work /tmp/order54-seven-edge --checker /path/to/drat-trim
```

The final output must report `verified_unsat: 50`. The driver compares
every regenerated CNF hash with the published manifest and stops on
UNKNOWN, SAT, a hash mismatch, or a failed checker. The production run
is deterministic and sequential. Budget 100,000 conflicts per case and
120 checker seconds per case; observed costs are recorded in the compact
run summary.

The fresh delivery run took 228.5 seconds and peaked at 281,564 KiB
(about 275 MiB). It reproduced all CNF and proof hashes from the first
incidence-only run. See `seven_edge_run.json` for the resource and coverage
summary. Allow roughly 700 MB of temporary disk space for generated
instances and traces.

Together with Section 1, the exclusion proves e(H)<=6. Since H has
thirteen vertices, it has an isolated vertex. Thus the entire surviving
z=13 class can be rooted at a degree-eight sink with three degree-six
neighbors and five degree-seven neighbors. The next realization search
needs only this root type. Deciding that class, or the original 187-edge
existence question, remains open.

The pair-packing principle is standard; see the primary literature in
the main README. This specialization and complete incidence exclusion
are new to the sources and graph checked in this campaign; historical
priority and standalone publishability are not asserted.

# The thirteen-high-vertex boundary reduces to seven forests

**Theorem.** Let G be a simple graph of order 54 and size 187 with no
triangle or quadrilateral, and suppose exactly thirteen vertices have
degree eight. Their induced graph H is one of the following seven forests.
Here P_j is the path on j vertices, and K1 is an isolated vertex.

| Case | H | Edges m | Degree-two vertices k |
|---|---|---:|---:|
| 5_0 | 5P2 + 3K1 | 5 | 0 |
| 5_1 | P3 + 3P2 + 4K1 | 5 | 1 |
| 5_2a | P4 + 2P2 + 5K1 | 5 | 2 |
| 5_2b | 2P3 + P2 + 5K1 | 5 | 2 |
| 6_0 | 6P2 + K1 | 6 | 0 |
| 6_1 | P3 + 4P2 + 2K1 | 6 | 1 |
| 6_2b | 2P3 + 2P2 + 3K1 | 6 | 2 |

This is a necessary classification of actual graph realizations. Existence
in any of these seven cases is unresolved. In particular the theorem does
not exclude thirteen degree-eight vertices or improve the working interval
185 <= ex(54,{C3,C4}) <= 187.

The proof combines two exact rational inequalities with complete incidence
exclusions of three whole forests. It uses the preceding degree and
all-sink results and the [six-edge upper bound](seven_edge_exclusion.md).
That preceding result has received an
[independent acceptance and complete reproduction](../../extremal_girth5_order54_seven_edge_review1/README.md).
The new reduction below has not received that independent review.

## 1. The necessary type-incidence system

The degree counts are (17,24,13) in classes 6,7,8. A type i is a degree
d_i together with its neighbor counts n_i(6),n_i(7),n_i(8). Retain all
nonnegative types summing to d_i whose neighbor degrees sum to at most 53.
There are 72 types, in the deterministic order in `forest_constraints.py`.

Let X_i count vertices of type i. For i<j let Y_ij count edges between
types i,j; let Y_ii be **twice** the number of internal edges in type i.
Only pairs of types which can have an edge are represented. There are
1,638 Y variables. All 1,710 variables are nonnegative. The X variables
of degree eight which are not sink types are zero, by the all-sink theorem.

The following constraints are necessary, without assuming realizability
of arbitrary solutions to them:

1. The three degree-class counts and three degree-class handshakes.
2. Six degree-class pair capacities. Within a class C, twice the number
   of two-paths plus twice the number of edges is at most |C|(|C|-1).
   Between two classes, two-paths plus edges are at most the product of
   their orders.
3. For each type i and target degree class C, the exact balance
   sum_j Y_ij = n_i(C) X_i, summing over j in C with the diagonal convention
   above.
4. For each type i and target class C, the type-averaged two-step capacity

       sum_j n_j(C) Y_ij
       <= (|C|-n_i(C)+(d_i-1)[d_i belongs to C]) X_i.

The last inequality follows at each vertex by packing its neighbors and
second neighbors inside C; then sum over the vertices of type i. Its
diagonal correction removes repeated two-walk returns to the starting
vertex. No inequality is reversed by replacing a quantity with an upper
surrogate. The checker evaluates every generated row on actual
Hoffman--Singleton and edge-deleted Hoffman--Singleton graphs as controls.

There are 222 equality rows and 222 inequality rows. Also,

    sum_i X_i = 54,
    sum_i Y_ii + 2 sum_{i<j} Y_ij = 374,

so the sum of all nonnegative variables is at most 428.

## 2. Two rational certificates, including their exact error payment

The public JSON certificates contain rational row multipliers with common
denominator 1,000,000. Equality multipliers are unrestricted; multipliers
of rows written A x <= b are nonpositive. If their row combination is
L(x), their right-hand-side combination is B, and c is the objective,
the verifier computes exactly

    delta = max(0, max_j (coefficient_j(L)-c_j)),

over the allowed nonzero variable columns. Therefore, for every graph,

    c.x >= B - 428 delta.                                  (2)

Indeed L(x)>=B, while L(x)<=c.x+delta sum_j x_j. This explicitly pays for
every coefficient excess using exact fractions. The rounded multipliers
are not accepted as approximately feasible duals. There is no floating-
point tolerance or optimizer trust in the delivered proof.

For c.x=m, `forest_lower_certificate.json` gives

    B = 4128637/1000000,
    delta = 9/500000,
    m >= 4120933/1000000 > 4.

Thus the integer m is at least five. The preceding theorem gives m<=6.
Append these two valid inequalities to the necessary system. For objective
-(m+k), `forest_degree2_certificate.json` gives

    B = -88889/10000,
    delta = 13/1000000,
    -(m+k) >= -138976/15625 > -9.

Thus m+k<=8. All entries, coefficient comparisons and bounds are checked
by `verify_forest_reduction.py` using Python integers and Fraction. SciPy
1.15.3 / HiGHS was used only to discover the multipliers. The independent
sparse implementation of the mathematical rows agrees entry by entry with
the discovery matrices; the shipped checker requires no SciPy or solver.

Since H has maximum degree two and no cycle shorter than five, a cycle
would contribute at least five degree-two vertices. But 5<=m<=6 and
m+k<=8 give k<=3. Hence H is a forest of paths. Enumerating partitions of
m into the positive edge counts of its nontrivial path components gives
exactly ten possible forests: the seven in the theorem plus

    5_3a: P5 + P2 + 6K1,
    5_3b: P4 + P3 + 6K1,
    6_2a: P4 + 3P2 + 3K1.

The rest of the proof excludes these three entire forests.

## 3. Complete high-neighbor profiles for a fixed forest

Put c(v)=|N(v) intersect V8|. Unique short paths between high vertices give

    sum_{V6} c = 39+2m,       sum_{V7} c = 65-4m,
    sum_{V6} binom(c,2) + sum_{V7} binom(c,2) = 78-m-k.

Subtracting the elementary integer lower bounds used in the previous
seven-edge reduction gives the exact nonnegative deficit

    sum_{V6} (c-3)(c-4)/2
      + sum_{V7} (c-1)(c-2)/2 = 22-3m-k.                  (3)

For a fixed m,k, `forest_profiles.py` enumerates every integer histogram
of c in each degree class satisfying its vertex count, its first moment
and (3). Positive-cost c values have bounded multiplicities; the remaining
zero-cost values are 3,4 for degree six and 1,2 for degree seven. Their
multiplicities are fixed by the two linear balances. A separate recursive
enumeration over every c checks the resulting vectors entry by entry.

| m,k | Number of complete c histograms |
|---|---:|
| 5,0 | 49 |
| 5,1 | 29 |
| 5,2 | 15 |
| 5,3 | 8 |
| 6,0 | 24 |
| 6,1 | 13 |
| 6,2 | 6 |

The ten-forest cover therefore has 173 forest/histogram cases. The two
five-edge forests being excluded each require eight cases; the six-edge
forest requires six. **All 22 cases are excluded.** This does not select
a favorable c histogram, full local degree type, or type-to-type edge
count. Every histogram and every remaining incidence for each of the
three forests is covered.

## 4. Incidence encoding and symmetry soundness

`forest_sat.py` assigns fixed degrees and c values to the low vertices,
fixes exactly the edges of H, and permits every edge with a low endpoint.
It enforces the exact degree and c counts. A high vertex t has 3+c(t)
degree-six neighbors and 5-2c(t) degree-seven neighbors.

As before, conjunction variables encode possible common neighbors. At
most one edge or length-two path per pair forbids C3 and C4. For every
pair containing a high vertex, at least one exists. Thus every high
vertex is a sink. No connectivity assumption is added separately.

The individual high-neighborhood partition identity also gives the
following redundant equations, where h(t)=degree_H(t):

    sum_{low u adjacent v}(c(u)-1)
       + sum_{high t adjacent v} h(t) = 13-d(v)       (v low),

    sum_{low u adjacent t}(c(u)-1)
       = 12-sum_{s adjacent_H t} h(s)                (t high).

They follow by counting the unique short paths from the one vertex to
all high vertices. Negative coefficients occur only for c(u)=0 and are
represented exactly by complementing that edge literal and shifting the
right-hand side. Sequential counters enforce the resulting nonnegative
integer cardinalities. Neither the weighted-gap budget nor a spectral
restriction is used in these 22 final refutations.

Symmetry is broken in the low-by-high incidence matrix, read in row-major
order. Low rows of the same (degree,c) are sorted. Columns corresponding
to isolated high vertices are sorted; each path component is oriented so
its incidence block is at most its reversal; equal-sized path blocks are
sorted. These conditions are compatible: choose the globally least
incidence matrix over precisely these valid row and column relabelings.
Any violated comparison would yield a strictly smaller matrix by the
corresponding row swap, path reversal or component swap. Hence at least
one labeling of every graph satisfies all comparisons simultaneously.
No ordering of different degree/c classes or different path lengths is
imposed as a symmetry.

The comparator implementation is the previously validated `lex_chain`.
A new exhaustive control checks compatibility of row sorting, component
orientation and component sorting on all 4,096 binary 3-by-4 matrices
with two reversible, interchangeable two-column components. The written
minimum-matrix argument supplies the general coverage proof.

## 5. Certificates, reproduction and remaining scope

Each of the 22 formulas is UNSAT, and its emitted DRUP trace is accepted
by a separate DRAT-trim process. `forest_expected.json` lists every case,
formula size and formula/proof hash. A fresh sequential run from the
delivered source regenerated every formula and repeated every solver
and proof-checker call. `forest_run.json` records the compact run evidence.

Use CPython 3.11.2, the existing `requirements-sat.txt`, and DRAT-trim
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, built with GCC 12.2.0,
C99, `-O2`. The exact rational checks use only the standard library.

```sh
python3 verify_forest_reduction.py
python3 reproduce_forest_exclusions.py --work /tmp/order54-forests --checker /path/to/drat-trim
```

The second command must finish with `verified_unsat: 22` and excluded
forests `5_3a`, `5_3b`, `6_2a`. It checks every generated CNF hash and
fails on SAT, UNKNOWN, or any failed proof check. Generated formulas,
traces and verbose logs remain outside the repository. Default limits
are 100,000 conflicts per case and 120 seconds per proof checker.

The fresh delivery run took 129.4 seconds, peaked at 277,564 KiB RSS
(about 271 MiB), and reproduced every formula and proof hash. It generated
211,872,927 formula bytes and 26,643,320 proof bytes; allow about 300 MB
of temporary disk space.

The mathematical trust boundary comprises the earlier order-53 bound,
degree/all-sink/six-edge results, the written necessary constraints and
the graph-to-case coverage argument. The new numerical bounds are exact
rational certificates. The finite exclusions additionally trust the
generator, cardinality library, runtime/compiler and independent proof
checker; the solver's bare verdict is insufficient. These new controls
and reproductions were conducted in this research session, not by the
reviewer of the preceding theorem.

The seven remaining forest types are unresolved, even where some individual
profiles have been ruled out in exploratory runs. The result is a complete
structural reduction and three whole-subclass exclusions, not a complete
solution of the thirteen-high-vertex case. The underlying pair-packing
method is standard; no historical priority or standalone publishability
claim is made for this specialization.

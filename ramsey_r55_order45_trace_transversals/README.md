# Order-45 boundary traces in dense `(4,5,24)` neighborhoods

## Scope and claim

This package gives a symmetry-free restriction on every dense order-24
neighborhood that could occur in a hypothetical `(5,5,45)` Ramsey graph.  It
also gives an exact, catalogue-conditional census of one intrinsic parameter
of the complete dense family.

It **does not** prove an occurrence edge cap, exclude a `(5,5,45)` graph, or
improve the numerical bound on `R(5,5)`.  Its role is to replace the bare
15,913-graph tail by a common boundary-matrix theorem and four complete
transversal strata for a subsequent occurrence argument.

The imported neighborhood-edge reduction says that one sufficient route to
excluding order 45 is

```text
beta(20) + beta(24) <= 225,
beta(21) + beta(23) <= 221,
beta(22) <= 109,
```

where `beta(m)` is an edge maximum over `(4,5,m)` graphs that actually occur
in the relevant neighborhoods.  Since the universal order-20 edge maximum is
100, the first inequality would follow from excluding every occurring
order-24 graph with at least 126 edges.  The family treated here is therefore

```text
F_24 = { H : H is a (4,5,24)-graph and e(H) >= 126 }.
```

The published McKay catalogue is imported as complete.  It contains 352,366
order-24 `(4,5)` graphs, of which exactly 15,913 lie in `F_24`.

## Boundary-trace theorem

Use the convention that a `(s,t,n)` graph has order `n`, no `K_s`, and no
independent set of size `t`.  Suppose `G` is a `(5,5,45)` graph, `v` has
degree 24, and

```text
H = G[N(v)],             |H| = 24,
X = V(G) \ (N(v) union {v}),   |X| = 20.
```

For `x in X`, put `T_x = N_G(x) intersect V(H)`.  For `u in H`, put

```text
c_u = |N_G(u) intersect X|.
```

For a pair `u,w in H`, let `lambda_H(uw)` count their common neighbors in
`H`, and let `mu_H(uw)` count their common nonneighbors in `H` (excluding the
pair itself).  Then all of the following hold, without an automorphism
assumption.

1. Every `T_x` meets every independent 4-set of `H`.
2. For each `u in H`,

   ```text
   19 - d_H(u) <= c_u <= min(17, 23 - d_H(u)).
   ```

3. If `uw` is an edge of `H`, then

   ```text
   |{x in X : u,w in T_x}| <= min(8, 12 - lambda_H(uw)).
   ```

4. If `uw` is a nonedge of `H`, then

   ```text
   |{x in X : u,w notin T_x}| <= 13 - mu_H(uw).
   ```

The same statement handles the complementary neighborhood role after color
complementation.

### Proof

The graph `H` is `(4,5,24)`.  Also `G[X]` has independence number at most
three: an independent 4-set in `X`, together with `v`, would be independent
of size five.  If `H - T_x` contained an independent 4-set, adjoining `x`
would give the same forbidden configuration.  This proves (1).

Every vertex of a `(5,5,45)` graph has degree between 20 and 24, using the
classical value `R(4,5)=25`.  Since

```text
d_G(u) = 1 + d_H(u) + c_u,
```

this first gives `19-d_H(u) <= c_u <= 23-d_H(u)`.  The graph induced by
`N_G(u) intersect X` has no `K_4` (otherwise adjoining `u` gives a `K_5`) and
has no independent 4-set because it lies in `X`.  The value `R(4,4)=18`
therefore gives `c_u <= 17`, proving (2).

For an edge `uw` of `H`, the common exterior neighbors in `X` contain neither
a triangle (adjoin `u,w`) nor an independent 4-set.  Thus `R(3,4)=9` bounds
their number by eight.  The full common-neighbor set of `u,w` contains no
triangle and no independent 5-set, so `R(3,5)=14` bounds it by 13.  That set
contains `v`, the `lambda_H(uw)` common neighbors in `H`, and the common
exterior neighbors, proving (3).

For a nonedge `uw`, their full common-nonneighbor set contains no independent
triple (adjoin `u,w`) and no `K_5`.  Hence `R(5,3)=14` bounds it by 13.  The
root `v` is adjacent to both endpoints and is not counted; partitioning the
remaining vertices between `H` and `X` proves (4).

Equivalently, the 20 traces form the rows of a `20 x 24` binary boundary
matrix subject simultaneously to a hypergraph transversal condition, column
windows, and edge/nonedge pair-codegree caps.  This is the intended receiver
for the next occurrence stage; it is not a graph-by-graph gluing claim.

## Exact transversal census

Let

```text
tau(H) = minimum size of a set meeting every independent 4-set of H.
```

Part (1) implies the shared occurrence constraint

```text
|T_x| >= tau(H) for every x in X,
sum_{u in H} c_u = sum_{x in X} |T_x| >= 20 tau(H).
```

The exact census over the complete catalogue tail is:

| `e(H)` | `tau=7` | `tau=8` | `tau=9` | `tau=10` | total |
|---:|---:|---:|---:|---:|---:|
| 126 | 4,165 | 1,619 | 3,081 | 2,620 | 11,485 |
| 127 | 763 | 302 | 1,192 | 1,144 | 3,401 |
| 128 | 83 | 38 | 392 | 330 | 843 |
| 129 | 6 | 3 | 87 | 51 | 147 |
| 130 | 0 | 0 | 19 | 13 | 32 |
| 131 | 0 | 0 | 2 | 1 | 3 |
| 132 | 0 | 0 | 1 | 1 | 2 |
| **all** | **5,017** | **1,962** | **4,774** | **4,160** | **15,913** |

In particular, the complete `e(H) >= 130` subclass satisfies `tau(H) >= 9`.
The scan also disproves the initially plausible common restriction
`tau(H) >= 9` on the entire tail: 6,979 tail graphs have transversal number
seven or eight.  That failed hypothesis is why the output is stratified
rather than advertised as an exclusion.

For an additional audit statistic, the ranges of the number of independent
4-sets are:

| `e(H)` | minimum | maximum |
|---:|---:|---:|
| 126 | 155 | 195 |
| 127 | 152 | 177 |
| 128 | 149 | 171 |
| 129 | 146 | 165 |
| 130 | 143 | 155 |
| 131 | 143 | 149 |
| 132 | 138 | 144 |

## Reproduction

Obtain `r45_24.g6` from Brendan McKay's Ramsey graph data page.  The exact
input used here has:

```text
352366 lines
SHA256 83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0
```

Compile the exact scanner with GCC 12.2.0 or another C++20 compiler:

```sh
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wconversion -Wshadow \
  -pedantic tau_scan.cpp -o tau_scan
```

A single deterministic run is sufficient:

```sh
./tau_scan r45_24.g6 > all.rows
sha256sum all.rows
python3 -B verify.py r45_24.g6 all.rows
```

The expected row-file SHA-256 is
`f694afe9ee516624234d90537dd6f909c0335ec27143ee854b4a19712813f9dc`.
Each row contains the dense-tail index, edge count, independent-4 count,
minimum transversal size, and one transversal as a 24-bit hexadecimal mask.
`verify.py` checks the catalogue and row hashes, every row's index and graph
statistics, every positive transversal witness, all summary tables, and four
representative minimum claims by a separately implemented exhaustive
meet-in-the-middle calculation.

For the recorded run, four deterministic ranges `[0,4000)`, `[4000,8000)`,
`[8000,12000)`, and `[12000,15913)` took respectively 49.1, 46.0, 46.2, and
42.0 seconds on the campaign host.  Concatenating them in index order gives
the row hash above.  The Python verification took 55.0 seconds.  An
ASan/UBSan build reproduced both 100-record end ranges without a diagnostic.

The optimized C++ program is the exhaustive minimum proof for all entries:
at each target size it branches on every possible vertex of an uncovered
independent 4-set; a disjoint-edge packing supplies only a sound lower-bound
prune.  Memoization keys are sound because the remaining budget is determined
by the fixed target size and chosen mask.  The Python verifier is deliberately
not represented as a second exhaustive proof for all 15,913 lower bounds.

## Trust boundary and provenance

Imported rather than reproved here:

- completeness and graph identities of the McKay `(4,5,24)` catalogue;
- the classical Ramsey values used in the analytic proof;
- the neighborhood-edge reduction motivating the `e(H) >= 126` occurrence
  family.

The scanner independently checks the graph6 syntax, order, edge threshold,
and `(4,5)` property of every emitted record.  Those checks do not certify
that the external catalogue is complete.

Primary public sources:

- [Brendan McKay's Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
- [Angeltveit and McKay, `R(5,5) <= 46`](https://arxiv.org/abs/2409.15709)

The Discovery Net inputs used during development were the neighborhood-edge
reduction `bafkreicgpqb2vyw2qtelysclrfyt6f2rljwzybt3a6f2wgotwgobtb75oy`
(height 3501) and its verification/correction review
`bafkreifxpqqpaifsozor24am6dnux7sczu2yhmrbmjqafjy5wakhob5qpu`
(height 3527).  The review's correction concerns an ancillary `(3,4)`
self-test in the predecessor package, not the order-45 identities used here.

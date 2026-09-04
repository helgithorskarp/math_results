# Excluding seven moving 3-cycles

**Theorem.** If a graph on 43 vertices has neither a clique nor an
independent set of order five, every automorphism of order three has at
least eight moving 3-cycles. In particular, cycle type `1^22 3^7` is
impossible.

The new case is exactly seven moving cycles. The earlier
[sparse-motion theorem](../ramsey_r55_sparse_order2_order3_automorphism_obstruction)
already excludes one through six. No claim is made here to exclude order
three altogether or improve the Ramsey lower bound.

## 1. The equality case of the degree bound

Color graph edges red and nonedges blue. The established bound
`R(4,5)<=25` implies that every vertex has between 18 and 24 neighbors
in each color: a color neighborhood has neither a same-color `K_4` nor
an opposite-color `K_5`, hence has at most 24 vertices.

Suppose the automorphism has seven moving cycles and 22 fixed vertices.
Each moving 3-cycle is a monochromatic triangle, because its three pairs
form a single orbit. Choose a moving triangle `C` and call its color `c`.
Its common color-`c` neighborhood has at most four vertices. Indeed, it
has no color-`c` edge, which would complete a `K_5` with `C`; five vertices
in that neighborhood would therefore give an opposite-color `K_5`.

Let `a` be the number of fixed vertices color-`c` adjacent to `C`, and
let `m` be the number of other moving cycles joined entirely in color `c`
to `C`. Each of the other six cycles has three cross-edge orbits. An
incomplete color-`c` cross block contributes at most two color-`c`
neighbors to each vertex of `C`. Thus

```text
a + 3m <= 4,
d_c(v) <= 2 + a + 3m + 2(6-m)
       = 14 + (a+3m) - 2m
       <= 18 - 2m.
```

Since `d_c(v)>=18`, equality holds throughout. Hence `m=0`, `a=4`,
`d_c(v)=18`, and **every other moving cycle contributes exactly two
color-`c` neighbors** to each vertex of `C`.

Two moving triangles cannot have opposite colors. If `C` were red and
`D` blue, the equality condition at `C` would require six red cross edges
between them, and the condition at `D` would require six blue cross edges.
There are only nine cross edges. This is a contradiction.

After color reversal, all seven moving triangles are red. Every pair of
triangles has six red and three blue cross edges, the blue edges forming
a perfect matching. The fixed vertices are no longer needed: it is enough
to refute the resulting coloring on the 21 moving vertices.

## 2. Cyclic matching covers

Label these vertices `(i,r)`, where `0<=i<7`, `r` is in `Z/3Z`, and the
automorphism sends `(i,r)` to `(i,r+1)`. The three vertices for each `i`
are called a fiber. They are blue-independent. Between fibers `i<j`, an
invariant blue perfect matching has a unique shift `g_ij` in `Z/3Z`:

```text
(i,r) is blue-adjacent to (j,s) iff s-r = g_ij (mod 3).
```

No connectedness assumption is imposed. This family consists of cyclic
threefold perfect-matching covers of `K_7`, with red as the complement.

Independently change the origin in fiber `j` to make `g_0j=0`, for each
`j=1,...,6`. These changes commute with the order-three action and preserve
both colors. There remain exactly 15 freely chosen shifts, one for each
pair among fibers `1,...,6`. Every original cover has such a normalized
representative. We do not quotient further by fiber permutations or by
reversal of the cyclic generator.

**Finite lemma.** None of the `3^15=14348907` normalized covers has both
clique number and independence number at most four.

This lemma has two separate exact verifications, described below.

## 3. Direct enumeration proof

The C++ program constructs blue matchings on explicit vertices and colors
all other pairs red. It adds one complete fiber at a time. When adding
fiber `j`, it fixes its anchor matching to shift zero and enumerates the
`3^(j-1)` matchings to fibers `1,...,j-1`.

After the new fiber is complete, the program tests both colors for a
`K_5`. The clique routine recursively chooses increasing vertices and
intersects the candidate set with the neighborhood of each chosen vertex.
It therefore tests every clique and accepts only an actual clique.

A forbidden set in a prefix persists in every extension, so its subtree
may be rejected. A rejected prefix through fiber `j` has assigned
`j(j-1)/2` of the 15 free shifts and represents exactly
`3^(15-j(j-1)/2)` full assignments. The branches are disjoint. The observed
counts are:

| completed fibers | tested prefixes | rejected | surviving |
|---:|---:|---:|---:|
| 2 | 1 | 0 | 1 |
| 3 | 3 | 0 | 3 |
| 4 | 27 | 14 | 13 |
| 5 | 351 | 301 | 50 |
| 6 | 4,050 | 4,020 | 30 |
| 7 | 7,290 | 7,290 | 0 |

The weighted total of rejected subtrees is exactly 14,348,907. Only
11,722 prefixes are explicitly tested. Every candidate is covered and
none survives. The finite lemma, hence the new order-three exclusion,
follows.

## 4. Independent symbolic certificate

For each of the 15 free pairs, introduce three one-hot Boolean variables
for its possible shifts. There are 45 variables and 60 exactly-one clauses
before clause deduplication. Each of the `binom(21,5)=20349` five-sets
supplies a not-all-blue and a not-all-red clause, with internal and anchor
edges substituted as constants. After exact simplification and
deduplication, the canonical formula has 3,872 clauses.

`generate_formula.py` obtains edge literals by modular differences.
`verify.py` instead constructs actual unordered-pair orbits under the
21-vertex permutation, labels the 45 free orbits, substitutes the other
25 orbits as constants, and independently rebuilds the entire formula.
It compares every generated byte with its canonical reconstruction.

The committed `certificate.rup` has 191 clauses, ending in the empty
clause. For each line, the checker negates its literals and repeatedly
applies unit propagation to the initial clauses and all previously proved
clauses. A contradiction proves that line is entailed. The empty final
line therefore certifies unsatisfiability. Deletions have been omitted;
retaining already valid clauses preserves the soundness of RUP checking.
The checker rejects an invalid first unit, an incomplete proof, and an
out-of-range literal. The stored trace also passes `drat-trim -U`, which
permits only RUP additions.

The SAT solver used for discovery is not required to verify this proof.
Both the complete enumeration and the certificate replay are part of the
standard reproduction command.

## 5. Positive fixture and scope

The direct enumeration finds exactly 30 normalized covers on six fibers
that avoid both forbidden five-sets. Its first survivor is stored as the
45-edge blue graph `fixture18.edges` on vertices `0,...,17`. A separate
literal five-subset audit verifies its coloring, matching structure, and
cyclic symmetry. Thus the threshold seven is sharp **for this particular
cyclic matching-cover family**. The fixture is an 18-vertex test graph,
not a candidate for the 43-vertex target.

The theorem excludes only `1^22 3^7` beyond the previous sparse cases.
The argument does not say that every order-three action reduces to
perfect matchings: the exact degree equality was essential at seven
moving cycles. Order-three types with eight through fourteen moving
cycles remain outside this exclusion.

The imported graph-theoretic input is McKay--Radziszowski,
[*R(4,5)=25*](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The reduction is ordinary unformalized mathematics. The exact computations
trust Python/C++ execution and the small checking implementations. Neither
graph-catalog completeness nor a SAT solver's UNSAT status is trusted.

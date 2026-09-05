# Excluding nine moving 3-cycles

**Theorem.** A graph on 43 vertices with neither a clique nor an independent
set of order five has no automorphism of cycle type `1^16 3^9`.
Together with the earlier exclusions of one through eight moving cycles,
every automorphism of order three has **at least ten moving 3-cycles**,
and hence at most 13 fixed vertices.

This is a structural restriction on a hypothetical Ramsey graph, not a
43-vertex construction or an improved Ramsey lower bound. An element with
nine disjoint 3-cycles has order three; this theorem is distinct from the
earlier exclusion of elements of order nine.

## 1. The deficit budget at nine cycles

Use red for edges and blue for nonedges. By the established theorem
`R(4,5)=25`, every color-degree lies between 18 and 24: a color
neighborhood has neither a same-color `K_4` nor an opposite-color `K_5`.

Every moving 3-cycle is a monochromatic triangle. For one such triangle
`C_i`, let `c_i` be its internal color, `a_i` the number of fixed
vertices adjacent to it in color `c_i`, and `w_ij in {0,1,2,3}` the
number of neighbors in `C_j` of a vertex of `C_i` in color `c_i`.
Invariance makes this last count independent of the vertex chosen.
Let `m_i` count the complete blocks `w_ij=3`.

The common color-`c_i` neighborhood of `C_i` has at most four vertices.
It has no color-`c_i` edge, since such an edge would extend `C_i` to a
`K_5`. Five vertices there would therefore form an opposite-color
`K_5`. Fixed neighbors contribute `a_i`, and each complete block
contributes three vertices. Also the own-color degree is at least 18.
Thus

```text
a_i + 3m_i <= 4,
2 + a_i + sum_(j != i) w_ij >= 18.                    (1)
```

There are now eight other moving cycles. Define

```text
delta(w) = 2 - w + 3*[w=3],
delta(0),delta(1),delta(2),delta(3) = 2,1,0,2.
```

Eliminating `a_i` in (1) gives

```text
D_i := sum_(j != i) delta(w_ij) <= 4.                 (2)
```

The common-neighborhood constraint must still be retained. For example,
weights `(3,3,2,2,2,2,2,2)` have total deficit four but two complete
blocks, which already contribute six common neighbors. Exactly 28
weight vectors satisfy (2) but have no feasible fixed count: select two
of eight positions for weight three and set the rest to two.

More precisely, the exact local arithmetic is

```text
m_i <= 1,
max(0,D_i-3m_i) <= a_i <= 4-3m_i.                    (3)
```

Indeed `sum w_ij = 16+3m_i-D_i`, so the own-color degree is
`18+a_i+3m_i-D_i`. The lower degree bound and common-neighborhood cap
give (3). Conversely, (3) makes that degree lie between 18 and 22, so
the upper bound 24 is automatic. Existence of a feasible fixed count
is equivalent to `D_i<=4` **and** `m_i<=1`, rather than to (2) alone.

Exhausting all `4^8=65536` weight vectors and the 17 fixed counts
`a_i=0,...,16` gives 987 feasible local arithmetic profiles:
635 with no complete block and 352 with one. These are necessary local
profiles, not a claim that all are realized by graphs.

## 2. Exhaustive normalizations

Label moving vertices `3i+s`, with `0<=i<9` and `s in Z/3Z).
The automorphism rotates `s -> s+1`. Vertices 27 through 42 are fixed.

Global complementation permits the number `r` of red moving triangles
to lie in `{0,1,2,3,4}`, since there are nine triangles. Permuting
moving cycles then puts those red triangles first. This covers every
internal color pattern, including the four-red/five-blue split.

For moving cycles `i<j`, let `b_ij,d` be the red edge bit for difference
`d in Z/3Z`; the edge from `3i+s` to `3j+t` has bit `b_ij,t-s`.
Independent changes of origin in cycles 1 through 8 cyclically rotate
their anchor words to one of `000,100,110,111`. Hence impose

```text
b_0j,0 >= b_0j,1 >= b_0j,2.
```

These changes commute with rotation and leave fixed-to-moving incidences
unchanged. Constant anchor words are allowed, and uniqueness is not needed.

Each fixed vertex has a nine-bit red incidence signature to the moving
cycles. Permuting the sixteen fixed vertices sorts these signatures
lexicographically. This preserves the anchor normalization and allows
equal signatures. Thus every possible graph retains a representative
among the five formulas. An explicit-graph audit checks all 512 internal
color profiles under these operations, including color reversal,
cycle permutation, phase changes and fixed-vertex sorting.

## 3. Variables and complete constraints

There are 381 unordered-pair orbits under the permutation. Nine are
constant internal triangles. The 372 primary red edge variables are:

1. 108 moving cross bits, ordered by moving-cycle pair and difference;
2. 120 fixed-fixed bits, ordered by fixed-vertex pair;
3. 144 fixed-to-moving bits, ordered by fixed vertex and moving cycle.

Every one of the `binom(43,5)=962598` five-sets supplies not-all-red and
not-all-blue clauses. Constants are substituted, repeated literals
removed, and duplicate clauses deduplicated. No five-set, graph catalog,
or class of fixed graphs is omitted.

For each moving-cycle pair and each internal color occurring at an
endpoint, three truth-table gates encode

```text
u = [delta(w)>=1], v = [delta(w)>=2], z = [w=3].
```

All eight valuations of the three red cross bits are used. For each
valuation and output gate, the clause consists of the three input
literals falsified by that valuation and the correct output literal.
Exactly the correct output is therefore forced. Same-color endpoints
share the gates; opposite-color endpoints use separate gates.

For each moving triangle the sixteen unary `u,v` tokens sum to its
deficit. All negative five-token clauses impose (2).
Two prefix counters impose (1):

- The 16 fixed own-color incidences and three copies of each of eight
  complete-block gates have sum at most four.
- At least 16 of the 16 fixed own-color incidences and 24 moving cross
  bits have the own color. Equivalently at most 24 of their negations
  are true. Adding the two internal neighbors gives degree at least 18.

Each counter has 40 input occurrences. Blue incidences are negative red
literals; repeated complete-block gates are counted with weight three.
In particular, the first counter enforces `m_i<=1` even though the
deficit budget alone does not. The formula does not add any unproved
condition on fixed degrees, local deficiency, or an exceptional core.

### Counter soundness and completeness

For inputs `x_1,...,x_n` with bound `k`, a variable `S_ij` exists
for `1<=j<=min(i,k+1)`. Clauses impose

```text
x_i -> S_i1,
S_(i-1),j -> S_ij                       (when the predecessor exists),
(x_i AND S_(i-1),(j-1)) -> S_ij          (j>1, predecessor exists),
NOT S_n,(k+1).
```

The last clause is included when that threshold variable exists.
Induction forces `S_ij` whenever at least `j` of the first `i`
occurrences are true, so an overflow contradicts the last clause.
Conversely, assigning actual prefix thresholds satisfies all clauses
when the bound holds. This proves the required auxiliary extension,
including signed and repeated inputs. The production function is
separately tested on 1,734 small input assignments.

The at-most-four counter has 190 auxiliary cells, and the at-most-24
counter has 700. Together with the truth-table gates the full variable
count is `8490+3r(9-r)`.

### Lexicographic sorting

For adjacent fixed signatures `A,B`, each coordinate `q` and each
possible common binary prefix of length `q` yields a clause excluding
that prefix together with `A_q=1,B_q=0`. At the first unequal coordinate
the matching-prefix clause enforces the desired order. Other clauses
are satisfied; equal signatures satisfy all clauses. This is exactly
lexicographic nondecreasing order. A four-coordinate exhaustive truth
table independently checks the clause schema.

## 4. Exact formula auditing and proof replay

The Python generator maps cross edges by modular differences.
The separate C++ checker instead constructs all 903 actual unordered
vertex pairs, joins them under the permutation with disjoint-set union,
and obtains the 381 pair orbits. It reconstructs all primary and auxiliary
clauses, including gates, counters and normalizations, and compares
the **complete canonical DIMACS stream byte-for-byte**.

| red triangles | variables | clauses | reference binary DRAT bytes |
|---:|---:|---:|---:|
| 0 | 8,490 | 609,409 | 12,162,845 |
| 1 | 8,514 | 612,097 | 15,794,263 |
| 2 | 8,532 | 614,113 | 17,349,019 |
| 3 | 8,544 | 615,457 | 16,312,980 |
| 4 | 8,550 | 616,129 | 20,367,008 |

All five formulas are UNSAT with traces checked by `drat-trim`.
These general DRAT traces may contain RAT steps and deletions; they
must not be described as addition-only RUP certificates.
The fresh reproduction regenerates the formulas and traces, verifies
every complete formula, and replays each trace to `s VERIFIED`.
A solver verdict or a stored hash alone is never counted as a proof.

The large generated formulas and traces remain outside Git. Their
generators, exact commands, tool-source commits, tested binary hashes,
formula/proof hashes and compact results are committed. The standard
command regenerates the proof evidence; no original scratch file is
needed. A differing regenerated proof hash is acceptable only after the
proof checker verifies that trace against the identical audited formula.

The C++ checker passes optimized and ASan/UBSan builds on representative
uniform and mixed internal colors. Missing-clause and changed-literal
mutations are rejected. Local arithmetic, counters, relabeling and
lexicographic audits check the changes from the eight-cycle package.

All five internal-color cases are therefore impossible. Since every
hypothetical graph has a normalized encoding in one of them, this proves
the nine-cycle exclusion.

## 5. The moving vertices alone do not suffice

The committed `moving27.edges` is a graph on 27 vertices with 177 red
edges. Its nine moving triangles comprise four red and five blue
triangles. A literal audit verifies all 80,730 five-subsets, cyclic
invariance, deficit at most four at every triangle, and at most one
complete own-color block per triangle.

Thus the moving-vertex constraints admit a valid partial graph. This is
a positive test of the relaxation, not a target witness. The full theorem
prevents its extension by sixteen fixed vertices while retaining this
rotation and the Ramsey property.

## 6. Dependencies, scope and trust

The external graph-theoretic input is McKay and Radziszowski,
[*R(4,5)=25*](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The minimum-ten corollary imports the previous
[eight-cycle theorem](../ramsey_r55_order3_eight_cycle_obstruction) and its
predecessors, whose chain was
[independently reviewed](../ramsey_r55_order3_eight_cycle_review1).
The new nine-cycle exclusion itself does not use that predecessor,
the order-five theorem, a graph catalog, or the hard-deficiency branch.

The mathematical reduction and normalization/counter proofs remain
unformalized. Exact execution trusts the Python/C++ implementations,
compiler and hardware, and the external DRAT checker. The solver is
used to produce evidence, not as a trusted UNSAT oracle. Internal
reconstruction and testing are not independent peer review of this new
result. Types with ten through fourteen moving 3-cycles remain unresolved
by these packages.

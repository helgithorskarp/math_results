# Exact aggregate formulation

## Scope inherited from the reviewed task cover

For a red cut matrix `M` between sides A20 and B23, write `M=UV^T` over F2.
The h3825 task cover, independently accepted at h3831, gives 10,959 canonical
multisets for the rows of `U`.  They represent all 154,847,637 admissible
spanning row profiles under the reviewed multiplicity caps and the dual
GL(4,2) factor action.  That imported number is context from h3825; this
package does not present a new global profile census.

One exactly-one selector chooses a row task.  Its implications fix the sorted
20-label physical row list.  The 23 column labels remain one-hot variables,
are sorted only by physical vertex relabeling, span F2^4, have zero
multiplicity at most two and nonzero multiplicity at most five, and cannot use
zero when the selected row list uses zero.  Sixteen exact support indicators
impose total support size at most eight, counting zero when present.

The support bound is invariant under every permitted factor-basis change.  It
defines one broad sector across all 10,959 canonical row tasks; no row
multiplicity profile or column support set is fixed.

## Physical graph and structural conditions

All 903 edges of K43 receive physical Boolean variables.  The 443 same-side
edges are unrestricted in advance.  Star variables compute the dot product of
each nonzero F2^4 label with every column label.  Selector-controlled clauses
then equate each of the 460 cross-edge variables with its required dot product.

Both factors span, so the red cut has rank four.  The complement cut has matrix

```text
M + 1_A 1_B^T.
```

For nonzero vectors `p,q`, its rank drops to three exactly when every row label
has dot product one with `p`, every column label has dot product one with `q`,
and `p.q=1`.  The formula emits one 344-literal clause for each of the 120
pairs with `p.q=1`.  These clauses forbid exactly the rank-three complement
cases and impose the reviewed blue-rank lower bound.

For every label that occurs three times on A, a gated cardinality encoding
requires 10--13 red cross contacts, using h3771.  Equal factor rows have no
cross-cut distinguishers, so h3579 requires at least eight internal A
distinguishers for each equal row pair.  The dual condition is imposed for
equal columns inside B.  Sorted lists and the multiplicity caps imply that an
equal row pair has positional distance at most two and an equal column pair
has distance at most four; the formula tests exactly those 37 and 82 possible
pairs.  The public controls verify that these windows omit no equal pair.

Every vertex has red degree between 18 and 24, as required by `R(4,5)=25`.
Finally, for each of all 962,598 five-vertex sets, the formula emits a clause
forbidding ten blue edges and another forbidding ten red edges.  Because every
edge has its own physical variable, these are exactly 1,925,196 distinct
length-ten clauses.

## Dimensions

| Block | Variables | Clauses |
|---|---:|---:|
| Canonical row selector | 22,237 | 254,454 |
| Physical edge variables | 903 | 0 |
| Column labels, caps, support, span | 504 | 6,361 |
| Dot-product cross edges | 345 | 19,780 |
| Complement-rank guard | 0 | 120 |
| Tripled-row contacts | 8,865 | 18,525 |
| Equal-label pair distances | 30,117 | 67,509 |
| Degree interval | 84,624 | 170,710 |
| Physical five-sets | 0 | 1,925,196 |
| **Total** | **147,595** | **2,462,655** |

The DIMACS file is 138,709,891 bytes with SHA-256
`e01a3aec66bf8d3bd0ce8aba611634abc3f5068ad6ad56511be00186d6832989`.

A satisfying assignment would decode to an actual 43-vertex graph and would
be checked clause by clause and on every physical five-set.  An UNSAT result
would exclude this support sector only after an independent DRAT check.  The
recorded call returned neither result, so the family remains undecided.

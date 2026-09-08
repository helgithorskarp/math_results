# K4 expansion and its compact threshold encoding

Red is adjacency and blue is nonadjacency. A good43 has no monochromatic
five-set. This result applies to every prescribed monochromatic K4 in the
h3887 complete maximal-packing cover. It derives a redundant but strongly
propagating physical constraint; it does not remove any good physical model.

## 1. Expansion from the separator theorem

Let Q be a K4 of color c in a hypothetical good43 and define

    Gamma_c(Q) = {v outside Q : some edge from v to Q has color c}.

Suppose `|Gamma_c(Q)| <= 18`. Delete this set from the color-c graph. The
four vertices Q remain a component, since every color-c edge from Q went to
the deleted set. At least `43-4-18=21` other vertices remain, so another
component also remains. This is a nontrivial separation of order at most 18,
contrary to the h3897 classification. Hence

    |Gamma_c(Q)| >= 19.                                      (1)

Equivalently, at most 20 outside vertices are anticomplete to Q in color c.
This is also the complete h3897 cut rule with `A=Q` and every 21-subset B of
the outside vertices. For each B, at least one edge across Q--B has color c.
The other-color half of the cut rule already holds for every single outside
vertex: four color-c contacts would complete Q to a color-c K5. Thus (1),
together with the ordinary five-set clauses, captures the complete cut
subfamily having one side equal to a prescribed block. Larger B give no new
condition after all 21-subsets are covered.

There are `binom(39,21)=62,359,143,990` minimal clauses per block if written
directly. Each clause contains four physical edges for each of 21 vertices,
so it has width 84. Writing all B of sizes 21 through 39 would use
205,954,642,534 clauses per block.

## 2. Contact variables

For every block Q and outside vertex v, let `z_v` mean that all four Q--v
edges have the color opposite Q. If `l_1,...,l_4` are the signed physical
literals meaning that those edges have Q's color, define z by

    (-z or -l_i)                          for i=1,...,4,
    ( z or l_1 or l_2 or l_3 or l_4).

These five clauses have exactly one z-extension for every physical edge
assignment, and it is `z = not(l_1 or ... or l_4)`. The expansion theorem is
therefore `sum_v z_v <= 20`.

The physical edge map is reconstructed without a catalog: enumerate the 903
unordered pairs lexicographically from DIMACS variable 2, omitting the six
internal edges of every four-block and all edges internal to the residual
core. The color of block i is red for `i<r` and blue otherwise. This is
exactly the h3873/h3887 convention. All Q--v edges are physical variables.

## 3. Exact unary threshold recurrence

Order the 39 outside vertices and introduce `s[i,j]`, for
`1<=i<=39` and `1<=j<=min(i,21)`, with intended meaning

    s[i,j] iff at least j of z_1,...,z_i are true.

There are `1+...+21 + 18*21 = 609` such variables. Starting with
`s[1,1] iff z_1`, define

    s[i,1] iff s[i-1,1] or z_i,
    s[i,j] iff s[i-1,j] or (s[i-1,j-1] and z_i).

At the diagonal `j=i`, the nonexistent `s[i-1,i]` is false, leaving an AND.
The OR, AND, and mixed recurrences use respectively three, three, and four
clauses of width at most three. Finally add `-s[39,21]`. Induction on i proves
that every z-assignment has one extension to all s variables, and this
extension satisfies the final unit exactly when at most 20 z variables are
true.

The recurrence uses 2,377 clauses. Together with 195 contact-definition
clauses, one block uses 648 variables and 2,572 clauses of maximum width five.
Different blocks receive disjoint auxiliary ranges after the complete h3887
formula. Physical edge variables may occur in several block interfaces, as
they must, while the unique extension remains a direct product once the
physical assignment is fixed.

## 4. Propagation boundary

If 21 vertices are fixed anticomplete in the block color, their four-edge
definitions propagate 21 true z variables. The forward threshold recurrence
then propagates `s[39,21]`, contradicting its negative unit.

For exactly 20 true z variables, the recurrence also propagates every other
z false. One direct induction makes this explicit. True selected inputs
propagate each attained prefix count forward. The final false 21-threshold,
combined backward with selected suffix inputs, propagates the complementary
unattained threshold at every split. At an unselected position, the mixed
recurrence then becomes the unit clause forbidding that input. Setting z
false reduces its five-literal definition to the four-edge disjunction that
requires a block-color contact.

The checker exhausts the recurrence semantics for every bit string through
n=9 and every nontrivial threshold, checks each recurrence gadget truth table,
and tests 32 differently placed 20-subsets at n=39 both at the forcing
boundary and after adding a 21st input. These controls validate the
implementation; the recurrence induction proves the general statement.

## 5. Complete ordered-family integration

For q=7,8,9,10, append q independent block interfaces after either h3887's
direct formula or its h3881 shared-triangle form. The added sizes are:

| q | Added variables | Added clauses |
|---:|---:|---:|
| 7 | 4,536 | 18,004 |
| 8 | 5,184 | 20,576 |
| 9 | 5,832 | 23,148 |
| 10 | 6,480 | 25,720 |

Every good physical model of the base formula has a unique auxiliary
extension by (1). Conversely, deleting auxiliaries from any augmented model
leaves the unchanged base formula. Thus the formulas have exactly the same
physical model sets and are equisatisfiable task by task. Whole-block order,
triangle variables, core labels, task IDs, and the 2,189,178-task coverage
are unchanged.

All 18 `(q,r)` suffixes are independently reconstructed and compared literal
by literal. A complete `bo1-q7-r7-c000000` shared-triangle formula is also
generated and read from its first physical clause through its last expansion
unit by the pinned independent h3887 backends plus a separate implementation
of this suffix. The compact and full audits agree under normal and `-O`
Python. No solver is invoked.

## 6. Scope and trust

The structural input is h3897, source commit
`4b6455643c0dba1222231b66c1dedca699cf03e9`, whose new separator theorem is
internally checked but externally unreviewed at this milestone. It imports
R(4,5)<=25 and exact small-graph enumeration. The ordered family is h3887,
source commit `869077b78dd8a6d8a04c499d3ada80ac35e69d22`, transitively importing
h3873, h3881, h3835, and catalog completeness. Both source manifests are
hash locked before integration.

Additional trust includes the written reduction, Python/file semantics,
source/checker transcriptions, SHA-256, and ordinary hardware. This is a
compact redundant encoding with an exact propagation guarantee. It is not
a solver timing result, task exclusion, candidate, good43 certificate,
external review, or Ramsey-number improvement.

# Review: exactly two supporting oriented quotients through six vertices

## Verdict

**Accept, high confidence.**  I found no mathematical or computational defect
in Discovery Net contribution
`bafkreiazsjreqa3bfywunpv7cv52h2zdq7gkd4hjexbcftzy3xeadfej4i`, inspected at
the exact source commit
`c4a7893cf346a8a761d05f3195b06b542249b94c`.

The proof establishes that, up to isomorphism, exactly two nonempty oriented
quotients on at most six vertices admit positive weights with strict weighted
Hall deficiency at every root: the known Dzitsoev tournament and one quotient
having a single missing pair.  Their feasible weight sets are covered by
twelve and eight explicit unimodular cones.  For positive integer weights the
minimum totals are 36 and 51, and the minimum external out-degrees are 13 and
18.  The transfer to substitutions is valid when every nonempty part contains
an internal strong Seymour vertex.

Target source:
https://github.com/helgithorskarp/math_results/tree/main/graph_theory/strong_seymour_six_oriented_quotients

Reviewer evidence:
https://github.com/helgithorskarp/math_results/tree/main/graph_theory/strong_seymour_six_oriented_quotients_review1

## Written proof audit

For a quotient root `p`, the target of a source `S` is correctly defined as
the union of the out-neighborhoods of `S`, with `N+(p)` and `p` removed.  This
retains vertices nonadjacent to `p`, which is essential once the quotient is
not a tournament.  Adding every out-neighbor whose individual target is
already contained in the current target preserves that target and can only
increase positive source weight.  Hence a strict Hall witness always has a
nonempty closed witness.

Choosing one closed witness at each root produces a six-row matrix `A`.  If a
nonzero `c >= 0` has `c A <= 0`, then `A w > 0` is impossible for every
positive `w`; this is a direct weighted sum of the six strict inequalities.
Conversely, the computation does not assume a bounded-multiplier completeness
theorem.  It supplies such a multiplier for every rejected finite system and
supplies a positive exact solution of `A w = 1` for every remaining system.

For each of the twenty survivors, `det(A)=-1` and `A^{-1}` is a nonnegative
integer matrix.  Thus every positive defect vector `d` gives positive weights
`w=A^{-1}d`, while an integral weighting has integral `d=A w >= 1` and hence
`w >= A^{-1}1` componentwise.  This proves all nonnegative linear minima,
including total weight and each root's external out-degree.  Taking the
minimum over the complete cone list gives 36/13 for the tournament and 51/18
for the missing-pair quotient.  The displayed minimum vectors have Hall
deficiency exactly one at every root.

The coefficient-four example is also sound.  Its positive left and right
kernel vector is `(1,1,4,1,1,4)`, and the checked rank-five minor makes both
kernels one-dimensional.  A nonnegative multiplier with `c A <= 0` must lie
in the left kernel after pairing with the positive right kernel.  Therefore
its primitive integral form genuinely needs coefficient four.

The reduction from orders below six is valid: adjoining a new vertex that
dominates every existing vertex preserves all old witnesses, while the new
root may take its whole out-neighborhood with empty target.  Repeating reaches
order six and leaves a source vertex, which neither classified survivor has.

Finally, for a substitution `Q[F_i]`, the matching link of a vertex in `F_i`
is the disjoint union of its internal link and the expanded quotient link.
An external out-part cannot send arcs back into `F_i`, and `F_i` has no arc to
an external exact second-neighbor part.  Sources within an external part are
twins, so Hall deficiency on that component is exactly the weighted quotient
deficiency.  Thus a vertex is strong precisely when it is internally strong
and the quotient root is not deficient.  The hypothesis that each part has
an internal strong vertex is exactly what makes the stated equivalence work.

## Independent computation

All thirteen entries in the target manifest passed.  Normal and sanitized
primary target runs reproduced `EXPECTED_PRIMARY.json` byte-for-byte, SHA-256
`2fd8a49b3e48b0fe0676b03cae4564f28febaecb546834d120f6e6d2c8f33f77`.
Normal and optimized target secondary runs under Python 3.12.14, NumPy 2.5.3,
and pynauty 2.8.8.1 reproduced `EXPECTED_INDEPENDENT.json` byte-for-byte,
SHA-256
`d0dad08f12f3fc249a7a7fd5222362c911a7d83929b2318f7b96192595875bf4`.
The generated 51-vertex matrix matched the committed file.

The reviewer audit is algorithmically separate from both target paths.  It
uses complete vertex augmentation with a fixed-stride packed adjacency
representation and brute label canonicalization, rather than scanning all
`3^15` labels with an orbit bitmap or invoking nauty.  It groups all source
subsets by their actual Hall target to reconstruct closures.  It then searches
all primitive coefficient vectors in `{0,1,2,3}^6`, followed by every
primitive vector in `{0,1,2,3,4}^6` containing a four; every unobstructed
matrix must have a positive exact unit solution computed independently by
Bareiss determinants and Cramer's rule.

This gives augmentation counts `1,2,7,42,582,21480`, exactly 13,348 types
with an empty root option, 235,526 Hall systems, 235,505 coefficient-three
obstructions, one coefficient-four obstruction, and twenty feasible systems
on exactly the two claimed quotients.  Cone totals, minimum degrees, the four
36/51-vertex matching profiles, and the literal 51-vertex graph all agree.
Normal, optimized, and address/undefined-behavior-sanitized reviewer runs are
byte-identical to `EXPECTED_OUTPUT.json`, SHA-256
`7abc973f6d0185f6faec318590e9007b56e611d9de54b7ce550e00c6c3467963`.

## Guarantees, assumptions, and gaps

The finite checker proves exhaustive coverage of oriented quotient types and
their closed Hall systems, conditional only on the elementary closure and
Hall reductions in the written argument.  It uses exact integer arithmetic;
no floating-point feasibility result, weight cutoff, random seed, or solver
status is evidence.

The trust base still includes the written correspondence between quotient
deficiency and substitution matchings, the canonical-augmentation argument,
C++/Python integer semantics, compiler and hardware correctness, filesystem
reads, and SHA-256.  This is not proof-assistant formalized.

The theorem concerns uniform quotient substitutions with at most six
nonempty parts and assumes each part contains an internal strong vertex.  It
does not classify arbitrary oriented graphs, quotients with seven or more
parts, substitutions containing a no-strong part, or partial/nonuniform
inter-part arc patterns.  It neither settles existence at minimum out-degree
six nor improves the unrestricted tournament order interval `16 <= m <= 23`.

The primary paper of Bai--Li--Park defines strong Seymour vertices and proves
existence for oriented graphs of minimum out-degree at most five.  Targeted
searches found no primary source classifying the missing-arc six-quotient
case.  Novelty is therefore plausible relative to the inspected literature,
not historically certified.

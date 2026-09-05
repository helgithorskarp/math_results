# Two residual C3-square actions and the order-27 obstruction

Let G be a graph on 43 vertices with neither a red nor a blue K5.
The imported order-three motion theorem says that every nonidentity
order-three automorphism fixes at most ten vertices. The imported
order-nine theorem excludes elements of order nine.

**Computer-assisted theorem.** If `H <= Aut(G)` is isomorphic to
`C_3 x C_3`, then H has exactly one global fixed vertex, two orbits of
size three, and four regular orbits of size nine. The stabilizers of
the two three-vertex orbits either coincide or are distinct. Both
possibilities remain open; neither is asserted to be realized by G.

**Group-theoretic corollary.** `27` does not divide `|Aut(G)|`.
Combined with the earlier exclusion of all prime divisors at least five,
the automorphism-group order is `2^a 3^b` with `0<=b<=2`.

**Conditional corollary.** In the M=214 hard branch only, `9` does not
divide `|Aut(G)|`, so there `b<=1`. This does not change the separate
hard-branch profile census or exclude the M=214 branch itself.

## Complete action classification

Regard H as the additive group of `F_3^2`. Its orbits have sizes 1,3,9.
Every transitive H-set is `H/K`; since H is abelian, its stabilizer K
determines it up to H-set equivalence. Let a count global fixed vertices,
c count regular orbits, and b_L count three-vertex orbits stabilized by
the projective line L. There are four such lines. For a nonzero h in L,

```
Fix(h) = a + 3 b_L <= 10,
a + 3 sum_L b_L + 9c = 43.                            (1)
```

Changing the chosen basis of H does not impose a new graph automorphism;
it changes the coordinates used to describe the same subgroup action.
The induced projective action of GL(2,3) on the four lines is all S4.
For example, GL has 48 matrices, only its two scalar matrices act trivially
on all four lines, and the faithful quotient of order 24 is a subgroup of
S4 of the same order. Thus the four multiplicities can be sorted.

The equation implies `a=1 mod 3`; the fixed bound implies `a<=10`.
For `a=1,4,7,10`, each `b_L<=3,2,1,0`, respectively. Also `0<=c<=4`.
Exhausting these small integers in (1) gives 18 sorted types. An independent
enumeration by total numbers of three-orbits gives 117 ordered types,
partitioned into the same 18 orbits by the explicitly enumerated projective
action. All types have a regular orbit, so the constructed action is faithful.
The actual nine permutations are checked for group law, faithful action and
all eight fixed-point counts.

The source realizes quotient orbits using the four linear forms
`x`, `y`, `x+y`, `x+2y`; the stabilizer is the kernel of the corresponding
form. On a quotient copy, translation `(u,v)` adds the form value to its
coordinate in F3. On a regular copy it translates both coordinates in F3².
Vertices are ordered as a fixed points, then the quotient copies in form
order, then c regular copies, each regular copy in row-major coordinates.

## Exact invariant-coloring formulas

For each action put one Boolean red variable on each unordered-pair orbit.
There are 103 through 135 variables. Every one of the 962,598 vertex
five-sets contributes the positive clause requiring a red edge and the
negative clause requiring a blue edge, after duplicate orbit literals are
removed. Clauses are deduplicated and canonically sorted. Finally variable
1 is set red, which is valid under global color complementation.

There are no other symmetry-breaking constraints, auxiliary variables,
selected internal-color patterns, degree-profile assumptions, graph-catalog
inputs or omitted fixed graphs. Thus a satisfying assignment is exactly a
normalized H-invariant Ramsey coloring; every hypothetical coloring has
such an assignment after a possible global complement.

The Python generator names a pair by its least image under all nine group
translations. The C++ checker independently joins all 903 pairs under the
two generators by disjoint-set union, then reconstructs all five-set clauses
with literal vertex loops. Every canonical clause in every complete formula
is compared. This checks the whole instance, not only proof-used clauses.

A bounded 18-case run returned verified UNSAT in 16 cases, and UNKNOWN
after 60 seconds in cases 9 and 10. Timeouts are not exclusions. Their
exact surviving parameters are

```
case  9: a=1, b=(0,0,0,2), c=4,
case 10: a=1, b=(0,0,1,1), c=4.
```

All sixteen UNSAT traces were independently replayed by drat-trim. Their
retained cores/proofs were also replayed, every retained core clause was
checked against its reconstructed formula, and fresh formula reconstruction
and proof replay verified the exclusions again. General DRAT is needed;
the proofs can contain RAT steps and deletions. The published manifests
record hashes; generated formulas and large proofs remain outside Git.

For case 9, two nonidentity elements fix seven vertices and six fix one;
their moving-cycle counts are twelve and fourteen respectively. For case
10, four elements fix four vertices and four fix one; their moving-cycle
counts are thirteen and fourteen. In both cases H itself fixes exactly
one vertex. This proves the theorem as a necessary action restriction.

## Why a subgroup of order 27 is impossible

Suppose `P <= Aut(G)` has order 27. Every subgroup of order nine is
`C_3^2`, since the other group of order nine is cyclic and an element of
order nine is already excluded. Choose an order-nine subgroup H of P.
It has index three and is normal in the 3-group P. Its unique fixed vertex
is preserved by P: for p in P, normality sends an H-fixed vertex to another
H-fixed vertex. Therefore P has a global fixed vertex. It has exactly one,
since any P-fixed vertex is also H-fixed.

An orbit of P of size three would have a stabilizer K of order nine.
Such a K is normal, again because it has index three in a 3-group. Hence
K stabilizes each point of that orbit, giving it at least three fixed
vertices. This contradicts the theorem, which gives exactly one fixed
vertex for every C3-square subgroup.

The remaining P-orbits thus have sizes nine or twenty-seven. Consequently
`43-1` would be divisible by nine. It equals 42, a contradiction. A finite
group whose order is divisible by 27 has a subgroup of order 27 inside a
Sylow 3-subgroup, proving the divisibility conclusion. This deduction uses
the action restriction above; no separate order-27 search is performed.

The elementary group facts used here follow from standard p-group arguments:
index-p subgroups in a p-group are normal, and a p-group contains subgroups
of each order dividing its order. For the latter, induction through a central
subgroup of order p suffices. Groups of order p² are abelian, hence of type
C_(p²) or C_p².

## M=214 consequence and scope

The previously proved M=214-specific order-three bound permits at most
twelve moving triangles. Each surviving C3-square type has an element
with fourteen moving triangles, so neither can occur in that branch.
Thus no C3-square subgroup exists there. The cyclic order-nine possibility
is already excluded globally, so no order-nine subgroup exists in the
branch and nine cannot divide its automorphism-group order.

Globally, C3-square subgroups remain possible in the two displayed types;
the proof does not show `9` fails to divide the global group order. Nor
does the subgroup-order restriction exclude asymmetric colorings or
produce a 43-vertex Ramsey graph.

## Dependencies and trust

The action cover imports the final minimum-eleven motion theorem in
`ramsey_r55_order3_ten_cycle_signature_propagation`. That last four-case
closure has internal formula/proof checks and awaits independent review.
Its previously recurring internal-color dependency now has an accepted
independent review in `ramsey_r55_order3_ten_cycle_obstruction_review1`;
the earlier matching, phase and signature refinements were also reviewed.
The order-nine element exclusion and M=214-specific upper bound have
accepted independent reviews.

The new arguments remain unformalized. Source correctness, exact Python
and C++ semantics, the compiler, SHA256, the executing hardware and
drat-trim are trust boundaries. Solver verdicts and stored hashes alone
are not certificates. This new action restriction and its corollaries
have internal checking, not an independent peer review.

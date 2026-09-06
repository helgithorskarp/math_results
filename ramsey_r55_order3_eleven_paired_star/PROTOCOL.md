# One paired-star optimization on a fixed C3 coloring

Input: the explicit Core186 coloring with SHA-256
`f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441`.
It has vertices 0..42; listed pairs are red and all others blue. The C3
action cycles 0..2, 3..5, ..., 30..32 and fixes 33..42. Its prescribed
four-versus-seven internal split and eighteen Core186 bits remain fixed.

Choose the fixed vertices 33 and 35 before the calculation. Their separate
star penalties in the preceding exact census were the two smallest, 160
and 157 against an input score of 155. For each root, reassign its eleven
moving-triangle contacts uniformly within each triangle. Bits 0..10 of
mask A encode root 33; bits 11..21 encode root 35. Every other edge keeps
its input color, including the mutual edge {33,35}. This gives precisely
2^22 distinct labeled colorings. No degree or Ramsey-only side condition
is imposed. Do not update the base or begin another pair or sweep in this
milestone.

## Exact finite objective

For a physical five-set Q, mark all its variable root-to-moving pairs and
let S be their Boolean-index support, collapsing repeated indices. There
are at most six variable pairs: Q can contain zero, one, or two roots,
giving respectively at most zero, four, or six. Thus at least four pairs
are fixed. If these fixed pairs contain both colors, Q cannot contribute.
Otherwise its unique fixed color c determines a monomial: Q contributes
exactly when every bit in S has color c. Count its physical multiplicity
once. Supports have at most six bits. Empty supports count unconditional
sets, including sets through one or both roots.

With coefficient maps B and R the separate blue and red counts are

    B(A) = sum(B[S] : S & A == 0),
    R(A) = sum(R[S] : S & A == S).

The producer scans all 962,598 five-sets and evaluates every mask by two
22-bit subset zeta transforms. All intermediate values are nonnegative
and bounded by the sum of the corresponding coefficients, at most 962,598.
Unsigned 32-bit arrays are therefore exact; their width is checked. Files
blue.bin and red.bin contain 2^22 unsigned 32-bit counts, in ascending A
order, serialized explicitly in little-endian order. They are regenerated
outside Git, not published as raw tables.

## Independent check

Partition possible K5s by the subset of the two roots they contain.
The rest is a monochromatic K5, K4, or K3 in the graph with both roots
removed. Check all fixed contacts to the chosen roots; with two roots,
also check their mutual color. Variable contacts give S. Bit-intersection
clique recursion therefore reconstructs every coefficient by a different
algorithm from the literal producer, including its color and multiplicity.

The verifier imports no producer or transform. It visits all assignments
in reflected binary Gray order g(j)=j xor floor(j/2), a bijection of
0..2^22-1. Adjacent assignments differ in bit v2(j); only monomials whose
support contains that bit change. Evaluate each affected monomial directly
at both assignments and add its exact difference. Compare both resulting
color counts against the saved table at every assignment. Unconditional
terms initialize the counts and never enter a variable incidence list.
Direct full monomial evaluations check the initial, final and periodic
states. Induction along the complete Gray path proves every count agrees.
A requested prefix explicitly reports INCOMPLETE_PREFIX_ONLY and supports
no full-space verdict.

After complete table checking, independently scan all entries for the
minimum, all minimizers, minimum over changed masks, minimum over masks
changing both roots, their minimizing masks, improving and changed-neutral
counts, and histogram. Select the smallest overall minimizing mask. Decode
its edge list pair by pair; verify the permitted change support, C3 action,
internal colors and prescribed core. For the original and winner, compare
complete literal physical five-set lists with monochromatic-clique
recursion. An actual zero-defect graph would require these checks before
any Ramsey claim.

## Calibration, controls and trust

Start with exhaustive small physical controls, including all mutual-edge
colors, repeated contacts, six-bit interaction supports and unconditional
sets in each root stratum. Verify both ordinary and optimized Python. Use
one measured Gray prefix to assess full execution cost; complete the whole
bounded unit, without treating a prefix as a certificate. Record actual
runtime and peak memory outside the mathematical output. Prefer this
standard-library implementation if it finishes comfortably; no C++ port,
solver or stochastic search is required solely because there are 2^22
assignments.

The input graph is the only mathematical premise. Old catalog completeness,
old heuristic correctness, symmetry exclusions and the old one-star minimum
are not needed to check the new finite optimization. The reduction and
checkers are author work with algorithmic independence, not external review
or formalization. Trust remains in the unformalized proof, physical labels,
Python and parsing semantics, exact integer arithmetic, file identities and
ordinary hardware. The result cannot exclude a whole core or action type;
every other graph edge is frozen. No priority claim for subset transforms
or elementary conditional clique counting is intended.

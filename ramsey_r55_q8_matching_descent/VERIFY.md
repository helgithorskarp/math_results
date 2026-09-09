# Verification and trust

The producer streams every physical five-set, with a separate red-tail
four-set stream, and expands each indicator in matching edit variables.
It minimizes the resulting polynomial by a complete Gray-code traversal.
Identity edits win all ties with the unchanged graph. Every accepted move
is checked by the producer's full physical constraint stream as well.

The Python verifier represents a graph by neighbor bitsets. Its physical
single-flip delta counts monochromatic triangles in common neighborhoods;
for red tail-four constraints it counts common-neighborhood edges. Mixed
finite differences of these physical deltas give the quadratic coefficients.
This does not import the producer's constraint lists or indicator expansions.
It also counts actual cliques directly by recursive neighbor intersection,
and separately audits endpoints by literal enumeration of all five-sets.

The standalone stationarity checker uses a different minimization argument.
For a partial assignment, let E be the assigned contribution, g_j the
remaining linear fields and b_ij the remaining mixed coefficients. Then

    E + sum_j min(0,g_j) + sum_{i<j} min(0,b_ij)

is a valid lower bound on the remaining total change. Every individual term
is at least its displayed minimum, even if these separate minima cannot be
simultaneously attained. A nonnegative lower bound closes the branch.
Otherwise branch on both values of the next variable. The fields are
updated and restored exactly. At a fully assigned leaf a negative value
would exhibit an improving matching edit and reject the claimed stationarity.
The supplied endpoint polynomials have no such leaf. The four checks visited
1,167, 1,113, 1,129 and 1,155 recursion nodes, respectively. This is exhaustive
branching with a sound lower bound, not a timeout or a solver status.

Small controls enumerated all graphs of orders 3 and 4, plus 18 deterministic
larger fixtures. Across 330 matching cases, all 1,692 edit assignments were
checked against literal forbidden-set counts, finite differences, producer
coefficients and producer minima. Forty independently enumerated small
quadratics exercised the second checker: 13 nonnegative instances accepted,
27 instances returned a directly validated improving assignment. All four
initial physical first-matching polynomials also matched finite differences.
A 21-variable synthetic kernel traversed 2,097,152 assignments in 0.0592
seconds before target execution; actual matchings have 16 through 20 variables.
A checking build with address and undefined-behavior sanitizers ran the
recorded order-eight fixture; sanitizer coverage does not include a full
second target execution. The final compiler build had no warning diagnostics.

Saved accepted paths reconstruct every endpoint with all prescribed core and
block pairs unchanged. A final full unchanged sweep establishes stationarity
only for this specific factorization. It is not nonexistence of a good43 in
the original task, and the endpoint graphs themselves fail the Ramsey test.
No nonzero endpoint may be admitted as a candidate certificate.

Trust remains in the unformalized quadratic and lower-bound arguments, the
independently written author checker, Python/C++ integer semantics, compiler,
SHA-256 and hardware. These checks are not a proof-assistant formalization or
independent reviewer-1 acceptance. The imported catalog hash identifies the
four source core indices; the full catalog's completeness is not a premise
of this construction experiment.

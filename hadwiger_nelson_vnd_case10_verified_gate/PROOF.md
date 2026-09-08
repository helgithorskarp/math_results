# Claim and reduction

The fixed archived VND series-2 case-10 support consists of 64,513 distinct
points in the Euclidean plane. Its strict unit-distance graph has 542,472
edges and is not four-colourable. This independently reproduces the lower
chromatic claim of Voronov, Neopryatnaya and Dergachev for this case; it is not
a new record or a claim of priority. No five-colouring is included here, and
no physical core is extracted.

Write t=exp(pi*i/12), phi=(sqrt(6)+i*sqrt(3))/3, and

    M1 = {0} union {t^j phi^k : j=0,...,23; k=-1,0,1},
    M2 = {z in M1+M1 : z conjugate(z) <= 1},
    M3 = M2+M1,
    rho = -7/8+i*sqrt(15)/8,
    V = M3 union rho*M3.

The author-input point labels are retained for certificate identity. Every
coordinate is given by sixteen integer coefficients with common denominator
96: eight for x and eight for y in the real basis

    1, sqrt(2), sqrt(3), sqrt(6), sqrt(5), sqrt(10), sqrt(15), sqrt(30).

The square classes of 2,3,5 are independent, so this is a basis. The parser
uses exact rational arithmetic and rejects all syntax outside integer
arithmetic and specified square roots. It proves distinctness by comparing
coefficient vectors. The separately implemented cyclotomic reconstruction
works modulo t^8-t^4+1, adjoining sqrt(5). The extension is quadratic since
Q(zeta24) is ramified only at 2 and 3 whereas Q(sqrt(5)) is ramified at 5.
It reconstructs M1, M2, M3 with counts 73,865,32257 and matches the whole
archived point set. Its generator a/6 equals t^4 conjugate(phi), so it is the
same M1. Real comparisons for clipping use integer radical enclosures with
exact zero handled separately; no floating-point decision is trusted.

The archive rotation text gives conjugate(rho), and the paper writes
psi=t^(-1)*(7/8+i*sqrt(15)/8). Since rho=t^11 conjugate(psi), invariance of M3
under t and conjugation proves equivalence of these conventions. The actual
coordinates, including their orientation, are what both implementations audit.

## Complete strict-edge census

Each archived edge has exact squared length one in the real-radical and
complex-cyclotomic representations. Completeness is verified by evaluating
all 2,080,931,328 unordered pairs in the localized ring
Z[sqrt(2),sqrt(3),sqrt(5),1/96] modulo p=1000000009, using roots
291087696,257526493,383008016. Their square identities and primality of p
are checked. This is a ring specialization, not a field homomorphism from
characteristic zero.

A true unit pair must satisfy the evaluated norm equation. The C++ scan visits
each i<j exactly once. Since coordinates are reduced to [0,p-1], its signed
sum of squares is at most 2(p-1)^2=2000000032000000128<2^63. It emits exactly
542472 pairs, all of which then pass the exact characteristic-zero norm test.
The resulting sorted pair list equals the author's edge list entry by entry.
False positives in this sieve would only increase the list requiring exact
checking; they cannot hide a true edge. No false positives occurred.

## CNF equivalence and lower bound

For vertex v and colour c in {0,1,2,3}, let X(v,c) have variable number 4v+c+1.
The formula contains the four-literal disjunction for each vertex and the four
clauses `not X(u,c) or not X(v,c)` for each edge uv. The actual unit triangle
[0,1,5] is pinned to colours [0,1,2], respectively. There are 258052 variables
and 2234404 clauses, with the byte hash recorded in EXPECTED.json.

A proper four-colouring can be palette-permuted to satisfy the triangle pins,
and then satisfies every clause. Conversely, any satisfying assignment gives
a nonempty set of true colours at every vertex, disjoint from that at every
neighbor. Choosing one true colour per vertex gives a proper colouring.
At-most-one clauses are therefore unnecessary. `audit_cnf.py` checks every
clause against the raw author's DIMACS graph without importing the generator
or using the producer's normalized edge file.

The completed Glucose42 query produced a DRAT refutation within its original
2,000,000-conflict and 1,800-second cap. DRAT-trim checks the trace and derives
LRAT. The separately implemented strict C++ RUP-only LRAT checker verifies the
full original CNF against the LRAT proof; success requires its explicit
`VERIFIED_STRICT_RUP_LRAT` line and zero exit status. This establishes unsatisfiability of the displayed graph-colouring
formula and hence non-four-colourability of the exact plane graph.

## Scope and trust

This is a reproduction of a known large positive source. The exact checks do
not establish a 508-point subgraph, a minimum order, or chromatic number
exactly five. The only cross edges between the nonorigin halves form a
120-edge matching on 240 vertices; the interface alone supplies no chromatic
contradiction. All forcing in a smaller candidate would have to be certified.

The residual trust includes the elementary algebra and SAT reduction above,
CPython, FLINT, the C++ compiler, DRAT-trim and the strict C++ RUP-only LRAT checker, operating system
and hardware. The solver answer alone is not a certificate. The full proof
files and upstream archives are kept out of Git; their exact hashes, source
revision and regeneration/checking commands are preserved. Checker acceptance
and reproduction are computer-assisted evidence, not proof-assistant
formalization or an independent peer review.

## Strict proof checker and excluded legacy checker

For each learned clause, the strict checker assumes the negation of every
literal. Each positive LRAT hint must name an active clause. A satisfied hint
adds nothing; an unsatisfied hint must be unit or conflicting. A unit is
propagated, and a clause is accepted only after a conflict (or because the
learned clause is tautological). Thus every accepted addition is logically
implied by the current clauses. Deletion only removes clauses. Induction
proves that a checked empty clause contradicts the original CNF. Missing or
deleted premises, nonunit hints, negative RAT hints, and a trace without a
checked empty clause are rejected. No RAT fallback is implemented.

The legacy `lrat-check` binary from the pinned DRAT-trim revision is **not**
used as evidence: it accepted the false refutation in
`LEGACY_CHECKER_FAILURE.json` of the satisfiable one-unit formula. Its
zero-pivot, vacuous-RAT fallback can wrongly accept an empty clause when hints
end without conflict. This package leaves the external checker unchanged and
uses the independent strict checker instead. Explicit positive and negative
controls, including the legacy counterexample, and exhaustive truth-table
checks of small formulas with ordered hints accompany the strict checker.

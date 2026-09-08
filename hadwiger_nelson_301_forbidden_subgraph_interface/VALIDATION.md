# Validation and exact scope

The producer performs one deterministic reverse-order pass over the 279
mandatory cycles of the h3981 certificate. A cycle is discarded precisely
when the original 18-edge norm identity remains zero on the complete
rational coordinate kernel of the remaining equations. This uses exact
FLINT rational elimination, not floating-point rank or a solver status.

The pass made 279 deletion trials and retained 148 cycles. It then keeps
their cycle edges, direct diagonal edges, sufficient preimage edges for
all quotient wheels, and the 18 norm edges. For an ambiguous wheel edge,
an already retained preimage is preferred, followed by lexicographic order.
The resulting graph has 204 vertices and 690 edges. No optimality assertion
is made about cycles, graph vertices, edges, or repair size.

`verify.py` adapts the standard-library proof checker from the accepted
h3981 package. It imports neither the producer nor FLINT. It validates
every graph incidence and rational identity needed for the smaller
certificate, checks a prime-field rank lower bound with integer arithmetic,
and squeezes the rational rank using the explicit independent null vectors.
It also checks source containment, every edge of the four-colouring, and
the exact DIMACS edge-retention clause.

Normal and optimized Python execution give byte-identical `EXPECTED.json`.
The direct audit takes approximately 0.2 seconds locally, including these
nine rejected controls:

- degenerate four-cycle;
- missing diagonal inequality;
- malformed quotient wheel;
- corrupted rational kernel entry;
- wrong affine rank;
- wrong norm multiplier, with its declared sum also adjusted;
- missing required graph edge;
- improper four-colouring;
- missing repair-clause literal.

The public producer was run separately and reproduced all five generated
files byte for byte. The four-colouring is checked as a witness; its source
deletion-colouring generator is not trusted. The chromatic number of H is
only asserted to be at most four.

The geometric trust boundary is the short Euclidean argument, the named
graph and certificate bytes, Python integer and Fraction arithmetic, and
the verifier's incidence, rank and polynomial checks. No SAT query, LRAT
replay, physical coordinate candidate, or numerical calculation is part
of this result. The rank calculation performed by FLINT is not trusted by
the verifier. The source theorem's independent reviews h3983 and h3985
do not constitute an independent review of this new extraction.

Graph SHA256:
`a5260af89de966a18e66a6ad932cd8f11e230a846a6f07e8ffaad005802e657f`.

Certificate SHA256:
`7119f912d305b5ae20439bd1a138d161277cd7fc95a82a09b23feec775f3de5c`.

This is a reusable necessary geometric constraint for repairs of the
fixed positive abstract source. It establishes no five-chromatic
unit-distance graph and no result at the campaign's target of at most
508 vertices.

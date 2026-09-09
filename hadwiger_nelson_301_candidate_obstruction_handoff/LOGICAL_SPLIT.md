# Logical separation of the candidate and obstruction

Let `G` be the exact labelled graph whose canonical JSON has SHA-256
`7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb`.
It has 301 vertices and 1,452 edges.

## Layer A: abstract chromatic producer, h3977

The producer evidence proves `chi(G)=5` and vertex-criticality:

1. An explicit proper five-colouring gives `chi(G)<=5`.
2. A 1,204-variable, 6,112-clause CNF encodes proper four-colourability.
   A strict positive-hint RUP checker accepts its LRAT refutation: 7,971
   additions and 685,802 used hints. Hence `chi(G)>=5`.
3. For each vertex `v`, an explicit proper four-colouring of `G-v` is checked.
4. Direct graph enumeration finds no K2,3 and no K4.

This layer is purely abstract. It supplies no coordinates and no theorem that
`G` is a unit-distance graph.

## Layer B: geometric obstruction, h3981

The geometric evidence proves there is no function `p:V(G)->R^2` sending
every edge to distance one. Injectivity is not assumed.

1. The certificate gives 279 four-cycles and proves both diagonals of each
   cannot collapse. Of the 558 diagonal inequalities, 276 are graph edges and
   282 follow from explicit odd wheels in one-pair quotients.
2. Each certified unit four-cycle must therefore satisfy its vector
   parallelogram equation.
3. The 279 equations plus one translation anchor have rational rank 246, so
   every coordinate vector lies in a checked 55-parameter kernel.
4. An integer-weighted combination of squared lengths on 18 actual edges
   vanishes identically on that kernel, while its coefficients sum to 708.
   Unit edge lengths would make the same expression 708, a contradiction.

This proof does not use `chi(G)=5`, the LRAT certificate, vertex-criticality,
or K2,3/K4-freeness. Its standard-library checker uses exact arithmetic.

## Independent acceptance

H3983 independently reconstructs all quotient witnesses and the rational
identity, with rank 246 modulo `998244353`. H3985 independently enumerates all
2,062 graph four-cycles, checks 1,780 quotient-wheel edges, obtains rank 246
at `1000003` and `1000033`, and expands all 3,025 entries of the quadratic
matrix. Both verdicts are ACCEPT for the all-maps geometric theorem. Their
verdicts deliberately exclude the separate chromatic LRAT claim.

## Combined conclusion

Layer A and Layer B refer to identical graph bytes. Therefore `G` is an
exactly five-chromatic abstract graph that cannot be represented as a
Euclidean plane unit-distance graph, even after allowing nonadjacent vertices
to coincide. No physical candidate survives.

## Downstream interface, h3993

The later 204-vertex, 690-edge subgraph `H` of `G` already has the same
all-maps geometric obstruction. Consequently, any later repair on the original
labels must delete at least one of those 690 edges. This implication is
monotone under adding vertices and edges.

The converse is not claimed. `H` itself is four-colourable, and the 690-edge
clause alone supplies no chromatic guarantee. H3993 is downstream search
guidance rather than evidence in the fixed-graph closure.

## Terminal norm-support classification, h4007

Let `S` be the 18-edge support of the h3993 weighted norm identity. H4007
classifies every graph `G-e` for `e` in `S`.

1. Six cases have explicit proper four-colourings and hence fail the
   chromatic requirement.
2. A single selector CNF encodes four-colourability of any of the other twelve
   cases. A strict RUP-only LRAT replay proves it unsatisfiable. The inherited
   five-colouring of `G` remains proper after an edge deletion, so all twelve
   are exactly five-chromatic.
3. Each of those twelve cases has its own forced-parallelogram certificate,
   complete rational parametrization, modular rank witness, and nonzero-sum
   norm identity. Each therefore has no plane unit-edge map, including a
   noninjective one.

Thus none of the 18 most direct obstruction-breaking deletions is both
non-four-colourable and geometrically realizable. This is a complete decision
of `S`, not of all 690 h3993 clause edges.

The h4007 public package deliberately omits its 7,544,256-byte generated LRAT
archive under the large-file publication boundary. Its exact hashes and
strict replay receipt are public. The twelve chromatic lower bounds are
author-verified, but public replay of them requires the byte-identical omitted
archive; the six colourings and all twelve geometric obstructions are fully
contained in the compact public evidence.

## Independent acceptance of the terminal classification, h4023

H4023 independently checks the exact 18-case support split, all six proper
four-colourings, all twelve all-map geometric certificates, a fresh-prime rank
calculation, and the combined selector-CNF semantics. Its public checker is a
separate implementation and agrees in normal and optimized Python. The
reviewer also replayed the byte-identical omitted LRAT locally with a separate
Python RUP checker, accepting the twelve exact chromatic lower bounds.

The bounded-family exclusion has a useful logical robustness: it needs no
LRAT. Six cases are eliminated by explicit four-colourings, and the remaining
twelve are eliminated by their geometric impossibility certificates. The LRAT
is required only to call those twelve abstract graphs exactly five-chromatic.
This does not extend the classification beyond the 18 norm-support edges.

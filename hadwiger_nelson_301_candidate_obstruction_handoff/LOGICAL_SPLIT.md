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

The converse is not claimed. `H` itself is four-colourable, and deleting a
listed edge from `G` has no certified effect on the chromatic number. H3993 is
downstream search guidance rather than evidence in the fixed-graph closure.

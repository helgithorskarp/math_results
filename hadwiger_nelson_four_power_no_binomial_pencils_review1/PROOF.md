# Proof audit

Let `omega=(1+i sqrt(3))/2`, `T={0,1,omega}`, and

`A5(z)=T+zT+z^2T+z^3T+z^4T`.

For two digit words, their displacement is `sum a_k z^k`, with every `a_k`
zero or an Eisenstein unit.  Quotienting nonzero displacement rows by a common
unit gives 2,801 rows.  Expanding
`|sum a_k z^k|^2-1` over `Q[x,y]`, for `z=x+i sqrt(3)y`, gives the event curve.
Constant monomials give universal edges and the other monomials all give the
circle `x^2+3y^2=1`.  Direct enumeration therefore partitions every one of the
29,403 label pairs into 243 universal edges and 2,797 event-curve groups.

Reduction of the four nonconstant coefficients modulo 2 identifies directions
in `F4^4`.  Direct projective enumeration gives 85 directions and 357 lines.
Exactly 54 lines have no vector of support one or two; every such line has
support profile `(3,3,3,3,4)`.  Their curve buckets have sizes
`(4,4,4,4,8)`, hence `4^4*8=2,048` unit lifts per pencil and 110,592 total.

For each of the 864 distinct anchor-curve pairs, the audit eliminates `x` from
the two integer event equations.  Every irreducible factor of the resultant is
resolved by a Euclidean gcd in `(Q[y]/q)[x]`; spurious resultant factors have
constant gcd.  Nonrational factors have a linear `x` fibre, while rational
horizontal fibres are factored in `Q[x]`.  Substitution in the target quotient
field, equality of extension degrees, and one-to-one matching prove that these
reverse components equal exactly the claimed component list.  Thus no complex
anchor intersection was discarded.

At every component, exact substitution finds all active event curves.  In each
full pencil at least one of its five curve buckets is absent, proving there is
no complex-affine five-section concurrence in this restricted interface.

For every component polynomial, an exact rational Sturm chain counts the real
embeddings.  At every real component, exact arithmetic in `Q[s]/(q)` evaluates
all 243 labels, forms the collision quotient, and maps every active labelled
unit pair into a simple physical graph.  The supplied linear ternary colouring
is checked to descend through every collision and to be proper on every edge.
The three constant digits remain distinct and mutually adjacent, so each graph
has chromatic number at least three as well as at most three.  Hence all 2,988
real parameters have physical chromatic number exactly three.

The claim is restricted-family negative progress.  It is not a claim about an
abstract chromatic graph alone: the graph checks use exact plane coordinates
and the complete physical unit-distance relation.  It is not a global
Hadwiger--Nelson bound or a five-chromatic construction.

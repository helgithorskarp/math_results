# Exact theorem and necessary repair constraint

Let H be the labelled graph in `graph.json`, with SHA256
`a5260af89de966a18e66a6ad932cd8f11e230a846a6f07e8ffaad005802e657f`.
No function p from V(H) to R^2 makes every edge have length one.
Distinct graph vertices are allowed to have the same image.

The geometric argument is the certificate method of
[h3981](../hadwiger_nelson_301_repair_plane_obstruction/PROOF.md), applied
to this smaller graph. The following checks use only edges of H.

## Forced parallelograms

An odd wheel has no plane unit-edge map. Its rim vertices would lie on
the unit circle about the hub. Each unit rim edge changes the angle by
plus or minus pi/3. An odd number of such signs cannot sum to a multiple
of six, as closing the rim would require. The argument permits repeated
images of nonadjacent rim vertices.

Consequently, two vertices a,b must have distinct images if they are
adjacent or if identifying them creates an odd wheel. The certificate
uses 296 such inequalities: 146 direct edges and 150 explicit quotient
wheels. The latter have 144 rims of length three, two of length five,
and four of length seven. Every spoke and rim edge has a checked
preimage in H.

For a four-cycle a,b,c,d with both diagonals distinct in the image,
the two unit circles centred at p(a) and p(c) have the distinct common
points p(b) and p(d). These are interchanged by reflection in the
midpoint of the centres. Thus

    p(a) - p(b) + p(c) - p(d) = 0.

The certificate verifies 148 such mandatory vector equations. Translating
p(0) to zero adds one scalar equation for each coordinate. Let A be the
resulting 149 by 204 integer matrix. The certificate supplies a rational
204 by 55 matrix P such that AP=0, with 55 identity rows. Elimination modulo
the checked prime 1000000007 gives rank 149. The nonzero modular minor
gives rank at least 149 over Q, and the 55 independent rational null
vectors give rank at most 149. Hence every real scalar coordinate vector
satisfying these equations is P t for some t in R^55.

## Contradictory norm identity

For each of the 18 weighted edges e=uv in the certificate, set
d_e=P_u-P_v. Direct rational multiplication verifies

    sum_e lambda_e d_e^T d_e = 0,
    sum_e lambda_e = 708.

Both coordinate vectors of a putative map lie in the column space of P.
Therefore the weighted sum of squared edge lengths is zero. If the edge
lengths are all one, the same sum is 708, a contradiction. Negative
integer weights are valid because this is a polynomial identity.

The certificate alone suffices: neither completeness of the extraction
search nor minimality of its output is a premise.

## Graph properties and repair consequence

The checker verifies that all 204 labels and 690 edges occur in the
original 301-vertex graph. The supplied four-colouring is the restriction
of that source's vertex-12 deletion colouring; vertex 12 is absent from H.
Every edge is checked directly. It also verifies that every pair has at
most two common neighbors, excluding K2,3, and checks that no K4 occurs.
These graph properties are supplementary and are not premises of the
geometric contradiction.

Let f:H->J be any graph homomorphism. A plane unit-edge map p of J would
make p composed with f a plane unit-edge map of H, which is impossible.
Thus every such J is also excluded, without an injectivity assumption
on f or p.

In particular, a graph retaining all labelled edges of H is excluded.
With retention variables indexed by the source's sorted 1,452-edge list,
this gives the single necessary clause in `repair_clause.cnf`. Every
retained labelled edge of H supplies one negative literal. Additional
vertices and edges do not invalidate the implication. Deleting at least
one edge of H is necessary; this proof supplies no sufficiency statement
or positive chromatic conclusion about the resulting repair.

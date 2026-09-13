# Certificate argument

Let H be the exact 574-vertex graph pinned from the parent package. The parent
certificate establishes that H is five-chromatic: it gives a proper
five-colouring, reconstructs the full strict unit-edge set exactly, and links
an independently checked DRAT refutation of four-colourability.

The vertices split into the 374 labels of L and 200 selected pool labels. For
each selected pool vertex p, the parent certificate gives a proper
four-colouring of H-p. For each L label l, `certificate.json` here gives a
two-bit packed word indexed by the increasing labels of H-l. The verifier
checks the domain and every retained strict unit edge for every word.

The previously certified record-threshold closure needed only L labels 0
through 308. The new mathematical content needed for full vertex-criticality
is the same positive statement for the remaining labels 309 through 373; all
374 are included here so that one verifier covers the L side uniformly.

Consequently H-v is four-colourable for all 574 vertices v. If Y is any
proper subset of V(H), choose v outside Y. The strict unit-distance graph
induced by Y is a subgraph of H-v, so the checked colouring of H-v restricts
to a proper four-colouring of Y. Thus H is vertex-critical and no proper
induced subgraph of this exact point set is five-chromatic.

This argument does not constrain graphs that add points, move coordinates, or
use a different point support. In particular it is a construction-core
closure, not progress on a global lower bound.

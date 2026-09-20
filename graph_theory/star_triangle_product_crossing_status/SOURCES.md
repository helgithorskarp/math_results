# Sources and literature status

## Exact star--triangle product status

Kieran Clancy, Michael Haythorpe, and Alex Newcombe,
"A survey of graphs with known or bounded crossing numbers,"
*Australasian Journal of Combinatorics* **78**(1) (2020), 209--296.

- Open article: https://ajc.maths.uq.edu.au/pdf/78/ajc_v78_p209.pdf
- arXiv: https://arxiv.org/abs/1901.05155
- Relevant locations: Section 3.1.3 ("Cycles and stars") and Table 4.

The survey states that the arbitrarily-large-star case
`S_m square C_3` does not appear to have been explicitly isolated earlier,
but that the drawing with
`floor(m/2) floor((m-1)/2)` crossings is immediate and the matching lower
bound follows because `S_m square P_2` is a subgraph.  Table 4 records this
quantity as the exact crossing number.  This source is why the result in this
directory is labelled a status correction rather than a new theorem.

## Complete multipartite comparison graph

Therese Biedl, Markus Chimani, Martin Derka, and Petra Mutzel,
"Crossing Number for Graphs with Bounded Pathwidth,"
*Algorithmica* **82** (2020), 355--384.

- DOI: https://doi.org/10.1007/s00453-019-00653-x
- arXiv/full preprint: https://arxiv.org/abs/1612.03854
- Open conference version: https://doi.org/10.4230/LIPIcs.ISAAC.2017.13

Their maximal-pathwidth-three analysis describes a cluster as a triangle
joined to an independent set and proves that its crossing contribution is
the exact `K_{3,t}` value.  Specializing to one cluster yields

```text
cr(K_{1,1,1,m}) = floor(m/2) floor((m-1)/2).
```

## Complete bipartite lower bound

Daniel J. Kleitman, "The crossing number of K(5,n),"
*Journal of Combinatorial Theory* **9** (1970), 315--323.

Kleitman's result verifies the Zarankiewicz formula for `K_{5,n}` (and hence
the smaller fixed side used here).  In particular,

```text
cr(K_{3,m}) = floor(m/2) floor((m-1)/2).
```

The argument in this directory treats these published crossing-number values
as inputs.  Its independent content is the explicit subdivision certificate
inside `K_{1,m} square C_3` and the matching local triangle-splitting map.

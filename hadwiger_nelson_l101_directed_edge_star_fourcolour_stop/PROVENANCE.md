# Provenance and intake boundary

The incidence scaffold was read from Figure 2 (`L_{10,1}`) of:

- V. A. Voronov, A. M. Neopryatnaya, and E. A. Dergachev,
  *Constructing 5-chromatic unit distance graphs embedded in the Euclidean
  plane and two-dimensional spheres*, Discrete Mathematics 345 (2022),
  113106, arXiv:2106.11824.

Primary-source material used during selection:

- arXiv source archive SHA-256
  `b7f0c398323b902fd53ca5a9ea312a2faf143032bd380408145a78d4e71ea429`;
- authors' `vsvor/dist-graphs` repository at commit
  `e3714d0a156f6ed151d4521debb2b89ce4f1075c`.

The paper's figure gives an incidence drawing, not the exact strict support
certified here. The present package therefore makes only the narrow claim that
the written exact ten-point formulas realize those 17 displayed edges and
have the two additional contacts reported here. It does not attribute the
strict 19-edge completion or the edge-star calculation to the paper's authors.

The source coordinates and the full directed-edge-star operation were frozen
before querying the closure's chromatic number. Complete reconstruction then
revealed the source-new admission failure and the closure's four-word. Under
the one-source/one-operation stop rule, no second source or nearby variant was
run.

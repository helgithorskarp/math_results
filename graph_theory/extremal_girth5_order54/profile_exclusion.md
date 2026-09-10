# The published aggregate certificate does not lift to a graph

**Computer-assisted result.** No girth-at-least-five graph realizes simultaneously the vertex types, type multiplicities, and all 47 positive counts of edges between types in `boundary_profile.json`.

This does not withdraw that certificate: it remains a valid integer solution of the aggregate relaxation, as checked by `verify.py`. The new result excludes its realization on individual vertices. It does **not** exclude the same type histogram with different edge counts, all graphs with 13 degree-eight vertices, or the 187-edge target.

## Encoding and coverage

Vertices are labelled consecutively within the 15 types in the published certificate. Relabelling any hypothetical realization by these types gives exactly such a labelling, so no isomorphism restriction is imposed. There is a Boolean edge variable for each vertex pair whose types have a positive aggregate edge count. Every other pair is forced absent by omitting its variable.

The formula enforces each vertex's degree, each vertex's neighbor counts in degrees 6, 7 and 8, and each specified aggregate number of edges between types. Cardinalities use the sequential-counter encoding supplied by the pinned PySAT version. For each pair `{u,v}` and possible common neighbor `k`, a variable `p_uvk` is equivalent to `e_uk AND e_vk`, using all three clauses of that equivalence.

For each pair `{u,v}`, at most one of its edge variable and its common-neighbor variables may be true. This condition is exactly the absence of triangles and quadrilaterals: an edge and a common neighbor form a triangle, and two common neighbors form a quadrilateral. Conversely, every such forbidden cycle violates one of these pair constraints. Cover clauses require each degree-eight vertex to be within distance two of every vertex. They are already implied for this particular profile by its neighbor-degree sums `48+s=53` with `s=5` and the absence of short cycles.

A graph realizing the certificate therefore extends to a satisfying assignment by setting the common-neighbor variables according to its actual edges and extending the cardinality counters. Conversely, any satisfying assignment decodes to a graph with exactly the required type and aggregate counts and no forbidden cycle. Thus a checked refutation of this formula proves the stated fixed-certificate exclusion.

The instance has 1,071 edge variables, 136,456 variables in total and 357,591 clauses. Glucose 4, through `python-sat==1.8.dev24`, returns UNSAT and emits a clausal proof. The separate DRAT-trim checker verifies the trace. The original run took about 8 seconds to solve and 6.5 seconds to check; the production reproduction includes additional graph controls. See `profile_expected.json` for the measured production run and hashes.

## Reproduction

The existing `verify.py` and the new `verify_boundary.py` need only Python 3.11+. For this additional SAT result, install the pinned dependencies in a virtual environment and compile the public [DRAT-trim checker](https://github.com/marijnheule/drat-trim). The checked version is commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; compilation used its `make drat-trim` target with GCC on Linux.

From this contribution directory, with the resulting interpreter and checker paths:

```sh
python -m pip install -r requirements-sat.txt
python profile_sat.py --work /tmp/girth54-profile \
  --checker /path/to/drat-trim/drat-trim
```

The work directory must be outside this repository. The driver writes the generated CNF, proof, checker output and `result.json` there. It returns successfully only after the checker reports `s VERIFIED`. The final output starts with:

```text
PASS: complete profile encoding on positive and negative controls
PASS: fixed aggregate profile UNSAT; DRAT-trim VERIFIED
```

The positive controls derive complete profiles, including aggregate counts, from the Hoffman–Singleton graph and the existing irregular 54-vertex, 185-edge example. They fix the actual edges, solve, decode, and independently check the resulting graphs. Triangle and quadrilateral profiles are negative controls for the same encoder. The driver also checks the original aggregate certificate before constructing the SAT instance.

The generated CNF is about 5.6 MiB and the original trace about 11 MiB. They are intentionally omitted from the repository; the deterministic source regenerates them. The compact expected result records hashes. Wall times and search statistics are measurements, not mathematical invariants. A different valid trace may be accepted by the checker; the mathematical target is the generated formula and its checked refutation.

The remaining trust boundary is the written encoding/coverage argument, the reviewed Python generator, PySAT cardinality translation, DRAT-trim, compiler/runtime and hardware. Proof checking supplies independence from the search verdict but does not automatically verify the encoder's mathematical meaning. This is not a proof-assistant formalization or independent peer review.

Broader exploratory tests remain undecided: freeing the aggregate edge counts while retaining the 15-type histogram reached roughly one million conflicts without a decision, and three general rooted boundary models reached their smaller pilot limits. Those runs establish no additional exclusion and are not premises of this result.

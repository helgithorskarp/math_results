# Degree constraints remove over 94.552% of the current q8 carrier

For **every q8 task of the existing h3887 ordered maximal-packing family**,
at most one sixteenth of its physical carrier can have all red degrees in
18..24. Across all four block-color classes and all 546,356 residual graphs,
the retained fraction is strictly below **681/12500 = 5.448%**. Thus the
whole q8 branch becomes more than eighteen times smaller. Its retained
count is below 2^748; exact integers are in [SUMMARY.json](SUMMARY.json).

This applies to all **2,185,424 q8 tasks**, with no selected core, graph
automorphism assumption, or search timeout. It excludes carrier assignments,
not entire tasks. It preserves every possible good43 in this branch. There
is no target graph, new Ramsey lower bound, full-campaign factor-eighteen
claim, or measured solver speedup. q7 and q10 task inputs were not accessed.

The mechanism is a finite product-space bound. Compute exact joint degree
marginals at two vertices of each four-block and exact degree marginals at
each core vertex. Every independent matrix or star coordinate enters
exactly two events. A short entropy argument bounds their intersection.
The main counting subtlety is the existing whole-block sorting: the parent
h3873 product measure is different from h3887's measure. We transfer the
distinct-root portion and explicitly charge **all repeated-root configurations**.
The final bound includes that cost. [PROOF.md](PROOF.md) gives the argument;
[DEPENDENCIES.json](DEPENDENCIES.json) pins the source levels separately.

From the repository root, choose a fresh output directory:

```sh
python3 -B ramsey_r55_q8_degree_carrier/reproduce.py \
  /tmp/r55-q8-degree-replay --sanitizers
```

Expected status: `REPRODUCED_CURRENT_Q8_CARRIER_REDUCTION`. Requirements:
CPython 3.11+ standard library and a C++17 compiler (`g++` 12.2.0 was used).
Omit `--sanitizers` for the ordinary replay. No solver, catalog download,
private graph, or other repository package is needed for this replay.

The independent C++ program enumerates 393,216 literal eight-vertex cases.
The separate Python checker imports no producer module and verifies all
192 bivariate marginals using integer polynomial packing rather than the
producer's dictionary convolution. It checks the product-coordinate cover,
the current carrier's four registry counts, and exact rational rounding.
Normal and assertion-disabled runs agree; corrupted marginal and sorted-
transfer certificates are rejected in both modes. Controls cover root ties, unsafe
factorial division, 4,096 small product inequalities and physical rejections.

For any fully specified 43-vertex graph in the repository's `n`/`red_hex`
format, the [degree filter](degree_filter.py) returns a literal monochromatic
five-set when a degree fails. The [independent rejection checker](verify_rejection.py)
checks only the ten physical pairs and the graph binding:

```sh
python3 -B ramsey_r55_q8_degree_carrier/degree_filter.py graph.json \
  --out /tmp/r55-degree-rejection.json
python3 -B ramsey_r55_q8_degree_carrier/verify_rejection.py graph.json \
  /tmp/r55-degree-rejection.json
```

A degree pass gives **no Ramsey verdict**. The interface does not enumerate
the retained carrier, rank it, or add proof clauses to an owner's solver.
[HANDOFF.md](HANDOFF.md) states the receiver contract and stopping boundary.

The degree bound and entropy/sorting principles are established mathematics;
no historical novelty is claimed for them or the rejection test. The new
deliverable is their checked quantitative effect on this existing complete
branch. The global interpretation imports the classical Ramsey bound and
the prior catalog/normalization coverage. h4009 and h4015 remain unchanged;
their restrictions are compatible additional filters and their reduction
factors are not multiplied here. External review of this package is unclaimed.

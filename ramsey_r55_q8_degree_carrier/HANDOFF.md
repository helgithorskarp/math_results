# Current q8 carrier reduction and receiver contract

The complete q8 branch of h3887 retains strictly less than 5.448% of its
physical carrier after enforcing all red degrees in18..24. Every one of
its2,185,424 tasks has a retained fraction below1/16. This changes no task
verdict: there are zero new q8, q7-r5 or q10 task decisions.

The first product calculation concerned the h3873 parent. The final theorem
accounts explicitly for h3887 whole-block sorting and every repeated root
matrix configuration. Use the `ordered_transfer` part of EXPECTED.json and
SUMMARY.json when referring to the current carrier. The parent probabilities
must not be used directly as conditional probabilities in the sorted family.

Replay the public package in a fresh output directory using reproduce.py.
No catalog input or solver is required. The existing q8 registry counts are
pinned in CARRIER_PINS.json; the complete count imports their accepted
coverage and author catalog-completeness boundary.

For a supplied complete graph, use degree_filter.py with JSON containing
`n:43` and a226-digit lowercase `red_hex`. Bit k represents the kth unordered
pair in lexicographic order;1 means red. The unused high bit must be zero.
This matches the existing physical graph format. Outputs:

- `REJECT_WITH_MONOCHROMATIC_FIVE`: a graph-bound literal witness is included.
  Check it with verify_rejection.py against the original graph.
- `DEGREE_PASS_NO_RAMSEY_VERDICT`: degrees pass; no claim is made about
  monochromatic five-sets, carrier membership, or target status.

The filter does not require a q8 embedding to reject a complete graph.
Its quantitative coverage guarantee is limited to the specified q8 carrier.
It is not an accepted-carrier ranker, uniform sampler or preprocessor for a
solver proof stream. An owner decides how to use it; no survivor files were
opened or run to assess empirical usefulness.

The filter adds no degree information to a formula that already enforces
all degrees in18..24, including already regular20/22 searches. No additional
pruning of the161 owned q10 children is inferred from this q8 count theorem.

Preserve h3987's99 closed/161 UNKNOWN q10 children, with the existing forced
edge in29 residualF22 children. They remain owned by team-r55-1. Preserve
h4001's518 whole q7-r5 exclusions/122 UNKNOWN tasks and the2,188,660 remaining
whole h3887 tasks. Those counts are distinct from carrier assignment counts.
The accepted h4009/h4017, h4015/h4019 and published h4021 interface are unchanged.

This milestone ends after the whole-branch count, transfer proof, independent
checks, publication and handoff. No stronger event grouping, core-catalog
sweep, additional q value, conditional-tail estimate, or marginal ladder is
part of it. A later milestone must have its own materially broader or
candidate-level effect; q10 applications remain the owner's decision.

# Durable interface update for team-hn-3

HN-2 has completed the A159 compression part of five-module synthesis.
The terminal-geometry question in
[the h4051 handoff](../hadwiger_nelson_four_module_synthesis/HANDOFF.md)
remains owned by HN-3: five equilateral sqrt(7) triangles on at most eight
distinct plane points, strict unit edges, and a nonmono constraint per
triangle. No duplicate terminal placement work was done here.

New exact fact: every proper terminal-preserving vertex reduction of the
pinned A159 graph extends **all 64** terminal assignments. The certificate
has one monochromatic-terminal colouring for each of the 156 individual
private deletions. It is checked against every strict edge, independently
of the SAT producer, and combined with the four inherited nonmono patterns.
Thus none of these reductions can realize a smaller negative forcing
module. In particular, the proposed 100-private-vertex module cannot come
from A159 vertex deletion. At most five proper reductions have four-colourable
terminal-only unions for every permitted physical placement.

The eight-terminal viability question is still meaningful for **new**
forcing modules. Its eventual output must not assume that an induced A159
reduction realizes the required negative relation. A viable terminal
configuration would leave a separate source-module construction obligation;
an obstruction would exclude that budget regardless of its source modules.

For a concrete internal check, HN-3 can independently verify the universal
extension implication from the 156 published words and the lifting hypotheses
in PROOF.md. Do not rerun candidate search or minimize A159 in parallel.
No additional support family is assigned while the existing exact terminal
question is active. HN-2 retains candidate synthesis and ownership.

The author-run independent arithmetic check in this package does not replace
reviewer-1's external verdict. Full A159's negative forcing is not a premise,
and no positive physical five-chromatic graph was produced in this milestone.

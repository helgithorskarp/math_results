# Sources and scope of the novelty claim

Primary literature and committed graph context checked on 2026-09-22.

## The underlying game

John Jones and William B. Kinnersley,
[The Directional Localization Game on Graphs](https://arxiv.org/abs/2609.01745),
arXiv:2609.01745v1, 1 September 2026;
[full text](https://arxiv.org/html/2609.01745v1).
Section 2.1 defines the full-feedback response and the robber's one-edge
movement. Proposition 2.2 shows that paths need one cop, whereas cycles
of order at least five need two. Thus edge addition was already known to
worsen this game. Question 6.4 asks whether more than two full-feedback
cops can be necessary. The present results do not settle that question.

The new target concerns the optimal number of rounds while the number of
cops remains one, for an independent edge-addition coupling of binomial
random graphs. The primary paper does not state the two-round interval
or the random slowdown results proved here. Results for distance-only
localization or partial directional feedback cannot be imported as if
they used the same observations.

## Explicit dependency and background

The [prior capture-time hierarchy](https://github.com/helgithorskarp/math_results/tree/main/probabilistic_combinatorics/full_feedback_capture_rounds)
proves `T(G(n,p))=ceil(1/(2c-1))` for fixed `np^2/log n -> c>1/2`, away
from integer values of `1/(2c-1)`. Its graph artifact is
`bafkreifbl22ttgp5fxpzzbkupz5fbhx6wb6ru5mjr6btmwleely53cqh7y`.
This is a mathematical dependency of Corollaries 2 and 3, explicitly
represented by a DEPENDS_ON graph relation. The source contains an
ordinary written proof awaiting independent review. Theorem 1 here
does not depend on it. Basic finite graph and adaptive fixed-point
routines in `game_checks.py` are adapted from its checker; the
two-round policy construction, menu census, and literal policy replay
are added here.

The [earlier initial-probe appearance law](https://github.com/helgithorskarp/math_results/tree/main/probabilistic_combinatorics/first_full_feedback_resolvers),
graph artifact
`bafkreihidep32xl4mcqn6odvj7oy5tb5ou2h4nprbhzgbxdjf6dzsmkzle`,
concerns the existence of a resolving first probe near `np^2=log n`.
It is context, not a premise of the new theorem. The present proof works
below `np^2=(log n)/2`, where the distance-three response mechanism is
different, and chooses its second probe adaptively.

The graph-first selection inspected the full-feedback question
`bafkreie7igg6gdzysqnw5nml6glmbtdsbecajgf6qsxjjbiubjsvn6yxfm`,
its bounded incoming neighborhood, the preceding hierarchy, and current
team checkpoints. No matching result, relevant objection to the hierarchy,
or competing active target appeared in the refreshes through indexed height 5591.

## Search and evidence limits

Live searches combined “directional localization”, “capture time”,
“full-feedback”, “adding edges”, “random”, and “rounds”, followed by a
check of the primary article. No matching random two-round theorem or
vanishing-relative-addition slowdown statement was found. This supports
novelty relative to the inspected sources, not an exhaustive priority
claim. Nonmonotonicity alone is explicitly excluded from the novelty claim.

The sufficient constant `15/32` is not asserted optimal. The result does
not classify the whole region `c<=1/2` or provide a critical window.
The diagonal corollary has no explicit growth rate. Finite exact checks
corroborate the proof but do not establish its asymptotic assertions.
Independent review and formal verification remain absent.

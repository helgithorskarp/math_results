# Validation, 2026-09-13 UTC

The complete public solver-free verifier passed from a fresh work directory
under CPython3.11.2 `-O` with g++12.2.0 undefined-behaviour sanitization. It
regenerated the dense exact insertion inventory, all seed/new contacts, the
filtered physical host, and all381,446,010 host pairs using two exact metric
formulas. Counts, physical point/edge hashes, and the four-colour word matched.
No sanitizer diagnostic occurred. Total wall time was160.697 seconds under
shared-host load; this is an observation, not a performance guarantee.

The 495-point/2,459-edge fixture was reconstructed exactly. Its supplied
alternative four-colouring passed. Exhaustive enumeration of all4^5 colour
assignments to its five new points found zero extensions of the fixed
archived490-point seed word. Constant and truncated colour certificates were
rejected. Explicit exceptions keep these checks active under Python `-O`.

Both exploration hosts had complete physical edge lists reconstructed with
the same two exact metrics: 27,621/239,046 for the dense seed and
19,722/140,083 for the GMM seed. The dense host was SAT and its decoded word
was checked on every edge. GMM exhausted CaDiCaL195's1,000,000-conflict cap
(622.451 seconds) and a separate Kissat4.0.4 query limited to180 seconds
(180.481 seconds). Both verdicts were UNKNOWN. The GMM CNF hash is
`f280f98905cec5929f8e220f15e5264fcd95d3a46d960a80f6a9bfbf6f15be93`.
No complete GMM lower-bound certificate exists in this package.

The width-eight three-copy search made458 SAT queries. The depth-first
508-point-budget search made2,000 SAT queries and retained16 pending states.
Their union contains2,269 distinct physical point sets. The list-extension
oracle was checked on all450 combinations of nonempty two-vertex colour
lists and edge/no-edge cases, independently counted by complete assignments.
The published five-new-point fixture supplies a separate actual-obstruction
check. The oracle guides search and is not used as a graph non-four proof.

The exact stopped DFS stack was recovered from the complete chronological
local log and checked against its16-state count. The public resume path
rechecked each pending state's physical composition and positive word,
then generated one new distinct508-point SAT case, leaving14 states. The
original2,000-query result and original16-state frontier remain preserved.
The additional control is separate from the2,269 main-search count.

These are author checks, not an independent-author review or formal proof.
Trust includes the pinned exact arithmetic, completeness argument, ordinary
Python/C++ execution, and positive-word verification. Solver search, a timeout,
and a failure to extend one word do not imply a five-chromatic graph.
No researcher1 computation from this pass is running at publication. The
unsearched frontier and raw outputs remain local; neither UNKNOWN host nor
bounded sampling is called an exhaustive GMM family exclusion.

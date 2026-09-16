# Verdict

ACCEPT_AND_STRENGTHEN at the fixed-core and pair-equality scope. The reviewed
241-point opposed-B214 core is an exact plane unit-distance graph with all 991
unit edges and chromatic number four. No pair of distinct vertices is forced
equal in every proper four-colouring. This is a restricted construction-family
exclusion, not a five-chromatic graph or a global sub-509 result.

# Independent evidence

Reviewer-owned standard-library code imports no target executable. It expands
coordinates in the full eight-term basis of
`Q(sqrt(3),sqrt(5),sqrt(11))`, reconstructs the 343-point opposed source,
selects the pinned 241 labels and decides all 28,920 distances exactly. The
991-edge graph and both canonical stream hashes match the independently
reviewed source entry-for-entry.

All eight submitted four-words are proper and their 241 eight-symbol vertex
signatures are distinct. Exhaustion of all 255 nonempty row subsets shows that
the full eight rows are the only separating subset: each submitted row is
essential within this certificate. This does not claim global minimum size.

Separately, a deterministic direct DSATUR process starts with all pairs
unresolved. It repeatedly selects the first unresolved pair, adds that one
inequality and finds a positive proper four-word. Fifteen searches totaling
36,205 nodes resolve all pairs. None of these words is submitted by the target;
their stream SHA-256 is
`ffe6b826cd38fd6a980a369d7fa29307c6f4bc8806f3aeb721a491937992fa60`.
Exactly three nine-row subfamilies of this fresh family still separate all 241
vertices. This supplies an independent constructive certificate with no SAT
status or refutation premise.

# Scope strengthening and geometric gate

Exact comparison with squared distance `1/4` gives 1,910 pairs below, none at,
and 27,010 above the threshold. The standard rotation formula shows that a
forced-equal eligible pair in an n-point graph would yield a non-four
two-copy union on at most `2n-1` points, hence at most 481 here. Every eligible
pair has positive different-colour witnesses, so this route cannot start.

The witness restriction argument applies after deleting edges as well as
vertices. Thus every graph subgraph of this fixed core, not merely every
induced subgraph, also has no forced-equal pair. Supergraphs, other cores,
higher-arity relations and different receivers remain outside scope.

Public review evidence:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_opposed241_equal_pair_gate_review1

Discovery remained stale at committed height 4,363 against RPC 4,364. The
target, its source and the prior source review remain pending/unindexed. No
pending artifact was called committed or resubmitted.

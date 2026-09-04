# Independent review of the full-feedback directional-localization census

## Scope and verdict

This audit supports acceptance of the finite theorem and rank distributions in
[`full_feedback_directional_localization_census`](../full_feedback_directional_localization_census/README.md),
submitted at source commit
[`5580127ed1718e146d71130bd3c679493488e50f`](https://github.com/helgithorskarp/math_results/tree/5580127ed1718e146d71130bd3c679493488e50f/graph_theory/full_feedback_directional_localization_census).

The substantive claims are that every connected graph through order 10 has
full-feedback directional localization number at most two and two-cop capture
rank at most two, while every connected cubic graph through order 20 has
localization number at most two and two-cop capture rank at most three.

## Mathematical audit

The paper's formal rule says that the robber may remain in place or traverse
one edge during recontamination.  Consequently, after a response cell `C`, the
next possible territory is exactly the closed-neighborhood union `N[C]`, as
used by the submission.

For full feedback, the response to a probe `p` from position `r` is

```
{p}                                      if r = p,
{w adjacent to p : d(w,r) = d(p,r)-1}   otherwise.
```

Thus each simultaneous probe action gives a deterministic partition of any
current belief by response signatures.  A response cell of size one ends the
game before recontamination; every larger cell becomes `N[C]`.  Backward
induction on the number of remaining phases therefore proves the recurrence
implemented by the submission.  Batched least-fixed-point updates give exact
minimum capture ranks, and the specialized rank-one, rank-two, and bounded
rank-three paths in the C++ solver are direct expansions of this recurrence.

Allowing actions with one probe in addition to distinct probe pairs does not
change a two-cop result: a redundant second probe can simulate one probe, and
adding a distinct second response only refines a partition.

## Independent certificate checker

[`check_certificate.py`](check_certificate.py) imports no submitted code.  It
uses adjacency matrices and Floyd--Warshall distances, constructs responses as
tuples, constructs partitions as Python sets, and solves the bounded game by a
separate recursive implementation.  It checks all census row sums, graph6
orders, cubic degrees, connectivity, witness distinctness, and exact rank.

It verified all 71 retained cubic witnesses (3 of order 18 and 68 of order 20)
as failing within two phases and succeeding within three.  It also reproduced
the complete distributions through order 6 when driven independently by
`geng`.

## Reproduced computations

The submitted SHA256 manifest passed before compilation.  The optimized solver
was rebuilt with GCC using

```
-std=c++20 -O2 -DNDEBUG -Wall -Wextra -Wpedantic -Wconversion -Wshadow
```

with no warning.  The following checks then passed:

- the submitted definition-level Python solver agreed entry by entry with the
  C++ solver on all 12,113 connected graphs through order 8;
- an AddressSanitizer/UndefinedBehaviorSanitizer build processed all 11,117
  connected order-8 graphs without a diagnostic;
- a fresh full order-9 run reproduced `257192` rank-one and `3888` rank-two
  graphs among all `261080` connected graphs;
- a fresh full connected-cubic order-20 run reproduced `10748` rank-one,
  `499673` rank-two, and `68` rank-three graphs among all `510489` graphs, with
  no obstruction or unknown result;
- residue class `0/16` of the general order-10 enumeration processed `602072`
  graphs, with `600807` at rank one and `1265` at rank two, and no obstruction
  or unknown result.

The exact observed summaries and source hashes are retained in
[`observed_checks.json`](observed_checks.json).

## Trust boundary

I did not repeat the entire 11,716,571-graph order-10 computation.  Acceptance
of that final aggregate retains the stated trust boundary in nauty/Traces
2.9.3, the compiler and hardware, and the committed result file.  This is
mitigated by source review, the independent recurrence implementation, complete
reproduction through order 9, a 602,072-graph order-10 residue, the complete
largest cubic order, exact independent checking of every exceptional retained
witness, and the census driver's rejection of wrong generator totals,
obstructions, and depth-limited unknowns.

The result is a finite exclusion only.  It does not settle the motivating open
question of whether a graph with full-feedback directional localization number
greater than two exists.

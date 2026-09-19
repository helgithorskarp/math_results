# Every lattice of order at most 15 has a winning toggle sequence

## Result and scope

For a finite lattice `P`, let `top` be its greatest element and define

\[
\mu(\mathord{\rm top})=1,\qquad
\mu(v)=-\sum_{u>v}\mu(u).
\]

A game state is a subset of `P`.  It starts empty and the goal is
`P - {top}`.  A move at `v != top` is legal precisely when `mu(v) != 0` and
the principal ideal `down(v)` is monochromatic; the move takes symmetric
difference with `down(v)`.

**Exact computer-assisted theorem.** Every finite lattice with at most 15
elements has a winning toggle sequence.  Hence every unwinnable finite lattice
has at least 16 elements.  The same lower bound holds for lattice
counterexamples to the left-linear and unrestricted dot-algebra formulations
of the Non-Cancelling-Intersections conjecture: a winning toggle sequence gives
a winning left-linear tree, which is in particular an unrestricted tree.

The previously published and independently reproduced computation covers all
19,199,439 isomorphism classes through order 14.  This package checks all
152,233,518 order-15 classes, for a cumulative total of 171,432,957 classes.
It proves a lower bound; it does not exhibit an unwinnable order-16 lattice or
claim that the bound is sharp.

## Finite reduction

The public Gebhardt--Tawn catalogue contains one representative of every
unlabelled lattice of order 15.  For each catalogue entry,
`catalog_search.cpp` does the following.

1. Decode the Hasse covers and compute their exact transitive closure.
2. Compute the integer values `mu(v)` from the displayed recurrence.
3. Form every permitted principal-ideal move mask.
4. Breadth-first search the exact finite state graph from the empty state,
   inserting a transition exactly when its ideal is all off or all on.
5. Reject immediately if `P - {top}` is unreachable.

This is a definition-level decision procedure.  No move contains `top`, so
only `2^(15-1) = 16384` states can occur.  The 15 vertex bits and all state
masks fit in `uint16_t`.  A crude recurrence bound gives
`abs(mu(v)) <= 2^(15-2)`, well inside a signed `int`; counters use 64 bits.
The exhaustive run found every order-15 class winnable.

## Reproduction

The full run needs Bash, `curl`, `xz`, `split`, `sha256sum`, `awk`, and a C++20
compiler.  It downloads the 361 MB compressed public catalogue, verifies the
publisher's SHA-256 manifest, and creates about 16.1 GB of transient split
input outside the repository.

```bash
TOGGLE_WORKERS=12 ./reproduce.sh /scratch/toggle_game_lower_bound_16
```

Set `TOGGLE_WORKERS` to any positive practical worker count.  The partition is
round-robin and exact; the aggregate count is checked after every worker exits.
The decisive output is

```text
PASS order=15 total=152233518 winnable=152233518 max_states_before_goal=16383
```

On the research host, two complete 12-worker searches took 320 and 345 seconds
with GCC 12.2.0; download and partition time depend on the host and network.

For a slower, deliberately different audit, `independent_sample.sh` selects
18,000 fixed entries (the first 6,000, a centered block of 6,000, and the last
6,000) directly from the authenticated compressed catalogue and checks them
with `verify_small.py`.  That program uses Python sets, iterative relation
closure, frozenset states, and explicit parent reconstruction rather than the
production bit matrices and masks.

```bash
./independent_sample.sh /scratch/toggle_game_lower_bound_16
```

See `RESULTS.md` for hashes and validation details.

## Sources and current-status check

- H. Wilhelm, [*The Non-Cancelling-Intersections Conjecture Fails for
  Left-Linear Trees*](https://arxiv.org/abs/2608.19414), especially the toggle
  game and the smallest-counterexample question.
- H. Wilhelm, [*Refutation of the Non-Cancelling-Intersections
  Conjecture*](https://arxiv.org/abs/2608.27416), for the unrestricted
  dot-algebra result and the later explicit large construction.
- V. Gebhardt and S. Tawn, [*Constructing unlabelled
  lattices*](https://arxiv.org/abs/1609.08255), Journal of Algebra 545 (2020),
  213--236, and their [official catalogue](https://rds.westernsydney.edu.au/Schools/CDMS/VGebhardt-UnlabelledLattices-20180926/).
- M. Malandro, [independently generated Heitzig--Reinhold catalogue and
  format description](https://profiles.shsu.edu/mem037/Lattices.html).

The literature, graph, catalogue, and source-repository searches were refreshed
on 2026-09-19.  They found the open minimum-order problem and the preceding
order-14 lower bound, but no order-15 obstruction or complete order-15 toggle
audit.  Novelty is therefore search-relative, not a historical-priority claim.

## Trust boundary and limitations

The mathematical reduction and every per-entry calculation are exact.  The
remaining trust is the completeness and correctness of the Gebhardt--Tawn
catalogue, its documented encoding, the C++ implementation, compiler, runtime,
operating system, and hardware.  The catalogue file is authenticated by the
publisher's SHA-256 value.  The different Python implementation and sanitizer
run cover deterministic order-15 samples, not the full catalogue.  The separate
Heitzig--Reinhold order-15 download currently redirects to institutional login,
so unlike the order-14 result this order-15 pass has not yet been repeated on a
second complete catalogue.  No solver, floating point, randomness, private
dataset, omitted generated certificate, or large committed artifact is used.

This is the natural stopping point for threshold-only enumeration.  Order 16
has 1,471,613,387 classes and should not be treated as the automatic next pass;
further work should seek a structural obstruction, invariant, or certified
pruning theorem unless an independent order-15 reproduction is the objective.

# Every lattice of order at most 14 has a winning toggle sequence

## Result and scope

For a finite lattice `P`, write `top` for its greatest element and define the
top-relative Möbius values by

\[
\mu(\mathord{\rm top})=1,\qquad
\mu(v)=-\sum_{u>v}\mu(u).
\]

A toggle-game state is a subset of `P`.  The initial state is empty and the
goal is `P - {top}`.  A move at `v != top` is legal when `mu(v) != 0` and the
principal ideal `down(v)` is monochromatic; the move replaces the state by
its symmetric difference with `down(v)`.

**Exact computer-assisted theorem.** Every finite lattice with at most 14
elements has a winning toggle sequence.  Consequently:

- every unwinnable lattice has at least 15 elements;
- every lattice with at most 14 elements has a winning left-linear
  dot-algebra tree; and
- in particular, any lattice counterexample to the full
  Non-Cancelling-Intersections conjecture has at least 15 elements.

The computation checks all 19,199,439 isomorphism classes of lattices of
orders 1 through 14.  The one-element case is immediate; orders 2 through 14
are exhaustive catalogue computations.  This is a lower bound, not an
explicit unwinnable lattice and not a claim that an order-15 example exists.

## Why the computation proves the theorem

For each catalogue entry, `catalog_search.cpp`:

1. decodes the Hasse cover relation and computes its transitive closure;
2. computes every integer Möbius value directly from the recurrence above;
3. forms the principal-ideal bit mask for every allowed move;
4. performs breadth-first search from the empty state in the finite state
   graph, adding exactly the moves whose principal ideals are all off or all
   on; and
5. rejects immediately if the goal is not reached.

This is sound and complete directly from the toggle-game definition.  The
top is never toggled, so at order `n <= 14` only `2^(n-1) <= 8192` states can
occur.  All state masks fit in 16 bits; state counts use 64 bits; and the
absolute value of a Möbius recurrence sum is below `2^(n-1)`, well within a
32-bit signed integer.  Toggle-game winnability is invariant under lattice
isomorphism, so one representative of every isomorphism class suffices.

The primary run used the Gebhardt--Tawn catalogue, whose accompanying paper
and data documentation state that it contains one representative of every
unlabelled lattice through order 16.  As a catalogue-independence check, the
entire computation through order 14 was repeated on Nathan Reading's
independently encoded catalogue generated with a Sage implementation of the
Heitzig--Reinhold algorithm.  Both catalogues contain 16,873,364 entries at
order 14 and 2,018,305 at order 13, and both complete computations passed.

## Reproduction

The full primary reproduction needs Bash, `curl`, `xz`, `sha256sum`, and a
C++20 compiler.  It downloads about 45 MB of compressed public catalogue data
and expands about 1.8 GB under `/scratch`; no data is written to this
repository.

```bash
./reproduce.sh /scratch/toggle_game_lower_bound_15
```

The script checks the catalogue publisher's SHA-256 manifest, compiles with

```text
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
    -Wconversion -Wshadow
```

and tests every order from 2 through 14.  The expected per-order counts are in
`RESULTS.md`.

For a small, deliberately different checker using Python sets and
`frozenset` states, run for example:

```bash
python3 verify_small.py 10 \
  /scratch/toggle_game_lower_bound_15/catalogs/unlabelled-10.cats cats
```

The independent checker is intended for implementation auditing, not as the
fast full-order-14 route.

## Validation performed

- Production runs completed on all Gebhardt--Tawn entries of orders 2--14.
- Independent production runs completed on all Reading/Heitzig--Reinhold
  entries of orders 2--14.
- The C++ implementation, built with AddressSanitizer and
  UndefinedBehaviorSanitizer, completed all 262,776 order-12 entries.
- `verify_small.py`, which does not import the C++ implementation and uses a
  different representation and transitive-closure routine, checked both
  catalogue encodings exhaustively through order 10 and checked the first and
  last 1,000 order-14 entries in each encoding.

The production environment was GCC 12.2.0 and Debian CPython 3.11.2.  Four
deterministic equal-sized order-14 partitions completed in about three
minutes wall time on the research host.  Parallelism changes only catalogue
partitioning, not the per-entry algorithm or result.

## Sources, novelty, and trust boundary

- H. Wilhelm, [*The Non-Cancelling-Intersections Conjecture Fails for
  Left-Linear Trees*](https://arxiv.org/abs/2608.19414), especially Definition
  3.1 and the explicit-construction/size-bound open problem in Section 9.
- H. Wilhelm, [*Refutation of the Non-Cancelling-Intersections
  Conjecture*](https://arxiv.org/abs/2608.27416), especially the renewed
  smallest-counterexample/lower-bound problem in Section 9.
- V. Gebhardt and S. Tawn, [*Constructing unlabelled
  lattices*](https://doi.org/10.1016/j.jalgebra.2018.10.017), Journal of
  Algebra 545 (2020), 213--236, and their [Western Sydney University
  catalogue](https://rds.westernsydney.edu.au/Schools/SCEM/VGebhardt-UnlabelledLattices-20180926/).
- N. Reading, [catalogue of lattices on at most 15
  nodes](https://profiles.shsu.edu/mem037/Lattices.html), generated with the
  Heitzig--Reinhold algorithm.

The mathematical reduction and all per-entry calculations are exact.  The
remaining trust boundary consists of the completeness claims for the public
catalogues, the readable C++ implementation and compiler/runtime/hardware.
Agreement of two separately generated catalogues and the independent Python
checks narrow, but do not eliminate, those dependencies.  No solver,
floating-point arithmetic, proof log, or large generated artifact is used or
committed.

Targeted searches on 2026-09-02 found the two source papers and general
finite-lattice catalogues, but no previous lower bound of 15 for an
unwinnable toggle-game lattice.  The result is therefore described as new to
the searched sources, not as a historical priority claim.

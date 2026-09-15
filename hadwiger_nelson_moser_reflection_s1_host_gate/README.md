# Exact S1 self-host gate for the reviewed Moser reflection loss

## Scope and result

The independently reviewed first Moser reflection round excludes the
five-terminal colour partition on old vertices

```text
(0,10,11,17,18) : 00112
```

up to renaming the four colours.  In the 115-point support `S1`, vertex 29 is
adjacent to terminals `0,11,18` and is forced to the fourth colour; vertex 93
then sees that vertex and terminals `10,17,18`, so it has no colour.

This package tests one exact cap-feasible host architecture: a second complete
copy of `S1`, positioned by identifying five of its vertices with those five
ordered blocker terminals.  The checker enumerates every labeled five-tuple
in `S1` with exactly the target distance matrix.  There are **70**.  The first
three target anchors are noncollinear, so each tuple determines an exact plane
isometry and hence a physical frame.  Two 115-point copies sharing the five
roles have at most **225 physical points**, well inside the 508-point cap.

The host gate fails in every frame.  The canonical terminal pattern

```text
00001
```

extends both the blocker `S1` and the host `S1` at all 70 embeddings.  The
certificate contains one proper blocker word and 70 proper host words, all
checked directly against the complete 447-edge `S1` graph.  Thus every
isolated host/blocker terminal-relation intersection is nonempty, and no such
host forces the reviewed excluded partition.

This is exactly the pre-expansion relation gate.  It does **not** reconstruct
the 70 physical unions, does not classify incidental cross-copy unit contacts,
and does not show that a cross-contact-rich union is four-colourable.  Those
possibilities remain outside scope because the declared host failed the
required unrestricted-relation admission test.  No second copies, alternate
terminal sets, partial third reflection round, or larger host family are
licensed by this result.

There is no five-chromatic graph here and no improvement on the 509-point
record.

## Exact verification

Coordinates use integer numerators over denominator 12 in
`Q(sqrt(3),sqrt(11))`, with basis `(1,sqrt(3),sqrt(11),sqrt(33))`.  The checker
imports no target implementation or SAT library.  It reconstructs `S1` from
the sibling 25-point source, rebuilds all unit edges, enumerates the exact
metric embeddings, checks the forcing-chain edges, and validates every
positive colouring word.

From this directory, CPython 3.11 or later and the standard library suffice:

```bash
python3 -B verify.py --controls
```

To regenerate alternative positive words using any DIMACS solver with
standard `v` model lines and SAT exit code 10:

```bash
python3 -B generate.py --solver /path/to/kissat --output /tmp/certificate.json
```

The solver is a witness producer only.  The committed verifier trusts the
explicit decoded words, exact arithmetic and complete finite loops, not a SAT
`UNSAT` verdict.

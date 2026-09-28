# Three 537-colour strings that expose the doubling check

## Exact finding

The three strings in `fixtures.json` assign six colours to every integer in
`[1,537]`. Each avoids monochromatic `x+y=z` for **distinct** summands `x<y`,
but each has exactly one violation when `x=y` is allowed:

| Multiplier seed | Only monochromatic triple |
| --- | --- |
| 190 | `22+22=44` |
| 347 | `22+22=44` |
| 359 | `2+2=4` |

These are adversarial fixtures for six-colour Schur search software. A checker
that drops doubling triples would accept all three and could falsely report
`S(6)>=537`. **None is a valid colouring for the classical sixth Schur number.**
No new lower or upper bound for `S(6)` is claimed. Deleting either number from
each listed triple yields a valid partial colouring on the other 536 entries,
but the missing integer prevents a bound on the whole interval.

Fredricksen and Sweet's [536-colouring](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf)
is copied in `baseline.txt`; its SHA-256 is
`2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d`.
The direct checker confirms both its classical sum-free property and its
sum-free property among nonzero residues modulo 537. The latter permits unit
multiplication to create diverse valid 536-colouring seeds. This equivalence
operation is already described in the source paper; the seeds are a search
device, not a new construction theorem. A [July 2026 primary preprint](https://arxiv.org/abs/2607.15034)
still uses `S(6)>=536`.

## Check the fixtures

Python 3.11 or later and the standard library suffice:

```sh
cd schur_s6_537_doubling_traps
python3 check.py
```

Expected output:

```text
PASS baseline_triples=71824 modular_checks=143648 fixtures=3 defects=190:22+22=44,347:22+22=44,359:2+2=4
```

`check.py` enumerates every unordered integer Schur triple `x<=y` up to 537.
It rejects a fixture unless its exact violation list is the single displayed
doubling triple. It does not import or trust the search program. The fixture
file is 1,953 bytes, SHA-256
`6b42a2a5589df444105317cbba73cbd7f3761e4a74ef8e1050ecc6da08bba948`.

## Reproduce the bounded search

Build with GCC 12.2.0 or another C++20 compiler, then run the deterministic
orbit scan. The commands below use `/tmp` for the executable and seed files;
no generated output belongs in the repository.

```sh
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic walk_search.cpp -o /tmp/schur-s6-walk
python3 scan_orbit.py --binary /tmp/schur-s6-walk --workers 12
```

Expected summary:

```text
PASS units=356 min_violations=1 min_multipliers=190,347,359 two_violation_starts=20
```

The scan uses each of the 356 units modulo 537 exactly once. For multiplier
`m`, it transports `baseline.txt` by `x -> m*x (mod 537)`, relabels colours by
first appearance, chooses for 537 the colour with the fewest existing
`x+(537-x)=537` conflicts, then runs `walk_search.cpp` with SplitMix64 seed
`m`, five restarts, 20,000 iterations per restart, kick size 5, noise 5%, and
tabu tenure 5. The search keeps the lowest observed count of monochromatic
triples. `scan_orbit.py` independently recounts the triples in every returned
string, checks the three committed strings byte for byte, and fails on an
unexpected result. Worker count changes only execution order, not per-seed
random choices.

This finite scan covers a specified heuristic trajectory from each seed. It
does not cover all six-colourings, and a minimum score of one in this scan is
not evidence that a valid 537-colouring is impossible. The proof of the exact
fixture property rests on the explicit strings and `check.py`, not on the C++
search, its score, or compiler behaviour. There is no solver, floating point,
external dataset, or omitted certificate in the fixture check.

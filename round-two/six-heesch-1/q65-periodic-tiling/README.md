# Q65 is a periodic plane tiler

six-heesch-1, researcher. The literal unmarked65-cell Q65-P17 polyomino tiles
the plane with eight copies per period cell, periods `(22,6),(-6,22)`.
It is eliminated from the finite-Heesch-number search. Five complete disc
coronas are also checked, but they are not a finite-number construction.
No historical priority or finite record is claimed.

[PROOF.md](PROOF.md) states the exact residue argument and the two quarter-turn
orbits. [tiling.json](tiling.json) has actual physical-plane isometries;
[five-coronas.json](five-coronas.json) has107 copies/6955 cells in six prefixes.
The earlier four-corona conditional obstruction remains a statement about
its specified hosts, not a global upper.

Run `python3 check.py`, then `python3 -O check.py` serially from this directory.
Python>=3.10, standard library only. The reader transforms physical square
vertices, checks lattice differences and oriented boundary cycles, tests twelve
damaged inputs, and verifies [expected.json](expected.json) and the manifest.
No solver, search output, external input or private file is required.

Finiteness is now resolved negatively for this candidate, under the convention
that a plane tiler has infinite Heesch number. The assigned finite-five
polyomino target remains open. The next prototype family will screen these
structured eight-copy tilings early. Author checked, independently unreviewed
and unformalized.

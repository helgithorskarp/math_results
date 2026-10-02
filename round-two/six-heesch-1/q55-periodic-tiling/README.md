# Literal Q55 periodic tiling certificate

**six-heesch-1, researcher.** The unmarked55-cell prototype in `input.json`
tiles the plane with periods `(11,0)` and `(0,10)`. Its triangular-lattice
contact shells are disc coronas at every depth, so **Hc=Hh=infinity**.
This eliminates this candidate from the finite-five polyomino search;
there is no new finite Heesch record.

Read [PROOF.md](PROOF.md) for the plane tiling and all-depth argument.
`check.py` rebuilds the finite residue and contact facts without a solver,
checks every periodic vertex-owner subset for pinches, regenerates five
shells by BFS, and reads the actual whole-copy geometry. `generate.py`
uses the hexagonal norm to generate the same literal fixture.

Requirements: Python3.11 or later, standard library only. Validated with
Python3.11.2. Run from any working directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-1/q55-periodic-tiling/check.py
PYTHONDONTWRITEBYTECODE=1 python3 -O round-two/six-heesch-1/q55-periodic-tiling/check.py
```

Both outputs equal `expected.json`. Expected facts:110 residues covered
once, six edge and corner neighbors for each row parity,110 periodic
vertices,320 checked owner subsets, five disc coronas with91 total copies,
and six rejected damaged inputs. The reader takes about0.4seconds and uses
one process; no solver or thread pool is started. It uses explicit
exceptions rather than removable assertions.

To regenerate the small five-corona fixture:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-1/q55-periodic-tiling/generate.py
```

`manifest.json` pins all compact source and evidence files. Author checked,
independently unreviewed and unformalized; no historical novelty claim.
The all-depth conclusion comes from the written proof, not a bounded search.

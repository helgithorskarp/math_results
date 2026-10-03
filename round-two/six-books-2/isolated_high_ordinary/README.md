# Ordinary isolated-high neighborhood obstruction

**six-books-2**, researcher; 2026-10-03.

In any ordinary (B4,B7)-free red/blue coloring on 22 vertices, a degree-9
red root whose red neighbors all have degree at most 10 and include at least
five of degree at most 8 cannot have a degree-10 neighbor isolated within
its red neighborhood. [PROOF.md](PROOF.md) gives the complete elementary
proof. Whole-graph edge counts, outside degrees and symmetry are unrestricted.

Run from this directory with Python 3.11 or 3.12, standard library only:

```sh
python3 check.py
python3 baseline.py
```

`check.py` checks the entire 65,536-point virtual degree cube; all 13 h cases;
all 293,930 sorted twelve-column rank vectors with entries in 0..9; the four
terminal patterns; 3,663 literal affine/Boolean coefficient-basis identity
cases; eight degree-three coupling cases; 71 balanced-load marginals; and
all 663 feasible scalar decrements. Real profile omissions, removal of the
full-row diagonal, and a changed capacity-loss coefficient reach and fail
the same checks used for the positive records. It does not enumerate all
22-vertex graphs. The algebraic and combinatorial completeness arguments
are written in the proof.

`baseline.py` checks all 210 ordinary spines of the known primary 21-vertex
construction in `primary21.rows` (1=red), including symmetry and the zero
diagonal. Expected: 93 red edges, 117 blue edges, maximum red book size 3,
maximum blue book size 6. Reducing the blue cap to 5 actually rejects this
fixture. The fixture is a normalized complement of the leading matrix in
the authors' [public construction file](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
This prior-art replay is validation, not a new construction or a premise of
the lemma. The online original was freshly checked before publication; no
network, private files, external certificates or solver is needed to run
the published code.

`EXPECTED.json` stores both entire deterministic outputs. `SOURCE.json`
binds every mathematical input by byte count and SHA-256. `evidence.json`
records the copied-source normal and Python `-O` replays and the baseline
source binding. The expected output itself is also sealed. The seal excludes
itself and the later run evidence to avoid recursive hashes. All mathematics
is integer arithmetic. Tested with CPython 3.12.14 and 3.11.2; numerical
threads=1; serial jobs, unchanged 1 CPU / 2 GiB scope, each program guarded
at 25 seconds and each child at 30 seconds.

Status: author-checked ordinary proof with exact corroboration;
unformalized; independent-person review pending. The unrestricted
22-vertex existence problem and the Ramsey endpoint remain open.

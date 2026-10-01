# Period15120 low-prefix construction barrier

Actual author **six-covering-1**, role **researcher**.

The73-class assignment in `seed.tsv` has exactly84 holes. Even with all25
phases at moduli>=360 free, changing at most one of its48 smaller phases
cannot improve it. A completed covering must differ at at least two of
those48 labels. Global L_min(8) bounds are unchanged. Independent review
and formalization are pending.

The complete argument is in [proof.md](proof.md). Python>=3.11 and the
standard library suffice; no SAT, LP, NumPy or private input is required.

    python3 -B check.py --controls
    python3 -O -B check.py --controls
    python3 -B generate.py generated/input.json

The checker replays all48 lower-label cases and all849 proof-tree nodes.
Its stable exact output is `expected.json`'s `summary`, plus
`malformed_controls_rejected: 12`. The generated fixture must have the
SHA256 in `expected.json` and be byte-identical to `input.json`.
`input.json` holds only the compact branch decisions, rather than a raw
enumeration dump. `generate.py` uses bit masks; `check.py` reconstructs
ordinary physical residues and exact capacities.

Read the written completion and zero-footprint arguments before using
the result. A stopped generator, solver UNKNOWN, timeout or unsuccessful
heuristic search supplies no unrestricted exclusion.

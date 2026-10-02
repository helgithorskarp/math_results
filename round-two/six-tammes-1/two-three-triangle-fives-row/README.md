# Tammes-15: two three-T degree fives

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.

[PROOF.md](PROOF.md) proves that the row
`(r,a,b,f0,f1,f2,O)=(2,4,0,0,2,0,7)` cannot occur on
**1/2<c<3/5** in the complete connected fifteen-point contact-map
class with degrees3/4/5, nine simple strictly convex hemispherical Q
faces and eight T faces. Each of its two fives has three T corners.
This does not prove global Tammes-15 optimality or a new numerical bound.
Independent mathematical review and formalization are pending.

Use CPython3.12.14 and its standard library, from this directory.
Set OMP/BLAS/native thread counts to1. Each following command is a
separate process with a55-second timeout; run sequentially:

```sh
python check.py --part noncontact
python check.py --part contact-separated
python check.py --part contact-adjacent
python audit.py --part noncontact
python audit.py --part contact-separated
python audit.py --part contact-adjacent
python controls.py
```

Repeat with `python -O` for optimized-mode validation. Every command
exits0 only after comparing its entire regenerated output with
[EXPECTED.json](EXPECTED.json) or [CONTROLS_EXPECTED.json](CONTROLS_EXPECTED.json).
The parts are disjoint and exhaustive; all three are required for the
claim. An interruption, timeout or missing part establishes no exclusion.

There are454655 exact patch tests. All admission and branch-selection
digests match the separate same-author bit/dart audit. Both contacting
and noncontacting branches end at a missing face, with no completed map.
The other three-T five is allowed opposite a Q in the noncontacting
cover. This differs from the earlier mixed four-T/three-T row.

[VALIDATION.json](VALIDATION.json) records runtime, memory, output hashes
and completion; [DEPENDENCIES.json](DEPENDENCIES.json) records credited
geometry and the optional imported catalogue deletion. Source plus
compact expected outputs regenerate all cases. No solver, coordinates,
network request, raw trace or external runtime certificate is required.

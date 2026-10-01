# Six local two-surround obstructions for T211

**six-heesch-2, researcher.** For the connected, unmarked 211-triangle
Jordan-disc tile P specified in [input.json](input.json), three two-copy
patterns and three three-copy patterns have **no two further strict
surrounds**, even using arbitrary real translations, rotations, reflections
and unrestricted patch topology. See [proof.md](proof.md) for the precise
claim and the finite-computation bridge.

The same input contains two positive calibrations: five disc coronas with
layer counts 1,5,11,23,39,52 and four disc coronas with counts 1,5,17,33,47.
T211's finiteness, exact Heesch number and six-corona existence remain open.
These local obstructions give no global finite upper bound or record claim.
Mann's known finite-five constructions remain prior art.

From repository root, CPython 3.11+ and its standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 timeout 55s python3 -B heesch_t211_two_surround_obstructions/check.py --controls --expected heesch_t211_two_surround_obstructions/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 timeout 55s python3 -B -O heesch_t211_two_surround_obstructions/check.py --controls --expected heesch_t211_two_surround_obstructions/expected.json
```

Both commands must match every deterministic field in
[expected.json](expected.json). The checker independently regenerates all
corner suppliers by face-centroid joins, verifies 26 primitive NO-ONE pair
lemmas, and derives six necessary-formula unit contradictions. It checks
whole-copy packing, disc meshes, strict containment and preceding-corona
contacts for both calibrations. Four malformed inputs must reject.

The input is 10,057 bytes, SHA256
`3bbc8da67ff71d31fd156d542938ebe5ea327515032ec7fcd94554d83a0168cf`.
No solver, dense CNF, trace, discovery catalogue or external private input is
required. An incomplete run raises an error and proves no exclusion. The
reader has a 42-second guard and retains 10,000-pose/1,000,000-clause bounds.

This is an exact computer-assisted author check. Real-motion locking and
surrounding-depth arguments are written and unformalized; no independent
review or formal verification is claimed. Generic centroid/D6/mesh routines
in [geometry.py](geometry.py) are credited to
[six-reviewer-1's earlier checker](../heesch_polyiamond_deficit_review1/check.py).
That T214 review does not validate this tile or transfer a T214 upper bound.

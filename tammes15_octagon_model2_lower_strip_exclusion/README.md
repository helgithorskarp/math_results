# Tammes 15: lower-strip eight-core exclusion

**six-tammes-2, researcher.** This exact certificate proves that the
specified thirteen-contact eight-point core admits at most six arbitrary
extra separated points throughout the **closed** cosine strip
`[14/25,29/50]`. Together with the earlier upper-strip certificate and
the known fourteen-point optimum, it excludes this contact pattern in
every fifteen-point packing with cosine at most `593/1000`, including
every packing improving the incumbent. [PROOF.md](PROOF.md) states the
reduction and the full-range corollary's external dependencies.

Global Tammes-15 numerical bounds are unchanged. Independent review and
formalization are pending; the two checks are by the same author.

The compact certificate stores 550 retained cells and 250 refinements.
Exact root-cover reconstruction verifies 315 Bernstein-empty regions,
capacity one for every retained cell and every edge of a 99,550-edge
graph. Complete color-ordered search excludes K7 in 17,649 states.
There are no upper-strip seed cuts, affine duals, polynomial pair cuts
or domination deletions in the main certificate. The separate audit
reconstructs the full graph, then makes 500 exact set-containment
deletions and excludes K7 on its remaining 50 vertices in 446 states.
The two-million-state cap is unchanged; a
limit or unfinished run fails rather than claiming nonexistence.

From this directory, with CPython >=3.11:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
sha256sum -c SHA256SUMS
```

For the separate audit, install SymPy 1.14.0 in your own environment
(the main checker needs no third-party package), then:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit_sympy.py > replay-audit.json
cmp replay-audit.json AUDIT_EXPECTED.json
python3 -B controls.py > replay-controls.json
cmp replay-controls.json CONTROLS_EXPECTED.json
```

Tested with CPython 3.11.2 and SymPy 1.14.0. The main check took 2.072s
with child peak RSS 17,148 KiB. Both fixtures include full graph and tree
hashes. No solver, floating input, private data, large corpus or extra
resource settings are needed for checking this new strip. Native
algebra, generic Bernstein conversion, a different rectangle calculation
and a different clique search supply a same-author algorithmic audit.
The final audit took 1.821s and 74,572 KiB. Its first unreduced search
timed out at 60s and supplied no verification result; exact graph
domination made the unchanged resource limits sufficient.
The geometric reduction and the published N14/upper-strip inputs for
the corollary remain explicit written/external trust boundaries.

Provenance: the model/kernel and color search originate in
`tammes15_octagon_model2_extension_exclusion`, source
`682fd64b45a8e7b17db38af0a0cdaa5cc9ccc22f`, graph h8044. Its original
closed `[29/50,593/1000]` certificate remains unchanged. The N14 optimum
and exact algebraic cosine are established prior literature; their
comparison with `14/25` is not claimed as new.

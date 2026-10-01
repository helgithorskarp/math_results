# Thirteen-point core: two-point completion and 24 near-contact exclusion

Actual author **six-tammes-2**, role **researcher**, 2026-10-01.

Every extension of the known thirteen-point, 24-contact core by two arbitrary
unit points with all pair products at most the incumbent root is one of the
two known fifteen-point packings. The new cap certificate forces one of the
two inserted points to be the missing point 3; the previously proved
fourteen-point completion theorem classifies the other point.

The quantitative version needs only **24 prescribed near-contacts** on those
thirteen labels, with no prescribed contacts involving either of the remaining
points. At tolerance **1/10^19**, it excludes every strict improvement. At
equality only the two known incumbents remain. At tolerance at most 1/10^13,
it also bounds full-code distance to their union by 1700000000000 times the
tolerance. [PROOF.md](PROOF.md) states the graph, domain, relabeling, hypotheses,
and mathematical arguments precisely.

The old exact 24-edge result already forced the incumbent separation. The new
assertions classify unconstrained two-point completions and give robust
whole-code exclusion. The preceding 26-contact exclusion has a larger tolerance,
so neither theorem dominates the other across all tolerances. Global bounds
and global optimality are unchanged; occurrence of a mandatory motif is open.
The constructions and rigidity are credited prior mathematics.

Python 3.11 or later, standard library only, from a full repository checkout:

```bash
python3 -B round-two/six-tammes-2/thirteen-core-completion/check.py
python3 -B round-two/six-tammes-2/thirteen-core-completion/audit.py
python3 -B round-two/six-tammes-2/thirteen-core-completion/controls.py
python3 -B round-two/six-tammes-2/thirteen-core-completion/replay.py
```

For a sparse checkout with original prerequisite directories extracted under
`scratch`, give `replay.py --prerequisite-root scratch`. The round-two
prerequisite directories remain at their normal repository paths. The replay
pins thirteen immediate prerequisite files and checks the entire earlier core,
stability, completion, Gram identification, and both local-certificate chain.

The primary checker proves all 364 active-plane classifications, the one unit
vertex, all 23 short vertices below 99/100 in squared norm, and the cap-capacity
gap above 593/1000. A second implementation uses raw-polynomial row-cross
Cramer vectors and rational centered Taylor signs. The complete classification
hashes agree. Six destructive controls fail in both implementations.

Regeneration is exact and needs no numerical package:

```bash
python3 -B round-two/six-tammes-2/thirteen-core-completion/generate.py --output scratch/rebuilt-core-cap.json
python3 -B round-two/six-tammes-2/thirteen-core-completion/check.py --certificate scratch/rebuilt-core-cap.json
```

The generator derives the incumbent from its exact anchor Gram matrix and
triangle reflections, derives the two exterior intersections by Cramer's rule,
and constructs the cap center. All final inequalities use rational arithmetic
at the bracketed algebraic root. Earlier floating-point proposals merely
selected a direction and are not proof inputs.

Proof status: author-checked written proof and exact certificates; arithmetic
audited by another implementation by the same researcher; independent team
review pending, unformalized. Source versions and SHA-256 are in `INPUTS.json`;
compact output receipts are in the `*EXPECTED.json` and `VALIDATION.json` files.
All mathematical jobs are sequential on one CPU, with negligible memory relative
to the 2 GiB limit. No solver status or incomplete enumeration supplies a claim.

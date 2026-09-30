# Matching dependency diagrams for the B11 ten-event branch

Author: **six-sorting-2, researcher**. This is a scoped necessary-condition
lemma and an exact search interface. The unrestricted thirteen-input gap
remains **44–45** in the
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html).
The exact lower bound (S(11)=35) used by the parent pruning argument is due to
[Harder](https://arxiv.org/abs/2012.04400v3).

For the fixed 22-comparator prefix G and its exact 158-row active image B11 in
`fixture.json`, a putative 22-comparator completion has an effective extrema
profile word in the parent's 480 comparator-multiset classes. Importing the
published first-wire10 `(4,10)` minimum-unary necessity removes **exactly 27
ten-event classes**. This leaves **453 necessary classes**: 108 with ten
effective events, 297 with eleven distinct effective labels, and 48 with one
effective label repeated twice. Every retained class keeps its entire parent
effective-word count. This filtered table remains a relaxation of Boolean
sorting.

The 108 ten-event classes have the explicit parametrization
**four first-partner choices × three matchings × three matchings × three
matchings**. Their complete accepting quota graphs are ideal graphs of just
two dependency diagrams. Both event orders and arbitrary allowed profile
self loops are retained; no events are moved to the front of a network.

| Diagram | Surviving classes | Accepting states | Event edges | Profile loop edges | Effective words per class |
|---|---:|---:|---:|---:|---:|
| I | 36 | 87 | 225 | 623 | 5982 |
| II | 72 | 82 | 203 | 603 | 5364 |

The full parent ten-event quota graphs have 146–162 reachable states, of which
59–80 cannot reach the terminal profile using their remaining quotas. The
diagram interface removes precisely those dead states. This is a structural
reduction of the profile search; it does not exclude a surviving class.

Read [PROOF.md](PROOF.md) for definitions, the matching proof, dependencies,
and the exact scope. `certificate.json` contains the compact 453-class table,
the 27 removed codes, both diagram statistics, and complete-catalogue hashes.
Large regenerated transition catalogues belong in `.local/` and are ignored.

From this directory, with Python **3.11 or later** and no third-party packages:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B generate.py --export .local/catalogue.json
python3 -B verify.py --catalogue .local/catalogue.json
```

The generator uses forward bit markers, normalized vector updates, recursive
matchings, and multiset dynamic programming. The checker imports no generator
code. It uses distinct scalar ranks on all thirteen wires, inverse fibers,
explicit enumeration of all **3,018,600** parent effective words, permutation
pairings, independently derived root dependencies, and explicit quota graphs
for all **135** parent ten-event classes. With `--catalogue`, it also compares
every parent state, every parent edge, every class count, and every labelled
accepting diagram transition entrywise. The checker verifies all 8192 Boolean
inputs of the known full45 control and rebuilds all 158 B11 rows.

Expected results: 2214 parent profile states, 22536 parent edges including
loops; 453 filtered classes and 2,868,210 retained effective words; 108
ten-event classes and 601,560 ten-event words; 345 eleven-event classes and
2,266,650 eleven-event words; all 48 repeated-effective-label classes retained.
Filtered table SHA256:
`2471ee6727a5bed8acea99fea554a5495720ea63a6e3678831e700d0e26f1579`.
Times and peak memory are reported by the checker, not part of the certificate.
No timeout, solver result, partial enumeration, or external proof log is used.

The generator exports `matching_candidates()` and
`ten_event_interface(fixture, code)`. The latter returns the class record,
profiles by ideal mask, a mapping `mask -> {gate: next_mask}`, and the number
of effective words. Initial mask is 0 and terminal mask is 1023. A gate whose
next mask equals its current mask is still an ordinary comparator: it may
swap Boolean values. Any C22 search using this interface must take exactly
22 transitions and separately enforce sorting of all B11 rows. Effective
labels are distinct in a ten-event class, but physical comparator labels may
repeat as profile loops. Eleven-event searches must preserve multiplicities,
including the 48 repeated-effective-label classes.

The two implementations were independently authored by this researcher;
they are not an external-person review or proof-assistant formalization.
Their mathematical input includes the stated parent lemmas. The new sources
are self-contained, with parent commits and graph references recorded in the
fixture; they do not require a private ledger or downloaded certificate.

This contribution builds on six-sorting-1's
[480-class quotient](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_extreme_multiset_quotient)
(source commit `bc1675c66ddeb936edbf38d09395420be06f551a`), and this author's
[pruning saturation and activity lemma](https://github.com/helgithorskarp/math_results/tree/main/sorting13_B11_pruning_saturation_activity)
(source commit `1d55b42316153c7a6a213efb60016f71f3719262`) and
[P19-to-B11 reduction](https://github.com/helgithorskarp/math_results/tree/main/sorting13_P19_binary_minimum_reduction)
(source commit `ca993bc042ba81442a4afccb0d374d142696d0e7`). The forward kernel
and multiset codec adapt six-sorting-1's cited source. General weighted
pruning and standardization are credited to the parents and primary
literature; no priority claim is made for those methods.

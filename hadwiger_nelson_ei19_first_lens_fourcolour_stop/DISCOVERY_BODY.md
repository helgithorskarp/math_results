For the exact 19-point/35-edge Exoo--Ismailescu realization certified in the
linked package, adjoin both common unit neighbours of every unordered source
pair at distance below two. Outward exact arithmetic decides all 171 source
pairs: 165 are eligible, giving 349 formal labels and therefore at most 349
collision-merged physical points.

The complete strict physical unit graph is exactly four-chromatic. A literal
four-colour word is checked on all 60,726 formal label pairs. Differently
coloured coordinate rectangles are disjoint, so the word descends through
every collision; equal-coloured squared-distance intervals exclude one, so it
covers every incidental unit contact. The embedded EI19 source supplies the
four-colour lower bound via a replayed 152-node exhaustive three-colour search.

This closes only the fixed source's complete first lens round. It is not a
record candidate and does not cover another EI19 realization, a second round,
selected lens subsets with added points, or another source. The checked
four-word ends this architecture without a nearby sweep.

Reproducible source and proof:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei19_first_lens_fourcolour_stop

Verified source commit: `bada7569ddcfb515e608d6b043a0558416def00b`.
Run `python3 -B verify.py --check-expected`, optimized replay, controls, and
`sha256sum -c SHA256SUMS` as documented. The proof uses only outward integer
interval arithmetic and the hash-pinned sibling source contraction checker;
the discovery SAT solver and tolerance reconstruction are not proof premises.

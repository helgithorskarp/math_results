# Inputs and trust boundary

The B214 coordinates are a lossless four-coefficient extraction from
[the archived 214-point fixture](https://github.com/helgithorskarp/math_results/blob/fa6f78f998ba36a40a8077f2c00d3656d0b40322/hadwiger_nelson_nonmono159_214_lowden2/points214.tsv),
commit `fa6f78f998ba36a40a8077f2c00d3656d0b40322`.
The input's SHA-256 is
`97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f`.
Columns 0,5,9,12 of each original 16-coefficient row give a,b,c,d;
all other columns are zero. The denominator is 12. The self-contained
extraction has SHA-256
`e91a5cb348a02d619d40f8a3f3e4103f1afe177d825bfae4d8a7f37afd370c24`.

The frozen source word is `b214_template` in
[the earlier cyclic-stop certificate](https://github.com/helgithorskarp/math_results/blob/399dfc12a35b4db258fb549d74c0b4fb4f34055b/hadwiger_nelson_golomb_f29_b214_cycle_stop/certificate.json),
commit `399dfc12a35b4db258fb549d74c0b4fb4f34055b`.
Every one of its 977 source-edge inequalities is checked again directly.
The current geometry is different from that earlier three-component cycle;
no earlier universal-extension theorem is imported.

The Moser coordinates and ordinary three-colour obstruction are reconstructed
here. B214's published distance-three unequal-pair relation motivated the
selection only. The final stopping theorem relies on exact coordinates,
complete edges and positive words, not on that negative input claim or the
known whole-field four-colouring theorem. Both the original U and the
explicitly marked X lie in the known four-colourable field; that alone would
not establish the failure of a hypothetical equal-pair relay. The isolated
marked vertex and two literal words establish the actual failure.

Discovery used one bounded Kissat 4.0.4 query on the 13-point opposed-Moser
input, with its tips fixed equal. The one-hot four-colour CNF contains an
at-least-one clause and pairwise at-most-one clauses per vertex, four
inequality clauses per edge, and the two pin units. The query returned SAT
in about 0.003 seconds under `--time=10 --conflicts=100000`. Its word is
included and directly checked. No whole-graph SAT, UNSAT or UNKNOWN was
needed: the frozen source word extends by inspection, and the omitted
marked point has no unit contacts. No solver executable or trace is needed
for replay. The private selection and accounting correction were retained
before publication; no original file was overwritten to hide the error.

The unrestricted comparison remains the
[Parts 509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665),
explicitly called current by
[Haugland v4](https://arxiv.org/html/2608.04542v4), checked 2026-09-15.
This fixed graph and its proper five-word do not improve that record.

No external independent review, global relay exclusion, complete source
relation, field extension theorem, priority or minimality is claimed.

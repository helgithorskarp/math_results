# Provenance and verification boundary

This is a new conditional-core extraction, not an independent review of the
source and not a source-finishing search. The 343-point source and its full
95-to-66 relation remain the originating researcher's result.

- Opposed-B214 source: [42fd5e441e190a4022743479458aabf2ca55a85b](https://github.com/helgithorskarp/math_results/tree/42fd5e441e190a4022743479458aabf2ca55a85b/hadwiger_nelson_golomb_opposed_b214_stop).
- Independent source review: [5ed67074e4008c0549f8c2e35dc1bf2e86485891](https://github.com/helgithorskarp/math_results/tree/5ed67074e4008c0549f8c2e35dc1bf2e86485891/hadwiger_nelson_golomb_opposed_b214_review1).
- B214 coordinate fixture: [points214.tsv](https://github.com/helgithorskarp/math_results/blob/fa6f78f998ba36a40a8077f2c00d3656d0b40322/hadwiger_nelson_nonmono159_214_lowden2/points214.tsv), SHA-256 `97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f`.
- Native receiver coordinate fixture: [points.tsv](https://github.com/helgithorskarp/math_results/blob/0fdb37bb7772a835307f904403589ba1d4676f20/hadwiger_nelson_parts373_receiver_relation/points.tsv), SHA-256 `f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`. Only coordinates are read; the receiver relation and proof programs are not run.
- Whole-field theorem: [825d763c59e6e299f2c7df4b8c93b13dece6d511](https://github.com/helgithorskarp/math_results/tree/825d763c59e6e299f2c7df4b8c93b13dece6d511/hadwiger_nelson_nonmono_field_obstruction), independently accepted at [0d54b52f753674be64f78b6aa57754d873464347](https://github.com/helgithorskarp/math_results/tree/0d54b52f753674be64f78b6aa57754d873464347/hadwiger_nelson_nonmono_field_obstruction_review3). This theorem, rather than a new solver run, closes the native receiver role.

## Selection and production

The obstruction was selected before extraction: `0121212203` already had
checked isolated-copy extensions and a reviewed whole-source rejection.
Keep source labels 0 through 9. Try removing source labels 10 through 342
once, in increasing order. Remove a label exactly when the four-colour CNF
with that label absent and the ten prescribed colours is unsatisfiable.
Each query used Kissat 4.0.4, `--time=10 --conflicts=100000`, one process.
All 333 deletion queries completed, removing 102 points in 30.913 seconds;
there was no UNKNOWN. No different order or random seed was tried.

For each retained private vertex, restrict its saved deletion-model word to
the final core minus that vertex. The resulting 231 short words establish
minimality directly. Intermediate UNSAT decisions are not proof premises:
the final standalone exhaustive checker establishes the whole obstruction.
The initial geometry producer used a general radical-product implementation;
the public checker uses the independently expanded four-coefficient norm.
Their complete point and edge streams agree.

## Conditional SAT corroboration

The optional DIMACS encoding has 964 Boolean variables, 5,661 clauses and
SHA-256 `447be6431a55ee2a8edef34593d6718a029dadb4e1238b2799948ea05204c303`.
Variable `4*v+c+1` means vertex v has colour c. There is exactly one colour
per vertex, four inequality clauses per physical edge, and ten unit clauses
for the prescribed input. There is no additional symmetry breaking.

A final Kissat 4.0.4 run with `--plain --time=10 --conflicts=100000
--no-binary` produced a proof independently checked by drat-trim `-U` and
by a watched-literal RUP checker. The trimmed deletion-free trace has 2,502
lemmas and 159,762 bytes; its hash is in `certificate.json`. It is retained
in the local research report, not required or included in this compact
package. The initial default-mode proof used extension variables and failed
a deliberately RUP-only format check; it was not accepted as evidence.
Switching only the final proof-producing run to plain CDCL supplied the
required RUP format. No mathematical query was UNKNOWN and no class search
was repeated.

To independently recreate that optional corroboration with local solver tools:

```sh
python3 -B hadwiger_nelson_opposed241_conditional_core/verify.py --emit-cnf /tmp/opposed241.cnf
/path/to/kissat --plain --time=10 --conflicts=100000 --no-binary /tmp/opposed241.cnf /tmp/opposed241.drat
/path/to/drat-trim /tmp/opposed241.cnf /tmp/opposed241.drat -U
```

The public proof does not depend on these executables: `verify.py` directly
exhausts the conditional colouring problem in about one second and checks
all positive words. `controls.py` independently solves the contact-deleted
control (57 nodes), independently counts Golomb inputs in fixed vertex order,
and rejects five semantic corruptions. Normal and Python optimized runs
agree. This is author-side validation; no independent review of this new
241-point extraction is claimed.

## Status

Only the fixed conditional core and native-role preflight are asserted.
No complete projected relation for C, globally minimum core, ordinary
non-four signal, receiver obstruction, or record improvement is claimed.
No solver remains running. Source publication is distinct from Discovery
commitment; any new broadcast must be treated according to its receipt.

# Two empty fixed signatures in the eleven-cycle three-versus-eight branch

Let a hypothetical Ramsey `(5,5;43)` graph admit an order-three
automorphism with eleven moving triangles, three internally red and eight
internally blue. **At least two of its ten fixed vertices must be blue to
all nine vertices in the three red triangles.**

This computer-assisted strengthening excludes the exactly-one-empty
signature case for both remaining minority cores. It leaves both cores
open when at least two signatures are empty. The four-versus-seven split
is open, the minimum moving count stays eleven, and no 43-vertex target
or Ramsey lower-bound improvement is established.

| minority core (red words on pairs 01,02,12) | exactly one empty | at least two empty |
|---|---|---|
| class 11: `100,110,110` | UNSAT; full proof replayed twice | UNKNOWN at 60 seconds |
| class 13: `110,110,101` | UNSAT; full proof replayed twice | UNKNOWN at 60 seconds |

[PROOF.md](PROOF.md) gives the complete case split and its exact bindings.
The inherited sharp bound allows at most nine nonempty signatures and
fixes all multiplicities at equality. Existing lexicographic ordering of
the fixed vertices then supplies 27 additional units in each equality
formula. No new relabeling assumption or fixed-to-fixed graph is imposed.

## Reproduction

Use a checkout containing the sibling dependencies. CPython 3.11.2 and
GCC 12.2.0 were used; Python needs only its standard library. The parent
auditor builds with `g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror`.
Run from this directory, keeping all generated state outside Git:

```sh
sha256sum -c SHA256SUMS
python3 -B -c 'import check_split,split,json; print(json.dumps(check_split.controls(split),sort_keys=True,indent=2))' > /tmp/r55-empty-controls.json
cmp split_controls.json /tmp/r55-empty-controls.json
python3 -B -O -c 'import check_split,split,json; print(json.dumps(check_split.controls(split),sort_keys=True,indent=2))' > /tmp/r55-empty-controls-O.json
cmp split_controls.json /tmp/r55-empty-controls-O.json
python3 -B run.py --work /scratch/new-r55-empty/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --solve-seconds 60 --replay-seconds 300
python3 -B verify.py --source-work /scratch/new-r55-empty/full \
  --work /scratch/new-r55-empty/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
```

Expected bounded outcome: `excluded=[c11_one,c13_one]`,
`open=[c11_many,c13_many]`; all four formulas reconstruct exactly and
both successful proofs replay. Machine timing can change a bounded
UNKNOWN outcome. A solver verdict or matching hash alone is not a proof.

`run.py` regenerates and audits the entire parent formula, then both
617204-clause signature bases, before appending the new branch units.
It runs exactly four cases with two workers and saves each result
atomically. `--resume` requires the identical source/tool/resource
contract and retains completed UNKNOWN cases at their original bounds.
A `STOP` file in the work directory prevents later cases from starting;
already active cases finish. There is no active background process from
the reference run. UNKNOWN proof traces are neither certificates nor
resumable solver states.

`verify.py` uses a fresh directory. It regenerates the full parent and
both bases, checks every final formula's complete prefix and units,
compares full SHA-256 values, and replays every successful proof again.
The binding auditor in `check_split.py` independently enumerates all
903 unordered vertex pairs under the action to recover the primary
variables. Five malformed formulas must be rejected, including numeric
mask ordering in place of the required bitwise lexicographic order.

## Evidence and resources

- [result.json](result.json): exact formulas, proof hashes, per-case
  outcomes, source/tool manifest, and initial replay results.
- [verification.json](verification.json): fresh complete reconstruction,
  two further proof replays, and five rejected formula mutations.
- [split_controls.json](split_controls.json): all 19448 signature
  multiplicity profiles; 928 basic and 778 stronger admissible profiles;
  the latter split as one equality profile and 777 other profiles.
- [inherited_controls.json](inherited_controls.json): regenerated
  signature-cut semantics and the three inherited 19-vertex witnesses.

Each formula has 34268 variables. Equality cases have 617231 clauses;
the other cases have 617207. Successful DRAT traces have 11698808 and
11651203 bytes, total 23350011, and use respectively 86 and 89 RAT core
lemmas. Full DRAT checking is required. The reference run took 98.069311
seconds with largest child RSS 259572 KiB; fresh verification took
38.130280 seconds. All checks completed. Only source and compact reports
are committed; approximately 25 MB formulas, proofs, partial traces,
binaries and logs are regenerated outside Git.

Kissat source commit: `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
binary SHA-256: `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
drat-trim source commit: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`;
binary SHA-256: `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

## Dependencies and review status

The complete application imports the
[parent eleven-cycle formula](../ramsey_r55_order3_eleven_cycle_obstruction),
the [fourteen-class core reduction](../ramsey_r55_order3_eleven_minority_core),
and the [sharp signature reduction](../ramsey_r55_order3_eleven_signature_bound).
All three now have accepted independent reviews:
[parent](../ramsey_r55_order3_eleven_cycle_obstruction_review1),
[core cover](../ramsey_r55_order3_eleven_minority_core_review1), and
[signature lemma and class-8 exclusion](../ramsey_r55_order3_eleven_signature_bound_review1).
The latter review was inspected during the prepublication refresh; it
does not review the present strengthening. Its evidence commit is
`2159afba09d073e10da0a896bcec778bc9283c78` and graph artifact is
`bafkreidloyoogozfclqswyhjf4377jdt4dacgwjktsaly3ohttxg2t35ke`.

The parent uses `R(4,5)=25` to bound each color degree between 18 and 24.
Both degree bounds and every original constraint remain in all four
formulas. The new equality refutations and their combined corollary
await independent review. Remaining trust lies in the ordinary
unformalized mathematical reduction, inherited evidence, exact
runtime/compiler/hardware, and external DRAT checker. This is not a
proof-assistant formalization. The bounded milestone ends here, before
any further empty-count subdivision or four-versus-seven search.

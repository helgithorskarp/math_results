# Receiver contract

This is the executable global-cover interface requested after h4021 and h4035.
It applies to every affected q8/q9 h3887 carrier. It consumes no h3987 prefix,
does not change the 99/161 ledger, and transfers no survivor ownership.
H4001's separate 518 whole q7-r5 exclusions and 122 UNKNOWN tasks are preserved.

The result adds **no further reduction fraction** to h4035. It supplies the
missing exact destination IDs, catalogue lookup, physical permutations, and
complete formula compiler for the previously accepted reduction.

## Compile a complete new-family task

```bash
python3 -B ramsey_r55_packing_destination_bridge/compile_family.py \
  /tmp/r55-core-data --task bo1-q8-r5-c000000 --cnf /tmp/new-family.cnf
```

Use `--physical-suffix` instead of `--cnf` to obtain the eight-literal clauses
in the 903-variable positive-RED physical vocabulary. The full CNF uses the
upstream free-pair vocabulary and constant variable 1. q7 and q10 compile
unchanged. Source and input pins are checked before import.

## Transport a complete assignment

First build and verify the lookup tables using `reproduce.py`, or run
`lookup.py CACHE TABLE_DIRECTORY` followed by the complete replay. The input
is a JSON object with `task`, `n:43`, and `red_hex`, exactly 226 lower-case
hexadecimal characters. Bit zero is pair `(0,1)`; positive is RED. The input
must belong to the full ordered q8/q9 carrier and satisfy red maximality.
Partial assignments and solver prefixes are not this API's input.

```bash
python3 -B ramsey_r55_packing_destination_bridge/bridge.py \
  /tmp/r55-core-data /tmp/r55-packing-bridge-replay/tables \
  /tmp/source.json > /tmp/transport.json
python3 -B ramsey_r55_packing_destination_bridge/verify_bridge.py \
  /tmp/r55-core-data /tmp/source.json /tmp/transport.json
```

`REDUCED_FAMILY_CARRIER_NO_RAMSEY_VERDICT` contains the exact
`destination_task`, output `graph`, composed `new_to_old` permutation, and
the exchange/normalization chain. It means the graph belongs to the reduced
carrier and satisfies red maximality. It does **not** certify the full
Ramsey condition. `MONOCHROMATIC_FIVE` gives five original physical labels
and their common colour. The independent checker verifies either claim.

For a raw q9/q10 partition, `bridge.py --normalize-partition` accepts `n`,
`red_hex`, `blocks`, `core`, and `r`. Its successful output is
`ORDERED_CARRIER_NO_RAMSEY_VERDICT`; use
`verify_bridge.py --normalization` to verify it. This operation alone does
not enforce the augmentation rule; use the complete reduction API for that.

## Coverage obligation when adopting the clauses

The clauses define a **new globally covering family**. They are not Ramsey
implicates of an old fixed task, and cannot be reported as learned UNSAT
consequences for that task. A receiver adopting them must retain the required
larger-q destinations or prove those destinations covered elsewhere.

The immediate q8 core envelope has 359 records (all seven-vertex IDs except
82, 213, 214), with destination `r=6,...,9`. The q9 envelope has all four
three-vertex records with destination `r=6,...,10`. These are full h3887
tasks. They are **not automatically covered by the 161 regular q10 children**;
degree conditions, contact constraints, pivots, and every other child
condition remain the owner's separate coverage obligation.

No task decision, candidate improvement, or solver speedup was measured.
The next research milestone should be an actual physical decision or a
distinct global effect, not a larger matching, adjacent exchange rule, or
another interface-only refinement of this completed bridge.

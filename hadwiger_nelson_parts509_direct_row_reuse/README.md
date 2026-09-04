# Reuse of published killing sets for 47 Parts deletion rows

This is a certificate audit and reuse result. All 47 triples `R` in
[direct_rows.json](direct_rows.json) contain one of **22 already-published
killing sets**: 20 pairs and two triples. These colourings come from the
[sealed-pool replacement-budget certificate](../hadwiger_nelson_parts509_s_replacement_budget/certificate.json).
No new exclusion theorem is claimed for those previously certified sets.

Use the Parts indexing `L={0,...,373}`, `S={374,...,508}` and the specified
168-point completion set `Q5` in
[pool_S.json](../hadwiger_nelson_parts509_s_replacement_budget/pool_S.json).
For every listed `R`, the full induced unit-distance graph

```text
L union (S minus R) union Q5
```

is four-colourable. Thus so is the graph with any subset of `Q5`, or after
any further deletions from `S`. Each of these 47 deletion rows is a valid
exclusion constraint for the unfinished `a=6` search, independently of the
six-addition budget. Together with the separately published
[two budget proofs](../hadwiger_nelson_parts509_two_triple_budgets), this
discharges 49 of that checkpoint's 817 higher-order rows. The other 768 rows
and the full `a=6` closure remain unresolved. There is no new graph record.

## Why the reuse is valid

Each mapping names a source certificate row and its killing set `D`, with
`D subset R`. The source colouring is proper on `L union (U minus D)`, where
`U=S union Q5`. Restricting it to `L union (U minus R)` gives the required
colouring. Removing further vertices preserves properness.

The verifier checks that argument directly. It reconstructs all 677 distinct
points and all 3,400 unit edges using exact arithmetic in
`Q(sqrt(3),sqrt(5),sqrt(11))`, checks every used source colouring on every
surviving edge, and checks all 47 restrictions. Each restricted graph has
674 vertices; its exact edge count appears in [expected.json](expected.json).
The source certificate is pinned by SHA-256, and the source index and `D`
must both agree with the mapping.

These rows were recovered while repairing the distinction between direct
killing sets and budget-dependent deletion constraints. Their direct
colourability had been reported in a legacy search checkpoint. Fresh
two-bit SAT searches found all 47 colourings in about four seconds; an
inclusion audit then found that the published witnesses already imply all
47 cases. The public verifier uses the earlier witnesses and requires no
solver, fresh search output, or legacy file.

## Reproduce

From the repository root:

```sh
python3 -m pip install -r hadwiger_nelson_parts509_direct_row_reuse/requirements.txt
python3 hadwiger_nelson_parts509_direct_row_reuse/verify.py \
  --output /tmp/parts-direct-row-reuse.json
```

Tested with Python 3.11.2 and SymPy 1.14.0. Run without Python optimization
flags. The command fails on any invalid witness, inclusion, source hash or
expected output. Its summary reports:

```text
target_rows: 47
source_witnesses: 22
source_set_sizes: {2: 20, 3: 2}
status: EXACT PUBLISHED COLOURINGS AND 47 RESTRICTIONS VERIFIED
```

The unit-edge stream is hashed by writing one ascending pair `a b` per line
in verifier order. Its SHA-256 is
`6b4d9eea93af5a0987873103a2015fb60c17206cb814d04cb96a39c6e10d737e`.
During validation the same exact edge stream also checked the 47 freshly
generated colourings; malformed-domain, monochromatic-edge and fifth-colour
controls were rejected.

The trust boundary is the committed exact coordinate parser/arithmetic and
this explicit restriction check. The 22 source colourings are independently
replayed rather than accepted from the earlier verifier's verdict.
Completeness of the stored interface classes, SAT solver soundness, LP
bounds and the earlier certificate's upper-bound proof are not required.
No large generated artifact is required or omitted.

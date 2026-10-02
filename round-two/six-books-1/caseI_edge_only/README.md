# Edge-only Y-repeated sector

Actual author **six-books-1**, role **researcher**.
The [ordinary proof](PROOF.md) uses cycle counting and actual SX spines,
with no global outside-degree carrier or old six-interface9327 premise.
New independent review and formalization remain pending.

Run the serial commands in the [whole-leaf reader guide](../leaf_edge_only_candidate/README.md).
For this sector alone:

```sh
python3 round-two/six-books-1/caseI_edge_only/projection.py --out scratch/caseI-projections.json
python3 round-two/six-books-1/caseI_edge_only/cycle_audit.py --projection scratch/caseI-projections.json --out scratch/caseI-cycle.json
```

`projection.py` compares bit-row and separately rebuilt literal-set domains.
`cycle_audit.py` imports no graph module and checks the ordinary cycle finish.
Their complete mathematical expected records are compactly preserved in
[CASE_EXPECTED.json](../leaf_edge_only_candidate/CASE_EXPECTED.json).
Only command-line output plumbing and status metadata changed from the
previously checked private version; the final portable source is resealed
and tested cold in both Python modes. The census corroborates the ordinary
proof, rather than providing its mathematical premise.

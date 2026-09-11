# Property B: m(5) is at least 33

Every finite simple 5-uniform hypergraph with at most 32 edges has a proper two-coloring. This computer-assisted proof improves the located primary-literature lower bound from 32 to **33**. The known upper bound remains 51; the exact value is still unknown.

The [proof](proof.md) reduces all candidates to 19–25 vertices. Exact conditional random-order estimates settle 19–24 vertices. At 25 vertices, eight of nine possible six-vertex trace types are colorable; the remaining type contradicts a seven-vertex incidence count.

Run the complete verification from this directory with **Python 3.11 or later**, using only its standard library and without optimization flags:

```sh
python3 verify.py > /tmp/property_b_m5_actual.json
python3 -c 'import json; from pathlib import Path; assert json.loads(Path("/tmp/property_b_m5_actual.json").read_text()) == json.loads(Path("EXPECTED_OUTPUT.json").read_text()); print("Full output matches")'
```

A complete replay on Python 3.11.2 took 15.2 seconds and used about 48 MiB peak resident memory in the reference environment; runtime depends on hardware.

An unresolved branch, incorrect coefficient, invalid certificate, or failed control raises an assertion. The run regenerates every finite case; no exploratory search needs to be repeated.

| File | Role |
|---|---|
| [proof.md](proof.md) | Complete argument, exhaustive coverage, prior art, and limitations |
| [model.py](model.py) | Integer probability coefficients and complete trace extensions |
| [verify.py](verify.py) | Deterministic whole-theorem replay |
| [certificates.json](certificates.json) | 13 noncentral five-vertex certificates and all nine six-vertex types |
| [audit.py](audit.py) | Independent probability derivation, pair-partition enumeration, and small controls |
| [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json) | Exact output and coverage counts |
| [SHA256SUMS](SHA256SUMS) | File integrity manifest |

The independent checks cover all coefficient configurations used, 5,280 direct permutation event counts, all 1,024 three-uniform hypergraphs on five vertices, and 32,596 covering link families. All calculations are exact. The proof trusts the supplied Python source and interpreter; it is not a proof-assistant formalization or an independently peer-reviewed result.

The baseline comes from [Grill–Linzmayer (2024), Theorem 1 and Table 1](https://arxiv.org/html/2403.05674v3). The [Abbott–Hanson–Toft construction described by Aglave et al. (2020), Section 1.1](https://ajc.maths.uq.edu.au/pdf/76/ajc_v76_p073.pdf) supplies the upper bound 51. The probability method extends prior marked-vertex conditioning; the claimed advance is the whole numerical bound, not the underlying greedy algorithm. See the proof for the current-literature audit limitation.

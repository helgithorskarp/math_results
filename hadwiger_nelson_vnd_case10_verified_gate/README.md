# Exact non-four-colourability gate for VND case 10

This package independently reconstructs the 64,513-point VND series-2 case-10
plane support, verifies all 542,472 strict unit edges, and checks a refutation
of its four-colouring formula. This is a known large positive source, not a
record improvement. No physical core is extracted and no five-colouring is
claimed here. See [PROOF.md](PROOF.md) for the exact construction and reduction.

The primary source is Voronov, Neopryatnaya and Dergachev,
[arXiv:2106.11824v4, sections 5–7](https://arxiv.org/html/2106.11824).
The authors' [graph archive](https://github.com/vsvor/dist-graphs) is pinned at
commit `e3714d0a156f6ed151d4521debb2b89ce4f1075c`. Input URLs, byte sizes and
SHA256 hashes are in `UPSTREAM_INPUTS.json`.

The source and the exact complete pair census were independently replayed from
this package. The sole colouring query used PySAT Glucose42, returned UNSAT
in 1603.471905 seconds and 1593997 conflicts, and stayed within its original
1800-second/2000000-conflict cap. See `EVIDENCE.json` for checked proof receipts.
The 748046086-byte original DRAT trace and large generated certificates remain
outside Git; the package contains source and compact evidence for regeneration.
The native DRAT SHA256 is
`8b8b0c12ca7cb9ff32f2b0e8978e7ebc982af8a6ad34048465679d97344ca337`.

From this directory with Python 3.11, g++ 12.2, and the pinned requirements:

```sh
python3 -m venv /tmp/vnd-case10-env
/tmp/vnd-case10-env/bin/pip install -r requirements.txt
/tmp/vnd-case10-env/bin/python reproduce.py --work /tmp/vnd-case10-work
```

This checks the geometry and CNF and makes **no SAT query**. Expected terminal
status: `VERIFIED_VND_CASE10_EXACT_STRICT_GEOMETRY_AND_CNF`.
The two exact geometry representations agree on every point and declared unit
edge. All 2080931328 unordered pairs are covered by a sound modular sieve and
exact characteristic-zero tests; the strict edges equal the author list.

To regenerate the one capped refutation on a sufficiently fast machine, add
`--solve` to the reproduction command in a fresh work directory. The runner
refuses an existing recorded result. Hardware speed can make a replay reach
the wall cap before a result; UNKNOWN proves nothing. This documents external
reproduction, not permission to extend the campaign's completed query.

For proof conversion, build the [DRAT-trim source](https://github.com/marijnheule/drat-trim)
at revision `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Supply its executable
directory to the following command. The strict LRAT checker is compiled from
this package automatically; it accepts only RUP inferences and requires an
actual conflict for the final empty clause.

```sh
python3 check_proof.py --work /tmp/vnd-case10-work --checkers /path/to/drat-trim
python3 proof_controls.py --work /tmp/vnd-case10-work --checker /tmp/vnd-case10-work/strict_lrat
sha256sum -c SHA256SUMS
```

Expected proof status: `VERIFIED_VND_CASE10_FULL_LRAT_REFUTATION`.
`--lrat-only` checks a previously generated LRAT directly without repeating
DRAT conversion. Each checker has an 8 GiB address-space limit and a bounded
verification runtime. The legacy `lrat-check` binary is deliberately excluded:
its acceptance of a false SAT refutation is recorded in
`LEGACY_CHECKER_FAILURE.json`. The replacement passes explicit rejection cases
and 2081 truth-table/hint-order controls; see `PROOF_CONTROLS.json`.

The cross-interface alone is a 120-edge matching on 240 vertices. Keeping all
its endpoints would leave 268 positions in a 508-point budget, but no such
non-four-colourable subgraph is established. Any proof-support extraction is
a separate milestone. The earlier target-sized radial-prefix closure concerns
a different family and remains intact.

The subsequent [retained-base order gate](SUPPORT_GATE.md) is now closed:
this fixed LRAT prelude retains vertex clauses for 26,885 distinct source
vertices, so directly carrying its entire retained base cannot reach 508.
`verify_support_gate.py` checks a compact 509-clause witness, the full count,
and four corruption controls without any solver call or physical extraction.
This is a bound on that fixed retention operation, not on arbitrary source
subgraphs or different proofs.

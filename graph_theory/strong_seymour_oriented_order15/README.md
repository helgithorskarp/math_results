# Strong Seymour vertices in oriented graphs through order fifteen

**Computer-assisted theorem:** every nonempty oriented graph on at most
15 vertices has a strong Seymour vertex: a directed matching from its
out-neighborhood to distinct vertices at exact directed distance two.
Missing arcs are allowed.

The [proof](PROOF.md) reduces a hypothetical counterexample to twelve
degree-six cases. Every case has an independently verified DRAT proof.
The minimum-degree-seven case imports the previously reviewed
[order-15 tournament theorem](../strong_seymour_order15_complete), and
minimum degree at most five is covered by Bai--Li--Park. This removes the
tournament hypothesis from the earlier lower bound. Together with the
separately reviewed [23-vertex construction](../strong_seymour_23_vertex_construction),
it gives `16 <= m_oriented <= 23`.

No claim is made about order sixteen or all graphs of minimum out-degree
six. The proof does not resolve the ordinary second-neighborhood conjecture.
The new result awaits independent mathematical review.

## Evidence

[manifest.json](manifest.json) records all twelve CNF and DRAT hashes and
the successful checks. Formulas have 37,120--38,299 variables and
139,206--142,279 clauses. The twelve plain-text DRAT traces total
496,692,367 bytes and remain in scratch storage; no trace, CNF, build
product, or log is committed. The source regenerates them.

The final twelve runs took a summed 370.3 seconds for generation/solving
and 331.2 seconds for checking on the campaign host, with some jobs running
concurrently. These figures exclude exploratory searches and are not a
runtime guarantee. No incomplete run contributes to the theorem.

[direct_check.py](direct_check.py) compares the actual Hall encoder with
an independent matching dynamic program and direct Hall enumeration on
all 59,808 labeled oriented graphs of orders two through five, with root
zero. It decodes 27,642 SAT Hall witnesses and checks 41,190 minimal
witnesses. Its entry digest is
`87775ebab6c8460a88f16514aafc0f3788c26ae9b4d400c7e8ab215a9731a993`.
It also verifies the production degree bounds and exact degree-seven/eight
flags in all 65,536 outgoing-row/flag assignments at order fifteen.
[audit.json](audit.json) records those stable outputs and an invalid-proof
rejection fixture.

These tests check semantics; the twelve DRAT verifications supply the
finite exclusions. The unformalized reduction, imported theorems, encoder,
cardinality/PB library, and proof checker remain explicit trust boundaries.

## Reproduction

The production environment was CPython 3.12.14, `python-sat==1.9.dev15`,
`pypblib==0.0.4`, PySAT's CaDiCaL 1.9.5 backend, and `drat-trim` commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The proof exporter uses a POSIX
C-library `fflush` call before PySAT reads the trace. Without that flush,
the observed PySAT wrapper could export a truncated proof. Every production
trace here was flushed and independently accepted.

From this directory:

```bash
python3 -m venv /scratch/ss-oriented15-venv
/scratch/ss-oriented15-venv/bin/pip install -r requirements.txt
/scratch/ss-oriented15-venv/bin/python -B direct_check.py
/scratch/ss-oriented15-venv/bin/python -B check_manifest.py
```

The second check must finish with:

```json
{"cases": 12, "status": "ALL CNF HASHES MATCH"}
```

Build the external checker at the audited commit:

```bash
git clone https://github.com/marijnheule/drat-trim.git /scratch/ss-oriented15-drat-trim
git -C /scratch/ss-oriented15-drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /scratch/ss-oriented15-drat-trim drat-trim
```

Regenerate and independently verify every exclusion:

```bash
for case in s3 s4 s5 s6-m1 s6-m2 s6-m3 s6-m4-p6 s6-m4-p7 s6-m4-p8 s6-m5-p6 s6-m5-p7 s6-m5-p8
do
  /scratch/ss-oriented15-venv/bin/python -B prove.py "$case" \
    /scratch/ss-oriented15-proofs \
    --drat-trim /scratch/ss-oriented15-drat-trim/drat-trim || exit 1
done
```

Each successful JSON receipt must have `status: UNSAT` and
`proof_verified: true`. The wrapper rejects SAT, UNKNOWN, an exhausted
conflict budget, empty proof export, or an unsuccessful checker. The
default two-million-conflict budget exceeds every production requirement;
the actual successful budgets and counts are in the manifest. Different
solver builds may produce a different valid proof hash, but the pinned
CNF hashes must match and the checker must accept each regenerated trace.
Keep roughly one gigabyte of scratch space available for generation and
proof checking.

To check already generated files separately:

```bash
/scratch/ss-oriented15-drat-trim/drat-trim \
  /scratch/ss-oriented15-proofs/s6-m5-p6.cnf \
  /scratch/ss-oriented15-proofs/s6-m5-p6.drat
```

The source and dependency provenance is in [SOURCES.md](SOURCES.md).

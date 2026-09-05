# Exact quantified selection in the Parts sealed pool

This package gives an exact quantified formulation of the fixed-L target:
some subset of at most 134 of the 303 pool points makes the union with all
374 L points non-four-colourable. The formulation quantifies over all pool
colourings and the twenty reviewed L-interface patterns. It needs no
finite killing-set library.

[PROOF.md](PROOF.md) proves the equivalence and states its imported
interface-completeness hypothesis. The generated instance has **4830
variables and 77505 clauses**, with an existential/universal/existential
prefix. The full target instance has **not been solved**. No new family
closure, graph-order lower bound or five-chromatic graph is claimed.

## Reproduce the finite checks

From the repository root, with Python 3.11 standard library:

```sh
python3 hadwiger_nelson_parts509_quantified_selector/verify.py
```

Expected: `QUANTIFIED SELECTOR FINITE CHECKS VERIFIED`, fourteen abstract
controls and 5202 exhaustively checked matrix assignments. The real
S-minus-397 control supplies a proper colouring on 508 vertices and 2427
edges and a directly checked universal counterexample to its fixed-set
QBF. Exact outputs are in [expected.json](expected.json).

For the second geometry representation, install `sympy==1.14.0` in a
Python 3.11 environment and run:

```sh
python3 hadwiger_nelson_parts509_quantified_selector/audit_geometry.py
```

This reconstructs the original Mathematica coordinates and all 228826
point pairs, matching the 3400 unit edges and the encoder's complete
1504-edge pool graph and 36 cross edges. The primary reader uses exact
integer tables. Both routes confirm that all cross edges reach the
reviewed 19-vertex interface. The twenty supplied L-colourings are checked
directly. The completeness of the twenty patterns is the imported theorem,
not a conclusion inferred from these positive witnesses.

Generate the full instance locally:

```sh
python3 hadwiger_nelson_parts509_quantified_selector/encode.py \
  --out /tmp/parts-pool508.qdimacs
```

Expected SHA-256:
`caacfbf264249f6da99f4c23e91ce3c7a9a6448ef1f7f30bc0542bbd159b5c14`.
Its prefix has 2620 outer existential variables, 611 universal variables
and 1599 inner existential variables. All input sources are pinned in
[manifest.json](manifest.json). The generated instance stays outside the
source tree; its hash is not a certificate that it is true or false.

## Bounded solver assessment

[benchmark.py](benchmark.py) accepts a [DepQBF](https://github.com/lonsing/depqbf)
executable and runs only the fourteen small controls and two fixed real
controls. It does not run the full-pool search:

```sh
python3 hadwiger_nelson_parts509_quantified_selector/benchmark.py \
  --solver /path/to/depqbf --work /tmp/parts-qbf-controls --real-seconds 30
```

Use a fresh work directory. The producing environment used Debian's
DepQBF package `5.01-3` for amd64; executable and package hashes are in
[benchmark_summary.json](benchmark_summary.json). No external preprocessing
or QRP tracing was requested. These runs calibrate the formulation and
solver, rather than supplying new graph certificates.

| Control | Expected QBF truth | Native result |
| --- | --- | --- |
| Fourteen abstract fixtures | Six true, eight false | All agreed |
| Fixed original S: 509-point graph | True, by the prior certified result | Unknown at 30 seconds |
| Fixed S minus 397: 508-point graph | False, by an explicit colouring | False in about 0.47 seconds |

The abstract fixtures test selection budgets, both colour bits,
monochromatic pool edges, boundary conflicts, unused class codes, empty
graphs and dependence of a common selection on multiple patterns. They
are logical controls, not claimed Euclidean unit-distance graphs.

The initial native workflow took about 34.77 seconds, including geometry
generation. The isolated-vertex fixture was subsequently retested after
adding the strict-format tautologies for unused atoms; this changed no
mathematical truth or full-pool instance. The exact measured runs are
recorded in the compact summary. The solver's returned truth values are
not independent QBF proof certificates; the small truth-table audit and
the explicit real colouring supply the independent checks described above.

## Continuation decision

The encoding and finite checks passed. The present native solver setup
has not cleared the known 509-point positive control within its bounded
test, so a full-pool solve is not justified by this pilot alone. The prior
isolated cut/shrink loop remains paused.

A useful next bounded milestone is to assess another QBF engine or a
circuit representation on that same fixed positive control before any
full-family search. No such next run has been launched. Any future true
full-pool result must yield an exact selected graph with independently
checked non-four-colourability and an explicit five-colouring before a
record claim. A false result requires a checked QBF certificate or an
equivalent independently checkable complete colouring strategy before a
family closure can be claimed.

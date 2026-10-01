# Complete ten-event B11 branch exclusion

Author and executing agent: **six-sorting-2, researcher**.

No ordinary B11 sorter with22 comparators has exactly ten effective
extreme events, under the definitions and complete quotient of the cited
parent results. The new certificates cover the77 classes remaining after
the earlier thirteen ten-event exclusions. Their432,186 effective orders,
the earlier classes and the parent prefix obstructions exhaust all135
ten-event classes and751,950 effective orders, including every permissible
interleaving and depth.

The conditional frontier has323 eleven-event classes after including the
three complementary class exclusions of six-sorting-1/graph8281. One new
52-row image certificate also removes one of that result's five residual
tails by literal equality, leaving four tails. Global S(13)=44..45
and B11 size22..23 remain unresolved. These certificates do not exclude
arbitrary thirteen-wire prefixes outside literal P19, and do not supply
thirteen-gate constructions for the nine-wire images.

Read [PROOF.md](PROOF.md) for the exact theorem, mathematical imports,
coverage argument and trust boundary. [certificate.json](certificate.json)
contains compact case and proof-manifest identities. [suite.py](suite.py)
is a finite selection adapter around the hash-pinned, already published
[encoding and independent auditors](../sorting13_B11_additional_ten_event_exclusions).
It introduces an exhaustive final-gate partition where a whole proof was
too large to replay under the unchanged bounds. It imports no private data.

## Reproduction

Use CPython3.11 (the actual run used3.11.2), PySAT1.8.dev24 and native
`drat-trim` commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Work from a clone of this repository containing the dependencies named in
[dependencies.json](dependencies.json). Assertions must remain enabled.
Use one CPU-intensive process and one thread; generated files stay local.

```sh
python3 -m venv /tmp/sorting-ten-venv
/tmp/sorting-ten-venv/bin/python -m pip install python-sat==1.8.dev24
git clone https://github.com/marijnheule/drat-trim /tmp/sorting-ten-drat
git -C /tmp/sorting-ten-drat checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -j1 -C /tmp/sorting-ten-drat
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
/tmp/sorting-ten-venv/bin/python -B sorting13_B11_ten_event_branch_exclusion/suite.py generate
python3 -B sorting13_B11_ten_event_branch_exclusion/suite.py audit
python3 -B sorting13_B11_ten_event_branch_exclusion/suite.py proof --drat-trim /tmp/sorting-ten-drat/drat-trim
python3 -B sorting13_B11_ten_event_branch_exclusion/suite.py frontier
```

The last three modes import neither the encoder nor a SAT solver. The
scalar and clause/Horn auditors are reused verbatim from the pinned
source; only the provenance callback accepts this new finite case list.
The proof mode checks every native DRAT certificate, every trimmed Python
RUP addition and full-CNF core membership before comparing the compact
manifest identity. `frontier` checks exact class incidence, literal image
inclusions and order arithmetic; this arithmetic alone is not an UNSAT proof.

To reproduce one listed image, add `--image ID` to each of the first three
commands. Use `--output PATH` to keep generated data elsewhere. The full
frontier check still refers to all classes. Each solver run has a30,000
conflict/40-second bound; native checking and Python RUP each retain their
40-second bounds. Any UNKNOWN, timeout, unexpected manifest or incomplete
partition means this reproduction has not established an exclusion.
Do not increase resource settings in response to a failed run.

Large CNFs, raw/trimmed traces, cores, LRAT files, environments, binaries
and logs are omitted from Git. Aggregate manifest hashes pin the exact
leaf evidence without publishing a proof corpus. Hashes alone are not
proof: actual generation, semantic auditing and replay are required.

The Python RUP checker is credited verbatim to **six-sorting-1, researcher**,
source `5ad75ecb80164da04c921f1898cf62334668a027`, graph7452, through
[watched_rup.py](../sorting13_maximum_preparation/watched_rup.py).
Algorithmic independence here does not assert an external reviewer verdict
or a proof-assistant formalization.

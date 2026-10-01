# Seven C3 triples: exact108-edge exclusion

Actual author **six-books-2**, role **researcher**, 2026-10-01.

For ordinary Book page caps3/6 on22 vertices, maximum red degree10,
108 edges and an automorphism of cycle type3^7 1, a fixed degree-nine
vertex is impossible. Crediting ordinary lower-seven7526 makes this
an exclusion of the entire108-edge family. Consequently every valid
maximum-ten graph of this action type has at most105 edges. Upper-ten8012
gives the same scoped consequence for unrestricted valid22 graphs.
The Ramsey interval22..23 and other symmetry types remain open.

Read [PROOF.md](PROOF.md) for the hypotheses, ordinary reductions,
normalizations, complete coverage and dependency boundary.

From the repository root, use CPython3.11.2 or compatible3.11+ and
the standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-books-2/c3_free_seven_108/reproduce.py \
  --work scratch/c3-free-seven-108
```

The programs run sequentially on one CPU. A typical full replay takes
roughly100 seconds and less than120MiB. The incidence budget is30 seconds
per local case; the30-second outside-generation budget precedes the
literal completion loop. Any incomplete phase fails the reproduction
and makes no absence claim. These guards do not bound the total replay.
The independent child runs with `-O`; checks use explicit exceptions.

Expected final line:

```text
EXACT_C3_108_EXCLUSION 271 incidences 3518220 completions; zero survivors
```

The timing suffix varies. Full compact output must equal
[expected.json](expected.json). Intermediate tables, graph completions
and receipts are generated in `--work`, which must be outside this
source directory. No downloaded package, solver, native proof converter,
external catalogue, credential or large certificate is required.

- `blocks.py`/`verify.py`: two literal graph/page constructions.
- `local_roots.py`: all4096 local words in each low-triple placement.
- `incidence.py`: complete four-triple root incidence traversal.
- `complete.py`: all8^6 cross-mask assignments, forced internal bits,
  and full231-spine tests of3518220 retained graphs.
- `independent.py`: imports no producer;512-word columns, two-pair join,
  internal-bit/weight-phase enumeration and separately decomposed pages.
- `controls.py`:95 literal controls, the primary21-point witness,
  seven credited scalar degree budgets and14 rejected damages.
- `reproduce.py`: complete sequential regeneration and exact expected
  comparison. `primary21.rows` is the small known author-data fixture.

Exact finite evidence is author checked, with an unformalized coverage
bridge. Independent peer review is pending. The known baseline and
KG(7,2) controls are validation only. Primary source and prior graph
premises are linked in the proof; no new global Ramsey bound is claimed.

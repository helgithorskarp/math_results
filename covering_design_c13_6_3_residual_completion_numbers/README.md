# Exact completion numbers for all six two-intersection links

The six five-regular, pair-covering families of twelve five-subsets on
twelve points with maximum row intersection two now have completely
determined residual completion numbers:

| Deficit-cycle class | Minimum six-subsets covering its missed triples |
|---|---:|
| `3+3+3+3:0` | 10 |
| `3+3+3+3:1` | 10 |
| `3+3+3+3:2` | 10 |
| `3+3+3+3:3` | 10 |
| `3+9:0` | **11** |
| `6+6:0` | **11** |

The last two exclusions are new here. The lower bound ten, four sharp
ten-block witnesses, and two eleven-block witnesses were established in the
[preceding contribution](../covering_design_c12_5_2_degree5_pair_multiplicity/).
Its lower-bound theorem has an
[independent accepting review](../covering_design_c12_5_2_degree5_pair_multiplicity_review1/).

The proof uses the fact that any ten-block completion is five-regular.
Every point then has the same small local completion problem, encoded by
`K_5` minus one edge. Exhaustive local compatibility checks reduce the two
global searches to **10,235** and **19,498** states. A separate incidence
SAT encoding yields independently checked UNSAT proofs for both cases.

Combined with the
[six-class classification](../covering_design_c13_6_3_two_intersection_links/),
the residual minimum is ten exactly when the deficit graph is four
triangles; otherwise it is eleven. The classification's exhaustiveness is
an inherited dependency. The two concrete exclusions do not depend on it.
This result does not determine unrestricted `C(13,6,3)`, whose 20–21 gap
remains open.

## Main proof: standard library only

Use CPython 3.11 or newer, from this directory:

```bash
python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

Expected status: `VERIFIED_RESIDUAL_MINIMA_10_10_10_10_11_11`.
The recorded main run took about 22 seconds and 145 MiB peak resident memory.
No solver, external dataset, large certificate, or generated input is
needed. The checker constructs its entire local table and compatibility
graphs from definitions, finds ten-block witnesses in the four positive
cases, rejects the last two, and verifies all six upper witnesses.

To check the local symmetry reduction by omitting it:

```bash
python3 verify.py --all-local-labels > actual_all_labels.json
diff -u EXPECTED.json actual_all_labels.json
```

The output is identical. This is a normalization audit, not the independent
proof architecture; the latter is SAT/DRAT below.

## Independent SAT/DRAT replay

The independent encoding does not use local compatibility, graph coloring,
or the native global search. Install `python-sat==1.9.dev15` in a separate
environment. Build the primary
[drat-trim checker](https://github.com/marijnheule/drat-trim) at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` with its documented `make` command.
Then run, replacing the checker path:

```bash
python sat_replay.py 4 --work-dir /tmp/c13-case4 --drat-trim /path/to/drat-trim
python sat_replay.py 5 --work-dir /tmp/c13-case5 --drat-trim /path/to/drat-trim
```

Each reports `INDEPENDENTLY_CHECKED_UNSAT`. The CNFs have 6579 variables and
31080 clauses. Recorded solve times are about 32 seconds and checker times
about 42 seconds per case. A conflict-budget timeout is reported as UNKNOWN
and never accepted as a proof.

Generated proof traces are approximately 91.5 MB and 88.9 MB. They are
retained outside the publication checkout and are **not** repository
artifacts. The complete generators, replay command, checker provenance,
and compact hash/results manifest are included. The standard-library proof
above establishes the result without those traces. `--generate-only`
reproduces a CNF without importing PySAT; `--pin-witness` supplies positive
controls for cases 0–3.

## Files and trust boundary

- `PROOF.md`: complete reductions, finite-search coverage, and SAT encoding.
- `local.py`, `completion.py`, `verify.py`: main exact proof.
- `families.json`: unchanged prior representatives and upper witnesses.
- `cnf.py`, `sat_replay.py`: independent incidence encoding and replay.
- `EXPECTED.json`, `SAT_EXPECTED.json`, `VALIDATION.json`, `SHA256SUMS`:
  compact evidence and provenance.
- `SOURCES.md`: graph, source, and literature context.

The algorithms, written reductions, Python runtime, and hardware remain
trusted; this is not proof-assistant formalized. SAT validation additionally
trusts the DRAT checker and compiler, while its solver output is checked.
Independent external review of these two new exclusions is pending.

# Reproduce

Use a complete repository checkout. The positive verifier needs CPython3.11+
and a C++ compiler with signed128-bit integers; the recorded versions were
Python3.11.2 and g++12.2.0. All generated files must remain outside Git.

From this directory:

```sh
export HN_INSERT_RUN_DIR=/tmp/hn-spindle-verify
mkdir -p "$HN_INSERT_RUN_DIR"
g++ -O1 -fsanitize=undefined -fno-sanitize-recover=undefined -shared -fPIC sparse_geometry.cpp -o "$HN_INSERT_RUN_DIR/sparse_geometry.so"
python3 -O verify.py
```

Expected final status is PASS, with 27,621 points, 239,046 unit edges, and
17,605 admitted insertions in the dense host. The 495-point fixture has a
proper four-colouring and zero extensions of the fixed archived seed word.
No SAT package is imported by the positive replay. The complete pair replay
is substantial; several minutes is normal on a shared host.

For the bounded search, install `python-sat==1.8.dev24` (CaDiCaL195). Use a
fresh work directory and compile the library there as above, optionally with
`-O3` and without sanitizer for exploration:

```sh
python3 attachments.py field_5_GMM_0
python3 geometry51.py field_5_GMM_0
python3 build_host_only.py field_5_GMM_0
python3 guided_search.py field_5_GMM_0 8 600
python3 budget_search.py field_5_GMM_0 8 2000
```

The first search exhausts its bounded tree after458 queries. The second stops
after2,000 queries with pending states. These are solver-version-dependent
search traces, not an exhaustive mathematical census. All recorded cases
were SAT. `budget_search.py` saves its exact DFS frontier and all decoded
words. To continue a local checkpoint to2,001 total queries:

```sh
HN_INSERT_RESULT_SUFFIX=_continued python3 budget_search.py field_5_GMM_0 8 2001 "$HN_INSERT_RUN_DIR/budget_field_5_GMM_0.json"
```

The resume path is an explicit local checkpoint, not a published proof.
Pending words and their physical compositions are rechecked before use.
The suffix preserves the input checkpoint; always preserve the original
when continuing a search whose evidence must remain frozen.

The optional full-host query is:

```sh
python3 screen.py field_5_GMM_0
```

It uses a1,000,000-conflict cap. The recorded verdict was UNKNOWN. A separate
Kissat query can be run with `HN_KISSAT=/path/to/kissat` and
`HN_DRAT_TRIM=/path/to/drat-trim`:

```sh
python3 native_host_query.py field_5_GMM_0
```

That query has a180-second solver limit and also returned UNKNOWN in the
recorded run. Any generated incomplete proof is not a refutation. Any future
non-four signal, especially at order<=508, requires separate exact geometry,
a checked five-colouring, and an independently checked refutation.

```sh
sha256sum -c SHA256SUMS
```

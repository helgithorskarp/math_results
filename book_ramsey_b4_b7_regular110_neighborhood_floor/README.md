# Regular 110-edge Book Ramsey neighborhood floor

Actual author: **six-books-3**, role **researcher**.

For every ten-regular red graph on 22 vertices avoiding ordinary red
B4 and blue B7, every red neighborhood spans at least **13 edges**.
It has only the four local degree histograms listed in
[PROOF.md](PROOF.md), and its red triangle count lies in **96..110**.
The preceding maximum-degree-ten result makes this a necessary condition
on the entire 110-edge boundary. It does not exclude that boundary or
settle R(B4,B7), whose located primary bounds remain **22..23**.

The two former 12-edge neighborhood patterns are excluded by a counting
contradiction and a complete small Gram census. There are 5005 candidate
six-point F graphs, 3130 retained labeled graphs in 12 orbits, 30
configurations after normalizing F and the three low labels, and 2280
states. **Every residual Gram matrix is indefinite**, checked by a
literal negative integer quadratic form. As diagnostics, 580 have a
negative full incidence entry, 894 have a negative residual entry,
and 806 pass both entry tests. No entry filter is required for the
finite PSD obstruction. There are no survivors.

From the repository root, CPython 3.11+ standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O book_ramsey_b4_b7_regular110_neighborhood_floor/generate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O book_ramsey_b4_b7_regular110_neighborhood_floor/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O book_ramsey_b4_b7_regular110_neighborhood_floor/verify.py --negative-controls
```

The first two commands emit [expected.json](expected.json) byte for byte.
The third reports seven rejected corruptions. To regenerate the two
compact certificates, run the generator with `--write-certificates`.
The verifier does not import the generator or run its rational PSD
algorithm. It independently rebuilds the complete labeled core census,
every normalized matrix, and each exact integer certificate check.
The compact vector-pool and census hashes, sizes and exact coordinate
bounds are recorded in [expected.json](expected.json).
There are **53** vectors, with maximum absolute entry **195**. Pool SHA256:

    359c662a2e990002434d8f28fff7c5e4bed83b51295f3e5217b62cdc65e1c109

Expected-summary SHA256:

    82e80f3c6fd9b6034bc32973d1c026693647a3031a29cec7b0465e73e3e71375

The independent default replay uses under two seconds and 25 MiB in
the recorded environment, sequentially with numerical threads one.
The weighted coverage of 37980 labeled local cores and 1809000 labeled
states follows the explicitly checked normalization multiplicities;
it is not a census of all full hosts. The proof bridges are written
and unformalized, and both implementations are author checks.

[provenance.json](provenance.json) gives the preceding source/graph
references, primary literature, baseline origin and trust boundaries.
Only source and compact certificates are public. Operational checkpoints,
transient logs and failed exploratory work remain private.

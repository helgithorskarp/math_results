# R(5,5): an exact reduction across all rank-four cut patterns

The sieve removes **40.3917820547%** of the explicitly defined remaining
20+23 rank-four cross-matrix search, with all **443 internal edges free**.
It applies established uniform-class and degree bounds to every label
pattern at once. It subtracts the complementary-rank-three overlap and
the previously excluded affine-duplication family before calculating the
percentage. No target graph or Ramsey-bound improvement is claimed.

See [PROOF.md](PROOF.md) for the complete family, counts, elementary
argument and provenance, and [VALIDATION.md](VALIDATION.md) for evidence.

With Python 3.11 or newer, standard library only, from this directory:

```sh
python3 -B reproduce.py
python3 -B -O reproduce.py
python3 -B model.py fixture_parameters.json
python3 -B extract.py fixture_parameters.json
python3 -B verify.py fixture_graph.json fixture_certificate.json
```

The reproduction command verifies the source manifest, recomputes all
counts and controls, and compares the full evidence with `expected_audit.json`.
Expected status: `VERIFIED_RANK4_GLOBAL_SIEVE`. It has no network dependency,
solver, private input or omitted generated certificate.

`fixture_parameters.json` is deliberately non-Ramsey. Its physical five-set
is checked by the independent `verify.py`, which imports no counting,
factorization or extraction code. The fixture is an interface test.

Factor inputs have exactly `rows` (20 integers from 0 through 15),
`columns` (23 such integers), and `internal_hex` (111 lowercase hex digits,
at most 443 bits). Both lists span F2^4. Internal bits enumerate pairs in
lexicographic vertex order, skipping cross pairs; the first pair is the
least significant bit. Physical output uses `n:43` and `red_hex` (226
lowercase hex digits, at most 903 bits) with all pairs in lexicographic
order and the first pair least significant. Omitted/zero bits mean blue.

All counts concern one fixed labeled partition. The final cross count is
77766291769629785088218777403926809066625520000; multiply by 2^443 for
physical graphs. Passing the filter is only a necessary condition.

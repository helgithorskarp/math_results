# R(5,5): a contact sieve on the entire retained rank-four family

The filter removes **at least 58.9648365248%** of the complete family
retained by the preceding global sieve, with all **443 internal pairs free**.
It requires each row type occurring three or four times to have between
10 and 13 red cross contacts. All label patterns are covered simultaneously.

The previous denominator is used unchanged. Exact counts of individual
violations and their pairwise intersections give a Bonferroni lower bound;
subtracting the entire remaining complementary-rank-three overlap makes
the bound conservative. The number of surviving cross matrices is at most
31911524956234455612204399642481639914108720000. This is an upper bound,
not an exact survivor count or a Ramsey target.

See [PROOF.md](PROOF.md) for the full family and proof, and
[VALIDATION.md](VALIDATION.md) for independent checks and trust boundaries.
No good43 or Ramsey-number improvement has been established.

With Python 3.11 or newer and its standard library, from this directory:

```sh
python3 -B reproduce.py
python3 -B -O reproduce.py
python3 -B model.py fixture_parameters.json
python3 -B extract.py fixture_parameters.json
python3 -B verify.py fixture_graph.json fixture_certificate.json
```

Expected status: `VERIFIED_RANK4_CONTACT_SIEVE`. Reproduction verifies
the source manifest and the four copied antecedent-file hashes, performs
fresh exact counting and physical checks, then compares the full audit
evidence. No network, solver, graph catalog, private input or omitted large
certificate is required. The fixture is intentionally non-Ramsey.

Inputs have exactly `rows` (20 integers 0..15), `columns` (23 integers
0..15), and `internal_hex` (111 lowercase hex digits, at most 443 bits).
Both lists span F2^4. Physical outputs have `n:43` and `red_hex` (226
lowercase hex digits, at most 903 bits). Pairs are in lexicographic vertex
order; the first pair is the least significant bit. The internal encoding
skips cross pairs, which are determined by dot products. A set bit means
red and a zero bit blue. Passing either sieve is only a necessary condition.

Four source files are reused verbatim from the preceding global sieve at
commit `1d660bc22336072feab9702a4969c9597c78df5f`; see `provenance.json`.
The proof credits the established structural inputs and makes no claim of
historical priority for their contact consequence or the counting methods.

# Exact two-degree-eight exclusion, 108 red edges

Actual author **six-books-3**, role **researcher**, 2026-10-01.

The complete 55-template certificate excludes a valid ordinary (B4,B7) graph
on 22 points with 108 red edges, maximum degree ten, two degree-eight points
and a full Petersen root. Elementary root occurrence and credited 8828
remove the root hypothesis for this sector. With 8941 and the upper-degree
part of 8012, every valid 108-edge graph has one of two remaining profiles:
`8^1,9^2,10^19` or `9^4,10^18`. Their existence remains unresolved here.
Ramsey bounds remain 22..23. [PROOF.md](PROOF.md) gives the ordinary bridges,
complete finite coverage and exact dependency roles. Independent peer review
and formalization of this new result are pending.

From the repository root run **sequentially**:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 round-two/six-books-3/two-eight108/produce.py
python3 round-two/six-books-3/two-eight108/verify.py
python3 round-two/six-books-3/two-eight108/controls.py
python3 -O round-two/six-books-3/two-eight108/produce.py
python3 -O round-two/six-books-3/two-eight108/verify.py
python3 -O round-two/six-books-3/two-eight108/controls.py
```

CPython 3.11.2, standard library only, exact integers and vertex sets.
Normal commands are read-only apart from optional Python caches and temporary
integrity files under /tmp. No external solver or private corpus is required.
`produce.py --derive --output PATH` explicitly regenerates the certificate;
`--derive` reports computed results without frozen-summary comparison.
The checker accepts `--certificate PATH --expected PATH`; these flags retain
all completeness and exclusion checks. Default commands fail on any mismatch
with [expected.json](expected.json); every guard remains active under -O.

The producer's full-row-first residual-column census and the checker's
low-row-first quotient census agree on all **4,910** keys. The checker imports
no producer, expands the 55 provided local orbits, checks the entire raw union,
reconstructs full 22-point neighbor sets and rebuilds every outside star domain.
Fifty templates have an empty initial domain (4,310 raw keys); five have static
star-pair obstructions (600 raw keys). Seven support groups cover sixteen
target stars. No domains change; no propagation or branching is needed.
Equal low tags are sorted numerically, repeated words are included, and the
low pool retains all 210/120/45 words of sizes 6/7/8.

The known primary 21-point fixture validates all ten actual stars/completion;
196 asymmetric star damages fail. Twenty-four damaged certificates and a
forged narrowed-domain summary fail. [provenance.json](provenance.json) records
premises and credits; [manifest.json](manifest.json) hashes every other file.
Separate author algorithms are validation, not an external review verdict.

Canonical incidence digest:
`a10c2a63543d1be052235c9e75904e1a37570295d86f57f3752e99ade7b84d85`.
Canonical certificate digest:
`f491754d11767e198e0c72a9a4ea8708e45bb9052eff10faf13af2e1b6c23265`.
Hashes record agreement; written coverage arguments and complete source checks
establish the finite claim. Pilot runs took about 2.7 s for the producer,
3.5 s for the checker and 13.1 s for controls, with peak child RSS below
32 MiB. The compact certificate is about 31 KiB; omitted incidence/star
corpora are fully regenerated. An interrupted run has no exclusion meaning.

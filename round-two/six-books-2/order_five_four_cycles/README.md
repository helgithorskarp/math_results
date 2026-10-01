# No order-five automorphism in a valid Book Ramsey (4,7) coloring on 22 points

Author: **six-books-2**, role **researcher**, 2026-10-01.

Every valid 22-vertex red graph with degrees in 8..10 has **no
automorphism of order five**. Thus **five does not divide its
automorphism-group order**. Valid means red-edge common-red
neighbor count at most three and blue-edge common-blue neighbor count
at most six, for ordinary books. The universal degree theorem gives
the corresponding exclusion for every valid 22-vertex graph.

The [four-cycle proof](PROOF.md) derives the complete two block families and proves
their coverage, including the alternative internal generator at every
degree-nine orbit in the disjoint case. It explicitly imports the
degree theorem and the regular blue-codegree lemma. Its global corollary
inherits the former's historical spectral-classification premise.
The reductions are written mathematics, not formalized proofs. The
finite exclusion is exact and reproducible. The companion
[fixed-point argument](FIXED_POINTS.md) excludes the other three possible
cycle types by ordinary pair counting, without a finite host census or
regular-codegree premise. No independent review of this new result is
claimed. The unrestricted **22<=R(B4,B7)<=23** interval remains open.

## Reproduce

CPython **3.11.2** was used; Python 3.11+ standard library suffices.
No solver, external package, random search, floating-point decision,
external certificate, or graph catalogue is needed by these programs.
Run the two jobs **sequentially** from the repository root:

```sh
cd round-two/six-books-2/order_five_four_cycles
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B -O generate.py --output literal_results.json
python3 -B -O verify.py --literal literal_results.json --output orbit_results.json
python3 -B -O check_fixed_points.py
```

Require successful exits and `status: complete`. The generator produces
**18,250** actual forbidden books: 10,250 disjoint templates and 8000
shared templates. The separate verifier imports no generator code. It
checks every certificate with literal neighbor sets, its exact
correlation count entrywise, admissibility and distinctness of all keys,
and the exact cardinality of both normalized grids. It then scans
**4,562,500** unnormalized templates: 2,562,500 disjoint and 2,000,000
shared, retaining every cross-block phase and both difference classes.
No template survives either complete route. Progress output every
250,000 templates is informational; it is not a completed proof.

The canonical compact-JSON SHA256 of the literal **records array** is
`7308685d5b823f1639ee00746e26d10b7314e3e9d5e44b3d66dbf218de696ab5`.
The concatenated five-byte first-violation tuples in the unnormalized
iteration have SHA256
`0df739b48ed1d20e28c26516772478796fa70ef244315c3ed921c5ccafbcdd69`.
Complete family counts and the unnormalized histogram are in
[expected.json](expected.json). These hashes identify exact results;
they do not replace the coverage proof or checking each obstruction.

The local literal report was **899,095 bytes**, including variable
timing metadata. Its file-byte hash is therefore not a reproducibility
criterion. Reports, caches and the full witness array are generated
local output and are omitted from publication. The source is sufficient
to regenerate all of them. Both jobs use one CPU process; the complete
author executions used under 40 MiB peak resident memory each. Generation
took 2.130 seconds / 30672 KiB peak RSS; the separate complete verifier,
including its controls and literal checking, took 96.265 seconds /
35016 KiB. These are measured runs, not resource guarantees.

For a shorter exact verification of the entire normalized certificate
domain, run:

```sh
python3 -B -O verify.py --literal literal_results.json --certificates-only
```

This verifies the normalized proof route and omits the additional full
unnormalized replay. For algebra/encoding controls only:

```sh
python3 -B -O generate.py --controls
python3 -B -O verify.py --controls
```

The latter tests all 231 literal spines in each of 64 deterministic
arbitrary cyclic graphs, all 210 spines of a positive KG(7,2) control,
all 2048 disjoint local mask/generator states, the 82 size/generator
classes, 2304 shared-cycle mask states, and 373248 shared-independent
integer states. These validate the written identities/reductions; they
are not a census of unrestricted hosts. The KG construction is known
prior art, reproduced by literal root-pair disjointness, with 105 red
spines of page count three and 105 blue spines of page count five.

Both programs accept `--limit` for a local prefix. A proper prefix writes
`status: partial` and cannot establish the full result. The literal
verifier rejects such a producer report. Limits outside 1..18250 and
1..4562500 respectively are errors. Certificate validation uses explicit
exceptions, so it remains active with Python `-O`.

After generating the complete literal report, the reproducible failure
controls can be run separately:

```sh
python3 -B -O check_failures.py --literal literal_results.json
```

All **24 controls** pass: altered keys, literal books, coverage counters,
hashes and histograms are rejected; an actual partial producer is
rejected; an actual unnormalized prefix is labelled partial; and four
out-of-range limits are rejected. The admissible degree-nine alternate
generator is also positively retained. This script exercises the
verifier interface and imports it; it is not a third proof algorithm.

## Imported mathematics and provenance

- Degree range 8..10: committed lemma **8012**,
  `bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`,
  source commit `ce3177a731086284ee89f18a8a3948b672b3c64e`;
  [proof and dependency scope](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md).
- A blue pair in a valid ten-regular graph has at least two common red
  neighbors: committed lemma **8541**,
  `bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a`,
  source commit `53fa7ea66251df9d255b7d0ff9d0ff309580d42a`;
  [standalone ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md).

The full committed statements and source provenance were read. These
predecessor checkers were not replayed here. The minimum-eight corollary
inherits the uniform-incidence result and accepted
Bussemaker--Cvetkovic--Seidel least-eigenvalue-minus-two classification;
the maximum-ten part imports its finite Gram exclusion. The regular
blue-codegree theorem itself has an ordinary proof without that
classification. The earlier Kneser and irregular-seed switching results
are context, not dependencies.

Primary literature and the authors' polycirculant construction code
were checked live on 2026-10-01. Their equal-orbit-size definition does
not cover this action with two fixed vertices. References and precise
scope are in [PROOF.md](PROOF.md). No historical priority assertion is
made. Publication is source plus compact expected evidence; a complete
search and its written reduction, rather than a timeout or a hash,
support the scoped exclusion.

The fixed-point script also passes in normal Python mode. It validates
the exact degree possibilities, all nine degree-pair inequalities and
all six one-orbit packing bounds against
[expected_fixed_points.json](expected_fixed_points.json). These are
arithmetic controls for the ordinary proof, not an unrestricted census.

# Independent six-element spectral-downset review

Reviewer: **six-reviewer-5**, independent mathematical reviewer.
[REVIEW.md](REVIEW.md) gives the verdict, finite coverage proof, exact trust
boundaries and constructive refinements. General Conjecture H remains open.

Reproduce from repository root with GCC 12+ and Python 3.11+, standard
libraries only. Choose a generated-work directory outside this repository:

```sh
python3 -B spectral_downset_six_review5/reproduce.py --work /tmp/downset-review5
python3 -B -O spectral_downset_six_review5/reproduce.py --work /tmp/downset-review5-opt
```

Each command compiles a single-threaded C++17 census, enumerates all
7,828,354 labeled downsets, directly quotients by all 720 coordinate
permutations, generates 16,350 fresh positive partitions, and independently
checks their entire stream in Python. It also checks all 46,080 permutation
basis images, an exhaustive small reference, the exceptional exact matrix,
fractional primal/dual certificates and the refinements. Output must equal
[expected.json](expected.json). The source generator is never imported.

The original matrix data and proposed degree-seven annihilator are in the
small code/fixture; every required identity is checked directly. Full
catalogs and binaries are regenerated in the chosen private work directory.
Approximate resources: one process at a time, below 100 MiB for the census,
several seconds of census time plus compilation and Python verification.
No numerical solver, downloaded proof corpus or proprietary library.

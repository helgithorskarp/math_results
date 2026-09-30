# R137 minimum kernels require three unary events

Author and executing agent: **six-sorting-1, researcher**.

Every standard 18-comparator sorter of the exact 137-state ten-wire target
R in fixture.json has exactly three unary minimum events and two binary
minimum merges. The minimum routes use exactly 3, 2, 3 comparators for the
single-zero rows initially at 0, 1, 5. Every unary event touches a singleton
leaf of the minimum forest. With the earlier preparation theorem, global
minimum extraction occurs at comparator 8 or later within the R suffix.

This is a conditional structural result. **R remains 18..19, the Y1/Y2
targets remain 20..21, and the global thirteen-input minimum remains
44..45.** It excludes the two-unary R18 class, not the remaining
three-unary class, the unary-maximum Y20 classes or arbitrary thirteen-wire
prefixes. It gives no 44-comparator sorting network.

R is the common lower-ten-wire image of two literal 26-comparator prefixes
on thirteen inputs, each holding the largest three values on wires 10..12.
Both prefixes, all 137 rows and a known 19-comparator completion are in the
small fixture. The scalar verifier rederives both full Boolean images and
checks the 45-comparator controls on all 16,384 original inputs.

Reproduce with standard-library **Python 3.11 or later on Linux/POSIX**, assertions enabled,
one CPU and one job at a time. From this directory:

```bash
python3 generate.py
python3 generate.py --resume
```

Repeat the resume command until `status` is `all_cases_complete` with
`completed_cases` 850. Then run:

```bash
python3 verify.py
python3 verify.py --resume
```

Again finish all 850 cases. Each invocation starts no new case after 35
seconds and passes a 45-second batch deadline; each class has a 50,000-state
cap. An incomplete run establishes no exclusion. Exact, source-bound local
prefix caches and progress go under ignored scratch/. Resume trusts those
self-generated local caches; remove only this directory's scratch/ for a
fresh replay. The verifier regenerates its own states, using no generator
state set as seeds, and compares full state sets, counts and hashes. A
50,000-state in-memory cache reduces repeated file decoding; it adds no
mathematical pruning.

The complete catalogue has 1,138 words. The sole-maximum-gate condition
excludes 288; the other 850 all have empty closures. These represent
16,321,664 phase-state appearances and 375,659,335 candidate transitions.
Exact shared-prefix factoring computes 1,029 distinct nongate closures,
508,468 distinct node-state entries and 11,428,494 nongate transitions.
The largest individual class has 30,930 states. certificate.json contains
compact catalogue, aggregate and canonical state-set hashes, not a large
proof-state corpus. No SAT solver, external package or fixed-depth
restriction is used.

[PROOF.md](PROOF.md) states the finite coverage and imports. This builds on
[the two-unary lower restriction](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_two_unaries),
source 311db353e65858960dbdc995253abfaddb895427, graph
bafkreiauub7gqvdcvd2equ5n3von7w7c4f2ovtapmuqbxq7i4aqlrstfha.
The inherited minimum-once and preparation theorems and published sorting
lower bounds are not rerun here. The two exact algorithms complement the
written abstraction/completeness argument; this is not external-person
review or proof-assistant formalization.

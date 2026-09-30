# Every induced 17-vertex Kneser core has maximum valid host order 21

Author: **six-books-3**, role **researcher**, 2026-09-30.

Let K have the 21 two-subsets of {0,...,6} as vertices, with red edges
between disjoint subsets and all other pairs blue. For every four-element
vertex set S of K, **every coloring containing an induced color-preserving
copy of K-S and avoiding a red B4 and a blue B7 has at most 21 vertices**.
K attains the bound. All binom(21,4)=5985 deleted sets are covered. Every
edge incident to the other vertices is arbitrary; the host need not be
regular, symmetric or representable by root disjointness. Books are
ordinary subgraphs, with unrestricted page-to-page edges.

The [proof](PROOF.md) reduces the fixed cores by explicit root-point
actions to ten types. It certifies complete one-vertex and colored-pair
domains, including tests for repeated patterns. No repeated pattern is
compatible. It then enumerates every valid prefix with three, four and
five outside vertices in increasing pattern order. A book at an earlier
prefix excludes all its completions by heredity. All ten five-vertex
lists are empty. The generator uses saturated old-spine constraints and
new-spine page counts. The complete native checker independently
visits masks in Gray-code order, checks pairs and prefixes as full graphs,
and maps every deletion to a representative by checked point isomorphisms.
All domains, pairs and retained prefixes agree entry for entry. A Python
comparison layer also checks every final book location with literal sets.
No degree or edge-count cut is used.

The consequence is that every 21-vertex deletion of a hypothetical valid 22-vertex
coloring differs from K, under **every** labeling, on a graph of changed
pairs with vertex-cover number at least five. This strengthens the earlier
[induced 18-core obstruction](../book_ramsey_b4_b7_kneser18_obstruction/PROOF.md),
whose cover bound was four. It does not decide the unrestricted Ramsey number.

| Deleted root type | Deleted sets | Patterns | Colored pairs | Valid20 | Valid21 | Final22 tests |
|---|---:|---:|---:|---:|---:|---:|
| star4 | 105 | 1690 | 146469 | 175980 | 3125 | 857 |
| path4 | 1260 | 927 | 76680 | 172664 | 6844 | 637 |
| fork | 1260 | 1040 | 79183 | 130936 | 5716 | 542 |
| cycle4 | 105 | 1003 | 63508 | 147588 | 6247 | 1468 |
| paw | 420 | 1574 | 194070 | 376918 | 4617 | 849 |
| triangle edge | 210 | 1411 | 177248 | 521025 | 6764 | 872 |
| star edge | 420 | 1134 | 119355 | 195809 | 7247 | 448 |
| path edge | 1260 | 505 | 34376 | 99650 | 6442 | 3316 |
| two wedges | 630 | 634 | 59118 | 229402 | 6769 | 1278 |
| wedge two edges | 315 | 262 | 11651 | 48484 | 5824 | 54 |

All final 22-vertex lists are empty. Totals: 10,180 patterns; 961,658 colored
pairs; 2,098,456 valid 20-vertex prefixes; 59,595 valid 21-vertex prefixes;
and 10,321 final joining tests. Generation took 620.1 seconds with
332,604 KiB peak RSS on the author's one-CPU run.

## Reproduce

Run from this directory with CPython 3.11+ (standard library), a
GCC/Clang-compatible C++17 compiler, and one CPU thread. Require every
command to succeed:

```bash
set -e
mkdir -p /tmp/kneser17-build
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 generate.py --scratch /tmp/kneser17-cases --summary /tmp/kneser17-summary.json
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic native_check.cpp -o /tmp/kneser17-build/native_check
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 /tmp/kneser17-build/native_check /tmp/kneser17-native
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check_native.py /tmp/kneser17-cases /tmp/kneser17-native --expected native_expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 controls.py /tmp/kneser17-cases
```

The author's GCC 12.2.0 native run took 17.5 seconds/55,592KiB; the entrywise
Python comparison and all 10,321 literal book-location checks took 21.25 seconds/
767,896KiB. These follow the 620.1-second generator run. Controls took 56.4 seconds/
440,440KiB. All jobs are sequential. [verify.py](verify.py) supplies a
slower full set-graph reference (`python3 verify.py /tmp/kneser17-cases`);
five of ten types were replayed with it in addition to the complete
native cross-check. All ten domain trees were separately checked, and
the smallest type had a prior complete set-graph prefix reproduction.

A checking build can replace the optimized native executable:

```bash
g++ -std=c++17 -O1 -g -Wall -Wextra -Wconversion -pedantic -fsanitize=address,undefined -fno-omit-frame-pointer native_check.cpp -o /tmp/kneser17-build/native_check_san
/tmp/kneser17-build/native_check_san /tmp/kneser17-native-san --case wedge_two_edges
python3 check_native.py /tmp/kneser17-cases /tmp/kneser17-native-san --case wedge_two_edges --expected native_expected.json
```

This author checking run completed in 3.35 seconds/171,868KiB and included
the full 5,985-deletion census, exact red/blue threshold tests, eight small
Gray-domain comparisons and the complete smallest core. The full Python
comparison also passes under `python3 -O`, with checks still enabled.

The generator records atomic per-level checkpoints in the specified scratch
directory. Add `--resume` to continue those files after interruption; the
native checker still recomputes every domain and prefix from scratch.
Completion requires every representative and every level. Partial state,
interruption, failure or absence of a summary is never a proof verdict.
[expected.json](expected.json) contains deterministic counts and hashes
of every domain, pair list and retained prefix level. The large generated
lists stay in scratch and are omitted from Git. No external data, graph
catalogue, solver or floating-point arithmetic is needed.

Controls independently sweep all 131,072 masks for each of the ten cores,
compare all 68,906 pair/color tests for the smallest core with literal full
19-vertex set graphs, and reject six damaged certificates. These checks
cover an omitted valid prefix as well as falsely complete state, a wrong
core, an unjustified conflict, an omitted pair and a corrupted joining mask.
Author validation is not an independent peer-review verdict. The domain,
core-coverage and prefix-completeness bridges are written and unformalized.

## Book locations

Of the final 10,321 assignments, exactly 69 have no cross-spine book.
There are 24 cycle4 assignments with only blue outside/outside violations,
and 45 assignments with both red outside/outside and blue core/core
violations. [native_expected.json](native_expected.json) records their
exact cohorts and location histograms. This limits a useful refinement
from [the independent 18-core review](../book_ramsey_kneser18_review1/README.md);
that review is credited context, not a review of this new result.

[witness.json](witness.json) gives one literal cycle4 example. Every
pair extension and its first-four prefix are valid, all full red degrees
are 7--11, and its only forbidden books have blue outside/outside spines.
The checked blue spine 17,18 has pages 0,4,11,12,13,19,21. This graph is
invalid and supplies a counterexample to the analogous cross-spine
strengthening, not a 22-vertex Ramsey witness. `check_native.py` checks
all fixture statements directly, without importing either generator.

## Attribution and scope

The seed is known: Dai--Lin [Remark 4.1](https://arxiv.org/html/2606.07214v1#S4.SS1)
recalls its complementary triangular graph and credits Hoffman. The seed's
105 red edges, red degrees 10, red spine-codegrees 3 and blue spine-codegrees 5
are checked exactly. Reproducing it is validation; the scoped contribution
here is the arbitrary-extension exclusion for all 5,985 induced 17-vertex cores.
No priority claim for this restriction is made.

Primary [Lidicky et al., Table 1](https://arxiv.org/html/2407.07285v2#S2)
and [Radziszowski DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
were refreshed 2026-09-30. The located global interval remains
22<=R(B4,B7)<=23; the global upper certificate was not replayed here.
There is no assertion that every 22-vertex coloring contains a core from
this family. The teammates' [universal degree/capacity restrictions](../book_ramsey_4_7_degree_reductions/capacity.md)
and [fixed Steiner-core repair restrictions](../book_ramsey_disjointness_family/THREE_RED_EDGES.md)
were read and are complementary; neither is a premise of this proof.

Generic native direct-book, Gray-domain and point-map helpers are adapted
with attribution from six-reviewer-1, [independent.cpp](../book_ramsey_kneser18_review1/independent.cpp),
source 0b527dd00c913e5148b473d8e0d2bc556d11bf75. This author's new native
parts are the four-deletion census, five-prefix traversal and book-location
records. Reimplementing the prefix recurrence alone would be performance
validation; the independent domain traversal, full graph tests and root
isomorphism census add distinct validation mechanisms. The earlier review
does not cover this 17-core theorem.

# A reduction for free involutions in R(B4,B7)

Author: **six-books-2**, role **researcher**, 2026-09-30.

Every ordinary red-B4/blue-B7-free coloring on 22 vertices with a
fixed-point-free color-preserving involution needs **at least two fully
red orbit pairs and at least seven uniform orbit pairs**. An orbit pair
is uniform when all four edges between its two two-vertex orbits have
one color. Inside-orbit colors are arbitrary, and every such involution
is covered.

[PROOF.md](PROOF.md) gives a self-contained analytic proof. It excludes
zero or one fully red pair at any blue density, then classifies and
excludes both possible six-uniform-pair shapes. Its two matrix mechanisms
are a commuting-square integer congruence and an invariant-space trace
that forces eigenvalue eleven in a six-by-six sign matrix with row bound
five. The checks below validate formulas and coverage; no finite
computation is a premise of the analytic lemma.

The unrestricted located interval remains 22..23. This result does not
assert an involution for arbitrary hypothetical 22-vertex witnesses, or
exclude patterns with seven or more uniform pairs and at least two red
pairs. No regularity, degree, peer core theorem, external graph catalogue,
solver or floating-point premise is used. Author checks are not peer
review or proof-assistant formalization.

## Reproduction

Requirements: Python standard library and a C++17 GNU-compatible compiler
with `__builtin_popcount`. Tested on Linux with Python 3.11.2 and GNU
g++ 12.2.0; actual toolchain versions are recorded in the author's audit.
From the repository root, run

```sh
python3 book_ramsey_b4_b7_free_involution/check.py --scratch /tmp/book-free-involution-check
```

The runner builds with `-std=c++17 -O2 -Wall -Wextra -Wpedantic` and runs
all jobs sequentially with thread counts one. Each child has a 120-second
timeout; any timeout, failed build, malformed result or mismatch raises
an error and cannot produce a completed summary. Generated binaries,
survivor lists and logs stay in scratch, outside this directory. The
complete tested run took 65.30 seconds with 100,436 KiB peak child RSS,
including compilation. No large artifact or external mathematical
input is required.

The compact expected values are in [expected.json](expected.json):

| Check | Exact coverage |
| --- | --- |
| [census.cpp](census.cpp) | 3,858,660 normalized six-pair color patterns; 7,700 pass relaxed matching budgets; 56 patterns/3,584 inside-color assignments pass all necessary budgets |
| [independent_census.py](independent_census.py) | Separately constructs literal two-point page sets and set-based quotient budgets; compares every survivor and flag entry and reconstructs exactly 28 instances of each of the two analytic shapes |
| [formula_controls.cpp](formula_controls.cpp) | 1,967,496 small lifted graphs; 51,366,336 general matching-spine checks; 13,038,960 uniform-spine difference checks; clique-square and commutation checks |
| [matrix_controls.py](matrix_controls.py) | All eight rank-one sign blocks, 720 normalized shape-A row tuples, 2,160 normalized shape-B row tuples; exact Fraction coordinates and traces -7,-4 |

The quotient census fixes each possible one-, two-, or three-red-edge
form up to orbit relabeling, then enumerates every disjoint blue set.
Matching signs are relaxed separately at each spine. Its survivors are
**necessary patterns**, not valid graphs. The inside flags cover all
2^11 choices; the separate Python checker enumerates active flags and
expands every inactive flag choice, comparing the complete resulting
lists. The five-pair option in `census.cpp` is an additional supported
diagnostic; it is not needed by the runner or the analytic proof.

Formula controls enumerate all blue/parallel/crossed choices and all
inside flags on three through five orbits, and all four cross types on
three and four orbits. Thus they compare actual graph common neighbors
with the formulas, rather than another implementation of the formulas.
Neither these small controls nor the quotient census enumerate all
order-22 graphs or all matching signings.

Arithmetic: a colored graph has at most 22 vertices, using a 32-bit
unsigned vertex mask; a quotient has 55 pairs, using a 64-bit unsigned
pair mask. Every shift is below the respective width. C++ counters are
64-bit and all stated counts are below 2^32; signed page and matrix
expressions are bounded by small multiples of the orbit order. Python
uses unbounded integers and exact fractions. Checks use explicit
exceptions and remain enabled under Python `-O`.

The full literal-formula controls also passed address and undefined
behavior sanitizers, with identical output and no diagnostic, in
16.87 seconds including compilation (142,104 KiB peak child RSS):

```sh
g++ -std=c++17 -O1 -g -Wall -Wextra -Wpedantic -fsanitize=address,undefined -fno-omit-frame-pointer book_ramsey_b4_b7_free_involution/formula_controls.cpp -o /tmp/book-formula-sanitized
/tmp/book-formula-sanitized
```

The trust boundary is the written analytic reasoning, plus the compiler,
Python interpreter and source inspection for validation. There is no
enumeration-completeness bridge in the theorem: the finite census is an
independent audit of an explicit complete written case argument.

## Primary context

[Lidicky--McKinley--Pfender--Van Overberghe, Table 1 and Section 3.3](https://arxiv.org/html/2407.07285v2),
[Radziszowski, DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
and [Wesley, Section 3](https://arxiv.org/html/2410.03625v2) were reopened
2026-09-30. The eleven-by-two representation is known polycirculant/
block-circulant structure; no priority claim is made for it or for an
exhaustive search of historical sources. The primary 21-vertex construction
was separately reproduced as baseline validation. The published general
upper flag-algebra certificate was not replayed here.

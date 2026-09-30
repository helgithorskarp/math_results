# A five-class component of valid Book Ramsey graphs

Author: **six-books-3**, role **researcher**, 2026-09-30.

For the published irregular 21-vertex (B4,B7)-avoiding graph H, the
component under **arbitrary two-vertex replacements, with every
intermediate graph valid**, consists of exactly five isomorphism classes.
Every graph in the component has trivial automorphism group. On a fixed
21-element vertex set this component therefore has exactly **5 * 21!**
elements. This classifies an entire component, rather than a bounded
number of moves or changed edges.

A replacement changes any number of edge colors, provided every changed
pair meets a set of at most two vertices. A graph is valid when each red
edge has at most three red common neighbors and each blue edge at most
six blue common neighbors. These are ordinary noninduced book conditions.
Vertex relabeling is allowed for isomorphism; exchanging the two colors
is not allowed.

There is a second certificate consequence: **every valid host containing
any induced 19-vertex subgraph of any of the five representatives has
order at most 21**. Each of the 1,050 indexed cores attains this maximum
in its own representative. Thus no 22-vertex witness can contain any
of those induced cores. This strengthens the earlier incumbent-only
[induced19 classification](../book_ramsey_b4_b7_induced19_rigidity/README.md).
The unrestricted gap 22 <= R(B4,B7) <= 23 remains unresolved.

## The five representatives

Use the precise labeled H in [h21.json](h21.json). The compact
[manifest](templates.json) specifies these symmetric differences from H:

| Name | Toggled pairs | Red edges |
| --- | --- | ---: |
| H | none | 93 |
| A | (6,16), (10,16) | 93 |
| B | (9,16), (10,16) | 93 |
| D | (3,10), (3,19), (9,16), (10,16), (11,19) | 94 |
| E | D's toggles plus (0,17) | 93 |

These representatives were previously found in the complete
[radius-seven classification](../book_ramsey_b4_b7_incumbent_edit_certificate/README.md).
Here their two-vertex replacement closure is certified independently of
that earlier enumeration. After removing self-loops, the quotient
component on isomorphism classes has exactly the edges

    H--A, H--B, A--B, B--D, D--E.

The displayed H-A, H-B, B-D, D-E moves already connect all five: their
changed pairs meet {16}, {16}, {3,19}, and {0}, respectively.

## Proof architecture

For each representative and each deleted pair, [generate.py](generate.py)
builds a complete decision tree for all red-neighbor patterns of one
added vertex. Necessary clauses from saturated old spines imply forced
assignments; every unforced split keeps both values. Complete assignments
are checked against the full graph definition. Every unordered pair of
patterns, including repeated patterns, is tested with both joining colors.
Every valid 21-vertex completion receives an explicit vertex permutation
to one of the five representatives.

[verify.py](verify.py) imports no generator code. It derives the clauses
from explicit page sets, uses clause scanning instead of implication
reachability, verifies every tree branch and leaf, tests every pair by
set-based graph reconstruction, and checks each isomorphism permutation
against the full edge set. The generator's canonical ordering is only
a witness-finding device; the checker does not trust it.

All 1,050 compatibility graphs are loop-free and triangle-free. Outside
vertices in any valid host have distinct, pairwise compatible patterns,
so they form a clique. A 19-vertex core therefore allows at most two
outside vertices. The full completion lists also prove closure of the
five classes under every two-vertex replacement. Three rounds of exact
joint color refinement distinguish all 105 template vertices, proving
pairwise nonisomorphism and trivial automorphism groups. The induction
from one-step closure to the entire component, and the labeling count,
are written in [PROOF.md](PROOF.md).

## Reproduce

Python 3.11+, standard library only; tested with CPython 3.11.2. Assertions
must be enabled. From the repository root:

```sh
mkdir -p scratch/books_component
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_b4_b7_replacement_component/generate.py --certificate scratch/books_component/component-proof.json --summary scratch/books_component/component-run.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_b4_b7_replacement_component/verify.py scratch/books_component/component-proof.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_b4_b7_replacement_component/controls.py scratch/books_component/component-proof.json
```

The checker compares the complete compact diagnostics with
[expected.json](expected.json). Total: 88,086 tree nodes, 43,656
necessary-kernel models, 6,996 valid patterns, and 1,260 colored pair
completions with checked isomorphism witnesses. The canonical projection
SHA256 is

    bbf642bf7a06630c34e2462a4518cd9a4ba7b14f1fe0818995dd7ae1fc5a4abe

Counts and hashes are diagnostics; the checked trees and all-pair
reconstruction establish coverage. Generation took 5.11s and verification
16.31s, with peak RSS below 27MiB. The locally generated 675388-byte proof
tree is not committed and is not a required external input.

[controls.py](controls.py) independently sweeps all 524,288 patterns of
E-{16,19}, reproducing its largest 34-pattern domain entry by entry.
It rejects a missing representative, a false conflict, an omitted valid
pair, a bijective false isomorphism, a wrong target class and incomplete
status. Controls took 2.20s. Only one CPU job/process runs at a time;
there is no solver, floating-point arithmetic or parallel job pool.

This is an exact computer-assisted theorem with unformalized elementary
bridges. It is not a proof-assistant formalization or an independent
peer-review verdict. There is no timeout or incomplete-search inference.
The proof's remaining trust is the displayed mathematics, inspected
source, input fixture and Python's exact integer/set execution.

## Primary source and scope

H is the known witness of Lidicky, McKinley, Pfender and Van Overberghe,
[Small Ramsey numbers for books, wheels, and generalizations](https://arxiv.org/abs/2407.07285),
Table 1. Its author-repository source is
[R_B4_B7_construction_21vertices.txt](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
The off-diagonal zeros in that matrix are red. Original file SHA256:
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55.
The normalized H fixture SHA256 is
189afcebf499016989b196498ccb3ed6431c7599f3ee5c638784f29be0d4eda0.
The source repository is distributed under CC BY 4.0; the small
mathematical fixture is reproduced with attribution. No novelty is claimed
for H, its Ramsey lower bound, or the general pattern-compatibility idea.

The primary paper and Radziszowski's April 24, 2026
[Small Ramsey Numbers survey](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
Table IXa, were refreshed on 2026-09-30. The located global gap remains
22..23. The published upper certificate has not been independently
audited here. This specific component classification was not located in
the searched primary sources; no priority assertion is made. Other valid
21-vertex graphs may lie in other components. No teammate structural
theorem is assumed by this proof.

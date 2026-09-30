# Induced19 completion rigidity for the primary Book Ramsey witness

Author: **six-books-3**, role **researcher**, 2026-09-30.

**Scoped computer-assisted theorem.** For the primary 21-vertex witness H,
delete any two vertices S and retain its induced 19-vertex graph C. Every
(B4,B7)-avoiding graph containing an **induced** copy of C has at most
21 vertices. In particular, no 22-vertex witness can retain any of these
210 cores. The maximum 21 is attained by H itself.

There is also an exact rigidity statement for 21-vertex completions.
Keep the 19 core labels fixed and allow the two new vertices to be swapped.
Every valid completion is H or one of the two graphs

    A = H toggled on {(6,16),(10,16)},
    B = H toggled on {(9,16),(10,16)}.

The complete rule is:

| Deleted original vertices S | Allowed completions | Compatibility graph |
|---|---|---|
| 16 belongs to S | H, A, B | Three-leaf star (20 cores) |
| S = {6,10} | H, A | Two disjoint edges (1 core) |
| S = {9,10} | H, B | Two disjoint edges (1 core) |
| Every other S | H | Single edge (188 cores) |

Isolated vertices in the compatibility graphs are omitted from this table.
No claim that H, A, B are pairwise nonisomorphic is made. Books are ordinary
subgraphs; the retained backbone C is induced. The Ramsey gap remains
22 <= R(B4,B7) <= 23.

For attempted extensions of H, this rules out every repair in which all
changed old pairs can be covered by one or two original vertices, regardless
of the number of such changes. [PROOF.md](PROOF.md) supplies the precise
general compatibility argument, finite coverage proof, and corollary.

## Certificate architecture

For each C, enumerate every red-neighbor set that can be assigned to one
new vertex while avoiding the books. Saturated old spines give binary
implications; complete binary decision trees plus literal graph checks
give the exact domain. Check every unordered pair of domain patterns and
both colors of their joining edge, including pairs of identical patterns.

All 210 resulting compatibility graphs are loop-free and triangle-free.
Any three additional vertices would require either a loop or a triangle,
so no valid graph can add more than two vertices. This covers all 2^60
colorings of the three new vertices' incident pairs for each fixed core
without listing them. No symmetry of H is assumed or used.

`generate.py` builds implication closures with integer bit sets.
`verify.py` independently checks the tree by scanning necessary clauses
and verifies all graphs using explicit vertex sets. It imports no
generator routines. Tree branching is checked for complete coverage;
conflict and invalid leaves are justified directly. The checker also
compares every allowed pair to the three claimed templates.

There are 18,246 decision-tree nodes, 9,055 consistent necessary-kernel
assignments, and 1,308 valid one-vertex domain patterns across the 210
cores. Domains have sizes 2 through 24. The canonical projection of
deleted pairs, domains, and compatible pair colors has SHA-256
`ad2c7b6c7215271dbd34d2bb627e1230773a009947a7a42603d7346f593f1a05`.
Its exact serialization is in both source files. `expected.json` records
the compact expected statistics and hash.

## Reproduction

Python 3.11.2, standard library only, assertions enabled. From this directory:

```sh
mkdir -p scratch
python3 generate.py --certificate scratch/domains-proof.json --summary scratch/domain-run.json
python3 verify.py scratch/domains-proof.json
python3 controls.py scratch/domains-proof.json
```

The verifier must report all 210 cores, the displayed projection hash,
shape counts 188/20/2, and maximum host order 21. The controls must report
entry-level agreement for a direct sweep of all 524,288 patterns of
H minus {6,18}, with 24 survivors. They also reject a false root conflict,
an omitted core, a fabricated compatible loop, and an incorrect valid-leaf
assignment.

Measured runs used one process and no native numerical or solver threads:
generation 0.89 s / 19,672 KiB peak RSS; verification 3.32 s / 18,256 KiB;
controls 3.17 s. Timings vary with host load. The deterministic temporary
decision-tree bundle is 113,112 bytes and is generated locally rather than
committed. No external proof data or large artifact is required.

## Input, attribution, and status

`h21.json` contains the 93 red edges of the authors' known irregular
[21-vertex construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
Its vertex labels are unchanged, 0 through 20; off-diagonal **zero** matrix
entries become red edges. Original source-byte SHA-256:
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
The normalized red-edge fixture SHA-256 is
`189afcebf499016989b196498ccb3ed6431c7599f3ee5c638784f29be0d4eda0`.
The verifier checks the fixture hash and the red/blue codegree caps 3/6.

Credit: Lidicky, McKinley, Pfender, Van Overberghe,
[Small Ramsey numbers for books, wheels, and generalizations](https://arxiv.org/abs/2407.07285),
Table 1 and supporting repository. The fixture is an edge-list complement
conversion of their matrix, distributed there under CC BY 4.0.
The [April 2026 primary survey](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
Table IXa, retains the gap. Current primary papers and relevant team
source were inspected before this classification; no priority claim is
made for the new scoped restriction or for the general compatibility idea.
The baseline construction and its lower bound are known results.

The finite certificate checks and the hand-written completion bridge give
an exact computer-assisted result. They are not proof-assistant checked.
The trust boundary is the displayed elementary reductions, the checker
implementation, and Python's exact integer/set operations. The generator
is not trusted by the independent checker. Both programs and controls
are by the same researcher; this is not independent peer review.

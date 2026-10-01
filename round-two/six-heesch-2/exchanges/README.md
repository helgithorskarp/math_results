# One-delete-two-add polyhex family

**six-heesch-2, researcher.** All 4,990 free connected hole-free eighteen-cell
shapes obtained by deleting one cell from the known seventeen-cell H4 seed
and adding two cells either tile periodically or have `H_h <= 2`, allowing
all real Euclidean motions and reflections.

| Checked result | Shapes |
|---|---:|
| `H_h=0` | 3,471 |
| `H_h=1` | 1,008 |
| `H_h=2`, with two-corona certificates | 2 |
| `1 <= H_h <= 2` | 14 |
| Periodic tiling | 495 |

The fourteen interval cases are not asserted to have exact Heesch number
two. Exact `H_c` values are generally not classified. No member of this
family supplies a finite-five polyhex, and no new record is claimed.

The [proof](proof.md) gives the two complete generation arguments,
depth-one supported-contact pruning, and an odd-cycle obstruction for the
last survivor. Its pair domains stabilize while the compulsory triangle
has inconsistent star types. Canonical case 3598 has exactly `H_h=2`; its
two-corona witness has 1, 7, 14 copies and four holes only in the final union.
Case 3602 reproduces the earlier graft case 18. Twenty-six members are prior
grafts; the other 4,964 are disjoint from both earlier sixteen-cell growth families.

Run from repository root with CPython 3.11 or newer, standard library,
assertions enabled, and one native thread:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-heesch-2/exchanges/verify.py
```

The replay independently regenerates all 4,990 canonical shapes, validates
every periodic certificate, checks positive corona constructions, and
regenerates all negative searches with rejection-DAG auditing. Expect
the table above and result SHA256
`8a9a980e059c5cfb720250400017c1b3112cb2bce65a9de1c0c3af3146781e25`.
The complete compact replay passed in 1,738.651 seconds (about 29 minutes),
using 56,136 KiB maximum RSS on one CPU with CPython 3.11.2. It audited
532,993 negative calls and 1,884,869 failed states. The replay avoids
rediscovering periodic tilings. A node guard or interruption leaves
incomplete work and gives no whole-family verdict.

For only the stable-domain example and its odd-cycle proof, append `--focus`.
This also regenerates the family, and explicitly reports
`complete_family:false`. Optional `--checkpoint PATH` stores private
operational progress; `--stop-after N` returns an incomplete result.
Checkpoints are not standalone mathematical certificates.

The source imports the already published exact geometry, cover auditor,
pair-peeling code and seed fixture from the parent directory; retain that
directory when reproducing. [expected.json](expected.json) records the
canonical case indices and proof routes. [certificates.json](certificates.json)
contains 495 compact periodic witnesses and the two lower-bound witnesses.
No private dataset, solver, external input or raw proof corpus is required.

These computer-assisted findings have not been formalized and do not carry
an independent reviewer verdict. Shared integer isometry primitives and
the written geometric/depth arguments remain part of the trust boundary.

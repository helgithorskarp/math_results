# A four-parent palette exclusion for classical Schur-six

Four independently obtained near-colourings define a nonlocal family of
six-colour words on `[1,537]`. Relabel each parent as specified below. At each
position, allow any colour appearing there in at least one aligned parent;
ignore the one hole in parent C. **No word in this entire palette family is a
valid classical Schur colouring**, with `x=y` included.

This is an exact restriction on a large construction search space, not an
upper bound on `S(6)`. A valid 537-colouring, if it exists, must use a colour
outside this particular four-parent palette at some position. The result
also holds after simultaneously permuting all six colour labels.

## Explicit family

The four saved 537-entry inputs are copied byte for byte from previously
published work:

| Local copy | Origin | Directly checked status |
| --- | --- | --- |
| [`parent_a.txt`](parent_a.txt) | [`best2.txt`](../schur_s6_distant_two_defect_search/best2.txt) | 2 defects |
| [`parent_b.txt`](parent_b.txt) | [`best4.txt`](../schur_s6_nonlocal_doubling_search/best4.txt) | 4 defects |
| [`parent_c.txt`](parent_c.txt) | [`traded.txt`](../additive_combinatorics/schur6_support_exchange_traps/traded.txt) | hole at 161, no assigned defect |
| [`parent_d.txt`](parent_d.txt) | [`best2.txt`](../schur_s6_weighted_onehole_search/best2.txt) | 2 defects |

Keep A's colour labels. For B, C and D, the following row gives, in order,
the **old parent label** that becomes new label `1,2,3,4,5,6`:

```text
B: 1 6 5 2 3 4
C: 1 3 2 6 5 4
D: 5 2 1 4 6 3
```

The maps are permutations and leave C's hole unassigned. The resulting
position palettes have sizes `1,2,3,4` at respectively `10,97,320,110`
positions. Their raw Cartesian product contains
`2^97 * 3^320 * 4^110 > 10^248` distinct complete words, most of which
already violate Schur equations. The ten singleton positions are
`104,284,296,304,343,361,408,428,512,516`; none of the first 103 entries
is fixed. The family permits changes throughout every old colour class.

## Exact certificate and trust boundary

For every allowed `(position,colour)` pair, `encode.py` makes one Boolean
variable. Each position gets exactly one allowed colour. For each unordered
`x<=y` and `x+y<=537`, and each colour available at all involved positions,
a negative clause forbids that monochromatic equation. Repeated literals
are collapsed when `x=y`. Thus a SAT assignment is exactly a valid word in
the stated family; an independently checked UNSAT proof excludes the family.
There is no first-use normalization or extra fixed prefix.

The separate standard-library `audit.py` checks each parent's defects and
hole, reconstructs the aligned palettes, and compares the complete DIMACS
clause **multiset** with an independent endpoint-first traversal of all
72,092 Schur triples. It imports neither the encoder nor a solver. The CNF
has 1,604 variables and 53,932 clauses, SHA-256
`d6f554606c9d980baff5435f27d54908db38cf180d1374042fe8a3d8adbe24c6`.

CaDiCaL 1.9.5 at source commit
`146207318796f094dcded87349a64f0c6927309e`, built with GCC 12.2,
returned `UNSATISFIABLE`. Its 10,169,326-byte binary DRAT proof has SHA-256
`a48c10a38cc513c17104c5b34d9260c5b36fe74bd8bb766e5bc30a7c00cb7cff`.
Independently, [drat-trim](https://github.com/marijnheule/drat-trim) at
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` returned `s VERIFIED`,
using 24,018 input clauses and 132,913 learned clauses in its core. The raw
proof and CNF are generated locally and omitted from this compact repository
directory. Solver `UNSAT` alone is not the proof.

## Reproduce

Use Python 3.11 or later, [CaDiCaL 1.9.5](https://github.com/arminbiere/cadical)
and the cited drat-trim. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B encode.py --output /tmp/schur-four-parent.cnf
python3 -B audit.py /tmp/schur-four-parent.cnf
cadical -q -n /tmp/schur-four-parent.cnf /tmp/schur-four-parent.drat
drat-trim /tmp/schur-four-parent.cnf /tmp/schur-four-parent.drat
```

The audit prints
`PASS parents=4 n=537 variables=1604 clauses=53932 palettes=10,97,320,110 doubling_included=yes`,
and the final command must
print `s VERIFIED`. A regenerated proof may have different bytes after a
compiler or solver change; DRAT verification, not a matching proof hash, is
the gate.

This palette arose from a constructive crossover attempt. Adding a fifth
distinct near-colouring remained `UNKNOWN` after 30 seconds in CaDiCaL and
120 seconds in Kissat; adding a sixth remained `UNKNOWN` after 30 seconds in
CaDiCaL and 120 seconds in Kissat. Those timeouts establish no exclusion or
new lower bound. The independently checked 536 construction remains the
published lower bound; the first decisive target is still a complete valid
word through 537.

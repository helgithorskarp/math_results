# Recorded validation

Date: 2026-09-07. Interpreter: CPython 3.11.2 on Linux. Standard library only;
Python integers and exact combinatorial predicates throughout. No solver,
graph catalog, network input or randomness is used during reproduction.

The two complete runs, using final executable source, returned PASS and
byte-identical output matching `expected.json`:

| Command | Wall seconds | Peak child RSS, KiB |
|---|---:|---:|
| `python3 reproduce.py` | 32.769498 | 15112 |
| `python3 -O reproduce.py` | 33.433934 | 18152 |

Runs overlapped on the same host; these are observations, not isolated
benchmarks or resource guarantees. Correctness checks use explicit exceptions
and remain active with `-O`.

Expected report SHA-256:

`d20ee9a0e24cedc533dba692046c68a79206c63a5b0fcd03d9c99ebdb7d38a78`

The complete results are:

- 21 side-order/independence tuples covered with no duplication or omission;
  all 16 through separator order 19 excluded. Twenty of the 21 tuples through
  order 20 are excluded; (20,10,13,2,2) is a necessary residual only.
- 49,054 integer clique-attachment population vectors independently checked.
- Two full 698-free-pair branches audited through all 3,850,392 physical
  monochromatic events. Exact clause-length histograms and literal-stream
  digests agree with compatible-clique enumeration. There are no initial
  empty or unit clauses in either branch.
- Clique-growth control: all 33,867 labeled graphs of orders 1 through 6,
  131,418 eligible contact classes, and 842,894 clique extensions checked
  against literal independent triples. Prefix cores suffice for this finite
  control because all labeled graphs are included; this is not symmetry
  reduction in the target theorem.
- Contact-cover control: 6,144 graphs with a physical anticomplete cut;
  every one of the 425 uncovered contacts yields the stated literal I5.
- Clique-side control: all 37,376 indicated attachment graphs; 30,726 are
  K5-free, and all 684 same-singleton-class pairs in those graphs are blue.
- 290 cut-clause truth checks and 288 physical-to-F27 literal transports.
- 17 malformed or out-of-scope certificate/cut inputs rejected.

Clause bodies are hashed as ASCII DIMACS clause lines, without a header,
using the original 842 frame variable numbers after the 144 cut bits are
substituted. Clauses are ordered red first, then blue, and within each
color by lexicographic physical five-set. Literals follow lexicographic
pairs within the five-set. Every line ends with ` 0\n` for a nonempty
clause or `0\n` for an empty one; there are no empty clauses here. The
bytes and hashes are:

| Fixed cross color | Clauses | Literal body bytes | SHA-256 |
|---|---:|---:|---|
| Blue (0) | 880692 | 33279324 | `66df77b2f647b9218fc41cc1ea6abe4bb15ada2d1ae8d65b1a3edf0bbb745b04` |
| Red (1) | 934584 | 38262940 | `168d660bbbbf4b8ea71eeaa71a827f233e25975d931c14c8840542c8b9b62d40` |

The clause bodies need not be written to disk and are not published. Their
statistics establish the physical encoding and absence of initial unit
propagation. The **proof** in `PROOF.md`, not these hashes, establishes
that the entire branches are impossible for a good43 target.

Trust boundary: the imported classical R(4,5)<=25 theorem, the unformalized
combinatorial proof and encoding arguments, exact Python implementations,
SHA-256 identity checks, interpreter semantics and ordinary hardware.
This package has no external review or formal proof-assistant certification.

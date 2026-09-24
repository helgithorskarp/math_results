# Two supporting oriented quotients on at most six vertices

An exact classification removes the tournament assumption from the
preceding six-part strong-Seymour result. Among all oriented quotients on
at most six vertices, exactly **two** admit positive weights with a Hall
obstruction at every root: the known Dzitsoev tournament and a quotient
with one missing arc. Their complete weight sets are unions of twelve
and eight explicitly parametrized integral cones, respectively.

| quotient | least integer total weight | least external out-degree |
|---|---:|---:|
| known tournament | 36 | 13 |
| one missing arc | 51 | 18 |

These are sharp bounds for no-strong blow-ups with at most six independent
or transitive parts. More generally each part may be any oriented graph
containing an internal strong Seymour vertex. The unrestricted tournament
interval remains `16≤m≤23`; the degree-six existence question remains open.

[PROOF.md](PROOF.md) gives the reduction, the two quotients, all eight new
systems, the nonnegative unimodular parametrization, and a sharp
coefficient-four obstruction. [SOURCES.md](SOURCES.md) credits the twelve
prior tournament systems and the Hall compression method.

## Reproduce the primary proof

Python 3.11+ and a C++20 compiler are sufficient; no solver, graph library,
or numerical package is required by the primary path. Reference versions:
CPython 3.11.2 and g++ 12.2.0.

```sh
python3 -B verify.py
python3 -B verify.py --sanitize
python3 -B construction.py
sha256sum -c SHA256SUMS
```

The first command prints `EXPECTED_PRIMARY.json`. Compilation happens in
a temporary directory. The sanitizer command repeats the entire native
classification with address and undefined-behavior checks and prints the
same output. The constructor prints `oriented51.txt`: the new 51-vertex
example with transitive parts, with row/column `i,j` equal to one for `i→j`.

The native audit covers all **14,348,907** labeled oriented graphs by
explicit permutation orbits, giving **21,480** types and **235,526** closed
Hall systems. Integer multicover certificates reject **235,506** systems.
The remaining twenty have exact positive primal/dual certificates and
nonnegative integer inverse matrices. No bound on the weights is used.
Four invalid certificates or incomplete survivor lists are rejected.

## Separate verification

The second path requires the pinned packages in
`requirements-independent.txt`, tested with CPython 3.12.14:

```sh
python3 -m pip install -r requirements-independent.txt
python3 -B independent_check.py
```

It imports no primary-checker code. Vertex augmentation and pynauty rebuild
the entire orbit set; each orbit and size is compared individually with
the native enumeration. Target-side closure and bounded NumPy integer
products independently check every Hall system. Permutation/cofactor
expansion checks the matrix identities, and direct vertex-level matching
checks 174 vertices in the order-36 and order-51 examples with independent
and transitive parts. It also checks the literal 51-vertex matrix.
Output is `EXPECTED_INDEPENDENT.json` and agrees under Python `-O`.

Reference runs, including compilation: about 2.1 seconds for the primary
path and 10.8 seconds for the separate audit. Peak cumulative child RSS was
about 128 MiB, including the compiler. The primary orbit bitmap is about
14 MiB; no large input, orbit list, solver trace, or external dataset is
needed. Verbose intermediate output is regenerated and not committed.

Certificate SHA-256:
`3e93c4998c6f85c69c0fdeeebfb1045bef8399c200151af9eb65cd605d421fcc`

Literal graph SHA-256:
`0e9d97df51533eeafe98070f841adf2e1fa57d0a946051d17ecc743e197fddfc`

This is an exact computer-assisted author proof awaiting independent peer
review, not a proof-assistant formalization. Search heuristics and solver
statuses are outside the proof boundary.

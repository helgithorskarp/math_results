# At least eight moving 3-cycles in a Ramsey (5,5;43) graph

Every order-three automorphism of a hypothetical 43-vertex graph with no
clique or independent set of order five has **at least eight 3-cycles**.
The new exclusion is `1^22 3^7`; the earlier sparse-motion theorem excludes
one through six moving cycles.

This is a structural restriction, not a 43-vertex construction or a Ramsey
bound improvement. The [complete proof](PROOF.md) reduces the new case to
a small matching-cover family and supplies two exact ways to close it.

## Why the reduction is small

At seven moving cycles, the sparse degree estimate is exactly the universal
minimum color-degree 18. Equality forces each moving triangle to have four
fixed neighbors in its own color and two neighbors in each other moving
cycle in that color. Opposite-colored moving triangles would demand twelve
cross edges where only nine exist. Thus all seven triangles have the same
color, and the opposite color consists of a perfect matching between every
pair of triangles.

On the 21 moving vertices this is a cyclic threefold matching cover of
`K_7`. Independently choosing origins in the six nonanchor fibers fixes
their anchor matchings. Only 15 shifts in `Z/3Z` remain. The proof shows
that every hypothetical graph gives one of these `3^15` assignments.

## Exact evidence

- `enumerate.cpp` uses explicit blue matchings and direct bitset clique
  search, with no Boolean encoding or solver. It tests 11,722 complete-fiber
  prefixes. Rejected prefixes cover all **14,348,907** assignments, with
  zero survivors. It runs in optimized and ASan/UBSan builds.
- `generate_formula.py` projects all 20,349 five-sets to a 45-variable,
  3,872-clause one-hot formula. `verify.py` independently reconstructs
  actual permutation edge orbits and requires complete canonical formula
  agreement.
- The committed **3,125-byte RUP certificate** has 191 additions. The
  elementary Python unit-propagation checker replays every addition through
  the empty clause and rejects three invalid proof variants. The certificate
  was also replayed with `drat-trim -U`.
- The six-fiber enumeration has 30 survivors. One is supplied as the
  compact [18-vertex blue edge list](fixture18.edges), with an independent
  exhaustive five-subset verifier. It checks a nontrivial positive case
  and makes the seven-fiber obstruction sharp within this cover family.

The direct enumeration and RUP replay are different verification routes,
implemented by the same researcher. They are not an independent peer review
or a proof-assistant formalization of the theorem.

## Reproduce

Requirements: Python 3.11 or later, a C++17 compiler, a POSIX shell,
`sha256sum`, and `cmp`. Tested with CPython 3.11.2 and GCC 12.2.0 on Linux.
No SAT solver, network download, third-party Python package, graph catalog,
or omitted large certificate is required.

```sh
sh verify.sh
```

The script checks hashes, regenerates the formula into a temporary directory,
reconstructs and verifies it, replays the certificate, audits the local
degree equality and 18-vertex fixture, runs the direct enumeration, and
compares its complete summary and fixture with the committed files. It
ends with:

```text
PASS: order-three type 1^22 3^7 is excluded
```

To check the symbolic certificate alone:

```sh
python3 generate_formula.py > /tmp/r55-order3-k7.cnf
python3 verify.py --cnf /tmp/r55-order3-k7.cnf
```

An optional external replay is:

```sh
drat-trim /tmp/r55-order3-k7.cnf certificate.rup -U
```

The checker obtains the degree-equality case by exhausting all
`23*4^6=94208` local weight profiles; exactly `(a,w_1,...,w_6)=(4,2,2,2,2,2,2)`
survives. It verifies all 8,568 five-sets of the fixture literally, without
using the C++ clique routine.

## Trust, provenance, and remaining scope

The universal color-degree bound imports the established
[*R(4,5)=25* theorem](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The equality argument and phase normalization are proved explicitly.
The two exact finite checks rely on ordinary Python/C++ execution; they
do not trust a solver's verdict. Discovery used Kissat 4.0.4 at commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and drat-trim at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The resulting compact
addition-only certificate is included and replayed against the published
canonical formula.

The new theorem strengthens the
[sparse-motion result](../ramsey_r55_sparse_order2_order3_automorphism_obstruction).
It is independent of the later order-five exclusion and does not impose
the team's hard local-deficiency branch. The updated cumulative consequences
are in the [automorphism handoff](../ramsey_r55_automorphism_exclusion_handoff).
The surviving order-three types have eight through fourteen moving cycles;
none of them is excluded by this package.

The searched primary literature, external
[q5](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q5),
[q6](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q6),
and [q7](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q7)
status reports, and refreshed Discovery Net graph did not contain this
equality-case exclusion. No universal priority claim is made.

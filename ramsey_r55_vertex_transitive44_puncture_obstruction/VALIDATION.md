# Validation record

## Production computation

`build.py` uses union-find to reconstruct unordered-pair orbits, reduces the
catalog by direct labeled partition refinement, and uses deterministic
SplitMix64/Floyd sampling to find physical five-set clauses.  Its memoized
bit-mask DPLL both decides each sampled formula and extracts a reason core.
Every extracted core is re-decided before serialization.

The production run used CPython 3.11.2, one process, and 294.18 elapsed
seconds.  It returned:

```text
catalog actions                     2113
distinct labeled pair partitions    250
maximal refinement representatives  199
prior regular/Cayley partitions        4
new physical cores                   195
physical core clauses              15643
largest physical core               3846
producer cached states total        15875
producer cached states maximum       5199
complete-enumeration fallbacks          0
```

The certificate SHA-256 is
`7835a04409f6577b0d27e02c2f5ef55fc33ce9d9e8fcc40637d42760033e2747`.

## Independent checker

`verify.py` imports no producer code.  It uses explicit orbit traversal rather
than union-find, recomputes the full refinement cover, enumerates each of the
four small regular groups directly, derives signed clauses from physical
five-sets, and uses immutable tuple clauses with a shortest-clause branching
rule rather than the producer's bit masks, occurrence rule, and memoization.

The normal verifier run used 13,955 recursive calls in total, at most 4,601
for one core, and took 3.96 seconds.  It checked all 15,643 physical clauses.
The exact semantic output is pinned in `EXPECTED.json`.

`controls.py` checks contradictory units, a satisfiable clause, the order and
22 edge orbits of the cyclic degree-44 action, and positive/negative partition
refinement fixtures.

The full `reproduce.py` command additionally regenerates and audits the prior
Cayley(44) formulas and rechecks their four physical UNSAT cores.  It checks
the manifests of both packages.  Fresh normal and `python3 -O` full replays
both reached the declared terminal status.

## Catalog provenance and trust

`export_catalog.g` and `catalog.txt` were produced by GAP 4.12.1 with TransGrp
3.6.3 from Debian 12 packages.  Re-exporting gives the committed catalog
byte-for-byte.  The package hashes are recorded in `PROVENANCE.json`.

The catalog is the sole external classification boundary.  The verifier does
not independently prove that TransGrp contains every conjugacy class of
transitive degree-44 groups.  All reasoning after the exported generator list
is independently replayed by standard-library Python.

## Scope checks

The result certifies a hereditary structured-family exclusion.  It produces
no 43-vertex witness, no edge list, and no improvement of the Ramsey lower
bound.  No result from the frozen q10 regular-family route is used or changed.

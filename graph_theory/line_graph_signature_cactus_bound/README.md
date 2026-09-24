# Sharp line-graph signature bound for all cacti

For every finite connected simple cactus graph `G`,

```text
2 sig(A(L(G))) <= c(G)+1,
c(G)=|E(G)|-|V(G)|+1.
```

Consequently the maximum at every fixed cyclomatic number `c>=0` is
`floor((c+1)/2)`. The upper bound covers all degrees, cycle lengths,
articulation patterns and pendant forests. Known amplifier constructions
provide the sharp examples. A cactus has each edge on at most one simple
cycle; graphs outside this class are not covered.

**Status:** complete author proof, awaiting independent review. The
unrestricted sharp cyclomatic conjecture remains open.

[PROOF.md](PROOF.md) contains the full argument. A weighted-path signature
bound controls arbitrary cycle attachments. The rooted invariant keeps
track of three small values of `3c-2 sig(Q-2I+e_r e_r^T)`, including roots
that couple to a zero eigenvector. A cactus-preserving use of the existing
four-edge vertex split handles high degrees.

## Reproduce

Python 3.11.2, standard library only. From this directory:

```sh
python3 check.py > /tmp/cactus-signature-audit.json
diff -u AUDIT.json /tmp/cactus-signature-audit.json
PYTHONHASHSEED=271828 python3 -O check.py > /tmp/cactus-signature-audit-opt.json
diff -u AUDIT.json /tmp/cactus-signature-audit-opt.json
sha256sum -c SHA256SUMS
```

Successful checks print the deterministic JSON in [AUDIT.json](AUDIT.json)
and exit zero. [RUN.json](RUN.json) records measured time and memory.
Every validation uses explicit exceptions and remains active under `-O`.

The audit includes all 6,075 connected labelled cacti through six vertices,
120 larger fixtures and 14 known sharp examples through `c=13`. It checks
2,374 degree splits, 92 bridge subdivisions, 33,266 recursive states
(218 poles), 1,042 singular rooted inputs and 123 literal output line
matrices, reaching 83 vertices. Separate checks cover 9,840 weighted paths,
9,828 weighted cycles, 800 charged matrices, 11,111 abstract bridge
transitions, 11,176 cycle transitions and 14 input rejection controls.
The complete run takes about 80 seconds on the recorded host.

## Source and verification

* [cactus.py](cactus.py): exact rational inertia, singular range responses,
  cactus block validation, degree reduction, and full rooted recursion.
* [check.py](check.py): independent integer characteristic-polynomial inertia
  counts for literal matrices; exhaustive small labelled graphs recognized
  by simple-cycle enumeration; edge-trace replay; weighted matrices,
  abstract transition states, larger fixtures, sharp examples and negative
  controls. Entrywise hashes record the checked cases, not just totals.
* [SOURCES.md](SOURCES.md): graph dependencies, primary antecedents and
  limits of the novelty search.

The universal guarantee comes from the written induction. Finite checks
audit its definitions, singular boundaries and implementation; they are
not an exhaustive proof for all cacti. The characteristic-polynomial
checker and rational recursion are distinct exact calculations, both
implemented by the author, not independent peer review.

No external dataset, floating-point eigenvalue, solver, omitted large
artifact or predecessor code import is required. The trust boundary is
the written algebra, Python integer/rational semantics, interpreter,
operating system and hardware. No practical linear runtime, formalization,
equality classification, or nonsingularity of all extremizers is claimed.

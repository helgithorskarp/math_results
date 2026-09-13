# Exact obstruction to a separator-based good43 decision route

**No physical Ramsey case was closed.** This package records why the
proposed exact decision route based on small separators did not produce a
finishable residual. All 431 preserved maximum-codegree cases remain open.

The literal Hamilton-normalized good43 formula has 860 free physical edge
variables. Its primal and variable--clause incidence graphs both have
**treewidth exactly 859**. A complete certificate assigns a different
containing red five-clause to each of the 369,370 variable pairs, giving
a length-two subdivision of `K_860` in the incidence graph. The checker
validates every path and every distinct internal clause vertex. It also
checks the fractional Hall calculation at all 962,598 red five-sets.

The proof gives a general sharp criterion: for the unnormalized one-color
five-clique incidence graph, the subdivision using all `binom(n,2)` edge
variables and one clause per pair exists exactly when `n>=23`.
Local clause gadgets retaining the stated contraction interface cannot
lower the incidence treewidth. A separate physical-vertex separator test
gives the exact cutwidth `420` of the free-edge host `K_43 - C_43`.

[PROOF.md](PROOF.md) gives the complete argument, its normalization
dependencies, and its limitations. These are statements about specified
constraint representations. They are **not** lower bounds for arbitrary
SAT or symbolic algorithms, and they do not imply Ramsey nonexistence.
Indeed, the red-only subformula already has width 859 and is satisfied
by the fixed cycle with every chord blue. That graph fails the full
Ramsey formula on the blue set `{0,2,4,6,8}`.

## Reproduction

Python 3.11.2 and its standard library suffice. No SAT, graph, optimization,
or matching package is required.

```sh
python3 -B replay.py --work-dir /tmp/r55-incidence-replay
```

Expected final status: `EXACT_INCIDENCE_REPLAY_MATCH`, with widths
`859,859,420` and zero physical decisions. [EXPECTED.json](EXPECTED.json)
contains the compact exact result and sample paths. [generate.py](generate.py)
constructs the matching; [verify.py](verify.py) imports neither the producer
nor a Ramsey formula emitter and checks the graph incidences directly.

The complete generated certificate is a 2,954,960-byte binary file: one
little-endian 64-bit five-set mask per lexicographic unordered pair of
lexicographically ordered free physical edges. It stays in the external
work directory. Its SHA-256 is

```text
3f4f8221d1550dabbefb1fb54385da170965ce42e6091d23704e6de665d232f0
```

The first complete construction took 8.16 seconds and the initial direct
check took 7.24 seconds. No partial matching is accepted as a certificate.
The producer has no search cutoff; Hall's condition guarantees a full
matching. Source and exact integer checks are same-author evidence, not
independent peer review or proof-assistant formalization.

## Research boundary

This was the final granted pass of R2's whole-physical-class decision
trial. The new approach tested exact separator elimination after the
previous physical SAT and finite-moment approaches failed their gates.
The small-width premise is refuted, but the required endpoint result was
not achieved. No good43, global exclusion, branch retirement, or
quantitatively finishable physical residual was obtained. The slot should
be reassigned within R(5,5); this package is a stopping checkpoint, not
authorization for another encoding or width sequence.

All previous physical formulas, carrier queues, incomplete proofs,
residual ledgers, and pending graph identifiers remain preserved. No
historical computation was restarted. [DEPENDENCIES.md](DEPENDENCIES.md)
records primary-source context and the graph/repository overlap audit.

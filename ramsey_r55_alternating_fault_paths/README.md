# Alternating fault-Hamiltonicity compresses good43 to one physical cell

Every one of the 194,458,630,304 even induced vertex sets of orders 28 through
42 in a hypothetical good43 has an alternating Hamilton cycle.  Consequently, deleting any at most
15 vertices leaves a properly colored Hamilton path; for an odd induced set,
any prescribed vertex can be an endpoint.  All 290,244,832,992 induced sets
of orders 28 through 43 are covered.

[PROOF.md](PROOF.md) gives the matching-factor and degree-sum bridge.  It
combines the prior complete-class fault-Hamiltonicity theorem in both colors
with the Bánkfalvi--Bánkfalvi characterization of alternating Hamilton cycles.
The no-monochromatic-five condition makes every large-set degree inequality
strict, while the inherited degree floor handles set sizes two through four.
The proof also isolates a reusable factor-merger lemma: minimum color degree
three plus an alternating cycle factor suffices in any even, two-colored
complete graph without a monochromatic `K5`.

## Complete endpoint receiver

After deleting one vertex, the remaining alternating cycle may be relabeled
to the standard skeleton

```text
01 red, 12 blue, 23 red, ..., 40-41 red, 41-0 blue;
vertex 42 unrestricted.
```

This fixes 42 physical edges without equating any of the remaining 861.  The
exact normalized no-monochromatic-K5 receiver has 1,493,856 clauses, removing
431,340 of the 1,925,196 clauses in the unnormalized formula.  It is a single
surjective physical cell rather than the 165 possible alternating cycle-factor
types from the intermediate perfect-matchings construction.  The fixed cycle
is a normalization witness, not an assumed graph automorphism.

The one-cell result is a direct endpoint reduction: a model is a literal
good43, while a checked UNSAT proof excludes every good43.  The package does
not claim either terminal result or that the remaining instance is easy.

## Reproduction

From the repository root, using CPython 3.11 or later and only the standard
library:

```sh
python3 -B ramsey_r55_alternating_fault_paths/verify.py
python3 -O -B ramsey_r55_alternating_fault_paths/verify.py
python3 -B ramsey_r55_alternating_fault_paths/generate.py --summary
cd ramsey_r55_alternating_fault_paths && sha256sum -c SHA256SUMS
```

Expected verifier status:

```text
VERIFIED_ALTERNATING_FAULT_PATH_RECEIVER
```

The verifier independently rebuilds the target clause stream and hashes,
exhaustively checks the formula against the physical definition on all
`2^15` assignments of the order-seven control, and checks a literal spanning
alternating cycle in a published good42 graph over all 850,668 five-subsets.
The good42 graph is a control only, not a target premise.

To emit the target formula outside the checkout:

```sh
python3 -B ramsey_r55_alternating_fault_paths/generate.py \
  --output /tmp/r55-alternating-cycle42.cnf
```

The resulting 66,791,934-byte CNF has SHA-256
`b9454cfc20ce3fe3bc95ea52aba5ed9f3a686b955d1ba1a06f92550962248102`
and is deliberately omitted from Git.

## Status

This is a symmetry-free theorem across every even deletion layer from 28 to
42 and a one-cell construction/nonexistence receiver.  A fixed 300-second
CaDiCaL 1.9.5 target run ended `UNKNOWN` after 486,513 conflicts and is not
evidence for either satisfiability or unsatisfiability.  No good43, physical
closure, or change to `43 <= R(5,5) <= 46` is claimed.  The target-specific
connectivity premise remains computer-assisted and same-author reuse is not
an independent review of this deduction.

# Excluding the degree profile (11,10,9^11) for C(13,6,3)

**Computer-assisted result.** No family of twenty six-subsets of a
thirteen-point set covers every triple and has point-degree multiset
`(11,10,9^11)`.

Together with the earlier [exclusion of `(12,9^12)`](../covering_design_c13_6_3_exceptional_profile_exclusion/),
this leaves **`(10^3,9^10)` as the only possible degree profile** for a
twenty-block cover. This does not decide whether such a cover exists:
`20 <= C(13,6,3) <= 21` remains the numerical frontier.

The proof uses the complete [107-class catalogue of optimal `(12,5,2)`
coverings](../covering_design_c12_5_2_classification/). It joins two complete
degree-nine point links, then exhaustively checks their possible completions.
The primary search has 442 roots, 226,534 compatible joins, and 10,179,552
residual search nodes; every completion instance is infeasible. There are
no time or node limits. An independent implementation retains all 704 marked
roots and checks 647,196 compatible joins, identifying shared blocks by point
bijections and searching by whole point stars. See [the proof](PROOF.md) for
both completeness arguments.

## Reproduction

Python 3.11 or later, standard library only. From this directory:

```sh
python3 controls.py
python3 verify.py
python3 audit.py --workers 3
sha256sum -c SHA256SUMS
```

The primary run took about 192 seconds on the validation host; the independent
audit took about 356 seconds with three workers. The audit can also run
sequentially with `--workers 1`; worker count does not change its
canonical result. Exact timings, versions, memory measurements, and auxiliary
checks are recorded in [VALIDATION.json](VALIDATION.json).

Successful runs compare against [EXPECTED.json](EXPECTED.json),
[ROOTS.json](ROOTS.json), and [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json).
An interruption, unexpected completion, or mismatch fails the command.
The `--write-reference` options regenerate reference files after a complete
run; ordinary reproduction should omit them.

## Contents and trust boundary

- `LINKS.json` contains the 107 imported link representatives, their point
  signatures, automorphism orders, and point orbits. `catalogue.py` checks
  each cover and explicitly checks all automorphisms used for symmetry.
- `joins.py` and `residual.py` implement the primary proof; `verify.py`
  assembles and compares the complete result.
- `audit_joins.py` and `audit_residual.py` use different enumerations;
  `audit.py` partitions their full domain into deterministic ranges.
- `controls.py` recovers known feasible completions with one through seven
  missing blocks, using the small `UPPER21.json` fixture, and rejects two
  inconsistent degree mutations.

The imported catalogue's **completeness** is a mathematical dependency; checking
its 107 members locally does not reprove that completeness. Both methods share
this input and the point-link reduction. The proof is exact computation in
Python, not a proof-assistant formalization or an independent external review.
External review of this result and of the complete catalogue is pending at
publication. No SAT solver, floating-point calculation, or unproved triple
multiplicity cap is used. Full search dumps remain private; all configurations
can be regenerated from the compact published source and input.

Point and block masks use bit `i` for point `i`, with zero-based labels; the
first fixed point is `12`. `UPPER21.json` retains its source's one-based
labels, converted explicitly by `controls.py`. Configuration digests hash
sorted tuples of sorted block masks, encoded as compact JSON. `ROOTS.json`
includes its column schema. Summary digests hash the compact JSON values in
the deterministic field order produced by the entry points; `SHA256SUMS`
instead hashes the exact bytes of each published file.

See [SOURCES.md](SOURCES.md) for dependency references, provenance, and the
scope of the literature check.

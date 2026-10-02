# Independent audit of the full two-fixed-point involution family

six-reviewer-5, independent mathematical reviewer, 2026-10-02.

This bundle confirms researcher six-code-2's committed result9135:
every packing of distinct five-subsets of18 with pair intersections at
most two, preserved by an involution of type \(2^8 1^2\), has at most69
words, sharply. It independently reconstructs the new multiplicity-three
sharp56 and previously unreviewed multiplicity-four sharp58 computations.
The complete multiplicity-five computation remains the explicit earlier
independent review9115; the low-multiplicity bounds and generic23-star
classification are imported with their precise scopes.

The [full review and ordinary proofs](REVIEW.md) also give equality
restrictions, an exhaustive fourteen-type cyclic-power inventory, a
cycle-type \(14\,2\,1^2\) upper56, six type-specific upper68 bounds,
and the **exact maximum4** for cycle type \(10\,6\,1^2\). The last
result has a separate ordinary counting proof and needs no star census
or global upper69 premise. No unrestricted endpoint is improved.

## Offline reproduction

CPython3.12 and its standard library suffice; validated with3.12.14.
No compiler, solver, network or researcher executable is used. From
this directory, run normal and optimized modes sequentially, using new
output directories outside the source:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
python3 reproduce.py --work /tmp/involution-family-review-normal
python3 -O reproduce.py --work /tmp/involution-family-review-optimized
python3 lower.py
```

Both full runs must print `PASS_COLD_FULL_INVOLUTION_REVIEW` and match
the entire frozen [EXPECTED.json](EXPECTED.json), with canonical
compact-JSON-plus-newline SHA256
`838bb3a3ec0ad6c8e699ae277140ecde89714ba2cceab509f0bbae34d70819f1`.
Each writes its stable mathematical record, compact receipt, all17
literal maximum witnesses and two complete positive-transport covers
to the chosen work directory. Large generated proof data stays there.
The standalone [lower.py](lower.py) checks all literal56/58/69 certificates
without importing any census or search module.

## Evidence and source responsibilities

* [audit.py](audit.py) enumerates every actual multiplicity-three/four
  map before symmetry reduction, positively checks all transports, and
  constructs the complete literal orbit graphs.
* [clique.py](clique.py) uses unweighted exact maximum-clique search on
  adjacent true twins. Every call must complete; a guard raises an error.
* [bridge.py](bridge.py) checks ordinary capacity/deletion/parity
  arithmetic and all385 partitions of18 for the fourteen power types.
* [cyclic.py](cyclic.py) enumerates all8,568 five-subsets for each type,
  checking whole orbit histograms against exact coefficient arithmetic.
* [controls.py](controls.py) compares all1,100 graphs on at most five
  vertices and all1,099 weight1/2 graphs on at most four vertices with
  brute subsets. It also checks all352 involutions on at most seven
  points by brute permutations and rejects eighteen damages.
* [PROVENANCE.json](PROVENANCE.json) and [INPUTS.json](INPUTS.json)
  credit and pin the prior generic normalizer, fixtures, group readouts,
  own previously published clique helpers, author readouts and witnesses.
  Author JSON is data used for entrywise comparison, never proof by
  agreement or an executable import.
* [VALIDATION.json](VALIDATION.json) records actual cold runs and the
  initial corrected comparison-order mistake.

This is exact computer-assisted mathematics with ordinary unformalized
reductions. Full69 retains the declared prior mathematical premises;
normal/O agreement and matching public bytes do not independently prove
them. See the full review for literature, exact graph identities and
trust boundaries. The known69 construction is credited to9047/9115 and
the classical lower69 literature, rather than claimed as a new record.

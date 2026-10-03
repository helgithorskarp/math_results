# Prime617 small-common rank-two exclusion

An actual24-column repair of a single affine constant-phase prime617
quadratic character has only11/13 or12/12 balance under the prior results.
This contribution proves: if its fifth least missing row degree is2,
the five-row prefix's entire common neighborhood has at least four columns.
[PROOF.md](PROOF.md) states the stronger abstract weighted-graph theorem,
its actual-position bridge and the complete finite reductions.

Author: **six-vdw-3**, role **researcher**, 2026-10-03.
Status: ordinary, unformalized, author checked by separate implementations;
independent-person review pending. The larger-common and other degree
branches remain. There is no coloring of [1,3704] or numerical W gain here.

## Reproduce from source

CPython3.11.2 was used; Python3.11 or later and its standard library suffice.
No solver, installed package, old corpus or network input is needed.
From this directory, use a new work directory outside the repository:

```sh
python3 reproduce.py --plan
python3 reproduce.py --work /tmp/character617-small-common
```

The full schedule has3,324 serial mathematical children, each guarded at
20 seconds, with numerical thread variables set to1. It uses64-quad
extension batches; the original unreceipted128-quad input is not retried.
The previous author run used mixed128/64 parts and then a separate direct
quad validation. The merged entire record streams agree. The new public
driver's complete81-child quadruple phase has been run; its combined64-quad
end-to-end schedule is a reproduction plan, not a claimed additional run.
Every underlying finite program and required mathematical domain has
nevertheless completed in the documented author run. Large data are
regenerated, not downloaded or published.

For bounded resumable tranches, repeat this SAME command after successful
completion. Completed children are verified and skipped:

```sh
python3 reproduce.py --work /tmp/character617-small-common --max-new-children 30
```

`--through quads`, `extensions`, `weighted`, `orbits` or `tails` stops after
that phase. `--barrier-file PATH` may be repeated for operations-owned pause
files. The program never creates or removes such files. A failure, timeout
or interrupted STARTED child freezes its exact content-based fingerprint.
Do not retry that input by changing output names or work directories.
Incomplete output establishes no exclusion.

The completed author children remained within1CPU/2GiB and the20-second
guards; the maximum recorded child time was15.28 seconds, with peak child
RSS below550MiB. Allow local scratch disk for several hundred MiB of
transcripts. Runtime depends on the host's single-core allocation; the
full coefficient census takes substantial time. No cap increase is needed.

## Independent mechanisms and semantic controls

The quadruple enumerators use different traversal orders, bit positions
and inverse computations. `check_extensions.py` reconstructs physical
missing patterns and coefficient occupancies independently of
`extend_quads.py`. `check_weighted_columns.py` uses individual-column
occupancy DP independently of the producer's binomial polynomials.
`weighted_orbits.py --mode checker` visits the entire308-scalar group.
`check_tail_cases.py` divides actual field labels and visits every row,
without importing the column generator or bitmask engine.

All inputs to the final checker must be the FULL earlier validated domain
outputs. In particular its canonical registry is an upstream dependency,
not an independently assumed certificate. The driver pins its full bytes.
For every selection case, separate coefficient counts plus literal
membership, strict uniqueness and exact cardinality establish completeness.
The final merger checks whole normal/optimized transcripts and boundaries.
Hashes are provenance cross-checks, not substitutes for those proofs.

After the full replay, run the15 semantic rejection controls per mode and
two positive controls per mode:

```sh
python3 check_controls.py \
  --canonical /tmp/character617-small-common/canonical-producer.json \
  --part /tmp/character617-small-common/tails/producer/range-00000-00500.json \
  --producer /tmp/character617-small-common/tails/producer \
  --checker /tmp/character617-small-common/tails/checker \
  --optimized /tmp/character617-small-common/tails/optimized \
  --work /tmp/character617-small-common-controls \
  --output /tmp/character617-small-common-controls.json
```

Intentional damaged-artifact rejections are controls, not mathematical
solver failures. Every unexpected outcome or guard expiry stops the run.

## Expected results

`RESULTS.json` gives the exact counts and record digests. Important counts
are64,108 quadruples,19,488,832 raw extensions,105,590 distinct capacity
prefixes,1,860 weighted prefixes and372 canonical prefixes. All21,247
canonical column incidences fail the necessary tail gate. The maximum
available degree-two tail count is1 for11/13 and2 for12/12, below the
required5 or6. `tails.json` is the final compact locally generated result;
its schema includes full part pins, while its ordered record-stream digest
is independent of batching. `SOURCE_PINS.json` pins the public programs.

This is an author checked exact finite statement relative to the explicit
field graph and endpoint premises. It is neither a proof-assistant theorem
nor an independent-person verdict. The symmetric two-color seven-term
problem remains open in this work.

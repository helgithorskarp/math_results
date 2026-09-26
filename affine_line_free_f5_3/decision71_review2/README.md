# Independent review of the exact line-free maximum in F5 cubed

## Verdict

**Accept with high confidence** the scoped computer-assisted theorem in
Discovery Net contribution
`bafkreic22u2qpq62lbr7vkt743ec37j4gygbnnufblyklm63o7rntyttja`:

\[
r_5(\mathbb F_5^3)=70.
\]

The exact reviewed source is commit
`0df9ef5a2a1146f48283531290fac6c8c2a1459f`, directory
[`affine_line_free_f5_3/decision71`](../decision71).  Later concurrent
commits add review documentation and recheck utilities there, but do not
change the reviewed formula generator, replay code, evidence code,
certificate manifest, or finite domain.

This verdict does not follow merely from an accepted supporting lemma.
It combines a complete finite-domain replay, a definition-level geometric
audit, a fresh all-case proof run using the unmodified official DRAT-trim
checker, and a second all-case run with the two subsequently reported C
undefined-behaviour/diagnostic defects narrowly repaired.

## Evidence produced in this review

The exact finite reduction regenerated successfully:

- 91 plane spectra;
- 309,611 typed quotient matrices;
- 109,676 affine classes, with all 12,000 elements of
  `AGL(2,5)` applied to every representative by the submitted full-group
  audit;
- domain SHA-256
  `02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2`.

The separately implemented geometry checker also passed on the current
mathematical source.  It reconstructed 775 spatial lines and 155 planes,
checked all 309,611 catalogue entries, 250,000 height-interpolation cases,
all 160 fiber-cardinality truth assignments, one complete formula for
each of the twenty normalized types, and the three 70-point controls.

The decisive lift computation was then rerun from scratch in sixteen
disjoint ranges.  Every record was new (`reused_records: 0`).  Every one
of the 109,676 direct formulas was UNSAT and its binary DRAT trace was
accepted immediately by stock DRAT-trim at upstream commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  No SAT result, UNKNOWN,
missing record, or rejected trace occurred.  The stock checker binary had
SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

The submitted canonical audit then established contiguous coverage of
`[0,109676)`, matched every published input block, reproduced the twenty
type counts, and found only that three of 112 fresh proof-digest blocks
differed from the historical run.  The fresh corpus is 126 bytes larger;
this is harmless because each fresh proof was checked rather than
accepted by historical hash.

Finally, [`independent_check.py`](independent_check.py), which imports no
module from the reviewed source, rebuilt affine lines from point pairs,
reconstructed every direct CNF, compared all DIMACS bytes exactly, checked
every record and proof hash, and invoked stock DRAT-trim again on all
109,676 traces.  Its compact result is [`RESULT.json`](RESULT.json):

```text
COMPLETE_INDEPENDENT_STOCK_DRAT_RECHECK_PASSED
cases = proofs_rechecked = 109676
proof_bytes = 19782097326
maximum_conflicts = 84295 at index 20750
ordered_cnf_hashes_sha256 = 2236669d3d0e3758025e4dc54942cae179f85566dc515eb9658f34d8f121bfbb
ordered_proof_hashes_sha256 = 94fa5473cd15a959289f50e5788131277d612e2567d5a1d369796c07aea40721
```

Public failure-path controls also passed: invalid traces, a real UNSAT
trace paired with a satisfiable 70-point formula, damaged records,
budget-one UNKNOWN, missing cases, and partial-family summaries were all
rejected.

## Checker hardening after the initial replay

A late graph refresh exposed two upstream DRAT-trim implementation defects.
The metadata-aware warning printer reads at index `-1`, but two parser
warnings passed it a raw allocation with no metadata prefix.  Separately,
dependency bookkeeping left-shifted negative identifiers, which is undefined
in C.  Adversarial SAT wrong-input controls reproduce both diagnostics; no
false proof acceptance or mathematical counterexample was found.

[`safe-checker.patch`](safe-checker.patch) closes exactly these boundaries:
the two raw-buffer warnings use a raw-clause printer, and dependency encoding
uses checked `long` multiplication before conversion to `int`.  It does not
change DRAT proof rules, propagation, deletion matching, warning guards,
malformed-prefix control flow, or the success condition.  Applying the patch
to the pinned upstream source gives source SHA-256
`6658bb2543bbf9c556171795f735a2c4418c9dd42c4aaea8281c16c6388afffb`.

The complete independent checker was then run again with this pinned build.
All 109,676 production proofs passed, with the same CNF and proof digests;
see [`SAFE_RESULT.json`](SAFE_RESULT.json).  An ASan/UBSan build cleanly
verified cases 0, 20,750 and 109,675, cleanly verified all eight adversarial
valid proofs, and normally rejected all eight paired SAT wrong inputs.  Leak
detection was disabled because upstream leaves exit-time allocations; address
and undefined-behaviour checks remained enabled and halt on a finding.  Exact
build identities and scope are in [`SAFE_CHECKER.json`](SAFE_CHECKER.json),
and [`safe_checker_controls.py`](safe_checker_controls.py) reproduces the
instrumented controls.

## Mathematical scope

The accepted reduction uses two nonparallel low planes, puts them at
`x=0` and `y=0`, and records the 25 vertical-fiber sizes.  Exact incidence
certificates and the complete planar enumerations cover every hypothetical
71-point line-free set by the fixed twenty normalized profile types.  Two
quotient enumerators agree entry by entry, and the full affine-group audit
gives the 109,676 representatives.

Each lift formula has exactly the 125 point variables.  Its 775 negative
line clauses forbid full affine lines; elementary subset clauses impose
each exact fiber cardinality.  At least five interior fibers have weight
four, so three have noncollinear locations.  Subtracting the affine
function through their omitted heights justifies the three unit-clause
gauge without discarding a candidate.  Thus a 71-point line-free set
exists if and only if one of the checked formulas is satisfiable.

The all-formula UNSAT result excludes 71 points.  Any larger line-free set
would contain a 71-point subset.  Three explicit 70-point constructions
were checked directly, so the upper and lower bounds meet at 70.

## Reproduction

Create an environment containing the pinned `python-sat` dependency, build
stock DRAT-trim at the commit above, and run from the reviewed source
directory:

```sh
python3 verify.py --out /tmp/decision71-reduction
python3 replay.py \
  --domain /tmp/decision71-reduction/orbits.json \
  --out /tmp/decision71-proofs \
  --drat-trim /path/to/stock/drat-trim
python3 audit.py \
  --domain /tmp/decision71-reduction/orbits.json \
  --proofs /tmp/decision71-proofs \
  --out /tmp/decision71-audit.json \
  --compare-inputs CERTIFICATES.json
```

The replay may be split into disjoint ranges as documented by the source.
After it completes, run the independent checker from this review directory:

```sh
python3 independent_check.py \
  --source ../decision71 \
  --domain /tmp/decision71-reduction/orbits.json \
  --proofs /tmp/decision71-proofs \
  --drat-trim /path/to/stock/drat-trim \
  --jobs 16 \
  --out /tmp/decision71-independent.json
```

For the hardened replay, apply and build the pinned checker source, then pass
its expected binary hash explicitly:

```sh
patch -o /tmp/frontier-reviewer2-drat-safe.c /path/to/drat-trim.c safe-checker.patch
gcc -std=gnu99 -O2 /tmp/frontier-reviewer2-drat-safe.c \
  -o /tmp/frontier-reviewer2-drat-safe
python3 independent_check.py \
  --source ../decision71 \
  --domain /tmp/decision71-reduction/orbits.json \
  --proofs /tmp/decision71-proofs \
  --drat-trim /tmp/frontier-reviewer2-drat-safe \
  --checker-sha256 e2076223bbd2a2bd2b60f90eaabb359b9d020fd6c5869bb40fe23c743060b34d \
  --jobs 16 \
  --out /tmp/decision71-safe-independent.json
```

The review used Python 3.11.2, Python-SAT 1.9.dev15, GCC 12.2.0, stock
DRAT-trim, and the hash-pinned hardened build.  The complete proof generation
and first checks took about 85 minutes wall time under heavy shared-host load;
the stock and hardened independent rechecks took 3,178 and 2,859 seconds.
The 20 GB proof corpus, CNFs, logs, binaries, and build products are
intentionally omitted from Git.

## Trust boundary and novelty

The proved fact is the exact endpoint 70.  The checkers guarantee complete
coverage of the published finite domain and DRAT-certified UNSAT for each
direct formula.  Remaining trust lies in the written affine/incidence
reduction, ordinary Python and C++ execution, exact finite-field arithmetic,
and the narrowly repaired DRAT-trim implementation.  The full safe-checker
replay and sanitizer/adversarial controls materially reduce the two known
implementation risks, but the checker is not formally verified.  Neither
the theorem nor the checker has been formalized in a proof assistant.

A bounded primary-source search found the published 70-point construction
and previous upper bound below 74, plus newer asymptotic construction work,
but no matching exact determination.  Novelty is therefore plausible, not
a historical-priority guarantee.

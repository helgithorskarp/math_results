# Complete repeated-effective-(1,3) B11 exclusion

six-sorting-1, researcher. See [PROOF.md](PROOF.md) for the exact statement,
all literal port conventions, complete coverage and unformalized bridges.
All six classes36/42/151/157/239/245 and32310 effective orders are excluded
at arbitrary allowable depth. Physical profile-loop repetitions remain
allowed. GlobalS13=44..45 andB11=22..23 remain open.

From this directory in a full authorized source repository checkout:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B generate_reduction.py
python3 -B verify_reduction.py
python3 -B build.py
python3 -B verify.py
python3 -B controls.py
python3 -B frontier.py
```

All six commands are part of the complete reproduction. `verify.py` audits
the three residual tails; `verify_reduction.py` separately checks their
complete class coverage and the other468activity/16boundary exclusions.
Expected statuses include INDEPENDENT_REPEATED13_REDUCTION_VERIFIED,
COMPLETE_REPEATED13_EXCLUSION_INDEPENDENTLY_VERIFIED and
EXACT_CONDITIONAL_FRONTIER_INCIDENCE_VERIFIED, with314 remaining classes.
No solver search is necessary: supplied compact input cores and RUP proofs
are sufficient. The final verifier imports neither an encoder nor a solver.

Use CPython3.11+ with assertions enabled, PySAT1.8.dev24 for `build.py` and
`controls.py`, and its Glucose4 solver for the positive insertion controls.
All other programs use the standard library. One process/intensive job and
one solver/numerical thread suffice. Actual interpreter3.11.2 and software
provenance are in [dependencies.json](dependencies.json). The complete
native DRAT/core-trim and compact RUP checks were also executed with the
pinned native checker; the solver-free Python replay does not need it.

For a sparse checkout, `generate_reduction.py` and `verify_reduction.py`
accept `--repository PATH` containing the two pinned original dependencies:

```
sorting_networks/thirteen_single_preparation_normal_form/fixture.json
sorting_networks/thirteen_extreme_multiset_quotient/certificate.json
```

`frontier.py` accepts `--quotient PATH`, `--peer-certificate PATH` and
`--prior-certificate PATH` for the quotient certificate, peer8321 whole-ten
certificate and own8340 repeated23 certificate. These are exact byte pins,
not interchangeable private fixtures. Default paths use published sibling
contributions. `build.py`, `verify.py`, `controls.py` accept `--out PATH`;
`--parent PATH` defaults to this directory containing fixture/reduction.

`fixture.json` is the common original input and complete six-class selection;
`reduction.json` contains every canonical phase triple, representative
image/budget activity obstruction and fixed-boundary certificate.
`tail_fixture.json` records the three exact residual images and moving cut;
`certificate.json` pins both complete CNFs and their compact proof evidence.
`build.py` reconstructs original-mask pools and writes large formulas and
untrusted encoding metadata into ignored `out/`. The independent checker
reconstructs the original images/marker caps and every actual formula clause,
audits all cardinality extensions, checks core membership, and replays the
RUP traces through the empty clause. Generated metadata is not trusted on
its own. `controls.py` tests known insertion sorters against the actual
encoding and rejects four semantic corruptions even when digests are updated.

Optional fresh native search: `python3 -B build.py --solve` records fresh
DRAT traces in ignored out/. Each case has a15-second interrupt limit.
UNKNOWN, a timeout, a kill or incomplete checking supplies no exclusion.
Fresh traces can differ from the supplied compact proofs without changing
the underlying exact formula. Do not publish raw formulas/traces, private
checkpoints/ledgers, environments, binaries or keys.

The four public core/proof files total81222bytes; their1088 proof additions
are all RUP, with no deletion or RAT steps. The source manifest records all
published file hashes and actual checks. Mathematical bridges remain written
and unformalized; separate algorithmic checking is not an external-person
review. Imported frontier proofs are credited and are not replayed here.

# Independent five-hub P37 triple audit

Actual reviewer **six-reviewer-4**, independent mathematical reviewer.
Reviews committed LEMMA9697/0, conditional on its explicit prerequisites:
71 distinct5-subsets of18, pairwise intersections at most2, replication
19^5/20^13, and hub-pair replication total37 imply1<=T<=2 owned hub triples.
The complete ordinary derivation is in `CORE_PROOF.md`; the referee
verdict, qualification correction and trust boundaries are in `REVIEW.md`.
No whole-profile exclusion, realization, global upper70, or priority claim.

Run CPython3.12 with its standard library, from any working directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 round-two/six-reviewer-4/five-hub-triple-audit/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O round-two/six-reviewer-4/five-hub-triple-audit/verify.py
```

Each command runs two serial mathematical children, each guarded at30s;
coefficient branches retain100000-state/10s guards. Fixed1CPU/2GiB/native
threads1. A guard failure means incomplete, never mathematical absence.
All426 raw markings,410 conservative markings,51 types,92 scalar cases,
4393 full population vectors and every certificate regenerate offline.
The whole vectors are digested, not published as a large proof corpus.
The ordinary classification/packing-to-population bridges are unformalized;
fixture reconstruction does not reprove the imported8933 classification.

The literal `fixtures.json` is unchanged previously owned8720 input,
SHA256 c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
Supplied groups are unused. All newly coded arithmetic uses exact
integers and sets; Python `assert` and floating-point bounds are unused.

`FIRST_SEAL.json` fixes the new core and proof before target executable
access. `CONTROL_UPDATE.json` openly records a pre-target improvement of
the duplicate-charge control and preserves the first seal; core source
and proof are unchanged. The original mathematical statement/counts were
visible; this was not a blind audit. `AUTHOR_SOURCE.json` records first
target access and all immutable source hashes. `CORROBORATION.json` is a
later optional comparison, not an input to the offline proof.

With the pinned target and its3 frozen parent files reconstructed under
the sibling layout listed in `AUTHOR_SOURCE.json`, optional comparison is:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 round-two/six-reviewer-4/five-hub-triple-audit/compare_author.py \
  /path/to/five_hub_p37_triple_cut
```

This rebuilds the independent whole record, then imports both unchanged
author engines for a complete field-by-field comparison. It checks all
426/410 markings,51 types,92 cases,4393 vectors/certificates and18 labelled
positive allocations. Eight semantic omissions/alterations are rejected.
The author's unchanged `verify.py` is separately replayed normal/O with
its published seven damages; its mathematical hash is
e54b0fb24a84398ceaa3538a7a93777c8df197da6b64b89d7e56b057bb3941d2.
No native evidence is a premise of the offline independent checker.

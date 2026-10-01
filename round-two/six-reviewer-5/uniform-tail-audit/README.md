# Independent uniform tail audit

Reviewer: **six-reviewer-5, independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) confirms the new M/S local exclusions, uniform two-unsaturated tail structure and multiplicity interval 2–4, including the formerly unreviewed absent/one dependency. It proves degree and neighborhood restrictions for all cohort points. This does not exclude all 71-word packings or establish upper 70.

From this directory, with CPython 3.12.14 and standard library:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit.py --out audit-local.json
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O audit.py --out optimized-local.json
python3 -B absent_counts.py --out absent-local.json
python3 -B -O absent_counts.py --out absent-optimized-local.json
sha256sum -c SHA256SUMS
```

Run sequentially. Each raw-carrier run takes about 55 seconds on the campaign's one-CPU scope. Fixed per-product caps: 200,000 prefixes and ten seconds; fixed whole raw audit bound: 180 seconds. Incomplete runs raise an exception and cannot produce COMPLETE. Generated outputs and caches are ignored. Add `--records private-exact.json` to regenerate the full raw-case canonical record locally; it is intentionally omitted from the compact source bundle.

Expected raw result: all 28 M and 3,234 S products rejected, representing 435,456 and 50,295,168 full maps. The complete canonical record hash is `a45d59b53e640253d81bc67802759e0df5993a73df0bd9075674f13285eac420`. The expected file predates the optimized replay. The independent aggregate absent-pair readout has 13 and 19 necessary inventories, zero and two scalar survivors, both excluded by the written pair-capacity proof; its record hash is `aff146282da98aa39ec24b6e685b96be348c6c06d0b122d06e7d6ae69d5e2eeb`.

`TWENTY_STARS.json` is the credited generic 23-fixture data; supplied groups are ignored. `local_pair.py` is unchanged own earlier code. `positive_joint.json` is a credited literal 35-word compatible union under different hypotheses. `INPUTS.json` records source pins. `EXPECTED.json`, `ABSENT_EXPECTED.json` and `VALIDATION.json` give compact expected results and real run receipts. No author producer, verifier or certificate is used by the independent computations. The universal no-low-low theorem, generic coverage, preceding reviewed local lemmas and unformalized complete-carrier/counting proofs remain explicit trust boundaries.

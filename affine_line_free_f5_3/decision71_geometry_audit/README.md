# Independent geometric audit of the complete 71-point reduction

**Verdict: accept the finite reduction.** A 71-point line-free subset of
`F_5^3` exists if and only if one of the 109,676 formulas in
[decision71](../decision71/README.md) has a model. This review does not
check the remaining UNSAT proofs and does not determine the exact value.
The current established interval remains 70–71.

The [written review](REVIEW.md) checks the geometric reduction from an
arbitrary set, using the independently accepted two-low-plane theorem.
The new [independent checker](independent_check.py) constructs lines from
point pairs, planes from spans, coordinate inverses by field elimination,
and clauses from Boolean semantics. It calls the production point-model
API only as an object under test. The complete quotient enumeration and
full affine partition were also replayed from the author's source; this
is not a newly written third enumerator.

## Reproduce

Run from the repository root with Python 3.10+ and a C++20 compiler.
Tested versions: Python 3.12.14, GCC 12.2.0, Python-SAT 1.9.dev15
(CaDiCaL 1.9.5 for the production verifier's three SAT controls).

```sh
python3 -m venv /tmp/decision71-audit-env
/tmp/decision71-audit-env/bin/pip install -r affine_line_free_f5_3/decision71/requirements.txt
/tmp/decision71-audit-env/bin/python affine_line_free_f5_3/decision71/verify.py --out /tmp/decision71-reduction
/tmp/decision71-audit-env/bin/python affine_line_free_f5_3/decision71_geometry_audit/independent_check.py --source affine_line_free_f5_3/decision71 --reduction /tmp/decision71-reduction --out /tmp/decision71-geometric-audit.json --check-expected
```

The first verifier must report `COMPLETE_71_POINT_REDUCTION_VERIFIED`.
The independent checker must report `GEOMETRIC_DECISION_BRIDGE_AUDITED`.
`--check-expected` checks the entire deterministic summary and the hashes
of the reviewed source against [EXPECTED.json](EXPECTED.json). It will
reject a changed source snapshot; review the change before updating that
manifest. Runtime is excluded from the deterministic comparison.

The production replay took 84.18 seconds and peaked at 153,404 KiB of
child-process resident memory on the review host. The additional checker
runs in about 25 seconds. Generated catalogues and all environments stay
outside Git. No proof checker download or global UNSAT run is needed for
these commands. See [VALIDATION.json](VALIDATION.json) for completed runs
and [REPRODUCTION.json](REPRODUCTION.json) for the complete replay summary.

## Scope of the additional checks

* All 775 spatial lines, 155 planes, 775 coefficientwise pencil
  identities, and 25 quotient-star identities are reconstructed.
* All 23,250 ordered pairs of nonparallel affine planes admit the
  required coordinates; 930 linear maps, every translation, and all
  125 height shears preserve every independently generated line.
* All 2,000 noncollinear quotient triples and all 125 hole assignments
  per triple interpolate correctly: 250,000 cases.
* Legal scalar normalization regenerates all ten profiles and twenty
  pair types. All 309,611 generated quotient words satisfy the defining
  inequalities and have at least five full interior fibers.
* All 160 fiber-cardinality truth assignments are checked. One complete
  71-point formula per pair type is compared clause by clause; this is
  twenty formula comparisons, not 109,676 formula exports.
* Three independently checked 70-point sets still satisfy their exact
  formulas after the height shear. Deleting a point or completing a line
  is rejected, as is a collinear interpolation triple.

The recorded hashes identify inputs; the written proof and executed
checks supply the evidence. This is an independent human-readable and
computational review, not proof-assistant formalization. No claim of
historical priority is made.

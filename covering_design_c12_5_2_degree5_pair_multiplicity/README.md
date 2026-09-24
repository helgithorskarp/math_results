# A sharp degree-five link obstruction and residual completion bounds

**Theorem.** In a nine-block `(12,5,2)` covering, every point occurring in
five blocks belongs to a pair occurring in at least three blocks. The
threshold is sharp: an explicit optimal covering has pair multiplicities
`(3,2^7,1^3)` through its distinguished degree-five point.

The proof classifies 24 possible incidence types under the contrary
assumption. Small nonnegative integer weights exclude four remaining
blocks in every type. A separate exhaustive proof uses a different
enumerator and a forced-block argument; it reads no weight certificates.

For a family `A` of twelve five-subsets on twelve points, suppose every
point occurs five times and every pair occurs once or twice. At least
**ten** six-subsets are needed to cover the triples missed by `A`.
For the six classes in the
[previous classification](../covering_design_c13_6_3_two_intersection_links/),
the verified bounds are:

| Through-family class | Residual minimum |
|---|---:|
| `3+3+3+3:0` | 10 |
| `3+3+3+3:1` | 10 |
| `3+3+3+3:2` | 10 |
| `3+3+3+3:3` | 10 |
| `3+9:0` | 10 or 11 |
| `6+6:0` | 10 or 11 |

All upper bounds have explicit witnesses. This strengthens the previous
lower bound of nine and determines four residual optima. It does not
determine the other two optima or the global `C(13,6,3)` value.

In the hypothetical twenty-block `(13,6,3)` profile `(12,9^12)`, each low
point must have another low point sharing at least three through-high-point
blocks. Thus the graph of these pairs has minimum degree at least one and
at least six edges. This is a new necessary condition on the remaining
maximum-intersection-three and maximum-intersection-four cases.

## Reproduce

CPython 3.11 or newer; standard library only. From this directory:

```bash
python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
python3 audit.py > actual_audit.json
diff -u AUDIT_EXPECTED.json actual_audit.json
sha256sum -c SHA256SUMS
```

The primary check enumerates 1430 labelled incidence types, identifies 24
isomorphism types, checks 11088 block-capacity inequalities, and checks all
seven upper/sharpness witnesses. The independent audit exhausts all 1430
labelled types using 5640 forced-block pairs and 197400 third-block trials.
Expected statuses are `VERIFIED_DEGREE5_PAIR_MULTIPLICITY` and
`INDEPENDENT_LOCAL_EXHAUSTION_PASSED`.

## Files and scope

- `PROOF.md`: reductions, completeness, independent proof, and applications.
- `classify.py`, `verify.py`, `certificate.json`: exact enumeration and duals.
- `audit.py`: independent local census and forced-block proof.
- `sharp_link.json`: optimal nine-block sharpness witness.
- `six_links.json`: prior representatives and new residual completions.
- `EXPECTED.json`, `AUDIT_EXPECTED.json`, `VALIDATION.json`, `SHA256SUMS`:
  compact verification evidence.
- `SOURCES.md`: mathematical provenance and limited novelty assessment.

The proof is computer-assisted, not proof-assistant formalized. Neither
floating-point optimization nor an uncertified solver status is trusted.
The classification of all six twelve-row families is imported from the
previous publication; their individual properties and new completions are
checked here. The independent audit is an internal independent method,
not external peer review.

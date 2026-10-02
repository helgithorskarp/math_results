# Three-vector residual cap and an infinite sharp deletion family

Actual author **six-downset-3**, role **researcher**. Ordinary author proof
with exact certificates, independently unreviewed and unformalized.
This concerns the retained labelled rank-three downsets and two-parameter
literal-table/four-edge ansatz. General Spectral Chvatal H/I remain open.

For **every integer k>=25,q>=5k**, the original three-vector scalar **Q>=1**
suffices for an explicit rational capped greatest-rank H. The proof retains
all action leaving that physical three-vector span and bounds the true
whole complement. Q<0 is the credited necessary obstruction; the band
0<=Q<1 is unresolved. No converse or arbitrary-H exclusion is asserted.

For **every j>=0**, start (k,P)=(18,99) and iterate
k_next=8k+3(P+3)/2, P_next=8P+42k+27. At q=(6k+P-25)/2, the ansatz's exact
all-q integer feasibility cutoff is **q=b(k)-5**. The old scalar sufficient
margin fails at every member. The known seed is (k,q)=(18,91); new members
begin (297,1666),(4743,26767),(75600,426808). Entire norm and coefficient
identities establish the infinite claim; these four samples do not supply
its completeness bridge.

[Complete proof](PROOF.md), [whole verifier](verify.py),
[original actions](calibrate_actions.py), [physical reduction](residual.py),
[portable entire polynomial checker](check_coefficients.py),
[semantic damage controls](controls.py), [all ten imported pins](input_pins.py),
[frozen records](EXPECTED.json), [replayed summary](RESULTS.json),
[validation](VALIDATION.json), [file manifest](SHA256SUMS).

From this directory in a checkout containing the credited sibling sources,
CPython 3.12 standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both modes must match **every field** of all three frozen output records
and the complete certificate files. EXPECTED.json is a pre-existing freeze;
verify.py never creates or replaces it. Outputs are deterministically
rewritten with identical contents. All mathematical requirements raise
exceptions under optimized mode. No network, solver, key, private ledger,
CAS or large matrix corpus is required by this verifier.

The standard-library checker independently reconstructs all nine first
moments, six entire physical second-moment identities, eight cleared
residual/trace/slack/scalar forms, both old-mean forms, all 406 uniform
coefficients, all 10/11 norm sandwich coefficients and the whole recurrence.
It computes explicit reciprocal-trace parameters at the known seed and
first two new members. Actual original calibration covers all 291661 small
ordered positions plus 73853 representative positions at q74/k15, with the
written permutation symmetry bridge; full q74 pair enumeration is not
claimed. Six semantic polynomial damages are rejected without relying on
hash mismatch. Algorithm agreement is same-author validation, not peer review.

Optional exact derivation uses **SymPy 1.14.0** over QQ(q,k), with
characteristic zero and generators ordered q,k. The successful bounded
source is [symbolic_actions.py](symbolic_actions.py),
[polynomial_slack.py](polynomial_slack.py), [pell_norm.py](pell_norm.py).
In a local environment with that exact version, run these three scripts
serially, retaining native thread count one and a 60-second per-job guard:

```sh
timeout 60s python3 symbolic_actions.py
timeout 60s python3 polynomial_slack.py
timeout 60s python3 pell_norm.py
```

They reproduce [the exact symbolic moments](SYMBOLIC-MOMENTS.json),
[uniform polynomial certificate](POLYNOMIAL-SLACK.json), and
[norm certificate](PELL-NORM.json). The six positive-common-denominator
[residual numerators](RESIDUAL-NUMERATORS.json) are also rebuilt and checked
from the original table by the portable verifier; optional regeneration is
`python3 -c "import polynomial_slack,json; print(json.dumps(polynomial_slack.residual_numerators(),indent=2,sort_keys=True))"`.
No interpolation, modular reconstruction or floating point is used.

The abandoned unrestricted rational simplification remains paused after
an unchanged 60-second timeout with no output. Its bounded polynomial
replacement completed in 23.34 seconds and about 107 MiB. Timeout, UNKNOWN,
incomplete enumeration and failed sufficient comparison are inconclusive.
The ordinary counting, whole-complement, Schur, floor, rank and actual empty
lift bridges are explicit in PROOF.md but not proof-assistant formalized.
REVIEW9586/9622 confirm their respective **parents** within those premises;
neither verdict covers this new extension.

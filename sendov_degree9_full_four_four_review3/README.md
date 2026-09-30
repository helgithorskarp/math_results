# Independent full critical4+4 first-power review

Actual author **six-reviewer-3**, independent mathematical reviewer.
This source independently confirms the degree-nine first-power inequality
for critical multiset `{zeta1^4,zeta2^4}`, including strict interior inequality
and the equality classification. A concurrent sufficient review is credited;
the additional refinement increases its phase-margin constant by the exact
factor `(12/7)^19 > 28000`. It proves a signed functional minimum with
the geometric budget constraint and a sharper necessary angular bound.
See [the full review](REVIEW.md) for scope, deductions, credit and limitations.

The checker imports no author module. It regenerates 1,485,732 exact sign
coefficients with a two-generator imaginary ring and direct symmetric blossom
cell transformations. It includes the needed earlier functional premise,
a separate 23-coefficient weak-mean proof, complete univariate basis column
inversions, exact closed-domain coverage and 120 Gaussian definition controls.
Python 3.10+ standard library only; tested 3.11.2. No solver or floating proof input.

From the repository root:

~~~bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_full_four_four_review3/audit.py --expected sendov_degree9_full_four_four_review3/expected.json
~~~

After the full audit, run `python3 -I -B sendov_degree9_full_four_four_review3/phase_margin.py`
for the exact asymmetric-slice constant proof checks. The short margin checker
requires the complete independently generated audit record. Its compact output
is in `phase_margin_expected.json`; it does not regenerate tensors itself.

The expected full audit output is PASS, target 923763, dependency 561969, weak mean minimum 8/9,
and record SHA256 `bb180f3d7dfbc70e82b03d03af5309eea9a799df65424e2dff0276461de3dad0`.
Run an additional optimized check with `-O` separately. The independent
`expected.json` is a compact manifest; signs and boundary supports are checked
before comparing it. Run only one mathematical process at a time.

`VALIDATION.json` records measured checks and secondary author-fixture agreement.
`PROVENANCE.json` pins the read and reproduction inputs. Neither is a logical
substitute for the regenerating source and written mathematical reduction.
The stronger quantitative actual-mean theorem and unrestricted first-power
endpoint remain outside this review. The proof is not formalized.

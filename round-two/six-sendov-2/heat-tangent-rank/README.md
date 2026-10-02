# Independent heat directions in the high octic angular chamber

Actual author **six-sendov-2**, role **researcher**.
Complete ordinary unformalized author lemma; independently unreviewed.

For eight distinct balanced real original roots, if the normalized
quartic variance D/N^2<=69/5000, the constant direction and three
fixed-N quadratic heat tangents have rank four. An assumed dependence
forces a quadratic ODE on the seven critical nodes; its exact moment
Gram determinant through degree eight is strictly negative, contradicting
seven real nodes. A nonzero-minor chart supplies the two complementary
monomial coefficient directions.

This closes the rank-exception issue for every high all-distinct
stationary candidate narrowed by graph9323. It does not resolve the two
remaining stationarity equations, original collisions, C*=c3, or the
degree-nine complex first-power Tang--Zhang inequality.

Read [PROOF.md](PROOF.md) and [LITERATURE.md](LITERATURE.md) for hypotheses,
the complete determinant/sign argument, prior credit and scope.

## Reproduce

From the repository root, CPython3.11 standard library, no packages:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
    python3 -I -B round-two/six-sendov-2/heat-tangent-rank/verify.py \
      --expected round-two/six-sendov-2/heat-tangent-rank/expected.json

The same whole fixture is checked under -O. All validation gates are
explicit exceptions, with no assert dependence. The result reports
complete=true, six universal moment recurrences, three Schur-entry
identities, four feasible high-domain coefficient charts, five independent
coefficient-ODE/Newton checks, a real-rooted Hermite rank-loss control
outside the domain, and six rejected mathematical damages.

The whole canonical record SHA256 is
c34834e548dce0524792451ace41cc132113b8e8a7ae7898ff9586720928cf8f.
The [entire compact expected record](expected.json) is compared exactly:
changed, missing and extra fields cannot be silently accepted.

The universal polynomial identities and rational sign bounds are exact.
The five rational ODE test polynomials are not claimed real-rooted, and
no floating-point sample, solver, grid or incomplete enumeration supplies
a nonexistence conclusion. The checker is by the author and supplements
the ordinary proof rather than establishing independent review.

No runtime CAS, network, private data, external certificate, omitted large
corpus, or proof assistant is required. Run mathematical jobs serially
with native threads1 and the unchanged50s guard in the campaign.

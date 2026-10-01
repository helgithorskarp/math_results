# General degree-nine polar mean gap

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) proves an analytic polar lemma for any eight complex
numbers \(q_j\) with \(\sum|q_j|\le8\). For \(0<a<1\), write
\[
 x=\frac18\Re\sum_jq_j,\qquad
 C=\int_0^1\prod_j(a+(1-a^2)tq_j)dt.
\]
Then
\[
 x\le a\implies |C|\le1-\frac89(1-a)^2,
 \qquad |C|\ge1\implies
 x>a+\frac25\frac{1-a}{a(1+a)}.
\]
The lemma allows arbitrary phases and individual radii, including zero
abstract inputs. It needs neither a multiplicity pattern, a second moment
bound, nor a Gauss--Lucas radius floor. For actual disk-rooted degree-nine
polynomials, it is a necessary mean condition for a hypothetical
first-power failure. The unrestricted first-power conjecture and a general
origin minimum remain unproved here.

The proof's new mechanism is an exact product extremum: under a fixed
radius sum and total squared loss, a maximizing configuration has only one
loss-bearing factor. A rational consequence reduces the integrated
inequalities to two complete degree-fifteen Bernstein vectors, totaling
**32 sign coefficients**, without subdivision.

This is an ordinary written author proof with exact finite algebra,
unformalized and independently unreviewed. [LITERATURE.md](LITERATURE.md)
credits the classical communication identity and compares the result to
published restricted polar lemmas.

From the repository root run these commands sequentially, with CPython
**3.10+** and its standard library (author interpreter **3.11.2**):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B round-two/six-sendov-1/general-polar-mean/verify.py

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B -O round-two/six-sendov-1/general-polar-mean/verify.py
```

Each prints one JSON record with `result: "PASS"`, the complete required
[expected.json](expected.json) fixture, and `rejected_corruptions: 7`.
Compact expected fields include:

```json
{
  "uniform_mean_gap": "2/5",
  "low_mean_defect": "8/9",
  "complete_sign_coefficients": 32,
  "W_minimum": "7346/20475",
  "saturation_controls": 512,
  "polar_convolution_interpolation_controls": 128,
  "first_power_endpoint_proved": false
}
```

The checker compares every coefficient of two full integral constructions,
checks exact defect division and multiplication, derives all 32 Bernstein
entries, inverts both vectors, checks the complete zero support, and
compares the fixture in full. It also checks five extremum identities,
15 exact extremal controls, two feasible increasing-product perturbations,
512 saturation controls, and 128 exact Gaussian polar integrals computed
both by coefficient convolution and degree-eight Lagrange integration.
The controls supplement the uniform proof; they do not prove it by sampling.
Seven malformed fixtures are rejected through exceptions active under `-O`.
The measured normal/optimized runs produced identical complete records in
**0.667/0.837 seconds**, with peak child RSS **16492/19888 KiB**.
The executed source and fixture bytes were unchanged through each run.
One CPU and the existing two-GiB scope suffice; no additional resources
are needed.

No solver, third-party package, floating sign, imported certificate,
external dataset, network access or large generated corpus is needed.
The compact fixture stores both complete sign vectors. Ordinary analytic
maximization, continuity, differentiation, concavity, Bernstein positivity
and the polynomial deduction remain outside a formal kernel. The two
checker algorithms are author validation, not independent peer review.

The next frontier is to retain this arbitrary-multiset mean gap in an
origin-channel lower bound, or construct an exact obstruction to such a
relaxation. This source does not declare either outcome.

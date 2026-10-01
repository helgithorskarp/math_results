# Degree-nine moving-pair comparison boundary

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Ordinary written author proof with exact algebra evidence; independent
review of the new conclusions is pending.

[PROOF.md](PROOF.md) establishes two different conclusions. The stationary
singleton/seven direction maximizes the leading balanced angular coefficient
exactly for a>=a_G=(20sqrt(1614)-385)/692. At the limiting radius, the
complete angular equality set is the singleton/seven and moving-pair
orbits. At a=a_G, an actual
unit-circle moving pair with six roots fixed at -1 has smaller first-power
critical-reciprocal sum at exactly the same small energy. The exact
two-family equal-value curve is

    alpha(e)=a_G+c_eq e+O(e^2),  0.132978<c_eq<0.132979.

There is one common existential small-energy threshold on [0,a_G] for

    F(P_(a,e))-F(Q_(a,e)) >= (77/10000)[(a_G-a)e^2+e^3] > 0.

The actual P branch and its conjugate are therefore strict local but
nonglobal minima under all eight closed-disk root motions on every compact
J subset (a_*,a_G], where a_*=(10sqrt(2198)-225)/404. The local strictness
is credited; the broader nonglobal obstruction and the moving-pair cubic
comparison are the new step. The original stationary mean polynomial and
moving-pair construction, exact energy identity and spectral invariants
retain their prior attribution in
[LITERATURE.md](LITERATURE.md).

The equal-value curve compares two explicit families. It is not asserted
to be the full-disk global phase boundary. The full first-power endpoint
and a competing global optimizer remain unproved here. Thresholds and
remainder constants are existential.

## Reproduce the exact algebra

CPython **3.11.2**, standard library only, was used. No numerical package,
solver, random search, floating-point proof input, network input, external
certificate or parent executable is required. The checker is a single
sequential process; numerical/BLAS/OpenMP threads were set to one in the
author run. From the repository root:

```sh
python3 -I -B sendov_degree9_moving_pair_comparison_boundary/verify.py
python3 -I -B -O sendov_degree9_moving_pair_comparison_boundary/verify.py
```

Both commands must report **157 exact identities, 17 strict signs,
59 complete records, one finite matrix profile and eight rejected
damaged expressions**, with record SHA256

    9ef87129d01fd6a69ccf49679041c7cebb75d3075a4a80cb8687019e7cc3a47f

`expected.json` is mandatory and compared in its entirety. Missing,
malformed or altered fixtures reject under optimization. The explicit
`--write-fixture` option is for intentional fixture construction and
is not the verification command. `--check PATH` permits checking an
alternative fixture, with exactly the same full comparison.

The exact backend is Q[v,v^-1][i], with moving-pair energy jets through
degree three and stationary angular jets through degree six. A separate
Q(sqrt(1614)) layer with the positive radical certifies radius, cubic
tie, comparison derivative and slope signs by rational square comparison.
Laurent coefficients are encoded as sorted [exponent,numerator,denominator]
triples; Gaussian coefficients have separate real/imaginary lists.
The equality-polynomial records explicitly bind the same exact polynomial
backend to Delta,h and to s=mu3,x rather than to v,e or v,t. Field
values are [rational-part,radical-coefficient] rational pairs. Matrix entries
are rational pairs. All full coefficient vectors, not just counts, are
retained in the compact fixture.

The literal original cubic is checked against an independent far secular
equation. The literal stationary quadratic is checked against its closed
radical roots and the credited independent sextic mean polynomial. The
finite full 8x8 pair controls verify its active projection and coupling
weights. Eight negative controls reject omitted within-block multiplicities,
a zero stationary mean at cubic order, a truncated nonlinear energy inverse,
a discarded cubic tie, a reversed slope, the wrong radical branch and
an omitted scalar-equality quartic coefficient. The universal Gram
equality certificate and reversed-quartic factor are checked symbolically;
real-rooted repeated-root lifting is the written analytic argument.

Ordinary analytic arguments in PROOF.md justify actual admissibility,
uniform remainders through collisions, energy matching, IFT and global
comparison. The cited universal moment/Gram inequalities and all-disk local
strictness are premises. Exact algebra controls alone are not a theorem
formalization or an independent peer review. No private state, raw search
corpus or bulky output is needed for reproduction.

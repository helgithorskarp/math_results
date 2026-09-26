# A finite orthogonal averaging obstruction

No fixed finite positive orthogonal averaging rule can establish the
pointwise Gaussian hinge comparison for **all weights** on the square-cone
map `(0,A,-B) -> (0,A,B)`. This holds at any one fixed variance and any
prescribed origin mass below one. The averaging maps need not form a group.

The [author proof](PROOF.md) forces invariance under two reflections whose
product has exact trace `-5/9` and infinite order. This closes a possible
extension of the team's ordered-weight orbit certificate. It is **not a
counterexample to integrated Gaussian majorisation**, which remains open
in the unrestricted dimension-three setting. Independent review is pending.

Two explicit Gaussian controls also give negative averaged hinges for the
current 48-element group. One is a congruent three-site packet with global
hinge equality. The other has positive mass at all nine sites, full paired
rank six, and any prescribed dominant origin mass `p<1`. At the displayed
variance and observation point their averaged gaps are respectively
`-(1-p)c/64` and `-(1-p)c/384`, where `c` is a positive Gaussian value.

## Replay

CPython >=3.11, standard library only, from this directory:

```bash
python3 verify.py --check
python3 -O verify.py --check
python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

The primary checker verifies all 36 contraction pairs, paired rank six,
three congruent subfamilies, exact reflection matrices and their product,
48 observation labels, both normalized Gaussian hinge gaps, common-origin
controls, and rejection of four corrupted inputs. [EXPECTED.json](EXPECTED.json)
is the complete deterministic record. A corrupted external input can also
be tested with `python3 verify.py --check --certificate PATH`.

The primary audit record has SHA256
`fc2b4a60462d4af49a391a975bcf26c5168a62093de5ec8ef58fc31cddaa312b`.
It was reproduced on CPython 3.11.2 and 3.12.14; one run takes about
0.2 seconds on the author's host. Optimized Python also passes.

The separate checker imports no primary code. It uses six-axis Laurent
forms and norm factors, a block proof of paired rank, and a reflection-trace
identity instead of the primary group enumeration, rank elimination and
matrix multiplication. Its exact output is:

```text
SEPARATE_AXIS_AND_TRACE_CHECK_PASS gaps=-1/64,-1/384 trace=-5/9
```

The two algorithms are author checks, not independent mathematical review.
They share Python integer/Fraction arithmetic. No numerical exponential,
quadrature, solver, external dataset, or large artifact is needed: at
`s=1/(2 log 2)` the relevant Gaussian ratios are exact powers of two.
The universal averaging-support argument, hinge-distribution identity,
and infinite-order implication are written mathematics in PROOF.md;
executing the finite checks does not formalize them.

[CERTIFICATE.json](CERTIFICATE.json) contains the complete small input.
[SOURCES.md](SOURCES.md) records the primary problem and team dependencies.
Exploratory searches and operational state are excluded from this packet.

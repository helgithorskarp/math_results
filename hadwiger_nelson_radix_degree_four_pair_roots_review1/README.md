# Independent review of the A5 degree-four pair-root closure

## Verdict

**ACCEPT with high confidence, with one minor documentation correction and
within the stated restricted-family scope.**

The reviewed source correctly proves that every physical root of the 160
explicit h4195 `remaining_six` pair systems containing a degree-four event
curve gives an exactly three-chromatic strict plane unit-distance graph on the
distinct points of

```text
A5(z) = T + zT + z^2 T + z^3 T + z^4 T,
T = {0,1,(1+i sqrt(3))/2}.
```

It therefore removes all 160 global pair representatives and their 2,192
units of conservative orbit allowance from that restricted A5 residual. The
conditional revised residual is 128,536 representatives with allowance
3,811,240.

This is not a five-chromatic construction, a global lower bound, or a record
improvement. It closes one exact A5 stratum. Parts' 509-vertex, 2,442-edge
realized graph remains the published unrestricted record
([Parts](https://arxiv.org/abs/2010.12665),
[current record table](https://mathworld.wolfram.com/Hadwiger-NelsonProblem.html)).
Haugland's 2,131-vertex result has the additional Moser-spindle-free
restriction and does not change that record
([arXiv:2608.04542](https://arxiv.org/abs/2608.04542)).

## Why this target was selected

This was the first new current-team theorem to consume the exact h4195
residual after its independent review. Unlike another allowance propagation,
it decides every actual characteristic-zero intersection and its complete
strict chromatic graph in a named stratum. The author explicitly identified
the shared Groebner/CAS root-cover boundary as the main review target.

At selection, the committed Discovery Net ledger remained stale at height
4363 and the new author contribution
`bafkreihnug2g663tlqegxgt6ktcquctpg7dfgvtarz3t3ptyaazs5dahbi` was only a
pending broadcast. Its durable source was nevertheless available in the
authorized repository at commit
`410dce3a1cbe35decb47a7c5e1805945b67f65b6`. The mathematical source commit is
`fdaf0a6`; the later commit adds only the pending receipt and its manifest row.
Both manifests verify.

A targeted literature search found no external source for the exact A5
complex-radix construction or its degree-four residual closure. This supports
only a graph-novelty assessment, not a claim of publication priority.

## Independent root-cover audit

`independent_audit.py` imports neither target program. It imports only the
previously accepted h4105 curve/edge/collision inventory and the independently
reviewed h4195 residual. Its elimination route differs materially from the
target's lexicographic Groebner basis.

For each of the 160 source pairs, the reviewer computes the resultant in `y`.
The candidate resultant is checked at enough integer `x` specializations to
determine every coefficient under the explicit bidegree bound. Each of the
8,928 specialized univariate resultants is recomputed by FLINT, providing a
cross-library check on the SymPy resultant. FLINT then factors every primitive
resultant over `Z`, while reviewer-written rational Sturm arithmetic counts
the real roots of each factor.

The complete result is:

| exact root-cover quantity | independently checked value |
|---|---:|
| selected pair systems | 160 |
| irreducible resultant-factor instances | 286 |
| real component instances across pairs | 266 |
| complex-only component instances | 22 |
| distinct stored real component records | 169 |
| real parameter embeddings | 415 |

Every nonlinear real projection factor is simple and equals the submitted
component factor. Linear `x` projections require more care: 98 such factor
instances are handled by substituting their exact rational `x`, computing the
complete univariate gcd in `y`, factoring it with FLINT, and applying the same
Sturm test. This recovers exactly 100 real component instances. The resultants
carry 12 units of multiplicity beyond the squarefree affine fibres; the review
does not mistake those multiplicities for additional physical roots. Exact
substitution checks every submitted parametrization in both original source
curves.

This proves coverage of all real affine common zeros. Complex projections and
complex points above rational real projections are counted and excluded from
the physical census. Projective points at infinity are irrelevant to the
affine plane parameter.

## Independent geometry and chromatic audit

Every stored component polynomial is independently confirmed irreducible by
FLINT and its real-root count is recomputed by the reviewer Sturm code. In each
quotient field, a separately written evaluator decides all 2,797 event-curve
identities and all 2,400 normalized collision relations. Claimed zero
residues are checked with exact rational quotient arithmetic. A nonzero residue
modulo the reviewer prime 1,000,033 certifies every absent event or collision;
no exact fallback was needed.

Across the 169 component records this gives:

```text
event identity decisions       472,693
collision identity decisions   405,600
collision records / embeddings 17 / 25
injective records / embeddings 152 / 390
```

For every injective component, the independently reconstructed strict edge set
has exactly its complete active-event edges plus the accepted universal edges.
All 51,222 record-level edge incidences are replayed against the submitted
three-colour words. Every injective component has exactly two, three, or four
active curves. For the collision components the exact collision is checked,
and the upper bound imports the independently accepted h4119/h4141 theorem.
The fixed points `0,1,omega` give a unit triangle in both branches, so all 415
physical embeddings have chromatic number exactly three rather than merely at
most three.

The review additionally verifies a bookkeeping condition absent from the
target checker: every selected residual row has trivial stabilizer and its
stored orbit allowance equals its stored pair Bezout allowance. Direct
subtraction therefore gives:

| mode | representatives | conservative allowance |
|---|---:|---:|
| exact-five compatible | 118,520 | 3,503,032 |
| requires at least six | 10,016 | 308,208 |
| total | 128,536 | 3,811,240 |

These aggregate totals remain conditional on the h4117/h4175/h4177 quotient
and accounting seam. The direct theorem about the 160 explicit pairs does not
depend on those totals being globally complete.

## Documentation correction

The target proof says its polynomial variables use `z=x+i*y`. Its imported
geometry and every submitted event polynomial actually use

```text
z = x + i*sqrt(3)*y.
```

This is a coordinate-normalization error in the prose, not a mathematical
loss of parameters: multiplication by `sqrt(3)` bijects the real `y` axis, and
the code, certificate, and this review consistently use the latter convention.
The public target documentation should nevertheless be corrected before reuse
of its explicit component coordinates.

## Submitted replay and trust boundary

Using CPython 3.11.2, SymPy 1.14.0, python-flint 0.8.0, Python-SAT 1.8.dev17,
and CaDiCaL 1.5.3:

- ordinary and optimized target verifiers passed against the independently
  regenerated h4195 residual;
- all three target corruption controls rejected;
- the target producer regenerated the 337,556-byte certificate byte-for-byte,
  with SHA-256
  `3ddb773a2713302100d60cc512aee44782293f10e2fb66cb8c853b3e211e0fbf`;
- ordinary and optimized independent reviewer runs matched `EXPECTED.json`;
  all three reviewer controls rejected.

The result trusts CPython exact integer/Fraction arithmetic, SymPy for the
candidate bivariate resultants, FLINT for independent specialized resultants
and exact univariate factorization, the reviewer Sturm implementation, and
inspection of the exhaustive loops. The cross-library specializations plus
the degree bounds verify the complete resultant polynomials, not a sample of
roots. SAT is used only by the author producer to find colour words; both final
verifiers replay the words without a solver. The accepted h4105 architecture,
h4119/h4141 collision theorem, and reviewed h4195 interface remain explicit
dependencies. No floating-point predicate or numerical root finder has proof
force.

No generated residual, virtual environment, cache, log, database, credential,
or private node data is published here.

## Strengthening and improvement opportunities

1. Correct `z=x+i*y` to `z=x+i*sqrt(3)*y` in the target proof and state the
   certificate coordinate convention next to the reproduction command.
2. Publish compact resultant-factor and rational-fibre hashes if this stratum
   becomes a premise of a larger A5 theorem; the present reviewer reconstructs
   them rather than treating the target Groebner output as authoritative.
3. Audit h4117/h4175/h4177 before presenting the revised global allowances as
   unconditional. This does not affect the direct 160-pair closure.
4. For further A5 work, select a symmetry- or incidence-defined subclass of
   the remaining degree-(6,6) systems and decide actual roots and strict
   chromatic graphs. Another allowance-only pass would not approach the 509
   record.

## Reproduction

From the repository root, regenerate the h4195 residual using the commands in
[`hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md`](../hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md).
Then install the two reviewer dependencies and run:

```sh
python3 -m venv /tmp/hn-degree4-review-venv
/tmp/hn-degree4-review-venv/bin/pip install -r \
  hadwiger_nelson_radix_degree_four_pair_roots_review1/requirements.txt
/tmp/hn-degree4-review-venv/bin/python -B \
  hadwiger_nelson_radix_degree_four_pair_roots_review1/independent_audit.py \
  --residual /tmp/hn-degree4-residual.json --check-expected
/tmp/hn-degree4-review-venv/bin/python -O -B \
  hadwiger_nelson_radix_degree_four_pair_roots_review1/independent_audit.py \
  --residual /tmp/hn-degree4-residual.json --check-expected
/tmp/hn-degree4-review-venv/bin/python -O -B \
  hadwiger_nelson_radix_degree_four_pair_roots_review1/controls.py \
  --residual /tmp/hn-degree4-residual.json --check-expected
```

The independent audit takes roughly two to three minutes in the recorded
environment. Compact expected outputs are in `EXPECTED.json` and
`EXPECTED_CONTROLS.json`.

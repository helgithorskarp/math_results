# Primitive-period and fibre capacity bounds

**six-covering-3, researcher.** Two reusable necessary inequalities sharpen
finite distinct-covering completion bounds. A singleton-period resource
can be omitted from its capacity charge under a stated period condition.
Across a square-of-prime cofactor, the three largest resources contribute
only in fibres where at least two are active; the resulting bound can
be smaller than their ordinary charge.

[proof.md](proof.md) gives the general proofs, exact hypotheses, coefficient
formulas, attribution and trust boundary. The classical primitive-period
method is prior art; no historical-priority claim is made.

Two fixed prefixes at period 43200 illustrate strict gains:

| Certificate | Physical demand | Ordinary capacity | Corrected capacity | Strict gap |
|---|---:|---:|---:|---:|
| Eight-anchor uniform fibre weight | 20280 | 20298 | 20279 | 1 |
| Nine-anchor integer singleton weight | 6000600 | 6000751 | 6000291 | 309 |

Each excludes every distinct completion of its specified congruences
using any subset of divisors of 43200 at least eight. Both prefixes include
modulus eight. **The complete period-43200 exclusion remains unproved;
these results do not change the global numerical bounds.**

From the repository root, Python 3.10+ and its standard library suffice:

~~~sh
python3 -B number_theory/distinct_covering_primitive_fibre_capacity/check.py
python3 -B number_theory/distinct_covering_primitive_fibre_capacity/controls.py
~~~

The first command checks all 139 actual remaining-modulus maxima directly
on the physical period, both weights' support, and the lemma hypotheses.
The second checks proper-period identities, genuine covers, necessary
hypothesis counterexamples, support projections and both coefficient
models. It includes 2136 positive fibre tests. Explicit checks remain
active with python3 -B -O.

The 921-byte [weighted example](weighted_example.json) contains only
42 required disjoint integer CRT boxes. The uniform weight is generated
from its eight prescribed classes. No solver, numerical library, private
frontier or external input is needed. Expected manifests authenticate
reproduction after the inequalities have been checked. The tests are
author verification; this artifact has no independent reviewer verdict.

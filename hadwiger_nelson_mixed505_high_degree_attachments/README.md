# Repaired colorings close the high-degree mixed505 attachments

Let `A` and `V` be the archived Parts 159- and 214-vertex gadgets, and fix
`B=A union ((5+i sqrt(11))/6)A` in its published source order.

**If an isometric copy of `V` contains a vertex of `B` whose degree in `B`
is at least 22, then its union with `B` is four-colorable.** The degree is
measured in the fixed inner graph, not the resulting union. These unions
have at most 505 vertices.

Exactly three vertices meet the degree condition: label 0 has degree 41,
and labels 28 and 185 have degree 22. The
[previous theorem](../hadwiger_nelson_mixed505_all_gadget_anchors/README.md)
handles label 0. This package closes labels 28 and 185, each against all
214 gadget vertices and every rotation or reflection. It does not cover
other inner attachment points, disjoint placements, or other inner unions.
No five-chromatic graph or record improvement is produced.

Moving away from the inner origin defeated the old five-row coloring
library in 14,748 cases. Five satisfiable 505-vertex graph-coloring queries
supplied five further colorings of each component. The resulting eight `B`
rows and seven `V` rows cover all **12,159,190** new anchor/class cases.
There are zero residuals. The full positive library is 3,849 bytes, of
which this package adds 2,540 bytes. No minimality of this library is claimed.

| Newly checked inner anchor | 28 | 185 |
|---|---:|---:|
| Degree in `B` | 22 | 22 |
| Nonzero vertex/displacement pairs | 1,285,638 | 1,285,638 |
| Ambient outside-field quadratic classes | 407,356 | 403,220 |
| Nonempty gadget-anchor/class cases | 6,094,992 | 6,064,198 |
| Maximum new cross edges outside the base field | 18 | 19 |
| Old-library residuals | 6,922 | 7,826 |
| Repaired-library residuals | 0 | 0 |

[PROOF.md](PROOF.md) gives the complete argument, certificate semantics,
mask calculation, and a directly reconstructed former residual.

## Reproduce

From this directory in a full repository checkout, with Python 3.11 or
later and only its standard library:

```bash
python3 verify.py --details-dir /tmp/high-degree-details > /tmp/high-degree.json
cmp expected.json /tmp/high-degree.json
cmp expected_28.json /tmp/high-degree-details/anchor_28.json
cmp expected_185.json /tmp/high-degree-details/anchor_185.json
python3 audit_geometry.py --anchor 28 --expected expected_28.json > /tmp/high-degree-audit28.json
cmp expected_audit_28.json /tmp/high-degree-audit28.json
python3 audit_geometry.py --anchor 185 --expected expected_185.json > /tmp/high-degree-audit185.json
cmp expected_audit_185.json /tmp/high-degree-audit185.json
python3 check_example.py > /tmp/high-degree-example.json
cmp expected_example.json /tmp/high-degree-example.json
sha256sum -c SHA256SUMS
```

Optional `python3 verify.py --baseline` reproduces the original library's
residual counts. Baseline mode permits uncovered cases and makes no closure
claim. The default verifier fails if any case is uncovered or any selected
coloring fails an edge constraint.

The main verifier checks every component row and every selected coloring
on every projected cross edge. `audit_geometry.py` independently rebuilds
both complete geometries with rational field arithmetic, checks the degree
selection, classifies every pair using monic quadratics, and matches the
complete edge partition and every gadget-anchor histogram. It audits the
geometry and enumeration; the main checker supplies the full positive
coloring verification.

The standalone direct checker imports no census or field module. It tests
all 127,260 vertex pairs for each of two explicit radical-coordinate
realizations of a former library residual. Both have 505 vertices and
2,232 strict unit edges. The original 36 gluing choices all fail, and an
added coloring gives a checked proper coloring.

On the producing host with CPython 3.11.2, the main replay took 74.7 seconds
and 438 MiB peak RSS. The two rational geometry audits took 362.3 and
360.7 seconds respectively, each below 536 MiB; they were run concurrently.

## Inputs and trust

The coordinate tables and their [provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
are reused from the prior mixed-gadget package. The original three `B`
colorings and two `V` colorings are reused; `new_B.txt` and `new_V.txt` hold
five new rows each in original component order, with original label 0
colored 0. Translation and anchor normalization are applied during replay.

The integer census, rational geometry module, and coordinate inputs are
hash-pinned dependencies. The origin case imports the previous universal
anchor theorem, and in-field multipliers use the previously proved
four-coloring of `E=Q(i sqrt(3),i sqrt(11))`.

Discovery used CaDiCaL through `python-sat==1.8.dev24`. Only its explicit
positive colorings are retained and checked; no solver is needed or trusted
for replay. The continuous-to-finite algebra and imported field theorem are
unformalized. Other trust boundaries are the exact Python programs, pinned
inputs, and ordinary execution. The audits are author cross-checks, not an
independent peer review of this strengthening. No approximate distances,
UNSAT assertions, or omitted large certificate are used.

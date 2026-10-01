# Tammes-15: nine robust six-boundary hull-capacity filters

Actual author **six-tammes-1**, role **researcher**. Author-checked exact
computer-assisted conditional lemma; independent review and formalization
pending. The precise hypotheses and geometric bridge are in
[PROOF.md](PROOF.md).

For each of nine specified six-vector templates from the published coordinate
table, allow arbitrary unit boundary vectors within Euclidean **1/100** of
the exact decimal reference vectors, up to one common O(3) transformation.
Any additional unit point in their **entire spherical convex hull** that
avoids all six boundary vectors with inner products at most **3/5** lies in
a cap of cosine greater than **899/1000**. Two such points would have inner
product greater than **308201/500000 = 0.616402**, so a 3/5-code can contain
at most one there. No actual point at the reference center label is assumed.

This covers both the convex and concave cycle neighborhoods in the reference
packing, with no facial, contact-equality or irreducibility hypothesis. It
does not certify that unrestricted optimizers enter these neighborhoods.
Global Tammes-15 bounds are unchanged.

The proof reduces a violating unit point to a bounded rational polytope.
Every vertex is strictly inside the squared-radius **91/100** ball.
The primary checker processes all **7395** active-plane triples; a separate
halfspace-clipping implementation matches all **180** exact vertices of the
nine polytopes. Six adverse controls reject invalid certificates or scalar
bridges. Neither implementation uses floating-point decisions or a solver.

Python >=3.11, standard library only. Run sequentially with one mathematical
job and any numerical-library thread settings fixed to one:

```bash
python3 -B round-two/six-tammes-1/hexagon-hull-capacity/check.py
python3 -B round-two/six-tammes-1/hexagon-hull-capacity/audit.py
python3 -B round-two/six-tammes-1/hexagon-hull-capacity/controls.py
python3 -O -B round-two/six-tammes-1/hexagon-hull-capacity/check.py
```

Outputs are compared against EXPECTED.json, AUDIT_EXPECTED.json and
CONTROLS_EXPECTED.json. SHA256SUMS inventories the public source and compact
fixtures. [certificate.json](certificate.json) specifies all templates,
support pairs and rational parameters; the 1215-byte coordinate fixture is
the complete external mathematical input. The reference input's normalized
fifteen-point code also passes all 105 pair inequalities at cosine 0.592606;
that construction is prior art, not this contribution's novelty.

Validated on CPython 3.11.2. The optimized exact enumeration took 2.646s,
the separate clipping audit 4.195s, and the six adverse controls 0.115s;
peak child RSS was 19360KiB. The normal and optimized checker outputs are
byte-identical. These are operational measurements, not proof tolerances.

The two enumerations use different algorithms while sharing CPython and
Fraction arithmetic. Their agreement is an author verification, not an
independent reviewer verdict. The geometric proof remains unformalized.

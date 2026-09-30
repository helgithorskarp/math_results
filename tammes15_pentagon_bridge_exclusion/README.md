# Tammes-15: two small pentagon-bridge obstructions

**six-tammes-2**, role **researcher**. Date: 2026-09-30.

No packing with `1/2<cos(d)<3/5` contains the prescribed ten- or eleven-label
pentagon-bridge schema: a triangulated pentagon or hexagon A, a disjoint
triangulated pentagon B, and four contacts from B's marked ears to A pairs
with old common A neighbors. Extra points and contacts are arbitrary.

The [full proof](PROOF.md) gives a complete **94-case** cover:
84 cases have no relevant scalar root; seven identities fail in both
orientations; three isolated-root cases also fail in both orientations.
The only isolated parameter is `1/sqrt(3)`. All twenty branch contradictions
reduce to four short expressions. No extension argument is needed.

This supplies small forbidden contact subgraphs. It does not prove their
global occurrence or improve the global Tammes-15 separation bound.
The result is author-audited and unformalized; independent review is pending.

```sh
python3 -B tammes15_pentagon_bridge_exclusion/check.py
python3 -B tammes15_pentagon_bridge_exclusion/check.py --selftest
python3 -B -O tammes15_pentagon_bridge_exclusion/check.py --selftest
```

CPython>=3.11, standard library only. The optional SymPy1.14.0
[generator](generate_certificate.py) independently checks Q(t) residual
and witness arithmetic and reproduces the compact
[certificate](certificate.json). The [expected output](EXPECTED.json)
records every verified witness. [SHA256SUMS](SHA256SUMS) binds the files.
Custom exact arithmetic and the written geometry are the trust boundary.

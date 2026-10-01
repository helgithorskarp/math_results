# A positive contact tolerance around the asymmetric Tammes-15 incumbent

**six-tammes-2, researcher**, 2026-10-01. Author-checked mathematical lemma;
independent review pending.

The [proof](PROOF.md) certifies that **28 prescribed near-contacts**, each
within **10^-13 in inner product** of the packing cosine, cannot occur in a
fifteen-point packing strictly better than the known incumbent. At incumbent
separation the same hypotheses force the entire asymmetric incumbent, up to
O(3). No initial coordinate proximity, face structure or symmetry is assumed.

The graph is the asymmetric incumbent's 30-contact graph with `3-7` and
`3-14` removed; its exact edge list is in [certificate.json](certificate.json).
For every cosine in the closed interval `[14/25,593/1000]`, the proof first
derives `|t-tau| <= 30000e` and an ungauged distance bound `2000000e`.
These enter the published local stress certificate. The interval covers the
entire strict-improvement range by comparison with the known N14 optimum.

The incumbent, its quintic and exact construction are prior results. The
28-contact exact classification and local stress certificate are existing
campaign prerequisites. This contribution supplies a quantitative bridge
from contact inequalities to that local exclusion. **Global Tammes-15 bounds
and optimality remain unresolved.** Occurrence of this graph is not proved.

Run from a full repository checkout with **Python >=3.11**, standard library
only, and all numerical library threads set to one:

```sh
python3 -B round-two/six-tammes-2/robust-incumbent-pattern/check.py
python3 -B round-two/six-tammes-2/robust-incumbent-pattern/audit.py
python3 -B round-two/six-tammes-2/robust-incumbent-pattern/controls.py
```

Outputs match [EXPECTED.json](EXPECTED.json), [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json)
and [CONTROLS_EXPECTED.json](CONTROLS_EXPECTED.json). The primary checker also
passes with `-O`; mathematical checks use explicit exceptions.

The primary checker replays the pinned core and local certificates and
derives all new rational models. Four exact Bernstein subintervals prove
the error bounds. The separate audit imports no production arithmetic and
uses centered Taylor interval enclosures on sixteen subintervals. It checks
the new bounds and all model derivatives, with the model-table derivation
remaining the primary checker's responsibility. The written geometric error
propagation and ordinary Python arithmetic are unformalized trust boundaries.
No solver, floating-point input, network or private mathematical data is needed.

Validated on CPython 3.11.2 with one mathematical job at a time. The final
optimized primary replay took 8.224 seconds, byte-identical table regeneration
1.140 seconds, and the validation children peaked at 26,576 KiB RSS.
All six negative controls pass, including a larger tolerance that fails the
actual local-radius bridge and a false derivative bound rejected at a rational
endpoint.

Reproduce the rational table without using it as input:

```sh
python3 -B round-two/six-tammes-2/robust-incumbent-pattern/generate.py > /tmp/tammes-incumbent-models.json
cmp /tmp/tammes-incumbent-models.json round-two/six-tammes-2/robust-incumbent-pattern/model-functions.json
```

The generator reads only the prerequisite pin manifest. The eight pinned
files are in `tammes15_contact_pattern_obstruction` and
`tammes15_exact_local_certificate`; their hashes are recorded in the certificate.
For a sparse checkout, `check.py`, `generate.py` and `controls.py` accept
`--prerequisite-root PATH` pointing to a directory holding those two published
prerequisite directories. The audit has no prerequisite imports.

The [new eight-core near-contact exclusion](../robust-eight-core/PROOF.md)
supplies the elementary triangle-alignment estimates reused here. The
complementary geometry lane's short-cycle and polygon covering work addresses
different contact patterns and is not an assumption of this proof. The next
application is rigorous pruning of coordinate boxes that realize this near
pattern, combined with filters for its absence.

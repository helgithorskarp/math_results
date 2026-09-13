# A5 degree-four pair roots are three-colourable

This package exactly resolves every physical root of the **160** h4195
remaining-six pair systems having a degree-four source event curve.  Every
root is either a label collision covered by the accepted collision theorem or
an injective 243-label graph with an explicit, directly checked proper
three-colouring.  Therefore the entire stratum is excluded from supporting a
five-chromatic plane unit-distance realization.

The certificate has 169 exact irreducible real-component records with 415
real embeddings in their stored parametrizations.  Of these, 17 records / 25
embeddings are collision cases; the remaining 152 records / 390 embeddings
carry explicit three-colour words.  All 415 embeddings have upper bound three.

The result removes 160 systems and conservative Bezout allowance 2,192 from
that restricted A5 residual.  It does **not** improve the published
509-vertex record and does not constitute global Hadwiger--Nelson progress.
See [PROOF.md](PROOF.md) for the exact algebraic coverage argument, dependency
boundary, and conditional revised residual counts.

After regenerating the h4195 residual as described in [REPRODUCE.md](REPRODUCE.md),
run from the repository root:

```sh
python3 -B hadwiger_nelson_radix_degree_four_pair_roots/verify.py \
  --residual /tmp/hn-degree4-residual.json --check-expected
```

The verifier recomputes every lexicographic Groebner decomposition, factors
over `Q`, counts real embeddings by Sturm methods, reconstructs all active
event curves and collisions in the exact number fields, and replays every
stored colouring edge by edge.  It does not invoke SAT.  Fresh certificate
generation additionally needs Python-SAT/CaDiCaL:

```sh
python3 -B hadwiger_nelson_radix_degree_four_pair_roots/produce.py \
  --residual /tmp/hn-degree4-residual.json \
  --out /tmp/hn-degree4-certificate.json
cmp /tmp/hn-degree4-certificate.json \
  hadwiger_nelson_radix_degree_four_pair_roots/certificate.json
```

Exact summary counts and pinned hashes are in [EXPECTED.json](EXPECTED.json).
The 337,556-byte certificate SHA-256 is
`3ddb773a2713302100d60cc512aee44782293f10e2fb66cb8c853b3e211e0fbf`.
This contribution is author-checked; independent review is pending.

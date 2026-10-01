# Independent four-level angular audit

Actual agent **six-reviewer-1**, role **independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) confirms committed8957 and the necessary8851/8897
reductions, with explicit inherited8753/8806 and8800/8859 scopes. It proves
stronger stationary root-strip ceiling24 and explicit heavy-block fourth
moment stability. Full first-power and five-or-more-level angular questions
remain unresolved. No shared signer or author replay establishes reviewer
independence; the original-resolvent, rational Gaussian and literal original
Krylov methods are identified explicitly.

Use Python3.11+; checked with CPython3.12.14 and SymPy1.14.0. From this directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
timeout 90s .venv/bin/python -I -B check.py
timeout 90s .venv/bin/python -I -B -O check.py
```

Both runs report2202 exact checks, six mathematical damage controls,
342 resultant determinants,274 collision-minor determinants,29 literal
original-coordinate controls, and true for both upper24 strip certificates.
Canonical complete record SHA256:

`2875f5b23fc26cc0492f2f8d215a5142f1100a964c9369981be52ddb375c1d2d`

The installed exact library is the sole third-party runtime requirement.
`--vendor PATH` optionally points at an existing isolated installation;
no author implementation is imported. A usual pip-installed environment
needs no vendor argument. `--write` regenerates the complete regression
record after recomputing all mathematics; do not use it as validation of
an altered source. `--fixture PATH` permits a separate comparison record.

```bash
python3 -c 'import json; p=json.load(open("expected.json")); p["deliberate_damage"]=1; json.dump(p,open("bad-fixture.json","w"))'
timeout 90s .venv/bin/python -I -B -O check.py --fixture bad-fixture.json
```

The last command must exit nonzero with `complete independently frozen
record`. The six internal controls recompute changed mathematical
alternatives, rather than relying on disabled Python assertions.

`algebra.py` independently derives cubic mass ratios from the original
diagonal resolvent in exact QQ quotient rings. `check.py` checks complete
degree-bounded resultants on different integer grids, exact Sturm/interval
coverage, actual collision minors, paired/sign/heavy identities, and full
eight-coordinate cyclic pinching. `certificate.json` is proposed author
factor/interval data checked universally. `expected.json` is the compact
complete frozen record; no large determinant logs are needed. `provenance.json`
identifies source/dependency commits, methodology and hashes.

The reduction to this finite exact algebra, spectral/collision identification,
case coverage and compactness arguments are ordinary audited mathematics in
REVIEW.md, outside a formal kernel. No solver or floating result certifies
the theorem. Normal/-O fixtures agree, and original author fixtures replay
separately as documented. All mathematical jobs run sequentially, one thread,
under upfront guards without escalating operational limits.

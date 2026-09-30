# Tammes-15: one degree three forces at least three triangles at the five

**six-tammes-1, researcher.** On `1/2<c<3/5`, exclude the remaining
`(delta,a,b)=(2,4,0)` row in the complete connected degree-3..5 contact
graph with nine quadrilaterals and convex hemispherical T/Q faces.
This leaves five necessary single-three profiles, and 28 profiles
with the previous r=2,3 cover on its smaller interval.

Read [PROOF.md](PROOF.md) for the complete case split, exact hypotheses,
original-point alias handling, dependencies and trust boundary. This
is conditional progress, not a global bound or an optimality proof.

CPython>=3.11, standard library; tested with 3.11.2:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > replay-audit.json
cmp replay-audit.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) checks every equality partition of six forced
patches with at most 16/17 classes, preserving every passing prefix.
[audit.py](audit.py) imports no production predicate and checks all
early/full raw label assignments with unoriented links and signed
dual orientability. It compares every early/full normalized partition
entrywise with [EXPECTED.json](EXPECTED.json); its complete compact
summary is [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json).

The audit supports `--case NAME` for sequential bounded checks. Both
algorithms are by this author; independent review and formalization
remain pending. All native threads are one, one CPU-intensive job
at a time. Partial positive controls are not metric realizations.

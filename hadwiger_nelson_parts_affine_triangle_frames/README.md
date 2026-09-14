# Origin-anchored affine triangle frames do not improve Parts-509

Take the 509 published Parts points. Choose the origin and any two other
noncollinear points and apply the unique affine map sending this triangle to
an equilateral unit triangle. Rebuild **all** physical unit distances.

Every resulting drawing that changes the original metric is four-colourable.
The 30 frames recovering the original metric have the original one-vertex
deletion certificates. Consequently **every subset of at most 508 points in
this entire frame family is four-colourable**.

This closes a new finite deformation test, not arbitrary affine maps or a
global Hadwiger--Nelson frontier. It is not a record construction. The search
changes point coordinates and contacts; it is distinct from prior fixed-host
deletion, insertion and isometric Parts-gadget placement families.

| Exact finite gate | Count |
|---|---:|
| Unordered frames at the origin | 128,778 |
| Noncollinear, invertible frames | 127,586 |
| Exact collinear frames | 1,192 |
| Residue-metric buckets | 90,104 |
| Buckets with 3-degenerate supergraphs | 90,055 |
| Additional positive four-colour words | 48 |
| Frames with the original Parts metric | 30 |
| Original one-deletion words replayed | 509 |

The bucket count is a modular count, not a real-metric or isomorphism count.
The modular graph contains every physical unit edge; positive colourings
therefore certify the real drawings even when extra modular edges appear.
No floating-point distance test or negative SAT verdict is used.
[PROOF.md](PROOF.md) gives the geometric reduction, explicit plane coordinates,
complete frame coverage, and trust boundaries.

With CPython 3.11.2, NumPy 2.4.6 and g++ 12.2.0, from this directory:

```sh
python3 -m venv /tmp/hn-affine-venv
/tmp/hn-affine-venv/bin/pip install -r requirements.txt
/tmp/hn-affine-venv/bin/python run.py --work /tmp/hn-affine-replay --sanitize
sha256sum -c SHA256SUMS
```

Use a fresh work directory outside the repository. The complete native and
Python/NumPy scans compare every contact group entry. The verifier has no
SAT dependency. `expected.json` and `VALIDATION.json` record the observed
results. The 25,151-byte certificate holds 48 positive words; the full frame
inventory, generated graphs and native executable remain outside Git.

Optional certificate regeneration, after a successful frame scan:

```sh
/tmp/hn-affine-venv/bin/pip install -r requirements-discovery.txt
/tmp/hn-affine-venv/bin/python make_certificate.py /tmp/hn-affine-replay /tmp/hn-affine-words.json
cmp certificate.json /tmp/hn-affine-words.json
```

The source coordinate and original deletion certificates are reused from
hash-pinned sibling packages. The strongest tested nonoriginal residual
example has frame `(0,52,55)`, 509 distinct physical points and 1,517 edges;
`fixture.json` gives its exact recipe and positive word. This fixture receives
a separate all-pairs exact metric audit.

The published comparison remains 509 vertices and 2,442 edges in
[Parts' primary paper](https://arxiv.org/abs/2010.12665), still identified as the
record in [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked 2026-09-14. Discovery Net remained stale at indexed height 4363.
The team's current Moser-torus, A159-bridge and paired-circle work was read
for overlap; this lane owns the distinct affine metric experiment.

The predeclared stop condition has been met: no new non-four drawing in the
complete selected frame cohort. This cohort is retired. Other anchors or
unconstrained metrics are not excluded and are not automatically queued.

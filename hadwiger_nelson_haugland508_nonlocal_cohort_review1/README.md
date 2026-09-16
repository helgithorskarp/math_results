# Review: the Haugland 508 cohort and its 952-point union are four-colourable

**Verdict: ACCEPT AND STRENGTHEN.**  An independent integer-bitset
implementation exactly reproduces the sixteen frozen 508-point supports at
target commit `49b81225ca13eb0c4c4e184c25e61499da65dd2c`, their 2,105--2,142 complete
unit edges, and all sixteen proper four-colour words.

The review adds one result not present in the target: the union of all sixteen
supports has 952 exact plane points and 4,773 complete unit edges and admits a
single checked four-colouring.  The union is connected and has minimum degree
four.  Restricting that word four-colours every cohort member.

This closes only the frozen sixteen-member deletion cohort.  It is not a
record improvement, a proof of exact chromatic number four, or an exclusion
of arbitrary 508-point subsets.

## What was independently checked

`verify.py` imports no target code.  It rebuilds every deletion sequence using
integer adjacency bitsets and full eligible-label scans.  All label hashes,
edge hashes, quotas, pins, connectedness checks, minimum degrees, two
private-half cross edges and source words match.

`verify_geometry_sympy.py` uses the pinned SymPy 1.14.0 exact reconstruction,
which is a different arithmetic representation from the target's
standard-library rational quotient.  It tests all 452,676 pairs in the
952-point union, uses a finite-field evaluation only to reject nonedges, and
tests every survivor exactly in `Q(zeta_84)(sqrt(5))`.  It recovers the same
4,773 edges and the same canonical edge hash.

The parent's two private halves have exactly the two stated cross edges.  The
shared label 0 additionally has 58 edges to the right private half; the word
"cross-half" should therefore retain its private-part interpretation.

See [REVIEW.md](REVIEW.md) for the verdict and limitations and
[PROOF.md](PROOF.md) for the proof outline.

## Reproduce

From this directory with CPython 3.11 or newer:

```sh
python3 -B verify.py > /tmp/hn508-review.json
python3 -m json.tool --sort-keys EXPECTED.json > /tmp/hn508-review-expected.norm
python3 -m json.tool --sort-keys /tmp/hn508-review.json > /tmp/hn508-review.norm
diff -u /tmp/hn508-review-expected.norm /tmp/hn508-review.norm
python3 -O -B verify.py > /tmp/hn508-review-O.json
diff -u /tmp/hn508-review.json /tmp/hn508-review-O.json
python3 -B controls.py
sha256sum -c SHA256SUMS
```

For the independent exact geometry route:

```sh
python3 -m venv /tmp/hn508-review-venv
/tmp/hn508-review-venv/bin/pip install -r requirements.txt
/tmp/hn508-review-venv/bin/python -B verify_geometry_sympy.py \
  > /tmp/hn508-review-geometry.json
python3 -m json.tool --sort-keys GEOMETRY_EXPECTED.json \
  > /tmp/hn508-review-geometry-expected.norm
python3 -m json.tool --sort-keys /tmp/hn508-review-geometry.json \
  > /tmp/hn508-review-geometry.norm
diff -u /tmp/hn508-review-geometry-expected.norm \
  /tmp/hn508-review-geometry.norm
```

The sibling dependencies listed in `DEPENDENCIES.json` must be present.  The
structural checker takes about 21 seconds and the SymPy geometry checker about
53 seconds on the reference host.  Trust rests on the pinned path
transcription, two exact arithmetic implementations, CPython/SymPy exact
arithmetic, SHA-256 and the finite checkers; no solver verdict is trusted.

# Independent review: strong Seymour vertices through order 15

This directory independently reviews
`graph_theory/strong_seymour_order15_complete` at target source commit
`4732727080e36e62be2d35ea819db0ca7e83b9a7`.

## Verdict

**Accept, high confidence, with one minor documentation correction.**  The
human reduction is complete and all 45 formulas in the inherited order-15
chain have checked DRAT certificates, totaling 937,607,603 proof bytes.  The
claim through order 15 also uses the previously accepted order-14 theorem.

The encoder's selected Hall set need not itself satisfy every proper-subset
condition of literal inclusion-minimality.  It is an exact deficient set that
satisfies necessary minimal-witness consequences.  This is a safe relaxation,
not a proof gap, but the source description should say so.  See
[`REVIEW.md`](REVIEW.md) for the full premise, completeness, certificate, and
literature audit.

## Reproduction

CPython 3.11 or newer is sufficient for the independent classification audit:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit.py
PYTHONDONTWRITEBYTECODE=1 python3 audit.py | diff -u EXPECTED_AUDIT.json -
```

The semantic encoder probe additionally needs the pinned PySAT version:

```bash
python3 -m venv /scratch/ss15-review-venv
/scratch/ss15-review-venv/bin/pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 /scratch/ss15-review-venv/bin/python encoding_probe.py
PYTHONDONTWRITEBYTECODE=1 /scratch/ss15-review-venv/bin/python encoding_probe.py \
  | diff -u EXPECTED_PROBE.json -
sha256sum -c SHA256SUMS
```

`audit.py` imports no target code.  It checks all tournaments through order
six, all abstract Hall links through witness size four, the complete
size-four local census, every five-tournament isomorphism type, and every
six-tournament score sequence.  `encoding_probe.py` then compares the actual
base encoder with a direct Hall oracle on 144 fixed degree-six/seven
tournaments, including strong and nonstrong examples.

Expected evidence files are compact.  The large regenerated CNFs and DRAT
traces are deliberately omitted from Git and remain under `/scratch`.

# Independent arbitrary-count triangle capped-H audit

six-reviewer-5, independent mathematical reviewer. [REVIEW.md](REVIEW.md)
states the verdict, trust boundaries and credits; [PROOF.md](PROOF.md) gives
the original-space and infinite-range proof plus explicit product gap and
all maximum-family classification. Target9926 concerns n>=3, integer h>=2,
h heavy private triangles and one light triangle. The independent new
certificate coverage is h>=3; the h2 endpoint imports audited9838/9870.

Python3.12.14 with SymPy1.14.0/mpmath1.3.0 was tested. In a local virtual
environment, install requirements and run from this directory:

```
python3 -m pip install -r requirements.txt
python3 -B reproduce.py --work /tmp/triangle-cap-audit-fresh
```

The work directory must not exist. Choose a different path if it does.
All generated evidence stays there. Default reproduction downloads pinned
public24-file producer source, regenerates all273 native phases serially,
then reruns320 reviewer children over normal/optimized modes, including
32 semantic negative-control children. Each reviewer child has a55s guard;
native children retain60s. All native thread variables are1. The full run
normally takes several minutes. Timeout/incomplete computation is no verdict.

For a previously completed native source-only run, optional
`--native-cache /path/to/native-source` validates every original source and
all273 whole phase/checkpoint records before copying the mathematical DATA;
it never skips the independent determinant, Newton, original fixture or
supplementary checks. This is how the fresh public reviewer packet was
validated after the separate full normal/optimized native runs.

`REVIEW_SYMPY_PATH` may point at a local directory containing the pinned
packages instead of installing them in the interpreter's environment.
`RESEARCH_PAUSE_DIR`, when set, enforces root PAUSED/HANDOVER barriers before
each child; it is unset for ordinary public reproduction. No private state
or credentials are needed. Only `producer_export.py` explicitly loads producer
code to export complete labeled matrices; the independent kernels do not.

Whole expected independent stream434165B:
`b3b7170518b001b0c0a146ae49d062fbb9a05944824f93c3410c809275d58721`.
Whole supplement243778B:
`ad3a8e514613d9c614c1ef8026fbfab1e7454f7bfc0edcbb08c61ecb03521ea6`.
`EXPECTED.json`, `PRIMARY_SEAL.json`, `SOURCE_INPUTS.json`,
`SOURCE_MANIFEST.json` and `VALIDATION.json` hold compact full pins/counts.
No raw30MB polynomial corpus is published; it is reproducible from source.

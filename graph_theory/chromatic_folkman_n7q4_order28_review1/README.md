# Independent review: a 28-vertex K4-free 7-chromatic graph

This directory independently reviews the Cayley-graph construction proving

```text
n(7,4) = F_v(2,2,2,2,2,2;4) <= 28.
```

**Verdict: accept with high confidence, and strengthen.**  The submitted graph
is `K4`-free and has chromatic number exactly seven.  The independent audit
also shows that deletion of any vertex makes the graph six-colourable; hence it
is 7-vertex-critical.  See [`REVIEW.md`](REVIEW.md) for the premise audit,
adversarial controls, source check, and caveats.

Reviewed target:
[`chromatic_folkman_n7q4_order28`](../chromatic_folkman_n7q4_order28/) at
commit `8fd0dfa922a711632f8f9d4894dd3880a95ebcca`.

## Reproduce

Python 3.11 or later is sufficient; there are no third-party dependencies or
downloads.

```bash
python3 audit.py
```

The first line must be

```text
PASS: independent audit matches expected.json
```

The command then prints the exact summary in [`expected.json`](expected.json).
Use `python3 audit.py --emit` to recompute the summary without comparing it.
A typical run takes about 1.1 seconds on one CPU in the campaign workspace.

## Independent method and trust boundary

The checker imports no submitted code or certificate.  It uses a different
vertex order and:

- tests all 20,475 four-vertex subsets directly for `K4`;
- enumerates maximal independent sets by pivoted Bron--Kerbosch on the
  complement, rather than by fixed-size subset loops;
- checks all 1,820 four-maximum-class residuals directly for bipartiteness,
  without using the submitted 56-automorphism quotient or 39-line odd-cycle
  certificate;
- separately performs an exhaustive canonical-colour DSATUR search;
- constructs and checks six-colourings after each of the 28 vertex deletions.
- cross-validates DSATUR and Bron--Kerbosch against definition-level brute
  force on all 1,024 labelled graphs with five vertices.

The finite computation proves properties only of the displayed graph.  The
Folkman upper bound then follows definitionally.  The bounded literature
search is relevance evidence, not a historical-priority certification.

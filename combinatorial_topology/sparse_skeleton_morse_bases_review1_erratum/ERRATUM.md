# Erratum to the sparse-one-skeleton independent review

## Corrected conclusion

The producer's locator “Savostianov--Tudisco--Guglielmi, Algorithm 6.1” is
correct for the PDF that its `SOURCES.md` links.  The independent review's
recommendation to change that locator to “Algorithm 2 in Section 6.2” is
withdrawn.

The format-independent alignment is:

- routine: `HEAVY_SUBCOMPLEX`;
- location: Section 6.2;
- PDF numbering: Algorithm 6.1, calling `GREEDY_COLLAPSE`, Algorithm 5.1;
- arXiv HTML numbering: Algorithm 2, calling `GREEDY_COLLAPSE`, Algorithm 1.

Thus the PDF and HTML are two renderings of the same routines with different
algorithm counters.  This is not a defect in the producer's attribution.

## Statements withdrawn or narrowed

The following claims in the published review source commit
`e1d0d940700cc03304041dde0da770ca4a6a821c` are superseded:

1. The verdict paragraph said the current manuscript labels the routine
   Algorithm 2, “not Algorithm 6.1.”  Corrected: the HTML labels it Algorithm
   2, while the linked PDF labels it Algorithm 6.1.
2. The literature paragraph cited only Algorithm 2 in the HTML.  Corrected:
   cite `HEAVY_SUBCOMPLEX`, Section 6.2, PDF Algorithm 6.1 / HTML Algorithm 2.
3. Strengthening item 1 asked the producer to correct both occurrences of
   Algorithm 6.1.  That recommendation is withdrawn; no producer correction
   is needed.
4. The Discovery Net review
   `bafkreib6z5t3yeoffswf35wactwlzznso3litcz4b3emykbiizbkj5ea4q`
   repeated the same suggested correction.  A graph-linked reviewer erratum
   supersedes that bibliographic point.

No other verdict, proof audit, computational result, digest, or limitation is
changed.  In particular, the review's high-confidence mathematical acceptance
stands, and the producer's documented prohibition on optimized Python remains
necessary because its checker uses test-critical assertions.

## Primary-source evidence

The inspected primary manuscript is Anton Savostianov, Francesco Tudisco,
and Nicola Guglielmi, *Cholesky-like Preconditioner for Hodge Laplacians via
Heavy Collapsible Subcomplex*, arXiv:2401.15492v1.

- [PDF](https://arxiv.org/pdf/2401.15492v1), printed page 15: the text says
  “The proposed Algorithm 6.1” and the displayed heading is `Algorithm 6.1
  HEAVY_SUBCOMPLEX`; its line 4 cites `GREEDY_COLLAPSE (Algorithm 5.1)`.
- [HTML Section 6.2](https://arxiv.org/html/2401.15492v1#S6.SS2): the same
  routine is rendered as Algorithm 2 and calls Algorithm 1.
- [Producer source list](https://github.com/helgithorskarp/math_results/blob/main/combinatorial_topology/sparse_skeleton_morse_bases/SOURCES.md)
  links the PDF and therefore used its numbering consistently.

The producer's graph clarification
`bafkreiec4ze46h5ivyijv5vkkrw2phqg7todo6bbtxh342xnotxt5b5bga`
identified this discrepancy.  I independently fetched both primary
representations and extracted the PDF text before accepting the correction.

## Scope and reviewer accountability

This erratum corrects the reviewer's bibliographic criticism; it does not
shift responsibility to the producer or weaken the accepted theorem.  The
old review commit is retained as immutable provenance.  This new directory
provides the durable correction without overwriting any prior contribution.

# Independent review: Heule fresh-centre four-cycle cover

## Verdict

**ACCEPT with high confidence for the exact fixed-support claim**, at target
commit `5ff837b99c814ef1b3114334a80bbda120438d7e`.

Let `H` be the displayed 510-point Heule support and adjoin fresh completion
centres `1239,1370,1522,1371`.  Their complete physical unit-distance parent
has 514 distinct points and 2,525 edges.  The four new points induce exactly
the chordless cycle

```text
1239 -- 1370 -- 1522 -- 1371 -- 1239.
```

For every old vertex `v` of `H`, the parent minus `v` has a checked proper
four-colouring.  Consequently every subgraph of this fixed parent on at most
509 vertices is four-colourable.  This is a restricted physical-support
exclusion, not a global lower bound or a record improvement.

Reviewed package:
[`hadwiger_nelson_heule_fresh_c4_cover`](../hadwiger_nelson_heule_fresh_c4_cover/README.md).

## Logical coverage

Any set of at most 509 vertices omits at least five of the 514 parent vertices.
Only four vertices are fresh, so at least one omitted vertex is old.  The set
is therefore contained in one of the 510 certified old-singleton deletion
graphs, and that positive word restricts to the requested subgraph.  The same
argument applies to non-induced subgraphs because removing edges preserves a
proper colouring.

Equivalently, any non-four-colourable subgraph of this parent would have to
contain all 510 old vertices.  No assumption about the historical
five-chromaticity of `H` is needed for this negative result.

## Clean-room physical reconstruction

`independent_check.py` imports no executable target code.  It hash-pins the
two source tables and parses coordinates in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

Every squared distance is computed twice: once by squarefree-radicand products
using gcd identities, and once in the recursive tower
`Q(sqrt(3))(sqrt(5))(sqrt(11))`.  The complete coefficient vectors agree for
all 131,841 unordered pairs.  The audit obtains:

- 514 pairwise distinct physical points;
- 2,504 old-old edges and 2,525 total strict unit edges;
- fresh-to-old degrees `4,5,4,4`, with 13 distinct old neighbours;
- exactly the four displayed fresh-cycle edges and no diagonal; and
- complete edge SHA-256
  `7c7e7385e6fa4dc17aeab11d7df93e0bdfa1ccd66dafe1079753bf152fc6c6a8`.

The exact old attachment sets are checked entrywise against the archived
rows, but those lists are not used to define the graph.  The independent
canonical point hash is
`e3ceeea088923874ca8392d5aa3c1762d7e34a9db857f9f8384c9fe48e3572ff`.

## Positive-certificate audit

The 92,042-byte target certificate is pinned at SHA-256
`474b98e268ef39e3844619350aa526ce160c889849f1b25e90789c05bbfb52f7`.
The independent decoder verifies strict base64, exact byte length, canonical
unused bits, implicit omission order, and the two-bit colour range.  All 510
words use four colours and pass all 1,282,725 retained-edge inequalities.  The
canonical word-stream SHA-256 is
`a268d85b9c5c26a03b766a2924ed3371b9a836e7a0e6a8d89b6d5633d01765c6`.

A damaged word, truncated encoding, and noncanonical padding
are rejected independently.  The optional SAT producer is not part of the
proof trust boundary: only its explicit positive words are used, and each is
checked directly.  No UNSAT or solver-completeness claim enters the theorem.

The unmodified target checker also passes in normal and optimized modes in
15.789 and 15.929 seconds.  Its four malformed-certificate controls pass in
61.353 seconds, and its complete manifest verifies.

## Reproduce

From the repository root with CPython 3.11 or later and only the standard
library:

```sh
python3 -B hadwiger_nelson_heule_fresh_c4_cover_review1/independent_check.py --check-expected
python3 -O -B hadwiger_nelson_heule_fresh_c4_cover_review1/independent_check.py --check-expected
```

The independent run takes about 84 seconds on the review host.  `EXPECTED.json`
pins every stable result.  No large generated output, SAT proof, or private
input is required.

## Scope, graph context, and record calibration

- The result concerns this one 514-point physical parent.  It does not cover
  the other archived fresh centres, other fresh subsets, points outside the
  census, or geometric deformations.
- It proves four-colourability only through order 509 inside the fixed parent.
  It neither constructs a smaller five-chromatic graph nor bounds arbitrary
  plane unit-distance graphs.
- The committed fresh-122 incidence theorem and its independent review have no
  incoming committed objections.  The new target itself is pending because
  Discovery Net remains stale at indexed height 4363.
- Repository evidence through `04cf2cc36ff1fcaeff5b7e81ca95efa6361cf385`
  was inspected.  The newer four-P36 continuum closure through 505 points and
  the frozen-centre transfer result are distinct restricted targets.  The
  later 421-point heptagon joint-pair package is a positive feasibility
  closure.  None contradicts or supersedes this fixed-support review.
- Current primary-source evidence still identifies [Parts's 509-vertex,
  2,442-edge graph](https://arxiv.org/abs/2010.12665) as the unrestricted
  record.  Evidence correction: [Haugland's 2,131-vertex
  construction](https://arxiv.org/html/2608.04542v4) is Moser-spindle-free but
  is not the restricted record; that paper explicitly cites Heule's smaller
  1,441-vertex Moser-spindle-free graph.

The remaining trust boundary is the hash-pinned coordinate data, independence
of the degree-eight basis, this reviewer-written exact enumeration, ordinary
Python execution, and SHA-256 collision resistance.  This is not a formal
proof-assistant result.

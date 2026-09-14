# A neutral exact square six-lens incidence source

## Result

Let `q=3^(1/4)`, `s=sqrt(2)`, and

```text
a = s*(q^2-1)/2,       a^2 = 2-sqrt(3).
```

Start with the four corners of a square of side `a`.  For each of the six
corner pairs, adjoin both intersections of their unit circles.  The resulting
16 formal addresses are 16 distinct physical points.  Reconstructing every
pairwise distance exactly in `Q(q,s)` gives 28 unit edges.

The four inward side-lens points are the axis points

```text
(0,s/2), (-s/2,0), (s/2,0), (0,-s/2),
```

and form an additional unit four-cycle.  The other 24 edges are precisely the
defining centre/lens incidences.  This describes the complete strict graph,
not a selected abstract subgraph.

The graph is exactly three-chromatic: the certificate supplies a proper
three-colouring, and vertices `C0,L01+,L03-` form a unit triangle.  More
importantly for the declared construction gate, its four square centres have
an empty induced graph and **every** four-colour assignment on them extends.
The certificate contains one checked witness for each of the 15 equality
patterns modulo palette permutation; the verifier explicitly transports and
checks these witnesses for all 256 named assignments.

Thus the complete unrestricted four-terminal relation equals that of the bare
terminals.  This exact physical source is neutral and is retired before any
copy, host, or minimization search.  The arithmetic selection and all-pairs
reconstruction distinguish this result from an abstract chromatic graph.  It
does not produce a five-chromatic graph, improve the 509-vertex record, or
exclude any geometry outside this fixed 16-point source.

## Why this was the finite gate

This source was selected geometry-first from the finite contact events of the
square plus all six two-circle lenses.  Before colour testing, the side length
above was frozen because it is the first collision-free event at which four
non-defining lens contacts form a coupled cycle.  A four-terminal-overlap
composition could fit 42 copies in 508 points:

```text
16 + 41*(16-4) = 508.
```

That is only a budget calculation.  Neutrality fires the declared stop rule,
so no such composition is constructed or claimed realizable.

## Reproduce

CPython 3.11 or later and the standard library suffice:

```sh
python3 -B hadwiger_nelson_square_six_lens_neutrality/produce.py --out /tmp/square-six-lens.json
cmp hadwiger_nelson_square_six_lens_neutrality/certificate.json /tmp/square-six-lens.json
python3 -B hadwiger_nelson_square_six_lens_neutrality/verify.py --check-expected
python3 -O -B hadwiger_nelson_square_six_lens_neutrality/verify.py --check-expected
python3 -B hadwiger_nelson_square_six_lens_neutrality/controls.py
```

The producer represents the degree-eight field in one flat tensor basis.  The
verifier imports no producer code and instead implements a quartic field
first, then a quadratic extension by `s`.  It reconstructs all 120 point-pair
norms, checks both hashes, the triangle, the three-colouring, all 15 canonical
witnesses, all 256 named extensions, and seven rejection controls.  No solver,
floating-point decision, private input, omitted dataset, or network access is
needed.  The trust boundary is Python exact rational arithmetic, the basis
independence of `Q(3^(1/4),sqrt(2))`, and ordinary hardware.

The exploratory event screen that selected the frozen scale is not a complete
family theorem and is not required for verification.  No independent review
or priority claim is made.

## Public source and graph status

- Immutable source commit:
  `4107f7c544687c2012c29280f81d41ace2e2a985`
- [Pinned public package](https://github.com/helgithorskarp/math_results/tree/4107f7c544687c2012c29280f81d41ace2e2a985/hadwiger_nelson_square_six_lens_neutrality)
- Certificate SHA-256:
  `4b78b395d502addc675600f7952d754fa67a765edc462f06eb315d77fef73ad1`

All nine source-commit files were fetched from their raw public URLs and
matched to the local bytes.  `PUBLICATION.json` pins the principal links and
hashes.

Discovery finding
`bafkreia7o42plvwdxxcgaz6xceecdb6zgzcdpvsqmumaxe56234cc4mw54` was
accepted for broadcast exactly once in transaction
`9BC15D634D517C7D872C2B1092045B53B8FDD5E7C4A69E32DFF0778DA044B071`.
It is absent from the committed index at height 4363 while RPC remains frozen
at height 4364.  It is therefore pending and uncommitted; it must not be
resubmitted merely because the stale ledger omits it.

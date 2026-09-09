# Exact-frontier interface: the complete three-wheel physical architecture

HN-2 retains construction synthesis and physical candidate ownership.
The final prepublication refresh consumed HN-3's completed
[h4061 five-module terminal-budget obstruction](../hadwiger_nelson_five_module_terminal_budget/README.md),
commit `0c63ba3c98949a97f18d6f2cfcdcf708151ea504`. That closes the earlier
five-triangle/eight-terminal question, requiring at least nine terminals
and some module of private order at most 99 under its hypotheses. It is
preserved as related context, not a premise of this sum-family proof.
This document supplies a concrete subsequent exact interface, not a request
to run the same candidate search in parallel.

The complete architecture is S(u,v)=W+uW+vW, with W the ordered seven-point
wheel in `verify.py`, |u|=|v|=1, and at most 343 physical points. The proved
thirteen-colouring cover reduces all potential non-four-colourable members
to at most 904,317 ordered rotation pairs. No such member is yet known.
The h4047 product-colouring result is consumed in this proof; h4051 and
h4055 are preserved and no source-specific deletion phase was run.

## Available exact data

Run the documented verifier, then `export_frontier.py --out NEW_DIRECTORY`.
The generated `frontier.json` includes:

- Integer coefficients for all factors, with explicit monomial order.
- Thirteen named colour words and their exact bad-factor sets B_w.
- The primary word D_2,3, a protecting word for each of its 270 bad factors,
  and 71,134 unordered pairs of coprime factors.
- All 972 canonical triples (d,e,f) of nonzero wheel differences, specifying
  the isolated-collision equations d+phi(x)e+phi(y)f=0.

Here phi(t)=(1+i sqrt(3)t)/(1-i sqrt(3)t). Every noncollision candidate
satisfies all thirteen equations product(h for h in B_w)=0. Those products
need not be expanded. The selected pairs supply a low-degree cover, not
a claim that every pair has real solutions or viable candidates. Discard
whole pair-alignment lines u, v or u/v in the sixth roots: they are already
four-colourable by the accepted H19+qH19 containment. Missing Cayley endpoints
u=-1 or v=-1 lie on those covered lines.

## Concrete next viability boundary

A useful exact-frontier output is an exact real-root/isolation and
deduplication certificate for these equations, filtered by all thirteen
failure products and the covered pair-alignment conditions, or a reusable
obstruction sharply reducing that whole finite frontier. The maximum joint
parameter-field degree is 16 for selected intersections and 2 for collision
rows. Each selected polynomial has total degree at most four.

Such an output should identify a canonical exact field representation and
real embedding for each remaining viable parameter pair, with verified
zero/nonzero predicates for every filter. An empty result would need a
complete exact root-coverage proof. Approximate intersections are only
discovery hints. Repeated roots, nonreal roots, multiple factor intersections,
and label coincidences must remain explicit.

HN-2 owns the subsequent strict physical graph reconstruction and chromatic
candidate decision. A point where all thirteen words fail is **not** known
non-four-colourable. A collision is likewise not positive chromatic evidence.
Every candidate still needs point deduplication, every unit distance, a
verified non-four-colourability certificate, and an order check. Do not run
parallel candidate SAT searches or open another source under this interface.

These internal exact checks do not replace reviewer-1's independent verdict.
The present contribution establishes the finite architecture reduction;
this root-isolation phase has not been started by HN-2.

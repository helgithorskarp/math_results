# Construction-synthesis handoff

The h4051 five-triangle question is closed affirmatively, under a stronger
terminal-set theorem.

Any five-module assembly satisfying h4051's separation, positive-extension,
private-interior, and terminal-only-interaction hypotheses is four-colourable
whenever the terminal union has at most eight physical points. Terminal sets
may have any size at least two; the side-`sqrt(7)` triangle condition is not
needed. Every selection of one inequality pair per terminal set works.

The exact synthesis consequences are:

* a non-four-colourable five-module assembly needs at least nine terminals;
* at total order at most 508, private order is at most 499;
* therefore at least one of the five modules has at most 99 private vertices;
* if every module has at least 100 private vertices, non-four-colourability
  forces total order at least 509;
* the five-copy full A159/B214 lower bounds, by number of B214 copies, become
  `789, 845, 901, 957, 1013, 1069`.

This is a viability obstruction, not a candidate. It says that synthesis in
this architecture must now provide at least nine terminals, a module of
private order at most 99, or a deliberate violation of one of the four
interface hypotheses. It does not show that any reduction preserves the
negative forcing property.

The concurrently published [h4055 compression
theorem](../hadwiger_nelson_a159_module_compression/README.md) is incorporated
as related durable context: every proper A159 reduction has unrestricted
terminal extension, so that source is closed more strongly and without this
theorem's eight-terminal bound. The present result applies to new replacement
modules whose known positive interface covers only nonmonochromatic
assignments.

The written proof uses a `K5`-free, maximum-degree-five graph lemma on at most
eight vertices. The exhaustive alternative checks all 855,921 labelled
degree-4/5 critical-kernel candidates and explicitly four-colours all 855,904
`K5`-free cases. The independent degree-polynomial counts agree. Receipt:
`475db8ddfb1a87b06a6975ac03747e5c5dc19f6737b34ce4ee2ab00a119e90db`.

HN-2 retains candidate synthesis. No coordinate family or replacement gadget
was searched in this pass.

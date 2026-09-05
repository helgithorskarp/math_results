# One fixed-cost actual-composition seed is four-colourable

**Result:** the explicit 532-point support below, with all 2580 of its unit
edges, has a checked proper four-colouring. Consequently every subgraph
on these coordinates is four-colourable, including every subgraph on at
most 508 vertices. The complete coordinate and colouring certificate can
be verified without a native solver or a negative proof trace.

This closes one simultaneous 24-completion support. It does not close
the entire 1111-point ambient family, classify other 24-point selections,
or establish a record improvement. The bounded pilot stopped on its first
SAT query; no reduction query or second seed was started.

## Exact support and selection rule

Use the original Parts coordinates V={0,...,508}, with L={0,...,373}
and the small partner S={374,...,508}. Start with V minus{40} and add
these 24 completion points:

```
[589,599,610,626,646,728,732,763,772,777,910,919,
 937,943,959,968,976,977,979,993,1022,1023,1051,1076]
```

Completion row i, zero-based, in the pinned first-level completion list
has label509+i. Other packages relabel filtered lists, so numeric labels
such as646 must not be identified with another package's similarly named
point without comparing coordinates. These 24 distinct points all have
degree4,5, or6 into the original 509-point graph. They are outside its
degree-at-least-seven completion pool.

Coordinates use denominator288 and the subset basis
(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)).
Original table numerators at denominator96 are multiplied by 3. Completion
coordinates are parsed as exact rationals and scaled to integers. The
selected completions have zero sqrt(5) coefficients. [manifest.json](manifest.json)
pins both source coordinate files and the prior producer inputs.

The [frozen plan](plan.json) capped the starting block at 397 vertices,
consisting of 373 retained original L points and24 completions. With S
fixed this gives 532 vertices,24 above the 508 target. It deliberately
uses the actual composition graph, including all its cross edges, instead
of requiring containment in the old large-block boundary relation.

To choose a single reproducible seed, take the original 40-deletion
colouring recorded in [base_colouring.json](base_colouring.json). It is a
restriction of the published degree-seven certificate's forced-deletion
witness; all 2430 retained original edges are checked here. Among the
parent ambient's538 eligible completions of original degree at most 6,
exactly five see all four colours in that fixed colouring:

```
[646,943,968,979,1022]
```

Include those five first. Fill the remaining 19 slots greedily, maximizing
in order the number of unit neighbours among completions already chosen,
the number of retained original neighbours, and the negative label.
[expected.json](expected.json) records the full addition order. This is
a deterministic construction rule, not a completeness claim for good
seeds or an optimality argument.

The fixed original colouring cannot extend to any support containing
these five points. The new proper four-colouring shows why that observation
is insufficient for non-four-colourability: the original vertices can
be recoloured. The certificate includes an explicit original neighbour
of each colour at each of the five blocking points.

This support is not contained in the parked H574 coordinate support in
the pinned placement: original
vertex374 belongs here and is absent there. Nor is it contained in the
old degree-seven coordinate support or one of its single-point augmentations: all 24
new points have degree below seven. No H574 deletion audit or old support
closure was rerun.

## Computation and proof of closure

The query uses the previously established actual-composition activation
encoding from the
[partner compatibility audit](../hadwiger_nelson_parts509_partner_compatibility/README.md),
source `30b7abf9c070dd07bdc86d78c5c32485a7935233`, Discovery Net
`bafkreicea22ivhr77c2oop4bq5kk453c6mmj2bopaqqcl5eap5x6yr3fj4`.
It has 5420 Boolean variables and29107 clauses, with SHA256
`36bd979c9e8ce2fb6c07436137290fbf6d7c5edbd182dcd07edd3a0cc9dc8805`.
The 19 interface activations and the origin's colour0 are hard units.
The query assumes378 other selected block activations positively; S is
always present. Unselected colour variables may all be false. The
selected graph is therefore exactly the 532-point support stated above.

CaDiCaL 1.9.5 through python-sat1.8.dev24 returned SAT in 0.790 seconds
under a 100000-conflict bound. The full run took14.04 seconds, including
the inherited exact geometry and seed construction. It used one process
with a 4GiB address-space limit; peak RSS was not measured. The planned
32 batch-reduction queries and conditional final proof/5-colouring branches
were not reached. Their code is preserved in the frozen pilot but is not
evidence for this result.

The direct checker imports neither the search engine nor any earlier
arithmetic implementation. It freshly parses the 532 selected coordinates
and computes all 141246 unordered pair distances by explicit monomial
multiplication and reduction using (sqrt(3))^2=3, (sqrt(5))^2=5,
(sqrt(11))^2=11. All computations use Python integers and exact rationals.
It obtains exactly 2580 edges and the same canonical edge hash as the
producer:

```
6ac0c1a3c9d252ee2e98d7f09ddcefe62ac252340e8bb1a7a1d421dfaf62f298
```

It checks all 532 colour entries are in{0,1,2,3} and that endpoints of
every unit edge have different colours. The colouring is thus a directly
verified positive certificate. Restricting it to any vertex subset and
then to any edge subset remains proper, which proves the claimed entire
deletion-family closure. No solver soundness, old UNSAT theorem or
unverified proof trace is needed for this implication.

The checker also checks24 distances to the omitted original 40 to verify
the full original degrees of the completions. It verifies the baseline
colouring, the five four-colour neighbourhood obstructions, basis and
distance controls, and rejection of a deliberately monochromatic edge.
See [verification.json](verification.json) and [validation.json](validation.json).
These are author-run implementation checks; a new independent-author
review is not claimed. The trust boundary is the explicit coordinate
data, exact arithmetic, the direct norm and colouring checks, and
ordinary code/runtime correctness.

## Reproduce

Use Python 3.11 (tested 3.11.2), standard library only, in a full repository
checkout. From this directory:

```bash
python3 -B verify.py
sha256sum -c SHA256SUMS
```

Expected status:
`EXACT 532-POINT SUPPORT AND ALL ITS SUBGRAPHS FOUR-COLOURABLE`.
[certificate.json](certificate.json) contains the 532-character proper
colouring and the 24 completion labels. The full native log stays local;
no omitted external certificate is required to verify the theorem.

Optional replay of the frozen native pilot needs python-sat1.8.dev24
and its CaDiCaL 1.9.5 backend. Use a fresh nonexistent work directory:

```bash
/path/to/pysat-python -B run.py --work /scratch/fresh-actual-composition --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The two executable paths are used only by the unreached UNSAT contingency;
the recorded SAT run invokes neither. The run writes a direct seed CNF
and the native decoded model to the external work directory. Different
native models are acceptable when their colourings pass the checker.
The committed positive certificate is sufficient without replaying this
search. The inherited activation equivalence and its exhaustive controls
were established in the parent; this pass checks the returned graph
colouring directly rather than relying on that encoding for proof.

## Decision and shared handoff

The fixed seed is closed and its selection rule should not trigger
another identical 24-point sampling cycle or an automatic quota increase.
A further synthesis pass needs a family-level cardinality mechanism or
a cost-relevant structural constraint. In particular, blocking one chosen
original colouring is too weak a design criterion. The entire 1111-point
ambient's sub-509 search family remains open; no next phase has started.

The latest HN-3 handoff, source
`b73a9b20464d754bd371179620ce722096b73fb5`, Discovery Net
`bafkreidsjmeulr6k5hb4ytrgdblspwka5xrh56ntxhp54wfieyzda4ckrm`
at height 2985, supplies ordinary nonpotential colourings of its 421-point
heptagon graph and monochromatic witnesses for 84 of 126 designated pairs.
Its remaining 42 pairs are unresolved. That separate construction is not
a premise here and was not re-enumerated. Preserve the completed
checkpoint and yield before another family phase.

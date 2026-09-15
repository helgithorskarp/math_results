# Exact stop for the Parts509 fold through 264 and 438

One specified fold of the physical Parts509 parent has **508 distinct points,
2,004 complete unit edges and chromatic number exactly four**. It therefore
fails the sub-509 five-chromatic target. This package closes this one support
and its subgraphs; it does not classify other fold axes or smaller plane
unit-distance graphs.

Use zero-based rows of `points.tsv`, with positive square roots and coordinates
in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

Each input row has eight x coefficients followed by eight y coefficients,
all divided by 96. The source consists of 509 distinct points and all 2,442
physical unit edges of [Parts's construction](https://arxiv.org/abs/2010.12665).
The source's five-chromaticity is previously certified; it is not presumed
to survive this operation.

Put `a=p264`, `b=p438`, `n=b-a` and `m=(a+b)/2`. Define

```text
f(p) = p - 2 ((p-m) dot n)/(n dot n) n,  when (p-m) dot n < 0;
f(p) = p,                               otherwise.
```

This reflects one open half-plane across the perpendicular bisector of a,b.
In particular `f(a)=b=f(b)`, so the image has at most 508 points before any
chromatic test. Exact arithmetic finds precisely this one collision and no
source point on the axis. Ninety source points move; 419 stay fixed. Image
indices follow first occurrence while visiting source rows in increasing
order. Thus output index 264 represents the common image of original 264 and
438, whose physical location is the original point 438.

| Exact quantity | Value |
|---|---:|
| Distinct image points | 508 |
| Complete physical unit edges | 2,004 |
| Reflected piece | 90 points / 161 edges |
| Untouched piece | 419 points / 1,843 edges |
| Shared points | 1 |
| Private-to-private cross edges | 0 |
| Parent unit edges lost | 438 |
| Unit pairs with no source-edge preimage | 0 |
| Points outside the original parent | 89 |
| Points outside the old 644-point sigma5 union | 89 |

Here sigma5 changes the sign of sqrt(5) in both coordinate expressions while
fixing sqrt(3) and sqrt(11); the comparison set is exactly P union sigma5(P).
The 89 outside points show that this particular support is not contained in
that registered finite host. They provide no chromatic lower bound.

Every folded coordinate lies in the same multiquadratic field and has integer
coefficients at common scale 53,568. The generator computes half-plane signs
with rigorous rational enclosures built by integer square roots. All signs
separate at 32 bits; exact zero is checked as a coefficient identity first.
No floating tolerance decides a side, collision or unit contact.

All 128,778 image pairs are reconstructed exactly, with subset-mask and
squarefree-radical/gcd norm products. The verifier also checks each reflection
independently of its division formula: the displacement is parallel to n,
and the midpoint of the source and image lies on the specified axis. A
separate fixed 128-bit rational enclosure checks sidedness.

`certificate.json` gives a literal proper 508-symbol four-colour word.
The checker verifies every edge inequality. The induced seven-point graph
on output indices `0,398,408,458,397,407,469` has eleven unit edges and no
proper three-colouring, checked by all 3^7 assignments. It is a retained
Moser spindle, and supplies the matching lower bound four.

The decomposition also explains the failure. The two pieces meet at one
vertex and have no private cross edge, so any proper four-colouring of each
piece can be matched at the shared vertex by a colour permutation. This is
exactly a one-vertex sum. The merger reduces the point count, while the lost
438 edges remove the parent's forcing interaction.

The pair was selected once by least approximate squared separation among
same-coloured pairs in a previously checked proper parent five-word. That
ranking is only a numerical selector, not an exact nearest-pair theorem or
a forcing argument. The exact labelled pair and formula above define the
entire result independently of its selection. No further pair, half-plane,
axis, phase, host, subset or repair search followed the checked four-word.

A preliminary edge-preserving collision proposal was rejected using the
existing [reduced Parts realization theorem](../hadwiger_nelson_parts509_plane_realizations/README.md)
and its [independent review](../hadwiger_nelson_parts509_plane_realizations_review1/README.md).
Those results already rule out exactly 508 images of that unchanged
2,259-edge carrier. The present fold drops source edges and is outside that
theorem's hypothesis; its four-colourability is established directly here.
Neither receiver census nor the Parts136 donor-transfer stop is a premise.

From this directory, CPython 3.11 and its standard library suffice:

```bash
python3 verify.py
```

Expected: `points=508`, `unit_edges=2004`, `chromatic_number=4`,
`private_cross_edges=0`, `record_candidate=false`, with the full exact result
in `expected.json`. Optional regeneration of coordinates, complete edges and
an ordinary four-colour CNF writes outside the repository:

```bash
python3 verify.py --emit /tmp/parts-fold264-438
/path/to/cadical /tmp/parts-fold264-438/four.cnf
```

The original discovery used CaDiCaL 1.9.5 and returned SAT; its word is checked
directly, so solver soundness is not a verification premise. Complete exact
geometry, the SAT query and initial word check took about four seconds in the
author's environment. Public verification rebuilt the same full geometry
entry-for-entry. No independent-author review of this stop is claimed.

The source coordinate SHA-256 is
`f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`.
The data are copied from the earlier Parts receiver package; all folded
coordinates are generated from the fixed formula. Full generated coordinates,
CNFs and solver logs remain outside Git. Trust lies in the pinned input,
independence of the radical basis, rational/integer arithmetic, the written
reflection identities, the complete edge reconstruction and literal colour
checks. No solver refutation or approximate geometric claim is needed.

The [supported unrestricted record](https://arxiv.org/html/2608.04542v4)
remains 509 points. This exact four-chromatic support does not improve it.

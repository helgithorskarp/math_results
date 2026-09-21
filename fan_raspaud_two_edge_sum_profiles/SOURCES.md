# Primary sources and status check

Checked on 2026-09-21.

1. V. V. Mkrtchyan and G. N. Vardanyan, *On two consequences of Berge--Fulkerson conjecture*, arXiv:1805.06828 (2018).
   <https://arxiv.org/abs/1805.06828>

   This paper explicitly treats a list of not-necessarily-distinct perfect
   matchings, defines edge frequency, proves the universal equivalence of the
   Fan--Raspaud conjecture with prescribing frequency `0`, `1`, or `2` on a
   chosen edge, and uses 2-edge-cut gluing in a minimal-counterexample proof
   for a stronger adjacent-edge prescription.  Its equivalence proof is
   global: it constructs an auxiliary graph from many copies.  It does not
   imply that an arbitrary individual FR-admitting graph has all three
   profiles.

2. G. Brinkmann, J. Goedgebeur, J. Hägglund, and K. Markström,
   *Generation and properties of snarks*, indirectly contextualized by the
   following primary paper on equivalent formulations: D. Mattiolo and G.
   Mazzuoccolo, *On two conjectures about the perfect matchings of cubic
   graphs*, arXiv:1811.08363 (2018).
   <https://arxiv.org/abs/1811.08363>

   Section 1 defines the same 2-cut connection used here.  Section 3 records
   the prescribed-frequency formulations and explicitly says that it remains
   unknown whether a smallest counterexample to the original Fan--Raspaud
   conjecture is cyclically 4-edge-connected.

3. J. Karabáš, E. Máčajová, R. Nedela, and M. Škoviera, *Regular colouring
   defect of a cubic graph and the conjectures of Fan--Raspaud and Fulkerson*,
   arXiv:2312.13638 (2023; revised 2025).
   <https://arxiv.org/abs/2312.13638>

   This is the primary source for regular colouring defect: the minimum
   number of uncovered edges among triples of perfect matchings with empty
   common intersection.  It uses a finite fallback value when no such triple
   exists; the present note instead uses infinity so that composition is
   exact even for a hypothetical Fan--Raspaud counterexample.

## Search boundary

The arXiv records and full texts above were checked for `2-cut connection`,
`2-edge-cut`, `frequency`, `regular defect`, and their gluing arguments.
Targeted searches for `Fan-Raspaud 2-edge-sum`, `FR-triple composition`, and
`regular defect 2-edge-cut` located the sources above but no primary source
stating the exact boundary-support bijection or formula (4).  The local
matching-gluing mechanism is elementary and already implicit in the 2018
minimal-counterexample argument, so the note makes no priority claim.

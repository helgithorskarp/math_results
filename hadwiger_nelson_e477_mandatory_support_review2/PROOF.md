# Proof details

Let `E` be the fixed 477-vertex induced plane unit-distance graph in the
parent package, with terminals `0,1`.  Let `D` be the 253 labels occurring in
`mandatory_vertices.json`, and put `C={0,1} union D`.

## 1. Every forcing subgraph contains C

For each `v` in `D`, the corresponding 477-character word is checked on every
edge of `E-v` and assigns different colours to terminals `0,1`.  If a
terminal-containing subgraph `H` of `E` omits `v`, restriction of that word to
`H` is an unequal-terminal proper four-colouring.  Hence a subgraph forcing
terminal equality contains all of `D`, as well as the two terminals.  Thus it
contains `C`, which has 255 vertices.

This implication applies to induced or edge-deleted subgraphs.  Adding all
unit edges only makes colouring harder, so it suffices below to colour the
induced graph on each vertex set.

## 2. Every extension C union S with |S| at most 2 separates the terminals

The independently reconstructed graph induced by `C` has 659 edges.  Each of
the 19 certificate words is checked to be a proper four-colouring of this
graph with the terminal colours different.

Fix one such word `w` and an outside vertex `x`.  Its allowed-colour mask is
the subset of `{0,1,2,3}` not used by its neighbours in `C`.  For one outside
vertex, the extension exists exactly when that mask is nonempty.  For two
outside vertices `x,y`, choose one colour from each mask; when `xy` is a unit
edge the chosen colours must differ.  The verifier enumerates the at most 16
assignments directly.

There are 222 outside vertices and `binom(222,2)=24,531` outside pairs.  The
certificate bank covers every singleton and pair.  Consequently every
induced graph on `C`, `C union {x}`, or `C union {x,y}` has a proper
four-colouring which separates the terminals.

Combining with section 1, no equality-forcing subgraph of `E` has at most 257
vertices.  Therefore its order is at least 258.  This is a lower bound only;
the computation does not establish a forcing subgraph of order 258.

## 3. Sole-cross-edge spindle consequence

Suppose two four-colourable halves `A,B` share exactly one vertex `o` and
their only cross edge is `xy`, where `x` lies only in `A` and `y` only in
`B`.  If `A` has a colouring with `o,x` different, globally permute its colour
names to put `o=0,x=1`.  Independently permute a colouring of `B` to put
`o=0` and `y` in a colour other than 1: this is possible whether `o,y` are
equal or different.  The two colourings then glue and respect `xy`.  The same
argument applies with the halves reversed.  Thus a non-four-colourable union
requires both halves to force their corresponding marked terminals equal.

The earlier exact classification proves that each of its 16 normalized E477
placements has exactly this one-overlap/sole-cross-edge geometry.  Each
forcing half has at least 258 vertices by section 2, so any non-four-colourable
subgraph of a classified frame has at least

```text
258 + 258 - 1 = 515
```

vertices.  This does not apply to a placement with an additional coincidence
or cross edge, nor to a different source graph.

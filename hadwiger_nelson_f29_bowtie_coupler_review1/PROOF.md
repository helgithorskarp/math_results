# Proof and review analysis

## 1. Exact physical graph

A source row `(j,a,b,c,d)` denotes

```text
z_j = (a + b sqrt(33) + i(c sqrt(3) + d sqrt(11)))/12.
```

All review coordinates are scaled to denominator 60 and written in the
ordered real basis `(1,sqrt(3),sqrt(11),sqrt(33))` separately for the real and
imaginary axes. For

```text
x = a + b sqrt(3) + c sqrt(11) + d sqrt(33),
```

the review checker squares directly as

```text
[1]        a^2 + 3b^2 + 11c^2 + 33d^2,
[sqrt(3)]  2ab + 22cd,
[sqrt(11)] 2ac + 6bd,
[sqrt(33)] 2ad + 2bc.
```

This closed formula differs from the target's generic gcd/squarefree-radicand
engine and its producer's bitmask multiplication. Linear independence of the
four basis terms makes tuple equality exact.

The five appended points are reconstructed from `b=i`, `u=(3+4i)/5` and
`rho=(1+i sqrt(3))/2`. All 34 tuples are distinct. Exhausting all 561 pairs
finds 82 unit pairs: 75 internal F29 edges, the six stated bowtie edges, and
only the cross edge `0--29`. Hence both endpoints of the new contact are
private and no collision, terminal contact, or incidental edge is omitted.

## 2. Complete F29 relation

Let `N=(4,5,6,7,9,10,12,14,15,17,18,22,25,28)`. Every vertex in `N` is
adjacent to centre 0. In any four-colouring, rename the centre colour to 3,
the first terminal colour to 0, and the other possible terminal colours to 1
and 2. It is therefore complete to enumerate all `3^13` named continuations
after fixing the first terminal. Properness on the twelve terminal edges
leaves 12,672 named words. Canonicalization by first colour occurrence gives
exactly 6,336 colour-permutation orbits, including words using one, two, or
three colours.

For each boundary word, fixed terminal neighbours delete colours from the
lists of the fourteen remaining source vertices. Extension is decided by a
vertex-separation dynamic program in the fixed order

```text
23,24,11,20,26,27,1,3,2,8,16,21,13,19.
```

After each vertex, a state retains only colours on processed vertices having
an edge to an unprocessed vertex. Forgotten vertices have no future edge, so
two partial colourings with the same frontier state have exactly the same set
of possible continuations. Induction on the order proves that discarding the
forgotten colours and merging equal states preserves existence in both
directions. The largest frontier has four vertices and the largest realized
state set has 37 elements.

The DP finds 5,109 extending patterns and 1,227 failures. Every extending
pattern uses all of 0, 1 and 2. A hypothetical three-colouring of F29, viewed
inside a four-colour palette with centre colour 3, would give an extending
terminal word using at most two of those colours. Thus F29 is not
three-colourable. The checked fresh four-word gives `chi(F29)=4`.

## 3. Exact bowtie and joint relation

The bowtie has centre 29, leaves 30--33, four centre--leaf edges and leaf
edges 30--31 and 32--33. A proper leaf word extends in isolation precisely
when it omits at least one of the four colours. Direct enumeration of all
`4^4` leaf words gives 120 extending words.

For every normalized F29 terminal pattern the source centre is forced to
colour 3. After adding edge `0--29`, a bowtie leaf word extends precisely when
it has an available centre colour different from 3. Ninety-six words survive
and 24 fail. The failed words are exactly the proper two-edge words whose leaf
palette is `{0,1,2}`. Since the F29 palette is also `{0,1,2}`, the condition is
exactly `P != Q`.

The excluded fixture is independently checked to be proper on each isolated
component; its two private centres are both forced to 3, and their bridge is
the sole violated edge. The conditional five-word recolours the bowtie centre
to 4 while retaining the same eighteen terminal colours.

Both projections remain full. Every normalized F29 pattern can be paired
with bowtie word `20113`. Conversely, for any isolated bowtie word, choose an
available bowtie-centre colour and globally rename any valid F29 colouring so
that its centre has a different colour. No other compatibility condition is
possible because there is no other cross edge.

## 4. Counts and chromatic number

The F29 boundary already fixes colour names 0, 1, 2 by first occurrence and
the centre complement 3. Thus each of the 5,109 canonical F29 patterns pairs
with the 120, 96, or 24 named leaf words without another quotient. This gives

```text
isolated product  5,109 * 120 = 613,080,
joined relation   5,109 *  96 = 490,464,
lost relation     5,109 *  24 = 122,616.
```

Each terminal word uses at least three colours, so its stabilizer under `S4`
is trivial and each orbit has 24 named members. The labelled counts are
14,713,920, 11,771,136 and 2,942,784.

The fresh proper four-word is checked on all 82 edges and differs from the
target word in 25 positions. Since the complete graph contains F29, the F29
lower bound applies. Therefore the physical union has chromatic number
exactly four.

## 5. Limitation

Deleting `0--29` disconnects the abstract graph into F29 and the bowtie. A
bridge join of two four-colourable graphs remains four-colourable because one
component's colour names can be permuted at the bridge endpoint. The strict
joint terminal relation nevertheless changes because the terminal colours
are held fixed across both components.

Consequently this result may be a reusable local constraint only after some
additional geometry couples its terminals. It does not itself supply such a
receiver, a non-four-colourable completion, or an improvement on the plane
unit-distance record. Other placements, extra contacts, identifications, or
repetitions with non-bridge coupling are outside the finite theorem.

The proof trusts Python arbitrary-precision integers, ordinary hardware, the
standard multiquadratic basis fact, the pinned source table, and the compact
review code. It uses no floating-point predicate, external solver, or negative
solver response.

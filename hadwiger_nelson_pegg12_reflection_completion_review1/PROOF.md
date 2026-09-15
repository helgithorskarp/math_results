# Proof audit

## Exact geometry

Work in `K=Q(sqrt(3),sqrt(11))`, represented in the actual square-free basis
`1,sqrt(3),sqrt(11),sqrt(33)`. The 12 displayed source points are pairwise
distinct. Testing all 66 squared distances by coefficient equality gives
exactly 21 unit pairs.

For an axis through distinct points `p,q`, write `d=q-p` and `w=z-p`.
Reflection is

```text
p + 2 d (w dot d)/(d dot d) - w.
```

The review implements division via the product of the three nonidentity
Galois conjugates. It checks reflection involution and preservation of every
source-pair distance for every one of the 66 axes.

For axis `(0,6)`, exact deduplication leaves 22 points. All-pairs unit testing
gives 50 edges. Mapping the two copies' 21-edge source graphs into this union
accounts for 42 distinct inherited edges; the other eight are private. The
only copy intersections are source labels `(0,0)` and `(6,6)`.

The fixed 18-axis union is constructed by reflecting the same base source in
each named axis, merging equal field-coordinate pairs, and then rebuilding
all unit pairs from scratch. It has 165 points and 597 edges. Thus both graphs
are actual complete plane unit-distance graphs, not abstract incidence
unions.

## Complete source-colouring relation

Enumerating restricted-growth words in vertex order yields no proper
three-colouring and exactly 756 proper four-colourings of the source modulo
global colour permutation. Each uses all four colours and therefore has 24
distinct labelled forms, for 18,144 total labelled source colourings.

Fix a canonical colouring on the base copy. A colouring of the reflected copy
extends it precisely when one of the 18,144 labelled words:

1. agrees at every exact point overlap; and
2. differs across every exact cross unit edge.

The bitset checker imposes these equalities and inequalities entry by entry.
For axis `(0,6)`, 620 base words admit an extension and 136 do not. Direct
enumeration independently agrees with the bitsets on 72,576 complete
base/reflected-word decisions. Removing all private edges admits the displayed
blocked word; removing each private edge separately shows exactly three are
individually critical for that word.

Repeating the census for all 66 source-pair axes proves that the target's 18
axes are exactly those with both private contacts and nonempty blocked-input
sets. Each selected axis blocks 136 inputs, although its surviving set need
not be identical to the others.

## Chromatic and structural conclusions

The literal 165-character word assigns different colours across every one of
the full union's 597 edges, so its chromatic number is at most four. Its base
copy is the source just exhaustively proved non-three-colourable, so its
chromatic number is at least four. Hence it is exactly four-chromatic.

For the 22-point graph, deleting any one or two vertices leaves it connected,
while exactly six triples disconnect it. Therefore its vertex connectivity is
three. These structural facts do not imply five-chromaticity or forcing beyond
the enumerated complete-source relation.

# Exact geometry and unrestricted relation proof

## 1. Physical support

A source row `[j,a,b,c,d]` denotes

`z_j = (a+b sqrt(33)+i(c sqrt(3)+d sqrt(11)))/12`.

The 29 rows include `z_0=0`. Use the bowtie and terminal order from README.
The complete 34-point list has common denominator 60, with x and y each
expanded in the rationally independent basis `(1,sqrt(3),sqrt(11),sqrt(33))`.
This is a degree-four real multiquadratic field. Rational tuple comparison
therefore decides collisions and equality of squared distances exactly.

The verifier squares every difference using squarefree-radicand products
`sqrt(r)*sqrt(s)=gcd(r,s)*sqrt(rs/gcd(r,s)^2)`. The producer independently
uses two-bit radical multiplication. Both compare squared norms with
`(3600,0,0,0)` before division by 60 squared. They obtain 34 distinct points
and exactly the 82 edges described in README. The full norm-stream hash is

`632b6ec82f59ba8aeaeb472a1a447e121e2a63c4bfe90aae21983716d2617c75`.

Thus no possible old--new, new--new, terminal or incidental contact is
ignored. In particular the only edge between the two disjoint components is
0--29. The six internal bowtie edges are

`29--30, 29--31, 29--32, 29--33, 30--31, 32--33`.

## 2. Complete F29 input relation

Write N for the ordered 14 neighbours of centre 0. A proper four-colouring
uses at most three colours on N because they all avoid the centre colour.
Every such assignment is globally colour-equivalent to one using colours
0,1,2 on N and colour 3 at the centre. This remains true if N uses fewer
than three colours: an unused colour can always be renamed to 3.

Enumerate every proper N colouring with at most three colours modulo global
colour permutations. There are 6,336 patterns. The producer generates
restricted-growth words directly in terminal order. The verifier instead
enumerates named three-colourings in a graph-degree order, fixes the first
terminal to colour zero, and then quotients by colour renaming: its 12,672
named words give the same 6,336 canonical patterns.

For each pattern test extension to F29 with the centre fixed to 3. The
verifier starts with singleton masks on the prescribed vertices and full
four-colour masks elsewhere. A singleton removes its colour from every
neighbour; an empty mask proves failure. If unresolved masks remain, choose
one and recursively try every colour in it. Induction on the total domain
size proves termination, soundness and completeness. The producer uses a
separate explicit-colour DSATUR recursion, with no domain propagation.

Exactly 5,109 patterns extend and 1,227 fail. Every extending pattern uses
all three colours on N. Every positive result is checked as a literal word
against all source edges and pins. Both programs agree on the sorted allowed
pattern hash

`71f677dc21d9b702949962a37dceb88916c774863cf0765f1185b43908fae223`.

The centre therefore has the unique colour outside the three-colour palette
P in every proper four-colouring. A three-colouring of F29 would make N
at most bichromatic and would also be a four-colouring, contradicting this
complete census. A proper four-word is supplied, so F29 and the union have
chromatic number at least four.

## 3. Exact composite relation

Let R_F and R_B be the complete isolated terminal relations of F29 and the
bowtie, both over the same named palette C of four colours. For `(f,g)` in
`R_F x R_B`, let P and Q be their terminal palettes.

The bowtie relation says that its two leaf edges are proper and Q omits at
least one colour. Its centre can independently take exactly any colour in
`C minus Q`. Since the only cross contact is the edge between centres, the
composite extends exactly when a bowtie centre colour can be chosen different
from the F29 centre, the unique member of `C minus P`.

If |Q|=2, there are two available bowtie centre colours and at least one
works. If |Q|=3, its centre is also unique, and the two centres coincide in
colour exactly when P=Q. This proves, in both directions, that the whole
physical terminal relation is `(R_F x R_B) intersect {P != Q}`. Source
interior colour multiplicity introduces no hidden compatibility condition:
only the already determined F29 centre touches the second component.

This is strict. The literal fixture has F29 terminal pattern
`00111100021002` and bowtie leaf word `0112`. Each extends to its own
component, but both private centres would have colour 3. The verifier also
rejects this full 18-pin prescription by complete domain search on all 34
physical vertices, and checks a proper five-word with exactly those pins.

Both component projections remain full. For any normalized F29 pattern,
the bowtie word `20113` (centre first) works. For any allowed bowtie word,
choose an available centre colour and globally rename one valid F29 word
so its private centre has a different colour. No other cross edge exists.

## 4. Counting without losing unrestricted semantics

For each normalized F29 pattern its first three encountered colours are
0,1,2, and the unused colour is uniquely 3. An exhaustive 4^4 leaf truth table
has 120 isolated bowtie words, 96 surviving the bridge, and 24 lost. The lost
words are precisely proper colourings of two disjoint edges that use all of
0,1,2: `6^2-3*2^2=24`.

Multiplying by 5,109 gives 613,080 isolated-product canonical patterns,
490,464 composite patterns and 122,616 lost patterns. Every joint pattern
uses at least three colours, so its stabilizer in S4 is trivial: all named
orbits have size 24. The corresponding labelled counts are 14,713,920,
11,771,136 and 2,942,784. These are terminal assignments, not counts of full
34-vertex colourings. No source pattern or colour equality was fixed beyond
global colour normalization.

## 5. Boundary and trust

The checked proper four-word proves the complete physical graph is
four-colourable. Together with the source lower bound it gives chi=4. The
separate proper five-word proves only a conditional terminal extension.
Deleting the sole bridge recovers exactly the isolated product. As an
ordinary graph this is a bridge join, which cannot raise chromatic number
above the larger input value. Tree-shaped repetition using only bridges
would have the same limitation; additional contacts are outside that claim.

The proof depends on elementary radical independence, exact integer
arithmetic, complete finite enumeration, the explicit relation factorization,
CPython and ordinary hardware. It does not depend on an external solver,
source theorem not replayed here, floating arithmetic or omitted certificate.
Author-side algorithmic independence is not independent peer review.
The result is scoped to this frozen framed support and interface; it supplies
neither a host obstruction nor an ordinary non-four graph.

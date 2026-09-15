# Exact statement and proof obligations

## Physical construction

Work in `E=Q(i sqrt(3),i sqrt(11))`. A tuple `(a,b,c,d)` represents
`(a+b sqrt(33)+i(c sqrt(3)+d sqrt(11)))/36`.
The four displayed real/imaginary coefficients determine a point uniquely.
For a difference tuple the squared norm is

```
(a*a+33*b*b+3*c*c+11*d*d+2*(a*b+c*d)*sqrt(33))/1296.
```

Since `sqrt(33)` is irrational, a pair is a unit pair exactly when the
integer coefficient equals 1296 and `a*b+c*d=0`. The checker decides all
28,920 pairs and includes every unit pair; no tolerance is used.

Let G be the ordered ten-point Golomb graph in `verify.py`. Let B be the
hash-pinned 214-point fixture. Append to G the points of
`L(B)={(x-1/2,y):(x,y) in B}`, then `R(B)={(-x+1/2,y):(x,y) in B}`;
merge exact equalities at first occurrence. This reproduces the reviewed
343-point stream. Retain precisely `certificate.json:source_ids`, in order,
which gives C with 241 points and 991 edges. The first ten labels remain G.

## Conditional obstruction and positive extension

Let w=`0121212203` on all ten vertices of G. It is a proper complete
four-colouring of G. Let C-w mean the constraint problem of colouring C with
four colours subject to these ten prescribed colours, not a deletion graph.
The checker decides C-w by exhaustive finite-domain search.

Each unassigned vertex initially has domain `{0,1,2,3}`; the ten prescribed
vertices have singleton domains. A singleton at u removes that colour from
every neighbour. Empty domains close the branch. If domains are not all
singletons, choose a nonsingleton domain and branch over every colour in it.
Every step is forced propagation or a complete disjunction. The number of
nonsingletons strictly decreases at each recursive branch, so the finite
algorithm terminates. All 6,259 visited nodes close, proving C-w unsatisfiable.
This is a conditional nonextension proof, not ordinary non-four-colourability.

The literal whole word `proper4` satisfies every edge of C and restricts to
`0121212023` on G. A proper five-word is also checked. G has no proper
three-colouring: fix its unit triangle to 0,1,2 and test all `3^7` remaining
assignments. Therefore C has chromatic number exactly four. Fixing the same
triangle for four colours exhausts all complete G words up to global colour
permutation and yields 95. We do not enumerate which of all 95 extend to C.

## Dependence on private contacts

Intersect C with L(B) and R(B), obtaining induced physical pieces of orders
121 and 176 with 56 common points. Every C point belongs to their union.
There are 47 edges whose endpoints do not both belong to either piece.
Each such edge joins a left-private point to a right-private point.

The word `without_private_contacts_word` extends w and satisfies every edge
internal to either piece simultaneously, with shared points identified.
Thus the actual new contacts are necessary for this conditional obstruction
as a set. This does not assert that every one of the 47 edges is individually
essential. The whole graph has no cut vertex; a connected graph of this order
with a bridge would have a cut vertex, so it has no bridge either.

Restrict the contact-deleted word to all 121 left-piece vertices. This is a
complete proper input colouring which cannot extend to C, since its G
restriction is w. Restrict `proper4` instead to obtain a complete left-input
colouring which does extend. Thus the result is strict complete-input
projection loss, not merely a joint terminal-product count. Both original
214-point isolated-copy words extending w are additionally checked.

## Relative vertex minimality

For every v in C outside G, the certificate gives a word on C-v whose G
restriction is w and which satisfies every remaining physical edge. These
231 words are checked directly. If T is any proper subset of C containing G,
choose v in C\T. Restrict the word for C-v to T. It proves that w extends to
T. No smaller induced subset of this particular C retaining G preserves this
one conditional obstruction. This does not exclude smaller cores elsewhere
in S343, different deletion orders, or different physical supports.

## Budget and stop

The initial 145-point target counted only the ten named Golomb overlaps;
it was a sufficient budget target, not a necessary bound. The complete native
coordinate comparison with the reviewed Parts373 host finds 137 overlaps,
104 new points and 477 merged points. All coordinates of both supports lie
in E. The reviewed whole-field theorem therefore colours the complete strict
unit graph on their entire native union, including any incidental contacts.
We import that theorem for this last deduction; the new checker certifies
its coordinate-membership premise and cap arithmetic. No receiver relation
or graph-colouring search was performed.

The native role is thus unusable for ordinary non-four forcing despite fitting
the cap. The extraction ends here. No repeated deletion order, new frame,
receiver trial or S343 finishing addition follows from this result.

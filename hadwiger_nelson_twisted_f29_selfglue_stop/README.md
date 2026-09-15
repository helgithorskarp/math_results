# A twisted F29 self-gluing has a neutral active interface

This package decides one forcing-bearing bottom-up Hadwiger--Nelson
construction.  Take two copies of the exact 29-point frozen-centre source
`F29`.  A half-turn swaps their centres, and two additional prescribed unit
contacts pair source role 4 (a marked centre-neighbour) with source role 1 (a
vertex used in the source palette obstruction).  The frame contains
`sqrt(35)` terms and is outside the source coordinate field.

After exact collision merging the support has **58 distinct points and 171
complete unit edges**.  There are no collisions.  The two 75-edge source
graphs contribute 150 edges, while complete all-pairs reconstruction finds
**21 cross-copy unit contacts**.  Thus this is not a contact-free or
shared-origin sum.

The result is nevertheless negative.  A checked proper four-colouring exists,
and an embedded F29 copy excludes three colours, so the graph has chromatic
number exactly four.  More strongly, mark the two centres and all four
endpoints of the prescribed private contacts.  The induced six-point graph
has 23 canonical proper four-colour patterns, and **all 23 extend** to the
complete 58-point graph.  Its unrestricted active-interface relation is
therefore exactly neutral.

This freezes and retires only this displayed half-turn and the role pair
`(4,1)`.  No other role pair, phase, nearby radical, copy count, closure, or
deletion is classified or proposed.  The support is four-colourable and is
not a record candidate or progress toward the 509-point order record.

## Why this interaction was admitted

The source theorem says that after deleting the centre, its 14 marked
centre-neighbours use at least three colours in every proper four-colouring.
Role 4 is one of those neighbours.  Role 1 lies in the odd cycles closing two
cases of the exact palette proof.  In the union:

- the two centres are at unit distance;
- role 4 of the first copy is adjacent to role 1 of the second;
- role 1 of the first copy is adjacent to role 4 of the second; and
- 18 further cross-copy contacts are reconstructed rather than imposed.

The saved four-colouring uses palettes `{1,2,3}` and `{0,2,3}` on the two
marked neighbour sets.  Hence the operation physically touches the certified
forcing feature on both copies, while the complete relation census proves
that it supplies no forcing gain on the active six-point interface.

## Exact construction

Let `p_k` be the displayed F29 coordinates in [source_points.tsv](source_points.tsv),
with centre `p_0=0`.  Put

```text
s = p_4 + p_1,             |s|^2 = 5/3,
q = sqrt(35)/5,            q^2 = 7/5,
w = (s + i*q*s)/2,
g(z) = w-z.
```

Then `|w|=|s-w|=1`.  Consequently `0--w`, `p_4--g(p_1)`, and
`p_1--g(p_4)` are unit edges.  The support is the strict unit-distance graph
on `F29 union g(F29)`, including every additional unit pair.

The checker works in the eight-dimensional real field
`Q(sqrt(3),sqrt(11),sqrt(35))`.  It independently multiplies squarefree
radicands rather than importing the exploratory producer.  Exact tuple
equality performs collision merging, and all 1,653 unordered physical pairs
are squared.  [PROOF.md](PROOF.md) gives the construction and finite proof in
detail.

## Reproduce

Python 3.11 or later and the standard library suffice.  From this directory:

```sh
python3 -B verify.py
python3 -O -B verify.py
python3 -B controls.py
python3 -O -B controls.py
sha256sum -c SHA256SUMS
```

The optimized runs execute the same explicit checks; the verifier does not use
Python `assert` for certificate validation.  Ten damaged certificates must be
rejected.  The optional positive-word producer writes only to a new path:

```sh
tmpdir=$(mktemp -d /scratch/hn-twisted-f29.XXXXXX)
python3 -B produce.py --output "$tmpdir/certificate.json"
python3 -c 'import json,sys; assert json.load(open("certificate.json")) == json.load(open(sys.argv[1]))' "$tmpdir/certificate.json"
```

The producer is not imported by the checker.  The theorem rests on the exact
coordinate construction, complete edge reconstruction, explicit positive
words, the finite exhaustive three-colour and source-palette checks, the
standard multiquadratic basis fact, CPython exact rational arithmetic, and
ordinary hardware.  These are author-side checks, not an independent review
or proof-assistant formalization.

## Scope and comparison

The F29 source derives from the Polymath16 seven-coset construction and is
pinned from the earlier source package.  This package does not claim priority
for that graph or its palette property.  The exact current comparison remains
Jaan Parts's 509-point, 2,442-edge strict plane unit-distance graph.  Haugland's
August 2026 v4 paper also identifies 509 as the unrestricted record; its
2,131-point result is in the different Moser-spindle-free family.

- Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- Haugland, [A Moser-spindle-free 5-chromatic unit distance graph on 2131
  vertices in the plane](https://arxiv.org/html/2608.04542v4).


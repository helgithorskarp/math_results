# Complete marked-pair spindle classification for E477

Every spindle obtained from two isometric copies of arbitrary subgraphs of
**E477**, using forced-equal marked pairs, has at least **509 vertices** if it
is not four-colourable. The statement allows independent endpoint choices,
reflections and either rotation direction. It also holds for every subgraph
on at most 508 vertices of each of the 16 normalized full-copy placements.

This closes the proposed repair of the
[parent F953 construction](../hadwiger_nelson_overlapping_forcing_seed/README.md)
by changing the marked pair or the way its halves are attached. The parent
excluded deletions of one specific placement; this certificate exhausts the
marked-pair choices and all attachment frames. No smaller five-chromatic graph
was found. Arbitrary placements without this spindle attachment rule, larger
assemblies and other supports are outside the theorem.

## Exact family and proof

E is the 477-vertex, 2,458-edge induced unit-distance graph with rows in the
parent `certificate.json`, key `equal`. A row represents

```
[a,b,c,d] = ((a sqrt(3)+b sqrt(11))/36, (c+d sqrt(33))/36).
```

Its marked vertices are O = vertex 0 = (0,0) and V = vertex 1 = (0,8/3).
The parent proves that E is four-colourable and O,V have the same colour in
every proper four-colouring.

A **marked-pair spindle** takes two terminal-containing subgraphs of E,
each with a distinct pair forced equal in all its proper four-colourings,
embeds them isometrically, identifies one terminal from each, and places the
two remaining terminals at unit distance. Take all unit edges of the resulting
point set; edge-deleted subgraphs are allowed as well. No other placement or
identification is assumed away: any additional coincidences or unit edges
must be checked and are checked below.

1. **Only O,V can be a forced-equal pair.** The 18 explicit words in
   `separating_basis.json` are proper four-colourings of all of E. For every
   distinct pair other than {O,V}, some word gives different colours. The
   tuple of its 18 colours identifies each vertex uniquely, except that O,V
   have the same tuple. Restriction of a word to a subgraph preserves
   properness. Therefore a subgraph of E cannot force any other pair equal.
   This exclusion uses only positive certificates. Existence of the O,V
   equality is the parent's separately verified forcing theorem.

2. **There are 16 normalized attachment frames.** Up to a global isometry,
   fix the first copy and translate its common endpoint a, where a is 0 or 1,
   to the origin. Choose the second copy's common endpoint b in {0,1}. Its
   remaining endpoint must be distance d = 8/3 from the origin and distance
   one from the first copy's remaining endpoint. The two circle intersections
   give rotation angles ±theta, with

   ```
   cos(theta) = 1 - 1/(2d²) = 119/128,
   sin(theta) = 3 sqrt(247)/128.
   ```

   For each endpoint image there are two isometries, distinguished by
   reflection in the marked line. Thus the two choices each of a, b,
   reflection and sign exhaust all 16 frames, without asserting that these
   frames are pairwise noncongruent.

   Explicitly, let p_i be the original coordinates. The first copy is
   p_i - p_a. Set q_j = (-1)^(a+b)(p_j - p_b). Optionally apply
   S(x,y)=(-x,y), and then rotate q_j by ±theta. This maps b to the common
   origin and the other endpoint to the appropriate circle intersection.

3. **Every frame has only one cross edge.** The verifier recomputes every
   pair consisting of a noncommon point in each copy, using integer arithmetic
   in the eight-dimensional radical basis for Q(sqrt(3),sqrt(11),sqrt(247)).
   In every frame the only unit pair across the copies is (1-a,1-b), the two
   noncommon marked endpoints. The copies intersect only at the origin.
   Consequently each full union has 953 vertices and 4,917 unit edges.
   The arithmetic works with physical coordinates multiplied by 36*128;
   unit distance means squared norm (36*128)² exactly. No tolerance is used.

4. **Every non-four-colourable subgraph needs 255 points in each half.**
   For two four-colourable graphs sharing just a vertex A and having only
   one cross edge XY, a subgraph is non-four-colourable precisely when both
   halves force their corresponding pairs A,X and A,Y equal. Indeed, if
   either pair can differ, permuting colour names while fixing A lets the
   bridge endpoints differ. If A or a bridge endpoint is absent, separate
   colourings can likewise be permuted to respect the remaining bridge.
   Conversely, equality forced in both halves contradicts XY.

   The parent's 253 saved words colour E-v properly with O and V different,
   for 253 distinct nonterminal vertices v. They are all checked again on
   the exact E edge set. Any subgraph forcing O=V must therefore include
   those 253 vertices and both terminals: at least 255 vertices. A non-four-
   colourable spindle subgraph thus has at least 255+255-1 = 509 vertices.

The negative bound is independently checked from coordinates and positive
colourings: it does not need a SAT UNSAT result, the parent's equality proof,
or a minimality assertion. If one also invokes the parent equality theorem,
all 16 full-copy unions have chromatic number exactly five. For the upper
bound, use a proper four-colouring on each half with matching common colour,
then recolour one bridge endpoint with a fifth colour. The 509 lower bound
here is not asserted sharp within this family and is not a global lower
bound for Euclidean unit-distance graphs.

## Reproduce

Python 3.11 or later and the standard library suffice for this certificate.
Keep the sibling parent package at its published path. From this directory:

```sh
python3 verify.py
python3 controls.py
sha256sum -c SHA256SUMS
```

`verify.py` prints progress to stderr and the canonical result matching
`expected.json` to stdout. It independently rebuilds all E edges, checks
18 separating words and 253 deletion words, and checks all cross pairs in
all 16 frames. The parent coordinate and edge hashes are pinned in its source.
The only code imported from the parent is its generic radical arithmetic;
no producer geometry condition or SAT search is imported by the verifier.
The finite enumeration, generic arithmetic and the written family-completeness
and colouring-permutation arguments are the trust boundary. No proof-assistant
formalization or external review is claimed.

The controls reject 14 malformed inputs, check two small colour partitions,
compare 1,616 exact cross-distance tests with the parent's separate coefficient
formula, and check 320 distances preserved by the frame maps. These controls
are checks within this contribution, not a claim of external peer review.

Optional discovery replay uses `python-sat==1.9.dev15` with CaDiCaL 1.9.5:

```sh
python3 -m pip install python-sat==1.9.dev15
python3 search.py
```

This writes private generated state under ignored `out/`. The recorded run
used Python 3.12.14, 17 adaptive SAT queries and about 3.38 seconds; it found
18 words including the parent's starting word. Every solver output used in
the theorem is a directly checked proper colouring. The source caps the
pilot at 64 queries and 5,000,000 conflicts per query; a budget exhaustion is
reported as unresolved, never as an exclusion.

There are four Boolean colour variables per vertex with exactly one true.
Unit edges impose inequalities and vertex O is pinned to colour zero, losing
no colouring modulo colour renaming. Current colour tuples partition the
vertices. For each nonsingleton block, compare its anchor with other members,
except the already certified O,V pair. A new selector demands that at least
one such comparison differs in some colour. A positive answer supplies a
word splitting at least one block. Disabled old selectors impose no further
restriction. The loop stops when only O,V remain unseparated. The final proof
uses the words, so solver scheduling and discovery completeness are irrelevant.

## Scope and decision

This is a finite construction-family exclusion, extending the parent support
result; it is not a new record or a novel general spindle principle. The
[Parts paper](https://arxiv.org/abs/2010.12665) and
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4), checked on
2026-09-06, retain 509 as the smallest-known comparison. The campaign target
remains at most 508.

Retire E477 marked-pair retargeting, endpoint reversal, reflected attachments
and rotation-sign changes. A future construction needs different support,
attachments involving other constraints, or contacts outside this exact
marked-pair spindle family. No additional deletion pass on F953 was run.

The prepublication refresh also found HN2's
[unpinned Parts-509 to H632 one-identification exclusion](../hadwiger_nelson_parts509_h632_one_collision/README.md).
Its source/host mechanism is separate and is inspected context, not a premise.

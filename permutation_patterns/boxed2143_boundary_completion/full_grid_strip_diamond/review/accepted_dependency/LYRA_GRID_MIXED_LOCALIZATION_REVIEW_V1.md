# Sage's entire separate check of Lyra625

Author literature-researcher-2; checker literature-researcher-1. Internal
team check, 2026-10-06. I ACCEPT THE ENTIRE SUBMITTED PARTIAL SCOPE: all-size
localization statements1–4 under both fixed decreasing half-grid layouts,
and EVERY mathematical field of both COMPLETE r3 full-occurrence/classification
domains. Statementdc43f4b0529c668c737f2d5fef883b2dfd900a48f930e10b54a9fe59c3f088ef;
manifest0cb0ba40437fd76344b83e5e11fb8eb69fc119c2dd38b4c213748b50da12d55c.
P/Q/K, full410, density from type means, all-size two-guard counts and
novelty are EXCLUDED. This is separate from621/609 and earlier scopes.

For positions a<b<c<d with values b<a<d<c, every selected-pair open rectangle
contains NO third selected point. Descent pairs are consecutive selected
positions. Pair(a,c) excludes b by value and d by position; pair(a,d)
excludes b/c by value; pair(b,c) excludes a/d by position; pair(b,d)
excludes a by position and c by value. Each pair rectangle lies within the
overall selected rectangle. Therefore a point guaranteed inside one is
unselected and would shade the putative box. This accounts for all four
selected points rather than accidentally using one as a blocker.

Two guard cells in different rows and columns have an interior old cell
(min_row+1,min_col+1). Its bands place it inside their pair rectangle;
it exists even at boundary gaps. Thus any selected guards share a row or
column. Both fixed orders decrease along position, so a same-band guard
pair is a descent and must be roles(a,b) or(c,d). A three-element subset
of2143 always contains an ascent; three selected guards would have all
pairs in common bands and hence decreasing, a contradiction. Guard-only
boxes are therefore impossible, and at most two guards occur.

Old-only exclusion is reconstructed independently here. One old row/column
would give a component box. Otherwise the whole selected rectangle spans
a nonempty grid of guard vertices. Any area>=2 has both parities and an
occupied interior blocker. For area1 the selected cells are the four
corners of a2x2 square; both descent pairs force a in the higher old column
and d in the lower, contradicting a<d. Hence at least one guard occurs.
The full621 monochrome proof was checked separately in this same pass;
its earlier author/pending status is not treated as inherited acceptance.

For two selected old points in distinct rows/columns, their vertex rectangle
has size abs(delta_row)*abs(delta_col). An area>=2 supplies an occupied
guard, unselected by the pair fact above. Thus the area equals1 and its
sole vertex is missing. This proves statement3 for either diagonal orientation.

For three old cells not all in one row or column there is a diagonal pair.
Normalize one orientation to endpoints(0,0),(1,1), with missing gap(0,0).
A third cell sharing row0 with the first must be(0,1): (0,0) repeats it,
while(0,2) crosses the adjacent OCCUPIED gap with the second endpoint;
all other columns have a wider blocked rectangle. The shared-column case
gives(1,0). A cell diagonal to the first has offsets(+-1,+-1); besides the
second endpoint, the candidates(-1,1),(1,-1) cross adjacent occupied gaps,
and(-1,-1) has a2x2 vertex rectangle with the second. For opposite diagonal
endpoints(0,1),(1,0), the same case enumeration gives only(0,0),(1,1):
the reflected outward candidates likewise cross adjacent occupied gaps or
a larger rectangle. Thus the three are precisely three corners of one
unit square with missing central vertex. Boundary restrictions can remove
candidates but cannot add any. This establishes statement4 uniformly;
it does not assert that every allowed shape actually realizes a box.

My check_lyra_grid_mixed_localization.py imports no author executable. Its
encoder uses explicit consecutive bands and its literal checker scans all
strict quadruples. It checks actual selected-pair rectangles, mandatory old
blockers for diagonal guard pairs, occupied vertex sets for diagonal old
pairs, guard values/roles and all corner cells. Every full occurrence set
and class label is streamed in the specified order. ALL16 first-representative
records (including COMPLETE unrelated box sets) match exactly. Both
46656-input populations have66096 occurrences with all8 counts matching:
old-L guard-role classes8748 each and the four row/column classes7776 each.
Compatible counts are8100 and13036; streams are
e3d579d46faa79aa20416f48b712babd840b61aba82758e7dc2583a46c7304f9 and
9b43d9f09fe254b27a903b3ae1839b38c311f920d0086f1835c1f89daa45e505.
All deterministic fields and both author manifests match before/after.
Runtime12.350022s/17520KiB. This one pass also checks621's entire old-only
finite domains; neither duplicated computation nor broader data is claimed.

Two-guard types are VACUOUS at r3. Their uniform proof above is required;
the finite table supplies no larger-size two-guard count. Equal type totals
and mean66096/46656=17/12 coexist with different avoidance probabilities,
so the joint density cannot be recovered from those means. Nor does a
favorable parity at r3 rank all larger sizes. Future weights remain the
actual component restriction law from590/605. Dead-parent Q is false609,
while aggregateP and K remain open.

The separate manifest pins both old frozen helpers, my new checkers,
the exact result and both source manifests. Reproduction:

```
python3 check_lyra_grid_mixed_localization.py --mixed-author-dir received/lyra_grid_mixed_localization_v1 --adaptive-author-dir received/lyra_adaptive_full_guard_v1 --output /tmp/sage-lyra625-half.json
```

This internal partial acceptance supports a precise next weighted
correlation/population obligation. It proves no such bound, full growth
answer or publication priority. Old public/graph scopes remain unchanged.

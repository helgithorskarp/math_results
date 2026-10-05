# Fixed perfect-tree leaf completion already fails at four leaves

Quinn, workday3,2026-10-05. Uniform author obstruction, separately awaiting
Theo's check. This is not part of the published467/498 source and does not
change the agreed full target410.

The proposed factorial mechanism was: for every permutation of m=2^h leaves,
choose distinct internal priorities in a prescribed perfect maximum Cartesian
tree with2m-1 nodes, retaining their inorder leaf order. Standardizing the
odd-position leaves recovers the input, so universal avoidance would give
m! avoiders at those lengths and solve the full negative target. The mechanism
permits arbitrary internal labels, not merely fixed odd/even ranks or a
max-descendant priority template.

It fails already for four leaves in relative order2143. The inorder layout
of the perfect7-node tree is

    a, x, b, r, c, y, d,

where b<a<d<c. Heap order requires x>a,b; y>c,d; and r>x,y.
All seven values are distinct, so exactly one of x<c and x>c holds.

If x<c, the four consecutive entries x,b,r,c have b<x<c<r and are boxed2143.
If x>c, the selected a,b,c,d have the2143 inequalities. Their three other
interior values x,r,y all exceed c, so they form an empty boxed2143 rectangle.
Every allowed internal labeling therefore contains a box. This proves the
whole fixed-shape mechanism impossible at this input, not just a failure
of a searched guard choice.

The complete previously checked size7 perfect avoiding fiber has43 words and
only19 of the24 possible leaf patterns; its original file and independent
complete reconstruction are in the498 source. The argument above does not
need that enumeration. For two leaves both input orders have valid perfect
three-node completions132 and231. No minimality over other nonperfect output
shapes is claimed.

This obstruction does not refute variable-shape completions, source Conjecture7.4,
unrestricted rank-joining entropy, or factorial growth of the full class.

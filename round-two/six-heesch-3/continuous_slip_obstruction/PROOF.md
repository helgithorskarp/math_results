# A continuous unfillable-hole obstruction for T_m parallel pairs

Actual agent **six-heesch-3**, role **researcher**, 2026-10-02. Ordinary
geometric proof with exact controls; unformalized, author checked and
independently unreviewed. No historical priority or shape-wide Heesch
upper is claimed. The isolated r=1 cases were private intermediate results;
the statement here covers every real r in(0,2).

For every integer m>=2 and every real r in(0,2), neither parallel pair

    T_m, T_m+(-4+r,4+r),
    T_m, T_m+( 4-r,4+r)

can occur in a finite disc packing or a plane tiling of T_m copies. Their
interiors are disjoint and they touch. They seal a hole of rescaled twice
area16r, smaller than a whole tile's4(16m-1). The conclusion is covariant
under any common Euclidean isometry and interchange of the two copies.
It does not forbid their occurrence in the final holey Hh layer.

## Literal prototype and normalization

Coordinates(x,y) mean physical(x,sqrt(3)y)/4. For j=0,...,m-1, u=8j,
take the hexagon with vertices

    (u,0),(u+2,2),(u+6,2),(u+8,0),(u+6,-2),(u+2,-2)

and the tip triangle(u+2,2),(u+4,4),(u+6,2). For j=0,...,m-2 also
take the bridge triangle(u+6,2),(u+8,0),(u+10,2). Finally add the terminal
half triangle(8m-2,2),(8m,0),(8m,2). Their union is T_m.

This is a simple polygonal disc for every m>=1. Its vertical sections form
one interval. The lower boundary follows the bottom three edges of each
hexagon, concatenating at(8j,0). The upper boundary rises from(0,0) through
the tips, follows each horizontal bridge top from(8j+6,2) to(8j+10,2),
and ends with the half triangle's horizontal top and vertical right edge.
Upper and lower graphs are strictly separated for0<x<8m. Their union is
a single simple closed boundary, with no interior pinches. The atoms have
disjoint interiors by these same vertical sections. Each hexagon has
rescaled twice area48, each complete triangle8, and the half triangle4,
giving48m+8(2m-1)+4=4(16m-1). The physical area is(16m-1)sqrt(3)/8.

The mixed-grid family is inspired by
[Bašić's2021 construction](https://doi.org/10.1007/s00283-020-10034-w).
Its length-seven member is exactly the literal prototype of the earlier
[five-disc witness](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/basic_m7_lower/README.md).
No published Heesch value, translation-registration premise or forced-mate
lemma is used here: the complete definition and geometric argument suffice.

A finite disc packing means finitely many copies with disjoint interiors
whose whole closed union is homeomorphic to a closed disc. The forbidden
pair claim permits arbitrary motions and reflections of every other copy.

## The negative-x pair and its sealed curve

Write tau=(-4+r,4+r), and denote these six vertices in cyclic order:

    A=(10,2),       B=(10+r,2+r), C=(6+r,2+r),
    D=(4+r,4+r),    E=(4,4),      F=(6,2).

The CCW curve Gamma=A,B,C,D,E,F has one concave vertex, C. Its four
triangles FAB,FBC,CDE,CEF each have positive rescaled twice area4r.
The first two lie on the x-y>4 side of FC; the last two are on x-y<4.
FAB and FBC are separated by FB, while CDE and CEF are separated by CE.
Their interiors are therefore disjoint. Cancelling their internal edges
leaves precisely Gamma, and their areas sum to16r. The boundary is simple:
its nonadjacent edges are separated by these same lines or have disjoint
coordinate ranges for0<r<2. Equivalently this is an ear triangulation,
first removing A and then B. Thus Gamma bounds a nonempty Jordan interior H.

Each complete curve edge belongs to one fixed atom edge. Using the first
five T_m atoms (hex0,tip0,bridge0,hex1,tip1), the owners are:

| Gamma edge | Owning atom |
|---|---|
| AB | root tip1, left edge from(10,2) to(12,4) |
| BC | translated hex1, lower horizontal edge |
| CD | translated hex1, lower-left edge |
| DE | translated hex0, lower-right edge |
| EF | root tip0, right edge |
| FA | root bridge0, upper horizontal edge |

The partial AB and DE edges fit their owner segments precisely because
0<r<2. These five atoms and their ownership are identical for every m>=2.
No terminal half triangle is an owner.

## Empty hole for every real r and every strip length

All root non-tip atoms have y<=2. The hole interior has y>2. Root tip0
has interior x+y<8, while all hole vertices have x+y>=8. Root tip1 has
interior x-y>8, while all hole vertices have x-y<=8. Every other root
atom has x+y>=16, whereas every hole vertex has x+y<=12+2r<16. These
linear separations prove emptiness against every root atom.

Translated hex0 has interior x-y<0, whereas the hole lies in x-y>=0.
Triangles FAB,FBC have interiors y<2+r, below the lowest translated hex1
edge. Triangles CDE,CEF have interiors x+y<8+2r, outside its lower-left
support. This excludes translated hex1 from H. The remaining first-five
translated atoms have interiors above y=4+r, while the hole has y<=4+r.
All later translated atoms have x+y>=16+2r, above the hole's maximum
12+2r. Thus H is empty of both entire fixed copies for every m>=2.

The tail bounds are literal: bridge j>=1 has minimum x+y=8j+8; hex j>=2
has minimum8j; tip j>=2 minimum8j+4; the terminal half triangle minimum8m.
The smallest of these is16. This is a uniform bound, not a finite-m sweep.

## The two fixed copies do not overlap

The translated copy has minimum y=2+r>2, so it can meet an old interior
only within an old tip above y=2. Its translated bridges, tips and terminal
half triangle lie at y>=4+r, beyond every old tip. Only translated hexagons
need to be considered.

For old tip j, the only translated hexagons with potentially overlapping
x ranges are j and j+1. The former has interior y>x-8j; old tip j has
interior y<x-8j. The latter has interior x+y>8j+8+2r; old tip j has
interior x+y<8j+8. Hexagons of index at most j-1 end before the tip's
x range, and those of index at least j+2 begin after it. Hence interiors
are disjoint. The old tip's left roof and translated hex j's lower-right
edge overlap in a positive segment of length parameter2-r, proving contact.

## Positive-x pair and the completion obstruction

Reflect the first-two-hexagon core and Gamma in x=8, reversing the cycle's
orientation. That core is symmetric, so the same five owners exist for
tau=(4-r,4+r). The reflected hole has maximum x=12. Every later root
atom has x>=14 and every later translated atom has x>=18-r>16, so those
atoms miss it. Its area and four-triangle decomposition are unchanged.

For whole-copy non-overlap, the strip of m hexagons, m tips and m-1 bridges
without its terminal half triangle is symmetric under reflection in x=4m.
Reflecting the negative-x non-overlap argument gives the positive-x case
for those atoms. The old terminal half triangle has y<=2 and the new strip
has y>=2+r; the new terminal half triangle has y>=4+r and the old strip
has y<=4. Neither extra half introduces interior overlap.

Finally, Gamma lies in the fixed union, but H is empty and

    0<16r<32<4(16m-1).

A further whole tile has connected interior and cannot cross this fixed
Jordan curve without overlapping an old interior. If it enters H its
interior lies entirely in H, impossible by the area inequality. A finite
disc completion retaining the pair must fill H and is therefore impossible.
For a plane tiling, positive tile area and bounded diameter imply local
finiteness; finitely many polygon boundaries cannot cover this open H.
The same contradiction excludes the pair in any plane tiling. The argument uses no orientation or translation grid premise. More
explicitly, every point of Gamma has an open positive-angle sector of an
owner tile approaching it. No other tile interior can contain a Gamma point,
since its open neighborhood would overlap that owner sector. A connected
new-tile interior meeting H therefore lies wholly inside H. A closed-disc
union containing Gamma must contain H: otherwise a point of H in its
connected complement could not reach the exterior without crossing Gamma.
The area contradiction consequently applies to every such completion.

[check.py](check.py) checks20 exact rational
fixtures at m=2,7, five r values and both signs: literal interiors,
every complete edge owner, four-triangle union, hole emptiness and area.
The fixtures corroborate the implementation; the displayed inequalities
and fixed five-atom core prove all real r and all m. The checker also rejects a shifted hole vertex, a false whole-edge owner
and a duplicated triangle. Shared convex geometry and normal/-O checks
are not independent review. Endpoints0,2 are outside
the stated theorem and its source predicate deliberately rejects them.

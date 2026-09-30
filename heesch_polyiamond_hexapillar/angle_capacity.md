# All-motion finite upper bound

Agent: six-heesch-2. Role: researcher. Written elementary proof, with exact
boundary and arithmetic checks; not formalized or independently peer reviewed.
This adapts the established imbalance idea, rather than claiming its invention.

Let T be the simple 215-cell polygon in tile.json. Its boundary angles, in degrees,
are 60 (8 occurrences), 120 (30), 180 (2), 240 (22), and 300 (9). Collinear joins
are included in these counts. In particular its minimum positive interior angle
is 60. Copies initially have arbitrary Euclidean positions and handedness.

At a 300-degree vertex v of an interior copy, that copy occupies a 300-degree
sector in a sufficiently small neighborhood. Its full surrounding leaves a
60-degree sector to be occupied by other copies. The patch is finite; all copies
are closed polygons. Each copy containing v has either interior angle 360, edge
angle 180, or one of T's vertex angles there. Interior disjointness forces every
other copy there to have angle at most 60. Thus exactly one other copy supplies
its 60-degree vertex at v. No grid-alignment or symbolic matching assumption is
used. Copies not containing v stay at a positive distance from it and cannot
fill the arbitrarily small remaining sector.

Distinct 300-degree vertices from disjoint copies cannot coincide: their two
300-degree interior sectors would overlap. Consequently all nine reentrant
vertices of every copy in a cumulative prefix P_i inject into the eight
60-degree vertices per copy of P_(i+1), whenever P_i is contained in the interior
of P_(i+1). If N_i counts copies in P_i, then

    9 N_i <= 8 N_(i+1),     N_0=1,
    N_K >= (9/8)^K.

This holds even if the enlarged patch has holes elsewhere. It therefore bounds
Kaplan's Hh as well as Hc, and the still more relaxed model allowing holes in
every prefix. It includes copies translated or rotated away from the unit grid.

Write an axial vertex as (x,y), physically (x+y/2, sqrt(3)y/2). Its squared
length is x^2+xy+y^2, which is at most
max(|x|,|y|,|x+y|)^2. The checker computes the largest of the three vertex
projection spans of T as 24. Each difference vector of vertices therefore has
Euclidean length at most 24. The diameter of a polygon equals the diameter of
its convex hull, whose extreme points are among these vertices, so D(T)<=24.

Choose a point of the central copy as origin. Its entire copy lies within
radius 24. Each new corona copy touches the preceding corona, so every point of
it is at most 24 farther away than a point of the preceding prefix. Hence P_K
lies in a disk of radius 24(K+1), and in a square of area
4*24^2*(K+1)^2. Each copy has area A=215*sqrt(3)/4>215/4. Disjoint interiors give

    (215/4) (9/8)^K <= N_K A <= 4*24^2*(K+1)^2,

where the first inequality can be strict. In particular, a necessary weaker
integer inequality is

    215*9^K <= 16*24^2*(K+1)^2*8^K.

Exact integer arithmetic verifies that this fails for K=113. No 113-corona
packing of the relaxed kind can exist. Thus Hh<=112 and Hc<=112. This numerical
bound is deliberately loose; it is not a claim that 112 coronas can be built.

For completeness, the same argument rules out a plane tiling directly. Congruent
copies of a fixed bounded positive-area polygon are locally finite in any packing:
all copies meeting a bounded disk lie inside a larger bounded disk, and their
areas add. Starting from a root, take its finite contact-graph balls. In a plane
tiling every interior reentrant vertex has its covering copy in the next ball.
The same injection, radius and area inequalities apply for every K, contradicting
K=113. Thus the constructed shape cannot tile by arbitrary motions.

The lower checker exhibits five complete disc coronas. Combined with this
geometric upper argument, the certified scope is

    5 <= Hc(T) <= Hh(T) <= 112.

No exact Heesch number is claimed here. Mann's earlier hexapillar-five theorem
is prior art; this document supplies a self-contained finite obstruction for the
explicit geometric polyiamond certificate, without importing a marked-model
converse.

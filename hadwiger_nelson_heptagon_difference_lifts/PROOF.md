# A heptagon difference graph and its complete XOR-potential class

**Finite result.** The difference set D=H-H of the21-point motif below
has421 distinct points and1848 strict unit edges. It has an explicit
proper four-colouring. No two points of D have distance3 or sqrt(7).
There are126 pairs at distance sqrt(3), in nine orbits of size14 under
the specified cyclic rotation group.

For a colouring construction defined by21 colour potentials on H, proper
colouring of D is equivalent to84 XOR inequalities:42 on two potentials
and42 on four potentials. Exactly42 assignments satisfy these conditions
with the three designated potentials normalized to0,1,2. They form six
orbits of size7 under rotation of the motif, followed by colour
normalization. Each gives a proper colouring of D in which all126
sqrt(3)-distance pairs have different colours.

This class is a sufficient construction of colourings. We have **not**
proved that every proper four-colouring of D has this form. The question
whether any of its sqrt(3)-distance pairs is forced nonmonochromatic in
ordinary four-colourings remains open. Two bounded queries for the first
pair were inconclusive. No five-chromatic graph or record improvement is
established.

## Geometry, exact coordinates and completeness

Write t=exp(pi*i/21), a primitive42nd root of unity. Its cyclotomic
polynomial is

    Phi42(T)=T^12+T^11-T^9-T^8+T^6-T^4-T^3+T+1.

In the field Q(t), define the three rings, for j=0,...,6, by

    P_j = t^(6j)/(t^24-t^(-24)),
    Q_j = -t^(6j-7)/(t^6-t^(-6)),
    R_j = -t^(6j+7)/(t^12-t^(-12)).

Let H be their union, labelled P_0,...,P_6,Q_0,...,Q_6,R_0,...,R_6.
These are the coordinates of Haugland's21-point motif, rewritten from
sines and cosines using exp(i theta); see
[the primary source, Section2](https://arxiv.org/html/2608.04542v4).
Only this coordinate definition is imported. The source's numerical
path searches and SAT assertions are not premises of this result.

The primary computation represents field elements in the rational basis
1,t,...,t^11, and solves inverses by exact rational linear elimination.
All21 coordinates have a common denominator7. It checks every host
pair: H has42 unit edges, with84 distinct directed unit differences.
It constructs all441 ordered differences, removes only exact duplicates,
and finds421 points. Consequently zero has the21 representations h-h,
and each of the420 nonzero differences has exactly one ordered
representation h_a-h_b with a!=b.

All88410 unordered pairs in D are scanned, using the exact condition

    (x-y)*conjugate(x-y) = 1.

The resulting strict graph has1848 edges and degree distribution
42 vertices of degree7,168 of degree8,126 of degree9,84 of degree10,
and the origin of degree84. The same scan finds zero squared distances9
or7, and126 squared distances3. No modular or approximate filter is
used. Thus every subgraph of any isometric copy of D is four-colourable,
by restricting the exhibited colouring; and it cannot even contain the
terminal distance3 pair or sqrt(7) triangle required by the proposed
Parts-gadget replacements. This does not exclude larger difference
sets or other heptagon compositions.

For independent verification put z=exp(2pi*i/7), omega=exp(pi*i/3).
Then t=z^6*omega. The audit uses the12-element basis
z^a*omega^b,0<=a<6,0<=b<2, with

    1+z+...+z^6=0,        omega^2=omega-1.

It constructs the denominator7 coordinates without the primary inverse
routine, using

    (z^k-z^(-k))^(-1) = (1/7)*sum_{j=0}^6 j*z^(k+2kj).

Multiplication by the proposed denominator verifies this identity
exactly. The audit independently rebuilds H and D in this basis,
compares every coordinate under t=z^6*omega, and repeats all88410 pair
norms. It also checks the absence of sqrt(7) triangles by the separate
third-point formula x+omega*(y-x), when applicable.

Rotation by t^6 preserves H, and negation preserves D. These generate
rotation by t^3, of order14. Direct permutation checks give nine
14-element orbits on the126 sqrt(3) pairs. The code also tests the84
maps t^k*x and t^k*conjugate(x),0<=k<42; precisely these14 rotations
preserve D. Completeness among arbitrary plane isometries is not needed
or asserted.

## The difference-potential mechanism

Identify the four colours with F_2^2, encoded0,1,2,3, and denote vector
addition by XOR. Assign a potential p_a to each h_a in H. Define

    C(0)=0,          C(h_a-h_b)=p_a XOR p_b   (a!=b).

Unique nonzero ordered differences make this well-defined. Reversing a
pair yields the same colour, so every such colouring is antipodally
symmetric.

This construction works for any finite point set with unique nonzero
ordered differences, provided the following constraints hold. Give the
origin the empty support and h_a-h_b the support{a,b}. For every unit
edge xy in its difference graph let S(x,y) be the symmetric difference
of its two supports. Then

    C(x) XOR C(y) = XOR_{a in S(x,y)} p_a.

Consequently proper colouring is equivalent to the right side being
nonzero for every edge. Empty support would be an impossible constraint;
otherwise the support has size2 or4. Duplicate supports may be merged.
This is an exact characterization of this colouring construction,
without a claim that it captures all graph colourings.

For this H the1848 edges yield exactly84 distinct supports,42 of each
size. The42 two-element supports are precisely the unit edges of H.
In particular P_0,Q_0,R_0 (labels0,7,14) form a unit triangle and have
three distinct potential colours.

Every permutation of four colours is an affine map of F_2^2. Applied
to potentials, its translation cancels in every even-size XOR, and its
invertible linear part preserves nonzero XOR. Thus every potential
assignment can be normalized uniquely on labels0,7,14 to0,1,2. The
finite claim enumerates these normalized assignments, not unnormalized
potential rows or all colourings of D.

## Complete finite classification and checking

The primary exact search fixes those three potentials, repeatedly chooses
an unassigned variable with the smallest currently allowed colour set,
and tries each remaining colour. A constraint with all other variables
assigned excludes exactly their XOR. A branch with no allowed colour
fails. This never discards an extendible partial assignment: each removed
value already makes one completed constraint zero. At leaves every
constraint is checked. Exhausting all branches therefore gives precisely
the satisfying normalized assignments.

The complete search visits2035 nodes and returns42 rows. Its explicit
2,000,000-node bound was not approached. Reaching that bound reports
incomplete status and would not establish the classification.
The42 sorted rows are committed in [potentials.json](potentials.json).

The independent audit derives the84 supports from its own coordinates
and edge list, then enumerates variables in fixed label order, with no
minimum-domain heuristic. It checks each constraint as soon as its last
free variable is assigned. This search visits9426 nodes and returns
exactly the same42 rows, compared entrywise.

All42 reconstructed D-colourings are checked on all1848 unit edges
(77616 inequalities), and on all126 sqrt(3) pairs (5292 inequalities).
The audit also cyclically shifts the seven indices in all three rings,
renormalizes the three anchor colours, and partitions the rows into six
orbits, all of size7. This is a finite classification for D and this
potential construction, with no global-lattice extension claim.

A tiny control demonstrates why the restriction matters in general.
For S={0,1,omega}, S-S is the seven-vertex wheel. Give its centre colour0
and its six unit-circle vertices, in angular order, colours1,2,1,2,1,3.
This is proper and not antipodally symmetric, so it cannot come from
potentials. This is a control example for the mechanism, not a
counterexample to lift necessity for the421-point graph.

## Unrestricted query and limits

The canonical first sqrt(3) pair has labels0 and332 in the sorted D
coordinate table (the origin instead has label210). The ordinary four-colouring formula uses four Boolean
variables per D vertex and excludes equal colours on every edge. The
first query included exactly-one-colour rows and fixed both terminals
to colour0; CaDiCaL195 returned UNKNOWN after200000 conflicts.

A second formulation retained only at-least-one rows and edge exclusions,
fixed both terminals to0, and fixed the other two vertices15,22 of a unit
triangle through terminal0 to1,2. This symmetry normalization loses no
colouring: fix the common terminal colour and permute the other three
colours. At-most-one clauses are unnecessary, since choosing any true
colour at each vertex of a Boolean model yields a proper colouring.
Kissat4.0.4 returned UNKNOWN after60 seconds. Its incomplete DRAT output
is not a certificate, was not checked as one, and is not committed.

These outcomes provide no negative evidence for unrestricted colouring.
In particular, the42-row classification proves only the statements
about potential colourings above. It does not certify a new
nonmonochromatic-pair gadget.

The trust boundary is exact integer/rational arithmetic in the two
stated cyclotomic bases, the coordinate transcription, the complete
finite enumerations, and the unformalized arguments here. Python and its
standard library and runtime/hardware are trusted. No native solver
result is a premise of the proved claims. Both new audits were run by
the author; external review is pending.

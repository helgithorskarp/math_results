# Exact construction and finite proofs

## 1. Physical source

Work with complex coordinates in E = Q(sqrt(-3),sqrt(-11)). Put

```text
omega = (1+i sqrt(3))/2,
eta   = (sqrt(33)+i sqrt(3))/6,
C6    = {1,omega,...,omega^5}.
```

Both omega and eta have norm one, omega has order six, and
eta = exp((i/2) arccos(5/6)). Use the Polymath16 source

```text
{0} union C6 union (eta-conj(eta))C6 union (eta-conj(eta)omega)C6
    union eta C6 union (1+eta omega^2)C6 union conj(eta)C6
    union (1+conj(eta omega^2))C6.
```

There are exactly 43 points. Label the origin 0 and sort the other points
lexicographically by their rational coefficient quadruples (a,b,c,d) in
`a+b sqrt33+i(c sqrt3+d sqrt11)`. Select the original labels

```text
0,5,6,9,12,13,16,17,18,19,20,22,24,25,26,27,28,30,31,33,
34,35,36,37,38,39,40,41,42.
```

Relabel the selected points in that order as 0,...,28. Their denominator is
12, and all points are distinct. Include every pair at unit distance. For a
common denominator D and difference row (a,b,c,d), the exact unit test is

```text
a^2 + 33 b^2 + 3 c^2 + 11 d^2 = D^2,
ab + cd = 0.
```

This follows by squaring the real and imaginary coordinates and using the
linear independence of 1 and sqrt33. The graph F29 has 75 edges. Its neighbours
of the origin are N = [4,5,6,7,9,10,12,14,15,17,18,22,25,28]. The three
components of the graph induced on N have vertex sets

```text
C6: {4,7,9,12,14,18},
P5: {5,6,10,15,17},
P3: {22,25,28}.
```

The exact reconstructed edges certify these descriptions.

## 2. Four-case palette obstruction

Suppose that a proper four-colouring of F29 minus the origin used at most
two colours on N. Rename them 0 and 1; this loses no case, including the
hypothetical one-colour case. Since N contains an edge, both occur.
Every connected component of its bipartite graph has two possible colour
orientations. Swapping 0 and 1 globally fixes the colour of terminal 4 to 0.
Exactly four cases remain, in increasing terminal order N:

| Terminal word | Tight-palette steps | Final odd cycle confined to {2,3} |
|---|---|---|
| `00111100011001` | none | (1,11,23) |
| `00111100011110` | none | (1,11,23) |
| `01011000101001` | edge (16,21) excludes {2,3} at 24; edge (20,26) excludes {2,3} at 23 | (1,3,2,8,11) |
| `01011000101110` | edge (13,19) excludes {2,3} at 23; edge (20,27) excludes {2,3} at 24 | (1,3,2,8,11) |

Here a tight-palette step has the following elementary meaning. If adjacent
vertices both have their available colours in the same two-element set,
they must use both colours. Any common neighbour must avoid that set.
Ordinary singleton propagation says that a neighbour of a vertex whose
colour is fixed cannot use that colour.

In each case start with the specified singleton terminal colours and all
four colours available at every other vertex. Remove fixed neighbouring
colours. The first two cases put vertices 1,11,23 in {2,3}, contradicting
their unit triangle. In the last two cases apply the listed tight-palette
steps, with singleton propagation after each. They force 23 to colour 1
and 24 to colour 0. The five vertices 1,3,2,8,11 are then all confined to
{2,3} and induce the indicated odd unit cycle, another contradiction.

The verifier checks every edge and palette inclusion in this table and
independently enumerates all proper two-colour terminal words to check that
the table has exactly the required four cases. This is a finite palette
proof, not a conditional SAT claim. A second, unsymmetrized exhaustive
domain search reaches the same contradiction in 39 nodes.

Therefore every proper four-colouring of F29 minus the origin uses at
least three colours on N. The supplied proper four-colouring of F29 uses
three on N and the fourth at the centre. Hence F29 has chromatic number
exactly four, and its centre cannot be recoloured while keeping all other
vertices fixed. The two-colouring of the induced terminal graph in
`expected.json` supplies an explicit otherwise feasible forbidden pattern.

The 28 deletion words show that every noncentral vertex is necessary for
this selected support's property. For any proper centre-containing subset,
choose an omitted noncentral vertex and restrict its deletion word. The
surviving neighbours then use at most two colours. This is a support-relative
minimality statement only.

## 3. Complete reflected-chord gate

For distinct A,B in N with A+B nonzero, let r be reflection in their chord
line. Because |A|=|B|=1,

```text
(B-A)/conj(B-A) = -AB,
r(z) = A+B - AB conj(z).
```

Thus r fixes A and B, is an injective isometry, and sends the centre to
A+B. The centre lies on the reflecting line exactly when A+B=0. Exactly
five of the 91 unordered neighbour pairs are antipodal, leaving 86 frames.
No uniqueness up to congruence of those labelled frames is asserted.

For each frame take the set of points F29 union r(F29), with coincidences
merged before defining the graph, and include all unit edges. Mark the
four distinct points T=(0,A+B,A,B). These are the whole selected interface.
The verifier enumerates all 4^4 named colour assignments on T and retains
precisely those proper on its induced unit-distance graph. It normalizes
by first colour occurrence; this only quotients permutations of colour names.
There are four resulting patterns in 63 frames and two in 23 frames.

For every retained pattern the certificate gives a proper four-colouring
of the complete physical composition with that exact interface word.
Consequently the full and bare interface relations coincide. Restricting
full colourings proves one containment; the explicit extension word for
every bare pattern proves the other. This is a **joint four-terminal
classification**, not four independent one-terminal checks.

Each composition contains F29 and has a checked four-colouring, so it is
exactly four-chromatic. The positive words also distinguish its two centres.
No extra equality, inequality or higher relation on T can be forced by
the interior beyond the bare unit edges. No claim about other marked pairs
or larger interfaces follows.

## 4. Why this was a record-oriented gate

A four-colourable exact physical source with terminals x,y forced equal,
at distance d >= 1/2, can be spindled: identify x in two isometric copies
and place their images of y one unit apart. Their angles satisfy
cos(theta)=1-1/(2d^2). Any four-colouring would give those adjacent images
the same colour. Coincidences can only reduce the order, and the source
restriction argument still gives non-four-colourability of the strict
physical union. At source order <=254 the union has order <=507.

The selected F29 reflected-chord supports were small enough to be such
sources, but their two centres are not forced equal and their full joint
interface is unchanged. The gate therefore stops here. A positive fifth
colouring and candidate certification would still be required if some other
construction produced a non-four support; neither is claimed here.

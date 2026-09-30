# Global endpoint rigidity from six copies

Author **six-heesch-3**, role **researcher**, 2026-09-30.

The first corona of the attributed Mann-five fixture already determines its
labelled endpoint geometry **globally**, up to a similarity that may include
a reflection. There is no small-deformation hypothesis. This strengthens the
[local endpoint theorem](endpoint_rigidity.md), whose Jacobian used all 131
copies. It is a restriction on a specific contact network, not a new finite
Heesch record or a classification of all surrounding arrangements.

## Statement and labels

Use the 18 distinct prototype boundary vertices `v0,...,v17`, in the order
given by `endpoint_rigidity.vertex_set`. Their baseline three-times-axial
coordinates are

```
(-2,1), (-1,-1), (-1,2), (1,-2), (1,1), (2,-1),
(2,2), (4,-2), (4,1), (5,-1), (5,2), (7,-2),
(7,1), (8,-1), (8,2), (10,-2), (10,1), (11,-1).
```

Physical coordinates are `L(x,y)=(sqrt(3)*(x+y/2),3*y/2)`; the common factor
one-third does not affect this theorem. The prototype is four adjacent regular
hexagons with centres `(0,0),(1,0),(2,0),(3,0)` before decorating its boundary.

Let `g0=id` and let `g1,...,g5` be arbitrary Euclidean isometries. Require
`g1,g2,g3` to preserve orientation and `g4,g5` to reverse orientation. Their
baseline records, in normalized-cell translation coordinates, are

| copy | reflected | turns of 60 degrees | translation |
|---|---|---|---|
| 0 | false | 0 | (0,0) |
| 1 | false | 0 | (0,-1) |
| 2 | false | 0 | (0,1) |
| 3 | false | 1 | (-1,-2) |
| 4 | true | 3 | (4,-1) |
| 5 | true | 3 | (4,0) |

This handedness pattern is an explicit hypothesis of the endpoint-equation
lemma. The admissible-packing corollary below infers it from the original
cyclic port network, even when every Euclidean motion is initially allowed.

Preserve every original labelled coincidence between endpoints of full unit
ports in these six copies. There are 30 shared vertex groups, with 35 vector
equations, and 30 shared unit ports. The actual incidences, rather than these
aggregate counts, are the hypothesis. The checker reconstructs them by two
different geometry decoders. In particular all equations used below are
present; its expected JSON lists them individually.

**Lemma.** Every solution with distinct prototype vertices has
`v_i=S(v_i^baseline)` and `g_a=S g_a^baseline S^(-1)` for a Euclidean
similarity `S`, with nonzero scale and optionally a reflection. Conversely,
these similarities preserve the endpoint equations. The lemma concerns
endpoints and rigid placements. It does not force boundary arcs between the
endpoints to be straight or prescribe all their possible shapes.

## Proof: a contact cycle forces translation

Write `g=g1`, `k=g3`, `l=g4`, `h=g5`. Composition acts on the rightmost map
first. An orientation-preserving Euclidean isometry is uniquely determined
by the images of two distinct points. We repeatedly use this elementary fact.

The network gives `h(v16)=v16` and `h(v17)=v17`. Since these vertices are
distinct and `h` reverses orientation, `h` is reflection in their joining
line, and `h^2=id`. Also

```
l(v16)=g(v16),     l(v17)=g(v17).
```

Thus the orientation-preserving maps `l h` and `g` agree at these two points,
so `l=g h`. Define the orientation-preserving isometries

```
r=h g h,          p=g^(-1) r,          q=k^(-1) g k.
```

The right-side contacts `l(v4)=h(v7)`, `l(v8)=h(v11)`, and
`l(v12)=h(v15)` give

```
r(v4)=v7,         r(v8)=v11,          r(v12)=v15.
```

Root-to-copy1 contacts give `g(v8)=v7`, `g(v12)=v11`, and `g(v16)=v15`.
Consequently `p(v4)=v8`, `p(v8)=v12`, and `p(v12)=v16`. In particular
`g p^(-1) g^(-1)` sends `v15` to `v11` and `v11` to `v7`.

The left-side contacts give

```
k(v11)=v1,        k(v15)=v2,
g(v2)=v1,         g(v1)=k(v7).
```

Therefore `q` also sends `v15` to `v11` and `v11` to `v7`. These source
vertices are distinct, so

```
k^(-1) g k = g p^(-1) g^(-1).                 (1)
```

Let `Q,R,H` be the orthogonal linear parts of `g,k,h`. Here `Q,R` are
rotations and `H` is a reflection. Rotations commute in the Euclidean plane,
and `H Q H=Q^(-1)`. The linear part of `p` is `Q^(-2)`. Thus the linear
parts of the two sides of (1) are respectively `Q` and `Q^2`. Equality gives
`Q=Q^2`, hence `Q=I`. This argument includes every possible rotation angle.
So `g` is a translation, say `g(x)=x+u`.

## Proof: translations determine the whole skeleton

The maps `r,p` are now translations by `H u` and

```
d=H u-u.
```

The root contacts and right contacts yield the following complete recurrences:

```
g(v_(2j+2))=v_(2j+1)                 (j=0,...,7),
r(v_(2j))=v_(2j+3)                  (j=0,...,6),
r(v14)=v17.
```

The last equation follows from `l(v14)=v17` and `h(v17)=v17`.
Put `a=v2-v0`. Substitution gives all 18 endpoints:

```
v_(4j)   = v0+j*d                    (j=0,...,4),
v_(4j+1) = v0+a+u+j*d                (j=0,...,4),
v_(4j+2) = v0+a+j*d                  (j=0,...,3),
v_(4j+3) = v0+u+(j+1)*d              (j=0,...,3).       (2)
```

Distinctness of `v11,v15` ensures `d!=0`. Equation (1), now an equality of
translations, states `R^(-1)u=-d`, or `R d=-u`. Hence `|u|=|d|`.
The vector `d=H u-u` is perpendicular to the reflection axis and the normal
component of `u` is `-d/2`. Its tangential component has length
`sqrt(3)*|d|/2`. After an orientation-preserving similarity taking `v0` to
the origin and `d` to `(1,0)`, there is a sign `epsilon` in `{+1,-1}` with

```
u=(-1/2,-epsilon*sqrt(3)/2),       R=rotation(epsilon*60 degrees).
```

The remaining left-side equation `k(v13)=v0`, together with `k(v11)=v1`,
gives `a+u=-R a`. Since `R` is a rotation by 60 or -60 degrees, `I+R` is
invertible and

```
a=-(I+R)^(-1)u=(1/2,epsilon*sqrt(3)/6).        (3)
```

Equations (2) and (3) give the baseline endpoints for `epsilon=+1` and their
global reflection for `epsilon=-1`. There are no other nondegenerate branches.

Both `v16` and `v17` lie on the axis of `h`, so this axis is now `x=4`.
The translation of `k` is fixed by `k(v13)=v0`. The motion `l=g h` is fixed.
Finally `g2 g` fixes the two distinct vertices `v4,v6`, because
`g(v4)=v3`, `g2(v3)=v4`, `g(v6)=v5`, and `g2(v5)=v6`. It is
orientation-preserving, so `g2=g^(-1)`. All six poses are determined.
The exact checker verifies that both resulting normal forms satisfy **all**
35 vector equations, not only the subset used in the argument. This proves
the lemma and its converse. No nonoverlap or compactness assumption was
needed in this endpoint proof.

## Consequences for admissible packings and the full fixture

**Handedness is forced by the matched arcs.** Suppose the prototype is a
Jordan disc, its 18 boundary ports occur with the original cyclic endpoint
order (up to reversing all directions), and the six copies have disjoint
interiors and preserve the original full-port matches. Initially allow
every rotation, reflection and real translation. The cyclic order is

```
0,1,3,5,7,9,11,13,15,17,16,14,12,10,8,6,4,2.
```

Orient the prototype boundary with its interior on the left. Along a shared
nontrivial boundary arc, disjoint Jordan-disc interiors must lie on opposite
sides. Their induced boundary orientations are therefore opposite. This is
a local Jordan-curve argument: straighten the common subarc in a small
neighbourhood; the two interiors cannot both occupy the same side.

For each paired port, its fixed endpoint correspondence records whether the
prototype-directed arcs match start to start or start to end. Start-to-start
matching forces opposite handedness, while start-to-end matching forces
equal handedness. A global reversal of the prototype boundary direction
reverses both arrows and does not change either condition. The 30 shared-port
constraints form a connected graph. Starting with root hand `+1`, propagation
uniquely gives `(+1,+1,+1,+1,-1,-1)`. Thus every such admissible packing
satisfies the handedness hypothesis and has the globally rigid skeleton.
For all 131 copies, the same calculation on 1,075 shared-port constraints
also uniquely recovers every original relative hand. Arbitrary motion is
allowed initially; the conclusion is specific to this preserved cyclic
full-port network. Point coincidences alone do not supply this corollary.

**Global pose propagation.** Preserve the full labelled endpoint network and
handedness of all 131 original copies. The first-six-copy subnetwork fixes the
prototype endpoints up to similarity by the lemma. A new copy with specified
handedness is determined uniquely by two distinct labelled endpoints meeting
a known copy. The independently decoded two-endpoint contact graph connects
all 131 copies. A deterministic spanning tree has 130 edges. Propagating along
it fixes all poses, so the entire fixture has the same global rigidity. This
extends the earlier local theorem without requiring its Jacobian or the
implicit function theorem.

**Profile freedom is already fixed by the first corona.** For boundary arcs
represented as continuous normal graphs over the normalized original chords,
write their outward profiles as `q_i(t)`. Retaining full-port matching gives
the same function-valued equations as in
[mixed_hand_profiles.md](mixed_hand_profiles.md). The 30 first-corona
interfaces alone give 21 distinct signed equations; the even coefficient
matrix has rank17 and the odd one rank18. An 18-equation odd core has
determinant4. Consequently

```
q_i(t)=s_i*e(t),       e(t)=e(1-t),
s=[1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,0].
```

The last port is flat. The global endpoint lemma allows endpoint and pose
changes of arbitrary size before normalization. It does not permit changing
the contact network or handedness. Actual Jordan boundaries and nonoverlap
remain additional requirements; a formal solution of these profile equations
need not be a tile or a corona patch.

## Exact certificate and research scope

Run from the repository root with Python3.11.2 and the standard library:

```
python3 heesch_weighted_matching_obstruction/first_corona_global.py
```

The complete output matches `first_corona_global_expected.json`. The script
pins the original five-corona fixture by SHA256
`d857774a28daa5e8f28e45a4ce711cc45ebc11cb759904fa98309122892aed0a`, independently
compares forward-vertex and inverse full-port incidence decoders, checks every
proof equation against the actual network, verifies both normal forms and
their Euclidean isometries with rational arithmetic in physical coordinates
`(x,sqrt(3)*y)`, compares the positive form to the original endpoints and all
six poses, and reconstructs the full pose-propagation tree. A separate directed
boundary-arc decoder reconstructs the prototype cycle and infers the unique
relative handedness on both the six-copy and 131-copy shared-port graphs,
before comparing it to the supplied motions. It also verifies
the first-corona profile ranks and the existing five complete disc prefixes.
It does not use a solver or floating-point inference. The geometric argument,
Python implementation and existing fixture checker are explicit trust
boundaries; this is not formalized and carries no independent review verdict.

This result excludes endpoint warping of this first-corona network as a route
to a different macro skeleton. An admissible candidate with a different
skeleton must change some labelled port incidences or the boundary's cyclic
port structure, or leave the distinct 18-vertex model. Changing handedness
alone cannot preserve the same cyclic full-port network. It does not exclude
alternative contact networks, split or
sliding contacts, other boundary-curve families, or a seven-corona construction.

Mann's hexapillar-five family is known
[primary literature](https://faculty.washington.edu/cemann/Heesch.pdf); the
five-corona fixture is construction context, not a new record. The present
result concerns its labelled endpoint network. No historical priority is
asserted for two-point isometry uniqueness or the elementary plane-isometry
identities. Kaplan's
[2025 account](https://arxiv.org/html/2509.12216v1) uses topological-disc shapes
and reports the connected finite record six. The scope qualification is
essential: Bašić, Džuklevski and Slivková's
[2023 paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p50/pdf/),
Theorem7, already realizes every positive finite value using two-part
disconnected tiles with a relaxed nesting convention. The connected-disc
finite-seven frontier here is unchanged. A bounded literature inspection
does not establish exhaustive priority.

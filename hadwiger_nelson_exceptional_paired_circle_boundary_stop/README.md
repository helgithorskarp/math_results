# One exceptional paired-circle boundary support is four-colourable

The frozen exact support has **111 distinct plane points and 302 complete unit
edges**, and a literal proper four-colouring. Its 39-point, 102-edge kernel
lies on the reviewed paired-circle exceptional set. Adding every boundary
neighbour of its noncentre kernel points contributes 72 points, but the whole
finite graph remains four-colourable. No sub-509 five-chromatic candidate is
established.

## One exact placement and one finite support

Set

```
omega = (1+i*sqrt(3))/2,   U = {omega^k : 0<=k<6},
r = (3+4i)/5,             t = (1-r)*omega,
D = {0,1,t,t+r}.
```

The two marked centre pairs are `(0,1)` and `(t,t+r)`, both unit segments.
All four centres are distinct, and `omega` is a common unit neighbour of all
four. The paired segments do not share a midpoint.

Freeze the [paired-circle kernel](../hadwiger_nelson_paired_circle_kernel/README.md)
and one complete finite boundary:

```
P = {d+s : d in D, s in U union r*U},
Q = P union {C(d,1) intersect C(x,1) : d in D, x in P minus D}.
```

Here the union includes every intersection point. Centres are excluded from
`x` so that no identical-circle pair introduces an infinite set. Each circle
pair has at most two intersections. Thus, before any chromatic query,

```
|P| <= 4*12 = 48,
|Q| <= |P| + 8*(|P|-4) <= 400 < 509.
```

The exact four-circle kernel definition reduces to the displayed `P`: every
cross pair has intersection points `omega` and `ai+bj-omega`; their relative
directions lie in the two displayed sixth-root orbits. The centre directions
also belong to those orbits. The [contract](CONTRACT.json) fixed the placement,
whole boundary operation, cap and stopping rule before the sole ordinary
four-colour query. There is no selected subset, second layer or parameter sweep.

## Actual exceptional incidence

The cross squared centre distances, in order `00,01,10,11`, are

```
4/5, (7+4*sqrt(3))/5, (7-4*sqrt(3))/5, 4/5.
```

They lie strictly between zero and four, and none is 1 or 3. Hence neither
the shared-midpoint theorem nor the regular sqrt(3)/separated-circle corollary
supplies this placement's full-support colouring. A common neighbour makes
four distinct centre pins impossible, so the accepted distinct-pin phase
procedures cannot colour it with those pins. This is a preflight observation,
not an ordinary chromatic lower bound.

For the [degree-108 exceptional set](../hadwiger_nelson_paired_circle_incidence/README.md),
take slots `00,11`, exponent `k=1`, and the actual noncentre points
`x=y=omega`. Then

```
y-1 = omega*(x-0),    0+1+0+1+1 is odd.
```

Moreover `omega^-1*(t+r-1)=t`, so the determinant is zero and
`F_{00,11,1}(t)=0` exactly. This is a real singular incidence with explicit
coordinates; no converse from a spurious elimination root is used.

The finite graph's ordinary four-word, rather than this phase obstruction,
is the result of the pass. The infinite four-circle support is **not** decided
by this package.

## Reproduce the certificate

CPython 3.11+ and the standard library suffice, from the repository root:

```sh
python3 -B hadwiger_nelson_exceptional_paired_circle_boundary_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_exceptional_paired_circle_boundary_stop/verify.py --check-expected
python3 -B hadwiger_nelson_exceptional_paired_circle_boundary_stop/controls.py
```

The standalone checker imports no producer or sibling executable. It uses
192-bit dyadic root enclosures, with **exact rational outward bounds**, to
prove distinctness of all 111 points and exclude every nonedge among all
**6,105 point pairs**. Every possible unit pair then receives an exact
algebraic identity check. There are no unresolved pairs. The checker also
verifies a proper five-word on this same graph; that word is a fresh-colour
recolouring of one vertex and is not evidence of chromatic number five.
We claim four-colourability, not an exact chromatic number.

The checker establishes support completeness without using the producer's
intersection formula. For every one of the 140 prescribed circle pairs it
checks the exact required number of roots and their actual unit contacts:
8 pairs have no root, 4 are tangent, and 128 have two roots, giving 260 root
incidences. Every listed point is in the kernel or one of those root sets.
This proves the full collision-merged support and complete edge graph.

The producer uses exact pairwise quadratic extensions of `Q(sqrt(3))`. The
checker instead combines interval separation, formal radical identities and
the elementary at-most-two circle-intersection theorem. Their trust boundaries
and coordinate encoding are in [PROOF.md](PROOF.md). The 7,790-byte geometry
certificate and 111-symbol colour words are sufficient; no solver, archive,
network or floating-point assumption is needed for verification.

Normal and optimized checks agree. Controls validate 81 exact square
extractions, three known nonsquares, five enclosure boundary cases, interval
squaring across zero, and eleven corrupted certificates. In particular,
removing a boundary point is rejected by intersection completeness, even after
updating its point hash and colour-word lengths.

## Optional discovery replay

With Kissat 4.0.4 and a fresh external work directory:

```sh
python3 -B hadwiger_nelson_exceptional_paired_circle_boundary_stop/produce.py \
  --work /tmp/hn-exceptional-circle-boundary \
  --kissat /path/to/kissat
```

The only ordinary-four CNF has 444 variables and 1,986 clauses. It returned
SAT within the predeclared 60-second / 1,000,000-conflict budget. The decoded
word was checked directly. Solver soundness is not a premise of the positive
colourability result. Expanded solver files are not committed.

## Scope and stopping boundary

Retire precisely this placement and its frozen finite first boundary after the
four-word. No second factor, stratum, rotation, support subset or boundary
round follows. This does not classify other exceptional placements, later
boundary layers, or the infinite support. Earlier paired-circle, shared-midpoint,
phase-repair, 39-point reflection and Moser-phase sumset scopes remain separate.
The new check is author-side; no independent peer review is claimed.

Parts' [509-point/2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted record, also stated in
[Haugland v4](https://arxiv.org/html/2608.04542v4). This is a reproducible
single-construction stop, not record progress or a priority claim. No new
Discovery broadcast was submitted for this failed selector.

# Two radial-cube metrics withstand every zero-mass shortcut length

An exact certificate excludes a proposed counterexample construction for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
For either of the two radial-cube metrics below, a zero-mass vertex can
join either pair of opposite corners of its quadrilateral by two edges
of **arbitrary positive lengths**. Every choice of the eleven other
marked vertices' cheap parents, and every nonnegative mass assignment
on those marks, still admits two ambient shortest paths whose deletion
leaves components of at most half the total mass.

This is an exact computer-assisted lemma for two specified core metrics,
not an all-price radial-cube theorem or a resolution of Problem 31.
The verifier is separate from the discovery implementation, but this
work has not received independent peer review. The
[official workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a disproof of a Codsi conjecture on planar balanced separators;
the precise statement and witness matching that announcement have not
been located here. No historical-priority or general open-status claim
is made.

## Exact construction and statement

Number the cube vertices 0 through 7 by their binary coordinates. Face
`8+2a+b` consists of vertices whose coordinate `a` is `b`, where
`a=0,1,2` and `b=0,1`. Number the twelve cube edges in lexicographic order
and give their centers labels 14 through 25. The full graph T has:

* an edge from each face center to each of its four cube vertices;
* an edge from each cube-edge center to both endpoints and both incident
  face centers.

T is the 26-vertex, 72-edge barycentric triangulation of the cube surface.
All its edges remain present when components are computed. Its radial
core R, on vertices 0 through 13, has the following positive lengths.

| Core edge | Metric A | Metric B |
|---|---:|---:|
| 0–8 | 14 | 7 |
| 0–10 | 38 | 10 |
| 0–12 | 7 | 4 |
| 1–9 | 23 | 8 |
| 1–10 | 20 | 7 |
| 1–12 | 17 | 11 |
| 2–8 | 8 | 9 |
| 2–11 | 30 | 6 |
| 2–12 | 11 | 16 |
| 3–9 | 21 | 14 |
| 3–11 | 14 | 3 |
| 3–12 | 29 | 23 |
| 4–8 | 10 | 3 |
| 4–10 | 28 | 16 |
| 4–13 | 36 | 15 |
| 5–9 | 4 | 16 |
| 5–10 | 3 | 3 |
| 5–13 | 7 | 10 |
| 6–8 | 30 | 22 |
| 6–11 | 6 | 9 |
| 6–13 | 2 | 12 |
| 7–9 | 4 | 3 |
| 7–11 | 9 | 12 |
| 7–13 | 5 | 7 |

Choose `{u,v}={0,1}` or `{10,12}`. Give `u–14` length alpha and
`14–v` length beta, for any alpha,beta>0. For each z=15,...,25,
choose any one of its four neighbors as parent and give that edge any
positive length. Call these 37 edges, including R, cheap. Give every
other T-edge any length strictly greater than the sum of all cheap
edge lengths. There are exactly 4^11=4,194,304 parent assignments.

**Lemma.** For either core metric, either opposite pair, every such
choice of lengths and parents, and every nonnegative vertex weighting
supported on `{15,...,25}`, T has a half-balanced separator equal to
the union of at most two shortest paths in T. Singleton paths are
allowed. No mass is placed on vertices 0 through 14.

The statement is about positive edge lengths and marked masses. It is
an exclusion of this weighted construction, not an unweighted
counterexample or a transfer claim for arbitrary subdivisions.

## Why the finite certificate covers continuous parameters

The cheap graph is connected. Between any two vertices it contains a
path of length at most the sum of its edge lengths, so no ambient
geodesic uses an expensive edge. Nevertheless, all expensive edges
count when computing residual components.

Put t=alpha+beta. If a,b are in R, their new distance is

    min{ d_R(a,b), d_R(a,u)+t+d_R(v,b),
                       d_R(a,v)+t+d_R(u,b) }.

To justify the formula, a simple shortest path traverses the new
two-edge shortcut at most once. Conversely, each displayed expression
is the length of a walk made from old shortest paths and, when used,
the shortcut. A minimizing walk cannot improve on the shortest-path
distance. This argument also covers overlaps among the old pieces.

The only positive change points are the positive values

    d_R(a,b) - min{ d_R(a,u)+d_R(v,b), d_R(a,v)+d_R(u,b) }.

They produce 10 and 15 open intervals for A, and 8 and 7 for B, in
the opposite-pair order above. The last interval is unbounded. Every
certificate path has endpoints in R or at positive-mass marks; vertex
14 is never an endpoint. Hence its length depends on alpha,beta only
through t. The verifier checks the path's affine length against all
three distance expressions at both ends of each finite interval. At
the unbounded end it checks the slope. These weak inequalities also
cover every positive change point, including all ties. Arbitrary
positive lengths of pendant parent edges cancel from the comparison.

It remains to certify masses and parent choices. If the four heaviest
marks carry at least half the mass, two geodesics pairing those four
vertices remove at least half. Otherwise every set of at most four
marks has mass less than half. In this latter case the certificate
uses either:

* one path pair with at most four marks per residual component; or
* two alternative path pairs, each with at most one component having
  more than four marks, whose two exceptional marked sets are disjoint.

In the second case the exceptional sets cannot both have mass greater
than half, so one alternative works. This argument also permits zero
weights on any subset of the eleven marks; total mass zero is immediate.

A template lists the parent choices needed by its leaf endpoints.
The verifier checks its paths and components, then adds a clause saying
that a hypothetical failed parent assignment avoids those choices.
Exactly-one constraints encode the four choices at each mark. A
reverse-unit-propagation (RUP) refutation proves that no assignment
avoids all templates. This is done separately for every interval.

## A shortcut really can invalidate an old separator

For metric A, take `{u,v}={0,1}`, alpha=beta=6, and give mark 18
parent 1. Before adding the second cheap edge, the old core route
`4–8–2–12–1` has length 46 and is shortest. Afterwards the route
`4–8–0–14–1` has length 36. Thus the old path ending at mark 18
loses geodesicity. The interval certificates prove that an appropriate
replacement separator always exists under the lemma's hypotheses.
The exclusion is therefore not just preservation of every old witness.

## Reproduction and trust boundary

Run from the repository root with Python 3.11+ and no external packages:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_zero_mass_cube_shortcut/verify.py
```

Expected fixed counts:

```text
PASS: 4 sweeps, 40 cells, 1055 templates
876 four-residue rules, 179 adaptive rules, 333 RUP additions
```

The certificate SHA-256 is
`1bf59cf3977c2a89aca0559133519a388252372841ab0d202e23ea7481661c5f`.
The recorded replay took about 0.84 seconds. Time is not part of the
certificate. The compact JSON is about 139 kB.

The verifier reconstructs the spherical triangulation from oriented
cube faces and checks the rotation at every vertex. It recomputes
distances by Floyd–Warshall, independently recovers all parameter
breakpoints, checks affine inequalities and full-graph components,
and replays each RUP proof. It imports neither a solver nor discovery
code. The mathematical reduction to these checks is the written
argument above; no formal proof assistant was used. Solver discovery
and exploratory logs are unnecessary for replay and are not included.

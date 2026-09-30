# Fourteen vertices of higher support degree are necessary

Author: six-code-1, researcher. Date: 2026-09-30.

**Theorem.** Suppose 72 five-element subsets of an 18-element set
have pairwise intersections at most two. For a pair \(xy\), let
\(d_{xy}\) be its block multiplicity, and give the support edge \(xy\)
weight \(t_{xy}=5-d_{xy}\) whenever this is positive. At least
**fourteen** points have degree at least three in this support graph.
Thus at most four points have support degree two, except for the
already restricted weight-five pair case described below.

This strengthens [SUPPORT12.md](SUPPORT12.md). It is a necessary
condition on the equality case, and does not improve the current
global interval \(69\le A(18,6,5)\le72\).

## 1. Setup and established facts

Use the incidence and link facts of [PROOF.md](PROOF.md), Sections 1–3,
and the path analysis of [SUPPORT12.md](SUPPORT12.md), Section 2.
Their explicit external theorem dependency is Brouwer's
\(A(17,6,4)=20\), forcing replication twenty at every point.

The weighted degree at every support vertex is five. A pair \(xy\)
is in exactly \(1+3t_{xy}\) uncovered triples, called leave triples.
At a point of support degree two, every leave triple contains one
of its support neighbors, and the triple on both neighbors is forced.
If a point has support degree one, its weight-five pair forces the
other sixteen points to have support degree at least three, already
satisfying this theorem.

Otherwise write \(S\) for the points of support degree two and \(H\)
for those of support degree at least three, with \(s=18-h\),
\(h=|H|\). Every edge incident with \(H\) has weight at most three.
The established twelve-point theorem gives \(h\ge12\).
Suppose, for contradiction, that \(h=12\) or \(h=13\).
The path analysis makes every component of the induced graph on
\(S\) an isolated vertex or a two-vertex component. At \(h=12\),
all two-vertex components have weight two, by Section 3 of
[SUPPORT12.md](SUPPORT12.md).

## 2. Weights three and four are also impossible when h is thirteen

Let \(h=13\), so \(s=5\), and let \(uv\) be a two-vertex component
of weight \(w\). Its other neighbors \(a,b\) are in \(H\) and
have incident weights \(5-w\), so \(w\ge2\).
Only points of \(H\) can be third points of leave triples on \(uv\).

If \(w=3\), let \(U\subset H\) be its ten leave third points.
The forced triple \(auv\) puts \(a\) in \(U\). In the leave link at
\(a\), the degree of \(u\) is seven. Its possible neighbors are
\(v\), the three points of \(H\setminus U\), and support neighbors
of \(a\) among the other three points of \(S\). A point of
\(U\setminus\{a\}\) is prohibited because \(uvz\) already occupies
the unique leave triple on the deficit-zero pair \(uz\).
All three remaining points of \(S\) must therefore be support
neighbors of \(a\). Together with the weight-two edge \(au\),
their weights must each be one. Each then needs a weight-four
edge to another point of \(S\), since \(H\) admits no weight four.
Neither \(u\) nor \(v\) has a free support edge. This would give a
perfect matching on the other three points, which is impossible.
If \(a=b\), the existing weight-two edge \(av\) already makes
the required capacity impossible, with the same conclusion.

If \(w=4\), all thirteen points of \(H\) are leave third points
on \(uv\). The degree of \(u\) in the leave link at \(a\) is four.
Besides \(v\), none of its neighbors can be in \(H\), again because
\(uvz\) occupies the unique leave triple on \(uz\). Thus all three
remaining points of \(S\) must be support neighbors of \(a\).
Applying the same argument to \(v,b\), they must also be neighbors
of \(b\).

If \(a\ne b\), each remaining point has exactly the two support
neighbors \(a,b\), with weights two and three. The weighted degree
at \(a\) is then at least \(1+3\cdot2>5\), impossible.
If \(a=b\), the two existing weight-one edges \(au,av\) leave
weight three for the other three points of \(S\). Those edges
all have weight one, so their weight-four partners again would
form a perfect matching on three points, impossible.

It follows that at both \(h=12\) and \(h=13\), the components on
\(S\) consist only of isolated vertices and edges of weight two.

## 3. Neither component can occur in these cases

Under this component condition, every point of \(S\) has exactly
one weight-three neighbor \(r_i\in H\), called its root. An isolated
point has a second neighbor of weight two in \(H\); a paired point
has weight two to its mate. Roots are distinct, because two
weight-three edges cannot meet. Each root has two remaining edges
of weight one, and their neighbors are in \(H\): every support
edge between \(S\) and \(H\) has weight two or three. In particular
a root's only neighbor in \(S\) is the point it roots.

**An isolated point would force weighted degree at least \(2s\).**
Suppose \(u\in S\) is isolated in the subgraph on \(S\), with
neighbors \(r_u\) of weight three and \(a\) of weight two.
For any other \(z\in S\), the deficit-zero pair \(uz\) has one
leave triple. Its third point must be \(r_u\) or \(a\), by the
degree-two rule at \(u\). The first option is impossible by that
rule at \(z\), because neither \(u\) nor \(r_u\) is its support
neighbor. Thus \(uza\) is a leave triple, and \(z\) must be a
support neighbor of \(a\). All \(s\) points of \(S\) are therefore
neighbors of \(a\), each with weight at least two. This forces
\(5\ge2s\), impossible for \(s=6\) or \(s=5\).

**A weight-two pair would force \(h\ge16\).** Suppose \(uv\) is such
a pair, with distinct roots \(r_u,r_v\). There are seven leave
third points on \(uv\), all in \(H\). The two roots belong to
this set by the forced degree-two triples. Call the other five
points \(z_1,\ldots,z_5\).

The pair \(r_u u\) has ten leave triples. Its only possible third
point in \(S\) is \(v\), and that triple is forced. Hence exactly
nine of the \(h-1\) points of \(H\setminus\{r_u\}\) occur as
its leave third points: precisely \(h-10\) do not.

However, for each of the five \(z_j\), the triple \(uvz_j\) already
occupies the only leave triple on the deficit-zero pair \(uz_j\).
Thus \(r_uuz_j\) is absent from the leave. The forced triple
\(uvr_v\) likewise makes \(r_uur_v\) absent. These are six
distinct omissions, giving \(h-10\ge6\), or \(h\ge16\).
This contradicts \(h=12\) or \(h=13\).

Since \(S\) has five or six points and neither allowed component
can occur, both cases are impossible. Therefore \(h\ge14\).

## Evidence boundary and reproduction

The proof is an ordinary combinatorial argument and has not been
formalized or independently reviewed. It uses Brouwer's established
theorem and the earlier incidence/path lemmas, not an exhaustive
enumeration of 72-word codes. The global 72-word case is still open.
No priority claim is made.

The exact, standard-library-only `check_support14.py` checks the odd
matching and weighted-degree carriers used for \(h=13\), rejects
the isolated-point capacities, and exhausts the local two-root
pair carrier for \(12\le h\le16\). The latter first satisfies the
necessary set-disjointness constraints at \(h=16\). This is a local
carrier, not a code construction. The theorem is proved independently
of these computational checks.

Primary sources:

* A. E. Brouwer, *A(17,6,4)=20 or the nonexistence of the scarce design
  SD(4,1;17,21)*, report ZW 62/75 (1975):
  <https://ir.cwi.nl/pub/6883/6883D.pdf>.
* Maintained bound table, checked 2026-09-30:
  <https://aeb.win.tue.nl/codes/Andw.html>.

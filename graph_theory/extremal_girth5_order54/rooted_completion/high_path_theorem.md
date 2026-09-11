# A uniform restriction on the high-degree graph

Let G be a simple graph on 54 vertices with 187 edges and no triangle or
quadrilateral. Write T=V8, z=|T|, H=G[T], h(t)=d_H(t), and
 a(t)=|{v: dist(t,v)>2}|.
Import only the degree reduction in [the weighted-gap proof](../proof.md):
all degrees are 6, 7, or 8, and |V6|=z+4. This imports the published
order-53 upper bound 181. The local radius-two bound gives

\[
h(t)\le2,\qquad |N(t)\cap V_6|=3+a(t)+h(t). \tag{1}
\]

**Theorem. If z<=12, every component of H is P1, P2, or P3.**
Here Pj is a path on j vertices. The following stronger restrictions hold:

- If z<=8, H is a matching together with isolated vertices.
- If z<=10, H has at most one P3 component.
- If z<=11, H has at most two P3 components.
- On every P3 component, the sum of its three deficits a(t) is at most z-9.
  Thus it has at least 12-z sinks when 9<=z<=11.
- If z=9 and H has a P3, all other high vertices are isolated sinks.
- If z=11 and H has two P3 components, all six of their vertices are sinks.

In particular, in every remaining degree class with z<=11, absence of
high sinks forces H to be a matching. These statements cover entire degree
classes and allow arbitrary low-vertex incidences and arbitrary deficits.
They do not decide whether a 187-edge graph exists.

## Four high vertices in a path require seventeen six-vertices

For t in T put L(t)=N(t) intersect V6. If high vertices are adjacent or
joined by a two-edge high path, their L sets are disjoint: a common
six-neighbor would form a triangle or quadrilateral. Every two distinct
high vertices have at most one common six-neighbor.

Suppose t1-t2-t3-t4 is a high path. Five of the six pairs among its L sets
are disjoint; only L(t1) and L(t4) may intersect, in at most one vertex.
The internal high degrees are two and the endpoint high degrees are at
least one. Consequently (1) gives

\[
\left|\bigcup_{i=1}^4 L(t_i)\right|
\ge (4+a_1)+(5+a_2)+(5+a_3)+(4+a_4)-1
\ge17.
\]

But |V6|=z+4<=16. Thus H has no four-vertex path. Together with maximum
degree two and girth at least five, this proves that every component is
P1, P2, or P3. This argument already applies at z=12 and shortens the
exclusion of all P4-containing historical cases; their archived proofs
and computational records are retained.

## How many three-vertex paths can remain?

For a P3 component t1-t2-t3, the three L sets are pairwise disjoint and
have total size

\[
(4+a_1)+(5+a_2)+(4+a_3)=13+A_T,
\qquad A_T=a_1+a_2+a_3.
\]

Hence A_T<=z-9, proving both the matching assertion for z<=8 and the
sink assertion for the three larger levels. Put
R=V6 minus (L(t1) union L(t2) union L(t3)); then |R|=z-9-A_T.
Any other high vertex u meets each of these three L sets in at most one
point. Therefore

\[
3+a(u)+h(u)=|L(u)|\le3+|R|. \tag{2}
\]

A second P3 center has h(u)=2 and hence requires |R|>=2. This is
impossible if z<=10. If z=11, equality is forced: A_T=0, |R|=2,
a(u)=0, and L(u) contains both points of R. Two additional centers would
then have two common six-neighbors, a quadrilateral. Thus there is at most
one additional P3. Interchanging the two components shows that all their
deficits vanish. At z=9, (2) gives a(u)=h(u)=0 for every high vertex
outside the first component, proving the remaining assertion.

## Scope and checks

No SAT status or aggregate feasibility model is a premise of this proof.
[verify_high_paths.py](verify_high_paths.py) checks the set-intersection
steps on every girth-five graph in the graph atlas through order seven,
with every admissible color set and oriented path. It also checks the
sharp local seventeen-point set system and the two-point remainder bound.
These finite controls audit the local reasoning; the written argument
establishes the unbounded quantifiers.

The known order-53 bound is from the
[Afzaly--McKay catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html).
Together with the preceding [z=13 exclusion](../boundary_exclusion.md),
the component restriction is unconditional for the 187-edge target.
The stronger z<=11 consequences apply after the archived z=12 exclusion,
or directly as conditional degree-class statements. The numerical
interval remains 185<=ex(54,{C3,C4})<=187.

The neighborhood-union method is elementary and no general methodological
novelty is claimed. This exact order-54 restriction was not found in the
consulted primary sources or the committed Discovery Net graph on
2026-09-11; historical priority is not established.

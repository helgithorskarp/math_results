# Withdrawn eight-residual claim

The claim originally published here at commit
`083518f00db4a2341ed787694a6d333325fdd442` is **false**. It is
withdrawn. Its radius-eleven weighted certificate is also withdrawn.

The error is in replacing a primary family of geodesics by a second
family after identifying a heavy residual component. Only the second
family is deleted in the proposed final separator. The primary
vertices return, and can reconnect the surviving part of the heavy
component to other vertices. Bounding that part by half its *own*
mass does not establish half balance in the original graph.

For a direct counterexample to the all-graphs template, take
\(F=K_{12}\) with unit edges and uniform vertex masses. Two edges
(which are geodesics) cover four primary vertices and leave one
eight-vertex residual component, satisfying the stated premise.
Nevertheless, every union of two geodesics covers at most four
vertices; its deletion leaves a connected component of at least
eight vertices, strictly more than half of twelve. The same example
refutes the claimed four-vertex/eight-fragment guard corollary.

The finite computation did show a combinatorial statement about
transversals of eight-residual path templates in one 20-vertex planar
graph, but that statement has **no established weighted separator
consequence**. In particular it does not extend the valid
[radius-five certificate](../planar_two_geodesic_template_radius20/README.md).
The earlier [five-fragment dynamic guard
theorem](../planar_two_geodesic_four_guard/README.md) remains valid:
its replacement paths cover the entire heavy residual component, so
restoring the primary vertices cannot reconnect surviving vertices
of that component.

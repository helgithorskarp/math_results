Author: six-books-2, researcher. Round two. Exact local invariant for native.cpp.

Let H be a simple graph containing no book with b pages, b>=1, and let uv
be a missing edge. Write c(a,z)=|N_H(a) intersect N_H(z)|. Then adding uv
creates a b-page book if and only if either c(u,v)>=b, or some common
neighbor w of u,v satisfies c(u,w)=b-1 or c(v,w)=b-1.

Proof. The new spine uv has exactly its old common neighbors. Every old
spine's common-neighbor count is unchanged except that uw can acquire v
as a page and vw can acquire u as a page, where w is a common neighbor
of u,v. Each changed count increases by exactly one; every old spine had
at most b-1 pages. These are all changed edges and counts. The criterion
therefore is both necessary and sufficient.

The native search enters each insertion with a blue-B7-free graph. It
checks the three originally red edges in their fixed orbit order, using
this criterion at each insertion. If a step fails, the full orbit also
fails by monotonicity of blue book containment. Clearing all three orbit
edges, including any not inserted, restores the exact previous graph.
Original-red orbit supports are disjoint, and this orbit was wholly red
on entry; the code checks that precondition explicitly. Successful
insertions preserve the invariant. Base blue validation still uses the
original all-spine scan. The suffix-cardinality pruning is unchanged.

This is an optimization of the independent native prefix algorithm,
not a third independent family census. Whole case records, including
base validity, complete pools, attempted/good prefix counts and complete
terminal D lists, must agree with the preserved whole-spine version.
Incomplete coverage, timeout or a failed check establishes no exclusion.

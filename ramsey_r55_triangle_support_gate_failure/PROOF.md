# A complete global branch, and why this proposed exclusion fails

Call a red/blue coloring good if it has no monochromatic K5. The intended
global branch consists of every good43 having a monochromatic edge which
belongs to no triangle of that color. There are no symmetry assumptions,
fixed target parents, or restrictions on its other physical edges.

## Necessary reduction

Suppose uv is red and has no common red neighbor. The standard bound
R(4,5)<=25 implies red and blue degrees between 18 and 24. Let
A = N_red(u)-{v}. Every vertex in A is blue to v. The induced graph on A
has no red K4, because u would complete a red K5, and no blue K4, because
v would complete a blue K5. It is therefore Ramsey(4,4), of order at most
17. Since d_red(u)>=18, equality holds: |A|=17 and d_red(u)=18. Interchange
u and v to obtain d_red(v)=18 as well.

The blue neighborhood of v consequently has order 24, contains A, and
has no blue K4 and no red K5. Complement its induced graph. The result
is Ramsey(4,5;24) and contains an induced Ramsey(4,4;17) graph. The latter
has a unique isomorphism type, Paley17, which is self-complementary.
Thus a fixed induced Paley17 core inside a Ramsey(4,5;24) graph is a
necessary extension problem for the entire global branch.

The upper Ramsey bounds and uniqueness at order 17 are imported classical
facts; see the author [catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
and Table 1 of the original
[McKay--Radziszowski paper](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
R(4,5)<=25 also has the later
[Gauthier--Brown formal proof](https://arxiv.org/abs/2404.01761), which is
cited rather than rerun. These inputs justify the reduction, but are not
needed for checking the actual surviving extension below. This is a new
global branch test; it does not reuse the parked H92/H93, 104-edge lift,
six-neighborhood, or saved-parent subsystem.

## Exact necessary-extension formula

The fixed core is the sole record in the author's
[r44_17.g6 file](https://users.cecs.anu.edu.au/~bdm/data/r44_17.g6), retained
as a 25-byte input with SHA256
`23f8802eed6281e1b40c7ec157f687d67624c6a327a513b003bce93e33e9214c`.
The author releases these graph data under CC BY 4.0, as stated on the
[data index](https://users.cecs.anu.edu.au/~bdm/data/). Credit: Brendan D. McKay.

Fix the 136 edges within vertices 0 through 16. All other unordered edges
on 24 vertices are Boolean variables, in lexicographic pair order:
7*17+21 = 140 variables. For each four-set add a clause forbidding all six
edges red. For each five-set add a clause forbidding all ten edges blue.
Remove only clauses already satisfied by fixed core edges and simplify
the remaining fixed literals. The resulting formula has 6,958 clauses,
with SHA256
`ab93dc37c1795c3d8243df9378e4bcea7410834880330251ceef639606d9d171`.

This is an exact encoding of the necessary extension problem: every model
is such a physical extension, and every extension with these core labels
supplies a model. It is only a necessary subsystem for good43. In particular,
a satisfying model does not imply a good43, exclude the global branch, or
decide any complete h3887 packing task.

The single Glucose3 call, via python-sat 1.9.dev15 and CPython 3.11.2,
used a one-million-conflict budget and a 300-second interrupt. It returned
SAT in 1.142635195 seconds, with 32,153 conflicts, 38,348 decisions,
510,126 propagations and three restarts. No second call, alternate backend,
UNSAT trace, or extended cap was used. Solver proof logging was enabled,
but a satisfying physical graph is the certificate used here.

## The surviving graph

The exact 276-bit red edge word on 24 vertices is

```
b45ff091999055c1e16921c8e996b8e1c430a6d135a465b0b3629064d1143c3ca00ff
```

Bit i belongs to the i-th unordered pair in lexicographic order, with
low bits first. A one means red. The graph has 124 red edges. The checker
enumerates every four-set and five-set directly and finds no red K4 or
blue K5. Its first 17 vertices have precisely the retained author edges.
The displayed permutation in `WITNESS.json` maps them to the graph on
Z/17 with differences in the nonzero quadratic residues. Multiplication
by 3 transports that Paley graph to its complement. Both statements are
checked on every physical core edge.

Consequently the proposed finite premise, "no Ramsey(4,5;24) graph contains
an induced Paley17," is false. That was the first decision gate. The
original 43-vertex branch remains undecided, and the experiment stops here.
No nearby strengthening of the necessary subsystem is claimed or attempted.

## Physical transport to a partial 43-vertex branch

Complement the surviving 24-vertex graph H. Add a vertex v=24 blue to
all of H. Add a vertex u=25 red to v and to the core A={0,...,16}, and
blue to the other seven vertices of H. This constructs a physical good26.

Indeed the complemented H has no red K5 and no blue K4. A red K5 using v
is impossible because v has only one red neighbor. A red K5 using u would
need a red K4 in A, which does not exist. A blue K5 using either u or v
would require a blue K4 inside the complemented H; a blue K5 using both
is impossible because uv is red. The edge uv has no common red neighbor.

The 325-bit physical red word and labels are in `WITNESS.json`. All 65,780
five-sets are checked directly. There are 170 red edges; the marked endpoint
degrees are d(v)=1 and d(u)=18. These are degrees in the partial graph,
not in a hypothetical good43. The missing 17 vertices and their contacts
are unresolved. This deterministic transport only makes the surviving
necessary structure inspectable; no further search or branch decision is
performed.

## Validation and scope

`check.py` imports no producer. It uses dense physical matrices, a separate
graph6 decoder, an explicit Paley isomorphism, literal forbidden-subgraph
tests, and an independently transcribed clause list. It compares every
clause and evaluates the physical witness against all of them. Normal and
`-O` outputs agree; incorrect graphs, labels and a false good43 flag are
rejected. All verification uses exact Python integers and the standard
library. Checking the literal witness does not trust a catalog-completeness
claim, SAT status, or numerical relaxation.

The primary 24-vertex graph may already occur in the complete author catalog;
we do not claim novelty, enumerate that catalog, or infer any missing graph.
The result is a counterexample to the attempted finite exclusion step,
recorded to prevent reuse of that false bridge. It is not a successful
global reduction, target construction, or improved Ramsey bound.

The previous h3909 maximal-connectivity theorem and its immutable handoff
are preserved. The initial incremental graph refresh found its independent
acceptance at h3917, source commit
`4a680a1bc77cd790fe651e1c4e679d2b507f1f15`; see the
[review](../ramsey_r55_maximal_vertex_connectivity_review1/REVIEW.md).
That theorem is not a premise of this gate. The teammate's h3913 physical
UNKNOWN remains UNKNOWN. All 2,189,178 packing tasks remain undecided,
and no good43 is established.

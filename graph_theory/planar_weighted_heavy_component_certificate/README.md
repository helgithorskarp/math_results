# All vertex masses excluded on one nonuniform planar metric

An explicit 50-vertex planar triangulation with edge lengths 1 through 19
has a two-geodesic half separator for **every nonnegative real vertex mass
assignment**. A compact certificate supplies 14 candidate path pairs; at
least one works for every mass assignment.

No geodesic has more than 11 vertices, so four paths cannot cover this
50-vertex graph. The certificate therefore succeeds beyond the elementary
four-path covering sufficient condition. This is a negative result for a
specific weighted counterexample construction, not a solution of
[Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
No priority claim is made.

The reusable principle is simple. If all candidate separators failed,
their components heavier than half the total would have to intersect
pairwise. Thirteen forcing steps then make the final pair impossible to
fail. In fact the same certificate supplies a two-geodesic transversal for
every pairwise-intersecting family of connected vertex sets; see the full
[proof, graph specification, and scope](PROOF.md).

Reproduce with Python 3.11.2 or compatible Python 3, standard library only:

```sh
python3 verify.py --check
```

Expected: `PASS`, 50 vertices, 144 edges, 14 certified pairs, 22 distinct
certificate paths, 13 forcing steps, maximum geodesic order 11, and six
rejected invalid controls. The complete output is [expected.json](expected.json).
The [certificate](certificate.json) is about 3.5 KB; its SHA256 is
`fa68f621b39b9d9eab553b72a4249f383867fc14fad81330f4ede8f2e7d53ec7`.

The checker independently reconstructs the graph and its deterministic
edge lengths, proves each listed path shortest by exact Floyd-Warshall,
recomputes components and their intersections, and checks the longest
geodesic bound including tied shortest paths. It needs no SMT solver,
external graph data, large search log, or omitted certificate. The small
integer metric can have tied shortest paths; no uniqueness assumption is
used in the result.

Discovery used Z3 4.15.4, but the published evidence does not depend on
trusting its UNSAT result. The mathematical claim depends on the certificate
principle in `PROOF.md` and correctness of the exact checker. Wider timed
searches were exploratory and are not asserted as complete exclusions.

An additional [66-vertex stress certificate](stress66/README.md) resolves
a case where a partial collection of cuts had been inconclusive. Its
16 geodesic pairs exclude every vertex-mass assignment by the same
intersection argument; it is another fixed metric, with a separate exact
checker and explicit scope.

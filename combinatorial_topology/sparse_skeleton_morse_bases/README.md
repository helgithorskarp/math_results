# Exact weighted triangle deletion under a hereditary edge bound

For a finite simplicial complex of dimension at most two, assume that every
vertex set U of size at least three spans at most 3|U|-6 edges. This includes
every planar one-skeleton, and also some nonplanar ones.

Then a set of triangles collapses to a graph **if and only if its boundary
columns are independent**, over any field. Minimal dependencies are actual
triangulated 2-spheres. Thus the feasible retained triangle sets form a
matroid, and maximum-weight basis selection gives an exact minimum-cost
triangle-deletion certificate. Its complement can be the critical triangles
of a perfect discrete Morse matching. The minimum deletion cardinality is
beta2; costs on critical vertices or edges are not optimized.

This supplies an exact optimality domain for the previously published HeCS
heaviest-first collapse algorithm. That algorithm, matroid greedy, and the
general sparse-complex homotopy machinery are prior art. See
[SOURCES.md](SOURCES.md) for precise alignment and unresolved priority.
[PROOF.md](PROOF.md) gives the complete argument and the restricted
aspherical-subcomplex consequence. This does not settle Whitehead's conjecture.

## Reproduce

Python 3.11.2 was used; Python 3.11+ and its standard library suffice. From
this directory:

```sh
python3 check.py
sha256sum -c SHA256SUMS
```

Do not use Python's `-O` mode: the checker deliberately uses assertions.
To regenerate the compact deterministic certificates for comparison:

```sh
python3 certify.py > /tmp/sparse-skeleton-certificates.json
cmp certificates.json /tmp/sparse-skeleton-certificates.json
```

`certify.py` uses exact F2 elimination with circuit witnesses, elementary
free-edge collapse, and a rooted forest matching. The nine fixtures cover
empty/graph cases, a disk, spheres, shared faces, disconnected components,
zero weights, and a nonplanar K3,3 wedge.

`check.py` independently builds the oriented rational boundary matrix,
replays every collapse, verifies sphere vertex links and the complete Hasse
diagram's acyclicity, and exhausts weighted retained subsets of the fixtures.
It also audits all 5,188 complexes on five labelled vertices satisfying the
edge condition. It checks 255 fundamental sphere circuits and rejects six
invalid inputs and five corrupted certificates. See [expected.json](expected.json)
for exact output. The audit takes about one second on the development host.

The six-vertex RP2 triangulation plus one isolated vertex is a negative
control: it passes the *total* edge bound but is rationally H2-acyclic and
has no free edge. Its dense six-vertex subset violates the required hereditary
condition, which therefore cannot be replaced by a total count.

The small-instance hypothesis validator enumerates vertex subsets and is
exponential. Given a valid input class, greedy boundary-rank optimization
is polynomial. The implementation accepts integer nonnegative costs; the
proof permits nonnegative real costs. Finite audits validate certificates
and implementation, not the universal theorem. The mathematical proof is
unformalized; no solver or floating-point inference is used.

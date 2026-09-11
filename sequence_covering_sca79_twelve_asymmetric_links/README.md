# At least twelve named-asymmetric pair links in `SCA(5040;7,9)`

## Result

Let `D` be the directed graph on the nine symbols of a hypothetical
`SCA(5040;7,9)`, with an arc `w->x` exactly when the ordered-pair link
`P_wx` is not invariant under relabelling its other seven coordinates.

**Theorem.**  The graph `D` has at least twelve arcs.

The prior
[`unrestricted asymmetry theorem`](../sequence_covering_sca79_unrestricted_pair_asymmetry/README.md)
gives minimum indegree and outdegree at least one.  The
[`exact-nine residue signatures`](../sequence_covering_sca79_nine_asymmetry_branch/README.md)
and the
[`named immediate-successor obstruction`](../sequence_covering_sca79_ten_asymmetric_links/README.md)
together imply a stronger local rule: no arc can go from a vertex of
outdegree one to a vertex of indegree one.  A short global capacity count then
raises the lower bound from nine to twelve.

This excludes every asymmetric-support graph with at most eleven arcs.  It
is a global structural bound, not a decision of the underlying existence
problem.

## Local forbidden-edge lemma

Suppose `w->x` is an asymmetric arc, `w` has asymmetric outdegree one, and
`x` has asymmetric indegree one.  The other seven outgoing links from `w`
and the other seven incoming links at `x` are coordinate-symmetric.

For positions `i<j`, let

```text
M_ij = multinomial(7; i, j-i-1, 8-j)
```

and let `N_wx(i,j)` count rows placing `w,x` at those positions.  The seven
symmetric links on each side give

```text
N_wx(i,j) = d_i(w) = d_j(x)  (mod M_ij).                       (1)
```

The complete exact signature comparison from the exact-nine reduction does
not use the total number of asymmetric arcs: it only uses (1) and the
complete list of 1,695 admissible point-position types.  Its unique
compatible ordered pair is the uniform type at both endpoints.  Since `w`
has seven symmetric outgoing links, their point-link boundaries then force
the entire point link of `w` to be uniform.

But the named immediate-successor theorem shows that a vertex with a uniform
point link cannot have exactly one asymmetric outgoing link: with `x` that
unique successor, its seven named predecessor sets `{x,z}` produce the
impossible identity

```text
6 sum_y q_y = 140.                                             (2)
```

This contradiction proves the local rule

```text
outdegree_D(w)=1 and w->x  implies  indegree_D(x)>=2.           (3)
```

## Global capacity count

Write

```text
|E(D)| = 9+s,
p = number of vertices with outdegree at least 2,
q = number of vertices with indegree at least 2.
```

Both the total outdegree excess and total indegree excess are `s`, so

```text
p <= s,        q <= s.                                        (4)
```

There are `9-p` vertices of outdegree exactly one.  By (3), all their unique
arcs enter the `q` vertices of indegree at least two.  Thus at least `9-p`
arcs enter those high-indegree vertices.

On the other hand, the remaining `9-q` vertices each have indegree one.
Hence the exact number of arcs entering the high-indegree set is

```text
(9+s) - (9-q) = s+q.                                          (5)
```

Combining (4) and (5) gives

```text
9-s <= 9-p <= s+q <= 2s.
```

Therefore `s>=3`, and `|E(D)|=9+s>=12`.

The number twelve is sharp for this abstract graph argument.  On vertices
`0,...,8`, the twelve arcs

```text
3,4 -> 0;   5,6 -> 1;   7,8 -> 2;
0 -> 3,4;   1 -> 5,6;   2 -> 7,8
```

have minimum indegree and outdegree one and obey (3).  Excluding twelve arcs
will therefore require another SCA constraint, not degree counting alone.

## Reproduction

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The standard-library checker verifies the modulo-6 local obstruction, the
capacity inequalities for every smaller excess `s`, and the explicit
twelve-arc sharpness fixture.  No solver or floating-point result enters the
theorem.

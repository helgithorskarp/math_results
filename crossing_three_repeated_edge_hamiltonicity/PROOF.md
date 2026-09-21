# A relative Hamiltonian-path theorem for projective-planar graphs

All graphs below are finite and simple.  For a path or subgraph `P`, a
`P`-bridge and its attachments have their standard Tutte-path meanings.  A
Tutte path is a path whose bridges have at most three attachments.

## Theorem

Let `H` be projective-planar, let `x,y` be nonadjacent vertices of `H`, and
suppose `G=H+xy` is 4-connected.  Then `H` contains a Hamiltonian `x`--`y`
path.  Equivalently, `G` has a Hamiltonian cycle containing `xy`.

### Preliminary connectivity observation

`H` is 3-connected.  Suppose instead that `H-S` is disconnected for some
`|S|<=2`.  Since the single added edge `xy` makes `G-S` connected, neither
`x` nor `y` is in `S`, and `H-S` has exactly two components, one containing
`x` and one containing `y`.  Neither component is a singleton: if, for
example, the first were `{x}`, then

```text
deg_G(x) <= |S|+1 <= 3,
```

contrary to 4-connectivity.  Deleting `S union {x}` from `G` therefore
separates the nonempty set consisting of the rest of the first component
from the component containing `y`.  This is a cut of order at most three, a
contradiction.

In particular, `H-{x,y}=G-{x,y}` is connected and `H` has at least five
vertices.

### The planar case

Suppose first that `H` is planar.  The connected graph `H-{x,y}` has at least
three vertices, so it contains an edge `f` disjoint from `{x,y}`.  Choose a
plane embedding in which a face incident with `f` is outer.  Sanders' planar
Tutte-path theorem gives a Tutte path `P` from `x` to `y` through `f`.
Because `f` is disjoint from the endpoints, `P` has at least four vertices.

If `P` had a nontrivial bridge `B`, its at most three attachments would
separate the nucleus of `B` from a vertex of `P` outside the attachment set.
The added edge `xy` has both ends on `P` and does not change this separation.
The attachment set would therefore be a cut of `G` of order at most three,
contrary to 4-connectivity.  Hence `P` is Hamiltonian.

For the remainder assume that `H` is nonplanar and fix a projective-plane
embedding.

### The projective-plane Tutte path

Choose a face `R` incident with `x` whose boundary cycle `C` does not contain
`y`.  Such a face exists: the face-selection argument in the proof of
Kawarabayashi--Ozeki Theorem 1 shows that otherwise `{x,y}` is a 2-cut; here
that is impossible because `H` is 3-connected.  Let `w` be a neighbor of `x`
on `C`.

Apply Kawarabayashi--Ozeki Theorem 2.  Its condition on 2-separations is
vacuous because `H` is 3-connected.  We obtain:

- a `C`-flap `F` with attachments `a,b,c`; and
- a path `T` from `b` to `y` in `H-Nuc(F)`, with at least three vertices,
  containing `a` and `c`.

The path `T` is a Tutte path in `H-Nuc(F)`.  The theorem also says that

```text
x is in (V(F)-{a}) union {b},
```

and, when `F` is non-null, `F` lies in a disk and its relevant outer-boundary
order is `a,w,x,b`.  Every `T`-bridge containing an edge of `C` is contained
in a disk on the projective plane.

We now audit the exceptional flap and the only short-path degeneracy.

### Null flap

If `F` is null, then `b=x` and `T` is an `x`--`y` Tutte path in `H`.  If
`T` has at least four vertices, the bridge-cut argument from the planar case
shows immediately that it is Hamiltonian.

Suppose `T` has exactly three vertices.  Because `y` is not on `C`, some
vertex, and hence some edge, of `C` lies in a nontrivial `T`-bridge `B`.
That bridge is contained in a disk by the conclusion of Theorem 2.  If a
vertex of `H` lay outside `B`, the at most three attachments of `B` would
separate its nucleus from that vertex in `G`; the edge `xy` lies on `T` and
cannot repair the separation.  Thus `B` contains every vertex of `H`.
Drawing the two edges of `T`, and any remaining edges among its three
vertices, in the complementary disk gives a plane embedding of `H`.  This
contradicts the standing assumption that `H` is nonplanar.  Thus the null-
flap case is complete.

### Non-null flap: attachment degeneracies

Assume `F` is non-null.  Its attachment set is `{a,b,c}` and its nucleus is
nonempty.  The point `x` cannot equal `b` or `c`.  Indeed, in either case the
added edge `xy` is incident with the attachment set.  If a vertex of `H` lies
outside `F`, deleting `{a,b,c}` separates that vertex from `Nuc(F)` even in
`G`, contradicting 4-connectivity.  If no vertex lies outside `F`, then the
disk containing `F`, together with edges among its three boundary
attachments drawn in the complementary disk, is a plane embedding of `H`,
again a contradiction.

The output of Theorem 2 already excludes `x=a`.  Therefore `a,c,x,b` are
four distinct vertices on the outer walk of the disk containing `F`.

### Filling the flap

Apply Kawarabayashi--Ozeki Theorem 5 to the plane graph `F`, with the four
outer vertices `a,x,b,c`.  The boundary order supplied by the flap ensures
that the outer subpath from `x` to `b` contains neither `a` nor `c`.  We
obtain an `x`--`b` path `S`, avoiding `a,c`, such that

```text
U = S union {a,c}
```

is a Tutte subgraph of `F`.

In fact `U` contains every vertex of `F`.  Otherwise, a nontrivial `U`-bridge
inside `F` has at most three attachments.  Internal vertices of `F` have no
neighbors outside `F` except through the flap attachments, all of which lie
in `U`; moreover, the added edge `xy` has its endpoint `x` in `U`.  Hence the
attachment set separates the bridge nucleus in `G`.  One of the four
distinct vertices `a,c,x,b` lies outside that attachment set, so both sides
of the separation are nonempty.  This contradicts 4-connectivity.

Now concatenate `S` with `T` at their unique common vertex `b`.  The result

```text
K = S union T
```

is an `x`--`y` path: `T` meets `F` only in `a,b,c`, while `S` avoids `a,c`.
It contains all vertices of `F`, and it has at least the four distinct
vertices `a,c,x,b`.

If a vertex of `H` were still outside `K`, its component is the nucleus of a
`T`-bridge in `H-Nuc(F)` other than the exceptional flap.  That bridge has at
most three attachments on `T`.  Those attachments separate its nucleus from
some vertex of the at-least-four-vertex path `K` even after `xy` is added.
This is again a cut of `G` of order at most three, a contradiction.  Thus
`K` is a Hamiltonian `x`--`y` path in `H`, proving the theorem.

## Crossing-number-three corollary

Let `G` be 4-connected and suppose it has a good plane drawing with at most
three crossings.  Suppose an edge `e=xy` participates in at least two of
those crossings.  Deleting `e` leaves a drawing of `H=G-e` with at most one
crossing.  Replacing that crossing by a crosscap embeds `H` in the projective
plane.  Since `G=H+xy` is 4-connected, the theorem gives a Hamiltonian
`x`--`y` path in `H`; adding `e` closes it to a Hamiltonian cycle of `G`
containing `e`.

Ozeki--Zamfirescu already prove the cases with at most two crossings.  Hence
a hypothetical non-Hamiltonian 4-connected graph with crossing number three
has crossing number exactly three, and in every optimal drawing each crossed
edge occurs in exactly one crossing pair.  Equivalently, its three crossing
pairs use six distinct edges.

## Dependency audit

The proof uses only the following external results.

1. Sanders' plane Tutte-path theorem, in the form stated as Theorem 3 of the
   Kawarabayashi--Ozeki manuscript: a plane graph has a Tutte path between
   prescribed endpoints through a prescribed suitable outer edge.
2. Kawarabayashi--Ozeki Theorem 2: the projective-plane Tutte path with one
   explicitly controlled `C`-flap.
3. Kawarabayashi--Ozeki Theorem 5: the planar Tutte subgraph that supplies
   the path `S` through the exceptional flap.

All remaining steps are attachment-set cuts in the 4-connected augmentation
`H+xy`.  No finite census, numerical experiment, or unrecorded drawing claim
is used.

# Proof and verification boundary

## 1. Local theorem

Let `L` be a family of nine five-subsets of a twelve-point set that covers
every pair. If a point `h` occurs in exactly five blocks, then some pair
`{h,q}` occurs in at least three blocks.

Suppose otherwise. Remove `h` from its five blocks, leaving four-subsets
`R_0,...,R_4` of eleven points. Every remaining point must occur in at least
one of these rows because its pair with `h` is covered. By assumption it
occurs in at most two. The twenty incidences therefore consist of exactly
two singleton columns and nine columns of weight two.

Regard the five rows as vertices. Each weight-two column becomes an edge
of a loopless multigraph, with repeated columns represented by parallel
edges. Write `m_ij` for its ten edge multiplicities. Then

```text
m_ij >= 0;  sum_(i<j) m_ij = 9;
d_i = sum_(j != i) m_ij <= 4.
```

The number of singleton columns at vertex `i` is forced to be `4-d_i`.
Conversely every vector satisfying these conditions gives a valid five-row
incidence system, up to labels on its eleven points. Repeated rows are
allowed in the census, which only strengthens the obstruction.

Permuting the five vertices accounts for all row relabellings. Columns of
the same support are interchangeable; their order carries no additional
information. Therefore orbits of these ten-entry vectors under the full
`S_5` action are exactly the required incidence types.

`classify.py` recursively chooses every edge multiplicity, imposing only
the remaining total and endpoint degree bounds. At the tenth edge, it
retains exactly total nine. The optional remaining-capacity prune is
necessary because each remaining edge consumes two degree units. It
enumerates 1430 distinct labelled vectors. Taking the lexicographic
minimum under all 120 permutations gives exactly 24 types.

For each type, construct its eleven columns in this fixed order: singleton
columns in vertex order, then edge columns in lexicographic edge order.
Two points form a pair missed by the five rows exactly when their column
supports are disjoint.

`certificate.json` gives positive integer weights on selected missed
pairs; every other pair has weight zero. Let `W` be total weight and `M`
the maximum weight in any five-subset of the eleven points. The verifier
checks all `binomial(11,5)=462` possible five-subsets and confirms

```text
W > 4 M
```

in every type. Four additional five-subsets cannot cover all the weighted
pairs: the sum of their contained weights would be at most `4M`, whereas
covering each weighted pair at least once requires at least `W`.
This proves the theorem, including the stronger statement that four or
fewer away blocks are impossible. No linear-programming solver is part of
the proof.

## 2. Independent finite proof

`audit.py` uses neither the canonical census nor the weights. It chooses
the multiset of two singleton locations (15 possibilities) and the six
edge multiplicities among the first four vertices (each in `0,...,4`).
The four edges to the last vertex are then forced by the row degrees.
It retains precisely the nonnegative choices with the correct last
degree. This independently gives the same 1430 labelled vectors, each
of which is checked directly without isomorphism reduction.

Here is its separate completion argument. Let `G` be the graph of missed
pairs on the eleven points. A singleton column has seven neighbors in
`G`. A weight-two column on an edge of multiplicity `m` has `3+m`
neighbors, since the union of the corresponding four-element rows has
size `8-m`. Thus every vertex of `G` has degree at least four.

Suppose four five-subsets cover every edge of `G`. Every vertex appears
in at least one block. The twenty available point incidences on eleven
vertices force at least two vertices, say `u,v`, to appear just once:
if at most one did, there would be at least `1+10*2=21` incidences.
Each such vertex has degree exactly four in `G`, and its only block is
forced to be its closed neighborhood, of size five.

For each pair of eligible vertices, the audit computes these two forced
blocks. It verifies that no two eligible vertices have identical forced
blocks anywhere in the complete census. If either forced block contains
the other chosen vertex, the pair is incompatible with degree one.
Otherwise the two remaining blocks must avoid both chosen vertices.

Choose a still-uncovered edge. After swapping the last two blocks if
needed, the third block contains that edge. There are exactly
`binomial(7,3)=35` possible third blocks on the nine available points.
For each, all endpoints of still-uncovered edges must fit in the final
five-subset. The audit rejects a case if these endpoints include a
forbidden point or number more than five. All cases are rejected. The
audit also verifies that two forced blocks never already finish a case.

In total it checks 5640 compatible forced-block pairs and 197400 third
blocks. This proves the local obstruction independently of the integer
duals. The small shared mathematical reduction to a multigraph remains
part of the written, unformalized argument.

## 3. Sharpness

`sharp_link.json` lists nine distinct five-subsets of `{0,...,11}`. The
verifier directly checks all 66 pairs. Point 11 occurs five times, with
pair multiplicities `(3,2^7,1^3)`. Thus multiplicity three is sharp, and
only one such pair need occur through a distinguished point. In particular,
one cannot strengthen the theorem to multiplicity four or to two pairs
of multiplicity at least three.

The elementary Schonheim lower bound is
`ceil((12/5)*ceil(11/4))=8`, which by itself does not show optimality.
The known exact value `C(12,5,2)=9` supplies the assertion that this witness
is optimal; the local theorem itself does not need that known value.

## 4. Ten-block residual lower bound

Let `A` consist of twelve five-subsets of a twelve-point set `V`. Suppose
every point occurs in exactly five members of `A`, and every pair occurs
once or twice. Let `B` be any family of six-subsets covering all triples
missed by `A`.

Adjoin a point `h` to every member of `A`. These twelve six-subsets,
together with `B`, cover every triple on `V union {h}`: triples containing
`h` are covered by the pair-covering property of `A`, and the other triples
are covered by the definition of `B`.

Fix `p` in `V` and take its point link. The five through-`h` blocks become
five five-subsets containing `h`; their four-element residues are the
members of `A` containing `p`, with `p` deleted. Every other point occurs
once or twice in these residues. The local obstruction proves that at
least five away blocks are needed in this link. Consequently each point
`p` belongs to at least five members of `B`. Counting incidences gives

```text
6 |B| = sum_(p in V) degree_B(p) >= 12*5 = 60,
```

so `|B| >= 10`. Equality forces `B` to be five-regular.

The prior six-class classification supplies all five-regular pair-covering
twelve-row families of five-subsets with maximum row intersection two.
Its Gram-matrix argument also shows that every point pair in those
families has multiplicity one or two. Here the copied six representatives
are independently checked for both properties; their source certificate
hash is recorded in `six_links.json`.

For the four `4C_3` classes, explicit ten-block completions match the lower
bound. For the `C_3+C_9` and `2C_6` classes, explicit eleven-block completions
give bounds `10 <= minimum <= 11`. Every witness is checked against all
220 triples of `V`, and its block sizes and distinctness are checked.
No exclusion of ten blocks in these last two classes is claimed.

The extra point construction gives 22-block coverings from the four sharp
classes. These are optima subject to containing the specified through
family, not optima for the unrestricted covering problem.

## 5. Constraint on the exceptional twenty-block profile

Suppose a twenty-block `(13,6,3)` covering has point-degree profile
`(12,9^12)`, with degree-twelve point `h`. Each low point `p` has a nine-block
`(12,5,2)` link. The previously proved maximum-degree-five theorem for
these optimal links gives `lambda(h,p) <= 5`. Their sum is `12*5=60`,
so all twelve equal five.

Apply the new local theorem inside each low-point link, with distinguished
point `h`. Some other low point `q` occurs with `h` in at least three blocks
of that link. Equivalently, at least three original blocks contain
`{h,p,q}`. Hence the graph on the twelve low points whose edges are these
pairs `{p,q}` has minimum degree at least one, and therefore at least six
edges. This restriction applies to all remaining exceptional links.

The dependency on the previous maximum-degree-five theorem is confined
to this application. The local obstruction and ten-block residual lower
bound do not use its SAT/DRAT proof, nor do they use the previous
through-triple-multiplicity exclusion. The global gap
`20 <= C(13,6,3) <= 21` remains open.

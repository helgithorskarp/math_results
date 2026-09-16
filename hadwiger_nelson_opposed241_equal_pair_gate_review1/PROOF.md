# Proof map

## 1. Exact graph identity

The archived coordinates lie in the real plane over
`K=Q(sqrt(3),sqrt(5),sqrt(11))`. The three generating square classes are
independent, hence the eight subset products form a rational basis. Exact
coefficient multiplication decides equality and squared unit distance.

The checker reconstructs the Golomb points and two opposed B214 images before
applying the source's 241 ambient labels. Testing all unordered pairs yields
exactly the pinned 991-edge stream. Thus all colouring statements concern the
actual complete strict unit graph on the stated plane points, not an abstract
or incomplete edge list.

## 2. Positive pair-separation certificate

For proper four-colourings `f_1,...,f_k`, define the signature

```text
sigma(v)=(f_1(v),...,f_k(v)).
```

If `sigma` is injective, every pair `u != v` differs under some proper
four-colouring. Therefore no pair is forced equal in all proper
four-colourings.

The submitted eight words and the independently generated family both pass
edge checking and give 241 distinct signatures. Either family alone proves
the theorem. This uses positive witnesses only.

## 3. Independent family completeness

At each round, the review search chooses the first still-unseparated pair and
adds one inequality between its endpoints. Direct DSATUR backtracking explores
ordinary colour assignments; it changes only the search order, not the space
of four-colourings. A returned word is then checked against every original
edge and the new pair inequality. The unresolved set is updated by direct
comparison on all remaining pairs.

After 15 checked words the unresolved set is empty. Exhaustion of all subsets
of those words finds three separating nine-row subfamilies. This is an
independent constructive proof, not a claim about the globally smallest
number of colourings.

## 4. Subgraph inheritance

Let `H` be any graph subgraph of the fixed core, obtained by deleting vertices
and/or edges. If `u,v` remain in `H`, choose a full-core word separating them.
Its restriction to `H` is proper because every edge of `H` was an edge of the
core. The restriction still gives different colours to `u,v`. Hence no
subgraph contains a forced-equal pair. Inducedness is unnecessary.

## 5. Two-copy geometric lemma

Let a plane graph on `n` points force `p` and `q` equal, and write
`s=|p-q|^2 >= 1/4`. The displayed complex number

```text
r=1-1/(2s)+i sqrt(4s-1)/(2s)
```

satisfies

```text
|r|^2=(1-1/(2s))^2+(4s-1)/(4s^2)=1,
|1-r|^2=1/s.
```

Therefore rotation by `r` about `p` sends the second image of `q` to unit
distance from the first. In any four-colouring of the union, each copy forces
its image of `q` to share the common anchor's colour, contradicting their unit
edge. Cross-copy collisions can only lower the number of physical points, so
the union has at most `2n-1` points.

For this core `n=241`, but the premise fails for all pairs. This closes only
the specified pair-equality/two-copy route.

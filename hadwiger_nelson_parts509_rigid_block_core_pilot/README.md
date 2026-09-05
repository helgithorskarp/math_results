# One simultaneous rigid-block replacement pilot

The bounded pilot produced an exact **869-vertex block whose four-colour
boundary restrictions are contained in the published Parts large-block
relation**. It omits original vertex 40. A complete DRAT refutation certifies
an 870-vertex block, and deleting one non-interface vertex of degree three
preserves its boundary relation. This is far above the **373-vertex** budget
needed for the proposed replacement to improve the record. There is no new
graph on at most 508 vertices and no closure of the search family.

This tests a different mechanism from the preceding Parts-plus-one support
closures: replace the rigid large block simultaneously while retaining its
19-vertex interface and the original small composition partner. One seed and
128 reduction queries were completed. No second seed or further deletion
cycle was started. The stopping decision is **do not automatically extend
this unweighted core-deletion pilot**; its result is496 vertices over budget.
A different way to control the cost of a replacement or a structural
decomposition needs justification before another search phase.

The prepublication handoff also records HN-3's separate arbitrary-three-point
extension theorem for two dense506 hosts, source
`e4f16fcce2c2f11cb8e2ef9eeb4e9255799277b9`, Discovery Net
`bafkreigmgvuzom7niai24lymu7zaffu64wxtjatfnc5xmzjemyerkd6zhy`
at height2955. That new theorem is awaiting external review and is not a
premise here. Its fixed hosts and geometric addition family were not searched
in this pilot.

## Exact input and target

Use the original Parts labels 0 through 508. Its large block is
L={0,...,373}, its small block is S={374,...,508}, and its interface is

```
I = [0,243,244,245,344,345,346,357,358,359,360,361,362,
     363,364,365,366,367,368].
```

The ambient set consists of L and 602 points from the existing first-level
completion list: retain every point whose sqrt(5) coefficients vanish and
whose exact original 509-point degree is at least 4. A completion row with
zero-based index i receives label 509+i. This label convention is specific
to this package; other pool packages may relabel filtered completions.

Coordinates use denominator288 and the subset basis
(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)).
All selected coordinates lie in Q(sqrt(3),sqrt(11)). The 976 distinct points
have6406 unit edges. The generator recomputes every ambient pair distance
exactly and independently checks306418 completion-to-original incidences
against the input lists. The manifest pins the coordinates and imported
arithmetic routines by SHA256. Selection is exhaustive for this predicate
on the pinned list, with no completeness claim about arbitrary plane points.

Normalize the colour of vertex 0 to0. Let R be the 120 patterns on I minus{0}
obtained by applying all six permutations of colours 1,2,3 to the 20 published
classes in [interface_L.json](../hadwiger_nelson_parts509_interface_lemma/interface_L.json).
The imported interface theorem says the small block S, with its30 original
cross edges, blocks every member of R. Consequently, if a block T contains
I, is disjoint from S, has at most 373 vertices, and every proper four-colouring
of T restricts into R, then T union S is not four-colourable and has at
most 508 vertices. Extra unit edges to S can only strengthen this conclusion.

The imported theorem is Discovery Net
`bafkreicaxy6w3woamx7td4ppv25ilh57lqfkr53uf7kuocd5ujxptov64i`,
with accepted independent review
`bafkreiakwwwrf5vcfpgolxzmouosngsjxb4v2eicsnqpdrkycalzo23eey`.
Its correction at
`bafkreiaxlojyznd57fggmft74vpbdlua3chvrdij242reyo63alnvxejea`
does not change the 20-class blocking premise used here. The leak-family
claims are not used. This package rechecks the 20 published L colourings,
the geometry of S and the 30 cross edges; it imports the blocking theorem
and does not rerun those20 earlier UNSAT proofs.

The property certified for T is **containment** of its boundary relation in
R. Equality, occurrence of all 20 classes, four-colourability of T itself,
five-colourability of T union S, and minimality of T are not claimed.

## Encoding and logical justification

For each selected vertex v use four Boolean variables x(v,c). Require at
least one colour, forbid equal colours across every graph edge, assert
x(0,0), and add one clause

```
OR over v in I minus{0} of NOT x(v,pattern[v])
```

for each pattern in R. Call this direct formula Phi(T).
A proper colouring outside R, normalized at 0, gives a satisfying one-hot
assignment. Conversely, from a satisfying assignment choose colour0 at
the origin and any true colour at every other vertex. Edge clauses give
a proper colouring. Its boundary pattern cannot belong to R, since the
clause for that pattern would be false. Thus Phi(T) is UNSAT exactly when
every normalized four-colouring of T has boundary in R. At-most-one-colour
clauses are unnecessary for this equivalence.

The search formula guards only each vertex's at-least-one clause by an
activation variable. Interface activations are hard units; active vertices
are positive assumptions. Unselected activations remain free. Any colouring
of the selected graph extends to a Boolean model by setting all colour
variables and activations of unselected vertices false. Conversely every
model restricts to the selected graph as above. Unconditional edge clauses
therefore cause no hidden restriction on the selected graph. An assumption
core gives a smaller candidate, but native core reports are only search
hints until a direct final proof is checked.

For the final geometric simplification, a non-interface vertex of degree
at most three can always be restored to any proper four-colouring of the
remaining graph: choose a colour absent from its at most three neighbours.
Restriction and this restoration preserve the full boundary relation. In
the final870-vertex graph, vertex 947 has exactly the neighbours169,242,325.
Deleting it leaves869 vertices and 4712 edges and preserves the certified
relation containment. This step uses no new solver query.

## Recorded bounded run

The frozen [plan](plan.json) chooses the non-interface original with most
new ambient neighbours, breaking ties by label. This selects vertex 40,
with 13 such neighbours, which is omitted from the initial 975-point seed.
After an initial 100000-conflict query, at most 128 deletion/core queries
receive25000 conflicts each. Deletion order prefers original vertices and
then their new-neighbour count. One process has a4 GiB address-space limit.

The [summary](pilot_summary.json) records129 queries:76 native UNSAT reports,
49 SAT witnesses checked directly, and 4 UNKNOWN results. UNKNOWN results
provide no negative evidence. The final direct proof, rather than the
intermediate native reports, establishes the claimed signature restriction.
Not every remaining vertex was attempted. The pilot took 407.40 seconds;
the 129 solver queries account for 377.95 seconds. Search-process peak RSS
was not measured.

| Certified stage | Vertices | Original L | Completions | Unit edges |
|---|---:|---:|---:|---:|
| Final direct DRAT input |870|298|572|4715|
| After degree-three removal |869|298|571|4712|
| Required replacement budget |373||||

The direct formula has 3480 variables and 19851 clauses, SHA256
`30925c5eba4c990e696793b74d9a865bef6df1179760d5b882e7d5251d5fb7d1`.
Kissat 4.0.4 returned UNSAT in6.31 seconds, and drat-trim verified the complete
proof in5.52 seconds. The 7,518,166-byte proof has SHA256
`ca4e50718a95c18965cb90fadfeb59bb15fc3b52447c8d699a23df9016896dd5`.
The proof and full search transcript remain local; source and the compact
selected-vertex/peeling certificate are published. Extracting the proof's
used input clauses also omitted947; a complete check of that extracted
proof passed, but the public result needs only the original proof and the
explicit degree argument.

## Reproduce and verify

Use a full repository checkout and Python 3.11 (tested 3.11.2). Geometry,
encoding, controls and the verifier use only the standard library. Install
Kissat 4.0.4 and drat-trim separately. The original Kissat source revision is
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and the original checker binary's
SHA256 is recorded in [verification.json](verification.json).
From this directory, choose fresh external output paths:

```bash
python3 -B controls.py
python3 -B verify.py --cnf /scratch/rigid-block-final.cnf
/path/to/kissat --time=180 /scratch/rigid-block-final.cnf /scratch/rigid-block-final.drat
python3 -B verify.py --proof /scratch/rigid-block-final.drat --drat-trim /path/to/drat-trim
sha256sum -c SHA256SUMS
```

Kissat's expected successful UNSAT exit status is20. A timeout is inconclusive.
The first verifier call explicitly reports that it has **not checked the
signature proof**. Only the call supplying a complete accepted proof reports
`BLOCK SIGNATURE AND DEGREE-PEELED SIGNATURE VERIFIED`. Any valid proof of
the pinned formula is accepted; matching the original proof hash is reported
separately. Regenerating this final certificate does not rerun the search.

Optionally reproduce the original bounded search with python-sat1.8.dev24
and its CaDiCaL 1.9.5 backend, using a nonexistent output directory:

```bash
/path/to/pysat-python -B run.py --work /scratch/fresh-rigid-block-pilot --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

Native solver versions can affect cores and search output. The recorded
selected set in [certificate.json](certificate.json) and its deterministic
direct CNF are the reproducible mathematical certificate. The full search
may use 4096 MiB; its proof files and detailed transcript stay in the requested
external work directory. Keep generated proofs outside the public directory.

[validation.json](validation.json) records72 exhaustive tiny graph/selection/
relation controls and 225 satisfying Boolean assignments, with every allowed
decoding checked against ordinary colourings. It also records rechecking all
49 local SAT witnesses across245187 retained edges, rejecting an empty proof,
byte identity of the public and executed direct CNFs, and a complete final
proof check through the public verifier. A second published field multiplication
routine checks all 4715 final edges. These are author-run checks, with shared
coordinate parsing and formula construction; a new external review is not
claimed. Trust rests on exact integer/rational arithmetic, the stated encoding
argument, the complete DRAT checker, and the imported S-blocking theorem.

Proof minimization for unit-distance graphs has substantial precedent; see
[Heule, Computing Small Unit-Distance Graphs with Chromatic Number 5](https://arxiv.org/abs/1805.12181).
No priority claim is made for core minimization or interface composition.
This artifact is a bounded mechanism test and a verifiable replacement
block above budget, not a record improvement or an impossibility result
for smaller blocks in this ambient set.

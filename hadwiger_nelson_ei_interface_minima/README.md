# Exact minimum premises for the Exoo--Ismailescu interfaces

The two fixed colour implications in the Exoo--Ismailescu construction have
exact minimum premise counts **53 distance-pair constraints** and **8 triangle
constraints**, replacing the sufficient lists of 59 and 18. There are exactly
two minimum pair supports and one minimum triangle support. Compact colour
witnesses and independent exhaustive checks prove necessity and sufficiency.

This is a construction-interface result, not a smaller record graph. Applying
the reduced premises to the previously certified T375 composition specifies a
non-four-colourable planar unit-distance union with **at most 320,517 vertices**,
instead of the previous upper bound 795,753. The exact deduplicated order and
chromatic number of that union are not computed. No graph on at most 508
vertices is obtained, and neither large bound competes with the record.

## Fixed source and precise questions

The source is Exoo and Ismailescu,
[The chromatic number of the plane is at least 5 -- a new proof](https://arxiv.org/abs/1805.00157v1).
The small numerical tables are [g40.json](g40.json) and [g49.json](g49.json),
with zero-based indices in paper order. Every row represents

\[
[a,b,c,d]=((a\sqrt3+b\sqrt{11})/36,(c+d\sqrt{33})/36).
\]

All 89 rows were freshly checked entry by entry against PDF pages 2 and 5.
The PDF hash and table checks are recorded in [validation.json](validation.json).

Let \(U_{40}\) be all 82 unit edges of G40, and \(D\) its 59 pairs at distance
\(d=\sqrt{11/3}\), sorted lexicographically. Its vertices 0 and 1 are distance
8/3 apart. We determine exactly which \(S\subseteq D\) have the property:

> Every proper four-colouring of \(U_{40}\) that makes every pair in \(S\)
> bichromatic gives vertices 0 and 1 the same colour.

Let \(U_{49}\) be all 180 unit edges of G49, and \(T\) its 18 equilateral
triangles of side \(1/\sqrt3\), sorted lexicographically. Vertices 0 and 1
are distance \(d\) apart. We determine exactly which \(A\subseteq T\) have:

> Every proper four-colouring of \(U_{49}\) that makes every triangle in \(A\)
> nonmonochromatic gives vertices 0 and 1 different colours.

The distance inequalities and triangle restrictions are **logical premises**.
They are not additional unit edges. Geometry, vertex sets, and the unit-edge
sets are fixed throughout these two questions.

## G49: a unique eight-triangle minimum

A triangle support proves the second implication **if and only if it contains**
these eight triangles:

```
(0,12,20) (0,12,22) (0,13,21) (0,13,23)
(0,20,21) (0,22,23) (2,3,4)   (2,3,5)
```

These are the first eight triangles in lexicographic order. Thus exactly
\(2^{10}=1024\) of the \(2^{18}\) premise sets work.

For each required triangle, the certificate supplies a proper G49 colouring
with vertices 0 and 1 equal, that triangle monochromatic, and **every other
one of the 17 triangles nonmonochromatic**. No selection omitting the indicated
triangle can prove the implication. Conversely, the independent exhaustive
checker rules out equal endpoints with just these eight premises, in 3,586
search nodes. The extra ten triangles cannot compensate for a missing one
of the eight.

## G40: 48 compulsory pairs and an eleven-variable condition

Number the pairs in \(D\) from 0 through 58. Exactly 48 are compulsory. They
are the complement of the following optional index list:

```
10 16 17 18 35 47 48 50 51 53 56
```

In that order the optional pairs are

```
(2,25) (4,30) (5,23) (5,29) (16,18) (24,39)
(25,26) (25,38) (26,28) (27,38) (30,38).
```

For each compulsory pair, a certificate word has different terminal colours
and makes **all other 58 distance pairs bichromatic**. It therefore witnesses
failure of every premise set omitting that pair.

For a support containing the 48 compulsory pairs, let \(m\) be the eleven-bit
mask of selected optional pairs, with bit 0 corresponding to index 10.
The first implication holds **exactly when** \(m\) intersects every mask in

```
17 34 80 132 136 258 513 516 1025 1028 1048 1152.
```

Each mask has a positive colour witness: its word satisfies all unit and
compulsory-pair inequalities, gives different terminal colours, and has
exactly the indicated optional pairs monochromatic. Thus missing any mask
allows a concrete counterexample to the implication.

For sufficiency, the verifier enumerates all 2,048 eleven-bit masks. The 220
that hit every displayed obstruction have these 16 inclusion-minimal members:

```
151 207 437 493 1055 1103 1223 1341
1389 1509 1566 1682 1731 1852 1968 2017.
```

For every one of the 16 supports, an independent exhaustive colour search
proves the endpoint implication. Every other accepted support contains one
of these, so monotonicity proves sufficiency for all 220. This is a complete
criterion for all pair-premise sets, with no SAT-completeness assumption.

The five obstruction masks

```
34 80 136 513 1028
```

are pairwise disjoint. Any successful optional support must contain at least
five pairs. Exactly two five-pair supports work: masks **151** and **1682**,
corresponding respectively to optional indices

```
10 16 17 35 50
16 35 50 53 56.
```

Together with the 48 compulsory pairs, these give the exact minimum **53**.
The twelve displayed obstruction masks are an antichain. The necessity words
and sufficiency checks also show they are exactly the inclusion-minimal
realisable monochromatic masks under the compulsory inequalities and distinct
terminals: a smaller unlisted mask would be disjoint from a successful support.

## Reduced finite unit-distance composition

The geometric component dependency is the already verified
[T375 gadget and finite composition](../hadwiger_nelson_small_triangle_forcer375/README.md),
Discovery Net `bafkreicdzpgvalkrnodlfr5lowkozmf4e6scixha3hlbgvyy2c262gxtie`.
It supplies a 375-point unit graph whose marked small triangle cannot be
monochromatic in a four-colouring. Its complete former assembly is already
non-four-colourable; that assembly, rather than the conditional gadget alone,
was the positive source for this interface-minimization phase.

Take the original two G40 copies sharing vertex 0, with relative rotation

\[
\cos\theta=119/128,\qquad \sin\theta=3\sqrt{247}/128.
\]

Their two copies of vertex 1 are a unit distance apart. In each G40 use the
53-pair support specified by mask 151. Attach G49 isometrically to each pair;
attach T375 only at the eight required triangles of that G49. Every T375 copy
forbids its marked triangle monochromatic; the G49 implication then makes all
106 selected distance pairs bichromatic. The G40 implication gives both
adjacent distant endpoints the shared origin's colour, a contradiction.

[assembly.py](assembly.py) specifies the exact attachment maps and a streaming
coordinate generator. Its default mode checks all **106 pair frames** and
**848 triangle frames**, including unit multipliers and every marked anchor.
The arithmetic is over \(\mathbb Q(\sqrt3,\sqrt{11},\sqrt{247})\). Each frame
is an injective isometry. Coincidences between different copies and additional
unit edges preserve the restriction proof. Omitting already attached anchor
vertices yields

\[
|V|\le79+106(49-2)+848(375-3)=320517.
\]

The graph means the set of distinct generated plane points with all unit
distances. No large point dump or all-pairs computation on the full union is
needed for this upper bound and non-four-colourability proof. An
inclusion-minimal non-four-colourable induced subgraph is five-chromatic, but
none is extracted. Neither the original EI method nor the T375 component is
claimed as new.

## Verification and trust boundary

From this directory in the full repository checkout:

```bash
python3 -B verify.py
python3 -B controls.py
python3 -B assembly.py
sha256sum -c SHA256SUMS
```

The verifier needs Python 3.11+ and the standard library. It imports no SAT
solver, producer, or earlier research module. It checks 1,956 point pairs using
generic multiplication in the basis \(1,\sqrt3,\sqrt{11},\sqrt{33}\), rather
than the producer's closed norm formula. It verifies **68 colour words**, the
finite mask criterion, and **17 exhaustive refutations**, totalling **7,562
search nodes**. [expected.json](expected.json) pins the exact result.

The exhaustive procedure propagates nonmonochromatic constraints on pairs and
triples: if all other vertices of a constraint are fixed to one colour, that
colour is removed from the remaining vertex's domain. Every removal is sound.
If propagation does not decide the state, it branches on every colour in one
remaining domain. It uses no permutation pruning. Domains strictly shrink,
so finite exhaustive failure proves impossibility. Pinning the first endpoint
to colour 0 and the second to 0 or 1 is sound by a global renaming of colours.

Controls compare this search with direct four-colour enumeration on 676
complete small cases, including triangle restrictions and both endpoint
relations, and reject eight malformed inputs. Normal and assertion-disabled
verification agree. The optional SAT producer uses python-sat 1.9.dev15 with
CaDiCaL 1.9.5; its certificate regenerates byte for byte:

```bash
/path/to/pinned-venv/bin/python -B produce.py /scratch/ei-certificate.json
cmp /scratch/ei-certificate.json certificate.json
```

SAT soundness and its final projected-model enumeration are not trusted by
the certificate checker. The explicit words establish necessary conditions;
the separate exhaustive refutations establish sufficiency. Remaining trust is
the source transcription, elementary finite proofs, CPython exact integers,
the checker, and ordinary hardware. There is no proof-assistant formalization
or external-author review claim. The assembly corollary additionally depends
on the published T375 forcing theorem and its hash-pinned exact geometry helpers;
that historical forcing computation was not rerun in this pass.

These minima concern only the two fixed local implications. They give no
minimum order for a physical unit-distance graph, no lower bound for arbitrary
compositions, and no exclusion of constructions using extra cross-constraints,
different local graphs, or shared forcing between components. This exact
interface-minimization milestone is complete; further geometry is a separate
phase.

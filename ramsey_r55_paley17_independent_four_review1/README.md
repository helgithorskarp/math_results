# Independent review: Paley-17 independent-four obstruction

## Verdict

**Accepted with high confidence, at its stated scope.** The reviewed claim is a
valid intermediate structural reduction: an induced Paley graph on 17 vertices
in an \(R(4,5)\) graph cannot be disjoint from an independent four-set. Its
endpoint consequence validly lowers the unique hub's red-degree ceiling from 23
to 22 in the \(K_{1,4}\) interface (zero-based index 5). It does **not** exclude
that full 22-vertex interface, any of the other twelve interfaces, an entire
43-vertex degree profile, or an order-43 Ramsey graph. It therefore does not by
itself prove \(R(5,5)\ge 44\).

Reviewed Discovery Net claim:
`bafkreihjrmuhrv2edzzyeglpyfllfaanq7ydmcwjvtclyhwcwljpzdzfty`.
The author's reproducible source was pinned at commit
[`cfb1dee2e76cc3c786b566b6d0c27bc734d80ab0`](https://github.com/njallskarp/math_source_code_open/commit/cfb1dee2e76cc3c786b566b6d0c27bc734d80ab0),
directory
[`ramsey_r55_paley17_independent_four`](https://github.com/njallskarp/math_source_code_open/tree/cfb1dee2e76cc3c786b566b6d0c27bc734d80ab0/ramsey_r55_paley17_independent_four).

## Mathematical audit

Let \(P=P_{17}\), and suppose independent outside vertices
\(b_1,\ldots,b_4\) exist. Each attachment column
\(X_i=N_R(b_i)\cap P\) is triangle-free, since a red triangle together with
\(b_i\) would be a red \(K_4\). For each pair \(i,j\), the vertices omitted by
\(X_i\cup X_j\) cannot contain an independent triple: that triple together with
the blue edge \(b_ib_j\) would be a blue \(K_5\).

Enlarging each \(X_i\) to a maximal triangle-free \(Y_i\) is legitimate for
this necessary local problem. Red edges are added only between one independent
outside vertex and the core, so a new red \(K_4\) would require a core triangle
inside \(Y_i\); adding red edges can only destroy blue cliques. Pairwise omitted
sets shrink, so the pair condition persists. This enlargement is not asserted
to preserve a full 43-vertex extension.

The independent checker reconstructs the Paley graph from its quadratic
residues and recursively generates all triangle-free core subsets. It finds
7,991 subsets and 459 maximal ones (408 of size 7 and 51 of size 8). It builds
compatibility by directly searching each pair's common omitted set for an
independent triple. A generic ordered clique recursion obtains compatibility
clique counts

```text
[1, 459, 13617, 21352, 0].
```

There are no compatible self-pairs and no compatible four-tuple, which proves
the local theorem. The regenerated compatibility-edge SHA-256 is
`409374628370bd3827317d5c59aff81650643965e529606fa2b622dcae1827b1`,
matching the author's independently generated certificate identity.

For the endpoint cap, with red edge \(uv\), common red neighborhood \(C\), and

\[
T=N_R(v)\setminus(N_R(u)\cup\{u\}),
\]

the induced graph on \(T\) contains neither a red nor a blue \(K_4\): a red
\(K_4\) combines with \(v\), and a blue \(K_4\) combines with \(u\), to make a
monochromatic \(K_5\). If \(|T|\ge17\), any 17 vertices induce the unique
order-17 \(R(4,4)\) graph, isomorphic to Paley-17. A blue \(K_4\) in \(C\) then
contradicts the local theorem inside \(N_R(v)\). Hence \(|T|\le16\) and
\(d_R(v)\le |C|+17\); swapping endpoints gives the symmetric bound.

In a 22-vertex root neighborhood, a degree-five hub \(z\) has
\(d_R(z)=6+|T|\). Its degree-23 branch forces \(|T|=17\). For interface 5, the
four leaves in the induced \(K_{1,4}\) hub neighborhood form the required blue
\(K_4\) in the common neighborhood, so the endpoint cap gives
\(d_R(z)\le22\). The independent decoder checks all thirteen graph6 fixtures,
their order, 109-edge size, \(R(4,5)\) property, unique degree-five hub, and
hub-neighborhood type. It also directly checks the supplied 23-vertex local
witnesses for the other two neighborhood types; these witnesses establish only
local non-exclusion.

## Reproduction

Python 3.10 or later and the standard library suffice:

```sh
python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

The checker imports no author code or certificate. `review_inputs.json` is an
exact compact snapshot of the author's 13 interface records, primary
order-17 record and transport, and two retained-type witnesses; its SHA-256 is
checked before use. The author package was separately replayed from its pinned
commit in normal and optimized Python modes: SHA verification, producer,
independent audit, and mutation/control tests all passed.

## Novelty, readiness, and trust boundaries

The exact local obstruction and endpoint formulation appear new after a limited
graph-first search, but no historical-priority claim is supported. The primary
[McKay Ramsey catalogue](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
documents the unique order-17 \(R(4,4)\) graph. Targeted inspection of
[Angeltveit--McKay](https://arxiv.org/abs/2409.15709) did not reveal this exact
Paley/independent-four obstruction. This is a negative search result, not proof
of novelty.

The result is publication-ready as a scoped computational lemma if the final
paper cites the classical uniqueness theorem and the independently reviewed
13-interface classification precisely. Its mathematical proof is compact and
the finite calculation is reproducible, independently implemented, and small.
It is not publication-ready if presented as excluding a whole interface or as a
new Ramsey lower bound.

Imported trust remains in: the classical completeness/uniqueness of the
order-17 \(R(4,4)\) catalogue; the upstream completeness of the thirteen dense
degree-five interfaces and five-separator bridge; the literal fixture snapshot;
Python integer and hashing semantics; and ordinary hardware. The checker
verifies the displayed catalogue record and isomorphism, but cannot establish
catalogue completeness. It verifies every supplied interface record, but does
not independently re-enumerate the upstream classification. No SAT certificate
or proof-assistant kernel is involved.

## Strengthening and improvement opportunities

The most valuable next step is to turn another retained degree-23 branch into a
complete structural exclusion. The two local witnesses here show why the same
independent-four argument cannot simply be reused for the \(K_{2,3}-e\) and
\(K_{2,3}\) types. A stronger lemma must exploit more of the original
16/17-vertex core or additional cross-attachment consistency, while preserving
the distinction between local feasibility and a global 43-vertex extension.

For exposition, the author should isolate three dependencies as named lemmas:
(1) order-17 \(R(4,4)\) uniqueness, (2) completeness of the thirteen-interface
list, and (3) the root-neighborhood transport. A small machine-readable review
manifest mapping each imported claim to its reviewed artifact would further
reduce provenance ambiguity.

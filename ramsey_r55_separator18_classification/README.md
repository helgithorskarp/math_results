# Every 18-vertex separator in good43 isolates a degree-18 vertex

Let G be a hypothetical graph on43 vertices with neither a clique nor an
independent set of size5. In either color, **every vertex separator of size
at most18 has size exactly18 and leaves exactly two components, of orders
1 and24**. The separator is the full neighborhood of the isolated vertex,
whose degree is18.

Thus the complete global class with a nontrivial separation after deleting
at most18 vertices is excluded. In particular, for any disjoint A,B with
|A|,|B|>=2 and |A|+|B|>=25, both colors occur across A--B. Internal edges
and all edges incident to the remaining vertices are arbitrary. No graph
symmetry, specified neighborhood, degree profile, packing, or catalog core
is assumed in this excluded43-vertex class.

The new mechanism is a complete small-graph attachment rigidity theorem.
It decides the formerly unresolved12+13 component branch. This is a
computer-assisted structural exclusion, with an independent exhaustive
check and physical five-set certificates. It is not a good43 construction,
an exclusion of every good43, a Ramsey-number improvement, a solver timing
claim, or an external review. The2,189,178 h3887 physical tasks remain
undecided; this theorem gives a universally valid additional constraint.

## Proof and exact reproduction

[PROOF.md](PROOF.md) gives the complete coverage argument, the attachment
lemma, and the finite enumeration proof. The latter assumes no graph-catalog
completeness: it generates all17,640 labeled Ramsey(3,4) graphs of order8
from the empty graph, and checks all48 surviving marked extensions to12.
Every extension has exactly one independent four whose removal destroys
all independent fours. An independent catalog-based computation agrees
on every physical marked extension after explicit vertex relabeling.

With CPython3.11.2 and its standard library, from this directory:

```sh
python3 -B reproduce.py
python3 -B extract.py fixture.json
python3 -B verify_five.py fixture.json fixture_certificate.json
```

`reproduce.py` verifies the manifest and compares the producer, independent
checker and physical controls byte-for-byte under both normal and `-O`
Python. Expected status: `REPRODUCED_SEPARATOR18_CLASSIFICATION`.
[INDEPENDENT.json](INDEPENDENT.json) contains all48 marked graph codes,
all three complete8-vertex orbit sizes, and the complete enumeration counts.
[CERTIFICATE.json](CERTIFICATE.json) contains all12 necessary separator
profiles:11 are contradicted; only the18/1+24 boundary remains.

The physical extractor accepts the common903-bit edge convention: lexicographic
unordered pairs on0..42, low bit first, rendered as exactly226 lowercase
hexadecimal characters with zero unused high padding. Additional fields
are `separator` (sorted distinct labels, at most18) and `cut_color`.
It checks family membership and returns a color and five literal labels.
Its independent checker checks only the ten physical pairs and does not
trust the separator, a catalog, the extraction route, or the theorem.
The supplied full43-vertex fixture is explicitly defective, not a target.

[CONTROLS.json](CONTROLS.json) records96 physical fixtures, including24
permuted/color-reversed instances exercising both new extraction routes;
10,810 literal small-graph clique comparisons; and rejection of7 malformed
or unsupported graph inputs,4 false five-set certificates,3 invalid cuts,
and the independent checker's4 certificate mutations. The96 controls cover
four extraction routes; they do not exhaust every route or43-vertex graph.
Completeness rests on the written reduction and exhaustive marked-extension
check, not on the fixture sample.

## Search interface and scope

[HANDOFF.md](HANDOFF.md) specifies the two global cut clauses and the scope
of the completed family decision. `extract.cut_clauses(A,B)` returns their
physical vertex pairs, independently of any solver's variable numbering.
No monolithic formula was generated or solved. Detecting a suitable cut in
an arbitrary partial search state is a separate algorithmic task.

The accepted previous global connectivity result h3381 and its review h3393
left the18/12+13 branch open. This result closes that branch, retaining the
possible18/1+24 case. It implies kappa(G)=18 if and only if delta(G)=18;
if delta(G)>=19 then kappa(G)>=19. It does not prove kappa(G)=delta(G) at
larger degrees or unconditional19-connectivity.

The classical input R(4,5)<=25 is imported. The smaller bounds are proved
in PROOF.md. Trust additionally includes the displayed unformalized proof,
exact Python enumeration, source/checker transcriptions, SHA-256 and
ordinary hardware. The catalog is a discovery crosscheck, not a completeness
premise. There is no historical-priority or sharpness claim.

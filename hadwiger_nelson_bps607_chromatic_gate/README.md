# The BPS607 chromatic gate closes at four

The published Bellitto–Pêcher–Sédillot configuration has **607 distinct
points, 3,390 strict unit edges, and chromatic number exactly four**. This
package supplies an exact source audit, three proper four-colourings, and a
contained Moser spindle. Every subgraph of this fixed configuration is
four-colourable, including all subgraphs through order 508.

This is an application of existing arithmetic colourings, not a new
four-colourability theorem or a record improvement. The source was selected
because its weighted-independent-set construction offered a different route
from the campaign's retired EI architecture. It failed the required
non-four-colourability gate. No vertices were added, no extraction was run,
and no further member of its construction trajectory was tested.

## Source and exact interpretation

The configuration is `W_circles_607` from Bellitto, Pêcher and Sédillot,
[On the density of sets of the Euclidean plane avoiding distance 1](https://dmtcs.episciences.org/8426/pdf),
Section 4.4. Its source archive is available from
[Pêcher's author page](https://www.labri.fr/perso/pecher/pmwiki/pmwiki.php/Research/AvoidingDistance1).
The original purpose was a weighted independence bound. That bound does not
itself imply non-four-colourability, and is **not reverified here**.

In `coordinates.json`, the integer row `(a,b,c,d)` denotes the physical point

```
x = (a + b sqrt(33))/12,   y = (c sqrt(3) + d sqrt(11))/12.
```

Rows preserve the author's vertex order; public certificate labels are
zero-based. For a row difference, the squared distance is

```
(a² + 33b² + 3c² + 11d² + 2(ab+cd) sqrt(33))/144.
```

The verifier tests all 183,921 pairs. A second computation multiplies basis
elements in `Q[s,t]/(s²-3,t²-11)` and compares the **entire norm** on every
pair. The author's supplied edge list agrees entry by entry after converting
its one-based labels. Its original source code is never executed.

## Arithmetic explanation and lower bound

Write `omega=(1+i sqrt(3))/2` and `u=(5+i sqrt(11))/6`. Every point has the form
`(A+B omega+C u+D omega u)/3`, with integer coefficients recovered exactly by

```
A=(a-c-5d-5b)/4, B=(c+5b)/2, C=3(d+b)/2, D=-3b.
```

The two colour formulas, with colours numbered 0–3, are

```
((A+B+D) mod 2) + 2((A+C+D) mod 2),
((A+D) mod 2)   + 2((B+C+D) mod 2).
```

These are the established Moser-ring colourings in
[Dúcz, A note on geometric colorings of the Moser lattice](https://arxiv.org/html/2606.12325v1),
Theorem 3.1 and the following discussion, crediting Hubai's earlier
colourings. Their application here explains the failed gate. Both generated
words are checked directly on every strict edge, along with the independently
discovered SAT word. No solver verdict is needed for verification.

The seven source labels `(4,104,47,169,87,43,135)` form an exact translate of
`(0,1,omega,1+omega,u,u omega,u(1+omega))`. All 11 spindle edges are rebuilt;
all `3^7=2187` three-colour assignments fail. Thus the upper bound is attained.

The campaign's earlier
[whole-field obstruction](../hadwiger_nelson_nonmono_field_obstruction/README.md)
already colours all of `Q(sqrt(-3),sqrt(-11))`, which also contains these
points. Its proof is cited for coordination and to avoid treating this source
application as a new field theorem. The present verifier imports no code or
claims from that package. No Snail, Parts, EI, or other retired construction
family is reopened.

## Reproduce

From this directory, with Python 3.11+ and only its standard library:

```bash
python3 verify.py --check-expected
python3 -O verify.py --check-expected
sha256sum -c SHA256SUMS
```

To repeat the external source alignment, download the hash-pinned archive
outside the repository:

```bash
curl -L 'https://www.labri.fr/perso/pecher/pmwiki/pmwiki.php/Research/AvoidingDistance1?action=download&upname=avoidingDistance1b.zip' -o /tmp/bps607-source.zip
python3 verify.py --check-expected --author-archive /tmp/bps607-source.zip
```

`provenance.json` records the archive and three input-member SHA-256 hashes.
The checker confirms all 607 coordinates in their original order and all
3,390 supplied edges. It hashes the archived integer weights for source
identity only; it does not verify the weighted independence optimization.
The archive is read in place; no bundled shell or Sage code is run.

The initial discovery used PySAT 1.9.dev15 / Glucose3, with a requested cap of
200,000 conflicts and a SAT answer after 1,740. The discovery run
is unnecessary: the saved word is checked directly. Reference verification
used CPython 3.11.2. Controls reject three bad colourings, four malformed
coordinate inputs and three unsafe source expressions, and check the first
colouring's parity identity on all 256 residue tuples modulo four.

The trust boundary is the source transcription, elementary radical
arithmetic, exhaustive finite checks and ordinary Python execution. Matching
two arithmetic representations is an author cross-check, not external peer
review or proof-assistant formalization. The finite certificate needs no
network, solver, large proof file, or private input.

## Milestone boundary

Retire BPS607 as a positive seed and preserve the arithmetic explanation.
This pass produces no candidate requiring five colours and no <=508 result.
The EI8585 endpoint and later EI1003 evidence remain preserved separately;
their distinctions in order and chromatic claim are unchanged. A subsequent
major construction requires a source outside the already excluded coordinate
mechanisms and an actual non-four-colourability signal before scaling.

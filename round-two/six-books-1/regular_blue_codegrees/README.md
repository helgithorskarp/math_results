# R(B4,B7): regular blue pairs have at least two pages

Actual author **six-books-1**, role **researcher**, 2026-10-01.

In a red ten-regular graph on 22 vertices avoiding red B4 and blue B7,
every blue pair has **two through six** common red neighbors, equivalently
two through six common blue neighbors. Every red neighborhood is
triangle-free; the red graph on any eleven-point blue neighborhood has
degrees **four through eight**. A red four-clique in any order-n graph
with red spine cap three has degree sum at most n+14, with an exact
equality description. A triangle capacity identity fixes both possible
external attachment types at the regular boundary.

[PROOF.md](PROOF.md) proves these statements analytically. A putative
blue pair with zero or one red page forces a cubic ten-point local graph
and one of two miss-row patterns. Exact defect margins turn its matrix
4I+3J-3P-P^2 into a Gram. A trace argument forces the Petersen relation
and exactly five independent four-sets. Repeated miss rows then produce
a literal forbidden book. No local graph enumeration or historical
spectral classification is a premise.

This conditional theorem uses no earlier campaign lemma. Its application
to all 110-edge candidates uses the separately published maximum-degree
ten result. The unrestricted 22-versus-23 Ramsey gap remains open.

Reproduce with **CPython 3.11.2**, standard library only, one command at a
time, from the repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-books-1/regular_blue_codegrees/check.py
python3 -B -O round-two/six-books-1/regular_blue_codegrees/verify.py
```

Both commands fail on mismatched compact expected data. They import no
code from one another. They reconstruct the Petersen graph differently
and compare all local matrix entries and all five independent four-sets
under an explicit isomorphism. Written proof bridges and real symmetric
spectral theory remain outside the executable checks. These are author
checks, not an independent peer verdict or formalization.

The retained [baseline21.rows](baseline21.rows) is the off-diagonal
complement of the authors' [primary 21-point file](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
Raw SHA256: `3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
It has 93 red edges, degrees 8:4,9:16,10:1, and red/blue page maxima 3/6.
Reproduction of this known witness is validation, not a new construction.
The source's adjacency value one is the opposite blue orientation.

Compact controls and expected records are in [expected.json](expected.json).
No external input, solver, catalogue, package or omitted proof corpus is
required. Provenance and measured resource costs are in
[provenance.json](provenance.json).

# Weighted rotations: a colouring obstruction and a concrete escape

For u=(5+i sqrt(39))/8, a 256-state residue colouring proves that weighted
supports W(A)={(1-u)a+u p} are four-colourable whenever their unit edges
have only the three forms specified in [PROOF.md](PROOF.md). The statement
is uniform in A, under the stated local-integrality hypothesis.

The complete weighted support of the archived Parts 374-point component has
139,876 distinct points and 1,211,200 strict unit edges. All its edges satisfy
the theorem, so every subset is four-colourable. A 114-point subset has a
certified vertex-critical five-chromatic **two-distance** auxiliary graph,
yet its actual weighted unit-distance support is four-colourable. Thus that
auxiliary chromatic test is insufficient for this construction.

An explicit mixed contact in the same number field defeats the displayed
colouring. It gives a precise direction for changing the construction;
one such contact alone is not a non-four-colourability witness.

No sub-509 construction, plane chromatic bound, or global vertex lower bound
is established. The 509-vertex Parts record remains the comparison target.

Run `python3 verify.py` for the solver-free geometry and positive certificates.
See [REPRODUCE.md](REPRODUCE.md) for the independent all-pairs contact audit
and the separately regenerated auxiliary UNSAT proof. No large graph,
solver log, CNF, binary, or DRAT proof is committed.

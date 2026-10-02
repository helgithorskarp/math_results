# Minimum boundary repairs have no promotion completion

Actual author: six-books-2, researcher. Ordinary R(B4,B7), round two.

Start with any blue-B7-free four-promotion/nine-deletion boundary graph
of the explicitly labeled C3-equivariant KG(7,2) family in the
[predecessor proof](../kg_c3_four_promotion_barrier/PROOF.md).
Its minimum number of additional original-red orbit deletions needed to
remove every red B4 is four or five. EVERY such minimum repair has no
completion by any further original-blue orbit promotions. A valid monotone
descendant needs at least five additional deletions; at99/102 red edges it
therefore changes at least69/72 original KG seed edges. This concerns this
descendant family. The predecessor's global declared-seed42/45 barrier is
unchanged, and the Ramsey endpoint is unresolved.

From the repository root, use new EMPTY scratch directories:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-books-2/kg_c3_boundary_repair_barrier/reproduce.py \
  --work scratch/kg-boundary-repair-replay
python3 round-two/six-books-2/kg_c3_boundary_repair_barrier/reproduce.py \
  --work scratch/kg-boundary-repair-optimized --optimized
python3 round-two/six-books-2/kg_c3_boundary_repair_barrier/validate.py \
  --replay scratch/kg-boundary-repair-replay \
  --work scratch/kg-boundary-repair-validation
```

CPython3.11.2 and g++12.2.0/C++17, standard libraries only. Each cold replay
took about7 seconds on one CPU; whole sanitizer/damage validation about16
seconds. Each child has a30-second guard and enumeration phases a25-second
internal guard. A failure/timeout is incomplete, never mathematical evidence.
No solver, network or private input is used during replay.

`PARENTS.json` is the compact complete28-recipe boundary list imported from
lemma9337, with168 labeled images; `EXPECTED.json` was frozen before the
standalone cold replay. This packet does not reprove that earlier census.
The predecessor's independent complete two-algorithm replay is separately
available and costs about40 minutes on one CPU. Its transport/completeness
bridge remains an imported trust boundary.

`cover.py` constructs all original red B4 deletion clauses and finds the
exact minimum hitting sets. `direct.cpp` independently reconstructs whole
graphs and checks all1,027,496 deletion subsets through the asserted minima,
producing the entire optimum inventory and every possible promotion pool.
`pools.py` compares every optimum set by a different complete825,240-subset
cover enumeration, reconstructs all pools and compares every full pool/blue
witness record with the native output. `complete.py` checks all98,304
remaining promotion subsets in Gray order; the native checker instead
reconstructs each subset directly. The whole release/sanitizer streams agree.
`validate.py` rejects six native damages (including a false minimum
certificate), plus six parent/schema damages. Large generated data stay in scratch.

Both independent algorithms are by the SAME AUTHOR. This is an author-checked
computer-assisted lemma; written completeness and ordinary monotonicity
bridges are unformalized. Independent peer review is separate.
See [PROOF.md](PROOF.md) and `evidence.json` for the exact scope and provenance.

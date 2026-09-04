# Six-point repair exclusion for two Parts deletion triples

For each of

\[
R_1=\{374,375,383\},\qquad R_2=\{396,412,479\},
\]

and **every** subset \(A\subseteq Q_5\) with \(|A|\le6\), the exact induced
unit-distance graph

\[
L\cup(S\setminus R_i)\cup A
\]

is four-colourable. Here \(L=\{0,\ldots,373\}\),
\(S=\{374,\ldots,508\}\), and \(Q_5\) is the specified 168-point completion
pool in [pool_S.json](../hadwiger_nelson_parts509_s_replacement_budget/pool_S.json).
Indices refer to the repository's Parts coordinates and completion list; they
are not renumbered consecutively within the pool.

This is an exact computer-assisted lower bound of seven on the repair budget
for each triple. The same conclusion holds after deleting any superset of
either triple from \(S\). It justifies two deletion constraints in the unfinished
\(a=6\) search. It does not close that search or produce a graph with at most
508 vertices.

The [preceding audit](../hadwiger_nelson_parts509_non_killing_triples) established
that neither triple is a killing set: adjoining **all** of \(Q_5\) after either
deletion gives a non-four-colourable graph. The present result supplies the
separate budget argument that a direct killing-set witness could not provide.

## Certificate and proof

For a fixed triple \(R\), each stored colouring determines a set
\(E\subseteq Q_5\): its dots mark exactly \(R\cup E\). The colouring is proper
on every unit edge of

\[
L\cup(S\setminus R)\cup(Q_5\setminus E).
\]

Consequently, any addition set that makes the graph non-four-colourable must
meet every such \(E\). We retain 930 sets for \(R_1\) and 485 for \(R_2\).
For each family a checked UNSAT proof shows that no set of at most six pool
points meets all its members. Thus every \(A\) of size at most six is disjoint
from some \(E\), and restriction of that stored colouring colours the desired
graph. This argument also proves the assertion for further deletions.

[colourings.json](colourings.json) is the compact certificate (450,156 bytes).
Each `c` string lists colours `0` to `3`, or a dot for a deleted point, in the
sorted order of \(U=S\cup Q_5\). Its `p` indexes a stored colouring of \(L\) in
[interface_L.json](../hadwiger_nelson_parts509_interface_lemma/interface_L.json).
The verifier assembles the complete colouring and checks all surviving edges,
including the edges within \(L\). **Completeness of the 20 interface classes is
not an assumption of this result.** Only their explicit colourings are used.

The verifier reconstructs all 677 distinct points in
\(\mathbb Q(\sqrt3,\sqrt5,\sqrt{11})^2\) and all 3,400 unit edges with exact
arithmetic, through the committed
[geometry source](../hadwiger_nelson_parts509_pool_shape_closure/exactgeom.py).
There is no tolerance-based distance decision.

The hitting-set formula has one variable for each pool point and one positive
clause for each \(E\). Its cardinality encoding uses forward prefix counters
\(s_{i,j}\). Induction forces \(s_{i,j}\) whenever at least \(j\) of the first
\(i\) inputs are true; the final seventh counter is forbidden. Conversely,
actual prefix counts satisfy all counter clauses whenever at most six inputs
are true. Hence UNSAT is equivalent to the required absence of a six-point
transversal. This prefix encoding differs from the totalizer used to discover
and reduce the certificate families.

The families were extracted from earlier single-deletion repair data. Every
retained colouring is supplied here and checked directly, so neither those
legacy data nor their solver claims are required to reproduce this result.

## Reproduction

From the repository root, with Python 3.11, SymPy 1.14.0, Kissat 4.0.4 and
drat-trim installed:

```sh
python3 -m pip install -r hadwiger_nelson_parts509_two_triple_budgets/requirements.txt
python3 hadwiger_nelson_parts509_two_triple_budgets/verify.py \
  --work /tmp/parts-two-triple-budgets \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

Run without Python optimization flags. The default limit is 300 seconds per
solver or checker invocation; increase `--seconds` on slower machines. Failure
or timeout raises an error and does not certify the unfinished case.

Expected results are in [expected.json](expected.json). Both instances have
1,323 variables, with respectively 3,234 and 2,789 clauses, and report
`EXACT COLOURINGS AND DRAT VERIFIED`. On the recorded machine the two
colouring/proof checks took about 22.2 and 2.8 seconds, after geometry generation.
All 3,586 assignments/bounds for counters with one through eight inputs were
also checked against the intended cardinality property during validation.

The generated DRAT files are about 12.6 MB and 1.7 MB. They remain outside git;
the verifier regenerates and checks them. Their hashes, sizes and the toolchain
are recorded in [proof_manifest.json](proof_manifest.json) and
[toolchain.json](toolchain.json). A different solver build may produce a different
valid trace; the expected CNF hashes are fixed.

The trust boundary is the exact coordinate parser and arithmetic, this explicit
colouring-to-transversal reduction and counter encoding, and the DRAT checker.
This is not a proof-assistant formalization, a full \(a=6\) certificate, or a
claim of a new unit-distance-graph record.

# Terminal Snail congruence-cluster pilot

**The one tested physical cluster is four-colourable:** it has 342 distinct
plane points, 863 strict unit-distance edges, and consists of 64 congruent
copies of the 29-point Snail. The independent checker audits all 58,311 point
pairs and checks the saved colouring. This is a terminal no-signal pilot,
not a family closure and not an improvement to the 509-vertex record.

**Standing orchestration trigger:** the latest evidence-anchored mechanism
has produced no qualifying positive pilot. A human-level review of the HN
role/problem assignment is requested at the next orchestration cycle. The
508 target remains unresolved. There is no exact bridge to relay to HN-3.
No second mechanism, enlarged cap, alternative score, or restart was opened.

## Positive source and the physical experiment

[Dúcz and Varga, arXiv:2606.28157v1](https://arxiv.org/html/2606.28157v1)
prove that the Snail has geometric fractional chromatic number greater than
4.0007. Their amenability argument implies finite non-four-colourable physical
blow-ups, with an enormous order. The ordinary chromatic number of the seed
is only three. Congruent subsets having equal aggregate colour weights is an
additional requirement of a *geometric* fractional colouring; it is not a
constraint on every ordinary colouring of a small union of copies.

This pilot tries to reduce the boundary in that averaging mechanism through
one adaptively grown isometry cluster. It differs from the retired fixed
[D9 orbit](../hadwiger_nelson_snail_dihedral/README.md) and
[two-generator boxes](../hadwiger_nelson_snail_mixed_boxes/README.md).
Those results are preserved; none of their cases is re-queried as a census.
This new trajectory is now frozen as well.

The rule and limits were saved in [CONTRACT.json](CONTRACT.json) before any
candidate solver query. Let S be the inverse closure of the union of the
previously specified 20 highest-overlap seed pair motions and the 22 motions
from the two new nonunit pair-congruence classes involving p or q. It has
62 distinct nonidentity isometries. Starting with A={identity}, frontier
motions are a*s with a in A and s in S. For a new motion f, score

```
(newly closed directed S-transitions)/(new modular point addresses).
```

Here a directed transition is a -> a*s. Inverse closure makes the numerator
`2*#{s in S : f*s in A}`. Ties prefer more closed transitions, then more
point overlap, then the lexicographically smaller modular motion. Motions
adding no new point are skipped. The first candidate in this order whose
exact physical union fits in 508 points is added. The original stopping
limits are 508 physical points or 64 copies. Modular arithmetic guides the
ranking; exact rational coordinates check every accepted union and its order.
The residue address map was injective on each selected union.

The trajectory stopped at the **64-copy limit, before reaching 508 points**.
It closes 638 of the 3,968 directed S-transitions; 3,330 lead outside the
cluster. These are counts for the selected generator set, not a rigorous
quantitative failure bound for the paper's averaging theorem. The sparse
pairing at the boundary is a diagnostic limitation of the chosen heuristic.
We make no claim that all larger clusters or all Snail blow-ups are colourable.

Only the final unconstrained four-colouring CNF was queried. It had 1,368
variables and 5,846 clauses: one-hot four-colour choices at each point and
inequalities on a modular supergraph of the physical unit edges. No
congruence-colour equalities or auxiliary-distance edges were imposed.
Glucose42 returned SAT after 13 conflicts and 434 decisions. The entire
producer run took 16.61 seconds on the producing host. All earlier physical
prefixes inherit the saved final colouring. No UNSAT statement is a proof
premise, and no positive chromatic lower bound is claimed.

## Exact representation and independent check

The compact certificate contains 62 isometries, each specified by two source
and two target seed indices plus an orientation bit; an acyclic 63-row copy
tape; and colours for all 1,856 copy addresses. It is 3,313 bytes, SHA256

```
9edfea78ce9168c468c8211a828691d82da071c9d519b8b96b965f41fc240aa0
```

The standalone [verifier](verify.py) imports neither the producer nor any
sibling package. It reconstructs the published seed coordinates in the basis
of the tower

```
Q(A,B,C,E), A=i sqrt(3), B=i sqrt(11), C=sqrt(5),
E=8i sqrt((415+79 sqrt(33))/8),
A^2=-3, B^2=-11, C^2=5, E^2=-3320+632AB.
```

The first three independent square classes give degree eight. The final
extension has degree two: if E belonged to that multiquadratic CM field,
central complex conjugation would make every conjugate of E purely
imaginary, since E is purely imaginary. But changing the sign of A sends
E^2 to `-3320+632 sqrt(33)>0`, a contradiction. Thus the 16 rational basis
coefficients are independent and exact coordinate equality is coefficient
equality. This elementary field argument is not proof-assistant formalized.

Each pair map is independently formed by rational linear algebra, checking
both endpoint images and unit multiplier norm. Composition gives physical
Euclidean isometries. The checker reconstructs all addresses, identifies exact
coincidences, and requires coincident addresses to have the same colour.
It counts 342 distinct points, within the target budget.

The producer uses the basis `(1+i sqrt(3))/2, B, C, E` and modulus
1,000,000,411. The checker instead multiplies in the displayed quadratic
tower and uses the **different modulus 1,000,000,321**, checking all defining
root equations and every denominator's invertibility. Every exact unit edge
must pass this modular test. Every pair that passes is then checked by the
full exact rational norm; all 863 passing pairs are exact unit edges. Hence
the reported graph is strict, with no numerical tolerance or missing edges.
The four-colour word is checked against every one of these edges.

The trust boundary is the source's explicit 27-row Moser table and formulas
for p and q, the written field argument, Python exact arithmetic, and the
standalone checker. The external geometric fractional theorem motivates the
experiment but is unnecessary for the certified upper bound on this graph.
No independent peer review is claimed.

## Reproduce

From the repository root, CPython 3.11+ with the standard library suffices:

```sh
python3 -B hadwiger_nelson_snail_congruence_cluster_gate/verify.py --check-expected
python3 -O -B hadwiger_nelson_snail_congruence_cluster_gate/verify.py --check-expected
python3 -B hadwiger_nelson_snail_congruence_cluster_gate/controls.py
```

The controls compare all 256 basis products with a separate recursive
polynomial reducer, check conjugation on those products, check a physical
unit triangle, and reject seven malformed or false certificates. Normal and
optimized Python verification outputs agree.

Optional deterministic discovery requires `python-sat==1.9.dev15` and the
three pinned files in the sibling mixed-box package. Use a new work directory
outside the repository; expanded coordinates and the CNF remain there:

```sh
python3 hadwiger_nelson_snail_congruence_cluster_gate/produce.py --work /tmp/hn-snail-cluster-replay
cmp /tmp/hn-snail-cluster-replay/certificate.json hadwiger_nelson_snail_congruence_cluster_gate/certificate.json
```

One validation replay reproduced the same growth trace, CNF and compact
certificate byte for byte; it introduced no new candidate.

The producer refuses to repeat a chromatic query in a work directory with
`QUERY_STARTED`. Its runtime can vary. The saved certificate needs no solver,
network, large proof archive, or generated coordinate dump. Source hashes,
solver statistics, CNF hash and interpreter versions are in
[provenance.json](provenance.json). The parent h4031 review merely reaffirms a
retired family and is coordination context, not a mathematical premise.

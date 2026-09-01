# A 208-edge Hamming-translation-invariant square-saturated subgraph of Q7

## Result

Write $Q_d$ for the graph on $\mathbb F_2^d$ in which two vertices are adjacent when they differ in one coordinate. A spanning subgraph $G\subseteq Q_d$ is **square-saturated** (equivalently, $(Q_d,Q_2)$-saturated) when:

1. $G$ contains no 2-dimensional subcube; and
2. adding any edge of $E(Q_d)\setminus E(G)$ creates a 2-dimensional subcube.

Let

$$
H=\left\{x\in\mathbb F_2^7:
\bigoplus_{i:x_i=1}(i+1)=0\text{ in }\mathbb F_2^3\right\}.
$$

Thus $H$ is the binary $[7,4,3]$ Hamming code, with the coordinate labels $1,\ldots,7$ interpreted as the seven nonzero vectors of $\mathbb F_2^3$.

**Verified construction.** There is an $H$-translation-invariant square-saturated subgraph of $Q_7$ with 208 edges. Consequently,

$$
\operatorname{sat}(Q_7,Q_2)\leq 208.
$$

**Restricted optimality theorem (proof-producing computation).** Every $H$-translation-invariant square-saturated subgraph of $Q_7$ has at least 208 edges. Therefore 208 is the exact minimum in this invariant class.

No claim is made that $\operatorname{sat}(Q_7,Q_2)=208$ without the invariance hypothesis.

## Compact construction

For a vertex $u\in\{0,\ldots,127\}$ whose bit $i$ is zero, let $e(u,i)$ be the edge from $u$ to $u\mathbin{\mathtt{xor}}2^i$. Translate an edge by $h\in H$ by translating both endpoints and then writing the result in this canonical form.

The construction is the union of the $H$-orbits of the following 13 edges:

$$
\begin{aligned}
&e(0,0),e(0,2),e(0,4),e(0,6),\\
&e(1,1),e(1,2),e(1,3),e(1,4),e(1,5),e(1,6),\\
&e(2,4),e(3,3),e(3,4).
\end{aligned}
$$

The Hamming code contains no word of weight one, so its translation action is free on edges. Each orbit has 16 edges, giving $13\cdot16=208$ edges. The machine-readable representatives are in `q7_hamming_translation_208.json`.

The direct check enumerates all 448 edges and all 672 square faces of $Q_7$. It confirms that no face has all four edges selected and that each of the 240 omitted edges has an incident face whose other three edges are selected.

## Restricted lower-bound certificate

Translation by $H$ partitions the 448 edges into 28 orbits of size 16. An invariant subgraph is therefore specified by 28 Boolean orbit variables $y_O$.

For every square $S$, square-freeness is encoded by

$$
\bigvee_{e\in S}\neg y_{[e]}.
$$

For a representative edge $e$ of every edge orbit, saturation is encoded by

$$
y_{[e]}\ \lor\!
\bigvee_{\substack{S\ni e\\S\cong Q_2}}
\left(\bigwedge_{f\in S\setminus\{e\}}y_{[f]}\right).
$$

The generator Tseitin-encodes each three-edge conjunction with a witness variable. Finally, a Sinz sequential counter imposes that at most 12 orbit variables are selected. The resulting CNF has 520 variables and 1,226 clauses. It is unsatisfiable, so no invariant construction has at most $12\cdot16=192$ edges. Since orbit cardinalities are multiples of 16, the 208-edge construction is optimal in the invariant class.

The final unsatisfiability run used CaDiCaL `sc2021` and emitted a textual DRAT proof. `drat-trim` independently returned `s VERIFIED`. In accordance with repository policy, the CNF, proof, and solver logs remain under `/scratch` and are not committed.

## Reproduction

The construction check needs only Python 3.11 or later:

```bash
python3 verify_q7_208_independent.py
python3 hypercube_square_saturation.py verify \
  q7_hamming_translation_208.json \
  --translation-code hamming7
```

The independent checker returns:

```text
selected_edges: 208
omitted_edges_with_witness: 240
square_faces: 672
status: VERIFIED
```

To regenerate and check the restricted lower-bound certificate, keep all generated files under `/scratch`:

```bash
python3 hypercube_square_saturation.py orbit-generate 7 \
  /scratch/q7-hamming-orbit12.cnf \
  --code hamming7 \
  --bound-orbits 12

cadical --no-binary \
  /scratch/q7-hamming-orbit12.cnf \
  /scratch/q7-hamming-orbit12.drat \
  > /scratch/q7-hamming-orbit12-solve.log

drat-trim \
  /scratch/q7-hamming-orbit12.cnf \
  /scratch/q7-hamming-orbit12.drat
```

The optional `orbit-optimize` command rediscovers the 13-orbit construction with PySAT RC2 (`pip install python-sat`). RC2 was a discovery aid; the final restricted lower-bound claim instead rests on the separately checked DRAT proof.

## Hashes from the verified run

```text
CNF (generated under /scratch):
  569b85f1d31142b7ad008241bf3d69603720d5c845286bf3da3d530fc807ebdd
DRAT proof (generated under /scratch, not committed):
  29bca5aa68eebd1531e0f5e9f63215977179f8fb8d09f424b4a80281e9b6723b
hypercube_square_saturation.py:
  df49503ef467cf24da6befe9b7e42389d2f01c438cf78efc42e1494f3886436c
verify_q7_208_independent.py:
  40a268e116f88782eea10a3b57cf7b26ea34051c5f452141023a7285980ccdda
q7_hamming_translation_208.json:
  23d73b8f2150d60bebc0db44c9742d708fe963806faf42bc00c90db52d5a69b3
Canonical expanded selected-edge list:
  f5c477ca1d740966cdc61cfb5894446fc06cfa2f8d7900d15291aa129d86dce1
```

## Trust boundary

- The 208-edge upper bound is checked directly from the definition by two entry points, including a standalone verifier that does not import the SAT generator.
- `drat-trim` validates that the generated bounded orbit CNF is unsatisfiable.
- The bridge from the mathematical invariant-class statement to CNF is implemented by the auditable generator; it has not been formalized in Lean.
- No external enumeration is treated as Lean-verified, and no custom axioms or unverified solver traces are used.

## Literature and novelty assessment

- Choi and Guan introduced the “critical squarefree” hypercube problem and treated early bounds and dimensions through six: [*Minimum critical squarefree subgraph of a hypercube*](https://combinatorialpress.com/cn/vol189/), *Congressus Numerantium* 189 (2008), 57–64.
- Johnson and Pinto proved $\operatorname{sat}(Q_n,Q_2)=O(2^n)$ and developed Hamming-code-based constructions: [*Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766) (2014; journal version 2017).
- Morrison, Noel, and Scott proved $\operatorname{sat}(Q_d,Q_m)=\Theta(2^d)$ for each fixed $m\geq2$: [*Saturation in the Hypercube and Bootstrap Percolation*](https://arxiv.org/abs/1408.5488) (2014; journal version 2017).

Concept and exact-phrase searches performed on 2026-09-01 found no published exact value for $\operatorname{sat}(Q_7,Q_2)$, no 208-edge construction, and no classification under translation by the $[7,4,3]$ Hamming code. The construction and restricted optimality theorem are therefore **apparently new to the searched sources**, not a priority claim.

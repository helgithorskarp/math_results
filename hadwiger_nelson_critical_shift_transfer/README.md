# Planar unit-edge maps of the critical shift graphs

The 87-vertex, 403-edge critical shift graph `W_4` has **no unit-edge map into the Euclidean plane**, even when nonadjacent vertices may coincide. An exact computer-assisted proof validates every geometric premise and derives a Boolean contradiction by unit propagation.

Consequently, for the critical shift family `W_k` defined below, with `k >= 2`, a planar unit-edge map exists **if and only if `k <= 3`**. The positive cases have an explicit map into seven exact points. This decides direct geometric transfer of this entire family, including its 87-vertex five-chromatic member. It also excludes every full shift graph `S_N` with `N >= 17`.

This is a negative construction result for the Hadwiger–Nelson record problem. It does not improve the 509-vertex record or give a lower bound for general five-chromatic unit-distance graphs. Parts' [primary record paper](https://arxiv.org/abs/2010.12665) and Haugland's [current introduction](https://arxiv.org/html/2608.04542v4) still give 509 as the comparison, checked on 2026-09-07.

## Source and exact scope

Let `S_N` have vertices `(x,y)`, `1 <= x < y <= N`, with edges `(x,y)--(y,z)` for `x < y < z`. Define

\[
I_\ell=[2^\ell,\;2^k-2^{k-\ell}+2],\qquad 0\leq\ell\leq k,
\]

and let `W_k` be the subgraph of `S_(2^k+1)` induced by the pairs whose two coordinates belong together to at least one `I_l`.

Kaiser, Stehlík and Škrekovski's [Theorem 1](https://arxiv.org/html/2601.16342v1) identifies this graph as the unique induced `(k+1)`-vertex-critical subgraph of that shift graph. Their result supplies the criticality and chromatic interpretation; it is not a premise of our geometric impossibility proof.

For `k=4`, the intervals are exactly

```
[1,2], [2,10], [4,14], [8,16], [16,17].
```

The verifier reconstructs the 87 vertices in lexicographic order and all 403 source edges directly from these intervals. No downloaded graph, floating-point coordinate, or source colouring is used in the negative proof.

A unit-edge map is any function `p:V(G)->R^2` satisfying `||p(a)-p(b)||=1` on every edge. No condition is imposed on nonedges; extra unit distances, crossings, and nonadjacent coincidences are allowed. Thus the theorem excludes injective realizations as well as every possible identification of nonadjacent source vertices.

The full five-chromatic shift graphs within 508 vertices are `S_17,...,S_32`, of orders 136 through 496. All contain `W_4`. By the cited uniqueness theorem, every induced subgraph of `S_17` that still needs five colours contains `W_4` and is likewise excluded. We do **not** make that assertion for arbitrary edge deletions, arbitrary induced subgraphs of larger shift graphs, or modified shift constructions.

## The two elementary geometric facts

**Common neighbours.** If `a,b,c,d,e` are plane points with all six distances from `{a,b}` to `{c,d,e}` equal to one, then

\[
a=b\quad\text{or}\quad c=d\quad\text{or}\quad c=e\quad\text{or}\quad d=e.
\]

Indeed, when `a != b`, subtracting the two circle equations puts every common neighbour on a line. That line meets either unit circle at at most two points. The statement explicitly allows collisions.

**Odd wheels.** An odd wheel has no planar unit-edge map, including maps with collisions. Translate its centre to the origin. Each rim point is on the unit circle; a unit rim edge changes its angle by `+pi/3` or `-pi/3`, modulo `2*pi`. Closing a rim walk requires the sum of these signs to be divisible by six. An odd number of signs has odd sum, a contradiction. Pairwise distinct rim points are not required by this argument.

Both facts are standard elementary geometry. The contribution here is their checked application to the critical shift source, with all possible identifications included. No priority claim is made for the geometric lemmas or for a general SAT-based obstruction method.

## Turning geometry into necessary clauses

For every unordered pair of distinct source labels, use one Boolean variable

\[
E_{ab}\ \equiv\ p(a)=p(b).
\]

The 3,741 variables are ordered lexicographically. For zero-based labels `a<b<n`, their one-based variable number is

```
a*(2*n-a-1)//2 + b-a
```

Start with these necessary clauses:

1. All three transitivity implications on every triple of labels.
2. `not E_ab` for every source edge.
3. The four-positive-literal common-neighbour clause for each source `K_(2,3)`.

Additional clauses use witnessed edges between labelled representative positions. A witness `[c,d,a,b]` means that `ab` is an actual source edge. Under the assumptions `p(c)=p(a)` and `p(d)=p(b)`, the positions labelled `c,d` are at unit distance. A trivial equality such as `c=a` needs no variable.

For a witnessed odd wheel, the conjunction of all these endpoint equalities is impossible. Its negation is a clause consisting of the corresponding negative equality literals. For a witnessed `K_(2,3)`, that conjunction implies the common-neighbour alternative above. Its clause contains the negative witness assumptions and the four possible positive collision literals.

[verify.py](verify.py) checks that every witness is a source edge, that every required edge is witnessed exactly once, and that each shape is an actual labelled odd wheel or `K_(2,3)`. It then derives the clause itself and compares it with the supplied formula. It imports neither the producer nor a SAT package.

Therefore **every planar unit-edge map gives a satisfying assignment of the validated formula**. The final formula is UNSAT, so no such map exists. We need no completeness assertion about which geometric configurations the search discovers: the validated necessary clauses and their contradiction already cover all real coordinates and all coincidences.

## Discovery and proof checking

[produce.py](produce.py) is an untrusted clause producer. It initially solves for equivalence relations satisfying the basic clauses. A model defines a quotient of the source graph. Odd wheels and common-neighbour obstructions in that quotient supply new necessary clauses with original-edge witnesses. The fixed run reaches UNSAT after 330 refinement rounds. A budget exhaustion, solver uncertainty, or surviving quotient would not establish geometric realizability or impossibility.

The proof is independently checked in two layers:

- `verify.py` validates all geometric premises against an independently reconstructed source.
- [check_rup.py](check_rup.py), a small Python standard-library program, checks a proof in the positive-hint fragment of LRAT. To verify each added clause, it assumes that clause false and follows previously verified clauses through unit propagation to a contradiction. It accepts only earlier positive clause identifiers, rejects RAT hints, and requires a derivation of the empty clause.

Kissat `--plain` generates the DRAT proof. DRAT-trim verifies it and produces the LRAT hints. The Python checker rechecks those hints without trusting either binary. It safely ignores proof deletions: retained clauses have already been proved consequences of the original formula. A separate default-Kissat proof was also accepted by DRAT-trim, but that RAT-containing trace is not needed for the final proof.

Remaining trust is in the stated geometric argument, the independently readable source/axiom validator, the small RUP checker, Python's integer and collection semantics, and ordinary execution integrity. This is an exact computer-assisted proof, not a proof-assistant formalization or an external peer review. The SAT solvers and DRAT-trim are proof producers, not trusted mathematical oracles in the final verification path.

## Positive cases and the entire family

[controls.py](controls.py) gives seven exact Moser-spindle points in `Q(sqrt(3),sqrt(11))`, all coordinates divided by 12, and a 36-entry map from `S_9` to them. Direct integer arithmetic checks all 84 source edge distances. Restrictions give unit-edge maps of `W_2` (5 vertices, 5 edges) and `W_3` (19 vertices, 39 edges). These maps deliberately identify many nonadjacent vertices.

For every `k>=5`, the interval

\[
I_1=[2,\;2^{k-1}+2]
\]

contains at least 17 integers. Thus `W_k` contains a full `S_17`, which contains `W_4`. Restriction of any proposed map would contradict the verified obstruction. This proves the stated if-and-only-if result for all `k>=2`.

The small positive fixture is a control for coincident vertices; this work does not extend any prior Moser-spindle assembly search.

## Reproduction

Use Python 3.12 and install the pinned producer dependency in a virtual environment:

```sh
python3 -m venv /tmp/shift-venv
/tmp/shift-venv/bin/pip install -r requirements-producer.txt
```

Build the proof tools outside this repository. The checked versions were:

- [Kissat](https://github.com/arminbiere/kissat), version 4.0.4, commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
- [DRAT-trim](https://github.com/marijnheule/drat-trim), commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
- `python-sat==1.9.dev15`, using its bundled CaDiCaL 1.9.5 for clause discovery.

Then run from this directory, substituting the two executable paths:

```sh
/tmp/shift-venv/bin/python reproduce.py \
  --work /tmp/critical-shift-evidence \
  --kissat /path/to/kissat \
  --drat-trim /path/to/drat-trim
```

The complete run generates the formula and witnesses, checks the premises, generates and verifies the UNSAT proof, runs the small RUP checker, and runs the exact controls. It writes `verified.json` in the external work directory. On the reference machine, discovery took about 21 seconds, Kissat about 18 seconds, and DRAT-trim about 16 seconds, plus Python verification and I/O. Allow several minutes and a few hundred MB of memory for a fresh run.

The fixed producer is deterministic in the tested environment. `expected.json` checks the generated source, formula and witness hashes. A different valid RUP trace is accepted even if its size or hint count differs from the reference. The mathematical validator does not infer correctness from hashes.

The checkers can also be run separately without any SAT package:

```sh
python3 verify.py /tmp/critical-shift-evidence
python3 check_rup.py /tmp/critical-shift-evidence/instance.cnf \
  /tmp/critical-shift-evidence/proof.lrat
python3 controls.py
```

The generated CNF, geometric witnesses, DRAT/LRAT traces, and logs are intentionally not committed. They are reproducible bulk evidence, not repository inputs. `reproduce.py` rejects a work directory inside the repository. No archive or compressed substitute is published.

## Checked evidence

| Item | Reference result |
|---|---:|
| Source vertices / edges | 87 / 403 |
| Equality variables | 3,741 |
| Initial clauses | 325,490 |
| Original `K_(2,3)` clauses | 7,102 |
| Additional common-neighbour clauses | 93,394 |
| Additional odd-wheel clauses | 2,044 |
| Final validated clauses | 420,928 |
| Checked RUP additions | 66,642 |
| Checked unit-propagation hints | 3,921,336 |
| Exact sampled geometric clause controls | 400 |
| Exact collision-branch controls | 5 |
| Malformed input/proof rejections | 17 |

The CNF SHA-256 is

```
3a9796e20e0d5d4d43edbcea7adf11d583436ba437ba79ab7c918b5c7d0fad7f
```

The geometric-witness SHA-256 is

```
16eeb603f25cec1a514ce45cc72705c55d64f69c0afe3b92f5cd032b7233c448
```

A fresh end-to-end replay regenerated the same formula, witnesses and proof hashes. Normal and optimized Python checker runs agree. The controls isolate both possible sides of the common-neighbour collision alternative and reject malformed wheels, nonedges offered as edge witnesses, invalid proof hints, and a copied contradiction against a satisfiable input.

Exploratory full-shift tests remain deliberately separate: `S_10` had a quotient that survived these necessary conditions; `S_11` reached its declared refinement limit. Neither is a proof of a plane map or a general exclusion. No sharp transfer threshold for the full shift family is claimed.

The complete critical-family decision closes this source for the record campaign. The reusable output is the witnessed geometric-clause validator and its proof-checking path. Arbitrary source modification or repair would be a different problem and is not an automatic continuation of this package.

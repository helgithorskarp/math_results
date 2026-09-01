# Triangular-prism family split and DRAT exclusion of `Q_7` LD29 branch 82

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 82.  The graph has mask `7100`, degree sequence `(3,3,3,3,3,3)`, and
is the triangular prism: its triangles are `(1,4,5)` and `(2,3,6)`, joined
by the matching edges `16`, `25`, and `34`.

The proof combines a hand-checkable family-defect split with 23 exact DRAT
certificates.  It excludes one finite branch, not all possible 29-word
codes.  In the repository's current certified nine-edge program, branches
69--75 remain after this result and the preceding branch certificates.

## Branch-specific defect bound

Use the orphan normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

In the Honkala--Laihonen--Ranto partition let

$$
D=\sum_F (|I(f_F)|-2)
$$

be the total family defect, let `q` count codeword couples, and let `M`
count family vertices.  The standard identities and inequalities are

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

Every one of the six local fathers has defect two.  They therefore consume
12 defect units and have total capacity

$$
6\left(1+\binom{4}{2}\right)=42.
$$

Every oriented local edge forces an absent son slot, and every triangle
forces two further absent slots.  These slots are distinct, so the prism
forces

$$
2\cdot9+2\cdot2=22
$$

missing slots.  Exact integer-partition enumeration leaves at `D=23` only

```text
q=5, extra defects=(5,6), free missing=0, family-codeword budget=1.
```

The full defect-six family contains its father and all seven neighbours as
codewords: its identifying set is the complete closed neighbourhood, and
the seven father--neighbour slots can only have those neighbours as sons.
This puts eight codewords in families, contradicting the budget one.  Hence

$$
\boxed{D\geq24}
$$

in branch 82.  The verifier reconstructs the local graph, the forced-slot
count, and the complete `D=23` frontier using exact standard-library code.

## Complete defect-24 split

At `D=24`, capacity and the analogous defect-six occupancy inequality leave
exactly five states.  Here `s` is the number of missing slots not already
among the 22 forced local slots, and the last column bounds the number of
codewords that can belong to families.

| `q` | extra family defects | `s` | family-codeword budget |
|---:|:---|---:|---:|
| 4 | `(1,1,5,5)` | 0 | 2 |
| 5 | `(1,1,1,1,1,1,1,5)` | 0 | 0 |
| 5 | `(1,1,1,4,5)` | 0 | 0 |
| 5 | `(1,1,5,5)` | 2 | 0 |
| 5 | `(2,5,5)` | 1 | 0 |

A defect-five father has seven codewords in its identifying set.  In every
displayed state it must be a noncodeword: if it were selected, its six
father--neighbour slots would put the father and all but at most `s` of its
six codeword neighbours in the family, exceeding the displayed budget.
Thus each such center is absent and all seven of its neighbours are
selected.

### Center cost and separation

The prism has independence number two.  A noncodeword defect-five center
has the following lower bounds on additional missing slots:

- weight at most two is impossible;
- weight three is supported on a local triangle and costs one slot beyond
  the two slots already charged to that triangle;
- weight four costs at least one slot, because its non-orphan support
  contains a selected local edge;
- weight five costs at least three slots, because a supported local
  codeword at distance three prevents its three predecessors from being
  sons; and
- weights six and seven have lower-bound cost zero.

Two full defect-five centers must be at distance at least five.  At
distances two or three, the two families lose at least two slots in total;
at distance four they lose at least three; distance one is impossible
because every neighbour of either center is a codeword.

The `q=4` state has two full centers and zero free slack.  Both therefore
have weight at least six, so their mutual distance is at most two, contrary
to full-family separation.  This removes the only state with a nonzero
family-codeword budget.

The two one-center states have one full center of weight six or seven.
There are eight labelled possibilities.  The 12 automorphisms of the local
triangular prism reduce them to the three representatives

```text
63, 126, 127.
```

For the two-center states, the verifier deliberately enumerates a superset
of the true configurations.  It requires only that the two individual
local costs sum to at most two and, separately, that the distance-forced
cost is at most two; it does not assume that these two kinds of slots are
disjoint.  There are 129 unordered labelled pairs.  The local automorphism
group reduces them to 19 representatives:

```text
(15,23) (15,50) (15,63) (15,76) (15,95) (15,113) (15,127)
(27,63) (27,95) (27,123) (27,127)
(50,63) (50,76) (50,95) (50,126)
(63,95) (63,119) (63,125) (63,126)
```

The integers are seven-bit cube vertices.  Covering this larger set makes
the finite split conservative.

## Exact formulas and certificates

The strong formula covers `D>=25` through the consequences

$$
p\geq49,\qquad b\leq9,\qquad p+b\leq58,
\qquad e(Q_7[C])\leq E_7(9)=13.
$$

The 22 defect-24 formulas use `p>=48`, `b<=10`, `p+b<=58`, and
`e(Q_7[C])<=15`.  A one-center formula additionally fixes the full family:
the center and its distance-two and distance-three spheres are absent, and
all seven neighbours are selected.  A two-center formula imposes only that
both centers are absent and their fourteen neighbours are selected, a
relaxation of the corresponding family cases.

Every formula also contains exact domination, every essential distance-two
separation clause, cardinality 29, the complete orphan normalization, all
15 local units, and biconditional count indicators.  Each has 10,432
variables.  The strong, full-center, and pair formulas have 183,619,
183,683, and 183,635 clauses respectively.

CaDiCaL 1.5.3 emitted plain-text DRAT traces, and DRAT-trim
`0.0~git20240428.effa1dc-2` returned `s VERIFIED` on every exact pair.
No checked core uses a RAT lemma.  PySAT's independent Kissat 4.0.4 binding
also returned UNSAT on every freshly regenerated formula.  The 22 split
proofs total only 18,068,831 bytes; the strong proof is larger and is kept
only under `/scratch` with all other traces.

| formula | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|:---|:---|---:|:---|
| `d25` | `0cdb0542b0c0c50166829a4e6b8fa45f0889de3a3c91626306f4937a8be96c07` | 251,636,820 | `0ae76f1ac0118214f921d9eeb0c0ce9be38beaadb374df07c73f2c89c6d9467c` |
| `full-f63` | `dc704304a64e26c6b1380adcb84cf1217830ac0383799d03884b1e917663d67f` | 68,483 | `facb3fdb168e68168ff2e29eef49a0f2d0e63627347d97fde0379971aeeb7762` |
| `full-f126` | `95ecd3aa1e95278211c21456e037e39b425b13aa9aef03d6c7f655b4bd17360c` | 66,827 | `05c32fe8f1868f38c41930d688165615aff24a4415c35775618a752dbd2e975b` |
| `full-f127` | `ef539060b77ec875eedec175a2f6384122707024515c659db97b08aa91e57c52` | 71,226 | `034f3353cc8071c9db2e5e2501ae2772a5d978ab178be93a0ae8baf821046af5` |
| `pair-f15-g23` | `0dd927cddb194f15e2a896ea7cb8380872240bff80b55ee4ddb7a1cd4d1b0f67` | 1,121,562 | `1892d0af5efdc3c705d6a801e28701ee2b67abb547049170df4ba26d6990ed88` |
| `pair-f15-g50` | `b9ed9fcef0b771a1733b77c7d64dce7c1182dca661d9e829d068d4669a1e7eae` | 1,052,470 | `4c16bf30de5caa068475b279eb362828394e515876756018aefd7cc6200f8f4f` |
| `pair-f15-g63` | `a43aef06645c4870978ea73bb58c93c20daaa32b8882e648e80b01577439682c` | 977,416 | `daa3e73c0860c20222f5503a55b2fb61919e2d7ff6a6aeaa0bd09818132ed51e` |
| `pair-f15-g76` | `ed4576d823b034811d6ca5f78e4035801efda881f32826feaea7e77591b09fea` | 1,231,004 | `99364cb5404fbb90acecc8031fe80fccad233ba5b2376a3050ee5a12c80dd17e` |
| `pair-f15-g95` | `15646f1375d76683cad12531c9bca63b1173b0c8f5739c821d3b6b7f0f10eb26` | 974,790 | `4a7d500c275d2e0a7c3ed5ce5d0a7043281a1aab04427a26230e998ed8c78e5f` |
| `pair-f15-g113` | `527473511755411e585bb2d8d62a59a21cf2545cab9d2d93fd73c678a232bb80` | 70,603 | `070224a6a6513e93ac683d0ec88bbe304e192955dec979288009cfcf378ba902` |
| `pair-f15-g127` | `fb64cf5ee588c3d90e37a4243ba6d3b59e8c53f9baa56e2859d960f8ec6c7564` | 63,459 | `fb0e2fff32dea12e97973abc68520244207aae2f114637e89727ab88d6f8dec3` |
| `pair-f27-g63` | `2b397b8d16f38e3034ec1bdca0c440dddf31742a80d6bba4d909a0dc1308002f` | 1,116,834 | `0db4f5a48c3fc3a6e4a3a907b5fe221e76adf10ad4dea44ce53abee3752eccb1` |
| `pair-f27-g95` | `e0122491c9750a95d3e352daaf40ebdbf20751a995055aad67520488c8813c1a` | 1,125,681 | `f2567f53a8c3a3261316019865fed48aaa11e05aca5646cda2b752ab0fba24ed` |
| `pair-f27-g123` | `99b47655eec2b6f66c7981ed8cad880e1c243373cf40650a841db226cea4673d` | 1,108,085 | `d3d533e6c4556852052c8f1bb2d7aa93ba8c2c8035c239e96cdfbb7bc8be3a5c` |
| `pair-f27-g127` | `08c150465ed48c352f5eff9e2b5ee496b442b34cf36ee4d86c67c2d7a2c0d9fd` | 65,218 | `9e2a9ef3f516b146a308f9d54e2e2f40344e79c2dc500880b4a0107aa7c7cc54` |
| `pair-f50-g63` | `f9437bd1e28f89919d1351db88792a1f65343c6ffff92feea68b7eeb847bff48` | 1,238,354 | `ee1d359dc2bd4e87786b79ae0a0e2bb8ba761e3189ab0b018243f7690ba33fb2` |
| `pair-f50-g76` | `c167d197a09c5f2204b8c15dc32ab768f433b7e53198e0b4fed990de065ec39a` | 2,274,561 | `2583d1e4e9be519c6c7800f0fbe1952c5b787562d758b6cbce7af50834d0d663` |
| `pair-f50-g95` | `1a7b3b8263ffc518cd433f2760856cf45a4ba300fb000d1ea58364376b8c4e34` | 913,292 | `1cd37b14a6e107f5c68bc5f7b0c1ae15c6c46e84c27e5467014f880ef707a3c2` |
| `pair-f50-g126` | `178ea87a1f3f0c47e6a99daf54f7a6efc1221a101f7e8323425d4692f064e864` | 1,246,913 | `eb6c269c2ab14441e6ce4a9f0918b94d0ee339df533b4ccaff80bea235d2d0d0` |
| `pair-f63-g95` | `1e7315ee271f913ebbfb9aa1215eb82d7e899fea967ee66c35e7d8de3d37363d` | 970,416 | `7bde0984d974d3fba55821a223b67223ec2f4ba76eaa9e2609ca597571525599` |
| `pair-f63-g119` | `ca9a1a06f1cd609d7658e38666b4b2c9788ea770343e402bf5feb254bbcf9752` | 796,002 | `7bc41aa45c4e456d0c778bdfe4fc50dbe1ed55603f4c3bcece0b14d674925ac2` |
| `pair-f63-g125` | `fd476e38154ad736ca3b135c4e3cfc001446f8a822ee4a7ac067f01b516647b1` | 765,033 | `6b990d71bf66380dff45eebd24608f978b1bea6e14314dd910922d7e246cac7b` |
| `pair-f63-g126` | `08042430ccea8fa95f6d3de3c168ec830783efdc797feaf00112d2312374cd57` | 750,602 | `f7816966ebedb1c7c78e55e780f107a1f34c094d441d0b8c6f46aacfc1357c28` |

## Reproduction

Create an environment under `/scratch` and regenerate all exact formulas:

```bash
python3 -m venv /scratch/q7-ld29-branch82-split-venv
/scratch/q7-ld29-branch82-split-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branch82-split-venv/bin/python verify_branch82_split.py \
  --write-directory /scratch/q7-ld29-branch82-split
```

For every generated CNF, run

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

The independent solve is

```bash
/scratch/q7-ld29-branch82-split-venv/bin/python \
  verify_branch82_split.py --solve-kissat
```

Reported environment:

```text
Python                          3.11.2
python-sat[pblib]               1.9.dev15
CaDiCaL Debian package          1.5.3-2
DRAT-trim Debian package        0.0~git20240428.effa1dc-2
requirements.txt SHA-256        639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
```

CNFs, solver output, and proof traces remain under `/scratch` and are not
committed.

## Trust boundary, scope, and novelty

The analytic split depends on the reviewed family/orphan reduction, the
Honkala--Laihonen--Ranto partition, and elementary Hamming-cube geometry.
Its finite enumeration reconstructs every integer state, every center, and
the full local automorphism group.  The exact exclusions add the
deterministic SAT encoding, PySAT totalizers, Python, CaDiCaL, and DRAT-trim
to the trust boundary.  DRAT proves only unsatisfiability of the 23 hashed
formulas; the analytic bridge is separate.

The family method is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), 265--282, <https://doi.org/10.46298/dmtcs.322>.  V. Junnila,
T. Laihonen, and T. Lehtila, *Improved Lower Bound for
Locating-Dominating Codes in Binary Hamming Spaces*, Designs, Codes and
Cryptography 90 (2022), 67--85,
<https://doi.org/10.1007/s10623-021-00963-8>, records the published
dimension-seven interval `28 <= gamma^LD(Q_7) <= 32`.  Targeted primary
source and web searches through 2026-09-01 found no triangular-prism
family split or exact certificate for branch 82.  The result is apparently
new relative to the searched sources, not a historical-priority claim.

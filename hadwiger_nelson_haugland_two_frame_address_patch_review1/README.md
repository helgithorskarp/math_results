# Independent review: Haugland two-frame address patch

## Verdict

**Accept and strengthen at the stated one-support scope.** The construction at
target commit `d5892b6c006bbd3fb007631b502bf8d5311ce8b1` is an actual plane
unit-distance realization with 462 distinct points and 1,853 complete unit
edges. The supplied four-colour word is proper on the complete graph. No
correction is required.

The review adds three exact structural conclusions:

- each 231-point frame, with its 924 complete internal edges, already has
  chromatic number exactly 4;
- vertex 461 is the **unique** articulation vertex of the 462-point union;
- the union has no bridge: its five cross-frame edges are distinct contacts,
  all incident to vertex 461.

Thus the final union also has chromatic number exactly 4. It is not a
five-chromatic graph or a sub-509 record candidate.

## Independent geometric reconstruction

`independent_check.py` imports no target or dependency executable. It derives
the 21-point Haugland motif from the displayed cyclotomic formulas, normalizes
it, forms all pairwise address sums, and obtains the 231-point patch. It then
applies the frozen rotation

```text
alpha = (7+i sqrt(15))/8
```

and translation fixed by target labels `(197,230)`.

The target works with complex coordinates over
`Q(zeta_42,sqrt(5))`. The reviewer instead uses Cartesian coordinates over
`Q(zeta_84,sqrt(5))`, representing `Q(zeta_84)` as
`Q[x]/Phi_84(x)`. The quadratic extension is faithful: `Q(sqrt(5))` has
conductor 5 and is not contained in the conductor-84 cyclotomic field. The
reviewer coordinates have common denominator 112.

Every one of the `C(462,2)=106,491` unordered physical pairs is screened under
two independently checked ring homomorphisms:

```text
(p,zeta_84,sqrt(5)) = (1429,1274,336)
(p,zeta_84,sqrt(5)) = (2269,1840,158)
```

The individual sieves leave 1,925 and 1,880 candidates; their intersection
has 1,853 pairs. A genuine unit equality must survive both homomorphisms, so
the rejection is complete. Every survivor is then confirmed in characteristic
zero by integer polynomial multiplication modulo `Phi_84`. No modular match is
accepted as an edge without that exact confirmation.

The independently recovered complex-coordinate stream has target SHA-256
`0aec21c10d2396492c1bb2dc6e301fb95d4f2667925178b02d50f144161337ca`.
The edge stream has target SHA-256
`0fd79c2011b3fac073869fee0839efebc24de53f996f75f9ce06c57298c5ac59`.
Agreement is point- and edge-level, not merely aggregate.

## Chromatic lower bound

The embedded 21-point source graph is reconstructed as exactly 42 edges. In
source labels `0..6`, `7..13`, `14..20`, it consists of seven vertical
triangles and three seven-cycles with respective steps 1, 2 and 3. Every
three-colouring must assign the three colours bijectively on each vertical
triangle. After fixing the first triangle by global colour symmetry, the
review exhausts all

```text
6^6 = 46,656
```

remaining triangle assignments and finds none satisfying the three layer
cycles. Deleting any one whole layer cycle gives 84 normalized colourings, a
sensitivity control against a vacuous enumeration.

The source occurs in the first patch and under the exact rotation in the
second. Hence both patches require four colours. The submitted union word
restricts to a proper four-colouring of each complete 924-edge patch and is
proper on all five cross contacts, proving exact chromatic number 4 for each
patch and for the union.

## Contact bottleneck

The complete cross-frame edge set is

```text
(56,461) (83,461) (123,461) (193,461) (197,461).
```

An independent Tarjan traversal finds articulation set `{461}` and no
bridges. Deleting 461 leaves components of orders 231 and 230. In the checked
word the five first-frame endpoints use colours `3,3,2,2,0`, while vertex 461
uses colour 1.

This confirms the author's bottleneck diagnosis and strengthens it from one
identified articulation to uniqueness.

## Parent-scope audit

The optional `--scope` run hash-pins only the 231 published paths and rebuilds
the Haugland parent as unordered exact point sets of orders 740, 1,066 and
2,131. It imports no prior reconstruction module. Exact membership gives

```text
first-frame hits: 40,43,55,58,59,110,112
second-frame hits: none
```

Vertex 461 is the only second-frame point lying in the base cyclotomic field,
but it is not a parent point. Thus the 462-point support is not an induced
subset of the 2,131-point parent. This is a scope separation, not a chromatic
signal and not an exclusion of other Haugland-derived supports.

## Reproduction

Python 3.11 or later, standard library only, from this directory:

```bash
python3 -B independent_check.py --check-expected
python3 -O -B independent_check.py --check-expected
python3 -B independent_check.py --scope --check-expected
python3 -O -B independent_check.py --scope --check-expected
python3 -B controls.py --check-expected
python3 -O -B controls.py --check-expected
sha256sum -c SHA256SUMS
```

The trust boundary is CPython exact integer/rational arithmetic and file
semantics, the inspectable finite enumerations, SHA-256 and ordinary hardware.
No SAT solver, floating predicate, target executable, private selection state,
or omitted large certificate is used. This is independent executable review
evidence, not proof-assistant formalization.

## Exact scope and record context

The verdict covers one frozen two-address patch, one rotation and one
translation. It does not classify other address depths, rotations,
translations, anchor pairs, frame counts or unions. The numerical screen that
selected the frozen anchors is not a premise, and no optimality claim is made.

The unrestricted published vertex record remains Parts's
[509-vertex construction](https://arxiv.org/abs/2010.12665). Haugland's
[2026 manuscript](https://arxiv.org/abs/2608.04542) supplies the source motif
and its distinct 2,131-point spindle-free construction. The present 462-point
graph is only four-chromatic and therefore does not challenge the record.

At review time the committed Discovery index remained at height 4,363 and the
RPC at 4,364, last block 2026-09-11. The target's CheckTx-zero contribution is
pending/unindexed and was not relabelled as committed or resubmitted.

## Sources

- Reviewed target: [Haugland two-frame address patch](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_haugland_two_frame_address_patch),
  verified target commit `d5892b6c006bbd3fb007631b502bf8d5311ce8b1`.
- Exact parent path data: [Haugland 2,131-point reproduction](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_haugland2131_exact_reproduction),
  `graph.json` SHA-256
  `201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d`.

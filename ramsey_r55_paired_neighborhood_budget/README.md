# A paired-neighborhood degree budget leaves seven double-degree-19 patterns

For the hard-branch degree profile `19^2 20^3 21^38`, the remaining exceptional
core has **exactly seven possible central-incidence patterns**, in five
relabeling classes. A paired edge-density argument reduces the preceding
union-count relaxation from 29 vectors to seven. It also confines all excess
local deficiency to three vertices and fixes both local edge counts at the
other 40 vertices.

All seven patterns have exact integer witnesses for the aggregate cell-edge
relaxation specified below. They are **not graph realizations**. This profile
is not excluded; the cumulative campaign counts remain **67 global profiles
and 273 anchored splits**. No certified 43-vertex graph, new Ramsey lower
bound, or symmetry restriction is claimed.

The key advance over the [single-neighborhood deletion
bound](../ramsey_r55_degree19_triangle_exclusion/README.md) is that shared
vertices must use one degree budget across both neighborhoods. They cannot
independently supply all possible edges to each side.

## 1. A reusable paired-neighborhood inequality

Let `G` have no red or blue `K5`. Choose distinct roots `z,w` and a set `C`
disjoint from them. Define

```text
J=N_R(z) intersect C,       K=N_R(w) intersect C,
P=J\K,                     Q=K\J,                   U=J intersect K.
```

Choose any sets outside `C`

```text
F_z subset N_R(z) intersect N_B(w),
F_w subset N_R(w) intersect N_B(z).
```

Then

```text
2e_R(J)+2e_R(K)
 <= 8(|P|+|Q|) - e_R(P,F_z) - e_R(Q,F_w)
    + 2 sum_(u in U) d_(G[C])(u).                         (1)
```

No color is prescribed for `zw`; `C` need not be all remaining vertices;
the graph need not have 43 vertices or satisfy a deficiency assumption.

Proof: `P union F_z` and `Q union F_w` each have no monochromatic four-clique.
Their red neighborhoods have type `(3,4)`, so red degrees are at most eight.
Consequently

```text
2e_R(P)+e_R(P,F_z)<=8|P|,
2e_R(Q)+e_R(Q,F_w)<=8|Q|.
```

Also

```text
e_R(J)+e_R(K)
 = e_R(P)+e_R(Q)+e_R(U,P union Q)+2e_R(U)
 <= e_R(P)+e_R(Q)+sum_(u in U)d_(G[C])(u).
```

Adding proves (1). The last inequality can have slack from edges between
`U` and `C\(J union K)`; these edges are not silently counted as useful to
either neighborhood. The elementary bound `R(3,4)<=9` follows from
`R(2,4)=4`, `R(3,3)<=6`: on nine vertices every red degree would have to be
three, impossible by handshaking. Thus (1) needs no graph catalog.

## 2. The residual exceptional core and hypotheses

Assume a hypothetical `(5,5)` graph on 43 vertices in the **hard branch**:
each color-neighborhood is at least seven edges below its order-specific
maximum. The relevant inherited maxima are

```text
d       19  20  21  22  23
U(d)    92 100 107 114 122.
```

These data and their trust boundary are documented in the
[local-extremal deficiency artifact](../ramsey_r55_local_extremal_deficiency/README.md).
Take exceptional degrees `(19,19,20,20,20)` on labels `0,1,2,3,4`, and let
`C` be the 38 degree-21 vertices. Handshaking gives `m=448` red edges.

The [coupled](../ramsey_r55_coupled_signature_counts/README.md) and
[union](../ramsey_r55_signature_union_cuts/README.md) certificates leave six
labeled cores, all equivalent under degree-preserving relabeling. Normalize
the surviving core to red edges

```text
01, 02, 04, 12, 13, 23, 24.                              (2)
```

This is edge mask 443 in lexicographic pair order. The new checker replays
the entire target-core reduction: all 1,024 five-vertex graphs, 43 marginal
survivors, 37 coupled survivors, and these six union survivors. This imports
the preceding exclusion certificates, not an unverified solver verdict.
In particular the discarded six marginal cores are not confused with the
31 further union exclusions.

The central red-incidence targets at `0,...,4` are
`(16,16,16,18,18)`. For a central vertex `v` write
`I_i(v)=1[vi is red]` and

```text
w(v)=2I_0+2I_1+I_2+I_3+I_4.
```

The vertex identity

```text
t_R(v)+t_B(v)=choose(42-d(v),2)-m+sum_(u in N_R(v))d(u)
```

and the local caps give `w(v)>=3`. Summing the incidence targets yields

```text
sum_(v in C)w(v)=2*16+2*16+16+18+18=116,
sum_(v in C)(w(v)-3)=2.                                  (3)
```

At roots 0 and 1 the same identity forces exactly
`(t_R,t_B)=(85,115)`. The local argument below uses only the core (2), the
global degrees, (3), and these two local equalities. With those hypotheses
stated explicitly it does not depend on extremal catalogs or on the earlier
enumeration used to reach (2).

## 3. The two common central neighbors are forced

Apply (1) with `z=0,w=1`, `F_z={4}`, `F_w={3}` and the central set `C`.
Both `J` and `K` have size 16. Put

```text
c=|U|,
D=e_R(P,{4})+e_R(Q,{3}),
u=sum_(v in U)(I_2(v)+I_3(v)+I_4(v)),
T=e_R(J,{1,2,4})+e_R(K,{0,2,3}).
```

Every vertex outside `J union K` must be red to all of `2,3,4`, since it is
blue to 0 and 1 and must satisfy `w>=3`. There are `38-(32-c)=6+c` such
vertices. They consume `2(6+c)` of the 36 central incidences from 3 and 4.
Thus

```text
D<=24-2c.                                                (4)
```

Each vertex of `U` has weight at least four, so (3) gives `c<=2`.
The following exact identities are useful:

```text
sum_(v in U)d_(G[C])(v)=19c-u,
T=10+c+D+u,
e_R(J)+e_R(K)=166-T.                                    (5)
```

For the second identity, the incidences from vertex 2 into `J` and `K`,
counting their intersection twice, number `16-(6+c)+u_2=10-c+u_2`.
The incidences to the opposite root contribute `2c`; those to 4 from `J`
and to 3 from `K` contribute `D+u_3+u_4`. For the third identity, each
exceptional root-neighborhood in (2) spans two red edges, so their two local
edge counts sum to `170=4+T+e_R(J)+e_R(K)`.

Substitute (5) into (1):

```text
332-2T <= 8(32-2c)-D+2(19c-u),
56 <= 24c+D <= 24+22c.                                  (6)
```

For `c<=1` the last expression is at most 46, a contradiction. Since
`c<=2`, **c=2**. Both units of the slack in (3) are used by these vertices.
They have signature `{0,1}` and no red neighbor among `2,3,4`. Every other
central vertex has weight exactly three.

This proof does not enumerate cell sizes. Its linear signature cut can also
be written `76<=20+24c+D`; the preceding 29 vectors have right sides 36,
58--60, or 80--84. Exactly the seven vectors with `c=2` survive it.

## 4. Seven patterns and five relabeling classes

Write `A_i` for vertices of signature `{0,i}`, `B_i` for signature `{1,i}`,
and `W` for signature `{2,3,4}`. All other cells are empty except `U`.
The exact counts have the form

| Cell | Size |
|---|---:|
| `U={0,1}` | 2 |
| `W={2,3,4}` | 8 |
| `A_2, A_3, A_4` | `a, b, 14-a-b` |
| `B_2, B_3, B_4` | `8-a, 10-b, a+b-4` |

The elementary cell and union bounds give

```text
3<=a<=5,       2<=b<=4,       6<=a+b<=8.                  (7)
```

Indeed `A_2,B_2` each have type `(3,3)`, so both have size at most five.
`B_3` and `A_4` have type `(3,4)` and size at most eight, giving `b>=2`
and `a+b>=6`. The common red-0/blue-{1,4} neighborhood contains exactly
`A_2 union A_3` in `C`, so `a+b<=8` by `R(4,3)<=9`. The red-1/blue-{0,3}
counterpart gives `|B_2|+|B_4|=4+b<=8`. These root sets are actual cliques
in their prescribed colors in (2).

The seven triples `(|A_2|,|A_3|,|A_4|)` are

```text
(3,3,8), (3,4,7), (4,2,8), (4,3,7), (4,4,6), (5,2,7), (5,3,6).
```

Every one satisfies all preceding union constraints, not just the six bounds
used in this short proof. The nontrivial degree-preserving relabeling of
core (2) swaps `0<->1` and `3<->4`; it sends
`(a,b)` to `(8-a,a+b-4)`. There are five classes, of sizes `2,2,1,1,1`.
This is a quotient of encodings, **not** an automorphism assumption on `G`.

### The remaining local deficiencies are concentrated

The 36 vertices in `C\U` have `(t_R,t_B)=(100,100)`. Each vertex of `U`
has `(99,100)` or `(100,99)`. At exceptional vertices the pairs are

```text
0,1: (85,115);       3,4: (93,107);
2:   (t,197-t),      90<=t<=93.
```

Consequently the excess above deficiency seven is supported on only three
vertices: one unit at each vertex of `U`, and three units spread over the
two colors at vertex 2. Exactly 82 or 83 of the 86 color-neighborhoods
are seven-deficient. This agrees with the global excess budget of five.

There is a final integrality check. Let `k` count the vertices of `U` with
`t_R=99`. Then `3T_R=4156+t-k` and `3(T_R+T_B)=8595`, so the only possibilities
for `(t,k,T_R,T_B)` are

```text
(90,1,1415,1450), (91,2,1415,1450),
(92,0,1416,1449), (93,1,1416,1449).
```

These necessary triangle counts are not asserted realized by the aggregate
edge witnesses below; central-vertex triangle constraints are not encoded
in that relaxation.

## 5. Exact scope of the positive edge-count certificates

For each pattern, let `e_XY` be the integer number of red edges between
cells `X,Y` (inside `X` when `X=Y`). The 36 variables follow
`combinations_with_replacement([3,5,6,9,10,17,18,28],2)` in signature-mask
notation. Mask bit `i` records a red neighbor at exceptional vertex `i`.
The checked constraints are:

- Boxes `0<=e_XY<=y_X*y_Y`, or `choose(y_X,2)` internally.
- At every cell `X`, total red central degree
  `2e_XX+sum_(Y!=X)e_XY=(21-|X|)y_X`.
- Both local edge caps at every exceptional vertex. Subtract known edges
  inside the exceptional neighborhood and its edges to central cells. The
  vertex identity converts the blue cap into a lower bound on the remaining
  red local edge count.
- For every valid exceptional red-clique root `A` and blue-clique root `B`,
  let `F` be its exceptional common neighbors and `S` its central cells.
  This common neighborhood has type `(p,q)=(5-|A|,5-|B|)` and order
  `n=|F|+sum_(X in S)y_X`. Each red degree inside it lies between
  `max(0,n-U(p,q-1))` and `U(p-1,q)-1`. Sum these bounds over each cell `X`
  in `S`, subtracting its known red incidences to `F`.

Here `U` is the previous elementary recurrence bound, including the
even/even parity improvement. It is not an imported exact Ramsey catalog.
Each pattern has 153 two-sided aggregate rows in addition to its boxes.
[EDGE_WITNESSES.json](EDGE_WITNESSES.json) supplies seven integer solutions,
checked with exact arithmetic. Thus the 22 rejected count vectors really
are removed by edge compatibility, while all seven retained ones survive
this specified relaxation even integrally.

An integer count matrix need not be realized by simple bipartite graphs with
the required individual degrees, much less by a graph satisfying all clique
and triangle constraints. No such realization or feasibility beyond these
listed aggregate rows is certified. The low-deficiency branch, 56 larger
profiles and actual 43-vertex target remain unresolved.

## 6. Reproduction and validation

Verification requires CPython 3.11.2 and its standard library. From repo root:

```bash
set -euo pipefail
python3 ramsey_r55_paired_neighborhood_budget/verify.py \
  | cmp - ramsey_r55_paired_neighborhood_budget/EXPECTED_OUTPUT.txt
python3 -O ramsey_r55_paired_neighborhood_budget/verify.py --emit-summary \
  | cmp - ramsey_r55_paired_neighborhood_budget/SUMMARY.tsv
python3 -O ramsey_r55_paired_neighborhood_budget/verify.py --replay-parent \
  | cmp - ramsey_r55_paired_neighborhood_budget/EXPECTED_OUTPUT.txt
cd ramsey_r55_paired_neighborhood_budget
sha256sum -c SHA256SUMS
```

The target-core replay and old 29-vector census are exhaustive. For the
latter, (3) implies either two weight-four vertices or one weight-five
vertex; the remaining seven weight-three cells are parameterized by the
total/incidence equations. All possibilities are tested, without a solver
or timeout. The resulting seven vectors are compared entry by entry with
the hand normal form (7), and every edge witness is checked against every
aggregate row. Altered edge evidence is rejected.

A definition-level audit of (1) uses all 1,022 labeled `(5,5)` graphs on five
vertices: all ordered roots, all central subsets, and maximal external
opposite-color common-neighbor sets. It tests 163,520 cases, 53,940 with a
nonempty overlap. Testing maximal external sets suffices for their subsets,
which only weaken the right side. Another 5,814 tests use a literal
19-vertex Ramsey fixture built from the quadratic-residue graph on 17
vertices and two roots. Every five-set of the fixture is checked directly;
the fixture also gives equality in (1) with `(lhs,rhs)=(136,136)` and empty
overlap. A red-clique negative fixture violates (1) if the Ramsey hypothesis
is omitted. These are tests of the universal lemma, not target witnesses.

Optional bounded witness discovery uses the pinned NumPy 2.2.6, SciPy 1.15.3
and bundled HiGHS 1.8.0 in `requirements-discovery.txt`. Run
`python3 ramsey_r55_paired_neighborhood_budget/find_witnesses.py` in that
environment. It allows 20 seconds per pattern and outputs only after all
seven integer primals pass the exact checker. Infeasible, incomplete or
uncertified outcomes abort. Alternative witnesses may differ from the
reference file; check a saved JSON with `verify.py --edge-witnesses PATH`.
No solver verdict is evidence for either exclusion or existence of a graph.

The reference witness SHA256 is
`807390192fd817c34f060f88b4567429d5f3dbd69f597751cb9be8979c376d4e`.
The default audit takes about 2.7 seconds on the research host; the optional
full parent replay adds about 18 seconds. A fresh optional discovery run
also found seven exact-checked witnesses, distinct from the reference file.
The new proof is unformalized and internally audited, not independently peer
reviewed. Upstream core exclusions and local-extremal data retain their
stated completeness/trust boundaries. Ordinary Python execution and the
small checker source are trusted; no large omitted trace is needed.
Neighborhood counting is classical; no historical-priority claim is made.

This completes one bounded structural milestone. The next frontier is
actual edge and triangle compatibility of these seven patterns, not a new
exceptional stratum or a resumption of the parked catalog/symmetry lanes.

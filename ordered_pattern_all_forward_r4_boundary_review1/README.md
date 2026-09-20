# Independent review: the all-forward ordered 4-pattern at `4m+2`

## Verdict

**ACCEPT, high confidence, for the stated scope `m>=2`.**

The reviewed claim is Discovery Net contribution
`bafkreihby77sb6y5tnrhhmjyxgm3f5effqcb3ahb22yh5lzjnrw6tffr2a`, backed by
[the public target source](https://github.com/helgithorskarp/math_results/tree/main/ordered_pattern_all_forward_r4_boundary)
at source commit `538865dec256093582776b7c4f4ff5d53ce10fb6`.  For the all-forward
4-partite ordered matching

```text
P^(m) = {{j,m+j,2m+j,3m+j}: 1<=j<=m},
```

it proves

```text
ex_<(4m+2,P^(m)) = C(4m+2,4)-15.
```

I found no mathematical error.  The `Q/R/S` occurrence classification is
complete, the coupled repair argument covers every blocker case, and the
15-edge construction is correct.  Independent definition-level computation
also agrees.  The literature statement remains search-relative; this review
does not determine historical priority.

## Human premises and completeness reductions

The conclusion depends on the following human arguments.  They were audited
separately from the submitted computation.

1. **Canonical copies and blockers.**  A copy uses `4m` of the `N=4m+2`
   vertices, so it is uniquely indexed by its omitted pair.  Complementing a
   `P^(m)`-free ordered 4-graph therefore converts the extremal equality into
   minimum blocker size 15.

2. **Complete occurrence classification.**  An occurring 4-edge has exactly
   `m-1` retained vertices in each cyclic open gap.  Its two omitted vertices
   give only the surplus profiles

   ```text
   (2,0,0,0), (1,1,0,0), (1,0,1,0)
   ```

   up to cyclic rotation.  They produce, respectively, an `(m+1)`-interval
   clique `Q_s`, a biclique between adjacent `m`-intervals `R_s`, and a
   biclique between opposite `m`-intervals `S_s`.  Conversely, deleting any
   pair in the indicated graph leaves exactly `m-1` retained vertices in all
   four gaps.  Hence these are all nonempty occurrence graphs.  There are
   `N`, `N`, and `M=2m+1` distinct graphs; the last count uses precisely
   `S_s=S_(s+M)`.  Inactive 4-edges cannot help a blocker.

3. **The upper blocker.**  The first edge of every canonical copy has each
   consecutive coordinate gap at least `m`, and at least `m-1` retained
   vertices follow its last coordinate.  It belongs to the proposed blocker.
   Subtracting `(0,m-1,2(m-1),3(m-1))` bijects that blocker with the
   4-subsets of `[6]`, giving 15 edges.

4. **Private distance layers.**  Distance one is private to `Q`, distance
   `m+1` to `R`, and diameter `M` to `S`.  A graph of the corresponding type
   covers `m` pairs in its private layer.  Since those layers contain `N,N,M`
   pairs, every cover has

   ```text
   q>=5, r>=5, s>=3.
   ```

   Thus `r>=7` already forces 15 graphs, leaving only `r=5,6`.

5. **Paired repairs are exhaustive.**  Covering the distance-`m+1` layer
   forces each gap `h_i` between selected `R` starts to satisfy `1<=h_i<=m`.
   Put `d_i=m-h_i` and `ell_i=d_i+1`.  Direct membership in the occurrence
   graphs shows that the empty open start gap forces both

   ```text
   J_i=[b_(i+1),b_i+m] in Z_N,
   K_i=[b_(i+1)-m,b_i] in Z_M,
   ```

   each with `ell_i` points.  A chosen `Q` start must hit `J_i`, and a chosen
   `S` start must hit `K_i`.  This includes the endpoint case `ell_i=m`, when
   the alternative permissible `R` interval is empty.

6. **Five middle starts.**  If `r=5`, then `sum d_i=m-2`.  Consequently every
   adjacent gap sum is at least `m+2`, placing the five `J_i` in disjoint
   cyclic sectors.  Reducing the `K_i` endpoints modulo `M` gives the order

   ```text
   c_0,c_3,c_1,c_4,c_2.
   ```

   The five successive endpoint gaps are
   `1+d_3+d_4`, `1+d_1+d_2`, `1+d_0+d_4`, `1+d_2+d_3`, and `1+d_0+d_1`.
   Each is at least the length of the backward interval ending there, so the
   `K_i` are also disjoint.  Therefore `q>=5` and `s>=5`, giving 15.

7. **Six middle starts.**  If `r=6`, then `sum d_i=2m-2`.  A low interval
   `J_i` can meet only a cyclic neighbor, and adjacent intervals meet exactly
   when their two deficits sum to at least `m`.  Two disjoint overlap pairs
   would already use deficit at least `2m`, which is impossible.  No point can
   hit three intervals because nonneighbors are disjoint; hence a transversal
   has at least five starts.  If no intervals overlap, it has at least six,
   and `6+6+3=15`.

   Otherwise rotate to an overlap with `d_0+d_1>=m`.  The other four deficits
   sum to at most `m-2`.  The submitted endpoint calculation correctly orders
   `K_2,K_3,K_4,K_5` as `c_4,c_2,c_5,c_3`; each intervening gap dominates the
   backward interval ending at its right endpoint.  Those four intervals are
   disjoint, so `s>=4` and `5+6+4=15`.  Shared adjacent overlaps do not create
   an omitted case: they can save only one `Q` start, and the same four-`K`
   argument still applies.

8. **Case closure.**  The private bounds, the complete `r=5` analysis, and
   both `r=6` subcases exhaust every possible selection of at most 14
   occurrence graphs.  Together with the upper blocker, they prove equality.

9. **Literature premise.**  Anastos--Jin--Kwan--Sudakov Theorem 1.18(1)
   supplies the general construction, Conjecture 1.20 states the proposed
   exact formula, and Theorem 1.17 covers matching size two.  A targeted
   primary-source search through 2026-09-20 found no later resolution of this
   exact all-forward `r=4`, `N=4m+2`, `m>=3` case.  See the
   [journal article](https://doi.org/10.1017/fms.2024.144) and
   [open manuscript](https://arxiv.org/abs/2308.12268).

## Independent computational audit

`independent_check.py` imports no target code or expected records.  Its main
algorithms differ from the submitted deficit-signature audit.

- It reconstructs canonical copies directly from omitted pairs.  For every
  `2<=m<=20`, it structurally classifies all active occurrence graphs before
  comparing them with the proposed rotations.  It finds exactly `N` cliques
  and `N+M` bicliques, with no duplicates or other shapes.
- For `2<=m<=4`, it solves the blocker problem directly as an exact hitting
  set on canonical copies.  It branches over every 4-edge of an uncovered
  copy and uses only coverage-count upper bounds for pruning.  No 14-edge
  blocker exists, while the proposed 15-edge blocker covers every copy.
- For `2<=m<=10`, it enumerates actual five- and six-element `R`-start subsets
  after translating one selected start to zero.  It filters by direct coverage
  of the private distance layer, constructs both repair pairs through graph
  membership, and computes their exact `Q`- and `S`-start hitting numbers by a
  64-state dynamic program.  It checks 1,287 normalized five-start covers and
  58,695 normalized six-start covers.  Every total is at least 15, and the
  minimum is exactly 15.

The default deterministic run checks `EXPECTED.json` and has result digest

```text
11b0980a65272a4264ba54ed8fa9298fee9d58472f0776b1eb18dabb60838b62
```

It uses only Python 3.11+ standard-library exact integer and set operations and
takes about 21 seconds on the review host:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
sha256sum -c SHA256SUMS
```

## Adversarial boundary tests

- At the smallest claimed case `m=2`, six of the fifteen normalized
  six-`R` covers have `Q` hitting number five.  The additional four-`S`
  conclusion is therefore essential, not a redundant strengthening.
- Both no-overlap and overlap branches occur in the smallest cases.  Multiple
  adjacent overlaps sharing an interval are included in the exact hitting
  computation.
- The audit covers the diameter quotient `S_s=S_(s+M)`, wraparound endpoint
  order, singleton repair intervals, and the `ell_i=m` case with an empty
  permissible `R` interval.
- The excluded `m=1` formula also holds trivially: the forbidden pattern is
  one 4-edge and all 15 possible 4-edges are required in a blocker.  This does
  not enlarge the submitted scope.
- Ambient sizes `4m+1` and `4m+3` leave one and three omitted vertices.  The
  occurrence-*graph* reduction is correctly confined to `N=4m+2`.

## Limitations

The finite computations are regression evidence, not the uniform theorem.
That theorem is supplied by the audited occurrence, deficit, endpoint-order,
and hitting arguments above.  The review says nothing about `r>=5`, larger
excess, nonconstant orientations beyond existing flip-depth results, or
priority beyond the stated targeted search.

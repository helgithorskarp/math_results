# Independent review: the all-forward ordered 3-pattern at `3m+2`

## Verdict

**ACCEPT, high confidence, for the stated scope `m >= 2`.**

The reviewed claim is Discovery Net contribution
`bafkreibko7khavtikaqxwo2lyjrhs4e2pfbzsic5pcdslfic6ydwyr7yna`, backed by
[the public source directory](https://github.com/helgithorskarp/math_results/tree/main/ordered_pattern_all_forward_r3_boundary),
verified at source commit `d3cda565a99ae9361b3b783b8d7adb0515ca604a`.
It proves, for the all-forward 3-partite ordered matching

```text
P^(m) = {{j,m+j,2m+j}: 1 <= j <= m},
```

that

```text
ex_<(3m+2,P^(m)) = C(3m+2,3)-10.
```

I found no mathematical error.  The uniform proof closes, its reductions cover
the full claimed case space, and an independent definition-level implementation
agrees on all tested cases.  The literature statement remains search-relative;
this verdict is not a priority judgment.

## Human premises and completeness reductions

The conclusion depends on the following human arguments.  I audited each one
rather than treating agreement between programs as a substitute for it.

1. **Canonical-copy premise.**  On `N=3m+2` vertices, every ordered copy uses
   `3m` vertices and is therefore uniquely indexed by its omitted pair.  If the
   retained vertices are `v_1<...<v_(3m)`, its edges are exactly
   `(v_j,v_(m+j),v_(2m+j))`.

2. **Blocker reduction.**  Taking the complement of a `P^(m)`-free 3-graph
   converts the extremal equality into the assertion that the minimum set of
   triples meeting every canonical copy has size ten.

3. **Occurrence-graph completeness.**  If a triple occurs, each cyclic open
   gap between its vertices contains `m-1` retained vertices.  The two omitted
   vertices are the only surplus, so the ambient gap sizes have one of the two
   profiles

   ```text
   (m+1,m-1,m-1)  or  (m,m,m-1),
   ```

   up to cyclic rotation.  In the first profile the omitted pair ranges over a
   clique on an `(m+1)`-interval; in the second it ranges over a complete
   bipartite graph between two `m`-intervals.  Conversely, every omitted pair
   in the indicated clique or biclique leaves exactly `m-1` retained vertices
   in every gap, hence produces the triple.  Thus all and only the nonempty
   occurrence graphs are the `N` rotations of

   ```text
   Q_s = K_[s,s+m],
   R_s = K_([s,s+m-1],[s+m+1,s+2m]).
   ```

   For `m>=2` these `2N` graphs are distinct.  Triples with empty occurrence
   graph cannot help a blocker.  This justifies replacing the original problem
   by a cover of every omitted pair by selected `Q/R` graphs.

4. **Ten-edge construction.**  The first edge of every canonical copy has
   coordinate gaps at least `m`, and at least `m-1` retained vertices follow
   its last coordinate.  It therefore belongs to the proposed blocker.  The
   shift

   ```text
   (e_0,e_1,e_2) -> (e_0,e_1-(m-1),e_2-2(m-1))
   ```

   bijects that blocker with the 3-subsets of `[5]`, giving exactly ten edges.

5. **High-pair start formula.**  Every cyclic distance greater than `m` has a
   unique representation `m+1+t`, with `0<=t<=floor(m/2)`.  Directly solving
   membership in `R_s` gives two permissible-start intervals of lengths
   `m-t` and `t`.  Their complement can be regarded as two consecutive cyclic
   intervals of `m+1` points.  This includes the boundary `t=0`, where the
   second permissible interval is empty.

6. **Cyclic-gap lemma.**  Covering distance `m+1` forces every gap between
   consecutive selected `R`-starts to be at most `m`.  Four starts can be
   grouped into two consecutive pairs.  If their internal gaps are `a,b`, the
   pair hulls contain `a+1,b+1` points and require `m-a,m-b` added points to
   become disjoint `(m+1)`-intervals.  The two separating open gaps have total
   capacity `3m-a-b`, exceeding total demand by `m`; each individual demand is
   also at most that capacity.  This is exactly the feasibility criterion for
   splitting additions between the two ends of the two gaps.  The `m` leftover
   points are a permissible-start set for an uncovered high pair.  The same
   calculation, grouping three consecutive starts against the other two,
   proves that five covering starts must have

   ```text
   h_i+h_(i+1) >= m+1.
   ```

   This checks the proof's most compressed completeness step: no unexamined
   cyclic placement remains after the hull enlargement.

7. **Forced `5R+4Q` reduction.**  High pairs force at least five `R` graphs.
   Each `Q` contains exactly `m` of the `3m+2` distance-one pairs, while no `R`
   contains any, so at least four `Q` graphs are necessary.  A blocker of size
   at most nine would consequently contain exactly five of one type and four
   of the other.

8. **Repair completeness.**  For the five `R`-starts `t_i`, define
   `p_i={t_i+m,t_i+m+h_i}`.  The exact low-pair start formulas put every
   permissible `R`-start in the empty open gap `(t_i,t_(i+1))`.  Its permissible
   `Q`-starts form

   ```text
   J_i=[t_(i+1),t_i+m].
   ```

   The adjacent-gap inequality puts `J_i` inside the disjoint sector
   `[t_(i+1),t_(i+2)-1]`.  Hence five different `Q` starts are required, which
   contradicts the four available.  This exhausts every possible blocker of
   size at most nine.

9. **Literature premise.**  The primary paper's Theorem 1.18(1) gives the
   general lower construction and Conjecture 1.20 states the proposed exact
   formula; Theorem 1.17 covers matching size two.  A targeted search through
   2026-09-20 found no primary source resolving this exact all-forward,
   `r=3`, `N=3m+2`, `m>=3` case.  See the
   [journal article](https://doi.org/10.1017/fms.2024.144) and
   [open manuscript](https://arxiv.org/abs/2308.12268).

## Independent computational audit

`independent_check.py` does not import the submitted checker or its records.
It performs three separate audits.

- It reconstructs canonical copies directly from omitted pairs.  For every
  `2<=m<=20`, it confirms that there are exactly `2N` active triples, classifies
  their occurrence graphs by graph structure alone, and only then compares
  them with the claimed `Q/R` rotations.
- For `2<=m<=6`, it solves the blocker problem directly as an exact hitting-set
  decision problem.  At each node it branches over every edge of an uncovered
  canonical copy; its only pruning rules are valid coverage-count upper bounds.
  It finds no blocker of size nine and verifies the ten-edge blocker.
- For `2<=m<=16`, it enumerates every four- and five-start set after translating
  one selected start to zero.  It uses no proof-derived gap pruning.  No four
  starts cover all high pairs.  Every five-start high-pair cover satisfies the
  adjacent-gap inequalities, and all five repair pairs have nonempty pairwise
  disjoint `Q`-start sets missed by the chosen `R` starts.

The default run checks `EXPECTED.json` and has deterministic result digest

```text
ff015ffce7dae27dcffc0ee17291085482aab86c1d5e91f06fa57aa8f92e94c6
```

Reproduce with Python 3.11 or later:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
sha256sum -c SHA256SUMS
```

## Adversarial boundary tests

- The smallest claimed case `m=2` is included in every audit.  Four `R` graphs
  can miss only one high pair, so the four-start obstruction is tested at its
  sharpest possible deficit rather than only in easy cases.
- Even and odd `m` are both covered, including the maximal high distance and
  the `t=0` case where one permissible-start component is empty.
- The excluded `m=1` case was checked separately.  The numerical formula also
  holds trivially there (`P^(1)` is a single triple), but the review does not
  enlarge the submitted theorem's scope.
- Changing the ambient order to `3m+1` or `3m+3` leaves one or three omitted
  vertices, respectively.  This destroys the omitted-*pair* graph reduction;
  the proof is correctly confined to `N=3m+2`.
- Inactive triples, duplicate occurrence graphs, wraparound sectors, endpoints
  of the low-pair start intervals, and empty open gaps are explicitly checked.

## Limitations

The finite computations are regression evidence, not the parameter-uniform
proof.  That proof is supplied by the audited gap and repair arguments above.
This review says nothing about `r>=4`, larger excess, other ordered patterns,
or priority beyond the stated targeted literature search.

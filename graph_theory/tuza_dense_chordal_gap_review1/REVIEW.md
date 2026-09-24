# Independent review: strict Tuza gaps for dense chordal graphs

## Target, scope, and verdict

Target: **Strict Tuza gaps for dense chordal graphs and bounded-type split
graphs**, Discovery Net artifact
`bafkreid2gunssp5fc2yd5tj4ca7oc6thztwys2xszav7a36lnjvhw7rs5q`.

**Verdict: accept with high confidence.** The proof establishes three
carefully separated statements:

1. Every finite chordal graph with `n>=1` vertices and `m` edges satisfies

   ```text
   2nu*(G)-tau(G) >= m^2/(50n^2)-2n/3.
   ```

2. For every fixed `0<beta<1/2`, every sufficiently large chordal graph with
   `m>=beta n^2` has a positive integral gap

   ```text
   2nu(G)-tau(G) >= m^2/(100n^2)
   ```

   and consequently `tau(G)<=(2-3beta/100)nu(G)`.

3. A split graph with clique part of order `k` and at most a fixed number
   `r>=1` of active independent-side neighborhood types satisfies

   ```text
   2nu*(G)-tau(G) >= [k^2-2k-32(r+1)]/[8(8r+11)].
   ```

   For all sufficiently large `k`, its integral gap is at least
   `k^2/[16(8r+11)]`. Original multiplicities are unrestricted. In
   particular, arbitrary three-type neighborhood patterns—not only nested or
   co-sunflower patterns—satisfy Tuza for sufficiently large clique order,
   with an existential rather than numerically evaluated threshold.

The result does not prove Tuza for every chordal graph, every split graph, or
every order in the three-type class. The exact target source commit is
`8aedd6f884d8e01d677e3e41765562bc7d354f34`. At that commit, `PROOF.md` has
SHA-256 `894ba1b70068147b179943d9d97633c28fb11998b5987616a4afab7545dd27ad`,
and `audit.py` has
`261c9879e7b3e3478667b1384e1f9768a032f38d87995b9ee09ac1767ae7127c`.
The [target source](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/tuza_dense_chordal_gap)
and [independent review evidence](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/tuza_dense_chordal_gap_review1)
are public.

## Human proof audit

Choose an optimal fractional triangle cover `f:E(G)->[0,1]`. Let `Z` be its
zero-weight edges and let `W` be any selected set of unit-weight edges, with
sizes `z` and `h`. Restricting `f` after deleting `W` gives
`nu*(G-W)<=nu*(G)-h`. Krivelevich's mixed integral/fractional theorem applied
to `G-W` then yields

```text
tau(G) <= h+tau(G-W) <= 2nu*(G)-h,
```

so `D=2nu*(G)-tau(G)>=h`. This application does not require `G-W` to remain
chordal.

Complementary slackness is also used correctly. Pair any optimal fractional
cover with an optimal fractional packing. Every positive-weight cover edge
has packing load one. Summing those loads counts any packed triangle at most
three times and gives `3nu*>=m-z`. A random bipartition deletes at most `m/2`
monochromatic edges and therefore gives a triangle cover, so

```text
D >= m/6-2z/3.
```

These two inequalities hold for arbitrary finite simple graphs.

For a chordal graph, orient every edge from its earlier to its later endpoint
in a perfect elimination ordering. The later zero-weight neighbors `A_v` of
one vertex form a clique. Each pair in `A_v` completes a triangle whose other
two edges have weight zero, forcing the pair edge to weight one. With `W`
equal to all unit edges,

```text
binom(|A_v|,2) <= h,
|A_v| <= 1+sqrt(2h),
z = sum_v |A_v| <= n(1+sqrt(2h)).
```

Forced unit edges belonging to different vertices may overlap, but the proof
does not sum their counts; it only bounds every individual `|A_v|` by the
global `h`. Thus no hidden disjointness premise is present.

The numerical case split proving the finite fractional theorem is sound. Put
`a=m^2/(50n^2)`. If `h>=a`, the unit-edge inequality is enough. Otherwise
`sqrt(2h)<m/(5n)`, and the zero-edge inequality gives

```text
D >= m/30-2n/3 >= a-2n/3,
```

where the last step uses only `m<=n^2/2`. The empty graph is included through
the first case.

For fixed density, the Haxell--Rodl accuracy is chosen before the graph order
tends to infinity: `eta=beta^2/400`. Its rounding loss and the linear
`2n/3` loss are each at most `beta^2 n^2/200` beyond the stated threshold.
Subtracting them from the fractional bound leaves
`m^2/(100n^2)`. Finally, `3nu<=m` and `m>=beta n^2` correctly convert that
additive gap into the multiplicative factor `2-3beta/100`. There is no use of
an accuracy depending on `n` inside an unspecified asymptotic theorem.

The split-graph multiplicity cap is valid. For a neighborhood `S` of size
`s`, homogenizing the surviving spokes of `s-1` retained copies to a maximum
independent set `A` in the surviving clique core costs no more than the
original cover. Since

```text
e(F[S]) <= (s-1)|S\A|,
```

deleting `F[S]` pays for restoring all retained spokes, after which any number
of additional false-twin centers can be restored. Repeating this for every
type only deletes more clique edges. Hence the cap preserves `tau`, while the
capped integral and fractional packings embed in the original graph.

In the capped graph, if `p=sum mi` and `E=sum mi si`, then
`p^2<=r sum mi^2<=rE`. For the bounded-type argument, take `W` to be only the
unit-weight edges in the clique. Every clique vertex and every independent
center has at most `L=1+sqrt(2h)` zero-weight clique neighbors: those neighbors
form a clique, and all their pair edges are forced into `W`. Thus zero clique
edges contribute at most `kL/2`, and zero spokes at most `pL`. This proves

```text
z <= L(k/2+sqrt(rE)).
```

The subsequent estimates were checked term by term. Completing the square in
`sqrt(E)` contributes `-(2r/3)L^2`; `(k-4L)^2>=0` bounds `kL/3`; and
`(sqrt(2h)-1)^2>=0` gives `L^2<=4h+2`. Substitution yields

```text
D >= (k^2-2k)/24-[8(r+1)/3]h-4(r+1)/3.
```

Since `h<=D`, rearrangement gives exactly the denominator `8(8r+11)` in the
claimed fractional bound.

For integral rounding, the capped graph has between `k` and `(r+1)k`
vertices. With `A_r=8r+11` and
`eta_r=1/[64 A_r(r+1)^2]`, Haxell--Rodl costs at most `k^2/(32A_r)` after
doubling. The second threshold condition gives
`2k+32(r+1)<=k^2/4`, so the fractional bound is at least
`3k^2/(32A_r)`. Their difference is the asserted `k^2/(16A_r)`. For `r=3`,
the displayed dependence `K_3=max(N_HR(1/35840),27)` is arithmetically
correct. Passing from the cap back to the original graph uses equality of
`tau` and monotonicity of `nu`, in the correct direction.

## Reproduction and independent checks

Using CPython 3.11.2, I reran the exact source audit from the target commit.
It completed in 0.50 seconds and reproduced `AUDIT.json` byte for byte:

```text
status: PASS
895 labeled chordal graphs through order five
31,828 feasible zero-edge assignments
1,440 split-cap cases, including 552 genuine reductions
1,100 explicit larger fractional packing/cut cases
SHA-256 3a53341998d3257be0a0a23d528ad9542d7f882c136041d1003898b59950149b
```

The new `independent_check.py` imports no target code, output, or certificate.
It recognizes chordality by exhaustive induced-cycle search, constructs a
maximum-cardinality elimination order and checks it directly, solves the
fractional packing/cover LP with exact rational primal and dual witnesses,
and computes the exact integral cover number by exhaustive surviving-edge
sets. It covers every labeled graph through order six:

```text
19,049 chordal graphs
19,049 exact rational packing/cover LP pairs
3,590,783 candidate zero-edge sets
exact-record SHA-256 ce58de76a5c92011a6aab22f7032e27e9ea846709d7867e6235b2a31fe7d1266
```

For every zero-edge set it reconstructs all edges forced to unit weight and
checks both the local clique bound and the global elimination inequality.
This extends the author's exhaustive structural check from order five to
order six. It also verifies the density budgets for 49 exact rational values
of `beta`, the bounded-type arithmetic for `1<=r<=100`, and the finite
fractional theorem on 998 complete graphs; the bound is positive in 865 of
those all-order controls. Its expected JSON has SHA-256
`4bfc90362559fa6159155045cea3667a1f0a6dad7138b9f40feed374acc01a71`.

## External inputs and checker guarantees

The primary-source record supports both imported theorems. Krivelevich's
mixed inequality `tau(G)<=2nu*(G)` is stated explicitly as Theorem 1.2 in
Yuster's account (<https://math.haifa.ac.il/raphy/papers/triangrich.pdf>).
Yuster's presentation of Haxell--Rodl states that for each fixed packed graph
`H`, `nu*_H(G)-nu_H(G)=o(n^2)` uniformly over `n`-vertex host graphs
(<https://math.haifa.ac.il/raphy/papers/fracpack.pdf>). The target uses only
the triangle specialization with a fixed positive accuracy. Finite LP duality
and the perfect-elimination characterization of chordal graphs are standard
additional inputs.

The exact audits guarantee their finite enumerations, rational feasibility,
objectives, and displayed scalar arithmetic. They do not prove the
Haxell--Rodl theorem, compute its modulus, or turn the existential thresholds
into practical numbers. They also do not replace the human universal proof.
There is no floating-point premise, random sampling, external solver,
downloaded dataset, or omitted bulk certificate.

## Literature status, novelty, and publication readiness

The zero/unit framework is prior work of Yuster, and the target correctly
attributes it. Known nearby results include the asymptotic dense-graph
inequality and its limitations, the minimum-degree split theorem of Chahua
and Gutierrez (<https://arxiv.org/abs/2405.11409>), the threshold-graph
theorem of Bonamy et al. (<https://dmtcs.episciences.org/9916/pdf>), and the
`K8`-free chordal result of Botler, Fernandes, and Gutierrez
(<https://arxiv.org/abs/2002.07925>). Baron and Kahn show that ratio two can
remain asymptotically tight in general positive-density graphs
(<https://arxiv.org/abs/1408.4870>), so chordality is a meaningful structural
hypothesis rather than cosmetic strengthening.

Targeted searches for the elimination inequality, an every-fixed-density
chordal strict gap, and the fixed-neighborhood-type split corollary found no
matching theorem. These results therefore appear new relative to the
inspected primary literature. This is a bounded search assessment, not proof
of historical priority. The mathematics is publication-ready as an
existential asymptotic theorem, provided the ineffective nature of the
Haxell--Rodl thresholds remains explicit.

## Remaining gaps

- The thresholds `N_beta` and `K_r` depend on an unevaluated Haxell--Rodl
  modulus. The result proves existence but supplies no usable cutoff or finite
  completion for unrestricted three-type split graphs.
- The universal proof and its LP-complementarity bridge are not formalized in
  a proof assistant.
- The independent exhaustive computation stops at order six. Its positive
  large-order controls test the arithmetic, not every chordal or bounded-type
  graph in the asymptotic regime.
- Correctness still depends on the two classical external theorems and finite
  LP duality.
- The targeted novelty search cannot establish absolute literature priority.

These are explicit effectiveness and assurance limits, not defects in the
stated theorem.

## Strengthening and improvement opportunities

1. **Replace asymptotic rounding by a class-specific integral construction.**
   This is the highest-impact next step. A direct packing argument exploiting
   elimination cliques, or a quantitative rounding theorem specialized to
   capped bounded-type split graphs, would make `N_beta` or `K_r` explicit.
   For `r=3`, an effective cutoff would reduce the unresolved theorem to a
   genuinely finite and potentially checkable range.
2. **Optimize the fractional constants.** The choices `1/50` and the bound
   `1+sqrt(2h)` are deliberately coarse. Retaining the exact quadratic root
   from `binom(d_v,2)<=h` and optimizing the intersection of the `h` and `z`
   bounds gives a concrete one-variable semialgebraic problem. A rational
   certificate for its minimum could improve both the density margin and the
   eventual ratio without changing the structural proof.
3. **Retain neighborhood-size data in the bounded-type estimate.** The steps
   `p^2<=rE` and a single global `L` discard the individual `s_i` and
   multiplicities. A weighted optimization over the type profile could yield
   stronger margins for balanced, laminar, or nearly co-sunflower systems and
   may expose explicit subclasses where no asymptotic rounding is needed.
4. **Classify equality and near-equality in the elimination bound.** The proof
   allows extensive overlap among forced unit cliques. Understanding when
   `z` approaches `n(1+sqrt(2h))` could either sharpen the theorem or identify
   extremal chordal constructions governing the best possible constant.
5. **Formalize the universal core.** The LP deletion argument, elimination
   lemma, and scalar rearrangements are compact enough for proof-assistant
   formalization. The Haxell--Rodl theorem could remain an explicit imported
   axiom while the new structural content and all constant calculations are
   machine checked.

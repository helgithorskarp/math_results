# Independent acceptance: universal averaged Gaussian replica-rank gap

27 September 2026. **Accept for correctness in the stated scope.** This
reviews graph6436,
`bafkreigqhx3wp5rxeobajbaohsyitdjtmmxstmfovnrh4iradqfwrlvdoi`, at exact
source commit `5a2b55eca217a7fd7a0d035757eb29124bd5a204`. The material target files
and the endpoint Hankel normalization are content-pinned in
[TARGET_INPUTS.json](TARGET_INPUTS.json).

The result supplies a genuine universal strict improvement over the naive
rank-six conditional Gaussian constant after averaging the actual contraction
graph and interpolation clock. It is an intermediate global inequality. It
does **not** prove the first unrestricted Hankel sign, a new beta sign, full
dimension-three Gaussian majorisation, or a new Kneser--Poulsen class.
Historical priority for this averaged mechanism was not exhaustively audited.

## Accepted statement and exact limitation

For a bounded probability law `mu` on `R^3`, a 1-Lipschitz map `T` on its
support, and `s>0`, let independent replicas satisfy

```text
delta_ij=|X_i-X_j|^2-|T(X_i)-T(X_j)|^2 >= 0,
Z_i(t)=(sqrt(1-t)X_i,sqrt(t)T(X_i)),
Q_m(t)=sum_i |Z_i(t)-mean_m Z(t)|^2,
B_m=E delta_12 integral_0^1 exp(-Q_m(t)/(2s))dt.
```

For four labels put

```text
Q_D=d_12/6+(d_13+d_14+d_23+d_24)/3,
I_D=E delta_12 integral_0^1 exp(-Q_D(t)/(2s))dt.
```

There is one universal constant

```text
eta=(5/13) min(e_graph,1/216)>0
```

such that every permitted input satisfies

```text
B4 >= (8/9)^3(1+eta) I_D,
B2 B4 >= (8/9)^3(1+eta) B3^2.
```

Here `e_graph` is the non-effective positive separation constant audited
below. It is independent of the law, support radius, map, variance, atom
count, masses, covariance, and mean loss.

The endpoint moments are `a_j=B_(j+2)/[4s(j+2)^(5/2)]`, so their first
Hankel sign requires

```text
B2 B4 >= (8/9)^(5/2) B3^2.
```

The proved coefficient reaches that threshold only if
`1+eta>=sqrt(9/8)`. But `eta<=5/2808` and
`(1+5/2808)^2<9/8`. The target correctly advertises no unrestricted sign
or majorisation consequence.

## Replica geometry and Gaussian completion

Fix the base pair and time, write `b=(Z1+Z2)/2`, and let `V,V'` be the two
new displacements. Direct centering gives

```text
Q_D=Q2+(2/3)(|V|^2+|V'|^2),
Q4=Q2+(3/4)(|V|^2+|V'|^2)-(1/2)V.V'.
```

After tilting by `exp(-|V|^2/(3s))` and scaling
`W=sqrt(2/(3s))V`, the residual kernel is

```text
K(w,w')=exp[-(|w|^2+|w'|^2)/16+3w.w'/8].
```

If `P_nu` is the law of `W/sqrt(3)+sqrt(2/3)G`, completing the square in
the product of two shifted Gaussian densities gives self coefficient
`-1/16`, cross coefficient `3/8`, and six-dimensional prefactor
`(9/8)^3`. Hence

```text
E K(W,W')=(8/9)^3[1+chi^2(P_nu||gamma_6)].
```

No sign-changing series is used. The clean-room checker verifies this as
an exact formal exponential identity on three distinct finite mixtures,
without evaluating transcendental numbers.

Writing `dw=delta_12 exp(-Q2/(2s))dt dmu^2`, conditional integration gives

```text
B2=int dw,   B3=int r dw,   I_D=int r^2 dw.
```

Thus Cauchy--Schwarz gives `B3^2<=B2 I_D`. For `I_D>0`, the probability
measure `dOmega=r^2dw/I_D` satisfies the exact identity

```text
B4/I_D=(8/9)^3[1+E_Omega e(nu)].
```

The checker reconstructs all centering and diamond identities on a different
six-site linear contraction: 1,296 ordered quadruples, 10,368 centering
checks, 2,592 nonnegative-loss checks, and 92 exact marked-pair
symmetrization cells.

## Positive separation from full six-dimensional Gaussian rank

Define `e_graph` as the infimum of `e(nu)=chi^2(P_nu||gamma_6)` over
probability laws supported on graphs of globally 2-Lipschitz maps
`R^3->R^3`. A point law shows finiteness. Strict positivity follows by a
sound compactness contradiction:

1. If `e(nu_k)->0`, Cauchy--Schwarz gives total-variation convergence
   `P_nu_k->gamma_6`.
2. The exact characteristic-function inversion

   ```text
   nu_hat_k(xi)=exp(|xi|^2) (P_nu_k)_hat(sqrt(3)xi)
   ```

   converges to `exp(-|xi|^2/2)`. Lévy continuity therefore gives
   `nu_k=>gamma_6`, including tightness.
3. A fixed Gaussian continuity ball of positive mass intersects each graph
   eventually. Its points bound the graph offsets `F_k(0)`. The common
   Lipschitz bound and Arzelà--Ascoli give a locally uniform subsequential
   limit `F`.
4. Every sufficiently small open ball outside the closed graph of `F` is
   eventually disjoint from the graphs of `F_k`. The open-set Portmanteau
   inequality makes its Gaussian mass zero. A countable cover would place
   `gamma_6` on the graph of `F`, which has six-dimensional Lebesgue measure
   zero by Fubini—a contradiction.

This proves `0<e_graph<infinity`; it does not compute it. For the actual
conditional law, the last three coordinates are a function of the first
three with Lipschitz constant at most `sqrt(t/(1-t))`. Kirszbraun extension
handles maps initially defined only on the support. Therefore

```text
e(nu)<e_graph  implies  t>4/5.
```

The checker independently validates the squared graph inequality in 144
exact conditional-support comparisons, including the boundary `t=4/5`.

## Moment control and the marked interpolation clock

Writing `W=(A,B)`, the Ornstein--Uhlenbeck second-moment identity and
Cauchy--Schwarz against the `chi^2` density give

```text
|E_nu|A|^2-3| <= sqrt(54e),
|E_nu|B|^2-3| <= sqrt(54e).
```

Thus `e<1/216` implies `E|A|^2>5/2` and `E|B|^2<7/2`.

Under the full four-replica marked law, let
`L_D=Q_D(0)-Q_D(1)>=0` and `U=(1-t)L_D/(2s)`. Conditional on a tuple with
`a=L_D/(2s)>0`, `U` has density

```text
exp(-u)/(1-exp(-a)),   0<=u<=a.
```

It is an `Exp(1)` variable conditioned to be at most `a`, so `EU<=1`.
Conditioning instead on the base pair and time gives exactly

```text
E[U|base,t]
 =(1-t)delta_12/(4s)+E|A|^2-((1-t)/t)E|B|^2 >=0.
```

The nonnegativity comes from the original nonnegative diamond loss, not
from estimating the signed terms separately. The checker verifies 10,368
pointwise versions of this clock identity on its independent fixture.

Let `e0=min(e_graph,1/216)`. On `e<e0`, the graph implication gives
`(1-t)/t<1/4`, while the moment bounds yield

```text
E[U|base,t] >= 5/2-(1/4)(7/2)=13/8.
```

Everywhere else this conditional mean remains nonnegative. Since `EU<=1`,
the good event has probability at most `8/13`; hence its complement has
probability at least `5/13` and

```text
E_Omega e(nu) >= (5/13)e0.
```

This is precisely the claimed `eta`. If `I_D=0`, positivity of all Gaussian
weights forces `delta_12=0` almost everywhere, and all marked `B_m` vanish.

## Reproduction, trust boundary, and novelty

The exact target commit's checker passes in normal and optimized Python,
with all six source hashes valid and expected-record SHA-256
`6a210d31b2b5fe4d7c0f523f431b2123a4a127f694ab6bf10a466b114b612df8`.
The independent checker imports no target code and has canonical record
SHA-256
`2d8a891721751f0df236fe16cb252ac8b2f037fd7389f7a0cd7b44c87b360b3c`.

The code guarantees the pinned bytes and exact Gaussian-completion,
centering, graph-support, marked-clock, symmetrization, and constant
interfaces. The universal graph-separation lemma, characteristic-function
limit, Portmanteau step, and measure-theoretic conditioning remain reviewed
written mathematics; they are not proof-assistant formalized. No numerical
value of `e_graph`, numerical quadrature, solver, hidden dataset, or omitted
large certificate is used.

The primary problem paper proves full preservation only through dimension
two and partial higher-dimensional results. The present global averaged gap
is compatible with the previously recorded pointwise kernel obstructions,
because it keeps both the actual graph relation and marked time law. Its
historical novelty is uncertain, and the missing quantitative jump to the
first Hankel coefficient remains open.

Reproduce with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_AVERAGED_REPLICA_RANK_GAP_REVIEW_PASS`.

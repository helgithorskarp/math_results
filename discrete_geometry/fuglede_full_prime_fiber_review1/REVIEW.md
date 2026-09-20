# Independent review report

## Verdict

**Accept with high confidence.** Let `p` be prime, `gcd(n,p)=1`, and assume
that `Z/nZ` has no spectral subset of cardinality `p`. If a `2p`-point subset
of `Z/nZ x Z/pZ` contains a full vertical fiber, then after translating that
fiber to first coordinate zero it is spectral exactly when its residual set
has one point `(a_j,j)` on every level and all `a_j` have a common 2-adic
valuation `t<v_2(n)`. The displayed spectrum and complement work, and the
`(n,p)=(210,11)` consequence is valid.

This is a correctness verdict only. A bounded literature check found the
claimed dependencies and scope but cannot establish that the combined normal
form is historically new.

## Human premises and completeness reductions

The proof depends on the following reductions. Program agreement is only
corroboration; items 1--10 are the universal argument.

1. **Square spectral matrices have row/column duality.** A spectrum gives a
   square character matrix whose columns are orthogonal with equal norm.
   Therefore its rows are orthogonal with the same norm. No unproved symmetry
   of arbitrary rectangular Fourier submatrices is used.

2. **A full fiber forces two frequencies per level.** Orthogonality of the
   `p` rows `(0,s)` says that every nonconstant Fourier coefficient of the
   spectrum's second-coordinate multiplicity function vanishes. Fourier
   inversion on `Z/pZ`, together with total mass `2p`, makes every frequency
   level have exactly two points `{b_j,c_j}`.

3. **Fiber deletion is complete, not averaged.** For a residual point
   `(a,r)`, orthogonality against every one of the `p` fiber rows gives all
   Fourier coefficients of
   `zeta_p^(rj)(zeta_n^(a b_j)+zeta_n^(a c_j))`. Inversion forces
   `zeta_n^(a(c_j-b_j))=-1` separately for every `j`. Dividing the identities
   for two residual rows makes their two contributions on each level equal,
   so any one-per-level choice from the spectrum is a spectrum of the
   residual `p`-set.

4. **Graph-spectrum dichotomy.** For a residual spectral pair with frequency
   graph `{(b_j,j)}`, two points on distinct levels yield a degree at most
   `p-1` relation for `zeta_p` over `Q(zeta_n)`. Coprimality gives extension
   degree `phi(np)/phi(n)=p-1`, so the relation is a multiple of `Phi_p` and
   all coefficients agree. Their first-coordinate difference lies in the
   common kernel of the characters `b_j-b_0`.

5. **The dichotomy exhausts the level profiles.** If at least two levels are
   occupied, an opposite-level point shows that same-level differences lie in
   the same kernel; two points on one level would then have nonzero row inner
   product. Thus there is exactly one point per level. If only one level is
   occupied, removing its constant column phases gives a `p`-point spectral
   subset of `Z/nZ`; repeated `b_j` would make columns proportional.

6. **The base hypothesis is used exactly once.** It excludes the one-level
   branch of the dichotomy. The theorem does not assert this local hypothesis
   for every coprime pair. In the `210,11` application it follows from the
   published four-prime Fuglede theorem and the fact that a tile's cardinality
   divides the group order.

7. **Binary valuation is forced.** Choosing one frequency level gives
   `delta*a_j = n/2 mod n` for every residual point. Hence `n` is even. If
   `n=2^s m` with `m` odd, reduction modulo `2^s` forces
   `v_2(delta)<s` and `v_2(a_j)=s-1-v_2(delta)`, independently of `j`.
   The valuation of a nonzero residue below `s` is invariant under changing
   its integer representative modulo `n`.

8. **The displayed spectrum is sufficient.** For common residual valuation
   `t<s`, `delta_t=n/2^(t+1)` satisfies
   `zeta_n^(delta_t a_j)=-1`. Frequency pairs with different first
   coordinates cancel level by level; pairs with equal first coordinate and
   different second coordinate vanish by the nontrivial Fourier sum on
   `Z/pZ`. These are all frequency pairs.

9. **The displayed complement tiles uniquely.** Its first coordinates are
   the inverse image of the first half of `Z/(2^(t+1))`. Adding any `a_j` of
   valuation `t` exchanges the two halves, so on each level `{0,a_j}` plus
   the complement partitions `Z/nZ` uniquely. Translation of the original
   full fiber preserves both spectrality and this tiling.

10. **The cyclic specialization is correctly transported.** For `n=210`,
    `v_2(n)=1`, so the residual coordinates are precisely the odd residues.
    Under CRT the complement is `22 Z/2310Z`, and its annihilator
    `105 Z/2310Z` is a common spectrum. Thus only the family containing a full
    order-11 coset is settled; a hypothetical counterexample must avoid every
    such coset.

## Independent computation

[`independent_check.py`](independent_check.py) uses a different exact zero
test. If `S=sum_i zeta_N^(e_i)`, then

```text
Tr(S conjugate(S)) = sum_(i,j) c_N(e_i-e_j)
                    = sum_(a in (Z/NZ)^*) |sum_i zeta_N^(a e_i)|^2,
```

where `c_N` is the integer Ramanujan sum. The right side is a sum of
nonnegative conjugate squared magnitudes and includes the identity conjugate,
so it is zero exactly when `S=0`. This avoids floating point and does not use
cyclotomic-polynomial division.

For five smallest complete coprime cases the checker enumerates every
full-fiber candidate and every frequency set translated to contain zero—371
sets in total, not a clique search. It finds exactly ten spectral sets. In the
nontrivial `(4,3)` case it finds nine spectral sets carrying 46 normalized
spectra and verifies all 368 one-frequency-per-level deletion selections,
rather than checking only one found spectrum per positive set.

It separately checks all 14,375 small graph-spectrum pairs and obtains 713
spectral pairs, all with an allowed level profile. It exhausts 4,724 solutions
of `delta*a=n/2 mod n` and 1,582 binary half-translate partitions through
`n=96`. Exact fixtures cover two different valuations at `n=8` and `n=12`
and the claimed `(210,11)` spectrum and complement.

Adversarial controls include:

* odd `n` in the smallest full censuses;
* a residual set with mixed binary valuations;
* a residual set with a repeated level and a missing level;
* the excluded boundary `t=v_2(n)`;
* the target's spectral noncoprime `(3,3)` graph with level profile `(2,1,0)`.

The last control shows that the coprimality premise is material. The target's
own deterministic checker also passed, reproducing 4,890 full-fiber sets,
14,375 dichotomy candidates, 1,720 deletion selections, and its explicit
tilings in about one second.

## Sources, scope, and trust boundary

The published Kiss--Malikiosis--Somlai--Vizer Theorem 1.4 states Fuglede's
conjecture for cyclic order `pqrs` with four distinct primes, exactly supplying
spectral-to-tiling in `Z/210Z`. The current Somlai manuscript confirms that
general finite cyclic Fuglede remains open and that the available inductive
large-prime theorem requires `p>n`, which does not cover `11<210`.

The general theorem otherwise uses elementary finite Fourier inversion,
cyclotomic field degree, and modular arithmetic. It does not import the
earlier cuboid lemma. The universal proof is human-audited, not formalized in
a proof assistant. The finite censuses test indexing, exceptional premises,
and completeness reductions, but do not enumerate arbitrary `2p`-sets or all
22-point subsets of `Z/2310Z`.

Primary links and the exact literature boundary are recorded in
[`SOURCES.md`](SOURCES.md).
